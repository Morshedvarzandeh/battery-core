"""Draw the course's lesson illustrations as small, consistent line drawings.

Writes one SVG per lesson to docs/assets/art/. The drawings are decorative —
on the course cards, beside each lesson title and in the link-preview images —
so they carry no text a reader needs. Re-run after changing a drawing, then
re-run scripts/render_preview_images.py:

    python scripts/draw_lesson_art.py
"""

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "art"
INK, MUTED, LINE = "#202938", "#596579", "#c3cad5"
BLUE, WASH = "#2459a8", "#eef4ff"
TERRA, SAND = "#c8693f", "#f5e9dc"
SLATE, SLATE_W = "#64748b", "#e3e7ed"
COPPER, COPPER_S = "#d6a37a", "#a8784f"
ALU, ALU_S = "#cfd5dd", "#8a95a6"
W, H = 480, 300


def svg(name, title, body):
    text = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">\n'
        f"<title>{title}</title>\n"
        "<defs>"
        f'<marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
        f'<marker id="k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
        "</defs>\n"
        f'<g fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" font-family="Arial, Helvetica, sans-serif">\n'
        + body
        + "\n</g>\n</svg>\n"
    )
    (OUT / f"{name}.svg").write_text(text, encoding="utf-8")


def particles(rng, x0, x1, y0, y1, n, rmin, rmax, fill, stroke, tries=4000):
    placed = []
    for _ in range(tries):
        if len(placed) >= n:
            break
        r = rng.uniform(rmin, rmax)
        x = rng.uniform(x0 + r, x1 - r)
        y = rng.uniform(y0 + r, y1 - r)
        if all(math.hypot(x - a, y - b) > r + c + 2 for a, b, c in placed):
            placed.append((x, y, r))
    return "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
        for x, y, r in placed
    ), placed


# 1 · cell anatomy -----------------------------------------------------------
rng = random.Random(1)
neg, _ = particles(rng, 142, 224, 124, 246, 14, 6, 9, SLATE_W, SLATE)
pos, _ = particles(rng, 258, 338, 124, 246, 14, 6, 9, SAND, TERRA)
electrons = "".join(
    f'<circle cx="{x}" cy="{y}" r="5" fill="{BLUE}" stroke="none"/>'
    for x, y in [(134, 78), (180, 46), (300, 46), (346, 78)]
)
svg(
    "cell-anatomy",
    "A lithium-ion cell powering a lamp: electrons go round the wire, lithium ions cross inside",
    f'''
<rect x="118" y="116" width="244" height="138" rx="10" fill="#ffffff"/>
<rect x="126" y="122" width="12" height="126" fill="{COPPER}" stroke="{COPPER_S}" stroke-width="1.4"/>
<rect x="138" y="122" width="88" height="126" fill="#ffffff" stroke="none"/>
{neg}
<path d="M228 122 V248 M234 122 V248 M240 122 V248 M246 122 V248 M252 122 V248" stroke="{LINE}" stroke-width="1.4" stroke-dasharray="3 4"/>
{pos}
<rect x="342" y="122" width="12" height="126" fill="{ALU}" stroke="{ALU_S}" stroke-width="1.4"/>
<path d="M132 116 V46 H222 M258 46 H348 V116"/>
<circle cx="240" cy="46" r="18" fill="#ffffff"/>
<path d="M232 52 Q236 38 240 50 Q244 38 248 52" stroke-width="1.6"/>
<path d="M240 18 V10 M262 24 L268 18 M218 24 L212 18 M270 46 H278 M210 46 H202" stroke="{TERRA}" stroke-width="2"/>
{electrons}
<path d="M154 96 L154 70" stroke="{BLUE}" marker-end="url(#a)"/>
<path d="M326 70 L326 96" stroke="{BLUE}" marker-end="url(#a)"/>
<path d="M160 214 H318" stroke="{BLUE}" stroke-width="3.2" marker-end="url(#a)"/>
<text x="110" y="196" font-size="22" fill="{INK}" stroke="none" text-anchor="end" font-weight="700">−</text>
<text x="370" y="196" font-size="22" fill="{INK}" stroke="none" font-weight="700">+</text>
''',
)

# 2 · cell architecture --------------------------------------------------------
rng = random.Random(2)
stack = f'''
<rect x="54" y="78" width="12" height="160" fill="{COPPER}" stroke="{COPPER_S}" stroke-width="1.4"/>
<rect x="66" y="78" width="42" height="160" fill="{SLATE_W}" stroke="{SLATE}" stroke-width="1.4"/>
<rect x="108" y="78" width="16" height="160" fill="#ffffff" stroke="{LINE}" stroke-width="1.4"/>
<rect x="124" y="78" width="42" height="160" fill="{SAND}" stroke="{TERRA}" stroke-width="1.4"/>
<rect x="166" y="78" width="12" height="160" fill="{ALU}" stroke="{ALU_S}" stroke-width="1.4"/>
<rect x="66" y="132" width="42" height="40" fill="none" stroke="{BLUE}" stroke-width="2.4"/>
<path d="M108 132 L262 74 M108 172 L262 246" stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="4 4"/>
'''
cx, cy, R = 340, 160, 104
inner, placed = particles(
    rng, cx - R, cx + R, cy - R, cy + R, 60, 13, 22, SLATE_W, SLATE
)
inner_ps = [(x, y, r) for x, y, r in placed if math.hypot(x - cx, y - cy) < R - r + 4]
inner = "".join(
    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#ffffff" stroke="{SLATE}" stroke-width="1.8"/>'
    f'<path d="M{x - r * 0.55:.1f} {y - r * 0.25:.1f} H{x + r * 0.55:.1f} M{x - r * 0.6:.1f} {y + r * 0.15:.1f} H{x + r * 0.6:.1f}" stroke="{SLATE_W}" stroke-width="1.6"/>'
    for x, y, r in inner_ps
)
cdots = []
while len(cdots) < 60:
    x, y = rng.uniform(cx - R, cx + R), rng.uniform(cy - R, cy + R)
    if all(math.hypot(x - a, y - b) > c + 4 for a, b, c in inner_ps):
        cdots.append((x, y))
carbon = "".join(
    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{INK}" stroke="none"/>'
    for x, y in cdots
)
ions_at = []
while len(ions_at) < 6:
    x, y = rng.uniform(cx - R + 20, cx + R - 20), rng.uniform(cy - R + 20, cy + R - 20)
    if all(math.hypot(x - a, y - b) > c + 7 for a, b, c in inner_ps) and all(
        math.hypot(x - a, y - b) > 9 for a, b in cdots
    ):
        ions_at.append((x, y))
ions = "".join(
    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{BLUE}" stroke="none"/>'
    for x, y in ions_at
)
svg(
    "cell-architecture",
    "Zooming into one electrode: particles, conductive carbon and electrolyte-filled pores",
    f'''
{stack}
<clipPath id="lens"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>
<g clip-path="url(#lens)"><rect x="{cx - R}" y="{cy - R}" width="{2 * R}" height="{2 * R}" fill="{WASH}" stroke="none"/>{inner}{carbon}{ions}</g>
<circle cx="{cx}" cy="{cy}" r="{R}" stroke-width="2.4"/>
''',
)

# 3 · capacity and C-rate ------------------------------------------------------
svg(
    "capacity-and-c-rate",
    "Three discharges with equal area: higher current, shorter time, same charge",
    f'''
<path d="M70 40 V250 H430" stroke="{MUTED}"/>
<rect x="70" y="206" width="320" height="44" fill="{WASH}" stroke="{BLUE}"/>
<rect x="70" y="162" width="160" height="88" fill="{BLUE}" fill-opacity="0.16" stroke="{BLUE}"/>
<rect x="70" y="74" width="80" height="176" fill="{BLUE}" fill-opacity="0.3" stroke="{BLUE}"/>
<rect x="300" y="64" width="104" height="54" rx="7" fill="#ffffff"/>
<rect x="404" y="80" width="9" height="22" rx="2" fill="{INK}" stroke="none"/>
<rect x="312" y="76" width="20" height="30" rx="3" fill="{BLUE}" stroke="none"/>
<rect x="340" y="76" width="20" height="30" rx="3" fill="{BLUE}" stroke="none"/>
<rect x="368" y="76" width="20" height="30" rx="3" fill="{BLUE}" stroke="none" fill-opacity="0.35"/>
<circle cx="330" cy="176" r="26" fill="#ffffff"/>
<path d="M330 176 V160 M330 176 L342 184" stroke-width="2.4"/>
<path d="M324 146 H336" stroke-width="2.4"/>
''',
)

# 4 · cell production ---------------------------------------------------------
svg(
    "cell-production",
    "A roll-to-roll electrode line: unwind, slot-die coating, dryer, calender, rewind",
    f'''
<path d="M24 262 H456" stroke="{LINE}"/>
<circle cx="62" cy="168" r="36" fill="#ffffff"/><circle cx="62" cy="168" r="11"/><path d="M62 168 m-26 0 a26 26 0 0 1 26 -26" stroke="{LINE}"/>
<path d="M62 204 H186" stroke="{COPPER_S}" stroke-width="3"/>
<path d="M126 204 H186" stroke="{SLATE}" stroke-width="7"/>
<path d="M104 132 H140 L130 186 H114 Z" fill="#ffffff"/>
<path d="M122 186 V198" stroke="{BLUE}" stroke-width="3"/>
<path d="M122 96 V132" />
<rect x="186" y="150" width="122" height="92" rx="6" fill="#ffffff"/>
<path d="M186 204 H308" stroke="{SLATE}" stroke-width="7"/>
<path d="M208 182 q8 -10 0 -20 q-8 -10 0 -20 M240 182 q8 -10 0 -20 q-8 -10 0 -20 M272 182 q8 -10 0 -20 q-8 -10 0 -20" stroke="{TERRA}"/>
<path d="M308 204 H422" stroke="{SLATE}" stroke-width="5"/>
<circle cx="350" cy="179" r="24" fill="#ffffff"/><circle cx="350" cy="179" r="5" fill="{INK}" stroke="none"/>
<circle cx="350" cy="229" r="24" fill="#ffffff"/><circle cx="350" cy="229" r="5" fill="{INK}" stroke="none"/>
<path d="M350 132 V150" marker-end="url(#k)"/>
<circle cx="422" cy="168" r="34" fill="#ffffff"/><circle cx="422" cy="168" r="11"/><path d="M422 168 m0 -24 a24 24 0 0 1 24 24" stroke="{SLATE}" stroke-width="4"/>
<path d="M150 228 H176" stroke="{BLUE}" marker-end="url(#a)"/><path d="M372 254 H398" stroke="{BLUE}" marker-end="url(#a)"/>
''',
)

# 5 · solid-state production -----------------------------------------------------
rng = random.Random(5)
layers = []
y = 106
for _unit in range(3):
    layers.append(
        f'<rect x="132" y="{y}" width="216" height="10" fill="{SLATE_W}" stroke="{SLATE}" stroke-width="1.4"/>'
    )
    y += 10
    layers.append(
        f'<rect x="132" y="{y}" width="216" height="12" fill="{WASH}" stroke="{BLUE}" stroke-width="1.4"/>'
    )
    y += 12
    layers.append(
        f'<rect x="132" y="{y}" width="216" height="16" fill="{SAND}" stroke="{TERRA}" stroke-width="1.4"/>'
    )
    dots = "".join(
        f'<circle cx="{rng.uniform(138, 342):.1f}" cy="{y + 8:.1f}" r="3" fill="{TERRA}" stroke="none"/>'
        for _ in range(16)
    )
    layers.append(dots)
    y += 16
    layers.append(
        f'<rect x="132" y="{y}" width="216" height="5" fill="{ALU}" stroke="{ALU_S}" stroke-width="1.2"/>'
    )
    y += 5
svg(
    "solid-state-cell-production",
    "A stack of solid layers pressed between two plates",
    f'''
<path d="M240 20 V58"/>
<rect x="116" y="58" width="248" height="26" rx="4" fill="{ALU}"/>
<path d="M172 88 V100" stroke="{BLUE}" stroke-width="2.4" marker-end="url(#a)"/><path d="M240 88 V100" stroke="{BLUE}" stroke-width="2.4" marker-end="url(#a)"/><path d="M308 88 V100" stroke="{BLUE}" stroke-width="2.4" marker-end="url(#a)"/>
{"".join(layers)}
<rect x="116" y="{y + 6}" width="248" height="26" rx="4" fill="{ALU}"/>
<path d="M240 {y + 32} V276"/>
<circle cx="420" cy="150" r="42" fill="#ffffff"/>
<circle cx="404" cy="154" r="17" fill="{SAND}" stroke="{TERRA}"/>
<circle cx="437" cy="146" r="17" fill="{WASH}" stroke="{BLUE}"/>
<path d="M420 140 V160" stroke="{INK}" stroke-width="3"/>
<path d="M348 140 L378 146" stroke="{LINE}" stroke-dasharray="4 4"/>
''',
)

# 6 · battery aging ---------------------------------------------------------------
svg(
    "battery-aging",
    "Capacity falling over time toward the 80 percent line, with a thermometer and a particle wrapped in a growing film",
    f'''
<path d="M60 40 V250 H400" stroke="{MUTED}"/>
<path d="M60 108 H400" stroke="{TERRA}" stroke-dasharray="6 6"/>
<path d="M60 66 C130 74 200 84 260 98 C310 110 350 140 392 196" stroke="{BLUE}" stroke-width="3"/>
<circle cx="296" cy="108" r="6" fill="{TERRA}" stroke="none"/>
<circle cx="132" cy="196" r="25" fill="{SAND}" stroke="{TERRA}" stroke-width="2"/>
<circle cx="132" cy="196" r="20" fill="#ffffff" stroke="{SLATE}"/>
<path d="M120 192 H144 M118 200 H146" stroke="{SLATE_W}" stroke-width="2"/>
<rect x="430" y="44" width="18" height="128" rx="9" fill="#ffffff"/>
<circle cx="439" cy="186" r="18" fill="{TERRA}" stroke="{INK}"/>
<path d="M439 170 V96" stroke="{TERRA}" stroke-width="7"/>
<path d="M452 64 H460 M452 88 H460 M452 112 H460 M452 136 H460" stroke-width="1.6"/>
''',
)

# 7 · Fick's first law --------------------------------------------------------------
rng = random.Random(7)
dots = []
for _ in range(220):
    x = 60 + 360 * (rng.random() ** 1.8)
    yy = rng.uniform(86, 214)
    dots.append(
        f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="4" fill="{BLUE}" stroke="none" fill-opacity="0.85"/>'
    )
svg(
    "ficks-first-law",
    "Particles crowded on one side spreading toward the other: diffusion runs down the concentration gradient",
    f'''
<rect x="56" y="78" width="368" height="144" rx="8" fill="#ffffff"/>
{"".join(dots)}
<path d="M110 254 H372" stroke="{INK}" stroke-width="3" marker-end="url(#k)"/>
<rect x="56" y="40" width="368" height="14" rx="7" fill="url(#g)" stroke="none"/>
<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{WASH}"/></linearGradient>
''',
)

# 8 · battery materials lab -------------------------------------------------------
tiles = []
for i in range(6):
    for j in range(4):
        tiles.append(
            f'<rect x="{270 + i * 30}" y="{60 + j * 30}" width="24" height="24" rx="3" fill="{SLATE_W if (i + j) % 3 else WASH}" stroke="{LINE}" stroke-width="1.2"/>'
        )
svg(
    "battery-materials-lab",
    "Two electrode materials at different potentials; the gap between them is the cell voltage",
    f'''
<path d="M70 40 V262" stroke="{MUTED}"/>
<path d="M64 70 H76 M64 120 H76 M64 170 H76 M64 220 H76" stroke="{MUTED}" stroke-width="1.6"/>
{"".join(tiles)}
<rect x="100" y="70" width="64" height="56" rx="6" fill="{SAND}" stroke="{TERRA}"/>
<text x="132" y="106" font-size="22" font-weight="700" fill="{INK}" stroke="none" text-anchor="middle">Cu</text>
<rect x="100" y="196" width="64" height="56" rx="6" fill="{SLATE_W}" stroke="{SLATE}"/>
<text x="132" y="232" font-size="22" font-weight="700" fill="{INK}" stroke="none" text-anchor="middle">Zn</text>
<path d="M196 98 V224" stroke="{BLUE}" stroke-width="3" marker-start="url(#a)" marker-end="url(#a)"/>
<path d="M172 98 H210 M172 224 H210" stroke="{BLUE}" stroke-dasharray="4 4"/>
<path d="M270 196 H444 M270 214 H400 M270 232 H420" stroke="{LINE}" stroke-width="6"/>
''',
)
print("drawn", sorted(p.name for p in OUT.iterdir()))

# 0 · the course as a whole ---------------------------------------------------------
rng = random.Random(10)
neg0, _ = particles(rng, 172, 232, 150, 238, 9, 5, 7, SLATE_W, SLATE)
pos0, _ = particles(rng, 256, 316, 150, 238, 9, 5, 7, SAND, TERRA)
svg(
    "course",
    "A lithium-ion cell lighting a lamp, surrounded by the course topics: how it is rated, how it is made and how it ages",
    f'''
<rect x="150" y="144" width="180" height="102" rx="9" fill="#ffffff"/>
<rect x="158" y="150" width="10" height="90" fill="{COPPER}" stroke="{COPPER_S}" stroke-width="1.4"/>
{neg0}
<path d="M238 150 V240 M244 150 V240 M250 150 V240" stroke="{LINE}" stroke-width="1.4" stroke-dasharray="3 4"/>
{pos0}
<rect x="312" y="150" width="10" height="90" fill="{ALU}" stroke="{ALU_S}" stroke-width="1.4"/>
<path d="M163 144 V92 H226 M254 92 H317 V144"/>
<circle cx="240" cy="92" r="15" fill="#ffffff"/>
<path d="M233 97 Q236 85 240 95 Q244 85 247 97" stroke-width="1.5"/>
<path d="M240 68 V60 M258 74 L264 68 M222 74 L216 68" stroke="{TERRA}"/>
<circle cx="190" cy="92" r="4.5" fill="{BLUE}" stroke="none"/><circle cx="290" cy="92" r="4.5" fill="{BLUE}" stroke="none"/>
<path d="M182 218 H300" stroke="{BLUE}" stroke-width="3" marker-end="url(#a)"/>
<circle cx="74" cy="104" r="44" fill="#ffffff" stroke="{LINE}"/>
<rect x="46" y="86" width="56" height="30" rx="5" fill="#ffffff"/><rect x="102" y="94" width="5" height="14" rx="1.5" fill="{INK}" stroke="none"/>
<rect x="53" y="92" width="11" height="18" rx="2" fill="{BLUE}" stroke="none"/><rect x="68" y="92" width="11" height="18" rx="2" fill="{BLUE}" stroke="none"/><rect x="83" y="92" width="11" height="18" rx="2" fill="{BLUE}" stroke="none" fill-opacity="0.35"/>
<circle cx="82" cy="226" r="44" fill="#ffffff" stroke="{LINE}"/>
<circle cx="68" cy="214" r="13" fill="#ffffff"/><circle cx="68" cy="214" r="3" fill="{INK}" stroke="none"/>
<circle cx="68" cy="240" r="13" fill="#ffffff"/><circle cx="68" cy="240" r="3" fill="{INK}" stroke="none"/>
<path d="M40 227 H112" stroke="{SLATE}" stroke-width="4"/>
<circle cx="406" cy="104" r="44" fill="#ffffff" stroke="{LINE}"/>
<path d="M378 86 C392 88 404 92 414 98 C424 104 430 114 436 128" stroke="{BLUE}" stroke-width="2.6"/>
<path d="M376 104 H436" stroke="{TERRA}" stroke-dasharray="4 4"/>
<circle cx="402" cy="226" r="44" fill="#ffffff" stroke="{LINE}"/>
<path d="M372 226 C380 214 390 214 398 226 C406 238 416 238 424 226" stroke="{BLUE}" stroke-width="2.4"/>
<rect x="414" y="198" width="10" height="40" rx="5" fill="#ffffff" stroke-width="1.6"/><circle cx="419" cy="242" r="7" fill="{TERRA}" stroke="{INK}" stroke-width="1.6"/>
''',
)


# 9 · Chapter 2 teaser: an equivalent circuit -------------------------------------
def resistor(x, y, w):
    pts = [f"{x},{y}"]
    step = w / 8
    for i in range(1, 8):
        pts.append(f"{x + i * step:.1f},{y + (-10 if i % 2 else 10)}")
    pts.append(f"{x + w},{y}")
    return f'<polyline points="{" ".join(pts)}"/>'


svg(
    "equivalent-circuit",
    "An equivalent-circuit model: a voltage source, a series resistor and a resistor-capacitor pair",
    f"""
<circle cx="80" cy="150" r="26" fill="#ffffff"/>
<path d="M80 136 V164 M66 150 H94" stroke="{BLUE}" stroke-width="2.4"/>
<path d="M80 124 V80 H130"/>
{resistor(130, 80, 70)}
<path d="M200 80 H250"/>
<path d="M250 80 V50 H280"/>{resistor(280, 50, 60)}<path d="M340 50 H370 V80"/>
<path d="M250 80 V110 H296 M314 110 H370 V80"/>
<path d="M296 94 V126 M314 94 V126" stroke-width="3"/>
<path d="M370 80 H420 V220 H80 V176"/>
<circle cx="420" cy="80" r="5" fill="{INK}" stroke="none"/><circle cx="420" cy="220" r="5" fill="{INK}" stroke="none"/>
<path d="M110 248 H170 V266 C200 266 230 258 270 255 C320 252 360 251 420 251" stroke="{TERRA}" stroke-width="2.6"/>
""",
)

# 10 · CellForge layout editor: a machine drawing with selection handles -----------
svg(
    "layout-editor",
    "A machine diagram being edited: one roller is selected, with handles to move and resize it",
    f"""
<path d="M40 210 H440" stroke="{SLATE}" stroke-width="5"/>
<circle cx="90" cy="176" r="32" fill="#ffffff"/><circle cx="90" cy="176" r="9"/>
<rect x="160" y="110" width="110" height="80" rx="6" fill="#ffffff"/>
<path d="M182 168 q8 -10 0 -20 q-8 -10 0 -20 M214 168 q8 -10 0 -20 q-8 -10 0 -20 M246 168 q8 -10 0 -20 q-8 -10 0 -20" stroke="{TERRA}"/>
<circle cx="330" cy="186" r="22" fill="#ffffff"/><circle cx="330" cy="186" r="5" fill="{INK}" stroke="none"/>
<circle cx="330" cy="234" r="22" fill="#ffffff"/><circle cx="330" cy="234" r="5" fill="{INK}" stroke="none"/>
<rect x="300" y="156" width="60" height="60" fill="none" stroke="{BLUE}" stroke-width="1.6" stroke-dasharray="5 4"/>
<rect x="295" y="151" width="10" height="10" fill="#ffffff" stroke="{BLUE}"/><rect x="355" y="151" width="10" height="10" fill="#ffffff" stroke="{BLUE}"/>
<rect x="295" y="211" width="10" height="10" fill="#ffffff" stroke="{BLUE}"/><rect x="355" y="211" width="10" height="10" fill="#ffffff" stroke="{BLUE}"/>
<path d="M392 120 L392 154 L401 146 L408 162 L414 159 L407 143 L419 143 Z" fill="#ffffff" stroke="{INK}" stroke-width="1.8"/>
<rect x="60" y="60" width="150" height="28" rx="5" fill="#ffffff" stroke="{LINE}"/>
<path d="M72 74 H160" stroke="{LINE}" stroke-width="6"/>
""",
)
