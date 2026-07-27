# Battery Core learning path

`battery-core` is organized as an independent sequence of battery concepts.
Books, papers, standards, and public datasets may inform the work, but the
project's explanations, examples, code, tests, notebooks, and visualizations
are written specifically for this repository.

## Fundamentals sequence

| Part | Concept | Status | Main format |
| ---: | --- | --- | --- |
| 01 | [Cell anatomy and charge/discharge paths](https://morshedvarzandeh.github.io/battery-core/fundamentals/cell-anatomy-workbench/) | Available — launch online | Browser workbench |
| 02 | [Nominal capacity and C-rate](https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/02_capacity_and_c_rate.ipynb) | Available after PR #5 is merged | Python API and Jupyter notebook |
| 03 | Voltage, energy, and power | Planned | Python API and Jupyter notebook |
| 04 | Open-circuit voltage and state of charge | Planned | Documentation and notebook |
| 05 | Simple internal-resistance model | Planned | Python model and notebook |
| 06 | Dynamic equivalent-circuit models | Planned | Python model and notebook |

The Part 01 link opens the published GitHub Pages workbench. The Part 02 link
opens the executable notebook in Binder after its files are merged into
`main`.

Each part should state its assumptions, units, limitations, and validation
method. A new part is added only when its implementation and learning material
are ready.

## Existing physics building blocks

The repository also contains tested physics modules that will be connected to
the main sequence when the required intermediate concepts are complete:

- Fick's first law for local diffusive flux;
- its documentation, example, and transport notebook.

This prevents an already useful implementation from being presented as the
next fundamentals lesson before the necessary concepts have been introduced.
