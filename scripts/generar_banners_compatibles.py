#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera archivos de banner ultra-compatibles con LinkedIn:
- portada.jpg (1128 x 191 px, tamaño oficial exacto de Página de Empresa de LinkedIn)
- banner.jpg (1584 x 396 px, tamaño estándar 4:1)
Nombres simples sin guiones ni caracteres especiales para evitar bugs del uploader.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"

def create_clean_banners():
    # 1. portada.jpg (1128 x 191) - Oficial Company Page
    W1, H1 = 1128, 191
    img1 = Image.new("RGB", (W1, H1), (11, 15, 25))
    draw1 = ImageDraw.Draw(img1)
    
    for x in range(W1):
        ratio = x / W1
        r = int(11 + ratio * (26 - 11))
        g = int(15 + ratio * (24 - 15))
        b = int(25 + ratio * (68 - 25))
        draw1.line([(x, 0), (x, H1)], fill=(r, g, b))

    logo_path = ASSETS_DIR / "logo-nube-para-pymes-dark.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        th1 = 65
        tw1 = int(logo.width * (th1 / logo.height))
        logo1 = logo.resize((tw1, th1), Image.Resampling.LANCZOS)
        img1.paste(logo1, (160, int((H1 - th1) / 2)), logo1)

    try:
        font1 = ImageFont.truetype("arial.ttf", 20)
        font1_sub = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font1 = ImageFont.load_default()
        font1_sub = ImageFont.load_default()

    draw1.text((580, 70), "26 Herramientas Gratuitas para Pymes", fill=(255, 255, 255), font=font1)
    draw1.text((580, 100), "nubeparapymes.online · Sin registro · Privadas", fill=(56, 189, 248), font=font1_sub)

    out1 = ROOT / "portada.jpg"
    img1.save(out1, "JPEG", quality=92)
    print(f"[OK] Creado: {out1} ({out1.stat().st_size / 1024:.1f} KB, 1128x191)")

    # 2. banner.jpg (1584 x 396)
    W2, H2 = 1584, 396
    img2 = Image.new("RGB", (W2, H2), (11, 15, 25))
    draw2 = ImageDraw.Draw(img2)
    for x in range(W2):
        ratio = x / W2
        r = int(11 + ratio * (26 - 11))
        g = int(15 + ratio * (24 - 15))
        b = int(25 + ratio * (68 - 25))
        draw2.line([(x, 0), (x, H2)], fill=(r, g, b))

    if logo_path.exists():
        th2 = 120
        tw2 = int(logo.width * (th2 / logo.height))
        logo2 = logo.resize((tw2, th2), Image.Resampling.LANCZOS)
        img2.paste(logo2, (120, int((H2 - th2) / 2)), logo2)

    try:
        font2 = ImageFont.truetype("arial.ttf", 34)
        font2_sub = ImageFont.truetype("arial.ttf", 20)
    except Exception:
        font2 = ImageFont.load_default()
        font2_sub = ImageFont.load_default()

    draw2.text((700, 140), "26 Herramientas Gratuitas para Pymes", fill=(255, 255, 255), font=font2)
    draw2.text((700, 195), "nubeparapymes.online · Finanzas · Ventas · Marketing", fill=(56, 189, 248), font=font2_sub)

    out2 = ROOT / "banner.jpg"
    img2.save(out2, "JPEG", quality=92)
    print(f"[OK] Creado: {out2} ({out2.stat().st_size / 1024:.1f} KB, 1584x396)")

if __name__ == "__main__":
    create_clean_banners()
