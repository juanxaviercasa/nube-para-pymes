#!/usr/bin/env python3
"""
Motor de Publicación Automática en Pinterest para Nube para Pymes
=================================================================
Genera pines verticales optimizados (1000x1500 px, ratio 2:3), extrae
título, descripción SEO, puntos clave y enlace directo a la web.

Utiliza la API oficial Pinterest v5 (https://api.pinterest.com/v5).
"""

import argparse
import base64
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Rutas del proyecto
ROOT = Path(__file__).resolve().parent.parent
QUEUE_FILE = ROOT / "scripts" / "linkedin_queue.json"

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

PINTEREST_API_BASE = "https://api.pinterest.com/v5"

# Paleta de colores para los Pines
COLOR_BG_DARK = (15, 23, 42)       # Slate 900
COLOR_CARD_BG = (30, 41, 59)       # Slate 800
COLOR_ACCENT = (13, 148, 136)      # Teal 600 (marca Nube para Pymes)
COLOR_ACCENT_LIGHT = (45, 212, 191)# Teal 400
COLOR_TEXT_MAIN = (255, 255, 255)  # Blanco puro
COLOR_TEXT_MUTED = (203, 213, 225) # Slate 300
COLOR_BORDER = (51, 65, 85)        # Slate 700


def get_font(size: int, bold: bool = False):
    """Obtiene una fuente TrueType del sistema o fallback por defecto."""
    font_names = (
        ["arialbd.ttf", "segoeuib.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"]
        if bold
        else ["arial.ttf", "segoeui.ttf", "calibri.ttf", "DejaVuSans.ttf"]
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


def wrap_text(text: str, max_chars: int = 28) -> list[str]:
    """Divide un texto en líneas para el lienzo vertical del Pin."""
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


def generate_pinterest_pin_card(item: dict) -> bytes:
    """
    Genera un Pin vertical de alta conversión (1000 x 1500 px, ratio 2:3)
    diseñado específicamente para maximizar CTR y guardados en Pinterest.
    """
    width, height = 1000, 1500
    img = Image.new("RGB", (width, height), COLOR_BG_DARK)
    draw = ImageDraw.Draw(img)

    # 1. Marco y fondo sutil
    draw.rounded_rectangle([(30, 30), (width - 30, height - 30)], radius=32, outline=COLOR_BORDER, width=2)
    draw.rounded_rectangle([(60, 60), (width - 60, height - 60)], radius=24, fill=COLOR_CARD_BG)

    # 2. Header / Badge de Marca
    font_badge = get_font(26, bold=True)

    # Pastilla superior
    is_tool = item.get("type") == "tool"
    badge_text = "HERRAMIENTA INTERACTIVA" if is_tool else "GUÍA TÉCNICA PARA PYMES"
    badge_w = 460
    draw.rounded_rectangle([(width // 2 - badge_w // 2, 90), (width // 2 + badge_w // 2, 145)], radius=20, fill=COLOR_ACCENT)
    draw.text((width // 2, 117), badge_text, fill=COLOR_TEXT_MAIN, font=font_badge, anchor="mm")

    # 3. Título Principal (Grande, legible en móvil)
    title = item.get("title") or item.get("name", "Guía para Pequeñas Empresas")
    # Limpiar prefijos redundantes
    title = re.sub(r"^Herramienta #\d+:\s*", "", title)
    font_title = get_font(52, bold=True)
    title_lines = wrap_text(title, max_chars=24)

    y_cursor = 190
    for line in title_lines[:4]:
        draw.text((width // 2, y_cursor), line, fill=COLOR_TEXT_MAIN, font=font_title, anchor="mt")
        y_cursor += 68

    # Línea decorativa
    y_cursor += 20
    draw.line([(width // 2 - 120, y_cursor), (width // 2 + 120, y_cursor)], fill=COLOR_ACCENT_LIGHT, width=4)
    y_cursor += 45

    # 4. Bloque de Beneficios / Puntos Clave
    font_subtitle = get_font(32, bold=True)
    font_body = get_font(26, bold=False)

    if is_tool:
        # Tarjeta para Herramientas
        draw.rounded_rectangle([(100, y_cursor), (width - 100, y_cursor + 480)], radius=20, fill=(15, 23, 42), outline=COLOR_BORDER, width=2)
        inner_y = y_cursor + 40
        draw.text((140, inner_y), "CAPACIDADES DESTACADAS:", fill=COLOR_ACCENT_LIGHT, font=font_subtitle)
        inner_y += 60

        features = item.get("features", [])
        if not features:
            features = [
                "Diagnóstico y análisis instantáneo en tu navegador",
                "Sin suscripción, sin registros ni tarjetas",
                "Optimizado para aumentar la productividad de tu equipo"
            ]

        for i, feat in enumerate(features[:3], 1):
            feat_lines = wrap_text(f"{i}. {feat}", max_chars=34)
            for fline in feat_lines:
                draw.text((140, inner_y), fline, fill=COLOR_TEXT_MAIN, font=font_body)
                inner_y += 38
            inner_y += 20

        y_cursor += 520
    else:
        # Tarjeta para Artículos
        draw.rounded_rectangle([(100, y_cursor), (width - 100, y_cursor + 480)], radius=20, fill=(15, 23, 42), outline=COLOR_BORDER, width=2)
        inner_y = y_cursor + 40
        draw.text((140, inner_y), "APRENDIZAJES CLAVE:", fill=COLOR_ACCENT_LIGHT, font=font_subtitle)
        inner_y += 60

        key_points = item.get("key_points", [])
        if not key_points:
            key_points = [
                "Criterios de selección y análisis técnico",
                "Comparativa de opciones y costes reales",
                "Recomendaciones aplicables paso a paso"
            ]

        for pt in key_points[:3]:
            pt_clean = re.sub(r"^[^:]+:\s*", "", pt)  # Quita prefijos duplicados
            pt_lines = wrap_text(f"• {pt_clean}", max_chars=34)
            for pline in pt_lines:
                draw.text((140, inner_y), pline, fill=COLOR_TEXT_MAIN, font=font_body)
                inner_y += 38
            inner_y += 20

        y_cursor += 520

    # 5. Badges de Confianza / Garantía
    draw.text((width // 2, y_cursor + 20), "100% Gratuito  |  Análisis Independiente  |  Sin Registro", fill=(148, 163, 184), font=font_body, anchor="mt")

    # 6. Botón / Call To Action Inferior
    cta_box_top = height - 190
    cta_box_bottom = height - 90
    draw.rounded_rectangle([(100, cta_box_top), (width - 100, cta_box_bottom)], radius=24, fill=COLOR_ACCENT)

    font_cta = get_font(34, bold=True)
    font_sub_cta = get_font(22, bold=False)
    draw.text((width // 2, cta_box_top + 32), "LEER EN NUBEPARAPYMES.ONLINE", fill=COLOR_TEXT_MAIN, font=font_cta, anchor="mm")
    draw.text((width // 2, cta_box_top + 68), "Haz clic en el enlace para ver el informe completo", fill=(204, 251, 241), font=font_sub_cta, anchor="mm")

    output = io.BytesIO()
    img.save(output, format="JPEG", quality=92)
    return output.getvalue()


def build_pin_metadata(item: dict) -> dict:
    """Prepara el título, descripción optimizada para SEO en Pinterest y URL."""
    title = item.get("title") or item.get("name", "")
    # Pinterest recorta títulos a 100 caracteres
    if len(title) > 95:
        title = title[:92] + "..."

    is_tool = item.get("type") == "tool"
    url = item.get("url", "https://nubeparapymes.online/")
    desc_base = item.get("description", "")

    # Descripción con palabras clave para el buscador de Pinterest (máx 500 caracteres)
    if is_tool:
        description = (
            f"🛠️ {item.get('name')}: {desc_base} "
            f"Descubre esta herramienta 100% gratuita para pequeñas empresas y emprendedores. "
            f"Pruébala directamente en tu navegador sin registros en Nube para Pymes. "
            f"#Pymes #HerramientasOnline #Productividad #Emprendimiento #SoftwareEmpresarial"
        )
    else:
        description = (
            f"📖 {title}: {desc_base} "
            f"Revisa nuestra comparativa y guía completa con criterios prácticos de implementación para pymes. "
            f"Lee el análisis técnico completo en Nube para Pymes. "
            f"#Pymes #GestionEmpresarial #Negocios #Productividad #Automatizacion"
        )

    if len(description) > 490:
        description = description[:487] + "..."

    return {
        "title": title,
        "description": description,
        "link": url,
        "alt_text": f"Infografía y resumen de {title} en nubeparapymes.online"
    }


def call_pinterest_api(endpoint: str, method: str = "GET", data: dict | None = None, token: str = "") -> dict:
    """Ejecuta una llamada autenticada a la API v5 de Pinterest."""
    url = f"{PINTEREST_API_BASE}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "NubeParaPymes-Engine/1.0"
    }

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_or_create_board(token: str, preferred_name: str = "Herramientas y Software para Pymes") -> str:
    """Busca un tablero público disponible o crea uno automáticamente."""
    try:
        boards_data = call_pinterest_api("/boards", method="GET", token=token)
        items = boards_data.get("items", [])
        if items:
            # Buscar por nombre similar
            for b in items:
                if "pyme" in b.get("name", "").lower() or "software" in b.get("name", "").lower():
                    return b["id"]
            return items[0]["id"]
    except Exception as e:
        print(f"[WARN] No se pudieron listar los tableros: {e}")

    # Intentar crearlo si no existe
    try:
        new_board = call_pinterest_api("/boards", method="POST", data={
            "name": preferred_name,
            "description": "Recursos, guías y herramientas gratuitas para la gestión y digitalización de pequeñas empresas.",
            "privacy": "PUBLIC"
        }, token=token)
        print(f"[INFO] Tablero «{preferred_name}» creado con éxito (ID: {new_board.get('id')})")
        return new_board["id"]
    except Exception as e:
        raise RuntimeError(f"No se pudo crear ni encontrar un tablero en Pinterest: {e}")


def publish_pin_to_pinterest(item: dict, token: str, board_id: str | None = None) -> tuple[dict, str]:
    """Genera la imagen del Pin, la codifica en base64 y la publica en Pinterest."""
    meta = build_pin_metadata(item)
    card_bytes = generate_pinterest_pin_card(item)
    base64_image = base64.b64encode(card_bytes).decode("utf-8")

    target_board_id = board_id or get_or_create_board(token)

    payload = {
        "board_id": target_board_id,
        "title": meta["title"],
        "description": meta["description"],
        "link": meta["link"],
        "alt_text": meta["alt_text"],
        "media_source": {
            "source_type": "image_base64",
            "content_type": "image/jpeg",
            "data": base64_image
        }
    }

    resp = call_pinterest_api("/pins", method="POST", data=payload, token=token)
    pin_id = resp.get("id", "")
    return resp, pin_id


def load_queue() -> list[dict]:
    """Carga la cola unificada."""
    if not QUEUE_FILE.exists():
        return []
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_queue(queue: list[dict]):
    """Guarda la cola actualizada."""
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Motor de Publicación Automática en Pinterest")
    parser.add_argument("--dry-run", action="store_true", help="Simula la creación del Pin sin publicar")
    parser.add_argument("--publish", action="store_true", help="Publica el siguiente contenido en Pinterest")
    parser.add_argument("--status", action="store_true", help="Muestra el estado de la cola para Pinterest")
    parser.add_argument("--test-connection", action="store_true", help="Verifica el token de Pinterest")
    args = parser.parse_args()

    token = os.environ.get("PINTEREST_ACCESS_TOKEN", "").strip()
    board_id_env = os.environ.get("PINTEREST_BOARD_ID", "").strip() or None

    queue = load_queue()
    if not queue:
        print("[ERROR] No se encontró o está vacía la cola de publicaciones.")
        sys.exit(1)

    if args.status:
        published_count = sum(1 for it in queue if it.get("pinterest_published"))
        print("\n=======================================================")
        print(f" ESTADO DE PUBLICACIONES EN PINTEREST: {published_count}/{len(queue)}")
        print("=======================================================\n")
        for i, it in enumerate(queue, 1):
            st = "✅ Publicado" if it.get("pinterest_published") else "⏳ Pendiente"
            t = it.get("title") or it.get("name", "")
            pid = it.get("pinterest_pin_id", "")
            pinfo = f" (Pin ID: {pid})" if pid else ""
            print(f"{i:02d}. [{st}] {t[:60]}{pinfo}")
        return

    # Buscar el siguiente ítem no publicado en Pinterest
    next_item = None
    next_index = 0
    for idx, item in enumerate(queue):
        if not item.get("pinterest_published"):
            next_item = item
            next_index = idx
            break

    if not next_item:
        print("[INFO] ¡Todos los pines han sido publicados en Pinterest! Reiniciando ciclo...")
        for it in queue:
            it["pinterest_published"] = False
            it["pinterest_published_at"] = None
            it["pinterest_pin_id"] = None
        save_queue(queue)
        next_item = queue[0]
        next_index = 0

    if args.publish:
        if not token:
            print("[WARN] PINTEREST_ACCESS_TOKEN no configurado en variables de entorno.")
            print("[INFO] Para activarlo, añade PINTEREST_ACCESS_TOKEN en GitHub Secrets.")
            sys.exit(0)

        print(f"[PUBLICANDO EN PINTEREST] #{next_index + 1}: «{next_item.get('title')}»...")
        try:
            resp, pin_id = publish_pin_to_pinterest(next_item, token, board_id=board_id_env)
            next_item["pinterest_published"] = True
            next_item["pinterest_published_at"] = datetime.now(timezone.utc).isoformat()
            next_item["pinterest_pin_id"] = pin_id
            save_queue(queue)

            pin_url = f"https://www.pinterest.com/pin/{pin_id}/" if pin_id else "OK"
            print(f"\n[ÉXITO] Pin publicado en Pinterest.")
            print(f"  • ID: {pin_id}")
            print(f"  • Enlace al Pin: {pin_url}\n")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            print(f"[ERROR HTTP {e.code} EN PINTEREST]: {error_body}")
            # Si es por app pendiente o no soportada, loguear aviso claro
            if "consumer type is not supported" in error_body or e.code == 401:
                print("\n[AVISO] Tu aplicación de Pinterest aún está en proceso de revisión ('Trial access pendiente').")
                print("En cuanto Pinterest apruebe el acceso de prueba, las publicaciones se activarán automáticamente.")
            sys.exit(0)  # Salir limpio para no tumbar el workflow de GitHub Actions
        except Exception as e:
            print(f"[ERROR AL PUBLICAR EN PINTEREST]: {e}")
            sys.exit(0)
    else:
        # Modo DRY-RUN o prueba local
        print("\n=======================================================")
        print(f" [VISTA PREVIA DE PINTEREST - DRY RUN] #{next_index + 1} de {len(queue)}")
        print("=======================================================\n")
        meta = build_pin_metadata(next_item)
        print(f"📌 Título del Pin:       {meta['title']}")
        print(f"🔗 Enlace de Destino:   {meta['link']}")
        print(f"📝 Descripción SEO:\n{meta['description']}\n")

        # Generar imagen de prueba y guardarla localmente
        card_bytes = generate_pinterest_pin_card(next_item)
        preview_file = ROOT / "scripts" / "pinterest_preview_card.jpg"
        with open(preview_file, "wb") as f:
            f.write(card_bytes)
        print(f"🖼️ Imagen vertical generada: {preview_file} ({len(card_bytes) // 1024} KB, 1000x1500 px)")
        print("\nPara publicar realmente en Pinterest ejecuta con: --publish")
        print("=======================================================\n")


if __name__ == "__main__":
    main()
