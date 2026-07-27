"""Static checks for the Lithium-ion Cell Architecture tutorial."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TUTORIAL = (
    ROOT
    / "docs"
    / "fundamentals"
    / "lithium-ion-cell-architecture"
)


def test_architecture_tutorial_assets_exist() -> None:
    for name in ("index.html", "styles.css", "app.js", "README.md"):
        assert (TUTORIAL / name).is_file()


def test_architecture_tutorial_uses_only_local_assets() -> None:
    html = (TUTORIAL / "index.html").read_text(encoding="utf-8")
    assert 'href="styles.css"' in html
    assert 'src="app.js"' in html
    assert "https://" not in html.split("<footer>", maxsplit=1)[0]


def test_architecture_tutorial_is_clearly_conceptual() -> None:
    html = (TUTORIAL / "index.html").read_text(encoding="utf-8")
    assert "Conceptual visualization" in html
    assert "not to scale" in html
    assert "not molecular dynamics" in html
    assert "Animation direction does not represent current" in html


def test_architecture_tutorial_contains_required_topics() -> None:
    html = (TUTORIAL / "index.html").read_text(encoding="utf-8")
    javascript = (TUTORIAL / "app.js").read_text(encoding="utf-8")

    for topic in (
        "Negative composite electrode",
        "Positive composite electrode",
        "Separator",
        "Conductive additive",
        "Binder",
        "Electrolyte-filled pores",
        "LiPF",
    ):
        assert topic in html

    for molecule in ("EC", "PC", "DMC", "EMC", "DEC"):
        assert f"{molecule}:" in javascript


def test_architecture_tutorial_has_accessible_controls() -> None:
    html = (TUTORIAL / "index.html").read_text(encoding="utf-8")
    assert 'aria-label="Operating direction"' in html
    assert 'role="tablist"' in html
    assert 'aria-live="polite"' in html
    assert 'href="#tutorial"' in html
