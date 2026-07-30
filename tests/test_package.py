"""Tests for the package's public surface and version metadata."""

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:  # Python 3.10 has no tomllib; the project still supports it.
    import tomli as tomllib

import battery_core

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"


def test_version_matches_pyproject() -> None:
    """``__version__`` is read from metadata, so it cannot drift."""
    pyproject = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    assert battery_core.__version__ == pyproject["project"]["version"]


def test_version_is_not_the_uninstalled_fallback() -> None:
    """A test run against an installed package must not hit the fallback."""
    assert battery_core.__version__ != "0.0.0"


def test_all_names_are_importable() -> None:
    for name in battery_core.__all__:
        assert hasattr(battery_core, name), name


def test_all_is_sorted_and_unique() -> None:
    assert battery_core.__all__ == sorted(battery_core.__all__)
    assert len(battery_core.__all__) == len(set(battery_core.__all__))
