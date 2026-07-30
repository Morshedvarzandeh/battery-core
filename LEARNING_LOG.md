# Learning log

This log records modeling decisions and lessons so that the reasoning behind
the code remains visible as the project grows.

## 2026-07-29 — Chapter 1 integration review

- Process-guide ranges and scientific literature can support an educational
  process sequence without turning illustrative scores into factory predictions.
- Solid-state production is not one route: electrolyte class changes the
  material preparation, densification, atmosphere, interface, and finishing
  requirements.
- Replacing liquid electrolyte and a separate porous separator removes filling
  and wetting from the reference route, but it does not remove dendrite,
  internal-short, moisture, toxicity, solvent, or fire risk.
- Aging mechanisms can be organized around capacity, impedance, and
  self-discharge for teaching, but those three outputs are not an exhaustive
  diagnostic model.
- Apparent short-term capacity recovery does not reverse degradation, and deep
  discharge should not be presented as a general cell-rejuvenation method.
- A chapter-level study guide should connect modules through shared focus points
  and checkpoints while leaving each interactive module responsible for its own
  specialized teaching interface.

## 2026-07-27 — Fick's first law

- A constitutive law can be implemented without choosing a mesh, time
  integrator, or boundary-condition scheme. Keeping that boundary explicit
  makes the physics reusable by future solvers.
- The minus sign in Fick's first law carries physical meaning: passive
  diffusion is down the concentration gradient. Tests should therefore check
  direction, not only magnitude.
- SI units cannot be inferred from plain numeric inputs, so the public API and
  documentation must state the required units clearly.
- Rejecting non-finite quantities at the physics boundary prevents `NaN` and
  infinity from silently contaminating later numerical calculations.

## 2026-07-27 — Capacity and C-rate

- C-rate is a normalization of current by nominal capacity; it is not a
  chemistry-specific performance model.
- The ideal duration `1 / C-rate` is an exact definitional calculation, but it
  must not be presented as a guarantee of real voltage-cutoff time.
- Current magnitude, current direction, energy, and voltage are separate
  concepts and should not be combined prematurely in one API.
- A 20 Ah example is useful for arithmetic, but the nameplate value must not be
  treated as rate-independent usable capacity.

## 2026-07-30 — Validating inputs at the physics boundary

- An argument order that is safe to transpose is a silent-error hazard, not a
  style question. Nominal capacity sits first in `current_from_c_rate` and
  second in `c_rate_from_current`, so a swapped positional call returned a
  plausible number instead of failing. Making both functions keyword-only is
  worth a breaking change, because the wrong answer was indistinguishable from
  the right one.
- Coercing input with `np.asarray(value, dtype=np.float64)` quietly parses the
  string `"20"` into `20.0`. A physics boundary should reject what is not a
  number rather than guess at it.
- Two failure classes deserve two exception types: `TypeError` when the input
  is not numeric, `ValueError` when it is numeric but outside its physical
  domain. Keeping them distinct lets a caller tell a programming mistake from a
  domain violation.
- Zero is not automatically an invalid input. A rest step is a real operating
  condition, so a zero current and a zero C-rate must be accepted. The
  exception is `1 / C-rate`, where zero is undefined rather than unphysical.
  Validation limits belong to each quantity's physics, not to a shared habit of
  rejecting non-positive numbers.
- A scalar-only guard such as `if not np.isfinite(x)` fails twice on arrays: it
  raises an ambiguity error for many elements and silently skips the check for
  one element. Validation written for scalars does not generalize by accident.
- Sharing the validators in one module keeps the convention consistent, but the
  helpers still need their own direct tests. Reaching them only through calling
  code leaves branches such as complex-dtype rejection unexercised.

Future entries may discuss voltage, energy, equivalent-circuit behavior, and
numerical diffusion solvers. SPM, SPMe, and DFN models remain deferred.
