/* Guarded edits to the exported apps. Fail loudly if an upstream bundle changes. */
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const R = 'window.NPPRegion';
function patch(name, edit) {
  const file = path.join(root, 'js', name+'.js');
  let text = fs.readFileSync(file, 'utf8');
  if (text.startsWith('/* NPP_REGIONAL_V1 */')) return;
  function replace(before, after, all = false) {
    if (!text.includes(before)) throw Error(name+': missing target '+before.slice(0,100));
    text = all ? text.split(before).join(after) : text.replace(before, after);
  }
  edit(replace, () => text);
  fs.writeFileSync(file, '/* NPP_REGIONAL_V1 */\n'+text);
  console.log('Regional integration:', name);
}
patch('calculadora-precios-venta-igv', (rep, text) => {
  const format=text().match(/function er\(e,t\)\{return Number\.isFinite\(e\)\?[^}]+maximumFractionDigits:2[^}]+\}\)\}[^}]+\}/);
  // Function boundary is unique in this exported pricing module.
  const start=text().indexOf('function er(e,t){return Number.isFinite');
  const end=text().indexOf('function tr(e)',start);
  if(start<0||end<0)throw Error('pricing formatter');
  rep(text().slice(start,end),'function er(e,t){return '+R+'.money(e,t)}');
  rep('var mm=[{code:"PEN",symbol:"S/"},{code:"USD",symbol:"$"},{code:"EUR",symbol:"€"}]','var mm=Array.from(new Set(['+R+'.active().currency,"PEN","USD","EUR","CAD","GBP"])).map(code=>({code,symbol:code}))');
  rep('[n,a]=(0,_.useState)("S/")','[n,a]=(0,_.useState)('+R+'.active().currency)');
  rep('_m=()=>{let[e,t]','_m=()=>{'+R+'.connect(_,p=>{a(p.currency);s(items=>items.map(item=>({...item,tax:'+R+'.rate(p)})))});let[e,t]');
  rep('Gp=({symbol:e,onSave:t})=>{let','Gp=({symbol:e,onSave:t})=>{'+R+'.connect(_,()=>s(String('+R+'.rate())));let');
  rep('Jp=({symbol:e})=>{let','Jp=({symbol:e})=>{'+R+'.connect(_,()=>o(String('+R+'.rate())));let');
  rep('(0,_.useState)("18")','(0,_.useState)(()=>String('+R+'.rate()))',true);
  rep('tax:18,units:','tax:'+R+'.rate(),units:',true);
  rep('let t=[{...e,id:crypto.randomUUID(),date:','let t=[{...e,regional:'+R+'.snapshot(),id:crypto.randomUUID(),date:');
  rep('var Qn=[{id:"general",label:"IGV General",short:"General 18%",rate:18},{id:"reducido",label:"IGV Reducido",short:"Reducido 10%",rate:10}]','var Qn=[{id:"general",label:'+R+'.taxName(),short:'+R+'.taxLabel(),rate:'+R+'.rate()}]');
  rep('let c=Qn.find(e=>e.id===l)?.rate??18','let c='+R+'.rate()');
  rep('Editable. Por defecto 18%.','Editable según tu operación y configuración regional.');
});
patch('generador-cotizaciones', rep => {
  rep('Bn=e=>{let t=e.reduce((e,t)=>e+zn(t),0),n=t*In;return{subtotal:t,igv:n,total:t+n}}','Bn=(e,p)=>'+R+'.totals(e,p||'+R+'.active())');
  const old='Hn=(e,t="PEN")=>Pn[t]+" "+(Number.isFinite(e)?e:0).toLocaleString("es-PE",{minimumFractionDigits:2,maximumFractionDigits:2})';
  rep(old,'Hn=(e,t)=>'+R+'.money(e,t)');
  rep('Bn(n.items)','Bn(n.items,n.regional||'+R+'.legacy(n.currency))');
  rep('Bn(e.items)','Bn(e.items,e.regional||'+R+'.legacy(e.currency))',true);
  rep('currency:"PEN",exchangeRate:0','currency:'+R+'.active().currency,regional:'+R+'.snapshot(),exchangeRate:0');
  rep('Pn={PEN:"S/",USD:"$"}','Pn=Object.fromEntries(Array.from(new Set(['+R+'.active().currency,"PEN","USD","EUR","CAD","GBP"])).map(c=>[c,c]))');
  rep('w("IGV (18%)",','w('+R+'.taxLabel(n.regional||'+R+'.legacy(n.currency)),');
  rep('children:"IGV (18%)"','children:'+R+'.taxLabel()',true);
  rep('data:e};return n.unshift(r)','data:{...e,regional:e.regional||'+R+'.snapshot()}};return n.unshift(r)');
  rep('let f=e=>{d(e),window.setTimeout',R+'.connect(_,p=>t(e=>({...e,currency:p.currency,regional:p,applyDetraction:p.country==="PE"&&e.applyDetraction})));'+R+'.documentAPI({items:e.items,setTaxes:rates=>t(e=>({...e,items:e.items.map(item=>({...item,taxRate:rates[item.id]??null}))}))});let f=e=>{d(e),window.setTimeout');
});
patch('creador-facturas-proforma', (rep, text) => {
  const start=text().indexOf('function Kn(t,e){let n=Number.isFinite');
  const end=text().indexOf('function qn(t)',start);
  if(start<0||end<0)throw Error('proforma formatter');
  rep(text().slice(start,end),'function Kn(t,e){return '+R+'.money(t,e)}');
  const pdf=text().indexOf('bf=(t,e)=>');
  const pdfEnd=text().indexOf(';function xf',pdf);
  rep(text().slice(pdf,pdfEnd),'bf=(t,e)=>'+R+'.money(t,e)');
  rep('YS=["$","€","S/"]','YS=Array.from(new Set(['+R+'.active().currency,"PEN","USD","EUR","CAD","GBP"]))');
  rep('currency:"$",taxRate:0,notes:','currency:'+R+'.active().currency,regional:'+R+'.snapshot(),taxRate:'+R+'.rate(),notes:');
  rep('let{subtotal:z,taxAmount:B,total:U}=(0,_.useMemo)(()=>{let t=l.reduce((t,e)=>t+e.qty*e.price,0),e=t*s.taxRate/100;return{subtotal:t,taxAmount:e,total:t+e}},[l,s.taxRate])','let{subtotal:z,igv:B,total:U}=(0,_.useMemo)(()=>'+R+'.totals(l,s.regional||{...'+R+'.legacy('+R+'.code(s.currency)),taxes:[{name:"Tax",rate:s.taxRate}]},item=>item.qty*item.price),[l,s.taxRate,s.regional])');
  rep('K=t=>o(e=>({...e,...t}))','K=t=>o(e=>({...e,...t,...("taxRate" in t?{regional:{...(e.regional||'+R+'.legacy('+R+'.code(e.currency))),taxes:[{name:'+R+'.taxName(),rate:t.taxRate}]}}:{})}))');
  rep('function eC(){let','function eC(){'+R+'.connect(_,p=>o(e=>({...e,currency:p.currency,taxRate:'+R+'.rate(p),regional:p})));let');
  rep('let{subtotal:z,igv:B',R+'.documentAPI({items:l,setTaxes:rates=>u(items=>items.map(item=>({...item,taxRate:rates[item.id]??null})))});let{subtotal:z,igv:B');
  rep('n&&(e(n.issuer),i(n.logo),r(n.client),o({...ZS(),...n.meta})','n&&('+R+'.restore(n.meta.regional||{...'+R+'.legacy('+R+'.code(n.meta.currency)),taxes:[{name:"Tax",rate:n.meta.taxRate}]},n.meta.currency),window.dispatchEvent(new CustomEvent("npp:document-region")),e(n.issuer),i(n.logo),r(n.client),o({...ZS(),...n.meta,regional:'+R+'.snapshot()})');
});
for(const name of ['calculadora-descuentos-promociones','calculadora-prestamos-amortizaciones','comparador-campanas-avanzado','simulador-tco-fisico-nube'])patch(name,(rep,text)=>{
  const patterns=[...text().matchAll(/new Intl\.NumberFormat\("(?:es-ES|es-MX)",\{style:"currency",currency:"(?:USD|MXN)",[^}]+\}\)/g)];
  if(!patterns.length)throw Error(name+': fixed formatter not found');
  for(const {0:old} of patterns)rep(old,R+'.formatter('+old.slice(old.indexOf('{'),-1)+')');
  const roots={'calculadora-descuentos-promociones':'function Yp(){','calculadora-prestamos-amortizaciones':'function Xm(){','comparador-campanas-avanzado':'lS=()=>{','simulador-tco-fisico-nube':'function aS(){'};
  if(roots[name])rep(roots[name],roots[name]+R+'.connect(_);');
});
