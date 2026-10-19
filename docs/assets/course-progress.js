/* Battery Core — course progress.
 *
 * Coursera-style completion tracking without an account: each syllabus item
 * has a stable id, and "Mark as complete" records it in this browser's
 * localStorage. Nothing is sent anywhere; clearing site data clears it, and a
 * browser that blocks storage still gets a working page, just without memory.
 *
 * Markup contract:
 *
 *   <button data-complete="p02">Mark as complete</button>
 *       Toggles item p02. The button text and aria-pressed follow the state.
 *
 *   <li data-progress-item="p02">…</li>
 *       Any element: gets data-done="true" once p02 is complete.
 *
 *   <div data-progress-summary data-total="6">…<span data-progress-count>
 *       <span data-progress-bar> and role="progressbar" are kept up to date.
 *
 * Elements marked `hidden data-progress-ui` are revealed only when this script
 * runs, so a page without JavaScript never shows a button that does nothing.
 */
(() => {
  "use strict";

  const KEY = "battery-core-course-progress";

  function load() {
    try {
      const raw = window.localStorage.getItem(KEY);
      const data = raw ? JSON.parse(raw) : null;
      return data && typeof data.completed === "object" && data.completed ? data : { completed: {} };
    } catch (error) {
      return { completed: {} };
    }
  }

  function save(state) {
    try {
      window.localStorage.setItem(KEY, JSON.stringify(state));
    } catch (error) {
      /* storage blocked: the page still works for this visit */
    }
  }

  let state = load();

  const isDone = id => Boolean(state.completed[id]);

  function render() {
    document.querySelectorAll("[data-complete]").forEach(button => {
      const done = isDone(button.dataset.complete);
      button.setAttribute("aria-pressed", String(done));
      button.textContent = done ? "✓ Completed" : "Mark as complete";
    });

    document.querySelectorAll("[data-progress-item]").forEach(el => {
      if (isDone(el.dataset.progressItem)) el.dataset.done = "true";
      else delete el.dataset.done;
    });

    document.querySelectorAll("[data-progress-summary]").forEach(summary => {
      const ids = (summary.dataset.items || "").split(/\s+/).filter(Boolean);
      const done = ids.filter(isDone).length;
      const total = ids.length;
      const count = summary.querySelector("[data-progress-count]");
      if (count) count.textContent = `${done} of ${total} complete`;
      const bar = summary.querySelector("[role=progressbar]");
      if (bar) {
        bar.setAttribute("aria-valuemax", String(total));
        bar.setAttribute("aria-valuenow", String(done));
        const fill = bar.querySelector("span");
        if (fill) fill.style.width = total ? `${(100 * done) / total}%` : "0%";
      }
    });
  }

  document.addEventListener("click", event => {
    const button = event.target.closest("[data-complete]");
    if (!button) return;
    const id = button.dataset.complete;
    state = load();
    if (isDone(id)) delete state.completed[id];
    else state.completed[id] = new Date().toISOString();
    save(state);
    render();
  });

  /* Another script on this page recorded an item (the final exam does). */
  window.addEventListener("battery-core-progress", () => {
    state = load();
    render();
  });

  /* Another tab marked something complete: follow it. */
  window.addEventListener("storage", event => {
    if (event.key === KEY) {
      state = load();
      render();
    }
  });

  document.querySelectorAll("[data-progress-ui][hidden]").forEach(el => {
    el.hidden = false;
  });
  render();
})();
