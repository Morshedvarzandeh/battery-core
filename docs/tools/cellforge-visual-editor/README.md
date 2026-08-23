# CellForge Layout Editor

An authoring tool, not a lesson. The Chapter 1 production simulator draws every
machine from fixed SVG coordinates, so a label that overlaps at one screen width
overlaps for every reader. This editor opens those diagrams, lets a maintainer
move, rename, and resize any part on the canvas, and exports only what changed.

It belongs to the **toolkit** tier of the course, which is why the page is
orange rather than mint: it builds the material instead of teaching it. See
[`docs/assets/README.md`](../../assets/README.md) for the colour roles.

## The three diagrams

| Diagram | What it is |
| --- | --- |
| Coating | The Part 03 coating line: slurry delivery, slot die, backing roll, inline pattern camera, wet-film gauge. |
| Calendering | The Part 03 calendering line: infeed cleaning, the controlled nip, closed-loop thickness feedback. |
| Standard template | Not a machine. The skeleton the other two share, for starting a new process step. |

The standard template gives a new diagram the same frame, the same four zone
divisions, one web line at `y = 214` with flow arrows, placeholder machines
(feed unit, process head, drive roll, inspection camera, inline gauge), and
input/in-process/output state badges. Rename the placeholders into the machines
the step actually needs, and the result is already on the course grid and at the
course label scale. Starting from a blank canvas is what produced the label
overlaps this tool exists to fix.

Each diagram keeps its own edits and its own undo history while you switch
between them. **Reset this diagram** restores only the one on screen.

## Editing

- **Select** — click any label or machine part on the canvas.
- **Move** — drag it, use the nudge buttons, or use the arrow keys. Arrow keys
  move by 1 unit, Shift + arrow by 5. Snap to grid rounds to 5.
- **Rewrite** — edit the text field. Only labels accept text.
- **Resize** — the size slider scales a part from 70% to 140% about its centre.
- **Check** — the collision count rechecks after every change and marks any two
  labels whose rendered boxes overlap.

Below 600px the canvas shows one of three sections at a time, so the editor is
usable on a phone without shrinking the labels to nothing.

## Export

**Copy all layouts** and **Download JSON** both produce the same payload: a
version marker and, per diagram, one entry for each part that moved, scaled, or
was renamed.

```json
{
  "version": 1,
  "layouts": {
    "coating": [],
    "calendering": [],
    "template": [
      { "id": "component-label-2-2", "dx": 5, "dy": 0, "scale": 1, "text": "Dry-electrode calender" }
    ]
  }
}
```

Unchanged parts are omitted, so the payload is a diff rather than a snapshot.
Apply it to the coordinates in the Part 03 payload under
`docs/fundamentals/battery-production/payload/`, then re-run
`tests/test_battery_production_simulator.py` so the change is checked the same
way the rest of the course is.

**Save draft** keeps work in this browser's `localStorage` under
`cellforge-layout-draft`. It is a convenience, not storage: clearing site data
discards it, and it never leaves the browser.

## Run locally

From the repository root:

```bash
python -m http.server 8000 -d docs
```

Then open:

```text
http://localhost:8000/tools/cellforge-visual-editor/
```

No build step, no JavaScript libraries, and no external network resources. The
page loads `../../assets/site.css` and nothing else.

## Tests

`tests/test_cellforge_visual_editor.py` checks the page statically: unique
element ids, every ARIA reference resolving to a real id, all three stations
present, the export and clipboard fallbacks intact, the mobile sections and
collision feedback in place, and no external script sources.
