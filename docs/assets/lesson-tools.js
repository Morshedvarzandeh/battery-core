/* Battery Core — lesson calculators.
 *
 * Every calculator on a lesson page mirrors one tested function in
 * `battery_core`, term for term, including its input rules:
 *
 *   current_from_c_rate   I = C · Q        Q > 0, C ≥ 0
 *   c_rate_from_current   C = I / Q        Q > 0, I ≥ 0
 *   ideal_duration_hours  t = 1 / C        C > 0  (1/0 is undefined)
 *   nominal_energy_wh     E = Q · V        Q > 0, V > 0
 *   ficks_first_law_flux  J = −D · dc/dx   D ≥ 0, every value finite
 *
 * The HTML already contains the worked-example results, so a reader without
 * JavaScript sees a correct page. This file only makes the numbers respond.
 * Nothing is stored and nothing leaves the browser.
 */
(() => {
  "use strict";

  const $ = (selector, root = document) => root.querySelector(selector);

  const read = input => {
    const raw = String(input.value).trim();
    if (raw === "") return NaN;
    return Number(raw);
  };

  const trim = text => text.replace(/\.?0+$/, "");

  function fixed(value, digits = 2) {
    if (!Number.isFinite(value)) return "—";
    if (Math.abs(value) >= 1e5 || (value !== 0 && Math.abs(value) < 1e-3)) return sci(value);
    return trim(value.toFixed(digits));
  }

  const SUPER = { "-": "⁻", "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹" };

  function sci(value, digits = 2) {
    if (!Number.isFinite(value)) return "—";
    if (value === 0) return "0";
    const [mantissa, exponent] = value.toExponential(digits).split("e");
    const power = String(Number(exponent)).replace(/[-0-9]/g, ch => SUPER[ch]);
    return `${mantissa.replace("-", "−")} × 10${power}`;
  }

  function duration(hours) {
    if (!Number.isFinite(hours)) return "—";
    if (hours >= 1) return `${trim(hours.toFixed(2))} h`;
    const minutes = hours * 60;
    if (minutes >= 1) return `${trim(minutes.toFixed(1))} min`;
    return `${trim((minutes * 60).toFixed(1))} s`;
  }

  function rateLabel(rate) {
    if (rate > 0 && rate < 1) {
      const inverse = 1 / rate;
      if (Math.abs(inverse - Math.round(inverse)) < 1e-9) return `C/${Math.round(inverse)}`;
    }
    return `${trim(rate.toFixed(3))}C`;
  }

  function note(el, text, isError = false) {
    if (!el) return;
    el.textContent = text;
    if (isError) el.dataset.state = "error";
    else delete el.dataset.state;
  }

  /* ---- Lesson 2: current from C-rate -------------------------------------- */
  function forwardCalculator(root) {
    const cap = $("[name=capacity]", root);
    const rate = $("[name=c_rate]", root);
    const out = {
      current: $("[data-out=current]", root),
      hours: $("[data-out=duration]", root),
      label: $("[data-out=label]", root),
    };
    const msg = $(".calc-note", root);
    // The rate table sits in the lesson text above the calculator, not inside it.
    const table = document.querySelector("table[data-out=table]");

    function update() {
      const q = read(cap);
      const c = read(rate);
      if (!Number.isFinite(q) || q <= 0) {
        out.current.textContent = out.hours.textContent = out.label.textContent = "—";
        note(msg, "Nominal capacity must be a finite, positive number of ampere-hours.", true);
        return;
      }
      if (!Number.isFinite(c) || c < 0) {
        out.current.textContent = out.hours.textContent = out.label.textContent = "—";
        note(msg, "C-rate must be a finite number of zero or more.", true);
        return;
      }
      out.current.textContent = `${fixed(q * c)} A`;
      out.label.textContent = c === 0 ? "rest" : rateLabel(c);
      if (c === 0) {
        out.hours.textContent = "undefined";
        note(msg, "Zero current is a rest step: physical, but 1 / 0 has no duration.");
      } else {
        out.hours.textContent = duration(1 / c);
        note(msg, "Ideal duration assumes the full nominal capacity is available at this current — a real cell may reach its voltage limit sooner.");
      }
      if (table) {
        table.querySelectorAll("tr[data-rate]").forEach(row => {
          const r = Number(row.dataset.rate);
          row.querySelector("[data-cell=current]").textContent = `${fixed(q * r)} A`;
        });
        const capCell = table.querySelector("[data-out=table-capacity]");
        if (capCell) capCell.textContent = `${fixed(q)} Ah`;
      }
    }

    [cap, rate].forEach(el => el.addEventListener("input", update));
    update();
  }

  /* ---- Lesson 2: C-rate from current -------------------------------------- */
  function inverseCalculator(root) {
    const cap = $("[name=capacity]", root);
    const cur = $("[name=current]", root);
    const out = {
      rate: $("[data-out=c_rate]", root),
      hours: $("[data-out=duration]", root),
    };
    const msg = $(".calc-note", root);

    function update() {
      const q = read(cap);
      const i = read(cur);
      if (!Number.isFinite(q) || q <= 0) {
        out.rate.textContent = out.hours.textContent = "—";
        note(msg, "Nominal capacity must be a finite, positive number of ampere-hours.", true);
        return;
      }
      if (!Number.isFinite(i) || i < 0) {
        out.rate.textContent = out.hours.textContent = "—";
        note(msg, "Current is a magnitude here: a finite number of zero or more.", true);
        return;
      }
      const c = i / q;
      out.rate.textContent = `${fixed(c, 2)}C`;
      out.hours.textContent = c === 0 ? "undefined" : duration(1 / c);
      note(msg, c === 0
        ? "Zero current is a rest step: its C-rate is exactly 0."
        : "Check the datasheet discharge curve for the real duration at this current.");
    }

    [cap, cur].forEach(el => el.addEventListener("input", update));
    update();
  }

  /* ---- Lesson 2: nominal energy ------------------------------------------- */
  function energy(wh) {
    if (wh >= 1000) return `${fixed(wh / 1000, 2)} kWh`;
    return `${fixed(wh, 2)} Wh`;
  }

  function energyCalculator(root) {
    const cap = $("[name=capacity]", root);
    const volt = $("[name=voltage]", root);
    const count = $("[name=cells]", root);
    const out = {
      cell: $("[data-out=cell_energy]", root),
      total: $("[data-out=energy]", root),
    };
    const msg = $(".calc-note", root);

    function update() {
      const q = read(cap);
      const v = read(volt);
      const n = read(count);
      const blank = () => { out.cell.textContent = out.total.textContent = "—"; };
      if (!Number.isFinite(q) || q <= 0) {
        blank();
        note(msg, "Nominal capacity must be a finite, positive number of ampere-hours.", true);
        return;
      }
      if (!Number.isFinite(v) || v <= 0) {
        blank();
        note(msg, "Nominal voltage must be a finite, positive number of volts.", true);
        return;
      }
      if (!Number.isInteger(n) || n < 1) {
        blank();
        note(msg, "The number of cells must be a whole number, 1 or more.", true);
        return;
      }
      const e = q * v;
      out.cell.textContent = energy(e);
      out.total.textContent = energy(e * n);
      note(msg, "A rating: delivered energy is lower at high current, at low temperature and in an aged cell.");
    }

    [cap, volt, count].forEach(el => el.addEventListener("input", update));
    update();
  }

  /* ---- Fick's first law --------------------------------------------------- */
  function fickCalculator(root) {
    const d = $("[name=diffusivity]", root);
    const dc = $("[name=delta_c]", root);
    const dx = $("[name=delta_x_um]", root);
    const out = {
      gradient: $("[data-out=gradient]", root),
      flux: $("[data-out=flux]", root),
      direction: $("[data-out=direction]", root),
    };
    const msg = $(".calc-note", root);

    function update() {
      const D = read(d);
      const deltaC = read(dc);
      const deltaXum = read(dx);
      const blank = () => { out.gradient.textContent = out.flux.textContent = out.direction.textContent = "—"; };
      if (!Number.isFinite(D) || D < 0) {
        blank();
        note(msg, "The diffusion coefficient must be finite and non-negative.", true);
        return;
      }
      if (!Number.isFinite(deltaC) || !Number.isFinite(deltaXum) || deltaXum <= 0) {
        blank();
        note(msg, "Give a finite concentration change and a positive distance.", true);
        return;
      }
      const gradient = deltaC / (deltaXum * 1e-6);   // mol/m³ per m
      const flux = -D * gradient;
      out.gradient.textContent = `${sci(gradient)} mol/m⁴`;
      out.flux.textContent = `${sci(flux)} mol/(m²·s)`;
      out.direction.textContent = flux > 0 ? "toward +x" : flux < 0 ? "toward −x" : "no net flux";
      note(msg, "Diffusion always runs down the concentration gradient — the minus sign in J = −D dc/dx.");
    }

    [d, dc, dx].forEach(el => el.addEventListener("input", update));
    update();
  }

  const CALCULATORS = {
    "c-rate-forward": forwardCalculator,
    "c-rate-inverse": inverseCalculator,
    energy: energyCalculator,
    "fick-flux": fickCalculator,
  };

  document.querySelectorAll("[data-calc]").forEach(root => {
    const build = CALCULATORS[root.dataset.calc];
    if (build) build(root);
  });
})();
