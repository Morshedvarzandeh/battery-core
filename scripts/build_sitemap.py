"""Write docs/sitemap.xml from the pages that exist under docs/.

Every `index.html` under `docs/` is a public page and goes in the sitemap,
except the ones search engines should not index on their own:

- `assets/` holds the page template, not a page;
- `fundamentals/battery-aging/panels/` are fragments embedded in the Part 04
  lesson, and each carries `<meta name="robots" content="noindex">`.

Run it from the repository root after adding or removing a page:

    python scripts/build_sitemap.py

`tests/test_site_seo.py` fails when the sitemap and the pages disagree.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = "https://learn.lemonergy.com/"
EXCLUDED_PREFIXES = ("assets/", "fundamentals/battery-aging/panels/")

# Higher for the pages a learner starts from; everything else is the default.
PRIORITY = {"": "1.0", "chapter-1/": "0.9", "glossary/": "0.7"}


def page_paths(docs: Path = DOCS) -> list[str]:
    """Return the site-relative path of every indexable page, sorted."""
    paths = []
    for page in docs.rglob("index.html"):
        rel = page.parent.relative_to(docs).as_posix()
        rel = "" if rel == "." else rel + "/"
        if rel.startswith(EXCLUDED_PREFIXES):
            continue
        paths.append(rel)
    return sorted(paths, key=lambda p: (p.count("/"), p))


def render(paths: list[str], lastmod: str) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for rel in paths:
        lines += [
            "  <url>",
            f"    <loc>{SITE}{rel}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            f"    <priority>{PRIORITY.get(rel, '0.8')}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> int:
    paths = page_paths()
    (DOCS / "sitemap.xml").write_text(
        render(paths, date.today().isoformat()), encoding="utf-8"
    )
    print(f"wrote {len(paths)} URLs to docs/sitemap.xml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
