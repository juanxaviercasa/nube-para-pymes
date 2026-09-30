/* Change text nodes in place: preserve React nodes, events and user-entered data. */
(function () {
  if (!location.pathname.startsWith('/en/')) return;
  const dictionary = window.NPP_TOOL_TEXT || {};
  const patterns = (window.NPP_TOOL_PATTERNS || []).map(([source, target]) => [new RegExp(source, 'g'), target]);
  const excluded = 'script, style, textarea, input, [contenteditable="true"], [data-user-content]';
  function translate(value) {
    const key = value.trim().replace(/\s+/g, ' ');
    let translated = dictionary[key] || dictionary[value.trim()] || value.trim();
    for (const [pattern, target] of patterns) translated = translated.replace(pattern, (...match) => target.replace(/\$(\d+)/g, (_, index) => {
      const captured = match[Number(index)] || '';
      return dictionary[captured.trim()] || captured;
    }));
    return value.replace(value.trim(), () => translated);
  }
  function text(node) {
    if (!node.parentElement || node.parentElement.closest(excluded)) return;
    const next = translate(node.data);
    if (next !== node.data) node.data = next;
  }
  function visit(root) {
    if (!root) return;
    if (root.nodeType === Node.TEXT_NODE) return text(root);
    if (root.nodeType !== Node.ELEMENT_NODE || root.matches(excluded)) return;
    // A translated phrase may span typographic elements. Keep those elements
    // and their React identity; only update their existing text nodes.
    if (root.childNodes.length > 1 && root.matches('h1,h2,h3,p,div,td,th,footer,label,button,a,span,strong,small,li,option') && !root.querySelector('input,textarea,select,button,a,div,p,ul,ol,table,li')) {
      const value = root.textContent;
      const next = translate(value);
      if (value !== next) {
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
        let first = true;
        while (walker.nextNode()) {
          walker.currentNode.data = first ? next : '';
          first = false;
        }
      }
    }
    for (const name of ['placeholder', 'aria-label', 'title']) {
      const value = root.getAttribute(name);
      if (value && translate(value) !== value) root.setAttribute(name, translate(value));
    }
    root.childNodes.forEach(visit);
  }
  function start() {
    visit(document.body);
    new MutationObserver(records => records.forEach(record => {
      if (record.type === 'characterData') visit(record.target.parentElement);
      else if (record.type === 'attributes') visit(record.target);
      else record.addedNodes.forEach(visit);
    })).observe(document.body, {subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ['placeholder', 'aria-label', 'title']});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
