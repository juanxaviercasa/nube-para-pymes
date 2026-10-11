const {chromium}=require('playwright');
const {createServer}=require('./preview_server');
const fs=require('node:fs');const assert=require('node:assert/strict');
(async()=>{
 const server=createServer();await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||(fs.existsSync('C:/Program Files/Google/Chrome/Application/chrome.exe')?'C:/Program Files/Google/Chrome/Application/chrome.exe':undefined),headless:true});
 try{
  for(const width of [390,1366])for(const lang of ['es','en']){
   const page=await browser.newPage({viewport:{width,height:1000}});
   await page.route('https://challenges.cloudflare.com/turnstile/**',r=>r.fulfill({contentType:'application/javascript',body:'window.turnstile={render:function(selector,options){window.testContactOptions=options; options.callback("browser-test-token");return 1;},reset:function(){window.testContactOptions.callback("browser-test-token");}};'}));
   let deliveries=0;let failure=false;
   await page.route('**/api/contact',async route=>{
    if(route.request().method()==='GET')return route.fulfill({json:{ready:true,siteKey:'browser-test-sitekey'}});
    deliveries++;const data=route.request().postDataJSON();assert.equal(data.category,'servicios');assert.equal(data.email,'owner@example.com');assert.equal(data.consent,true);assert.equal(data.turnstile,'browser-test-token');
    return route.fulfill({status:failure?503:200,json:{success:!failure}});
   });
   const about=lang==='es'?'/sobre-nosotros/':'/en/about-us/';await page.goto(base+about);
   assert.equal(await page.locator('h1').count(),1);const image=page.locator('.npp-about-image img');await image.waitFor();assert.ok(await image.evaluate(i=>i.complete&&i.naturalWidth>0));assert.ok((await image.boundingBox()).width<=341);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
   if(lang==='es') {fs.mkdirSync('artifacts/brand-pages',{recursive:true});await page.screenshot({path:`artifacts/brand-pages/about-${width}.png`,fullPage:true});}
   const contact=lang==='es'?'/contacto/':'/en/contact/';await page.goto(base+contact+'?tipo=servicios#consulta');await page.locator('#npp-submit-btn').waitFor({state:'visible'});
   assert.equal(await page.locator('[name=category]:checked').getAttribute('value'),'servicios');
   await page.locator('[name=name]').fill('Prueba del formulario');await page.locator('[name=email]').fill('owner@example.com');await page.locator('[name=message]').fill('Quiero mejorar el proceso de atención de mi negocio.');
   await page.locator('[name=consent]').check();await page.waitForFunction(()=>!document.querySelector('#npp-submit-btn').disabled);
   failure=true;await page.locator('#npp-submit-btn').click();await page.waitForFunction(()=>document.querySelector('#npp-form-msg').dataset.state==='error');assert.ok((await page.locator('[name=message]').inputValue()).includes('atención'));
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
   failure=false;await page.locator('#npp-submit-btn').click();await page.waitForFunction(()=>document.querySelector('#npp-form-msg').dataset.state==='success');assert.equal(await page.locator('[name=message]').inputValue(),'');assert.equal(deliveries,2);
   await page.close();console.log(`PASS ${width}px ${lang}: about image size, responsive layout, inquiry category, failed delivery preserves text, confirmed delivery clears it.`);
  }
 }finally{await browser.close();await new Promise(r=>server.close(r));}
})().catch(e=>{console.error(e);process.exitCode=1});
