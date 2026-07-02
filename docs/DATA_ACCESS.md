# Acceso a datos — hallazgos y restricciones (2026-07-02)

## Objetivo
Localizar un panel longitudinal **público y descargable en este entorno** que
siga a los mismos individuos en el tiempo, permita filtrar docentes y observar
quién abandona la profesión, para un modelo probit de abandono.

## Restricción encontrada: política de egress
La red de salida del entorno **solo permite GitHub y los registros de paquetes**
(PyPI, npm, crates…). El resto de hosts devuelve **403 (policy denial)** o no es
alcanzable. Verificado con sondeo directo:

| Host | Resultado |
|---|---|
| `raw.githubusercontent.com`, `github.com` | ✅ alcanzable |
| `pypi.org` / `files.pythonhosted.org` | ✅ (bypass proxy) |
| `www2.census.gov` (CPS) | ❌ 403 |
| `www.ine.es` (EPA) | ❌ 403 |
| `nces.ed.gov`, `data.nber.org`, `cps.ipums.org` | ❌ no alcanzable |
| `dataverse.harvard.edu`, `zenodo.org`, `microdata.worldbank.org` | ❌ no alcanzable |

**Consecuencia:** ninguna de las fuentes que identifican específicamente a
docentes y los sigue en el tiempo (NCES SASS/TFS, CPS enlazada, PSID completo,
EPA, SOEP, NLSY) es descargable directamente hoy. Búsqueda en GitHub de
microdatos nacionales con ocupación=docente: sin resultados utilizables (solo
dashboards con datos sintéticos o datos administrativos no compartibles).

## Lo que SÍ se hizo (pipeline validado sobre panel real)
`src/01_panel_attrition_demo.py` descarga y analiza el **PSID Earnings Panel
1976-1982** (`AER::PSID7682` vía Rdatasets en raw.githubusercontent), 595
individuos × 7 años. Es un panel real que sigue a los mismos individuos, con
ocupación (white/blue collar). Se implementa TODA la maquinaria pedida:

1. Construcción de transiciones t→t+1 por individuo.
2. Definición de "abandono" como salida ocupacional (white-collar en t →
   no white-collar en t+1) — análogo estructural de "dejar la profesión".
3. Perfil descriptivo *stayer vs leaver*.
4. **Probit** con errores robustos cluster por individuo.
5. Efectos marginales medios (AME) rankeados → predictor más fuerte.
6. Perfil del decil de mayor riesgo (= docente/individuo "típico" que abandona).

Basta **sustituir el CSV por un panel con docentes codificados** y el mismo
código responde la pregunta real. La ocupación aquí es demasiado gruesa
(white/blue) para ser "profesores", así que esto es demostración de método, no
el resultado sustantivo final.

## Opciones para conseguir datos de docentes reales (decisión pendiente)
1. **Ampliar la allowlist de egress** a un host de datos (p.ej. `nces.ed.gov`,
   `cps.ipums.org` o `www.ine.es`). Es una política del entorno; la fija quien
   creó el environment. Es la vía más limpia.
2. **Aportar tú un extracto**: descargar de IPUMS-CPS / NCES un CSV con
   ocupación (y variable de enlace individual) y subirlo al repo; el pipeline lo
   consume tal cual.
3. **Credenciales IPUMS**: con una API key de IPUMS podría generar el extracto
   enlazado CPS por API (si se permite el host `api.ipums.org`).
4. Seguir con un **panel proxy** (PSID/NLSY vía paquetes) solo para metodología.
