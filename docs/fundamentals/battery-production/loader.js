(() => {
  const parts = [
    "payload/source-01.part", "payload/source-02.part",
    "payload/source-03.part", "payload/source-04.part",
    "payload/source-05.part", "payload/source-06.part",
    "payload/source-07.part", "payload/source-08.part",
    "payload/source-09.part", "payload/source-10.part",
    "payload/source-11.part", "payload/source-12.part",
    "payload/source-13.part", "payload/source-14.part",
    "payload/source-15.part", "payload/source-16.part",
    "payload/source-17.part", "payload/source-18.part",
    "payload/source-19.part", "payload/source-20.part",
    "payload/source-21.part", "payload/source-22.part",
    "payload/source-23.part", "payload/source-24.part",
    "payload/source-25.part", "payload/source-26.part",
  ];
  const status = document.getElementById("load-status");

  // The payload replaces the whole document, so the shared chrome has to be
  // put back afterwards rather than sitting in this page's own markup.
  function injectChrome() {
    const head = document.head || document.documentElement;
    ["../../assets/module-theme.css", "../../assets/site-chrome.css"].forEach(href => {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = href;
      head.appendChild(link);
    });
    const icon = document.createElement("link");
    icon.rel = "icon";
    icon.type = "image/svg+xml";
    icon.href = "../../assets/favicon.svg";
    head.appendChild(icon);
    const bar = document.createElement("div");
    bar.className = "bc-modulebar";
    bar.innerHTML = '<span class="bc-modulebar-part">Part 03 &middot; Chapter 1</span>' +
      '<span>Lithium-ion battery production</span>' +
      '<span class="bc-modulebar-spacer"></span>' +
      '<a href="../../">Course home</a>' +
      '<a href="../../chapter-1/">Chapter 1</a>';
    document.body.insertBefore(bar, document.body.firstChild);
    const footer = document.createElement("footer");
    footer.className = "bc-footer";
    footer.innerHTML = '<p>Battery Core \u00b7 A project of Lemonergy</p>' +
      '<div class="bc-footer-links">' +
      '<a href="../../">Course home</a>' +
      '<a href="../../license/">AGPL-3.0-or-later</a>' +
      '<a href="../../license/#commercial">Commercial use</a>' +
      '</div>';
    document.body.appendChild(footer);
  }

  async function boot() {
    try {
      const responses = await Promise.all(parts.map(path => fetch(path)));
      const failed = responses.find(response => !response.ok);
      if (failed) throw new Error(`Could not load ${failed.url} (${failed.status})`);
      const html = (await Promise.all(responses.map(response => response.text()))).join("");
      document.open();
      document.write(html);
      document.close();
      injectChrome();
    } catch (error) {
      console.error(error);
      if (status) status.textContent = "The simulator source could not be loaded. Serve the docs directory over HTTP and reload this page.";
    }
  }

  boot();
})();
