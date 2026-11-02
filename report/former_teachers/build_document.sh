#!/bin/sh
# Rebuild the full draft from the authors' draft.docx:
#   1) insert Section 3; 2) apply the corrections to Section 2, write the
#   Introduction, insert the EAG-style figures and apply the layout of OECD
#   Education Working Paper No. 342 (Schweickert and Torres, 2026);
#   3) render once to compute the page numbers of the table of contents.
# Figures: python3 replication/deck_figures/fig_oecd_former_teachers.py
# Usage: sh build_document.sh path/to/authors_draft.docx
set -e
cd "$(dirname "$0")"
export PYTHONPATH=section3_src FIG_DIR="$PWD/figures"
T=$(mktemp -d)
python3 build_section3.py section3_v6 "$1" "$T/s3.docx"
python3 section3_src/restyle_torres.py "$T/s3.docx" "$T/pass1.docx"
soffice --headless --convert-to pdf --outdir "$T" "$T/pass1.docx" >/dev/null 2>&1
python3 section3_src/toc_pages.py "$T/pass1.docx.toc.json" "$T/pass1.pdf" section3_src/toc_pages.json
python3 section3_src/restyle_torres.py "$T/s3.docx" Former_Teachers_draft.docx section3_src/toc_pages.json
soffice --headless --convert-to pdf --outdir . Former_Teachers_draft.docx >/dev/null 2>&1
rm -f Former_Teachers_draft.docx.toc.json
