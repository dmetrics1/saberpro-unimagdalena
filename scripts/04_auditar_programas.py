"""Auditoria de programas: contrasta el JSON maestro contra las bases del Icfes.

Reconstruye de forma independiente (directo del Excel/cache del Icfes) cada
valor por programa y año y lo compara con data/processed/datos_informe.json:

  1. NBC asignado en parametros.yml vs ID_NBC que reporta el Icfes cada año.
  2. Puntaje global y competencias genéricas del programa (radar_historico).
  3. Referencia NBC nacional (global, competencias y n) usada en el radar.
  4. Pruebas específicas del programa y de su NBC (especificas_historico).
  5. Programas del yml que no aparecen en el JSON y viceversa.

Sale con código 1 si encuentra errores, para detener el pipeline antes de
publicar datos inconsistentes.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import polars as pl

import lib_saberpro as sp

# ID_NBC que el Icfes usa para programas aún no clasificados: solo advertencia
NBC_SIN_CLASIFICAR = 99
TOLERANCIA = 0.5


def _int(v):
    n = sp.safe_num(v)
    return int(n) if n is not None else None


def cargar_icfes(agregados_dir, norm_mapping, renombres):
    """Devuelve {anio: {prog_clean: {...}}} y {anio: {nbc_id: {prueba|GLOBAL: (puntaje, n)}}}."""
    programas, nbcs = {}, {}
    for cache in sorted(agregados_dir.glob("*.cache.parquet")):
        anio = int(re.search(r"20\d{2}", cache.name).group())
        df = pl.read_parquet(cache).filter(
            pl.col("MEDIDA_AGREGACION").is_in(["PUNTAJE_GLOBAL", "PUNTAJE_PRUEBA"])
        )
        progs_anio = defaultdict(dict)  # prog_clean -> id_icfes -> registro
        nbcs_anio = defaultdict(dict)
        for r in df.iter_rows(named=True):
            agreg = sp.clean_text(r["AGREGACION"])
            medida = sp.clean_text(r["MEDIDA_AGREGACION"])
            es_global = medida == "PUNTAJE_GLOBAL"
            prueba = "GLOBAL" if es_global else sp.clean_text(r["NOMBRE_PRUEBA"])
            puntaje = sp.safe_num(r["PROMEDIO_GLOBAL" if es_global else "PROMEDIO_PRUEBA"])
            n = _int(r["CANTIDADEVALUADOS"])
            if puntaje is None or not prueba:
                continue

            if agreg == "NBC":
                nbc_id = _int(r["ID_NBC"])
                if nbc_id is not None:
                    nbcs_anio[nbc_id][prueba] = (puntaje, n)
                continue

            if agreg != "PROGRAMA_ACADEMICO":
                continue
            if sp.normalize_ies_name(r["NOMBRE_INSTITUCION"], "agregados", norm_mapping) != "UNIVERSIDAD DEL MAGDALENA":
                continue
            id_icfes = _int(r["ID_PROGRAMA_ACAD"])
            nombre = renombres.get(id_icfes, r["NOMBRE_PROGRAMA_ACAD"])
            reg = progs_anio[sp.clean_text(nombre)].setdefault(
                id_icfes, {"nbc_id": _int(r["ID_NBC"]), "nbc_nombre": r["NBC"], "pruebas": {}}
            )
            reg["pruebas"][prueba] = (puntaje, n)

        # Con varios ID para el mismo nombre, el pipeline conserva el de mayor n
        programas[anio] = {
            prog: max(regs.values(), key=lambda x: (x["pruebas"].get("GLOBAL") or (0, 0))[1] or 0)
            for prog, regs in progs_anio.items()
        }
        nbcs[anio] = dict(nbcs_anio)
    return programas, nbcs


def main() -> None:
    params = sp.load_params()
    agregados_dir = sp.PROJECT_ROOT / params["agregados_dir"]
    # Opcional: auditar otro JSON (p. ej. el publicado) pasándolo como argumento
    json_path = Path(sys.argv[1]) if len(sys.argv) > 1 else sp.PROJECT_ROOT / params["output_json"]
    renombres = {int(k): v for k, v in (params.get("programas_por_id_icfes") or {}).items()}
    excluidos = {sp.clean_text(x) for x in (params.get("programas_excluidos") or [])}
    yml = {
        sp.clean_text(p["nombre"]): p
        for p in params["programas_unimagdalena"]
        if sp.clean_text(p["nombre"]) not in excluidos
    }

    print("-------------------------------------------------------")
    print("Auditando programas del JSON maestro contra las bases del Icfes...")
    icfes_prog, icfes_nbc = cargar_icfes(agregados_dir, sp.load_normalization(), renombres)
    datos = json.loads(json_path.read_text(encoding="utf-8"))
    json_progs = {sp.clean_text(p["programa"]): p for p in datos["programas"]}

    errores, avisos = [], []
    revisados = 0

    def comparar(contexto, esperado, obtenido):
        nonlocal revisados
        revisados += 1
        if esperado is None and obtenido is None:
            return
        if esperado is None or obtenido is None or abs(esperado - obtenido) > TOLERANCIA:
            errores.append(f"{contexto}: JSON={obtenido} Icfes={esperado}")

    for prog in sorted(set(yml) - set(json_progs)):
        avisos.append(f"{prog}: está en parametros.yml pero no en el JSON")
    for prog in sorted(set(json_progs) - set(yml)):
        errores.append(f"{prog}: está en el JSON pero no en parametros.yml")

    for prog, p in sorted(json_progs.items()):
        cfg = yml.get(prog)
        if cfg is None:
            continue
        nbc_cfg = cfg["nbc_id"]

        # 1. NBC configurado vs NBC del Icfes en cada año con datos
        for anio, progs_anio in sorted(icfes_prog.items()):
            reg = progs_anio.get(prog)
            if reg is None or reg["nbc_id"] == nbc_cfg:
                continue
            msg = (f"{prog} [{anio}]: NBC en yml={nbc_cfg} ({cfg['nbc_nombre']}) "
                   f"pero el Icfes lo clasifica en {reg['nbc_id']} ({reg['nbc_nombre']})")
            (avisos if reg["nbc_id"] == NBC_SIN_CLASIFICAR else errores).append(msg)

        # 2-3. Radar por año: programa y referencia NBC nacional
        for anio_s, h in (p.get("radar_historico") or {}).items():
            anio = int(anio_s)
            reg = icfes_prog.get(anio, {}).get(prog)
            ref = icfes_nbc.get(anio, {}).get(nbc_cfg, {})
            if reg is None:
                errores.append(f"{prog} [{anio}]: hay radar en el JSON pero el Icfes no reporta el programa")
                continue
            ctx = f"{prog} [{anio}]"
            comparar(f"{ctx} global programa", (reg["pruebas"].get("GLOBAL") or (None,))[0], h.get("global_programa"))
            comparar(f"{ctx} n programa", (reg["pruebas"].get("GLOBAL") or (None, None))[1], h.get("n_programa"))
            if "global_nbc_nacional" in h:
                comparar(f"{ctx} global NBC", (ref.get("GLOBAL") or (None,))[0], h.get("global_nbc_nacional"))
                comparar(f"{ctx} n NBC", (ref.get("GLOBAL") or (None, None))[1], h.get("n_nbc_nacional"))
            for c in h.get("competencias", []):
                prueba = sp.clean_text(c["competencia"])
                comparar(f"{ctx} {prueba} programa", (reg["pruebas"].get(prueba) or (None,))[0], c.get("puntaje_programa"))
                comparar(f"{ctx} {prueba} NBC", (ref.get(prueba) or (None,))[0], c.get("puntaje_nbc_nacional"))

        # 4. Específicas por año
        for anio_s, items in (p.get("especificas_historico") or {}).items():
            anio = int(anio_s)
            reg = icfes_prog.get(anio, {}).get(prog) or {"pruebas": {}}
            ref = icfes_nbc.get(anio, {}).get(nbc_cfg, {})
            for e in items:
                prueba = sp.clean_text(e["prueba"])
                ctx = f"{prog} [{anio}] específica {prueba}"
                comparar(f"{ctx} programa", (reg["pruebas"].get(prueba) or (None,))[0], e.get("puntaje_programa"))
                if e.get("puntaje_nbc_nacional") is not None or prueba in ref:
                    comparar(f"{ctx} NBC", (ref.get(prueba) or (None,))[0], e.get("puntaje_nbc_nacional"))

        # Bloque 2025 (KPI de portada y comparativos del año vigente)
        anio_v = params["anio_vigente"]
        h = (p.get("radar_historico") or {}).get(str(anio_v)) or {}
        if h:
            comparar(f"{prog} [{anio_v}] global_2025", h.get("global_programa"), p.get("global_2025"))
            comparar(f"{prog} [{anio_v}] global_nbc_nacional_2025", h.get("global_nbc_nacional"), p.get("global_nbc_nacional_2025"))

    print(f"Programas auditados: {len(json_progs)} | comparaciones: {revisados}")
    for a in avisos:
        print(f"  AVISO: {a}")
    if errores:
        print(f"\n{len(errores)} ERRORES:")
        for e in errores:
            print(f"  ERROR: {e}")
        print("-------------------------------------------------------")
        sys.exit(1)
    print("Auditoría OK: el JSON coincide con las bases del Icfes.")
    print("-------------------------------------------------------")


if __name__ == "__main__":
    main()
