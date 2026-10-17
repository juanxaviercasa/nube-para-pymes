const test=require('node:test');
const assert=require('node:assert/strict');
const R=require('../js/regional-settings');
test('Peru is default regardless of interface language',()=>{
 assert.equal(R.get().country,'PE');assert.equal(R.rate(),18);assert.equal(R.get().currency,'PEN');
});
test('Unknown rate is not interpreted as zero',()=>{
 assert.throws(()=>R.validate(R.preset('US')));
 const p=R.preset('US');p.taxes[0].rate=0;assert.equal(R.validate(p).taxes[0].rate,0);
});
test('Inclusive and exclusive taxes share a net base',()=>{
 const p=R.preset('ES');assert.deepEqual(R.breakdown(100,p).lines.map(x=>x.amount),[21]);
 p.priceMode='included';const t=R.breakdown(121,p);assert.ok(Math.abs(t.net-100)<1e-9);assert.equal(t.total,121);
});
test('Canadian components are parallel, not compounded',()=>{
 const p=R.preset('CA','MB');const t=R.breakdown(100,p);assert.equal(t.total,112);assert.deepEqual(t.lines.map(x=>x.amount),[5,7]);
 assert.equal(R.rate(R.preset('CA','NS')),14);assert.equal(R.rate(R.preset('CA','ON')),13);
});
test('Line items may have explicit zero or reduced rates',()=>{
 const p=R.preset('ES');const result=R.totals([{quantity:1,unitPrice:100},{quantity:1,unitPrice:100,taxRate:0},{quantity:1,unitPrice:100,taxRate:10}],p);
 assert.equal(result.igv,31);assert.equal(result.total,331);
});
test('Preferences do not alter existing draft snapshots or perform conversion',()=>{
 R.use(R.preset());const old=R.snapshot();R.set(R.preset('ES'));
 assert.equal(R.active().currency,'PEN');assert.equal(old.taxes[0].rate,18);R.apply();
 assert.equal(R.active().currency,'EUR');assert.match(R.money(100),/100/);assert.equal(old.currency,'PEN');
});
test('Invalid tax rates and currencies fail validation',()=>{
 for(const bad of [null,-1,NaN,Infinity,101]){const p=R.preset();p.taxes[0].rate=bad;assert.throws(()=>R.validate(p));}
 const p=R.preset();p.currency='USD;';assert.throws(()=>R.validate(p));
});
test('Imperial labels and compact currency formatting',()=>{
 const p=R.preset();p.units='imperial';R.use(p);
 assert.match(R.unit('Hasta 5 kg'),/11[,.]02 lb/);
 assert.doesNotThrow(()=>R.formatter({maximumFractionDigits:0}).format(100));
 assert.match(R.weight(.45359237),/1 lb/);
});
