const partData = {
  "negative-collector": {
    title: "Negative current collector",
    description: "A metallic foil that carries electrons between the negative composite coating and the external circuit. Copper is common for graphite-based negative electrodes.",
    transport: "Electrons in the metal",
    role: "Collects current without storing the cell's main reversible charge"
  },
  "negative-electrode": {
    title: "Negative composite electrode",
    description: "A porous coating containing an active material, conductive additive, binder, and electrolyte-filled pores. Graphite is a common active material.",
    transport: "Li⁺ in pores; electrons in solids",
    role: "Stores lithium and hosts electrochemical reactions"
  },
  separator: {
    title: "Separator",
    description: "A porous electronic insulator placed between the electrodes. Its pores contain electrolyte so ions can move while the solid membrane helps prevent direct electrode contact.",
    transport: "Ions through electrolyte-filled pores",
    role: "Physically separates electrodes and blocks a direct electronic path"
  },
  "positive-electrode": {
    title: "Positive composite electrode",
    description: "A porous coating built from positive active-material particles, conductive additive, binder, and electrolyte-filled pores. Common families include NMC, LFP, LMO, and LCO.",
    transport: "Li⁺ in pores; electrons in solids",
    role: "Stores lithium and hosts electrochemical reactions"
  },
  "positive-collector": {
    title: "Positive current collector",
    description: "A metallic foil that carries electrons between the positive composite coating and the external circuit. Aluminum is commonly used.",
    transport: "Electrons in the metal",
    role: "Collects current without acting as the main lithium-storage material"
  }
};

const modeText = {
  discharge: "During discharge, Li⁺ moves through the electrolyte toward the positive electrode, while electrons travel through the external circuit.",
  charge: "During charge, the external power source drives Li⁺ toward the negative electrode and electrons through the external circuit in the reverse direction."
};

const modeButtons = document.querySelectorAll(".mode-button");
const stackStage = document.querySelector(".stack-stage");
const directionCaption = document.querySelector(".direction-caption");

modeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    modeButtons.forEach((item) => {
      const selected = item === button;
      item.classList.toggle("active", selected);
      item.setAttribute("aria-pressed", String(selected));
    });
    const mode = button.dataset.mode;
    stackStage.dataset.mode = mode;
    directionCaption.innerHTML = modeText[mode];
  });
});

const layerButtons = document.querySelectorAll(".stack-layer");
const partTitle = document.querySelector("#part-title");
const partDescription = document.querySelector("#part-description");
const partTransport = document.querySelector("#part-transport");
const partRole = document.querySelector("#part-role");

layerButtons.forEach((button) => {
  button.addEventListener("click", () => {
    layerButtons.forEach((item) => item.classList.toggle("selected", item === button));
    const part = partData[button.dataset.part];
    partTitle.textContent = part.title;
    partDescription.textContent = part.description;
    partTransport.textContent = part.transport;
    partRole.textContent = part.role;
  });
});
document.querySelector('[data-part="negative-electrode"]').classList.add("selected");

document.querySelectorAll("[data-visibility]").forEach((checkbox) => {
  checkbox.addEventListener("change", () => {
    const coating = document.querySelector(".coating");
    coating.classList.toggle(`hide-${checkbox.dataset.visibility}`, !checkbox.checked);
  });
});

const molecules = {
  EC: {
    name: "Ethylene carbonate (EC)",
    formula: "C₃H₄O₃",
    family: "Cyclic carbonate",
    description: "A five-membered cyclic carbonate containing two ring oxygen atoms and two CH₂ groups.",
    lesson: "A solvent molecule can coordinate ions and occupy liquid-filled pores without being an electrode particle.",
    nodes: [
      ["C", 260, 90, "carbon"], ["O", 260, 35, "oxygen"],
      ["O", 175, 140, "oxygen"], ["O", 345, 140, "oxygen"],
      ["CH₂", 185, 235, "group"], ["CH₂", 335, 235, "group"]
    ],
    bonds: [[0,1,"double"],[0,2],[0,3],[2,4],[3,5],[4,5]]
  },
  PC: {
    name: "Propylene carbonate (PC)",
    formula: "C₄H₆O₃",
    family: "Cyclic carbonate",
    description: "A cyclic carbonate related to EC, with one methyl substituent on the carbon ring.",
    lesson: "Small structural changes distinguish solvents that can have different physical and electrochemical properties.",
    nodes: [
      ["C", 255, 85, "carbon"], ["O", 255, 30, "oxygen"],
      ["O", 170, 135, "oxygen"], ["O", 340, 135, "oxygen"],
      ["CH₂", 180, 230, "group"], ["CH", 330, 230, "group"], ["CH₃", 420, 255, "group"]
    ],
    bonds: [[0,1,"double"],[0,2],[0,3],[2,4],[3,5],[4,5],[5,6]]
  },
  DMC: {
    name: "Dimethyl carbonate (DMC)",
    formula: "C₃H₆O₃",
    family: "Linear carbonate",
    description: "A linear carbonate with two methoxy groups attached to the carbonate center.",
    lesson: "Linear and cyclic carbonate solvents may be blended to tune bulk electrolyte behavior.",
    nodes: [
      ["C", 260, 135, "carbon"], ["O", 260, 60, "oxygen"],
      ["O", 170, 160, "oxygen"], ["O", 350, 160, "oxygen"],
      ["CH₃", 85, 220, "group"], ["CH₃", 435, 220, "group"]
    ],
    bonds: [[0,1,"double"],[0,2],[0,3],[2,4],[3,5]]
  },
  EMC: {
    name: "Ethyl methyl carbonate (EMC)",
    formula: "C₄H₈O₃",
    family: "Linear carbonate",
    description: "An asymmetric linear carbonate with one methyl side and one ethyl side.",
    lesson: "The electrolyte is usually a formulation, not a single molecule; different solvents can be mixed.",
    nodes: [
      ["C", 245, 130, "carbon"], ["O", 245, 55, "oxygen"],
      ["O", 155, 160, "oxygen"], ["O", 335, 160, "oxygen"],
      ["CH₃", 70, 220, "group"], ["CH₂", 405, 215, "group"], ["CH₃", 470, 285, "group"]
    ],
    bonds: [[0,1,"double"],[0,2],[0,3],[2,4],[3,5],[5,6]]
  },
  DEC: {
    name: "Diethyl carbonate (DEC)",
    formula: "C₅H₁₀O₃",
    family: "Linear carbonate",
    description: "A symmetric linear carbonate with an ethyl group on each side.",
    lesson: "Molecular identity matters to electrolyte properties, but this tutorial does not calculate those properties.",
    nodes: [
      ["C", 260, 120, "carbon"], ["O", 260, 45, "oxygen"],
      ["O", 165, 150, "oxygen"], ["O", 355, 150, "oxygen"],
      ["CH₂", 100, 215, "group"], ["CH₃", 45, 285, "group"],
      ["CH₂", 420, 215, "group"], ["CH₃", 475, 285, "group"]
    ],
    bonds: [[0,1,"double"],[0,2],[0,3],[2,4],[4,5],[3,6],[6,7]]
  }
};

const svgNS = "http://www.w3.org/2000/svg";
const atomLayer = document.querySelector("#atom-layer");
const bondLayer = document.querySelector("#bond-layer");
const moleculeName = document.querySelector("#molecule-name");
const moleculeFormula = document.querySelector("#molecule-formula");
const moleculeDescription = document.querySelector("#molecule-description");
const moleculeFamily = document.querySelector("#molecule-family");
const moleculeLesson = document.querySelector("#molecule-lesson");

function nodePosition(node) {
  return { x: node[1], y: node[2] };
}

function drawBond(a, b, kind) {
  const start = nodePosition(a);
  const end = nodePosition(b);
  const line = document.createElementNS(svgNS, "line");
  line.setAttribute("x1", start.x);
  line.setAttribute("y1", start.y);
  line.setAttribute("x2", end.x);
  line.setAttribute("y2", end.y);
  line.setAttribute("class", "bond");
  bondLayer.appendChild(line);

  if (kind === "double") {
    const dx = end.x - start.x;
    const dy = end.y - start.y;
    const length = Math.hypot(dx, dy) || 1;
    const offsetX = -dy / length * 8;
    const offsetY = dx / length * 8;
    const second = document.createElementNS(svgNS, "line");
    second.setAttribute("x1", start.x + offsetX);
    second.setAttribute("y1", start.y + offsetY);
    second.setAttribute("x2", end.x + offsetX);
    second.setAttribute("y2", end.y + offsetY);
    second.setAttribute("class", "bond double-secondary");
    bondLayer.appendChild(second);
  }
}

function drawAtom(node) {
  const [label, x, y, type] = node;
  const group = document.createElementNS(svgNS, "g");
  group.setAttribute("class", `atom ${type}`);
  if (type === "group") {
    const rect = document.createElementNS(svgNS, "rect");
    const width = label.length > 2 ? 72 : 58;
    rect.setAttribute("x", x - width / 2);
    rect.setAttribute("y", y - 25);
    rect.setAttribute("width", width);
    rect.setAttribute("height", 50);
    rect.setAttribute("rx", 20);
    group.appendChild(rect);
  } else {
    const circle = document.createElementNS(svgNS, "circle");
    circle.setAttribute("cx", x);
    circle.setAttribute("cy", y);
    circle.setAttribute("r", 28);
    group.appendChild(circle);
  }
  const text = document.createElementNS(svgNS, "text");
  text.setAttribute("x", x);
  text.setAttribute("y", y + 1);
  text.setAttribute("font-size", label.length > 2 ? "19" : "23");
  text.textContent = label;
  group.appendChild(text);
  atomLayer.appendChild(group);
}

function selectMolecule(key) {
  const molecule = molecules[key];
  bondLayer.replaceChildren();
  atomLayer.replaceChildren();
  molecule.bonds.forEach(([start, end, kind]) => drawBond(molecule.nodes[start], molecule.nodes[end], kind));
  molecule.nodes.forEach(drawAtom);
  moleculeName.textContent = molecule.name;
  moleculeFormula.textContent = molecule.formula;
  moleculeDescription.textContent = molecule.description;
  moleculeFamily.textContent = molecule.family;
  moleculeLesson.textContent = molecule.lesson;
}

document.querySelectorAll("[data-molecule]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-molecule]").forEach((item) => {
      item.setAttribute("aria-selected", String(item === button));
    });
    selectMolecule(button.dataset.molecule);
  });
});
selectMolecule("EC");

const dissolveButton = document.querySelector("#dissolve-button");
const saltStage = document.querySelector("#salt-stage");
const saltCaption = document.querySelector("#salt-caption");
dissolveButton.addEventListener("click", () => {
  const dissolved = saltStage.dataset.state !== "dissolved";
  saltStage.dataset.state = dissolved ? "dissolved" : "paired";
  dissolveButton.setAttribute("aria-pressed", String(dissolved));
  dissolveButton.textContent = dissolved ? "Reset salt pair" : "Dissolve salt";
  saltCaption.textContent = dissolved
    ? "Conceptual result: Li⁺ and PF₆⁻ are separated in the solvent medium. Real solvation and ion association are more complex."
    : "Before the conceptual dissolve step, the ions are shown as an associated salt pair.";
});

const travelerData = {
  ion: {
    label: "Li⁺",
    className: "ion-traveler",
    passes: true,
    result: "Li⁺ can move through electrolyte-filled separator pores."
  },
  electron: {
    label: "e−",
    className: "electron-traveler",
    passes: false,
    result: "An intact separator is electronically insulating; electrons should use the external circuit instead."
  },
  particle: {
    label: "particle",
    className: "particle-traveler",
    passes: false,
    result: "Electrode particles are much larger than the conceptual pore pathway and should remain separated."
  }
};

let selectedTraveler = "ion";
const traveler = document.querySelector("#traveler");
const gateResult = document.querySelector("#gate-result");

document.querySelectorAll("[data-traveler]").forEach((button) => {
  button.addEventListener("click", () => {
    selectedTraveler = button.dataset.traveler;
    document.querySelectorAll("[data-traveler]").forEach((item) => {
      const selected = item === button;
      item.classList.toggle("active", selected);
      item.setAttribute("aria-pressed", String(selected));
    });
    const data = travelerData[selectedTraveler];
    traveler.className = `traveler ${data.className}`;
    traveler.innerHTML = data.label;
    gateResult.textContent = data.result;
  });
});

document.querySelector("#test-gate").addEventListener("click", () => {
  const data = travelerData[selectedTraveler];
  traveler.classList.remove("passed", "blocked");
  void traveler.offsetWidth;
  traveler.classList.add(data.passes ? "passed" : "blocked");
  gateResult.textContent = data.result;
});

document.querySelector("#quiz").addEventListener("submit", (event) => {
  event.preventDefault();
  const fields = [...event.currentTarget.querySelectorAll("fieldset")];
  let score = 0;
  fields.forEach((field) => {
    const selected = field.querySelector("input:checked");
    const feedback = field.querySelector(".feedback");
    const correct = selected && selected.value === field.dataset.answer;
    if (correct) {
      score += 1;
      feedback.textContent = "Correct.";
      feedback.className = "feedback correct";
    } else if (!selected) {
      feedback.textContent = "Choose an answer.";
      feedback.className = "feedback incorrect";
    } else {
      feedback.textContent = "Not quite. Review the relevant tutorial step and try again.";
      feedback.className = "feedback incorrect";
    }
  });
  document.querySelector("#quiz-score").textContent = `Score: ${score} / ${fields.length}`;
});
