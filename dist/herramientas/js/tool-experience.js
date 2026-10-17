/* Layout-only enhancements. No form values or local business data are changed. */
(() => {
  'use strict';
  if (!document.body?.dataset.appId) return;
  const body = document.body;
  const english = document.documentElement.lang.startsWith('en');
  function scheme() {
    const value = window.NPPTheme?.get() || 'light';
    if (body.dataset.nppScheme !== value) body.dataset.nppScheme = value;
  }
  function layout() {
    scheme();
    document.querySelectorAll('#root button').forEach(button => {
      if (/^(Activar modo (claro|oscuro)|(?:Switch to|Enable) (light|dark) mode)$/i.test(button.getAttribute('aria-label') || '')) button.dataset.nppNativeTheme = '';
      if (button.innerText.trim() && !button.matches('[role="switch"], [role="checkbox"]')) button.classList.add('npp-text-control');
    });
    const excluded = '#quotationPreview, #invoicePreview, #contractPreview, [data-user-content], [contenteditable="true"], [data-visual-edit-component="SignaturePreview"]';
    document.querySelectorAll('#root table, .op-main table').forEach(table => {
      if (table.closest(excluded) || table.closest('.npp-table-scroll')) return;
      const parent = table.parentElement;
      if (/auto|scroll/.test(getComputedStyle(parent).overflowX)) return;
      // Keep React-owned nodes in place so tab changes can unmount them safely.
      parent.classList.add('npp-table-scroll');
      if (!parent.hasAttribute('tabindex')) parent.tabIndex = 0;
      if (!parent.hasAttribute('role')) parent.setAttribute('role', 'region');
      if (!parent.hasAttribute('aria-label') && !parent.hasAttribute('aria-labelledby')) parent.setAttribute('aria-label', english ? 'Table: scroll horizontally to see all columns' : 'Tabla: desplázate horizontalmente para ver todas las columnas');
    });
    if (body.dataset.appId === 'calculadora-precios-venta-igv') {
      document.querySelectorAll('#root .overflow-x-auto').forEach(row => {
        if (row.querySelector('button') && !row.querySelector('table, input')) row.classList.add('npp-mobile-tabs');
      });
    }
  }
  let pending = false;
  const observer = new MutationObserver(() => {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => { pending = false; layout(); });
  });
  // Child changes include React tabs, drawers and generated results.
  observer.observe(body, {childList:true, subtree:true});
  new MutationObserver(scheme).observe(document.documentElement, {attributes:true, attributeFilter:['class', 'data-theme', 'style']});
  const nav = document.querySelector('.npp-tool-nav');
  if (nav) new ResizeObserver(() => body.style.setProperty('--npp-nav-height', `${nav.offsetHeight}px`)).observe(nav);
  layout();
})();
