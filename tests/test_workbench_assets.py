"""Static checks for the Cell Anatomy Workbench assets."""

from pathlib import Path


WORKBENCH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "fundamentals"
    / "cell-anatomy-workbench"
)


def test_workbench_assets_exist() -> None:
    for name in ("index.html", "styles.css", "app.js", "README.md"):
        assert (WORKBENCH / name).is_file()


def test_workbench_is_clearly_conceptual() -> None:
    html = (WORKBENCH / "index.html").read_text(encoding="utf-8")
    assert "Conceptual visualization — not a quantitative simulation" in html
    assert "Illustrative, not model output" in html


def test_workbench_references_local_assets() -> None:
    html = (WORKBENCH / "index.html").read_text(encoding="utf-8")
    assert 'href="styles.css"' in html
    assert 'src="app.js"' in html
    assert "https://" not in html


def test_workbench_contains_required_components() -> None:
    html = (WORKBENCH / "index.html").read_text(encoding="utf-8")
    for component in (
        "negative-electrode",
        "positive-electrode",
        "electrolyte",
        "separator",
        "negative-collector",
        "positive-collector",
    ):
        assert component in html


def test_workbench_motion_control_exposes_pressed_state() -> None:
    html = (WORKBENCH / "index.html").read_text(encoding="utf-8")
    javascript = (WORKBENCH / "app.js").read_text(encoding="utf-8")
    assert 'id="motion" aria-pressed="true"' in html
    assert 'motion.setAttribute("aria-pressed",String(running))' in javascript
