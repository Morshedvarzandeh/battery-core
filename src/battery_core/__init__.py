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

"""Core, solver-independent equations for battery modeling."""

from importlib.metadata import PackageNotFoundError, version

from battery_core.aging import arrhenius_factor, parabolic_film_thickness
from battery_core.capacity import (
    c_rate_from_current,
    current_from_c_rate,
    ideal_duration_hours,
)
from battery_core.diffusion import ficks_first_law_flux

__all__ = [
    "arrhenius_factor",
    "c_rate_from_current",
    "current_from_c_rate",
    "ficks_first_law_flux",
    "ideal_duration_hours",
    "parabolic_film_thickness",
]

try:
    __version__ = version("battery-core")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"
