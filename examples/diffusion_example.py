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
