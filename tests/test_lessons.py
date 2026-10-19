"""Static checks for the reading lessons: Lessons 1 to 4 and Fick's first law.

The lessons are the on-site, readable version of material that was previously
only reachable as a notebook. These checks keep them honest in the same ways
the rest of the course is kept honest: every worked number agrees with the
tested Python, the embedded aging panels are the notebook's own, and each
page has the structure, objectives and limits a lesson needs.
"""

from __future__ import annotations

import importlib.util
import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

from asset_checks import external_asset_references
from battery_core import (
    c_rate_from_current,
    current_from_c_rate,
    ficks_first_law_flux,
    ideal_duration_hours,
    nominal_energy_wh,
)
from battery_core.aging import arrhenius_factor

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASICS = DOCS / "fundamentals" / "battery-basics" / "index.html"
ANATOMY = DOCS / "fundamentals" / "cell-anatomy" / "index.html"
ARCHITECTURE = DOCS / "fundamentals" / "cell-architecture" / "index.html"
CAPACITY = DOCS / "fundamentals" / "capacity-and-c-rate" / "index.html"
PRODUCTION = DOCS / "fundamentals" / "cell-production" / "index.html"
SOLID_STATE = DOCS / "fundamentals" / "solid-state-cell-production" / "index.html"
AGING = DOCS / "fundamentals" / "battery-aging" / "index.html"
FICK = DOCS / "transport" / "ficks-first-law" / "index.html"
LESSONS = (
    BASICS,
    ANATOMY,
    ARCHITECTURE,
    CAPACITY,
    PRODUCTION,
    SOLID_STATE,
    AGING,
    FICK,
)
COACH = DOCS / "assets" / "study-coach.js"
TIMES = "\N{MULTIPLICATION SIGN}"  # as printed in the lesson tables


class _Structure(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.refs: list[str] = []
        self.h1 = 0
        self.iframes: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        if values.get("id"):
            self.ids.append(values["id"])
        for name in ("aria-labelledby", "aria-describedby", "aria-controls"):
            self.refs.extend(values.get(name, "").split())
        if tag == "h1":
            self.h1 += 1
        if tag == "iframe":
            self.iframes.append(values)


def _parse(path: Path) -> _Structure:
    parser = _Structure()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


@pytest.mark.parametrize("page", LESSONS, ids=lambda p: p.parent.name)
def test_lesson_structure_is_accessible(page: Path) -> None:
    parser = _parse(page)
    assert parser.h1 == 1
    assert len(parser.ids) == len(set(parser.ids)), "duplicate id"
    assert set(parser.refs) <= set(parser.ids), set(parser.refs) - set(parser.ids)
    html = page.read_text(encoding="utf-8")
    assert 'href="#main-content"' in html
    assert 'id="main-content"' in html
    assert 'aria-label="Breadcrumb"' in html


@pytest.mark.parametrize("page", LESSONS, ids=lambda p: p.parent.name)
def test_lesson_fetches_nothing_from_another_host(page: Path) -> None:
    assert external_asset_references(page.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize("page", LESSONS, ids=lambda p: p.parent.name)
def test_lesson_follows_the_course_discipline(page: Path) -> None:
    """Objectives before the content, a way to mark it complete after it."""
    html = page.read_text(encoding="utf-8")
    assert "Learning objectives" in html
    assert html.index("Learning objectives") < html.index('class="section-number">01')
    assert "data-complete=" in html
    assert 'src="../../assets/course-progress.js"' in html
    assert "A project of Lemonergy" in html
    assert "AGPL-3.0-or-later" in html


@pytest.mark.parametrize(
    ("page", "part", "item"),
    [
        (BASICS, "Lesson 0", "p00"),
        (ANATOMY, "Lesson 1", "p01"),
        (ARCHITECTURE, "Lesson 1B", "p01b"),
        (CAPACITY, "Lesson 2", "p02"),
        (PRODUCTION, "Lesson 3", "p03"),
        (SOLID_STATE, "Lesson 3B", "p03b"),
        (AGING, "Lesson 4", "p04"),
    ],
    ids=[
        "lesson-0",
        "lesson-1",
        "lesson-1b",
        "lesson-2",
        "lesson-3",
        "lesson-3b",
        "lesson-4",
    ],
)
def test_practice_quiz_is_scoped_to_its_part(page: Path, part: str, item: str) -> None:
    html = page.read_text(encoding="utf-8")
    assert f'id="study-coach" data-part="{part}"' in html
    assert 'src="../../assets/study-coach.js"' in html
    assert f'data-complete="{item}"' in html
    coach = COACH.read_text(encoding="utf-8")
    assert coach.count(f'part: "{part}"') >= 4, "a quiz needs questions"


def test_coach_links_point_at_the_on_site_lessons() -> None:
    coach = COACH.read_text(encoding="utf-8")
    lessons = (BASICS, ANATOMY, ARCHITECTURE, CAPACITY, PRODUCTION, SOLID_STATE, AGING)
    for page in lessons:
        assert f'module: "../fundamentals/{page.parent.name}/"' in coach, page
    # The labs are reached through their lessons, not directly from the quiz.
    for lab in ("cell-anatomy-workbench", "lithium-ion-cell-architecture",
                "battery-production", "solid-state-production"):
        assert f'module: "../fundamentals/{lab}/"' not in coach, lab
    assert "data-part" in coach or "dataset.part" in coach


# --- Part 02: every printed number is the tested function's ----------------


def test_capacity_rate_table_matches_the_python() -> None:
    html = CAPACITY.read_text(encoding="utf-8")
    row = (
        r'<tr data-rate="([\d.]+)">.*?'
        r'data-cell="current">([\d.]+) A</td><td class="num">([^<]+)</td>'
    )
    rows = re.findall(row, html)
    assert len(rows) == 7
    for rate, current, duration in rows:
        c = float(rate)
        assert float(current) == pytest.approx(
            current_from_c_rate(nominal_capacity_ah=20.0, c_rate=c)
        )
        hours = ideal_duration_hours(c)
        expected = f"{hours:g} h" if hours >= 1 else f"{hours * 60:g} min"
        assert duration == expected


def test_capacity_worked_example_matches_the_python() -> None:
    html = CAPACITY.read_text(encoding="utf-8")
    rate = c_rate_from_current(current_a=15.0, nominal_capacity_ah=3.2)
    assert f"{rate:.2f}C" in html  # 4.69C
    assert f"{ideal_duration_hours(rate) * 60:.1f} min" in html  # 12.8 min
    two_c = current_from_c_rate(nominal_capacity_ah=20.0, c_rate=2.0)
    assert f'<dd data-out="current">{two_c:g} A</dd>' in html


def test_capacity_lesson_keeps_the_runtime_caveat() -> None:
    html = CAPACITY.read_text(encoding="utf-8")
    assert "not a runtime prediction" in html
    assert "keyword arguments only" in html


# --- Part 04: tables agree with the tested Arrhenius factor -----------------


@pytest.mark.parametrize(
    ("temperature", "energy", "printed"),
    [
        (-10, 45_000, "0.09"),
        (45, 50_000, "3.55"),
        (60, 62_000, "13.84"),
        (35, 45_000, "1.80"),
    ],
)
def test_aging_arrhenius_table_matches_the_python(
    temperature: int, energy: int, printed: str
) -> None:
    factor = arrhenius_factor(
        temperature_c=temperature, activation_energy_j_per_mol=energy
    )
    assert f"{factor:.2f}" == printed
    assert f'<td class="num">{printed}{TIMES}</td>' in AGING.read_text(encoding="utf-8")


def test_aging_lesson_states_what_its_numbers_are() -> None:
    html = AGING.read_text(encoding="utf-8")
    assert "teaching models" in html
    assert "not a state-of-health estimator" in html
    assert html.count('href="https://doi.org/') >= 12


def _exporter():
    spec = importlib.util.spec_from_file_location(
        "export_aging_panels", ROOT / "scripts" / "export_aging_panels.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_aging_panels_are_the_notebooks_own() -> None:
    """Change a panel in the notebook and not here, and this fails. Re-run
    `python scripts/export_aging_panels.py` to bring them back in step."""
    exporter = _exporter()
    expected = exporter.render(exporter.load_assets())
    folder = DOCS / "fundamentals" / "battery-aging" / "panels"
    on_disk = {path.name for path in folder.iterdir()}
    assert on_disk == set(expected)
    for name, content in expected.items():
        assert (folder / name).read_text(encoding="utf-8") == content, name


def test_every_aging_panel_is_embedded_and_titled() -> None:
    parser = _parse(AGING)
    sources = [frame["src"] for frame in parser.iframes]
    panels = sorted(
        p.name
        for p in (DOCS / "fundamentals" / "battery-aging" / "panels").glob("*.html")
    )
    assert sorted(src.removeprefix("panels/") for src in sources) == panels
    for frame in parser.iframes:
        assert frame.get("title", "").startswith("Interactive panel:")
        assert frame.get("loading") == "lazy"


def test_aging_panels_are_kept_out_of_search_results() -> None:
    for panel in (DOCS / "fundamentals" / "battery-aging" / "panels").glob("*.html"):
        html = panel.read_text(encoding="utf-8")
        assert '<meta name="robots" content="noindex">' in html, panel.name
        assert external_asset_references(html) == [], panel.name


# --- Fick's first law ---------------------------------------------------------


def test_fick_worked_example_matches_the_python() -> None:
    flux = ficks_first_law_flux(1.0e-14, -5000.0 / 5.0e-6)
    assert flux == pytest.approx(1.0e-5)
    html = FICK.read_text(encoding="utf-8")
    assert f"1.00 {TIMES} 10⁻⁵ mol/(m²·s)" in html
    assert "toward +x" in html
    assert ficks_first_law_flux(2.0e-14, -3.0e7) == pytest.approx(6.0e-7)
    assert f"6 {TIMES} 10⁻⁷ mol/(m²·s)" in html


def test_fick_lesson_states_its_limits() -> None:
    html = FICK.read_text(encoding="utf-8")
    assert "not a time-evolution model" in html
    assert "second law" in html


# --- Structured data ----------------------------------------------------------


@pytest.mark.parametrize("page", LESSONS, ids=lambda p: p.parent.name)
def test_lesson_structured_data_describes_a_learning_resource(page: Path) -> None:
    html = page.read_text(encoding="utf-8")
    block = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert block
    graph = json.loads(block.group(1))["@graph"]
    lesson = next(node for node in graph if node["@type"] == "LearningResource")
    canonical = re.search(r'<link rel="canonical" href="([^"]+)">', html)
    assert canonical and lesson["url"] == canonical.group(1)
    assert lesson["isAccessibleForFree"] is True
    assert lesson["teaches"]


# --- Lesson 2: nominal energy -------------------------------------------------


@pytest.mark.parametrize(
    ("capacity", "voltage", "printed"),
    [(5.0, 3.85, "19.25 Wh"), (3.0, 3.6, "10.8 Wh"), (3.0, 3.2, "9.6 Wh"),
     (20.0, 3.65, "73 Wh")],
)
def test_capacity_energy_table_matches_the_python(
    capacity: float, voltage: float, printed: str
) -> None:
    energy = nominal_energy_wh(nominal_capacity_ah=capacity, nominal_voltage_v=voltage)
    assert f"{energy:.2f}".rstrip("0").rstrip(".") + " Wh" == printed
    assert f'<td class="num">{printed}</td>' in CAPACITY.read_text(encoding="utf-8")


def test_capacity_pack_example_matches_the_python() -> None:
    pack_voltage = 96 * 3.65
    energy = nominal_energy_wh(nominal_capacity_ah=50.0, nominal_voltage_v=pack_voltage)
    html = CAPACITY.read_text(encoding="utf-8")
    assert f'<td class="num">{pack_voltage:.1f} V</td>' in html
    assert f'<td class="num">{energy / 1000:.1f} kWh</td>' in html


def test_capacity_energy_calculator_defaults_to_the_worked_example() -> None:
    html = CAPACITY.read_text(encoding="utf-8")
    assert 'data-calc="energy"' in html
    energy = nominal_energy_wh(nominal_capacity_ah=20.0, nominal_voltage_v=3.65)
    assert f'<dd data-out="energy">{energy:g} Wh</dd>' in html


# --- Lessons 1 and 1B: the labs are framed, and the frames fit them -------------


@pytest.mark.parametrize(
    ("page", "lab"),
    [
        (ANATOMY, "cell-anatomy-workbench"),
        (ARCHITECTURE, "lithium-ion-cell-architecture"),
    ],
    ids=["lesson-1", "lesson-1b"],
)
def test_lab_is_framed_in_its_lesson(page: Path, lab: str) -> None:
    parser = _parse(page)
    frames = [f for f in parser.iframes if f.get("src") == f"../{lab}/"]
    assert len(frames) == 1
    assert "data-fit" in frames[0]
    assert frames[0].get("title")
    html = page.read_text(encoding="utf-8")
    assert 'src="../../assets/lab-frame.js"' in html
    lab_html = (DOCS / "fundamentals" / lab / "index.html").read_text(encoding="utf-8")
    # The lab hides its own course chrome when it is shown inside the lesson.
    assert 'src="../../assets/embed.js"' in lab_html
    assert lab_html.index("embed.js") < lab_html.index("</head>")


def test_embedded_labs_cannot_grow_their_own_frame() -> None:
    """A frame sized to its content, holding a page sized to the frame, would
    grow without end."""
    css = (DOCS / "assets" / "site-chrome.css").read_text(encoding="utf-8")
    assert "html[data-embedded] body" in css
    assert "min-height: 0 !important" in css


# --- Lessons 3 and 3B: simulators are opened, with a preview -------------------


@pytest.mark.parametrize(
    ("page", "simulator", "preview"),
    [
        (PRODUCTION, "battery-production", "cellforge-preview.webp"),
        (SOLID_STATE, "solid-state-production", "solidforge-preview.webp"),
    ],
    ids=["lesson-3", "lesson-3b"],
)
def test_simulator_lesson_links_its_simulator(
    page: Path, simulator: str, preview: str
) -> None:
    html = page.read_text(encoding="utf-8")
    assert f'href="../{simulator}/"' in html
    assert f'<img src="{preview}"' in html
    assert (page.parent / preview).is_file()
    assert (page.parent / preview).stat().st_size < 100_000
