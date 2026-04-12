const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const OUT_DIR = path.join(ROOT, 'ops', 'checklists');
const OUT_JSON = path.join(OUT_DIR, 'browser_qa_report.json');
const OUT_MD = path.join(OUT_DIR, 'browser_qa_report.md');
const BASE = 'https://dishadc.github.io/field-feather-co';

(async () => {
  const generatedAt = new Date().toISOString();
  const results = [];
  let overall = 'PASS';
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  const pageErrors = [];
  const consoleErrors = [];
  page.on('pageerror', err => pageErrors.push(String(err)));
  page.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });

  async function record(name, fn) {
    const item = { name, status: 'PASS' };
    try {
      const extra = await fn();
      Object.assign(item, extra || {});
    } catch (e) {
      item.status = 'FAIL';
      item.error = String(e.message || e);
      overall = 'FAIL';
    }
    if (item.status !== 'PASS') overall = 'FAIL';
    results.push(item);
  }

  await record('home_page', async () => {
    await page.goto(`${BASE}/?qa=1`, { waitUntil: 'networkidle' });
    await page.waitForSelector('h1');
    const hero = await page.locator('h1').textContent();
    if (!hero.includes('Paper goods for the birder')) throw new Error('Hero headline mismatch');
    const seasonal = await page.locator('#live-count').textContent();
    return { hero, seasonal };
  });

  await record('theme_toggle', async () => {
    const before = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    await page.click('[data-theme-toggle]');
    const after = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    if (before === after) throw new Error('Theme did not toggle');
    return { before, after };
  });

  await record('shop_filters', async () => {
    await page.goto(`${BASE}/shop.html?qa=1`, { waitUntil: 'networkidle' });
    await page.waitForSelector('#shop-grid article');
    const count = await page.locator('#shop-grid article').count();
    if (count < 5) throw new Error(`Unexpected product count: ${count}`);
    await page.fill('#filter-q', 'Texas');
    await page.waitForTimeout(300);
    const filteredTitles = await page.locator('#shop-grid .product-title').allTextContents();
    if (!filteredTitles.length || !filteredTitles.every(t => t.toLowerCase().includes('texas'))) {
      throw new Error('Search filter did not narrow to Texas products');
    }
    return { initial_count: count, filtered_titles: filteredTitles };
  });

  await record('product_detail', async () => {
    await page.goto(`${BASE}/product.html?sku=DIGI-STATE-TEXAS&qa=1`, { waitUntil: 'networkidle' });
    await page.waitForSelector('#product-detail h1');
    const title = await page.locator('#product-detail h1').textContent();
    if (!title.includes('Texas Birding')) throw new Error('Product title mismatch');
    const related = await page.locator('#related-grid article').count();
    if (related < 1) throw new Error('Related products not rendered');
    await page.click('.tab-btn[data-tab="specs"]');
    const specsVisible = await page.locator('#tab-specs.active').count();
    if (!specsVisible) throw new Error('Specs tab did not activate');
    return { title, related_count: related };
  });

  await record('mobile_nav', async () => {
    const mobile = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const mobilePage = await mobile.newPage();
    await mobilePage.goto(`${BASE}/?qa=mobile`, { waitUntil: 'networkidle' });
    await mobilePage.click('[data-nav-toggle]');
    const expanded = await mobilePage.locator('[data-mobile-panel].open').count();
    if (!expanded) throw new Error('Mobile nav did not open');
    await mobile.close();
    return { opened: true };
  });

  await browser.close();

  if (pageErrors.length || consoleErrors.length) {
    overall = 'FAIL';
  }

  const payload = {
    generated_at_utc: generatedAt,
    status: overall,
    results,
    page_errors: pageErrors,
    console_errors: consoleErrors,
  };

  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(OUT_JSON, JSON.stringify(payload, null, 2) + '\n');

  const lines = [
    '# Browser QA Report',
    '',
    `Generated (UTC): ${generatedAt}`,
    '',
    `Overall status: ${overall}`,
    '',
    '## Flow checks',
  ];
  for (const item of results) {
    lines.push(`- ${item.name}: ${item.status}`);
    for (const [k, v] of Object.entries(item)) {
      if (['name', 'status'].includes(k)) continue;
      lines.push(`  - ${k}: ${Array.isArray(v) ? v.join(' | ') : v}`);
    }
  }
  lines.push('', '## JS runtime issues');
  lines.push(`- page errors: ${pageErrors.length}`);
  lines.push(`- console errors: ${consoleErrors.length}`);
  if (pageErrors.length) pageErrors.forEach(e => lines.push(`  - ${e}`));
  if (consoleErrors.length) consoleErrors.forEach(e => lines.push(`  - ${e}`));

  fs.writeFileSync(OUT_MD, lines.join('\n') + '\n');
  process.stdout.write(JSON.stringify({ status: overall, out_json: OUT_JSON, out_md: OUT_MD }));
})();
