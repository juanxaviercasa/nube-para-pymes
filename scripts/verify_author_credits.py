#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

def check(condition, msg):
    if condition:
        print(f"  [OK] {msg}")
    else:
        print(f"  [ERROR] {msg}")
        raise AssertionError(msg)

print("=== VERIFICACIÓN DE PERFIL Y ATRIBUCIÓN GLOBAL DE AUTOR ===")

# 1. Portada (dist/index.html)
home_txt = (DIST / "index.html").read_text(encoding="utf-8")
check('href="https://juan.cabellorosas.com"' in home_txt, "Portada contiene enlace a juan.cabellorosas.com en bio")
check("Profesor de Matemáticas" in home_txt, "Portada contiene rol de Profesor de Matemáticas")
check("Desarrollador Web" in home_txt, "Portada contiene rol de Desarrollador Web")
check("Especialista en IA" in home_txt or "Inteligencia Artificial" in home_txt, "Portada contiene especialidad en IA")
check('Diseñado y Desarrollado por <a href="https://juan.cabellorosas.com"' in home_txt, "Footer de portada contiene firma de Xavier Cabello")

# 2. Portal de Herramientas (dist/herramientas/index.html)
tools_txt = (DIST / "herramientas/index.html").read_text(encoding="utf-8")
check('Diseñado y Desarrollado por <a href="https://juan.cabellorosas.com"' in tools_txt, "Portal de herramientas HTML contiene firma de autor")

# 3. Bundle React (dist/herramientas/js/index.js)
js_txt = (DIST / "herramientas/js/index.js").read_text(encoding="utf-8")
check('https://juan.cabellorosas.com' in js_txt, "Bundle React contiene enlace de autor")
check('Xavier Cabello' in js_txt, "Bundle React contiene nombre Xavier Cabello")

# 4. Páginas de WordPress (/sobre-nosotros/, /blog/, /contacto/)
for page in ["sobre-nosotros", "blog", "contacto"]:
    p_txt = (DIST / page / "index.html").read_text(encoding="utf-8")
    check('href="https://juan.cabellorosas.com"' in p_txt, f"Página /{page}/ contiene enlace a juan.cabellorosas.com")
    check('Xavier Cabello' in p_txt, f"Página /{page}/ contiene nombre Xavier Cabello en footer")

# 5. Muestra de las 26 herramientas
tool_samples = [
    "finanzas/calculadora-descuentos-promociones",
    "ventas/crm-pymes",
    "operaciones/inventario-compras-pymes",
    "marketing/analizador-titulares",
    "productividad/firma-correo-html"
]

for t in tool_samples:
    t_file = DIST / "herramientas" / t / "index.html"
    check(t_file.exists(), f"Herramienta {t} existe")
    t_txt = t_file.read_text(encoding="utf-8")
    check('href="https://juan.cabellorosas.com"' in t_txt, f"Herramienta {t} tiene enlace de autor en footer")
    check('Xavier Cabello' in t_txt, f"Herramienta {t} tiene nombre Xavier Cabello en footer")

print("\n=== TODAS LAS COMPROBACIONES DE ATRIBUCIÓN PASARON EXITOSAMENTE (100%) ===")
