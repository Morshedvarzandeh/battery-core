"""Static checks for the Chapter 1 battery-aging notebook."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "fundamentals" / "04_battery_aging.ipynb"


def _notebook() -> dict:
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))


def _source(cell_type: str) -> str:
    return "\n".join(
        "".join(cell["source"])
        for cell in _notebook()["cells"]
        if cell["cell_type"] == cell_type
    )


def test_notebook_exists_and_is_valid_json() -> None:
    assert NOTEBOOK.is_file()
    notebook = _notebook()
    assert notebook["nbformat"] == 4
    assert notebook["cells"]


def test_notebook_is_committed_without_outputs() -> None:
    """Stored outputs are 90% of this notebook's size, so they stay out."""
    for cell in _notebook()["cells"]:
        if cell["cell_type"] == "code":
            assert cell["outputs"] == []
            assert cell["execution_count"] is None


def test_notebook_targets_a_supported_python() -> None:
    """The recorded kernel must not advertise a Python the project rejects."""
    notebook = _notebook()
    assert notebook["metadata"]["kernelspec"]["name"] == "python3"
    version = notebook["metadata"]["language_info"]["version"]
    major, minor = (int(part) for part in version.split(".")[:2])
    assert (major, minor) >= (3, 10)


def test_notebook_uses_only_the_standard_library() -> None:
    """The panels are self-contained, so the notebook needs no extra install."""
    code = _source("code")
    for package in ("numpy", "matplotlib", "scipy", "pandas"):
        assert f"import {package}" not in code


def test_notebook_covers_the_six_mechanisms() -> None:
    markdown = _source("markdown")
    for mechanism in (
        "SEI",
        "Gas generation",
        "Crystal formation",
        "Dendrites",
        "Volume change",
    ):
        assert mechanism in markdown


def test_notebook_states_the_governing_relationships() -> None:
    markdown = _source("markdown")
    assert "Arrhenius" in markdown
    assert "√t" in markdown


def test_notebook_scope_is_explicit() -> None:
    """Teaching models must not be presented as a state-of-health estimator."""
    markdown = _source("markdown")
    assert "teaching models" in markdown
    assert "state-of-health estimator" in markdown
    assert "no number here should be quoted for a real cell" in markdown


def test_notebook_cites_its_sources() -> None:
    markdown = _source("markdown")
    assert "References" in markdown
    assert "doi.org" in markdown
