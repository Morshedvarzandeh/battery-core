# Solid-State Production — SolidForge simulator

SolidForge is an interactive browser lesson aligned with the February 2026 third
edition of the PEM RWTH Aachen/VDMA all-solid-state cell production guide.
It compares reference oxide, halide, sulfide, and polymer electrolyte routes
from material preparation through cell finishing.

Public URL after merge:

`https://morshedvarzandeh.github.io/battery-core/fundamentals/solid-state-production/`

## Learning scope

The simulator covers:

- lithium-metal foil extrusion and lamination;
- electrolyte-class-dependent mixing, compounding, coating, calendering,
  deposition, compacting, and sintering;
- separation, stacking, contacting, packaging, formation, and aging;
- component responsibility, route comparisons, process references, and a
  guided factory tour.

## Model scope and limitations

Published sources support the process sequence and displayed operating ranges.
The line-condition, interface, quality, throughput, margin, and energy outputs
are illustrative teaching relationships. They are not calibrated plant
predictions, equipment-sizing calculations, release criteria, or proof that
a particular solid electrolyte or lithium-metal design is safe.

Solid-state routes do not eliminate dendrite, internal-short, moisture,
toxicity, solvent, or fire risks. The relevant controls depend on the specific
materials and process. Site procedures, equipment manuals, validated recipes,
safety systems, and applicable regulations always take precedence.

## Repository packaging

The reviewed standalone HTML is kept verbatim across ordered files under
`payload/`. `loader.js` fetches those readable source parts, concatenates them
in order, and opens the complete simulator.

- `index.html` — lightweight loading page;
- `loader.js` — ordered source-part loader;
- `payload/source-01.part` through `payload/source-23.part` — the complete
  standalone HTML, split only at line boundaries.

## Local preview

From the repository root:

```bash
python -m http.server 8000 -d docs
```

Then open:

`http://localhost:8000/fundamentals/solid-state-production/`

The module must be served over HTTP because the loader retrieves the ordered
source parts with `fetch()`.

## Validation

Static tests reconstruct the standalone source and check route coverage,
scientific qualifications, accessibility references, JavaScript syntax, source
part ordering, and the distinction between illustrative scores and measured
factory outcomes.
