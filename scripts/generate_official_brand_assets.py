#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera y exporta todos los assets oficiales y unificados de la marca NubeParaPymes
a partir del master auténtico de Canva (sin pérdida de resolución ni artefactos).
"""

import subprocess
import io
import numpy as np
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
WP_07 = ROOT / "nubepymesexport" / "wp-content" / "uploads" / "2026" / "07"
WP_08 = ROOT / "nubepymesexport" / "wp-content" / "uploads" / "2026" / "08"

ASSETS_DIR.mkdir(parents=True, exist_ok=True)
WP_07.mkdir(parents=True, exist_ok=True)
WP_08.mkdir(parents=True, exist_ok=True)

# 1. Cargar el master de Canva desde git commit 76a15c9
print("1. Cargando master original de Canva...")
raw_data = subprocess.check_output([
    'git', 'show', '76a15c9:nubepymesexport/wp-content/uploads/2026/07/logo-nubeparapymes-header.webp'
])
orig_img = Image.open(io.BytesIO(raw_data)).convert("RGBA")
arr_orig = np.array(orig_img)

# Bounding box del contenido
alpha = arr_orig[:, :, 3]
ys, xs = np.where(alpha > 0)
ymin, ymax = ys.min(), ys.max()
xmin, xmax = xs.min(), xs.max()

# Recorte ajustado del logo claro
light_logo = orig_img.crop((xmin, ymin, xmax + 1, ymax + 1))
print(f"   Logo claro recortado: {light_logo.size} (Ratio: {light_logo.width/light_logo.height:.2f}:1)")

# 2. Generar el logo oscuro (texto blanco, icono idéntico)
arr_dark = np.array(orig_img).copy()
h, w, _ = arr_dark.shape
for y in range(h):
    for x in range(200, w):
        if arr_dark[y, x, 3] > 0:
            arr_dark[y, x, 0] = 255
            arr_dark[y, x, 1] = 255
            arr_dark[y, x, 2] = 255

dark_logo_full = Image.fromarray(arr_dark, "RGBA")
dark_logo = dark_logo_full.crop((xmin, ymin, xmax + 1, ymax + 1))
print(f"   Logo oscuro recortado: {dark_logo.size}")

# 3. Generar Isotipo Cuadrado (Icono nube + maletín + flecha)
orange_mask = (arr_orig[:,:,0] > 180) & (arr_orig[:,:,1] > 90) & (arr_orig[:,:,2] < 70) & (alpha > 100)
cloud_mask = (arr_orig[:,:,0] < 100) & (arr_orig[:,:,1] > 100) & (arr_orig[:,:,2] > 180) & (alpha > 100)
symbol_pixels = orange_mask | cloud_mask
sys, sxs = np.where(symbol_pixels)

# Bounding box ajustado del símbolo
s_ymin, s_ymax = sys.min() - 2, sys.max() + 3
s_xmin, s_xmax = sxs.min() - 3, sxs.max() + 5
s_ymin = max(0, s_ymin)
s_xmin = max(0, s_xmin)

icon_crop = orig_img.crop((s_xmin, s_ymin, s_xmax + 1, s_ymax + 1))
print(f"   Símbolo isotipo recortado: {icon_crop.size}")

# Crear lienzo 512x512 centrado
iso_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
target_w = 440
ratio = target_w / icon_crop.width
target_h = int(icon_crop.height * ratio)
resized_icon = icon_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
offset_x = (512 - target_w) // 2
offset_y = (512 - target_h) // 2
iso_512.paste(resized_icon, (offset_x, offset_y), resized_icon)
print(f"   Isotipo 512x512 generado.")

# 4. Guardar en assets/
print("2. Guardando assets unificados en assets/...")
light_logo.save(ASSETS_DIR / "logo-nube-para-pymes-light.webp", "WEBP", quality=95)
light_logo.save(ASSETS_DIR / "logo-nube-para-pymes-light.png", "PNG")

dark_logo.save(ASSETS_DIR / "logo-nube-para-pymes-dark.webp", "WEBP", quality=95)
dark_logo.save(ASSETS_DIR / "logo-nube-para-pymes-dark.png", "PNG")

iso_512.save(ASSETS_DIR / "logo-nube-para-pymes.png", "PNG")
iso_512.save(ASSETS_DIR / "logo-nube-para-pymes-impact.png", "PNG")

favicon_128 = iso_512.resize((128, 128), Image.Resampling.LANCZOS)
favicon_128.save(ASSETS_DIR / "favicon.png", "PNG")

favicon_64 = iso_512.resize((64, 64), Image.Resampling.LANCZOS)
favicon_64.save(ASSETS_DIR / "favicon-64.png", "PNG")

favicon_32 = iso_512.resize((32, 32), Image.Resampling.LANCZOS)
favicon_32.save(ASSETS_DIR / "favicon-32.png", "PNG")

# 5. Guardar versiones para WordPress (nubepymesexport)
print("3. Guardando versiones de cabecera de WordPress en nubepymesexport/...")
# Restaurar el master original con su proporción estándar
orig_img.save(WP_07 / "logo-nubeparapymes-header.webp", "WEBP", quality=95)

# Variantes de tamaño del header
h_200 = int(light_logo.height * (200 / light_logo.width))
light_200 = light_logo.resize((200, h_200), Image.Resampling.LANCZOS)
# Lo colocamos en un canvas de 200x67 si es necesario para compatibilidad exacta de Astra
canvas_200x67 = Image.new("RGBA", (200, 67), (0, 0, 0, 0))
canvas_200x67.paste(light_200, ((200 - 200) // 2, (67 - h_200) // 2), light_200)
canvas_200x67.save(WP_07 / "logo-nubeparapymes-header-200x67.webp", "WEBP", quality=95)

h_300 = int(light_logo.height * (300 / light_logo.width))
light_300 = light_logo.resize((300, h_300), Image.Resampling.LANCZOS)
canvas_300x100 = Image.new("RGBA", (300, 100), (0, 0, 0, 0))
canvas_300x100.paste(light_300, ((300 - 300) // 2, (100 - h_300) // 2), light_300)
canvas_300x100.save(WP_07 / "logo-nubeparapymes-header-300x100.webp", "WEBP", quality=95)

# Cuadrados WordPress
iso_300 = iso_512.resize((300, 300), Image.Resampling.LANCZOS)
iso_300.save(WP_08 / "logo-nube-para-pymes-2026-300x300.webp", "WEBP", quality=95)

iso_150 = iso_512.resize((150, 150), Image.Resampling.LANCZOS)
iso_150.save(WP_07 / "logo-nubeparapymes-header-150x150.webp", "WEBP", quality=95)
iso_150.save(WP_08 / "logo-nube-para-pymes-2026-150x150.webp", "WEBP", quality=95)

print("¡Todos los assets oficiales de marca generados y exportados exitosamente!")
