"""Static checks for the Battery Production learning simulator."""

from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "fundamentals" / "battery-production"
HTML = MODULE / "index.html"
LOADER = MODULE / "loader.js"
PAYLOAD = MODULE / "payload"
EXPECTED_PARTS = [
    "source-01.part", "source-02.part", "source-03.part",
    "source-04a.part", "source-04b.part",
    *[f"source-{index:02d}.part" for index in range(5, 19)],
]


class _StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[str] = []
        self.h1_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for name in ("aria-labelledby", "aria-describedby", "aria-controls"):
            if values.get(name):
                self.references.extend((values[name] or "").split())
        if tag == "h1":
            self.h1_count += 1


def _parts() -> list[Path]:
    return [PAYLOAD / name for name in EXPECTED_PARTS]


def _source() -> str:
    return "".join(path.read_text(encoding="utf-8") for path in _parts())


def test_production_loader_and_payload_exist() -> None:
    assert HTML.is_file()
    assert LOADER.is_file()
    parts = _parts()
    assert all(path.is_file() for path in parts)
    assert sorted(path.name for path in PAYLOAD.glob("source-*.part")) == sorted(EXPECTED_PARTS)
    html = HTML.read_text(encoding="utf-8")
    loader = LOADER.read_text(encoding="utf-8")
    assert 'src="loader.js"' in html
    for path in parts:
        assert f"payload/{path.name}" in loader
    assert "fetch(path)" in loader


def test_reconstructed_page_has_accessible_structure() -> None:
    source = _source()
    parser = _StructureParser()
    parser.feed(source)
    assert parser.h1_count == 1
    assert len(parser.ids) == len(set(parser.ids))
    assert set(parser.references).issubset(set(parser.ids))
    assert 'aria-modal="true"' in source
    assert 'aria-labelledby="tourTitle"' in source
    assert 'aria-describedby="tourText"' in source


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


def test_production_routes_and_process_stages_are_present() -> None:
    source = _source()
    for route in ("pouch", "cyl", "prism"):
        assert f'data-route="{route}"' in source
    for station in (
        "mixing", "coating", "drying", "calendering", "slitting",
        "vacdry", "formation", "aging", "eol",
    ):
        assert f'id:"{station}"' in source
    assert 'id:"stacking"' in source
    assert 'id:"winding"' in source


def test_production_scientific_qualifications_are_present() -> None:
    source = _source()
    assert "Vacuum-chamber evacuation ≈0.01 mbar" in source
    assert "Wetting-cycle pressure reference ≈150 mbar" in source
    assert "does not guarantee prevention of thermal runaway" in source
    assert "formation should not be treated as a reliable correction" in source
    assert "Hard-case gas-management and closure sequences vary by design" in source
    assert "actual criteria depend on chemistry, SOC, temperature and test duration" in source
    assert "defined capacity test with specified charge, rest, discharge and cutoff conditions" in source
    assert "Example plant shipping target: 10%–20% SOC" in source
    assert "PI 965 maximum: 30% SOC for UN 3480 shipped alone by air" in source


def test_standalone_page_uses_no_external_code_assets() -> None:
    source = _source()
    assert not re.search(r"<script[^>]+src=[\"\']https?://", source)
    assert not re.search(r"<link[^>]+href=[\"\']https?://", source)
