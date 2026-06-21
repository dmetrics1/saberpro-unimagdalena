# Informe Institucional Saber Pro — Universidad del Magdalena

[![Python](https://img.shields.io/badge/Python-2563EB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-7C3AED?style=flat-square&logo=javascript&logoColor=white)](https://developer.mozilla.org/docs/Web/JavaScript)
[![Pandas](https://img.shields.io/badge/pandas-06B6D4?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Estado](https://img.shields.io/badge/Estado-En%20producción-10B981?style=flat-square)]()
[![Uso](https://img.shields.io/badge/Uso-Institucional-9CA3AF?style=flat-square)]()

**Pipeline de datos en Python + informe institucional interactivo en HTML/JS** sobre los resultados **Saber Pro** de la Universidad del Magdalena: puntajes institucionales, competencias genéricas, cuadrantes Saber 11 → Saber Pro, valor agregado, SUE y comparativos por facultad y programa.

---

Proyecto para procesar resultados Saber Pro y construir un informe institucional interactivo de la Universidad del Magdalena. El flujo separa el procesamiento pesado en Python de la visualización en HTML:

```text
datos crudos -> scripts Python -> data/processed/datos_informe.json -> informe HTML
```

El informe final está en [informe/informe/index.html](./informe/informe/index.html) y debe abrirse desde un servidor local para que el navegador pueda cargar el JSON.

## 📸 Vista previa

<table>
  <tr>
    <td width="60%"><img src="resultados/cuadrantes_saber11_saberpro_2024.png" alt="Cuadrantes Saber 11 → Saber Pro 2024" /></td>
    <td width="40%"><img src="resultados/trayectoria_unimagdalena_2020_2024.png" alt="Trayectoria de valor agregado de la Universidad del Magdalena 2020-2024" /></td>
  </tr>
</table>

<sub>Salidas analíticas del pipeline: cuadrantes de valor agregado (Saber 11 → Saber Pro) y trayectoria institucional. El informe interactivo completo (12 visualizaciones) se sirve desde <code>informe/informe/index.html</code>.</sub>

> _Para máximo impacto, agrega también una captura del informe HTML interactivo en ejecución._

## Estado actual

- Pipeline de datos implementado: cuadrantes, agregados y JSON maestro.
- Informe HTML implementado con visualizaciones interactivas en JavaScript puro.
- Año vigente configurado: 2025.
- Datos agregados Saber Pro disponibles: 2020-2025.
- Base de cruce Saber 11 - Saber Pro disponible: 2018-2024.
- Cuadrantes y trayectoria de valor agregado se muestran de 2020 a 2024 (el JSON conserva 2018-2019 pero el front los filtra por n bajo).

## Estructura

```text
proyecto_informe_saberpro/
├── data/
│   ├── Perfiles_INBC_Anuales_2016_2024.parquet
│   ├── saberpro_agregados/
│   │   └── Base-de-datos-de-resultados-agregados-de-saber-pro-2020..2025.xlsx
│   ├── config/
│   │   ├── parametros.yml
│   │   └── normalizacion_ies.csv
│   └── processed/
│       ├── cuadrantes_procesados.json
│       ├── agregados_procesados.json
│       └── datos_informe.json
├── docs/
│   ├── README.md
│   ├── guia_operativa.md
│   ├── diccionario_json.md
│   ├── plan_maestro.md
│   ├── etapa2.md
│   └── etapa3.md
├── informe/
│   ├── README.md
│   ├── abrir_informe.bat
│   ├── abrir_informe.sh
│   ├── docs/             # solo stubs de redirección a docs/
│   └── informe/
│       ├── index.html
│       ├── assets/css/tokens.css
│       ├── assets/js/app.js
│       └── data/datos_informe.json
├── scripts/
│   ├── lib_saberpro.py
│   ├── 01_construir_cuadrantes.py
│   ├── 02_construir_agregados.py
│   ├── 03_consolidar_json.py
│   ├── 16_generar_graficos_cuadrantes_2022_2024.py
│   └── 17_generar_grafico_trayectoria_unimagdalena.py
├── resultados/           # gráficos estáticos opcionales (scripts 16 y 17)
├── requirements.txt
└── ejecutar_proyecto.bat
```

## Cómo ejecutar el pipeline de datos

Opción recomendada en Windows:

```powershell
.\ejecutar_proyecto.bat
```

Ese script crea o activa `venv`, instala dependencias, ejecuta los scripts 01-03 y copia el JSON maestro al informe HTML.

Para detalles del flujo, ejecución manual, instalación inicial y actualización con un año nuevo, ver la [guía operativa](./docs/guia_operativa.md).

## Cómo ver el informe

En Windows:

```powershell
.\informe\abrir_informe.bat
```

O manualmente:

```powershell
cd informe\informe
python -m http.server 8000
```

Luego abrir:

```text
http://localhost:8000
```

## Documentación

- [Índice de documentación](./docs/README.md)
- [Guía operativa](./docs/guia_operativa.md)
- [Diccionario del JSON maestro](./docs/diccionario_json.md)
- [Plan maestro](./docs/plan_maestro.md)
- [Arquitectura narrativa](./docs/etapa2.md)
- [Catálogo de visualizaciones](./docs/etapa3.md) — incluye la tabla canónica de las 12 visualizaciones del informe.

## Regla metodológica central

El proyecto usa dos fuentes con universos distintos. La nomenclatura **Fuente A / Fuente B** es la canónica y está fijada en `meta.convencion_n` del JSON maestro:

- **Fuente A** — Base de cruce Saber 11 - Saber Pro: se usa solo para cuadrantes, trayectoria y valor agregado. La medida de n es `crossed_n` con umbral mínimo 25.
- **Fuente B** — Bases agregadas oficiales Saber Pro: se usan para puntajes institucionales, competencias, SUE, departamentos, facultades, programas, Top 10 y niveles de desempeño. La medida de n es `CANTIDADEVALUADOS`.

No se deben mezclar los n de ambas fuentes en una misma lectura.

---

## 📄 Datos

Proyecto **institucional de la Universidad del Magdalena**. Los datos de Saber Pro y Saber 11 provienen del **ICFES** — resultados agregados oficiales de **acceso público**.

## 👤 Autor

Desarrollado por **Daniel Molina Barrios** — Economista & Data Scientist · Universidad del Magdalena.

[![GitHub](https://img.shields.io/badge/GitHub-2563EB?style=flat-square&logo=github&logoColor=white)](https://github.com/dmetrics1)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-7C3AED?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/daniel-molina-b76a4323b/)
