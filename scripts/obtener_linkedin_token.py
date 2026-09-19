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

    # 3. Verificar específicamente la página oficial de Nube para Pymes (145201650)
    print("\n[INFO] 3. Verificando acceso a la Página Oficial Nube para Pymes (ID: 145201650)...")
    target_org_id = "145201650"
    target_org_urn = f"urn:li:organization:{target_org_id}"
    can_publish_org = False

    try:
        test_req = urllib.request.Request(
            f"https://api.linkedin.com/v2/organizations/{target_org_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            },
            method="GET"
        )
        with urllib.request.urlopen(test_req, timeout=10) as t_resp:
            t_data = json.loads(t_resp.read().decode("utf-8"))
            print(f"  ✓ Confirmado: Acceso a la organización «{t_data.get('localizedName', 'Nube para Pymes')}» (ID: {target_org_id})")
            can_publish_org = True
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"  ⚠️ Tu token no tiene permisos de lectura/administración sobre la organización {target_org_id}.")
            print("     (Asegúrate de marcar 'w_organization_social' al generar el token).")
        else:
            print(f"  ℹ️ Estado de consulta para org {target_org_id}: HTTP {e.code}")
    except Exception as e:
        print(f"  ℹ️ Verificación de org: {e}")

    print("\n=======================================================")
    print(" 🔑 RESUMEN DE CONFIGURACIÓN PARA GITHUB ACTIONS")
    print("=======================================================")
    print(f"1) LINKEDIN_ACCESS_TOKEN")
    print(f"   Valor: {token}\n")

    print("2) LINKEDIN_ORGANIZATION_URN (Página Oficial Nube para Pymes)")
    print(f"   Valor: {target_org_urn}\n")

    if not has_org_permission and not can_publish_org:
        print("⚠️  ATENCIÓN:")
        print("   Este token NO tiene el permiso 'w_organization_social'.")
        print("   Para que LinkedIn te permita publicar en la página de empresa (145201650):")
        print("   1. Entra en https://www.linkedin.com/developers/ a tu app.")
        print("   2. En Settings -> LinkedIn Page, asocia tu página 'https://www.linkedin.com/company/145201650/' y haz clic en Verify.")
        print("   3. En Tools -> Token Generator, marca la casilla 'w_organization_social'.")
        print("   4. Copia el token generado y guárdalo en GitHub Secrets como LINKEDIN_ACCESS_TOKEN.")
    else:
        print("✅ ¡TODO LISTO PARA PUBLICAR EN NUBE PARA PYMES!")
        print("   Guarda este token en GitHub Secrets para publicar directamente en la página de empresa.")

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
