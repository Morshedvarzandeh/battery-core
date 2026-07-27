"""Tests for solver-independent diffusion physics."""

import numpy as np
import pytest

from battery_core.diffusion import ficks_first_law_flux


def test_zero_gradient_has_zero_flux() -> None:
    assert ficks_first_law_flux(1.0e-14, 0.0) == 0.0


@pytest.mark.parametrize(
    ("gradient", "expected_flux"),
    [(2.0e6, -2.0e-8), (-2.0e6, 2.0e-8)],
)
def test_flux_for_positive_and_negative_gradients(
    gradient: float, expected_flux: float
) -> None:
    assert ficks_first_law_flux(1.0e-14, gradient) == pytest.approx(expected_flux)


@pytest.mark.parametrize("diffusivity", [-1.0, np.inf, -np.inf, np.nan])
def test_invalid_diffusivity_is_rejected(diffusivity: float) -> None:
    with pytest.raises(ValueError, match="diffusivity"):
        ficks_first_law_flux(diffusivity, 1.0)


@pytest.mark.parametrize("gradient", [np.inf, -np.inf, np.nan])
def test_non_finite_gradient_is_rejected(gradient: float) -> None:
    with pytest.raises(ValueError, match="concentration_gradient"):
        ficks_first_law_flux(1.0e-14, gradient)


def test_array_with_non_finite_gradient_is_rejected() -> None:
    with pytest.raises(ValueError, match="concentration_gradient"):
        ficks_first_law_flux(1.0e-14, [0.0, np.nan])


def test_mass_flux_direction_and_sign_convention() -> None:
    """Molar and mass flux point down the concentration gradient."""
    gradients = np.array([-3.0, 0.0, 3.0])
    molar_flux = ficks_first_law_flux(2.0, gradients)
    molar_mass_kg_per_mol = 0.010
    mass_flux = molar_flux * molar_mass_kg_per_mol

    np.testing.assert_array_equal(molar_flux, np.array([6.0, 0.0, -6.0]))
    np.testing.assert_array_equal(mass_flux, np.array([0.06, 0.0, -0.06]))
