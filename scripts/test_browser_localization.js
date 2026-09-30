const {chromium} = require('playwright');
const {createServer} = require('./preview_server');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

(async () => {
  const server = createServer();
  console.log('Starting browser verification');
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
  const browser = await chromium.launch({executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || (fs.existsSync(chrome) ? chrome : undefined), headless: true});
  const context = await browser.newContext({viewport: {width: 1366, height: 900}, locale: 'en-US'});
  console.log('Chrome ready');
  // Third-party ads and analytics are not needed to verify local navigation.
  await context.route('**/*', route => new URL(route.request().url()).origin === base ? route.continue() : route.abort());
  const page = await context.newPage();
  const errors = [];
  const dynamicLinks = new Set();
  let current = '';
  page.on('pageerror', e => errors.push({page: current, error: e.message}));
  page.on('response', r => {if (r.url().startsWith(base) && r.status() >= 400) errors.push({page: current, status: r.status(), url: r.url().replace(base, '')});});
  async function visit(route) {
    current = route;
    console.log('Visiting:', route);
    const response = await page.goto(base + route, {waitUntil: 'load'});
    assert.equal(response.status(), 200, route);
    await page.waitForTimeout(250);
  }
  try {
    await visit('/en/');
    if (await page.locator('.cmplz-deny').isVisible()) await page.locator('.cmplz-deny').click();
    const footer = page.locator('footer').first();
    assert.match(await footer.innerText(), /Privacy Policy/);
    assert.doesNotMatch(await footer.innerText(), /Política|Metodología|Contacto|Términos/);
    fs.mkdirSync(path.join(__dirname, '../artifacts'), {recursive: true});
    await footer.screenshot({path: path.join(__dirname, '../artifacts/english-footer.png')});
    for (const slug of ['privacy-policy', 'about-us', 'review-methodology', 'contact', 'terms-and-conditions', 'cookie-policy', 'disclaimer', 'legal-notice']) {
      await visit('/en/' + slug + '/');
      assert.equal(await page.locator('html').getAttribute('lang'), 'en');
      const toggle = page.locator('a.np-lang-toggle').first();
      const target = await toggle.getAttribute('href');
      await toggle.click();
      await page.waitForURL(base + target);
      assert.equal(await page.locator('html').getAttribute('lang'), 'es');
    }
    await visit('/en/tools/');
    assert.match(await page.locator('main').innerText(), /Tools Directory/);
    assert.equal(await page.locator('main article').count(), 26);
    await page.locator('header input[type=search]').fill('CRM');
    assert.equal(await page.locator('main article:visible').count(), 1);
    await page.locator('header input[type=search]').fill('');
    assert.equal(await page.locator('main article:visible').count(), 26);
    await page.getByRole('tab', {name: /Finance/}).click();
    assert.equal(await page.locator('main article:visible').count(), 5);
    await page.getByRole('tab', {name: /^All/}).click();
    await page.getByRole('button', {name: 'Global settings', exact: true}).click();
    await page.getByRole('dialog').getByRole('button', {name: 'Close', exact: true}).click();
    const routes = JSON.parse(fs.readFileSync(path.join(__dirname, '../dist/language-routes.json')));
    const toolHeadings = [];
    for (const [es, en] of Object.entries(routes.pairs).filter(([es]) => /^\/herramientas\/[^/]+\/[^/]+\/$/.test(es))) {
      await visit(en);
      assert.equal(await page.locator('html').getAttribute('lang'), 'en');
      const appRoot = page.locator('#root');
      if (await appRoot.count()) {
        await page.waitForFunction(() => (document.getElementById('root')?.innerText || '').trim().length > 80);
        assert.doesNotMatch(await appRoot.innerText(), /Herramienta no encontrada|Page Not Found/);
      }
      await page.waitForTimeout(150);
      toolHeadings.push({route: en, headings: await page.locator('h1').allTextContents(), text: await page.locator('body').innerText()});
      assert.doesNotMatch(toolHeadings.at(-1).headings.join(' '), /\b(Analizador|profesionales|Promociones|Simulador|Corporativas|manejar|aligera)\b/);
      assert.doesNotMatch(toolHeadings.at(-1).text, /Formula: Precio neto|¿No sabes por dónde empezar|Cotización generada electrónicamente/);
      fs.writeFileSync(path.join(__dirname, '../artifacts/tool-headings.json'), JSON.stringify(toolHeadings, null, 2));
      assert.ok(await page.evaluate(() => Object.keys(window.NPP_TOOL_TEXT || {}).length > 100), 'Dynamic English translations missing: ' + en);
      const untranslated = await page.evaluate(() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        const missing = [];
        while (walker.nextNode()) {
          const node = walker.currentNode;
          if (node.parentElement.closest('script,style,textarea,input,[contenteditable="true"]')) continue;
          const key = node.data.trim();
          if (window.NPP_TOOL_TEXT[key] && window.NPP_TOOL_TEXT[key] !== key) missing.push(key);
        }
        return missing;
      });
      assert.deepEqual(untranslated, [], 'Spanish dynamic labels remain: ' + en);
      for (const href of await page.locator('a[href]').evaluateAll(nodes => nodes.map(node => node.href))) {
        const url = new URL(href);
        if (url.origin === base && !url.hash) dynamicLinks.add(url.pathname + url.search);
      }
      const switcher = page.locator('a.np-lang-toggle, a.np-footer-lang').first();
      if (await switcher.count()) assert.equal(await switcher.getAttribute('href'), es, en);
      console.log('Browser OK:', en);
    }
    fs.writeFileSync(path.join(__dirname, '../artifacts/tool-headings.json'), JSON.stringify(toolHeadings, null, 2));
    for (const route of dynamicLinks) {
      const response = await context.request.get(base + route);
      assert.ok(response.status() < 400, 'Broken JavaScript-generated link: ' + route);
    }
    await visit('/en/tools/en/index.html');
    assert.equal(new URL(page.url()).pathname, '/en/tools/');
    await page.setViewportSize({width: 390, height: 844});
    await visit('/en/');
    fs.mkdirSync(path.join(__dirname, '../artifacts'), {recursive: true});
    await page.screenshot({path: path.join(__dirname, '../artifacts/english-home-mobile.png'), fullPage: true});
    fs.writeFileSync(path.join(__dirname, '../artifacts/browser-errors.json'), JSON.stringify(errors, null, 2));
    assert.deepEqual(errors, [], 'Local asset failures or browser exceptions');
    console.log('Browser localization checks passed.');
  } catch (error) {
    fs.mkdirSync(path.join(__dirname, '../artifacts'), {recursive: true});
    fs.writeFileSync(path.join(__dirname, '../artifacts/browser-errors.json'), JSON.stringify({page: current, error: String(error), errors}, null, 2));
    await page.screenshot({path: path.join(__dirname, '../artifacts/browser-failure.png'), fullPage: true}).catch(() => {});
    throw error;
  } finally {
    await browser.close();
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
