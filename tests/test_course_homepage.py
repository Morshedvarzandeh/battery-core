"""Static checks for the public Battery Core course pages."""

from pathlib import Path

from asset_checks import external_asset_references

ROOT = Path(__file__).resolve().parents[1]
HOMEPAGE = ROOT / "docs" / "index.html"
CHAPTER_GUIDE = ROOT / "docs" / "chapter-1" / "index.html"
EDITOR = ROOT / "docs" / "tools" / "cellforge-visual-editor" / "index.html"
ASSETS = ROOT / "docs" / "assets"
STYLESHEET = ASSETS / "site.css"
PAGES = (HOMEPAGE, CHAPTER_GUIDE, EDITOR)


def test_course_homepage_assets_exist() -> None:
    assert HOMEPAGE.is_file()
    assert CHAPTER_GUIDE.is_file()
    assert STYLESHEET.is_file()


def test_design_system_ships_all_three_levels() -> None:
    """The template is the level a new page starts from; the bridge and the
    chrome are what a page with its own stylesheet uses instead. A missing one
    sends the next page back to inventing its own palette."""
    levels = ("page-template.html", "module-theme.css", "site-chrome.css", "README.md")
    for name in levels:
        assert (ASSETS / name).is_file(), name


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
    assert 'href="tools/cellforge-visual-editor/"' in html
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


def test_course_homepage_keeps_the_toolkit_out_of_the_module_count() -> None:
    """The layout editor builds the course rather than teaching it, so it
    carries its own status. Counting it as an available module would overstate
    how much of Chapter 1 there is to learn."""
    html = HOMEPAGE.read_text(encoding="utf-8")
    assert html.count('<span class="status">Toolkit</span>') == 1
    assert "CellForge layout editor" in html
    assert 'class="module-card available toolkit"' in html


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
    # Four core parts, two deeper views, and one toolkit entry.
    assert html.count('<article class="study-step">') == 4
    assert html.count("study-step-deeper") == 2
    assert html.count("study-step-toolkit") == 1
    for part in ("01", "01B", "02", "03", "03B", "04"):
        assert f"<strong>{part}</strong>" in html


def test_chapter_1_guide_links_every_module() -> None:
    html = CHAPTER_GUIDE.read_text(encoding="utf-8")
    assert 'href="../fundamentals/cell-anatomy-workbench/"' in html
    assert 'href="../fundamentals/lithium-ion-cell-architecture/"' in html
    assert 'href="../fundamentals/battery-production/"' in html
    assert 'href="../fundamentals/solid-state-production/"' in html
    assert 'href="../tools/cellforge-visual-editor/"' in html
    assert "notebooks/fundamentals/02_capacity_and_c_rate.ipynb" in html
    assert "notebooks/fundamentals/04_battery_aging.ipynb" in html


def test_both_index_pages_state_the_colour_roles() -> None:
    """A tier is only legible if the page says what the tiers are, so the
    legend is part of the design rather than an optional caption."""
    for path in (HOMEPAGE, CHAPTER_GUIDE):
        html = path.read_text(encoding="utf-8")
        assert 'class="tier-legend"' in html, path.name
        for tier in ("Core path", "Deeper view", "Toolkit"):
            assert tier in html, (path.name, tier)


def test_pages_fetch_nothing_from_another_host() -> None:
    for path in PAGES:
        html = path.read_text(encoding="utf-8")
        assert external_asset_references(html) == [], path.name


def test_pages_carry_the_licence_attribution() -> None:
    """The footer is the Appropriate Legal Notice required by the additional
    term in NOTICE, so it is not decoration and must not be dropped."""
    for path in PAGES:
        html = path.read_text(encoding="utf-8")
        assert "A project of Lemonergy" in html, path.name
        assert "AGPL-3.0-or-later" in html, path.name
        assert "MIT License" not in html, path.name
