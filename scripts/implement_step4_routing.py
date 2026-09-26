import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

SLUG_MAP = {
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
    "guiones-manejo-objeciones": "objection-handling-scripts",
    "inventario-compras-pymes": "inventory-purchasing",
    "organizador-matriz-contenidos": "content-matrix-planner",
    "simulador-tco-fisico-nube": "cloud-vs-onprem-tco-simulator",
    "tareas-proyectos-pymes": "tasks-projects-tracker"
}

# 1. Update root index.html
print("Updating root index.html...")
index_path = ROOT / "index.html"
index_content = index_path.read_text(encoding="utf-8")

# Nav language switcher
nav_switcher_es = """
              <a href="./en/index.html" class="inline-flex items-center gap-1 rounded-full border border-white/15 bg-white/5 px-3 py-1.5 text-xs font-bold text-white transition hover:border-brand hover:bg-white/10" title="Switch to English version" aria-label="Switch to English version">
                <span class="text-brand">ES</span>
                <span class="text-white/30">|</span>
                <span class="text-white/60 hover:text-white">EN</span>
              </a>
"""
if 'href="./en/index.html"' not in index_content:
    index_content = index_content.replace(
        '<button type="button" role="switch" aria-checked="false" aria-label="Alternar modo oscuro"',
        nav_switcher_es.strip() + '\n              <button type="button" role="switch" aria-checked="false" aria-label="Alternar modo oscuro"'
    )

# Footer language switcher
footer_lang_es = """
            <div class="flex items-center gap-2 text-xs text-fg-muted my-1">
              <span>Idioma / Language:</span>
              <span class="font-bold text-brand">Español</span>
              <span>·</span>
              <a href="./en/index.html" class="font-semibold text-cta hover:underline">English</a>
            </div>
"""
if '<span>Idioma / Language:</span>' not in index_content:
    index_content = index_content.replace(
        '<a href="./guia-uso-22-apps.html" class="text-sm font-semibold text-cta underline-offset-4 hover:underline">Guía completa de uso →</a>',
        footer_lang_es.strip() + '\n            <a href="./guia-uso-22-apps.html" class="text-sm font-semibold text-cta underline-offset-4 hover:underline">Guía completa de uso →</a>'
    )
index_path.write_text(index_content, encoding="utf-8")


# 2. Update en/index.html
print("Updating en/index.html...")
en_index_path = EN_DIR / "index.html"
en_index_content = en_index_path.read_text(encoding="utf-8")

nav_switcher_en = """
              <a href="../index.html" class="inline-flex items-center gap-1 rounded-full border border-white/15 bg-white/5 px-3 py-1.5 text-xs font-bold text-white transition hover:border-brand hover:bg-white/10" title="Cambiar a versión en Español" aria-label="Cambiar a versión en Español">
                <span class="text-white/60 hover:text-white">ES</span>
                <span class="text-white/30">|</span>
                <span class="text-brand">EN</span>
              </a>
"""
if 'href="../index.html"' not in en_index_content:
    en_index_content = en_index_content.replace(
        '<button type="button" role="switch" aria-checked="false" aria-label="Toggle dark mode"',
        nav_switcher_en.strip() + '\n              <button type="button" role="switch" aria-checked="false" aria-label="Toggle dark mode"'
    )

footer_lang_en = """
            <div class="flex items-center gap-2 text-xs text-fg-muted my-1">
              <span>Language / Idioma:</span>
              <a href="../index.html" class="font-semibold text-cta hover:underline">Español</a>
              <span>·</span>
              <span class="font-bold text-brand">English</span>
            </div>
"""
if '<span>Language / Idioma:</span>' not in en_index_content:
    en_index_content = en_index_content.replace(
        '<a href="./user-guide.html" class="text-sm font-semibold text-cta underline-offset-4 hover:underline">Complete User Guide →</a>',
        footer_lang_en.strip() + '\n            <a href="./user-guide.html" class="text-sm font-semibold text-cta underline-offset-4 hover:underline">Complete User Guide →</a>'
    )
en_index_path.write_text(en_index_content, encoding="utf-8")


# 3. Update root guia-uso-22-apps.html
print("Updating root guia-uso-22-apps.html...")
guide_path = ROOT / "guia-uso-22-apps.html"
guide_content = guide_path.read_text(encoding="utf-8")
if 'href="./en/user-guide.html"' not in guide_content:
    guide_content = guide_content.replace(
        '<div class="top"><a class="brand" href="./index.html">NubeParaPymes</a><a class="back" href="./index.html">Volver al directorio</a></div>',
        '<div class="top"><a class="brand" href="./index.html">NubeParaPymes</a><div style="display:flex;align-items:center;gap:14px;"><a class="lang-toggle" href="./en/user-guide.html" style="font-size:.85rem;font-weight:600;padding:4px 10px;border-radius:6px;border:1px solid var(--line);background:#132d4b;color:#fff;text-decoration:none;">EN</a><a class="back" href="./index.html">Volver al directorio</a></div></div>'
    )
    guide_path.write_text(guide_content, encoding="utf-8")


# 4. Enhance css/ayuda-apps.css
print("Updating css/ayuda-apps.css...")
css_path = ROOT / "css" / "ayuda-apps.css"
css_content = css_path.read_text(encoding="utf-8")

floating_styles = """
.np-lang-switch-floating{position:fixed;top:14px;right:18px;z-index:2147482500;display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.24);background:rgba(9,26,46,.88);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);color:#edf4ff;font:700 12px/1 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:.04em;text-decoration:none!important;box-shadow:0 8px 24px rgba(0,0,0,.35);transition:transform .18s ease,border-color .18s ease,background .18s ease}.np-lang-switch-floating:hover{transform:translateY(-2px);border-color:rgba(255,122,24,.7);background:rgba(13,32,55,.95)}.np-lang-switch-floating .np-lang-active{color:#ff7a18;font-weight:800}.np-lang-switch-floating .np-lang-sep{color:rgba(255,255,255,.3)}.np-lang-switch-floating .np-lang-inactive{color:rgba(237,244,255,.65)}.np-footer-lang{border:1px solid rgba(249,115,22,.5)!important;background:rgba(249,115,22,.12)!important;color:#fb923c!important}.np-footer-lang:hover{border-color:#f97316!important;background:#f97316!important;color:#fff!important}@media(max-width:560px){.np-lang-switch-floating{top:10px;right:12px;padding:5px 10px;font-size:11px}}
"""
if ".np-lang-switch-floating" not in css_content:
    css_content += "\n" + floating_styles.strip()
    css_path.write_text(css_content, encoding="utf-8")


# 5. Enhance js/ayuda-apps.js
print("Updating js/ayuda-apps.js...")
js_path = ROOT / "js" / "ayuda-apps.js"
js_code = """(function () {
  "use strict";

  var isEn = (document.documentElement.lang || "").toLowerCase().startsWith("en") || window.location.pathname.indexOf("/en/") !== -1;

  function loadDemoExperience() {
    if (!document.body || !document.body.dataset.appId) return false;
    if (document.querySelector("script[data-np-demo-experience]")) return true;
    var script = document.createElement("script");
    script.src = isEn ? "../js/demo-experience.js" : "./js/demo-experience.js";
    script.async = false;
    script.dataset.npDemoExperience = "true";
    document.head.appendChild(script);
    return true;
  }

  if (!loadDemoExperience()) {
    var demoAttempts = 0;
    var demoTimer = window.setInterval(function () {
      if (loadDemoExperience() || ++demoAttempts > 30) window.clearInterval(demoTimer);
    }, 80);
  }

  var config = window.NP_HELP_CONFIG;
  if (!config || !config.id) return;

  var storageKey = "np-help-seen-" + config.id;
  var tourKey = "np-tour-done-" + config.id;
  var activeTarget = null;
  var tourCard = null;
  var tourIndex = 0;

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function visible(element) {
    if (!element) return false;
    var style = window.getComputedStyle(element);
    var rect = element.getBoundingClientRect();
    return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
  }

  function findTarget(selectors) {
    var list = Array.isArray(selectors) ? selectors : [selectors];
    for (var i = 0; i < list.length; i += 1) {
      try {
        var nodes = document.querySelectorAll(list[i]);
        for (var j = 0; j < nodes.length; j += 1) {
          if (visible(nodes[j]) && !nodes[j].closest(".np-help-panel,.np-help-tour-card,.np-help-button,.np-lang-switch-floating")) return nodes[j];
        }
      } catch (error) {}
    }
    return null;
  }

  function clearHighlight() {
    if (activeTarget) activeTarget.classList.remove("np-tour-highlight");
    activeTarget = null;
  }

  function closeTour() {
    clearHighlight();
    if (tourCard) tourCard.remove();
    tourCard = null;
    document.body.style.overflow = "";
  }

  function finishTour() {
    try { localStorage.setItem(tourKey, "1"); } catch (error) {}
    closeTour();
  }

  function renderTourStep() {
    if (!tourCard) return;
    var steps = config.steps || [];
    if (tourIndex >= steps.length) {
      finishTour();
      return;
    }
    clearHighlight();
    var step = steps[tourIndex];
    activeTarget = findTarget(step.selector);
    if (activeTarget) {
      activeTarget.classList.add("np-tour-highlight");
      activeTarget.scrollIntoView({ behavior: "smooth", block: "center" });
    }
    var stepLabel = isEn ? ("Step " + (tourIndex + 1) + " of " + steps.length) : ("Paso " + (tourIndex + 1) + " de " + steps.length);
    var exitLabel = isEn ? "Exit" : "Salir";
    var backLabel = isEn ? "Back" : "Atrás";
    var nextLabel = tourIndex === steps.length - 1 ? (isEn ? "Finish" : "Terminar") : (isEn ? "Next" : "Siguiente");

    tourCard.innerHTML =
      "<h3>" + escapeHtml(step.title || config.name) + "</h3>" +
      "<p>" + escapeHtml(step.text) + "</p>" +
      "<div class=\"np-help-tour-meta\"><small>" + stepLabel + "</small>" +
      "<span><button class=\"secondary np-help-skip\" type=\"button\" data-tour-action=\"skip\">" + exitLabel + "</button> " +
      (tourIndex > 0 ? "<button class=\"secondary\" type=\"button\" data-tour-action=\"back\">" + backLabel + "</button> " : "") +
      "<button type=\"button\" data-tour-action=\"next\">" + nextLabel + "</button></span></div>";
  }

  function startTour() {
    closeTour();
    tourIndex = 0;
    tourCard = document.createElement("aside");
    tourCard.className = "np-help-tour-card";
    tourCard.setAttribute("role", "dialog");
    tourCard.setAttribute("aria-live", "polite");
    tourCard.addEventListener("click", function (event) {
      var action = event.target.getAttribute("data-tour-action");
      if (action === "next") { tourIndex += 1; renderTourStep(); }
      if (action === "back") { tourIndex = Math.max(0, tourIndex - 1); renderTourStep(); }
      if (action === "skip") closeTour();
    });
    document.body.appendChild(tourCard);
    document.body.style.overflow = "hidden";
    renderTourStep();
  }

  function closePanel(backdrop) {
    if (backdrop) backdrop.remove();
    document.body.style.overflow = "";
  }

  function openHelp() {
    try { localStorage.setItem(storageKey, "1"); } catch (error) {}
    var backdrop = document.createElement("div");
    backdrop.className = "np-help-backdrop";
    backdrop.setAttribute("role", "presentation");

    var eyebrow = isEn ? "Quick Help" : "Ayuda rápida";
    var closeAria = isEn ? "Close help" : "Cerrar ayuda";
    var whyTitle = isEn ? "What it does" : "¿Para qué te ayuda?";
    var howTitle = isEn ? "Quick Start" : "Cómo empezar";
    var tipTitle = isEn ? "Pro Tip" : "Consejo práctico";
    var tourBtn = isEn ? "Start Step-by-Step Tour" : "Iniciar tour paso a paso";
    var guideBtn = isEn ? "Read Full Written Guide" : "Leer la guía escrita completa";
    var guideUrl = config.guide || (isEn ? "./user-guide.html" : "./guia-uso-22-apps.html");
    if (isEn && guideUrl.indexOf("guia-uso-22-apps.html") !== -1) {
      guideUrl = guideUrl.replace("guia-uso-22-apps.html", "user-guide.html");
    }

    backdrop.innerHTML =
      "<section class=\"np-help-panel\" role=\"dialog\" aria-modal=\"true\" aria-labelledby=\"np-help-title\">" +
      "<div class=\"np-help-head\"><div><p class=\"np-help-eyebrow\">" + eyebrow + "</p><h2 id=\"np-help-title\">" + escapeHtml(config.name) + "</h2></div>" +
      "<button class=\"np-help-close\" type=\"button\" aria-label=\"" + closeAria + "\" data-help-action=\"close\">×</button></div>" +
      "<div class=\"np-help-body\"><h3>" + whyTitle + "</h3><p>" + escapeHtml(config.purpose) + "</p>" +
      "<h3>" + howTitle + "</h3><ol class=\"np-help-steps\">" + (config.quick || []).map(function (step) { return "<li>" + escapeHtml(step) + "</li>"; }).join("") + "</ol>" +
      "<h3>" + tipTitle + "</h3><p>" + escapeHtml(config.tip) + "</p>" +
      "<div class=\"np-help-actions\"><button class=\"np-help-action\" type=\"button\" data-help-action=\"tour\">" + tourBtn + "</button><a class=\"np-help-link\" href=\"" + escapeHtml(guideUrl) + "\">" + guideBtn + "</a></div></div></section>";
    backdrop.addEventListener("click", function (event) {
      if (event.target === backdrop || event.target.getAttribute("data-help-action") === "close") closePanel(backdrop);
      if (event.target.getAttribute("data-help-action") === "tour") { closePanel(backdrop); startTour(); }
    });
    document.body.appendChild(backdrop);
    document.body.style.overflow = "hidden";
    var closeButton = backdrop.querySelector("[data-help-action=close]");
    if (closeButton) closeButton.focus();
  }

  function init() {
    // 1. Help button
    if (!document.querySelector(".np-help-button")) {
      var button = document.createElement("button");
      button.className = "np-help-button";
      button.type = "button";
      button.setAttribute("aria-label", (isEn ? "Open help & tour for " : "Abrir ayuda y tour de ") + config.name);
      button.innerHTML = "<span aria-hidden=\"true\">?</span><span>" + (isEn ? "Help & Tour" : "Ayuda y tour") + "</span>";
      button.addEventListener("click", openHelp);
      document.body.appendChild(button);
      try {
        if (!localStorage.getItem(storageKey)) {
          button.classList.add("np-help-first-visit");
          window.setTimeout(function () { button.classList.remove("np-help-first-visit"); }, 4200);
        }
      } catch (error) {}
    }

    // 2. Floating language switcher
    if (!document.querySelector(".np-lang-switch-floating")) {
      var switcher = document.createElement("a");
      switcher.className = "np-lang-switch-floating";
      var currentFile = window.location.pathname.split("/").pop() || "index.html";

      var slugMap = {
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
        "guiones-manejo-objeciones": "objection-handling-scripts",
        "inventario-compras-pymes": "inventory-purchasing",
        "organizador-matriz-contenidos": "content-matrix-planner",
        "simulador-tco-fisico-nube": "cloud-vs-onprem-tco-simulator",
        "tareas-proyectos-pymes": "tasks-projects-tracker"
      };

      if (isEn) {
        var esTarget = "../" + config.id + ".html";
        switcher.href = esTarget;
        switcher.title = "Cambiar a versión en Español";
        switcher.setAttribute("aria-label", "Cambiar a versión en Español");
        switcher.innerHTML = '<span class=\"np-lang-inactive\">ES</span><span class=\"np-lang-sep\">|</span><span class=\"np-lang-active\">EN</span>';
      } else {
        var enSlug = slugMap[config.id] || config.id;
        var enTarget = "./en/" + enSlug + ".html";
        switcher.href = enTarget;
        switcher.title = "Switch to English version";
        switcher.setAttribute("aria-label", "Switch to English version");
        switcher.innerHTML = '<span class=\"np-lang-active\">ES</span><span class=\"np-lang-sep\">|</span><span class=\"np-lang-inactive\">EN</span>';
      }
      document.body.appendChild(switcher);
    }

    document.addEventListener("keydown", function (event) {
      var tag = document.activeElement && document.activeElement.tagName;
      if (event.key === "?" && tag !== "INPUT" && tag !== "TEXTAREA" && tag !== "SELECT") openHelp();
      if (event.key === "Escape") {
        var backdrop = document.querySelector(".np-help-backdrop");
        if (backdrop) closePanel(backdrop); else if (tourCard) closeTour();
      }
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
"""
js_path.write_text(js_code, encoding="utf-8")


# 6. Update tool footers in root and en/
print("Updating tool footers in root and en/...")
for es_base, en_slug in SLUG_MAP.items():
    es_file = ROOT / f"{es_base}.html"
    if es_file.exists():
        es_text = es_file.read_text(encoding="utf-8", errors="ignore")
        # Add English footer link if not present
        if 'np-footer-lang' not in es_text and '<span class="np-global-links">' in es_text:
            en_footer_btn = f'<a class="np-footer-link np-footer-lang" href="./en/{en_slug}.html">English (EN)</a>'
            es_text = es_text.replace(
                '<span class="np-global-links">',
                f'<span class="np-global-links">{en_footer_btn}'
            )
            es_file.write_text(es_text, encoding="utf-8")

    # In en/ files (both es_slug and en_slug)
    for target_name in [f"{es_base}.html", f"{en_slug}.html"]:
        en_file = EN_DIR / target_name
        if en_file.exists():
            en_text = en_file.read_text(encoding="utf-8", errors="ignore")
            if 'np-footer-lang' not in en_text and '<span class="np-global-links">' in en_text:
                es_footer_btn = f'<a class="np-footer-link np-footer-lang" href="../{es_base}.html">Español (ES)</a>'
                en_text = en_text.replace(
                    '<span class="np-global-links">',
                    f'<span class="np-global-links">{es_footer_btn}'
                )
                en_file.write_text(en_text, encoding="utf-8")

print("Step 4 routing & language switchers successfully implemented across all pages!")
