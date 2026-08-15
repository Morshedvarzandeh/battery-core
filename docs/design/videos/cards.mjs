import { chromium } from 'playwright';
import fs from 'node:fs';

const FONT = `"Liberation Sans","DejaVu Sans",sans-serif`;
const INK = '#1f2328', MUTED = '#59636e', BLUE = '#0969da', BG = '#f6f8fa';

const CAPS = [
  'Fifteen stations · powder to packed cell',
  'Open a station, get the machine',
  'Move one setpoint…',
  '…and the whole line answers',
  'One lamp per machine — from that station’s own verdict',
  'Nine components. The plant makes three.',
  'One material, fourteen states',
  'Change the format or the electrode route — the line rebuilds',
  '44 technologies, scored against series production',
  'The building, the air, and the bill'
];

const capHTML = t => `<!doctype html><meta charset="utf-8"><style>
 html,body{margin:0;width:1080px;height:300px;background:transparent}
 .wrap{display:flex;align-items:center;justify-content:center;height:100%;padding:0 54px;box-sizing:border-box}
 .cap{font:800 46px/1.24 ${FONT};color:#fff;background:rgba(20,24,28,.92);
      padding:26px 34px;border-radius:22px;text-align:center;letter-spacing:-.01em;
      box-shadow:0 18px 50px rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.14)}
</style><div class="wrap"><div class="cap">${t}</div></div>`;

const title = `<!doctype html><meta charset="utf-8"><style>
 html,body{margin:0;width:1080px;height:1920px;background:${BG};font-family:${FONT}}
 .p{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 96px}
 .mark{width:132px;height:132px;border-radius:34px;background:${INK};color:#fff;
   display:flex;align-items:center;justify-content:center;font:900 54px/1 ${FONT};letter-spacing:.02em;margin-bottom:56px}
 h1{font:900 116px/1.02 ${FONT};color:${INK};margin:0 0 30px;letter-spacing:-.035em}
 h2{font:700 54px/1.28 ${FONT};color:${MUTED};margin:0 0 60px;letter-spacing:-.015em}
 .rule{height:8px;width:176px;background:${BLUE};border-radius:4px;margin-bottom:52px}
 p{font:500 34px/1.5 ${FONT};color:${MUTED};margin:0;max-width:820px}
 b{color:${INK}}
 .pill{display:inline-block;margin-top:56px;font:800 28px/1 ${FONT};letter-spacing:.14em;
   color:${BLUE};border:2px solid ${BLUE};border-radius:999px;padding:18px 28px}
</style><div class="p">
 <div class="mark">CF</div>
 <h1>CellForge</h1>
 <h2>A lithium-ion cell production line,<br>simulated in the browser.</h2>
 <div class="rule"></div>
 <p>Fifteen stations from powder to packed cell — every one drawn as the machine you would
 stand next to, with a live setpoint lab wired to all of them.</p>
 <span class="pill">GRAPHITE / NMC REFERENCE ROUTE</span>
</div>`;

const end = `<!doctype html><meta charset="utf-8"><style>
 html,body{margin:0;width:1080px;height:1920px;background:${INK};font-family:${FONT};color:#fff}
 .p{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 96px}
 h1{font:900 76px/1.1 ${FONT};margin:0 0 34px;letter-spacing:-.03em}
 .rule{height:8px;width:176px;background:${BLUE};border-radius:4px;margin:0 0 44px}
 p{font:500 33px/1.55 ${FONT};color:#c9d1d9;margin:0 0 30px;max-width:840px}
 .src{font:700 27px/1.5 ${FONT};color:#8b949e;margin-top:26px}
 .url{font:800 30px/1.4 ${FONT};color:#79c0ff;margin-top:44px;word-break:break-all}
</style><div class="p">
 <h1>A teaching model —<br>not a plant prediction.</h1>
 <div class="rule"></div>
 <p>“Published sources support the process sequence and displayed operating ranges.
 Capacity, throughput, wetting, process-health and risk-control outputs are illustrative
 teaching relationships. They are not calibrated plant predictions, equipment-sizing
 calculations or release criteria.”</p>
 <p class="src">Process data after PEM RWTH Aachen &amp; VDMA,<br>
 <i>Production Process of a Lithium-Ion Battery Cell</i>, 5th ed., February 2026.</p>
 <div class="url">morshedvarzandeh.github.io/battery-core</div>
</div>`;

const b = await chromium.launch();
const ctx = await b.newContext({ deviceScaleFactor: 1 });
const p = await ctx.newPage();

await p.setViewportSize({ width: 1080, height: 1920 });
await p.setContent(title); await p.waitForTimeout(250);
await p.screenshot({ path: 'card-title.png' });
await p.setContent(end); await p.waitForTimeout(250);
await p.screenshot({ path: 'card-end.png' });

await p.setViewportSize({ width: 1080, height: 300 });
for (let i = 0; i < CAPS.length; i++) {
  await p.setContent(capHTML(CAPS[i]));
  await p.waitForTimeout(120);
  await p.screenshot({ path: `cap-${String(i + 1).padStart(2, '0')}.png`, omitBackground: true });
}
await b.close();
console.log('cards written:', fs.readdirSync('.').filter(f => f.startsWith('cap-') || f.startsWith('card-')).join(' '));
