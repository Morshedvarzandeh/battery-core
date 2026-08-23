# Changelog

All notable changes to `battery-core` are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[semantic versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- The project is relicensed from MIT to the **GNU Affero General Public License
  v3.0 or later**, with one additional term permitted by section 7(b) of that
  licence: the attribution to Lemonergy must stay visible. `NOTICE` states the
  term and how to comply, and every page footer now carries the attribution as
  its Appropriate Legal Notice.

- Chapter 1 reads as one designed chapter rather than six separately authored
  pages. Each module had been written standalone against a generic blue-on-white
  token set, so every lesson rendered white while the course shell around it was
  navy. All of them now use the course palette.

  Colour also means something now. Mint is the core path, blue is optional
  depth, and orange is the toolkit — a rule stated in a legend on the homepage
  and the study guide instead of being left to inference. `--orange` had been
  declared in `site.css` since the homepage landed and never used; it is the
  toolkit hue.

- The CellForge layout editor is part of the site. It was added standalone in
  0.3.0 with its own light/dark palette, no header or footer, no link from
  anywhere, and three `unpkg.com` script tags that nothing on the page used —
  the only external requests in `docs/`. It is rebuilt on the course design
  system, reachable from the homepage and the study guide, and self-contained
  like everything else.

### Added

- A standard page template, `docs/assets/page-template.html`, and the design
  system it belongs to, documented in `docs/assets/README.md`. A new page copies
  the template and inherits the palette, header, footer, skip link, responsive
  rules, and licence attribution instead of deciding each one again.

- `docs/assets/module-theme.css` restates the generic token contract in course
  colours, so a module written against it adopts the palette without any change
  to its own layout. `docs/assets/site-chrome.css` carries the shared header and
  footer separately, because a module with its own token vocabulary — the
  workbench reads `--muted` as a text colour, not a surface — needs the chrome
  without the bridge.

- A study coach on the Chapter 1 guide, with seventeen questions. The chapter
  already asked a checkpoint question after every part, but reading one and
  thinking "yes, roughly" is not answering it.

  Eight of the questions are **marked outright**: numeric drills, multiple
  choice, select-all, and putting the production route into order. Every wrong
  option says which misconception it is and why it fails, which is the part
  that does the teaching. Every drill number comes from a relationship the
  tested Python implements — `current_from_c_rate`, `ideal_duration_hours`,
  `arrhenius_factor`, `parabolic_film_thickness` — and a test compares the two
  physical constants the browser cannot import against `battery_core.aging`, so
  the copy cannot drift.

  The other nine ask for an explanation, and those are **not** marked. Grading
  prose offline means keyword matching, and keyword matching grades vocabulary
  rather than understanding: "the separator does not block electrons" contains
  every right word and is wrong, while a correct answer in different words
  scores nothing. A confidently wrong grade is worse than no grade, because the
  learner cannot tell it happened. So the coach shows what a complete answer
  covers and the learner ticks their own, and the interface says which kind of
  question they are on before they answer.

- The coach has a face: a lemon in a headset, for Lemonergy. It is drawn as
  inline SVG rather than embedded, so it stays sharp at any size, costs no
  request on a page meant to be self-contained, and can change expression —
  idle, thinking, happy, encouraging — which a bitmap cannot. Expressions swap
  whole paths by `display` rather than animating the CSS `d` property, which
  Firefox does not support.

  Its yellow, `--lemon`, is the one hue outside the colour-role system, and
  narrowly so: the mascot is illustration, not a UI state, so it never marks a
  tier, a status, or a control.

  It runs entirely in the browser: no network, no account, no key. Progress
  lives in `localStorage`, and a browser with site data blocked studies without
  saved progress rather than getting a broken page. A `<noscript>` block points
  at the questions, which are all written out in the sequence above it.

  An AI tutor can be attached for free-form follow-up by pointing
  `data-tutor-endpoint` at a proxy that holds an API key server-side. It is off
  by default, so the page ships making no network request at all, and
  `docs/assets/README.md` carries a complete reference worker plus what it
  costs and where it will be wrong.

- A third diagram in the CellForge editor: a standard template. It is not a
  machine but the skeleton the coating and calendering diagrams share — the same
  frame, the same four zone divisions, one web line with flow arrows,
  placeholder machines to rename, and input/in-process/output state badges. A
  new process step starts on the course grid and at the course label scale
  rather than from a blank canvas, which is what produced the label overlaps the
  editor exists to fix.

## [0.3.0] — 2026-07-30

### Added

- `battery_core.aging`, with the two rate laws that account for most of how a
  cell wears out: `arrhenius_factor` for the temperature dependence of a
  thermally activated process, and `parabolic_film_thickness` for
  diffusion-limited film growth, where quadrupling the time doubles the film.

  Both are keyword-only. Each takes two arguments of the same kind and unit —
  two temperatures, two times — so a transposed positional call would return a
  plausible wrong number rather than fail.

  Neither function supplies chemistry-specific constants. An activation energy
  and a reference thickness are inputs, exactly as the diffusion coefficient is
  an input to Fick's first law. Fitted coefficients belong to a validated model
  of a specific cell.

- Chapter 1 course material: Part 03B, an all-solid-state production simulator,
  and Part 04, an interactive battery-aging notebook. Part 03's lithium-ion
  simulator is updated to the February 2026 PEM RWTH Aachen and VDMA edition,
  which adds the solvent-free dry-electrode route and plant-level views.

### Fixed

- `ruff` and `mypy` now run in CI. They were configured in 0.2.0 but nothing
  invoked them.
- mypy no longer pins an analysis target older than the interpreter it runs
  under, which made it reject NumPy's type stubs and abort before checking any
  of this project's code.
- The version test no longer imports `tomllib` unguarded, which broke the
  Python 3.10 leg of the test matrix.

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
