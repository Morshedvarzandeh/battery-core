# Module clips

Short social clips of the interactive modules in this repository, rendered from the
modules themselves. Nothing here uses stock footage, stock music, or an external media
asset: the footage is a real browser session, the cards are HTML rendered to PNG, and
the music bed is synthesised by ffmpeg.

Rendered `.mp4` files are **not committed** — each is roughly 20–25 MB and one command
regenerates it. Only the pipeline lives here.

First clip produced with it: the CellForge battery-production simulator,
1080×1920, 59.3 s, H.264 + AAC.

## Prerequisites

- Node with `playwright` and its Chromium (`npx playwright install chromium`)
- an ffmpeg built with `libx264` and `aac` — `npm i ffmpeg-static` provides one, and
  `build.sh` picks it up automatically. The ffmpeg bundled with Playwright is
  video-only and **cannot** do the final encode.
- the docs tree served over HTTP, because the simulators fetch their source parts:

```bash
python -m http.server 8765 -d docs
```

## Render

```bash
node drive.mjs     # drives the page, records rec/*.webm, writes timeline.json
node cards.mjs     # renders card-title.png, card-end.png, cap-01..10.png
bash build.sh      # trims, speeds up, burns captions, adds the music bed, muxes
```

`build.sh` calls `music.py` for the bed, so it can also be rendered on its own:

```bash
python3 music.py music.wav 59.3
```

Environment variables:

| variable | default | meaning |
|---|---|---|
| `MODULE_URL` | `http://127.0.0.1:8765/fundamentals/battery-production/` | page to record |
| `ZOOM` | `1.7` | page zoom; keeps the compact layout and legible type at 1080 px wide |
| `REC_DIR` | `./rec` | where the raw `.webm` lands |
| `SPEED` | `1.5` | playback speed applied to the recording |
| `OUT_NAME` | `cellforge-linkedin-1080x1920.mp4` | final file |
| `FF` | auto-detected | path to a full ffmpeg |
| `MUSIC_GAIN` | `0.45` | bed level at the mux; the clip lands near −26 dB mean |

## The music bed

`music.py` writes the WAV with nothing but the Python standard library — no samples,
no third-party audio, nothing to clear for rights. It plays a I-V-vi-IV progression in
C major at 100 BPM: plucked arpeggios with a fast decay, a quiet pad, one root note per
bar, and two short reverb taps.

The shape matters more than the notes. Sustained minor chords with slow swells read as
a thriller soundtrack no matter how quiet they are; short plucks in a major key read as
a product demo. If you rework it, keep the plucks.

## Adapting it to another module

1. Rewrite the scene block in `drive.mjs` — the marked sections `A`…`I` are ordinary
   Playwright steps against that module's own selectors.
2. Rewrite `CAPS` in `cards.mjs` (caption text) and the title and end cards.
3. Update the caption windows in `build.sh`. They are in **body time after the
   speed-up**, i.e. the mark from `timeline.json` divided by `SPEED`.

`drive.mjs` records at a 1080×1920 viewport with page zoom, so a module's own responsive
layout does the work instead of cropping a desktop capture. Scroll targets are fractions
of the scrollable height, so they survive layout changes.

## One rule for the wording

The end card quotes the module's own scope statement verbatim — for CellForge:

> Published sources support the process sequence and displayed operating ranges.
> Capacity, throughput, wetting, process-health and risk-control outputs are illustrative
> teaching relationships. They are not calibrated plant predictions, equipment-sizing
> calculations or release criteria.

Keep that card. These modules are teaching models, and a clip that travels without the
qualification invites the reader to treat illustrative scores as measured plant results.
