/* Battery Core — size a lab frame to the lab inside it.
 *
 * A lesson shows an interactive lab in an <iframe data-fit>. A fixed height
 * either clips the lab or leaves a gap under it, and the right height changes
 * with the screen width and with what the reader opens inside the lab. The
 * lab is served from the same site, so the lesson can measure it directly and
 * follow it as it changes. Without JavaScript the frame keeps the height set
 * in the HTML and scrolls, which still works.
 */
(() => {
  "use strict";

  function contentHeight(doc) {
    const body = doc.body;
    if (!body) return 0;
    const style = doc.defaultView.getComputedStyle(body);
    const margins = parseFloat(style.marginTop) + parseFloat(style.marginBottom);
    return Math.ceil(body.getBoundingClientRect().height + margins);
  }

  function fit(frame) {
    let doc;
    try {
      doc = frame.contentDocument;
    } catch (error) {
      return; // not same-origin: keep the height from the HTML
    }
    if (!doc || !doc.body) return;
    const height = contentHeight(doc);
    if (height > 0) frame.style.height = `${height}px`;
  }

  function watch(frame) {
    let observer = null;
    const attach = () => {
      fit(frame);
      if (observer) observer.disconnect();
      let doc;
      try {
        doc = frame.contentDocument;
      } catch (error) {
        return;
      }
      if (!doc || !doc.body || !("ResizeObserver" in window)) return;
      observer = new ResizeObserver(() => fit(frame));
      observer.observe(doc.body);
    };
    frame.addEventListener("load", attach);
    if (frame.contentDocument && frame.contentDocument.readyState === "complete") attach();
  }

  document.querySelectorAll("iframe[data-fit]").forEach(watch);
})();
