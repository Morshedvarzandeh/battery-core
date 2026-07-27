# Learning log

This log records modeling decisions and lessons so that the reasoning behind
the code remains visible as the project grows.

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
