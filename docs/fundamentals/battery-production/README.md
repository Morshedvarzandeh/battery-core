# Battery Production — CellForge simulator

CellForge is an interactive browser lesson that follows a reference lithium-ion
cell-production route from incoming electrode materials to a formed, aged, tested,
and packed cell.

Public URL after merge:

`https://morshedvarzandeh.github.io/battery-core/fundamentals/battery-production/`

## Learning scope

The simulator supports pouch, cylindrical, and prismatic routes and covers:

- slurry mixing, coating, drying, calendering, and slitting;
- the solvent-free dry-electrode route: dry mixing, fibrillation, and dry coating;
- vacuum drying, sheet separation, stacking, or winding;
- tab joining, enclosure, electrolyte filling, and wetting;
- formation, pouch-cell degassing, aging, grading, and end-of-line testing;
- cell-component responsibility, material flow, process references, and a guided tour;
- plant-level views: a factory layout, machine detail, and a route comparison.

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

## Repository packaging

The reviewed standalone HTML is kept verbatim across ordered files under
`payload/`. `loader.js` fetches those readable source parts, concatenates them in
order, and opens the complete simulator. This packaging keeps each repository file
small enough for review while preserving the validated standalone page.

- `index.html` — lightweight loading page;
- `loader.js` — ordered source-part loader;
- `payload/source-01.part` through `payload/source-25.part` — the complete
  standalone HTML, split only at line boundaries.

## Local preview

From the repository root:

```bash
python -m http.server 8000 -d docs
```

Then open:

`http://localhost:8000/fundamentals/battery-production/`

The module must be served over HTTP because the loader retrieves the ordered source
parts with `fetch()`.

## Validation

Static tests reconstruct the standalone source and check chapter scope, route
coverage, scientific qualifications, accessibility references, JavaScript asset
ordering, and the distinction between illustrative scores and measured factory
outcomes.
