"""Static checks for the Battery Production learning simulator."""

from html.parser import HTMLParser
from pathlib import Path
import base64
import gzip
import json
import re


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "fundamentals" / "battery-production"
HTML = MODULE / "index.html"
LOADER = MODULE / "loader.js"
PAYLOAD = MODULE / "payload"
DELTA_PARTS = [PAYLOAD / f"review-2026-s{index:02d}.delta" for index in range(1, 9)]
EXPECTED_PARTS = [
    "source-01.part", "source-02.part", "source-03.part",
    "source-04a.part", "source-04b.part",
    *[f"source-{index:02d}.part" for index in range(5, 19)],
]
EXISTING_REVIEW_HEADING = (
    '<h1 class="sr">CellForge — Lithium-ion Cell Production Simulator</h1>\n'
)


class _StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[str] = []
        self.h1_count = 0
        self.buttons_without_type = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for name in ("aria-labelledby", "aria-describedby", "aria-controls"):
            if values.get(name):
                self.references.extend((values[name] or "").split())
        if tag == "h1":
            self.h1_count += 1
        if tag == "button" and not values.get("type"):
            self.buttons_without_type += 1


def _parts() -> list[Path]:
    return [PAYLOAD / name for name in EXPECTED_PARTS]


def _apply_delta(source: str, operations: list[list[object]]) -> str:
    lines = source.splitlines(keepends=True)
    for start, end, replacement in reversed(operations):
        lines[int(start):int(end)] = list(replacement)
    return "".join(lines)


def _source() -> str:
    original = "".join(path.read_text(encoding="utf-8") for path in _parts())
    original = original.replace(EXISTING_REVIEW_HEADING, "", 1)
    packed_delta = "".join(path.read_text(encoding="utf-8") for path in DELTA_PARTS)
    operations = json.loads(gzip.decompress(base64.b64decode(packed_delta)))
    return _apply_delta(original, operations)


def test_production_loader_and_payload_exist() -> None:
    assert HTML.is_file()
    assert LOADER.is_file()
    assert all(path.is_file() for path in DELTA_PARTS)
    parts = _parts()
    assert all(path.is_file() for path in parts)
    html = HTML.read_text(encoding="utf-8")
    loader = LOADER.read_text(encoding="utf-8")
    assert 'src="loader.js"' in html
    for path in parts:
        assert f"payload/{path.name}" in loader
    for path in DELTA_PARTS:
        assert f"payload/{path.name}" in loader
    assert "normalizeReviewBase" in loader
    assert "applyLineDelta" in loader
    assert "DecompressionStream" in loader


def test_reconstructed_page_has_accessible_structure() -> None:
    source = _source()
    parser = _StructureParser()
    parser.feed(source)
    assert parser.h1_count == 1
    assert parser.buttons_without_type == 0
    assert len(parser.ids) == len(set(parser.ids))
    assert set(parser.references).issubset(set(parser.ids))
    assert 'aria-modal="true"' in source
    assert 'aria-labelledby="tourTitle"' in source
    assert 'aria-describedby="tourText"' in source
    assert "function closeTour()" in source
    assert "tourReturnFocus" in source
    assert "mobile-skip" in source
    assert 'href="#lesson-content"' in source


def test_production_scope_is_explicit() -> None:
    source = _source()
    assert "Lithium-ion Cell Production Simulator" in source
    assert "digital twin" not in source.lower()
    assert "graphite / NMC" in source
    assert "not calibrated plant predictions" in source
    assert "Process-health score" in source
    assert "Illustrative SEI score" in source
    assert "Predicted yield" not in source
    assert "Safety margin" not in source


def test_wet_and_dry_routes_are_separate() -> None:
    source = _source()
    assert 'id:"mixing"' in source
    assert 'title:"Wet mixing and dispersing"' in source
    assert 'machine:"mixing", routes:ALL, proc:"wet"' in source
    assert 'id:"drymix"' in source
    assert 'title:"Dry mixing and fibrillation"' in source
    assert 'machine:"drymix", routes:ALL, proc:"dry"' in source
    assert 'id:"drycoat"' in source
    assert '{ id:"fibril", by:"drymix"' in source
    assert "four wet-processing stages" in source
    assert "replaced by two dry-processing stages" in source


def test_production_routes_and_process_stages_are_present() -> None:
    source = _source()
    for route in ("pouch", "cyl", "prism"):
        assert f'data-route="{route}"' in source
    for station in (
        "mixing", "drymix", "drycoat", "coating", "drying", "calendering",
        "slitting", "vacdry", "formation", "aging", "eol",
    ):
        assert f'id:"{station}"' in source
    assert 'id:"stacking"' in source
    assert 'id:"winding"' in source


def test_reference_recipe_and_temperatures_are_scoped() -> None:
    source = _source()
    assert "activeCathodeFrac = 0.95" in source
    assert "activeAnodeFrac = 0.95" in source
    assert 'label:"Pre-treatment temperature"' in source
    assert 'label:"Formation temperature assumption"' in source
    assert 'ctl:["pressP","soak","preT"]' in source
    assert 'ctl:["cRate","formT","vMax"]' in source
    assert "validated formation temperatures depend on chemistry" in source


def test_dry_route_cost_total_is_not_invented() -> None:
    source = _source()
    assert 't:"Dry mixing / fibrillation", lo:null, hi:null' in source
    assert 't:"Slitting share of combined range", lo:null, hi:null' in source
    assert "Not available from source" in source
    assert "A complete dry-route total is deliberately not calculated" in source
    assert "not a guaranteed complete-factory reduction" in source


def test_production_scientific_qualifications_are_present() -> None:
    source = _source()
    assert "formation should not be treated as a reliable correction" in source
    assert "does not guarantee prevention of thermal runaway" in source
    assert "Hard-case gas-management and closure sequences vary by design" in source
    assert "actual criteria depend on chemistry, SOC, temperature and test duration" in source
    assert "defined capacity test with specified charge, rest, discharge and cutoff conditions" in source
    assert "Example plant shipping target: 10%–20% SOC" in source
    assert "PI 965 maximum: 30% SOC for UN 3480 shipped alone by air" in source
    assert "not a universal acceptance limit" in source
    assert "does not by itself establish that the cell is safe" in source
    assert "water-based exhaust handling still depends on process emissions" in source


def test_standalone_page_uses_no_external_code_assets() -> None:
    source = _source()
    assert not re.search(r"<script[^>]+src=[\"']https?://", source)
    assert not re.search(r"<link[^>]+href=[\"']https?://", source)
