const { chromium } = require('playwright');
const fs = require('fs');
const out = process.argv[2];
const cases = [
  { id: 'where-attack', year: '1812', file: 'battle-of-fort-dearborn-grades-3-5', pick: [0, 1],
    claim: 'The officers wrote down the distance soon after: about one and a half or two miles. The Kinzie tree came much later.',
    unc: 'Heald gives two different distances, and the tree was pointed out about seventy years later.' },
  { id: 'trading-post', year: '1812', file: 'killing-of-jean-lalime-grades-9-10', pick: [1],
    claim: 'The deed record, as the Reader reports it, names Lalime as the buyer, with Kinzie as a witness.',
    unc: 'I have only the Reader’s report of the deed, not the deed itself.' },
  { id: 'chappel', year: '1835', file: 'schoolday-errand-grades-11-12', pick: [0, 2],
    claim: 'Chappel taught in a log house near the reservation line, but its exact lot is unknown.',
    unc: 'The 2018 history has no footnotes, and other accounts place the room elsewhere.' },
  { id: 'bronze-rescue', year: '1904', file: 'bronze-at-eighteenth', pick: [1, 2],
    claim: 'The bronze shows how Chicago remembered 1812 in 1893, more than what happened.',
    unc: 'A historian reports the doubt; I have not read the eyewitness accounts myself.' },
];
const sizes = [{ name: 'desktop', width: 1280, height: 800 }, { name: 'mobile', width: 390, height: 780 }];
(async () => {
  const browser = await chromium.launch(process.env.PW_EXECUTABLE ? { executablePath: process.env.PW_EXECUTABLE } : {});
  const report = [];
  for (const c of cases) for (const size of sizes) {
    const ctx = await browser.newContext({ viewport: { width: size.width, height: size.height }, deviceScaleFactor: 2 });
    const page = await ctx.newPage(); const errors = [];
    page.on('pageerror', e => errors.push(String(e))); page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(`http://127.0.0.1:${process.env.PORT}/web-fixture.html?year=${c.year}&file=${c.file}`);
    await page.waitForFunction(() => window.__ready === true);
    const hasModel = await page.evaluate(() => !!window.__model);
    if (!hasModel) { report.push({ c: c.id, size: size.name, error: 'no model' }); await ctx.close(); continue; }
    const boxes = page.locator('.jaunt-investigation-choice input');
    for (const i of c.pick) await boxes.nth(i).check();
    await page.fill('textarea[data-investigation-field="claim"]', c.claim);
    await page.fill('textarea[data-investigation-field="uncertainty"]', c.unc);
    await page.getByRole('button', { name: 'Review the sources' }).click();
    await page.getByRole('button', { name: 'Save to notebook' }).click();
    const status = await page.locator('.jaunt-investigation-status').textContent();
    await page.screenshot({ path: `${out}/${c.id}-case-${size.name}.png`, fullPage: true });
    // The viewport-sized top of the case: question, readings and the first evidence choices.
    await page.locator('.jaunt-investigation h4').first().scrollIntoViewIfNeeded();
    await page.screenshot({ path: `${out}/${c.id}-top-${size.name}.png` });
    await page.evaluate(() => { document.getElementById('gate').hidden = true; window.__mountNotebook(); });
    await page.locator('.field-notebook-entry details').first().evaluate(d => { d.open = true; });
    await page.locator('#field-notebook').screenshot({ path: `${out}/${c.id}-notebook-${size.name}.png` });
    const html = await page.evaluate(() => window.__exportHTML());
    const ex = await ctx.newPage(); await ex.setContent(html); await ex.screenshot({ path: `${out}/${c.id}-export-${size.name}.png`, fullPage: true }); await ex.close();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    report.push({ c: c.id, size: size.name, status, overlay: await page.evaluate(() => window.__overlay), overflow, errors });
    await ctx.close();
  }
  await browser.close();
  console.log(JSON.stringify(report, null, 1));
})();
