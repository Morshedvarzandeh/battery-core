"""Tests for the shared domain-validation helpers.

The convention under test is that ``TypeError`` means "not a number" and
``ValueError`` means "a number outside its physical domain".
"""

import numpy as np
import pytest

from battery_core.validation import (
    as_finite_array,
    non_negative_finite_array,
    positive_finite_array,
    scalar_or_array,
)

ALL_VALIDATORS = [as_finite_array, positive_finite_array, non_negative_finite_array]


@pytest.mark.parametrize("validator", ALL_VALIDATORS)
@pytest.mark.parametrize(
    "bad_value",
    ["20", "fast", [1.0, "2.0"], None, {"value": 1.0}, object()],
)
def test_non_numeric_input_raises_type_error(
    validator: object, bad_value: object
) -> None:
    """A non-numeric input is rejected instead of being coerced."""
    with pytest.raises(TypeError, match="param"):
        validator("param", bad_value)  # type: ignore[operator]


@pytest.mark.parametrize("validator", ALL_VALIDATORS)
@pytest.mark.parametrize("bad_value", [1 + 2j, np.array([1 + 2j]), np.complex128(3)])
def test_complex_input_raises_type_error(validator: object, bad_value: object) -> None:
    """Complex numbers are numeric but are not a real physical quantity."""
    with pytest.raises(TypeError, match="param"):
        validator("param", bad_value)  # type: ignore[operator]


@pytest.mark.parametrize("validator", ALL_VALIDATORS)
def test_bool_input_raises_type_error(validator: object) -> None:
    """``True`` is not a measurement, so it is not accepted as one."""
    with pytest.raises(TypeError, match="param"):
        validator("param", True)  # type: ignore[operator]


@pytest.mark.parametrize("validator", ALL_VALIDATORS)
@pytest.mark.parametrize("bad_value", [np.inf, -np.inf, np.nan])
def test_non_finite_input_raises_value_error(
    validator: object, bad_value: float
) -> None:
    """A non-finite float is numeric, so it is a domain error."""
    with pytest.raises(ValueError, match="param"):
        validator("param", bad_value)  # type: ignore[operator]


@pytest.mark.parametrize("validator", ALL_VALIDATORS)
def test_integer_input_is_cast_to_float64(validator: object) -> None:
    array = validator("param", 5)  # type: ignore[operator]
    assert array.dtype == np.float64
    assert array == 5.0


@pytest.mark.parametrize("validator", ALL_VALIDATORS)
def test_error_message_names_the_parameter(validator: object) -> None:
    """Every message identifies which argument was wrong."""
    with pytest.raises(TypeError, match="nominal_capacity_ah"):
        validator("nominal_capacity_ah", "20")  # type: ignore[operator]
    with pytest.raises(ValueError, match="nominal_capacity_ah"):
        validator("nominal_capacity_ah", np.nan)  # type: ignore[operator]


def test_as_finite_array_accepts_any_sign() -> None:
    np.testing.assert_allclose(
        as_finite_array("param", [-2.0, 0.0, 2.0]),
        np.array([-2.0, 0.0, 2.0]),
    )


@pytest.mark.parametrize("bad_value", [0.0, -1.0, [1.0, -1.0], [1.0, 0.0]])
def test_positive_rejects_zero_and_negative(bad_value: object) -> None:
    with pytest.raises(ValueError, match="param"):
        positive_finite_array("param", bad_value)


def test_positive_accepts_strictly_positive() -> None:
    np.testing.assert_allclose(
        positive_finite_array("param", [0.5, 1.0, 2.0]),
        np.array([0.5, 1.0, 2.0]),
    )


@pytest.mark.parametrize("bad_value", [-1.0, [1.0, -0.5]])
def test_non_negative_rejects_negative(bad_value: object) -> None:
    with pytest.raises(ValueError, match="param"):
        non_negative_finite_array("param", bad_value)


def test_non_negative_accepts_zero() -> None:
    """Zero is physical: it is a rest step, not a domain violation."""
    np.testing.assert_allclose(
        non_negative_finite_array("param", [0.0, 1.0]),
        np.array([0.0, 1.0]),
    )


@pytest.mark.parametrize("validator", ALL_VALIDATORS)
def test_empty_array_is_accepted(validator: object) -> None:
    """An empty array has no offending entry, so it passes and stays empty."""
    result = validator("param", np.array([]))  # type: ignore[operator]
    assert result.shape == (0,)
    assert result.dtype == np.float64


def test_scalar_or_array_returns_a_real_float_for_zero_d() -> None:
    """The 0-d case must be converted, not merely compared equal."""
    result = scalar_or_array(np.asarray(3.0))
    assert isinstance(result, float)
    assert not isinstance(result, np.ndarray)
    assert result == 3.0


def test_scalar_or_array_returns_the_array_unchanged() -> None:
    array = np.array([1.0, 2.0])
    result = scalar_or_array(array)
    assert isinstance(result, np.ndarray)
    assert result is array


def test_scalar_or_array_keeps_one_element_array_as_array() -> None:
    """A one-element 1-d array is not a scalar and must not be collapsed."""
    result = scalar_or_array(np.array([3.0]))
    assert isinstance(result, np.ndarray)
    assert result.shape == (1,)
