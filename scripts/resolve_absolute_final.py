import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

# Generador de cotizaciones
for f in [EN_DIR / "generador-cotizaciones.html", EN_DIR / "quote-estimate-generator.html"]:
    c = f.read_text(encoding="utf-8", errors="ignore")
    c = re.sub(r'text-subtle">Fecha\s+Issue Date</span>', 'text-subtle">Issue Date</span>', c)
    c = re.sub(r'text-subtle">Fecha\s+Expiration Date</span>', 'text-subtle">Expiration Date</span>', c)
    c = re.sub(r'text-subtle">Tipo\s+de Cambio \(S/ por \$\)</span>', 'text-subtle">Exchange Rate</span>', c)
    c = c.replace("Empresa Emisora", "Issuing Business")
    f.write_text(c, encoding="utf-8")

# Brand palette generator
for f in [EN_DIR / "generador-paletas-corporativas.html", EN_DIR / "brand-palette-generator.html"]:
    c = f.read_text(encoding="utf-8", errors="ignore")
    c = c.replace("Paletas que definen marcas , no solo pantallas.", "Color palettes that define brands, not just screens.")
    c = c.replace("Paletas que definen marcas, no solo pantallas.", "Color palettes that define brands, not just screens.")
    c = c.replace("Compilar y descargar tema", "Compile & Download Theme")
    f.write_text(c, encoding="utf-8")

# Advanced campaign comparator
for f in [EN_DIR / "comparador-campanas-avanzado.html", EN_DIR / "advanced-campaign-comparator.html"]:
    c = f.read_text(encoding="utf-8", errors="ignore")
    c = c.replace("Compara, simula, guarda escenarios y genera informes.", "Compare scenarios, simulate KPIs, track benchmarks, and generate reports.")
    f.write_text(c, encoding="utf-8")

# Email signature
for f in [EN_DIR / "firma-correo-html.html", EN_DIR / "html-email-signature.html"]:
    c = f.read_text(encoding="utf-8", errors="ignore")
    c = c.replace("Para: cliente@ejemplo.com", "To: client@example.com")
    f.write_text(c, encoding="utf-8")

# Terms generator
for f in [EN_DIR / "generador-politicas-terminos.html", EN_DIR / "terms-privacy-generator.html"]:
    c = f.read_text(encoding="utf-8", errors="ignore")
    c = re.sub(r'>\s*T[eé\ufffd]rminos\s*<', '>Terms of Service<', c)
    c = re.sub(r'>\s*Aviso Legal\s*<', '>Legal Notice<', c)
    f.write_text(c, encoding="utf-8")

print("Absolute final polish applied!")
