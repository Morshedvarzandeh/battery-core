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
FAVICON = ROOT / "docs" / "assets" / "favicon.svg"
DOCS = ROOT / "docs"


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


def test_coach_drills_implement_the_tested_relationships() -> None:
    """The drills are the answers the coach marks outright, so each one has to
    be the relationship the Python implements rather than a lookalike."""
    source = _coach()
    # current_from_c_rate: I = Q * C
    assert "current: capacity * rate" in source
    # ideal_duration_hours: t = 1 / C
    assert "hours: 1 / rate" in source
    # arrhenius_factor: exp[(Ea / R) * (1/T_ref - 1/T)]
    arrhenius = "(activation / MOLAR_GAS_CONSTANT) * (1 / referenceKelvin - 1 / kelvin)"
    assert arrhenius in source
    # parabolic_film_thickness: delta = delta_ref * sqrt(t / t_ref)
    assert "thickness * Math.sqrt(multiple)" in source


def test_coach_constants_match_the_python_exactly() -> None:
    """The browser cannot import `battery_core`, so the two constants it needs
    are copied. A copy drifts silently unless something compares them."""
    from battery_core.aging import ABSOLUTE_ZERO_C, MOLAR_GAS_CONSTANT

    source = _coach()
    assert f"MOLAR_GAS_CONSTANT = {MOLAR_GAS_CONSTANT};" in source
    assert f"ABSOLUTE_ZERO_C = {ABSOLUTE_ZERO_C};" in source


def test_coach_does_not_claim_to_mark_prose() -> None:
    """It cannot read an answer. Saying otherwise would be the unstated model
    limit this course exists to avoid."""
    source = _coach()
    assert "never claims to mark an answer" in source
    assert "keyword matching, which grades vocabulary" in source
    assert "tick what yours did" in source
    assert "A complete answer covers these" in source


def test_coach_separates_checked_from_self_checked() -> None:
    """A learner should be able to tell which kind of question they are on
    before answering, because the two are marked in different ways."""
    source = _coach()
    assert "function isAutoChecked(" in source
    assert '"Checked"' in source
    assert '"Self-checked"' in source
    for kind in ("drill:", "choice:", "multi:", "order:"):
        assert kind in source, kind


def test_auto_checked_questions_explain_wrong_options() -> None:
    """A distractor that is only marked wrong teaches nothing. Every option in
    every choice question carries the reason it is right or wrong."""
    source = _coach()
    blocks = re.findall(r"options: \[(.*?)\n      \],", source, re.S)
    assert blocks, "no choice questions found"
    for block in blocks:
        texts = re.findall(r"\n          text:", block)
        whys = re.findall(r"\n          why:", block)
        assert len(texts) == len(whys), (len(texts), len(whys))
        assert len(texts) >= 3


def test_ordering_question_is_a_real_process_route() -> None:
    source = _coach()
    for step in ("Mixing the slurry", "Coating the foil", "Drying the coating",
                 "Calendering to porosity", "Stacking or winding",
                 "Electrolyte filling", "Formation"):
        assert step in source, step
    # Shuffling that can return the input order opens the question pre-solved.
    assert "function shuffled(" in source
    assert "attempts < 20" in source


def test_mascot_is_drawn_not_fetched() -> None:
    """An embedded bitmap would be an external byte payload in a page that is
    meant to be self-contained, and could not change expression."""
    source = _coach()
    assert "function mascot()" in source
    assert "data:image" not in source
    assert "lemon-body" in source
    for mood in ("idle", "thinking", "happy", "encouraging"):
        assert f'setMood("{mood}")' in source or f'"{mood}"' in source, mood
    css = STYLESHEET.read_text(encoding="utf-8")
    # Firefox does not support the CSS `d` property, so expressions must not
    # depend on it or the mascot freezes there.
    assert "d: path(" not in css
    for mouth in ("mouth-idle", "mouth-happy", "mouth-flat", "mouth-soft"):
        assert mouth in css, mouth


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


def test_mascot_is_named() -> None:
    source = _coach()
    assert 'aria-label", "Volta' in source
    assert "Ask Volta" in source
    guide = GUIDE.read_text(encoding="utf-8")
    assert "Volta" in guide, "the name should be introduced where a reader meets it"
    readme = ASSETS_README.read_text(encoding="utf-8")
    assert "## Volta, the mascot" in readme


def test_every_page_has_a_favicon() -> None:
    """There was none at all before this: eight pages, eight blank tabs."""
    assert FAVICON.is_file()
    pages = [*sorted(DOCS.rglob("index.html")), DOCS / "assets" / "page-template.html"]
    assert len(pages) >= 9
    for page in pages:
        html = page.read_text(encoding="utf-8")
        assert 'rel="icon"' in html, page.relative_to(ROOT)
        assert "favicon.svg" in html, page.relative_to(ROOT)


def test_payload_loaders_restore_the_favicon() -> None:
    """`document.write` discards the original head, so the two simulators have
    to put the icon back with the rest of the chrome or they lose it."""
    for name in ("battery-production", "solid-state-production"):
        path = DOCS / "fundamentals" / name / "loader.js"
        loader = path.read_text(encoding="utf-8")
        assert 'icon.rel = "icon";' in loader, name
        assert "favicon.svg" in loader, name


def test_favicon_is_drawn_for_tab_size_not_scaled_down() -> None:
    """A shrunken illustration is mud at 16px. The favicon keeps only the parts
    that survive, so it must not carry the mascot's fine detail."""
    icon = FAVICON.read_text(encoding="utf-8")
    fine_detail = (
        "lemon-headset",
        "lemon-freckles",
        "lemon-shine",
        "lemon-glints",
        "lemon-sparkle",
        "data-mood",
    )
    for absent in fine_detail:
        assert absent not in icon, absent
    assert "viewBox" in icon
    assert "#ffd94a" in icon, "the lemon keeps the mascot's yellow"
