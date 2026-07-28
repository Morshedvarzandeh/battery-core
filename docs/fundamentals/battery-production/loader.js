(() => {
  const parts = ['payload/source-01.part', 'payload/source-02.part', 'payload/source-03.part', 'payload/source-04a.part', 'payload/source-04b.part', 'payload/source-05.part', 'payload/source-06.part', 'payload/source-07.part', 'payload/source-08.part', 'payload/source-09.part', 'payload/source-10.part', 'payload/source-11.part', 'payload/source-12.part', 'payload/source-13.part', 'payload/source-14.part', 'payload/source-15.part', 'payload/source-16.part', 'payload/source-17.part', 'payload/source-18.part'];
  const status = document.getElementById("load-status");

  async function boot() {
    try {
      const responses = await Promise.all(parts.map(path => fetch(path)));
      const failed = responses.find(response => !response.ok);
      if (failed) throw new Error(`Could not load ${failed.url} (${failed.status})`);
      const html = (await Promise.all(responses.map(response => response.text()))).join("");
      document.open();
      document.write(html);
      document.close();
    } catch (error) {
      console.error(error);
      if (status) status.textContent = "The simulator source could not be loaded. Serve the docs directory over HTTP and reload this page.";
    }
  }

  boot();
})();
