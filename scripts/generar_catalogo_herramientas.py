#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Catálogo Visual y PDF Carousel para LinkedIn:
"Las 26 Herramientas Gratuitas para Pymes de Xavier Cabello"

Genera un documento PDF de alta resolución optimizado para carruseles de LinkedIn (formato 4:5 vertical 1080x1350),
presentando cada una de las 26 herramientas del portal nubeparapymes.online con su propuesta de valor,
casos de uso y enlace directo.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Configurar salida UTF-8
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "dist" / "marketing"
HTML_FILE = OUTPUT_DIR / "catalogo_slides.html"
PDF_FILE = ROOT / "Catalogo_26_Herramientas_NubeParaPymes.pdf"

# Definición de las 26 herramientas organizadas por pilar estratégico
TOOLS_DATA = [
    # 1. Marketing
    {
        "cat": "marketing",
        "cat_name": "MARKETING & ADQUISICIÓN",
        "color": "#38BDF8",
        "icon": "📣",
        "slug": "analizador-titulares",
        "name": "Analizador de Titulares",
        "problem": "El 80% de las personas solo lee el titular antes de decidir si hace clic o abandona.",
        "benefit": "Evalúa fuerza, tono, impacto emocional y claridad de tus copys para anuncios y artículos.",
        "features": ["Puntuación algorítmica de atracción", "Detección de palabras de poder y emoción", "Comparador A/B de variantes en tiempo real"],
    },
    {
        "cat": "marketing",
        "cat_name": "MARKETING & ADQUISICIÓN",
        "color": "#38BDF8",
        "icon": "🔍",
        "slug": "auditor-seo-basico",
        "name": "Auditor Básico de SEO On-Page",
        "problem": "Tener una web invisible en Google cuesta miles de dólares en anuncios desperdiciados.",
        "benefit": "Audita etiquetas meta, jerarquía H1-H3, densidad de palabras clave y vista previa en Google.",
        "features": ["Diagnóstico de salud SEO al instante", "Previsualización real de snippet en SERP", "Checklist accionable de correcciones"],
    },
    {
        "cat": "marketing",
        "cat_name": "MARKETING & ADQUISICIÓN",
        "color": "#38BDF8",
        "icon": "📈",
        "slug": "comparador-campanas-avanzado",
        "name": "Comparador Avanzado de Campañas",
        "problem": "Invertir en Meta Ads o Google sin comparar retorno real conduce a quemar presupuesto.",
        "benefit": "Compara CPA, ROAS, CPC y conversión entre múltiples campañas y plataformas publicitarias.",
        "features": ["Cálculo automático de ROAS y ROI", "Simulación de escenarios de escala", "Exportación de informes ejecutivos"],
    },
    {
        "cat": "marketing",
        "cat_name": "MARKETING & ADQUISICIÓN",
        "color": "#38BDF8",
        "icon": "🎯",
        "slug": "consola-campanas",
        "name": "Consola de Campañas y UTMs",
        "problem": "No saber exactamente qué anuncio o enlace generó una venta impide tomar decisiones de inversión.",
        "benefit": "Genera y organiza enlaces UTM con nomenclatura limpia y consistente para analítica web.",
        "features": ["Constructor UTM para Google Analytics", "Validador de parámetros en vivo", "Historial de enlaces frecuentes"],
    },
    {
        "cat": "marketing",
        "cat_name": "MARKETING & ADQUISICIÓN",
        "color": "#38BDF8",
        "icon": "🗓️",
        "slug": "organizador-matriz-contenidos",
        "name": "Matriz de Contenidos Estratégica",
        "problem": "Publicar sin rumbo en redes agota a tu equipo y no genera prospectos calificados.",
        "benefit": "Planifica temas por pilares de contenido, etapas de embudo (TOFU/MOFU/BOFU) y canales.",
        "features": ["Mapeo por etapas del cliente", "Clasificación por formatos y canales", "Calendario editorial exportable"],
    },

    # 2. Finanzas
    {
        "cat": "finanzas",
        "cat_name": "FINANZAS & RENTABILIDAD",
        "color": "#10B981",
        "icon": "💰",
        "slug": "flujo-caja-pymes",
        "name": "Flujo de Caja para Pymes",
        "problem": "El 82% de las empresas que cierran lo hacen por falta de liquidez, no por falta de ventas.",
        "benefit": "Proyecta entradas y salidas de dinero semanales y mensuales para anticipar déficits de caja.",
        "features": ["Proyección de saldo disponible en tiempo real", "Alertas visuales de quiebre de caja", "100% privado: datos guardados en tu navegador"],
    },
    {
        "cat": "finanzas",
        "cat_name": "FINANZAS & RENTABILIDAD",
        "color": "#10B981",
        "icon": "🏷️",
        "slug": "calculadora-descuentos-promociones",
        "name": "Calculadora de Descuentos y Promociones",
        "problem": "Hacer descuentos sin calcular el punto de equilibrio destruye el margen neto de tu negocio.",
        "benefit": "Calcula cuántas unidades extra necesitas vender para compensar una rebaja de precio.",
        "features": ["Simulador de margen sobre ventas vs costo", "Análisis de promociones 2x1 y combos", "Cálculo de punto de equilibrio promocional"],
    },
    {
        "cat": "finanzas",
        "cat_name": "FINANZAS & RENTABILIDAD",
        "color": "#10B981",
        "icon": "🧾",
        "slug": "calculadora-precios-venta-igv",
        "name": "Calculadora de Precios de Venta e IGV",
        "problem": "Confundir margen con markup o no desglosar impuestos provoca pérdidas invisibles.",
        "benefit": "Convierte costo, margen neto deseado e impuesto (IGV/IVA) en el precio de venta final exacto.",
        "features": ["Desglose claro de costo, ganancia e impuesto", "Simulación de márgenes comerciales", "Exportación de ficha de precios"],
    },
    {
        "cat": "finanzas",
        "cat_name": "FINANZAS & RENTABILIDAD",
        "color": "#10B981",
        "icon": "🏦",
        "slug": "calculadora-prestamos-amortizaciones",
        "name": "Calculadora de Préstamos y Amortizaciones",
        "problem": "Los bancos ocultan el impacto real de las cuotas y los intereses a largo plazo.",
        "benefit": "Genera la tabla de amortización completa (método francés o alemán) y evalúa abonos de capital.",
        "features": ["Tabla detallada cuota por cuota", "Simulador de abonos extraordinarios a capital", "Comparador de créditos en paralelo"],
    },
    {
        "cat": "finanzas",
        "cat_name": "FINANZAS & RENTABILIDAD",
        "color": "#10B981",
        "icon": "👥",
        "slug": "calculadora-sobrecostos-laborales",
        "name": "Calculadora de Sobrecostos Laborales",
        "problem": "Contratar un colaborador cuesta mucho más que su salario nominal (gratificaciones, CTS, seguro).",
        "benefit": "Estima el costo total del empleador por puesto y departamento para presupuestar nómina sin sorpresas.",
        "features": ["Desglose de aportes legales y provisiones", "Cálculo mensual y anual consolidado", "Filtros por departamento o área"],
    },

    # 3. Ventas
    {
        "cat": "ventas",
        "cat_name": "VENTAS & CONVERSIÓN",
        "color": "#818CF8",
        "icon": "💼",
        "slug": "crm-pymes",
        "name": "CRM Ligero para Pymes",
        "problem": "Los prospectos se pierden en chats de WhatsApp y hojas de cálculo desordenadas.",
        "benefit": "Embudo comercial visual estilo Kanban para gestionar clientes, estados y montos de oportunidad.",
        "features": ["Embudo arrastrable (Lead, Contactado, Ganado)", "Historial de notas y llamadas por cliente", "Cero suscripciones mensuales: corre en tu equipo"],
    },
    {
        "cat": "ventas",
        "cat_name": "VENTAS & CONVERSIÓN",
        "color": "#818CF8",
        "icon": "📋",
        "slug": "generador-cotizaciones",
        "name": "Generador Profesional de Cotizaciones",
        "problem": "Enviar propuestas en Word o texto plano proyecta informalidad y reduce la tasa de cierre.",
        "benefit": "Crea cotizaciones elegantes y profesionales con logotipo, términos comerciales y descarga en PDF.",
        "features": ["Cálculo automático de ítems, descuentos y total", "Validez de la oferta y condiciones de pago", "Descarga instantánea en PDF limpio y formal"],
    },
    {
        "cat": "ventas",
        "cat_name": "VENTAS & CONVERSIÓN",
        "color": "#818CF8",
        "icon": "📄",
        "slug": "creador-facturas-proforma",
        "name": "Creador de Facturas Proforma",
        "problem": "Los clientes corporativos exigen una proforma detallada antes de emitir la orden de compra.",
        "benefit": "Emite facturas proforma estandarizadas con desglose tributario y datos bancarios para pago.",
        "features": ["Campos para emisor, cliente y cuenta de abono", "Generación local segura sin subir datos a servidores", "Formato listo para imprimir o enviar por correo"],
    },
    {
        "cat": "ventas",
        "cat_name": "VENTAS & CONVERSIÓN",
        "color": "#818CF8",
        "icon": "📱",
        "slug": "generador-codigos-qr",
        "name": "Generador de Códigos QR Empresariales",
        "problem": "Los generadores de QR comerciales caducan o cobran mensualidades sorpresa tras pocas lecturas.",
        "benefit": "Genera códigos QR de alta resolución permanentes para URLs, WhatsApp directo, Wi-Fi o vCard.",
        "features": ["Sin vencimiento ni redirecciones de terceros", "Exportación en formato PNG y SVG de alta nitidez", "Personalización de color y niveles de corrección"],
    },
    {
        "cat": "ventas",
        "cat_name": "VENTAS & CONVERSIÓN",
        "color": "#818CF8",
        "icon": "🛡️",
        "slug": "guiones-manejo-objeciones",
        "name": "ObjeciónPro: Guiones de Venta",
        "problem": "«Está muy caro», «Tengo que consultarlo», «La competencia es más barata»: objeciones que frenan ventas.",
        "benefit": "Biblioteca interactiva con respuestas empáticas, tácticas de reencuadre y argumentos de valor.",
        "features": ["Respuestas listas para copiar y personalizar", "Clasificación por tipo de objeción", "Modo práctica para entrenar a tu equipo"],
    },

    # 4. Legal
    {
        "cat": "legal",
        "cat_name": "LEGAL & BLINDAJE",
        "color": "#F59E0B",
        "icon": "⚖️",
        "slug": "generador-contratos-servicios",
        "name": "Generador de Contratos de Servicios",
        "problem": "Trabajar de palabra expone a tu negocio a impagos, entregables infinitos y litigios.",
        "benefit": "Redacta un contrato formal de prestación de servicios con cláusulas de alcance, hitos y pagos.",
        "features": ["Definición de penalidades y propiedad intelectual", "Cláusulas de confidencialidad y rescisión", "Exportación en borrador editable"],
    },
    {
        "cat": "legal",
        "cat_name": "LEGAL & BLINDAJE",
        "color": "#F59E0B",
        "icon": "🔄",
        "slug": "generador-politicas-devolucion",
        "name": "Generador de Políticas de Devolución",
        "problem": "La falta de reglas claras de garantía causa reclamos y malas reseñas en redes sociales.",
        "benefit": "Genera una política de cambios, garantías y devoluciones alineada a la realidad de tu comercio.",
        "features": ["Plazos y condiciones para cambio de producto", "Gestión de costos de envío en devoluciones", "Texto listo para insertar en tu tienda online"],
    },
    {
        "cat": "legal",
        "cat_name": "LEGAL & BLINDAJE",
        "color": "#F59E0B",
        "icon": "📜",
        "slug": "generador-politicas-terminos",
        "name": "LegalForge: Términos y Privacidad",
        "problem": "Operar una web sin política de privacidad y términos viola normativas de protección de datos.",
        "benefit": "Crea borradores de Términos de Servicio y Políticas de Privacidad adaptados a sitios Pyme.",
        "features": ["Cobertura de cookies y tratamiento de datos", "Limitación de responsabilidad y propiedad intelectual", "Formato web estructurado"],
    },

    # 5. Operaciones
    {
        "cat": "operaciones",
        "cat_name": "OPERACIONES & LOGÍSTICA",
        "color": "#EC4899",
        "icon": "📦",
        "slug": "inventario-compras-pymes",
        "name": "Gestión de Inventario y Compras",
        "problem": "El desabastecimiento frena pedidos y el exceso de stock inmoviliza tu capital de trabajo.",
        "benefit": "Control de stock mínimo, alertas tempranas de reposición y registro de proveedores.",
        "features": ["Alerta automática de productos por agotarse", "Historial de entradas y salidas de almacén", "Filtros rápidos por categoría y proveedor"],
    },
    {
        "cat": "operaciones",
        "cat_name": "OPERACIONES & LOGÍSTICA",
        "color": "#EC4899",
        "icon": "🚚",
        "slug": "calculadora-flete-envio-local",
        "name": "Calculadora de Flete y Envíos",
        "problem": "Calcular mal el costo de despacho local termina absorbiendo la ganancia del producto.",
        "benefit": "Estima el flete por peso volumétrico, distancia, tipo de vehículo y paradas de entrega.",
        "features": ["Cálculo automático de peso volumétrico", "Recargos por zonas difíciles o paradas extra", "Generador de manifiesto de despacho"],
    },
    {
        "cat": "operaciones",
        "cat_name": "OPERACIONES & LOGÍSTICA",
        "color": "#EC4899",
        "icon": "☁️",
        "slug": "simulador-tco-fisico-nube",
        "name": "Simulador TCO: Servidor Físico vs Nube",
        "problem": "¿Conviene comprar un servidor local o migrar a la nube (AWS/Azure/Google Cloud)?",
        "benefit": "Compara el Costo Total de Propiedad a 3 y 5 años incluyendo hardware, energía, soporte y licencias.",
        "features": ["Análisis de Capex vs Opex", "Cálculo del punto de equilibrio financiero", "Gráfico comparativo de costos acumulados"],
    },

    # 6. Productividad
    {
        "cat": "productividad",
        "cat_name": "PRODUCTIVIDAD & EQUIPO",
        "color": "#06B6D4",
        "icon": "✅",
        "slug": "tareas-proyectos-pymes",
        "name": "Gestión de Tareas y Proyectos",
        "problem": "Las tareas pendientes quedan en el olvido si el equipo no tiene visibilidad de las prioridades.",
        "benefit": "Tablero Kanban ligero para mover tareas de «Pendiente» a «En Progreso» y «Terminado».",
        "features": ["Etiquetas de prioridad (Urgente, Alta, Normal)", "Asignación de responsables y fechas límite", "Guardado local seguro en el navegador"],
    },
    {
        "cat": "productividad",
        "cat_name": "PRODUCTIVIDAD & EQUIPO",
        "color": "#06B6D4",
        "icon": "⚡",
        "slug": "conversor-optimizador-imagenes",
        "name": "WebP Forge: Optimizador de Imágenes",
        "problem": "Imágenes pesadas hacen que tu página cargue lento y aumentan el porcentaje de rebote.",
        "benefit": "Convierte imágenes a formato WebP moderno y comprime su peso hasta un 80% sin pérdida perceptible.",
        "features": ["Procesamiento 100% en tu navegador (privado)", "Ajuste manual de calidad y resolución", "Soporta JPG, PNG y WebP"],
    },
    {
        "cat": "productividad",
        "cat_name": "PRODUCTIVIDAD & EQUIPO",
        "color": "#06B6D4",
        "icon": "✉️",
        "slug": "firma-correo-html",
        "name": "Diseñador de Firmas de Correo HTML",
        "problem": "Firmas mal diseñadas que se deforman en celulares dañan la imagen de seriedad de tu empresa.",
        "benefit": "Diseña una firma con foto, logo, redes sociales y teléfonos que se ve perfecta en Gmail y Outlook.",
        "features": ["Compatibilidad móvil garantizada", "Copia en 1 clic para pegar en tu correo", "Diseño corporativo minimalista"],
    },
    {
        "cat": "productividad",
        "cat_name": "PRODUCTIVIDAD & EQUIPO",
        "color": "#06B6D4",
        "icon": "🔐",
        "slug": "generador-contrasenas-pymes",
        "name": "SecuKey: Contraseñas Seguras",
        "problem": "Usar la misma contraseña en correos y bancos es la causa #1 de hackeos en pequeñas empresas.",
        "benefit": "Genera contraseñas criptográficamente seguras con longitud y caracteres personalizados.",
        "features": ["Medidor de entropía y fortaleza en tiempo real", "Sin conexión: generadas en memoria RAM local", "Generación en lote para equipos de trabajo"],
    },
    {
        "cat": "productividad",
        "cat_name": "PRODUCTIVIDAD & EQUIPO",
        "color": "#06B6D4",
        "icon": "🎨",
        "slug": "generador-paletas-corporativas",
        "name": "Chroma: Paletas de Color Corporativas",
        "problem": "Elegir colores al azar produce marcas inconsistentes y textos ilegibles.",
        "benefit": "Crea esquemas de color profesionales a partir de un color base con verificación de contraste WCAG.",
        "features": ["Armonías cromáticas (análogas, complementarias)", "Códigos HEX, RGB y HSL listos para copiar", "Indicador de accesibilidad y contraste"],
    },
]


def build_slides_html() -> str:
    """Construye el documento HTML con 28 diapositivas listas para imprimir en PDF."""
    slides_html = []

    # SLIDE 1: PORTADA
    slides_html.append("""
    <div class="slide cover-slide">
      <div class="glow-bg"></div>
      <div class="slide-content">
        <div class="badge-tag">GUÍA VISUAL Y CATÁLOGO ESTRATÉGICO 2026</div>
        <h1 class="cover-title">26 Herramientas Gratuitas de Gestión para Pymes</h1>
        <p class="cover-subtitle">Sin suscripciones mensuales. Sin necesidad de registro. 100% privadas y ejecutadas localmente en tu navegador.</p>
        
        <div class="cover-pillars-grid">
          <div class="pillar-box"><span class="icon">📣</span><strong>Marketing</strong>5 Herramientas</div>
          <div class="pillar-box"><span class="icon">💰</span><strong>Finanzas</strong>5 Herramientas</div>
          <div class="pillar-box"><span class="icon">💼</span><strong>Ventas</strong>5 Herramientas</div>
          <div class="pillar-box"><span class="icon">⚖️</span><strong>Legal</strong>3 Herramientas</div>
          <div class="pillar-box"><span class="icon">📦</span><strong>Operaciones</strong>3 Herramientas</div>
          <div class="pillar-box"><span class="icon">⚡</span><strong>Productividad</strong>5 Herramientas</div>
        </div>

        <div class="cover-footer">
          <div class="author-block">
            <div class="author-label">Arquitectura y Desarrollo:</div>
            <div class="author-name">Xavier Cabello</div>
            <div class="author-sub">Especialista en Automatización y Software para Pymes</div>
          </div>
          <div class="portal-badge">nubeparapymes.online</div>
        </div>
      </div>
    </div>
    """)

    # SLIDES 2 A 27: LAS 26 HERRAMIENTAS
    for i, t in enumerate(TOOLS_DATA, 1):
        url = f"https://nubeparapymes.online/herramientas/{t['cat']}/{t['slug']}/"
        features_html = "".join(f"<li><span class='check'>✓</span> {feat}</li>" for feat in t["features"])

        slides_html.append(f"""
        <div class="slide tool-slide">
          <div class="slide-header">
            <div class="tool-counter">Herramienta #{i:02d} de 26</div>
            <div class="pillar-badge" style="background-color: {t['color']}22; color: {t['color']}; border-color: {t['color']}55;">
              {t['icon']} {t['cat_name']}
            </div>
          </div>

          <div class="slide-body">
            <h2 class="tool-title">{t['name']}</h2>
            
            <div class="problem-card">
              <div class="card-label">🚨 El problema común en las Pymes:</div>
              <div class="card-text">{t['problem']}</div>
            </div>

            <div class="solution-card">
              <div class="card-label">💡 Cómo te ayuda esta herramienta:</div>
              <div class="card-text">{t['benefit']}</div>
            </div>

            <div class="features-block">
              <div class="features-label">Capacidades destacadas:</div>
              <ul class="features-list">
                {features_html}
              </ul>
            </div>

            <div class="url-card">
              <div class="url-label">Acceso directo sin registro:</div>
              <div class="url-link">🔗 {url}</div>
            </div>
          </div>

          <div class="slide-footer">
            <div class="footer-left">
              <span>Desarrollado por <strong>Xavier Cabello</strong></span> · Nube para Pymes
            </div>
            <div class="footer-right">
              <span>nubeparapymes.online</span>
            </div>
          </div>
        </div>
        """)

    # SLIDE 28: LLAMADA A LA ACCIÓN FINAL
    slides_html.append("""
    <div class="slide cta-slide">
      <div class="glow-bg"></div>
      <div class="slide-content">
        <div class="badge-tag">EMPIEZA HOY MISMO</div>
        <h2 class="cta-title">Digitaliza tu negocio sin gastar en software complejo</h2>
        <p class="cta-text">Todas las 26 herramientas están disponibles gratis de manera indefinida. Diseñadas para que dueños de pequeñas empresas y equipos tomen el control de sus finanzas, ventas y operaciones.</p>

        <div class="cta-benefits">
          <div class="benefit-item">
            <span class="icon">🔒</span>
            <div><strong>100% Privacidad</strong>Tus datos contables y clientes no se envían a ningún servidor externo.</div>
          </div>
          <div class="benefit-item">
            <span class="icon">⚡</span>
            <div><strong>Cero Instalaciones</strong>Funcionan directamente desde tu navegador en PC o móvil.</div>
          </div>
          <div class="benefit-item">
            <span class="icon">🎁</span>
            <div><strong>Sin Registro Obligatorio</strong>Accede y utilízalas en segundos sin formularios innecesarios.</div>
          </div>
        </div>

        <div class="cta-box">
          <div class="cta-box-label">Explora el catálogo completo en línea:</div>
          <div class="cta-box-url">nubeparapymes.online/herramientas/</div>
        </div>

        <div class="cover-footer" style="margin-top: 40px;">
          <div class="author-block">
            <div class="author-label">Conectemos en LinkedIn:</div>
            <div class="author-name">Xavier Cabello</div>
            <div class="author-sub">Comparte este carrusel con otro emprendedor que lo necesite</div>
          </div>
          <div class="portal-badge">#NubeParaPymes</div>
        </div>
      </div>
    </div>
    """)

    all_slides = "\n".join(slides_html)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Catálogo 26 Herramientas - Nube para Pymes</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #030712;
      color: #F3F4F6;
      -webkit-font-smoothing: antialiased;
    }}
    
    @page {{
      size: 1080px 1350px;
      margin: 0;
    }}

    .slide {{
      width: 1080px;
      height: 1350px;
      max-width: 1080px;
      max-height: 1350px;
      padding: 80px 70px;
      position: relative;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #0B0F19;
      overflow: hidden;
    }}

    /* PORTADA */
    .cover-slide {{
      background: radial-gradient(circle at 80% 20%, #1E1B4B 0%, #0B0F19 70%);
      justify-content: center;
    }}
    .glow-bg {{
      position: absolute;
      top: -150px;
      right: -150px;
      width: 600px;
      height: 600px;
      background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, rgba(99, 102, 241, 0) 70%);
      filter: blur(60px);
      pointer-events: none;
    }}
    .badge-tag {{
      display: inline-block;
      padding: 8px 18px;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      color: #38BDF8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 9999px;
      margin-bottom: 28px;
      font-family: 'Outfit', sans-serif;
    }}
    .cover-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 64px;
      font-weight: 800;
      line-height: 1.15;
      color: #FFFFFF;
      margin-bottom: 24px;
      letter-spacing: -0.02em;
    }}
    .cover-subtitle {{
      font-size: 22px;
      line-height: 1.5;
      color: #94A3B8;
      margin-bottom: 48px;
      max-width: 900px;
    }}
    .cover-pillars-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-bottom: 60px;
    }}
    .pillar-box {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 16px;
      padding: 22px;
      font-size: 15px;
      color: #94A3B8;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .pillar-box .icon {{
      font-size: 28px;
      margin-bottom: 4px;
    }}
    .pillar-box strong {{
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      color: #FFFFFF;
    }}
    .cover-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 36px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .author-block .author-label {{
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #64748B;
      margin-bottom: 4px;
    }}
    .author-block .author-name {{
      font-family: 'Outfit', sans-serif;
      font-size: 24px;
      font-weight: 700;
      color: #38BDF8;
    }}
    .author-block .author-sub {{
      font-size: 14px;
      color: #94A3B8;
    }}
    .portal-badge {{
      font-family: 'Outfit', sans-serif;
      font-size: 18px;
      font-weight: 700;
      color: #F8FAFC;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      padding: 12px 24px;
      border-radius: 12px;
    }}

    /* SLIDE DE HERRAMIENTA */
    .tool-slide {{
      background: linear-gradient(180deg, #0D121F 0%, #080C14 100%);
    }}
    .slide-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 40px;
    }}
    .tool-counter {{
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 700;
      color: #64748B;
      letter-spacing: 1px;
    }}
    .pillar-badge {{
      font-family: 'Outfit', sans-serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 1px;
      padding: 8px 18px;
      border-radius: 9999px;
      border: 1px solid;
    }}
    .slide-body {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .tool-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 50px;
      font-weight: 800;
      line-height: 1.15;
      color: #FFFFFF;
      margin-bottom: 36px;
      letter-spacing: -0.02em;
    }}
    .problem-card {{
      background: rgba(239, 68, 68, 0.06);
      border: 1px solid rgba(239, 68, 68, 0.2);
      border-radius: 18px;
      padding: 24px 28px;
      margin-bottom: 22px;
    }}
    .solution-card {{
      background: rgba(56, 189, 248, 0.06);
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: 18px;
      padding: 24px 28px;
      margin-bottom: 30px;
    }}
    .card-label {{
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
      color: #E2E8F0;
      font-family: 'Outfit', sans-serif;
    }}
    .problem-card .card-label {{ color: #FCA5A5; }}
    .solution-card .card-label {{ color: #7DD3FC; }}
    .card-text {{
      font-size: 20px;
      line-height: 1.5;
      color: #F1F5F9;
    }}
    .features-block {{
      margin-bottom: 36px;
    }}
    .features-label {{
      font-family: 'Outfit', sans-serif;
      font-size: 14px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #94A3B8;
      margin-bottom: 16px;
    }}
    .features-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .features-list li {{
      font-size: 18px;
      color: #CBD5E1;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .features-list .check {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 26px;
      height: 26px;
      background: rgba(16, 185, 129, 0.15);
      color: #10B981;
      border: 1px solid rgba(16, 185, 129, 0.3);
      border-radius: 50%;
      font-weight: 700;
      font-size: 14px;
    }}
    .url-card {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px dashed rgba(255, 255, 255, 0.15);
      border-radius: 16px;
      padding: 18px 24px;
    }}
    .url-label {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #64748B;
      margin-bottom: 4px;
    }}
    .url-link {{
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      color: #38BDF8;
      word-break: break-all;
    }}
    .slide-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 24px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 14px;
      color: #64748B;
    }}
    .slide-footer strong {{
      color: #CBD5E1;
    }}

    /* CTA FINAL */
    .cta-slide {{
      background: radial-gradient(circle at 50% 30%, #1E1B4B 0%, #0B0F19 75%);
      justify-content: center;
    }}
    .cta-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 54px;
      font-weight: 800;
      line-height: 1.2;
      color: #FFFFFF;
      margin-bottom: 24px;
      letter-spacing: -0.02em;
    }}
    .cta-text {{
      font-size: 22px;
      line-height: 1.5;
      color: #94A3B8;
      margin-bottom: 44px;
      max-width: 900px;
    }}
    .cta-benefits {{
      display: flex;
      flex-direction: column;
      gap: 20px;
      margin-bottom: 48px;
    }}
    .benefit-item {{
      display: flex;
      align-items: center;
      gap: 20px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      padding: 20px 24px;
      border-radius: 16px;
      font-size: 17px;
      color: #94A3B8;
    }}
    .benefit-item .icon {{
      font-size: 32px;
    }}
    .benefit-item strong {{
      display: block;
      font-family: 'Outfit', sans-serif;
      font-size: 19px;
      color: #FFFFFF;
      margin-bottom: 2px;
    }}
    .cta-box {{
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.15), rgba(99, 102, 241, 0.15));
      border: 1px solid rgba(56, 189, 248, 0.4);
      padding: 28px 36px;
      border-radius: 20px;
      text-align: center;
    }}
    .cta-box-label {{
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: #E2E8F0;
      margin-bottom: 8px;
      font-weight: 600;
    }}
    .cta-box-url {{
      font-family: 'Outfit', sans-serif;
      font-size: 36px;
      font-weight: 800;
      color: #38BDF8;
      letter-spacing: -0.01em;
    }}
  </style>
</head>
<body>
  {all_slides}
</body>
</html>"""


def find_browser_executable() -> str | None:
    """Busca Google Chrome o Microsoft Edge en rutas estándar de Windows."""
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def export_pdf(html_path: Path, pdf_path: Path) -> bool:
    """Exporta el HTML a PDF usando Chrome o Edge en modo headless."""
    browser = find_browser_executable()
    if not browser:
        print("[ERROR] No se encontró Google Chrome ni Microsoft Edge para exportar el PDF.")
        return False

    print(f"[INFO] Utilizando navegador: {browser}")
    print(f"[INFO] Exportando carrusel PDF de 28 diapositivas a: {pdf_path.name}...")

    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={str(pdf_path)}",
        f"file:///{str(html_path).replace(os.sep, '/')}",
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if res.returncode == 0 and pdf_path.exists() and pdf_path.stat().st_size > 1000:
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            print(f"[ÉXITO] PDF generado correctamente: {pdf_path} ({size_mb:.2f} MB)")
            return True
        else:
            print(f"[WARN] El navegador retornó código {res.returncode}: {res.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Error ejecutando navegador: {e}")
        return False


def print_linkedin_post_copy():
    """Imprime el texto sugerido para acompañar la publicación del carrusel PDF en LinkedIn."""
    copy_text = """
======================================================================
 TEXTO SUGERIDO PARA PUBLICAR EL CARRUSEL EN LINKEDIN (Xavier Cabello)
======================================================================

🚨 El 82% de las pequeñas empresas fracasa por falta de control en su flujo de efectivo, desorden en ventas o cobros tardíos.

La mayoría cree que la solución es pagar cientos de dólares al mes en suscripciones de software complejas que nadie en el equipo termina usando.

Por eso construí y puse a disposición pública este catálogo de 26 herramientas 100% gratuitas, privadas y diseñadas para el día a día de una Pyme:

📊 ¿Qué incluye este catálogo interactivo?
• Finanzas: Flujo de caja proyectado, cálculo de margen e IGV, tabla de amortización de préstamos y sobrecostos laborales.
• Ventas: CRM visual liviano, generador de cotizaciones profesionales y creador de facturas proforma.
• Marketing: Analizador de titulares persuasivos, auditor SEO on-page y consola de enlaces UTM.
• Operaciones y Legal: Control de stock de almacén, calculadora de fletes y generadores de contratos de servicios.
• Productividad: Compresor WebP de imágenes, generador de firmas HTML corporativas y contraseñas seguras.

🔒 Lo más importante:
1. Sin necesidad de registro obligatorio.
2. Cero costos ni suscripciones ocultas.
3. Tus datos nunca salen de tu computadora (se procesan en local en tu navegador).

👉 Desliza el carrusel para ver las 26 herramientas en detalle.
🔗 Pruébalas gratis directamente en: https://nubeparapymes.online/herramientas/

¿Cuál de estas áreas es la que más te quita tiempo hoy en tu negocio? Te leo en los comentarios. 👇

──────────
👨‍💻 Desarrollado por Xavier Cabello · Nube para Pymes
#Pymes #SoftwareEmpresarial #Productividad #FinanzasPyme #VentasB2B #TransformacionDigital #Emprendimiento #XavierCabello #NubeParaPymes
======================================================================
"""
    print(copy_text)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    html_content = build_slides_html()
    HTML_FILE.write_text(html_content, encoding="utf-8")
    print(f"[OK] Archivo HTML de diapositivas generado: {HTML_FILE}")

    pdf_ok = export_pdf(HTML_FILE, PDF_FILE)
    if pdf_ok:
        print(f"[OK] El catálogo en PDF está listo para ser subido como documento en LinkedIn.")

    print_linkedin_post_copy()


if __name__ == "__main__":
    main()
