# Part 02 — Nominal capacity and C-rate (lesson page)

The readable, on-site version of Part 02:
`https://learn.lemonergy.com/fundamentals/capacity-and-c-rate/`

## What it teaches

Nominal capacity as charge under stated conditions, C-rate as a normalised
current, the ideal duration `t = 1 / C`, the equal-area picture behind it, and
why a real cell can reach its cutoff voltage before the ideal duration.

## What it simplifies

Only the ideal conversions are calculated. No voltage, energy, heat, aging,
kinetics or rate-dependent capacity is modelled; the page says so and does
not draw a synthetic rate-capacity curve.

## How it works

- Equations are MathML, rendered by the browser with no external library.
- The two calculators (`../../assets/lesson-tools.js`) mirror
  `current_from_c_rate`, `c_rate_from_current` and `ideal_duration_hours`,
  including their input rules. The HTML already contains the worked-example
  results, so the page reads correctly without JavaScript.
- The practice quiz is the Chapter 1 study coach scoped to `data-part="Part 02"`.
- `tests/test_lessons.py` compares every printed number with the Python.

The notebook `notebooks/fundamentals/02_capacity_and_c_rate.ipynb` remains the
place to change the code and plot it yourself.
