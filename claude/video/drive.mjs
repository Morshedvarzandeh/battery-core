import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';

const URL = 'http://127.0.0.1:8765/fundamentals/battery-production/';
const OUT = './rec';
fs.rmSync(OUT, { recursive: true, force: true });

const b = await chromium.launch({ args: ['--force-device-scale-factor=1'] });
const ctx = await b.newContext({
  viewport: { width: 1080, height: 1920 },
  deviceScaleFactor: 1,
  recordVideo: { dir: OUT, size: { width: 1080, height: 1920 } }
});
const t0 = Date.now();
const p = await ctx.newPage();
const errs = [];
p.on('pageerror', e => errs.push(e.message));

const marks = [];
let t0page = null;
const mark = (label) => marks.push({ label, t: (Date.now() - t0page) / 1000 });
const wait = ms => p.waitForTimeout(ms);

await p.goto(URL, { waitUntil: 'networkidle' });
await p.waitForSelector('#sliders input', { state: 'attached' });
// zoom so the compact (drawer) layout is used and text reads on a phone
await p.evaluate(() => { document.documentElement.style.zoom = '1.7'; });
await p.addStyleTag({ content: `
  *{scrollbar-width:none!important}
  ::-webkit-scrollbar{display:none!important}
` });
await wait(900);

// helpers injected once
await p.evaluate(() => {
  window.__scrollTo = (frac, ms) => new Promise(res => {
    const max = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    const y = max * frac;
    const s = window.scrollY, d = y - s, t = performance.now();
    const ease = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
    const step = now => {
      const k = Math.min(1, (now - t) / ms);
      window.scrollTo(0, s + d * ease(k));
      k < 1 ? requestAnimationFrame(step) : res();
    };
    requestAnimationFrame(step);
  });
  window.__setSlider = (id, to, ms) => new Promise(res => {
    const el = document.getElementById(id);
    const from = Number(el.value), t = performance.now();
    const step = now => {
      const k = Math.min(1, (now - t) / ms);
      el.value = String(from + (to - from) * k);
      el.dispatchEvent(new Event('input', { bubbles: true }));
      k < 1 ? requestAnimationFrame(step) : res();
    };
    requestAnimationFrame(step);
  });
});

t0page = Date.now();
mark('START');

/* ---- A · the overview, top to line map ---------------------------------- */
mark('A');
await wait(1600);
await p.evaluate(() => window.__scrollTo(0.16, 2200));
await wait(2500);
await p.evaluate(() => window.__scrollTo(0.42, 2400));
await wait(2700);

/* ---- B · open one station ----------------------------------------------- */
mark('B');
await p.evaluate(() => window.__scrollTo(0, 500));
await wait(600);
await p.click('#navBtn');
await wait(1100);
await p.click('#stationDrawer [data-go="calendering"]');
await wait(1800);
await p.evaluate(() => window.__scrollTo(0.10, 1200));
await wait(1800);

/* ---- C · the setpoint lab, live ----------------------------------------- */
mark('C');
await p.click('#labBtn');
await wait(1400);
await p.evaluate(() => {
  const el = document.getElementById('sl-force');
  el.scrollIntoView({ block: 'center', behavior: 'smooth' });
});
await wait(1200);
mark('C2');
await p.evaluate(() => window.__setSlider('sl-force', 2500, 3200));
await wait(3600);
await wait(1400);

/* ---- D · the station reacts --------------------------------------------- */
mark('D');
await p.click('#labClose');
await wait(900);
await p.evaluate(() => {
  const v = document.querySelector('#console .verdict');
  if (v) v.scrollIntoView({ block: 'center', behavior: 'smooth' });
});
await wait(2600);

/* ---- E · the whole line, with lamps -------------------------------------- */
mark('E');
await p.click('#navBtn');
await wait(900);
await p.click('#stationDrawer [data-go="view:machine"]');
await wait(1600);
await p.evaluate(() => window.__scrollTo(0.40, 2000));
await wait(2200);
await p.evaluate(() => window.__scrollTo(0.62, 1600));
await wait(2000);

/* ---- F · cell anatomy ---------------------------------------------------- */
mark('F');
await p.click('#navBtn');
await wait(800);
await p.click('#stationDrawer [data-go="view:anatomy"]');
await wait(1500);
await p.evaluate(() => window.__scrollTo(0.28, 1500));
await wait(1700);
await p.evaluate(() => {
  const b = document.querySelector('.layerlist [data-layer="sei"]');
  if (b) b.click();
});
await wait(1800);

/* ---- G · material flow --------------------------------------------------- */
mark('G');
await p.click('#navBtn');
await wait(800);
await p.click('#stationDrawer [data-go="view:flow"]');
await wait(1400);
await p.evaluate(() => window.__scrollTo(0.38, 2400));
await wait(2600);

/* ---- H · the line rebuilds ----------------------------------------------- */
mark('H');
await p.evaluate(() => window.__scrollTo(0, 500));
await p.click('#navBtn');
await wait(1000);
await p.click('#routeOpts [data-route="cyl"]');
await wait(1500);
await p.click('#procOpts [data-proc="dry"]');
await wait(2200);

/* ---- I · radar and factory ----------------------------------------------- */
mark('I');
await p.click('#stationDrawer [data-go="view:radar"]');
await wait(1800);
await p.evaluate(() => window.__scrollTo(0.26, 1800));
await wait(2000);
mark('I2');
await p.click('#navBtn');
await wait(700);
await p.click('#stationDrawer [data-go="view:factory"]');
await wait(1600);
await p.evaluate(() => window.__scrollTo(0.44, 2200));
await wait(2400);

mark('END');
const total = (Date.now() - t0page) / 1000;
const preroll = (t0page - t0) / 1000;
await ctx.close();
await b.close();

const video = fs.readdirSync(OUT).find(f => f.endsWith('.webm'));
fs.writeFileSync('./timeline.json', JSON.stringify({ preroll, total, marks, video, errs }, null, 1));
console.log(JSON.stringify({ preroll, total, video, errs }, null, 1));
console.log(marks.map(m => `${m.label}\t${m.t.toFixed(2)}`).join('\n'));
