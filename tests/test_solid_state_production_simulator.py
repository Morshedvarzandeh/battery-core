"""Static checks for the all-solid-state production learning simulator."""

import re
from html.parser import HTMLParser
from pathlib import Path

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


def test_loader_and_payload_exist() -> None:
    assert HTML.is_file()
    assert LOADER.is_file()
    assert all(path.is_file() for path in _parts())
    assert sorted(path.name for path in PAYLOAD.glob("source-*.part")) == sorted(
        EXPECTED_PARTS
    )
    html = HTML.read_text(encoding="utf-8")
    loader = LOADER.read_text(encoding="utf-8")
    assert 'src="loader.js"' in html
    for path in _parts():
        assert f"payload/{path.name}" in loader
    assert "fetch(path)" in loader


def test_reconstructed_page_has_accessible_structure() -> None:
    source = _source()
    parser = _StructureParser()
    parser.feed(source)
    assert parser.h1_count == 1
    assert len(parser.ids) == len(set(parser.ids))
    assert set(parser.references).issubset(set(parser.ids))


def test_guided_tour_is_an_accessible_modal() -> None:
    """The tour is a modal dialog labelled by its own live heading and body."""
    source = _source()
    assert 'role="dialog"' in source
    assert 'aria-modal="true"' in source
    assert 'aria-labelledby="tourTitle"' in source
    assert 'aria-describedby="tourText"' in source


def test_electrolyte_classes_and_process_stages_are_present() -> None:
    source = _source()
    for route in ("oxide", "sulfide", "halide", "polymer"):
        assert f'data-route="{route}"' in source
    for station in (
        "ballmill", "mixing", "compounding", "calender", "drycoat",
        "sintering", "stacking", "contacting", "formation",
    ):
        assert f'id:"{station}"' in source


def test_solid_state_scope_is_explicit() -> None:
    """Nothing here may read as a calibrated model of a production line."""
    source = _source()
    assert "All-Solid-State Cell Production Simulator" in source
    assert "illustrative teaching relationships" in source
    assert "not calibrated plant predictions" in source
    assert "no solid-state line is in series production" in source
    assert "teaching score, not a yield prediction" in source
    assert "digital twin" not in source.lower()


def test_standalone_page_uses_no_external_code_assets() -> None:
    source = _source()
    assert not re.search(r"<script[^>]+src=[\"\']https?://", source)
    assert not re.search(r"<link[^>]+href=[\"\']https?://", source)
