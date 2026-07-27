# Capacity and C-rate

This page defines the ideal relationships among nominal capacity, current,
C-rate, and duration. It is independently written and is not a reproduction of
any textbook section.

## Nominal capacity

Nominal capacity \(Q_\mathrm{nominal}\) is commonly reported in ampere-hours
(Ah). It describes electric charge under stated test conditions; it is not an
energy rating and does not by itself specify cell voltage.

Because

\[
1\ \mathrm{Ah} = 1\ \mathrm{A}\times 1\ \mathrm{h},
\]

a 20 Ah rating means that 20 amperes sustained for one hour would transfer
20 Ah of charge in the ideal arithmetic sense.

## C-rate

C-rate normalizes current by nominal capacity:

\[
C_\mathrm{rate} = \frac{I}{Q_\mathrm{nominal}},
\]

so the corresponding current is

\[
I = C_\mathrm{rate}Q_\mathrm{nominal}.
\]

When capacity is entered in Ah, the numerical C-rate has units of reciprocal
hours. Common labels include:

| Label | Numerical C-rate |
| --- | ---: |
| C/10 | 0.1 h⁻¹ |
| 1C | 1 h⁻¹ |
| 2C | 2 h⁻¹ |
| 10C | 10 h⁻¹ |

For a 20 Ah cell, these rates correspond ideally to 2 A, 20 A, 40 A, and 200 A.

## Ideal constant-current duration

If the full nominal capacity were available at every rate, the duration would
be

\[
t_\mathrm{ideal}
= \frac{Q_\mathrm{nominal}}{I}
= \frac{1}{C_\mathrm{rate}}.
\]

Therefore, C/10 corresponds to 10 hours, 1C to 1 hour, 2C to 30 minutes, and
10C to 6 minutes.

## Ideal arithmetic versus real-cell operation

The equations above define C-rate and ideal duration. They do **not** guarantee
that a real cell will remain above its permitted voltage limit for exactly that
long. Usable duration can differ because of:

- ohmic and polarization voltage losses;
- transport limitations and nonuniform active-material utilization;
- temperature;
- cell chemistry and construction;
- state of health and prior use; and
- the test method, current profile, and voltage limits.

At high current, terminal voltage may reach the lower cutoff before the nominal
charge has been delivered. At low current, measured capacity may exceed or fall
below the nameplate value depending on the rating conditions and the cell.

`battery-core` currently implements only the ideal conversions. Predicting
voltage-cutoff time requires a cell model and validated parameters.

## Python API

```python
from battery_core import current_from_c_rate, ideal_duration_hours

current_a = current_from_c_rate(20.0, 10.0)
duration_min = ideal_duration_hours(10.0) * 60.0

print(current_a)     # 200.0
print(duration_min)  # 6.0
```

## Assumptions and limitations

- Current is treated as a positive magnitude; charge/discharge sign conventions
  belong to a later current-sign module.
- Capacity, current, and C-rate must be finite and positive.
- No voltage, energy, heat, aging, kinetics, or rate-dependent capacity is
  calculated.
- The functions accept NumPy-compatible arrays for comparisons and plots.

## References and further reading

These sources provide broader battery-modeling context. The explanation,
examples, code, tests, and notebook in `battery-core` are independently
authored.

1. T. B. Reddy, ed., *Linden's Handbook of Batteries*, 4th ed., McGraw-Hill,
   2011.
2. G. L. Plett, *Battery Management Systems, Volume I: Battery Modeling*,
   Artech House, 2015.
