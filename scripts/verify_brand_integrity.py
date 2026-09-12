#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

def check(condition, msg):
    if condition:
        print(f"  [OK] {msg}")
    else:
        print(f"  [ERROR] {msg}")
        raise AssertionError(msg)

print("=== VERIFICACIÓN INTEGRAL DE LA MARCA UNIFICADA ===")

# 1. Portada WordPress (dist/index.html)
home_html = (DIST / "index.html").read_text(encoding="utf-8")
check("logo-nubeparapymes-header-200x67.webp" in home_html, "Portada contiene referencia al logo 200x67")
wp_logo = DIST / "wp-content/uploads/2026/07/logo-nubeparapymes-header-200x67.webp"
check(wp_logo.exists(), "Archivo de logo WordPress 200x67 existe")
img_wp = Image.open(wp_logo)
check(img_wp.mode == "RGBA", "Logo WP tiene canal alfa RGBA transparente")
print(f"       -> Dimensiones WP: {img_wp.size}")

# 2. Portal de Herramientas (dist/herramientas/index.html)
tools_html = (DIST / "herramientas/index.html").read_text(encoding="utf-8")
check("/herramientas/assets/logo-nube-para-pymes-dark.webp" in tools_html, "Portal de herramientas tiene logo dark en cabecera")
check("/herramientas/assets/logo-nube-para-pymes-light.webp" in tools_html, "Portal de herramientas tiene logo light en pie")
check("lucide-cloud" not in tools_html or "bg-ink text-white" not in tools_html, "Logo genérico de nube negra eliminado del footer")

dark_logo = DIST / "herramientas/assets/logo-nube-para-pymes-dark.webp"
check(dark_logo.exists(), "Archivo de logo dark existe")
img_dark = Image.open(dark_logo)
check(img_dark.mode == "RGBA", "Logo dark tiene canal alfa RGBA transparente")
print(f"       -> Dimensiones Dark Logo: {img_dark.size}")

light_logo = DIST / "herramientas/assets/logo-nube-para-pymes-light.webp"
check(light_logo.exists(), "Archivo de logo light existe")
img_light = Image.open(light_logo)
check(img_light.mode == "RGBA", "Logo light tiene canal alfa RGBA transparente")
print(f"       -> Dimensiones Light Logo: {img_light.size}")

# 3. Favicons e Isotipos
fav = DIST / "herramientas/assets/favicon.png"
check(fav.exists(), "Favicon en herramientas/assets existe")
img_fav = Image.open(fav)
check(img_fav.size == (128, 128), "Favicon tiene resolución 128x128")
check(img_fav.mode == "RGBA", "Favicon es RGBA transparente")

iso = DIST / "assets/logo-nube-para-pymes.png"
check(iso.exists(), "Isotipo master en assets existe")
img_iso = Image.open(iso)
check(img_iso.size == (512, 512), "Isotipo master es 512x512")

print("=== TODAS LAS COMPROBACIONES DE IDENTIDAD VISUAL PASARON CON ÉXITO ===")
