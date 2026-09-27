/**
 * Double-safety resilience guard for the language switcher on the main portal.
 * Guarantees that the ES|EN switch is always visible in the header navbar and footer,
 * regardless of React hydration, dynamic re-renders, or load order.
 */
(function () {
  "use strict";

  var isEn = (document.documentElement.lang || "").toLowerCase().startsWith("en") || window.location.pathname.indexOf("/en/") !== -1;

  function ensureNavSwitch() {
    var themeBtn = document.querySelector('header button[role="switch"]');
    if (themeBtn && !document.getElementById("np-nav-lang-switcher")) {
      var a = document.createElement("a");
      a.id = "np-nav-lang-switcher";
      a.href = isEn ? "/herramientas/" : "/en/tools/";
      a.className = "inline-flex items-center gap-1 rounded-full border border-white/15 bg-white/5 px-3 py-1.5 text-xs font-bold text-white transition hover:border-brand hover:bg-white/10";
      a.title = isEn ? "Cambiar a versión en Español" : "Switch to English version";
      a.setAttribute("aria-label", a.title);
      if (isEn) {
        a.innerHTML = '<span class="text-white/60 hover:text-white">ES</span><span class="text-white/30">|</span><span class="text-brand">EN</span>';
      } else {
        a.innerHTML = '<span class="text-brand">ES</span><span class="text-white/30">|</span><span class="text-white/60 hover:text-white">EN</span>';
      }
      themeBtn.parentNode.insertBefore(a, themeBtn);
    }

    var footerRight = document.querySelector(".np-portal-footer-right");
    if (footerRight && !document.getElementById("np-footer-lang-switcher")) {
      var fdiv = document.createElement("div");
      fdiv.id = "np-footer-lang-switcher";
      fdiv.className = "flex items-center gap-2 text-xs text-fg-muted my-1";
      if (isEn) {
        fdiv.innerHTML = '<span>Language / Idioma:</span><a href="/herramientas/" class="font-semibold text-cta hover:underline">Español</a><span>·</span><span class="font-bold text-brand">English</span>';
      } else {
        fdiv.innerHTML = '<span>Idioma / Language:</span><span class="font-bold text-brand">Español</span><span>·</span><a href="/en/tools/" class="font-semibold text-cta hover:underline">English</a>';
      }
      footerRight.insertBefore(fdiv, footerRight.firstChild);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ensureNavSwitch);
  } else {
    ensureNavSwitch();
  }

  [60, 200, 500, 1000, 2000].forEach(function (t) {
    window.setTimeout(ensureNavSwitch, t);
  });

  var root = document.getElementById("root") || document.body;
  var observer = new MutationObserver(function () {
    ensureNavSwitch();
  });
  observer.observe(root, { childList: true, subtree: true });
})();
