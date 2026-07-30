from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "labs" / "battery-materials-lab" / "index.html"


class _Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.aria_refs: list[str] = []
        self.external_scripts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        data = dict(attrs)
        element_id = data.get("id")
        if element_id:
            self.ids.append(element_id)

        aria_labelledby = data.get("aria-labelledby")
        if aria_labelledby:
            self.aria_refs.extend(aria_labelledby.split())

        script_source = data.get("src")
        if tag == "script" and script_source:
            self.external_scripts.append(script_source)


def test_battery_materials_lab_is_self_contained_and_scoped() -> None:
    text = PAGE.read_text(encoding="utf-8")
    parser = _Parser()
    parser.feed(text)

    assert len(parser.ids) == len(set(parser.ids))
    assert set(parser.aria_refs) <= set(parser.ids)
    assert parser.external_scripts == []
    assert 'let negativeId = "zn"' in text
    assert 'let positiveId = "cu"' in text
    assert "Active-material-only estimate" in text
    assert "Read the table as half-reactions" in text
    assert "nothing dissolves" not in text
    assert "within microseconds" not in text
    assert "unpkg.com" not in text


def test_course_homepage_links_to_battery_materials_lab() -> None:
    homepage = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert 'href="labs/battery-materials-lab/"' in homepage
