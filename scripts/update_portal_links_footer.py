#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de actualización de enlaces canónicos y footer en el Portal de Herramientas.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Catálogo oficial de las 26 herramientas
TOOLS = [
    # Marketing (5)
    {"slug": "analizador-titulares", "cat": "marketing", "src": "analizador-titulares.html"},
    {"slug": "auditor-seo-basico", "cat": "marketing", "src": "auditor-seo-basico.html"},
    {"slug": "comparador-campanas-avanzado", "cat": "marketing", "src": "comparador-campanas-avanzado.html"},
    {"slug": "consola-campanas", "cat": "marketing", "src": "consola-campanas.html"},
    {"slug": "organizador-matriz-contenidos", "cat": "marketing", "src": "organizador-matriz-contenidos.html"},

    # Finanzas (5)
    {"slug": "calculadora-descuentos-promociones", "cat": "finanzas", "src": "calculadora-descuentos-promociones.html"},
    {"slug": "calculadora-precios-venta-igv", "cat": "finanzas", "src": "calculadora-precios-venta-igv.html"},
    {"slug": "calculadora-prestamos-amortizaciones", "cat": "finanzas", "src": "calculadora-prestamos-amortizaciones.html"},
    {"slug": "calculadora-sobrecostos-laborales", "cat": "finanzas", "src": "calculadora-sobrecostos-laborales.html"},
    {"slug": "flujo-caja-pymes", "cat": "finanzas", "src": "flujo-caja-pymes.html"},

    # Ventas (5)
    {"slug": "creador-facturas-proforma", "cat": "ventas", "src": "creador-facturas-proforma.html"},
    {"slug": "generador-codigos-qr", "cat": "ventas", "src": "generador-codigos-qr.html"},
    {"slug": "generador-cotizaciones", "cat": "ventas", "src": "generador-cotizaciones.html"},
    {"slug": "guiones-manejo-objeciones", "cat": "ventas", "src": "guiones-manejo-objeciones.html"},
    {"slug": "crm-pymes", "cat": "ventas", "src": "crm-pymes.html"},

    # Legal (3)
    {"slug": "generador-contratos-servicios", "cat": "legal", "src": "generador-contratos-servicios.html"},
    {"slug": "generador-politicas-devolucion", "cat": "legal", "src": "generador-politicas-devolucion.html"},
    {"slug": "generador-politicas-terminos", "cat": "legal", "src": "generador-politicas-terminos.html"},

    # Operaciones (3)
    {"slug": "calculadora-flete-envio-local", "cat": "operaciones", "src": "calculadora-flete-envio-local.html"},
    {"slug": "simulador-tco-fisico-nube", "cat": "operaciones", "src": "simulador-tco-fisico-nube.html"},
    {"slug": "inventario-compras-pymes", "cat": "operaciones", "src": "inventario-compras-pymes.html"},

    # Productividad (5)
    {"slug": "conversor-optimizador-imagenes", "cat": "productividad", "src": "conversor-optimizador-imagenes.html"},
    {"slug": "firma-correo-html", "cat": "productividad", "src": "firma-correo-html.html"},
    {"slug": "generador-contrasenas-pymes", "cat": "productividad", "src": "generador-contrasenas-pymes.html"},
    {"slug": "generador-paletas-corporativas", "cat": "productividad", "src": "generador-paletas-corporativas.html"},
    {"slug": "tareas-proyectos-pymes", "cat": "productividad", "src": "tareas-proyectos-pymes.html"},
]

def update_bundle_js():
    js_file = ROOT / "js" / "index.js"
    content = js_file.read_text(encoding="utf-8")
    
    # 1. Actualizar los slugs de las herramientas
    for tool in TOOLS:
        old_slug_pattern = f'slug:"./{tool["src"]}"'
        new_slug = f'slug:"/herramientas/{tool["cat"]}/{tool["slug"]}/"'
        if old_slug_pattern in content:
            content = content.replace(old_slug_pattern, new_slug)
        else:
            print(f"[WARN] No se encontró {old_slug_pattern} en js/index.js")

    # 2. Hacer compatible la búsqueda de favoritos con slugs antiguos o nuevos
    content = content.replace(
        'n.map(e=>_m.find(t=>t.slug===e)).filter(e=>!!e)',
        'n.map(e=>_m.find(t=>t.slug===e||t.slug.includes(e)||e.includes(t.slug))).filter(e=>!!e)'
    )

    # 3. Actualizar el footer en React
    # Localizar el footer de React
    footer_pattern = r'\(0,K\.jsx\)\("footer",\{className:"border-t border-line bg-surface"[^\}]*children:\(0,K\.jsxs\)\("div",\{className:"mx-auto flex max-w-7xl flex-col items-center justify-between gap-3 px-5 py-8 sm:flex-row sm:px-8".*?\}\)\}\)'
    
    new_react_footer = (
        '(0,K.jsx)("footer",{className:"border-t border-line bg-surface","data-visual-edit-loc":"src/pages/Index.tsx:410:6","data-visual-edit-component":"footer","data-visual-edit-editable":"false",children:(0,K.jsxs)("div",{className:"mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-5 py-8 md:flex-row sm:px-8",children:['
        '(0,K.jsxs)("div",{className:"flex flex-col items-center gap-3 sm:flex-row text-center sm:text-left",children:['
        '(0,K.jsxs)("a",{href:"/",className:"flex items-center transition-opacity hover:opacity-90","aria-label":"NubeParaPymes - Inicio",children:['
        '(0,K.jsx)("img",{src:"/herramientas/assets/logo-nube-para-pymes-light.webp?v=20260912",alt:"NubeParaPymes",className:"h-8 w-auto object-contain block dark:hidden"}),'
        '(0,K.jsx)("img",{src:"/herramientas/assets/logo-nube-para-pymes-dark.webp?v=20260912",alt:"NubeParaPymes",className:"h-8 w-auto object-contain hidden dark:block"})'
        ']}),'
        '(0,K.jsx)("span",{className:"hidden md:inline text-line",children:"|"}),'
        '(0,K.jsx)("span",{className:"text-xs sm:text-sm text-fg-muted",children:"Herramientas gratuitas para tu negocio"})'
        ']}),'
        '(0,K.jsxs)("div",{className:"flex flex-wrap items-center justify-center gap-5 text-sm font-medium",children:['
        '(0,K.jsx)("a",{href:"/herramientas/guia-uso/",className:"text-fg-muted transition-colors hover:text-cta",children:"Gu\\xEDa de uso"}),'
        '(0,K.jsx)("a",{href:"/",className:"text-fg-muted transition-colors hover:text-cta",children:"Inicio"}),'
        '(0,K.jsx)("a",{href:"/sobre-nosotros/",className:"text-fg-muted transition-colors hover:text-cta",children:"Sobre Nosotros"}),'
        '(0,K.jsx)("a",{href:"/blog/",className:"text-fg-muted transition-colors hover:text-cta",children:"Blog"})'
        ']}),'
        '(0,K.jsxs)("div",{className:"flex flex-col items-center md:items-end text-center md:text-right gap-1 pr-0 md:pr-14",children:['
        '(0,K.jsxs)("p",{className:"text-xs sm:text-sm text-fg-muted",children:["\\xA9 ",(new Date).getFullYear()," NubeParaPymes \\xB7 Todos los derechos reservados"]}),'
        '(0,K.jsxs)("p",{className:"text-xs sm:text-sm text-fg-muted",children:["Dise\\xF1ado y Desarrollado por ",(0,K.jsx)("a",{href:"https://juan.cabellorosas.com",target:"_blank",rel:"noopener",className:"font-bold text-cta hover:underline",children:"Xavier Cabello"})]})'
        ']})'
        ']})})'
    )

    match = re.search(footer_pattern, content)
    if match:
        content = content[:match.start()] + new_react_footer + content[match.end():]
        print("[OK] Footer de React reemplazado con éxito.")
    else:
        print("[ERROR] No se pudo encontrar el patrón del footer en js/index.js")

    js_file.write_text(content, encoding="utf-8")
    print("[OK] js/index.js actualizado.")

def update_directory_experience_js():
    dx_file = ROOT / "js" / "directory-experience.js"
    txt = dx_file.read_text(encoding="utf-8")
    for tool in TOOLS:
        old_href = f'href: "./{tool["src"]}"'
        new_href = f'href: "/herramientas/{tool["cat"]}/{tool["slug"]}/"'
        txt = txt.replace(old_href, new_href)
    dx_file.write_text(txt, encoding="utf-8")
    print("[OK] js/directory-experience.js actualizado.")

def update_index_html():
    idx_file = ROOT / "index.html"
    content = idx_file.read_text(encoding="utf-8")

    # Reemplazar todos los enlaces a las herramientas por sus rutas canónicas
    for tool in TOOLS:
        target_href = f"/herramientas/{tool['cat']}/{tool['slug']}/"
        content = content.replace(f'href="./{tool["src"]}"', f'href="{target_href}"')
        content = content.replace(f'href="{tool["src"]}"', f'href="{target_href}"')

    # Reemplazar el footer estático
    old_footer_pattern = r'<!-- Footer -->\s*<footer class="border-t border-line bg-surface">.*?</footer>'
    new_html_footer = '''<!-- Footer -->
      <footer class="border-t border-line bg-surface">
        <div class="mx-auto max-w-7xl px-5 py-8 sm:px-8">
          <div class="flex flex-col items-center justify-between gap-4 md:flex-row">
            <div class="flex flex-col sm:flex-row items-center gap-3 text-center sm:text-left">
              <a href="/" class="flex items-center transition-opacity hover:opacity-90" aria-label="NubeParaPymes - Inicio">
                <img src="./assets/logo-nube-para-pymes-light.webp?v=20260912" alt="NubeParaPymes" class="h-8 w-auto object-contain block dark:hidden">
                <img src="./assets/logo-nube-para-pymes-dark.webp?v=20260912" alt="NubeParaPymes" class="h-8 w-auto object-contain hidden dark:block">
              </a>
              <span class="hidden md:inline text-line">|</span>
              <span class="text-xs sm:text-sm text-fg-muted">Herramientas gratuitas para tu negocio</span>
            </div>
            
            <div class="flex flex-wrap items-center justify-center gap-5 text-sm font-medium">
              <a href="./guia-uso-22-apps.html" class="text-fg-muted hover:text-cta transition-colors">Guía de uso</a>
              <a href="/" class="text-fg-muted hover:text-cta transition-colors">Inicio</a>
              <a href="/sobre-nosotros/" class="text-fg-muted hover:text-cta transition-colors">Sobre Nosotros</a>
              <a href="/blog/" class="text-fg-muted hover:text-cta transition-colors">Blog</a>
            </div>

            <div class="flex flex-col items-center md:items-end text-center md:text-right gap-1 pr-0 md:pr-14">
              <p class="text-xs sm:text-sm text-fg-muted">© 2026 NubeParaPymes · Todos los derechos reservados</p>
              <p class="text-xs sm:text-sm text-fg-muted">Diseñado y Desarrollado por <a href="https://juan.cabellorosas.com" target="_blank" rel="noopener" class="font-bold text-cta hover:underline">Xavier Cabello</a></p>
            </div>
          </div>
        </div>
      </footer>'''

    match = re.search(old_footer_pattern, content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_html_footer + content[match.end():]
        print("[OK] Footer de index.html actualizado.")
    else:
        print("[WARN] No se encontró el bloque del footer en index.html")

    # Bump version para forzar invalidación de caché
    content = content.replace('./js/index.js?v=20260912', './js/index.js?v=20260912-3')

    idx_file.write_text(content, encoding="utf-8")
    print("[OK] index.html actualizado.")

if __name__ == "__main__":
    update_bundle_js()
    update_directory_experience_js()
    update_index_html()
