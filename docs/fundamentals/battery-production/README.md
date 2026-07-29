# Battery Production — CellForge simulator

CellForge is an interactive browser lesson that follows a reference lithium-ion
cell-production route from incoming electrode materials to a formed, aged, tested,
and packed cell.

Public URL after merge:

`https://morshedvarzandeh.github.io/battery-core/fundamentals/battery-production/`

## Learning scope

The simulator supports pouch, cylindrical, and prismatic formats and two electrode
manufacturing routes:

- a wet route with wet mixing and dispersing, slurry coating, drying, and calendering;
- a dry route with dry mixing/fibrillation and dry coating before the shared downstream chain;
- slitting, vacuum drying, sheet separation, stacking, or winding;
- tab joining, enclosure, electrolyte filling, wetting, and pre-treatment;
- formation, pouch-cell degassing, aging, grading, and end-of-line testing;
- component responsibility, material flow, a machine overview, factory/environment
  views, technology radar, guided tour, and cited references.

The process data and displayed production ranges follow the February 2026 fifth
edition of the PEM RWTH Aachen and VDMA guide, supplemented by the peer-reviewed
sources cited in the page.

The quantitative reference recipe is graphite/NMC. Other chemistries and process
routes require different material properties, operating windows, and validation.

## Model scope and limitations

Published sources support the process sequence and displayed operating ranges.
Capacity, throughput, wetting, process-health, interphase, OEE, and risk-control
outputs are illustrative teaching relationships. They are not calibrated plant
predictions, equipment-sizing calculations, product-release criteria, or a
connection to a live factory asset.

The capacity calculation uses the 95 wt% active-material fractions in the selected
2026 reference formulations. It remains a simplified active-material estimate.
Pre-treatment temperature and the illustrative formation-temperature assumption
are separate controls.

Dry-route investment is deliberately not summed into a complete factory total.
The source does not separately quote dry mixing/fibrillation or separate slitting
from the combined calendering-and-slitting range. Reported dry-coating savings are
process-comparison potentials, not guaranteed complete-factory savings.

The machine schematics are educational redraws informed by the cited production
references. Site procedures, equipment manuals, validated recipes, safety systems,
and applicable regulations always take precedence.

## Repository packaging

The original reviewed source remains split across the existing ordered files under
`payload/`. `review-2026.delta` contains a compact, gzip-compressed line delta for
this scientific and accessibility revision. `loader.js` reconstructs the original
source, applies the delta in memory, and opens the validated page. Static tests
verify that the reconstructed result matches the expected 2026 revision.

## Local preview

From the repository root:

```bash
python -m http.server 8000 -d docs
```

Then open:

`http://localhost:8000/fundamentals/battery-production/`

The module must be served over HTTP because the loader retrieves the ordered source
parts and revision delta with `fetch()`.

## Validation

Static tests reconstruct the standalone source and check:

- wet and dry route ownership, including the separate dry-mixing station;
- the 95 wt% active-material fractions and separated temperature controls;
- dry-route cost limitations and scientific qualifications;
- chapter scope, cell-format coverage, and illustrative-model labels;
- accessible headings, tour-dialog relationships, focus management, and mobile navigation;
- delta reconstruction, JavaScript asset ordering, and the absence of external code dependencies.
