"""Tests for ideal capacity and C-rate relationships."""

import numpy as np
import pytest

from battery_core.capacity import (
    c_rate_from_current,
    current_from_c_rate,
    ideal_duration_hours,
)


@pytest.mark.parametrize(
    ("c_rate", "expected_current_a", "expected_hours"),
    [
        (0.1, 2.0, 10.0),
        (1.0, 20.0, 1.0),
        (2.0, 40.0, 0.5),
        (10.0, 200.0, 0.1),
    ],
)
def test_twenty_ah_examples(
    c_rate: float,
    expected_current_a: float,
    expected_hours: float,
) -> None:
    assert current_from_c_rate(
        nominal_capacity_ah=20.0, c_rate=c_rate
    ) == pytest.approx(expected_current_a)
    assert ideal_duration_hours(c_rate) == pytest.approx(expected_hours)


def test_ten_c_duration_is_six_minutes() -> None:
    minutes = ideal_duration_hours(10.0) * 60.0
    assert minutes == pytest.approx(6.0)


def test_c_rate_round_trip() -> None:
    current = current_from_c_rate(nominal_capacity_ah=20.0, c_rate=2.5)
    assert c_rate_from_current(
        current_a=current, nominal_capacity_ah=20.0
    ) == pytest.approx(2.5)


def test_array_inputs_are_vectorized() -> None:
    rates = np.array([0.1, 1.0, 10.0])
    np.testing.assert_allclose(
        current_from_c_rate(nominal_capacity_ah=20.0, c_rate=rates),
        np.array([2.0, 20.0, 200.0]),
    )
    np.testing.assert_allclose(
        ideal_duration_hours(rates),
        np.array([10.0, 1.0, 0.1]),
    )


def test_broadcasting_capacity_and_rate() -> None:
    capacities = np.array([10.0, 20.0, 40.0])
    rates = np.array([0.5, 1.0, 2.0])
    np.testing.assert_allclose(
        current_from_c_rate(nominal_capacity_ah=capacities, c_rate=rates),
        np.array([5.0, 20.0, 80.0]),
    )


def test_rest_step_zero_c_rate_gives_zero_current() -> None:
    """A rest step is physical: zero C-rate means zero current."""
    assert current_from_c_rate(nominal_capacity_ah=20.0, c_rate=0.0) == 0.0


def test_rest_step_zero_current_gives_zero_c_rate() -> None:
    """A rest step is physical: zero current means zero C-rate."""
    assert c_rate_from_current(current_a=0.0, nominal_capacity_ah=20.0) == 0.0


def test_current_profile_with_rest_step() -> None:
    """A current profile may contain a rest (0 A) segment."""
    currents = np.array([0.0, 10.0, 20.0])
    np.testing.assert_allclose(
        c_rate_from_current(current_a=currents, nominal_capacity_ah=20.0),
        np.array([0.0, 0.5, 1.0]),
    )


@pytest.mark.parametrize("bad_value", [-1.0, np.inf, -np.inf, np.nan])
def test_invalid_c_rate_is_rejected(bad_value: float) -> None:
    with pytest.raises(ValueError, match="c_rate"):
        current_from_c_rate(nominal_capacity_ah=20.0, c_rate=bad_value)


@pytest.mark.parametrize("bad_value", [0.0, -1.0, np.inf, -np.inf, np.nan])
def test_invalid_c_rate_for_duration_is_rejected(bad_value: float) -> None:
    with pytest.raises(ValueError, match="c_rate"):
        ideal_duration_hours(bad_value)


@pytest.mark.parametrize("bad_value", [0.0, -1.0, np.inf, -np.inf, np.nan])
def test_invalid_capacity_is_rejected(bad_value: float) -> None:
    with pytest.raises(ValueError, match="nominal_capacity_ah"):
        current_from_c_rate(nominal_capacity_ah=bad_value, c_rate=1.0)
    with pytest.raises(ValueError, match="nominal_capacity_ah"):
        c_rate_from_current(current_a=20.0, nominal_capacity_ah=bad_value)


@pytest.mark.parametrize("bad_value", [-1.0, np.inf, -np.inf, np.nan])
def test_invalid_current_is_rejected(bad_value: float) -> None:
    with pytest.raises(ValueError, match="current_a"):
        c_rate_from_current(current_a=bad_value, nominal_capacity_ah=20.0)


@pytest.mark.parametrize("bad_value", ["20", "fast", [1.0, "2.0"]])
def test_non_numeric_input_raises_type_error(bad_value: object) -> None:
    """A numeric-looking string must be rejected, not silently parsed."""
    with pytest.raises(TypeError):
        current_from_c_rate(nominal_capacity_ah=bad_value, c_rate=1.0)


def test_positional_call_raises_type_error() -> None:
    """The keyword-only signature guards against transposed arguments."""
    with pytest.raises(TypeError):
        current_from_c_rate(20.0, 10.0)  # type: ignore[misc]
    with pytest.raises(TypeError):
        c_rate_from_current(20.0, 40.0)  # type: ignore[misc]
