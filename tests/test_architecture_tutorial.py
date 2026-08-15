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

"""Static checks for the Lithium-ion Cell Architecture tutorial."""

import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TUTORIAL = ROOT / "docs" / "fundamentals" / "lithium-ion-cell-architecture"


class _StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for attribute in ("aria-labelledby", "aria-describedby"):
            if values.get(attribute):
                self.references.extend((values[attribute] or "").split())


def _read(name: str) -> str:
    return (TUTORIAL / name).read_text(encoding="utf-8")


def test_architecture_tutorial_assets_exist() -> None:
    for name in ("index.html", "styles.css", "app.js", "README.md"):
        assert (TUTORIAL / name).is_file()


def test_architecture_tutorial_uses_only_local_assets() -> None:
    html = _read("index.html")
    assert 'href="styles.css"' in html
    assert 'src="app.js"' in html
    # no asset may be pulled from the network; a URL in prose or in the
    # licence header is not an asset reference
    assert 'src="https://' not in html
    assert 'href="https://' not in html
    assert "url(https://" not in html
    assert "unpkg.com" not in _read("styles.css") + _read("app.js")


def test_architecture_tutorial_is_layer_first_and_conceptual() -> None:
    html = _read("index.html")
    for text in (
        "Step 1 · Assemble the five physical layers",
        "The electrolyte matters — but it is not layer 6.",
        "Step 2 · Zoom into one selected layer",
        "Step 3 · Enter the liquid inside a selected pore",
        "Conceptual visualization only",
        "does not represent",
    ):
        assert text in html


def test_architecture_tutorial_contains_reviewed_interactions() -> None:
    html = _read("index.html")
    javascript = _read("app.js")
    for text in (
        "Component under pointer",
        "Take me to a porous layer",
        "Zoom into pore electrolyte",
        "Associated pair",
        "Separate ions",
        "Orient solvent",
        "Electronic path",
        "Ionic path",
    ):
        assert text in html
    for molecule in ("EC", "PC", "DMC", "EMC", "DEC"):
        assert re.search(rf"\b{molecule}: \{{", javascript)


def test_architecture_tutorial_contains_all_five_layers() -> None:
    javascript = _read("app.js")
    for layer in (
        "Negative current collector",
        "Negative composite electrode",
        "Separator",
        "Positive composite electrode",
        "Positive current collector",
    ):
        assert layer in javascript
    assert "Copper current collector" in javascript
    assert "Aluminium current collector" in javascript


def test_architecture_tutorial_has_valid_accessibility_references() -> None:
    html = _read("index.html")
    parser = _StructureParser()
    parser.feed(html)
    assert len(parser.ids) == len(set(parser.ids))
    assert not (set(parser.references) - set(parser.ids))
    assert 'role="tablist"' in html
    assert 'aria-live="polite"' in html
    assert 'href="#cell-architecture"' in html


def test_scientific_qualifications_are_present() -> None:
    combined = _read("index.html") + _read("app.js") + _read("README.md")
    assert "shutdown behavior is not universal" in combined
    assert "does not prevent every failure mode" in combined
    assert "coordination" in combined
    assert "composition, concentration and temperature" in combined
    assert "not a sixth structural layer" in combined
