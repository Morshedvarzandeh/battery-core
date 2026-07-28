(() => {
    const root = document.getElementById("cell-architecture");
    if (!root) return;
    const $ = id => document.getElementById(id);

    /* ------------------------------------------------------------------
       Layer data. `why` answers the question the original tutorial left
       open: not just what each layer is, but why it cannot be anything else.
       ------------------------------------------------------------------ */
    const layers = {
      1: { short: "Negative current collector", title: "Layer 1 · Negative current collector",
           description: "A metallic copper foil supporting the negative electrode coating.",
           phase: "Dense metal", job: "Collect and distribute electronic current",
           moves: "Electrons through the metal",
           why: "Copper, not aluminium: aluminium alloys with lithium at the low potential of the negative electrode, so it would be destroyed there.",
           skin: "skin-1", caption: "Copper foil", porous: false },
      2: { short: "Negative composite electrode", title: "Layer 2 · Negative composite electrode",
           description: "A porous coating of active material, conductive additive, binder and electrolyte-filled pores.",
           phase: "Porous composite solid + pore liquid",
           job: "Store lithium and host interfacial electrochemical reactions",
           moves: "Electrons through solids; Li⁺ and anions through pore electrolyte",
           why: "Graphite can reversibly host lithium between its sheets without bulk dissolution or plating during intended operation, supporting repeated cycling when the cell remains within its operating limits.",
           skin: "skin-2", caption: "Porous coating", porous: true },
      3: { short: "Separator", title: "Layer 3 · Separator",
           description: "A porous, electronically insulating membrane whose pores are filled with liquid electrolyte.",
           phase: "Porous polymer + pore liquid",
           job: "Keep the electrodes apart while maintaining ionic continuity",
           moves: "Li⁺ and anions through pore electrolyte; no electrons through the membrane",
           why: "Polyolefin membranes are thin, electronically insulating and porous. Some designs soften and close pores at elevated temperature, but shutdown behavior is not universal and does not prevent every failure mode.",
           skin: "skin-3", caption: "Porous membrane", porous: true },
      4: { short: "Positive composite electrode", title: "Layer 4 · Positive composite electrode",
           description: "A porous coating of positive active material, conductive additive, binder and electrolyte-filled pores.",
           phase: "Porous composite solid + pore liquid",
           job: "Store lithium and host interfacial electrochemical reactions",
           moves: "Electrons through solids; Li⁺ and anions through pore electrolyte",
           why: "A transition-metal oxide or phosphate reversibly hosts lithium at a higher potential than the negative material; the difference between their electrode potentials produces the cell voltage.",
           skin: "skin-4", caption: "Porous coating", porous: true },
      5: { short: "Positive current collector", title: "Layer 5 · Positive current collector",
           description: "A metallic aluminium foil supporting the positive electrode coating.",
           phase: "Dense metal", job: "Collect and distribute electronic current",
           moves: "Electrons through the metal",
           why: "Aluminium, not copper: copper would oxidise and dissolve at the high potential of the positive electrode. Aluminium passivates instead.",
           skin: "skin-5", caption: "Aluminium foil", porous: false }
    };

    /* One source of truth, so the rail can never contradict the panels. */
    const state = { revealed: 1, focus: 1, poreUnlocked: false };

    /* ---------------- build the three layer controls ---------------- */
    const stack = $("ca-layer-stack");
    const mini = $("ca-mini-stack");
    const menu = $("ca-layer-menu");

    for (let n = 1; n <= 5; n += 1) {
      const d = layers[n];

      const tile = document.createElement("button");
      tile.type = "button";
      tile.className = `ca-tile ${d.skin}`;
      tile.dataset.layer = n;
      tile.setAttribute("aria-pressed", "false");
      tile.innerHTML =
        `<span class="ca-num">${n}</span>` +
        `<span class="ca-name">${d.short}</span>` +
        `<span class="ca-cap">${d.caption}</span>`;
      tile.addEventListener("click", () => setFocus(n));
      stack.appendChild(tile);

      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = `ca-mini ${d.skin}`;
      chip.dataset.layer = n;
      chip.setAttribute("data-tooltip", d.short);
      chip.setAttribute("title", d.short);
      chip.setAttribute("aria-label", `Go to layer ${n}, ${d.short}`);
      chip.addEventListener("click", () => {
        setFocus(n, true);
        root.querySelector(".ca-zoom").scrollIntoView({ behavior: "smooth", block: "center" });
      });
      mini.appendChild(chip);

      const choice = document.createElement("button");
      choice.type = "button";
      choice.className = "ca-choice";
      choice.dataset.layer = n;
      choice.textContent = `${n} · ${d.short}`;
      choice.setAttribute("aria-pressed", "false");
      choice.addEventListener("click", () => setFocus(n, true));
      menu.appendChild(choice);
    }

    /* ---------------- zoom visuals ---------------- */
    const hot = (cls, style, label, content = "") =>
      `<span class="${cls}" style="${style}" data-tooltip="${label}" tabindex="0" role="img" aria-label="${label}">${content}</span>`;

    function makeComposite(layer) {
      const positive = layer === 4;
      const grain = positive ? "oxide" : "graphite";
      const grainTip = positive
        ? "Positive active material: an oxide or phosphate grain. Lithium occupies sites inside the host crystal."
        : "Active material: graphite. Lithium sits between the stacked carbon sheets.";
      const ionTip = `Li⁺ in the pore electrolyte beside the ${positive ? "positive" : "negative"} composite electrode.`;
      return `<div class="ca-composite">
        ${["g1","g2","g3","g4","g5"].map(g => hot(`ca-grain ${grain} ${g}`, "", grainTip)).join("")}
        ${hot("ca-carbon","left:36%;top:32%","Conductive additive: carbon that helps electrons move through the porous coating.")}
        ${hot("ca-carbon","left:61%;top:23%","Conductive additive: carbon that helps electrons move through the porous coating.")}
        ${hot("ca-carbon","left:48%;bottom:20%","Conductive additive: carbon that helps electrons move through the porous coating.")}
        ${hot("ca-binder","left:21%;top:49%;width:38%;transform:rotate(-12deg)","Binder: polymer that holds the solid particles together. Not active material.")}
        ${hot("ca-binder","left:51%;top:59%;width:31%;transform:rotate(18deg)","Binder: polymer that holds the solid particles together. Not active material.")}
        ${hot("ca-poreion","left:13%;bottom:16%",ionTip,"Li⁺")}
        ${hot("ca-poreion","right:13%;top:12%",ionTip,"Li⁺")}
      </div>`;
    }

    const makeSeparator = () => `<div class="ca-separator">
      ${hot("","position:absolute;left:8%;top:10%;width:32%;height:58%;border-radius:12px;background:rgba(222,216,171,.42);border:1px dashed rgba(255,255,255,.22)","Separator polymer skeleton: the electronically insulating solid framework.")}
      ${hot("","position:absolute;right:10%;top:12%;width:28%;height:55%;border-radius:12px;background:rgba(66,151,199,.34);border:1px dashed rgba(255,255,255,.22)","Electrolyte-filled pore channels: the ionic path through the separator.")}
    </div>`;

    const makeFoil = metal => {
      const t = metal === "copper"
        ? "Copper current collector: a dense metallic foil for electron transport."
        : "Aluminium current collector: a dense metallic foil for electron transport.";
      return `<div class="ca-foil ${metal}" data-tooltip="${t}" tabindex="0" role="img" aria-label="${t}"></div>`;
    };

    const chip = (css, label) =>
      `<span class="ca-chip"><span class="ca-swatch" style="${css}"></span>${label}</span>`;

    function setLegend(layer) {
      const legend = $("ca-legend"), helper = $("ca-helper");
      if (layer === 1 || layer === 5) {
        helper.textContent = "Hover the foil to identify the dense metallic current collector.";
        legend.innerHTML = chip(layer === 1
          ? "background:linear-gradient(90deg,#713613,#e6a66e 48%,#b87333 72%,#5d2b0d);border-radius:3px"
          : "background:linear-gradient(90deg,#687b85,#e0e7ea 48%,#a8bbc5 72%,#596b75);border-radius:3px",
          layer === 1 ? "Copper foil" : "Aluminium foil");
      } else if (layer === 3) {
        helper.textContent = "Hover the highlighted regions to separate polymer from electrolyte-filled pore channels.";
        legend.innerHTML =
          chip("background:var(--ca-polymer);border-radius:3px", "Separator polymer") +
          chip("background:color-mix(in srgb, var(--ca-liquid) 78%, transparent)", "Electrolyte-filled pore channel");
      } else {
        const positive = layer === 4;
        helper.textContent = "Hover items in the drawing to identify active material, conductive additive, binder and Li⁺ in the pore liquid.";
        legend.innerHTML =
          chip(positive
            ? "background:radial-gradient(circle at 34% 28%,#8fd9bd,#4f987f 62%,#1f4d3f)"
            : "background:repeating-linear-gradient(0deg,#74858e 0 3px,#39474e 3px 6px);border-radius:3px",
            positive ? "Positive active material" : "Graphite active material") +
          chip("background:#0c0c0c;box-shadow:inset 0 0 0 2px rgba(255,255,255,.2)", "Conductive additive") +
          chip("background:var(--viz-series-2);width:20px;height:4px;border-radius:99px", "Binder") +
          chip("background:color-mix(in srgb, var(--ca-liquid) 78%, transparent)", "Pore electrolyte") +
          chip("background:var(--viz-series-1)", "Li⁺");
      }
    }

    /* ---------------- state ---------------- */
    function setFocus(layer, force = false) {
      if (!force && layer > state.revealed) return;
      state.focus = layer;
      const d = layers[layer];
      root.querySelectorAll(".ca-tile").forEach(b =>
        b.setAttribute("aria-pressed", String(Number(b.dataset.layer) === layer)));
      root.querySelectorAll(".ca-choice").forEach(b =>
        b.setAttribute("aria-pressed", String(Number(b.dataset.layer) === layer)));
      root.querySelectorAll(".ca-mini").forEach(b =>
        b.setAttribute("aria-current", String(Number(b.dataset.layer) === layer)));

      $("ca-layer-title").textContent = d.title;
      $("ca-layer-desc").textContent = d.description;
      $("ca-layer-phase").textContent = d.phase;
      $("ca-layer-job").textContent = d.job;
      $("ca-layer-moves").textContent = d.moves;
      $("ca-layer-why").textContent = d.why;
      $("ca-zoom-title").textContent = `Inside ${d.title.toLowerCase()}`;
      $("ca-zoom-copy").textContent = d.description;
      $("ca-crumb-layer").textContent = d.title;
      $("ca-crumb-depth").textContent = "Layer interior";
      $("ca-rail-location").textContent = `${d.title} · ${d.porous ? "porous; pore electrolyte present" : "dense metal; no pore electrolyte"}`;

      const v = $("ca-zoom-visual");
      if (layer === 1) v.innerHTML = makeFoil("copper");
      else if (layer === 5) v.innerHTML = makeFoil("aluminium");
      else if (layer === 3) v.innerHTML = makeSeparator();
      else v.innerHTML = makeComposite(layer);

      const pore = $("ca-pore");
      pore.disabled = !d.porous;
      pore.textContent = d.porous ? "Zoom into pore electrolyte" : "No pore electrolyte in dense metal";
      setLegend(layer);
    }

    function updateAssembly() {
      root.querySelectorAll(".ca-tile").forEach(b => {
        const n = Number(b.dataset.layer);
        b.classList.toggle("is-revealed", n <= state.revealed);
        b.disabled = n > state.revealed;
      });
      $("ca-count").textContent = `${state.revealed} of 5 layers visible`;
      const next = $("ca-next");
      next.disabled = state.revealed === 5;
      next.textContent = state.revealed === 5 ? "Complete stack assembled" : `Add layer ${state.revealed + 1}`;
      $("ca-not-layer").hidden = state.revealed !== 5;
      $("ca-progress").innerHTML = state.revealed === 5
        ? "<strong>Complete stack</strong>: five physical layers are assembled. Now separate the pore-filling electrolyte from the structural layers."
        : `<strong>${layers[state.revealed].title}:</strong> ${layers[state.revealed].description}`;
    }

    function lockPore() {
      state.poreUnlocked = false;
      $("ca-lock").hidden = false;
      $("ca-molecules").hidden = true;
    }

    $("ca-next").addEventListener("click", () => {
      if (state.revealed < 5) { state.revealed += 1; updateAssembly(); setFocus(state.revealed); }
    });
    $("ca-all").addEventListener("click", () => { state.revealed = 5; updateAssembly(); setFocus(5); });
    $("ca-reset").addEventListener("click", () => {
      state.revealed = 1;
      lockPore();
      updateAssembly();
      setFocus(1);
      setSaltStep(0);
      drawMolecule("EC");
      root.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    $("ca-back").addEventListener("click", () =>
      root.querySelector(".ca-assembly").scrollIntoView({ behavior: "smooth", block: "center" }));
    $("ca-goto-porous").addEventListener("click", () => {
      setFocus(2, true);
      root.querySelector(".ca-zoom").scrollIntoView({ behavior: "smooth", block: "center" });
      setTimeout(() => $("ca-pore").focus(), 600);
    });
    $("ca-pore").addEventListener("click", () => {
      const d = layers[state.focus];
      if (!d.porous) return;
      state.poreUnlocked = true;
      $("ca-lock").hidden = true;
      $("ca-molecules").hidden = false;
      $("ca-mol-parent").textContent = d.title;
      $("ca-mol-location").textContent = `Liquid pore phase inside ${d.title.toLowerCase()}`;
      $("ca-crumb-depth").textContent = "Pore electrolyte";
      $("ca-molecules").scrollIntoView({ behavior: "smooth", block: "start" });
    });

    const visual = $("ca-zoom-visual");
    const readout = $("ca-readout");
    const idle = "Move the pointer over an item to identify it.";
    const show = t => {
      const i = t.closest?.("[data-tooltip]");
      if (i && visual.contains(i)) readout.textContent = i.dataset.tooltip;
    };
    visual.addEventListener("mouseover", e => show(e.target));
    visual.addEventListener("focusin", e => show(e.target));
    visual.addEventListener("mouseleave", () => { readout.textContent = idle; });
    visual.addEventListener("focusout", e => {
      if (!visual.contains(e.relatedTarget)) readout.textContent = idle;
    });

    /* -------------------------------------------------------------------
       Molecules. Bonds reference atom indices, so a bond can never drift
       from its atom. The carbonyl C=O always points away from the rest of
       the molecule, and the two atoms sit far enough apart that both lines
       of the double bond are visible outside the atom circles.
       ------------------------------------------------------------------ */
    const molecules = {
      EC: { name: "Ethylene carbonate (EC)", formula: "C₃H₄O₃",
        desc: "A cyclic carbonate: a five-membered ring with the C=O pointing out of the ring.",
        atoms: [["C",260,120,"carbon"],["O",260,40,"oxygen"],["O",184,175,"oxygen"],["O",336,175,"oxygen"],["CH₂",213,265,"carbon"],["CH₂",307,265,"carbon"]],
        bonds: [[0,1,2],[0,2,1],[0,3,1],[2,4,1],[3,5,1],[4,5,1]] },
      PC: { name: "Propylene carbonate (PC)", formula: "C₄H₆O₃",
        desc: "A cyclic carbonate with a methyl group on one ring carbon.",
        atoms: [["C",252,118,"carbon"],["O",252,38,"oxygen"],["O",176,173,"oxygen"],["O",328,173,"oxygen"],["CH₂",205,263,"carbon"],["CH",299,263,"carbon"],["CH₃",396,296,"carbon"]],
        bonds: [[0,1,2],[0,2,1],[0,3,1],[2,4,1],[3,5,1],[4,5,1],[5,6,1]] },
      DMC: { name: "Dimethyl carbonate (DMC)", formula: "C₃H₆O₃",
        desc: "A linear carbonate with a methyl group on each side.",
        atoms: [["C",260,150,"carbon"],["O",260,55,"oxygen"],["O",165,205,"oxygen"],["O",355,205,"oxygen"],["CH₃",75,255,"carbon"],["CH₃",445,255,"carbon"]],
        bonds: [[0,1,2],[0,2,1],[0,3,1],[2,4,1],[3,5,1]] },
      EMC: { name: "Ethyl methyl carbonate (EMC)", formula: "C₄H₈O₃",
        desc: "A linear carbonate with one methyl group and one ethyl group.",
        atoms: [["C",250,130,"carbon"],["O",250,35,"oxygen"],["O",155,185,"oxygen"],["O",345,185,"oxygen"],["CH₃",65,235,"carbon"],["CH₂",430,232,"carbon"],["CH₃",462,300,"carbon"]],
        bonds: [[0,1,2],[0,2,1],[0,3,1],[2,4,1],[3,5,1],[5,6,1]] },
      DEC: { name: "Diethyl carbonate (DEC)", formula: "C₅H₁₀O₃",
        desc: "A linear carbonate with an ethyl group on each side.",
        atoms: [["C",260,125,"carbon"],["O",260,30,"oxygen"],["O",168,180,"oxygen"],["O",352,180,"oxygen"],["CH₂",88,228,"carbon"],["CH₃",58,300,"carbon"],["CH₂",432,228,"carbon"],["CH₃",462,300,"carbon"]],
        bonds: [[0,1,2],[0,2,1],[0,3,1],[2,4,1],[4,5,1],[3,6,1],[6,7,1]] }
    };

    const NS = "http://www.w3.org/2000/svg";
    function drawMolecule(key) {
      const d = molecules[key];
      const bonds = $("ca-bonds"), atoms = $("ca-atoms");
      bonds.replaceChildren(); atoms.replaceChildren();

      d.bonds.forEach(([i, j, order]) => {
        const a = d.atoms[i], b = d.atoms[j];
        const dx = b[1] - a[1], dy = b[2] - a[2];
        const len = Math.hypot(dx, dy) || 1;
        const nx = -dy / len, ny = dx / len;              // unit normal for the 2nd line
        (order === 2 ? [-4.5, 4.5] : [0]).forEach(o => {
          const line = document.createElementNS(NS, "line");
          line.setAttribute("x1", a[1] + nx * o); line.setAttribute("y1", a[2] + ny * o);
          line.setAttribute("x2", b[1] + nx * o); line.setAttribute("y2", b[2] + ny * o);
          line.setAttribute("class", "ca-bond");
          bonds.appendChild(line);
        });
      });

      d.atoms.forEach(([label, x, y, kind]) => {
        const g = document.createElementNS(NS, "g");
        g.setAttribute("class", "ca-atom " + kind);
        const c = document.createElementNS(NS, "circle");
        c.setAttribute("cx", x); c.setAttribute("cy", y);
        c.setAttribute("r", label.length > 1 ? 28 : 23);
        const t = document.createElementNS(NS, "text");
        t.setAttribute("x", x); t.setAttribute("y", y); t.textContent = label;
        g.append(c, t); atoms.appendChild(g);
      });

      $("ca-mol-title").textContent = d.name;
      $("ca-mol-formula").textContent = d.formula;
      $("ca-mol-desc").textContent = d.desc;
      root.querySelectorAll("#ca-mol-tabs .btn").forEach(b =>
        b.setAttribute("aria-selected", String(b.dataset.molecule === key)));
    }

    const tabs = $("ca-mol-tabs");
    Object.keys(molecules).forEach(key => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "btn"; b.dataset.molecule = key;
      b.textContent = key; b.setAttribute("role", "tab"); b.setAttribute("aria-selected", "false");
      b.addEventListener("click", () => drawMolecule(key));
      tabs.appendChild(b);
    });

    /* ---------------- salt lab ---------------- */
    const stages = [
      { title: "Stage 1 · Associated ion pair",
        caption: "Li⁺ and PF₆⁻ are drawn close together as an associated pair. The surrounding solvent molecules have no ordered orientation yet.",
        changes: "Reference state: the ions are drawn close together.",
        unchanged: "The solvent molecules keep the same atoms and bond connectivity." },
      { title: "Stage 2 · Greater ion separation",
        caption: "The ions are now drawn farther apart in the pore liquid. This shows ion separation only; it does not claim complete dissociation or a particular ion-pairing equilibrium.",
        changes: "The distance between Li⁺ and PF₆⁻ increases.",
        unchanged: "No solvent bonds break, and the solvent structures do not change." },
      { title: "Stage 3 · Conceptual solvent orientation",
        caption: "Carbonate oxygen-rich regions turn toward Li⁺. Several solvent oxygen donors may occupy its local coordination environment, but the number and identities depend on composition, concentration and temperature. The environment around PF₆⁻ is drawn differently and less ordered only as a conceptual contrast; real anion coordination is also dynamic and composition-dependent.",
        changes: "Nearby solvent molecules move and reorient; the local environments around Li⁺ and PF₆⁻ are shown as different, dynamic arrangements.",
        unchanged: "The solvent molecules are not chemically transformed. Only their positions and orientations change." }
    ];

    let saltStep = 0;
    function setSaltStep(step) {
      saltStep = Math.max(0, Math.min(2, step));
      $("ca-salt-stage").dataset.step = String(saltStep);
      root.querySelectorAll("[data-salt-step]").forEach(b =>
        b.setAttribute("aria-pressed", String(Number(b.dataset.saltStep) === saltStep)));
      $("ca-salt-title").textContent = stages[saltStep].title;
      $("ca-salt-caption").textContent = stages[saltStep].caption;
      $("ca-salt-changes").textContent = stages[saltStep].changes;
      $("ca-salt-unchanged").textContent = stages[saltStep].unchanged;
      $("ca-salt-next").textContent = saltStep === 2 ? "Restart sequence" : "Next change";
    }
    root.querySelectorAll("[data-salt-step]").forEach(b =>
      b.addEventListener("click", () => setSaltStep(Number(b.dataset.saltStep))));
    $("ca-salt-next").addEventListener("click", () => setSaltStep(saltStep === 2 ? 0 : saltStep + 1));
    $("ca-salt-reset").addEventListener("click", () => setSaltStep(0));

    /* ---------------- init ---------------- */
    updateAssembly();
    setFocus(1);
    drawMolecule("EC");
    setSaltStep(0);
  })();
