/* Generated route data is prepended by the production build. */
(function () {
  'use strict';
  var routes = window.NPP_ROUTES;
  if (!routes) return;
  var pairs = routes.pairs;
  var reverse = {};
  Object.keys(pairs).forEach(function (key) { reverse[pairs[key]] = key; });
  function normalize(path) {
    if (routes.aliases[path]) return routes.aliases[path];
    path = path.replace(/\/index\.html$/, '/');
    if (!/\.[^/]+$/.test(path) && !path.endsWith('/')) path += '/';
    return routes.aliases[path] || path;
  }
  var path = normalize(location.pathname);
  var isEn = path.indexOf('/en/') === 0;
  var opposite = isEn ? reverse[path] : pairs[path];
  // An explicit URL always wins over an old cookie. A Spanish switch must never
  // be redirected back to English on arrival by a previous preference.
  function remember(lang) {
    try { localStorage.setItem('npp_user_lang', lang); } catch (_) {}
    try { document.cookie = 'npp_user_lang=' + lang + '; path=/; max-age=31536000; SameSite=Lax'; } catch (_) {}
  }
  remember(isEn ? 'en' : 'es');
  var selector = '.np-lang-toggle, .np-footer-lang, #np-nav-lang-switcher, #np-footer-lang-switcher a, .menu-item-lang-switcher a';
  function fixLink(a) {
    var raw = a.getAttribute('href');
    if (!raw || /^(#|mailto:|tel:|javascript:|data:)/i.test(raw)) return;
    var url;
    try { url = new URL(raw, location.href); } catch (_) { return; }
    if (url.origin !== location.origin && url.hostname !== 'nubeparapymes.online' && url.hostname !== 'apps.nubeparapymes.online') return;
    var switcher = a.matches(selector) || raw === './en/index.html';
    var target;
    if (switcher && opposite) {
      target = opposite;
      a.setAttribute('data-language-switch', 'true');
    } else {
      target = normalize(url.pathname);
      if (url.hostname === 'apps.nubeparapymes.online') target = routes.aliases[target] || (target === '/' ? '/herramientas/' : target);
      if (isEn && pairs[target]) target = pairs[target];
    }
    var next = target + url.search + url.hash;
    if (raw !== next) a.setAttribute('href', next);
  }
  function fixLinks(root) {
    if (root.matches && root.matches('a[href]')) fixLink(root);
    if (root.querySelectorAll) root.querySelectorAll('a[href]').forEach(fixLink);
  }
  function start() {
    function ensureSwitch() {
      if (!opposite || document.querySelector('.np-lang-toggle, #np-nav-lang-switcher')) return;
      var header = document.querySelector('.op-nav, header nav, header');
      if (!header) return;
      var link = document.createElement('a');
      link.className = 'np-lang-toggle';
      link.href = opposite;
      link.textContent = isEn ? 'EN | ES' : 'ES | EN';
      link.setAttribute('aria-label', isEn ? 'Cambiar a español' : 'Switch to English');
      link.style.cssText = 'display:inline-flex;align-items:center;white-space:nowrap;margin:8px;padding:6px 12px;border:1px solid currentColor;border-radius:999px;font-size:12px;font-weight:600;';
      header.appendChild(link);
    }
    ensureSwitch();
    fixLinks(document);
    new MutationObserver(function (records) {
      ensureSwitch();
      records.forEach(function (record) {
        if (record.type === 'attributes') fixLink(record.target);
        else record.addedNodes.forEach(fixLinks);
      });
    }).observe(document.body, {childList: true, subtree: true, attributes: true, attributeFilter: ['href']});
    document.addEventListener('click', function (event) {
      var a = event.target.closest && event.target.closest('a[href]');
      if (!a) return;
      fixLink(a);
      if (a.getAttribute('data-language-switch') === 'true') remember(isEn ? 'es' : 'en');
    }, true);
  }
  window.NPP_LANGUAGE = {normalize: normalize, opposite: opposite};
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
