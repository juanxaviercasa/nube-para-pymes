const {chromium}=require('playwright');
const {createServer}=require('./preview_server');
const fs=require('node:fs');
const assert=require('node:assert/strict');
(async()=>{
 const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const base='http://127.0.0.1:'+server.address().port;
 const chrome='C:/Program Files/Google/Chrome/Application/chrome.exe';
 const b=await chromium.launch({executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||(fs.existsSync(chrome)?chrome:undefined),headless:true});
 const context=await b.newContext();await context.addInitScript(()=>localStorage.setItem('onboarding-v2-done','1'));
 await context.route('**/*',r=>new URL(r.request().url()).origin===base?r.continue():r.abort());
 const page=await context.newPage();const errors=[];let current='';
 page.on('pageerror',e=>errors.push({current,error:e.message}));
 page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)errors.push({current,url:r.url(),status:r.status()})});
 const visit=async route=>{current=route;await page.goto(base+route,{waitUntil:'load'});await page.locator('[data-region-open]').waitFor();await page.waitForTimeout(180);};
 const open=()=>page.locator('[data-region-open]').click();
 const country=async c=>{await open();await page.locator('[name=country]').selectOption(c);};
 const apply=()=>page.locator('.npp-region-dialog button[type=submit]').click();
 try{
  await visit('/en/tools/');assert.equal(await page.evaluate(()=>NPPRegion.get().country),'PE');
  await visit('/herramientas/finanzas/calculadora-precios-venta-igv/');
  assert.equal(await page.locator('input[type=number]').nth(2).inputValue(),'18');
  await country('ES');await apply();await page.waitForFunction(()=>document.querySelectorAll('#root input[type=number]')[2]?.value==='21');
  await page.locator('input[type=number]').first().fill('70');await page.getByText(/EUR.*121/).first().waitFor();
  await country('US');assert.equal(await page.locator('[name=taxRate]').inputValue(),'');await apply();assert(await page.locator('.npp-region-dialog').isVisible());
  await page.locator('[name=taxRate]').fill('8.25');await apply();assert.equal(await page.evaluate(()=>NPPRegion.active().currency),'USD');
  await visit('/en/quote-estimate-generator/');assert.equal(await page.evaluate(()=>NPPRegion.get().country),'US');
  await country('ES');await page.locator('[name=priceMode]').selectOption('included');await apply();
  await page.locator('input[placeholder*="Descripción"]').first().fill('Servicio internacional');
  // Native controls must use the real regional settings for previews and exports.
  await page.locator('input[placeholder="0.00"]').first().fill('121');
  await page.waitForTimeout(200);
  assert.match(await page.locator('#root').innerText(),/EUR/);
  assert.equal(await page.locator('select[data-visual-edit-loc="src/components/QuoteHeaderForm.tsx:121:10"]').inputValue(),'EUR');
  assert.deepEqual(await page.evaluate(()=>{const d=NPPRegion.getDocument();const t=NPPRegion.totals(d.items);return {subtotal:Math.round(t.subtotal),tax:Math.round(t.igv),total:Math.round(t.total)}}),{subtotal:100,tax:21,total:121});
  await open();const itemRate=page.locator('[data-tax-item]').first();await itemRate.fill('0');await apply();
  assert.equal(await page.evaluate(()=>NPPRegion.getDocument().items[0].taxRate),0);
  await page.locator('input[placeholder*="Descripción"]').first().waitFor();
  await visit('/herramientas/ventas/creador-facturas-proforma/');
  assert.equal(await page.evaluate(()=>NPPRegion.active().currency),'EUR');
  await page.evaluate(()=>NPPRegion.set({...NPPRegion.preset('PE')}));
  await visit('/herramientas/operaciones/calculadora-flete-envio-local/');
  await open();await page.locator('[name=units]').selectOption('imperial');await page.locator('[data-freight-field=base]').fill('25');await apply();
  await page.waitForFunction(()=>NPPRegion.active().units==='imperial');
  assert.equal(await page.evaluate(()=>NPPRegion.freight().base),25);
  assert.match(await page.locator('#root').innerText(),/lb/);
  await page.evaluate(()=>NPPRegion.set({...NPPRegion.preset('ES'),priceMode:'included'}));
  await visit('/herramientas/operaciones/inventario-compras-pymes/');
  await page.locator('#sku').fill('R-1');await page.locator('#productName').fill('Producto');await page.locator('#productCost').fill('100');await page.locator('#productPrice').fill('121');
  await page.getByRole('button',{name:'Guardar producto',exact:true}).click();
  await country('PE');await apply();assert(await page.locator('.npp-region-dialog').isVisible());assert.match(await page.locator('[data-region-message]').innerText(),/otra moneda/);
  await page.locator('[data-save-defaults]').click();assert.equal(await page.evaluate(()=>NPPRegion.active().currency),'EUR');
  await page.reload();assert.equal(await page.evaluate(()=>NPPRegion.active().currency),'EUR');
  const pairs=JSON.parse(fs.readFileSync('dist/language-routes.json')).pairs;
  const routes=Object.entries(pairs).filter(([es])=>/^\/herramientas\/[^/]+\/[^/]+\/$/.test(es)).flat();
  for(const route of routes){
   await visit(route);
   for(const width of [360,768,1440]){
    await page.setViewportSize({width,height:900});
    await page.waitForTimeout(120);
    if(!(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2))) console.log('Overflow detail',route,await page.evaluate(()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+2&&e.getBoundingClientRect().width>0).slice(0,12).map(e=>({tag:e.tagName,cl:e.className,text:e.innerText?.slice(0,70)}))));
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+2),route+' page overflow '+width);
    await open();assert(await page.locator('.npp-region-dialog').isVisible());
    const overflow=await page.locator('.npp-region-dialog').evaluate(e=>e.scrollWidth>e.clientWidth+2);assert(!overflow,route);
    await page.locator('[data-region-close]').click();
   }
   console.log('Regional responsive OK',route);
  }
  fs.mkdirSync('artifacts/regional',{recursive:true});
  await visit('/herramientas/finanzas/calculadora-precios-venta-igv/');await country('CA');await page.locator('[name=region]').selectOption('MB');await page.screenshot({path:'artifacts/regional/settings-mobile.png'});
  fs.writeFileSync('artifacts/regional/browser-errors.json',JSON.stringify(errors,null,2));
  assert.deepEqual(errors,[]);console.log('PASS: regional defaults, explicit tax entry, live calculator update, ledger protection, 52 routes and mobile dialog.');
 }finally{await b.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1});
