(() => {
  const parts = ['payload/source-01.part', 'payload/source-02.part', 'payload/source-03.part', 'payload/source-04a.part', 'payload/source-04b.part', 'payload/source-05.part', 'payload/source-06.part', 'payload/source-07.part', 'payload/source-08.part', 'payload/source-09.part', 'payload/source-10.part', 'payload/source-11.part', 'payload/source-12.part', 'payload/source-13.part', 'payload/source-14.part', 'payload/source-15.part', 'payload/source-16.part', 'payload/source-17.part', 'payload/source-18.part'];
  const deltaParts = [
    'payload/review-2026-s01.delta',
    'payload/review-2026-s02.delta',
    'payload/review-2026-s03.delta',
    'payload/review-2026-s04.delta',
    'payload/review-2026-s05.delta',
    'payload/review-2026-s06.delta',
    'payload/review-2026-s07.delta',
    'payload/review-2026-s08.delta'
  ];
  const status = document.getElementById("load-status");

  async function unpackDelta(base64Text) {
    if (!("DecompressionStream" in window)) {
      throw new Error("This browser does not support gzip decompression.");
    }
    const binary = atob(base64Text.replace(/\s+/g, ""));
    const bytes = Uint8Array.from(binary, character => character.charCodeAt(0));
    const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
    return JSON.parse(await new Response(stream).text());
  }

  function normalizeReviewBase(source) {
    return source.replace(
      /<h1 class="sr">CellForge — Lithium-ion Cell Production Simulator<\/h1>\r?\n?/,
      ""
    );
  }

  function applyLineDelta(source, operations) {
    const lines = source.match(/.*(?:\n|$)/g) || [];
    if (lines.at(-1) === "") lines.pop();
    for (let index = operations.length - 1; index >= 0; index -= 1) {
      const [start, end, replacement] = operations[index];
      lines.splice(start, end - start, ...replacement);
    }
    return lines.join("");
  }

  async function boot() {
    try {
      const responses = await Promise.all([...parts, ...deltaParts].map(path => fetch(path)));
      const failed = responses.find(response => !response.ok);
      if (failed) throw new Error(`Could not load ${failed.url} (${failed.status})`);
      const sourceResponses = responses.slice(0, parts.length);
      const deltaResponses = responses.slice(parts.length);
      const source = normalizeReviewBase(
        (await Promise.all(sourceResponses.map(response => response.text()))).join("")
      );
      const packedDelta = (await Promise.all(deltaResponses.map(response => response.text()))).join("");
      const operations = await unpackDelta(packedDelta);
      const html = applyLineDelta(source, operations);
      document.open();
      document.write(html);
      document.close();
    } catch (error) {
      console.error(error);
      if (status) status.textContent = "The simulator source could not be loaded. Use a current browser, serve the docs directory over HTTP, and reload this page.";
    }
  }

  boot();
})();
