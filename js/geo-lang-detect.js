/**
 * NubeParaPymes — Intelligent Language & Geo Suggestion Banner
 * Detects browser language (e.g., English-speaking users on Spanish pages)
 * and displays an elegant, non-intrusive suggestion to switch versions.
 * 
 * Safe for SEO: Bypasses search engine bots (Googlebot, Bing, GPTBot, etc.)
 * Remembers user preference in localStorage.
 */
(function () {
  "use strict";

  // 1. Guard against search engine and AI crawlers
  var botPattern = /bot|googlebot|crawler|spider|robot|crawling|gptbot|claudebot|perplexity|bingbot|duckduckbot|slurp|facebookexternalhit|applebot/i;
  if (botPattern.test(navigator.userAgent)) {
    return;
  }

  var isEn = (document.documentElement.lang || "").toLowerCase().startsWith("en") || window.location.pathname.indexOf("/en/") !== -1;
  var pageLang = isEn ? "en" : "es";

  // Check saved preference
  var savedPref = null;
  try {
    savedPref = localStorage.getItem("np_lang_pref");
  } catch (e) {}

  if (savedPref) {
    return; // User has already made an explicit choice
  }

  // 2. Detect browser languages
  var userLanguages = navigator.languages || [navigator.language || navigator.userLanguage || "es"];
  var primaryLang = (userLanguages[0] || "es").toLowerCase();

  var userPrefersEnglish = primaryLang.startsWith("en");
  var userPrefersSpanish = primaryLang.startsWith("es");

  var shouldSuggestEn = !isEn && userPrefersEnglish;
  var shouldSuggestEs = isEn && userPrefersSpanish;

  if (!shouldSuggestEn && !shouldSuggestEs) {
    return; // User language matches current page language
  }

  // 3. Slug mapping to determine counterpart URL
  var SLUG_MAP = {
    "analizador-titulares": "headline-analyzer",
    "auditor-seo-basico": "basic-on-page-seo-auditor",
    "calculadora-descuentos-promociones": "discount-promotions-calculator",
    "calculadora-flete-envio-local": "local-shipping-calculator",
    "calculadora-precios-venta-igv": "sales-pricing-tax-calculator",
    "calculadora-prestamos-amortizaciones": "loan-amortization-calculator",
    "calculadora-sobrecostos-laborales": "labor-cost-payroll-burden-calculator",
    "comparador-campanas-avanzado": "advanced-campaign-comparator",
    "consola-campanas": "campaign-utm-console",
    "conversor-optimizador-imagenes": "image-converter-optimizer",
    "creador-facturas-proforma": "proforma-invoice-generator",
    "crm-pymes": "smb-crm",
    "firma-correo-html": "html-email-signature",
    "flujo-caja-pymes": "cash-flow-tracker",
    "generador-codigos-qr": "qr-code-generator",
    "generador-contrasenas-pymes": "smb-password-generator",
    "generador-contratos-servicios": "service-contracts-generator",
    "generador-cotizaciones": "quote-estimate-generator",
    "generador-paletas-corporativas": "brand-palette-generator",
    "generador-politicas-devolucion": "return-policy-generator",
    "generador-politicas-terminos": "terms-privacy-generator",
    "guia-uso-22-apps": "user-guide",
    "guiones-manejo-objeciones": "objection-handling-scripts",
    "inventario-compras-pymes": "inventory-purchasing",
    "organizador-matriz-contenidos": "content-matrix-planner",
    "simulador-tco-fisico-nube": "cloud-vs-onprem-tco-simulator",
    "tareas-proyectos-pymes": "tasks-projects-tracker"
  };

  var REVERSE_SLUG_MAP = {};
  Object.keys(SLUG_MAP).forEach(function (k) {
    REVERSE_SLUG_MAP[SLUG_MAP[k]] = k;
  });

  function getTargetUrl() {
    var filename = window.location.pathname.split("/").pop() || "index.html";
    var baseName = filename.replace(/\.html$/i, "");

    if (shouldSuggestEn) {
      if (baseName === "index" || baseName === "") return "./en/index.html";
      if (baseName === "guia-uso-22-apps") return "./en/user-guide.html";
      var enSlug = SLUG_MAP[baseName] || baseName;
      return "./en/" + enSlug + ".html";
    } else {
      if (baseName === "index" || baseName === "") return "../index.html";
      if (baseName === "user-guide") return "../guia-uso-22-apps.html";
      var esSlug = REVERSE_SLUG_MAP[baseName] || baseName;
      return "../" + esSlug + ".html";
    }
  }

  var targetUrl = getTargetUrl();

  // 4. Render sleek banner
  function showBanner() {
    if (document.getElementById("np-geo-lang-toast")) return;

    var toast = document.createElement("aside");
    toast.id = "np-geo-lang-toast";
    toast.setAttribute("role", "dialog");
    toast.setAttribute("aria-live", "polite");

    var title = shouldSuggestEn ? "Prefer English?" : "¿Prefieres español?";
    var text = shouldSuggestEn 
      ? "We detected your browser is in English. Switch to our English tools portal?" 
      : "Detectamos que tu navegador está en español. ¿Cambiar a la versión en español?";
    var acceptLabel = shouldSuggestEn ? "Switch to English" : "Ver en español";
    var dismissLabel = shouldSuggestEn ? "Stay in Spanish" : "Continuar en inglés";

    toast.innerHTML = 
      '<div style="display:flex;align-items:flex-start;gap:12px;">' +
        '<span style="font-size:22px;line-height:1;" aria-hidden="true">🌐</span>' +
        '<div style="flex:1;">' +
          '<strong style="display:block;font-size:13px;font-weight:700;color:#fff;margin-bottom:2px;">' + title + '</strong>' +
          '<p style="margin:0;font-size:12px;color:#cbd5e1;line-height:1.4;">' + text + '</p>' +
          '<div style="display:flex;align-items:center;gap:8px;margin-top:10px;">' +
            '<a id="np-geo-accept" href="' + targetUrl + '" style="display:inline-flex;align-items:center;justify-content:center;padding:5px 12px;border-radius:999px;background:#f97316;color:#fff;font-size:11px;font-weight:700;text-decoration:none;transition:background .15s ease;">' + acceptLabel + '</a>' +
            '<button id="np-geo-dismiss" type="button" style="background:transparent;border:1px solid rgba(255,255,255,0.2);color:#94a3b8;font-size:11px;font-weight:600;padding:4px 10px;border-radius:999px;cursor:pointer;transition:all .15s ease;">' + dismissLabel + '</button>' +
          '</div>' +
        '</div>' +
        '<button id="np-geo-close" type="button" aria-label="Close" style="background:transparent;border:0;color:#94a3b8;font-size:16px;cursor:pointer;padding:0;line-height:1;">&times;</button>' +
      '</div>';

    // Apply inline CSS
    toast.style.position = "fixed";
    toast.style.bottom = "20px";
    toast.style.left = "20px";
    toast.style.zIndex = "2147483640";
    toast.style.maxWidth = "380px";
    toast.style.width = "calc(100vw - 40px)";
    toast.style.background = "rgba(11, 27, 49, 0.95)";
    toast.style.backdropFilter = "blur(12px)";
    toast.style.webkitBackdropFilter = "blur(12px)";
    toast.style.border = "1px solid rgba(59, 130, 246, 0.35)";
    toast.style.borderRadius = "14px";
    toast.style.padding = "14px 16px";
    toast.style.boxShadow = "0 14px 35px rgba(0, 0, 0, 0.45)";
    toast.style.fontFamily = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    toast.style.transform = "translateY(20px)";
    toast.style.opacity = "0";
    toast.style.transition = "transform .25s ease, opacity .25s ease";

    document.body.appendChild(toast);

    // Animate in
    window.requestAnimationFrame(function () {
      toast.style.transform = "translateY(0)";
      toast.style.opacity = "1";
    });

    function dismiss(chosenLang) {
      try {
        localStorage.setItem("np_lang_pref", chosenLang || pageLang);
      } catch (err) {}
      toast.style.transform = "translateY(20px)";
      toast.style.opacity = "0";
      window.setTimeout(function () {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 260);
    }

    var acceptBtn = document.getElementById("np-geo-accept");
    var dismissBtn = document.getElementById("np-geo-dismiss");
    var closeBtn = document.getElementById("np-geo-close");

    if (acceptBtn) {
      acceptBtn.addEventListener("click", function () {
        try {
          localStorage.setItem("np_lang_pref", shouldSuggestEn ? "en" : "es");
        } catch (err) {}
      });
    }

    if (dismissBtn) dismissBtn.addEventListener("click", function () { dismiss(pageLang); });
    if (closeBtn) closeBtn.addEventListener("click", function () { dismiss(pageLang); });
  }

  // Display after short delay to prevent layout interference
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      window.setTimeout(showBanner, 1200);
    });
  } else {
    window.setTimeout(showBanner, 1200);
  }
})();
