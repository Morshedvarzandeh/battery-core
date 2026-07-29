(() => {
  const parts = ['payload/source-01.part', 'payload/source-02.part', 'payload/source-03.part', 'payload/source-04a.part', 'payload/source-04b.part', 'payload/source-05.part', 'payload/source-06.part', 'payload/source-07.part', 'payload/source-08.part', 'payload/source-09.part', 'payload/source-10.part', 'payload/source-11.part', 'payload/source-12.part', 'payload/source-13.part', 'payload/source-14.part', 'payload/source-15.part', 'payload/source-16.part', 'payload/source-17.part', 'payload/source-18.part'];
  const deltaPath = 'payload/review-2026.delta';
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
      const responses = await Promise.all([...parts, deltaPath].map(path => fetch(path)));
      const failed = responses.find(response => !response.ok);
      if (failed) throw new Error(`Could not load ${failed.url} (${failed.status})`);
      const source = (await Promise.all(responses.slice(0, -1).map(response => response.text()))).join("");
      const operations = await unpackDelta(await responses.at(-1).text());
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
