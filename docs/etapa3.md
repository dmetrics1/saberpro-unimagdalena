# ETAPA 3 — Catálogo de Visualizaciones
## Informe Institucional Saber Pro · Universidad del Magdalena

Catálogo completo de gráficos del informe, diseñado sobre los **campos reales** del
`datos_informe.json` generado en la Etapa 1. Cada visualización indica: sección, tipo,
campos del JSON que consume, mensaje principal, decisión que habilita, por qué se
prefiere a otras alternativas y prioridad (**Esencial / Recomendado / Opcional**).

**Convención de color (fija):** azul `#0183EF` = Unimagdalena / UNIMAGDALENA · naranja `#FF9400` =
referencia (nacional/NBC) · verde `#00A50B` = sobre la media · rojo `#D10500` = bajo
la media · primario `#004A87` = estructura.

**Principio anti-redundancia:** la presentación actual repite ~70 gráficos (uno por
programa). Aquí se sustituyen por **un único componente filtrable** (G9).

---

## Decisiones finales aprobadas (registro)

1. **Rango temporal por tipo de análisis:**
   - **Cuadrantes y trayectoria (G6, G7): 2020–2024.** Se excluyen 2018 y 2019 por su
     n muy bajo (≈30 estudiantes) y poca representatividad. La base de cruce no tiene
     2025, por eso el tope es 2024.
   - **Todo lo demás (G2, G3, G4, G5, G8, G9, G10, G11): 2020–2025.**
   - El JSON conserva 2018–2019 en `cuadrantes_por_anio` y `trayectoria_unimag`; el
     filtro "desde 2020" se aplica en el **front-end** (no se regenera el JSON).

2. **Regeneración total desde el JSON:** los 12 gráficos se construyen desde
   `datos_informe.json` con la identidad visual azul institucional y de forma
   interactiva. El PowerPoint queda solo como **referencia de contenido y estilo**; no
   se copian ni incrustan sus imágenes (que usan la paleta verde antigua y son
   estáticas).

---

## Resumen del catálogo

| ID | Sección | Gráfico | Tipo | Prioridad |
|----|---------|---------|------|-----------|
| G1 | 1 | Tarjetas KPI ejecutivas | KPI cards | Esencial |
| G2 | 2 | Radar competencias UM vs. nacional (6 ejes, filtrable por año) | Radar | Esencial |
| G3 | 2 | Evolución histórica global UM vs. nacional | Línea suave | Esencial |
| G4 | 3 | Ranking SUE (filtrable por año) | Barras verticales | Esencial |
| G5 | 3 | Comparativo con universidades del Departamento (filtrable por año) | Barras agrupadas | Esencial |
| G6 | 4 | Cuadrantes de valor agregado (filtrable por año) | Dispersión | Esencial |
| G7 | 4 | Trayectoria histórica de Unimagdalena | Recorrido temporal | Esencial |
| G8 | 5 | Desempeño por facultad (filtrable por año y competencia) | Barras horizontales | Esencial |
| G9 | 6 | Explorador de programas (componente filtrable) | Compuesto | Esencial |
| G10 | 7 | Top 10 por competencia | Barras horizontales | Recomendado |
| G11 | 7 | Niveles de desempeño institucional | Barras apiladas 100% | Recomendado |
| G12 | 5 | Mapa de calor competencias × facultad (filtrable por año) | Heatmap | Esencial |

---

## SECCIÓN 1 — Hero + KPIs

### G1 · Tarjetas KPI ejecutivas — **Esencial**
- **Tipo:** 3 tarjetas KPI con icono, tag de categoría, número grande y etiqueta. Embebidas sobre la franja inferior del hero azul (efecto incrustado).
- **Datos:**
  - **Desempeño** — `institucional.global.puntaje_unimag` (150).
  - **Posicionamiento** — `programas` (% que supera el promedio de su NBC: 23/39 = 59%, con sub-línea "23 de 39 programas").
  - **Cobertura** — `institucional.global.n_unimag` (2 982 evaluados).
- **Mensaje:** "Estado de la universidad de un vistazo en tres lecturas: cómo nos desempeñamos, cómo nos posicionamos, a quiénes representamos."
- **Decisión que habilita:** el rector capta en 5 segundos los tres indicadores ejecutivos más importantes sin distracciones.
- **Por qué esta y no otra:** menos KPIs (3 en lugar de 5) elevan la jerarquía visual; el icono y el tag de color tonal (azul / verde / naranja) refuerzan la lectura categorial. La posición SUE y la variación interanual se desplazan al cuerpo del informe (Sección 3, Sección 2) para no saturar el hero.
- **Diseño:**
  - Hero con sidebar flotante permanente a la izquierda y contenido centrado verticalmente en el ancho derecho.
  - 3 tarjetas blancas con esquinas 18px, sombra elevada y línea de acento superior tonal.
  - Cada tarjeta: icono SVG en cuadro suave (trofeo / diana / personas) + píldora "DESEMPEÑO / POSICIONAMIENTO / COBERTURA" + número 2rem + etiqueta + sub-línea opcional.
  - El conjunto hero + KPIs ocupa ~70 svh para llenar el primer viewport sin asomar la sección siguiente.

---

## SECCIÓN 2 — Panorama institucional

### G2 · Radar de competencias UM vs. nacional (filtrable por año) — **Esencial**
- **Tipo:** radar de **6 ejes** (5 competencias genéricas + Puntaje Global) con **selector de año** (2020-2025).
- **Datos:** `institucional.historico[<año>].competencias` para las 5 competencias y `institucional.historico[<año>].puntaje_unimag/nacional` para el eje Puntaje Global.
- **Mensaje:** "Cómo se compara Unimagdalena con el promedio nacional en cada competencia, en el año seleccionado."
- **Decisión:** identifica fortalezas/brechas transversales y permite revisar la evolución de esas brechas cambiando el año.
- **Por qué radar:** muestra las 6 dimensiones y la forma global del perfil en una sola figura, comparando dos series sin saturar.
- **Diseño:** polígono azul (UM) sobre polígono verde (nacional) con relleno tenue; etiquetas numéricas a cada lado del eje (UM hacia un lado, Nacional hacia el otro) para que nunca se peguen aunque los valores coincidan. Marcadores sólidos de color, tooltip con la competencia y el valor al hacer hover.

### G3 · Evolución histórica global UM vs. nacional — **Esencial**
- **Tipo:** línea temporal 2020-2025 con curvas suaves (Catmull-Rom).
- **Datos:** `institucional.historico` (6 puntos: anio, puntaje_unimag, puntaje_nacional).
- **Mensaje:** "Cómo ha evolucionado nuestra brecha con el país: de estar por debajo (142 vs 149 en 2020) a superarlo (150 vs 148 en 2025)."
- **Decisión:** evidencia la tendencia institucional para rendición de cuentas.
- **Por qué línea:** es el formato natural para evolución temporal; el cruce de las dos líneas cuenta la historia visualmente.
- **Diseño:** línea azul (UM) y verde (nacional) con marcadores sólidos; etiquetas numéricas encima/debajo de cada punto con lógica anti-choque (UM arriba si supera al nacional, abajo si no); eje Y auto-escalado a múltiplos de 5 según el rango de los datos; tooltip con el año y el valor al hacer hover.

---

## SECCIÓN 3 — Posicionamiento externo

### G4 · Ranking SUE (filtrable por año) — **Esencial**
- **Tipo:** barras **verticales** ordenadas de mayor a menor puntaje (37 universidades), con **selector de año** (2020-2025).
- **Datos:** `sue_ranking_historico[<año>]` (rank, nombre, abrev, puntaje, n, es_unimagdalena, es_caribe).
- **Mensaje:** "Posición de Unimagdalena entre las universidades públicas del país en el año seleccionado."
- **Decisión:** ubica a la institución frente a sus pares directos en el SUE y muestra cómo ha cambiado de posición año a año.
- **Por qué barras verticales:** comunica mejor el ranking comparado al ojo (vista de "perfil" de la cohorte SUE) y permite usar el eje X para etiquetas cortas con todas las 37 universidades visibles a la vez. La etiqueta de valor encima de cada barra elimina la necesidad de un eje numérico denso.
- **Diseño:**
  - **Tres categorías de color** (paleta alineada con Posicionamiento):
    - **Unimagdalena** → verde institucional (`#2BA85E`)
    - **Región Caribe** → naranja (`#FF9400`)
    - **Otras del SUE** → azul institucional (`#0F4FA8`)
  - Etiquetas X cortas (UNAL, UIS, Distrital, etc.) tomadas de `parametros.yml` bajo `sue_abreviaturas`, rotadas -45° para que las 37 quepan sin solaparse.
  - Tooltip al hover con el **nombre completo**, posición (`22 de 37`), puntaje y evaluados.
  - Etiqueta de valor encima de cada barra (la de Unimagdalena un poco más grande y en su color).
  - Leyenda inferior con las 3 categorías.

### G5 · Comparativo con universidades del Departamento (filtrable por año) — **Esencial**
- **Tipo:** barras agrupadas (6 grupos de barras: 5 competencias genéricas + Puntaje Global), con **selector de año** (2020-2025).
- **Datos:** `universidades_dept_historico[<año>]`. Universidades incluidas: Unimagdalena (a nivel `INSTITUCION`), U. Sergio Arboleda – Santa Marta y U. Cooperativa de Colombia – Santa Marta (ambas a nivel `SEDE`). La lista es configurable en `parametros.yml` bajo `universidades_dept_magdalena`.
- **Mensaje:** "Cómo se compara Unimagdalena con las universidades privadas del mismo territorio en cada competencia y en el global."
- **Decisión:** posicionamiento regional frente a la competencia directa por matrícula. Permite ver evolución cambiando el año.
- **Por qué barras agrupadas y no scatter o radar:** las barras agrupadas son el formato estándar para comparar pocas categorías × pocas series, fácil de leer para alta dirección. Cada competencia se lee independientemente sin la complejidad geométrica del radar.
- **Diseño:** Unimagdalena en azul institucional, Sergio Arboleda en verde, Cooperativa en naranja (paleta alineada con el resto del informe). Valor sobre cada barra con el color de la serie. Tooltip al hover con universidad + competencia + valor + evaluados. Leyenda inferior con los 3 nombres acortados; el tooltip muestra el nombre completo.
- **Nota:** la lista de 3 universidades es la cobertura efectiva del Icfes en Magdalena (verificado 2020-2025); UNICARIBE no reporta en las bases del Icfes para Magdalena.

---

## SECCIÓN 4 — Valor agregado (cuadrantes)

### G6 · Cuadrantes de valor agregado (filtrable por año) — **Esencial**
- **Tipo:** dispersión con 4 cuadrantes y selector de año (**2020-2024**).
- **Datos:** `cuadrantes_por_anio[año]` (limites x_mean/y_mean, instituciones[], nbcs_unimag[]). **Solo se leen los años 2020-2024; 2018-2019 se omiten en el front-end.**
- **Mensaje:** "Recibimos perfiles de entrada y los graduamos por encima de la media: ese es nuestro aporte."
- **Decisión:** demuestra el valor agregado de la formación, no solo el resultado absoluto.
- **Por qué dispersión:** es el único formato que cruza entrada (X=Saber 11) y salida (Y=Saber Pro) simultáneamente; los 4 cuadrantes dan lectura instantánea.
- **Diseño:** ejes con líneas de media; cuadrantes coloreados suaves (verde=Alto Aporte/Desempeño, rojo=Alerta); otras IES en gris, UM en rojo destacado, NBC de UM en azul. **Nota visible: datos hasta 2024.**

### G7 · Trayectoria histórica de Unimagdalena — **Esencial**
- **Tipo:** recorrido temporal sobre el plano de cuadrantes (línea con puntos por año, **2020-2024**).
- **Datos:** `trayectoria_unimag` (limites, puntos[] con anio, sb11, sbpro, cuadrante). **Filtrar puntos a 2020-2024 en el front-end.**
- **Mensaje:** "La historia de evolución: de 'Alto aporte' (2020) a 'Alto desempeño' (2024)."
- **Decisión:** narrativa central de mejora institucional — el corazón del propósito "cómo ha venido la universidad".
- **Por qué este:** convierte 7 años en una sola línea de progreso visual; es el gráfico más narrativo del informe.
- **Diseño:** flecha conectando los puntos cronológicamente, color degradado del más antiguo al más reciente, etiqueta de año en cada punto.

---

## SECCIÓN 5 — Facultades

### G8 · Desempeño por facultad (filtrable por año y por competencia) — **Esencial**
- **Tipo:** barras horizontales ordenadas, con un **selector de año** (dropdown) + **tabs de competencia** (píldoras estilo Top 10).
- **Datos:** `facultades_historico[<año>]` (6 facultades por año con `puntaje_global`, `n` y las 5 competencias genéricas, todas con promedio ponderado por evaluados). Para el año vigente cae sobre `facultades[]`.
- **Mensaje:** "Cómo le fue a cada facultad en el puntaje global y en cada competencia genérica, año a año."
- **Decisión:** focaliza apoyo institucional por facultad. El decano puede ver el desempeño global y switchear rápido entre las 5 competencias.
- **Por qué barras horizontales con tabs:**
  - Horizontales para que los nombres largos de facultad quepan a la izquierda.
  - Tabs visuales (en lugar de un segundo dropdown) hacen la comparación entre competencias 1-clic; el usuario ve en qué tab está parado.
- **Diseño:**
  - Cada barra con su propio color (paleta indexada de 6 tonos coherentes con el informe).
  - Las barras se reordenan según el valor de la competencia seleccionada (la facultad mejor en Inglés sube al tope cuando se elige Inglés).
  - Tooltip aclara "Promedio ponderado por evaluados" sin listar las demás competencias (esas se ven cambiando de tab).
  - Título dinámico: "Lectura Crítica promedio por facultad 2024" cambia al instante.

### G12 · Matriz de calor competencias × facultad (filtrable por año) — **Esencial** (sección 5)
- **Tipo:** heatmap tabular HTML (6 facultades × 5 competencias) con **selector de año** (2020-2025).
- **Datos:** `facultades_historico[<año>][].competencias[]`.
- **Mensaje:** "Vista panorámica de qué facultad domina qué competencia en cada año."
- **Decisión:** complementa a G8 mostrando todas las competencias de todas las facultades a la vez. Útil para vicerrectoría y planeación cuando hay que detectar patrones (ej. "todas las facultades flojean en Razonamiento Cuantitativo").
- **Por qué heatmap:** densidad informativa (30 celdas en un golpe de vista) imposible de transmitir con G8 sin saturar el chart.
- **Diseño:**
  - Gradiente de azul claro (`#E8F1FB`) a azul institucional (`#0F4FA8`) mapeado al rango min–max del año seleccionado.
  - Texto blanco automático en celdas con porcentaje > 0.55 del rango para mantener legibilidad.
  - Esquina `FACULTAD` y headers de columna con tratamiento editorial (mayúsculas + letter-spacing + acento bajo).
  - Columna de facultades como tarjetas blancas con borde lateral azul brillante.
  - Marcadores ★ en el valor máximo y ◇ en el mínimo del año.
  - Leyenda al pie con barra-gradiente y los valores mín/máx etiquetados como `BAJO` / `ALTO`.
  - Tooltip al hover con facultad + competencia + puntaje + año.
- **Nota de ubicación:** este gráfico estaba en la sección 7 (Síntesis) hasta v2.5; en v2.6 se mueve a la sección 5 (Facultades) porque es donde más sentido tiene narrativamente (el lector que examina facultades necesita esta vista panorámica). La sección 7 ahora se enfoca solo en la DOFA estratégica.

---

## SECCIÓN 6 — Programas

### G9 · Explorador de programas (componente filtrable) — **Esencial**
- **Tipo:** componente compuesto con selector facultad→programa, que actualiza 4 sub-vistas.
- **Datos:** `programas[]` (39 programas: competencias_2025[], especificas_2025[], niveles_2025[], historico[], global vs global_nbc_nacional, n_bajo).
- **Sub-vistas al seleccionar un programa:**
  1. Radar de competencias genéricas del programa vs. su NBC nacional.
  2. Barras de competencias específicas vs. NBC (ojo: algunos programas tienen 0 específicas → ocultar la sub-vista).
  3. Histórico del programa (línea 2020-2025).
  4. Niveles de desempeño del programa vs. NBC (barras apiladas).
- **Mensaje:** "Cada programa frente a su grupo de referencia nacional, y su evolución."
- **Decisión:** da a cada director su diagnóstico específico.
- **Por qué un componente filtrable y NO 39 secciones:** elimina la redundancia del PPTX (~70 gráficos repetidos); un solo módulo interactivo cubre todos los programas y escala solo cuando se agregan más.
- **Diseño:** badge de advertencia para programas con `n_bajo: true`; comparación siempre vs. NBC en naranja.

---

## SECCIÓN 7 — Competencias y Top 10

### G10 · Top 10 por competencia — **Recomendado**
- **Tipo:** barras horizontales, con pestañas por competencia.
- **Datos:** `top10.por_competencia` (5 competencias, 10 programas c/u) + `top10.global`.
- **Mensaje:** "Qué programas lideran cada competencia."
- **Decisión:** identifica referentes internos y buenas prácticas replicables.
- **Por qué recomendado:** reconocimiento y benchmarking interno; no es lo primero que ve el rector.

### G11 · Niveles de desempeño institucional — **Recomendado**
- **Tipo:** barras apiladas al 100% (Nivel 1-5), UM vs. nacional, por competencia.
- **Datos:** `niveles_desempeno` (5 competencias con distribucion_unimag[5] y distribucion_nacional[5]).
- **Mensaje:** "Cómo se distribuye nuestra población por nivel de logro — no solo el promedio."
- **Decisión:** revela si el promedio esconde concentración en niveles bajos/altos. **Análisis nuevo que el PPTX no tiene.**
- **Por qué recomendado:** aporta profundidad que el promedio oculta; valioso para vicerrectoría académica.
- **Diseño:** barras apiladas con escala de color de rojo (Nivel 1) a verde (Nivel 5); par UM/nacional por competencia.

---

## TRANSVERSAL / OPCIONAL

### G12 · Mapa de calor competencias × facultad — **Opcional**
- **Tipo:** heatmap (6 facultades × 5 competencias).
- **Datos:** `facultades[].competencias[]`.
- **Mensaje:** "Dónde está cada fortaleza/brecha en la matriz facultad-competencia."
- **Por qué opcional:** vista densa, más analítica que ejecutiva; útil para planeación, prescindible para el rector.

---

## Notas vigentes de implementación

1. **Todos los gráficos leen del JSON** — ningún dato hardcodeado.
2. **SVG/Canvas vanilla**, sin librerías pesadas.
3. **Programas con `n_bajo: true`** siempre con advertencia visual.
4. **Cuadrantes/trayectoria** muestran nota "datos hasta 2024".
5. **Específicas variables:** algunos programas tienen 0-3 pruebas específicas; el
   componente G9 debe adaptarse (ocultar sub-vista si no hay datos).

## Registro de criterios de implementación

> "Implementa el catálogo de 12 visualizaciones definido, respetando para cada gráfico
> el tipo, los campos exactos del `datos_informe.json` que consume, y la convención de
> color (azul=UM, naranja=referencia, verde/rojo=juicio). Prioriza los Esenciales
> (G1,G2,G3,G4,G6,G7,G9). Reemplaza los gráficos repetidos por programa por el único
> componente filtrable G9. Marca visualmente los programas con n_bajo. Aplica el rango
> temporal: cuadrantes y trayectoria (G6, G7) solo años 2020-2024 (filtrar en el
> front-end, NO regenerar el JSON); el resto de gráficos 2020-2025. Todos los gráficos
> se generan desde el JSON con identidad azul; no copiar imágenes del PowerPoint."
