"""Static checks for the SolidForge production learning simulator."""

from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "docs" / "fundamentals" / "solid-state-production"
HTML = MODULE / "index.html"
LOADER = MODULE / "loader.js"
PAYLOAD = MODULE / "payload"
EXPECTED_PARTS = [f"source-{index:02d}.part" for index in range(1, 24)]


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


def test_solid_state_loader_and_payload_exist() -> None:
    assert HTML.is_file()
    assert LOADER.is_file()
    parts = _parts()
    assert all(path.is_file() for path in parts)
    assert sorted(path.name for path in PAYLOAD.glob("source-*.part")) == EXPECTED_PARTS
    html = HTML.read_text(encoding="utf-8")
    loader = LOADER.read_text(encoding="utf-8")
    assert 'src="loader.js"' in html
    for path in parts:
        assert f"payload/{path.name}" in loader
    assert "fetch(path)" in loader


def test_reconstructed_solid_state_page_has_accessible_structure() -> None:
    source = _source()
    parser = _StructureParser()
    parser.feed(source)
    assert parser.h1_count == 1
    assert len(parser.ids) == len(set(parser.ids))
    assert set(parser.references).issubset(set(parser.ids))
    assert 'aria-modal="true"' in source
    assert 'aria-labelledby="tourTitle"' in source
    assert 'aria-describedby="tourText"' in source


def test_solid_state_scope_and_qualifications_are_explicit() -> None:
    source = _source()
    assert "All-Solid-State Cell Production Simulator" in source
    assert "3rd ed., February 2026" in source
    assert "not calibrated plant predictions" in source
    assert "illustrative teaching relationships" in source
    assert "does not eliminate lithium growth or short-circuit risk" in source
    assert "chemistry-specific moisture, toxicity and fire controls" in source
    assert "only usable because" not in source
    assert "impossible to cut mechanically" not in source
    assert "no liquid to short between" not in source
    assert "no flammable solvent" not in source


def test_solid_state_routes_and_process_stages_are_present() -> None:
    source = _source()
    for route in ("oxide", "halide", "sulfide", "polymer"):
        assert f'data-route="{route}"' in source
    for station in (
        "extrusion", "lamination", "mixing", "compounding", "tape",
        "calender", "compacting", "separation", "sintering", "stacking",
        "contacting", "formation",
    ):
        assert f'id:"{station}"' in source


def test_solid_state_page_uses_no_external_code_assets() -> None:
    source = _source()
    assert not re.search(r"<script[^>]+src=[\"\']https?://", source)
    assert not re.search(r"<link[^>]+href=[\"\']https?://", source)
