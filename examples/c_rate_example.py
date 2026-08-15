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

"""Evaluate ideal current and duration for several C-rates."""

import numpy as np

from battery_core import current_from_c_rate, ideal_duration_hours


def main() -> None:
    """Print ideal C-rate values for an illustrative 20 Ah cell."""
    nominal_capacity_ah = 20.0
    rates = np.array([0.1, 1.0, 2.0, 10.0])
    currents_a = current_from_c_rate(
        nominal_capacity_ah=nominal_capacity_ah, c_rate=rates
    )
    durations_h = ideal_duration_hours(rates)

    print("C-rate [h^-1]:", rates)
    print("Current [A]:", currents_a)
    print("Ideal duration [h]:", durations_h)


if __name__ == "__main__":
    main()
