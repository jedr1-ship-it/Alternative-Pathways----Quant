# Alternative Pathways — Abandono de la profesión docente

Estudio para caracterizar **por qué los docentes abandonan la profesión**: qué
factores predicen la salida, cuál pesa más, y cuál es el perfil típico del
docente que abandona. Estrategia: panel longitudinal de individuos → filtrar
docentes → observar quién deja la docencia en el tiempo → **probit** de abandono
con la mayor cantidad de características observadas.

## Estado actual
- **Estudio completo sobre microdatos oficiales de la CPS 2005–2025** (Census
  Bureau + mirror NBER): 20 paneles rotantes enlazados, 8,2M de enlaces
  individuales validados, **174.872 docentes con grado+ seguidos 12 meses**
  (129.897 con re-entrevista posterior).
- **Variable principal: *leaver persistente*** (fuera de la docencia en t+12 y
  en todas las re-entrevistas posteriores observables) = **15,1%** anual;
  definición convencional a 12 meses (17,6%) como robustez. Predictor más
  fuerte: tiempo parcial (+12,2 pp). Tendencia: ~13% (2005–10) → ~17% (2022–24).
- **Informe** estilo policy brief en `report/teacher_attrition_brief.pdf`
  (LaTeX, 6 figuras validadas, 1 tabla de regresión).
- Nota histórica: `src/01_panel_attrition_demo.py` fue la demo inicial de la
  metodología sobre el PSID 1976–1982; ver `docs/DATA_ACCESS.md`.

## Reproducir
```bash
pip install pandas numpy statsmodels matplotlib
python3 src/02_build_cps_panel.py    # descarga/enlaza CPS 2005-2025
python3 src/05_evolution.py          # retornos + evolución (exporta flags)
python3 src/03_model_attrition.py    # probit leaver persistente + robustez
python3 src/04_figures.py            # figuras y tabla del brief
```

## Estructura
```
data/raw/         microdatos descargados (PSID7682.csv)
src/              scripts de análisis
outputs/          reporte, perfil stayer/leaver, efectos marginales
docs/             notas de acceso a datos y diseño
```

## Referencias de método (economía del abandono docente)
Dolton & van der Klaauw (EJ 1995; ReStat 1999) · Stinebrickner (JOLE 2001; JHR
2002) · Hanushek, Kain & Rivkin (JHR 2004) · Clotfelter et al. (JPubE 2008) ·
Falch (AER 2011).
