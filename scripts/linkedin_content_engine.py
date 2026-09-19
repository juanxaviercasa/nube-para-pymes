#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Contenidos y Publicación Automatizada en LinkedIn: Nube para Pymes
Desarrollado para: Xavier Cabello / Nube para Pymes

Publica de forma automatizada e intercalada:
1. Artículos editoriales de análisis y comparativas de software (de nubepymesexport/)
2. Posts dedicados a las 26 herramientas interactivas gratuitas con sus guías y casos de uso

Utiliza la API oficial de LinkedIn v2 (ugcPosts).
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Configurar salida UTF-8 para evitar errores de codificación con emojis en Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
WP_EXPORT = ROOT / "nubepymesexport"
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
    "🛠️ Muchas pequeñas empresas pagan cientos de dólares al mes por herramientas que podrían resolver gratis. Te presento esta solución:",
    "⚡ ¿Sabías que el 80% de los retrasos operativos en una Pyme se deben a la falta de herramientas especializadas simples? Aquí tienes una lista para usar:",
    "📊 Menos hojas de cálculo desordenadas y más control de tu negocio: esta herramienta gratuita te ayuda a automatizar ese proceso en minutos:",
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

        # Solo procesar entradas editoriales legítimas
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

        # 3. Imagen OpenGraph
        img_m = re.search(r'<meta\s+property="og:image"\s+content="([^"]*)"', content)
        image_url = img_m.group(1).strip() if img_m else ""
        if image_url.startswith("/"):
            image_url = f"https://nubeparapymes.online{image_url}"

        # 4. Puntos clave (extraer hasta 3 encabezados relevantes)
        headings = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', content)
        key_points = []
        for h in headings:
            cleaned_h = clean_text(h)
            if cleaned_h and len(cleaned_h) > 10 and not any(skip in cleaned_h.lower() for skip in ["conclusión", "preguntas frecuentes", "deja un comentario", "artículos relacionados"]):
                key_points.append(cleaned_h)
            if len(key_points) >= 3:
                break

        # 5. Detección de categoría para hashtags
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
            "image": image_url,
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
    """
    Intercala artículos y herramientas (2 artículos por cada 1 herramienta).
    Preserva intacto el estado de publicaciones previas si ya existen en la cola.
    """
    history_map = {}
    if existing_queue:
        for item in existing_queue:
            history_map[item["slug"]] = {
                "published": item.get("published", False),
                "published_at": item.get("published_at"),
                "post_id": item.get("post_id"),
            }

    # Aplicar estado histórico a artículos
    for art in articles:
        art["type"] = "article"
        if art["slug"] in history_map:
            art.update(history_map[art["slug"]])
        else:
            art["published"] = False
            art["published_at"] = None
            art["post_id"] = None

    # Aplicar estado histórico a herramientas
    for tool in tools:
        tool["type"] = "tool"
        if tool["slug"] in history_map:
            tool.update(history_map[tool["slug"]])
        else:
            tool["published"] = False
            tool["published_at"] = None
            tool["post_id"] = None

    # Intercalar: 2 artículos, 1 herramienta...
    combined = []
    art_idx = 0
    tool_idx = 0
    total_art = len(articles)
    total_tools = len(tools)

    while art_idx < total_art or tool_idx < total_tools:
        # Añadir 2 artículos
        for _ in range(2):
            if art_idx < total_art:
                combined.append(articles[art_idx])
                art_idx += 1
        # Añadir 1 herramienta
        if tool_idx < total_tools:
            combined.append(tools[tool_idx])
            tool_idx += 1

    return combined


def init_or_load_queue() -> list[dict]:
    """Carga la cola de publicación o la inicializa/actualiza si no incluye herramientas."""
    all_articles = extract_articles()
    all_tools = extract_tools()

    if QUEUE_FILE.exists():
        try:
            raw_queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
            has_tools = any(item.get("type") == "tool" or item.get("slug", "").startswith("tool-") for item in raw_queue)

            if not has_tools and all_tools:
                # Actualizar e intercalar herramientas preservando lo ya publicado
                print("[INFO] Actualizando cola existente para integrar las 26 herramientas interactivas...")
                combined_queue = build_interleaved_queue(all_articles, all_tools, raw_queue)
                save_queue(combined_queue)
                return combined_queue

            # Sincronizar artículos o herramientas nuevos que falten
            existing_slugs = {item["slug"] for item in raw_queue}
            needs_save = False

            for art in all_articles:
                if art["slug"] not in existing_slugs:
                    art["published"] = False
                    art["published_at"] = None
                    art["post_id"] = None
                    raw_queue.append(art)
                    existing_slugs.add(art["slug"])
                    needs_save = True

            for tool in all_tools:
                if tool["slug"] not in existing_slugs:
                    tool["published"] = False
                    tool["published_at"] = None
                    tool["post_id"] = None
                    raw_queue.append(tool)
                    existing_slugs.add(tool["slug"])
                    needs_save = True

            if needs_save:
                save_queue(raw_queue)

            return raw_queue
        except Exception as e:
            print(f"[WARN] Error leyendo cola existente ({e}); reinicializando.")

    # Inicializar nueva cola intercalada desde cero
    queue = build_interleaved_queue(all_articles, all_tools)
    save_queue(queue)
    return queue


def save_queue(queue: list[dict]) -> None:
    """Guarda el estado de la cola en el archivo JSON."""
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")


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
    """Genera el texto de publicación para una de las 26 herramientas interactivas."""
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


def publish_to_linkedin(post_text: str, target_url: str, post_title: str) -> dict:
    """Publica un post con enlace enriquecido usando la API oficial de LinkedIn v2."""
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.environ.get("LINKEDIN_PERSON_URN")

    if not access_token or not person_urn:
        raise ValueError(
            "Faltan las variables de entorno LINKEDIN_ACCESS_TOKEN o LINKEDIN_PERSON_URN. "
            "Revisa GUIA_LINKEDIN_AUTOMATIZACION.md para configurarlas en GitHub Secrets."
        )

    # Normalizar URN de autor (ej: 'urn:li:person:abcdef123')
    author = person_urn.strip()
    if not author.startswith("urn:li:person:"):
        author = f"urn:li:person:{author}"

    endpoint = "https://api.linkedin.com/v2/ugcPosts"

    payload = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "originalUrl": target_url,
                        "title": {
                            "text": post_title[:200]
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=req_data,
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
            return json.loads(resp_body) if resp_body else {"status": resp.status}
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

    # Si ya se publicaron todos los elementos, reiniciar automáticamente la rotación
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

    if args.publish:
        print(f"[PUBLICANDO EN LINKEDIN] #{next_index + 1} ({type_label}): «{next_item['title']}»...")
        try:
            resp = publish_to_linkedin(post_content, next_item["url"], next_item["title"])
            post_id = resp.get("id", "OK")
            next_item["published"] = True
            next_item["published_at"] = datetime.now(timezone.utc).isoformat()
            next_item["post_id"] = post_id
            save_queue(queue)

            post_url = f"https://www.linkedin.com/feed/update/{post_id}/"
            print(f"\n[ÉXITO] Post publicado correctamente en LinkedIn.")
            print(f"  • ID: {post_id}")
            print(f"  • Tipo: {type_label}")
            print(f"  • URL Directa al Post: {post_url}\n")

            # Escribir en GitHub Step Summary si se ejecuta en GitHub Actions
            step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
            if step_summary:
                try:
                    with open(step_summary, "a", encoding="utf-8") as f:
                        f.write(f"## 🚀 ¡Post Publicado con Éxito en LinkedIn!\n\n")
                        f.write(f"- **Contenido:** {next_item['title']}\n")
                        f.write(f"- **Tipo:** {'🛠️ Herramienta Interactiva' if is_tool else '📖 Artículo de Blog'}\n")
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
        print(f"Para publicar realmente en LinkedIn ejecuta con: --publish")
        print(f"=======================================================\n")


if __name__ == "__main__":
    main()
