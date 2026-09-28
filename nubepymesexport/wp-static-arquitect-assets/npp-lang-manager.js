/**
 * Nube para Pymes - Universal Language Persistence & Auto-Router
 * Preserves user language preference (EN/ES) across page reloads, tabs, and visits.
 */
(function() {
  'use strict';

  var STORAGE_KEY = 'npp_user_lang';
  var COOKIE_KEY = 'npp_user_lang';
  
  var ES_TO_EN = {
  "ahorrar-horas-trabajo-administrativo": "save-hours-administrative-work",
  "alternativas-excel-control-inventario": "excel-alternatives-inventory-control",
  "alternativas-gratuitas-asana": "free-asana-alternatives",
  "alternativas-gratuitas-notion": "free-notion-alternatives",
  "alternativas-gratuitas-quickbooks": "free-quickbooks-alternatives",
  "alternativas-gratuitas-slack": "free-slack-alternatives",
  "apps-controlar-gastos-negocio": "best-business-expense-tracker-apps",
  "apps-gestion-tareas-freelancers": "task-management-apps-freelancers",
  "automatizacion-ia-pymes-criterios-decision": "ai-automation-smbs-decision-criteria",
  "automatizacion-redes-sociales-ia": "social-media-automation-ai",
  "automatizar-envio-facturas-recordatorios": "automate-invoice-delivery-reminders",
  "automatizar-facturacion-recurrente": "automate-recurring-invoicing",
  "chatbots-ia-pequenos-negocios": "ai-chatbots-small-businesses",
  "chatgpt-atencion-al-cliente": "chatgpt-customer-support-guide",
  "clickup-vs-monday": "clickup-vs-monday-comparison",
  "control-horarios-equipos-remotos": "time-tracking-remote-teams",
  "crear-tablero-kanban-desde-cero": "build-kanban-board-from-scratch",
  "crm-alternativas-gratuitas-salesforce": "free-salesforce-crm-alternatives",
  "crm-como-elegir-un-crm-segun-tamano-empresa": "how-to-choose-crm-by-company-size",
  "crm-con-ia-para-pymes-que-automatizar": "ai-crm-for-smbs-what-to-automate",
  "crm-con-whatsapp-integrado": "crm-with-whatsapp-integration",
  "crm-hubspot-vs-zoho-crm": "crm-hubspot-vs-zoho-comparison",
  "crm-integrado-whatsapp-business": "crm-integrated-whatsapp-business",
  "crm-para-freelancers": "crm-for-freelancers",
  "crm-para-inmobiliarias": "crm-for-real-estate",
  "digitalizacion-procesos-pyme-sin-programar": "smb-process-digitization-no-code",
  "digitalizar-procesos-negocio-pequeno": "digitize-small-business-processes",
  "elegir-software-segun-numero-empleados": "choose-software-by-team-size",
  "elegir-software-segun-presupuesto": "choose-software-by-budget",
  "facturacion-electronica-freelancers": "electronic-invoicing-freelancers",
  "facturacion-electronica-mexico": "electronic-invoicing-mexico-guide",
  "facturar-independiente-peru": "freelance-invoicing-peru-guide",
  "firma-electronica-pequenas-empresas": "electronic-signature-small-businesses",
  "geo-para-pymes-respuestas-inteligencia-artificial": "geo-for-smbs-ai-recommendations",
  "gestion-academias-online": "online-academy-management-software",
  "gestion-citas-profesionales-independientes": "appointment-scheduling-independent-professionals",
  "gestion-despachos-abogados": "law-firm-management-software",
  "gestion-proyectos-agencias-creativas": "project-management-creative-agencies",
  "gestion-proyectos-agencias-marketing": "project-management-marketing-agencies",
  "gestion-proyectos-gratis-vs-pago": "free-vs-paid-project-management",
  "gestion-tiendas-online": "ecommerce-store-management-software",
  "google-sheets-vs-software-especializado": "google-sheets-vs-dedicated-software",
  "google-workspace-vs-microsoft-365": "google-workspace-vs-microsoft-365-comparison",
  "herramientas-encuestas-feedback-clientes": "customer-feedback-survey-tools",
  "herramientas-ia-automatizar-tareas": "ai-tools-automate-business-tasks",
  "herramientas-profesores-particulares": "management-tools-private-tutors",
  "herramientas-videollamadas-equipos-remotos": "video-conferencing-remote-teams",
  "ia-contenido-marketing-pymes": "ai-content-creation-smb-marketing",
  "ia-generar-informes-reportes": "ai-business-reports-generation",
  "mejores-crm-gratuitos-espanol": "best-free-crm-platforms",
  "migrar-de-excel-a-un-crm": "how-to-migrate-excel-to-crm",
  "monday-com-vale-la-pena": "monday-com-review-is-it-worth-it",
  "notion-vs-clickup": "notion-vs-clickup-comparison",
  "organizar-equipo-remoto-trello": "manage-remote-teams-trello",
  "plataformas-elearning-vender-cursos": "elearning-platforms-sell-courses",
  "punto-de-venta-restaurantes": "pos-systems-restaurants",
  "que-es-un-crm-para-que-sirve": "what-is-a-crm-guide",
  "reuniones-eficientes-equipos-distribuidos": "efficient-meetings-distributed-teams",
  "seo-geo-para-pymes-visibilidad-ia": "seo-geo-smb-ai-visibility",
  "slack-vs-microsoft-teams": "slack-vs-microsoft-teams-comparison",
  "software-academias-idiomas": "language-school-management-software",
  "software-academias-matematicas": "math-tutoring-center-software",
  "software-contabilidad-pymes": "accounting-software-smbs",
  "software-gimnasios-estudios": "gym-fitness-studio-software",
  "software-local-o-en-la-nube": "on-premise-vs-cloud-software",
  "software-nomina-pymes-latam": "payroll-software-smbs-guide",
  "software-reservas-clinicas": "clinic-appointment-booking-software",
  "trello-vs-asana": "trello-vs-asana-comparison",
  "zapier-vs-make": "zapier-vs-make-comparison",
  "zoom-vs-google-meet": "zoom-vs-google-meet-comparison"
};
  
  var EN_TO_ES = {};
  for (var k in ES_TO_EN) {
    EN_TO_ES[ES_TO_EN[k]] = k;
  }

  var SPECIAL_ES_TO_EN = {
    'sobre-nosotros': 'about-us',
    'herramientas': 'tools',
    'directorio-herramientas': 'tools',
    'blog': 'blog'
  };

  var SPECIAL_EN_TO_ES = {
    'about-us': 'sobre-nosotros',
    'tools': 'herramientas',
    'user-guide': 'herramientas/guia-uso',
    'blog': 'blog'
  };

  function getStoredLang() {
    try {
      var cookieMatch = document.cookie.match(new RegExp('(?:^|; )' + COOKIE_KEY + '=([^;]*)'));
      if (cookieMatch && cookieMatch[1]) {
        return decodeURIComponent(cookieMatch[1]);
      }
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function setStoredLang(lang) {
    try {
      localStorage.setItem(STORAGE_KEY, lang);
      document.cookie = COOKIE_KEY + '=' + encodeURIComponent(lang) + '; path=/; max-age=31536000; SameSite=Lax';
    } catch (e) {}
  }

  var path = window.location.pathname.replace(/^\/+|\/+$/g, '');
  var parts = path ? path.split('/') : [];
  var isEn = (parts.length > 0 && parts[0] === 'en');

  var currentPref = getStoredLang();

  // 1. Detección automática en primera visita (sin preferencia previa guardada)
  if (!currentPref) {
    var userNavLang = (navigator.language || navigator.userLanguage || '').toLowerCase();
    if (userNavLang.startsWith('en')) {
      // Si el navegador es inglés y visita la portada raíz, enrutar a /en/
      if (parts.length === 0 || parts[0] === 'index.html') {
        setStoredLang('en');
        window.location.replace('/en/');
        return;
      }
    }
  } else {
    // 2. Si el usuario TIENE preferencia activa 'en', mantenerlo fijo en inglés
    if (currentPref === 'en' && !isEn) {
      // Usuario está en una ruta en español pero su preferencia es inglés
      var target = '/en/';
      if (parts.length === 0 || parts[0] === 'index.html') {
        target = '/en/';
      } else if (parts[0] in ES_TO_EN) {
        target = '/en/' + ES_TO_EN[parts[0]] + '/';
      } else if (parts[0] in SPECIAL_ES_TO_EN) {
        target = '/en/' + SPECIAL_ES_TO_EN[parts[0]] + '/';
      } else if (parts[0] === 'category' && parts.length > 1) {
        target = '/en/category/' + parts[1] + '/';
      } else if (parts[0] === 'blog') {
        target = '/en/blog/';
      }
      
      if (window.location.pathname !== target) {
        window.location.replace(target);
        return;
      }
    }
  }

  // 3. Capturar clics en selectores de idioma y en enlaces de navegación
  function bindInteractions() {
    document.querySelectorAll('a.np-lang-toggle').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        var href = btn.getAttribute('href') || '';
        if (href.startsWith('/en/') || href === '/en') {
          setStoredLang('en');
        } else {
          setStoredLang('es');
        }
      });
    });

    // Si estamos en versión en inglés, proteger que los clics internos no salgan a español
    if (isEn) {
      document.addEventListener('click', function(e) {
        var a = e.target.closest('a');
        if (!a) return;
        if (a.classList.contains('np-lang-toggle')) return; // Permitir que el botón cambie a español
        
        var href = a.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('http') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
        
        // Si el enlace apunta a /blog/ o /sobre-nosotros/ sin prefijo /en/
        if (href === '/blog/' || href === '/blog') {
          e.preventDefault();
          window.location.href = '/en/blog/';
        } else if (href === '/sobre-nosotros/' || href === '/sobre-nosotros') {
          e.preventDefault();
          window.location.href = '/en/about-us/';
        } else if (href === '/herramientas/' || href === '/directorio-herramientas/') {
          e.preventDefault();
          window.location.href = '/en/tools/';
        } else if (href.startsWith('/category/')) {
          e.preventDefault();
          window.location.href = '/en' + href;
        }
      }, true);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindInteractions);
  } else {
    bindInteractions();
  }
})();
