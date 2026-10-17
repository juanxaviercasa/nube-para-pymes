const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const {createServer} = require('./preview_server');
(async()=>{
 const root=path.resolve(__dirname,'..');
 const data=JSON.parse(fs.readFileSync(path.join(root,'content/todolima-tutorials.json'),'utf8'));
 const pairs=JSON.parse(fs.readFileSync(path.join(root,'dist/language-routes.json'),'utf8')).pairs;
 const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const base=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch({headless:true});
 const output=path.join(root,'artifacts/tutoriales');fs.mkdirSync(output,{recursive:true});
 try{
  const context=await browser.newContext();
  await context.addInitScript(()=>localStorage.setItem('onboarding-v2-done','1'));
  await context.route('**/*',r=>new URL(r.request().url()).origin===base?r.continue():r.abort());
  const p=await context.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
  for(const width of [390,1440]){
   await p.setViewportSize({width,height:900});
   for(const t of data.tools){
    const es=new URL(t.toolUrl).pathname;
    for(const route of [es,pairs[es]]){
     await p.goto(base+route,{waitUntil:'networkidle'});
     const link=p.locator('[data-npp-illustrated-tutorial] a');
     assert.equal(await link.count(),1,route);assert.equal(await link.getAttribute('href'),t.tutorialUrl);
     assert.equal(await link.getAttribute('target'),'_blank');assert.match(await link.getAttribute('rel'),/noopener/);
     assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),route+' overflow');
     if(route.startsWith('/en/'))assert.match(await link.innerText(),/Spanish/);
     if(t.slug==='calculadora-precios-venta-igv'){
      await link.focus();assert.ok(await link.evaluate(e=>e===document.activeElement));
      await p.screenshot({path:path.join(output,`tool-${width}-${route.startsWith('/en/')?'en':'es'}.png`)});
      await p.locator('.np-help-button').click();
      const help=p.locator('[data-npp-tutorial-help]');await help.waitFor();assert.equal(await help.getAttribute('href'),t.tutorialUrl);
      assert.equal(await p.locator('.np-help-actions [data-help-action=tour]').count(),1);
      await p.screenshot({path:path.join(output,`help-${width}-${route.startsWith('/en/')?'en':'es'}.png`)});
      await p.keyboard.press('Escape');assert.equal(await p.locator('.np-help-backdrop').count(),0);
     }
    }
   }
   for(const portal of ['/herramientas/','/en/tools/']){
    await p.goto(base+portal,{waitUntil:'networkidle'});
    assert.equal(await p.locator('[data-npp-tutorial-card]').count(),16);
    assert.equal(await p.locator('a[href*="todolima.com/herramientas/undefined"]').count(),0);
   }
  }
  assert.deepEqual(errors,[]);
  console.log('PASS: 16 tutorials, 32 bilingual tool pages, both portals, help panel, keyboard links and mobile/desktop layout.');
 }finally{await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1;});
