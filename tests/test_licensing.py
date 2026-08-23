"""Checks that the licensing stays intact and internally consistent.

The project is dual-licensed. The free option is AGPL-3.0-or-later plus one
additional term permitted by section 7(b) of that licence: the attribution to
Lemonergy must stay visible. That term only works if the notice actually
travels — with the source, with every built distribution, and in the Appropriate
Legal Notices of the pages themselves.

The commercial option only works if two other things hold: the offer is
discoverable from wherever someone lands, and contributed code carries an
inbound grant. Without the grant, Lemonergy cannot license a contributor's work
commercially, and the dual model quietly breaks the first time someone else
sends a patch.
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
COMMERCIAL = ROOT / "COMMERCIAL.md"
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
    assert {"LICENSE", "NOTICE"}.issubset(set(license_files))


def test_readme_points_at_both_the_licence_and_the_term() -> None:
    text = README.read_text(encoding="utf-8")
    assert "AGPL" in text
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


def test_commercial_option_is_documented() -> None:
    assert COMMERCIAL.is_file()
    text = COMMERCIAL.read_text(encoding="utf-8")
    assert "dual-licensed by Lemonergy" in text
    # The line between free and paid is the whole point of the page, so both
    # sides of it have to be spelled out rather than left to be guessed.
    assert "You are fine under the open licence" in text
    assert "You need a commercial licence if you want to" in text
    # Unmodified network use does not trigger section 13; saying otherwise
    # would overclaim what the licence actually requires.
    assert "modified* versions offered" in text or "*modified*" in text


def test_commercial_offer_is_reachable_from_the_metadata_and_the_site() -> None:
    """Someone who needs to pay has to be able to find out that they can."""
    pyproject = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    urls = pyproject["project"]["urls"]
    assert "COMMERCIAL.md" in urls["Commercial-License"]
    license_files = pyproject["tool"]["setuptools"]["license-files"]
    assert "COMMERCIAL.md" in license_files

    for path in SITE_PAGES:
        html = path.read_text(encoding="utf-8")
        assert "COMMERCIAL.md" in html, path.name
    for path in CHROME_SOURCES[1:]:
        text = path.read_text(encoding="utf-8")
        assert "COMMERCIAL.md" in text, path.name


def test_contributions_carry_an_inbound_grant() -> None:
    """Dual licensing needs the right to relicense contributed code. Without a
    stated inbound grant the model breaks on the first outside patch."""
    commercial = COMMERCIAL.read_text(encoding="utf-8")
    assert "## Contributions" in commercial
    assert "royalty-free right to licence" in commercial
    assert "AGPL-only" in commercial, "a contributor must be able to decline"

    readme = README.read_text(encoding="utf-8")
    assert "dual-licensed" in readme
    assert "COMMERCIAL.md" in readme

    notice = NOTICE.read_text(encoding="utf-8")
    assert "Dual licensing" in notice
    assert "COMMERCIAL.md" in notice


def test_licence_change_scope_is_stated_honestly() -> None:
    """Relicensing is forward-looking. Versions already released under MIT stay
    MIT for whoever holds them, and saying otherwise would misrepresent what
    the change achieves."""
    text = COMMERCIAL.read_text(encoding="utf-8")
    assert "cannot be withdrawn" in text
    assert "MIT" in text
