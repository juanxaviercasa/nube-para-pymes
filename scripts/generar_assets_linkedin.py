#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los assets oficiales optimizados para la Página de Empresa en LinkedIn:
1. Logotipo cuadrado oficial: 300x300 px (assets/linkedin-logo-300x300.png)
2. Banner de portada oficial: 1128x191 px (assets/linkedin-banner-1128x191.png)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"

def generate_linkedin_assets():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Logotipo Cuadrado 300x300 px
    # Usamos logo-nube-para-pymes-impact.png o logo-nube-para-pymes.png
    src_logo = ASSETS_DIR / "logo-nube-para-pymes-impact.png"
    if not src_logo.exists():
        src_logo = ASSETS_DIR / "logo-nube-para-pymes.png"

    img = Image.open(src_logo).convert("RGBA")
    logo_300 = img.resize((300, 300), Image.Resampling.LANCZOS)
    
    # Crear un contenedor con fondo blanco limpio para que resalte perfecto en el feed blanco y gris de LinkedIn
    bg_logo = Image.new("RGBA", (300, 300), (255, 255, 255, 255))
    # Pegar el logo centrado
    bg_logo.paste(logo_300, (0, 0), logo_300)
    logo_out = ASSETS_DIR / "linkedin-logo-300x300.png"
    bg_logo.save(logo_out, "PNG")
    print(f"[OK] Logotipo guardado: {logo_out} (300x300 px)")

    # 2. Banner de Portada 1128x191 px
    W, H = 1128, 191
    banner = Image.new("RGBA", (W, H), (15, 23, 42, 255)) # Dark navy #0F172A

    # Fondo con degradado moderno #0B0F19 a #1E1B4B
    draw = ImageDraw.Draw(banner)
    for x in range(W):
        ratio = x / W
        r = int(11 + ratio * (30 - 11))
        g = int(15 + ratio * (27 - 15))
        b = int(25 + ratio * (75 - 25))
        draw.line([(x, 0), (x, H)], fill=(r, g, b, 255))

    # Cargar logo horizontal oscuro (texto blanco)
    logo_dark_path = ASSETS_DIR / "logo-nube-para-pymes-dark.png"
    if logo_dark_path.exists():
        logo_dark = Image.open(logo_dark_path).convert("RGBA")
        target_h = 60
        target_w = int(logo_dark.width * (target_h / logo_dark.height))
        resized_logo = logo_dark.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # En LinkedIn Company Pages, el avatar de la empresa cubre los primeros ~160px inferiores a la izquierda.
        # Por ello, ubicamos el logo y los textos desplazados a la derecha (x = 220) para perfecta visibilidad.
        banner.paste(resized_logo, (200, int((H - target_h) / 2)), resized_logo)

    # Añadir texto descriptivo y URL en el banner a la derecha
    try:
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    draw.text((620, 70), "26 Herramientas Gratuitas para Pymes", fill=(248, 250, 252, 255), font=font_title)
    draw.text((620, 100), "nubeparapymes.online · Sin registro · 100% Privadas", fill=(56, 189, 248, 255), font=font_sub)

    banner_out = ASSETS_DIR / "linkedin-banner-1128x191.png"
    banner.save(banner_out, "PNG")
    print(f"[OK] Banner guardado: {banner_out} (1128x191 px)")

if __name__ == "__main__":
    generate_linkedin_assets()
