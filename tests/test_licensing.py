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
LICENSE_PAGE = ROOT / "docs" / "license" / "index.html"
LICENSE_PAGE_TEXT = ROOT / "docs" / "license" / "agpl-3.0.txt"
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
    # The metadata may point either at the file that ships in the wheel or at
    # the site's own licensing page. Both are real routes to the offer; what
    # matters is that whichever one is named actually exists.
    commercial_url = urls["Commercial-License"]
    if "license/#commercial" in commercial_url:
        page = (ROOT / "docs" / "license" / "index.html").read_text(encoding="utf-8")
        assert 'id="commercial"' in page, "metadata points at a section the page lacks"
    else:
        assert "COMMERCIAL.md" in commercial_url
        assert COMMERCIAL.exists()
    license_files = pyproject["tool"]["setuptools"]["license-files"]
    assert "COMMERCIAL.md" in license_files

    # The site reaches the commercial terms through its own licensing page
    # rather than sending a reader to a code host. Either route counts, so long
    # as every page has one.
    for path in SITE_PAGES:
        html = path.read_text(encoding="utf-8")
        assert "COMMERCIAL.md" in html or "license/#commercial" in html, path.name
    for path in CHROME_SOURCES[1:]:
        text = path.read_text(encoding="utf-8")
        assert "COMMERCIAL.md" in text or "license/#commercial" in text, path.name


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


def test_site_hosts_its_own_licence_page() -> None:
    """A reader should be able to read the terms without leaving the site, and
    without being handed off to whichever account happens to host the code."""
    assert LICENSE_PAGE.is_file()
    assert LICENSE_PAGE_TEXT.is_file()
    html = LICENSE_PAGE.read_text(encoding="utf-8")
    assert "dual-licensed by Lemonergy" in html
    assert 'id="commercial"' in html
    assert 'href="agpl-3.0.txt"' in html
    # The same line COMMERCIAL.md draws, drawn the same way.
    assert "modified</em> versions offered over a network" in html
    assert "cannot be withdrawn" in html
    # The hosted copy must be the licence itself, not a summary of it.
    body = LICENSE_PAGE_TEXT.read_text(encoding="utf-8")
    assert body == LICENSE.read_text(encoding="utf-8")


def test_licence_chrome_names_no_individual() -> None:
    """The footers carry Lemonergy, and the licence route they offer stays on
    this site. Neither should reach for a person's account."""
    for path in [*SITE_PAGES, LICENSE_PAGE]:
        html = path.read_text(encoding="utf-8")
        footer = html[html.rfind("<footer") :]
        assert "A project of Lemonergy" in footer, path.name
        assert "github.com" not in footer.lower(), (
            f"{path.name}: the footer should not hand a reader to a code host"
        )


def test_site_never_hands_a_reader_to_a_code_host() -> None:
    """The site is Lemonergy's. Nothing a reader can click should take them to
    an individual's account, so the licence and the roadmap are hosted here
    rather than linked out to wherever the code happens to live."""
    docs = ROOT / "docs"
    offenders = []
    for path in [*docs.rglob("*.html"), *docs.rglob("*.js")]:
        if "payload" in path.parts:
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for line_no, line in enumerate(lines, 1):
            if "github.com" in line:
                offenders.append(f"{path.relative_to(ROOT)}:{line_no}")
    assert not offenders, "github.com links on the site: " + ", ".join(offenders)


def test_site_hosts_the_roadmap_it_links_to() -> None:
    roadmap = ROOT / "docs" / "roadmap" / "index.html"
    assert roadmap.is_file()
    html = roadmap.read_text(encoding="utf-8")
    assert "Battery cell foundations" in html
    assert "Equivalent circuit models" in html
    docs = ROOT / "docs"
    for page in (docs / "index.html", docs / "chapter-1" / "index.html"):
        assert "roadmap/" in page.read_text(encoding="utf-8"), page.name


def test_the_site_declares_the_domain_it_is_served_from() -> None:
    """GitHub Pages reads docs/CNAME to decide which hostname it will answer on.
    It has to be a bare hostname on one line — a scheme, a path, or a trailing
    slash makes Pages reject it, and the site silently falls back to the
    default host, which is exactly the personal one we moved off."""
    cname = (ROOT / "docs" / "CNAME").read_text(encoding="utf-8")
    lines = [line for line in cname.splitlines() if line.strip()]
    assert len(lines) == 1, f"CNAME must hold exactly one hostname, got {lines}"
    host = lines[0]
    assert host == host.strip(), "CNAME hostname has surrounding whitespace"
    assert "://" not in host and "/" not in host, f"CNAME must be a bare host: {host}"
    assert host.endswith(".lemonergy.com") or host == "lemonergy.com", host


def test_every_canonical_url_points_at_the_domain_the_site_is_served_from() -> None:
    """A canonical tag tells search engines which URL is the real one. If the
    CNAME moves and a canonical is left behind, that page hands its ranking to
    a host we no longer serve, so the two have to be checked together."""
    host = (ROOT / "docs" / "CNAME").read_text(encoding="utf-8").strip()
    expected = f"https://{host}/"
    offenders = []
    for path in (ROOT / "docs").rglob("*.html"):
        if "payload" in path.parts:
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if 'rel="canonical"' in line and expected not in line:
                offenders.append(f"{path.relative_to(ROOT)}:{line_no}")
    assert not offenders, f"canonical URLs not on {expected}: " + ", ".join(offenders)


def test_nothing_published_points_a_reader_at_a_personal_pages_host() -> None:
    """The whole point of the custom domain is that a reader never lands on an
    individual's github.io. That holds only if no page, and no packaging
    metadata, still carries the old host."""
    targets = [
        *(ROOT / "docs").rglob("*.html"),
        *(ROOT / "docs").rglob("*.js"),
        *(ROOT / "docs").rglob("*.md"),
        ROOT / "README.md",
        ROOT / "pyproject.toml",
    ]
    offenders = []
    for path in targets:
        if "payload" in path.parts:
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "github.io" in line:
                offenders.append(f"{path.relative_to(ROOT)}:{line_no}")
    assert not offenders, "github.io references remain: " + ", ".join(offenders)
