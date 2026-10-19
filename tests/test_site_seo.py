"""Site-wide checks for what search engines and link previews read.

A page that a search engine cannot find, or finds under two addresses, or
previews as a blank card, is a page fewer learners reach. These checks keep
the sitemap in step with the pages, give every page a canonical address and a
preview, keep the structured data valid JSON, and make sure no internal link
or fragment points at nothing.
"""

from __future__ import annotations

import importlib.util
import json
import re
import struct
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = "https://learn.lemonergy.com/"


def _sitemap_module():
    spec = importlib.util.spec_from_file_location(
        "build_sitemap", ROOT / "scripts" / "build_sitemap.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SITEMAP = _sitemap_module()
PAGES = SITEMAP.page_paths()


def _page(rel: str) -> Path:
    return DOCS / rel / "index.html"


def test_sitemap_lists_exactly_the_public_pages() -> None:
    """Add a page and forget the sitemap, and this fails. Re-run
    `python scripts/build_sitemap.py`."""
    sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
    listed = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    assert listed == [SITE + rel for rel in PAGES]


def test_robots_points_at_the_sitemap_and_allows_the_site() -> None:
    robots = (DOCS / "robots.txt").read_text(encoding="utf-8")
    assert f"Sitemap: {SITE}sitemap.xml" in robots
    assert "Disallow: /\n" not in robots


def test_custom_domain_matches_the_canonical_host() -> None:
    assert (DOCS / "CNAME").read_text(encoding="utf-8").strip() == urlsplit(
        SITE
    ).hostname


def test_jekyll_is_off_so_markdown_sources_are_not_rendered_as_pages() -> None:
    assert (DOCS / ".nojekyll").is_file()


@pytest.mark.parametrize("rel", PAGES, ids=lambda r: r or "home")
def test_page_has_canonical_description_and_preview(rel: str) -> None:
    html = _page(rel).read_text(encoding="utf-8")
    canonical = re.findall(r'<link rel="canonical" href="([^"]+)">', html)
    assert canonical == [SITE + rel]
    description = re.search(r'<meta name="description" content="([^"]+)">', html)
    assert description, "missing meta description"
    assert 50 <= len(description.group(1)) <= 260, len(description.group(1))
    for prop in ("og:title", "og:description", "og:image", "og:url"):
        assert f'property="{prop}"' in html, prop
    assert f'<meta property="og:url" content="{SITE + rel}">' in html
    assert re.search(r"<title>[^<]{10,}</title>", html)


@pytest.mark.parametrize("rel", PAGES, ids=lambda r: r or "home")
def test_structured_data_is_valid_json(rel: str) -> None:
    html = _page(rel).read_text(encoding="utf-8")
    for block in re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S
    ):
        data = json.loads(block)
        assert data["@context"] == "https://schema.org"


def test_social_image_is_the_recommended_size() -> None:
    image = DOCS / "assets" / "og-image.png"
    header = image.read_bytes()[:24]
    assert header[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", header[16:24])
    assert (width, height) == (1200, 630)


# --- Internal links ------------------------------------------------------------


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if tag in ("iframe", "script", "img") and values.get("src"):
            self.links.append(values["src"])
        if (
            tag == "link"
            and values.get("href")
            and "canonical" not in values.get("rel", "")
        ):
            self.links.append(values["href"])


def _parsed(path: Path) -> _Links:
    parser = _Links()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def _html_files() -> list[Path]:
    skip = ("payload", "page-template.html")
    return [
        p
        for p in sorted(DOCS.rglob("*.html"))
        if not any(s in p.as_posix() for s in skip)
    ]


def _resolve(source: Path, href: str) -> tuple[Path, str] | None:
    parts = urlsplit(href)
    if parts.scheme or parts.netloc or href.startswith(("mailto:", "javascript:")):
        return None
    if not parts.path:
        return source, parts.fragment
    base = DOCS if parts.path.startswith("/") else source.parent
    target = (base / parts.path.lstrip("/")).resolve()
    if target.is_dir():
        target = target / "index.html"
    return target, parts.fragment


@pytest.mark.parametrize(
    "page", _html_files(), ids=lambda p: p.relative_to(DOCS).as_posix()
)
def test_internal_links_and_fragments_resolve(page: Path) -> None:
    broken = []
    for href in _parsed(page).links:
        resolved = _resolve(page, href)
        if resolved is None:
            continue
        target, fragment = resolved
        if not target.exists():
            broken.append(href)
            continue
        if (
            fragment
            and target.suffix == ".html"
            and fragment not in _parsed(target).ids
        ):
            broken.append(href)
    assert broken == []


@pytest.mark.parametrize("rel", PAGES, ids=lambda r: r or "home")
def test_preview_image_exists_at_the_recommended_size(rel: str) -> None:
    """Each page may have its own link-preview image; whichever it names must
    be on the site, be a PNG and be 1200 by 630 pixels."""
    html = _page(rel).read_text(encoding="utf-8")
    url = re.search(r'<meta property="og:image" content="([^"]+)">', html)
    assert url and url.group(1).startswith(SITE + "assets/"), rel
    image = DOCS / url.group(1).removeprefix(SITE)
    header = image.read_bytes()[:24]
    assert header[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", header[16:24]) == (1200, 630)
    assert image.stat().st_size < 150_000
    alt = re.search(r'<meta property="og:image:alt" content="([^"]+)">', html)
    assert alt and len(alt.group(1)) > 10


@pytest.mark.parametrize("rel", PAGES, ids=lambda r: r or "home")
def test_every_local_image_exists(rel: str) -> None:
    page = _page(rel)
    html = page.read_text(encoding="utf-8")
    for src in re.findall(r'<img [^>]*src="([^"]+)"', html):
        assert not src.startswith(("http:", "https:", "//")), src
        assert (page.parent / src).resolve().is_file(), src


def test_lesson_illustrations_are_self_contained() -> None:
    art = sorted((DOCS / "assets" / "art").glob("*.svg"))
    assert len(art) >= 9
    for drawing in art:
        svg = drawing.read_text(encoding="utf-8")
        assert "<title>" in svg, drawing.name
        assert "href=" not in svg, drawing.name
