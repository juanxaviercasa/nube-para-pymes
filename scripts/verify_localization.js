/* Regression checks for the published bilingual artifact and browser router. */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..', 'dist');
const data = JSON.parse(fs.readFileSync(path.join(root, 'language-routes.json'), 'utf8'));
const manager = fs.readFileSync(path.join(root, 'wp-static-arquitect-assets/npp-lang-manager.js'), 'utf8');
const read = route => fs.readFileSync(path.join(root, route, 'index.html'), 'utf8');
let checks = 0;
function check(value, message) { assert.ok(value, message); checks++; }

function boot(route, stored = 'en') {
  const listeners = {};
  const storage = new Map([['npp_user_lang', stored]]);
  const location = {pathname: route, href: 'https://nubeparapymes.online' + route, origin: 'https://nubeparapymes.online', replace() {throw new Error('Unexpected automatic redirect');}};
  const document = {readyState: 'loading', cookie: 'npp_user_lang=' + stored, addEventListener(type, callback) {listeners[type] = callback;}};
  const window = {};
  vm.runInNewContext(manager, {window, location, document, URL, localStorage: {getItem: key => storage.get(key), setItem: (key, value) => storage.set(key, value)}, MutationObserver: class {observe() {}}});
  return {window, location, document, listeners, storage};
}

for (const [es, en] of Object.entries(data.pairs)) {
  for (const [route, opposite, lang] of [[es, en, 'es'], [en, es, 'en']]) {
    const html = read(route);
    check(html.includes(`lang="${lang}"`), `Wrong HTML language: ${route}`);
    check(html.includes(`hreflang="${lang === 'es' ? 'en' : 'es'}" href="https://nubeparapymes.online${opposite}"`), `Wrong alternate: ${route}`);
    const runtime = boot(route);
    check(runtime.window.NPP_LANGUAGE.opposite === opposite, `Wrong browser switch: ${route}`);
    check(runtime.storage.get('npp_user_lang') === lang, `Stale preference overrides ${route}`);
    check(boot(route + 'index.html').window.NPP_LANGUAGE.opposite === opposite, `index.html alias: ${route}`);
  }
}

const footerPages = ['privacy-policy', 'about-us', 'review-methodology', 'contact', 'terms-and-conditions', 'cookie-policy', 'disclaimer', 'legal-notice'];
const home = read('/en/');
for (const slug of footerPages) {
  check(home.includes(`href="/en/${slug}/"`), `English footer lacks ${slug}`);
  check(read('/en/' + slug + '/').includes('lang="en"'), `Missing English page ${slug}`);
}
check(!/Pol(?:í|&iacute;)tica de Privacidad|Metodolog(?:í|&iacute;)a de Rese(?:ñ|&ntilde;)as/.test(home), 'Spanish footer labels on English home');
const portal = read('/en/tools/');
check(/src="\/js\/en-index.js/.test(portal), 'English controller missing');
check(!/src="[^\"]*\/js\/index.js/.test(portal), 'Spanish React bundle overwrites English portal');
check(!portal.includes('./en/index.html'), 'Nested English portal link');
check(!fs.readFileSync(path.join(root, 'herramientas/js/index.js'), 'utf8').includes('./en/index.html'), 'React generates nested English links');
check(data.aliases['/en/tools/en/index.html'] === '/en/tools/', 'Reported broken URL has no recovery');

// Exercise dynamic React links, modifier-click-safe href repair, and switchers.
const runtime = boot('/en/tools/');
function anchor(href, switcher = false) {
  const attrs = {href};
  return {getAttribute: key => attrs[key] ?? null, setAttribute: (key, value) => {attrs[key] = value;}, matches: () => switcher, attrs};
}
const spanishLink = anchor('/herramientas/ventas/crm-pymes/?demo=1#pipeline');
const switchLink = anchor('./en/index.html', true);
runtime.document.querySelectorAll = () => [spanishLink, switchLink];
runtime.document.querySelector = () => switchLink;
runtime.document.body = {};
runtime.listeners.DOMContentLoaded();
check(spanishLink.attrs.href === '/en/smb-crm/?demo=1#pipeline', 'Dynamic tool link loses translation/query/hash');
check(switchLink.attrs.href === '/herramientas/', 'Dynamic portal switch is broken');
runtime.listeners.click({target: {closest: () => switchLink}});
check(runtime.storage.get('npp_user_lang') === 'es', 'Switch preference not stored');

// Redirects must not loop with Cloudflare's .html and /index.html normalization.
const rules = fs.readFileSync(path.join(root, '_redirects'), 'utf8').split(/\r?\n/).filter(line => line && !line.startsWith('#')).map(line => line.trim().split(/\s+/));
const redirects = new Map();
for (const [source, target, status] of rules) {
  check(['200', '301', '302', '303', '307', '308'].includes(status), `Unsupported redirect status: ${status}`);
  check(!redirects.has(source), `Duplicate redirect: ${source}`);
  redirects.set(source, target);
}
for (const source of redirects.keys()) {
  if (source.includes('*')) continue;
  const seen = new Set();
  let current = source;
  while (redirects.has(current)) {
    check(!seen.has(current), `Redirect loop: ${source}`);
    seen.add(current);
    current = redirects.get(current);
  }
  check(!current.endsWith('.html'), `Cloudflare extension redirect risk: ${source} -> ${current}`);
  check(fs.existsSync(path.join(root, current, 'index.html')) || fs.existsSync(path.join(root, current)), `Missing redirect destination: ${current}`);
}
console.log(`Localization: ${checks} checks passed across ${Object.keys(data.pairs).length} page pairs.`);
