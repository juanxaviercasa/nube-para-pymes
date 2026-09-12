/* Nube para Pymes — directorio: orientación por resultados reales, compatible con los filtros y el bundle existente. */
(function () {
  "use strict";

  var tools = [
    { title: "Define tu precio final", text: "Calcula margen, IGV y precio de venta.", href: "./calculadora-precios-venta-igv.html", tag: "Precios" },
    { title: "Prepara una cotización", text: "Convierte un servicio en una propuesta clara.", href: "./generador-cotizaciones.html", tag: "Ventas" },
    { title: "Ordena tus oportunidades", text: "Visualiza contactos, etapas y próximos pasos.", href: "./crm-pymes.html", tag: "CRM" },
    { title: "Controla tu caja", text: "Registra entradas, salidas y cobros pendientes.", href: "./flujo-caja-pymes.html", tag: "Finanzas" },
    { title: "Revisa tu inventario", text: "Ve stock, reposición y costo de productos.", href: "./inventario-compras-pymes.html", tag: "Operación" },
    { title: "Comparte tu WhatsApp", text: "Genera un código QR para iniciar conversaciones.", href: "./generador-codigos-qr.html", tag: "Visibilidad" }
  ];

  function addStyles() {
    if (document.getElementById("np-directory-experience-style")) return;
    var style = document.createElement("style");
    style.id = "np-directory-experience-style";
    style.textContent = ".np-start-results{margin:1.5rem auto 2rem;max-width:72rem;padding:1.25rem;border:1px solid #cbdcf1;border-top:4px solid #f97316;border-radius:1.1rem;background:linear-gradient(115deg,#f8fbff 0%,#fff 64%);box-shadow:0 14px 32px rgba(10,25,47,.07)}.np-start-results__head{display:flex;justify-content:space-between;gap:1rem;align-items:end;margin-bottom:1rem}.np-start-results__eyebrow{margin:0 0 .3rem;color:#9a3412;font-size:.74rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase}.np-start-results h2{margin:0;color:#0a192f;font-size:clamp(1.25rem,2.3vw,1.7rem);line-height:1.18}.np-start-results__note{max-width:23rem;margin:0;color:#475569;font-size:.9rem;line-height:1.45}.np-start-results__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.75rem}.np-start-results__card{display:block;min-height:8.7rem;padding:1rem;border:1px solid #d7e4f5;border-radius:.85rem;background:#fff;color:#0a192f;text-decoration:none;transition:transform .16s cubic-bezier(.23,1,.32,1),box-shadow .16s cubic-bezier(.23,1,.32,1),border-color .16s}.np-start-results__card:hover{transform:translateY(-2px);border-color:#f97316;box-shadow:0 10px 20px rgba(10,25,47,.12)}.np-start-results__card:focus-visible{outline:3px solid #2563eb;outline-offset:3px}.np-start-results__tag{display:inline-block;margin-bottom:.6rem;padding:.2rem .45rem;border-radius:999px;background:#eaf3ff;color:#0f4c81;font-size:.69rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase}.np-start-results__card strong{display:block;margin-bottom:.35rem;font-size:1rem}.np-start-results__card span:last-child{color:#475569;font-size:.86rem;line-height:1.4}@media(max-width:760px){.np-start-results{margin:1rem;padding:1rem}.np-start-results__head{align-items:start;flex-direction:column}.np-start-results__grid{grid-template-columns:1fr 1fr}}@media(max-width:480px){.np-start-results__grid{grid-template-columns:1fr}}@media(prefers-reduced-motion:reduce){.np-start-results__card{transition:none}.np-start-results__card:hover{transform:none}}";
    document.head.appendChild(style);
  }

  function render() {
    if (document.querySelector(".np-start-results")) return true;
    var main = document.querySelector("main");
    if (!main) return false;
    var section = document.createElement("section");
    section.className = "np-start-results";
    section.setAttribute("aria-labelledby", "np-start-results-title");
    section.innerHTML = "<div class=\"np-start-results__head\"><div><p class=\"np-start-results__eyebrow\">Empieza por un resultado</p><h2 id=\"np-start-results-title\">Una necesidad concreta, una herramienta lista para usar.</h2></div><p class=\"np-start-results__note\">Cada acceso abre una herramienta gratuita y local. Puedes cargar un ejemplo antes de ingresar información propia.</p></div><div class=\"np-start-results__grid\">" + tools.map(function (tool) { return "<a class=\"np-start-results__card\" href=\"" + tool.href + "\"><span class=\"np-start-results__tag\">" + tool.tag + "</span><strong>" + tool.title + "</strong><span>" + tool.text + "</span></a>"; }).join("") + "</div>";
    main.insertBefore(section, main.firstChild);
    return true;
  }

  function init() {
    addStyles();
    render();
    [120, 450, 1100, 1900].forEach(function (delay) { window.setTimeout(render, delay); });
    var root = document.getElementById("root") || document.body;
    var observer = new MutationObserver(function () { if (!document.querySelector(".np-start-results")) render(); });
    observer.observe(root, { childList: true, subtree: true });
    window.setTimeout(function () { observer.disconnect(); }, 2600);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, { once: true }); else init();
})();
