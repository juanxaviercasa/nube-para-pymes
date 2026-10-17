const {chromium} = require('playwright');
const {createServer} = require('./preview_server');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

(async () => {
  const server = createServer();
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
  const browser = await chromium.launch({executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || (fs.existsSync(chrome) ? chrome : undefined), headless: true});
  const context = await browser.newContext();
  await context.addInitScript(() => localStorage.setItem('onboarding-v2-done', '1'));
  await context.route('**/*', route => new URL(route.request().url()).origin === base ? route.continue() : route.abort());
  const page = await context.newPage();
  const pairs = JSON.parse(fs.readFileSync(path.join(__dirname, '../dist/language-routes.json'))).pairs;
  const routes = Object.entries(pairs).filter(([es]) => /^\/herramientas\/[^/]+\/[^/]+\/$/.test(es)).flat();
  const output = path.join(__dirname, '../artifacts/tool-layout');
  fs.mkdirSync(output, {recursive:true});
  const errors = [], reports = [];
  let route = '';
  page.on('pageerror', error => errors.push({route, error:error.message}));
  page.on('response', response => {if (response.url().startsWith(base) && response.status() >= 400) errors.push({route, status:response.status(), url:response.url()});});
  try {
    for (route of routes) {
      await page.goto(base + route, {waitUntil:'load'});
      await page.waitForFunction(() => document.body.dataset.nppScheme && document.querySelector('h1'));
      await page.waitForTimeout(160);
      assert.equal(await page.locator('.npp-tool-nav').count(), 1, route);
      assert.equal(await page.locator('.npp-tool-bridge').count(), 1, route);
      assert.equal(await page.locator('.np-todolima-partner-banner').count(), 0, route);
      assert(await page.locator('.npp-tool-bridge').evaluate(e => !!(e.compareDocumentPosition(document.querySelector('.np-global-footer')) & Node.DOCUMENT_POSITION_FOLLOWING)), route);
      assert.equal(await page.locator('.npp-tool-back').getAttribute('href'), route.startsWith('/en/') ? '/en/tools/' : '/herramientas/');
      for (const mode of ['light', 'dark']) {
       const toggle = page.locator('[data-npp-theme-toggle]');
       if ((await toggle.getAttribute('aria-pressed') === 'true') !== (mode === 'dark')) await toggle.click();
       await page.waitForFunction(mode => document.body.dataset.nppScheme === mode, mode);
       await page.waitForTimeout(320);
       for (const width of [360, 390, 768, 1024, 1440]) {
        await page.setViewportSize({width, height:900});
        await page.waitForTimeout(45);
        const result = await page.evaluate(() => {
          const visible = el => {const r=el.getBoundingClientRect();return r.width>0 && r.height>0 && getComputedStyle(el).visibility!=='hidden';};
          const clipped = [...document.querySelectorAll('#root button, #root label, .op-field label, .npp-tool-bridge h2, .npp-tool-bridge p')].filter(visible).filter(el => {
            if (el.closest('[data-user-content], [contenteditable="true"]')) return false;
            const s=getComputedStyle(el);
            return ((s.overflowY==='hidden' || s.overflowY==='clip') && el.scrollHeight>el.clientHeight+2) || ((s.overflowX==='hidden' || s.overflowX==='clip') && el.scrollWidth>el.clientWidth+2 && s.textOverflow!=='ellipsis');
          }).map(el=>({tag:el.tagName, text:el.innerText.slice(0,90), cl:el.className}));
          const bar=document.querySelector('.np-demo-bar'), main=bar?.parentElement;
          const sample=document.querySelector('#root > .min-h-screen') || document.body;
          const canvas=getComputedStyle(sample).backgroundColor;
          const lowContrast=[];
          for (const el of document.querySelectorAll('#root h1, #root h2, #root h3, #root label, #root button, .op-card h3')) {
            if (!visible(el) || el.closest('[data-user-content], #quotationPreview, #invoicePreview, #contractPreview')) continue;
            const rgb=getComputedStyle(el).color.match(/[\d.]+/g)?.map(Number);
            let parent=el, bg;
            while(parent) {
              bg=getComputedStyle(parent).backgroundColor.match(/[\d.]+/g)?.map(Number);
              if(bg && (bg.length<4 || bg[3]>.95)) break;
              parent=parent.parentElement;
            }
            if(rgb?.length>=3 && bg?.length>=3 && rgb.slice(0,3).every(x=>x>210) && bg.slice(0,3).every(x=>x>210)) lowContrast.push({text:el.innerText.slice(0,70),cl:el.className});
          }
          return {canvas,lowContrast,pageWidth:document.documentElement.scrollWidth, viewport:innerWidth, clipped, scheme:document.body.dataset.nppScheme,
            demo:bar?{width:bar.getBoundingClientRect().width, parent:main.getBoundingClientRect().width, columns:getComputedStyle(main).gridTemplateColumns, span:getComputedStyle(bar).gridColumn}:null};
        });
        reports.push({route,width,mode,...result});
        if (result.pageWidth > width+2 || result.clipped.length || result.lowContrast.length) console.log('LAYOUT', JSON.stringify(reports.at(-1)));
        if (['calculadora-precios-venta-igv','firma-correo-html','generador-cotizaciones','crm-pymes','simulador-tco-fisico-nube','generador-paletas-corporativas'].some(slug=>route.includes('/'+slug+'/')) && [390,768,1440].includes(width)) {
          await page.screenshot({path:path.join(output,`${route.split('/').at(-2)}-${mode}-${width}.png`),fullPage:true});
        }
      }
      if (mode === 'light' && !route.startsWith('/en/')) await page.screenshot({path:path.join(output,`${route.split('/').at(-2)}-light-overview.png`)});
      await page.evaluate(()=>scrollTo(0,document.body.scrollHeight));
      assert((await page.locator('.npp-tool-nav').boundingBox()).y >= -1, route+' sticky navigation');
      await page.evaluate(()=>scrollTo(0,0));
      }
      if (await page.locator('[data-npp-theme-toggle]').getAttribute('aria-pressed') === 'true') await page.locator('[data-npp-theme-toggle]').click();
      console.log('Checked', route);
    }
    for (const directory of ['/herramientas/', '/en/tools/']) {
      await page.goto(base+directory);
      const toggle=page.locator('header button[role="switch"]').first();
      await toggle.waitFor();
      if (await toggle.getAttribute('aria-checked') !== 'true') await toggle.click();
      await page.waitForFunction(()=>localStorage.getItem('npp-theme')==='dark');
      await page.goto(base+'/herramientas/finanzas/calculadora-precios-venta-igv/');
      assert.equal(await page.locator('body').getAttribute('data-npp-scheme'), 'dark');
      await page.locator('[data-npp-theme-toggle]').click();
      await page.goto(base+directory);
      await toggle.waitFor();
      assert.equal(await toggle.getAttribute('aria-checked'), 'false');
    }
    // Exercise calculations, React tab unmounts and locally stored operational data.
    route='/herramientas/finanzas/calculadora-precios-venta-igv/';
    await page.goto(base+route);
    await page.locator('input[type=number]').first().fill('200');
    await page.getByText(/PEN\s*337[.,]14/).first().waitFor();
    await page.getByRole('button',{name:'Margen Inverso',exact:true}).click();
    await page.getByRole('button',{name:'Calculadora',exact:true}).click();
    await page.locator('input[type=number]').first().waitFor();
    route='/herramientas/ventas/crm-pymes/';
    await page.goto(base+route);
    await page.locator('#contactName').fill('Prueba responsive');
    await page.getByRole('button',{name:'Guardar contacto',exact:true}).click();
    await page.locator('#contactsTable').getByText('Prueba responsive',{exact:true}).waitFor();
    const failures=reports.filter(x=>x.pageWidth>x.width+2 || x.clipped.length || x.lowContrast.length);
    fs.writeFileSync(path.join(output,'report.json'),JSON.stringify({reports,errors,failures},null,2));
    assert.deepEqual(errors,[], 'Browser errors');
    assert.deepEqual(failures,[], 'Responsive overflow or clipped text; see artifacts/tool-layout/report.json');
    console.log(`PASS: ${routes.length} routes Ã— 5 viewport widths, theme changes, navigation and form interactions.`);
  } finally {
    fs.writeFileSync(path.join(output,'latest.json'),JSON.stringify({reports,errors},null,2));
    await browser.close();
    await new Promise(resolve=>server.close(resolve));
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
