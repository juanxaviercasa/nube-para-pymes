import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

REPLACEMENTS_V3 = {
    # Form labels & headers
    ">Fecha<": ">Date<",
    ">Fecha:<": ">Date:<",
    ">Moneda<": ">Currency<",
    ">Moneda:<": ">Currency:<",
    ">Cliente<": ">Client<",
    ">Cliente:<": ">Client:<",
    ">Empresa<": ">Company<",
    ">Empresa:<": ">Company:<",
    ">Tu Empresa<": ">Your Company<",
    ">Su Empresa<": ">Your Company<",
    ">Empresa Emisora<": ">Issuing Business<",
    ">Impuesto (%)<": ">Sales Tax / GST (%)<",
    ">Segunda moneda<": ">Secondary Currency<",
    ">Términos<": ">Terms of Service<",
    ">Términos y Condiciones<": ">Terms & Conditions<",
    ">Políticas y Términos<": ">Terms & Policies<",
    ">Documento no fiscal · Proforma sin valor tributario<": ">Commercial Document · Non-Fiscal Proforma<",
    'aria-label="Precio unitario"': 'aria-label="Unit price"',
    'aria-label="Porcentaje de descuento"': 'aria-label="Discount percentage"',
    'placeholder="Mi Empresa SAC"': 'placeholder="Acme Business LLC"',
    'placeholder="Cliente SAC"': 'placeholder="Global Client Inc"',
    'placeholder="cliente@correo.com"': 'placeholder="client@example.com"',
    'placeholder="Buscar por cliente..."': 'placeholder="Search by client..."',
    'placeholder="Buscar por descripción..."': 'placeholder="Search by description..."',
    'placeholder="Buscar cliente..."': 'placeholder="Search client..."',
    "Moneda: Soles (S/)": "Currency: USD ($)",
    "Moneda: Soles": "Currency: USD",

    # Terms & Policies Generator Sample Text
    "El responsable del tratamiento de tus datos personales es [Nombre de la Empresa], con actividad principal a través del sitio web [https://tusitio.com] y sujeto a la legislación vigente en [Country / State Jurisdiction]. Para cualquier consulta relacionada con tus datos puedes contactarnos en [correo@empresa.com].":
    "The data controller responsible for your personal data is [Company Name], operating via [https://yourdomain.com] under the jurisdiction of [Country / State Jurisdiction]. For privacy inquiries, contact us at [support@company.com].",

    "Nuestro sitio [https://tusitio.com] utiliza cookies propias y de terceros para mejorar la experiencia de navegación, analizar el uso del sitio y mostrar contenido relevante. Puedes configurar o rechazar el uso de cookies desde el aviso de cookies o desde la configuración de tu navegador. Al navegar, entendemos que continúas aceptas nuestra política de cookies.":
    "Our website [https://yourdomain.com] uses first-party and third-party cookies to improve browsing experience, analyze site usage, and serve relevant content. You can configure or decline cookies through your browser settings or our cookie banner.",

    "Conservaremos tus datos personales únicamente durante el tiempo necesario para cumplir con las finalidades descritas y las obligaciones legales. [Nombre de la Empresa] no cede tus datos a terceros salvo obligación legal o cuando sea imprescindible para la prestación del servicio (por ejemplo, proveedores de pago o logística).":
    "We retain your personal data only for as long as necessary to fulfill the specified operational purposes and legal requirements. [Company Name] does not sell your personal information to third parties.",

    "Puedes ejercer en cualquier momento tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad de tus datos escribiendo a [correo@empresa.com].":
    "You may exercise your rights to access, rectify, erase, restrict, or port your personal data at any time by contacting [support@company.com].",

    "Si te encuentras en la Unión Europea o el Espacio Económico Europeo, tratamos tus datos de conformidad con el Reglamento General de Protección de Datos (RGPD - UE 2016/679). Bases legales aplicables: tu consentimiento, la ejecución de un contrato, el interés legítimo de [Nombre de la Empresa] y el cumplimiento de obligaciones legales.":
    "If you are located in the European Union or European Economic Area, we process your data in accordance with the General Data Protection Regulation (GDPR - EU 2016/679) and applicable privacy frameworks.",

    "Nos reservamos el derecho de actualizar esta Privacy Policy. Cualquier cambio será publicado en esta":
    "We reserve the right to update this Privacy Policy periodically. Any modifications will be published on this",

    "Si tienes preguntas sobre esta Privacy Policy, puedes contactarnos en [correo@empresa.com].":
    "If you have questions regarding this Privacy Policy, please contact us at [support@company.com]."
}

files = list(EN_DIR.glob("*.html"))
count = 0
for f in files:
    content = f.read_text(encoding="utf-8", errors="ignore")
    modified = False
    for k, v in REPLACEMENTS_V3.items():
        if k in content:
            content = content.replace(k, v)
            modified = True
    if modified:
        f.write_text(content, encoding="utf-8")
        count += 1

print(f"Replacements V3 applied across {count} files!")
