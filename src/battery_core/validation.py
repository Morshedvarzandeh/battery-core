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

"""Shared domain-validation helpers for battery-core inputs.

Convention: :class:`TypeError` signals a non-numeric input, while
:class:`ValueError` signals a numeric input that falls outside its physical
domain. Every error message names the offending parameter.
"""

from typing import TypeAlias

import numpy as np
import numpy.typing as npt

FloatArray: TypeAlias = npt.NDArray[np.float64]


def as_finite_array(name: str, value: float | npt.ArrayLike) -> FloatArray:
    """Coerce ``value`` to a finite ``float64`` array.

    Args:
        name: Parameter name used in error messages.
        value: A scalar or array-like numeric input.

    Returns:
        The value as a ``float64`` NumPy array.

    Raises:
        TypeError: If the input dtype is not real-numeric (for example a
            string ``"20"`` or a complex number).
        ValueError: If any entry is non-finite.

    """
    array = np.asarray(value)
    if not np.issubdtype(array.dtype, np.number) or np.issubdtype(
        array.dtype, np.complexfloating
    ):
        raise TypeError(f"{name} must be a real numeric value")
    array = array.astype(np.float64)
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def positive_finite_array(name: str, value: float | npt.ArrayLike) -> FloatArray:
    """Validate that ``value`` is finite and strictly positive.

    Raises:
        TypeError: If the input is not real-numeric.
        ValueError: If any entry is non-finite or not strictly positive.

    """
    array = as_finite_array(name, value)
    if np.any(array <= 0.0):
        raise ValueError(f"{name} must contain only positive values")
    return array


def non_negative_finite_array(name: str, value: float | npt.ArrayLike) -> FloatArray:
    """Validate that ``value`` is finite and non-negative.

    Raises:
        TypeError: If the input is not real-numeric.
        ValueError: If any entry is non-finite or negative.

    """
    array = as_finite_array(name, value)
    if np.any(array < 0.0):
        raise ValueError(f"{name} must contain only non-negative values")
    return array


def scalar_or_array(value: FloatArray) -> float | FloatArray:
    """Return a Python ``float`` for a 0-d array, otherwise the array itself."""
    if value.ndim == 0:
        return float(value)
    return value
