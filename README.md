# battery-core

[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/01_ficks_first_law.ipynb)

`battery-core` is an early-stage, open-source project for building clear,
well-tested battery physics models and independently authored learning tools.
The quantitative Python API currently implements only Fick's first law;
single-particle (SPM), SPMe, and Doyle–Fuller–Newman (DFN) models are
intentionally out of scope for this first release.

## Learning resources

The project keeps conceptual learning tools separate from quantitative models:

- **[Cell Anatomy Workbench](docs/fundamentals/cell-anatomy-workbench/)** — a
  conceptual browser visualization of a layered-oxide/graphite lithium-ion cell,
  its components, and charge/discharge directions. It is not a quantitative
  simulation and does not calculate voltage, current, state of charge, or time.
- **Fick's first-law notebook** — an executable quantitative lesson that calls
  the tested `battery_core` Python implementation. Use the **Launch Binder**
  badge above to run it online.

To open the Cell Anatomy Workbench locally, run this command from the repository
root and visit
`http://localhost:8000/fundamentals/cell-anatomy-workbench/`:

```bash
python -m http.server 8000 -d docs
```

## Principles

- Use SI units internally and document every quantity.
- Keep physical equations separate from numerical discretizations and solvers.
- Prefer small typed functions over unnecessary classes.
- State assumptions and limitations alongside each model.
- Test physical sign conventions, input validation, and edge cases.
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

## Run online

Use the **Launch Binder** badge above to open the interactive Fick's first-law
notebook in your browser. The first build can take a few minutes while Binder
creates the environment.

## Quick start

```python
from battery_core.diffusion import ficks_first_law_flux

# D in m^2/s; dc_dx in mol/m^4; result in mol/(m^2 s)
flux = ficks_first_law_flux(1.0e-14, 2.0e6)
print(flux)  # -2e-08
```

See [`docs/diffusion/ficks_laws.md`](docs/diffusion/ficks_laws.md) for the
equation, assumptions, and sign convention, and
[`examples/diffusion_example.py`](examples/diffusion_example.py) for a runnable
example.

## Contributing

Contributions are welcome. Please keep physics independent of solver choices,
add tests for new behavior, document units and assumptions, and run `pytest`
before opening a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
