(() => {
 'use strict';
 const config = window.NP_TUTORIAL_PORTAL;
 if (!config || !Array.isArray(config.tools)) return;
 function decorate() {
  // Never insert links beside the start-result tiles: they are grid cells.
  document.querySelectorAll('[data-npp-tutorial-card]').forEach(link => {
   if (!link.closest('article')) link.remove();
  });
  for (const card of document.querySelectorAll('article[data-visual-edit-loc*="ToolCard"], article[data-npp-tool-card]')) {
   const links = [...card.querySelectorAll('a[href]')];
   const tool = config.tools.find(tool => links.some(link => new URL(link.href, location.href).pathname === tool.route));
   if (!tool || card.querySelector('[data-npp-tutorial-card]')) continue;
   if (!/^https:\/\/todolima\.com\/herramientas\/[a-z0-9-]+$/.test(tool.url) && !/^\/(?:herramientas\/guia-uso|en\/user-guide)\/#/.test(tool.url)) continue;
   const launch = links.find(link => new URL(link.href, location.href).pathname === tool.route);
   launch.classList.add('npp-tool-primary-action');
   const link = document.createElement('a');
   link.href = tool.url;
   if (tool.illustrated) { link.target = '_blank'; link.rel = 'noopener noreferrer'; }
   link.className = 'npp-tutorial-card-link';
   link.dataset.nppTutorialCard = tool.slug;
   link.textContent = config.english ? 'View tutorial' : 'Ver tutorial';
   link.setAttribute('aria-label', link.textContent + ': ' + card.querySelector('h2,h3')?.textContent + (tool.illustrated ? (config.english ? ' (Spanish, new tab)' : ' (otra pestaña)') : ''));
   card.append(link);
  }
 }
 function start() {
  decorate();let queued = false;
  new MutationObserver(() => {if (queued) return;queued = true;requestAnimationFrame(() => {queued = false;decorate();});}).observe(document.querySelector('#root') || document.body, {childList:true,subtree:true});
 }
 if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
