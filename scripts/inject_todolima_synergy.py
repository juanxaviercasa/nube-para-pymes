#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inyector de Sinergia y Enlazado Estratégico con Todo Lima (todolima.com)
1. Inserta un Smart Partner Banner en las 26 herramientas interactivas de Nube para Pymes.
2. Inserta bloques contextuales de recomendación hacia los directorios especializados de Todo Lima
   en los artículos relevantes de WordPress en nubepymesexport/.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP_EXPORT = ROOT / "nubepymesexport"

# 1. Mapeo de artículos a categorías y llamados de Todo Lima
ARTICLE_BRIDGES = {
    "punto-de-venta-restaurantes": {
        "title": "¿Gestionas un restaurante, pollería o cafetería en Lima?",
        "desc": "Un sistema POS optimiza comandas y cocina, pero para llenar mesas necesitas presencia local efectiva. Revisa cómo se posicionan los comercios gastronómicos en el <a href=\"https://todolima.com/pollerias\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Directorio de Pollerías de Lima</a>, <a href=\"https://todolima.com/chifas\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Chifas de Lima</a> y <a href=\"https://todolima.com/cevicherias\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Cevicherías de Lima</a>.",
        "url": "https://todolima.com/pollerias",
        "cta": "Explorar Directorio Gastronómico de Lima"
    },
    "software-reservas-clinicas": {
        "title": "¿Tienes un consultorio médico o clínica dental en Lima?",
        "desc": "Reducir el ausentismo de pacientes con software de citas es clave para la rentabilidad de consultorios privados en distritos como Miraflores, San Isidro o Surco. Consulta las opciones de atención publicadas en el <a href=\"https://todolima.com/dentistas\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Directorio de Dentistas de Lima</a> y <a href=\"https://todolima.com/veterinarias\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Veterinarias de Lima</a>.",
        "url": "https://todolima.com/dentistas",
        "cta": "Ver Especialistas de Salud en Lima"
    },
    "gestion-despachos-abogados": {
        "title": "¿Lideras un estudio jurídico o notaría en Lima?",
        "desc": "La gestión documental y seguimiento de expedientes judiciales en la capital se complementa con una presencia institucional de alta reputación. Descubre los estudios jurídicos destacados en el <a href=\"https://todolima.com/abogados\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Directorio de Abogados de Lima</a> y <a href=\"https://todolima.com/notarias\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Notarías en Lima</a>.",
        "url": "https://todolima.com/abogados",
        "cta": "Consultar Directorio Legal de Lima"
    },
    "crm-para-inmobiliarias": {
        "title": "¿Te dedicas a la intermediación inmobiliaria en Lima?",
        "desc": "En el mercado de venta y alquiler en Lima Metropolitana, la rapidez en WhatsApp decide el cierre de captaciones. Revisa el perfil y posicionamiento de los profesionales en el <a href=\"https://todolima.com/agentes-inmobiliarios\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Directorio de Agentes Inmobiliarios de Lima</a>.",
        "url": "https://todolima.com/agentes-inmobiliarios",
        "cta": "Ver Agentes Inmobiliarios en Lima"
    },
    "software-gimnasios-estudios": {
        "title": "¿Administras un gimnasio o complejo de canchas en Lima?",
        "desc": "El cobro ágil de membresías y la reserva de turnos deportivos por WhatsApp aumentan la retención de usuarios. Mira cómo los principales centros deportivos captan clientes en el <a href=\"https://todolima.com/alquiler-de-canchas\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Directorio de Alquiler de Canchas Sintéticas en Lima</a> y <a href=\"https://todolima.com/gimnasios\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Gimnasios de Lima</a>.",
        "url": "https://todolima.com/alquiler-de-canchas",
        "cta": "Explorar Centros Deportivos en Lima"
    },
    "facturar-independiente-peru": {
        "title": "¿Ofreces servicios profesionales independientes en Lima?",
        "desc": "Manejar correctamente el RUC 10 o RUC 20 ante SUNAT y emitir comprobantes electrónicos sin contingencias requiere asesoría experta. Encuentra contadores colegiados y asesores tributarios en el <a href=\"https://todolima.com/contadores\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Directorio de Contadores de Lima</a>.",
        "url": "https://todolima.com/contadores",
        "cta": "Buscar Contadores Colegiados en Lima"
    },
    "crm-integrado-whatsapp-business": {
        "title": "¿Quieres automatizar la atención de tu negocio en Lima por WhatsApp?",
        "desc": "Integrar tu WhatsApp con agentes inteligentes de Inteligencia Artificial que atiendan 24/7 y agenden cotizaciones en automático es una realidad accesible para pymes limeñas. Conoce las soluciones de <a href=\"https://todolima.com/auditoria\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Auditoría Digital y Asistentes IA de Todo Lima</a>.",
        "url": "https://todolima.com/auditoria",
        "cta": "Solicitar Demostración de Asistente IA"
    },
    "crm-con-whatsapp-integrado": {
        "title": "¿Recibes decenas de consultas en WhatsApp sin poder responder a tiempo?",
        "desc": "Los comercios y prestadores de servicios en Lima pierden hasta un 50% de clientes por demoras en respuesta. Descubre cómo implementar embudos de venta y flujos automáticos con el equipo de <a href=\"https://todolima.com/auditoria\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Todo Lima Soluciones B2B</a>.",
        "url": "https://todolima.com/auditoria",
        "cta": "Ver Soluciones de Automatización en Lima"
    },
    "seo-geo-para-pymes-visibilidad-ia": {
        "title": "¿Tu negocio en Lima aparece cuando buscan en Google Maps o ChatGPT?",
        "desc": "El posicionamiento local (GEO) es la estrategia con mayor retorno para captar clientes en los 43 distritos de Lima Metropolitana. Registra o audita tu negocio en el <a href=\"https://todolima.com\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Directorio Oficial Todo Lima</a> y multiplica tu visibilidad distrital.",
        "url": "https://todolima.com",
        "cta": "Ver Directorio Oficial Todo Lima"
    },
    "geo-para-pymes-respuestas-inteligencia-artificial": {
        "title": "¿Cómo optimizar tu empresa para los motores de respuesta con IA en Lima?",
        "desc": "Las búsquedas locales en Lima están migrando hacia respuestas generadas por IA. Estar indexado en directorios estructurados y verificados como <a href=\"https://todolima.com\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">todolima.com</a> garantiza que tu marca sea citada como referente en tu rubro y distrito.",
        "url": "https://todolima.com",
        "cta": "Indexar mi Negocio en Todo Lima"
    },
    "herramientas-profesores-particulares": {
        "title": "¿Impartes clases o diriges una academia educativa en Lima?",
        "desc": "La educación y capacitación personalizada en distritos de Lima requiere organización de horarios y captación ágil. Revisa el directorio de <a href=\"https://todolima.com/escuelas-de-manejo\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Escuelas de Capacitación en Lima</a> y conoce cómo estructuran su oferta.",
        "url": "https://todolima.com/escuelas-de-manejo",
        "cta": "Ver Directorio Educativo en Lima"
    },
    "digitalizar-procesos-negocio-pequeno": {
        "title": "¿Tienes una pyme o comercio en Lima Metropolitana?",
        "desc": "La digitalización empieza por tener una presencia web ultrarrápida y presencia en el mapa comercial de tu distrito. Únete a los más de 50 rubros mapeados en el <a href=\"https://todolima.com\" target=\"_blank\" rel=\"noopener\" style=\"color: #0284c7; font-weight: 700; text-decoration: underline;\">Directorio comercial de Todo Lima</a>.",
        "url": "https://todolima.com",
        "cta": "Publicar Negocio en Todo Lima"
    }
}

TOOL_BANNER_HTML = """<!-- [TODOLIMA_PARTNER_BANNER_START] -->
<div class="np-todolima-partner-banner" style="max-width: 960px; margin: 32px auto 16px auto; padding: 16px 22px; background: #0f172a; border: 1.5px solid #1e293b; border-left: 5px solid #0284c7; border-radius: 14px; color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; box-shadow: 0 4px 20px rgba(0,0,0,0.12);">
  <div style="display: flex; align-items: center; gap: 14px;">
    <span style="font-size: 28px; line-height: 1;">📍</span>
    <div>
      <strong style="color: #38bdf8; font-size: 0.96rem; display: block; margin-bottom: 3px;">¿Tienes un negocio o comercio en Lima Metropolitana?</strong>
      <span style="color: #94a3b8; font-size: 0.86rem; line-height: 1.4; display: block;">Solicita la revisión de tu ficha y presenta ubicación, servicios y formas de contacto. La inclusión no garantiza consultas ni ventas.</span>
    </div>
  </div>
  <a href="https://todolima.com" target="_blank" rel="noopener" style="padding: 9px 18px; background: #0284c7; hover:background: #0369a1; color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 0.84rem; white-space: nowrap; transition: background 0.2s;">Solicitar revisión de mi ficha →</a>
</div>
<!-- [TODOLIMA_PARTNER_BANNER_END] -->
"""

def generate_bridge_card_html(bridge_data):
    return f"""<!-- [TODOLIMA_BRIDGE_START] -->
<div class="npp-todolima-bridge" style="margin: 2.5em 0; padding: 1.4em 1.6em; background: #f8fafc; border: 1.5px solid #e2e8f0; border-left: 5px solid #0284c7; border-radius: 12px; font-family: inherit;">
  <div style="display: flex; align-items: flex-start; gap: 14px;">
    <div style="font-size: 26px; line-height: 1; flex-shrink: 0; margin-top: 2px;">📍</div>
    <div>
      <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 1.05rem; font-weight: 700;">{bridge_data['title']}</h4>
      <p style="margin: 0 0 12px 0; color: #334155; font-size: 0.92rem; line-height: 1.55;">
        {bridge_data['desc']}
      </p>
      <a href="{bridge_data['url']}" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 6px; padding: 7px 15px; background: #0284c7; color: #ffffff; font-weight: 600; font-size: 0.82rem; border-radius: 6px; text-decoration: none; transition: opacity 0.2s;">
        <span>{bridge_data['cta']}</span> →
      </a>
    </div>
  </div>
</div>
<!-- [TODOLIMA_BRIDGE_END] -->
"""

def inject_article_bridges():
    print("[SYNERGY] Inyectando puentes contextuales en artículos de nubepymesexport/...")
    count = 0
    for slug, bridge_data in ARTICLE_BRIDGES.items():
        article_file = WP_EXPORT / slug / "index.html"
        if not article_file.exists():
            print(f"  [OMITIDO] No encontrado: {slug}")
            continue

        content = article_file.read_text(encoding="utf-8")
        if "[TODOLIMA_BRIDGE_START]" in content:
            # Reemplazar versión existente para permitir actualizaciones
            content = re.sub(r'<!-- \[TODOLIMA_BRIDGE_START\] -->.*?<!-- \[TODOLIMA_BRIDGE_END\] -->\n?', '', content, flags=re.DOTALL)

        bridge_html = generate_bridge_card_html(bridge_data)
        
        # Insertar antes del cierre de .entry-content
        if "</div><!-- .entry-content .clear -->" in content:
            content = content.replace("</div><!-- .entry-content .clear -->", f"\n{bridge_html}\n</div><!-- .entry-content .clear -->")
            article_file.write_text(content, encoding="utf-8")
            count += 1
            print(f"  [OK] Puente inyectado en: {slug}")
        elif "</article>" in content:
            content = content.replace("</article>", f"\n{bridge_html}\n</article>")
            article_file.write_text(content, encoding="utf-8")
            count += 1
            print(f"  [OK] Puente inyectado antes de </article> en: {slug}")
        else:
            print(f"  [ERROR] No se encontró punto de anclaje en: {slug}")

    print(f"[SYNERGY] Total puentes inyectados en artículos: {count}")

def inject_tool_banners():
    print("[SYNERGY] Inyectando Smart Banner de Todo Lima en las 26 herramientas...")
    count = 0
    tool_files = [f for f in ROOT.glob("*.html") if f.name not in ("index.html", "404.html", "guia-uso-22-apps.html")]
    
    for tf in tool_files:
        content = tf.read_text(encoding="utf-8")
        if "[TODOLIMA_PARTNER_BANNER_START]" in content:
            content = re.sub(r'<!-- \[TODOLIMA_PARTNER_BANNER_START\] -->.*?<!-- \[TODOLIMA_PARTNER_BANNER_END\] -->\n?', '', content, flags=re.DOTALL)

        # Insertar antes de </footer> o antes de </body>
        if "</footer>" in content:
            content = content.replace("</footer>", f"{TOOL_BANNER_HTML}\n</footer>")
            tf.write_text(content, encoding="utf-8")
            count += 1
            print(f"  [OK] Banner inyectado en herramienta: {tf.name}")
        elif "</body>" in content:
            content = content.replace("</body>", f"{TOOL_BANNER_HTML}\n</body>")
            tf.write_text(content, encoding="utf-8")
            count += 1
            print(f"  [OK] Banner inyectado antes de </body> en: {tf.name}")

    print(f"[SYNERGY] Total herramientas con banner inyectado: {count}")

if __name__ == "__main__":
    inject_article_bridges()
    inject_tool_banners()
    print("[SYNERGY] Inyección de sinergia completada exitosamente.")
