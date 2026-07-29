"""Solver-independent constitutive relations for diffusion."""

from typing import TypeAlias

import numpy as np
import numpy.typing as npt

from battery_core.validation import (
    as_finite_array,
    non_negative_finite_array,
    scalar_or_array,
)

FloatArray: TypeAlias = npt.NDArray[np.float64]


def ficks_first_law_flux(
    diffusivity: float | npt.ArrayLike,
    concentration_gradient: float | npt.ArrayLike,
) -> float | FloatArray:
    """Calculate one-dimensional diffusive flux using Fick's first law.

    The implemented physical relation is ``J = -D * dc/dx``. This function
    evaluates the constitutive law only; it does not estimate a gradient,
    discretize a domain, or apply boundary conditions.

    Args:
        diffusivity: Diffusion coefficient ``D`` in square metres per second
            (m²/s). A scalar or array is accepted so a spatially varying
            medium can be described, and every value must be finite and
            non-negative. It broadcasts against ``concentration_gradient``.
        concentration_gradient: Spatial concentration gradient ``dc/dx`` in
            moles per cubic metre per metre (mol/m⁴). A scalar or array is
            accepted, and every value must be finite.

    Returns:
        Diffusive molar flux ``J`` in moles per square metre per second
        (mol/(m²·s)). A scalar input produces a float; an array-like input
        produces a NumPy array whose shape follows NumPy broadcasting.
        Positive flux is defined in the positive coordinate direction.

    Raises:
        TypeError: If either input is not a real numeric value.
        ValueError: If any ``diffusivity`` value is negative or non-finite, or
            if any concentration-gradient value is non-finite.

    """
    coefficient = non_negative_finite_array("diffusivity", diffusivity)
    gradient = as_finite_array("concentration_gradient", concentration_gradient)
    return scalar_or_array(-coefficient * gradient)
