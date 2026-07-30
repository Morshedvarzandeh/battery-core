"""Tests for the solver-independent degradation rate laws."""

import numpy as np
import pytest

from battery_core.aging import (
    ABSOLUTE_ZERO_C,
    MOLAR_GAS_CONSTANT,
    arrhenius_factor,
    parabolic_film_thickness,
)


def test_factor_is_one_at_the_reference_temperature() -> None:
    assert arrhenius_factor(
        temperature_c=25.0, activation_energy_j_per_mol=50_000.0
    ) == pytest.approx(1.0)


def test_factor_is_one_at_any_temperature_without_activation_energy() -> None:
    """Zero activation energy describes a temperature-independent process."""
    assert arrhenius_factor(
        temperature_c=60.0, activation_energy_j_per_mol=0.0
    ) == pytest.approx(1.0)


def test_rate_roughly_doubles_per_ten_degrees() -> None:
    """The familiar rule of thumb, near 50 kJ/mol."""
    factor = arrhenius_factor(
        temperature_c=35.0, activation_energy_j_per_mol=50_000.0
    )
    assert factor == pytest.approx(1.92, abs=0.01)


def test_hotter_is_faster_and_colder_is_slower() -> None:
    hot = arrhenius_factor(temperature_c=45.0, activation_energy_j_per_mol=50_000.0)
    cold = arrhenius_factor(temperature_c=0.0, activation_energy_j_per_mol=50_000.0)
    assert hot > 1.0 > cold > 0.0
    assert hot == pytest.approx(3.55, abs=0.01)


def test_factor_matches_the_closed_form() -> None:
    temperature_k, reference_k = 45.0 - ABSOLUTE_ZERO_C, 25.0 - ABSOLUTE_ZERO_C
    expected = np.exp(
        50_000.0 / MOLAR_GAS_CONSTANT * (1.0 / reference_k - 1.0 / temperature_k)
    )
    assert arrhenius_factor(
        temperature_c=45.0, activation_energy_j_per_mol=50_000.0
    ) == pytest.approx(expected)


def test_swapping_the_temperatures_inverts_the_factor() -> None:
    """Why the signature is keyword-only: both orders return plausible numbers."""
    forward = arrhenius_factor(
        temperature_c=45.0,
        activation_energy_j_per_mol=50_000.0,
        reference_temperature_c=25.0,
    )
    backward = arrhenius_factor(
        temperature_c=25.0,
        activation_energy_j_per_mol=50_000.0,
        reference_temperature_c=45.0,
    )
    assert forward * backward == pytest.approx(1.0)


def test_higher_activation_energy_is_more_temperature_sensitive() -> None:
    mild = arrhenius_factor(temperature_c=45.0, activation_energy_j_per_mol=45_000.0)
    steep = arrhenius_factor(temperature_c=45.0, activation_energy_j_per_mol=62_000.0)
    assert steep > mild > 1.0


def test_arrhenius_accepts_arrays() -> None:
    factors = arrhenius_factor(
        temperature_c=np.array([15.0, 25.0, 35.0]),
        activation_energy_j_per_mol=50_000.0,
    )
    assert isinstance(factors, np.ndarray)
    assert factors[0] < factors[1] < factors[2]
    assert factors[1] == pytest.approx(1.0)


def test_arrhenius_scalar_returns_a_real_float() -> None:
    result = arrhenius_factor(
        temperature_c=30.0, activation_energy_j_per_mol=50_000.0
    )
    assert isinstance(result, float)
    assert not isinstance(result, np.ndarray)


@pytest.mark.parametrize("bad_temperature", [ABSOLUTE_ZERO_C, -300.0, -1000.0])
def test_temperature_at_or_below_absolute_zero_is_rejected(
    bad_temperature: float,
) -> None:
    with pytest.raises(ValueError, match="temperature_c"):
        arrhenius_factor(
            temperature_c=bad_temperature, activation_energy_j_per_mol=50_000.0
        )
    with pytest.raises(ValueError, match="reference_temperature_c"):
        arrhenius_factor(
            temperature_c=25.0,
            activation_energy_j_per_mol=50_000.0,
            reference_temperature_c=bad_temperature,
        )


def test_negative_activation_energy_is_rejected() -> None:
    with pytest.raises(ValueError, match="activation_energy_j_per_mol"):
        arrhenius_factor(
            temperature_c=25.0, activation_energy_j_per_mol=-1_000.0
        )


@pytest.mark.parametrize("bad_value", [np.inf, -np.inf, np.nan])
def test_non_finite_arrhenius_input_is_rejected(bad_value: float) -> None:
    with pytest.raises(ValueError, match="temperature_c"):
        arrhenius_factor(
            temperature_c=bad_value, activation_energy_j_per_mol=50_000.0
        )


@pytest.mark.parametrize("bad_value", ["25", "hot"])
def test_non_numeric_arrhenius_input_is_rejected(bad_value: object) -> None:
    with pytest.raises(TypeError):
        arrhenius_factor(
            temperature_c=bad_value, activation_energy_j_per_mol=50_000.0
        )


def test_arrhenius_positional_call_raises_type_error() -> None:
    with pytest.raises(TypeError):
        arrhenius_factor(45.0, 50_000.0)  # type: ignore[misc]


def test_thickness_equals_reference_at_the_reference_time() -> None:
    assert parabolic_film_thickness(
        reference_thickness=12.0, elapsed_time=1.0
    ) == pytest.approx(12.0)


def test_growth_is_parabolic_not_linear() -> None:
    """Four times the time gives twice the film, which is the whole point."""
    one = parabolic_film_thickness(reference_thickness=12.0, elapsed_time=1.0)
    four = parabolic_film_thickness(reference_thickness=12.0, elapsed_time=4.0)
    assert four == pytest.approx(2.0 * one)
    assert four < 4.0 * one


def test_no_time_means_no_film() -> None:
    assert parabolic_film_thickness(
        reference_thickness=12.0, elapsed_time=0.0
    ) == 0.0


def test_zero_acceleration_stops_growth() -> None:
    assert parabolic_film_thickness(
        reference_thickness=12.0, elapsed_time=10.0, acceleration_factor=0.0
    ) == 0.0


def test_acceleration_factor_scales_time_not_thickness() -> None:
    """A factor of four accelerates like four times the time: twice the film."""
    plain = parabolic_film_thickness(reference_thickness=12.0, elapsed_time=1.0)
    fast = parabolic_film_thickness(
        reference_thickness=12.0, elapsed_time=1.0, acceleration_factor=4.0
    )
    assert fast == pytest.approx(2.0 * plain)


def test_reference_time_rescales_the_curve() -> None:
    thickness = parabolic_film_thickness(
        reference_thickness=10.0, elapsed_time=8.0, reference_time=2.0
    )
    assert thickness == pytest.approx(20.0)


def test_composes_with_the_arrhenius_factor() -> None:
    """The intended use: temperature accelerates a diffusion-limited film."""
    hot = parabolic_film_thickness(
        reference_thickness=12.0,
        elapsed_time=1.0,
        acceleration_factor=arrhenius_factor(
            temperature_c=45.0, activation_energy_j_per_mol=50_000.0
        ),
    )
    assert hot == pytest.approx(22.62, abs=0.01)


def test_thickness_accepts_arrays() -> None:
    thicknesses = parabolic_film_thickness(
        reference_thickness=12.0, elapsed_time=np.array([0.0, 1.0, 4.0])
    )
    assert isinstance(thicknesses, np.ndarray)
    np.testing.assert_allclose(thicknesses, np.array([0.0, 12.0, 24.0]))


def test_thickness_scalar_returns_a_real_float() -> None:
    result = parabolic_film_thickness(reference_thickness=12.0, elapsed_time=2.0)
    assert isinstance(result, float)
    assert not isinstance(result, np.ndarray)


@pytest.mark.parametrize(
    ("kwargs", "parameter"),
    [
        ({"reference_thickness": -1.0, "elapsed_time": 1.0}, "reference_thickness"),
        ({"reference_thickness": 12.0, "elapsed_time": -1.0}, "elapsed_time"),
        (
            {"reference_thickness": 12.0, "elapsed_time": 1.0, "reference_time": 0.0},
            "reference_time",
        ),
        (
            {
                "reference_thickness": 12.0,
                "elapsed_time": 1.0,
                "acceleration_factor": -1.0,
            },
            "acceleration_factor",
        ),
    ],
)
def test_out_of_domain_thickness_inputs_are_rejected(
    kwargs: dict, parameter: str
) -> None:
    with pytest.raises(ValueError, match=parameter):
        parabolic_film_thickness(**kwargs)


def test_thickness_positional_call_raises_type_error() -> None:
    with pytest.raises(TypeError):
        parabolic_film_thickness(12.0, 1.0)  # type: ignore[misc]
