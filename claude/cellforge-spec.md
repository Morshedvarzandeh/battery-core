# CellForge — source-derived specification

Scope of this document: `docs/fundamentals/battery-production/index.html`, `loader.js`,
and `payload/source-01.part` … `source-26.part`. Every statement below is quoted from,
or computed from, that code. Anything not present in the code is marked **NOT IN SOURCE**.

Line references (`L####`) are lines of the reconstructed page, i.e. `cat source-*.part`
in ascending order (5 214 lines). Part-file map:

| part | lines | part | lines | part | lines |
|---|---|---|---|---|---|
| source-01 | 1–218 | source-10 | 1843–1953 | source-19 | 3481–3753 |
| source-02 | 219–456 | source-11 | 1954–2129 | source-20 | 3754–3920 |
| source-03 | 457–656 | source-12 | 2130–2269 | source-21 | 3921–4156 |
| source-04 | 657–914 | source-13 | 2270–2430 | source-22 | 4157–4375 |
| source-05 | 915–1220 | source-14 | 2431–2618 | source-23 | 4376–4580 |
| source-06 | 1221–1523 | source-15 | 2619–2824 | source-24 | 4581–4828 |
| source-07 | 1524–1629 | source-16 | 2825–2996 | source-25 | 4829–5099 |
| source-08 | 1630–1739 | source-17 | 2997–3188 | source-26 | 5100–5214 |
| source-09 | 1740–1842 | source-18 | 3189–3480 | | |

`index.html` (22 lines) renders only `<h1>CellForge — Lithium-ion Cell Production Simulator</h1>`
and `<p id="load-status">Loading the interactive production simulator…</p>`; `loader.js`
fetches the 26 parts, joins them and calls `document.open(); document.write(html); document.close();`.
Failure text: `"The simulator source could not be loaded. Serve the docs directory over HTTP and reload this page."`

---

## 1 · TABS / VIEWS

The app shell (`<div class="app">`, L782) has three DOM sections that are switched by
`go()` / `showView()` (L3384–3409, L5119–5127): `#overview`, `#stationView`, `#layerView`.

### 1.1 Top-level views

| # | On-screen label | Where the label comes from | What it shows |
|---|---|---|---|
| 0 | **Factory overview** | `$("crumbTitle").textContent = "Factory overview"` (L3396) | Default state (`go(null)`, L5210). Cards: "Walk the line from powder to packed cell"; "Reference recipe"; "Model scope"; "What the 5th edition changed" (5 buttons); "The line" (station map by phase); "Illustrative reference-line estimates" (6 KPIs); "How to read this simulator"; "Three major defect drivers". Rendered by `renderOverview()` L3067–3172. |
| 1 | **Machine overview** — hint `the whole line, live` | `VIEWS[0]`, L3855 | `renderMachineOverview()` L4923. "The whole line on one screen": OEE donut block, CURRENT block, three sparklines, `lineSVG()` (every active station as one drawing with a status lamp), `alarmList()`, key, `floorSVG()` (4 halls in isometric plan), and the "What is real here and what is not" card. |
| 2 | **Cell anatomy** — `every layer, and who builds it` | `VIEWS[1]`, L3856 | `renderAnatomy()` L3959. Eyebrow "The big picture · 1 of 3". Nine components as a list + exploded SVG (`anatomySVG`), then Dimension / Material / Origin, role, why, "STATIONS THAT BUILD OR SHAPE IT — <ROUTE> ROUTE", "WHERE IT IS MOST EASILY RUINED". |
| 3 | **Material flow** — `powder to graded cell` | `VIEWS[2]`, L3857 | `renderFlow()` L4031. "The big picture · 2 of 3", heading `One material, ${chain.length} states`; one row per FLOW state with the station that makes it and a live model value. |
| 4 | **Process ↔ component** — `which station touches what` | `VIEWS[3]`, L3858 | `renderMatrix()` L4103. "The big picture · 3 of 3". Station × 9-component table with marks `●` make, `◉` both, `▲` risk, `◆` check; legend; two commentary cards. |
| 5 | **Technology radar** — `what is coming, and how soon` | `VIEWS[4]`, L3859 | `renderRadar()` L4322. 44-entry radar (`TECH`, L4190–4235) in 5 sectors × 3 readiness rings, list by sector, detail pane. |
| 6 | **Factory & environment** — `the building, the air, the bill` | `VIEWS[5]`, L3860 | `renderFactory()` L4465. Four-zone factory concept, "Production environment along the chain" table, `capexSVG()` investment chart, totals row. |
| 7 | **References** — `every number, sourced` | `VIEWS[6]`, L3861 | `renderRefs()` L5003. The 16 `REFS` entries with "Used for:" and URL. |
| 8 | **Station view** | `$("crumbTitle").textContent = st.title` (L3402) | One per active station (`renderStation()` L3175): machine schematic + hotspot readout, purpose, Arrives as / Leaves as, environment + investment, responsibility chips, Process parameters & requirements, Technology alternatives, Innovations & trends, Quality influences, Quality features, Operate this station console, Standard operating sequence. |

The seven `VIEWS` entries are rendered as buttons under the sidebar heading `THE BIG PICTURE`
(L812, `renderLayerNav()` L3865). Station buttons sit under `<nav id="nav" aria-label="Production stations">`,
grouped by `PHASES` = `Electrode manufacturing`, `Cell assembly`, `Cell finishing` (L1527–1531).

### 1.2 Other top-level switches (not views)

| Control | Labels | Effect |
|---|---|---|
| `#routeOpts` — `CELL FORMAT — CHANGES THE LINE` | `Pouch` / `Cylindrical` / `Prismatic` | sets `route`; rebuilds station list; L3433–3443 |
| `#procOpts` — `ELECTRODE ROUTE — CHANGES THE LINE` | `Wet` / `Dry` | sets `proc`; re-renders the rail sliders; L3446–3457 |
| `#runBtn` | `Ⅱ Pause line` ⇄ `▶ Run line`; tag `● RUNNING` ⇄ `❚❚ HELD` | toggles CSS animation class `is-run`; L3460–3466 |
| `#tourStart` | `▶ Start the guided factory tour` | opens the 20-stop modal dialog `#tour` (`TOUR`, L3752–3793) |
| `#navBtn` / `#labBtn` | `☰ Stations` / `⚙ Process lab` | open the sidebar / rail as drawers below 1280 px; L5149–5176 |
| `#resetBtn` | `RESET` | `S = { ...DEFAULTS }` (L3468) |
| per-station | `Reset this station` / `Break it` | reset or force this station's controls (`BREAK` map L5107–5111) |

The right-hand rail (`#processDrawer`, always visible ≥1280 px) is titled
`ILLUSTRATIVE PROCESS MODEL` / `Line condition`, with sections `SETPOINT LAB` and
`REFERENCE CELL OUTPUTS`.

---

## 2 · PROCESS STAGES

`STATIONS` array, L1539–1875, in code order. `ALL = "pouch cyl prism"`.
`active() = STATIONS.filter(s => s.routes.includes(route) && (!s.proc || s.proc === proc))` (L1534).
The number shown on screen is the position in `active()`, not `no`.

| # in code | `id` | `no` | Display name (`title`) | Phase | `routes` | `proc` |
|---|---|---|---|---|---|---|
| 1 | `mixing` | 01 | **Wet mixing and dispersing** | Electrode manufacturing | all | wet |
| 2 | `drymix` | 01D | **Dry mixing and fibrillation** | Electrode manufacturing | all | dry |
| 3 | `coating` | 02 | **Coating** | Electrode manufacturing | all | wet |
| 4 | `drying` | 03 | **Drying** | Electrode manufacturing | all | wet |
| 5 | `drycoat` | 03 | **Dry coating** | Electrode manufacturing | all | dry |
| 6 | `calendering` | 04 | **Calendering** | Electrode manufacturing | all | wet |
| 7 | `slitting` | 05 | **Slitting** | Electrode manufacturing | all | — (both) |
| 8 | `vacdry` | 06 | **Vacuum drying** | Electrode manufacturing | all | — (both) |
| 9 | `separation` | 07 | **Separation** | Cell assembly | pouch | — |
| 10 | `stacking` | 08 | **Stacking** | Cell assembly | pouch | — |
| 11 | `winding` | 08 | **Winding** | Cell assembly | cyl prism | — |
| 12 | `packPouch` | 09 | **Packaging — pouch** | Cell assembly | pouch | — |
| 13 | `packHard` | 09 | **Packaging — can** | Cell assembly | cyl prism | — |
| 14 | `fillPouch` | 10 | **Electrolyte filling — pouch** | Cell assembly | pouch | — |
| 15 | `fillHard` | 10 | **Electrolyte filling — can** | Cell assembly | cyl prism | — |
| 16 | `rollpress` | 11 | **Pre-treatment** | Cell finishing | pouch | — |
| 17 | `formation` | 12 | **Formation** | Cell finishing | all | — |
| 18 | `degassing` | 13 | **Degassing** | Cell finishing | pouch | — |
| 19 | `aging` | 14 | **Aging** | Cell finishing | all | — |
| 20 | `eol` | 15 | **End-of-line testing** | Cell finishing | all | — |

Route- and process-specificity:

* **Pouch only** — `separation`, `stacking`, `packPouch`, `fillPouch`, `rollpress`, `degassing`.
* **Cylindrical + prismatic only** — `winding`, `packHard`, `fillHard`.
* **Wet only** — `mixing`, `coating`, `drying`, `calendering`.
* **Dry only** — `drymix`, `drycoat`.
* **Every route and both electrode routes** — `slitting`, `vacdry`, `formation`, `aging`, `eol`.

Abbreviated labels used only in the machine-overview drawing (`SHORT`, L4613–4618):
`Packaging — pouch`→`Packaging`, `Packaging — can`→`Packaging`, `Electrolyte filling — pouch`→`Filling`,
`Electrolyte filling — can`→`Filling`, `End-of-line testing`→`EoL test`, `Vacuum drying`→`Vacuum dry`,
`Pre-treatment`→`Pre-treat`, `Winding`→`Winding + tabs`.

Each station also carries: `machine` (schematic key into `M`), `env{iso,dew,temp}`, `cost`,
`takt`, `purpose`, `inp`, `out`, `parts[]` (hotspots), `params[]`, `alts[]`, `innov[]`,
`qInf[]`, `qFeat[]`, `sop[]`. Machine investment strings, verbatim:

| id | `cost` | `takt` |
|---|---|---|
| mixing | € 30–55 M (mixing) | 20 min – 6 h per batch |
| drymix | Not separately quoted in the source | batch or continuous, equipment-dependent |
| coating | € 35–65 M (coating and drying) | 35–80 m/min |
| drying | € 35–65 M — quoted together with coating | dryer up to 100 m long |
| drycoat | € 45–60 M (coating and drying) | double-sided, single pass |
| calendering | € 10–15 M (calendering and slitting) | 60–100 m/min |
| slitting | € 10–15 M — quoted together with calendering | 80–150 m/min |
| vacdry | € 5–15 M (vacuum drying) | 8–48 h per batch |
| separation | € 20–30 M (separation) | ≈0.2 s per sheet |
| stacking | € 25–60 M (stacking) | ≈1 s per sheet |
| winding | € 20–30 M (winding) | up to 30 cells/min (cyl) |
| packPouch | € 20–35 M (packaging, pouch cells) | — |
| packHard | € 35–45 M cylindrical · € 45–60 M prismatic | — |
| fillPouch | € 35–45 M (electrolyte filling) | — |
| fillHard | € 35–45 M (electrolyte filling) | — |
| rollpress | € 5–15 M (high-temperature soaking) | soaking time, process-dependent |
| formation | € 65–95 M (formation) — the most capital-intensive station on the line | up to 15 h |
| degassing | € 10–15 M (degassing) | — |
| aging | € 15–45 M (aging) | up to 3 weeks |
| eol | € 5–15 M (EoL test) | — |

---

## 3 · ROUTES

Two orthogonal selectors: **cell format** (`route`, default `"pouch"`, L1943) and
**electrode route** (`proc`, default `"wet"`, L1533).

`GEOM` (L1936–1940) — the only geometry difference the model uses:

| route | `name` | `area` | `layers` | `unit` string |
|---|---|---|---|---|
| `pouch` | Pouch | 200 | 18 | `cm² per sheet · 18 double-sided layers` |
| `cyl` | Cylindrical | 1300 | 1 | `cm² of wound cathode (21700 class)` |
| `prism` | Prismatic | 12000 | 1 | `cm² of wound cathode` |

(`factor:1` is present on all three and is never read anywhere else in the source.)

### 3.1 Resulting station lists

| route + proc | stations, in order | count |
|---|---|---|
| pouch + wet (defaults) | mixing, coating, drying, calendering, slitting, vacdry, separation, stacking, packPouch, fillPouch, rollpress, formation, degassing, aging, eol | 15 |
| pouch + dry | drymix, drycoat, slitting, vacdry, separation, stacking, packPouch, fillPouch, rollpress, formation, degassing, aging, eol | 13 |
| cyl + wet / prism + wet | mixing, coating, drying, calendering, slitting, vacdry, winding, packHard, fillHard, formation, aging, eol | 12 |
| cyl + dry / prism + dry | drymix, drycoat, slitting, vacdry, winding, packHard, fillHard, formation, aging, eol | 10 |

Cylindrical and prismatic differ only in: `GEOM.area` (1300 vs 12000), the winding takt text
(`"up to 30 cells/min"` vs `"up to 6 cells/min"`, L2525), the packaging investment string
(`€ 35–45 M` vs `€ 45–60 M`, L2562), the housing readout (`"Deep-drawn can, 21700 class"` vs
`"Prismatic can and lid"`, L2558), the `CAPEX` row selected (L4427–4428), and the anatomy drawing
(L3928–3949). **The station list for cyl and prism is identical.**

### 3.2 What the electrode-route switch changes

* Rail sliders: `HEAD_WET = ["tC","tA","speed","dryT","force","vac","cRate","ageDays"]`,
  `HEAD_DRY = ["tC","tA","dcFib","dcRollT","dcLine","vac","cRate","ageDays"]` (L1930–1932).
* Porosity source term (see §5.1): calender force + roll temperature (wet) vs dry-coating line
  pressure + roll temperature (dry).
* `coatErr` becomes `dcErr`; `solventGap` and `crackGap` are forced to 0 on the dry route.
* Material-flow chain: `proc === "dry" ? [FLOW[0], ...FLOW_DRY, ...FLOW.slice(5)] : FLOW` (L4047–4049).
* `CAPEX` rows (L4415–4435) and the factory totals (`"Not available from source"` for dry).
* Claimed savings block `SAVING` (L3254–3259), shown only on the `drycoat` station page:
  `−35% CapEx`, `−45% Energy consumption`, `−55% Space`, `−70% Emissions`.

---

## 4 · INPUTS

All 40 user-adjustable parameters live in `CTL` (L1884–1927). `DEFAULTS` is built from `def`.
`good` is the "recommended window" drawn by `windowBar()` (L3025); it is not a clamp.
"Rail" = appears in the right-hand SETPOINT LAB for that electrode route.
"Stations" = station consoles that expose the control (`OPS[*].ctl`, L2320–2702).

| key | Label | Unit | min | max | default | step | recommended window (`good`) | rail | station consoles |
|---|---|---|---|---|---|---|---|---|---|
| `tC` | Cathode coat, per side | µm | 40 | 80 | 65 | 1 | 40–80 | wet + dry | coating, drycoat, stacking |
| `tA` | Anode coat, per side | µm | 50 | 100 | 80 | 1 | 50–100 | wet + dry | coating, drycoat, stacking |
| `speed` | Coating line speed | m/min | 35 | 80 | 60 | 1 | 35–80 | wet | coating, drying, calendering, drycoat |
| `dryT` | Dryer peak temperature | °C | 50 | 160 | 130 | 1 | 50–160 | wet | drying |
| `force` | Calender line force | N/mm | 400 | 2500 | 1700 | 25 | 400–2300 | wet | calendering |
| `vac` | Vacuum drying time | h | 8 | 48 | 22 | 1 | 16–48 | wet + dry | vacdry |
| `cRate` | Formation first charge | C | 0.1 | 0.5 | 0.25 | 0.05 | 0.1–0.35 | wet + dry | formation, degassing |
| `ageDays` | Aging period | d | 3 | 21 | 14 | 1 | 10–21 | wet + dry | aging, eol |
| `solid` | Slurry solid content | wt% | 40 | 75 | 58 | 1 | 50–68 | — | mixing, drying |
| `mixMin` | Dispersing time | min | 20 | 360 | 120 | 10 | 60–360 | — | mixing |
| `mixT` | Mixer jacket temperature | °C | 20 | 40 | 25 | 1 | 20–40 | — | mixing |
| `gap` | Slot-die gap | µm | 60 | 300 | 155 | 1 | 120–200 | — | coating |
| `dryLen` | Dryer length | m | 20 | 100 | 60 | 5 | 20–100 | — | drying |
| `dcLine` | Dry-coating line pressure | N/mm | 150 | 300 | 250 | 5 | 150–300 | dry | drycoat |
| `dcRollT` | Dry-coating roll temperature | °C | 50 | 200 | 120 | 5 | 50–200 | dry | drycoat |
| `dcFib` | Dry-mixing shear setting | % | 20 | 100 | 70 | 5 | 55–95 | dry | drymix |
| `dmTime` | Dry-mixing residence time | min | 5 | 90 | 30 | 5 | 15–60 | — | drymix |
| `dmT` | Dry-mixing temperature | °C | 15 | 70 | 30 | 5 | 20–50 | — | drymix |
| `dcPrimer` | Collector primer | — (choice) | `opts:["Carbon primer","Bare foil"]` | | 0 = Carbon primer | — | — | — | drycoat |
| `rollT` | Calender roll temperature | °C | 20 | 120 | 60 | 5 | 20–120 | — | calendering |
| `knife` | Cutting method | — (choice) | `opts:["Rolling knives","Laser"]` | | 0 = Rolling knives | — | — | — | slitting |
| `cutSpd` | Cutting speed | m/min | 80 | 150 | 110 | 5 | 80–150 | — | slitting, separation |
| `wear` | Blade wear | % | 0 | 100 | 20 | 5 | 0–70 | — | slitting, separation |
| `vacT` | Vacuum drying temperature | °C | 60 | 150 | 120 | 5 | 60–140 | — | vacdry |
| `sepMode` | Separation method | — (choice) | `opts:["Punching","Laser cutting"]` | | 0 = Punching | — | — | — | separation |
| `stackAcc` | Positioning tolerance | µm | 100 | 600 | 200 | 20 | 100–300 | — | stacking, winding |
| `webTens` | Web tension | N | 20 | 140 | 60 | 5 | 40–90 | — | winding, packHard |
| `drawDepth` | Pouch draw depth | mm | 2 | 10 | 6 | 0.5 | 2–8 | — | packPouch |
| `sealT` | Sealing temperature | °C | 150 | 230 | 190 | 5 | 180–200 | — | packPouch, packHard |
| `doseFac` | Electrolyte dose | × pore volume | 1 | 1.6 | 1.15 | 0.02 | 1.05–1.35 | — | fillPouch, fillHard |
| `fillP` | Wetting-cycle pressure | mbar | 20 | 400 | 150 | 10 | 50–250 | — | fillPouch, fillHard |
| `soak` | Wetting time | h | 1 | 36 | 12 | 1 | 6–36 | — | fillPouch, fillHard, rollpress |
| `pressP` | Roll-pressing pressure | MPa | 0.1 | 1.2 | 0.4 | 0.05 | 0.2–0.8 | — | rollpress |
| `preT` | Pre-treatment temperature | °C | 20 | 60 | 40 | 1 | 30–50 | — | rollpress |
| `formT` | Formation temperature assumption | °C | 15 | 60 | 25 | 1 | 20–45 | — | formation |
| `vMax` | Upper cut-off voltage | V | 4 | 4.4 | 4.2 | 0.05 | 4–4.25 | — | formation |
| `degP` | Degassing vacuum | mbar | 1 | 60 | 5 | 1 | 1–10 | — | degassing |
| `ageSOC` | Aging state of charge | % | 20 | 90 | 50 | 5 | 30–80 | — | aging |
| `ageHiT` | High-temperature stage | °C | 25 | 60 | 40 | 1 | 30–50 | — | aging |
| `shipSOC` | Final shipping state of charge | % | 5 | 60 | 15 | 5 | 5–30 | — | eol |

`preT` is the only control that no model output depends on: it does not appear anywhere in
`model()` (L1948–2105); it is read back only by the `rollpress` console (`ok(S.preT, 30, 50)`, L2617).

Control notes, verbatim (rendered under each slider, with the cited reference numbers):

* `tC` — "Typical production range 40–80 µm — from the electrode-processing literature, not from the PEM guide" [2]
* `tA` — "Typical production range 50–100 µm — from the electrode-processing literature, not from the PEM guide" [2]
* `speed` — "PEM range 35–80 m/min" [1]
* `dryT` — "PEM zone range 50–160 °C" [1]
* `force` — "PEM max 2 500 N/mm; above ≈2 300 it squeezes rather than compacts" [1,4]
* `vac` — "PEM range 8–48 h per batch; below ≈16 h moisture is off target" [1]
* `cRate` — "PEM range 0.1–0.5 C, stepped up over cycles" [1,7]
* `ageDays` — "PEM up to 3 weeks; under ≈10 d the screen stops working" [1]
* `solid` — "Less solvent means less to dry — but viscosity climbs fast" [2,8]
* `mixMin` — "PEM range 20 min – 6 h" [1]
* `mixT` — "PEM range 20–40 °C" [1]
* `gap` — "Set it to the wet film the recipe needs" [2]
* `dryLen` — "PEM: dryers up to 100 m" [1]
* `dcLine` — "PEM range 150–300 N/mm — this nip does the compaction the calender would otherwise do" [1]
* `dcRollT` — "PEM range 50–200 °C; warmer rolls soften the binder and raise adhesion" [1]
* `dcFib` — "Illustrative shear setting used to teach PTFE fibrillation; validated settings depend on mixer, binder and recipe" [1,14,15]
* `dmTime` — "Illustrative residence-time control; the source does not define one universal production window" [1,14,15]
* `dmT` — "Material- and equipment-dependent; excessive heat can promote agglomeration or alter binder behaviour" [14,15]
* `dcPrimer` — "PEM: the foil is often pre-treated with a carbon-based primer. Dry films hold on by mechanical interlocking, so bare metal gives them little to key into" [1,14]
* `rollT` — "Hot rolls compact more for the same force" [4]
* `knife` — "PEM lists both; laser leaves no burr but adds a heat-affected edge" [1]
* `cutSpd` — "PEM: mechanical 80–150 m/min" [1]
* `wear` — "A worn knife smears rather than cuts — change it by 70%" [1]
* `vacT` — "PEM range 60–150 °C; PVDF softens above ≈140 °C" [1]
* `sepMode` — "PEM: punching 0.2 s/sheet; laser is contact-free" [1]
* `stackAcc` — "PEM: stacking accuracy 200–300 µm" [1]
* `webTens` — "Too little telescopes the roll, too much tears the foil" [1]
* `drawDepth` — "PEM: deep drawing up to 10 mm; corners thin fastest past 8 mm" [1]
* `sealT` — "The PP sealant layer melts around 165 °C" [1]
* `doseFac` — "Under-dose and pores stay dry; over-dose and the cell gasses" [1]
* `fillP` — "PEM quotes a working pressure of about 150 mbar for filling and wetting" [1]
* `soak` — "Capillary action is slow — this is why cells queue here" [1]
* `pressP` — "Pouch route only — pushes electrolyte sideways into dry pores" [1]
* `preT` — "PEM high-temperature soaking / pre-treatment window: 30–50 °C" [1]
* `formT` — "Illustrative graphite/NMC assumption; validated formation temperatures depend on chemistry, design and manufacturer protocol" [7]
* `vMax` — "Reference graphite/NMC teaching limit: oxidation risk rises above about 4.25 V; actual limits depend on materials and protocol" [7]
* `degP` — "Pouch only — gas out, then the final seal" [1]
* `ageSOC` — "PEM range 30–80% SOC" [1]
* `ageHiT` — "PEM range 30–50 °C" [1]
* `shipSOC` — "Example plant target 10%–20%; PI 965 maximum 30% for UN 3480 shipped alone by air" [11,10]

"Break it" preset (`BREAK`, L5107–5111), applied to the current station's controls only:
`tC:80, tA:50, speed:80, dryT:60, force:2500, vac:8, cRate:0.5, ageDays:3, solid:75, mixMin:30,
mixT:40, gap:280, dryLen:20, rollT:120, knife:0, cutSpd:150, wear:100, vacT:60, sepMode:0,
stackAcc:600, webTens:140, drawDepth:10, sealT:150, doseFac:1, fillP:400, soak:1, pressP:1.2,
preT:60, formT:60, vMax:4.4, degP:60, ageSOC:20, ageHiT:25, shipSOC:60, dcLine:150, dcRollT:50,
dcFib:20, dmTime:5, dmT:70, dcPrimer:1`.

---

## 5 · OUTPUTS

### 5.1 The model — every formula, copied from `model()` (L1948–2105)

```js
const g = GEOM[route], pouch = route === "pouch", dry = proc === "dry";

const por  = dry
  ? clamp(52 - (S.dcLine - 150) / 150 * 30 - (S.dcRollT - 50) * 0.05, 15, 58)
  : clamp(50 - (S.force / 2500) * 30 - (S.rollT - 60) * 0.06, 15, 55);
const solidFrac = 1 - por / 100;
const activeCathodeFrac = 0.95;
const activeAnodeFrac = 0.95;
const capC = S.tC * 1e-4 * solidFrac * activeCathodeFrac * 4.65 * 180;
const capA = S.tA * 1e-4 * solidFrac * activeAnodeFrac * 2.24 * 350;
const np   = capA / capC;
const cellAh = capC * g.area * (g.layers > 1 ? 2 * g.layers : 1) / 1000;

const visc = 3000 * Math.exp(0.085 * (S.solid - 58)) * Math.pow(25 / S.mixT, 0.35);
const disp = clamp(100 - 40 * Math.exp(-(S.mixMin - 25) / 45));

const fibril  = clamp(S.dcFib + (S.dmTime - 30) * 0.35
                 - Math.max(0, 20 - S.dmT) * 0.45 - Math.max(0, S.dmT - 50) * 0.65);
const adhesion = clamp(94 - (S.dcPrimer ? 34 : 0) + (S.dcRollT - 50) * 0.06
                 - Math.max(0, 60 - fibril) * 1.2 - Math.max(0, fibril - 95) * 1.6);
const dcErr   = 0.6 + Math.max(0, 62 - fibril) * 0.16 + Math.max(0, fibril - 92) * 0.24
              + Math.abs(S.dcLine - 225) * 0.004;   /* areal-weight scatter, g/m² */

const volSolid = (S.solid / 100) * 0.72;            /* wt% → volume fraction */
const wetNeed  = S.tC / volSolid;                   /* wet film the recipe needs, µm */
const coatErr  = dry ? dcErr
               : 0.5 + Math.abs(S.gap - wetNeed) * 0.06 + (S.speed - 35) * 0.022
               + (100 - disp) * 0.05;               /* g/m² dry, target ±2 [1] */

const solventLoad = (100 - S.solid) / 42;
const needT = (40 + S.speed * 1.4) * solventLoad * (60 / S.dryLen);
const solventGap = dry ? 0 : Math.max(0, needT - S.dryT);      /* under-dried */
const crackGap   = dry ? 0 : Math.max(0, S.dryT - needT - 30); /* over-dried  */

const burrSlit = S.knife
  ? 2 + S.cutSpd * 0.01
  : 4 + S.wear * 0.10 + Math.max(0, S.cutSpd - 110) * 0.05;   /* µm */
const burrSep = pouch ? (S.sepMode ? 2.5 : 4.5 + S.wear * 0.12) : 0;
const burr = Math.max(burrSlit, burrSep);

const ppm = (18 + 420 * Math.exp(-(S.vac - 12) / 5.5)) * Math.pow(120 / S.vacT, 0.85);

const alignRisk = Math.max(0, S.stackAcc - 300) * 0.05
                + Math.abs(S.webTens - 60) * 0.03;
const sealQ = clamp(100 - Math.abs(S.sealT - 190) * 1.1 - Math.max(0, S.drawDepth - 8) * 5);

const wetDrive = S.soak * Math.max(0, S.doseFac - 0.98) * Math.pow(200 / S.fillP, 0.35)
               * (1 + (pouch ? S.pressP * 0.8 : 0)) / (por / 30);
const wetting  = clamp(100 - 55 * Math.exp(-wetDrive / 0.9));
const excess   = Math.max(0, S.doseFac - 1.35) * 60;   /* flooded cell gasses */

const seiQ = clamp(100 - Math.max(0, S.cRate - 0.2) * 90
                   - Math.max(0, S.formT - 50) * 1.6 - Math.max(0, 20 - S.formT) * 1.2
                   - Math.max(0, S.vMax - 4.25) * 140 - Math.max(0, ppm - 60) * 0.06);
const liLoss = 6 + Math.max(0, S.cRate - 0.2) * 22 + Math.max(0, S.formT - 45) * 0.35;

const shipOK = S.shipSOC <= 30;   /* PI 965 check for UN 3480 cells/batteries shipped alone by air */

const gasLeft   = pouch ? clamp(2 + (S.degP - 1) * 0.9 + (100 - seiQ) * 0.25, 0, 100) : 0;
const screenSens = clamp(35 + S.ageDays * 3.0 + (S.ageHiT - 25) * 1.0 + (S.ageSOC - 30) * 0.18);
const escape    = Math.max(0, 96 - screenSens) * 0.06;   /* defects that get past aging */

const uniformity = clamp(100 - Math.max(0, coatErr - 1) * 9 - solventGap * 0.5
                   - (dry ? Math.max(0, 90 - adhesion) * 0.55 : (100 - disp) * 0.3));
const moisture   = clamp(100 - Math.max(0, ppm - 40) * 0.18);
const npPenalty  = np < 1.02 ? (1.02 - np) * 260 : np > 1.25 ? (np - 1.25) * 90 : 0;
const cPenalty   = Math.max(0, S.cRate - 0.35) * 70;
const agePenalty = Math.max(0, 10 - S.ageDays) * 2.2;
const safety     = clamp(100 - npPenalty - cPenalty - Math.max(0, ppm - 60) * 0.12
                   - Math.max(0, burr - 8) * 2.5 - alignRisk * 1.5 - (100 - seiQ) * 0.25);
const yieldPct   = clamp(99.6 - solventGap * 0.55 - crackGap * 0.5 - Math.max(0, ppm - 40) * 0.05
                   - npPenalty * 0.5 - cPenalty * 0.5 - agePenalty
                   - Math.max(0, S.force - 2300) * 0.006
                   - Math.max(0, coatErr - 2) * 3.5
                   - Math.max(0, burr - 8) * 1.2
                   - Math.max(0, 96 - wetting) * 0.35
                   - Math.max(0, 90 - disp) * 0.12
                   - alignRisk - excess * 0.3
                   - (dry ? Math.max(0, 88 - adhesion) * 0.42 : 0)
                   - (pouch ? Math.max(0, 96 - sealQ) * 0.25 + gasLeft * 0.1 : 0)
                   - escape * 2, 55, 99.6);

/* --- throughput: 1 m effective coating width, 85% uptime --------------- */
const cathodePerCell = g.area * (g.layers > 1 ? 2 * g.layers : 1) / 10000;   /* m² */
const cellsDay = S.speed * 1.0 * 60 * 24 * 0.85 / (cathodePerCell * 2);
const gwh = cellsDay * 365 * cellAh * 3.65 / 1e9;
```

Helpers: `clamp(v, lo=0, hi=100) = Math.max(lo, Math.min(hi, v))` (L1535);
`fmt(n) = n >= 1000 ? Math.round(n).toLocaleString("en-US") : n.toFixed(n < 10 ? 2 : 1)` (L1536).

The constants `4.65`, `180`, `2.24`, `350`, `0.95`, `0.72`, `42`, `3.65` are literals in the code.
The code comments them as: "Illustrative active-material estimate. The 2026 reference recipes use
95 wt% active material in the dry solids for both electrodes. [1][2]".
There is **NOT IN SOURCE** any statement of units for `4.65 · 180` / `2.24 · 350` beyond the
output being labelled `mAh/cm²`.

### 5.2 Right-hand rail (`renderRail()`, L3364–3381)

| Label on screen | Value | Formula |
|---|---|---|
| `% PROCESS HEALTH` (gauge, `#yieldVal`) | `m.yieldPct.toFixed(1)` | `yieldPct`; ring uses `yieldPct.toFixed(0)` |
| `Coating uniformity` | `Math.round(m.uniformity) + "%"` | `uniformity` |
| `Moisture control` | `Math.round(m.moisture) + "%"` | `moisture` |
| `Risk-control score` | `Math.round(m.safety) + "%"` | `safety` |
| advice panel | `m.head` + `m.body`, `data-level = m.level` | flag chain L2060–2099 |
| `Capacity` | `m.cellAh.toFixed(1)` Ah · *route name* | `cellAh` |
| `Porosity` | `m.por.toFixed(0)%` — "after calendering" | `por` |
| `Moisture` | `m.ppm.toFixed(0)` — "ppm into the dry room" | `ppm` |
| `Output` | `m.gwh.toFixed(1)` — "GWh/a, this line" | `gwh` |

Default advice body: `` `Porosity ${por.toFixed(0)}%, N/P ${np.toFixed(2)}, residual moisture ${ppm.toFixed(0)} ppm, wetting ${wetting.toFixed(0)}%.` ``

### 5.3 Factory-overview KPIs (`renderOverview()`, L3139–3146)

| Label | Value | Sub-label |
|---|---|---|
| Reference capacity estimate | `m.cellAh.toFixed(1)` Ah | `GEOM[route].unit` |
| Illustrative cells per day | `fmt(m.cellsDay)` | assumes one 1 m line and 85% uptime |
| Illustrative annual output | `m.gwh.toFixed(1)` GWh | simplified geometry and uptime estimate |
| Process-health score | `m.yieldPct.toFixed(1)%` | teaching score, not a factory-yield prediction |
| Coating porosity | `m.por.toFixed(0)%` | set by calender line force |
| N/P ratio | `m.np.toFixed(2)` | anode capacity ÷ cathode capacity |

### 5.4 Station console readouts (`OPS[*].read`, L2320–2702)

Every row is `V(label, value, state, hint)`. State helpers: `ok(v,lo,hi)`,
`band(v,lo,hi,soft)` (L2316–2317).

**mixing** — Slurry viscosity `m.visc.toFixed(0)+" mPa·s"`, `band(visc,2000,6000,900)`;
Dispersion index `m.disp.toFixed(0)+"%"`; Solvent to remove `((100 - S.solid) * 10).toFixed(0)+" kg/t"`;
Batch time `(S.mixMin / 60).toFixed(1)+" h"`.

**drymix** — Illustrative fibrillation index `m.fibril.toFixed(0)+"%"` (hint "teaching indicator, not a release criterion");
Residence time `S.dmTime+" min"`; Mix temperature `S.dmT+" °C"`; Process solvent `"none"`.

**drycoat** — Fibrillation `m.fibril`; Adhesion to the foil `m.adhesion.toFixed(0)+"%"`;
Areal-weight scatter `"±"+m.dcErr.toFixed(1)+" g/m²"`; Porosity out of the nip `m.por.toFixed(0)+"%"`;
Solvent to evaporate `"none"`; Illustrative cathode areal capacity `m.capC.toFixed(2)+" mAh/cm²"`.

**coating** — Wet film the recipe needs `m.wetNeed.toFixed(0)+" µm"`; Gap error `(S.gap - m.wetNeed).toFixed(0)+" µm"`;
Coat weight scatter `"±"+m.coatErr.toFixed(1)+" g/m²"`; Illustrative cathode areal capacity `m.capC.toFixed(2)+" mAh/cm²"`;
Web throughput `(S.speed * 60).toFixed(0)+" m/h"`; Coating uniformity `m.uniformity.toFixed(0)+"%"`.

**drying** — Heat the web needs `m.needT.toFixed(0)+" °C"`; Peak set `S.dryT+" °C"`;
Margin `(S.dryT - m.needT).toFixed(0)+" °C"`; Residual solvent `m.solventGap > 0 ? (m.solventGap * 240).toFixed(0)+" ppm" : "< 300 ppm"`;
Binder migration `m.crackGap > 12 ? "high" : m.crackGap > 0 ? "some" : "low"`;
Dwell time in the dryer `(S.dryLen / S.speed * 60).toFixed(0)+" s"`.

**calendering** — Porosity `m.por.toFixed(0)+"%"`; Coating density `(4.65 * (1 - m.por / 100)).toFixed(2)+" g/cm³"`;
Illustrative cathode areal capacity `m.capC.toFixed(2)`; N/P ratio `m.np.toFixed(2)`;
Particle cracking `S.force > 2300 ? "likely" : S.force > 1900 ? "possible" : "unlikely"`;
Electrolyte access `m.por > 24 ? "good" : m.por > 19 ? "tight" : "poor"`.

**slitting** — Burr from this cut `m.burrSlit.toFixed(1)+" µm"`; Tallest burr in the cell `m.burr.toFixed(1)+" µm"`;
Method `S.knife ? "Laser" : "Rolling knives"`; Edge dust `S.knife ? "very low" : S.wear > 60 ? "high" : "low"`;
Heat-affected edge `S.knife ? "yes — binder degrades locally" : "none"`; Throughput `S.cutSpd+" m/min"`.

**vacdry** — Residual moisture `m.ppm.toFixed(0)+" ppm"` (hint "target below 50 ppm"); Batch time `S.vac+" h"`;
Oven temperature `S.vacT+" °C"`; Binder risk `S.vacT > 140 ? "PVDF softening" : "none"`;
HF risk carried forward `m.ppm > 80 ? "elevated" : "low"`.

**separation** — Burr from this cut `m.burrSep.toFixed(1)+" µm"`; Tallest burr in the cell `m.burr.toFixed(1)`;
Contour tolerance `S.sepMode ? "±60 µm" : "±200 µm"`; Cycle `S.sepMode ? "≈0.5 s/sheet" : "0.2 s/sheet"`;
Tool wear cost `S.sepMode ? "none — no contact" : "punch and die regrind"`; Method `S.sepMode ? "Laser cutting" : "Punching"`.

**stacking** — Positioning tolerance `S.stackAcc+" µm"`; Anode overhang left `Math.max(0, (600 - S.stackAcc) / 2).toFixed(0)+" µm"`;
Layers `"up to 120"`; Sheet rate `"≈1 s per sheet"`; Stack height `((S.tA * 2 + S.tC * 2 + 40) * 18 / 1000).toFixed(1)+" mm"`.

**winding** — Web tension `S.webTens+" N"`; Telescoping risk `S.webTens < 40 ? "high" : "low"`;
Foil tear risk `S.webTens > 100 ? "high" : S.webTens > 90 ? "some" : "low"`; Edge alignment `S.stackAcc+" µm"`;
Throughput `route === "cyl" ? "up to 30 cells/min" : "up to 6 cells/min"`.

**packPouch** — Draw depth `S.drawDepth.toFixed(1)+" mm"`; Film thinning at the corner `(S.drawDepth * 4.5).toFixed(0)+"%"`;
Sealing temperature `S.sealT+" °C"`; Seal quality `m.sealQ.toFixed(0)+"%"`;
Moisture ingress over life `m.sealQ >= 96 ? "within spec" : "elevated"`.

**packHard** — Housing `route === "cyl" ? "Deep-drawn can, 21700 class" : "Prismatic can and lid"`;
Lid safety devices `"burst disc + current interrupt"`; Weld energy proxy `S.sealT+" (index)"`;
Roll fit `S.webTens >= 40 && S.webTens <= 90 ? "clean insert" : "interference"`;
Machine investment `route === "cyl" ? "€ 35–45 M" : "€ 45–60 M"`.

**fillPouch** — Dose `S.doseFac.toFixed(2)+" × pore volume"`; Wetting-cycle pressure `S.fillP+" mbar"`;
Wetting reached `m.wetting.toFixed(0)+"%"`; Wetting time `S.soak+" h"`;
Free electrolyte `m.excess > 0 ? "yes — will gas" : "none"`; Porosity available `m.por.toFixed(0)+"%"`.

**fillHard** — Dose; Wetting-cycle pressure; Wetting reached; Wetting time; Port closure `"sealed after wetting"`;
`No roll pressing available` → `"wound cells cannot be squeezed"`.

**rollpress** — Pressure `S.pressP.toFixed(2)+" MPa"`; Wetting reached `m.wetting.toFixed(0)+"%"`;
Time saved vs soaking alone `(S.pressP * 14).toFixed(0)+" h"`;
Separator stress `S.pressP > 0.9 ? "high" : "acceptable"`; Pre-treatment temperature `S.preT+" °C"`.

**formation** — First charge `S.cRate.toFixed(2)+" C"`; Illustrative SEI score `m.seiQ.toFixed(0)+"%"`;
Illustrative irreversible loss `m.liLoss.toFixed(1)+"%"`; Time on the rack `(13 / (S.cRate / 0.25)).toFixed(1)+" h"`;
Cell temperature `S.formT+" °C"`; Upper cut-off `S.vMax.toFixed(2)+" V"`.

**degassing** — Vacuum level `S.degP+" mbar"`; Gas remaining `m.gasLeft.toFixed(1)+"%"`;
Gas generated at formation `(S.cRate * 34).toFixed(0)+" (index)"`; Final seal `"made after evacuation"`;
Cell thickness after `m.gasLeft < 6 ? "nominal" : "swollen"`.

**aging** — Total period `S.ageDays+" d"`; High-temperature stage `S.ageHiT+" °C"`;
State of charge `S.ageSOC+"%"`; Screen sensitivity `m.screenSens.toFixed(0)+"%"`;
Defects that would escape `(Math.max(0, 100 - m.screenSens) * 0.06).toFixed(2)+"%"`;
Floor space cost `(S.ageDays * 3.6).toFixed(0)+" (index)"`.

**eol** — Reference capacity estimate `m.cellAh.toFixed(1)+" Ah"`; Example plant target `S.shipSOC+"% SOC"`;
PI 965 air-shipping check `m.shipOK ? "≤30% — pass" : ">30% — fail"`;
Process-health score `m.yieldPct.toFixed(1)+"%"`; Cells per day, this line `fmt(m.cellsDay)`;
Annual output, this line `m.gwh.toFixed(1)+" GWh"`; Grading spread `"±"+(m.coatErr * 1.4).toFixed(1)+"% capacity"`.

Note: the `aging` console's "Defects that would escape" uses `(100 - screenSens) * 0.06`, while the
model's `escape` term uses `(96 - screenSens) * 0.06` — two different expressions in the source.

### 5.5 Machine-overview metrics (`kpis()`, L4552–4560; `lotId()`, `gradeOf`, L4563–4570)

```js
const a = clamp(99 - bad * 9 - warn * 3);                     /* availability  */
const e = clamp(72 + (S.speed - 35) / 45 * 26 - bad * 6);     /* performance   */
const q = clamp(m.yieldPct);                                  /* quality       */
return { a, e, q, oee: a * e * q / 10000, bad, warn, off: bad * 2 + warn, list, lv };
```
`bad` / `warn` are counts of `OPS[st.id].verdict(m)[0]` over the active stations.
Displayed as donuts `Overall` / `Availability` / `Performance` / `Quality`, under the heading
`OEE — ILLUSTRATIVE`. CURRENT block: `Line`, `Rate` (`${S.speed} m/min · ${fmt(m.cellsDay)} cells/day`),
`Illustrative grade` (`gradeOf(y) = y >= 98.5 ? "A" : y >= 97 ? "B" : y >= 95 ? "C" : "REWORK"`),
`Lot ID` (deterministic hash of `JSON.stringify(S) + route + proc`), `Stations off window`
(`${k.bad + k.warn} of ${k.list.length}`). Sparklines: `OEE` (%), `Scrap` (`100 - q`), `Alarm load` (`off`),
72-sample rolling history pushed on every `refresh()`.

### 5.6 Material-flow live values (`renderFlow()`, L4033–4053)

`slurry` `${m.visc.toFixed(0)} mPa·s · ${S.solid} wt% solids` · `wet` `${m.wetNeed.toFixed(0)} µm wet film` ·
`dryel` `${(m.solventGap*240).toFixed(0)} ppm solvent left` or `solvent removed` ·
`comp` `${m.por.toFixed(0)}% porosity · ${m.capC.toFixed(2)} mAh/cm²` · `dry` `${m.ppm.toFixed(0)} ppm residual water` ·
`piece` `burr ${m.burr.toFixed(1)} µm` · `stack` `N/P ${m.np.toFixed(2)}` · `filled` `${m.wetting.toFixed(0)}% wetted` ·
`formed` `SEI ${m.seiQ.toFixed(0)}% · ${m.liLoss.toFixed(1)}% Li spent` · `aged` `screen ${m.screenSens.toFixed(0)}%` ·
`graded` `${m.cellAh.toFixed(1)} Ah · ${m.yieldPct.toFixed(1)}% yield` ·
dry route adds `fibril` `${m.fibril.toFixed(0)}% fibrillation` and `film` `${m.por.toFixed(0)}% porosity · adhesion ${m.adhesion.toFixed(0)}%`.

### 5.7 Charts (`CHARTS`, L2918–3012)

Each chart is produced by `sweep(key, get, 60)` (L2712), which re-runs `model()` 61 times
across the control's full range. Bespoke charts: `agingOCVChart()` (L2832) —
`good(t) = 3.2*(1-e^(-t/1.6)) + 0.14*t*accel`, `bad(t) = 3.2*(1-e^(-t/1.6)) + 1.15*t*accel`,
`accel = 1 + (HT - 22)/28`, separation flagged as caught when `sep >= 5` (mV);
`formationChart()` (L2881) — `hours = 13 / (C / 0.25)`, `cc = hours*0.78`,
`v(t) = t < cc ? 2.8 + (S.vMax - 2.8)*(1 - e^(-t/(cc*0.34))) : S.vMax`.
EoL chart 2 plots `m.cellAh * 3.65 * S.shipSOC / 100` ("Watt-hours per cell as shipped") with
`xMark:30`, label `above IATA PI 965`.

### 5.8 Factory view totals (`renderFactory()`, L4465–4526)

`lo`/`hi` = arithmetic sums of the quoted `CAPEX` ranges for the active line;
`Machinery and equipment, total` shows `€ ${lo}–${hi} M` on the wet route and
`"Not available from source"` on the dry route; `Formation and aging share` =
`round(mid(Formation)+mid(Aging) / totalMid * 100)` on the wet route, `"Not calculated"` on dry.
Reference plant, verbatim: **"10 GWh per year, roughly 30 000 000 pouch cells per year, 80 Ah per cell."**

---

## 6 · WORKED EXAMPLE

Route `pouch`, electrode route `wet`, all controls at `def`. Arithmetic below is the model
executed by hand; it was cross-checked by running the extracted `model()` on Node 22 — all
displayed values match to the digits shown.

### 6.1 Run A — every input at its default

Inputs used: `tC 65, tA 80, speed 60, dryT 130, force 1700, vac 22, cRate 0.25, ageDays 14,
solid 58, mixMin 120, mixT 25, gap 155, dryLen 60, rollT 60, knife 0, cutSpd 110, wear 20,
vacT 120, sepMode 0, stackAcc 200, webTens 60, drawDepth 6, sealT 190, doseFac 1.15,
fillP 150, soak 12, pressP 0.4, formT 25, vMax 4.2, degP 5, ageSOC 50, ageHiT 40, shipSOC 15`.
`GEOM.pouch = {area:200, layers:18}`.

```
por        = 50 − (1700/2500)·30 − (60−60)·0.06 = 50 − 0.68·30 = 50 − 20.4        = 29.60 %
solidFrac  = 1 − 0.296                                                            = 0.704
capC       = 65·1e−4 · 0.704 · 0.95 · 4.65 · 180
           = 0.0065 · 0.704 = 0.004576 ; ·0.95 = 0.0043472 ; ·4.65 = 0.02021448 ; ·180
                                                                                  = 3.638606 mAh/cm²
capA       = 80·1e−4 · 0.704 · 0.95 · 2.24 · 350
           = 0.008 · 0.704 = 0.005632 ; ·0.95 = 0.0053504 ; ·2.24 = 0.011984896 ; ·350
                                                                                  = 4.194714 mAh/cm²
np         = 4.194714 / 3.638606                                                  = 1.152835
cellAh     = 3.638606 · 200 · (2·18) / 1000 = 3.638606 · 7200 / 1000              = 26.197966 Ah
visc       = 3000 · e^(0.085·0) · (25/25)^0.35                                    = 3000 mPa·s
disp       = 100 − 40·e^(−(120−25)/45) = 100 − 40·e^(−2.11111) = 100 − 40·0.121103 = 95.155867 %
volSolid   = (58/100)·0.72                                                        = 0.4176
wetNeed    = 65 / 0.4176                                                          = 155.651 µm
coatErr    = 0.5 + |155 − 155.651|·0.06 + (60−35)·0.022 + (100−95.155867)·0.05
           = 0.5 + 0.03906 + 0.55 + 0.242207                                      = 1.331287 g/m²
solventLoad= (100−58)/42                                                          = 1.0
needT      = (40 + 60·1.4) · 1.0 · (60/60) = 40 + 84                              = 124 °C
solventGap = max(0, 124 − 130)                                                    = 0
crackGap   = max(0, 130 − 124 − 30)                                               = 0
burrSlit   = 4 + 20·0.10 + max(0,110−110)·0.05                                    = 6.0 µm
burrSep    = 4.5 + 20·0.12                                                        = 6.9 µm
burr       = max(6.0, 6.9)                                                        = 6.9 µm
ppm        = (18 + 420·e^(−(22−12)/5.5)) · (120/120)^0.85
           = 18 + 420·e^(−1.818182) = 18 + 420·0.162320                           = 86.174657 ppm
alignRisk  = max(0,200−300)·0.05 + |60−60|·0.03                                   = 0
sealQ      = 100 − |190−190|·1.1 − max(0,6−8)·5                                   = 100
wetDrive   = 12 · (1.15−0.98) · (200/150)^0.35 · (1 + 0.4·0.8) / (29.6/30)
           = 12·0.17 = 2.04 ; ·1.105934 = 2.256105 ; ·1.32 = 2.978058 ; /0.986667 = 3.018302
wetting    = 100 − 55·e^(−3.018302/0.9) = 100 − 55·e^(−3.353669) = 100 − 55·0.034956
                                                                                  = 98.077420 %
excess     = max(0, 1.15 − 1.35)·60                                               = 0
seiQ       = 100 − max(0,0.25−0.2)·90 − 0 − 0 − 0 − max(0, 86.174657−60)·0.06
           = 100 − 4.5 − 1.570479                                                 = 93.929521 %
liLoss     = 6 + 0.05·22 + max(0, 25−45)·0.35 = 6 + 1.1                           = 7.1 %
shipOK     = 15 ≤ 30                                                              = true
gasLeft    = 2 + (5−1)·0.9 + (100−93.929521)·0.25 = 2 + 3.6 + 1.517620            = 7.117620 %
screenSens = 35 + 14·3.0 + (40−25)·1.0 + (50−30)·0.18 = 35 + 42 + 15 + 3.6        = 95.60 %
escape     = max(0, 96 − 95.6)·0.06                                               = 0.024
uniformity = 100 − max(0, 1.331287−1)·9 − 0 − (100−95.155867)·0.3
           = 100 − 2.981583 − 1.453240                                            = 95.565176 %
moisture   = 100 − max(0, 86.174657−40)·0.18 = 100 − 8.311438                     = 91.688562 %
npPenalty  = 0 (1.02 ≤ 1.152835 ≤ 1.25) ; cPenalty = 0 ; agePenalty = 0
safety     = 100 − 0 − 0 − 26.174657·0.12 − max(0, 6.9−8)·2.5 − 0 − (100−93.929521)·0.25
           = 100 − 3.140959 − 0 − 1.517620                                        = 95.341421 %
yieldPct   = 99.6 − 0 − 0 − 46.174657·0.05 − 0 − 0 − 0
             − max(0,1700−2300)·0.006 − max(0,1.331287−2)·3.5 − max(0,6.9−8)·1.2
             − max(0,96−98.07742)·0.35 − max(0,90−95.155867)·0.12 − 0 − 0
             − (0·0.25 + 7.117620·0.1) − 0.024·2
           = 99.6 − 2.308733 − 0.711762 − 0.048                                   = 96.531505 %
cathodePerCell = 200·36/10000                                                     = 0.72 m²
cellsDay   = 60 · 1.0 · 60 · 24 · 0.85 / (0.72·2) = 73 440 / 1.44                 = 51 000 cells/day
gwh        = 51 000 · 365 · 26.197966 · 3.65 / 1e9                                = 1.780014 GWh
```

**Displayed values, Run A**

| Where | Label | Value |
|---|---|---|
| Rail gauge | % PROCESS HEALTH | **96.5** (ring `--v:97`) |
| Rail | Coating uniformity | **96%** |
| Rail | Moisture control | **92%** |
| Rail | Risk-control score | **95%** |
| Rail advice | level `ok` | **"Model inside the training window"** / "Porosity 30%, N/P 1.15, residual moisture 86 ppm, wetting 98%." |
| Rail KPI | Capacity / Porosity / Moisture / Output | **26.2 Ah** · **30%** · **86 ppm** · **1.8 GWh/a** |
| Overview | Reference capacity estimate | **26.2 Ah** |
| Overview | Illustrative cells per day | **51,000** |
| Overview | Illustrative annual output | **1.8 GWh** |
| Overview | Process-health score | **96.5%** |
| Overview | Coating porosity | **30%** |
| Overview | N/P ratio | **1.15** |
| Calendering console | Porosity / Coating density / cathode areal capacity / N/P / Particle cracking / Electrolyte access | **30%** · **3.27 g/cm³** · **3.64 mAh/cm²** · **1.15** · **unlikely** · **good** |
| Calendering verdict | `ok` | "Nip inside the useful window" — "30% porosity, 3.27 g/cm³, N/P 1.15." |
| Coating console | wet film needed / gap error / coat weight scatter / uniformity | **156 µm** · **−1 µm** · **±1.3 g/m²** · **96%** |
| Drying console | heat needed / margin / dwell | **124 °C** · **6 °C** · **60 s** |
| Vacuum drying console | Residual moisture | **86 ppm** (state `warn`, "Above target, releasable under concession") |
| Filling console | Wetting reached | **98%** |
| Formation console | SEI score / irreversible loss / time on rack | **94%** · **7.1%** · **13.0 h** |
| Degassing console | Gas remaining | **7.1%** |
| Aging console | Screen sensitivity | **96%** |
| EoL console | capacity / PI 965 check / process health / cells per day / annual output / grading spread | **26.2 Ah** · **≤30% — pass** · **96.5%** · **51,000** · **1.8 GWh** · **±1.9% capacity** |
| Machine overview | Illustrative grade | `gradeOf(96.531505)` → **C · 96.5%** |

No advice flag fires: `disp 95.2 ≥ 85`, `2000 ≤ visc 3000 ≤ 6000`, `coatErr 1.33 ≤ 2`,
`force 1700 ≤ 2300`, `crackGap 0 ≤ 12`, `np 1.15` inside 1.02–1.25, `burr 6.9 ≤ 10`,
`ppm 86 ≤ 120`, `wetting 98 ≥ 90`, `sealQ 100 ≥ 90`, `solventGap 0 ≤ 10`, `cRate 0.25 ≤ 0.42`,
`vMax 4.2 ≤ 4.3`, `shipOK true`.

### 6.2 Run B — **Calender line force** (`force`) at its maximum, 2 500 N/mm

Only `force` changes; everything else stays at default.

```
por      = 50 − (2500/2500)·30 − 0                                              = 20.00 %   (was 29.60)
solidFrac= 0.80                                                                              (was 0.704)
capC     = 0.0065 · 0.80 · 0.95 · 4.65 · 180                                    = 4.134780 mAh/cm²
capA     = 0.008  · 0.80 · 0.95 · 2.24 · 350                                    = 4.766720 mAh/cm²
np       = 4.766720 / 4.134780                                                  = 1.152835  (unchanged —
           solidFrac cancels in the ratio)
cellAh   = 4.134780 · 7200 / 1000                                               = 29.770416 Ah
wetDrive = 2.978058 / (20/30) = 2.978058 / 0.666667                             = 4.467087
wetting  = 100 − 55·e^(−4.467087/0.9) = 100 − 55·e^(−4.963430) = 100 − 55·0.006989
                                                                                = 99.615608 %
yieldPct = 99.6 − 46.174657·0.05 − max(0, 2500−2300)·0.006 − (0 + 7.117620·0.1) − 0.024·2
         = 99.6 − 2.308733 − 1.200000 − 0.711762 − 0.048                        = 95.331505 %
gwh      = 51 000 · 365 · 29.770416 · 3.65 / 1e9                                = 2.022743 GWh
```
Unchanged by this input: `visc 3000`, `disp 95.155867`, `coatErr 1.331287`, `needT 124`,
`solventGap 0`, `crackGap 0`, `burr 6.9`, `ppm 86.174657`, `alignRisk 0`, `sealQ 100`,
`seiQ 93.929521`, `liLoss 7.1`, `gasLeft 7.117620`, `screenSens 95.6`, `escape 0.024`,
`uniformity 95.565176`, `moisture 91.688562`, `safety 95.341421`, `cellsDay 51 000`.

**Displayed values, Run B**

| Where | Label | Value | Δ vs Run A |
|---|---|---|---|
| Rail gauge | % PROCESS HEALTH | **95.3** (ring `--v:95`) | −1.2 |
| Rail | Coating uniformity | **96%** | — |
| Rail | Moisture control | **92%** | — |
| Rail | Risk-control score | **95%** | — |
| Rail advice | level `warn` | **"Calender line force very high"** — "Above roughly 2 300 N/mm this teaching model increases the risk of over-compression, particle damage and stress cracking. PEM caps line pressure at 2 500 N/mm." | was `ok` |
| Rail KPI | Capacity / Porosity / Moisture / Output | **29.8 Ah** · **20%** · **86 ppm** · **2.0 GWh/a** | +3.6 Ah, −10 pt, —, +0.2 |
| Overview | cells per day / annual output / process health / porosity / N/P | **51,000** · **2.0 GWh** · **95.3%** · **20%** · **1.15** | — / +0.2 / −1.2 / −10 / — |
| Calendering console | Porosity / density / areal capacity / N/P / Particle cracking / Electrolyte access | **20%** · **3.72 g/cm³** · **4.13 mAh/cm²** · **1.15** · **likely** (`bad`) · **tight** (`warn`) | |
| Calendering verdict | `bad` | "Squeezing, not compacting" — "Above roughly 2 300 N/mm the particles fracture and the coating develops stress cracks. PEM caps line pressure at 2 500 N/mm." | was `ok` |
| Filling console | Wetting reached | **100%** | +2 |
| EoL console | capacity / process health / annual output | **29.8 Ah** · **95.3%** · **2.0 GWh** | |
| Machine overview | Illustrative grade | `gradeOf(95.331505)` → **C · 95.3%** | same class |

Net effect in the code's own terms: maximum line force raises the illustrative capacity
estimate by **+13.6%** (26.2 → 29.8 Ah) and annual output by **+0.24 GWh**, drives porosity to
the bottom of the drawn "useful window" (20%), and costs **1.2 points** of process-health score,
all of it from the single term `− Math.max(0, S.force - 2300) * 0.006` (= 1.2).

---

## 7 · EXACT WORDING — scientific caveats and scope statements (verbatim)

### 7.1 Page-level scope

* Title / `<h1>`: `CellForge · Lithium-ion Cell Production Simulator` /
  `CellForge — Lithium-ion Cell Production Simulator`
* `<meta name="description">`: `CellForge — interactive lithium-ion cell production simulator for a reference graphite/NMC process route.`
* Topbar pill (L831): `Reference chemistry` `graphite / NMC`
* Sidebar footer (L818–821): `Process data after PEM RWTH Aachen, Production Process of a Lithium-Ion Battery Cell. Training simulation — site SOPs always govern.`
* Rail head (L850): `ILLUSTRATIVE PROCESS MODEL` / `Line condition`
* Rail advice default (L867–870): `Model inside the training window` / `Move a setpoint and the illustrative downstream relationships recalculate.`
* Source header comment (L891–896): `Process data after PEM RWTH Aachen, "Production Process of a Lithium-Ion Battery Cell". Every parameter range below is taken from that document; the physics chain that links them is a teaching model.`
* Model header comment (L1877–1879): `PROCESS MODEL — an illustrative simulator. One material state flows down the line and every station transforms it, so a setpoint change reaches the cell.`

### 7.2 Overview cards (L3080–3086)

> **Reference recipe** — "**Graphite negative electrode · NMC positive electrode.** The material properties, voltage guidance and simplified capacity relationships apply only to this reference chemistry. LFP, silicon-rich, sodium and solid-state routes require different inputs and process windows. The wet and dry electrode routes are both modelled, but both on this same chemistry."

> **Model scope** — "Published sources support the process sequence and displayed operating ranges. Capacity, throughput, wetting, process-health and risk-control outputs are illustrative teaching relationships. They are not calibrated plant predictions, equipment-sizing calculations or release criteria."

Overview KPI sub-labels (L3141–3143): "assumes one 1 m line and 85% uptime";
"simplified geometry and uptime estimate"; "teaching score, not a factory-yield prediction".

Overview "Three major defect drivers" (L3166–3168):

> "**Particles and burrs.** A burr from slitting or a particle rolled in at the calender can pierce the separator. A severe internal short can create local heating that external controls may not stop; prevention depends on cleanliness, edge quality, separator integrity and screening."
> "**Water.** Residual water can hydrolyse LiPF₆ and generate HF-containing species that degrade electrolyte and interfaces. That is why the dew point drops station by station to −50…−70 °C at electrolyte filling."
> "**Cross-contamination.** Anode and cathode powders look identical and are both black. Mixing rooms are commonly separated to reduce this risk."

### 7.3 Station data — quoted parameter and part strings

* `vacdry.params` (L1677): `Working pressure: 0.07 mbar < p < 1 000 mbar`
* `fillPouch` part note (L1771): "The chamber is evacuated — the guide quotes a **working pressure of about 150 mbar** — before a high-precision dosing needle meters the electrolyte. The very dry environment limits LiPF₆ hydrolysis and the formation of HF-containing species that can degrade interfaces and cell life."
* `fillP` control label / note (L1917): `Wetting-cycle pressure` — "PEM quotes a **working pressure of about 150 mbar for filling and wetting**"
* `eol.params` (L1869): `Allowable loss rate: under 5 mV/week` · `Example plant shipping target: 10%–20% SOC` · `PI 965 maximum: 30% SOC for UN 3480 shipped alone by air` · `Illustrative OCV-loss flag: 5 mV/week; actual criteria depend on chemistry, SOC, temperature and test duration`
* `eol` part "EOL test rig" (L1866): "Cells undergo a **defined capacity test with specified charge, rest, discharge and cutoff conditions**. The cell is then adjusted to its shipping SOC; pulse, DC-resistance, optical, OCV and leakage tests vary by manufacturer."
* `eol` part "Packing" (L1868): "Cells are covered in plastic and stacked in cardboard. An example plant target is 10–20% SOC. The applicable transport maximum depends on shipment configuration and mode; for UN 3480 shipped alone by air under PI 965, the file checks a 30% maximum."
* `drymix` part "High-shear zone" (L1564): "Mechanical work draws PTFE-based binder into fibrils that connect particles. The displayed fibrillation index is an **illustrative teaching relationship, not an equipment recipe**."
* `coating` part "Wet-film gauge" (L1585): "…The ±2 g/m² dry accuracy used here is a common working target from the electrode-processing literature, **not a figure the PEM guide quotes**."
* `aging` part "The decision" (L1853): "Stable OCV is one release indicator, **not proof of a defect-free cell**. Excessive voltage loss can indicate elevated self-discharge, leakage or an internal defect and should trigger the manufacturer's investigation and rejection criteria."
* `rollpress` part "Result" (L1805): "More uniform electrolyte distribution reduces poorly wetted or locally inactive regions and supports more uniform formation. The benefit depends on cell design and the full formation protocol."
* `formation.alts` (L1823): "Procedures differ by manufacturer and cell chemistry — formation recipes are treated as core know-how"
* `drymix` part "Screen and sealed transfer" (L1566): "…Release criteria are manufacturer-specific."

### 7.4 Component descriptions (`COMPONENTS`)

* Separator (L2199): "It physically separates the electrodes while supporting ionic transport. Because severe internal shorts can create local heating that external controls may not stop, cleanliness, edge quality, separator integrity and screening are essential. Some multilayer separator designs include a PE shutdown layer whose pores can close as temperature rises. **Shutdown behaviour depends on construction and does not guarantee prevention of thermal runaway.**"
* Anode (L2208): "The anode is typically designed with more usable capacity than the cathode. The target N/P ratio is design- and protocol-dependent; insufficient anode capacity raises the risk of lithium plating during charge."
* SEI (L2235): "The SEI is formed in situ during the first controlled cycles and cannot be inspected or reworked like a conventional manufactured part. It consumes a chemistry- and process-dependent fraction of cyclable lithium; formation rate, temperature, voltage limits and cleanliness all influence its properties and plating risk."
* Electrolyte (L2226): "…It is also why the dry room exists — Residual water can hydrolyse LiPF₆ and generate HF-containing species that degrade the electrolyte, interfaces and aluminium collector."

### 7.5 Advice-panel flags (`model()`, L2060–2099)

* `Calender line force very high` — "Above roughly 2 300 N/mm this teaching model increases the risk of over-compression, particle damage and stress cracking. PEM caps line pressure at 2 500 N/mm."
* `Anode heavily over-sized` — "N/P ratio X. Excess anode capacity is not fully utilised and reduces energy density; **it does not by itself establish that the cell is safe**."
* `Burr above the illustrative risk threshold` — "X µm on the cut edge against a 12–25 µm separator reference. **This is an illustrative risk flag, not a universal acceptance limit.**"
* `Residual moisture too high` — "X ppm going into the dry room. Residual water can hydrolyse LiPF₆ and generate HF-containing species that degrade electrolyte and interfaces."
* `Electrolyte has not reached every pore` — "Wetting X%. Incomplete wetting can create locally inactive or nonuniform regions. Additional rest or pressure cycling may help, but **formation should not be treated as a reliable correction for an inadequate filling process**."
* `Web is under-dried` — "At X m/min and Y wt% solids the teaching model estimates about Z °C but the setpoint is W °C. Excess residual solvent can impair adhesion, interfaces and cell performance."
* `Upper cut-off voltage too high` — "X V. Electrolyte oxidation and interfacial degradation can increase gas generation and impedance."
* `Above the air-freight state of charge limit` — "X% SOC. For this UN 3480 shipped-alone air scenario, PI 965 limits state of charge to 30%; other shipment configurations and modes use different requirements."
* `Anode under-sized — lithium plating risk` — "N/P ratio X. Insufficient anode capacity raises lithium-plating risk during charge and can contribute to internal-short hazards."

### 7.6 Console verdicts and hints

* `drymix` ok (L2355): "Illustrative fibrillation index X%. Release still depends on the manufacturer's homogeneity, agglomerate and powder-flow criteria."
* `fillPouch` bad (L2584): "X%. Incomplete wetting can create nonuniform regions. Increase wetting time or review pressure cycling and dose; **do not rely on formation to correct an inadequate filling process**."
* `rollpress` bad (L2619): "Above the selected teaching window, pressure on a wet stack raises separator-stress and particle-driven puncture risk. Actual limits depend on separator, stack geometry, cleanliness and equipment validation."
* `rollpress` ok (L2621): "X% illustrative wetting. More uniform electrolyte distribution supports more uniform formation, but **this score does not prove that every pore is wetted**."
* `formation` "Charging too fast" (L2638): "The selected first-charge rate is near the upper end of the reference range. Faster formation can change interphase properties and raise plating risk under some conditions; validated recipes are chemistry- and design-specific."
* `formation` "Cut-off too high" (L2640): "The selected cut-off exceeds the reference graphite/NMC teaching limit. Electrolyte oxidation, gas generation and accelerated degradation risk can rise, but actual limits depend on materials and protocol."
* `formation` ok (L2642): "X% illustrative SEI score and Y% illustrative first-cycle irreversible loss. Actual values depend on materials, electrolyte and formation protocol."
* `degassing` ok (L2660): "X% residual gas at Y mbar. **Hard-case gas-management and closure sequences vary by design**; pressure-relief devices do not replace controlled formation-gas management."
* `packHard` hint (L2559): "gas-handling and closure sequences vary by hard-case design"
* `aging` lead (L2665): "You are at aging. The cell is rested and monitored for OCV drift and other release indicators. This screen can reveal elevated self-discharge or latent internal defects, but **it is not a standalone proof of cell safety**."
* `aging` bad (L2675): "A slow self-discharge fault needs time and controlled temperature to appear as measurable voltage drift. Shortening the screen can reduce sensitivity."
* `aging` ok (L2679): "X days, Y °C stage, Z% illustrative sensitivity using a 5 mV/week teaching flag."
* `eol` read hints (L2687–2689): "the actual capacity test requires a defined charge/rest/discharge protocol"; "illustrative target; manufacturer-specific"; "UN 3480 cells/batteries shipped alone by air; other shipment configurations use different instructions"
* `eol` bad (L2695): "For this UN 3480 shipped-alone air scenario, PI 965 limits state of charge to 30%. Other shipment configurations and transport modes use different requirements."
* `eol` warn (L2696): "Illustrative process-health score is low"
* `drycoat` lead (L2360): "…Web speed is an explicit teaching assumption because the guide does not quote a separate dry-coating speed."

### 7.7 Chart notes

* Aging OCV chart, caught (L2875): "At X days and Y °C the two cells are Z mV apart — above the illustrative 5 mV/week flag, so this teaching example would trigger further investigation or rejection."
* Aging OCV chart, not caught (L2876): "At X days and Y °C the two cells are only Z mV apart. In this teaching example the separation is too small for the assumed screen. **A real release decision requires validated limits, measurement uncertainty and site procedures.**"
* Aging chart legend (L2871): "illustrative high-self-discharge cell"
* Formation chart note (L2911–2913): "…SEI quality X%, with Y% illustrative first-cycle irreversible loss. **Actual values are chemistry- and protocol-dependent.**"

### 7.8 Big-picture views

* Machine overview, "What is real here and what is not" (L4987–4992): "The station order, the phase split, the four-hall factory concept and the environment each hall needs are from the process guide. The lamps are real in the sense that they come from this simulator's own process windows. OEE, availability and performance are illustrative constructions on top of the teaching model — a plant measures them from run time, ideal cycle time and good count, none of which this simulator has. **Read them as a way of seeing the line react, not as a number to quote.**"
* `kpis()` code comment (L4551): "OEE, in the shape a plant would recognise. Illustrative, not measured."
* Radar disclaimer (L4364–4365): "**Disclaimer, from the source:** the radar is a snapshot of the industry, judged against use in series production. **It is an excerpt and does not claim to be exhaustive.**"
* Radar solid-state detail (L4352–4354): "This is a solid-state route. It replaces the liquid electrolyte and the separator with a solid electrolyte, so filling, wetting and degassing all disappear — which is why it needs its own line rather than a change to this one."
* Factory footnote (L4525): "Published ranges cover machinery and equipment only — not building, utilities, dry-room plant or land. For the wet route, the displayed total is the arithmetic sum of quoted station ranges. **A complete dry-route total is deliberately not calculated because the guide does not separately quote dry mixing/fibrillation or split slitting from the combined calendering-and-slitting range. The reported 35% CapEx reduction is a potential process comparison for dry coating, not a guaranteed complete-factory reduction.**"
* Dry-vs-wet card footnote (L3286–3289): "The four figures are the guide's own comparison against a wet coating line. Independent life-cycle work broadly agrees on the energy number at the manufacturing stage — around 41% less — but the saving shrinks to a few percent once the whole cradle-to-grave life cycle is counted, because cell production is only part of it."
* Matrix commentary (L4150–4151): "The separator is introduced during stacking or winding. Damage at this stage can create latent short-circuit risk, so cleanliness, alignment and edge quality are critical." · "The SEI is formed during formation. It is not installed as a conventional part, and its properties depend on the full formation and cleanliness history."
* References view (L5012–5014): "**What is modelled rather than cited:** the chain that connects one setpoint to the next is a teaching model, fitted so the defaults land near the reference plant. **Use it to understand direction and sensitivity, not to size real equipment.**"

### 7.9 Material-flow notes

* `filled` (L2300): "Electrolyte is dosed under vacuum and given time — sometimes with pressure cycling or roll pressing — to reach the porous structure. Incomplete wetting can create locally inactive or nonuniform regions and may not be fully corrected later."
* `formed` (L2302): "The first controlled cycles form the SEI and activate the cell. A chemistry- and process-dependent fraction of cyclable lithium is consumed during interphase formation."
* `aged` (L2304): "Days to weeks of rest with OCV logged. Excessive voltage loss can indicate elevated self-discharge or an internal defect; the threshold depends on chemistry, SOC, temperature and test duration."
* `stack` (L2296): "…The anode is typically designed with overhang beyond the cathode edge according to the cell design."

### 7.10 Guided-tour stops with scope language

* Stop "Then form and laminate the dry film" (L3770): "…The guide reports **potential savings for the dry-coating process comparison, not a guaranteed complete-factory result**."
* Stop "The dry route begins without slurry" (L3768): "…**The source does not provide one universal mixer recipe, so the controls here are explicitly illustrative and material-dependent.**"
* Stop "The most dangerous burr in the plant" (L3774): "Rolling knives cut the wide roll into daughter rolls. A burr can damage or pierce the separator and create a latent internal-short risk, so blade condition, edge inspection and cleanliness are critical."
* Stop "The cell's first controlled cycles" (L3782): "The reference guide shows stepped formation rates in the 0.1–0.5 C range. These first controlled cycles form the SEI, consume some cyclable lithium and can generate gas. Formation is capital- and time-intensive, and **validated recipes are manufacturer-specific**."
* Stop "Three weeks of watching" (L3784): "…Excessive OCV loss can indicate elevated self-discharge or an internal defect. **The actual threshold depends on chemistry, SOC, temperature, duration and the manufacturer's release procedure.**"
* Stop "What replaces all this next" (L3790): "…Three selected solid-state families — polymer, sulfide and oxide — replace the conventional liquid-electrolyte-filled separator architecture and therefore require different process chains. **Exact filling, wetting and gas-management steps depend on the chosen solid-state design.**"
* Stop "And where every number came from" (L3792): "Process parameters, room classes, machine investments and cycle times are from the 5th edition of the PEM RWTH Aachen and VDMA guide, February 2026. The physics linking them is from the peer-reviewed sources listed here. Every superscript number in this simulator opens the source it came from."

### 7.11 Primary reference string (`REFS[0]`, L2118–2120)

> Michaelis, S.; Rothhagen, B.; Heimes, H. H.; Born, H.; Kampker, A.; Scherer, C.; Lingohr, P.
> *Production Process of a Lithium-Ion Battery Cell*, **5th ed.**; PEM of RWTH Aachen University &
> VDMA: Frankfurt am Main, **February 2026**. ISBN 978-3-947920-71-6.
> Used for: "Process parameters, environment classes, machine investments and cycle times used in this simulator."

16 references in total (`REFS`, L2117–2166), numbered 1–16, each with `tag`, `txt`, `use`, `url`.

### 7.12 Wording that is absent by design

The page contains no occurrence of `digital twin` (any case), `Predicted yield`, or `Safety margin`
— the outputs are named `Process-health score`, `Risk-control score`, `Illustrative SEI score`,
`Illustrative fibrillation index`, `Illustrative irreversible loss`. These absences are asserted by
`tests/test_battery_production_simulator.py::test_production_scope_is_explicit`.

---

## Appendix · items checked for and NOT IN SOURCE

* Any calibration, validation or measured-plant dataset behind the model — **NOT IN SOURCE**.
* Units or a derivation for the capacity constants `4.65 · 180` and `2.24 · 350` — **NOT IN SOURCE**.
* A separate coating/web speed for the dry route — **NOT IN SOURCE** (stated explicitly in the `drycoat` lead).
* A dry-route machinery total — **NOT IN SOURCE** (`"Not available from source"`).
* A `drymix` investment figure — **NOT IN SOURCE** (`"Not separately quoted in the source"`).
* Any distinction between cylindrical and prismatic *stations* — **NOT IN SOURCE**; they share one station list.
* Any persistence, export, or save of setpoints — **NOT IN SOURCE**; `S` is in-memory only,
  reset by `#resetBtn` to `DEFAULTS`.
* Any audio, video, or animation timeline beyond CSS `spin` / `bob` / `flowdash` / `puff` classes — **NOT IN SOURCE**.
