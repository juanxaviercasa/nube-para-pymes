#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el banner de portada oficial de LinkedIn en formato estándar 4:1 (1584 x 396 px),
en modo RGB estándar (sin canal alfa que cause error en LinkedIn) y guardado en PNG y JPG.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"

def make_banner():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1584 x 396 px es la resolución nativa recomendada por LinkedIn (Ratio 4:1)
    W, H = 1584, 396
    banner = Image.new("RGB", (W, H), (11, 15, 25)) # Dark navy #0B0F19

    draw = ImageDraw.Draw(banner)
    
    # 1. Fondo degradado profesional
    for x in range(W):
        ratio = x / W
        r = int(11 + ratio * (26 - 11))
        g = int(15 + ratio * (24 - 15))
        b = int(25 + ratio * (68 - 25))
        draw.line([(x, 0), (x, H)], fill=(r, g, b))

    # 2. Resplandor sutil (glow)
    for r in range(180, 0, -5):
        alpha_val = int((1 - r / 180) * 20)
        draw.ellipse([W - 300 - r, -50 - r, W - 300 + r, -50 + r], outline=(56, 189, 248), width=1)

    # 3. Logo Nube para Pymes
    # Cargar logo horizontal oscuro
    logo_dark_path = ASSETS_DIR / "logo-nube-para-pymes-dark.png"
    if logo_dark_path.exists():
        logo_dark = Image.open(logo_dark_path).convert("RGBA")
        target_h = 130
        target_w = int(logo_dark.width * (target_h / logo_dark.height))
        resized_logo = logo_dark.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Pegar desplazado de la izquierda (x = 100) para no solaparse con el avatar en móvil
        # Como banner es RGB, usamos el canal alfa de resized_logo como máscara
        banner.paste(resized_logo, (100, int((H - target_h) / 2)), resized_logo)

    # 4. Textos de alto impacto a la derecha
    try:
        font_pill = ImageFont.truetype("arial.ttf", 16)
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_desc = ImageFont.truetype("arial.ttf", 20)
        font_url = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font_pill = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_desc = ImageFont.load_default()
        font_url = ImageFont.load_default()

    # Caja / Badge "CATÁLOGO 2026"
    draw.rectangle([(750, 85), (960, 118)], fill=(30, 41, 59), outline=(56, 189, 248), width=1)
    draw.text((765, 93), "CATÁLOGO 2026", fill=(56, 189, 248), font=font_pill)

    # Título principal
    draw.text((750, 135), "26 Herramientas Gratuitas para Pymes", fill=(255, 255, 255), font=font_title)
    
    # Subtítulo
    draw.text((750, 195), "Finanzas · Ventas · Marketing · Operaciones · Legal", fill=(203, 213, 225), font=font_desc)
    draw.text((750, 230), "Sin registro obligatorio · 100% Privadas en tu navegador", fill=(148, 163, 184), font=font_desc)

    # URL destacada
    draw.text((750, 275), "🔗  nubeparapymes.online", fill=(56, 189, 248), font=font_url)

    # Guardar en JPG y PNG (ambos en modo RGB 24-bit sin canal alfa)
    jpg_path = ASSETS_DIR / "linkedin-banner-1584x396.jpg"
    png_path = ASSETS_DIR / "linkedin-banner-1584x396.png"
    
    banner.save(jpg_path, "JPEG", quality=95)
    banner.save(png_path, "PNG")

    print(f"[OK] Banner JPG generado: {jpg_path} ({jpg_path.stat().st_size / 1024:.1f} KB)")
    print(f"[OK] Banner PNG generado: {png_path} ({png_path.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    make_banner()
