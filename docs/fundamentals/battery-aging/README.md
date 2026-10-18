# Part 04 — Battery aging (lesson page)

The readable, on-site version of Part 04:
`https://learn.lemonergy.com/fundamentals/battery-aging/`

## What it teaches

Six degradation mechanisms (corrosion, SEI passivation, gas generation, crystal
formation, dendrites and lithium plating, volume change and cracking), where in
the cell each happens, the Arrhenius rate law under them, and how they show up
as impedance rise, capacity fade and self-discharge.

## What it simplifies

Every equation is a teaching model — a √t film, Arrhenius factors, one-line
stress terms — that gets the direction, shape and rough relative size right.
It is not a state-of-health estimator. The page states this at the top, and
every section names the papers it draws on.

## The interactive panels

`panels/` holds the notebook's own panels, exported by
`scripts/export_aging_panels.py`. Do not edit them by hand: change the panel in
`notebooks/fundamentals/04_battery_aging.ipynb`, then run

```bash
python scripts/export_aging_panels.py
```

`tests/test_lessons.py` fails if the exported panels and the notebook disagree.
Each panel page carries `noindex`, because it is a fragment of this lesson.
