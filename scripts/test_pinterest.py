import os
import sys
import urllib.error
import urllib.request

token = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PINTEREST_ACCESS_TOKEN", "").strip()

if not token:
    print("Uso: python scripts/test_pinterest.py <TU_TOKEN_DE_PINTEREST>")
    sys.exit(1)

print(f"Probando token con API v5 de Pinterest...")
req = urllib.request.Request("https://api.pinterest.com/v5/user_account", headers={"Authorization": f"Bearer {token}"})
try:
    with urllib.request.urlopen(req) as resp:
        print("ESTADO: 200 OK - ¡Token activo y aplicación aprobada por Pinterest!")
        print(resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8")
    print(f"ESTADO: Error {e.code} - {body}")
    if "consumer type is not supported" in body:
        print("\n-> Tu aplicación todavía está en revisión ('Acceso a Trial pendiente'). Espera a que Pinterest la apruebe.")
