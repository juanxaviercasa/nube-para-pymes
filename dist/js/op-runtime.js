
(function(){
  const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const read=(key,fallback)=>{try{const v=JSON.parse(localStorage.getItem(key)||'');return v??fallback}catch(_){return fallback}};
  const write=(key,value)=>{localStorage.setItem(key,JSON.stringify(value));try{window.npBackup?.save(window.NP_BACKUP_CONFIG.appId,{[key]:value})}catch(_){} };
  const uid=()=>`${Date.now().toString(36)}-${Math.random().toString(36).slice(2,7)}`;
  const esc=(v)=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const money=(n,currency='PEN')=>new Intl.NumberFormat('es-PE',{style:'currency',currency,maximumFractionDigits:2}).format(Number(n)||0);
  const date=(v)=>v?new Intl.DateTimeFormat('es-PE',{dateStyle:'medium'}).format(new Date(`${v}T12:00:00`)):'—';
  const today=()=>new Date().toISOString().slice(0,10);
  const notify=(msg,kind='')=>{const el=$('#op-alert');if(!el)return;el.textContent=msg;el.className=`op-alert show ${kind}`;clearTimeout(window.__opAlertTimer);window.__opAlertTimer=setTimeout(()=>{el.className='op-alert'},4200)};
  window.OP={$, $$, read, write, uid, esc, money, date, today, notify};
  window.addEventListener('npBackup:changed',()=>window.location.reload());
})();
