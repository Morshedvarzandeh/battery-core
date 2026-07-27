"""Solver-independent constitutive relations for diffusion."""

from typing import TypeAlias

import numpy as np
import numpy.typing as npt

FloatArray: TypeAlias = npt.NDArray[np.float64]


def ficks_first_law_flux(
    diffusivity: float,
    concentration_gradient: float | npt.ArrayLike,
) -> float | FloatArray:
    """Calculate one-dimensional diffusive flux using Fick's first law.

    The implemented physical relation is ``J = -D * dc/dx``. This function
    evaluates the constitutive law only; it does not estimate a gradient,
    discretize a domain, or apply boundary conditions.

    Args:
        diffusivity: Diffusion coefficient ``D`` in square metres per second
            (m²/s). It must be finite and non-negative.
        concentration_gradient: Spatial concentration gradient ``dc/dx`` in
            moles per cubic metre per metre (mol/m⁴). A scalar or array is
            accepted, and every value must be finite.

    Returns:
        Diffusive molar flux ``J`` in moles per square metre per second
        (mol/(m²·s)). A scalar input produces a float; an array-like input
        produces a NumPy array with the same shape. Positive flux is defined
        in the positive coordinate direction.

    Raises:
        ValueError: If ``diffusivity`` is negative or non-finite, or if any
            concentration-gradient value is non-finite.

    """
    if not np.isfinite(diffusivity) or diffusivity < 0.0:
        raise ValueError("diffusivity must be finite and non-negative")

    gradient = np.asarray(concentration_gradient, dtype=np.float64)
    if not np.all(np.isfinite(gradient)):
        raise ValueError("concentration_gradient must contain only finite values")

    flux = -diffusivity * gradient
    if flux.ndim == 0:
        return float(flux)
    return flux
