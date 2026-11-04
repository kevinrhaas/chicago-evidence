import fs from 'node:fs';
import assert from 'node:assert/strict';
const base = new URL('./', import.meta.url);
const read = p => fs.readFileSync(new URL(p, base), 'utf8');
const candidate = read('candidate/chicago/4d/tools/smoke_renderer.mjs');
const original = read('source/tools/smoke_renderer.mjs');
const prefix = 'const drawer = await page.evaluate(() => {';
function parts(text) {
  const start = text.indexOf(prefix, text.indexOf('// T-1740 — the drawer'));
  assert(start >= 0); const end = text.indexOf('\n        });', start); assert(end > start);
  const collect = new Function('window', 'document', text.slice(start + prefix.length, end));
  const beginCheck = text.indexOf("!drawer.tabs.includes('people')", end);
  const endCheck = text.indexOf(',\n          JSON.stringify(drawer)', beginCheck);
  assert(endCheck > beginCheck);
  const check = new Function('drawer', 'gone', `return (${text.slice(beginCheck, endCheck)});`);
  return { collect, check };
}
const before = parts(original), after = parts(candidate);
const tabs = ['travel', 'evidence', 'settings', 'controls', 'whatsnew'];
const tiles = ['grades', 'sources', 'liberties', 'ground'];
const gone = ['city', 'fauna', 'plants', 'exclusions', 'uncertain', 'population', 'orderbook'];
function run(parts, api, extraTabs = [], extraTiles = []) {
  const a = { destinations: { targets: [] }, hud: { tab: 'controls', selectTab() {} }, ...api };
  const document = { querySelectorAll(selector) {
    if (selector === '.panel-tab') return [...tabs, ...extraTabs].map(tab => ({ hidden: false, dataset: { tab } }));
    if (selector === '#evidence-hub .ev-tile') return [...tiles, ...extraTiles].map(topic => ({ dataset: { topic } }));
    throw Error('Unexpected actual selector ' + selector);
  } };
  const drawer = parts.collect({ __chicago4d: a }, document);
  return { pass: parts.check(drawer, gone), drawer };
}
const adapter = { people: { open() {} } };
assert.equal(run(before, adapter).pass, false, 'Original predicate reproduces adapter-key failure');
assert.equal(run(after, adapter).pass, true, 'Intentional 1904 adapter is not a legacy mounted module');
const controls = [
  ['actual mountPeople zero-count/error return contract', { people: { people: 0, error: 'no mount', open() {}, search() {} } }],
  ['actual mountPeople nonempty return contract', { people: { people: 3308, error: null, open() {}, search() {} } }],
  ['other legacy resident module', { ...adapter, residents: {} }],
  ['missing public person-card route', {}],
  ['visible legacy People tab', adapter, ['people']],
  ['forbidden legacy Evidence tile', adapter, [], ['city']],
  ['legacy firm leak', { ...adapter, destinations: { targets: [{ kind: 'business' }] } }],
];
for (const [name, api, tabs, tiles] of controls) assert.equal(run(after, api, tabs, tiles).pass, false, name);
console.log(JSON.stringify({ scope: 'Actual original/candidate Stage14 collection callback and boolean assertion with controlled API/DOM data; NOT browser or runtime PASS', originalAdapterRejected: true, candidateAdapterAccepted: true, negativeControlsRejected: controls.map(c => c[0]), main1904AdapterUnchanged: true }, null, 2));
