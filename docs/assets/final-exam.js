/* Battery Core — the final exam.
 *
 * Twenty closed questions, written into the page so they can be read without
 * JavaScript. This file marks them: an answer is right only when exactly the
 * options marked data-correct="true" are chosen. A pass records the item
 * "exam" in the same course progress the syllabus reads, and opens a
 * statement of completion the learner can print.
 *
 * Everything stays in this browser's localStorage. The statement says so: it
 * is a record for the learner, not a verified certificate.
 */
(() => {
  "use strict";

  const form = document.getElementById("final-exam");
  if (!form) return;

  const EXAM_KEY = "battery-core-final-exam";
  const PROGRESS_KEY = "battery-core-course-progress";
  const pass = Number(form.dataset.pass) || 0;
  const questions = [...form.querySelectorAll("fieldset.exam-q")];
  const result = document.getElementById("exam-result");
  const reset = form.querySelector("[data-exam-reset]");
  const statement = document.getElementById("statement");
  const nameInput = document.getElementById("learner-name");

  const read = key => {
    try {
      const raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      return null;
    }
  };
  const write = (key, value) => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      /* storage blocked: the result still shows for this visit */
    }
  };

  const formatDate = iso => new Date(iso).toLocaleDateString(undefined, {
    year: "numeric", month: "long", day: "numeric",
  });

  function showStatement(record) {
    if (!statement || !record) return;
    statement.hidden = false;
    statement.querySelector("[data-statement-score]").textContent = `${record.score} of ${record.total}`;
    statement.querySelector("[data-statement-date]").textContent = formatDate(record.passedAt);
    const name = record.name || "";
    if (nameInput) nameInput.value = name;
    statement.querySelector("[data-statement-name]").textContent = name || "Your name";
  }

  function mark(fieldset) {
    const inputs = [...fieldset.querySelectorAll("input")];
    const answered = inputs.some(input => input.checked);
    const right = inputs.every(input => input.checked === (input.dataset.correct === "true"));
    return { answered, right };
  }

  form.addEventListener("submit", event => {
    event.preventDefault();
    const marks = questions.map(mark);
    const missing = marks.findIndex(m => !m.answered);
    if (missing !== -1) {
      result.textContent = `Question ${missing + 1} has no answer yet. Answer every question, then submit.`;
      questions[missing].scrollIntoView({ behavior: "smooth", block: "center" });
      questions[missing].querySelector("input").focus({ preventScroll: true });
      return;
    }
    let score = 0;
    marks.forEach((m, i) => {
      const fieldset = questions[i];
      fieldset.dataset.result = m.right ? "right" : "wrong";
      fieldset.querySelectorAll("input").forEach(input => {
        input.disabled = true;
        if (input.dataset.correct === "true") input.parentElement.dataset.key = "true";
      });
      const why = fieldset.querySelector(".exam-why");
      why.hidden = false;
      why.querySelector("[data-verdict]").textContent = m.right ? "Right." : "Not quite.";
      if (m.right) score += 1;
    });
    const total = questions.length;
    const passed = score >= pass;
    result.textContent = passed
      ? `You scored ${score} of ${total}. You passed — your statement of completion is below.`
      : `You scored ${score} of ${total}. You need ${pass} to pass. Review the marked questions and try again.`;
    result.dataset.state = passed ? "pass" : "fail";
    reset.hidden = false;

    const previous = read(EXAM_KEY) || {};
    const record = { ...previous, best: Math.max(previous.best || 0, score), total };
    if (passed && !previous.passedAt) {
      record.passedAt = new Date().toISOString();
      record.score = score;
    } else if (passed && score > (previous.score || 0)) {
      record.score = score;
    }
    write(EXAM_KEY, record);
    if (passed) {
      const progress = read(PROGRESS_KEY) || { completed: {} };
      progress.completed = progress.completed || {};
      if (!progress.completed.exam) progress.completed.exam = record.passedAt;
      write(PROGRESS_KEY, progress);
      window.dispatchEvent(new Event("battery-core-progress"));
      showStatement(record);
    }
    result.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  reset.addEventListener("click", () => {
    questions.forEach(fieldset => {
      delete fieldset.dataset.result;
      fieldset.querySelector(".exam-why").hidden = true;
      fieldset.querySelectorAll("input").forEach(input => {
        input.disabled = false;
        input.checked = false;
        delete input.parentElement.dataset.key;
      });
    });
    result.textContent = "";
    delete result.dataset.state;
    reset.hidden = true;
    questions[0].scrollIntoView({ behavior: "smooth", block: "start" });
  });

  if (nameInput) {
    nameInput.addEventListener("input", () => {
      const record = read(EXAM_KEY) || {};
      record.name = nameInput.value.trim();
      write(EXAM_KEY, record);
      statement.querySelector("[data-statement-name]").textContent = record.name || "Your name";
    });
  }

  const printButton = document.querySelector("[data-print-statement]");
  if (printButton) {
    printButton.addEventListener("click", () => {
      document.documentElement.classList.add("print-statement");
      window.print();
    });
    window.addEventListener("afterprint", () => {
      document.documentElement.classList.remove("print-statement");
    });
  }

  const saved = read(EXAM_KEY);
  if (saved && saved.passedAt) {
    showStatement(saved);
    result.textContent = `You passed on ${formatDate(saved.passedAt)} with ${saved.score} of ${saved.total}. You can take the exam again at any time.`;
    result.dataset.state = "pass";
  }
})();
