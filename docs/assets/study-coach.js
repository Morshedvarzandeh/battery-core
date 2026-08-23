/* Battery Core — Chapter 1 study coach.
 *
 * The chapter already asks a checkpoint question after every part. Reading a
 * question and thinking "yes, roughly" is not the same as answering it, so
 * this turns each one into a loop: answer first, then find out where you were.
 *
 * It runs entirely in the browser. No network, no account, no key. Progress
 * lives in this browser's localStorage, and clearing site data clears it.
 *
 * Two kinds of question, because two kinds are honestly possible offline:
 *
 *   Checked outright — numeric drills, multiple choice, select-all, and
 *   ordering. The answer space is closed, so the coach marks it exactly and
 *   says why a wrong option is wrong. Every number comes from the same
 *   definitions the tested Python implements.
 *
 *   Self-checked — the questions whose answer is an explanation. The coach
 *   never claims to mark an answer of that kind. It cannot read prose, and the
 *   only offline way to fake it is keyword matching, which grades vocabulary
 *   rather than understanding: "the separator does not block electrons"
 *   contains every right word and is wrong, while a correct answer in
 *   different words scores nothing. A confidently wrong grade is worse than no
 *   grade, because the learner cannot tell it happened. So it shows what a
 *   complete answer covers and lets the learner mark their own against it.
 *
 * An optional AI tutor can be attached for free-form follow-up questions; see
 * `assets/README.md` § An AI tutor. It is off unless `data-tutor-endpoint` on
 * the mount element is set to a URL, so the page ships self-contained.
 */

(function () {
  "use strict";

  var STORAGE_KEY = "battery-core-chapter-1-coach";

  /* Physical constants, matching `battery_core.aging` exactly. */
  var MOLAR_GAS_CONSTANT = 8.31446261815324;
  var ABSOLUTE_ZERO_C = -273.15;

  function pick(list) {
    return list[Math.floor(Math.random() * list.length)];
  }

  function formatNumber(value) {
    return Number(value.toFixed(3)).toString();
  }

  /* The drills. Each generates fresh numbers, so the answer cannot be
     remembered from last time, and each mirrors one tested function:
     `current_from_c_rate`, `ideal_duration_hours`, `arrhenius_factor`, and
     `parabolic_film_thickness`. */
  var DRILLS = {
    cRateCurrent: {
      label: "Constant current, in amperes",
      tolerance: 0.01,
      generate: function () {
        var capacity = pick([1.5, 2.2, 3.0, 4.5, 5.0, 12, 20, 50, 100]);
        var rate = pick([0.2, 0.5, 1, 2, 3, 5]);
        return { capacity: capacity, rate: rate, current: capacity * rate };
      },
      prompt: function (d) {
        return (
          "A cell with a nominal capacity of " +
          formatNumber(d.capacity) +
          " Ah is discharged at " +
          formatNumber(d.rate) +
          "C. What constant current does that definition give?"
        );
      },
      answer: function (d) {
        return d.current;
      },
      working: function (d) {
        return [
          "I = Q × C = " +
            formatNumber(d.capacity) +
            " Ah × " +
            formatNumber(d.rate) +
            " h⁻¹ = " +
            formatNumber(d.current) +
            " A",
          "The units carry the argument: Ah × h⁻¹ leaves amperes.",
        ];
      },
    },

    idealDuration: {
      label: "Ideal duration, in hours",
      tolerance: 0.01,
      generate: function () {
        var rate = pick([0.1, 0.2, 0.25, 0.5, 2, 4, 5]);
        return { rate: rate, hours: 1 / rate };
      },
      prompt: function (d) {
        return (
          "A cell is discharged at " +
          formatNumber(d.rate) +
          "C. How long does the ideal definition say a full nominal capacity lasts?"
        );
      },
      answer: function (d) {
        return d.hours;
      },
      working: function (d) {
        return [
          "t = 1 / C = 1 / " + formatNumber(d.rate) + " = " + formatNumber(d.hours) + " h",
          "That is a definition, not a runtime. A real cell stops at a cutoff voltage.",
        ];
      },
    },

    arrhenius: {
      label: "Rate ratio, dimensionless",
      tolerance: 0.02,
      generate: function () {
        var temperature = pick([35, 45, 55, 60]);
        var activation = pick([40000, 50000, 60000]);
        var reference = 25;
        var kelvin = temperature - ABSOLUTE_ZERO_C;
        var referenceKelvin = reference - ABSOLUTE_ZERO_C;
        return {
          temperature: temperature,
          reference: reference,
          activation: activation,
          factor: Math.exp(
            (activation / MOLAR_GAS_CONSTANT) * (1 / referenceKelvin - 1 / kelvin)
          ),
        };
      },
      prompt: function (d) {
        return (
          "A thermally activated ageing process has an activation energy of " +
          d.activation / 1000 +
          " kJ/mol. How many times faster does it run at " +
          d.temperature +
          " °C than at " +
          d.reference +
          " °C?"
        );
      },
      answer: function (d) {
        return d.factor;
      },
      working: function (d) {
        return [
          "k(T) / k(T_ref) = exp[(Ea / R) × (1/T_ref − 1/T)], both temperatures in kelvin",
          "T = " +
            formatNumber(d.temperature - ABSOLUTE_ZERO_C) +
            " K, T_ref = " +
            formatNumber(d.reference - ABSOLUTE_ZERO_C) +
            " K, R = 8.314 J/(mol·K)",
          "= " + formatNumber(d.factor) + " times faster",
          "Near 50 kJ/mol this is the familiar rule of thumb: roughly double per 10 °C.",
        ];
      },
    },

    filmGrowth: {
      label: "Film thickness, in nanometres",
      tolerance: 0.01,
      generate: function () {
        var thickness = pick([8, 12, 15, 20]);
        var multiple = pick([4, 9, 16, 25]);
        var referenceTime = pick([50, 100, 200]);
        return {
          thickness: thickness,
          multiple: multiple,
          referenceTime: referenceTime,
          elapsed: referenceTime * multiple,
          result: thickness * Math.sqrt(multiple),
        };
      },
      prompt: function (d) {
        return (
          "A passivating film is " +
          formatNumber(d.thickness) +
          " nm thick after " +
          d.referenceTime +
          " days. Under the same conditions, how thick is it after " +
          d.elapsed +
          " days?"
        );
      },
      answer: function (d) {
        return d.result;
      },
      working: function (d) {
        return [
          "δ(t) = δ_ref × √(t / t_ref) = " +
            formatNumber(d.thickness) +
            " nm × √" +
            d.multiple +
            " = " +
            formatNumber(d.result) +
            " nm",
          "The film is its own diffusion barrier, so growth is parabolic, not linear.",
          "Quadrupling the time doubles the thickness — it does not quadruple it.",
        ];
      },
    },
  };

  /* The question bank. Model answers and distractors are grounded in the
     modules and in the tested Python, and they keep the course's own line
     between an exact definition and a prediction. */
  var QUESTIONS = [
    {
      id: "p01-paths",
      group: "part",
      tier: "core",
      part: "Part 01",
      module: "../fundamentals/cell-anatomy-workbench/",
      moduleLabel: "Part 01 · Cell anatomy workbench",
      question:
        "Why do electrons travel the external circuit while lithium ions move inside the cell?",
      hints: [
        "Ask what each of the two internal materials — separator and electrolyte — will and will not carry.",
        "If both charge carriers could take the same path, what would the cell be doing instead of powering the load?",
      ],
      points: [
        "The electrolyte conducts lithium ions but not electrons.",
        "The separator is an electronic insulator, soaked in electrolyte, so it passes ions and blocks electrons.",
        "That leaves the external circuit as the only path electrons have between the electrodes.",
        "The detour through the load is the useful work: forcing electrons the long way round is what the cell is for.",
        "Electrons crossing inside would be an internal short — self-discharge and heat, no work delivered.",
      ],
    },
    {
      id: "p01-separator",
      group: "part",
      tier: "core",
      type: "choice",
      part: "Part 01",
      module: "../fundamentals/cell-anatomy-workbench/",
      moduleLabel: "Part 01 · Cell anatomy workbench",
      question: "Which statement is true of the separator?",
      hints: ["Two currencies cross a cell. Ask which one the separator is there to stop."],
      options: [
        {
          text: "It passes lithium ions and blocks electrons.",
          correct: true,
          why: "Yes. It is an electronic insulator whose pores are soaked in electrolyte, so ions pass and electrons cannot.",
        },
        {
          text: "It passes electrons and blocks lithium ions.",
          why: "That is the reverse. A separator carrying electrons would short the cell internally.",
        },
        {
          text: "It blocks both, and the ions travel round the external circuit instead.",
          why: "Ions never leave the cell. Only electrons take the external circuit — that separation is the whole point.",
        },
        {
          text: "It passes both, which is what lets current flow.",
          why: "Current flows because the two carriers are forced apart. If the separator passed electrons, the cell would self-discharge as heat.",
        },
      ],
    },
    {
      id: "p01b-pore-electrolyte",
      group: "part",
      tier: "deeper",
      part: "Part 01B",
      module: "../fundamentals/lithium-ion-cell-architecture/",
      moduleLabel: "Part 01B · Lithium-ion cell architecture",
      question:
        "Electrolyte fills the pores of both electrodes. Why is it not a sixth structural layer?",
      hints: [
        "What does it mean for something to be a layer in a left-to-right stack?",
        "Where in the stack would you place it — and how many places would you have to place it at once?",
      ],
      points: [
        "The five layers are structural: negative collector, negative composite electrode, separator, positive composite electrode, positive collector.",
        "A layer has one position in the left-to-right order and its own thickness in the stack.",
        "The electrolyte has neither: it is a phase filling pore space inside layers that already exist.",
        "It is present in the negative electrode, the separator, and the positive electrode simultaneously.",
        "Calling it layer six would imply it occupies its own slice of the stack thickness, which it does not.",
      ],
    },
    {
      id: "p02-drill",
      group: "part",
      tier: "core",
      type: "drill",
      drill: "cRateCurrent",
      part: "Part 02",
      module:
        "https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/02_capacity_and_c_rate.ipynb",
      moduleLabel: "Part 02 · Nominal capacity and C-rate",
      question: "Calculate the constant current for this cell and rate.",
      hints: [
        "Current is nominal capacity multiplied by C-rate, with capacity in ampere-hours and C-rate in reciprocal hours.",
        "The units do the work: Ah × h⁻¹ = A.",
      ],
      note:
        "This is the exact definition the tested Python implements. It is not a runtime prediction — see the runtime question.",
    },
    {
      id: "p02-duration",
      group: "part",
      tier: "core",
      type: "drill",
      drill: "idealDuration",
      part: "Part 02",
      module:
        "https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/02_capacity_and_c_rate.ipynb",
      moduleLabel: "Part 02 · Nominal capacity and C-rate",
      question: "Calculate the ideal duration at this rate.",
      hints: ["The ideal duration is the reciprocal of the C-rate, in hours."],
      note: "Exact by definition, and still not what a real cell will do.",
    },
    {
      id: "p02-real-runtime",
      group: "part",
      tier: "core",
      part: "Part 02",
      module:
        "https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/02_capacity_and_c_rate.ipynb",
      moduleLabel: "Part 02 · Nominal capacity and C-rate",
      question:
        "Ideal duration is 1 / C-rate. Why will a real cell usually run for less than that?",
      hints: [
        "What actually makes a real discharge stop? It is not that the nominal charge has been counted out.",
        "Think about what changes as you raise the current.",
      ],
      points: [
        "t = 1 / C is definitional, not a prediction: it says how long a full nominal capacity lasts at that rate, nothing more.",
        "A real discharge ends at a cutoff voltage, not when the nominal charge has passed.",
        "Usable capacity falls as rate rises, through ohmic drop, polarization, and diffusion limits.",
        "Temperature shifts both usable capacity and impedance, so the same cell gives a different runtime cold.",
        "An aged cell delivers less than nominal in the first place.",
      ],
      note:
        "The course keeps these apart deliberately: the formula is exact, the runtime is a prediction that needs a validated cell model.",
    },
    {
      id: "p03-order",
      group: "part",
      tier: "core",
      type: "order",
      part: "Part 03",
      module: "../fundamentals/battery-production/",
      moduleLabel: "Part 03 · Lithium-ion battery production",
      question: "Put the conventional electrode and cell route into process order.",
      hints: [
        "The electrode is finished as a coated, dried, densified web before anything is assembled.",
        "The electrolyte goes in after the stack exists, not before.",
      ],
      items: [
        "Mixing the slurry",
        "Coating the foil",
        "Drying the coating",
        "Calendering to porosity",
        "Stacking or winding",
        "Electrolyte filling",
        "Formation",
      ],
      note:
        "This is the wet route. The dry-electrode route replaces coating and drying with two dry stages and no process solvent.",
    },
    {
      id: "p03-upstream-downstream",
      group: "part",
      tier: "core",
      part: "Part 03",
      module: "../fundamentals/battery-production/",
      moduleLabel: "Part 03 · Lithium-ion battery production",
      question:
        "Name one upstream process change and follow it to a downstream cell-quality signal.",
      hints: [
        "Pick a process with a number you can turn up or down — a coating weight, a line force, a drying rate.",
        "A complete answer has three links, not two: process change, electrode property, measurable signal.",
      ],
      points: [
        "The chain has three links: a process window changes an electrode property, which changes electrochemical behaviour, which shows up as a measured signal at end of line.",
        "Coating: areal mass loading sets areal capacity, which shows up in formation and in final capacity grading.",
        "Calendering: line force sets porosity, which changes electrolyte wetting and shows up as formation time and cell impedance.",
        "Drying: too fast a rate drives binder migration, which weakens adhesion and shows up as cycle life.",
        "Naming the first and last link without the middle one is describing a correlation, not a mechanism.",
      ],
    },
    {
      id: "p03b-step",
      group: "part",
      tier: "deeper",
      type: "choice",
      part: "Part 03B",
      module: "../fundamentals/solid-state-production/",
      moduleLabel: "Part 03B · All-solid-state cell production",
      question: "Moving to an all-solid-state route, which process step disappears?",
      hints: ["Ask which step exists only because the electrolyte arrives as a liquid."],
      options: [
        {
          text: "Electrolyte filling and wetting",
          correct: true,
          why: "Yes. The electrolyte is already in the stack, so there is nothing to inject and no pores to wet.",
        },
        {
          text: "Calendering or densification",
          why: "The opposite: contact must now be made mechanically, so densification matters more, not less.",
        },
        {
          text: "Formation",
          why: "Formation still happens. Its conditions change, but the step does not disappear.",
        },
        {
          text: "Mixing",
          why: "Electrode materials still have to be prepared, whether as a slurry or a dry powder.",
        },
      ],
    },
    {
      id: "p03b-solid-electrolyte",
      group: "part",
      tier: "deeper",
      part: "Part 03B",
      module: "../fundamentals/solid-state-production/",
      moduleLabel: "Part 03B · All-solid-state cell production",
      question:
        "Why does choosing a solid electrolyte change which machines the line needs, rather than just swapping one material for another?",
      hints: [
        "When does a liquid electrolyte enter the cell, and when must a solid one?",
        "A liquid wets the pores by itself. What has to create contact when nothing flows?",
      ],
      points: [
        "A liquid electrolyte is filled in after assembly; a solid one is part of the stack and must be formed and densified during manufacture.",
        "The filling and wetting steps disappear, and layer-forming plus densification steps appear in their place.",
        "Interfacial contact must be made mechanically — stack pressure, calendering, sintering — because nothing flows into the pores.",
        "The family decides the equipment: oxides need high-temperature sintering, sulfides need a tightly controlled dry or inert atmosphere, polymers need heat and pressure.",
        "So the unit operations themselves change; the same line with a different drum would not build the cell.",
      ],
    },
    {
      id: "p04-impedance",
      group: "part",
      tier: "core",
      type: "multi",
      part: "Part 04",
      module:
        "https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/04_battery_aging.ipynb",
      moduleLabel: "Part 04 · Battery aging",
      question: "Select every symptom of impedance rise rather than capacity fade.",
      hints: [
        "One of the two costs you stored charge. The other costs you voltage while the charge is still there.",
        "Ask which measurement would move: an ampere-hour count, or a voltage under load.",
      ],
      options: [
        {
          text: "The terminal voltage sags further under the same load current.",
          correct: true,
          why: "Impedance rise. More internal resistance means a larger IR drop at the same current.",
        },
        {
          text: "A full discharge yields fewer ampere-hours at a defined rate and temperature.",
          why: "Capacity fade. The charge itself is gone, not just the voltage under load.",
        },
        {
          text: "Measured DC resistance or EIS resistance increases.",
          correct: true,
          why: "Impedance rise, measured directly.",
        },
        {
          text: "Cyclable lithium is consumed by SEI growth.",
          why: "Capacity fade — that lithium is no longer available to shuttle, so stored charge drops.",
        },
        {
          text: "The cell runs hotter for the same current.",
          correct: true,
          why: "Impedance rise. Ohmic loss goes as I²R, so more resistance means more heat at the same current.",
        },
      ],
      note:
        "They move independently: a cell can lose power capability while still holding most of its capacity, or the reverse.",
    },
    {
      id: "p04-arrhenius",
      group: "part",
      tier: "core",
      type: "drill",
      drill: "arrhenius",
      part: "Part 04",
      module:
        "https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/04_battery_aging.ipynb",
      moduleLabel: "Part 04 · Battery aging",
      question: "How much does temperature accelerate this process?",
      hints: [
        "Convert both temperatures to kelvin first — the relation is not linear in Celsius.",
        "k(T)/k(T_ref) = exp[(Ea/R) × (1/T_ref − 1/T)], with R = 8.314 J/(mol·K).",
      ],
      note:
        "`battery_core.aging.arrhenius_factor` implements exactly this. It takes an activation energy as an input and supplies no chemistry-specific constants, so it is a rate law, not a prediction about any particular cell.",
    },
    {
      id: "p04-film",
      group: "part",
      tier: "core",
      type: "drill",
      drill: "filmGrowth",
      part: "Part 04",
      module:
        "https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/04_battery_aging.ipynb",
      moduleLabel: "Part 04 · Battery aging",
      question: "How thick is the film after this much time?",
      hints: [
        "A growing film is its own diffusion barrier, so it does not grow linearly.",
        "δ(t) = δ_ref × √(t / t_ref).",
      ],
      note:
        "This is why ageing slows down rather than running away: quadrupling the time only doubles the film.",
    },
    {
      id: "p04-fade-vs-impedance",
      group: "part",
      tier: "core",
      part: "Part 04",
      module:
        "https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/04_battery_aging.ipynb",
      moduleLabel: "Part 04 · Battery aging",
      question:
        "Distinguish capacity fade from impedance rise, and name a condition that accelerates each.",
      hints: [
        "One of them costs you stored charge. The other costs you voltage under load.",
        "Ask what each one does to a measurement: an ampere-hour count, or a voltage drop.",
      ],
      points: [
        "Capacity fade is loss of deliverable charge, measured as fewer ampere-hours at a defined rate and temperature.",
        "Impedance rise is increased internal resistance, measured as a larger voltage drop under load, or a higher DC resistance or EIS resistance.",
        "They are independent: a cell can lose power capability while still holding most of its capacity, or the reverse.",
        "High temperature accelerates both, because both are chemistry — that is the Arrhenius factor in `battery_core.aging`.",
        "Storage at high state of charge drives SEI growth and so capacity fade; film growth thickening over time drives impedance rise, following a parabolic law where four times the time gives twice the film.",
      ],
      note:
        "`battery_core.aging` implements those two rate laws and supplies no chemistry-specific constants. It does not predict any particular cell's fade.",
    },
    {
      id: "ch-trace",
      group: "chapter",
      tier: "core",
      part: "Checkpoint 01",
      module: "../fundamentals/cell-anatomy-workbench/",
      moduleLabel: "Chapter checkpoint · Trace",
      question:
        "Trace the electron path and the lithium-ion path through a cell, first on discharge and then on charge.",
      hints: [
        "Start at one electrode and say what leaves it, in both currencies at once: ions and electrons.",
        "Then say what changes when an external source drives the process backwards.",
      ],
      points: [
        "Discharge: lithium leaves the negative electrode host, releasing Li⁺ into the electrolyte and an electron into the negative collector.",
        "Those electrons cross the external circuit through the load to the positive collector.",
        "Those Li⁺ cross the electrolyte and separator and intercalate into the positive electrode, so charge stays balanced at each electrode.",
        "Charge: an external source drives the reverse — Li⁺ returns to the negative electrode and electrons go the other way round the circuit.",
        "Polarity labels stay fixed; anode and cathode are reaction roles and swap between discharge and charge.",
      ],
    },
    {
      id: "ch-compare",
      group: "chapter",
      tier: "core",
      part: "Checkpoint 03",
      module: "../fundamentals/solid-state-production/",
      moduleLabel: "Chapter checkpoint · Compare",
      question:
        "Compare a conventional lithium-ion route with one solid-state route, and say which process steps actually change.",
      hints: [
        "List the conventional route in order first — you cannot say what changed without it.",
        "Pick one electrolyte family and commit to it. “Solid-state” in general has no single answer.",
      ],
      points: [
        "Conventional order: mixing, coating, drying, calendering, slitting, stacking or winding, assembly, electrolyte filling, sealing, formation, aging, grading.",
        "Electrolyte filling and wetting drop out, because the electrolyte is already in the stack.",
        "Layer forming plus a densification step — sintering, pressing, or calendering under load — appear.",
        "Atmosphere control tightens where the chosen electrolyte demands it, most sharply for sulfides.",
        "Formation and aging still exist, but under different conditions, so end-of-line testing is not carried over unchanged.",
      ],
      note:
        "A complete answer names which family it is comparing. Oxide, sulfide, halide, and polymer routes change different steps.",
    },
    {
      id: "ch-connect",
      group: "chapter",
      tier: "core",
      part: "Checkpoint 04",
      module:
        "https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/04_battery_aging.ipynb",
      moduleLabel: "Chapter checkpoint · Connect",
      question:
        "Connect an operating condition to a degradation mechanism, and then to a signal you could actually measure.",
      hints: [
        "Three links again. A condition and a symptom with nothing between them is not an explanation.",
        "Pick a condition you could set on a test bench: a temperature, a state of charge, a charging rate.",
      ],
      points: [
        "Condition: for example storage at 45 °C at high state of charge.",
        "Mechanism: accelerated SEI growth consuming cyclable lithium, with the film thickening as the square root of time.",
        "Signal: capacity fade measured at a fixed rate and temperature, with some impedance rise alongside it.",
        "A second chain worth having: fast charging at low temperature drives lithium plating, which shows up as sudden capacity loss, impedance rise, and a safety concern.",
        "The middle link is the one that makes it an explanation rather than a correlation.",
      ],
    },
  ];

  function loadState() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      var parsed = raw ? JSON.parse(raw) : null;
      if (parsed && parsed.results && typeof parsed.results === "object") {
        return parsed;
      }
    } catch (error) {
      /* A browser with site data blocked is a browser that studies without
         saved progress, not one that gets a broken page. */
    }
    return { version: 2, results: {} };
  }

  function saveState(state) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      return true;
    } catch (error) {
      return false;
    }
  }

  function element(tag, className, text) {
    var node = document.createElement(tag);
    if (className) {
      node.className = className;
    }
    if (text !== undefined) {
      node.textContent = text;
    }
    return node;
  }

  /* Shuffle, never returning the input order — an ordering question that opens
     already solved teaches nothing. */
  function shuffled(list) {
    if (list.length < 2) {
      return list.slice();
    }
    var copy;
    var attempts = 0;
    do {
      copy = list.slice();
      for (var i = copy.length - 1; i > 0; i -= 1) {
        var j = Math.floor(Math.random() * (i + 1));
        var swap = copy[i];
        copy[i] = copy[j];
        copy[j] = swap;
      }
      attempts += 1;
    } while (attempts < 20 && copy.every(function (item, index) {
      return item === list[index];
    }));
    return copy;
  }

  function isAutoChecked(question) {
    return question.type === "drill" || question.type === "choice" ||
      question.type === "multi" || question.type === "order";
  }

  function mount(root) {
    var state = loadState();
    var endpoint = (root.dataset.tutorEndpoint || "").trim();
    var filter = "all";
    var order = [];
    var index = 0;
    var hintsShown = 0;
    var settled = false;
    var active = null;

    var ui = buildInterface();
    root.appendChild(ui.wrapper);

    function visible() {
      return QUESTIONS.filter(function (question) {
        if (filter === "all") {
          return true;
        }
        if (filter === "missed") {
          var result = state.results[question.id];
          return !result || !result.done || result.covered < result.total;
        }
        if (filter === "checked") {
          return isAutoChecked(question);
        }
        return question.group === filter;
      });
    }

    function current() {
      return order[index];
    }

    function rebuild(keepId) {
      order = visible();
      if (!order.length) {
        order = QUESTIONS.slice();
        filter = "all";
      }
      var found = keepId
        ? order.findIndex(function (question) {
            return question.id === keepId;
          })
        : -1;
      index = found >= 0 ? found : 0;
    }

    function scoreSummary() {
      var answered = 0;
      var covered = 0;
      var total = 0;
      QUESTIONS.forEach(function (question) {
        var result = state.results[question.id];
        if (result && result.done) {
          answered += 1;
          covered += result.covered;
          total += result.total;
        }
      });
      return { answered: answered, covered: covered, total: total };
    }

    function recordResult(covered, total) {
      var question = current();
      state.results[question.id] = { done: true, covered: covered, total: total };
      if (!saveState(state)) {
        ui.live.textContent = "Progress could not be saved in this browser.";
      }
      updateProgress();
      ui.status.textContent = isAutoChecked(question)
        ? "Scored " + covered + " of " + total
        : "Answered — you marked " + covered + " of " + total + " points covered";
      ui.status.setAttribute("data-state", covered === total ? "clear" : "warning");
    }

    function updateProgress() {
      var summary = scoreSummary();
      var percent = Math.round((summary.answered / QUESTIONS.length) * 100);
      ui.progressFill.style.width = percent + "%";
      ui.progressTrack.setAttribute("aria-valuenow", String(summary.answered));
      ui.overall.textContent =
        summary.answered +
        " of " +
        QUESTIONS.length +
        " answered" +
        (summary.total ? " · " + summary.covered + " of " + summary.total + " scored" : "");
    }

    /* ---- Question types -------------------------------------------------
       Each renderer fills `ui.body` and returns the label and handler for the
       primary button. Auto-checked types settle to a score; the prose type
       reveals what a complete answer covers and lets the learner mark it. */

    function renderProse(question) {
      var field = element("label", "field");
      field.setAttribute("for", "coach-free-answer");
      field.appendChild(element("span", null, "Your answer — write it before revealing"));
      var input = document.createElement("textarea");
      input.id = "coach-free-answer";
      input.rows = 4;
      input.placeholder = "Answer in your own words. Nothing here is sent anywhere.";
      field.appendChild(input);
      ui.body.appendChild(field);

      return {
        label: "Show a complete answer",
        run: function () {
          ui.feedback.appendChild(
            element("p", "panel-label", "A complete answer covers these — tick what yours did")
          );
          var list = element("ul", "coach-points");
          question.points.forEach(function (point, position) {
            var item = element("li");
            var label = element("label");
            var box = document.createElement("input");
            box.type = "checkbox";
            box.id = "coach-point-" + question.id + "-" + position;
            box.addEventListener("change", function () {
              var boxes = ui.feedback.querySelectorAll("input[type=checkbox]");
              var covered = 0;
              Array.prototype.forEach.call(boxes, function (each) {
                if (each.checked) {
                  covered += 1;
                }
              });
              recordResult(covered, question.points.length);
            });
            label.setAttribute("for", box.id);
            label.appendChild(box);
            label.appendChild(element("span", null, point));
            item.appendChild(label);
            list.appendChild(item);
          });
          ui.feedback.appendChild(list);
          recordResult(0, question.points.length);
          setMood("thinking");
        },
      };
    }

    function renderDrill(question) {
      var spec = DRILLS[question.drill];
      var data = spec.generate();
      active = { spec: spec, data: data };

      ui.body.appendChild(element("p", "coach-drill-prompt", spec.prompt(data)));
      var field = element("label", "field");
      field.setAttribute("for", "coach-drill-input");
      field.appendChild(element("span", null, spec.label));
      var input = document.createElement("input");
      input.id = "coach-drill-input";
      input.type = "text";
      input.inputMode = "decimal";
      input.autocomplete = "off";
      field.appendChild(input);
      ui.body.appendChild(field);

      function showWorking() {
        var list = element("ul", "coach-working");
        spec.working(data).forEach(function (line) {
          list.appendChild(element("li", null, line));
        });
        ui.feedback.appendChild(element("p", "panel-label", "The working"));
        ui.feedback.appendChild(list);
      }

      input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
          event.preventDefault();
          ui.primary.click();
        }
      });

      return {
        label: "Check",
        keepOpen: true,
        run: function () {
          var entered = parseFloat(input.value);
          var expected = spec.answer(data);
          if (!isFinite(entered)) {
            ui.feedback.textContent = "";
            ui.feedback.appendChild(
              element("p", "coach-verdict", "Enter a number before checking.")
            );
            ui.feedback.firstChild.setAttribute("data-verdict", "warning");
            return;
          }
          var tolerance = Math.max(1e-6, Math.abs(expected) * spec.tolerance);
          var right = Math.abs(entered - expected) <= tolerance;
          ui.feedback.textContent = "";
          var verdict = element(
            "p",
            "coach-verdict",
            right
              ? "Correct — " + formatNumber(expected) + "."
              : "Not yet. The definition gives " + formatNumber(expected) + "."
          );
          verdict.setAttribute("data-verdict", right ? "right" : "wrong");
          ui.feedback.appendChild(verdict);
          showWorking();
          recordResult(right ? 1 : 0, 1);
          setMood(right ? "happy" : "encouraging");
          ui.live.textContent = verdict.textContent;
          settled = true;
        },
      };
    }

    function renderChoice(question) {
      var multiple = question.type === "multi";
      var name = "coach-choice-" + question.id;
      var inputs = [];
      var list = element("ul", "coach-options");
      question.options.forEach(function (option, position) {
        var item = element("li");
        var label = element("label");
        var box = document.createElement("input");
        box.type = multiple ? "checkbox" : "radio";
        box.name = name;
        box.id = name + "-" + position;
        label.setAttribute("for", box.id);
        label.appendChild(box);
        label.appendChild(element("span", null, option.text));
        item.appendChild(label);
        list.appendChild(item);
        inputs.push({ box: box, item: item, option: option });
      });
      ui.body.appendChild(
        element(
          "p",
          "panel-label",
          multiple ? "Select every one that applies" : "Select one"
        )
      );
      ui.body.appendChild(list);

      return {
        label: "Check",
        run: function () {
          ui.feedback.textContent = "";
          var chosen = inputs.filter(function (entry) {
            return entry.box.checked;
          });
          if (!chosen.length) {
            ui.feedback.appendChild(
              element("p", "coach-verdict", "Choose an option before checking.")
            );
            ui.feedback.firstChild.setAttribute("data-verdict", "warning");
            return;
          }
          var correctCount = 0;
          inputs.forEach(function (entry) {
            var wanted = Boolean(entry.option.correct);
            var got = entry.box.checked;
            entry.box.disabled = true;
            entry.item.setAttribute(
              "data-mark",
              wanted === got ? (wanted ? "right" : "unchosen-right") : "wrong"
            );
            if (wanted === got) {
              correctCount += 1;
            }
            /* Explain every option, not just the chosen ones. On a question
               that asks the learner to discriminate between two categories,
               knowing why they were right to reject an option is half the
               lesson. */
            if (entry.option.why) {
              entry.item.appendChild(element("p", "coach-why", entry.option.why));
            }
          });
          var perfect = correctCount === inputs.length;
          var verdict = element(
            "p",
            "coach-verdict",
            perfect
              ? "All correct."
              : correctCount + " of " + inputs.length + " classified correctly."
          );
          verdict.setAttribute("data-verdict", perfect ? "right" : "wrong");
          ui.feedback.insertBefore(verdict, ui.feedback.firstChild);
          recordResult(correctCount, inputs.length);
          setMood(perfect ? "happy" : "encouraging");
          ui.live.textContent = verdict.textContent;
          settled = true;
        },
      };
    }

    function renderOrder(question) {
      var items = shuffled(question.items);
      var list = element("ol", "coach-order");

      function draw() {
        list.textContent = "";
        items.forEach(function (text, position) {
          var item = element("li");
          item.appendChild(element("span", "coach-order-text", text));
          var controls = element("div", "coach-order-controls");
          [["↑", -1], ["↓", 1]].forEach(function (entry) {
            var button = element("button", "chip chip-ghost", entry[0]);
            button.type = "button";
            button.setAttribute(
              "aria-label",
              "Move “" + text + "” " + (entry[1] < 0 ? "up" : "down")
            );
            button.disabled =
              settled ||
              (entry[1] < 0 && position === 0) ||
              (entry[1] > 0 && position === items.length - 1);
            button.addEventListener("click", function () {
              var target = position + entry[1];
              var swap = items[position];
              items[position] = items[target];
              items[target] = swap;
              draw();
              ui.live.textContent = "Moved " + text + " to position " + (target + 1) + ".";
            });
            controls.appendChild(button);
          });
          item.appendChild(controls);
          list.appendChild(item);
        });
      }

      ui.body.appendChild(element("p", "panel-label", "Put these in process order"));
      draw();
      ui.body.appendChild(list);

      return {
        label: "Check",
        run: function () {
          var right = 0;
          settled = true;
          draw();
          items.forEach(function (text, position) {
            var correct = question.items[position] === text;
            if (correct) {
              right += 1;
            }
            list.children[position].setAttribute("data-mark", correct ? "right" : "wrong");
          });
          var perfect = right === items.length;
          var verdict = element(
            "p",
            "coach-verdict",
            perfect ? "Correct order." : right + " of " + items.length + " in the right place."
          );
          verdict.setAttribute("data-verdict", perfect ? "right" : "wrong");
          ui.feedback.appendChild(verdict);
          if (!perfect) {
            ui.feedback.appendChild(element("p", "panel-label", "The order is"));
            var answer = element("ol", "coach-working");
            question.items.forEach(function (text) {
              answer.appendChild(element("li", null, text));
            });
            ui.feedback.appendChild(answer);
          }
          recordResult(right, items.length);
          setMood(perfect ? "happy" : "encouraging");
          ui.live.textContent = verdict.textContent;
        },
      };
    }

    var RENDERERS = {
      drill: renderDrill,
      choice: renderChoice,
      multi: renderChoice,
      order: renderOrder,
    };

    function render() {
      var question = current();
      hintsShown = 0;
      settled = false;
      active = null;

      ui.counter.textContent = "Question " + (index + 1) + " of " + order.length;
      ui.part.textContent = question.part;
      ui.part.setAttribute("data-tier", question.tier);
      ui.format.textContent = question.moduleLabel;
      ui.prompt.textContent = question.question;
      ui.mode.textContent = isAutoChecked(question) ? "Checked" : "Self-checked";
      ui.mode.setAttribute("data-state", isAutoChecked(question) ? "clear" : "idle");

      ui.hintList.textContent = "";
      ui.hintList.hidden = true;
      ui.hint.disabled = !question.hints || !question.hints.length;
      ui.hint.textContent = "Show a hint";

      ui.body.textContent = "";
      ui.feedback.textContent = "";
      setMood("idle");

      var renderer = RENDERERS[question.type] || renderProse;
      var action = renderer(question);
      ui.primary.textContent = action.label;
      ui.primary.disabled = false;
      ui.primary.onclick = function () {
        if (settled && !action.keepOpen) {
          return;
        }
        action.run();
        if (!action.keepOpen) {
          ui.primary.disabled = true;
        }
        if (question.note) {
          ui.feedback.appendChild(element("p", "launch-note", question.note));
        }
      };

      ui.revisit.href = question.module;
      ui.revisit.textContent = "Revisit " + question.part;

      var result = state.results[question.id];
      ui.status.textContent = result && result.done
        ? (isAutoChecked(question) ? "Scored " : "Answered — ") +
          result.covered +
          " of " +
          result.total +
          (isAutoChecked(question) ? "" : " points covered")
        : "Not answered yet";
      ui.status.setAttribute("data-state", result && result.done ? "clear" : "idle");

      updateProgress();
    }

    function showHint() {
      var question = current();
      if (!question.hints || hintsShown >= question.hints.length) {
        return;
      }
      ui.hintList.hidden = false;
      ui.hintList.appendChild(element("li", null, question.hints[hintsShown]));
      hintsShown += 1;
      if (hintsShown >= question.hints.length) {
        ui.hint.disabled = true;
        ui.hint.textContent = "No more hints";
      } else {
        ui.hint.textContent = "Another hint";
      }
      setMood("thinking");
      ui.live.textContent = "Hint " + hintsShown + ": " + question.hints[hintsShown - 1];
    }

    function step(delta) {
      index = (index + delta + order.length) % order.length;
      render();
      ui.prompt.focus();
    }

    /* The mascot. Drawn rather than embedded: an inline SVG stays sharp at any
       size, costs no request, and can change expression, which a flat image
       cannot. `data-mood` drives the brows and mouth — see `site.css`. */
    function mascot() {
      var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.setAttribute("class", "coach-mascot");
      svg.setAttribute("viewBox", "0 0 64 64");
      svg.setAttribute("data-mood", "idle");
      svg.setAttribute("role", "img");
      svg.setAttribute("aria-label", "The study coach");
      svg.innerHTML = [
        '<path class="lemon-leaf" d="M30 14C24 6 14 5 9 8c-1 6 3 14 11 16 4 1 8 0 10-2z"/>',
        '<path class="lemon-stem" d="M30 13c-1-4-2-6-3-8"/>',
        '<path class="lemon-body" d="M32 12c12 0 22 10 22 24 0 13-9 23-22 23s-22-10-22-23c0-14 10-24 22-24z"/>',
        '<path class="lemon-shine" d="M20 24c3-5 8-8 12-8" />',
        '<g class="lemon-freckles">',
        '<circle cx="20" cy="39" r="1"/><circle cx="23" cy="42" r="0.9"/>',
        '<circle cx="44" cy="39" r="1"/><circle cx="41" cy="42" r="0.9"/>',
        "</g>",
        '<g class="lemon-headset">',
        '<path d="M50 30c0-10-5-15-11-17"/>',
        '<rect x="48" y="28" width="6" height="11" rx="3"/>',
        '<path d="M51 39c0 6-4 8-8 8"/>',
        '<circle class="lemon-mic" cx="42" cy="47" r="2.4"/>',
        "</g>",
        '<g class="lemon-eyes">',
        '<ellipse cx="25" cy="34" rx="5.4" ry="6"/><ellipse cx="40" cy="34" rx="5.4" ry="6"/>',
        "</g>",
        '<g class="lemon-pupils">',
        '<circle cx="25.6" cy="34.6" r="3.3"/><circle cx="40.6" cy="34.6" r="3.3"/>',
        "</g>",
        '<g class="lemon-glints">',
        '<circle cx="27" cy="32.6" r="1.1"/><circle cx="42" cy="32.6" r="1.1"/>',
        "</g>",
        '<g class="lemon-brows">',
        '<path class="brow-left" d="M20 25.5q5-3 10-0.5"/>',
        '<path class="brow-right" d="M35 25q5-2.5 10 0.5"/>',
        "</g>",
        /* Four mouths, one shown at a time. The CSS `d` property would be
           tidier but Firefox does not support it, and a mascot whose
           expression never changes in one major browser is worse than a
           slightly longer SVG. */
        '<g class="lemon-mouth">',
        '<path class="mouth-idle" d="M27.5 44q4.5 4 9 0"/>',
        '<path class="mouth-happy" d="M25.5 42.5q6.5 7.5 13 0"/>',
        '<path class="mouth-flat" d="M28 45q4.5 1.5 8.5 0"/>',
        '<path class="mouth-soft" d="M28 45.5q4.5 -1.2 8.5 0"/>',
        "</g>",
        '<g class="lemon-sparkle"><path d="M57 21l1 3 3 1-3 1-1 3-1-3-3-1 3-1z"/></g>',
      ].join("");
      return svg;
    }

    function setMood(mood) {
      ui.mascot.setAttribute("data-mood", mood);
    }

    function buildInterface() {
      var wrapper = element("div", "coach");

      var bar = element("div", "coach-bar");
      var counter = element("span", "pill", "Question 1 of " + QUESTIONS.length);
      var part = element("span", "pill coach-part", "Part 01");
      var mode = element("span", "pill coach-mode", "Checked");
      var spacer = element("span", "spacer");
      var filters = element("div", "control-row");
      var filterButtons = [];
      [
        ["all", "All"],
        ["checked", "Auto-checked"],
        ["part", "Part checkpoints"],
        ["chapter", "Chapter checkpoints"],
        ["missed", "Not yet complete"],
      ].forEach(function (entry, position) {
        var button = element("button", "chip", entry[1]);
        button.type = "button";
        button.setAttribute("aria-pressed", String(position === 0));
        button.addEventListener("click", function () {
          filter = entry[0];
          filterButtons.forEach(function (other, otherPosition) {
            other.setAttribute("aria-pressed", String(otherPosition === position));
          });
          rebuild(current() && current().id);
          render();
        });
        filters.appendChild(button);
        filterButtons.push(button);
      });
      bar.appendChild(counter);
      bar.appendChild(part);
      bar.appendChild(mode);
      bar.appendChild(spacer);
      bar.appendChild(filters);

      var progressTrack = element("div", "progress-track");
      progressTrack.setAttribute("role", "progressbar");
      progressTrack.setAttribute("aria-label", "Checkpoint questions answered");
      progressTrack.setAttribute("aria-valuemin", "0");
      progressTrack.setAttribute("aria-valuemax", String(QUESTIONS.length));
      progressTrack.setAttribute("aria-valuenow", "0");
      var progressFill = element("span");
      progressFill.style.width = "0%";
      progressTrack.appendChild(progressFill);

      var card = element("div", "panel coach-card");
      var head = element("div", "coach-head");
      var face = mascot();
      var headText = element("div");
      var format = element("p", "format", "");
      var prompt = element("h3", "coach-question", "");
      prompt.tabIndex = -1;
      headText.appendChild(format);
      headText.appendChild(prompt);
      head.appendChild(face);
      head.appendChild(headText);

      var body = element("div", "coach-body");
      var hintList = element("ul", "coach-hint-list");
      hintList.hidden = true;

      var actions = element("div", "control-row coach-actions");
      var hint = element("button", "chip", "Show a hint");
      hint.type = "button";
      var primary = element("button", "chip chip-primary", "Check");
      primary.type = "button";
      var previous = element("button", "chip chip-ghost", "← Previous");
      previous.type = "button";
      var next = element("button", "chip chip-ghost", "Next →");
      next.type = "button";
      actions.appendChild(hint);
      actions.appendChild(primary);
      actions.appendChild(previous);
      actions.appendChild(next);

      var feedback = element("div", "coach-feedback");

      var revisitRow = element("div", "control-row coach-revisit");
      var revisit = element("a", "card-action", "Revisit");
      revisitRow.appendChild(revisit);

      card.appendChild(head);
      card.appendChild(body);
      card.appendChild(hintList);
      card.appendChild(actions);
      card.appendChild(feedback);
      card.appendChild(revisitRow);

      var footer = element("div", "coach-bar coach-footer");
      var status = element("span", "pill", "Not answered yet");
      status.setAttribute("data-state", "idle");
      var overall = element("span", "coach-overall", "");
      var footSpacer = element("span", "spacer");
      var reset = element("button", "chip chip-ghost", "Reset progress");
      reset.type = "button";
      footer.appendChild(status);
      footer.appendChild(overall);
      footer.appendChild(footSpacer);
      footer.appendChild(reset);

      var live = element("p", "sr-only");
      live.setAttribute("role", "status");
      live.setAttribute("aria-live", "polite");

      wrapper.appendChild(bar);
      wrapper.appendChild(progressTrack);
      wrapper.appendChild(card);
      wrapper.appendChild(footer);
      wrapper.appendChild(live);

      hint.addEventListener("click", showHint);
      previous.addEventListener("click", function () {
        step(-1);
      });
      next.addEventListener("click", function () {
        step(1);
      });
      reset.addEventListener("click", function () {
        state = { version: 2, results: {} };
        saveState(state);
        rebuild();
        render();
        live.textContent = "Progress reset.";
      });

      return {
        wrapper: wrapper,
        counter: counter,
        part: part,
        mode: mode,
        mascot: face,
        format: format,
        prompt: prompt,
        body: body,
        hintList: hintList,
        hint: hint,
        primary: primary,
        feedback: feedback,
        revisit: revisit,
        status: status,
        overall: overall,
        progressTrack: progressTrack,
        progressFill: progressFill,
        live: live,
      };
    }

    if (endpoint) {
      attachTutor(root, ui, endpoint, current);
    }

    rebuild();
    render();
  }

  /* Optional AI tutor. Nothing below runs unless `data-tutor-endpoint` names a
     URL, so the default page makes no network request at all. The endpoint is
     expected to be a small proxy that holds the API key server-side and
     answers { question, context } with { reply }. Never put a key here: this
     file is public, and so is anything in it. */
  function attachTutor(root, ui, endpoint, currentQuestion) {
    var panel = element("div", "panel coach-tutor");
    panel.appendChild(element("p", "panel-label", "Ask the coach"));
    panel.appendChild(
      element(
        "p",
        "launch-note",
        "Answers come from a language model and can be wrong. Check anything surprising against the module."
      )
    );

    var field = element("label", "field");
    field.setAttribute("for", "coach-tutor-input");
    field.appendChild(element("span", null, "Your follow-up question"));
    var input = document.createElement("textarea");
    input.id = "coach-tutor-input";
    input.rows = 3;
    field.appendChild(input);

    var row = element("div", "control-row");
    var send = element("button", "chip chip-primary", "Ask");
    send.type = "button";
    var status = element("span", "pill", "Ready");
    status.setAttribute("data-state", "idle");
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    row.appendChild(send);
    row.appendChild(status);

    var reply = element("div", "coach-tutor-reply");
    reply.hidden = true;

    panel.appendChild(field);
    panel.appendChild(row);
    panel.appendChild(reply);
    root.appendChild(panel);

    send.addEventListener("click", function () {
      var question = input.value.trim();
      if (!question) {
        return;
      }
      send.disabled = true;
      status.textContent = "Asking…";
      status.setAttribute("data-state", "idle");
      var active = currentQuestion();
      window
        .fetch(endpoint, {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            question: question,
            context: {
              chapter: 1,
              checkpointId: active ? active.id : null,
              checkpoint: active ? active.question : null,
            },
          }),
        })
        .then(function (response) {
          if (!response.ok) {
            throw new Error("The tutor endpoint returned " + response.status);
          }
          return response.json();
        })
        .then(function (data) {
          reply.hidden = false;
          reply.textContent = String(data && data.reply ? data.reply : "");
          status.textContent = "Answered";
          status.setAttribute("data-state", "clear");
        })
        .catch(function (error) {
          reply.hidden = false;
          reply.textContent =
            "The coach is unavailable. The checkpoints above work without it. (" +
            error.message +
            ")";
          status.textContent = "Unavailable";
          status.setAttribute("data-state", "warning");
        })
        .then(function () {
          send.disabled = false;
        });
    });
  }

  function start() {
    var root = document.getElementById("study-coach");
    if (root) {
      mount(root);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
