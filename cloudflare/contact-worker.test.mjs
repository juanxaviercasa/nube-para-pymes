import {test} from 'node:test';
import assert from 'node:assert/strict';
import {handleContact} from './contact-worker.mjs';
import {readFileSync} from 'node:fs';

test('each site uses its own categories, origin and fixed destination',async()=>{
 const sites=JSON.parse(readFileSync(new URL('./sites.json',import.meta.url),'utf8'));
 for(const site of Object.values(sites)){
  const f=fixture();Object.assign(f.env,{CONTACT_ORIGIN:'https://'+site.domain,CONTACT_BRAND:site.name,CONTACT_TO:site.recipient,CONTACT_CATEGORIES:JSON.stringify(site.categories)});
  const proof=async()=>Response.json({success:true,hostname:site.domain,action:'contact'});
  const request=new Request('https://'+site.domain+'/api/contact',{method:'POST',headers:{Origin:'https://'+site.domain,'Content-Type':'application/json'},body:JSON.stringify({...valid,category:Object.keys(site.categories)[0],subject:'Consulta de prueba'})});
  assert.equal((await handleContact(request,f.env,proof)).status,200);
  assert.equal(f.sent[0].to,site.recipient);assert.equal(f.sent[0].from,'formularios@'+site.domain);assert.ok(f.sent[0].subject.includes(site.name));assert.ok(f.sent[0].text.includes('Consulta de prueba'));
 }
});

const valid = {name:'Consulta de prueba',email:'owner@example.com',category:'servicios',business:'Mi pyme',reference:'https://example.com/',message:'Quiero organizar las consultas de mi pequeño negocio.',consent:true,turnstile:'test-token',website:''};
function fixture() {
  const sent = [];
  const env = {CONTACT_TO:'nubepymesai@gmail.com',TURNSTILE_SITE_KEY:'public-key',TURNSTILE_SECRET:'private-secret',CONTACT_RATE_LIMITER:{limit:async()=>({success:true})},EMAIL:{send:async message=>sent.push(message)}};
  const proof = async()=>Response.json({success:true,hostname:'nubeparapymes.online',action:'contact'});
  const request = (data=valid, origin='https://nubeparapymes.online') => new Request('https://nubeparapymes.online/api/contact',{method:'POST',headers:{Origin:origin,'Content-Type':'application/json','CF-Connecting-IP':'192.0.2.1'},body:JSON.stringify(data)});
  return {env,sent,proof,request};
}
test('verified inquiry reaches only the configured recipient, with visitor reply-to', async()=>{
  const f=fixture(); const response=await handleContact(f.request({...valid,to:'attacker@example.com'}),f.env,f.proof);
  assert.equal(response.status,200); assert.equal((await response.json()).success,true);
  assert.equal(f.sent.length,1); assert.equal(f.sent[0].to,'nubepymesai@gmail.com'); assert.equal(f.sent[0].replyTo,valid.email);
  assert.ok(f.sent[0].text.includes(valid.message)); assert.ok(f.sent[0].subject.includes('Apoyo digital'));
});
test('cross-origin requests cannot send email',async()=>{
  const f=fixture();assert.equal((await handleContact(f.request(valid,'https://attacker.example'),f.env,f.proof)).status,403);assert.equal(f.sent.length,0);
});
test('invalid data, consent, honeypot and email header injection are rejected',async()=>{
  for(const update of [{consent:false},{website:'bot'},{category:'toString'},{message:'short'},{email:'x@example.com\r\nBcc:attacker@example.com'},{reference:'javascript:alert(1)'},{name:' '},null]) {
    const f=fixture();assert.equal((await handleContact(f.request(update===null?null:{...valid,...update}),f.env,f.proof)).status,400);assert.equal(f.sent.length,0);
  }
});
test('oversized and malformed bodies never reach email delivery',async()=>{
  const f=fixture();assert.equal((await handleContact(f.request({...valid,message:'x'.repeat(20000)}),f.env,f.proof)).status,400);
  const request=new Request('https://nubeparapymes.online/api/contact',{method:'POST',headers:{Origin:'https://nubeparapymes.online','Content-Type':'application/json'},body:'{invalid'});
  assert.equal((await handleContact(request,f.env,f.proof)).status,400);assert.equal(f.sent.length,0);
});
test('rate limits prevent delivery',async()=>{
  const f=fixture();f.env.CONTACT_RATE_LIMITER.limit=async()=>({success:false});assert.equal((await handleContact(f.request(),f.env,f.proof)).status,429);assert.equal(f.sent.length,0);
});
test('Turnstile must verify success, expected hostname and action',async()=>{
  for(const update of [{success:false},{hostname:'another.example'},{action:'login'}]) {
    const f=fixture();const proof=async()=>Response.json({success:true,hostname:'nubeparapymes.online',action:'contact',...update});assert.equal((await handleContact(f.request(),f.env,proof)).status,403);assert.equal(f.sent.length,0);
  }
});
test('mail or verification failure does not report success',async()=>{
  const f=fixture();f.env.EMAIL.send=async()=>{throw new Error('delivery failure')};assert.equal((await handleContact(f.request(),f.env,f.proof)).status,503);
  assert.equal((await handleContact(f.request(),f.env,async()=>{throw new Error('verification timeout')})).status,503);
});
test('public settings hide secrets and fail closed when setup is incomplete',async()=>{
  const f=fixture();let response=await handleContact(new Request('https://nubeparapymes.online/api/contact'),f.env);assert.deepEqual(await response.json(),{ready:true,siteKey:'public-key'});
  delete f.env.TURNSTILE_SECRET;response=await handleContact(new Request('https://nubeparapymes.online/api/contact'),f.env);assert.deepEqual(await response.json(),{ready:false,siteKey:null});assert.equal((await handleContact(f.request(),f.env,f.proof)).status,503);
});
