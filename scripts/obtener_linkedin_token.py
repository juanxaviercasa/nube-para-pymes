#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asistente de Verificación y Obtención de URN para LinkedIn: Nube para Pymes
Desarrollado para: Xavier Cabello / Nube para Pymes

Verifica la validez de tu Access Token de LinkedIn, detecta si tienes acceso
a tu Página de Empresa (Organization) o Perfil Personal (Person),
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

    print("\n[INFO] 1. Consultando perfil personal en la API de LinkedIn...")
    sub = ""
    name = ""
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

            print(f"  ✓ Identidad confirmada: {name} (Sub ID: {sub})")
    except Exception as e:
        print(f"  ✗ Nota en userinfo: {e}")

    print("\n[INFO] 2. Consultando Páginas de Empresa (Organizaciones) administradas...")
    org_list = []
    has_org_permission = False
    req_org = urllib.request.Request(
        "https://api.linkedin.com/v2/organizationalEntityAcls?q=roleAssignee",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req_org, timeout=15) as resp_org:
            org_data = json.loads(resp_org.read().decode("utf-8"))
            elements = org_data.get("elements", [])
            has_org_permission = True
            for elem in elements:
                target = elem.get("organizationalTarget", "")
                role = elem.get("role", "")
                state = elem.get("state", "")
                if target and state == "APPROVED":
                    # Intentar obtener el nombre de la empresa
                    org_name = ""
                    try:
                        org_id = target.split(":")[-1]
                        name_req = urllib.request.Request(
                            f"https://api.linkedin.com/v2/organizations/{org_id}",
                            headers={
                                "Authorization": f"Bearer {token}",
                                "Content-Type": "application/json",
                                "X-Restli-Protocol-Version": "2.0.0",
                            },
                            method="GET"
                        )
                        with urllib.request.urlopen(name_req, timeout=10) as name_resp:
                            name_data = json.loads(name_resp.read().decode("utf-8"))
                            org_name = name_data.get("localizedName", "")
                    except Exception:
                        pass
                    org_list.append((target, role, org_name))
            print(f"  ✓ Se detectaron {len(org_list)} página(s) de empresa administradas con acceso activo.")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("  ⚠️ El token actual NO tiene permiso 'r_organization_social' ni 'w_organization_social'.")
            print("     Esto significa que tu token solo fue generado con permisos personales ('w_member_social').")
        else:
            print(f"  ℹ️ Respuesta de organizaciones: HTTP {e.code}")
    except Exception as e:
        print(f"  ℹ️ Error consultando organizaciones: {e}")

    print("\n=======================================================")
    print(" 🔑 RESUMEN DE SECRETOS PARA GITHUB ACTIONS")
    print("=======================================================")
    print(f"1) LINKEDIN_ACCESS_TOKEN")
    print(f"   Valor: {token}\n")

    if org_list:
        print("🏢 PARA PUBLICAR EN TU PÁGINA DE EMPRESA (Nube para Pymes):")
        for org_urn, role, org_name in org_list:
            display = f" - «{org_name}»" if org_name else ""
            print(f"2) LINKEDIN_ORGANIZATION_URN{display}")
            print(f"   Valor: {org_urn}")
            print(f"   (Rol de administrador: {role})")
        print("\n3) LINKEDIN_REQUIRE_ORGANIZATION (Recomendado para blindar tu feed personal):")
        print("   Valor: true")
        print("   (Esto garantiza que si falta el URN de empresa, la acción se detendrá antes de tocar tu feed personal).")
    else:
        print("🏢 PARA PUBLICAR EN TU PÁGINA DE EMPRESA (Nube para Pymes):")
        print("   Para que las publicaciones vayan a tu PÁGINA DE EMPRESA y NUNCA a tu feed personal:")
        print("   a) Nombre del secreto: LINKEDIN_ORGANIZATION_URN")
        print("      Valor:              urn:li:organization:<NUMERO_ID_DE_TU_PAGINA>")
        print("   b) Nombre del secreto: LINKEDIN_REQUIRE_ORGANIZATION")
        print("      Valor:              true")
        print("")
        print("   🔍 ¿Cómo obtener el ID numérico de tu página de Nube para Pymes?")
        print("   1. Entra a LinkedIn y ve a administrar tu página 'Nube para Pymes'.")
        print("   2. Revisa la URL en la barra del navegador:")
        print("      https://www.linkedin.com/company/<NUMERO_ID>/admin/...")
        print("      Ese número es el ID (ejemplo: si es 10594321, el URN es urn:li:organization:10594321).")
        print("   3. Si tu URL muestra el nombre slug (ej: linkedin.com/company/nube-para-pymes/admin/):")
        print("      Haz clic derecho en la página -> 'Ver código fuente' y busca 'urn:li:organization:'")
        print("      El número que aparece a continuación es el ID de tu empresa.")
        print("")
        print("   🔐 IMPORTANTE SOBRE EL TOKEN:")
        print("   Para publicar en una página de empresa, tu aplicación de LinkedIn Developers debe tener:")
        print("   - Tu página vinculada en Settings -> LinkedIn Page -> Verify.")
        print("   - En Tools -> Token Generator: marcar el permiso 'w_organization_social'.")

    if sub:
        print("\n👤 PERFIL PERSONAL DETECTADO:")
        print(f"   (URN Personal: urn:li:person:{sub})")
        print("   Nota: Si NO configuras LINKEDIN_REQUIRE_ORGANIZATION=true ni LINKEDIN_ORGANIZATION_URN,")
        print("   el sistema solo podría publicar en este perfil.")

    print("\n📍 Dónde guardar estos secretos:")
    print("   https://github.com/juanxaviercasa/nube-para-pymes/settings/secrets/actions")
    print("=======================================================\n")


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
