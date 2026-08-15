# battery-core — open-source battery engineering fundamentals.
# Copyright (C) 2026 Morshed Varzandeh and battery-core contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
    # no asset may be pulled from the network; a URL in prose or in the
    # licence header is not an asset reference
    assert 'src="https://' not in html
    assert 'href="https://' not in html
    assert "url(https://" not in html


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
