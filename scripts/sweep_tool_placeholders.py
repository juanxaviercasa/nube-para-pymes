import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

SWEEPS = {
    # HTML tag text
    ">Costo<": ">Cost<",
    ">Precio<": ">Price<",
    ">Precio:<": ">Price:<",
    ">Descuento<": ">Discount<",
    ">Descuento:<": ">Discount:<",
    ">Cantidad<": ">Quantity<",
    ">Cantidad:<": ">Quantity:<",
    ">Ganancia<": ">Profit<",
    ">Ganancia:<": ">Profit:<",
    ">Impuesto<": ">Tax<",
    ">Impuesto:<": ">Tax:<",
    ">Descuento aplicado<": ">Applied Discount<",
    ">Descuento sugerido<": ">Suggested Discount<",
    ">Margen resultante<": ">Resulting Margin<",
    ">Punto de equilibrio<": ">Break-Even Point<",
    ">PROFORMA<": ">PROFORMA INVOICE<",
    ">Fecha: ": ">Date: ",
    "Documento no fiscal · Proforma sin valor tributario": "Commercial non-fiscal document · Commercial proforma",
    "Ingresa el costo y el precio normal para ver la comparativa de rentabilidad.": "Enter cost and regular price above to view profitability breakdown.",

    # Placeholders & attributes
    'placeholder="Costo"': 'placeholder="Cost"',
    'placeholder="Precio"': 'placeholder="Price"',
    'placeholder="Descuento"': 'placeholder="Discount"',
    'placeholder="Cantidad"': 'placeholder="Quantity"',
    'placeholder="Nombre"': 'placeholder="Name"',
    'placeholder="Empresa"': 'placeholder="Company"',
    'placeholder="Teléfono"': 'placeholder="Phone"',
    'placeholder="Correo"': 'placeholder="Email"',
    'placeholder="Descripción"': 'placeholder="Description"',
    'aria-label="Costo"': 'aria-label="Cost"',
    'aria-label="Precio"': 'aria-label="Price"',
    'aria-label="Descuento"': 'aria-label="Discount"',
    'aria-label="Cantidad"': 'aria-label="Quantity"',

    # Backup labels
    '"label":"Creador de facturas proforma"': '"label":"Proforma Invoice Generator"',
    '"label":"Generador de cotizaciones"': '"label":"Quote & Estimate Generator"',
    '"label":"Organizador de matriz de contenidos"': '"label":"Content Matrix Planner"',
    '"label":"Calculadora de préstamos"': '"label":"Loan & Amortization Calculator"',
    '"label":"Calculadora de sobrecostos laborales"': '"label":"Labor Cost Calculator"',
    '"label":"Calculadora de flete"': '"label":"Local Shipping Calculator"',
    '"label":"Calculadora de precios con IGV"': '"label":"Sales Pricing Calculator"',
    '"label":"Comparador de campañas"': '"label":"Ad Campaign Comparator"',
    '"label":"Consola de campañas"': '"label":"Campaign UTM Console"',
    '"label":"Firma de correo HTML"': '"label":"HTML Email Signature Generator"',
    '"label":"Generador de códigos QR"': '"label":"QR Code Generator"',
    '"label":"Generador de contraseñas"': '"label":"SMB Password Generator"',
    '"label":"Generador de contratos"': '"label":"Service Contract Generator"',
    '"label":"Generador de paletas corporativas"': '"label":"Brand Palette Generator"',
    '"label":"Generador de políticas de devolución"': '"label":"Return Policy Generator"',
    '"label":"Generador de políticas y términos"': '"label":"Terms & Privacy Generator"',
    '"label":"Guiones de manejo de objeciones"': '"label":"Objection Handling Scripts"',
    '"label":"Simulador TCO"': '"label":"TCO Simulator"'
}

files = list(EN_DIR.glob("*.html"))
modified_count = 0
for f in files:
    content = f.read_text(encoding="utf-8", errors="ignore")
    original = content
    for src, dst in SWEEPS.items():
        if src in content:
            content = content.replace(src, dst)
    if content != original:
        f.write_text(content, encoding="utf-8")
        modified_count += 1

print(f"Swept placeholders and labels across {modified_count} files!")
