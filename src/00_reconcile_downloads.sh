#!/bin/bash
# Verify integrity of all raw CPS files, delete corrupt ones, and fill any
# missing 2005-2023 month from the NBER mirror (Census-hosted 2024-2025 are
# handled by the main download loop). Safe to re-run until it reports OK.
cd "$(dirname "$0")/../data/raw/cps" || exit 1

echo "== integrity check =="
for f in *.dat.gz; do
  [ -e "$f" ] || continue
  if ! gzip -t "$f" 2>/dev/null; then
    # some census files are ZIP despite the name
    python3 -c "import zipfile,sys; zipfile.ZipFile('$f').testzip()" 2>/dev/null \
      || { echo "corrupt: $f (deleting)"; rm -f "$f"; }
  fi
done
for f in cpsb*.zip; do
  [ -e "$f" ] || continue
  python3 -c "import zipfile,sys; zipfile.ZipFile('$f').testzip()" 2>/dev/null \
    || { echo "corrupt: $f (deleting)"; rm -f "$f"; }
done

echo "== fill missing 2005-2023 from NBER =="
mon=(jan feb mar apr may jun jul aug sep oct nov dec)
for y in $(seq 2005 2023); do
  yy=${y:2:2}
  for i in $(seq 0 11); do
    mm=$(printf "%02d" $((i+1)))
    # present under either naming?
    [ -s "cpsb${y}${mm}.zip" ] && continue
    [ -s "${mon[$i]}${yy}pub.dat.gz" ] && continue
    curl -s --max-time 180 --retry 3 --retry-delay 4 \
      "https://data.nber.org/cps-basic3/dat/${y}/cpsb${y}${mm}_dat.zip" \
      -o "cpsb${y}${mm}.zip"
    if [ -s "cpsb${y}${mm}.zip" ] && python3 -c "import zipfile; zipfile.ZipFile('cpsb${y}${mm}.zip').testzip()" 2>/dev/null; then
      echo "fetched cpsb${y}${mm}.zip"
    else
      rm -f "cpsb${y}${mm}.zip"; echo "MISSING ${y}-${mm}"
    fi
  done
done

echo "== summary =="
echo "census-named files : $(ls *pub.dat.gz 2>/dev/null | wc -l)"
echo "nber-named files   : $(ls cpsb*.zip 2>/dev/null | wc -l)"
