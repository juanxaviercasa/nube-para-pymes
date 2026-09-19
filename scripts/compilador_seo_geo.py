#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador Autónomo de Artículos SEO + GEO para Nube para Pymes
===============================================================
Convierte borradores en Markdown a páginas estáticas completas sin depender
de WordPress ni Pantheon.

Genera de forma 100% programática (Pillow):
  1. Imagen destacada (Hero banner 1200x675 px)
  2. Diagrama / Framework conceptual (1200x675 px)
  3. Matriz de decisión / Checklist de criterios (1200x675 px)

Inyecta Schema.org JSON-LD (BlogPosting y FAQPage para motores de IA),
actualiza sitemap.xml, search-index.json y registra la nueva entrada
en la cola de redes sociales (scripts/linkedin_queue.json).
"""

import argparse
import html
import io
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Rutas del proyecto
ROOT = Path(__file__).resolve().parent.parent
BORRADORES_DIR = ROOT / "borradores"
BORRADORES_PUB_DIR = BORRADORES_DIR / "publicados"
DIST_DIR = ROOT / "dist"
WP_EXPORT_DIR = ROOT / "nubepymesexport"
QUEUE_FILE = ROOT / "scripts" / "linkedin_queue.json"

YEAR_MONTH = "2026/09"
UPLOADS_DIST = DIST_DIR / "wp-content" / "uploads" / YEAR_MONTH
UPLOADS_WP = WP_EXPORT_DIR / "wp-content" / "uploads" / YEAR_MONTH

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Colores de la marca Nube para Pymes
COLOR_BG_DARK = (15, 23, 42)        # Slate 900
COLOR_CARD_BG = (30, 41, 59)        # Slate 800
COLOR_ACCENT = (13, 148, 136)       # Teal 600
COLOR_ACCENT_LIGHT = (45, 212, 191) # Teal 400
COLOR_TEXT_MAIN = (255, 255, 255)   # Blanco puro
COLOR_TEXT_MUTED = (203, 213, 225)  # Slate 300
COLOR_BORDER = (51, 65, 85)         # Slate 700


def get_font(size: int, bold: bool = False):
    """Obtiene tipografía del sistema o fallback estándar."""
    font_names = (
        [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "arialbd.ttf", "segoeuib.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "arial.ttf", "segoeui.ttf", "calibri.ttf", "DejaVuSans.ttf"
        ]
    )
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def wrap_text(text: str, max_chars: int = 42) -> list[str]:
    """Divide un texto en líneas para lienzos visuales."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        current_line = []
        current_len = 0
        for w in words:
            if current_len + len(w) + 1 > max_chars:
                lines.append(" ".join(current_line))
                current_line = [w]
                current_len = len(w)
            else:
                current_line.append(w)
                current_len += len(w) + 1
        if current_line:
            lines.append(" ".join(current_line))
    return lines


# ==============================================================================
# GENERACIÓN DE LAS 3 IMÁGENES SINTÉTICAS (PILLOW)
# ==============================================================================

def generate_image_destacada(title: str, category: str, author: str) -> Image.Image:
    """Genera la Imagen 1: Portada de Autoridad Editorial (1200 x 675 px - 16:9)."""
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), COLOR_BG_DARK)
    draw = ImageDraw.Draw(img)

    # Marco exterior sutil
    draw.rounded_rectangle([(24, 24), (W - 24, H - 24)], radius=24, outline=COLOR_BORDER, width=2)
    draw.rounded_rectangle([(50, 50), (W - 50, H - 50)], radius=20, fill=COLOR_CARD_BG)

    # Pastilla superior de categoría (ancho dinámico)
    font_badge = get_font(20, bold=True)
    badge_text = f"GUÍA TÉCNICA · {category.upper()}"
    bbox = font_badge.getbbox(badge_text)
    text_w = bbox[2] - bbox[0]
    badge_w = text_w + 36
    draw.rounded_rectangle([(70, 75), (70 + badge_w, 122)], radius=14, fill=COLOR_ACCENT)
    draw.text((70 + badge_w // 2, 98), badge_text, fill=COLOR_TEXT_MAIN, font=font_badge, anchor="mm")

    # Título principal
    font_title = get_font(48, bold=True)
    title_lines = wrap_text(title, max_chars=34)
    y_cursor = 175
    for line in title_lines[:4]:
        draw.text((70, y_cursor), line, fill=COLOR_TEXT_MAIN, font=font_title)
        y_cursor += 62

    # Línea decorativa
    y_cursor += 15
    draw.line([(70, y_cursor), (280, y_cursor)], fill=COLOR_ACCENT_LIGHT, width=4)

    # Franja inferior de autor y portal
    footer_top = H - 120
    draw.line([(50, footer_top), (W - 50, footer_top)], fill=COLOR_BORDER, width=1)

    font_author = get_font(24, bold=True)
    font_brand = get_font(20, bold=False)
    draw.text((70, footer_top + 28), f"Autor: {author}", fill=COLOR_TEXT_MAIN, font=font_author)
    draw.text((70, footer_top + 58), "Nube para Pymes · Análisis independiente de software y procesos", fill=COLOR_TEXT_MUTED, font=font_brand)

    font_url = get_font(24, bold=True)
    draw.text((W - 70, footer_top + 45), "nubeparapymes.online", fill=COLOR_ACCENT_LIGHT, font=font_url, anchor="rm")

    return img


def generate_image_framework(framework_title: str, steps: list[str]) -> Image.Image:
    """Genera la Imagen 2: Diagrama de Marco de Trabajo / Framework Conceptual (1200 x 675 px)."""
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), COLOR_BG_DARK)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([(24, 24), (W - 24, H - 24)], radius=24, outline=COLOR_BORDER, width=2)
    draw.rounded_rectangle([(50, 50), (W - 50, H - 50)], radius=20, fill=COLOR_CARD_BG)

    # Cabecera del framework
    font_head_badge = get_font(20, bold=True)
    draw.rounded_rectangle([(70, 75), (420, 118)], radius=12, fill=(15, 23, 42), outline=COLOR_ACCENT, width=2)
    draw.text((245, 96), "FRAMEWORK METODOLÓGICO", fill=COLOR_ACCENT_LIGHT, font=font_head_badge, anchor="mm")

    font_head_title = get_font(38, bold=True)
    draw.text((70, 140), framework_title, fill=COLOR_TEXT_MAIN, font=font_head_title)

    # Renderizar los 4 pasos en cuadrícula 2x2
    box_w = 510
    box_h = 160
    positions = [
        (70, 215),          # Paso 1
        (W - 70 - box_w, 215), # Paso 2
        (70, 405),          # Paso 3
        (W - 70 - box_w, 405)  # Paso 4
    ]

    font_step_num = get_font(26, bold=True)
    font_step_text = get_font(22, bold=False)

    for i, step_text in enumerate(steps[:4]):
        x, y = positions[i]
        # Fondo de cada tarjeta
        draw.rounded_rectangle([(x, y), (x + box_w, y + box_h)], radius=14, fill=(15, 23, 42), outline=COLOR_BORDER, width=2)
        # Barra lateral izquierda en color acento
        draw.rounded_rectangle([(x, y), (x + 8, y + box_h)], radius=4, fill=COLOR_ACCENT)

        # Número del paso
        draw.text((x + 28, y + 24), f"FASE 0{i + 1}", fill=COLOR_ACCENT_LIGHT, font=font_step_num)

        # Texto del paso
        lines = wrap_text(step_text, max_chars=32)
        inner_y = y + 64
        for l in lines[:3]:
            draw.text((x + 28, inner_y), l, fill=COLOR_TEXT_MAIN, font=font_step_text)
            inner_y += 28

    # Pie
    font_footer = get_font(18, bold=False)
    draw.text((W // 2, H - 42), "Metodología editorial de optimización · Nube para Pymes", fill=COLOR_TEXT_MUTED, font=font_footer, anchor="mm")

    return img


def generate_image_matriz(title: str, key_points: list[str]) -> Image.Image:
    """Genera la Imagen 3: Matriz de Decisión / Checklist de Criterios (1200 x 675 px)."""
    W, H = 1200, 675
    img = Image.new("RGB", (W, H), COLOR_BG_DARK)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([(24, 24), (W - 24, H - 24)], radius=24, outline=COLOR_BORDER, width=2)
    draw.rounded_rectangle([(50, 50), (W - 50, H - 50)], radius=20, fill=COLOR_CARD_BG)

    # Cabecera
    font_badge = get_font(20, bold=True)
    draw.rounded_rectangle([(70, 75), (420, 118)], radius=12, fill=COLOR_ACCENT)
    draw.text((245, 96), "CHECKLIST Y CRITERIOS CLAVE", fill=COLOR_TEXT_MAIN, font=font_badge, anchor="mm")

    font_title = get_font(36, bold=True)
    draw.text((70, 140), "Criterios Esenciales para tu Pyme", fill=COLOR_TEXT_MAIN, font=font_title)

    # Filas de checklist
    font_check = get_font(24, bold=True)
    font_row = get_font(23, bold=False)

    y_cursor = 210
    for i, pt in enumerate(key_points[:4], 1):
        # Tarjeta de la fila
        draw.rounded_rectangle([(70, y_cursor), (W - 70, y_cursor + 78)], radius=12, fill=(15, 23, 42), outline=COLOR_BORDER, width=1)
        # Icono de check
        draw.rounded_rectangle([(88, y_cursor + 18), (130, y_cursor + 60)], radius=8, fill=COLOR_ACCENT)
        draw.text((109, y_cursor + 38), f"0{i}", fill=COLOR_TEXT_MAIN, font=font_check, anchor="mm")

        # Texto del criterio
        clean_text = re.sub(r"^[•\-\*✓\d\.]+\s*", "", pt)
        draw.text((150, y_cursor + 26), clean_text[:75], fill=COLOR_TEXT_MAIN, font=font_row)
        y_cursor += 94

    # Llamada a la acción inferior
    cta_y = H - 85
    font_cta = get_font(22, bold=True)
    draw.text((W // 2, cta_y), "Análisis completo, tablas y herramientas en: nubeparapymes.online", fill=COLOR_ACCENT_LIGHT, font=font_cta, anchor="mm")

    return img


# ==============================================================================
# PROCESAMIENTO DEL MARKDOWN Y METADATOS
# ==============================================================================

def parse_markdown_draft(file_path: Path) -> dict:
    """Lee un borrador en Markdown y extrae Frontmatter YAML y cuerpo."""
    content = file_path.read_text(encoding="utf-8")
    meta = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_yaml = parts[1]
            body = parts[2].strip()

            current_key = None
            current_list = None
            current_dict = None

            for raw_line in raw_yaml.split("\n"):
                line = raw_line.rstrip()
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue

                indent = len(line) - len(line.lstrip())

                # Si está entre comillas (ej: - "Fase 1: ..."), es un string, no un dict
                if stripped.startswith('- "') or stripped.startswith("- '"):
                    val = stripped[2:].strip().strip('"').strip("'")
                    current_dict = None
                    if current_key:
                        if not isinstance(meta.get(current_key), list):
                            meta[current_key] = []
                        meta[current_key].append(val)
                    continue

                # Elemento de lista que es un diccionario: "  - question: ..." (sin comillas envolventes)
                if stripped.startswith("- ") and ":" in stripped:
                    item_content = stripped[2:].strip()
                    sub_k, sub_v = item_content.split(":", 1)
                    current_dict = {sub_k.strip(): sub_v.strip().strip('"').strip("'")}
                    if current_key:
                        if not isinstance(meta.get(current_key), list):
                            meta[current_key] = []
                        meta[current_key].append(current_dict)
                    continue

                # Continuación de diccionario: "    answer: ..."
                if indent >= 4 and ":" in stripped and current_dict is not None:
                    sub_k, sub_v = stripped.split(":", 1)
                    current_dict[sub_k.strip()] = sub_v.strip().strip('"').strip("'")
                    continue

                # Elemento simple de lista: "  - elemento"
                if stripped.startswith("- "):
                    val = stripped[2:].strip().strip('"').strip("'")
                    current_dict = None
                    if current_key:
                        if not isinstance(meta.get(current_key), list):
                            meta[current_key] = []
                        meta[current_key].append(val)
                    continue

                # Clave de primer nivel: "key: value" o "key:"
                if ":" in stripped:
                    current_dict = None
                    k, v = stripped.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    current_key = k
                    if v:
                        meta[k] = v
                    else:
                        meta[k] = []

    meta["body_markdown"] = body
    if "slug" not in meta and "title" in meta:
        meta["slug"] = re.sub(r"[^a-z0-9]+", "-", meta["title"].lower()).strip("-")

    return meta


def markdown_to_html(md_text: str) -> str:
    """Convierte Markdown estándar a HTML limpio."""
    html_out = []
    lines = md_text.split("\n")
    in_list = False
    in_table = False
    table_rows = []

    for line in lines:
        stripped = line.strip()

        # Cerrar listas si la línea no es ítem
        if in_list and not (stripped.startswith("- ") or stripped.startswith("* ") or re.match(r"^\d+\.\s", stripped)):
            html_out.append("</ul>" if in_list == "ul" else "</ol>")
            in_list = False

        # Tablas markdown
        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(stripped)
            continue
        elif in_table:
            # Procesar tabla acumulada
            in_table = False
            html_out.append(render_markdown_table(table_rows))

        if not stripped:
            continue

        # Encabezados
        if stripped.startswith("### "):
            text = stripped[4:]
            html_out.append(f'<h3 class="wp-block-heading">{html.escape(text)}</h3>')
        elif stripped.startswith("## "):
            text = stripped[3:]
            heading_id = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
            html_out.append(f'<h2 class="wp-block-heading" id="{heading_id}">{html.escape(text)}</h2>')
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if in_list != "ul":
                html_out.append('<ul class="wp-block-list">')
                in_list = "ul"
            item_text = format_inline_markdown(stripped[2:])
            html_out.append(f"<li>{item_text}</li>")
        elif re.match(r"^\d+\.\s", stripped):
            if in_list != "ol":
                html_out.append('<ol class="wp-block-list">')
                in_list = "ol"
            item_text = format_inline_markdown(re.sub(r"^\d+\.\s", "", stripped))
            html_out.append(f"<li>{item_text}</li>")
        else:
            p_text = format_inline_markdown(stripped)
            html_out.append(f'<p class="wp-block-paragraph">{p_text}</p>')

    if in_list:
        html_out.append("</ul>" if in_list == "ul" else "</ol>")
    if in_table:
        html_out.append(render_markdown_table(table_rows))

    return "\n".join(html_out)


def format_inline_markdown(text: str) -> str:
    """Procesa negritas, enlaces y código en línea."""
    # Enlaces: [texto](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Negritas: **texto**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Cursivas: *texto*
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    return text


def render_markdown_table(rows: list[str]) -> str:
    """Renderiza una tabla en formato Astra/WordPress."""
    if len(rows) < 2:
        return ""
    header_cols = [c.strip() for c in rows[0].strip("|").split("|")]
    data_rows = rows[2:] if len(rows) >= 3 and "---" in rows[1] else rows[1:]

    h_html = "".join(f"<th>{format_inline_markdown(c)}</th>" for c in header_cols)
    b_html = []
    for r in data_rows:
        cols = [c.strip() for c in r.strip("|").split("|")]
        row_str = "".join(f"<td>{format_inline_markdown(c)}</td>" for c in cols)
        b_html.append(f"<tr>{row_str}</tr>")

    return f"""<figure class="wp-block-table is-style-stripes">
<table class="has-fixed-layout">
<thead><tr>{h_html}</tr></thead>
<tbody>{"".join(b_html)}</tbody>
</table>
</figure>"""


# ==============================================================================
# ENSAMBLADOR HTML COMPLETO CON SCHEMA.ORG (SEO + GEO)
# ==============================================================================

def build_article_html(meta: dict, body_html: str, img_destacada_url: str, img_framework_url: str, img_matriz_url: str) -> str:
    """Construye el documento HTML completo idéntico al tema Astra de Nube para Pymes."""
    title = meta["title"]
    slug = meta["slug"]
    description = meta.get("description", "")
    category = meta.get("category", "Productividad")
    category_slug = meta.get("category_slug", "automatizacion-ia")
    author = meta.get("author", "Xavier Cabello")
    canonical_url = f"https://nubeparapymes.online/{slug}/"
    date_published = meta.get("date", datetime.now().strftime("%Y-%m-%d"))

    # Inyectar las imágenes internas en el cuerpo
    body_parts = body_html.split('</h2>', 2)
    if len(body_parts) >= 3:
        # Tras la segunda sección H2, inyectar el Framework
        body_with_images = (
            body_parts[0] + '</h2>' +
            body_parts[1] + '</h2>' +
            f'\n<figure class="wp-block-image npp-editorial-card"><img src="{img_framework_url}" alt="Framework metodológico de {html.escape(title)}" loading="lazy"></figure>\n' +
            body_parts[2]
        )
    else:
        body_with_images = body_html

    # Inyectar la Matriz de decisión antes de la conclusión o al final
    body_with_images += (
        f'\n<figure class="wp-block-image npp-editorial-card"><img src="{img_matriz_url}" alt="Checklist y matriz de {html.escape(title)}" loading="lazy"></figure>\n'
    )

    # Inyectar FAQs si existen en el borrador
    faqs = meta.get("faqs", [])
    faq_schema_list = []
    if faqs:
        body_with_images += '\n<h2 class="wp-block-heading" id="preguntas_frecuentes">Preguntas Frecuentes (FAQ)</h2>\n'
        for faq in faqs:
            q = faq.get("question", "")
            a = faq.get("answer", "")
            body_with_images += f'<h3>{html.escape(q)}</h3>\n<p>{html.escape(a)}</p>\n'
            faq_schema_list.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": a
                }
            })

    # Construir Schema.org JSON-LD (GEO + SEO)
    schema_graph = [
        {
            "@type": "BlogPosting",
            "@id": f"{canonical_url}#blogposting",
            "headline": title,
            "description": description,
            "datePublished": f"{date_published}T08:00:00-05:00",
            "dateModified": f"{date_published}T08:00:00-05:00",
            "mainEntityOfPage": canonical_url,
            "url": canonical_url,
            "image": img_destacada_url,
            "author": {
                "@type": "Person",
                "name": author,
                "url": "https://nubeparapymes.online/author/xaviercabello/"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Nube para Pymes",
                "url": "https://nubeparapymes.online/"
            }
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://nubeparapymes.online/"},
                {"@type": "ListItem", "position": 2, "name": category, "item": f"https://nubeparapymes.online/category/{category_slug}/"},
                {"@type": "ListItem", "position": 3, "name": title, "item": canonical_url}
            ]
        }
    ]

    if faq_schema_list:
        schema_graph.append({
            "@type": "FAQPage",
            "mainEntity": faq_schema_list
        })

    schema_json = json.dumps({"@context": "https://schema.org", "@graph": schema_graph}, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang="es" prefix="og: https://ogp.me/ns#">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | Nube para Pymes</title>
<meta name="description" content="{html.escape(description)}">
<meta name="robots" content="index, follow, max-snippet:-1, max-video-preview:-1, max-image-preview:large">
<link rel="canonical" href="{canonical_url}">

<!-- OpenGraph / Facebook / LinkedIn -->
<meta property="og:locale" content="es_ES">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical_url}">
<meta property="og:site_name" content="Nube para Pymes">
<meta property="og:image" content="{img_destacada_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="675">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(description)}">
<meta name="twitter:image" content="{img_destacada_url}">
<meta name="twitter:label1" content="Escrito por">
<meta name="twitter:data1" content="{html.escape(author)}">

<!-- Schema.org JSON-LD (SEO + GEO para IAs) -->
<script type="application/ld+json">
{schema_json}
</script>

<link rel="stylesheet" href="/wp-content/themes/astra/assets/css/minified/main.min.css" media="all">
<link rel="stylesheet" href="/wp-includes/css/dist/block-library/style.min.css" media="all">
<link rel="stylesheet" href="/wp-static-arquitect-assets/search-modal.css">

<style>
.npp-editorial-card img {{
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(15, 44, 76, 0.1);
  margin: 32px 0;
  width: 100%;
  height: auto;
}}
.ast-author-box {{
  margin-top: 48px;
  padding: 28px;
  background: #f8fafc;
  border-left: 4px solid #0d9488;
  border-radius: 8px;
}}
</style>
</head>

<body class="wp-singular post-template-default single single-post ast-desktop ast-separate-container ast-right-sidebar">
<div class="hfeed site" id="page">
  <header class="site-header header-main-layout-1 ast-primary-menu-enabled" id="masthead">
    <div class="ast-container" style="display:flex; justify-content:space-between; align-items:center; padding:16px 20px;">
      <a href="/" rel="home" style="display:flex; align-items:center; text-decoration:none;">
        <img width="180" height="60" src="/wp-content/uploads/2026/07/logo-nubeparapymes-header-200x67.webp" alt="Nube para Pymes">
      </a>
      <nav>
        <a href="/blog/" style="margin-right:20px; text-decoration:none; font-weight:600; color:#0f172a;">Blog</a>
        <a href="/herramientas-gratis/" style="margin-right:20px; text-decoration:none; font-weight:600; color:#0f172a;">Herramientas Gratis</a>
        <a href="/sobre-nosotros/" style="text-decoration:none; font-weight:600; color:#0f172a;">Sobre Nosotros</a>
      </nav>
    </div>
  </header>

  <section class="ast-single-entry-banner" style="background:#0f172a; padding:48px 20px; color:#ffffff;">
    <div class="ast-container" style="max-width:860px; margin:0 auto;">
      <span style="background:#0d9488; color:#ffffff; padding:6px 14px; border-radius:12px; font-size:13px; font-weight:700; text-transform:uppercase;">{html.escape(category)}</span>
      <h1 class="entry-title" style="color:#ffffff; margin:18px 0 12px; font-size:38px; line-height:1.25;">{html.escape(title)}</h1>
      <div style="font-size:14px; color:#94a3b8;">Por <strong>{html.escape(author)}</strong> · Publicado en Nube para Pymes</div>
    </div>
  </section>

  <div id="content" class="site-content" style="max-width:860px; margin:40px auto; padding:0 20px;">
    <main id="main" class="site-main">
      <article class="ast-article-single">
        <figure class="wp-block-image npp-editorial-card">
          <img src="{img_destacada_url}" alt="{html.escape(title)}">
        </figure>

        <div class="entry-content clear">
{body_with_images}
        </div>

        <div class="ast-author-box">
          <h3 style="margin:0 0 8px; font-size:20px; color:#0f172a;">Sobre el Autor: {html.escape(author)}</h3>
          <p style="margin:0; font-size:15px; color:#475569; line-height:1.6;">
            Analista y creador en <strong>Nube para Pymes</strong>. Especializado en evaluación independiente de software, automatización de procesos y optimización de visibilidad digital para pequeñas empresas.
          </p>
        </div>
      </article>
    </main>
  </div>

  <footer style="background:#0f172a; color:#94a3b8; padding:48px 20px; margin-top:60px; text-align:center; font-size:14px;">
    <div class="ast-container" style="max-width:860px; margin:0 auto;">
      <p style="margin-bottom:12px;">© 2026 Nube para Pymes · Herramientas gratuitas y análisis de software independiente.</p>
      <div>
        <a href="/aviso-legal/" style="color:#cbd5e1; margin:0 10px;">Aviso Legal</a>
        <a href="/politica-de-privacidad/" style="color:#cbd5e1; margin:0 10px;">Privacidad</a>
        <a href="/herramientas-gratis/" style="color:#cbd5e1; margin:0 10px;">Catálogo de Herramientas</a>
      </div>
    </div>
  </footer>
</div>
</body>
</html>"""


# ==============================================================================
# PUBLICACIÓN Y ACTUALIZACIÓN DEL SITIO
# ==============================================================================

def publish_draft(draft_path: Path) -> dict:
    """Compila el borrador, genera sus 3 imágenes, actualiza el sitio y la cola social."""
    print(f"\n[1/5] Leyendo borrador: {draft_path.name}...")
    meta = parse_markdown_draft(draft_path)
    title = meta["title"]
    slug = meta["slug"]
    category = meta.get("category", "Productividad")
    author = meta.get("author", "Xavier Cabello")
    key_points = meta.get("key_points", [
        "Criterios técnicos para pequeñas empresas",
        "Análisis independiente de funciones y límites",
        "Recomendaciones paso a paso para aplicar hoy"
    ])
    framework_title = meta.get("framework_title", f"Framework de 4 Fases: {title[:35]}")
    framework_steps = meta.get("framework_steps", [
        "Fase 1: Diagnóstico inicial de requerimientos",
        "Fase 2: Selección técnica y descarte de opciones",
        "Fase 3: Implementación y capacitación básica",
        "Fase 4: Medición de ahorro de tiempo y costes"
    ])

    print(f"[2/5] Generando las 3 imágenes sintéticas con Pillow...")
    UPLOADS_DIST.mkdir(parents=True, exist_ok=True)
    UPLOADS_WP.mkdir(parents=True, exist_ok=True)

    # 1. Imagen Destacada
    im1 = generate_image_destacada(title, category, author)
    f1_webp = UPLOADS_DIST / f"{slug}-destacada.webp"
    f1_jpeg = UPLOADS_DIST / f"{slug}-destacada.jpg"
    im1.save(f1_webp, format="WEBP", quality=90)
    im1.save(f1_jpeg, format="JPEG", quality=90)
    shutil.copy2(f1_webp, UPLOADS_WP / f"{slug}-destacada.webp")

    # 2. Imagen Framework
    im2 = generate_image_framework(framework_title, framework_steps)
    f2_webp = UPLOADS_DIST / f"{slug}-framework.webp"
    f2_jpeg = UPLOADS_DIST / f"{slug}-framework.jpg"
    im2.save(f2_webp, format="WEBP", quality=90)
    im2.save(f2_jpeg, format="JPEG", quality=90)
    shutil.copy2(f2_webp, UPLOADS_WP / f"{slug}-framework.webp")

    # 3. Imagen Matriz / Checklist
    im3 = generate_image_matriz(title, key_points)
    f3_webp = UPLOADS_DIST / f"{slug}-matriz.webp"
    f3_jpeg = UPLOADS_DIST / f"{slug}-matriz.jpg"
    im3.save(f3_webp, format="WEBP", quality=90)
    im3.save(f3_jpeg, format="JPEG", quality=90)
    shutil.copy2(f3_webp, UPLOADS_WP / f"{slug}-matriz.webp")

    img1_url = f"/wp-content/uploads/{YEAR_MONTH}/{slug}-destacada.webp"
    img2_url = f"/wp-content/uploads/{YEAR_MONTH}/{slug}-framework.webp"
    img3_url = f"/wp-content/uploads/{YEAR_MONTH}/{slug}-matriz.webp"
    print(f"  • Imagen 1 (Destacada): {f1_webp.name} (1200x675 px)")
    print(f"  • Imagen 2 (Framework): {f2_webp.name} (1200x675 px)")
    print(f"  • Imagen 3 (Matriz):    {f3_webp.name} (1200x675 px)")

    print(f"[3/5] Compilando HTML con marcado Schema.org...")
    body_html = markdown_to_html(meta["body_markdown"])
    full_html = build_article_html(meta, body_html, img1_url, img2_url, img3_url)

    # Guardar en dist/ y en nubepymesexport/
    article_dist = DIST_DIR / slug
    article_wp = WP_EXPORT_DIR / slug
    article_dist.mkdir(parents=True, exist_ok=True)
    article_wp.mkdir(parents=True, exist_ok=True)

    (article_dist / "index.html").write_text(full_html, encoding="utf-8")
    (article_wp / "index.html").write_text(full_html, encoding="utf-8")
    print(f"  • Página creada: dist/{slug}/index.html")

    print(f"[4/5] Actualizando sitemap.xml y buscador...")
    update_sitemap(slug)
    update_search_index(meta)

    print(f"[5/5] Inyectando artículo en la cola de redes sociales...")
    add_to_social_queue(meta, img1_url)

    # Mover borrador a publicados
    BORRADORES_PUB_DIR.mkdir(parents=True, exist_ok=True)
    dest_draft = BORRADORES_PUB_DIR / draft_path.name
    shutil.move(draft_path, dest_draft)
    print(f"  • Borrador archivado en: {dest_draft.relative_to(ROOT)}")

    print(f"\n[ÉXITO] ¡Artículo «{title}» publicado correctamente!")
    print(f"  • URL local: dist/{slug}/index.html")
    print(f"  • URL canónica: https://nubeparapymes.online/{slug}/\n")
    return meta


def update_sitemap(slug: str):
    """Agrega la nueva URL a los archivos sitemap.xml de forma segura."""
    url_tag = f"""  <url>
    <loc>https://nubeparapymes.online/{slug}/</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""

    for sm_path in [DIST_DIR / "sitemap.xml", ROOT / "sitemap.xml"]:
        if sm_path.exists():
            txt = sm_path.read_text(encoding="utf-8")
            if f"/{slug}/" not in txt:
                txt = txt.replace("</urlset>", url_tag)
                sm_path.write_text(txt, encoding="utf-8")


def update_search_index(meta: dict):
    """Actualiza el archivo search-index.json."""
    entry = {
        "title": meta["title"],
        "url": f"/{meta['slug']}/",
        "description": meta.get("description", ""),
        "category": meta.get("category", "Blog")
    }

    for si_path in [DIST_DIR / "search-index.json", ROOT / "search-index.json"]:
        if si_path.exists():
            try:
                idx = json.loads(si_path.read_text(encoding="utf-8"))
                if not any(item.get("url") == entry["url"] for item in idx):
                    idx.append(entry)
                    si_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception as e:
                print(f"[WARN] No se pudo actualizar {si_path.name}: {e}")


def add_to_social_queue(meta: dict, image_url: str):
    """Añade la entrada a scripts/linkedin_queue.json."""
    if not QUEUE_FILE.exists():
        return

    try:
        queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        slug = meta["slug"]

        # Si ya existe, no duplicar
        if any(item.get("slug") == slug for item in queue):
            return

        new_item = {
            "type": "article",
            "slug": slug,
            "title": meta["title"],
            "description": meta.get("description", ""),
            "image": f"https://nubeparapymes.online{image_url}",
            "key_points": meta.get("key_points", []),
            "category": meta.get("category_slug", "default"),
            "url": f"https://nubeparapymes.online/{slug}/",
            "published": False,
            "published_at": None,
            "post_id": None,
            "pinterest_published": False,
            "pinterest_published_at": None,
            "pinterest_pin_id": None
        }

        # Insertar al inicio de los pendientes para priorizar el nuevo artículo
        insert_idx = 0
        for i, item in enumerate(queue):
            if not item.get("published"):
                insert_idx = i
                break

        queue.insert(insert_idx, new_item)
        QUEUE_FILE.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  • Añadido a la cola social (LinkedIn y Pinterest) en posición #{insert_idx + 1}")
    except Exception as e:
        print(f"[WARN] No se pudo añadir a la cola social: {e}")


def main():
    parser = argparse.ArgumentParser(description="Compilador Autónomo SEO + GEO para Nube para Pymes")
    parser.add_argument("--publicar-siguiente", action="store_true", help="Publica el primer borrador disponible en borradores/")
    parser.add_argument("--archivo", type=str, help="Ruta de un borrador específico a publicar")
    parser.add_argument("--listar", action="store_true", help="Muestra los borradores pendientes")
    args = parser.parse_args()

    BORRADORES_DIR.mkdir(parents=True, exist_ok=True)
    drafts = sorted([f for f in BORRADORES_DIR.glob("*.md") if f.is_file()])

    if args.listar:
        print("\n=======================================================")
        print(f" BORRADORES PENDIENTES ({len(drafts)})")
        print("=======================================================")
        for i, d in enumerate(drafts, 1):
            print(f" {i}. {d.name}")
        print()
        return

    target_draft = None
    if args.archivo:
        p = Path(args.archivo)
        if p.exists():
            target_draft = p
        else:
            print(f"[ERROR] No existe el archivo: {args.archivo}")
            sys.exit(1)
    elif args.publicar_siguiente or len(drafts) > 0:
        target_draft = drafts[0]

    if not target_draft:
        print("[INFO] No hay borradores pendientes en la carpeta borradores/.")
        sys.exit(0)

    publish_draft(target_draft)


if __name__ == "__main__":
    main()
