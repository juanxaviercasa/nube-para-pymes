(function () {
  "use strict";

  function loadDemoExperience() {
    if (!document.body || !document.body.dataset.appId || document.querySelector("script[data-np-demo-experience]")) return;
    var script = document.createElement("script");
    script.src = "./js/demo-experience.js";
    script.async = false;
    script.dataset.npDemoExperience = "true";
    document.head.appendChild(script);
  }

  loadDemoExperience();

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
          if (visible(nodes[j]) && !nodes[j].closest(".np-help-panel,.np-help-tour-card,.np-help-button")) return nodes[j];
        }
      } catch (error) {
        // Un selector no disponible no debe impedir el tour.
      }
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
    tourCard.innerHTML =
      "<h3>" + escapeHtml(step.title || config.name) + "</h3>" +
      "<p>" + escapeHtml(step.text) + "</p>" +
      "<div class=\"np-help-tour-meta\"><small>Paso " + (tourIndex + 1) + " de " + steps.length + "</small>" +
      "<span><button class=\"secondary np-help-skip\" type=\"button\" data-tour-action=\"skip\">Salir</button> " +
      (tourIndex > 0 ? "<button class=\"secondary\" type=\"button\" data-tour-action=\"back\">Atrás</button> " : "") +
      "<button type=\"button\" data-tour-action=\"next\">" + (tourIndex === steps.length - 1 ? "Terminar" : "Siguiente") + "</button></span></div>";
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
    backdrop.innerHTML =
      "<section class=\"np-help-panel\" role=\"dialog\" aria-modal=\"true\" aria-labelledby=\"np-help-title\">" +
      "<div class=\"np-help-head\"><div><p class=\"np-help-eyebrow\">Ayuda rápida</p><h2 id=\"np-help-title\">" + escapeHtml(config.name) + "</h2></div>" +
      "<button class=\"np-help-close\" type=\"button\" aria-label=\"Cerrar ayuda\" data-help-action=\"close\">×</button></div>" +
      "<div class=\"np-help-body\"><h3>¿Para qué te ayuda?</h3><p>" + escapeHtml(config.purpose) + "</p>" +
      "<h3>Cómo empezar</h3><ol class=\"np-help-steps\">" + (config.quick || []).map(function (step) { return "<li>" + escapeHtml(step) + "</li>"; }).join("") + "</ol>" +
      "<h3>Consejo práctico</h3><p>" + escapeHtml(config.tip) + "</p>" +
      "<div class=\"np-help-actions\"><button class=\"np-help-action\" type=\"button\" data-help-action=\"tour\">Iniciar tour paso a paso</button><a class=\"np-help-link\" href=\"" + escapeHtml(config.guide) + "\">Leer la guía escrita completa</a></div></div></section>";
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
    if (document.querySelector(".np-help-button")) return;
    var button = document.createElement("button");
    button.className = "np-help-button";
    button.type = "button";
    button.setAttribute("aria-label", "Abrir ayuda y tour de " + config.name);
    button.innerHTML = "<span aria-hidden=\"true\">?</span><span>Ayuda y tour</span>";
    button.addEventListener("click", openHelp);
    document.body.appendChild(button);
    try {
      if (!localStorage.getItem(storageKey)) {
        button.classList.add("np-help-first-visit");
        window.setTimeout(function () { button.classList.remove("np-help-first-visit"); }, 4200);
      }
    } catch (error) {}
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
