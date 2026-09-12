#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Ensamblado de Producción: Nube para Pymes
Unifica la exportación estática de WordPress (nubepymesexport/) con las 26
herramientas interactivas en dist/, adaptando rutas canónicas, assets,
redirecciones y sitemap.xml para despliegue serverless (Cloudflare Pages, Netlify, Render).
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
WP_EXPORT = ROOT / "nubepymesexport"
DIST = ROOT / "dist"

# Catálogo completo de las 26 herramientas categorizadas
TOOLS = [
    # Marketing (5)
    {"slug": "analizador-titulares", "cat": "marketing", "src": "analizador-titulares.html", "name": "Analizador de Titulares"},
    {"slug": "auditor-seo-basico", "cat": "marketing", "src": "auditor-seo-basico.html", "name": "Auditor SEO Básico"},
    {"slug": "comparador-campanas-avanzado", "cat": "marketing", "src": "comparador-campanas-avanzado.html", "name": "Comparador de Campañas"},
    {"slug": "consola-campanas", "cat": "marketing", "src": "consola-campanas.html", "name": "Consola de Campañas UTM"},
    {"slug": "organizador-matriz-contenidos", "cat": "marketing", "src": "organizador-matriz-contenidos.html", "name": "Matriz de Contenidos"},

    # Finanzas (5)
    {"slug": "calculadora-descuentos-promociones", "cat": "finanzas", "src": "calculadora-descuentos-promociones.html", "name": "Calculadora de Descuentos"},
    {"slug": "calculadora-precios-venta-igv", "cat": "finanzas", "src": "calculadora-precios-venta-igv.html", "name": "Calculadora de Precios con IGV"},
    {"slug": "calculadora-prestamos-amortizaciones", "cat": "finanzas", "src": "calculadora-prestamos-amortizaciones.html", "name": "Calculadora de Préstamos"},
    {"slug": "calculadora-sobrecostos-laborales", "cat": "finanzas", "src": "calculadora-sobrecostos-laborales.html", "name": "Calculadora de Sobrecostos Laborales"},
    {"slug": "flujo-caja-pymes", "cat": "finanzas", "src": "flujo-caja-pymes.html", "name": "Flujo de Caja y Cobranzas"},

    # Ventas (5)
    {"slug": "creador-facturas-proforma", "cat": "ventas", "src": "creador-facturas-proforma.html", "name": "Creador de Facturas Proforma"},
    {"slug": "generador-codigos-qr", "cat": "ventas", "src": "generador-codigos-qr.html", "name": "Enlaces y QR para WhatsApp"},
    {"slug": "generador-cotizaciones", "cat": "ventas", "src": "generador-cotizaciones.html", "name": "Generador de Cotizaciones"},
    {"slug": "guiones-manejo-objeciones", "cat": "ventas", "src": "guiones-manejo-objeciones.html", "name": "Guiones para Objeciones"},
    {"slug": "crm-pymes", "cat": "ventas", "src": "crm-pymes.html", "name": "CRM y Pipeline Comercial"},

    # Legal (3)
    {"slug": "generador-contratos-servicios", "cat": "legal", "src": "generador-contratos-servicios.html", "name": "Contratos de Servicios"},
    {"slug": "generador-politicas-devolucion", "cat": "legal", "src": "generador-politicas-devolucion.html", "name": "Políticas de Devolución"},
    {"slug": "generador-politicas-terminos", "cat": "legal", "src": "generador-politicas-terminos.html", "name": "Políticas y Términos"},

    # Operaciones (3)
    {"slug": "calculadora-flete-envio-local", "cat": "operaciones", "src": "calculadora-flete-envio-local.html", "name": "Calculadora de Flete Local"},
    {"slug": "simulador-tco-fisico-nube", "cat": "operaciones", "src": "simulador-tco-fisico-nube.html", "name": "Simulador TCO: Físico vs Nube"},
    {"slug": "inventario-compras-pymes", "cat": "operaciones", "src": "inventario-compras-pymes.html", "name": "Inventario, Proveedores y Compras"},

    # Productividad (5)
    {"slug": "conversor-optimizador-imagenes", "cat": "productividad", "src": "conversor-optimizador-imagenes.html", "name": "Optimizador de Imágenes WebP"},
    {"slug": "firma-correo-html", "cat": "productividad", "src": "firma-correo-html.html", "name": "Firma de Correo en HTML"},
    {"slug": "generador-contrasenas-pymes", "cat": "productividad", "src": "generador-contrasenas-pymes.html", "name": "Generador de Contraseñas"},
    {"slug": "generador-paletas-corporativas", "cat": "productividad", "src": "generador-paletas-corporativas.html", "name": "Paletas Corporativas"},
    {"slug": "tareas-proyectos-pymes", "cat": "productividad", "src": "tareas-proyectos-pymes.html", "name": "Tareas y Proyectos Operativos"},
]

def log(msg):
    print(f"[ASSEMBLE] {msg}")

def clean_and_prepare_dist():
    log("Preparando carpeta de salida dist/...")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)

def copy_wp_export():
    log(f"Copiando sitio estático de WordPress desde {WP_EXPORT.name} a dist/...")
    if not WP_EXPORT.exists():
        raise SystemExit(f"ERROR: No se encontró la carpeta {WP_EXPORT}")

    for item in WP_EXPORT.iterdir():
        dest = DIST / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
    log(f"WordPress copiado: {len(list(DIST.iterdir()))} elementos en raíz de dist/.")

def setup_herramientas_assets():
    log("Instalando assets de herramientas en dist/herramientas/...")
    target_herramientas = DIST / "herramientas"
    target_herramientas.mkdir(parents=True, exist_ok=True)

    dest_assets = target_herramientas / "assets"
    if (ROOT / "assets").exists():
        shutil.copytree(ROOT / "assets", dest_assets, dirs_exist_ok=True)
        shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)

    dest_css = target_herramientas / "css"
    if (ROOT / "css").exists():
        shutil.copytree(ROOT / "css", dest_css, dirs_exist_ok=True)

    dest_js = target_herramientas / "js"
    if (ROOT / "js").exists():
        shutil.copytree(ROOT / "js", dest_js, dirs_exist_ok=True)

    datos_compartidos = dest_js / "datos-compartidos.js"
    if datos_compartidos.exists():
        txt = datos_compartidos.read_text(encoding="utf-8")
        txt = txt.replace("./js/demo-experience.js", "/herramientas/js/demo-experience.js")
        datos_compartidos.write_text(txt, encoding="utf-8")

    ayuda_apps = dest_js / "ayuda-apps.js"
    if ayuda_apps.exists():
        txt = ayuda_apps.read_text(encoding="utf-8")
        txt = txt.replace("./js/demo-experience.js", "/herramientas/js/demo-experience.js")
        ayuda_apps.write_text(txt, encoding="utf-8")

    demo_exp = dest_js / "demo-experience.js"
    if demo_exp.exists():
        txt = demo_exp.read_text(encoding="utf-8")
        txt = txt.replace("./css/demo-experience.css", "/herramientas/css/demo-experience.css")
        demo_exp.write_text(txt, encoding="utf-8")

    log("Assets, CSS y JS de herramientas instalados y corregidos.")

def transform_html_asset_links(html_content):
    txt = html_content

    txt = re.sub(r'src=["\']\./js/([^"\']+)["\']', r'src="/herramientas/js/\1"', txt)
    txt = re.sub(r'href=["\']\./css/([^"\']+)["\']', r'href="/herramientas/css/\1"', txt)
    txt = re.sub(r'href=["\']\./assets/([^"\']+)["\']', r'href="/herramientas/assets/\1"', txt)
    txt = re.sub(r'src=["\']\./assets/([^"\']+)["\']', r'src="/herramientas/assets/\1"', txt)

    txt = re.sub(r'(\./)?guia-uso-22-apps\.html', r'/herramientas/guia-uso/', txt)

    for tool in TOOLS:
        old_link = f"./{tool['src']}"
        new_link = f"/herramientas/{tool['cat']}/{tool['slug']}/"
        txt = txt.replace(old_link, new_link)

        old_link_clean = f'href="{tool["src"]}"'
        new_link_clean = f'href="{new_link}"'
        txt = txt.replace(old_link_clean, new_link_clean)

    txt = txt.replace('href="./index.html"', 'href="/herramientas/"')
    txt = txt.replace("href='./index.html'", "href='/herramientas/'")

    txt = txt.replace('https://apps.nubeparapymes.online/', '/herramientas/')
    txt = txt.replace('https://nubeparapymes.online/', '/')

    return txt

def build_tools_portal():
    log("Construyendo el Portal Interactivo en dist/herramientas/index.html...")
    portal_src = ROOT / "index.html"
    if not portal_src.exists():
        log("ADVERTENCIA: No se encontró index.html en la raíz para el portal.")
        return

    content = portal_src.read_text(encoding="utf-8")
    content = transform_html_asset_links(content)

    content = content.replace('href="./"', 'href="/"')
    for tool in TOOLS:
        target_href = f"/herramientas/{tool['cat']}/{tool['slug']}/"
        content = content.replace(f'href="./{tool["src"]}"', f'href="{target_href}"')
        content = content.replace(f'href="{tool["src"]}"', f'href="{target_href}"')

    portal_dest = DIST / "herramientas" / "index.html"
    portal_dest.write_text(content, encoding="utf-8")
    log("Portal de herramientas generado con éxito.")

def build_usage_guide():
    log("Construyendo la Guía de Uso en dist/herramientas/guia-uso/index.html...")
    guide_src = ROOT / "guia-uso-22-apps.html"
    if not guide_src.exists():
        log("ADVERTENCIA: No se encontró guia-uso-22-apps.html.")
        return

    content = guide_src.read_text(encoding="utf-8")
    content = transform_html_asset_links(content)
    content = content.replace('href="./index.html"', 'href="/herramientas/"')

    dest_dir = DIST / "herramientas" / "guia-uso"
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / "index.html").write_text(content, encoding="utf-8")
    log("Guía de uso generada.")

def build_all_tools():
    log("Compilando las 26 herramientas en subdirectorios categorizados...")
    count = 0
    for tool in TOOLS:
        src_path = ROOT / tool["src"]
        if not src_path.exists():
            log(f"ADVERTENCIA: No se encontró {tool['src']}")
            continue

        target_dir = DIST / "herramientas" / tool["cat"] / tool["slug"]
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / "index.html"

        content = src_path.read_text(encoding="utf-8")
        content = transform_html_asset_links(content)

        content = re.sub(
            r'"guide":"(\./)?guia-uso-22-apps\.html',
            r'"guide":"/herramientas/guia-uso/',
            content
        )

        # Inyectar atribución de Xavier Cabello en np-global-footer
        author_badge = '<span class="np-global-author"> · Diseñado y Desarrollado por <a class="np-footer-author-link" href="https://juan.cabellorosas.com" target="_blank" rel="noopener" style="font-weight:700;color:#f97316;text-decoration:underline;">Xavier Cabello</a></span>'
        if "np-global-brand" in content and "juan.cabellorosas.com" not in content:
            content = re.sub(
                r'(<span class="np-global-brand">.*?</span>)',
                r'\1' + author_badge,
                content
            )

        target_file.write_text(content, encoding="utf-8")
        count += 1

    log(f"Se procesaron {count} herramientas en sus directorios canónicos.")

def create_legacy_redirect_stubs():
    log("Creando archivos HTML de redirección para compatibilidad total con enlaces antiguos .html...")
    target_herramientas = DIST / "herramientas"
    target_herramientas.mkdir(parents=True, exist_ok=True)

    count = 0
    for tool in TOOLS:
        canonical_url = f"/herramientas/{tool['cat']}/{tool['slug']}/"
        tool_name = tool.get('name', tool['slug'])
        stub_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={canonical_url}">
  <link rel="canonical" href="https://nubeparapymes.online{canonical_url}">
  <title>Redireccionando a {tool_name} — Nube para Pymes</title>
  <script>window.location.replace("{canonical_url}");</script>
</head>
<body>
  <p>Redireccionando a <a href="{canonical_url}">{tool_name}</a>...</p>
</body>
</html>
"""
        # Guardar en dist/herramientas/{tool['src']}
        (target_herramientas / tool['src']).write_text(stub_html, encoding="utf-8")
        # Guardar en dist/{tool['src']}
        (DIST / tool['src']).write_text(stub_html, encoding="utf-8")
        count += 1

    log(f"Se crearon {count} archivos HTML de redirección en dist/herramientas/ y dist/.")


def update_wp_directory_page():
    log("Actualizando enlaces en dist/directorio-herramientas/index.html...")
    wp_dir_file = DIST / "directorio-herramientas" / "index.html"
    if not wp_dir_file.exists():
        log("ADVERTENCIA: No se encontró dist/directorio-herramientas/index.html")
        return

    content = wp_dir_file.read_text(encoding="utf-8")

    for tool in TOOLS:
        old_url_full = f"https://apps.nubeparapymes.online/{tool['src']}"
        old_url_rel = f"/herramientas/{tool['src']}"
        new_url = f"/herramientas/{tool['cat']}/{tool['slug']}/"
        content = content.replace(old_url_full, new_url)
        content = content.replace(old_url_rel, new_url)

    # Actualizar menciones genéricas del portal
    content = content.replace("https://apps.nubeparapymes.online/", "/herramientas/")
    content = content.replace('target="_blank" rel="noopener"', '')
    content = content.replace(
        'Cada enlace lleva a la herramienta real en <a href="/herramientas/" >apps.nubeparapymes.online</a>',
        'Cada enlace lleva a la herramienta correspondiente en nuestro <a href="/herramientas/">Portal de Herramientas</a>'
    )
    content = content.replace(
        'Cada enlace lleva a la herramienta real en <a href="/herramientas/">apps.nubeparapymes.online</a>',
        'Cada enlace lleva a la herramienta correspondiente en nuestro <a href="/herramientas/">Portal de Herramientas</a>'
    )

    wp_dir_file.write_text(content, encoding="utf-8")
    log("Página de directorio de WordPress sincronizada con las nuevas rutas.")

def update_global_footers():
    log("Estandarizando la firma 'Desarrollado por Xavier Cabello' en todas las páginas de WordPress...")
    author_link = '<a href="https://juan.cabellorosas.com" target="_blank" rel="noopener" style="font-weight:700;color:inherit;text-decoration:underline;">Xavier Cabello</a>'

    patterns = [
        r'<div class="ast-footer-copyright"><p>&copy; 2026 Nube para Pymes\. Todos los derechos reservados(\s*\|\s*(Diseñado y )?Desarrollado por <a [^>]+>[^<]+</a>)?\.</p>',
        r'<div class="ast-footer-copyright"><p>&copy; 2026 Nube para Pymes\. Todos los derechos reservados\s*\|\s*(Diseñado y )?Desarrollado por <a [^>]+>[^<]+</a></p>',
        r'<div class="ast-footer-copyright"><p>&copy; 2026 Nube para Pymes\. Todos los derechos reservados\.</p>'
    ]

    replacement = f'<div class="ast-footer-copyright"><p>&copy; 2026 Nube para Pymes. Todos los derechos reservados | Diseñado y Desarrollado por {author_link}</p>'

    count = 0
    for html_file in DIST.rglob("*.html"):
        if "herramientas" in html_file.parts:
            continue
        try:
            txt = html_file.read_text(encoding="utf-8")
            modified = False
            for pat in patterns:
                if re.search(pat, txt):
                    txt = re.sub(pat, replacement, txt)
                    modified = True
            if "juan.cabellosalirrosas.com" in txt:
                txt = txt.replace("https://juan.cabellosalirrosas.com", "https://juan.cabellorosas.com")
                txt = txt.replace("http://juan.cabellosalirrosas.com", "https://juan.cabellorosas.com")
                modified = True
            if modified:
                html_file.write_text(txt, encoding="utf-8")
                count += 1
        except Exception as e:
            pass
    log(f"Firma de autor inyectada y normalizada en {count} páginas de WordPress.")

def update_redirects():
    log("Generando reglas 301 en dist/_redirects...")
    redirects_file = DIST / "_redirects"
    lines = [
        "# ==========================================",
        "# Reglas de Redirección 301 para Nube para Pymes",
        "# Compatibilidad total con apps antiguas y SEO",
        "# ==========================================",
        "",
        "# Portada y alias de Inicio",
        "/inicio          /    301",
        "/inicio/         /    301",
        "/home            /    301",
        "/home/           /    301",
        "",
        "# Rutas de herramientas y guías",
        "/herramientas-gratis      /herramientas/    301",
        "/herramientas-gratis/*    /herramientas/    301",
        "/herramientas    /herramientas/    301",
        "/guia-uso-22-apps.html    /herramientas/guia-uso/    301",
        "/guia-uso        /herramientas/guia-uso/    301",
        "",
        "# Redirecciones para las 26 herramientas (desde raíz .html a categoría canónica)",
    ]

    for tool in TOOLS:
        target_path = f"/herramientas/{tool['cat']}/{tool['slug']}/"
        # Redirecciones desde la raíz
        lines.append(f"/{tool['src']}    {target_path}    301")
        lines.append(f"/{tool['slug']}    {target_path}    301")
        lines.append(f"/{tool['slug']}.html    {target_path}    301")
        # Redirecciones desde /herramientas/
        lines.append(f"/herramientas/{tool['src']}    {target_path}    301")
        lines.append(f"/herramientas/{tool['slug']}    {target_path}    301")
        lines.append(f"/herramientas/{tool['slug']}.html    {target_path}    301")


    lines.extend([
        "",
        "# Reglas de seguridad y fallback de WordPress",
        "/wp-login.php    /    301",
        "/wp-admin/*      /    301",
        "/xmlrpc.php      /    404",
        "",
        "# Fallback 404 personalizado",
        "/*    /404.html    404",
        ""
    ])

    redirects_file.write_text("\n".join(lines), encoding="utf-8")
    log("dist/_redirects creado con reglas completas.")

def update_headers():
    log("Configurando reglas de caché y seguridad en dist/_headers...")
    headers_file = DIST / "_headers"
    lines = [
        "# ==========================================",
        "# Cloudflare Pages _headers: Cache & Security",
        "# ==========================================",
        "",
        "# HTML de herramientas y portada siempre revalidados para reflejar cambios de inmediato",
        "/*.html",
        "  Cache-Control: public, max-age=0, must-revalidate",
        "",
        "/herramientas/",
        "  Cache-Control: public, max-age=0, must-revalidate",
        "",
        "/herramientas/*",
        "  Cache-Control: public, max-age=0, must-revalidate",
        "",
        "# Assets estáticos",
        "/herramientas/assets/*",
        "  Cache-Control: public, max-age=3600, must-revalidate",
        "",
        "/assets/*",
        "  Cache-Control: public, max-age=3600, must-revalidate",
        "",
        "/wp-content/uploads/*",
        "  Cache-Control: public, max-age=31536000, immutable",
        "",
        "/*",
        "  X-Frame-Options: SAMEORIGIN",
        "  X-Content-Type-Options: nosniff",
        "  X-XSS-Protection: 1; mode=block",
        "  Referrer-Policy: strict-origin-when-cross-origin",
        ""
    ]
    headers_file.write_text("\n".join(lines), encoding="utf-8")
    log("dist/_headers configurado con éxito.")

def update_sitemap():
    log("Inyectando rutas de herramientas en dist/sitemap.xml y normalizando dominios...")
    sitemap_file = DIST / "sitemap.xml"
    if not sitemap_file.exists():
        log("ADVERTENCIA: No se encontró dist/sitemap.xml")
        return

    content = sitemap_file.read_text(encoding="utf-8")
    content = content.replace("https://dev-nube-para-pymes.pantheonsite.io", "https://nubeparapymes.online")
    content = content.replace("http://dev-nube-para-pymes.pantheonsite.io", "https://nubeparapymes.online")

    now = datetime.now().strftime("%Y-%m-%d")

    xml_entries = [
        f"  <url>\n    <loc>https://nubeparapymes.online/herramientas/</loc>\n    <lastmod>{now}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.9</priority>\n  </url>",
        f"  <url>\n    <loc>https://nubeparapymes.online/herramientas/guia-uso/</loc>\n    <lastmod>{now}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>",
    ]

    for tool in TOOLS:
        url = f"https://nubeparapymes.online/herramientas/{tool['cat']}/{tool['slug']}/"
        xml_entries.append(
            f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{now}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        )

    block = "\n" + "\n".join(xml_entries) + "\n</urlset>"
    if "</urlset>" in content:
        content = content.replace("</urlset>", block)
        sitemap_file.write_text(content, encoding="utf-8")
        log("Sitemap XML enriquecido con 28 nuevas URLs canónicas de herramientas.")

def update_robots_and_llms():
    log("Normalizando dist/robots.txt y dist/llms.txt con el dominio de producción...")
    # robots.txt
    robots_file = DIST / "robots.txt"
    if robots_file.exists():
        r_txt = robots_file.read_text(encoding="utf-8")
        r_txt = r_txt.replace("https://dev-nube-para-pymes.pantheonsite.io", "https://nubeparapymes.online")
        robots_file.write_text(r_txt, encoding="utf-8")

    # llms.txt
    llms_file = DIST / "llms.txt"
    if llms_file.exists():
        l_txt = llms_file.read_text(encoding="utf-8")
        l_txt = l_txt.replace("https://dev-nube-para-pymes.pantheonsite.io", "https://nubeparapymes.online")
        l_txt = l_txt.replace("https://apps.nubeparapymes.online/", "https://nubeparapymes.online/herramientas/")
        l_txt = l_txt.replace("apps.nubeparapymes.online", "nubeparapymes.online/herramientas")

        tools_md_block = ["", "## Herramientas Gratuitas para Pymes (Ejecución Local)", ""]
        for tool in TOOLS:
            url = f"https://nubeparapymes.online/herramientas/{tool['cat']}/{tool['slug']}/"
            tools_md_block.append(f"- [{tool['name']}]({url}): Herramienta de {tool['cat']} para pequeñas empresas.")

        l_txt += "\n" + "\n".join(tools_md_block) + "\n"
        llms_file.write_text(l_txt, encoding="utf-8")
        log("robots.txt y llms.txt actualizados con éxito.")

def update_search_index():
    log("Añadiendo las 26 herramientas a dist/search-index.json...")
    import json
    search_file = DIST / "search-index.json"
    if not search_file.exists():
        return

    try:
        data = json.loads(search_file.read_text(encoding="utf-8"))
        # Eliminar posibles duplicados previos de herramientas
        data = [item for item in data if not item.get("url", "").startswith("/herramientas/")]

        # Añadir portal general
        data.append({
            "title": "Portal de Herramientas Gratuitas para Pymes",
            "url": "/herramientas/",
            "excerpt": "Panel de control con 26 herramientas gratuitas de marketing, finanzas, ventas, legal, operaciones y productividad.",
            "content": "Portal de 26 herramientas gratuitas para pymes. Buscador en tiempo real, filtros por categoría, ejecución local en el navegador.",
            "type": "page"
        })

        for tool in TOOLS:
            url = f"/herramientas/{tool['cat']}/{tool['slug']}/"
            data.append({
                "title": tool["name"],
                "url": url,
                "excerpt": f"Herramienta gratuita de {tool['cat']} para pequeñas empresas. Ejecución en navegador sin registro.",
                "content": f"{tool['name']} - Categoría {tool['cat']}. Software local y gratuito para pymes.",
                "type": "tool"
            })

        search_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        log(f"Índice de búsqueda enriquecido ({len(data)} elementos indexados).")
    except Exception as e:
        log(f"ADVERTENCIA al procesar search-index.json: {e}")

def create_package_json():
    log("Verificando / creando package.json para despliegue automatizado...")
    pkg_file = ROOT / "package.json"
    pkg_content = """{
  "name": "nube-para-pymes",
  "version": "2.0.0",
  "description": "Sitio estático unificado y serverless para Nube para Pymes: WordPress + 26 Herramientas",
  "private": true,
  "scripts": {
    "build": "python scripts/assemble_production_site.py",
    "serve": "npx -y serve dist -l 3000",
    "test": "node scripts/verify_production_build.js"
  }
}
"""
    pkg_file.write_text(pkg_content, encoding="utf-8")
    log("package.json configurado.")

def main():
    start_time = datetime.now()
    log("=== INICIO DE ENSAMBLADO DE PRODUCCIÓN ===")
    clean_and_prepare_dist()
    copy_wp_export()
    setup_herramientas_assets()
    build_tools_portal()
    build_usage_guide()
    build_all_tools()
    create_legacy_redirect_stubs()
    update_wp_directory_page()

    update_global_footers()
    update_redirects()
    update_headers()
    update_sitemap()
    update_robots_and_llms()
    update_search_index()
    create_package_json()
    elapsed = (datetime.now() - start_time).total_seconds()
    log(f"=== ENSAMBLADO COMPLETADO EXITOSAMENTE en {elapsed:.2f}s ===")

if __name__ == "__main__":
    main()
