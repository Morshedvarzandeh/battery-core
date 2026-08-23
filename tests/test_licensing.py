"""Checks that the licence and its attribution term stay intact.

The project is AGPL-3.0-or-later with one additional term permitted by section
7(b) of that licence: the attribution to Lemonergy must stay visible. That term
only works if the notice actually travels — with the source, with every built
distribution, and in the Appropriate Legal Notices of the pages themselves.
"""

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:  # Python 3.10 has no tomllib; the project still supports it.
    import tomli as tomllib

ROOT = Path(__file__).resolve().parents[1]
LICENSE = ROOT / "LICENSE"
NOTICE = ROOT / "NOTICE"
README = ROOT / "README.md"
PYPROJECT = ROOT / "pyproject.toml"

SITE_PAGES = (
    ROOT / "docs" / "index.html",
    ROOT / "docs" / "chapter-1" / "index.html",
    ROOT / "docs" / "tools" / "cellforge-visual-editor" / "index.html",
    ROOT / "docs" / "assets" / "page-template.html",
)
CHROME_SOURCES = (
    ROOT / "docs" / "assets" / "site-chrome.css",
    ROOT / "docs" / "fundamentals" / "cell-anatomy-workbench" / "index.html",
    ROOT / "docs" / "fundamentals" / "lithium-ion-cell-architecture" / "index.html",
    ROOT / "docs" / "labs" / "battery-materials-lab" / "index.html",
    ROOT / "docs" / "fundamentals" / "battery-production" / "loader.js",
    ROOT / "docs" / "fundamentals" / "solid-state-production" / "loader.js",
)


def test_license_is_the_agpl_verbatim() -> None:
    text = LICENSE.read_text(encoding="utf-8")
    assert text.startswith("                    GNU AFFERO GENERAL PUBLIC LICENSE")
    assert "Version 3, 19 November 2007" in text
    # Section 13 is what distinguishes the AGPL from the GPL.
    section_13 = "13. Remote Network Interaction; Use with the GNU General Public"
    assert section_13 in text
    assert "MIT License" not in text
    # The licence text itself must stay unmodified: additional terms belong in
    # NOTICE, because section 7 treats them as separate from this document.
    assert "Lemonergy" not in text


def test_notice_states_the_attribution_term() -> None:
    text = NOTICE.read_text(encoding="utf-8")
    assert "Copyright (C) 2026 Lemonergy" in text
    assert "section 7(b)" in text
    assert "Battery Core is a project of Lemonergy." in text
    assert "Appropriate Legal Notices" in text


def test_packaging_metadata_names_the_licence_and_ships_the_notice() -> None:
    pyproject = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    project = pyproject["project"]
    classifiers = project["classifiers"]
    assert any("Affero" in item for item in classifiers)
    assert not any("MIT" in item for item in classifiers)
    assert any(author["name"] == "Lemonergy" for author in project["authors"])
    license_files = pyproject["tool"]["setuptools"]["license-files"]
    assert set(license_files) == {"LICENSE", "NOTICE"}


def test_readme_points_at_both_the_licence_and_the_term() -> None:
    text = README.read_text(encoding="utf-8")
    assert "GNU Affero General Public License" in text
    assert "NOTICE" in text
    assert "Lemonergy" in text
    assert "MIT License" not in text


def test_every_page_carries_the_attribution() -> None:
    for path in SITE_PAGES:
        text = path.read_text(encoding="utf-8")
        assert "A project of Lemonergy" in text, path.name
        assert "AGPL-3.0-or-later" in text, path.name


def test_module_pages_carry_the_shared_footer() -> None:
    """A module page is reached directly as often as it is reached from the
    course, so it needs the notice too — through the shared chrome rather than
    a copy of the markup in each page."""
    for path in CHROME_SOURCES:
        text = path.read_text(encoding="utf-8")
        assert "bc-footer" in text, path.name
    for path in CHROME_SOURCES[1:]:
        text = path.read_text(encoding="utf-8")
        assert "Lemonergy" in text, path.name
