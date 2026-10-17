/* One preference for the directory and all tools; legacy keys remain in sync. */
(() => {
  'use strict';
  const html = document.documentElement;
  const read = key => { try { return localStorage.getItem(key); } catch { return null; } };
  let current = read('npp-theme');
  if (!['light', 'dark'].includes(current)) {
    const legacy = read('npp_dark');
    current = legacy === 'true' ? 'dark' : legacy === 'false' ? 'light' : read('theme') || read('qg_theme') || 'light';
  }
  function apply(value, persist = true) {
    current = value === 'dark' ? 'dark' : 'light';
    html.dataset.nppTheme = current;
    html.classList.toggle('dark', current === 'dark');
    html.style.colorScheme = current;
    if (document.body?.dataset.appId) document.body.dataset.nppScheme = current;
    if (persist) {
      try {
        localStorage.setItem('npp-theme', current);
        localStorage.setItem('npp_dark', JSON.stringify(current === 'dark'));
        localStorage.setItem('theme', current);
        localStorage.setItem('qg_theme', current);
      } catch { /* The theme still works when storage is unavailable. */ }
    }
    const english = html.lang.startsWith('en');
    document.querySelectorAll('[data-npp-theme-toggle]').forEach(button => {
      button.setAttribute('aria-pressed', String(current === 'dark'));
      button.setAttribute('aria-label', english ? 'Switch to '+(current === 'dark' ? 'light' : 'dark')+' mode' : 'Activar modo '+(current === 'dark' ? 'claro' : 'oscuro'));
      button.textContent = current === 'dark' ? (english ? '☀ Light' : '☀ Claro') : (english ? '☾ Dark' : '☾ Oscuro');
    });
  }
  apply(current);
  window.NPPTheme = {get: () => current, set: apply};
  new MutationObserver(() => {
    const value = html.classList.contains('dark') ? 'dark' : 'light';
    if (value !== current) apply(value);
  }).observe(html, {attributes:true, attributeFilter:['class']});
  document.addEventListener('DOMContentLoaded', () => apply(current), {once:true});
  document.addEventListener('click', event => {
    if (!event.target.closest('[data-npp-theme-toggle]')) return;
    const next = current === 'dark' ? 'light' : 'dark';
    // Keep native React theme state (including chart colours) synchronized.
    const native = [...document.querySelectorAll('[data-npp-native-theme]')].find(button =>
      new RegExp(next === 'dark' ? 'oscuro|dark' : 'claro|light', 'i').test(button.getAttribute('aria-label') || ''));
    if (native) native.click();
    apply(next);
  });
  window.addEventListener('storage', event => {
    if (event.key === 'npp-theme' && ['light', 'dark'].includes(event.newValue)) {
      const next = event.newValue;
      if (next !== current && document.body?.dataset.appId) {
        const native = [...document.querySelectorAll('[data-npp-native-theme]')].find(button =>
          new RegExp(next === 'dark' ? 'oscuro|dark' : 'claro|light', 'i').test(button.getAttribute('aria-label') || ''));
        if (native) native.click();
      }
      apply(next, false);
      // The directory's React state is initialized from the mirrored key.
      if (!document.body?.dataset.appId) location.reload();
    }
  });
})();
