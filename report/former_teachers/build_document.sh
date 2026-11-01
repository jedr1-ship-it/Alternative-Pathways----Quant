#!/bin/sh
# Rebuild the full draft from the authors' draft.docx:
#   1) insert Section 3, 2) write the Introduction and apply the layout of
#   OECD Education Working Paper No. 342 (Schweickert and Torres, 2026).
# Usage: sh build_document.sh path/to/authors_draft.docx
set -e
cd "$(dirname "$0")"
export PYTHONPATH=section3_src
python3 build_section3.py section3_v6 "$1" /tmp/_s3.docx
python3 section3_src/restyle_torres.py /tmp/_s3.docx Former_Teachers_draft.docx section3_src/toc_pages.json
