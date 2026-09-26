from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index_file = ROOT / "index.html"
content = index_file.read_text(encoding="utf-8")

fixes = {
    "/herramientas/legal/generador-politicas-devolucion/": "./generador-politicas-devolucion.html",
    "/herramientas/legal/generador-politicas-terminos/": "./generador-politicas-terminos.html",
    "/herramientas/productividad/generador-contrasenas-pymes/": "./generador-contrasenas-pymes.html",
    "/herramientas/legal/generador-contratos-servicios/": "./generador-contratos-servicios.html"
}

for old, new in fixes.items():
    content = content.replace(old, new)

index_file.write_text(content, encoding="utf-8")
print("Fixed remaining 4 links in index.html!")
