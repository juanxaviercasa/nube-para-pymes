(function(){
  const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const workspaceKeys=new Set(['np_crm_pymes_v1','np_flujo_caja_pymes_v1','np_inventario_compras_pymes_v1','np_tareas_proyectos_pymes_v1']);
  let workspace;
  const hasRecords=value=>Object.entries(value||{}).some(([key,items])=>key!=='regional'&&Array.isArray(items)&&items.length);
  const read=(key,fallback)=>{try{const v=JSON.parse(localStorage.getItem(key)||'');if(v&&workspaceKeys.has(key)){workspace=v;if(hasRecords(v))window.NPPRegion.restore(v.regional,'PEN');}return v??fallback}catch(_){return fallback}};
  const write=(key,value)=>{if(workspaceKeys.has(key)){value.regional=window.NPPRegion.snapshot();workspace=value;}localStorage.setItem(key,JSON.stringify(value));try{window.npBackup?.save(window.NP_BACKUP_CONFIG.appId,{[key]:value})}catch(_){} };
  window.addEventListener('npp:before-region-apply',event=>{if(hasRecords(workspace)&&event.detail.currency!==window.NPPRegion.active().currency)event.preventDefault();});
  const uid=()=>`${Date.now().toString(36)}-${Math.random().toString(36).slice(2,7)}`;
  const esc=(v)=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const isEn = (document.documentElement.lang || '').toLowerCase().startsWith('en') || window.location.pathname.indexOf('/en/') !== -1;
  const money=(n,currency)=>window.NPPRegion.money(Number(n)||0,currency);
  const date=(v)=>window.NPPRegion.date(v);
  const today=()=>new Date().toISOString().slice(0,10);
  const notify=(msg,kind='')=>{const el=$('#op-alert');if(!el)return;el.textContent=msg;el.className=`op-alert show ${kind}`;clearTimeout(window.__opAlertTimer);window.__opAlertTimer=setTimeout(()=>{el.className='op-alert'},4200)};
  window.OP={$, $$, read, write, uid, esc, money, date, today, notify, isEn};
  window.addEventListener('npBackup:changed',()=>window.location.reload());
})();
