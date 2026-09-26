import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

tools = [
    "analizador-titulares.html",
    "auditor-seo-basico.html",
    "calculadora-descuentos-promociones.html",
    "calculadora-flete-envio-local.html",
    "calculadora-precios-venta-igv.html",
    "calculadora-prestamos-amortizaciones.html",
    "calculadora-sobrecostos-laborales.html",
    "comparador-campanas-avanzado.html",
    "consola-campanas.html",
    "conversor-optimizador-imagenes.html",
    "creador-facturas-proforma.html",
    "crm-pymes.html",
    "firma-correo-html.html",
    "flujo-caja-pymes.html",
    "generador-codigos-qr.html",
    "generador-contrasenas-pymes.html",
    "generador-contratos-servicios.html",
    "generador-cotizaciones.html",
    "generador-paletas-corporativas.html",
    "generador-politicas-devolucion.html",
    "generador-politicas-terminos.html",
    "guiones-manejo-objeciones.html",
    "inventario-compras-pymes.html",
    "organizador-matriz-contenidos.html",
    "simulador-tco-fisico-nube.html",
    "tareas-proyectos-pymes.html"
]

print(f"Total tools to inspect: {len(tools)}")
for t in tools:
    p = ROOT / t
    if not p.exists():
        print(f"MISSING: {t}")
        continue
    content = p.read_text(encoding="utf-8", errors="ignore")
    has_help = "NP_HELP_CONFIG" in content
    has_footer = "np-global-footer" in content
    scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', content)
    styles = re.findall(r'<link[^>]*href=["\']([^"\']+\.css[^"\']*)["\']', content)
    print(f"{t}: help={has_help}, footer={has_footer}, scripts={len(scripts)}, styles={len(styles)}")
