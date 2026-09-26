import json
import re

SLUG_MAP = {
    'ahorrar-horas-trabajo-administrativo': 'save-hours-administrative-work',
    'alternativas-excel-control-inventario': 'excel-alternatives-inventory-control',
    'alternativas-gratuitas-asana': 'free-asana-alternatives',
    'alternativas-gratuitas-notion': 'free-notion-alternatives',
    'alternativas-gratuitas-quickbooks': 'free-quickbooks-alternatives',
    'alternativas-gratuitas-slack': 'free-slack-alternatives',
    'apps-controlar-gastos-negocio': 'best-business-expense-tracker-apps',
    'apps-gestion-tareas-freelancers': 'task-management-apps-freelancers',
    'automatizacion-ia-pymes-criterios-decision': 'ai-automation-smbs-decision-criteria',
    'automatizacion-redes-sociales-ia': 'social-media-automation-ai',
    'automatizar-envio-facturas-recordatorios': 'automate-invoice-delivery-reminders',
    'automatizar-facturacion-recurrente': 'automate-recurring-invoicing',
    'chatbots-ia-pequenos-negocios': 'ai-chatbots-small-businesses',
    'chatgpt-atencion-al-cliente': 'chatgpt-customer-support-guide',
    'clickup-vs-monday': 'clickup-vs-monday-comparison',
    'control-horarios-equipos-remotos': 'time-tracking-remote-teams',
    'crear-tablero-kanban-desde-cero': 'build-kanban-board-from-scratch',
    'crm-alternativas-gratuitas-salesforce': 'free-salesforce-crm-alternatives',
    'crm-como-elegir-un-crm-segun-tamano-empresa': 'how-to-choose-crm-by-company-size',
    'crm-con-ia-para-pymes-que-automatizar': 'ai-crm-for-smbs-what-to-automate',
    'crm-con-whatsapp-integrado': 'crm-with-whatsapp-integration',
    'crm-hubspot-vs-zoho-crm': 'crm-hubspot-vs-zoho-comparison',
    'crm-integrado-whatsapp-business': 'crm-integrated-whatsapp-business',
    'crm-para-freelancers': 'crm-for-freelancers',
    'crm-para-inmobiliarias': 'crm-for-real-estate',
    'digitalizacion-procesos-pyme-sin-programar': 'smb-process-digitization-no-code',
    'digitalizar-procesos-negocio-pequeno': 'digitize-small-business-processes',
    'elegir-software-segun-numero-empleados': 'choose-software-by-team-size',
    'elegir-software-segun-presupuesto': 'choose-software-by-budget',
    'facturacion-electronica-freelancers': 'electronic-invoicing-freelancers',
    'facturacion-electronica-mexico': 'electronic-invoicing-mexico-guide',
    'facturar-independiente-peru': 'freelance-invoicing-peru-guide',
    'firma-electronica-pequenas-empresas': 'electronic-signature-small-businesses',
    'geo-para-pymes-respuestas-inteligencia-artificial': 'geo-for-smbs-ai-recommendations',
    'gestion-academias-online': 'online-academy-management-software',
    'gestion-citas-profesionales-independientes': 'appointment-scheduling-independent-professionals',
    'gestion-despachos-abogados': 'law-firm-management-software',
    'gestion-proyectos-agencias-creativas': 'project-management-creative-agencies',
    'gestion-proyectos-agencias-marketing': 'project-management-marketing-agencies',
    'gestion-proyectos-gratis-vs-pago': 'free-vs-paid-project-management',
    'gestion-tiendas-online': 'ecommerce-store-management-software',
    'google-sheets-vs-software-especializado': 'google-sheets-vs-dedicated-software',
    'google-workspace-vs-microsoft-365': 'google-workspace-vs-microsoft-365',
    'herramientas-encuestas-feedback-clientes': 'customer-feedback-survey-tools',
    'herramientas-ia-automatizar-tareas': 'ai-tools-automate-business-tasks',
    'herramientas-profesores-particulares': 'management-tools-private-tutors',
    'herramientas-videollamadas-equipos-remotos': 'video-conferencing-remote-teams',
    'ia-contenido-marketing-pymes': 'ai-content-creation-smb-marketing',
    'ia-generar-informes-reportes': 'ai-business-reports-generation',
    'mejores-crm-gratuitos-espanol': 'best-free-crm-platforms',
    'migrar-de-excel-a-un-crm': 'how-to-migrate-excel-to-crm',
    'monday-com-vale-la-pena': 'monday-com-review-is-it-worth-it',
    'notion-vs-clickup': 'notion-vs-clickup-comparison',
    'organizar-equipo-remoto-trello': 'manage-remote-teams-trello',
    'plataformas-elearning-vender-cursos': 'elearning-platforms-sell-courses',
    'punto-de-venta-restaurantes': 'pos-systems-restaurants',
    'que-es-un-crm-para-que-sirve': 'what-is-a-crm-guide',
    'reuniones-eficientes-equipos-distribuidos': 'efficient-meetings-distributed-teams',
    'seo-geo-para-pymes-visibilidad-ia': 'seo-geo-smb-ai-visibility',
    'slack-vs-microsoft-teams': 'slack-vs-microsoft-teams-comparison',
    'software-academias-idiomas': 'language-school-management-software',
    'software-academias-matematicas': 'math-tutoring-center-software',
    'software-contabilidad-pymes': 'accounting-software-smbs',
    'software-gimnasios-estudios': 'gym-fitness-studio-software',
    'software-local-o-en-la-nube': 'on-premise-vs-cloud-software',
    'software-nomina-pymes-latam': 'payroll-software-smbs-guide',
    'software-reservas-clinicas': 'clinic-appointment-booking-software',
    'trello-vs-asana': 'trello-vs-asana-comparison',
    'zapier-vs-make': 'zapier-vs-make-comparison',
    'zoom-vs-google-meet': 'zoom-vs-google-meet-comparison',
}

def verify_mapping():
    with open('scripts/posts_catalog.json', encoding='utf-8') as f:
        catalog = json.load(f)
        
    all_slugs = [p['slug'] for p in catalog]
    missing = [s for s in all_slugs if s not in SLUG_MAP]
    print(f"Total catalog posts: {len(all_slugs)}")
    print(f"Mapped slugs: {len(SLUG_MAP)}")
    print(f"Missing mappings: {len(missing)}")
    if missing:
        print("Missing:", missing)
        
    # Check for duplicate english slugs
    eng_slugs = list(SLUG_MAP.values())
    duplicates = [s for s in eng_slugs if eng_slugs.count(s) > 1]
    if duplicates:
        print("Duplicate english slugs:", set(duplicates))
    else:
        print("All English slugs are unique and valid!")
        
    with open('scripts/posts_slug_map.json', 'w', encoding='utf-8') as f:
        json.dump(SLUG_MAP, f, ensure_ascii=False, indent=2)
    print("Saved mapping to scripts/posts_slug_map.json")

if __name__ == '__main__':
    verify_mapping()
