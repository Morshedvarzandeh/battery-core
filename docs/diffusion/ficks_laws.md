# Fick's laws: current scope

## Fick's first law

For one-dimensional diffusion, `battery-core` implements the constitutive
relation

\[
J = -D\frac{\mathrm{d}c}{\mathrm{d}x},
\]

where:

| Symbol | Meaning | SI unit |
| --- | --- | --- |
| \(J\) | molar flux through unit area | mol m⁻² s⁻¹ |
| \(D\) | diffusion coefficient | m² s⁻¹ |
| \(c\) | concentration | mol m⁻³ |
| \(x\) | spatial coordinate | m |
| \(\mathrm{d}c/\mathrm{d}x\) | concentration gradient | mol m⁻⁴ |

Flux measures the amount of species crossing a unit area per unit time. The
minus sign means passive diffusion proceeds down the concentration gradient.
With positive \(x\) chosen as the reference direction, a positive gradient
therefore gives a negative flux, while a negative gradient gives a positive
flux. This is a molar flux, not a mass flux in kg m⁻² s⁻¹; multiplying by the
species' molar mass converts it to mass flux without changing its direction.

## Assumptions

The implemented equation assumes:

- a scalar, concentration-independent diffusion coefficient at each call;
- an isotropic medium, represented here in one spatial dimension;
- a continuum description with a locally defined concentration gradient;
- diffusion driven only by the concentration gradient; and
- SI-unit inputs, because numeric values do not carry runtime unit metadata.

The function accepts multiple precomputed gradient values for convenient
vectorized evaluation. It does not compute those gradients and makes no choice
of mesh or numerical solver.

## Limitations

Fick's first law alone is not a time-evolution model and does not define initial
or boundary conditions. It omits concentration- or temperature-dependent
diffusivity, anisotropic diffusion tensors, migration in an electric field,
convection, activity corrections for non-ideal mixtures, mechanics, reactions,
and interfacial transport. Its use in porous electrodes may require an
effective transport coefficient and additional homogenization assumptions.

Fick's second law, which combines conservation with a constitutive relation to
describe transient concentration, is not implemented yet. Neither are SPM,
SPMe, or DFN battery models.

## References and further reading

These sources provide historical and modern context; this page summarizes the
equation independently rather than reproducing textbook prose.

1. A. Fick, “On liquid diffusion,” *The London, Edinburgh, and Dublin
   Philosophical Magazine and Journal of Science*, 10(63), 30–39 (1855),
   doi: [10.1080/14786445508641925](https://doi.org/10.1080/14786445508641925).
2. J. Newman and K. E. Thomas-Alyea, *Electrochemical Systems*, 3rd ed.,
   Wiley-Interscience (2004).
