# Alternative Pathways — Abandono de la profesión docente

Estudio sobre **quién deja la docencia, adónde va y qué lo predice** en
EE.UU., 2015–2024, con el instrumento retrospectivo de la March CPS/ASEC
(Harris & Adams 2007): docente = ocupación del trabajo más largo del año
pasado en códigos K-12; *leaver* = ya no enseña en la semana de la encuesta
(otro empleo, paro o fuera de la fuerza laboral).

## Resultados principales (paper: `report/who_leaves_teaching.pdf`)
- **8,25%** de los docentes (graduados, K-12) deja la profesión al año.
  Composición: **5,1 pp fuera de la fuerza laboral**, 2,1 pp a otro empleo
  (⅕ de ellos dentro de la educación), 1,0 pp a paro.
- U por edad (mínimo ~4% a los 46-55; 12% a los 56-64; 28% a los 65+);
  pública 6,8% vs privada 11,6%; pico COVID (10,2% en marzo 2020) y vuelta
  al nivel previo en dos años.
- Predictores dominantes: **trabajar año parcial** (−9,4 pp si año completo),
  **tiempo parcial** (+4,4 pp), **sin pensión** (−2,4 pp con pensión);
  demografía un orden de magnitud menor.
- Mismo instrumento en profesiones comparables: enfermeras 8,0%,
  trabajadores sociales 13,6%, contables 6,3% — la docencia no es anómala.
- **Apéndice A**: validación persona a persona del instrumento contra un
  panel mensual enlazado (20 cohortes 2005-2024, PERIDNUM): acuerdo 99,1%
  donde ambos ven docente; la brecha de nivel del panel es reshuffling
  intra-educación + ruido de semana de referencia.
- **Apéndice B**: réplica de Harris & Adams (2007) en 2015-2024 — niveles y
  orden casi idénticos a 1992-2001.

## Reproducir
```bash
pip install pandas numpy statsmodels matplotlib pyarrow
python3 src/42_fetch_asec_harris.py   # ASEC 2016-2025 (Census, raw)
python3 src/44_main_analysis.py       # análisis principal -> outputs/main_*
python3 src/43_harris_update.py       # apéndice H&A -> outputs/ha_*
python3 src/45_paper_figures.py       # figuras y tablas del paper
cd report && pdflatex who_leaves_teaching.tex
```
Validación del instrumento (Apéndice A): `src/35...40_*` reconstruyen el
panel mensual 2005-2025 desde crudo y la tabla de confusión
(`outputs/tttt_march_allyears.csv`).

## Estructura
```
data/raw/asec/    ASEC person files (slim parquet por año)
data/raw/cps/     CPS mensual básico (slim parquet por mes)
src/              descarga, análisis, figuras (42-45 = pipeline actual)
outputs/          tablas CSV (main_* = paper; ha_* = apéndice H&A)
report/           who_leaves_teaching.tex/.pdf y tablas .tex
```

## Referencias de método
Harris & Adams (EER 2007) · Madrian & Lefgren (JESM 2000) · Aldeman & Yi
(Education Next 2025) · Ingersoll (AERJ 2001) · Grissmer & Kirby (TCR 1997)
· Brummet et al. (EEPA 2025).
