"""Static checks for the CellForge visual layout editor."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITOR = ROOT / "docs" / "tools" / "cellforge-visual-editor" / "index.html"
STATIONS = ("coating", "calendering", "template")


class _EditorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[str] = []
        self.script_sources: list[str] = []
        self.stylesheets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for name in ("for", "aria-controls", "aria-labelledby", "aria-describedby"):
            if values.get(name):
                self.references.extend((values[name] or "").split())
        if tag == "script" and values.get("src"):
            self.script_sources.append(values["src"] or "")
        if tag == "link" and values.get("rel") == "stylesheet":
            self.stylesheets.append(values.get("href") or "")


def _parsed() -> _EditorParser:
    parser = _EditorParser()
    parser.feed(EDITOR.read_text(encoding="utf-8"))
    return parser


def test_editor_is_accessible_and_structurally_complete() -> None:
    assert EDITOR.is_file()
    source = EDITOR.read_text(encoding="utf-8")
    parser = _parsed()
    assert len(parser.ids) == len(set(parser.ids))
    assert set(parser.references).issubset(set(parser.ids))
    for station in STATIONS:
        assert f'data-station="{station}"' in source
    assert 'aria-label="Editable CellForge production machine diagram"' in source
    assert 'href="#main-content"' in source
    assert 'id="main-content"' in source


def test_editor_uses_the_course_design_system() -> None:
    """The editor shipped with its own palette and three CDN scripts. A page
    that styles itself cannot stay in step with the rest of the course, and an
    external script is the one thing no other page in `docs/` loads."""
    parser = _parsed()
    assert parser.stylesheets == ["../../assets/site.css"]
    assert parser.script_sources == []
    source = EDITOR.read_text(encoding="utf-8")
    assert "unpkg.com" not in source
    assert "light-dark(" not in source
    assert 'data-tier="toolkit"' in source


def test_editor_carries_the_licence_attribution() -> None:
    source = EDITOR.read_text(encoding="utf-8")
    assert "A project of Lemonergy" in source
    assert "AGPL-3.0-or-later" in source


def test_editor_offers_a_standard_template_station() -> None:
    """The template is the reason a new diagram starts on the course grid
    instead of a blank canvas, so it needs the zones, the web line, the
    placeholder machines, and the state badges it promises."""
    source = EDITOR.read_text(encoding="utf-8")
    assert 'data-station="template"' in source
    assert ">Standard template<" in source
    for zone in ("INFEED", "PROCESS STEP", "INLINE QUALITY CONTROL", "OUTFEED"):
        assert zone in source
    for placeholder in (
        "Input reel",
        "Feed unit",
        "Process head",
        "Drive roll",
        "Inspection camera",
        "inline gauge",
        "Output reel",
    ):
        assert placeholder in source
    for badge in ("INPUT STATE", "IN-PROCESS STATE", "OUTPUT STATE"):
        assert badge in source


def test_editor_preserves_changes_and_exports_without_silent_failure() -> None:
    source = EDITOR.read_text(encoding="utf-8")
    assert 'localStorage.setItem("cellforge-layout-draft"' in source
    assert "navigator.clipboard.writeText" in source
    assert 'document.execCommand("copy")' in source
    assert "Clipboard blocked — select the text above and copy it" in source
    assert 'link.download="cellforge-layout-changes.json"' in source
    assert 'id="cf-export-status" role="status" aria-live="polite"' in source
    assert "window.openai" not in source


def test_editor_exports_every_station() -> None:
    """The export is keyed by station. Deriving the keys from the diagram set
    is what stops a fourth diagram from being silently left out of it."""
    source = EDITOR.read_text(encoding="utf-8")
    assert "const STATIONS=Object.keys(machines);" in source
    export = 'STATIONS.forEach(name=>{layouts[name]=collectChanges(saved[name]||"");});'
    assert export in source


def test_editor_has_mobile_sections_and_collision_feedback() -> None:
    source = EDITOR.read_text(encoding="utf-8")
    assert 'id="cf-mobile-nav" role="group" hidden' in source
    assert "Section 1 of 3" in source
    assert "root.clientWidth<600" in source
    assert "No label collisions" in source
    assert "cf-collision" in source
    # The mobile viewBox and the aspect ratio must key off the same signal;
    # a CSS media query keys off the viewport and the two disagree.
    assert 'svg.style.aspectRatio="340 / 318"' in source
    assert 'svg.style.aspectRatio="980 / 318"' in source
