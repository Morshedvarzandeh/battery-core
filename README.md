# Battery Core

**Open-source, executable battery engineering fundamentals.**

[Open the course homepage](https://morshedvarzandeh.github.io/battery-core/)
·
[Launch the Cell Anatomy Workbench](https://morshedvarzandeh.github.io/battery-core/fundamentals/cell-anatomy-workbench/)
·
[Launch the Lithium-ion Cell Architecture tutorial](https://morshedvarzandeh.github.io/battery-core/fundamentals/lithium-ion-cell-architecture/)
·
[Run Part 02 in Binder](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/02_capacity_and_c_rate.ipynb)
·
[Run the Fick's-law notebook](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/transport/ficks_first_law.ipynb)

`battery-core` develops battery concepts through interactive visualizations,
well-tested Python models, and independently authored executable notebooks.
More complete electrical, electrochemical, thermal, aging, and pack models will
be added gradually with explicit assumptions and validation.

## Learning sequence

The fundamentals are developed as connected parts, even when different formats
are best for different concepts:

1. **[Part 01 — Cell anatomy and charge/discharge paths](https://morshedvarzandeh.github.io/battery-core/fundamentals/cell-anatomy-workbench/)** — an interactive conceptual browser workbench.
2. **[Part 01B — Lithium-ion cell architecture](https://morshedvarzandeh.github.io/battery-core/fundamentals/lithium-ion-cell-architecture/)** — an interactive tutorial from cell layers to porous electrodes, electrolyte molecules, and separator function.
3. **[Part 02 — Nominal capacity and C-rate](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/02_capacity_and_c_rate.ipynb)** — a tested Python API and executable Jupyter notebook.
4. **Part 03 — Voltage, energy, and power** — planned.

See [`LEARNING_PATH.md`](LEARNING_PATH.md) for the growing sequence and the
distinction between fundamentals and existing physics building blocks.

### Part 01 — Cell Anatomy Workbench

The
**[live Cell Anatomy Workbench](https://morshedvarzandeh.github.io/battery-core/fundamentals/cell-anatomy-workbench/)**
explains cell components and charge/discharge directions. It is a conceptual
visualization, not a quantitative simulation. Its source files are in
[`docs/fundamentals/cell-anatomy-workbench/`](docs/fundamentals/cell-anatomy-workbench/).

### Part 01B — Lithium-ion Cell Architecture

The
**[interactive architecture tutorial](https://morshedvarzandeh.github.io/battery-core/fundamentals/lithium-ion-cell-architecture/)**
connects the full cell stack to porous composite electrodes, conductive
additives, binder, electrolyte-filled pores, carbonate solvent molecules,
dissolved ions, and separator behavior. The diagrams are original and
conceptual; no reference-book artwork or microscopy image is reused. Its source
files are in
[`docs/fundamentals/lithium-ion-cell-architecture/`](docs/fundamentals/lithium-ion-cell-architecture/).

To open either browser module locally, run this command from the repository root
and visit the corresponding path under `http://localhost:8000/`:

```bash
python -m http.server 8000 -d docs
```

### Part 02 — Capacity and C-rate

The
**[capacity and C-rate notebook](notebooks/fundamentals/02_capacity_and_c_rate.ipynb)**
uses the tested package functions to calculate current, C-rate, and ideal
constant-current duration. It clearly separates the exact ideal relationships
from real-cell voltage-cutoff behavior.

### Additional transport module

The
**[Fick's first-law notebook](notebooks/transport/ficks_first_law.ipynb)**
remains available as a tested transport-physics module. It is not presented as
the next fundamentals lesson.

## Principles

- Use explicit units; prefer SI, while documenting established battery
  conventions such as ampere-hours and C-rate when they improve clarity.
- Keep physical equations separate from numerical discretizations and solvers.
- Prefer small typed functions over unnecessary classes.
- State assumptions and limitations alongside each model.
- Test physical sign conventions, input validation, and edge cases.
- Separate exact definitions from empirical or model-dependent predictions.
- Label conceptual visualizations clearly and keep them separate from model output.

## Installation

Python 3.10 or newer is required.

```bash
python -m pip install .
```

For development, clone the repository and install the test dependencies:

```bash
python -m pip install -e '.[test]'
pytest
```

## Quick start

### Capacity and C-rate

```python
from battery_core import current_from_c_rate, ideal_duration_hours

current_a = current_from_c_rate(20.0, 10.0)
duration_minutes = ideal_duration_hours(10.0) * 60.0

print(current_a)          # 200.0
print(duration_minutes)   # 6.0
```

### Fick's first law

```python
from battery_core import ficks_first_law_flux

# D in m^2/s; dc_dx in mol/m^4; result in mol/(m^2 s)
flux = ficks_first_law_flux(1.0e-14, 2.0e6)
print(flux)  # -2e-08
```

See [`docs/diffusion/ficks_laws.md`](docs/diffusion/ficks_laws.md) for the
diffusion equation, assumptions, and sign convention.

## Contributing

Contributions are welcome. Please keep physics independent of solver choices,
add tests for new behavior, document units and assumptions, and run `pytest`
before opening a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
