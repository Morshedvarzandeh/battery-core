"""Static checks for the reading lessons: Parts 02 and 04 and Fick's first law.

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
)
from battery_core.aging import arrhenius_factor

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CAPACITY = DOCS / "fundamentals" / "capacity-and-c-rate" / "index.html"
AGING = DOCS / "fundamentals" / "battery-aging" / "index.html"
FICK = DOCS / "transport" / "ficks-first-law" / "index.html"
LESSONS = (CAPACITY, AGING, FICK)
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
    [(CAPACITY, "Lesson 2", "p02"), (AGING, "Lesson 4", "p04")],
    ids=["part-02", "part-04"],
)
def test_practice_quiz_is_scoped_to_its_part(page: Path, part: str, item: str) -> None:
    html = page.read_text(encoding="utf-8")
    assert f'id="study-coach" data-part="{part}"' in html
    assert 'src="../../assets/study-coach.js"' in html
    assert f'data-complete="{item}"' in html
    coach = COACH.read_text(encoding="utf-8")
    assert coach.count(f'part: "{part}"') >= 3, "a quiz needs questions"


def test_coach_links_point_at_the_on_site_lessons() -> None:
    coach = COACH.read_text(encoding="utf-8")
    assert 'module: "../fundamentals/capacity-and-c-rate/"' in coach
    assert 'module: "../fundamentals/battery-aging/"' in coach
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
