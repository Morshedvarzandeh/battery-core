"""Export the Part 04 notebook's interactive panels as pages for the website.

The battery-aging notebook carries its panels as self-contained HTML, stored
compressed in its setup cell. The website lesson embeds the same panels, so
this script writes them out next to the lesson instead of maintaining a second
copy by hand:

    docs/fundamentals/battery-aging/panels/panels.css   shared styles + site theme
    docs/fundamentals/battery-aging/panels/panels.js    shared model library
    docs/fundamentals/battery-aging/panels/<name>.html  one page per panel

Run it from the repository root after changing a panel in the notebook:

    python scripts/export_aging_panels.py

`tests/test_lessons.py` fails if the exported files and the
notebook disagree, so a panel cannot change in one place and not the other.
"""

from __future__ import annotations

import base64
import json
import re
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "fundamentals" / "04_battery_aging.ipynb"
OUTPUT = ROOT / "docs" / "fundamentals" / "battery-aging" / "panels"

# The notebook's own light/dark switch. The website has one light theme, so
# the switch is left out and every panel is pinned to the light theme below.
SKIPPED = {"theme"}

TITLES = {
    "map": "Mechanism map",
    "cell": "Inside one electrode sandwich",
    "sei": "SEI film growth",
    "gas": "Gas generation",
    "crystal": "Crystal formation and power fade",
    "plating": "Lithium plating risk",
    "cracking": "Cracking and depth of discharge",
    "sim": "All six mechanisms at once",
    "window": "Temperature window",
}

# Re-tune the notebook's design knobs to the course palette: cool neutrals and
# the blue core-path accent, on a transparent ground so the lesson's panel
# frame shows through.
SITE_THEME = """
/* --- Battery Core website theme (added by scripts/export_aging_panels.py) --- */
:root {
  --hue-accent: 258;
  --chroma-accent: 0.17;
  --hue-neutral: 255;
  --chroma-neutral: 0.01;
  --font-sans: "Source Sans 3", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Arial, sans-serif;
}
body {
  background: transparent;
  padding: 16px;
}
"""

PIN_LIGHT = """
/* Battery Core website: the course has one light theme, so pin every panel to
   it instead of following the operating system. */
document.documentElement.dataset.theme = "light";
"""

PAGE = """<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title} — Battery aging panel</title>
<link rel="stylesheet" href="../../../assets/fonts/fonts.css">
<link rel="stylesheet" href="panels.css">
</head>
<body>
<script src="panels.js"></script>
{widget}
</body>
</html>
"""


def load_assets(notebook: Path = NOTEBOOK) -> dict:
    """Return the notebook's compressed panel assets as a dictionary."""
    cells = json.loads(notebook.read_text(encoding="utf-8"))["cells"]
    for cell in cells:
        source = "".join(cell.get("source", []))
        match = re.search(r'b64decode\("([^"]+)"\)', source)
        if cell.get("cell_type") == "code" and match:
            return json.loads(zlib.decompress(base64.b64decode(match.group(1))))
    raise LookupError(f"no embedded panel assets found in {notebook}")


def render(assets: dict) -> dict[str, str]:
    """Return {file name: content} for every exported file."""
    files = {
        "panels.css": assets["css"] + SITE_THEME,
        "panels.js": assets["lib"] + PIN_LIGHT,
    }
    for name, widget in assets["widgets"].items():
        if name in SKIPPED:
            continue
        # On the website the panels sit in a lesson, not a notebook.
        widget = widget.replace("this notebook", "this lesson")
        files[f"{name}.html"] = PAGE.format(title=TITLES.get(name, name), widget=widget)
    return files


def main() -> int:
    files = render(load_assets())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (OUTPUT / name).write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} files to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
