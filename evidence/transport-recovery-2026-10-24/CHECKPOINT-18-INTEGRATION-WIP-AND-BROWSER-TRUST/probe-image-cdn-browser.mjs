import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire('/workspace/.cloud-setup/npm/package.json');
const { chromium } = require('playwright');
const resultPath = process.env.TRANSPORT_CDN_PROBE_RESULT || '/workspace/.cloud-setup/logs/transport-recovery/post-restart-image-browser-result.json';
if (fs.existsSync(resultPath)) throw new Error('Preserve previous probe; choose a fresh result path');
const browser = await chromium.launch({ executablePath: process.env.PW_EXECUTABLE, args: ['--enable-unsafe-swiftshader'] });
const result = { route: 'Actual Chromium HTTPS image navigation with normal certificate validation', errors: [] };
try {
  const page = await browser.newPage();
  page.on('requestfailed', r => result.errors.push(r.failure()?.errorText));
  const response = await page.goto('https://kevinrhaas.github.io/chicago-images/prairie-1904/files/a18-gh-courtyard-watercolor-thumb.jpg', { waitUntil: 'load', timeout: 60000 });
  result.status = response.status();
  result.image = await page.evaluate(() => ({ complete: document.images[0]?.complete, width: document.images[0]?.naturalWidth, height: document.images[0]?.naturalHeight }));
  result.pass = result.status === 200 && result.image.complete && result.image.width === 400 && result.errors.length === 0;
} catch (e) { result.pass = false; result.error = String(e); }
finally { await browser.close(); }
fs.writeFileSync(resultPath, JSON.stringify(result, null, 2)+'\n');
console.log(JSON.stringify(result));
if (!result.pass) process.exitCode = 1;
