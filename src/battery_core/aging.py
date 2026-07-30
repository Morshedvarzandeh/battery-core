"""Solver-independent rate relationships for battery degradation.

Two relationships account for most of how a cell ages, and both are general
enough to state without committing to a chemistry:

- an Arrhenius factor, because degradation is chemistry and chemistry speeds up
  with temperature; and
- a parabolic growth law, because a passivating film is its own diffusion
  barrier, so it thickens with the square root of time rather than linearly.

This module implements those two laws only. It does not fit them, combine them
into a state-of-health estimate, or supply chemistry-specific constants: an
activation energy and a reference film thickness are inputs, exactly as the
diffusion coefficient is an input to Fick's first law. Calibrated coefficients
belong to a validated model of a specific cell, not to this module.
"""

from typing import TypeAlias

import numpy as np
import numpy.typing as npt

from battery_core.validation import (
    as_finite_array,
    non_negative_finite_array,
    positive_finite_array,
    scalar_or_array,
)

FloatArray: TypeAlias = npt.NDArray[np.float64]

ABSOLUTE_ZERO_C: float = -273.15
"""Absolute zero in degrees Celsius."""

MOLAR_GAS_CONSTANT: float = 8.31446261815324
"""Molar gas constant ``R`` in J/(mol·K), exact under the 2019 SI definition."""


def _temperature_kelvin(name: str, value: float | npt.ArrayLike) -> FloatArray:
    """Validate a Celsius temperature and convert it to kelvin."""
    celsius = as_finite_array(name, value)
    if np.any(celsius <= ABSOLUTE_ZERO_C):
        raise ValueError(f"{name} must be above absolute zero ({ABSOLUTE_ZERO_C} °C)")
    return celsius - ABSOLUTE_ZERO_C


def arrhenius_factor(
    *,
    temperature_c: float | npt.ArrayLike,
    activation_energy_j_per_mol: float | npt.ArrayLike,
    reference_temperature_c: float | npt.ArrayLike = 25.0,
) -> float | FloatArray:
    """Calculate how much faster a thermally activated process runs at one
    temperature than at another.

    The implemented relation is
    ``k(T) / k(T_ref) = exp[(Ea / R) * (1 / T_ref - 1 / T)]`` with both
    temperatures in kelvin. For an activation energy near 50 kJ/mol this
    reproduces the familiar rule of thumb that the rate roughly doubles per
    10 °C.

    This function is keyword-only. Both temperatures are Celsius values of
    similar magnitude, so transposing them would silently invert the result:
    a factor of 3.5 and a factor of 0.29 are each plausible on their own.

    Args:
        temperature_c: Temperature of interest in degrees Celsius (°C). Must be
            above absolute zero.
        activation_energy_j_per_mol: Activation energy ``Ea`` in joules per mole
            (J/mol). Must be non-negative; zero describes a process with no
            temperature dependence, giving a factor of 1.
        reference_temperature_c: Temperature the factor is relative to, in
            degrees Celsius (°C). Defaults to 25 °C. Must be above absolute
            zero.

    Returns:
        The dimensionless rate ratio. It is greater than 1 above the reference
        temperature and less than 1 below it. Inputs follow NumPy broadcasting,
        and scalar inputs produce a float.

    Raises:
        TypeError: If any input is not a real numeric value.
        ValueError: If a temperature is at or below absolute zero, if any input
            is non-finite, or if the activation energy is negative.

    """
    temperature_k = _temperature_kelvin("temperature_c", temperature_c)
    reference_k = _temperature_kelvin(
        "reference_temperature_c", reference_temperature_c
    )
    activation_energy = non_negative_finite_array(
        "activation_energy_j_per_mol", activation_energy_j_per_mol
    )
    reciprocal_difference = 1.0 / reference_k - 1.0 / temperature_k
    exponent = activation_energy / MOLAR_GAS_CONSTANT * reciprocal_difference
    return scalar_or_array(np.exp(exponent))


def parabolic_film_thickness(
    *,
    reference_thickness: float | npt.ArrayLike,
    elapsed_time: float | npt.ArrayLike,
    reference_time: float | npt.ArrayLike = 1.0,
    acceleration_factor: float | npt.ArrayLike = 1.0,
) -> float | FloatArray:
    """Calculate the thickness of a diffusion-limited passivating film.

    The implemented relation is
    ``delta(t) = delta_ref * sqrt(t / t_ref * A)``. A growing film is its own
    diffusion barrier, so growth is parabolic: quadrupling the time doubles the
    thickness. ``A`` scales the elapsed time to account for conditions that run
    the reaction faster or slower, and :func:`arrhenius_factor` is the usual
    source of it.

    This function is keyword-only. ``elapsed_time`` and ``reference_time`` carry
    the same units and are therefore transposable, and swapping them returns the
    reciprocal of the intended ratio.

    Args:
        reference_thickness: Film thickness measured at ``reference_time`` under
            reference conditions, in any length unit. The result carries the
            same unit. Must be non-negative.
        elapsed_time: Time the film has been growing, in any time unit. Must be
            non-negative; zero means no film has formed yet.
        reference_time: Time at which ``reference_thickness`` was measured, in
            the same unit as ``elapsed_time``. Defaults to 1. Must be strictly
            positive.
        acceleration_factor: Dimensionless multiplier on elapsed time, such as
            an Arrhenius factor. Defaults to 1. Must be non-negative.

    Returns:
        Film thickness in the unit of ``reference_thickness``. Inputs follow
        NumPy broadcasting, and scalar inputs produce a float.

    Raises:
        TypeError: If any input is not a real numeric value.
        ValueError: If any input is non-finite, if ``reference_time`` is not
            strictly positive, or if any other input is negative.

    """
    thickness = non_negative_finite_array("reference_thickness", reference_thickness)
    elapsed = non_negative_finite_array("elapsed_time", elapsed_time)
    reference = positive_finite_array("reference_time", reference_time)
    acceleration = non_negative_finite_array(
        "acceleration_factor", acceleration_factor
    )
    return scalar_or_array(thickness * np.sqrt(elapsed / reference * acceleration))
