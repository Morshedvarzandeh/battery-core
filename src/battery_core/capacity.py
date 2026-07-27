"""Ideal capacity and C-rate relationships for battery cells."""

from typing import TypeAlias

import numpy as np
import numpy.typing as npt

FloatArray: TypeAlias = npt.NDArray[np.float64]


def _positive_finite_array(name: str, value: float | npt.ArrayLike) -> FloatArray:
    array = np.asarray(value, dtype=np.float64)
    if not np.all(np.isfinite(array)) or np.any(array <= 0.0):
        raise ValueError(f"{name} must contain only finite, positive values")
    return array


def _scalar_or_array(value: FloatArray) -> float | FloatArray:
    if value.ndim == 0:
        return float(value)
    return value


def current_from_c_rate(
    nominal_capacity_ah: float | npt.ArrayLike,
    c_rate: float | npt.ArrayLike,
) -> float | FloatArray:
    """Calculate constant current from nominal capacity and C-rate.

    The ideal definition is ``I = Q_nominal * C_rate`` when nominal capacity
    is expressed in ampere-hours and C-rate is expressed in reciprocal hours.

    Args:
        nominal_capacity_ah: Nominal cell capacity in ampere-hours (Ah).
        c_rate: Positive C-rate, such as ``0.1`` for C/10, ``1`` for 1C, or
            ``10`` for 10C.

    Returns:
        Constant current in amperes (A). Inputs follow NumPy broadcasting.
        Scalar inputs produce a float.

    Raises:
        ValueError: If either input contains a non-finite or non-positive value.

    """
    capacity = _positive_finite_array("nominal_capacity_ah", nominal_capacity_ah)
    rate = _positive_finite_array("c_rate", c_rate)
    return _scalar_or_array(capacity * rate)


def c_rate_from_current(
    current_a: float | npt.ArrayLike,
    nominal_capacity_ah: float | npt.ArrayLike,
) -> float | FloatArray:
    """Calculate C-rate from constant current and nominal capacity.

    Args:
        current_a: Positive current magnitude in amperes (A).
        nominal_capacity_ah: Nominal cell capacity in ampere-hours (Ah).

    Returns:
        C-rate in reciprocal hours (h⁻¹). Inputs follow NumPy broadcasting.
        Scalar inputs produce a float.

    Raises:
        ValueError: If either input contains a non-finite or non-positive value.

    """
    current = _positive_finite_array("current_a", current_a)
    capacity = _positive_finite_array("nominal_capacity_ah", nominal_capacity_ah)
    return _scalar_or_array(current / capacity)


def ideal_duration_hours(
    c_rate: float | npt.ArrayLike,
) -> float | FloatArray:
    """Calculate ideal full-capacity duration at a constant C-rate.

    The ideal duration is ``t = 1 / C_rate`` hours. This is a definitional
    relationship only. It does not predict voltage-cutoff time or rate-dependent
    usable capacity for a real cell.

    Args:
        c_rate: Positive C-rate.

    Returns:
        Ideal duration in hours. Scalar input produces a float.

    Raises:
        ValueError: If ``c_rate`` contains a non-finite or non-positive value.

    """
    rate = _positive_finite_array("c_rate", c_rate)
    return _scalar_or_array(1.0 / rate)
