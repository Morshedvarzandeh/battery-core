"""Static checks for the standalone CellForge visual layout editor."""

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITOR = ROOT / "docs" / "tools" / "cellforge-visual-editor" / "index.html"


class _EditorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for name in ("for", "aria-controls", "aria-labelledby", "aria-describedby"):
            if values.get(name):
                self.references.extend((values[name] or "").split())


def test_editor_is_accessible_and_structurally_complete() -> None:
    assert EDITOR.is_file()
    source = EDITOR.read_text(encoding="utf-8")
    parser = _EditorParser()
    parser.feed(source)
    assert len(parser.ids) == len(set(parser.ids))
    assert set(parser.references).issubset(set(parser.ids))
    assert 'data-station="coating"' in source
    assert 'data-station="calendering"' in source
    assert 'aria-label="Editable CellForge production machine diagram"' in source


def test_editor_preserves_changes_and_exports_without_silent_failure() -> None:
    source = EDITOR.read_text(encoding="utf-8")
    assert 'localStorage.setItem("cellforge-layout-draft"' in source
    assert "navigator.clipboard.writeText" in source
    assert 'document.execCommand("copy")' in source
    assert "Clipboard blocked — select the text above and copy it" in source
    assert 'link.download="cellforge-layout-changes.json"' in source
    assert 'id="cf-export-status" role="status" aria-live="polite"' in source
    assert "window.openai" not in source


def test_editor_has_mobile_sections_and_collision_feedback() -> None:
    source = EDITOR.read_text(encoding="utf-8")
    assert 'id="cf-mobile-nav" hidden' in source
    assert 'Section 1 of 3' in source
    assert 'root.clientWidth<600' in source
    assert "No label collisions" in source
    assert "cf-collision" in source
