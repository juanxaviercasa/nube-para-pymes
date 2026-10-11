// Token is read from a local session file; no credentials are saved to the repository.
const fs=require('node:fs');
const account='821ab621fcfca78218b3b9456fcb08cb';
async function main(){
 const token=fs.readFileSync(process.env.CF_TOKEN_FILE,'utf8').trim();
 async function api(path,method='GET',body){
  const multipart=body instanceof FormData;
  const response=await fetch('https://api.cloudflare.com/client/v4/'+path,{method,headers:{Authorization:'Bearer '+token,...(!multipart&&body?{'Content-Type':'application/json'}:{})},body:body?(multipart?body:JSON.stringify(body)):undefined});
  const result=await response.json();
  if(!response.ok||!result.success)throw new Error(path+' HTTP '+response.status+' '+JSON.stringify(result.errors));
  return result.result;
 }
 const sites=JSON.parse(fs.readFileSync('cloudflare/sites.json','utf8'));
 const widgets=await api(`accounts/${account}/challenges/widgets`);
 for(const [project,site] of Object.entries(sites)){
  const name='contact-'+project;
  const existing=widgets.find(x=>x.name===name);
  const widget=existing?await api(`accounts/${account}/challenges/widgets/${existing.sitekey}`):await api(`accounts/${account}/challenges/widgets`,'POST',{name,domains:[site.domain],mode:'managed',bot_fight_mode:false});
  if(!widget.secret)throw new Error('Turnstile secret unavailable for '+project);
  const worker=project+'-contact';
  const metadata={main_module:'contact-worker.mjs',compatibility_date:'2026-10-11',bindings:[
   {name:'EMAIL',type:'send_email',destination_address:site.recipient},
   {name:'CONTACT_TO',type:'plain_text',text:site.recipient},
   {name:'CONTACT_ORIGIN',type:'plain_text',text:'https://'+site.domain},
   {name:'CONTACT_BRAND',type:'plain_text',text:site.name},
   {name:'CONTACT_CATEGORIES',type:'plain_text',text:JSON.stringify(site.categories)},
   {name:'TURNSTILE_SITE_KEY',type:'plain_text',text:widget.sitekey},
   {name:'TURNSTILE_SECRET',type:'secret_text',text:widget.secret},
   {name:'CONTACT_RATE_LIMITER',type:'ratelimit',namespace_id:String(1001+Object.keys(sites).indexOf(project)),simple:{limit:5,period:60}}
  ]};
  const body=new FormData();body.set('metadata',JSON.stringify(metadata));body.set('contact-worker.mjs',new Blob([fs.readFileSync('cloudflare/contact-worker.mjs')],{type:'application/javascript+module'}),'contact-worker.mjs');
  await api(`accounts/${account}/workers/scripts/${worker}`,'PUT',body);
  await api(`accounts/${account}/workers/scripts/${worker}/subdomain`,'POST',{enabled:false,previews_enabled:false});
  const routes=await api(`zones/${site.zone}/workers/routes`);
  const pattern=site.domain+'/api/contact*';
  const route=routes.find(x=>x.pattern===pattern);
  if(route&&route.script!==worker)throw new Error('Existing route owned by another Worker: '+pattern);
  if(!route)await api(`zones/${site.zone}/workers/routes`,'POST',{pattern,script:worker});
  console.log(JSON.stringify({project,worker,domain:site.domain,recipient:site.recipient,configured:true}));
 }
}
main().catch(error=>{console.error(error.message);process.exitCode=1;});
