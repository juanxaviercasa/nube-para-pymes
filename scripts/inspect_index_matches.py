from pathlib import Path
import re

p = Path("en/index.html").read_text(encoding="utf-8")
keywords = [
    r'para pymes', r'herramientas gratuitas', r'descargar', r'guardar',
    r'limpiar', r'selecciona', r'seleccionar', r'elige', r'ejecuta',
    r'calcula', r'calcular', r'compara', r'comparar',
    r'empresa', r'cliente', r'proveedor', r'fecha', r'moneda',
    r'descuento', r'precio', r'ganancia', r'costo', r'impuesto',
    r'sobrecostos', r'prestamo', r'préstamo', r'amortizacion', r'amortización',
    r'contrasenas', r'contraseñas', r'politica', r'política', r'devolucion', r'devolución',
    r'terminos', r'términos', r'objecion', r'objeción', r'guiones',
    r'matriz', r'contenido', r'proforma', r'cotizacion', r'cotización',
    r'firma de correo', r'codigos qr', r'códigos qr', r'paletas',
    r'flujo de caja', r'inventario', r'tareas y proyectos'
]
for kw in keywords:
    matches = list(re.finditer(kw, p, re.IGNORECASE))
    if matches:
        print(f"Keyword '{kw}': {len(matches)} matches")
        for m in matches[:2]:
            start = max(0, m.start() - 30)
            end = min(len(p), m.end() + 30)
            print(f"   Context: {p[start:end]}")
