#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación para enlaces de herramientas y footer en dist/
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

TOOLS = [
    {"slug": "analizador-titulares", "cat": "marketing", "src": "analizador-titulares.html"},
    {"slug": "auditor-seo-basico", "cat": "marketing", "src": "auditor-seo-basico.html"},
    {"slug": "comparador-campanas-avanzado", "cat": "marketing", "src": "comparador-campanas-avanzado.html"},
    {"slug": "consola-campanas", "cat": "marketing", "src": "consola-campanas.html"},
    {"slug": "organizador-matriz-contenidos", "cat": "marketing", "src": "organizador-matriz-contenidos.html"},

    {"slug": "calculadora-descuentos-promociones", "cat": "finanzas", "src": "calculadora-descuentos-promociones.html"},
    {"slug": "calculadora-precios-venta-igv", "cat": "finanzas", "src": "calculadora-precios-venta-igv.html"},
    {"slug": "calculadora-prestamos-amortizaciones", "cat": "finanzas", "src": "calculadora-prestamos-amortizaciones.html"},
    {"slug": "calculadora-sobrecostos-laborales", "cat": "finanzas", "src": "calculadora-sobrecostos-laborales.html"},
    {"slug": "flujo-caja-pymes", "cat": "finanzas", "src": "flujo-caja-pymes.html"},

    {"slug": "creador-facturas-proforma", "cat": "ventas", "src": "creador-facturas-proforma.html"},
    {"slug": "generador-codigos-qr", "cat": "ventas", "src": "generador-codigos-qr.html"},
    {"slug": "generador-cotizaciones", "cat": "ventas", "src": "generador-cotizaciones.html"},
    {"slug": "guiones-manejo-objeciones", "cat": "ventas", "src": "guiones-manejo-objeciones.html"},
    {"slug": "crm-pymes", "cat": "ventas", "src": "crm-pymes.html"},

    {"slug": "generador-contratos-servicios", "cat": "legal", "src": "generador-contratos-servicios.html"},
    {"slug": "generador-politicas-devolucion", "cat": "legal", "src": "generador-politicas-devolucion.html"},
    {"slug": "generador-politicas-terminos", "cat": "legal", "src": "generador-politicas-terminos.html"},

    {"slug": "calculadora-flete-envio-local", "cat": "operaciones", "src": "calculadora-flete-envio-local.html"},
    {"slug": "simulador-tco-fisico-nube", "cat": "operaciones", "src": "simulador-tco-fisico-nube.html"},
    {"slug": "inventario-compras-pymes", "cat": "operaciones", "src": "inventario-compras-pymes.html"},

    {"slug": "conversor-optimizador-imagenes", "cat": "productividad", "src": "conversor-optimizador-imagenes.html"},
    {"slug": "firma-correo-html", "cat": "productividad", "src": "firma-correo-html.html"},
    {"slug": "generador-contrasenas-pymes", "cat": "productividad", "src": "generador-contrasenas-pymes.html"},
    {"slug": "generador-paletas-corporativas", "cat": "productividad", "src": "generador-paletas-corporativas.html"},
    {"slug": "tareas-proyectos-pymes", "cat": "productividad", "src": "tareas-proyectos-pymes.html"},
]

def check():
    errors = []
    
    # 1. Verificar index.html del portal
    portal_html = DIST / "herramientas" / "index.html"
    if not portal_html.exists():
        errors.append("Falta dist/herramientas/index.html")
    else:
        txt = portal_html.read_text(encoding="utf-8")
        for tool in TOOLS:
            expected = f'/herramientas/{tool["cat"]}/{tool["slug"]}/'
            if expected not in txt:
                errors.append(f"dist/herramientas/index.html no contiene enlace canónico {expected}")
        if "juan.cabellorosas.com" not in txt:
            errors.append("dist/herramientas/index.html no contiene juan.cabellorosas.com")
        if "Guía de uso" not in txt:
            errors.append("dist/herramientas/index.html no contiene 'Guía de uso' en footer")

    # 2. Verificar js/index.js (React bundle)
    bundle_js = DIST / "herramientas" / "js" / "index.js"
    if not bundle_js.exists():
        errors.append("Falta dist/herramientas/js/index.js")
    else:
        txt = bundle_js.read_text(encoding="utf-8")
        for tool in TOOLS:
            expected = f'slug:"/herramientas/{tool["cat"]}/{tool["slug"]}/"'
            if expected not in txt:
                errors.append(f"dist/herramientas/js/index.js no contiene slug {expected}")
        if "juan.cabellorosas.com" not in txt:
            errors.append("dist/herramientas/js/index.js no contiene juan.cabellorosas.com")

    # 3. Verificar directory-experience.js
    dx_js = DIST / "herramientas" / "js" / "directory-experience.js"
    if dx_js.exists():
        txt = dx_js.read_text(encoding="utf-8")
        if "./inventario-compras-pymes.html" in txt or "./crm-pymes.html" in txt:
            errors.append("dist/herramientas/js/directory-experience.js aún contiene enlaces antiguos .html")

    # 4. Verificar _redirects
    redirects_file = DIST / "_redirects"
    if not redirects_file.exists():
        errors.append("Falta dist/_redirects")
    else:
        txt = redirects_file.read_text(encoding="utf-8")
        for tool in TOOLS:
            req_rule = f"/herramientas/{tool['src']}    /herramientas/{tool['cat']}/{tool['slug']}/    301"
            if req_rule not in txt:
                errors.append(f"Falta regla de redirección: {req_rule}")

    if errors:
        print(f"FAILED con {len(errors)} errores:")
        for err in errors[:10]:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("SUCCESS: Todos los enlaces de herramientas, bundle de React, redirecciones y footer verificados al 100%.")

if __name__ == "__main__":
    check()
