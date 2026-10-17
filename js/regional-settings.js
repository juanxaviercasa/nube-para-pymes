/* Regional preferences and document snapshots. No exchange-rate conversion. */
((root, factory) => {
  const api = factory(root);
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.NPPRegion = api;
})(typeof window === 'undefined' ? globalThis : window, root => {
  'use strict';
  const KEY = 'npp_region_v1';
  const REVIEWED = '2026-10-17';
  const sources = {
    PE: 'https://emprender.sunat.gob.pe/principales-impuestos/impuesto-general-las-ventas-igv/impuesto-general-las-ventas',
    ES: 'https://sede.agenciatributaria.gob.es/Sede/iva/calculo-iva-repercutido-clientes/tipos-impositivos-iva.html',
    CA: 'https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/charge-collect-which-rate.html',
    US: 'https://www.cdtfa.ca.gov/taxes-and-fees/know-your-rate.htm'
  };
  const countries = {
    PE: {name: ['Perú', 'Peru'], currency: 'PEN', locale: 'es-PE', taxName: 'IGV', taxes: [{name: 'IGV', rate: 18}]},
    ES: {name: ['España', 'Spain'], currency: 'EUR', locale: 'es-ES', taxName: 'IVA', taxes: [{name: 'IVA', rate: 21}]},
    US: {name: ['Estados Unidos', 'United States'], currency: 'USD', locale: 'en-US', taxName: 'Sales tax', taxes: [{name: 'Sales tax', rate: null}]},
    CA: {name: ['Canadá', 'Canada'], currency: 'CAD', locale: 'en-CA', taxName: 'GST/HST', taxes: [{name: 'GST/HST', rate: null}]},
    GB: {name: ['Reino Unido', 'United Kingdom'], currency: 'GBP', locale: 'en-GB', taxName: 'VAT', taxes: [{name: 'VAT', rate: null}]},
    DE: {name: ['Alemania', 'Germany'], currency: 'EUR', locale: 'de-DE', taxName: 'VAT', taxes: [{name: 'VAT', rate: null}]},
    FR: {name: ['Francia', 'France'], currency: 'EUR', locale: 'fr-FR', taxName: 'TVA', taxes: [{name: 'TVA', rate: null}]},
    MX: {name: ['México', 'Mexico'], currency: 'MXN', locale: 'es-MX', taxName: 'IVA', taxes: [{name: 'IVA', rate: null}]},
    CL: {name: ['Chile', 'Chile'], currency: 'CLP', locale: 'es-CL', taxName: 'IVA', taxes: [{name: 'IVA', rate: null}]},
    CO: {name: ['Colombia', 'Colombia'], currency: 'COP', locale: 'es-CO', taxName: 'IVA', taxes: [{name: 'IVA', rate: null}]},
    CUSTOM: {name: ['Otro país / Personalizado', 'Other country / Custom'], currency: 'USD', locale: 'en-US', taxName: 'Tax', taxes: [{name: 'Tax', rate: null}]}
  };
  const copy = value => JSON.parse(JSON.stringify(value));
  function preset(country = 'PE', region = '') {
    if (!countries[country]) country = 'CUSTOM';
    const item = countries[country];
    let taxes = copy(item.taxes);
    if (country === 'CA') {
      if (region === 'ON') taxes = [{name: 'HST', rate: 13}];
      if (region === 'NS') taxes = [{name: 'HST', rate: 14}];
      if (region === 'MB') taxes = [{name: 'GST', rate: 5}, {name: 'PST', rate: 7}];
    }
    return {version: 1, country, region, currency: item.currency, locale: item.locale, units: 'metric', priceMode: 'excluded', taxes,
      freight: {base: 10, perKg: 2, van: 15, truck: 40, expressMultiplier: 1.65, expressSurcharge: 5, volumetricDivisor: 5000},
      source: sources[country] || '', reviewed: sources[country] ? REVIEWED : null};
  }
  function validate(value) {
    if (!value || !countries[value.country]) throw Error('country');
    if (!/^[A-Z]{3}$/.test(value.currency)) throw Error('currency');
    try { new Intl.NumberFormat(value.locale, {style: 'currency', currency: value.currency}); new Intl.Locale(value.locale); } catch { throw Error('locale'); }
    if (!['metric', 'imperial'].includes(value.units)) throw Error('units');
    if (!['included', 'excluded'].includes(value.priceMode)) throw Error('priceMode');
    if (!Array.isArray(value.taxes) || !value.taxes.length || value.taxes.length > 5) throw Error('taxes');
    for (const tax of value.taxes) {
      if (typeof tax.name !== 'string' || !tax.name.trim() || tax.name.length > 40 || !Number.isFinite(tax.rate) || tax.rate < 0 || tax.rate > 100) throw Error('rate');
    }
    if (value.taxes.reduce((sum, t) => sum + t.rate, 0) > 100) throw Error('rate');
    if (value.freight) for (const [key, amount] of Object.entries(value.freight)) {
      if (!Number.isFinite(amount) || amount < 0 || (['volumetricDivisor','expressMultiplier'].includes(key) && amount === 0)) throw Error('freight');
    }
    return copy({...value, version: 1, taxes: value.taxes.map(t => ({name: t.name.trim(), rate: t.rate}))});
  }
  function load() {
    try { const value = root.localStorage?.getItem(KEY); return value ? validate(JSON.parse(value)) : preset(); } catch { return preset(); }
  }
  let current = load();
  let draft = copy(current);
  const legacy = (currency = 'PEN') => ({...preset(), currency});
  const get = () => copy(current);
  const active = () => copy(draft);
  function set(value) {
    const next = validate(value);
    try { root.localStorage?.setItem(KEY, JSON.stringify(next)); } catch { /* Session use still works. */ }
    current = next;
    root.dispatchEvent?.(new CustomEvent('npp:region-saved', {detail: get()}));
    return get();
  }
  function use(value) { draft = validate(value); return active(); }
  function restore(value, currency) { return use(value || legacy(code(currency || 'PEN'))); }
  function apply() { use(current); root.dispatchEvent?.(new CustomEvent('npp:region-apply', {detail: active()})); }
  function rate(profile = draft) { return profile.taxes.reduce((sum, tax) => sum + tax.rate, 0); }
  function code(value = draft.currency) { return ({'S/': 'PEN', '$': 'USD', '€': 'EUR', '£': 'GBP'})[value] || value; }
  function money(value, currency = draft.currency, profile = draft, options = {}) {
    return new Intl.NumberFormat(profile.locale, {style: 'currency', currency: code(currency), currencyDisplay: 'code', minimumFractionDigits: 2, maximumFractionDigits: 2, ...options}).format(Number.isFinite(value) ? value : 0);
  }
  function number(value, profile = draft) { return new Intl.NumberFormat(profile.locale, {maximumFractionDigits: 2}).format(Number(value) || 0); }
  function formatter(options = {}) {
    const {currency, ...format} = options;
    if (format.maximumFractionDigits !== undefined && format.minimumFractionDigits === undefined) format.minimumFractionDigits = Math.min(2, format.maximumFractionDigits);
    return {format: value => money(value, draft.currency, draft, format)};
  }
  function date(value, profile = draft) {
    return value ? new Intl.DateTimeFormat(profile.locale, {dateStyle: 'medium'}).format(new Date(value + 'T12:00:00')) : '—';
  }
  function breakdown(amount, profile = draft, override = null) {
    const taxes = override === null ? profile.taxes : [{name: taxName(profile), rate: override}];
    const combined = taxes.reduce((sum, tax) => sum + tax.rate, 0) / 100;
    const net = profile.priceMode === 'included' ? amount / (1 + combined) : amount;
    const lines = taxes.map(tax => ({...tax, amount: net * tax.rate / 100}));
    const tax = lines.reduce((sum, line) => sum + line.amount, 0);
    return {net, tax, total: net + tax, lines};
  }
  function totals(items, profile = draft, amount = item => item.quantity * item.unitPrice * (1 - (item.discount || 0) / 100)) {
    const lines = items.map(item => breakdown(amount(item), profile, item.taxRate ?? null));
    return {subtotal: lines.reduce((sum, line) => sum + line.net, 0), igv: lines.reduce((sum, line) => sum + line.tax, 0), total: lines.reduce((sum, line) => sum + line.total, 0), lines};
  }
  function taxName(profile = draft) { return profile.taxes.map(tax => tax.name).join(' + '); }
  function taxLabel(profile = draft, items = documentBridge?.items || []) {
    if(items.some(item => item.taxRate !== null && item.taxRate !== undefined)) return taxName(profile) + (root.document?.documentElement.lang.startsWith('en') ? ' (rates per item)' : ' (tasas por concepto)');
    return profile.taxes.map(tax => `${tax.name} (${tax.rate}%)`).join(' + ');
  }
  function weight(kg, profile = draft) { return `${number(profile.units === 'imperial' ? kg / .45359237 : kg, profile)} ${profile.units === 'imperial' ? 'lb' : 'kg'}`; }
  function freight() { return {...preset().freight, ...draft.freight}; }
  function unit(text) {
    if(draft.units !== 'imperial') return text;
    return text.replace(/(\d+(?:\.\d+)?)(\s*(?:a|to|–|-)\s*(\d+(?:\.\d+)?))?\s*(kg|cm|km)\b/g, (_, a, range, b, kind) => {
      const factor={kg:1/.45359237,cm:1/2.54,km:1/1.609344}[kind];
      return number(Number(a)*factor)+(range?' – '+number(Number(b)*factor):'')+' '+({kg:'lb',cm:'in',km:'mi'})[kind];
    }).replace(/\bkg\b/g,'lb').replace(/\bcm\b/g,'in').replace(/\bkm\b/g,'mi');
  }
  let documentBridge;
  function documentAPI(value) { documentBridge = value; }
  function connect(React, handler) {
    const [, update] = React.useState(0);
    const callback = React.useRef(handler); callback.current = handler;
    React.useEffect(() => {
      const listener = () => { callback.current?.(active()); update(value => value + 1); };
      root.addEventListener('npp:region-apply', listener);
      return () => root.removeEventListener('npp:region-apply', listener);
    }, []);
  }
  const api = {KEY, countries, preset, validate, get, active, set, use, restore, apply, legacy, rate, code, money, number, date, formatter, breakdown, totals, taxName, taxLabel, weight, freight, unit, snapshot: active, documentAPI, getDocument: () => documentBridge, connect};
  if (root.document) {
    root.addEventListener('storage', event => { if (event.key === KEY) { current = load(); root.dispatchEvent(new CustomEvent('npp:region-saved', {detail:get()})); } });
  }
  return api;
});
