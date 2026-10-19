"""Static checks for the final exam, the cheat sheet and the About page.

The exam marks answers outright, so its answer key is the one place in the
course where a typo becomes a wrong grade. These checks hold the key to a
shape that can be marked, keep every question tied to a lesson, and keep the
statement of completion honest about what it is.
"""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

from asset_checks import external_asset_references
from battery_core import current_from_c_rate, ideal_duration_hours, nominal_energy_wh

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXAM = DOCS / "exam" / "index.html"
CHEAT = DOCS / "cheat-sheet" / "index.html"
ABOUT = DOCS / "about" / "index.html"
SYLLABUS = DOCS / "chapter-1" / "index.html"
ENGINE = DOCS / "assets" / "final-exam.js"
PROGRESS = DOCS / "assets" / "course-progress.js"
TIMES = "\N{MULTIPLICATION SIGN}"


class _Exam(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.questions: list[dict[str, object]] = []
        self.pass_mark = 0
        self.in_why = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        if tag == "form" and values.get("id") == "final-exam":
            self.pass_mark = int(values["data-pass"])
        if tag == "fieldset" and "exam-q" in values.get("class", ""):
            self.questions.append({"inputs": [], "links": []})
        if tag == "input" and self.questions and values.get("name", "").startswith("q"):
            self.questions[-1]["inputs"].append(values)  # type: ignore[union-attr]
        if tag == "div" and "exam-why" in values.get("class", ""):
            self.in_why = True
        if tag == "a" and self.in_why and self.questions:
            self.questions[-1]["links"].append(values.get("href", ""))  # type: ignore[union-attr]

    def handle_endtag(self, tag: str) -> None:
        if tag == "div":
            self.in_why = False


def _exam() -> _Exam:
    parser = _Exam()
    parser.feed(EXAM.read_text(encoding="utf-8"))
    return parser


def test_exam_has_twenty_markable_questions() -> None:
    exam = _exam()
    assert len(exam.questions) == 20
    assert 0 < exam.pass_mark <= len(exam.questions)
    for number, question in enumerate(exam.questions, 1):
        inputs = question["inputs"]
        assert isinstance(inputs, list) and len(inputs) >= 3, number
        kinds = {i["type"] for i in inputs}
        assert len(kinds) == 1, number
        correct = [i for i in inputs if i["data-correct"] == "true"]
        assert all(i["data-correct"] in ("true", "false") for i in inputs), number
        assert correct, f"question {number} has no right answer"
        if kinds == {"radio"}:
            assert len(correct) == 1, f"question {number} has several right answers"
        assert {i["name"] for i in inputs} == {f"q{number}"}, number


def test_exam_right_answers_are_not_always_in_the_same_place() -> None:
    positions = []
    for question in _exam().questions:
        inputs = question["inputs"]
        assert isinstance(inputs, list)
        positions.append(
            next(k for k, i in enumerate(inputs) if i["data-correct"] == "true")
        )
    assert len(set(positions)) >= 3
    assert max(positions.count(p) for p in set(positions)) <= 10


def test_every_exam_question_points_back_to_its_lesson() -> None:
    for number, question in enumerate(_exam().questions, 1):
        links = question["links"]
        assert isinstance(links, list) and len(links) == 1, number
        assert links[0].startswith("../fundamentals/"), links[0]


def test_exam_is_marked_in_the_browser_and_says_what_its_statement_is() -> None:
    html = EXAM.read_text(encoding="utf-8")
    assert 'src="../assets/final-exam.js"' in html
    assert 'src="../assets/course-progress.js"' in html
    assert "not an accredited certificate" in html
    assert "not been verified by Lemonergy" in html
    assert external_asset_references(html) == []
    engine = ENGINE.read_text(encoding="utf-8")
    assert "fetch(" not in engine
    assert 'input.dataset.correct === "true"' in engine
    assert "completed.exam" in engine
    assert 'new Event("battery-core-progress")' in engine
    assert '"battery-core-progress"' in PROGRESS.read_text(encoding="utf-8")


def test_syllabus_counts_the_final_exam() -> None:
    html = SYLLABUS.read_text(encoding="utf-8")
    assert 'data-items="p01 p02 p03 p04 checkpoint exam"' in html
    assert 'data-progress-item="exam"' in html
    assert 'href="../exam/"' in html
    assert 'data-progress-item="p00"' in html


def test_cheat_sheet_numbers_match_the_python() -> None:
    html = CHEAT.read_text(encoding="utf-8")
    one_c = current_from_c_rate(nominal_capacity_ah=20.0, c_rate=1.0)
    assert f"1C on 20 Ah = {one_c:g} A" in html
    assert f"2C → {ideal_duration_hours(2.0) * 60:g} min" in html
    energy = nominal_energy_wh(nominal_capacity_ah=20.0, nominal_voltage_v=3.65)
    assert f"20 Ah {TIMES} 3.65 V = {energy:g} Wh" in html
    assert "@page" in (DOCS / "assets" / "site.css").read_text(encoding="utf-8")


def test_about_page_faq_is_structured_data() -> None:
    html = ABOUT.read_text(encoding="utf-8")
    block = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    assert block
    graph = json.loads(block.group(1))["@graph"]
    faq = next(node for node in graph if node["@type"] == "FAQPage")
    assert len(faq["mainEntity"]) == html.count("<summary>")
    for item in faq["mainEntity"]:
        assert item["acceptedAnswer"]["text"]
        assert "<" not in item["acceptedAnswer"]["text"]
