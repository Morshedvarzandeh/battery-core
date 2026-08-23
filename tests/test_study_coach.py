"""Static checks for the Chapter 1 study coach.

The coach makes two promises the rest of the course is held to as well: it
runs entirely in the browser, and it does not claim to mark an answer it
cannot read. Both are easy to break by accident later, so both are checked.
"""

import json
import re
from pathlib import Path

from asset_checks import external_asset_references

ROOT = Path(__file__).resolve().parents[1]
COACH = ROOT / "docs" / "assets" / "study-coach.js"
GUIDE = ROOT / "docs" / "chapter-1" / "index.html"
STYLESHEET = ROOT / "docs" / "assets" / "site.css"
ASSETS_README = ROOT / "docs" / "assets" / "README.md"


def _coach() -> str:
    return COACH.read_text(encoding="utf-8")


def test_coach_ships_with_the_chapter_guide() -> None:
    assert COACH.is_file()
    html = GUIDE.read_text(encoding="utf-8")
    assert 'id="study-coach"' in html
    assert 'src="../assets/study-coach.js"' in html
    assert 'id="practice"' in html
    assert external_asset_references(html) == []


def test_coach_degrades_without_javascript() -> None:
    """The questions are all written out beside their parts, so a browser with
    scripting off still has the whole chapter."""
    html = GUIDE.read_text(encoding="utf-8")
    assert "<noscript>" in html
    assert "coach-noscript" in html


def test_coach_makes_no_network_request_by_default() -> None:
    """The AI tutor is opt-in. Without `data-tutor-endpoint` the page must not
    fetch anything, which is what keeps every fork self-contained."""
    html = GUIDE.read_text(encoding="utf-8")
    assert "data-tutor-endpoint" not in html
    source = _coach()
    # The only fetch in the file is inside the opt-in tutor.
    assert source.count("fetch(") == 1
    assert "if (endpoint) {" in source
    assert "attachTutor" in source


def test_coach_never_hardcodes_a_key() -> None:
    """Everything under docs/ is public. A key here is a key anyone can spend."""
    source = _coach()
    for marker in ("sk-ant", "api_key", "apiKey", "x-api-key", "Authorization"):
        assert marker not in source, marker
    assert "Never put a key here" in source


def test_coach_covers_every_checkpoint_in_the_guide() -> None:
    """A checkpoint that exists in the sequence but not in the coach is a
    question the learner is told to answer and never given a way to check."""
    source = _coach()
    ids = re.findall(r'\n      id: "([a-z0-9-]+)"', source)
    # Ids key saved progress, so a duplicate silently merges two questions.
    assert len(ids) == len(set(ids))
    parts = (
        "p01-paths",
        "p01b-pore-electrolyte",
        "p02-drill",
        "p02-real-runtime",
        "p03-upstream-downstream",
        "p03b-solid-electrolyte",
        "p04-fade-vs-impedance",
    )
    for part in parts:
        assert part in ids, part
    for chapter in ("ch-trace", "ch-compare", "ch-connect"):
        assert chapter in ids, chapter


def test_coach_drill_matches_the_tested_python() -> None:
    """The drill is the one answer the coach checks outright, so its arithmetic
    has to be the definition `battery_core.capacity` implements: I = Q x C and
    t = 1 / C."""
    source = _coach()
    assert "current: capacity * rate" in source
    assert "var hours = 1 / rate;" in source
    assert "I = Q × C = " in source  # noqa: RUF001 — the drill renders U+00D7
    assert "t = 1 / C = " in source


def test_coach_does_not_claim_to_mark_prose() -> None:
    """It cannot read an answer. Saying otherwise would be the unstated model
    limit this course exists to avoid."""
    source = _coach()
    assert "The coach never claims to mark an answer" in source
    assert "tick what yours did" in source
    assert "A complete answer covers these" in source


def test_coach_keeps_progress_local() -> None:
    source = _coach()
    assert 'STORAGE_KEY = "battery-core-chapter-1-coach"' in source
    # Storage can throw outright when site data is blocked; that must not take
    # the page down with it.
    assert source.count("catch (error)") >= 2
    assert "localStorage.getItem" in source
    assert "localStorage.setItem" in source


def test_coach_has_styles_and_documentation() -> None:
    css = STYLESHEET.read_text(encoding="utf-8")
    selectors = (".coach-card", ".coach-points", ".coach-hint-list", ".coach-noscript")
    for selector in selectors:
        assert selector in css, selector
    readme = ASSETS_README.read_text(encoding="utf-8")
    assert "## The study coach" in readme
    assert "## An AI tutor" in readme
    assert "data-tutor-endpoint" in readme


def test_documented_tutor_contract_matches_the_client() -> None:
    """The worker in the docs is what someone will deploy, so the JSON shape it
    answers has to be the shape the client actually sends and reads."""
    readme = ASSETS_README.read_text(encoding="utf-8")
    request_line = re.search(r"// request\n(\{.*\})", readme)
    response_line = re.search(r"// response\n(\{.*\})", readme)
    assert request_line and response_line
    request = json.loads(request_line.group(1))
    response = json.loads(response_line.group(1))
    assert set(request) == {"question", "context"}
    assert set(request["context"]) == {"chapter", "checkpointId", "checkpoint"}
    assert set(response) == {"reply"}

    source = _coach()
    for field in ("question:", "context:", "chapter:", "checkpointId:", "checkpoint:"):
        assert field in source, field
    assert "data.reply" in source
