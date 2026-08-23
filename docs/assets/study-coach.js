/* Battery Core — Chapter 1 study coach.
 *
 * The chapter already asks a checkpoint question after every part. Reading a
 * question and thinking "yes, roughly" is not the same as answering it, so
 * this turns each one into a loop: write an answer first, then compare it
 * against the points a complete answer covers, and score yourself honestly.
 *
 * It runs entirely in the browser. No network, no account, no key. Progress
 * lives in this browser's localStorage, and clearing site data clears it.
 *
 * The coach never claims to mark an answer. It cannot read prose, and pretending
 * otherwise would be exactly the kind of unstated model limit the rest of the
 * course refuses to ship. What it does is show what a complete answer contains
 * and let the learner check their own against it. The one exception is the C-rate
 * drill, where the answer is a number and can be checked outright.
 *
 * An optional AI tutor can be attached for free-form follow-up questions; see
 * `assets/README.md` § An AI tutor. It is off unless `data-tutor-endpoint` on
 * the mount element is set to a URL, so the page ships self-contained.
 */

(function () {
  "use strict";

  var STORAGE_KEY = "battery-core-chapter-1-coach";

  /* The question bank. Model answers are grounded in the modules and in the
     tested Python: `current_from_c_rate` is Q x C, `ideal_duration_hours` is
     1 / C, and `battery_core.aging` supplies rate laws but no chemistry
     constants. Where the course draws a line between a definition and a
     prediction, the answer draws it too. */
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
      part: "Part 02",
      module:
        "https://mybinder.org/v2/gh/Morshedvarzandeh/battery-core/main?urlpath=lab/tree/notebooks/fundamentals/02_capacity_and_c_rate.ipynb",
      moduleLabel: "Part 02 · Nominal capacity and C-rate",
      question: "Calculate the constant current for this cell and rate.",
      hints: [
        "Current is nominal capacity multiplied by C-rate, with capacity in ampere-hours and C-rate in reciprocal hours.",
        "The units do the work: Ah x h⁻¹ = A.",
      ],
      note:
        "This is the exact definition the tested Python implements. It is not a runtime prediction — see the next question.",
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

  /* The drill is the one question with a checkable answer, so it gets real
     numbers rather than a model answer to compare against. */
  var DRILL_CAPACITIES = [1.5, 2.2, 3.0, 4.5, 5.0, 12, 20, 50, 100];
  var DRILL_RATES = [0.2, 0.5, 1, 2, 3, 5];

  function pick(list) {
    return list[Math.floor(Math.random() * list.length)];
  }

  function newDrill() {
    var capacity = pick(DRILL_CAPACITIES);
    var rate = pick(DRILL_RATES);
    var hours = 1 / rate;
    return {
      capacity: capacity,
      rate: rate,
      current: capacity * rate,
      hours: hours,
      minutes: hours * 60,
    };
  }

  function formatNumber(value) {
    return Number(value.toFixed(3)).toString();
  }

  function formatDuration(drill) {
    if (drill.hours >= 1) {
      return formatNumber(drill.hours) + " h";
    }
    return formatNumber(drill.minutes) + " min";
  }

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
    return { version: 1, results: {} };
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

  function mount(root) {
    var state = loadState();
    var endpoint = (root.dataset.tutorEndpoint || "").trim();
    var filter = "all";
    var order = [];
    var index = 0;
    var hintsShown = 0;
    var revealed = false;
    var drill = null;

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

    function render() {
      var question = current();
      hintsShown = 0;
      revealed = false;
      drill = question.type === "drill" ? newDrill() : null;

      ui.counter.textContent = "Question " + (index + 1) + " of " + order.length;
      ui.part.textContent = question.part;
      ui.part.setAttribute("data-tier", question.tier);
      ui.format.textContent = question.moduleLabel;
      ui.prompt.textContent = question.question;

      ui.hintList.textContent = "";
      ui.hintList.hidden = true;
      ui.hint.disabled = !question.hints || !question.hints.length;
      ui.hint.textContent = "Show a hint";

      ui.reveal.hidden = false;
      ui.answer.hidden = true;
      ui.answer.textContent = "";

      ui.freeAnswer.hidden = Boolean(drill);
      ui.drill.hidden = !drill;
      if (drill) {
        ui.drillPrompt.textContent =
          "A cell with a nominal capacity of " +
          formatNumber(drill.capacity) +
          " Ah is discharged at " +
          formatNumber(drill.rate) +
          "C. What constant current does that definition give?";
        ui.drillInput.value = "";
        ui.drillFeedback.textContent = "";
        ui.drillFeedback.setAttribute("data-state", "idle");
        ui.reveal.textContent = "Show the working";
      } else {
        ui.freeInput.value = "";
        ui.reveal.textContent = "Show a complete answer";
      }

      ui.revisit.href = question.module;
      ui.revisit.textContent = "Revisit " + question.part;

      var result = state.results[question.id];
      ui.status.textContent = result && result.done
        ? "Answered — you marked " + result.covered + " of " + result.total + " points covered"
        : "Not answered yet";
      ui.status.setAttribute("data-state", result && result.done ? "clear" : "idle");

      updateProgress();
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
        (summary.total
          ? " · " + summary.covered + " of " + summary.total + " points covered"
          : "");
    }

    function showHint() {
      var question = current();
      if (!question.hints || hintsShown >= question.hints.length) {
        return;
      }
      ui.hintList.hidden = false;
      var item = element("li", null, question.hints[hintsShown]);
      ui.hintList.appendChild(item);
      hintsShown += 1;
      if (hintsShown >= question.hints.length) {
        ui.hint.disabled = true;
        ui.hint.textContent = "No more hints";
      } else {
        ui.hint.textContent = "Another hint";
      }
      ui.live.textContent = "Hint " + hintsShown + ": " + question.hints[hintsShown - 1];
    }

    function checkDrill() {
      var entered = parseFloat(ui.drillInput.value);
      if (!isFinite(entered)) {
        ui.drillFeedback.textContent = "Enter a number in amperes.";
        ui.drillFeedback.setAttribute("data-state", "warning");
        return;
      }
      var close = Math.abs(entered - drill.current) <= Math.max(0.01, drill.current * 0.01);
      ui.drillFeedback.textContent = close
        ? "Correct — " + formatNumber(drill.current) + " A."
        : "Not yet. " + formatNumber(entered) + " A is not what Q × C gives here.";
      ui.drillFeedback.setAttribute("data-state", close ? "clear" : "warning");
      ui.live.textContent = ui.drillFeedback.textContent;
      if (close) {
        recordResult(1, 1);
      }
    }

    function recordResult(covered, total) {
      var question = current();
      state.results[question.id] = { done: true, covered: covered, total: total };
      if (!saveState(state)) {
        ui.live.textContent = "Progress could not be saved in this browser.";
      }
      updateProgress();
      ui.status.textContent =
        "Answered — you marked " + covered + " of " + total + " points covered";
      ui.status.setAttribute("data-state", "clear");
    }

    function reveal() {
      if (revealed) {
        return;
      }
      revealed = true;
      var question = current();
      ui.reveal.hidden = true;
      ui.answer.hidden = false;
      ui.answer.textContent = "";

      if (drill) {
        ui.answer.appendChild(element("p", "panel-label", "The working"));
        var working = element("ul", "coach-working");
        [
          "I = Q × C = " +
            formatNumber(drill.capacity) +
            " Ah × " +
            formatNumber(drill.rate) +
            " h⁻¹ = " +
            formatNumber(drill.current) +
            " A",
          "t = 1 / C = " + formatDuration(drill) + " at that rate, ideally",
          "The units carry the argument: Ah × h⁻¹ leaves amperes.",
        ].forEach(function (line) {
          working.appendChild(element("li", null, line));
        });
        ui.answer.appendChild(working);
        recordResult(
          state.results[question.id] && state.results[question.id].covered ? 1 : 0,
          1
        );
      } else {
        ui.answer.appendChild(
          element("p", "panel-label", "A complete answer covers these — tick what yours did")
        );
        var list = element("ul", "coach-points");
        question.points.forEach(function (point, position) {
          var item = element("li");
          var label = element("label");
          var box = document.createElement("input");
          box.type = "checkbox";
          box.id = "coach-point-" + question.id + "-" + position;
          box.addEventListener("change", tally);
          label.setAttribute("for", box.id);
          label.appendChild(box);
          label.appendChild(element("span", null, point));
          item.appendChild(label);
          list.appendChild(item);
        });
        ui.answer.appendChild(list);
        recordResult(0, question.points.length);
      }

      if (question.note) {
        ui.answer.appendChild(element("p", "launch-note", question.note));
      }
      ui.live.textContent = "Answer shown.";
    }

    function tally() {
      var question = current();
      var boxes = ui.answer.querySelectorAll("input[type=checkbox]");
      var covered = 0;
      Array.prototype.forEach.call(boxes, function (box) {
        if (box.checked) {
          covered += 1;
        }
      });
      recordResult(covered, question.points.length);
    }

    function step(delta) {
      index = (index + delta + order.length) % order.length;
      render();
      ui.prompt.focus();
    }

    function buildInterface() {
      var wrapper = element("div", "coach");

      var bar = element("div", "coach-bar");
      var counter = element("span", "pill", "Question 1 of " + QUESTIONS.length);
      var part = element("span", "pill coach-part", "Part 01");
      var spacer = element("span", "spacer");
      var filters = element("div", "control-row");
      var filterButtons = [
        ["all", "All"],
        ["part", "Part checkpoints"],
        ["chapter", "Chapter checkpoints"],
        ["missed", "Not yet complete"],
      ].map(function (entry) {
        var button = element("button", "chip", entry[1]);
        button.type = "button";
        button.setAttribute("aria-pressed", String(entry[0] === "all"));
        button.addEventListener("click", function () {
          filter = entry[0];
          filterButtons.forEach(function (other, position) {
            other.setAttribute("aria-pressed", String(position === filterButtons.indexOf(button)));
          });
          rebuild(current() && current().id);
          render();
        });
        filters.appendChild(button);
        return button;
      });
      bar.appendChild(counter);
      bar.appendChild(part);
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
      var format = element("p", "format", "");
      var prompt = element("h3", "coach-question", "");
      prompt.tabIndex = -1;

      var freeAnswer = element("label", "field");
      freeAnswer.setAttribute("for", "coach-free-answer");
      freeAnswer.appendChild(
        element("span", null, "Your answer — write it before revealing")
      );
      var freeInput = document.createElement("textarea");
      freeInput.id = "coach-free-answer";
      freeInput.rows = 4;
      freeInput.placeholder = "Answer in your own words. Nothing here is sent anywhere.";
      freeAnswer.appendChild(freeInput);

      var drillBox = element("div", "coach-drill");
      var drillPrompt = element("p", "coach-drill-prompt", "");
      var drillField = element("label", "field");
      drillField.setAttribute("for", "coach-drill-input");
      drillField.appendChild(element("span", null, "Constant current, in amperes"));
      var drillInput = document.createElement("input");
      drillInput.id = "coach-drill-input";
      drillInput.type = "text";
      drillInput.inputMode = "decimal";
      drillInput.autocomplete = "off";
      drillField.appendChild(drillInput);
      var drillRow = element("div", "control-row");
      var drillCheck = element("button", "chip chip-primary", "Check");
      drillCheck.type = "button";
      var drillFeedback = element("span", "pill", "");
      drillFeedback.setAttribute("data-state", "idle");
      drillFeedback.setAttribute("role", "status");
      drillFeedback.setAttribute("aria-live", "polite");
      drillRow.appendChild(drillCheck);
      drillRow.appendChild(drillFeedback);
      drillBox.appendChild(drillPrompt);
      drillBox.appendChild(drillField);
      drillBox.appendChild(drillRow);

      var hintList = element("ul", "coach-hint-list");
      hintList.hidden = true;

      var actions = element("div", "control-row coach-actions");
      var hint = element("button", "chip", "Show a hint");
      hint.type = "button";
      var revealButton = element("button", "chip chip-primary", "Show a complete answer");
      revealButton.type = "button";
      var previous = element("button", "chip chip-ghost", "← Previous");
      previous.type = "button";
      var next = element("button", "chip chip-ghost", "Next →");
      next.type = "button";
      actions.appendChild(hint);
      actions.appendChild(revealButton);
      actions.appendChild(previous);
      actions.appendChild(next);

      var answer = element("div", "coach-answer");
      answer.hidden = true;

      var revisitRow = element("div", "control-row coach-revisit");
      var revisit = element("a", "card-action", "Revisit");
      revisitRow.appendChild(revisit);

      card.appendChild(format);
      card.appendChild(prompt);
      card.appendChild(freeAnswer);
      card.appendChild(drillBox);
      card.appendChild(hintList);
      card.appendChild(actions);
      card.appendChild(answer);
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
      revealButton.addEventListener("click", reveal);
      previous.addEventListener("click", function () {
        step(-1);
      });
      next.addEventListener("click", function () {
        step(1);
      });
      drillCheck.addEventListener("click", checkDrill);
      drillInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
          event.preventDefault();
          checkDrill();
        }
      });
      reset.addEventListener("click", function () {
        state = { version: 1, results: {} };
        saveState(state);
        rebuild();
        render();
        live.textContent = "Progress reset.";
      });

      return {
        wrapper: wrapper,
        counter: counter,
        part: part,
        format: format,
        prompt: prompt,
        freeAnswer: freeAnswer,
        freeInput: freeInput,
        drill: drillBox,
        drillPrompt: drillPrompt,
        drillInput: drillInput,
        drillFeedback: drillFeedback,
        hintList: hintList,
        hint: hint,
        reveal: revealButton,
        answer: answer,
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
    panel.appendChild(element("p", "panel-label", "Ask the tutor"));
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
            "The tutor is unavailable. The checkpoints above work without it. (" +
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
