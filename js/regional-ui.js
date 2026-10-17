(() => {
  'use strict';
  const R = window.NPPRegion;
  if (!R) return;
  const en = document.documentElement.lang.startsWith('en');
  const tr = (es, english) => en ? english : es;
  const esc = text => String(text ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const profileName = p => `${R.countries[p.country].name[en ? 1 : 0]}${p.region ? ' · '+p.region : ''} · ${p.currency}`;
  let dialog, form, launch, source, taxRows, editor;
  const legal = ['generador-contratos-servicios','generador-politicas-devolucion','generador-politicas-terminos'];
  const payroll = document.body.dataset.appId === 'calculadora-sobrecostos-laborales';
  let returnFocus;
  function renderSummary() {
    if (!launch) return;
    launch.textContent = profileName(R.get());
    const note = document.querySelector('.npp-region-summary');
    if (note) note.textContent = tr('Cálculo actual: ', 'Current calculation: ') + profileName(R.active()) + ' · ' + R.taxLabel() + ' · ' + tr(R.active().priceMode === 'included' ? 'Impuesto incluido' : 'Impuesto añadido', R.active().priceMode === 'included' ? 'Tax included' : 'Tax added');
    if (note && payroll) note.textContent = tr('Cálculo laboral: Perú. Usa los controles propios de moneda y tipo de cambio de esta herramienta; los impuestos de venta de la configuración regional no se aplican a la planilla.', 'Payroll calculation: Peru. Use this tool’s own currency and exchange-rate controls; regional sales taxes do not apply to payroll.');
    document.querySelectorAll('[data-region-jurisdiction]').forEach(node => {
      node.hidden = !payroll && !legal.includes(document.body.dataset.appId);
      if (!node.hidden) node.textContent = payroll
        ? tr('Modelo laboral de Perú: CTS, gratificaciones y aportes peruanos. Cambiar país o moneda no adapta estas reglas a otra legislación.', 'Peruvian payroll model: CTS, bonuses and Peruvian contributions. Country and currency settings do not adapt these rules to another jurisdiction.')
        : tr('Plantilla orientativa: revisa la legislación aplicable al contrato, la privacidad y los consumidores del país de uso. Cambiar de país no realiza una adaptación legal automática.', 'Draft template: review the applicable contract, privacy and consumer laws in the country of use. Changing country does not automatically adapt the legal terms.');
    });
  }
  function row(tax = {name:'',rate:null}) {
    const node = document.createElement('div');
    node.className = 'npp-tax-row';
    node.innerHTML = `<label>${tr('Nombre del impuesto','Tax name')}<input name="taxName" maxlength="40" required value="${esc(tax.name)}"></label><label>${tr('Tasa (%)','Rate (%)')}<input name="taxRate" type="number" min="0" max="100" step="0.001" required value="${tax.rate === null ? '' : esc(tax.rate)}"></label><button type="button" data-remove-tax aria-label="${tr('Quitar impuesto','Remove tax')}">×</button>`;
    node.querySelector('button').onclick = () => { if (taxRows.children.length > 1) node.remove(); };
    taxRows.append(node);
  }
  function preset() {
    const p = R.preset(form.elements.country.value, form.elements.region.value);
    form.elements.currency.value = p.currency;
    form.elements.locale.value = p.locale;
    taxRows.replaceChildren(); p.taxes.forEach(row);
    source.replaceChildren();
    if (p.source) {
      const link = document.createElement('a'); link.href = p.source; link.target = '_blank'; link.rel='noopener'; link.textContent = tr('Consultar fuente oficial','Official source');
      source.append(link, ` · ${tr('Revisado','Reviewed')}: ${p.reviewed}`);
    }
    form.querySelector('[data-country-note]').textContent = p.country === 'US'
      ? tr('Introduce la tasa estatal y local aplicable a tu operación. No existe una tasa nacional única.','Enter the state and local rate applicable to your transaction. There is no single national rate.')
      : p.country === 'CA' ? tr('Elige una provincia de ejemplo o introduce los impuestos correspondientes al lugar de suministro. HST se muestra como una única tasa.','Choose a province example or enter the taxes applicable to the place of supply. HST is displayed as one combined rate.')
      : p.country === 'ES' ? tr('21% es el tipo general. Puedes usar 10%, 4%, 0% u otra tasa aplicable a tu operación.','21% is the standard rate. Use 10%, 4%, 0% or another applicable rate for your transaction.')
      : tr('Las tasas sugeridas son editables. Un campo vacío no significa 0%. Para una operación sin impuesto, introduce 0 explícitamente.','Suggested rates are editable. An empty field does not mean 0%. Enter 0 explicitly for a transaction without tax.');
    form.querySelector('[data-province]').hidden = p.country !== 'CA';
  }
  function show() {
    returnFocus = document.activeElement;
    const p = R.get();
    form.elements.country.value = p.country;
    form.elements.region.value = p.region;
    preset();
    form.elements.currency.value = p.currency;
    form.elements.locale.value = p.locale;
    form.elements.units.value = p.units;
    form.elements.priceMode.value = p.priceMode;
    for (const input of form.querySelectorAll('[data-freight-field]')) input.value = (p.freight || R.preset().freight)[input.dataset.freightField];
    taxRows.replaceChildren(); p.taxes.forEach(row);
    const doc = R.getDocument();
    editor.replaceChildren();
    if (doc?.items) {
      const title = document.createElement('h3'); title.textContent=tr('Impuesto por concepto (%)','Tax per line item (%)'); editor.append(title);
      const help = document.createElement('p');help.textContent=tr('Vacío: usa los impuestos generales. 0: tasa cero para ese concepto.','Blank: use general taxes. 0: zero rate for that line.');editor.append(help);
      for (const item of doc.items) {
        const label=document.createElement('label');label.textContent=item.description || item.concept || tr('Concepto sin nombre','Unnamed item');
        const input=document.createElement('input');input.type='number';input.min='0';input.max='100';input.step='.001';input.dataset.taxItem=item.id;input.value=item.taxRate ?? '';label.append(input);editor.append(label);
      }
    }
    form.querySelector('[data-region-message]').textContent='';
    dialog.showModal(); form.elements.country.focus();
  }
  function save(apply) {
    if (!form.reportValidity()) return;
    const country=form.elements.country.value;
    const value={...R.get(), country, region:country==='CA'?form.elements.region.value:'', currency:form.elements.currency.value.trim().toUpperCase(), locale:form.elements.locale.value.trim(), units:form.elements.units.value, priceMode:form.elements.priceMode.value,
      taxes:[...taxRows.children].map(el=>({name:el.querySelector('[name=taxName]').value.trim(),rate:Number(el.querySelector('[name=taxRate]').value)})), source:R.preset(country).source, reviewed:R.preset(country).reviewed};
    if (form.querySelector('[data-freight-field]')) value.freight=Object.fromEntries([...form.querySelectorAll('[data-freight-field]')].map(input=>[input.dataset.freightField,Number(input.value)]));
    const message=form.querySelector('[data-region-message]');
    try { R.validate(value); } catch { message.textContent=tr('Revisa país, moneda ISO, formato e impuestos. La suma de tasas no puede superar 100%.','Check country, ISO currency, locale and taxes. Combined rates cannot exceed 100%.');return; }
    if (apply) {
      const event=new CustomEvent('npp:before-region-apply',{cancelable:true,detail:value});
      if (!window.dispatchEvent(event)) { message.textContent=tr('Este registro ya tiene importes en otra moneda. Conserva su moneda para evitar reinterpretarlos. Puedes guardar la nueva preferencia para otros cálculos.','This ledger already contains amounts in another currency. Keep its currency to avoid reinterpreting them. Save the new preference for other calculations.');return; }
    }
    R.set(value);
    if (apply) {
      R.apply();
      const overrides=Object.fromEntries([...editor.querySelectorAll('[data-tax-item]')].map(input=>[input.dataset.taxItem,input.value===''?null:Number(input.value)]));
      R.getDocument()?.setTaxes?.(overrides);
    }
    dialog.close();renderSummary();
    const status=document.querySelector('[data-region-status]');
    if(status) status.textContent=apply?tr('Configuración aplicada al cálculo actual. No se convirtieron importes.','Settings applied to this calculation. No amounts were converted.'):tr('Preferencias guardadas para nuevos cálculos. El cálculo abierto mantiene su configuración.','Preferences saved for new calculations. The open calculation keeps its settings.');
  }
  function init() {
    const nav=document.querySelector('.npp-tool-nav-links') || document.querySelector('header');
    if (!nav || document.querySelector('[data-region-open]')) return;
    const css=document.createElement('link');css.rel='stylesheet';css.href=new URL('../css/regional-settings.css',document.querySelector('script[data-npp-regional-ui]').src).href;document.head.append(css);
    launch=document.createElement('button');launch.type='button';launch.className='npp-region-open';launch.dataset.regionOpen='';launch.setAttribute('aria-haspopup','dialog');launch.setAttribute('aria-label',tr('País, moneda e impuestos','Country, currency and taxes'));launch.onclick=show;nav.append(launch);
    if(document.body.dataset.appId) {
      const block=document.createElement('section');block.className='npp-region-bar';block.setAttribute('aria-label',tr('Configuración regional','Regional settings'));block.innerHTML='<p class="npp-region-summary"></p><p data-region-jurisdiction hidden></p><p data-region-status role="status"></p>';
      const anchor=document.querySelector('.npp-tool-nav');if(anchor)anchor.after(block);
    }
    dialog=document.createElement('dialog');dialog.className='npp-region-dialog';dialog.setAttribute('aria-labelledby','npp-region-title');
    dialog.innerHTML=`<form><div class="npp-region-heading"><h2 id="npp-region-title">${tr('País, moneda e impuestos','Country, currency and taxes')}</h2><button type="button" data-region-close aria-label="${tr('Cerrar','Close')}">×</button></div>
      <p>${tr('El idioma se elige por separado. Los importes guardados mantienen su moneda; no se realiza conversión automática.','Language is selected separately. Saved amounts keep their currency; no automatic conversion is performed.')}</p>
      <div class="npp-region-grid"><label>${tr('País','Country')}<select name="country">${Object.entries(R.countries).map(([code,c])=>`<option value="${code}">${c.name[en?1:0]}</option>`).join('')}</select></label>
      <label data-province>${tr('Provincia de ejemplo','Province example')}<select name="region"><option value="">${tr('Introducir tasas manualmente','Enter rates manually')}</option><option value="ON">Ontario · HST 13%</option><option value="NS">Nova Scotia · HST 14%</option><option value="MB">Manitoba · GST 5% + PST 7%</option></select></label>
      <label>${tr('Moneda (código ISO)','Currency (ISO code)')}<input name="currency" pattern="[A-Za-z]{3}" maxlength="3" required list="npp-currencies"><datalist id="npp-currencies">${['PEN','USD','CAD','EUR','GBP','MXN','CLP','COP','BRL','JPY','AUD','CHF'].map(c=>`<option value="${c}">`).join('')}</datalist></label>
      <label>${tr('Formato de números y fechas','Number and date format')}<input name="locale" required list="npp-locales"><datalist id="npp-locales">${['es-PE','es-ES','en-US','en-CA','en-GB','fr-CA','de-DE','fr-FR','es-MX'].map(c=>`<option value="${c}">`).join('')}</datalist></label>
      <label>${tr('Unidades de flete','Shipping units')}<select name="units"><option value="metric">kg / km</option><option value="imperial">lb / mi</option></select></label>
      <label>${tr('Precios introducidos en documentos','Entered document prices')}<select name="priceMode"><option value="excluded">${tr('Sin impuesto: añadir al total','Tax excluded: add to total')}</option><option value="included">${tr('Con impuesto: desglosar del precio','Tax included: extract from price')}</option></select></label></div>
      <h3>${tr('Impuestos de venta','Sales taxes')}</h3><p data-country-note></p><div data-tax-rows></div><button type="button" data-add-tax>${tr('Añadir componente de impuesto','Add tax component')}</button><p data-tax-source></p><div data-tax-items></div>
      <p role="alert" data-region-message></p><div class="npp-region-actions"><button type="button" data-save-defaults>${tr('Guardar para nuevos cálculos','Save for new calculations')}</button><button type="submit">${tr('Aplicar al cálculo actual','Apply to current calculation')}</button></div></form>`;
    document.body.append(dialog);form=dialog.querySelector('form');source=form.querySelector('[data-tax-source]');taxRows=form.querySelector('[data-tax-rows]');editor=form.querySelector('[data-tax-items]');
    if(document.body.dataset.appId==='calculadora-flete-envio-local') {
      const freight=document.createElement('fieldset');freight.className='npp-region-grid';
      const legend=document.createElement('legend');legend.textContent=tr('Tarifas de envío propias (valores de ejemplo, no tarifas oficiales)','Your shipping rates (sample values, not official rates)');freight.append(legend);
      const labels={base:['Base de zona centro','Central-zone base'],perKg:['Costo por kg','Cost per kg'],van:['Recargo van','Van surcharge'],truck:['Recargo camión','Truck surcharge'],expressMultiplier:['Multiplicador express','Express multiplier'],expressSurcharge:['Recargo express','Express surcharge'],volumetricDivisor:['Divisor volumétrico (cm³/kg)','Volumetric divisor (cm³/kg)']};
      for(const [key,label] of Object.entries(labels)){const node=document.createElement('label');node.textContent=label[en?1:0];const input=document.createElement('input');input.type='number';input.min=['expressMultiplier','volumetricDivisor'].includes(key)?'.001':'0';input.step='.001';input.required=true;input.dataset.freightField=key;node.append(input);freight.append(node);}
      form.querySelector('.npp-region-actions').before(freight);
    }
    form.elements.country.onchange=()=>{form.elements.region.value='';preset();};form.elements.region.onchange=preset;
    form.querySelector('[data-add-tax]').onclick=()=>{if(taxRows.children.length<5)row();};
    form.querySelector('[data-region-close]').onclick=()=>dialog.close();form.querySelector('[data-save-defaults]').onclick=()=>save(false);form.onsubmit=e=>{e.preventDefault();save(true);};
    dialog.addEventListener('close',()=>returnFocus?.focus());
    window.addEventListener('npp:region-saved',renderSummary);window.addEventListener('npp:region-apply',renderSummary);window.addEventListener('npp:document-region',renderSummary);
    renderSummary();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
