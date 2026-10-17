(() => {
  'use strict';
  const config = window.NP_TUTORIAL_PORTAL;
  if (!config || !Array.isArray(config.tools)) return;
  function decorate() {
    for (const tool of config.tools) {
      const launch = Array.from(document.querySelectorAll('a[href]')).find(a => {
        const url = new URL(a.href, location.href);
        return url.origin === location.origin && url.pathname === tool.route;
      });
      if (!launch || document.querySelector('[data-npp-tutorial-card="' + tool.slug + '"]')) continue;
      if (!/^https:\/\/todolima\.com\/herramientas\/[a-z0-9-]+$/.test(tool.url)) continue;
      const link = document.createElement('a');
      link.href = tool.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.className = 'npp-tutorial-card-link';
      link.dataset.nppTutorialCard = tool.slug;
      link.textContent = config.english ? 'Illustrated tutorial (Spanish) ↗' : 'Tutorial con capturas ↗';
      link.setAttribute('aria-label', link.textContent + (config.english ? ' (opens in a new tab)' : ' (abre en otra pestaña)'));
      launch.insertAdjacentElement('afterend', link);
    }
  }
  function start() {
    decorate();
    let queued = false;
    new MutationObserver(() => {
      if (queued) return;
      queued = true;
      requestAnimationFrame(() => { queued = false; decorate(); });
    }).observe(document.querySelector('#root') || document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once:true});
  else start();
})();
