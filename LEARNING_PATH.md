# Battery Core learning path

`battery-core` is organized as an independent sequence of battery concepts.
Books, papers, standards, and public datasets may inform the work, but the
project's explanations, examples, code, tests, notebooks, and visualizations are
written specifically for this repository.

[Open the public course homepage](https://morshedvarzandeh.github.io/battery-core/)

## Chapter 1 — Battery Cell Foundations

| Part | Concept | Status | Main format |
| ---: | --- | --- | --- |
| 01 | [Cell anatomy and charge/discharge paths](https://morshedvarzandeh.github.io/battery-core/fundamentals/cell-anatomy-workbench/) | Available — launch online | Browser workbench |
| 01B | [Lithium-ion cell architecture](https://morshedvarzandeh.github.io/battery-core/fundamentals/lithium-ion-cell-architecture/) | Available — launch online | Interactive browser tutorial |
| 02 | [Nominal capacity and C-rate](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/02_capacity_and_c_rate.ipynb) | Available — launch notebook | Python API and Jupyter notebook |
| 03 | [Battery production — materials to finished cell](https://morshedvarzandeh.github.io/battery-core/fundamentals/battery-production/) | Available — launch online | Interactive production simulator |
| 04 | [Battery aging — how a cell wears out](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/04_battery_aging.ipynb) | Available — launch notebook | Interactive Jupyter notebook |

Part 01 introduces the cell components and charge/discharge paths. Part 01B moves
through the structural scales inside a lithium-ion cell. Part 02 introduces the
first quantitative battery-rating relationships. Part 03 follows a reference
graphite/NMC production route through electrode manufacturing, assembly,
formation, aging, grading, and final testing. It follows the February 2026
edition of the PEM RWTH Aachen and VDMA process guide, and it models the
solvent-free dry-electrode route alongside the conventional wet route, together
with plant-level factory, machine, and technology-comparison views.

The production simulator uses published process sequences and operating ranges,
but its capacity, throughput, wetting, process-health, interphase, and risk-control
outputs are illustrative teaching relationships rather than calibrated factory
predictions.

Part 04 turns from making a cell to losing it. It covers six degradation
mechanisms — SEI growth, gas generation, crystal formation, dendrites, volume
change, and contact loss — and shows how an Arrhenius factor and a √t film law
account for most of what a cell does as it ages. Its equations are teaching
models that reproduce the direction and rough relative size of each effect; they
are not a state-of-health estimator. Part 04 closes Chapter 1.

## Chapter 2 — Equivalent Circuit Models

| Part | Concept | Status | Main format |
| ---: | --- | --- | --- |
| 2.1 | Terminal voltage, current, power, and sign convention | Planned | Documentation and notebook |
| 2.2 | Open-circuit voltage and state of charge | Planned | Python model and notebook |
| 2.3 | Series-resistance or R0 model | Planned | Tested Python model and notebook |
| 2.4 | One-RC Thevenin model | Planned | Tested Python model and notebook |
| 2.5 | Multiple-RC and discrete-time ECMs | Planned | Python package and notebooks |
| 2.6 | Parameter identification and model validation | Planned | Data workflow and notebook |

Chapter 2 will start from measured terminal behavior and build only the model
complexity needed for the available data and validation objective.

Each part must state its assumptions, units, sign conventions, limitations, and
validation method. A new part is marked available only when its implementation and
learning material are ready.

## Supplementary interactive labs

- **[Electrode potentials and battery materials](https://morshedvarzandeh.github.io/battery-core/labs/battery-materials-lab/)** — a self-contained browser lab covering a Zn/Cu aqueous example, voltage references, the water stability window, lithium-ion intercalation, and representative electrode-material trade-offs.

## Existing physics building blocks

The repository also contains tested physics modules that can support later chapters:

- Fick's first law for local diffusive flux;
- its documentation, example, and transport notebook.
