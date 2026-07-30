# Battery Core

**Open-source, executable battery engineering fundamentals.**

[Open the course homepage](https://morshedvarzandeh.github.io/battery-core/)
·
[Launch the Cell Anatomy Workbench](https://morshedvarzandeh.github.io/battery-core/fundamentals/cell-anatomy-workbench/)
·
[Launch the Lithium-ion Cell Architecture tutorial](https://morshedvarzandeh.github.io/battery-core/fundamentals/lithium-ion-cell-architecture/)
·
[Open the Battery Production simulator](https://morshedvarzandeh.github.io/battery-core/fundamentals/battery-production/)
·
[Open the Battery Materials Lab](https://morshedvarzandeh.github.io/battery-core/labs/battery-materials-lab/)
·
[Run the C-rate notebook in Binder](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/02_capacity_and_c_rate.ipynb)
·
[Run the Fick's-law notebook](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/transport/ficks_first_law.ipynb)

`battery-core` develops battery concepts through interactive visualizations,
well-tested Python models, and independently authored executable notebooks.
Electrical, electrochemical, thermal, aging, and pack models are added gradually
with explicit assumptions and validation.

## Learning sequence

### Chapter 1 — Battery Cell Foundations

1. **[Part 01 — Cell anatomy and charge/discharge paths](https://morshedvarzandeh.github.io/battery-core/fundamentals/cell-anatomy-workbench/)** — inspect the named components and conceptual current paths.
2. **[Part 01B — Lithium-ion cell architecture](https://morshedvarzandeh.github.io/battery-core/fundamentals/lithium-ion-cell-architecture/)** — move from the five-layer stack to porous electrodes, pore electrolyte, molecules, ions, and transport paths.
3. **[Part 02 — Nominal capacity and C-rate](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/02_capacity_and_c_rate.ipynb)** — connect capacity, current, C-rate, and ideal duration through tested calculations.
4. **[Part 03 — Battery production](https://morshedvarzandeh.github.io/battery-core/fundamentals/battery-production/)** — follow a reference graphite/NMC route from slurry preparation to formation, aging, grading, and packing, with the solvent-free dry-electrode route alongside it.
5. **[Part 04 — Battery aging](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/04_battery_aging.ipynb)** — work through the six degradation mechanisms that wear a cell out, and why temperature drives all of them.

Part 03 connects cell components and ratings to the process steps that create,
assemble, activate, and screen a finished cell. Part 04 closes Chapter 1 by
following that finished cell through the rest of its life.

### Chapter 2 — Equivalent Circuit Models

Chapter 2 is planned. It will progress from terminal-voltage conventions and OCV
to resistance, one-RC and multiple-RC models, discrete-time implementation,
parameter identification, and validation against measured data.

See [`LEARNING_PATH.md`](LEARNING_PATH.md) for the complete roadmap and the
distinction among core chapters, supplementary labs, and existing physics building
blocks.

## Chapter 1 modules

### Part 01 — Cell Anatomy Workbench

The **[live Cell Anatomy Workbench](https://morshedvarzandeh.github.io/battery-core/fundamentals/cell-anatomy-workbench/)** explains cell components and charge/discharge directions. It is a conceptual visualization, not a quantitative simulation. Its source is in [`docs/fundamentals/cell-anatomy-workbench/`](docs/fundamentals/cell-anatomy-workbench/).

### Part 01B — Lithium-ion Cell Architecture

The **[interactive architecture tutorial](https://morshedvarzandeh.github.io/battery-core/fundamentals/lithium-ion-cell-architecture/)** assembles the five physical layers, keeps the parent stack visible during each zoom, and shows that electrolyte fills connected pores rather than forming a sixth structural layer. Its source is in [`docs/fundamentals/lithium-ion-cell-architecture/`](docs/fundamentals/lithium-ion-cell-architecture/).

### Part 02 — Capacity and C-rate

The **[capacity and C-rate notebook](notebooks/fundamentals/02_capacity_and_c_rate.ipynb)** uses tested package functions to calculate current, C-rate, and ideal constant-current duration while separating exact definitions from real voltage-cutoff behavior.

### Part 03 — Battery Production

The **[CellForge production simulator](https://morshedvarzandeh.github.io/battery-core/fundamentals/battery-production/)** follows pouch, cylindrical, and prismatic reference routes. Its graphite/NMC calculations are explicitly illustrative teaching relationships, not calibrated plant predictions or release criteria. Its source and limitations are documented in [`docs/fundamentals/battery-production/`](docs/fundamentals/battery-production/).

To open the browser modules locally, run:

```bash
python -m http.server 8000 -d docs
```

### Supplementary interactive lab — Battery materials

The **[Battery Materials Lab](https://morshedvarzandeh.github.io/battery-core/labs/battery-materials-lab/)** starts with a Zn/Cu aqueous cell and develops electrode-potential differences, reference electrodes, the water stability window, lithium-ion intercalation, and representative material trade-offs. It remains an advanced supplementary lab rather than a replacement for the chapter sequence.

### Additional transport module

The **[Fick's first-law notebook](notebooks/transport/ficks_first_law.ipynb)** remains available as a tested transport-physics building block.

## Principles

- Use explicit units; prefer SI while documenting established battery conventions such as ampere-hours and C-rate when useful.
- Keep physical equations separate from numerical discretizations and solvers.
- Prefer small typed functions over unnecessary classes.
- State assumptions and limitations alongside each model.
- Test sign conventions, input validation, expected values, and edge cases.
- Separate exact definitions from empirical or model-dependent predictions.
- Label conceptual and illustrative visualizations clearly and keep them distinct from validated model output.

## Installation

Python 3.10 or newer is required.

```bash
python -m pip install .
```

For development:

```bash
python -m pip install -e '.[test]'
pytest
```

To run the linter and type checker as well:

```bash
python -m pip install -e '.[test,lint]'
ruff check .
mypy
```

## Quick start

### Capacity and C-rate

```python
from battery_core import current_from_c_rate, ideal_duration_hours

current_a = current_from_c_rate(nominal_capacity_ah=20.0, c_rate=10.0)
duration_minutes = ideal_duration_hours(10.0) * 60.0

print(current_a)          # 200.0
print(duration_minutes)   # 6.0
```

### Fick's first law

```python
from battery_core import ficks_first_law_flux

flux = ficks_first_law_flux(1.0e-14, 2.0e6)
print(flux)  # -2e-08 mol/(m^2 s)
```

The diffusion coefficient may also be an array, which describes a spatially
varying medium and broadcasts against the gradient:

```python
import numpy as np

flux = ficks_first_law_flux(np.array([1.0e-14, 2.0e-14]), 2.0e6)
print(flux)  # [-2.e-08 -4.e-08]
```

See [`docs/diffusion/ficks_laws.md`](docs/diffusion/ficks_laws.md) for assumptions and the sign convention.

## Contributing

Contributions are welcome. Keep physics independent of solver choices, add tests
for new behavior, document units and assumptions, and run `pytest` before opening
a pull request.

See [`CHANGELOG.md`](CHANGELOG.md) for released changes, including the
keyword-only capacity API introduced in 0.2.0.

## License

This project is licensed under the [MIT License](LICENSE).
