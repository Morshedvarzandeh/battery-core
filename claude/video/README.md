# CellForge — LinkedIn clip pipeline

Reproduces `cellforge-linkedin-1080x1920.mp4` (9:16, 59.3 s, H.264 + AAC) from the
simulator itself. No external assets: the footage is a real browser session, the cards
are rendered from HTML, and the music bed is synthesised by ffmpeg.

## Prerequisites

- `playwright` with Chromium (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`)
- an ffmpeg build with `libx264` and `aac` (the Playwright-bundled ffmpeg is video-only
  and cannot do this step; `npm i ffmpeg-static` provides a suitable one)
- the docs served over HTTP: `python -m http.server 8765 -d docs`

## Steps

```bash
node drive.mjs     # drives the page, records rec/*.webm, writes timeline.json
node cards.mjs     # renders card-title.png, card-end.png, cap-01..10.png
bash build.sh      # trims, speeds up 1.5x, burns captions, adds the music bed, muxes
```

`drive.mjs` records at a 1080x1920 viewport with `zoom: 1.7`, so the page uses its own
compact (drawer) layout and the type stays legible on a phone. Scroll targets are
fractions of the scrollable height, so they survive layout changes.

`build.sh` reads the scene marks in `timeline.json`; caption windows in the `CAPS`
array are in body time *after* the 1.5x speed-up (mark / 1.5).

## Wording

The end card quotes the simulator's own scope statement verbatim. Keep it: the clip
shows illustrative teaching relationships, not calibrated plant predictions.
