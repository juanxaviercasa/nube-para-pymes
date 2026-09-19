#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asistente de Verificación y Obtención de URN para LinkedIn
Desarrollado para: Xavier Cabello / Nube para Pymes

Verifica la validez de tu Access Token de LinkedIn, obtiene tu Person URN oficial
y te muestra exactamente cómo configurarlo en GitHub Secrets.
"""

import json
import os
import sys
import urllib.error
import urllib.request

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def test_token(token: str):
    token = token.strip().strip('"').strip("'")
    if not token:
        print("[ERROR] El token ingresado está vacío.")
        return

    print("\n[INFO] Consultando la API de LinkedIn...")
    req = urllib.request.Request(
        "https://api.linkedin.com/v2/userinfo",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            name = data.get("name", "Usuario de LinkedIn")
            sub = data.get("sub", "")
            email = data.get("email", "No provisto")

            print("\n=======================================================")
            print(" ¡CONEXIÓN CON LINKEDIN EXITOSA! 🎉")
            print("=======================================================")
            print(f"👤 Nombre:    {name}")
            print(f"📧 Correo:    {email}")
            print(f"🆔 Sub ID:    {sub}")
            print(f"\n🔑 TUS SECRETOS PARA GITHUB ACTIONS:")
            print("───────────────────────────────────────────────────────")
            print(f"1) Nombre del secreto: LINKEDIN_ACCESS_TOKEN")
            print(f"   Valor:              {token[:15]}...{token[-10:]} (Usa el token completo)")
            print("")
            print(f"2) Nombre del secreto: LINKEDIN_PERSON_URN")
            print(f"   Valor:              urn:li:person:{sub}")
            print("───────────────────────────────────────────────────────")
            print("\n📍 Dónde colocarlos:")
            print("   Ve a https://github.com/juanxaviercasa/nube-para-pymes/settings/secrets/actions")
            print("   Haz clic en 'New repository secret' y añade ambos valores.")
            print("=======================================================\n")

    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        print(f"\n[ERROR {e.code}] No se pudo validar el token.")
        print(f"Detalle del error: {err_msg}")
        print("\nVerifica que al generar el token hayas marcado los permisos:")
        print("  - w_member_social")
        print("  - openid")
        print("  - profile")
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un fallo al conectar: {e}")


def main():
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    if len(sys.argv) > 1:
        token = sys.argv[1]

    if not token:
        print("=======================================================")
        print(" ASISTENTE DE CREDENCIALES DE LINKEDIN")
        print("=======================================================")
        try:
            token = input("\nPega aquí tu Access Token de LinkedIn y presiona Enter: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada.")
            return

    test_token(token)


if __name__ == "__main__":
    main()
