from pathlib import Path
from bs4 import BeautifulSoup
import json

ROOT = Path(__file__).resolve().parents[1]

tools = [
    "analizador-titulares.html",
    "auditor-seo-basico.html",
    "calculadora-descuentos-promociones.html",
    "calculadora-flete-envio-local.html",
    "calculadora-precios-venta-igv.html",
    "calculadora-prestamos-amortizaciones.html",
    "calculadora-sobrecostos-laborales.html",
    "comparador-campanas-avanzado.html",
    "consola-campanas.html",
    "conversor-optimizador-imagenes.html",
    "creador-facturas-proforma.html",
    "crm-pymes.html",
    "firma-correo-html.html",
    "flujo-caja-pymes.html",
    "generador-codigos-qr.html",
    "generador-contrasenas-pymes.html",
    "generador-contratos-servicios.html",
    "generador-cotizaciones.html",
    "generador-paletas-corporativas.html",
    "generador-politicas-devolucion.html",
    "generador-politicas-terminos.html",
    "guiones-manejo-objeciones.html",
    "inventario-compras-pymes.html",
    "organizador-matriz-contenidos.html",
    "simulador-tco-fisico-nube.html",
    "tareas-proyectos-pymes.html"
]

report = {}
for t in tools:
    p = ROOT / t
    soup = BeautifulSoup(p.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    h1 = soup.find("h1")
    h1_text = h1.get_text(strip=True) if h1 else ""
    buttons = [b.get_text(strip=True) for b in soup.find_all("button") if b.get_text(strip=True)]
    labels = [l.get_text(strip=True) for l in soup.find_all("label") if l.get_text(strip=True)]
    placeholders = [i.get("placeholder") for i in soup.find_all(["input", "textarea"]) if i.get("placeholder")]
    report[t] = {
        "title": soup.title.string if soup.title else "",
        "h1": h1_text,
        "buttons_count": len(buttons),
        "sample_buttons": buttons[:6],
        "labels_count": len(labels),
        "sample_labels": labels[:6],
        "placeholders_count": len(placeholders),
        "sample_placeholders": placeholders[:4]
    }

print(json.dumps(report, indent=2, ensure_ascii=False))
