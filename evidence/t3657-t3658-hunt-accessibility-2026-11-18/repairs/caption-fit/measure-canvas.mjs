import assert from 'node:assert/strict';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
const root = '/workspace/chicago-hunt/chicago/4d';
const before = '/tmp/t3658-resource-review/moment-before.js';
const after = path.join(root, 'renderers/web/js/moment.js');
const { chromium } = createRequire(path.join(root, 'tools/test_people_notebook.mjs'))('playwright');
const data = JSON.parse(fs.readFileSync(path.join(root, 'data/sidecars/1904/glessner_house.json')));
const metadata = { year: '1904', place: data.name, sourceSubject: data.name,
  sources: data.citations.filter(c => c.source_id && c.citation).map(c => ({ id: c.source_id, title: c.citation })) };
const server = http.createServer((req, res) => {
  const name = new URL(req.url, 'http://local').pathname;
  if (name === '/') { res.setHeader('Content-Type', 'text/html'); res.end('<!doctype html><html><body>Canvas-only caption timing fixture</body></html>'); return; }
  const file = name === '/js/moment-before.js' ? before : path.resolve(root, `renderers/web${name}`);
  if (file !== before && !file.startsWith(path.join(root, 'renderers/web/'))) { res.writeHead(403); res.end(); return; }
  fs.readFile(file, (error, bytes) => { res.writeHead(error ? 404 : 200, { 'Content-Type': 'text/javascript' }); res.end(error ? '' : bytes); });
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
let browser;
try {
  browser = await chromium.launch({ executablePath: '/usr/bin/chromium', args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 390, height: 780 } });
  const errors = []; page.on('pageerror', error => errors.push(error.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/`);
  const samples = await page.evaluate(async metadata => {
    const modules = { before: await import('/js/moment-before.js'), after: await import('/js/moment.js') };
    const source = document.createElement('canvas'); source.width = 390; source.height = 780;
    source.getContext('2d').fillRect(0, 0, source.width, source.height);
    const original = CanvasRenderingContext2D.prototype.measureText;
    const results = []; let calls = 0;
    CanvasRenderingContext2D.prototype.measureText = function(text) { calls++; return original.call(this, text); };
    try {
      for (let iteration = 0; iteration < 3; iteration++) for (const version of ['before', 'after']) {
        calls = 0;
        const start = performance.now();
        const pending = modules[version].stampMoment(source, metadata);
        const synchronousMs = performance.now() - start;
        const result = await pending;
        if (result.sources !== metadata.sources) throw Error('Source metadata changed');
        results.push({ iteration, version, calls, synchronousMs, blobBytes: result.blob.size });
      }
    } finally { CanvasRenderingContext2D.prototype.measureText = original; source.width = source.height = 1; }
    return results;
  }, metadata);
  assert.deepEqual(errors, []);
  assert(samples.filter(s => s.version === 'after').every(s => s.calls < 25));
  const report = { scope: 'Headless Chromium, real Canvas2D, 390x780 source; actual stampMoment before/after; no town or WebGL. Synchronous copy/caption time excludes PNG encoding; concurrent source gate may affect wall times.',
    browser: await browser.version(), captionChars: `Sources for ${metadata.sourceSubject}: ${metadata.sources.map(s => s.title).join('; ')}`.length,
    beforeSHA256: crypto.createHash('sha256').update(fs.readFileSync(before)).digest('hex'),
    afterSHA256: crypto.createHash('sha256').update(fs.readFileSync(after)).digest('hex'), samples, errors };
  fs.writeFileSync('/tmp/t3658-resource-review/canvas-timing.json', JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
} finally { if (browser) await browser.close(); await new Promise(resolve => server.close(resolve)); }
