# Changelog

All notable changes to `battery-core` are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[semantic versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-07-30

This release changes the capacity API in a way that breaks existing calls. See
the migration note below.

### Changed — breaking

- `current_from_c_rate` and `c_rate_from_current` now accept **keyword
  arguments only**. Nominal capacity is the first parameter of one function and
  the second of the other, so a transposed positional call returned a plausible
  but wrong number with no error. `c_rate_from_current(20.0, 40.0)` returned
  `0.5` where `2.0` was meant. Requiring argument names removes that failure
  mode.

  `ideal_duration_hours(c_rate)` is unchanged and still takes its single
  argument positionally.

  ```python
  # Before (0.1.0)
  current_from_c_rate(20.0, 10.0)
  c_rate_from_current(40.0, 20.0)

  # After (0.2.0)
  current_from_c_rate(nominal_capacity_ah=20.0, c_rate=10.0)
  c_rate_from_current(current_a=40.0, nominal_capacity_ah=20.0)
  ```

- Zero is now accepted wherever it is physical, so a rest step can be
  represented. `current_from_c_rate` accepts `c_rate = 0`, and
  `c_rate_from_current` accepts `current_a = 0`. Nominal capacity must still be
  strictly positive, and `ideal_duration_hours` still rejects a zero C-rate
  because `1 / 0` is undefined.

- Non-numeric input now raises `TypeError` instead of being coerced. The string
  `"20"` was previously parsed as `20.0`; it is now rejected. The project
  convention is `TypeError` for input that is not numeric and `ValueError` for
  numeric input outside its physical domain.

- `ficks_first_law_flux` accepts an array diffusivity for a spatially varying
  medium, broadcast against the concentration gradient. Previously a
  multi-element array raised "truth value of an array is ambiguous", and a
  one-element array bypassed the sign check entirely, so `np.array([-1.0])` was
  accepted as a valid diffusivity.

### Added

- `battery_core.validation`, a shared module of domain-validation helpers used
  by the capacity and diffusion modules: `as_finite_array`,
  `positive_finite_array`, `non_negative_finite_array`, and `scalar_or_array`.
  Error messages name the offending parameter.
- `lint` optional-dependency group, plus `ruff` and `mypy` configuration.

### Fixed

- `__version__` is read through `importlib.metadata` so it can no longer drift
  from the version declared in `pyproject.toml`.

## [0.1.0] — 2026-07-27

### Added

- `battery_core.capacity`: `current_from_c_rate`, `c_rate_from_current`, and
  `ideal_duration_hours`.
- `battery_core.diffusion`: `ficks_first_law_flux`.
