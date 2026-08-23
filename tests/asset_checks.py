"""Shared check for pages that must fetch nothing from another host.

Every page under `docs/` loads only files that sit beside it: no CDN scripts,
no hosted fonts, no analytics. The blunt version of that check — asserting the
string ``https://`` never appears — also rejects hyperlinks, and every page
footer links the repository and the licence. A link costs the reader nothing
until they click it.

So these helpers look at what the browser actually fetches while rendering:
scripts, stylesheets, images, media, and frames, plus whatever CSS pulls in.
"""

import re
from html.parser import HTMLParser

_FETCHED_ATTRS = {
    "script": ("src",),
    "img": ("src", "srcset"),
    "source": ("src", "srcset"),
    "iframe": ("src",),
    "embed": ("src",),
    "object": ("data",),
    "video": ("src", "poster"),
    "audio": ("src",),
    "track": ("src",),
}

_CSS_URL = re.compile(r"""url\(\s*['"]?([^'")]+)""", re.IGNORECASE)
_CSS_IMPORT = re.compile(r"""@import\s+(?:url\(\s*)?['"]([^'"]+)""", re.IGNORECASE)


def _is_external(value: str) -> bool:
    value = value.strip()
    if not value or value.startswith(("data:", "#")):
        return False
    return value.startswith(("http://", "https://", "//"))


class _AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.assets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        for attr in _FETCHED_ATTRS.get(tag, ()):
            for part in values.get(attr, "").split(","):
                if part.strip():
                    self.assets.append(part.split()[0])
        if tag == "link":
            rel = values.get("rel", "").lower().split()
            if {"stylesheet", "icon", "preload", "prefetch", "preconnect"} & set(rel):
                self.assets.append(values.get("href", ""))


def external_asset_references(html: str) -> list[str]:
    """Return the asset URLs in ``html`` that point at another host."""
    parser = _AssetParser()
    parser.feed(html)
    found = [url for url in parser.assets if _is_external(url)]
    for style in re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I):
        found.extend(external_css_references(style))
    return found


def external_css_references(css: str) -> list[str]:
    """Return the URLs in ``css`` that point at another host."""
    urls = _CSS_URL.findall(css) + _CSS_IMPORT.findall(css)
    return [url for url in urls if _is_external(url)]
