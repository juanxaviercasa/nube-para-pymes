#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Contenidos y Publicación Automatizada en LinkedIn: Nube para Pymes
Desarrollado para: Xavier Cabello / Nube para Pymes
Extrae artículos editoriales de nubepymesexport/, genera publicaciones optimizadas
para el algoritmo de LinkedIn y las publica a través de la API oficial de LinkedIn v2.
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
    "default": "#Pymes #SoftwareEmpresarial #Productividad #Emprendimiento #GestionDeNegocios",
}

# Ganchos persuasivos probados para captar atención en el feed
HOOK_TEMPLATES = [
    "🚨 ¿Tu empresa sigue perdiendo horas valiosas en tareas que hoy deberían estar 100% automatizadas?",
    "💡 Una de las decisiones más costosas para una pequeña empresa es elegir el software equivocado. Aquí te explico por qué:",
    "📊 Si estás evaluando herramientas para optimizar la gestión de tu negocio, este análisis te ahorrará semanas de pruebas y errores:",
    "⚡ Menos caos operativo y más rentabilidad: ese es el verdadero objetivo de digitalizar los procesos en una Pyme.",
    "🎯 ¿Excel o software especializado? Este es el criterio técnico y financiero que todo dueño de negocio debería considerar:",
]


def clean_text(raw_html: str) -> str:
    """Limpia etiquetas HTML, decodifica entidades y normaliza espacios."""
    if not raw_html:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw_html)
    text = html.unescape(text)
    return " ".join(text.split()).strip()


def extract_articles() -> list[dict]:
    """Escanea la carpeta nubepymesexport/ y extrae todos los artículos de blog."""
    articles = []
    if not WP_EXPORT.exists():
        print(f"[ERROR] No se encontró el directorio {WP_EXPORT}")
        return articles

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

        # Solo procesar entradas editoriales legítimas (excluir páginas de sistema)
        if "<article" not in content or "entry-title" not in content:
            continue
        if item.name in {"author", "category", "tag", "directorio-herramientas", "contacto", "sobre-nosotros", "aviso-legal", "politica-de-privacidad", "politica-de-cookies", "descargo-de-responsabilidad", "terminos-y-condiciones", "metodologia-de-resenas"}:
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

        # 4. Puntos clave (extraer hasta 3 encabezados H2 o H3 relevantes)
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
            "slug": item.name,
            "title": title,
            "description": desc,
            "image": image_url,
            "key_points": key_points,
            "category": cat_key,
            "url": f"https://nubeparapymes.online/{item.name}/",
        })

    return articles


def init_or_load_queue() -> list[dict]:
    """Carga la cola de publicación o la inicializa si no existe."""
    all_articles = extract_articles()

    if QUEUE_FILE.exists():
        try:
            queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
            # Sincronizar si hay artículos nuevos
            existing_slugs = {item["slug"] for item in queue}
            for art in all_articles:
                if art["slug"] not in existing_slugs:
                    art["published"] = False
                    art["published_at"] = None
                    art["post_id"] = None
                    queue.append(art)
            return queue
        except Exception as e:
            print(f"[WARN] Error leyendo cola existente ({e}); reinicializando.")

    # Inicializar nueva cola
    queue = []
    for art in all_articles:
        art["published"] = False
        art["published_at"] = None
        art["post_id"] = None
        queue.append(art)

    save_queue(queue)
    return queue


def save_queue(queue: list[dict]) -> None:
    """Guarda el estado de la cola en el archivo JSON."""
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_FILE.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")


def generate_linkedin_post(article: dict, hook_index: int = 0) -> str:
    """Genera el texto completo del post adaptado al algoritmo de LinkedIn."""
    hook = HOOK_TEMPLATES[hook_index % len(HOOK_TEMPLATES)]
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


def publish_to_linkedin(post_text: str, article_url: str, article_title: str) -> dict:
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
                        "originalUrl": article_url,
                        "title": {
                            "text": article_title[:200]
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
    parser.add_argument("--list", action="store_true", help="Lista el estado de todos los artículos en la cola.")
    parser.add_argument("--reset-queue", action="store_true", help="Reinicia el estado de la cola para volver a empezar.")
    args = parser.parse_args()

    queue = init_or_load_queue()

    if args.reset_queue:
        for item in queue:
            item["published"] = False
            item["published_at"] = None
            item["post_id"] = None
        save_queue(queue)
        print(f"[OK] Cola reiniciada. {len(queue)} artículos listos para un nuevo ciclo.")
        return

    if args.list:
        published_count = sum(1 for item in queue if item.get("published"))
        print(f"\n=== ESTADO DE LA COLA DE LINKEDIN ({published_count}/{len(queue)} publicados) ===")
        for i, item in enumerate(queue, 1):
            status = "✅ Publicado" if item.get("published") else "⏳ Pendiente"
            date = f" ({item.get('published_at')})" if item.get("published_at") else ""
            print(f"{i:02d}. [{status}{date}] {item['title'][:65]}")
        return

    # Buscar el próximo artículo no publicado
    next_article = None
    next_index = 0
    for idx, item in enumerate(queue):
        if not item.get("published"):
            next_article = item
            next_index = idx
            break

    # Si ya se publicaron todos, reiniciar automáticamente la rotación
    if not next_article:
        print("[INFO] ¡Se completaron los 78 artículos! Reiniciando automáticamente el ciclo con nuevos ángulos...")
        for item in queue:
            item["published"] = False
            item["published_at"] = None
            item["post_id"] = None
        save_queue(queue)
        next_article = queue[0]
        next_index = 0

    post_content = generate_linkedin_post(next_article, hook_index=next_index)

    if args.publish:
        print(f"[PUBLICANDO EN LINKEDIN] Artículo #{next_index + 1}: «{next_article['title']}»...")
        try:
            resp = publish_to_linkedin(post_content, next_article["url"], next_article["title"])
            post_id = resp.get("id", "OK")
            next_article["published"] = True
            next_article["published_at"] = datetime.now(timezone.utc).isoformat()
            next_article["post_id"] = post_id
            save_queue(queue)
            print(f"[ÉXITO] Post publicado correctamente en LinkedIn. ID: {post_id}")
        except Exception as e:
            print(f"[ERROR CRÍTICO] Falló la publicación: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"\n=======================================================")
        print(f" [VISTA PREVIA - DRY RUN] Artículo #{next_index + 1} de {len(queue)}")
        print(f"=======================================================\n")
        print(post_content)
        print(f"\n=======================================================")
        print(f"URL a compartir: {next_article['url']}")
        print(f"Para publicar realmente en LinkedIn ejecuta con: --publish")
        print(f"=======================================================\n")


if __name__ == "__main__":
    main()
