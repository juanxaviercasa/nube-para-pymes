import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

REPLACEMENTS_V4 = {
    # Precios Venta e Impuestos
    ">Calculadora<": ">Calculator<",
    ">Margen Inverso<": ">Reverse Margin<",
    ">Comparador<": ">Comparison<",
    ">Kits<": ">Bundle Kits<",
    "Lo que te cuesta adquirir o producir.": "Direct acquisition or production cost.",
    "Impuesto a pagar": "Sales Tax / GST Amount",
    "IGV 18% sobre el neto": "Sales Tax / GST (18%) on net",
    "Fórmula:</span> Precio neto = Costo ÷ (1": "Formula:</span> Net Price = Cost ÷ (1",
    "El impuesto se suma aparte sobre el precio neto.": "Sales tax is calculated separately on net price.",
    "Precio neto: S/": "Net Price: $",
    "Precio neto: ": "Net Price: ",

    # Objeciones
    "Involucra al cliente analítico en su propio proceso lógico y hace visibles las objeciones ocultas para poder resolverlas en el momento.":
    "Engages the analytical buyer in their own logical framework and surfaces hidden objections to resolve immediately.",

    "Introducir urgencia legítima sin manipular. El escéptico valora que reconozcas su derecho a decidir mientras cuantificas el costo de esperar.":
    "Introduces genuine commercial urgency without pressure. Skeptics appreciate respecting their autonomy while calculating the cost of delay.",

    "Reduce el compromiso a un mínimo asumible y usa la escasez de tiempo del cliente como argumento a tu favor, no en tu contra.":
    "Lowers commitment threshold to an easy yes and leverages their limited time as a compelling reason to evaluate efficiency.",

    "Me alegra que ya tengas un proveedor, significa que valoras esto. No te pido que cambies. Te propongo ser tu segundo proveedor para emergencias. Cuando tu proveedor actual te falle, ¿a quién llamas?":
    "\"I'm glad you already have a trusted vendor; that shows you prioritize this. I'm not asking you to switch. I propose being your backup partner for emergencies. When your primary vendor encounters a bottleneck, who do you call?\"",

    "No pelea la objeción, la valida. La prueba social de \"mis mejores clientes decían lo mismo\" reabre la puerta sin confrontación.":
    "Validates the objection rather than debating it. Social proof from similar clients reopens conversation collaboratively.",

    "El costo de no verlo": "The Cost of Inaction",

    "Convierte la falta de tiempo (la objeción) en la razón principal para escuchar, prometiendo devolver ese mismo tiempo multiplicado.":
    "Reframes limited time as the primary reason to listen, promising to return that invested time multiplied.",

    # Paletas Corporativas
    "Paletas que definen marcas , no solo pantallas.": "Color palettes that define enduring brands, not just screens.",
    "Paletas que definen marcas, no solo pantallas.": "Color palettes that define enduring brands, not just screens.",
    "Descargar paleta": "Download Palette",
    "Descargar Paleta": "Download Palette",
    "Exportar paleta": "Export Palette",

    # Inventario y Compras
    ">Empresa<": ">Company<",
    ">Proveedor<": ">Supplier / Vendor<",
    ">Proveedor:<": ">Supplier:<",
    "contactos de compra": "active suppliers",

    # Contratos y Términos
    "en los términos y condiciones siguientes:": "under the following terms and conditions:",
    "términos y condiciones": "terms and conditions",

    # Firma HTML
    "Modo oscuro similar al cliente": "Client Dark Mode Simulation",
    "Calle Gran Vía 28, Madrid": "120 Market Street, Suite 400"
}

files = list(EN_DIR.glob("*.html"))
updated = 0
for f in files:
    content = f.read_text(encoding="utf-8", errors="ignore")
    original = content
    for src, dst in REPLACEMENTS_V4.items():
        if src in content:
            content = content.replace(src, dst)
    if content != original:
        f.write_text(content, encoding="utf-8")
        updated += 1

print(f"Replacements V4 applied across {updated} files in en/!")
