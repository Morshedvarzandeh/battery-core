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

Future entries may discuss voltage, energy, equivalent-circuit behavior, and
numerical diffusion solvers. SPM, SPMe, and DFN models remain deferred.
