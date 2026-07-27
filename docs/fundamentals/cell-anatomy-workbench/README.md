# Cell Anatomy Workbench

This browser-based workbench is an independently authored, conceptual
visualization of a rechargeable lithium-ion intercalation cell.

It helps learners inspect:

- the negative and positive electrodes;
- the electrolyte and separator;
- the copper and aluminum current collectors;
- electron motion in the external circuit; and
- lithium-ion motion inside the cell during charge and discharge.

The workbench is **not a quantitative simulation**. It does not solve voltage,
current, concentration, state of charge, thermal, kinetic, degradation, or
porous-electrode equations. Animation speed has no physical scale.

## Run locally

From the repository root:

```bash
python -m http.server 8000 -d docs
```

Then open:

```text
http://localhost:8000/fundamentals/cell-anatomy-workbench/
```

No JavaScript libraries or external network resources are required.

## Terminology

The workbench keeps the labels **negative electrode** and **positive
electrode** fixed. It also explains the reaction-based definitions of
**anode** and **cathode**, which switch between discharge and charge. Battery
literature often uses anode and cathode as persistent material names according
to the discharge convention; the interface states this convention explicitly.

## Scientific scope

The cell is an illustrative layered-oxide/graphite lithium-ion cell with a
typical nominal-voltage range shown for context. The voltage is not calculated
by `battery-core` and must not be interpreted as model output.
