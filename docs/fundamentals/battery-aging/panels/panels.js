/* ==========================================================================
   Shared library for every embedded panel.
   The model here mirrors, term for term, the Python in the notebook cells.
   ========================================================================== */
"use strict";
const NS = "http://www.w3.org/2000/svg";
const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const fix = (v, n = 1) => v.toFixed(n);
const minus = s => String(s).replace("-", "−");

/* Tell the embedding frame how tall this panel actually is. srcdoc frames are
   same-origin with the notebook, so the panel can size itself and nothing needs
   to run in the notebook document. */
function fit() {
  try {
    const f = window.frameElement;
    if (f) f.style.height = Math.ceil(document.body.scrollHeight + 2) + "px";
  } catch (e) {}
}
addEventListener("load", () => requestAnimationFrame(fit));
addEventListener("resize", () => requestAnimationFrame(fit));

/* deterministic pseudo-random, so a drawing never jitters between updates */
function rng(seed) {
  let s = seed;
  return () => (s = (s * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
}

/* ---------- theme: follow the OS, then follow the notebook's toggle -------- */
(function theme() {
  const root = document.documentElement;
  root.dataset.theme = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  addEventListener("message", ev => {
    if (ev.data && ev.data.agingTheme) root.dataset.theme = ev.data.agingTheme;
  });
  const adopt = () => { try { if (parent.__agingTheme) root.dataset.theme = parent.__agingTheme; } catch (e) {} };
  adopt();
  addEventListener("load", adopt);
  addEventListener("message", () => requestAnimationFrame(fit));
})();

/* ==========================================================================
   Physics — one activation energy, one rate law, repeated
   ========================================================================== */
const R_GAS = 8.314;
const arrh = (Tc, Ea) => Math.exp(Ea / R_GAS * (1 / 298.15 - 1 / (Tc + 273.15)));

/* Will it plate? A probability, so it saturates at 1. */
function platingRisk(Tc, cRate) {
  if (cRate <= 0) return 0;
  const d = cRate / arrh(Tc, 35000);
  return clamp((d - 0.35) / (d + 1.0));
}
/* How much plates? An excess, so it does not saturate — the colder the cell,
   the further the charging current outruns what the graphite can absorb. */
function platingDrive(Tc, cRate) {
  if (cRate <= 0) return 0;
  return Math.max(0, cRate / arrh(Tc, 35000) - 0.6);
}

const DUTY = {
  storage:    { label: "Shelf storage",      cRate: 0.0, cyc: 0.02, dod: 0.0, gasMul: 1.0, corMul: 1.0, temp: 25,
                note: "Nothing is being asked of the cell — and it ages anyway." },
  hot:        { label: "Hot operation",      cRate: 0.7, cyc: 0.60, dod: 0.5, gasMul: 1.4, corMul: 1.5, temp: 45,
                note: "Every chemical side reaction runs faster; roughly double per +10 °C." },
  cold:       { label: "Cold / fast charge", cRate: 2.5, cyc: 0.80, dod: 0.6, gasMul: 1.0, corMul: 1.0, temp: 0,
                note: "Lithium arrives faster than graphite can take it in, and plates as metal." },
  cycling:    { label: "Deep cycling",       cRate: 1.0, cyc: 1.00, dod: 0.9, gasMul: 1.1, corMul: 1.1, temp: 30,
                note: "Particles swell and shrink thousands of times — mechanical fatigue." },
  overcharge: { label: "Overcharge",         cRate: 1.0, cyc: 0.50, dod: 0.5, gasMul: 4.0, corMul: 2.6, temp: 40,
                note: "Past the stability window the electrolyte decomposes and gases." },
};

const CAP_W = { sei: 0.30, dendrite: 0.34, cracking: 0.26, gas: 0.10, crystal: 0.06 };
const IMP_W = { sei: 0.55, corrosion: 1.60, cracking: 1.30, crystal: 0.90, gas: 0.25 };
const SD_W  = { dendrite: 3.40, gas: 1.10, crystal: 0.50 };

function severities(Tc, years, d) {
  const t = Math.max(years, 0);
  return {
    sei:       clamp(0.160 * Math.sqrt(t * arrh(Tc, 50000)) * (1 + 0.30 * d.cyc)),
    corrosion: clamp(0.032 * t * arrh(Tc, 45000) * d.corMul),
    gas:       clamp(0.013 * t * arrh(Tc, 62000) * d.gasMul),
    crystal:   clamp(0.100 * Math.pow(t * (0.25 + d.cyc), 0.6)),
    cracking:  clamp(0.105 * Math.pow(t * d.cyc * (0.35 + d.dod), 0.7)),
    dendrite:  clamp(0.115 * platingDrive(Tc, d.cRate) * Math.sqrt(t * (0.15 + d.cyc) / 10)),
  };
}
const sum = (w, s) => Object.keys(w).reduce((a, k) => a + w[k] * s[k], 0);
function effects(s) {
  return {
    capacity:  1 - clamp(sum(CAP_W, s), 0, 0.75),
    impedance: 1 + sum(IMP_W, s),
    selfDisch: 1.8 * (1 + sum(SD_W, s)),
  };
}
function yearsTo80(Tc, d) {
  for (let t = 0.1; t <= 30.05; t += 0.1) if (effects(severities(Tc, t, d)).capacity <= 0.80) return t;
  return null;
}

/* per-mechanism models used by the focused panels */
const SEI_D0 = 12.0, LI_PER_NM = 0.0043;
const seiThickness = (t, Tc) => SEI_D0 * Math.sqrt(Math.max(t, 0) * arrh(Tc, 50000));
const seiCapacity  = (t, Tc) => clamp(1 - LI_PER_NM * seiThickness(t, Tc));

const GAS_G0 = 1.20, GAS_R = 0.90, SWELL = 5.0, VENT = 14.0;
const gasVolume = (t, Tc, oc) =>
  GAS_G0 * arrh(Tc, 62000) * oc / GAS_R * (1 - Math.exp(-GAS_R * Math.max(t, 0)));

const OCV = 3.7, R0 = 0.030, V_CUT = 2.8;
const areaRatio = (n, k = 1) => 1 / (1 + 0.0016 * k * Math.pow(Math.max(n, 0), 0.85));

const mechDamage    = (n, dod) => clamp(0.0095 * Math.pow(Math.max(n, 0) * Math.pow(dod, 1.6), 0.6));
const mechCapacity  = (n, dod) => 1 - 0.45 * mechDamage(n, dod);
function cyclesTo80(dod) {
  for (let n = 10; n <= 40000; n += 10) if (mechCapacity(n, dod) <= 0.80) return n;
  return NaN;
}
const dendritePenetration = (Tc, c, n) => clamp(0.085 * platingDrive(Tc, c) * Math.sqrt(Math.max(n, 0) / 400));
const selfDischargeOf = pen => 1.8 * (1 + 3.4 * Math.pow(pen, 1.6)) + (pen >= 0.995 ? 28 : 0);

const MECH = {
  corrosion: { n: "01", cls: "m-corrosion", title: "Corrosion",
    where: "Collectors, active and inactive materials", feeds: "Impedance ↑", driver: "Temperature",
    body: "Deterioration by chemical interaction with the environment — a catch-all for the undesirable side reactions inside a cell: solvent attacking the current collectors, solvent reacting with electrode materials. The products can themselves be corrosive, so it feeds itself.",
    result: "Less conductive area and poorer contact → impedance rise, so power fade.",
    caveat: "A catch-all term — not every chemistry suffers every one of these reactions. The aluminium collector is shown here as one example." },
  sei: { n: "02", cls: "m-sei", title: "Passivation — the SEI film",
    where: "Graphite particle surfaces", feeds: "Capacity ↓", driver: "Temperature, time",
    body: "The solvent is not stable at the voltages inside a lithium-ion cell, so it reacts with graphite and leaves a film of reaction products on the particle surfaces. That film protects the graphite and greatly slows the reaction — but it never stops growing, and every repair consumes cyclable lithium.",
    result: "Lithium inventory consumed → capacity fade; a thicker film also adds impedance.",
    caveat: "A special case of corrosion, on low-potential negative electrodes — graphite, and also silicon and lithium metal." },
  gas: { n: "03", cls: "m-gas", title: "Gas generation",
    where: "Pores, then the cell's free volume", feeds: "Capacity ↓, safety", driver: "Temperature, overcharge",
    body: "Gas forms on charge. In aqueous cells it can ideally recombine on discharge; in lithium-ion cells it comes mainly from irreversible electrolyte decomposition. If it escapes through a breach, that capacity is gone. If it cannot escape, pressure builds until the cell ruptures — unless a vent opens first. In some chemistries the gas is explosive.",
    result: "Permanent capacity loss, swelling, venting, and a real safety hazard under abuse.",
    caveat: "Gas species and rates depend on chemistry, state of charge, temperature and abuse history." },
  crystal: { n: "04", cls: "m-crystal", title: "Crystal formation",
    where: "Electrode surfaces", feeds: "Impedance ↑ → power fade", driver: "Cycling",
    body: "Material removed from an electrode on discharge does not return to the same place on recharge. It builds up as crystal structures on the electrode surface instead, and those deposits cut the effective surface area the reaction has to work with.",
    result: "Less active area → higher resistance → the cell can no longer deliver high power.",
    caveat: "A very general redox-cell mechanism; the morphology differs enormously between chemistries." },
  dendrite: { n: "05", cls: "m-dendrite", title: "Dendrites (lithium plating)",
    where: "From the negative electrode through the separator", feeds: "Self-discharge ↑, shorts", driver: "Cold charging, high current",
    body: "Crystal growth that turns into a safety problem: metallic, tree-like structures growing from the electrode surface. Low temperature or overcurrent during charging deposits lithium as metal instead of inserting it, and those deposits can grow right through the separator.",
    result: "Rising self-discharge, then an internal short; the deposits also lock up lithium.",
    caveat: "A risk condition rather than normal operation — but it is exactly what cold fast-charging invites." },
  cracking: { n: "06", cls: "m-cracking", title: "Volume change and cracking",
    where: "Inside particles, binder, conductive additives", feeds: "Capacity ↓ and impedance ↑", driver: "Deep cycling",
    body: "Intercalation changes the volume of the host material. Repeated strain cracks the active particles, collapses the structure of some positive-electrode materials, and tears the binder and conductive additives that keep particles electrically connected.",
    result: "Active material and conductive pathways lost → capacity fade and impedance rise together.",
    caveat: "Severity depends strongly on chemistry, particle size and electrode design." },
};
const ORDER = ["corrosion", "sei", "gas", "crystal", "dendrite", "cracking"];

/* ==========================================================================
   Minimal plotting helpers — SVG strings, no dependencies
   ========================================================================== */
function plot(w, h, m, xd, yd) {
  const iw = w - m.l - m.r, ih = h - m.t - m.b, parts = [];
  const o = {
    w, h, m, iw, ih,
    x: v => m.l + iw * (v - xd[0]) / (xd[1] - xd[0]),
    y: v => m.t + ih - ih * (v - yd[0]) / (yd[1] - yd[0]),
    add(s) { parts.push(s); return o; },
    gridY(vals, fmt = String) {
      vals.forEach(v => o.add(`<line class="gridline" x1="${m.l}" x2="${w - m.r}" y1="${o.y(v).toFixed(1)}" y2="${o.y(v).toFixed(1)}"/>`)
                    .add(`<text class="axis-label" x="${m.l - 6}" y="${(o.y(v) + 3.5).toFixed(1)}" text-anchor="end">${fmt(v)}</text>`));
      return o;
    },
    ticksX(vals, fmt = String) {
      vals.forEach(v => o.add(`<text class="axis-label" x="${o.x(v).toFixed(1)}" y="${(m.t + ih + 15).toFixed(1)}" text-anchor="middle">${fmt(v)}</text>`));
      return o;
    },
    titleX(s) { return o.add(`<text class="axis-title" x="${(m.l + iw / 2).toFixed(1)}" y="${(m.t + ih + 30).toFixed(1)}" text-anchor="middle">${s}</text>`); },
    line(xs, ys, cls) {
      const d = xs.map((v, i) => `${i ? "L" : "M"}${o.x(v).toFixed(1)},${o.y(ys[i]).toFixed(1)}`).join(" ");
      return o.add(`<path class="series ${cls}" d="${d}"/>`);
    },
    dot(x, y, fill) { return o.add(`<circle class="dot" cx="${o.x(x).toFixed(1)}" cy="${o.y(y).toFixed(1)}" r="4.5" fill="${fill}"/>`); },
    baseline() { return o.add(`<line class="baseline" x1="${m.l}" x2="${w - m.r}" y1="${m.t + ih}" y2="${m.t + ih}"/>`); },
    svg(aria) { return `<svg class="fig" viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="${aria}">${parts.join("")}</svg>`; },
  };
  return o;
}

function pathOf(P, xs, ys) {
  return xs.map((v, i) => `${i ? "L" : "M"}${P.x(v).toFixed(1)},${P.y(ys[i]).toFixed(1)}`).join(" ");
}

function series(n, f) { return Array.from({ length: n }, (_, i) => f(i / (n - 1), i)); }

function legend(items) {
  return items.map(i => `<span class="legend-item"><i class="swatch" style="--c: ${i.c}"></i>${i.label}</span>`).join("");
}

function bind(ids, fn) {
  ids.forEach(id => {
    const n = document.getElementById(id);
    n.addEventListener("input", fn);
    n.addEventListener("change", fn);
  });
}
function segmented(sel, fn) {
  $$(sel + " button").forEach(b => b.addEventListener("click", () => {
    $$(sel + " button").forEach(o => o.setAttribute("aria-pressed", String(o === b)));
    fn(b.dataset.v, b);
  }));
}

/* Battery Core website: the course is dark-only, so pin every panel to the
   dark theme instead of following the operating system. */
document.documentElement.dataset.theme = "dark";
