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
