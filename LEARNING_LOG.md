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

Future entries may discuss numerical diffusion solvers, but SPM, SPMe, and DFN
models are deliberately deferred.
