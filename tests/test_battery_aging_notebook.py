"""Structural checks for the Chapter 1 battery-aging notebook."""

import ast
import base64
import json
import re
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "fundamentals" / "04_battery_aging.ipynb"


def _notebook() -> dict[str, object]:
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))


def _all_source(notebook: dict[str, object]) -> str:
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]  # type: ignore[index]
    )


def _assets(notebook: dict[str, object]) -> dict[str, object]:
    setup = "".join(notebook["cells"][1]["source"])  # type: ignore[index]
    match = re.search(r'base64\.b64decode\("([A-Za-z0-9+/=]+)"\)', setup)
    assert match is not None
    return json.loads(zlib.decompress(base64.b64decode(match.group(1))).decode())


def test_aging_notebook_is_clean_and_uses_the_project_kernel() -> None:
    notebook = _notebook()
    assert notebook["nbformat"] == 4
    assert notebook["metadata"] == {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.12"},
    }
    code_cells = [
        cell for cell in notebook["cells"]  # type: ignore[index]
        if cell["cell_type"] == "code"
    ]
    assert all(cell["execution_count"] is None for cell in code_cells)
    assert all(cell["outputs"] == [] for cell in code_cells)


def test_aging_notebook_code_is_valid_python() -> None:
    notebook = _notebook()
    for cell in notebook["cells"]:  # type: ignore[index]
        if cell["cell_type"] == "code":
            ast.parse("".join(cell["source"]))


def test_aging_notebook_keeps_models_and_claims_qualified() -> None:
    source = _all_source(_notebook())
    assert "Part 04 of Battery Core Chapter 1" in source
    assert "state-of-health estimator" in source
    assert "simplified outputs used by the teaching model" in source
    assert "cell- and duty-specific" in source
    assert (
        "deep discharge should not be used as a general rejuvenation method"
        in source
    )
    assert "it is not guaranteed to appear first" in source
    assert "warning signal rather than proof of one specific mechanism" in source
    assert "Nothing else" not in source
    assert "first year costs more than the next four" not in source
    assert "reconditioning" not in source.lower()


def test_aging_notebook_embeds_all_panels_without_external_code() -> None:
    assets = _assets(_notebook())
    assert set(assets["widgets"]) == {
        "theme", "map", "cell", "sei", "gas",
        "crystal", "plating", "cracking", "sim", "window",
    }
    joined = "\n".join(assets["widgets"].values())
    assert "Temperature shifts the aging balance" in assets["widgets"]["window"]
    assert not re.search(r"<script[^>]+src=[\"\']https?://", joined)
    assert not re.search(r"<link[^>]+href=[\"\']https?://", joined)


def test_aging_notebook_cites_primary_literature() -> None:
    source = _all_source(_notebook())
    for doi in (
        "10.1016/j.jpowsour.2005.01.006",
        "10.1149/2.044302jes",
        "10.1016/j.jpowsour.2018.02.063",
        "10.1007/s10008-006-0095-1",
        "10.1149/1945-7111/ac6d13",
    ):
        assert doi in source
