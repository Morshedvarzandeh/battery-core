"""Static checks for the public Battery Core course homepage."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOMEPAGE = ROOT / "docs" / "index.html"
STYLESHEET = ROOT / "docs" / "assets" / "site.css"


def test_course_homepage_assets_exist() -> None:
    assert HOMEPAGE.is_file()
    assert STYLESHEET.is_file()


def test_course_homepage_uses_local_styles() -> None:
    html = HOMEPAGE.read_text(encoding="utf-8")
    assert 'href="assets/site.css"' in html
    assert "<script" not in html


def test_course_homepage_links_available_modules() -> None:
    html = HOMEPAGE.read_text(encoding="utf-8")
    assert 'href="fundamentals/cell-anatomy-workbench/"' in html
    assert 'href="fundamentals/lithium-ion-cell-architecture/"' in html
    assert 'href="fundamentals/battery-production/"' in html
    assert 'href="labs/battery-materials-lab/"' in html
    assert "notebooks/fundamentals/02_capacity_and_c_rate.ipynb" in html
    assert "notebooks/fundamentals/04_battery_aging.ipynb" in html
    assert "notebooks/transport/ficks_first_law.ipynb" in html


def test_course_homepage_distinguishes_available_and_planned_parts() -> None:
    html = HOMEPAGE.read_text(encoding="utf-8")
    assert html.count('<span class="status">Available</span>') == 5
    assert '<span class="status">Planned</span>' in html
    assert "Equivalent Circuit Models" in html
    assert "Battery production" in html
    assert "Battery aging" in html


def test_course_homepage_has_accessibility_and_metadata() -> None:
    html = HOMEPAGE.read_text(encoding="utf-8")
    assert 'href="#main-content"' in html
    assert 'id="main-content"' in html
    assert 'name="description"' in html
    assert 'aria-label="Primary navigation"' in html
