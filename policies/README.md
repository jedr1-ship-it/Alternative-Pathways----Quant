# Re-attracting former teachers — políticas comparadas

Presentación (`Re-attracting_Former_Teachers.pptx`, 19 diapositivas, 16:9) que recopila
**16 políticas reales de 13 países** dirigidas a traer de vuelta al sistema educativo a
ex docentes: *switchers* (cambiaron de sector), *leavers* (salieron del mercado laboral)
y *retired* (jubilados).

## Estructura del archivo
1. Portada.
2. Definiciones: los tres grupos objetivo y las cinco categorías de instrumento
   (Financial incentives · Information & nudges · Support & training · Flexible positions ·
   Flexible re-certification).
3. Una diapositiva por política (16), ordenadas por país y categoría. Cada una lleva:
   bandera y país (arriba a la izquierda), categoría principal y grupos objetivo (arriba a
   la derecha), nombre y año de la política, descripción estructurada en cuatro bloques (*What it is /
   How it works / Means / Since*), línea de instrumentos secundarios y el pie `Source:` con
   enlace clicable.
   Las notas del orador de cada diapositiva contienen la verificación de fuentes y datos
   secundarios.
4. Tabla resumen: País | Política | Categoría | Grupo(s) objetivo.

`policies.csv` contiene los mismos datos en formato tabular (una fila por política, con
los cuatro bloques de la descripción, instrumentos secundarios y enlaces).

## Fuentes y verificación
Todas las fuentes son primarias (leyes, decretos, circulares, páginas de ministerios o
agencias) o institucionales (IES/REL Central, comité parlamentario, auditoría estatal); solo
dos cifras de alcance proceden de prensa (Le Devoir para Quebec, Público para Portugal) y
así se indica en la diapositiva o en las notas. Los enlaces se comprobaron el 17-09-2026
mediante indexación de buscadores de las páginas oficiales (el entorno de construcción no
permitía acceso HTTP directo).

## Regenerar la presentación
```bash
cd policies/build
npm install
node build.js          # escribe Re-attracting_Former_Teachers.pptx en esta carpeta
```
Los datos de cada política están en `build/policies.js`; el diseño, en `build/build.js`
(pptxgenjs; banderas de `flag-icons`, iconos de `react-icons`). Fuentes: Cambria (títulos)
y Calibri (texto); dos colores de texto por diapositiva.
