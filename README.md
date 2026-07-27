# battery-core

`battery-core` is an early-stage, open-source Python library for building clear,
well-tested battery physics models. The project currently implements only
Fick's first law; single-particle (SPM), SPMe, and Doyle–Fuller–Newman (DFN)
models are intentionally out of scope for this first release.

## Principles

- Use SI units internally and document every quantity.
- Keep physical equations separate from numerical discretizations and solvers.
- Prefer small typed functions over unnecessary classes.
- State assumptions and limitations alongside each model.
- Test physical sign conventions, input validation, and edge cases.

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
