"""Ideal capacity and C-rate relationships for battery cells."""

from typing import TypeAlias

import numpy as np
import numpy.typing as npt

from battery_core.validation import (
    non_negative_finite_array,
    positive_finite_array,
    scalar_or_array,
)

FloatArray: TypeAlias = npt.NDArray[np.float64]


def current_from_c_rate(
    *,
    nominal_capacity_ah: float | npt.ArrayLike,
    c_rate: float | npt.ArrayLike,
) -> float | FloatArray:
    """Calculate constant current from nominal capacity and C-rate.

    The ideal definition is ``I = Q_nominal * C_rate`` when nominal capacity
    is expressed in ampere-hours and C-rate is expressed in reciprocal hours.

    This function is keyword-only: ``nominal_capacity_ah`` and ``c_rate`` must
    be passed by name so a transposed call cannot silently return a plausible
    but wrong number.

    Args:
        nominal_capacity_ah: Nominal cell capacity in ampere-hours (Ah). Must
            be strictly positive.
        c_rate: C-rate, such as ``0.1`` for C/10, ``1`` for 1C, or ``10`` for
            10C. Must be non-negative; ``0`` represents a rest step.

    Returns:
        Constant current in amperes (A). Inputs follow NumPy broadcasting.
        Scalar inputs produce a float.

    Raises:
        TypeError: If either input is not a real numeric value.
        ValueError: If ``nominal_capacity_ah`` is non-finite or not positive,
            or if ``c_rate`` is non-finite or negative.

    """
    capacity = positive_finite_array("nominal_capacity_ah", nominal_capacity_ah)
    rate = non_negative_finite_array("c_rate", c_rate)
    return scalar_or_array(capacity * rate)


def c_rate_from_current(
    *,
    current_a: float | npt.ArrayLike,
    nominal_capacity_ah: float | npt.ArrayLike,
) -> float | FloatArray:
    """Calculate C-rate from constant current and nominal capacity.

    This function is keyword-only: ``current_a`` and ``nominal_capacity_ah``
    must be passed by name so a transposed call cannot silently return a
    plausible but wrong number.

    Args:
        current_a: Current magnitude in amperes (A). Must be non-negative;
            ``0`` represents a rest step.
        nominal_capacity_ah: Nominal cell capacity in ampere-hours (Ah). Must
            be strictly positive.

    Returns:
        C-rate in reciprocal hours (h⁻¹). Inputs follow NumPy broadcasting.
        Scalar inputs produce a float.

    Raises:
        TypeError: If either input is not a real numeric value.
        ValueError: If ``current_a`` is non-finite or negative, or if
            ``nominal_capacity_ah`` is non-finite or not positive.

    """
    current = non_negative_finite_array("current_a", current_a)
    capacity = positive_finite_array("nominal_capacity_ah", nominal_capacity_ah)
    return scalar_or_array(current / capacity)


def ideal_duration_hours(
    c_rate: float | npt.ArrayLike,
) -> float | FloatArray:
    """Calculate ideal full-capacity duration at a constant C-rate.

    The ideal duration is ``t = 1 / C_rate`` hours. This is a definitional
    relationship only. It does not predict voltage-cutoff time or rate-dependent
    usable capacity for a real cell.

    Args:
        c_rate: Strictly positive C-rate. A duration is undefined at ``0`` C
            (``1 / 0``), so a rest step is rejected here.

    Returns:
        Ideal duration in hours. Scalar input produces a float.

    Raises:
        TypeError: If ``c_rate`` is not a real numeric value.
        ValueError: If ``c_rate`` is non-finite or not strictly positive.

    """
    rate = positive_finite_array("c_rate", c_rate)
    return scalar_or_array(1.0 / rate)
