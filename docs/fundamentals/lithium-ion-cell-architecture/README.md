# Lithium-ion Cell Architecture tutorial

This browser module is Part 01B of the Battery Core fundamentals sequence. It is
an independently authored, layer-first tutorial that keeps the five-layer cell
stack visible while learners zoom into porous electrodes, separator pores,
carbonate solvents, dissolved ions, and the connected ionic and electronic
transport paths.

## Launch

After the module is merged and GitHub Pages deploys:

`https://morshedvarzandeh.github.io/battery-core/fundamentals/lithium-ion-cell-architecture/`

To run locally from the repository root:

```bash
python -m http.server 8000 -d docs
```

Then open:

`http://localhost:8000/fundamentals/lithium-ion-cell-architecture/`

## Learning scope

The tutorial includes:

- assembly of five physical layers from the negative side to the positive side;
- a persistent mini-stack showing the architectural origin of every zoom;
- an explicit explanation that electrolyte fills pores in layers 2, 3, and 4 and is not a sixth layer;
- selectable current collectors, composite electrodes, and separator;
- a fixed component readout and legend for active material, conductive additive, binder, pore electrolyte, Li+, polymer, and metal foil;
- original schematic connectivity diagrams for EC, PC, DMC, EMC, and DEC;
- a locked molecule view that opens only after entering a porous layer;
- a three-stage conceptual LiPF6 interaction: associated pair, greater separation, and solvent reorientation;
- a return path that automatically selects a porous layer when the learner becomes stuck;
- a final reconnection of ionic and electronic transport paths to the original five-layer stack.

## Scientific limitations

This is a conceptual visualization, not a quantitative electrochemical model.
Geometry, colors, pore sizes, molecular positions, and transitions are
illustrative. Transition speed must not be interpreted as current, C-rate,
diffusivity, conductivity, reaction rate, state of charge, or elapsed time.
The electrolyte section does not calculate coordination numbers, solvation
energies, ion-pairing equilibria, transport properties, stability, or
electrochemical reaction rates.

Some polyolefin separators can close pores at elevated temperature, but this
shutdown behavior is not universal and does not prevent every failure mode.
The SEI explanation is intentionally qualitative and notes that its composition
depends on solvents, salt, additives, electrode surface, and operating
conditions.

## Authorship and references

The explanations, code, interactions, and diagrams were created specifically for
Battery Core. No book figure, microscopy image, or molecular artwork is reused.

General architecture and terminology were informed by established lithium-ion
battery literature, including:

- G. L. Plett, *Battery Management Systems, Volume I: Battery Modeling*,
  Artech House, 2015.
- T. B. Reddy, ed., *Linden's Handbook of Batteries*, 4th ed.,
  McGraw-Hill, 2011.
