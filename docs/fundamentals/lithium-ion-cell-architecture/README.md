# Lithium-ion Cell Architecture tutorial

This browser module is Part 01B of the Battery Core fundamentals sequence. It is
an independently authored, interactive tutorial for moving from the full cell
stack down to porous-electrode ingredients, electrolyte solvent molecules, ions,
and separator function.

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

- clickable current collectors, electrodes, and separator;
- charge/discharge direction switching;
- a porous composite-electrode ingredient explorer;
- original schematic structures for EC, PC, DMC, EMC, and DEC;
- a conceptual LiPF6 dissolution interaction;
- a separator passage test for Li+, electrons, and electrode particles;
- a short knowledge check.

## Scientific limitations

This is a conceptual visualization, not a quantitative electrochemical model.
Geometry, colors, pore sizes, molecular positions, and motion are illustrative.
Animation speed must not be interpreted as current, C-rate, diffusivity,
conductivity, reaction rate, or elapsed time. The electrolyte section does not
calculate solvation, ion pairing, transport properties, stability, or
electrochemical reactions.

## Authorship and references

The explanations, code, interactions, and diagrams were created specifically for
Battery Core. No book figure, microscopy image, or molecular artwork is reused.

General architecture and terminology were informed by established lithium-ion
battery literature, including:

- G. L. Plett, *Battery Management Systems, Volume I: Battery Modeling*,
  Artech House, 2015.
- T. B. Reddy, ed., *Linden's Handbook of Batteries*, 4th ed.,
  McGraw-Hill, 2011.
