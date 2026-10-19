/* Battery Core — lab pages shown inside a lesson.
 *
 * The interactive labs (the cell-anatomy workbench, the architecture tutorial)
 * are full pages in their own right, with the course bar, the "next" bar and
 * the footer. A lesson page also shows the same lab in a frame, and there the
 * lesson already provides all of that. This marks the document as embedded,
 * so `site-chrome.css` and the lab's own stylesheet can hide the duplicates.
 *
 * Load it in <head>, before the stylesheets apply, so nothing flashes:
 *
 *     <script src="../../assets/embed.js"></script>
 */
(function () {
  "use strict";
  var embedded;
  try {
    embedded = window.self !== window.top;
  } catch (error) {
    embedded = true; // a cross-origin parent: certainly framed
  }
  if (embedded) document.documentElement.setAttribute("data-embedded", "");
})();
