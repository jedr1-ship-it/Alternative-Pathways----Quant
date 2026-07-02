# Alternative Pathways — Abandono de la profesión docente

Estudio para caracterizar **por qué los docentes abandonan la profesión**: qué
factores predicen la salida, cuál pesa más, y cuál es el perfil típico del
docente que abandona. Estrategia: panel longitudinal de individuos → filtrar
docentes → observar quién deja la docencia en el tiempo → **probit** de abandono
con la mayor cantidad de características observadas.

## Estado actual
- **Fase de datos.** Ver [`docs/DATA_ACCESS.md`](docs/DATA_ACCESS.md). La política
  de egress del entorno solo permite GitHub/PyPI, así que las fuentes con
  docentes (NCES SASS/TFS, CPS, EPA, PSID completo) no son descargables aún.
- **Maquinaria validada** sobre un panel real (PSID 1976-1982) en
  `src/01_panel_attrition_demo.py`: transiciones t→t+1, probit cluster-robusto,
  efectos marginales y perfil del que abandona. Lista para sustituir por datos
  de docentes.

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
