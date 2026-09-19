#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Contenidos y Publicación Automatizada en LinkedIn: Nube para Pymes
Desarrollado para: Xavier Cabello / Nube para Pymes

Publica de forma automatizada e intercalada:
1. Artículos editoriales de análisis y comparativas de software (de nubepymesexport/)
2. Posts dedicados a las 26 herramientas interactivas gratuitas con sus guías y casos de uso

Soporta:
- Publicación en Página de Empresa (Organization Page: urn:li:organization:XXXX)
- Publicación en Perfil Personal (Person Feed: urn:li:person:XXXX)
- Subida real de mínimo 3 imágenes en alta resolución por post (WebP convertido a JPEG/PNG)
- Resumen automático con enlaces directos para GitHub Actions

Utiliza la API oficial de LinkedIn v2 (assets + ugcPosts).
"""

from __future__ import annotations

import argparse
import html
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = ImageDraw = ImageFont = None

# Configurar salida UTF-8 para evitar errores de codificación con emojis en Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
WP_EXPORT = ROOT / "nubepymesexport"
UPLOADS_DIR = WP_EXPORT / "wp-content" / "uploads" / "2026" / "07"
ASSETS_DIR = ROOT / "assets"
QUEUE_FILE = ROOT / "scripts" / "linkedin_queue.json"

# Mapeo de categorías temáticas a hashtags estratégicos para LinkedIn
CATEGORY_HASHTAGS = {
    "crm": "#CRM #VentasB2B #AutomatizacionComercial #Pymes #GestionClientes",
    "contabilidad": "#ContabilidadPyme #FinanzasEmpresariales #FacturacionElectronica #Negocios #GestionPyme",
    "facturacion": "#Facturacion #GestionFinanciera #Pymes #Finanzas #Productividad",
    "proyectos": "#GestionDeProyectos #ProductividadLaboral #TrabajoRemoto #Liderazgo #MetodologiasAgiles",
    "ia": "#InteligenciaArtificial #Automatizacion #IAparaPymes #TransformacionDigital #Innovacion",
    "herramientas": "#SoftwareEmpresarial #HerramientasDigitales #Productividad #Pymes #Tecnologia",
    "marketing": "#MarketingDigital #EstrategiaComercial #VentasB2B #Pymes #Adquisicion",
    "finanzas": "#FinanzasPyme #FlujoDeCaja #Rentabilidad #GestionFinanciera #Negocios",
    "ventas": "#VentasB2B #CierreDeVentas #GestionComercial #Pymes #Negocios",
    "legal": "#LegalPyme #Contratos #BlindajeEmpresarial #Emprendimiento #Pymes",
    "operaciones": "#OperacionesPyme #Logistica #Inventario #ControlDeStock #Productividad",
    "productividad": "#ProductividadLaboral #Eficiencia #HerramientasPyme #TrabajoRemoto #Gestion",
    "default": "#Pymes #SoftwareEmpresarial #Productividad #Emprendimiento #GestionDeNegocios",
}

# Ganchos persuasivos para artículos de blog
HOOK_TEMPLATES_ARTICLE = [
    "🚨 ¿Tu empresa sigue perdiendo horas valiosas en tareas que hoy deberían estar 100% automatizadas?",
    "💡 Una de las decisiones más costosas para una pequeña empresa es elegir el software equivocado. Aquí te explico por qué:",
    "📊 Si estás evaluando herramientas para optimizar la gestión de tu negocio, este análisis te ahorrará semanas de pruebas y errores:",
    "⚡ Menos caos operativo y más rentabilidad: ese es el verdadero objetivo de digitalizar los procesos en una Pyme.",
    "🎯 ¿Excel o software especializado? Este es el criterio técnico y financiero que todo dueño de negocio debería considerar:",
]

# Ganchos persuasivos para herramientas interactivas
HOOK_TEMPLATES_TOOL = [
    "🛠️ Muchas pequeñas empresas pagan cientos de dólares al mes por herramientas que podrían resolver gratis. Te comparto esta solución:",
    "⚡ ¿Sabías que el 80% de los retrasos operativos en una Pyme se deben a la falta de herramientas especializadas simples? Aquí tienes una lista para usar:",
    "📊 Menos hojas de cálculo desordenadas y más control de tu negocio: esta herramienta gratuita te ayuda a optimizar ese proceso en minutos:",
    "💡 Diseñé esta herramienta pensando específicamente en resolver un dolor de cabeza recurrente para dueños de pequeños negocios:",
    "🎯 Sin registros engorrosos, sin suscripciones mensuales y con total privacidad: te comparto esta herramienta para tu día a día empresarial:",
]


def clean_text(raw_html: str) -> str:
    """Limpia etiquetas HTML, decodifica entidades y normaliza espacios."""
    if not raw_html:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw_html)
    text = html.unescape(text)
    return " ".join(text.split()).strip()


def wrap_text(text: str, max_chars: int = 42) -> list[str]:
    """Divide un texto en líneas para diseño visual de imágenes."""
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


def extract_articles() -> list[dict]:
    """Escanea la carpeta nubepymesexport/ y extrae todos los artículos editoriales."""
    articles = []
    if not WP_EXPORT.exists():
        print(f"[ERROR] No se encontró el directorio {WP_EXPORT}")
        return articles

    excluded_slugs = {
        "author", "category", "tag", "directorio-herramientas", "contacto",
        "sobre-nosotros", "aviso-legal", "politica-de-privacidad", "politica-de-cookies",
        "descargo-de-responsabilidad", "terminos-y-condiciones", "metodologia-de-resenas",
        "blog"
    }

    for item in sorted(WP_EXPORT.iterdir()):
        if not item.is_dir():
            continue
        index_file = item / "index.html"
        if not index_file.exists():
            continue

        try:
            content = index_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if "<article" not in content or "entry-title" not in content:
            continue
        if item.name in excluded_slugs:
            continue

        # 1. Título
        title_m = re.search(r'<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>(.*?)</h1>', content)
        title = clean_text(title_m.group(1)) if title_m else clean_text(item.name.replace("-", " ").title())

        # 2. Meta descripción
        desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
        desc = clean_text(desc_m.group(1)) if desc_m else ""

        # 3. Puntos clave
        headings = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', content)
        key_points = []
        for h in headings:
            cleaned_h = clean_text(h)
            if cleaned_h and len(cleaned_h) > 10 and not any(skip in cleaned_h.lower() for skip in ["conclusión", "preguntas frecuentes", "deja un comentario", "artículos relacionados"]):
                key_points.append(cleaned_h)
            if len(key_points) >= 3:
                break

        # 4. Categoría
        cat_key = "default"
        slug_lower = item.name.lower()
        if "crm" in slug_lower:
            cat_key = "crm"
        elif "contab" in slug_lower or "gasto" in slug_lower or "precio" in slug_lower or "quickbooks" in slug_lower:
            cat_key = "contabilidad"
        elif "factur" in slug_lower:
            cat_key = "facturacion"
        elif "proyecto" in slug_lower or "tarea" in slug_lower or "asana" in slug_lower or "trello" in slug_lower or "monday" in slug_lower or "notion" in slug_lower:
            cat_key = "proyectos"
        elif "ia" in slug_lower or "automatiz" in slug_lower or "chatgpt" in slug_lower or "chatbot" in slug_lower:
            cat_key = "ia"

        articles.append({
            "type": "article",
            "slug": item.name,
            "title": title,
            "description": desc,
            "key_points": key_points,
            "category": cat_key,
            "url": f"https://nubeparapymes.online/{item.name}/",
            "published": False,
            "published_at": None,
            "post_id": None,
        })

    return articles


def extract_tools() -> list[dict]:
    """Extrae las 26 herramientas interactivas del catálogo con sus guías y especificaciones."""
    try:
        scripts_dir = str(ROOT / "scripts")
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        from generar_catalogo_herramientas import TOOLS_DATA
    except Exception as e:
        print(f"[WARN] No se pudo importar TOOLS_DATA de generar_catalogo_herramientas.py ({e})")
        return []

    tools = []
    for i, t in enumerate(TOOLS_DATA, 1):
        tools.append({
            "type": "tool",
            "slug": f"tool-{t['slug']}",
            "tool_slug": t["slug"],
            "tool_number": i,
            "name": t["name"],
            "title": f"Herramienta #{i:02d}: {t['name']}",
            "description": f"{t['benefit']} {t['problem']}",
            "icon": t.get("icon", "🛠️"),
            "category": t.get("cat", "default"),
            "cat_name": t.get("cat_name", ""),
            "color": t.get("color", "#38BDF8"),
            "problem": t.get("problem", ""),
            "benefit": t.get("benefit", ""),
            "features": t.get("features", []),
            "url": f"https://nubeparapymes.online/herramientas/{t['cat']}/{t['slug']}/",
            "published": False,
            "published_at": None,
            "post_id": None,
        })
    return tools


def build_interleaved_queue(articles: list[dict], tools: list[dict], existing_queue: list[dict] | None = None) -> list[dict]:
    """Intercala artículos y herramientas (2 artículos por cada 1 herramienta) preservando el historial."""
    history_map = {}
    if existing_queue:
        for item in existing_queue:
            history_map[item["slug"]] = {
                "published": item.get("published", False),
                "published_at": item.get("published_at"),
                "post_id": item.get("post_id"),
            }

    for art in articles:
        art["type"] = "article"
        if art["slug"] in history_map:
            art.update(history_map[art["slug"]])
        else:
            art["published"] = False
            art["published_at"] = None
            art["post_id"] = None

    for tool in tools:
        tool["type"] = "tool"
        if tool["slug"] in history_map:
            tool.update(history_map[tool["slug"]])
        else:
            tool["published"] = False
            tool["published_at"] = None
            tool["post_id"] = None

    combined = []
    art_idx = 0
    tool_idx = 0
    total_art = len(articles)
    total_tools = len(tools)

    while art_idx < total_art or tool_idx < total_tools:
        for _ in range(2):
            if art_idx < total_art:
                combined.append(articles[art_idx])
                art_idx += 1
        if tool_idx < total_tools:
            combined.append(tools[tool_idx])
            tool_idx += 1

    return combined


def init_or_load_queue(force_refresh: bool = False) -> list[dict]:
    """Carga la cola de publicación desde el archivo JSON si existe, o la inicializa."""
    if not force_refresh and QUEUE_FILE.exists():
        try:
            raw_queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
            if raw_queue and len(raw_queue) > 0:
                has_tools = any(item.get("type") == "tool" or item.get("slug", "").startswith("tool-") for item in raw_queue)
                if has_tools:
                    return raw_queue
        except Exception as e:
            print(f"[WARN] Error leyendo cola existente ({e}); procediendo a sincronizar.")

    all_articles = extract_articles()
    all_tools = extract_tools()
    raw_queue = []
    if QUEUE_FILE.exists():
        try:
            raw_queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        except Exception:
            raw_queue = []

    combined = build_interleaved_queue(all_articles, all_tools, raw_queue)
    save_queue(combined)
    return combined

    queue = build_interleaved_queue(all_articles, all_tools)
    save_queue(queue)
    return queue


def save_queue(queue: list[dict]) -> None:
    """Guarda el estado de la cola en el archivo JSON."""
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")


def get_article_images(slug: str) -> list[bytes]:
    """Extrae mínimo 3 imágenes reales del artículo en local y las convierte a JPEG."""
    images_bytes = []
    html_file = WP_EXPORT / slug / "index.html"

    if html_file.exists():
        content = html_file.read_text(encoding="utf-8", errors="ignore")
        img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
        seen_filenames = set()

        for src in img_srcs:
            filename = Path(src).name
            if filename in seen_filenames:
                continue
            if any(skip in filename.lower() for skip in ["logo", "avatar", "icon", "header-200x67"]):
                continue

            local_path = UPLOADS_DIR / filename
            if local_path.exists() and Image is not None:
                try:
                    with Image.open(local_path) as im:
                        buf = io.BytesIO()
                        im.convert("RGB").save(buf, format="JPEG", quality=88)
                        images_bytes.append(buf.getvalue())
                        seen_filenames.add(filename)
                except Exception as e:
                    print(f"[WARN] No se pudo convertir {filename}: {e}")

            if len(images_bytes) >= 3:
                break

    # Si hay menos de 3 imágenes, complementar con imágenes de marca o infografías
    fallback_paths = [
        ASSETS_DIR / "linkedin-banner-1584x396.jpg",
        ASSETS_DIR / "logo-nube-para-pymes.png",
        ASSETS_DIR / "pinterest" / "pinterest-pin-10-herramientas-gratuitas.png",
        ASSETS_DIR / "pinterest" / "pinterest-pin-09-visibilidad-ia.png"
    ]
    for fb in fallback_paths:
        if len(images_bytes) >= 3:
            break
        if fb.exists() and Image is not None:
            try:
                with Image.open(fb) as im:
                    buf = io.BytesIO()
                    im.convert("RGB").save(buf, format="JPEG", quality=88)
                    images_bytes.append(buf.getvalue())
            except Exception as e:
                print(f"[WARN] Error con fallback {fb.name}: {e}")

    return images_bytes


def generate_tool_images(tool: dict) -> list[bytes]:
    """Genera 3 tarjetas visuales (1080x1080 px) de alta resolución para la herramienta."""
    if Image is None or ImageDraw is None:
        return []

    W, H = 1080, 1080
    cards_bytes = []

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_subtitle = ImageFont.truetype("arialbd.ttf", 30)
        font_body = ImageFont.truetype("arial.ttf", 26)
        font_small = ImageFont.truetype("arial.ttf", 20)
    except Exception:
        font_title = font_subtitle = font_body = font_small = ImageFont.load_default()

    category_name = tool.get("cat_name") or tool.get("category", "Herramienta").upper()
    tool_name = tool.get("name", "Herramienta")
    problem = tool.get("problem", "")
    benefit = tool.get("benefit", "")
    features = tool.get("features", [])
    url = tool.get("url", "https://nubeparapymes.online/herramientas/")

    def draw_base_card():
        im = Image.new("RGB", (W, H), (15, 23, 42))
        draw = ImageDraw.Draw(im)
        for y in range(H):
            ratio = y / H
            r = int(15 + ratio * (24 - 15))
            g = int(23 + ratio * (35 - 23))
            b = int(42 + ratio * (68 - 42))
            draw.line([(0, y), (W, y)], fill=(r, g, b))
        draw.rectangle([(0, 0), (W, 14)], fill=(56, 189, 248))
        draw.rounded_rectangle([(70, 60), (530, 115)], radius=12, fill=(30, 41, 59), outline=(56, 189, 248), width=2)
        draw.text((90, 75), f"NUBE PARA PYMES · {category_name}", fill=(56, 189, 248), font=font_subtitle)
        draw.text((70, 150), tool_name, fill=(255, 255, 255), font=font_title)
        draw.rounded_rectangle([(70, 235), (W - 70, 890)], radius=22, fill=(24, 33, 54), outline=(51, 65, 85), width=2)
        draw.text((70, 970), "Desarrollado por Xavier Cabello · Nube para Pymes", fill=(148, 163, 184), font=font_small)
        draw.text((W - 320, 970), "nubeparapymes.online", fill=(56, 189, 248), font=font_small)
        return im, draw

    # CARD 1: Problema común vs Solución
    im1, draw1 = draw_base_card()
    draw1.text((110, 280), "🚨 EL PROBLEMA COMÚN EN LAS PYMES:", fill=(248, 113, 113), font=font_subtitle)
    y_cursor = 340
    for line in wrap_text(problem, max_chars=40):
        draw1.text((110, y_cursor), line, fill=(226, 232, 240), font=font_body)
        y_cursor += 38
    y_cursor = max(y_cursor + 40, 520)
    draw1.text((110, y_cursor), "💡 CÓMO TE AYUDA ESTA HERRAMIENTA:", fill=(56, 189, 248), font=font_subtitle)
    y_cursor += 50
    for line in wrap_text(benefit, max_chars=40):
        draw1.text((110, y_cursor), line, fill=(203, 213, 225), font=font_body)
        y_cursor += 38
    b1 = io.BytesIO()
    im1.save(b1, format="JPEG", quality=90)
    cards_bytes.append(b1.getvalue())

    # CARD 2: 3 Capacidades destacadas
    im2, draw2 = draw_base_card()
    draw2.text((110, 280), "✨ 3 CAPACIDADES DESTACADAS:", fill=(52, 211, 153), font=font_subtitle)
    y_cursor = 360
    for i, feat in enumerate(features[:3], 1):
        draw2.text((110, y_cursor), f"{i}. {feat}", fill=(255, 255, 255), font=font_subtitle)
        y_cursor += 120
    b2 = io.BytesIO()
    im2.save(b2, format="JPEG", quality=90)
    cards_bytes.append(b2.getvalue())

    # CARD 3: Privacidad y CTA
    im3, draw3 = draw_base_card()
    draw3.text((110, 280), "🔒 BENEFICIOS DE ACCESO Y PRIVACIDAD:", fill=(56, 189, 248), font=font_subtitle)
    draw3.text((110, 360), "✓ 100% Gratuita para siempre", fill=(255, 255, 255), font=font_body)
    draw3.text((110, 420), "✓ Sin necesidad de crear cuenta ni registro", fill=(255, 255, 255), font=font_body)
    draw3.text((110, 480), "✓ Tus datos nunca salen de tu computadora", fill=(255, 255, 255), font=font_body)
    draw3.text((110, 540), "✓ Funciona directamente en tu navegador (PC y móvil)", fill=(255, 255, 255), font=font_body)
    draw3.rounded_rectangle([(110, 640), (W - 110, 780)], radius=16, fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    draw3.text((140, 665), "PRUÉBALA O COMPÁRTELA CON TU EQUIPO EN:", fill=(148, 163, 184), font=font_small)
    draw3.text((140, 705), url, fill=(56, 189, 248), font=font_subtitle)
    b3 = io.BytesIO()
    im3.save(b3, format="JPEG", quality=90)
    cards_bytes.append(b3.getvalue())

    return cards_bytes


def get_item_images(item: dict) -> list[bytes]:
    """Obtiene las imágenes para cualquier ítem (mínimo 3 imágenes)."""
    if item.get("type") == "tool":
        return generate_tool_images(item)
    return get_article_images(item["slug"])


def generate_article_post(article: dict, hook_index: int = 0) -> str:
    """Genera el texto de publicación para un artículo editorial."""
    hook = HOOK_TEMPLATES_ARTICLE[hook_index % len(HOOK_TEMPLATES_ARTICLE)]
    hashtags = CATEGORY_HASHTAGS.get(article.get("category", "default"), CATEGORY_HASHTAGS["default"])

    points_text = ""
    if article.get("key_points"):
        points_text = "📌 Criterios y aprendizajes clave analizados en este reporte:\n"
        for i, pt in enumerate(article["key_points"][:3], 1):
            points_text += f"  {i}. {pt}\n"
        points_text += "\n"

    post = f"""{hook}

📖 «{article['title']}»

{article['description']}

{points_text}👇 Lee el análisis técnico completo con tablas comparativas y recomendaciones:
🔗 {article['url']}

──────────
👨‍💻 Publicado por Xavier Cabello · Nube para Pymes
Herramientas gratuitas y análisis de software independiente para pequeñas empresas.

{hashtags} #XavierCabello #NubeParaPymes"""

    return post.strip()


def generate_tool_post(tool: dict, hook_index: int = 0) -> str:
    """Genera el texto de publicación para una herramienta interactiva."""
    hook = HOOK_TEMPLATES_TOOL[hook_index % len(HOOK_TEMPLATES_TOOL)]
    hashtags = CATEGORY_HASHTAGS.get(tool.get("category", "default"), CATEGORY_HASHTAGS["default"])
    tool_hashtags = f"{hashtags} #HerramientasGratis #SoftwarePyme #Productividad"

    num = tool.get("tool_number", "")
    num_str = f" #{num:02d} DE 26" if num else ""

    features_lines = ""
    for i, feat in enumerate(tool.get("features", []), 1):
        features_lines += f"  {i}. {feat}\n"

    post = f"""{hook}

🛠️ [HERRAMIENTA GRATUITA{num_str} PARA TU NEGOCIO]
{tool.get('icon', '⚡')} {tool['name']}

🚨 El problema común en las pequeñas empresas:
{tool.get('problem', '')}

💡 Cómo te ayuda a resolverlo:
{tool.get('benefit', '')}

✨ 3 Capacidades clave:
{features_lines}
🔒 100% gratuita, privada (los datos se procesan en tu navegador sin subirse a ningún servidor externo) y sin necesidad de registro ni tarjeta.

👇 Pruébala o compártela con tu equipo directamente aquí:
🔗 {tool['url']}

──────────
👨‍💻 Desarrollada por Xavier Cabello · Nube para Pymes
Software y herramientas independientes diseñadas para el día a día de las pequeñas empresas.

{tool_hashtags} #XavierCabello #NubeParaPymes"""

    return post.strip()


def generate_linkedin_post(item: dict, hook_index: int = 0) -> str:
    """Genera el texto del post despachando según el tipo de contenido."""
    if item.get("type") == "tool":
        return generate_tool_post(item, hook_index)
    return generate_article_post(item, hook_index)


OFFICIAL_ORGANIZATION_URN = "urn:li:organization:145201650"


def get_author_urn() -> tuple[str, str]:
    """
    Determina el URN del autor y el modo (Página de Empresa o Perfil Personal).
    Por defecto publica siempre en la Página de Empresa oficial de Nube para Pymes (145201650).
    """
    # 1. Verificar si se especificó un URN de Organización explícito en variables de entorno
    org_urn = os.environ.get("LINKEDIN_ORGANIZATION_URN") or os.environ.get("LINKEDIN_PAGE_URN")
    if org_urn:
        clean = org_urn.strip().strip('"').strip("'")
        if not clean.startswith("urn:li:organization:"):
            clean = f"urn:li:organization:{clean}"
        return clean, f"PÁGINA DE EMPRESA ({clean})"

    # 2. Verificar si se forzó explícitamente un URN de destino diferente
    target_urn = os.environ.get("LINKEDIN_TARGET_URN")
    if target_urn:
        clean = target_urn.strip().strip('"').strip("'")
        if clean.startswith("urn:li:organization:") or clean.isdigit():
            if not clean.startswith("urn:li:organization:"):
                clean = f"urn:li:organization:{clean}"
            return clean, f"PÁGINA DE EMPRESA ({clean})"
        if clean.startswith("urn:li:person:"):
            return clean, f"PERFIL PERSONAL ({clean})"

    # 3. Solo si se activa explícitamente LINKEDIN_FORCE_PERSON se permite perfil personal
    force_person = os.environ.get("LINKEDIN_FORCE_PERSON", "false").lower() in ("true", "1", "yes")
    person_urn = os.environ.get("LINKEDIN_PERSON_URN")
    if force_person and person_urn:
        clean = person_urn.strip().strip('"').strip("'")
        if not clean.startswith("urn:li:person:"):
            clean = f"urn:li:person:{clean}"
        return clean, f"PERFIL PERSONAL ({clean})"

    # 4. Predeterminado Oficial de la marca: Página de Empresa de Nube para Pymes
    return OFFICIAL_ORGANIZATION_URN, f"PÁGINA DE EMPRESA OFICIAL (Nube para Pymes - {OFFICIAL_ORGANIZATION_URN})"


def upload_single_image(image_bytes: bytes, author_urn: str, access_token: str) -> tuple[str, str]:
    """
    Sube una imagen binaria a LinkedIn.
    Intenta primero la API moderna (/rest/images?action=initializeUpload),
    y si no está habilitada en la app, usa el fallback (/v2/assets?action=registerUpload).
    Retorna (asset_urn, api_type).
    """
    # 1. Intentar API moderna de imágenes (/rest/images)
    try:
        init_url = "https://api.linkedin.com/rest/images?action=initializeUpload"
        init_payload = {
            "initializeUploadRequest": {
                "owner": author_urn
            }
        }
        init_req = urllib.request.Request(
            init_url,
            data=json.dumps(init_payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "LinkedIn-Version": "202401",
                "X-Restli-Protocol-Version": "2.0.0",
            },
            method="POST"
        )
        with urllib.request.urlopen(init_req, timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            upload_url = data["value"]["uploadUrl"]
            image_urn = data["value"]["image"]

        # Subida binaria del archivo mediante PUT:
        # CRÍTICO: upload_url es una URL pre-firmada de LinkedIn/S3.
        # NO DEBE llevar cabecera 'Authorization' (incluirla provoca error 403 Forbidden).
        put_req = urllib.request.Request(
            upload_url,
            data=image_bytes,
            headers={
                "Content-Type": "image/jpeg",
            },
            method="PUT"
        )
        with urllib.request.urlopen(put_req, timeout=45):
            pass

        return image_urn, "rest"

    except Exception as e_rest:
        print(f"    [INFO] Intento inicial con /rest/images: {e_rest}. Evaluando fallback con /v2/assets...")

    # 2. Fallback a API v2 (/v2/assets)
    register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    v2_payload = {
        "registerUploadRequest": {
            "recipes": [
                "urn:li:digitalmediaRecipe:feedshare-image"
            ],
            "owner": author_urn,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }
    v2_req = urllib.request.Request(
        register_url,
        data=json.dumps(v2_payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method="POST"
    )
    with urllib.request.urlopen(v2_req, timeout=25) as resp:
        res_json = json.loads(resp.read().decode("utf-8"))
        asset_urn = res_json["value"]["asset"]
        upload_url = res_json["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]

    # Subida binaria PUT a la URL pre-firmada (SIN Authorization)
    put_req = urllib.request.Request(
        upload_url,
        data=image_bytes,
        headers={
            "Content-Type": "image/jpeg",
        },
        method="PUT"
    )
    with urllib.request.urlopen(put_req, timeout=45):
        pass

    return asset_urn, "v2"


def publish_to_linkedin(post_text: str, target_url: str, post_title: str, image_bytes_list: list[bytes]) -> tuple[dict, int]:
    """Publica un post con galería visual de imágenes en LinkedIn (mínimo 3 imágenes obligatorias)."""
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("Falta la variable de entorno LINKEDIN_ACCESS_TOKEN en GitHub Secrets.")

    author_urn, mode_label = get_author_urn()
    print(f"[DESTINO DE PUBLICACIÓN] {mode_label} ({author_urn})")

    # Validación estricta: mínimo 3 imágenes requeridas
    if not image_bytes_list or len(image_bytes_list) < 3:
        raise ValueError(
            f"El post exige un mínimo estricto de 3 imágenes, pero solo se suministraron {len(image_bytes_list) if image_bytes_list else 0}."
        )

    print(f"[SUBIENDO IMÁGENES] Subiendo {len(image_bytes_list)} imágenes para el post...")
    uploaded_assets = []
    api_types = []

    for idx, img_bytes in enumerate(image_bytes_list, 1):
        try:
            asset_urn, api_type = upload_single_image(img_bytes, author_urn, access_token)
            uploaded_assets.append(asset_urn)
            api_types.append(api_type)
            print(f"  ✓ Imagen {idx}/{len(image_bytes_list)} subida [{api_type.upper()}]: {asset_urn}")
        except Exception as e:
            print(f"  ✗ ERROR crítico al subir la imagen {idx}/{len(image_bytes_list)}: {e}")
            raise RuntimeError(
                f"Falló la subida de la imagen #{idx} ({e}). "
                f"Se detiene la publicación para no emitir un post degradado sin imágenes."
            ) from e

    if len(uploaded_assets) < 3:
        raise RuntimeError(
            f"Se requieren mínimo 3 imágenes por post y solo se cargaron {len(uploaded_assets)}. "
            f"Se cancela la publicación para proteger la identidad de marca."
        )

    # 1. Si los assets son de la API moderna (urn:li:image:...), publicar con /rest/posts (MultiImage)
    if any(a.startswith("urn:li:image:") for a in uploaded_assets):
        print(f"[PUBLICANDO] Enviando post MultiImage ({len(uploaded_assets)} fotos) mediante /rest/posts...")
        rest_posts_url = "https://api.linkedin.com/rest/posts"
        post_payload = {
            "author": author_urn,
            "commentary": post_text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "content": {
                "multiImage": {
                    "images": [
                        {
                            "id": asset,
                            "altText": f"{post_title[:80]} - Imagen {i}"
                        }
                        for i, asset in enumerate(uploaded_assets, 1)
                    ]
                }
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }
        req = urllib.request.Request(
            rest_posts_url,
            data=json.dumps(post_payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "LinkedIn-Version": "202401",
                "X-Restli-Protocol-Version": "2.0.0",
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                post_id = resp.headers.get("x-restli-id") or "OK"
                return {"id": post_id, "status": resp.status}, len(uploaded_assets)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            print(f"[WARN] Error en /rest/posts ({e.code}: {err_body}). Intentando fallback con /v2/ugcPosts...")

    # 2. Fallback a /v2/ugcPosts
    print(f"[PUBLICANDO] Enviando post ({len(uploaded_assets)} fotos) mediante /v2/ugcPosts...")
    ugc_url = "https://api.linkedin.com/v2/ugcPosts"
    media_items = [
        {
            "status": "READY",
            "media": asset,
            "title": {"text": f"{post_title[:80]} - Foto {i}"}
        }
        for i, asset in enumerate(uploaded_assets, 1)
    ]
    ugc_payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "IMAGE",
                "media": media_items
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    req = urllib.request.Request(
        ugc_url,
        data=json.dumps(ugc_payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_body = resp.read().decode("utf-8")
            res_dict = json.loads(resp_body) if resp_body else {"status": resp.status}
            return res_dict, len(uploaded_assets)
    except urllib.error.HTTPError as e:
        error_content = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Error {e.code} desde la API de LinkedIn: {error_content}") from e


def main():
    parser = argparse.ArgumentParser(description="Motor de contenidos y publicación en LinkedIn para Nube para Pymes.")
    parser.add_argument("--dry-run", action="store_true", help="Muestra el próximo post sin publicarlo.")
    parser.add_argument("--publish", action="store_true", help="Publica el próximo post a la API oficial de LinkedIn.")
    parser.add_argument("--list", action="store_true", help="Lista el estado de todos los artículos y herramientas en la cola.")
    parser.add_argument("--reset-queue", action="store_true", help="Reinicia el estado de la cola para volver a empezar.")
    args = parser.parse_args()

    queue = init_or_load_queue()

    if args.reset_queue:
        for item in queue:
            item["published"] = False
            item["published_at"] = None
            item["post_id"] = None
        save_queue(queue)
        print(f"[OK] Cola reiniciada. {len(queue)} publicaciones listas para un nuevo ciclo.")
        return

    if args.list:
        published_count = sum(1 for item in queue if item.get("published"))
        tools_published = sum(1 for item in queue if item.get("published") and item.get("type") == "tool")
        articles_published = published_count - tools_published
        total_tools = sum(1 for item in queue if item.get("type") == "tool")
        total_articles = len(queue) - total_tools

        print(f"\n=========================================================================")
        print(f"📊 ESTADO DE LA COLA DE LINKEDIN ({published_count}/{len(queue)} PUBLICADOS)")
        print(f"   • Artículos editoriales: {articles_published}/{total_articles} publicados")
        print(f"   • Herramientas interactivas: {tools_published}/{total_tools} publicadas")
        print(f"=========================================================================\n")

        for i, item in enumerate(queue, 1):
            is_tool = item.get("type") == "tool"
            badge = "🛠️ [HERRAMIENTA]" if is_tool else "📖 [ARTÍCULO]   "
            if item.get("published"):
                status_icon = "✅ Publicado"
                post_id = item.get("post_id", "")
                link_info = f" -> https://www.linkedin.com/feed/update/{post_id}/" if post_id else ""
            else:
                status_icon = "⏳ Pendiente"
                link_info = ""

            title = item.get("title") or item.get("name", "")
            print(f"{i:02d}. {badge} [{status_icon}] {title[:60]}{link_info}")
        return

    # Buscar el próximo elemento no publicado
    next_item = None
    next_index = 0
    for idx, item in enumerate(queue):
        if not item.get("published"):
            next_item = item
            next_index = idx
            break

    if not next_item:
        print(f"[INFO] ¡Se completaron las {len(queue)} publicaciones del ciclo! Reiniciando automáticamente...")
        for item in queue:
            item["published"] = False
            item["published_at"] = None
            item["post_id"] = None
        save_queue(queue)
        next_item = queue[0]
        next_index = 0

    is_tool = next_item.get("type") == "tool"
    type_label = "Herramienta Interactiva" if is_tool else "Artículo Editorial"
    post_content = generate_linkedin_post(next_item, hook_index=next_index)
    item_images = get_item_images(next_item)

    if args.publish:
        print(f"[PUBLICANDO EN LINKEDIN] #{next_index + 1} ({type_label}): «{next_item['title']}»...")
        try:
            resp, count_images = publish_to_linkedin(post_content, next_item["url"], next_item["title"], item_images)
            post_id = resp.get("id", "OK")
            next_item["published"] = True
            next_item["published_at"] = datetime.now(timezone.utc).isoformat()
            next_item["post_id"] = post_id
            save_queue(queue)

            post_url = f"https://www.linkedin.com/feed/update/{post_id}/"
            print(f"\n[ÉXITO] Post publicado correctamente en LinkedIn.")
            print(f"  • ID: {post_id}")
            print(f"  • Tipo: {type_label}")
            print(f"  • Imágenes incluidas: {count_images}")
            print(f"  • URL Directa al Post: {post_url}\n")

            # Escribir en GitHub Step Summary si se ejecuta en GitHub Actions
            step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
            if step_summary:
                try:
                    with open(step_summary, "a", encoding="utf-8") as f:
                        f.write(f"## 🚀 ¡Post Publicado con Éxito en LinkedIn!\n\n")
                        f.write(f"- **Contenido:** {next_item['title']}\n")
                        f.write(f"- **Tipo:** {'🛠️ Herramienta Interactiva' if is_tool else '📖 Artículo de Blog'}\n")
                        f.write(f"- **Imágenes incluidas:** {count_images} imágenes en galería\n")
                        f.write(f"- **Enlace en tu web:** {next_item['url']}\n")
                        f.write(f"- **👉 Ver publicación en LinkedIn:** [{post_url}]({post_url})\n\n")
                        f.write(f"<details><summary><b>Ver texto completo del post publicado</b></summary>\n\n```text\n{post_content}\n```\n</details>\n")
                except Exception as ex:
                    print(f"[WARN] No se pudo escribir en GITHUB_STEP_SUMMARY: {ex}")

        except Exception as e:
            print(f"[ERROR CRÍTICO] Falló la publicación: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"\n=======================================================")
        print(f" [VISTA PREVIA - DRY RUN] #{next_index + 1} de {len(queue)} ({type_label})")
        print(f"=======================================================\n")
        print(post_content)
        print(f"\n=======================================================")
        print(f"URL de destino: {next_item['url']}")
        print(f"Imágenes preparadas para el post: {len(item_images)} imágenes")
        print(f"Para publicar realmente en LinkedIn ejecuta con: --publish")
        print(f"=======================================================\n")


if __name__ == "__main__":
    main()
