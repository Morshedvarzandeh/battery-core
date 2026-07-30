# All-solid-state production — SolidForge simulator

SolidForge is an interactive browser lesson that follows a reference
all-solid-state cell-production route from lithium metal and solid-electrolyte
powder to a formed, contacted cell. It is the counterpart to the lithium-ion
simulator in [`../battery-production/`](../battery-production/), and it is best
read after it.

Public URL after merge:

`https://morshedvarzandeh.github.io/battery-core/fundamentals/solid-state-production/`

## Learning scope

The simulator covers four solid-electrolyte classes — oxide, sulfide, halide,
and polymer — and the way each one changes the line:

- ball milling, mixing, compounding, and extrusion of the electrolyte;
- tape casting, aerosol deposition, co-extrusion, calendering, and dry coating;
- atomic layer deposition, isostatic compacting, sintering, and slitting;
- sheet separation, stacking under compression, contacting, and packaging;
- formation, plus the stack-pressure, interface, and dendrite-margin behavior
  that distinguishes a solid-state cell from a liquid-electrolyte one.

Each electrolyte class carries its own atmosphere, temperature, and pressure
requirements, and switching class rebuilds the station sequence accordingly.

## Model scope and limitations

The process sequence, parameter ranges, atmospheres, quality features, and
technology alternatives come from the published PEM RWTH Aachen and VDMA
process guide. Everything the simulator computes from them — resistance,
contact, dendrite margin, and energy — is an illustrative teaching relationship
rather than a calibrated plant prediction.

This limitation is stronger here than for the lithium-ion module, and it is
worth stating plainly: **no all-solid-state line is in series production**, so
no generally applicable process chain exists to calibrate against. The
line-condition, availability, and interface figures are illustrative
constructions layered on a teaching model. They are not equipment-sizing
calculations, product-release criteria, or a connection to a live asset.

The machine schematics are educational redraws informed by the cited
references. Site procedures, equipment manuals, validated recipes, safety
systems, and applicable regulations always take precedence.

## Repository packaging

The reviewed standalone HTML is kept verbatim across ordered files under
`payload/`. `loader.js` fetches those readable source parts, concatenates them
in order, and opens the complete simulator. This packaging keeps each
repository file small enough for review while preserving the validated
standalone page.

- `index.html` — lightweight loading page;
- `loader.js` — ordered source-part loader;
- `payload/source-01.part` through `payload/source-23.part` — the complete
  standalone HTML, split only at line boundaries.

Two accessibility corrections were applied to the reviewed source before
packaging: the page had no `h1`, and its guided tour was a dialog that did not
declare itself modal or point at its own heading and body text. Both now match
the lithium-ion module, and tests pin them.

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

Static tests reconstruct the standalone source and check electrolyte-class
coverage, process-stage coverage, the accessible heading and modal-tour
structure, JavaScript asset ordering, and the explicit statement that the
outputs are illustrative rather than measured.
