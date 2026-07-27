"""Evaluate Fick's first law for several prescribed gradients."""

import numpy as np

from battery_core.diffusion import ficks_first_law_flux


def main() -> None:
    """Print molar fluxes for a constant diffusion coefficient."""
    diffusivity_m2_per_s = 1.0e-14
    gradients_mol_per_m4 = np.array([-2.0e6, 0.0, 2.0e6])
    flux_mol_per_m2_s = ficks_first_law_flux(
        diffusivity_m2_per_s, gradients_mol_per_m4
    )

    print("dc/dx [mol/m^4]:", gradients_mol_per_m4)
    print("J [mol/(m^2 s)]:", flux_mol_per_m2_s)


if __name__ == "__main__":
    main()
