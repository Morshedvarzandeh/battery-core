# Battery Production — CellForge simulator

CellForge is an interactive browser lesson that follows a reference lithium-ion
cell-production route from incoming electrode materials to a formed, aged, tested,
and packed cell.

Public URL after merge:

`https://morshedvarzandeh.github.io/battery-core/fundamentals/battery-production/`

## Learning scope

The simulator supports pouch, cylindrical, and prismatic routes and covers:

- slurry mixing, coating, drying, calendering, and slitting;
- vacuum drying, sheet separation, stacking, or winding;
- tab joining, enclosure, electrolyte filling, and wetting;
- formation, pouch-cell degassing, aging, grading, and end-of-line testing;
- cell-component responsibility, material flow, process references, and a guided tour.

The quantitative reference recipe is graphite/NMC. Other chemistries and process
routes require different material properties, operating windows, and validation.

## Model scope and limitations

Published sources support the process sequence and displayed operating ranges.
Capacity, throughput, wetting, process-health, interphase, and risk-control outputs
are illustrative teaching relationships. They are not calibrated plant predictions,
equipment-sizing calculations, product-release criteria, or a connection to a live
factory asset.

The machine schematics are educational redraws informed by the cited production
references. Site procedures, equipment manuals, validated recipes, safety systems,
and applicable regulations always take precedence.

## Files

- `index.html` — document structure and accessible controls;
- `styles.css` — self-contained visual system and machine styling;
- `scripts/01-machine-schematics.js` — interactive process-equipment drawings;
- `scripts/02-stations-and-model.js` — station data, controls, and teaching model;
- `scripts/03-components-and-references.js` — components, material states, and sources;
- `scripts/04-operator-consoles.js` — station-specific operating panels;
- `scripts/05-response-charts.js` — setpoint-response visualizations;
- `scripts/06-rendering-and-tour.js` — navigation, rendering, and guided-tour behavior;
- `scripts/07-big-picture-views.js` — overview, flow, matrix, reference views, and startup.

## Local preview

From the repository root:

```bash
python -m http.server 8000 -d docs
```

Then open:

`http://localhost:8000/fundamentals/battery-production/`

## Validation

Static tests check local assets, chapter scope, route coverage, scientific
qualifications, accessibility references, and the distinction between illustrative
scores and measured factory outcomes.
