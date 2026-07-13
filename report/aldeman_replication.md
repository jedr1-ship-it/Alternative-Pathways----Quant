# Replicando Aldeman & Yi (2025): ¿abandonan los docentes la profesión en masa?

**Pregunta:** ¿se puede reproducir el 7,6 % de rotación docente anual que
publican Chad Aldeman y Samuel Yi en *Education Next* ("Are Teachers
Abandoning Their Profession in Large Numbers?", 2025) descargando los
microdatos de la CPS?

**Respuesta corta: sí.** Con el mismo instrumento y el periodo 2015-2024
obtengo **7,2 %** con los códigos de docente K-12 estándar (IC 95 %
≈ [6,9, 7,6]) y **8,8 %** si añado la categoría "otros docentes e
instructores". El 7,6 % de Aldeman & Yi queda **entre esas dos
definiciones** y en el borde de mi intervalo de confianza. Además reproduzco
el hecho que sostiene su argumento: **las enfermeras rotan al 7,8 %**, igual
que los docentes.

## El método (el suyo y el mío)

Aldeman & Yi siguen a Harris & Adams (2007). Usan una sola encuesta de la
**CPS ASEC** (suplemento de marzo), que pregunta a cada persona su ocupación
en la semana actual **y** su trabajo principal del año anterior. Un docente
es quien declara haber enseñado el año pasado; es *leaver* si su ocupación
actual ya no es docente (incluido no estar empleado). Esto capta solo a
quienes **dejan la profesión**, no a los *movers* que cambian de centro o
distrito. Para mitigar el tamaño muestral, agrupan 10 años.

Mi implementación:

- **Datos:** CPS ASEC person files, encuestas 2016-2025 (= años naturales
  2015-2024), descargados directamente del Census Bureau. Los años ≥2019 son
  CSV; 2016-2018 son fixed-width `.dat` que parseo con las posiciones del
  diccionario oficial de cada año (`src/27_fetch_asec.py`,
  `src/29_fetch_asec_fixedwidth.py`).
- **Instrumento:** `OCCUP` (ocupación del trabajo más largo del año pasado)
  vs `PEIOOCC` (ocupación actual). Base = enseñó el año pasado; leaver =
  `PEIOOCC` ya no es código docente, con `PEIOOCC = -1` (no empleado)
  contando como salida.
- **Códigos:** 2300 (preescolar/infantil), 2310 (primaria/media), 2320
  (secundaria), 2330 (educación especial). Son idénticos en los esquemas
  censales de 2010 y 2018, lo que hace comparable el pool a través del cambio
  de clasificación de 2020. "Otros docentes" es 2340 (esquema 2010) y se
  divide en 2350/2360 (esquema 2018); lo trato por era.
- **Ponderación:** `MARSUPWT`. Cálculo en `src/28_aldeman_turnover.py`.

## Resultados

| Cantidad | Réplica | Aldeman & Yi | Fuente A&Y |
|---|---:|---:|---|
| Rotación docente, códigos K-12, pool 2015-2024 | **7,2 %** | 7,6 % | CPS |
| Rotación docente, K-12 + "otros docentes" | 8,8 % | 7,6 % | CPS |
| Enfermeras tituladas (profesión comparable) | 7,8 % | ~7,6 % | CPS |
| Docentes públicos (clase de trabajador CPS) | 6,6 % | 7,9 % | NCES TFS |
| Docentes privados (clase de trabajador CPS) | 8,6 % | 11,7 % | NCES TFS |

Notas:

- **7,2 % vs 7,6 %.** La diferencia (0,4 pp) es del orden del error de
  muestreo (IC 95 % de mi estimación llega hasta 7,58 %) y se explica por el
  conjunto exacto de códigos de ocupación y por posibles diferencias de
  armonización (Aldeman probablemente usa códigos IPUMS). El 7,6 % está
  literalmente entre mi definición estricta (7,2 %) y la amplia (8,8 %).
- **Enfermeras ≈ docentes.** El corazón del argumento de Aldeman & Yi es que
  la rotación docente no es anómala: es comparable a la de otras profesiones.
  Mis enfermeras (7,8 %) reproducen exactamente su afirmación.
- **Gradiente por edad.** Reproduzco la forma en U: alta entre los más
  jóvenes (21-24: ~16 %), mínima en los 40 (~4 %) y alta de nuevo por
  jubilación (60-64: ~14 %; 65+: ~24 %) — coincide con su Figura 3.
- **Público/privado.** El 7,9 % y 11,7 % que cita Aldeman **no** salen de la
  CPS sino del *Teacher Follow-up Survey* del NCES (dato administrativo). No
  son un objetivo de réplica CPS; los incluyo solo como contexto. Mi split
  CPS reproduce la dirección (privado > público).

## Descomposición y matices

- De los ~7-9 pp de salida, ~3,4 pp cambian a **otra ocupación** y ~5,4 pp
  aparecen como **no empleados** en la semana de referencia (jubilación,
  cuidado familiar, paro).
- La **serie anual** de una sola ASEC es ruidosa (n≈3.000/año, SE≈1,5 pp): mi
  serie K-12 oscila entre 6,2 % y 8,5 % sin un pico de COVID nítido, mientras
  que Aldeman reporta 6,5 % (2019) → 9,8 % (2020). El *pool* de la década, en
  cambio, es estable y reproducible. No sobreajusto a los puntos anuales.
- El instrumento retrospectivo de una encuesta da cifras mucho más bajas
  (~7 %) que el **panel mensual enlazado** de la CPS (~15 %, ver
  `src/02_build_cps_panel.py`), porque este último arrastra mucho error de
  recodificación de ocupación mes a mes. Aldeman usa el retrospectivo, y es
  el que reproduce su número.

## Reproducir

```bash
pip install pandas numpy pyarrow
python3 src/27_fetch_asec.py            # ASEC CSV 2019-2025 (Census)
python3 src/29_fetch_asec_fixedwidth.py # ASEC fixed-width 2016-2018
python3 src/28_aldeman_turnover.py      # tabla de réplica -> outputs/
```

**Fuentes**

- Aldeman, C., & Yi, S. (2025). *Are Teachers Abandoning Their Profession in
  Large Numbers?* Education Next.
- Harris, D. N., & Adams, S. J. (2007). *Understanding the level and causes
  of teacher turnover: A comparison with other professions.* Economics of
  Education Review 26(3).
- U.S. Census Bureau, CPS ASEC public-use microdata, 2016-2025.
