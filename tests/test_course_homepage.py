"""Static checks for the public Battery Core course homepage."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOMEPAGE = ROOT / "docs" / "index.html"
CHAPTER_GUIDE = ROOT / "docs" / "chapter-1" / "index.html"
STYLESHEET = ROOT / "docs" / "assets" / "site.css"


def test_course_homepage_assets_exist() -> None:
    assert HOMEPAGE.is_file()
    assert CHAPTER_GUIDE.is_file()
    assert STYLESHEET.is_file()


def test_course_homepage_uses_local_styles() -> None:
    html = HOMEPAGE.read_text(encoding="utf-8")
    assert 'href="assets/site.css"' in html
    assert "<script" not in html


def test_course_homepage_links_available_modules() -> None:
    html = HOMEPAGE.read_text(encoding="utf-8")
    assert 'href="chapter-1/"' in html
    assert 'href="fundamentals/cell-anatomy-workbench/"' in html
    assert 'href="fundamentals/lithium-ion-cell-architecture/"' in html
    assert 'href="fundamentals/battery-production/"' in html
    assert 'href="fundamentals/solid-state-production/"' in html
    assert 'href="labs/battery-materials-lab/"' in html
    assert "notebooks/fundamentals/02_capacity_and_c_rate.ipynb" in html
    assert "notebooks/fundamentals/04_battery_aging.ipynb" in html
    assert "notebooks/transport/ficks_first_law.ipynb" in html


def test_course_homepage_distinguishes_available_and_planned_parts() -> None:
    html = HOMEPAGE.read_text(encoding="utf-8")
    assert html.count('<span class="status">Available</span>') == 6
    assert '<span class="status">Planned</span>' in html
    assert "Equivalent Circuit Models" in html
    assert "Battery production" in html
    assert "All-solid-state cell production" in html
    assert "Battery aging" in html


def test_course_homepage_has_accessibility_and_metadata() -> None:
    html = HOMEPAGE.read_text(encoding="utf-8")
    assert 'href="#main-content"' in html
    assert 'id="main-content"' in html
    assert 'name="description"' in html
    assert 'aria-label="Primary navigation"' in html


def test_chapter_1_guide_uses_course_design_and_complete_sequence() -> None:
    html = CHAPTER_GUIDE.read_text(encoding="utf-8")
    assert 'href="../assets/site.css"' in html
    assert 'href="#main-content"' in html
    assert 'id="main-content"' in html
    assert 'aria-label="Primary navigation"' in html
    assert 'role="progressbar"' in html
    assert 'aria-valuenow="6"' in html
    assert html.count('<article class="study-step') == 6
    for part in ("01", "01B", "02", "03", "03B", "04"):
        assert f"<strong>{part}</strong>" in html


def test_chapter_1_guide_links_every_module() -> None:
    html = CHAPTER_GUIDE.read_text(encoding="utf-8")
    assert 'href="../fundamentals/cell-anatomy-workbench/"' in html
    assert 'href="../fundamentals/lithium-ion-cell-architecture/"' in html
    assert 'href="../fundamentals/battery-production/"' in html
    assert 'href="../fundamentals/solid-state-production/"' in html
    assert "notebooks/fundamentals/02_capacity_and_c_rate.ipynb" in html
    assert "notebooks/fundamentals/04_battery_aging.ipynb" in html
