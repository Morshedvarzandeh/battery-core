#!/bin/bash
# battery-core — open-source battery engineering fundamentals.
# Copyright (C) 2026 Morshed Varzandeh and battery-core contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

set -euo pipefail
cd "$(dirname "$0")"
# an ffmpeg with libx264 + aac; `npm i ffmpeg-static` provides one
FF=${FF:-$(node -p "require('ffmpeg-static')" 2>/dev/null || echo ffmpeg)}
SRC=$(ls rec/*.webm)
PREROLL=$(python3 -c "import json;print(json.load(open('timeline.json'))['preroll'])")
OUT_NAME=${OUT_NAME:-cellforge-linkedin-1080x1920.mp4}
SPEED=${SPEED:-1.5}
BODY=$(SPEED="$SPEED" python3 -c "import json,os;t=json.load(open('timeline.json'));print(round(t['total']/float(os.environ['SPEED']),2))")
TITLE=3.5
ENDD=4.5

# caption windows, in body time after the 1.5x speed-up
CAPS=(
 "0.10 7.60"  "7.80 12.40" "12.60 19.70" "19.90 22.20" "22.40 29.20"
 "29.50 34.20" "34.40 39.00" "39.30 42.70" "42.90 46.50" "46.70 51.25"
)

# ---- 1 · body: trim preroll, speed up, burn captions ------------------------
FILTER="[0:v]setpts=PTS/${SPEED},fps=30,format=rgba,fade=t=in:st=0:d=0.5[b0]"
prev="b0"
for i in "${!CAPS[@]}"; do
  read -r s e <<< "${CAPS[$i]}"
  n=$((i+1)); idx=$((i+1))
  fo=$(python3 -c "print(round(${e}-0.3,2))")
  # the caption stream is looped, so its own clock matches the body clock
  FILTER="${FILTER};[${idx}:v]format=rgba,fade=t=in:st=${s}:d=0.3:alpha=1,fade=t=out:st=${fo}:d=0.3:alpha=1[c${n}]"
  FILTER="${FILTER};[${prev}][c${n}]overlay=0:1400:enable='between(t,${s},${e})'[b${n}]"
  prev="b${n}"
done
FILTER="${FILTER};[${prev}]format=yuv420p[body]"

CAPIN=()
for f in cap-*.png; do CAPIN+=(-loop 1 -framerate 30 -t "$BODY" -i "$f"); done

$FF -y -v warning -stats -ss "$PREROLL" -i "$SRC" "${CAPIN[@]}" \
  -filter_complex "$FILTER" -map "[body]" -an \
  -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -r 30 body.mp4

# ---- 2 · title and end cards ------------------------------------------------
$FF -y -v warning -loop 1 -i card-title.png -t "$TITLE" \
  -vf "fps=30,format=yuv420p,fade=t=in:st=0:d=0.5,fade=t=out:st=$(python3 -c "print($TITLE-0.5)"):d=0.5" \
  -c:v libx264 -preset medium -crf 19 -r 30 title.mp4
$FF -y -v warning -loop 1 -i card-end.png -t "$ENDD" \
  -vf "fps=30,format=yuv420p,fade=t=in:st=0:d=0.5,fade=t=out:st=$(python3 -c "print($ENDD-0.8)"):d=0.8" \
  -c:v libx264 -preset medium -crf 19 -r 30 end.mp4

printf "file '%s'\n" title.mp4 body.mp4 end.mp4 > concat.txt
$FF -y -v warning -f concat -safe 0 -i concat.txt -c copy silent.mp4

DUR=$(FFBIN="$FF" python3 - <<'PY'
import os, re, subprocess
out = subprocess.run([os.environ['FFBIN'], '-i', 'silent.mp4'], capture_output=True, text=True).stderr
h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', out).groups()
print(f"{int(h)*3600+int(m)*60+float(s):.2f}")
PY
)
echo "video duration: ${DUR}s"

# ---- 3 · music bed: two alternating chords, cross-faded ---------------------
ENVA="(0.5+0.5*sin(2*PI*t/16))"
ENVB="(0.5-0.5*sin(2*PI*t/16))"
CHA="(sin(2*PI*110*t)+0.7*sin(2*PI*164.81*t)+0.5*sin(2*PI*220*t)+0.32*sin(2*PI*329.63*t))"
CHB="(sin(2*PI*87.31*t)+0.7*sin(2*PI*174.61*t)+0.5*sin(2*PI*261.63*t)+0.32*sin(2*PI*349.23*t))"
AIR="0.035*sin(2*PI*659.26*t)*(0.5+0.5*sin(2*PI*t/7))"
EXPR="0.13*(${ENVA}*${CHA}+${ENVB}*${CHB})+${AIR}"
FOUT=$(python3 -c "print(round(${DUR}-3.6,2))")

$FF -y -v warning -f lavfi -i "aevalsrc=exprs=${EXPR}:duration=${DUR}:sample_rate=48000" \
  -af "aecho=0.8:0.88:60|140:0.28|0.18,lowpass=f=1500,highpass=f=45,afade=t=in:st=0:d=2.5,afade=t=out:st=${FOUT}:d=3.6,volume=0.85,alimiter=limit=0.9" \
  -c:a pcm_s16le music.wav

# ---- 4 · mux ----------------------------------------------------------------
$FF -y -v warning -i silent.mp4 -i music.wav -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -ac 2 -shortest -movflags +faststart \
  "$OUT_NAME"

ls -la "$OUT_NAME"
