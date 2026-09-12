import urllib.request
import re

req = urllib.request.Request('https://nubeparapymes.online/herramientas/js/index.js?v=20260912-3', headers={'User-Agent': 'Mozilla/5.0'})
js = urllib.request.urlopen(req).read().decode('utf-8')
slugs = re.findall(r'slug:"([^"]+)"', js)
print(f"Total slugs in live JS: {len(slugs)}")
for s in slugs[:10]:
    print(" ", s)

print("\nChecking live portal HTML:")
req_html = urllib.request.Request('https://nubeparapymes.online/herramientas/', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req_html).read().decode('utf-8')
print("Has Xavier Cabello in live HTML footer:", "juan.cabellorosas.com" in html)
print("Has Guía de uso in live HTML footer:", "Guía de uso" in html)
print("Has new script version in live HTML:", "index.js?v=20260912-3" in html)
