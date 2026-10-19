"""Render the 1200 by 630 link-preview images from the lesson illustrations.

Each public page names its own image in og:image. Needs Playwright with
Chromium (not a project dependency):

    python scripts/render_preview_images.py
"""

import html
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

DOCS = Path(__file__).resolve().parents[1] / "docs"
LOGO = (
    (DOCS / "index.html")
    .read_text(encoding="utf-8")
    .split('<svg class="brand-logo"', 1)[1]
    .split("</svg>", 1)[0]
)
LOGO = '<svg class="logo"' + LOGO + "</svg>"

CARDS = {
    # page path (relative to docs, "" = home) : (file, eyebrow, title, subtitle, art, footer)
    "": (
        "og-image.png",
        "Free online course · Beginner",
        "Battery Cell Foundations",
        "How a lithium-ion cell is built, rated, manufactured and why it ages.",
        "course",
        "7 lessons · about 5 hours · free, no account",
    ),
    "chapter-1/": (
        "og/syllabus.png",
        "Syllabus",
        "Battery Cell Foundations",
        "Six lessons, practice quizzes and a progress tracker.",
        "course",
        None,
    ),
    "fundamentals/battery-basics/": (
        "og/battery-basics.png",
        "Lesson 0",
        "What does a battery actually do?",
        "Cells, packs and the six numbers on a datasheet.",
        "course",
        None,
    ),
    "exam/": (
        "og/exam.png",
        "Final exam",
        "Battery Cell Foundations final exam",
        "Twenty questions, marked in your browser, with a statement of completion.",
        "course",
        None,
    ),
    "cheat-sheet/": (
        "og/cheat-sheet.png",
        "Reference",
        "Lithium-ion cell cheat sheet",
        "Formulas, rules and typical numbers on one printable page.",
        "capacity-and-c-rate",
        None,
    ),
    "about/": (
        "og/about.png",
        "About",
        "About Lemonergy Learn",
        "How the free battery course is made and checked, and answers to common questions.",
        "course",
        None,
    ),
    "fundamentals/cell-anatomy/": (
        "og/cell-anatomy.png",
        "Lesson 1",
        "How a lithium-ion cell works",
        "The parts of a cell, and why electrons go the long way round.",
        "cell-anatomy",
        None,
    ),
    "fundamentals/cell-architecture/": (
        "og/cell-architecture.png",
        "Lesson 1B",
        "Inside a lithium-ion cell, layer by layer",
        "Porous electrodes, separator and electrolyte.",
        "cell-architecture",
        None,
    ),
    "fundamentals/capacity-and-c-rate/": (
        "og/capacity-and-c-rate.png",
        "Lesson 2",
        "Capacity, C-rate and energy",
        "Convert current, C-rate, time and watt-hours, with calculators.",
        "capacity-and-c-rate",
        None,
    ),
    "fundamentals/cell-production/": (
        "og/cell-production.png",
        "Lesson 3",
        "How lithium-ion cells are made",
        "From mixing and coating to formation, aging and testing.",
        "cell-production",
        None,
    ),
    "fundamentals/solid-state-cell-production/": (
        "og/solid-state-cell-production.png",
        "Lesson 3B",
        "How solid-state batteries are made",
        "Four solid electrolytes, and what changes on the line.",
        "solid-state-cell-production",
        None,
    ),
    "fundamentals/battery-aging/": (
        "og/battery-aging.png",
        "Lesson 4",
        "Why lithium-ion batteries wear out",
        "Six aging mechanisms, temperature and the 80 % line.",
        "battery-aging",
        None,
    ),
    "transport/ficks-first-law/": (
        "og/ficks-first-law.png",
        "Transport",
        "Fick’s first law for battery materials",
        "Diffusion flux, the sign convention and a calculator.",
        "ficks-first-law",
        None,
    ),
    "labs/battery-materials-lab/": (
        "og/battery-materials-lab.png",
        "Interactive lab",
        "Electrode potentials and battery materials",
        "Build a cell from two half-reactions and compare materials.",
        "battery-materials-lab",
        None,
    ),
    "glossary/": (
        "og/glossary.png",
        "Reference",
        "Battery glossary",
        "55 battery terms in plain language, each linked to its lesson.",
        "course",
        None,
    ),
    "fundamentals/cell-anatomy-workbench/": (
        "og/cell-anatomy-workbench.png",
        "Lesson 1 · Interactive lab",
        "Cell anatomy workbench",
        "Follow electrons and lithium ions through a cell.",
        "cell-anatomy",
        None,
    ),
    "fundamentals/lithium-ion-cell-architecture/": (
        "og/lithium-ion-cell-architecture.png",
        "Lesson 1B · Interactive tutorial",
        "Cell architecture, one layer at a time",
        "Assemble the stack, then zoom into the pores.",
        "cell-architecture",
        None,
    ),
    "fundamentals/battery-production/": (
        "og/battery-production.png",
        "Lesson 3 · Simulator",
        "CellForge: cell production simulator",
        "Walk a lithium-ion production line, machine by machine.",
        "cell-production",
        None,
    ),
    "fundamentals/solid-state-production/": (
        "og/solid-state-production.png",
        "Lesson 3B · Simulator",
        "SolidForge: solid-state production simulator",
        "Oxide, sulfide, halide and polymer lines compared.",
        "solid-state-cell-production",
        None,
    ),
}

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1200px;height:630px;background:#ffffff;font-family:Arial,Helvetica,sans-serif;color:#202938}}
.wrap{{position:relative;box-sizing:border-box;width:1200px;height:630px;padding:56px 72px;display:grid;grid-template-columns:600px 1fr;column-gap:40px;border-top:10px solid #2459a8}}
.brand{{display:flex;align-items:center;gap:14px;grid-column:1/-1;margin-bottom:34px}}
.logo{{width:56px;height:56px}}
.brand b{{font-size:30px}} .brand span{{font-size:20px;color:#596579;margin-left:6px}}
.eyebrow{{font-size:22px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#2459a8;margin:0 0 18px}}
h1{{font-size:{size}px;line-height:1.08;margin:0 0 22px;letter-spacing:-.01em}}
p.sub{{font-size:28px;line-height:1.35;color:#596579;margin:0}}
.art{{align-self:center;width:100%}}
.foot{{position:absolute;left:72px;bottom:44px;font-size:22px;color:#596579}}
.foot b{{color:#2459a8}}
</style></head><body><div class="wrap">
<div class="brand">{logo}<b>Lemonergy</b><span>Learn · battery engineering courses</span></div>
<div><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="sub">{sub}</p></div>
<img class="art" src="file://{art}">
<div class="foot"><b>learn.lemonergy.com</b>{footer}</div>
</div></body></html>"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": 1200, "height": 630}, device_scale_factor=1
    )
    for out, eyebrow, title, sub, art, footer in CARDS.values():
        size = 64 if len(title) <= 30 else 54 if len(title) <= 42 else 48
        doc = TEMPLATE.format(
            logo=LOGO,
            eyebrow=html.escape(eyebrow),
            title=html.escape(title),
            sub=html.escape(sub),
            art=DOCS / "assets" / "art" / f"{art}.svg",
            size=size,
            footer=(" · " + html.escape(footer)) if footer else " · free online course",
        )
        tmp = Path(tempfile.gettempdir()) / "lemonergy_og.html"
        tmp.write_text(doc, encoding="utf-8")
        page.goto(f"file://{tmp}")
        page.wait_for_timeout(150)
        page.screenshot(
            path=str(DOCS / "assets" / out),
            clip={"x": 0, "y": 0, "width": 1200, "height": 630},
        )
    browser.close()
print("rendered", len(CARDS))
