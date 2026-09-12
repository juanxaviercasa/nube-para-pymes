import urllib.request

urls = [
    'https://nubeparapymes.online/',
    'https://nubeparapymes.online/herramientas/',
    'https://nubeparapymes.online/sobre-nosotros/',
    'https://nubeparapymes.online/herramientas/finanzas/calculadora-descuentos-promociones/'
]

print("Verificando despliegue de autor en vivo:")
for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as res:
            html = res.read().decode('utf-8')
            has_author = 'juan.cabellorosas.com' in html
            print(f"  [{res.status}] Enlace juan.cabellorosas.com: {has_author} -> {u}")
    except Exception as e:
        print(f"  ERR {e} -> {u}")
