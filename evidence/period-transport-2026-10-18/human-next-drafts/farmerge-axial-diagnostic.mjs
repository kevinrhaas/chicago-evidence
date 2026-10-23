/**
 * WHAT THE FAR MERGE SAVES, AND WHAT IT COSTS — read off the same frame twice.
 *
 *   PW_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
 *     node tools/measure_far_merge.mjs [--tiers full,balanced,light]
 *                                      [--only desktop|mobile|both]
 *                                      [--source] [--json f]
 *
 * T-0146's instrument. The claim the merge makes is a narrow one and it has two
 * halves, so it is measured in one page load with the merge turned OFF and back
 * ON at each of T-0135's five stands:
 *
 *   * **calls go down** — the thing it is for;
 *   * **triangles do not move, at all** — the thing that makes it free. A merge
 *     is only allowed while its cluster is wholly inside the frustum, so the
 *     same triangles are submitted either way and the delta must be exactly 0.
 *     A non-zero triangle delta here is the bug, not a tolerance.
 *
 * Turning the merge off and reading the same frame is the method T-0150's reach
 * gate uses and for its reason: a figure taken from two different trees can be
 * satisfied by any unrelated layer getting cheaper, and this one has to be
 * attributable by construction. `a.setFarMerge(false)` is harness-only and is
 * never a visitor setting.
 *
 * Defaults to the PUBLISHED mirror for the reason every renderer measurement
 * here does — the site loads the compressed derivatives. `--source` reads the
 * working tree instead.
 *
 * This is a measurement and not a gate; `tools/smoke_renderer.mjs` holds the
 * ceilings.
 */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

async function loadPlaywright() {
  let ns;
  try {
    ns = await import('playwright');
  } catch {
    const root = (process.env.NODE_PATH
      || execSync('npm root -g', { encoding: 'utf8' })).trim().split(path.delimiter)[0];
    ns = await import(path.join(root, 'playwright', 'index.js'));
  }
  return ns.chromium ? ns : ns.default;
}
const { chromium } = await loadPlaywright();

const HERE = '/workspace/chicago/chicago/4d/tools';
const argAt = (name) => {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] : null;
};
const wantSource = process.argv.includes('--source');
const jsonOut = argAt('--json');
const ONLY = argAt('--only') || 'desktop';
const TIERS = (argAt('--tiers') || 'full,balanced,light').split(',').map((s) => s.trim());

/** T-0135's stands, by the ids `tools/smoke_renderer.mjs` gives them.
 *
 * T-1580 — the axial stand targets the `lake_at_canal` ANCHOR, not `green_tree`.
 * It named the Green Tree's viewpoint, which was at Lake and Canal looking east
 * until T-0141 moved the inn 116 m and moved its viewpoint with it; from
 * 2026-09-24 every figure this tool recorded at "Lake Street at Canal" was taken
 * from across Lake Street at the inn's new front, and the merge read 0 of 21
 * clusters there. The ground now has its own authored anchor at the coordinates
 * the 201 -> 147 reading was taken at. The same repoint is in six sibling
 * measure_*.mjs tools, which carried the identical stand.
 */
const STANDS = [
  { id: 'lake_at_canal', kind: 'anchor', target: 'lake_at_canal',
    label: 'Lake Street at Canal, east down the axis' },
  { id: 'the_forks', kind: 'anchor', target: 'forks', label: 'the forks, from Wolf Point' },
  { id: 'from_above', kind: 'anchor', target: 'from_above', label: 'the open aerial' },
  { id: 'lake_and_market', kind: 'anchor', target: 'lake_market', label: 'Lake and Market' },
  { id: 'sauganash_26', kind: 'frame', target: 'sauganash_hotel', distance: 26,
    label: 'the Sauganash at 26 m' },
];

const VIEWPORTS = [
  { label: 'desktop 1280x800', width: 1280, height: 800 },
  { label: 'mobile 390x780', width: 390, height: 780 },
].filter((v) => ONLY === 'both' || v.label.startsWith(ONLY));

const TYPES = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.glb': 'model/gltf-binary',
  '.bin': 'application/octet-stream', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.wasm': 'application/wasm', '.md': 'text/markdown',
};

const ROOT = wantSource
  ? path.resolve(HERE, '..')
  : path.resolve(HERE, '../../../site/4d');
const ENTRY = wantSource ? '/renderers/web/index.html' : '/walk/';
if (!wantSource && !fs.existsSync(path.join(ROOT, 'walk', 'index.html'))) {
  console.error(`no published mirror at ${ROOT} — run tools/publish.sh first`);
  process.exit(2);
}
const PORT = Number(process.env.FAR_MERGE_PORT || 4207);
const server = http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split('?')[0]);
  let file = path.join(ROOT, url);
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!file.startsWith(ROOT) || !fs.existsSync(file)) {
    res.writeHead(404, { 'content-type': 'text/plain' });
    res.end(`not found: ${url}`);
    return;
  }
  res.writeHead(200, { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
await new Promise((r) => server.listen(PORT, r));
console.log(`serving ${ROOT} — ${wantSource ? 'source tree' : 'PUBLISHED mirror'}\n`);

const browser = await chromium.launch({
  executablePath: process.env.PW_EXECUTABLE || undefined,
  args: ['--enable-unsafe-swiftshader'],
});

try {
const page=await browser.newPage({viewport:{width:390,height:780}});
const errors=[];page.on('pageerror',e=>errors.push(String(e)));
await page.goto(`http://127.0.0.1:${PORT}${ENTRY}?year=1835`,{waitUntil:'load'});
await page.waitForFunction(()=>window.__chicago4d?.ready===true,null,{timeout:300000});
const result=await page.evaluate(async()=>{
 const a=window.__chicago4d;const settle=()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
 await a.setDetail('full');a.goTo('lake_at_canal');await settle();
 const naturalOn={stats:a.stats(),governor:a.governor};
 a.setFarMerge(false);await settle();const naturalOff={stats:a.stats(),governor:a.governor};
 a.setFarMerge(true);await settle();const naturalAgain={stats:a.stats(),governor:a.governor};
 const renderer=a.renderer;const original=renderer.renderBufferDirect;
 let draws={};
 renderer.renderBufferDirect=function(camera,scene,geometry,material,object,group){
   const before={calls:this.info.render.calls,triangles:this.info.render.triangles};
   const result=original.call(this,camera,scene,geometry,material,object,group);
   let layer=object;while(layer.parent&&layer.parent!==a.scene3d)layer=layer.parent;
   const key=(camera===a.camera?'main:':'shadow:')+(layer.name||layer.type||'unnamed');
   const row=draws[key]??={calls:0,triangles:0};
   row.calls+=this.info.render.calls-before.calls;row.triangles+=this.info.render.triangles-before.triangles;
   return result;
 };
 const forced=(enabled)=>{a.setFarMerge(enabled);draws={};a.step();return {stats:a.stats(),draws,governor:a.governor,merge:a.farMerge,shadowAutoUpdate:renderer.shadowMap.autoUpdate};};
 const forcedOn=forced(true),forcedOff=forced(false),forcedAgain=forced(true);
 renderer.renderBufferDirect=original;
 return {naturalOn,naturalOff,naturalAgain,forcedOn,forcedOff,forcedAgain};
});
fs.writeFileSync(jsonOut||'/tmp/farmerge-axial-diagnostic.json',JSON.stringify({result,errors},null,2));
console.log(JSON.stringify({errors,naturalDelta:result.naturalOff.stats.triangles-result.naturalOn.stats.triangles,naturalResidual:result.naturalAgain.stats.triangles-result.naturalOn.stats.triangles,forcedDelta:result.forcedOff.stats.triangles-result.forcedOn.stats.triangles,forcedResidual:result.forcedAgain.stats.triangles-result.forcedOn.stats.triangles,forcedCallsSaved:result.forcedOff.stats.drawCalls-result.forcedOn.stats.drawCalls},null,2));
await page.close();
} finally {await browser.close();server.close();}
