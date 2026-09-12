import urllib.request

urls = [
    'https://nubeparapymes.online/herramientas/tareas-proyectos-pymes.html',
    'https://nubeparapymes.online/herramientas/inventario-compras-pymes.html',
    'https://nubeparapymes.online/herramientas/productividad/tareas-proyectos-pymes/',
    'https://nubeparapymes.online/herramientas/operaciones/inventario-compras-pymes/',
    'https://nubeparapymes.online/herramientas/'
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=10)
        print(f"[{res.status}] -> {u}")
        if ".html" in u:
            content = res.read().decode('utf-8')
            has_redirect = "window.location.replace" in content
            print(f"       Contiene redirección JS: {has_redirect}")
    except Exception as e:
        print(f"[ERR {e}] -> {u}")
