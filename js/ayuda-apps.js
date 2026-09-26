(function () {
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
      .replace(/"/g, "&quot;")
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
      "<div class="np-help-tour-meta"><small>" + stepLabel + "</small>" +
      "<span><button class="secondary np-help-skip" type="button" data-tour-action="skip">" + exitLabel + "</button> " +
      (tourIndex > 0 ? "<button class="secondary" type="button" data-tour-action="back">" + backLabel + "</button> " : "") +
      "<button type="button" data-tour-action="next">" + nextLabel + "</button></span></div>";
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
      "<section class="np-help-panel" role="dialog" aria-modal="true" aria-labelledby="np-help-title">" +
      "<div class="np-help-head"><div><p class="np-help-eyebrow">" + eyebrow + "</p><h2 id="np-help-title">" + escapeHtml(config.name) + "</h2></div>" +
      "<button class="np-help-close" type="button" aria-label="" + closeAria + "" data-help-action="close">×</button></div>" +
      "<div class="np-help-body"><h3>" + whyTitle + "</h3><p>" + escapeHtml(config.purpose) + "</p>" +
      "<h3>" + howTitle + "</h3><ol class="np-help-steps">" + (config.quick || []).map(function (step) { return "<li>" + escapeHtml(step) + "</li>"; }).join("") + "</ol>" +
      "<h3>" + tipTitle + "</h3><p>" + escapeHtml(config.tip) + "</p>" +
      "<div class="np-help-actions"><button class="np-help-action" type="button" data-help-action="tour">" + tourBtn + "</button><a class="np-help-link" href="" + escapeHtml(guideUrl) + "">" + guideBtn + "</a></div></div></section>";
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
      button.innerHTML = "<span aria-hidden="true">?</span><span>" + (isEn ? "Help & Tour" : "Ayuda y tour") + "</span>";
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
        switcher.innerHTML = '<span class="np-lang-inactive">ES</span><span class="np-lang-sep">|</span><span class="np-lang-active">EN</span>';
      } else {
        var enSlug = slugMap[config.id] || config.id;
        var enTarget = "./en/" + enSlug + ".html";
        switcher.href = enTarget;
        switcher.title = "Switch to English version";
        switcher.setAttribute("aria-label", "Switch to English version");
        switcher.innerHTML = '<span class="np-lang-active">ES</span><span class="np-lang-sep">|</span><span class="np-lang-inactive">EN</span>';
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
