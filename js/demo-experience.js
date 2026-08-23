/* Nube para Pymes — experiencia de demostración local. Los fixtures se identifican como ficticios, conservan una copia de los datos locales y nunca realizan solicitudes externas. */
(() => {
  'use strict';

  const appId = document.body?.dataset?.appId;
  if (!appId) return;

  const CONFIG = {
    'crm-pymes': {
      keys: ['np_crm_pymes_v1'],
      state: {
        contacts: [
          { id: 'demo-c1', name: 'Taller Horizonte (ejemplo)', person: 'Lucía Vega', phone: '999 000 001', email: 'lucia@ejemplo.test', notes: 'Contacto ficticio para mostrar el flujo.', createdAt: '2026-08-01T10:00:00.000Z' },
          { id: 'demo-c2', name: 'Mercado Central (ejemplo)', person: 'Diego Ruiz', phone: '999 000 002', email: 'diego@ejemplo.test', notes: 'Datos locales de demostración.', createdAt: '2026-08-02T10:00:00.000Z' }
        ],
        opportunities: [
          { id: 'demo-o1', name: 'Paquete de gestión mensual', contactId: 'demo-c1', contactName: 'Taller Horizonte (ejemplo)', value: 2400, stage: 'Propuesta', probability: 65, nextDate: '2026-08-28', nextAction: 'Revisar alcance de la propuesta', createdAt: '2026-08-03T10:00:00.000Z' },
          { id: 'demo-o2', name: 'Renovación de servicio', contactId: 'demo-c2', contactName: 'Mercado Central (ejemplo)', value: 1200, stage: 'Calificado', probability: 45, nextDate: '2026-08-30', nextAction: 'Confirmar necesidades', createdAt: '2026-08-04T10:00:00.000Z' }
        ]
      }
    },
    'flujo-caja-pymes': {
      keys: ['np_flujo_caja_pymes_v1'],
      state: { transactions: [
        { id: 'demo-t1', type: 'income', status: 'paid', description: 'Venta de ejemplo', amount: 1850, category: 'Ventas', due: '2026-08-20', party: 'Cliente ficticio', notes: 'Demostración local.', createdAt: '2026-08-20T10:00:00.000Z' },
        { id: 'demo-t2', type: 'expense', status: 'paid', description: 'Compra de insumos', amount: 620, category: 'Operación', due: '2026-08-21', party: 'Proveedor ficticio', notes: 'Demostración local.', createdAt: '2026-08-21T10:00:00.000Z' },
        { id: 'demo-t3', type: 'income', status: 'pending', description: 'Cobro programado', amount: 950, category: 'Ventas', due: '2026-08-29', party: 'Cliente ficticio', notes: 'Ejemplo no real.', createdAt: '2026-08-22T10:00:00.000Z' }
      ] }
    },
    'inventario-compras-pymes': {
      keys: ['np_inventario_compras_pymes_v1'],
      state: {
        products: [
          { id: 'demo-p1', sku: 'EJ-001', name: 'Cuaderno corporativo (ejemplo)', cost: 12.5, price: 24.9, stock: 18, min: 8, createdAt: '2026-08-20T10:00:00.000Z' },
          { id: 'demo-p2', sku: 'EJ-002', name: 'Bolígrafo azul (ejemplo)', cost: 2.2, price: 5.5, stock: 4, min: 8, createdAt: '2026-08-20T10:00:00.000Z' }
        ],
        suppliers: [{ id: 'demo-s1', name: 'Suministros Modelo S.A.C.', person: 'Andrea León', phone: '999 000 003', email: 'proveedor@ejemplo.test', terms: 'Entrega referencial a 7 días.' }],
        movements: [{ id: 'demo-m1', productId: 'demo-p1', type: 'in', qty: 18, date: '2026-08-20', reason: 'Carga de demostración' }],
        purchases: [{ id: 'demo-pc1', productId: 'demo-p1', supplierId: 'demo-s1', qty: 18, cost: 12.5, date: '2026-08-20', note: 'Compra ficticia para la demostración.' }]
      }
    },
    'tareas-proyectos-pymes': {
      keys: ['np_tareas_proyectos_pymes_v1'],
      state: {
        projects: [{ id: 'demo-pr1', name: 'Lanzamiento de catálogo (ejemplo)', client: 'Negocio ficticio', due: '2026-09-05', notes: 'Proyecto local de demostración.', createdAt: '2026-08-20T10:00:00.000Z' }],
        tasks: [
          { id: 'demo-ta1', name: 'Definir productos prioritarios', projectId: 'demo-pr1', projectName: 'Lanzamiento de catálogo (ejemplo)', owner: 'Equipo comercial', priority: 'Alta', due: '2026-08-29', status: 'En curso', notes: 'Ejemplo local.', createdAt: '2026-08-20T10:00:00.000Z' },
          { id: 'demo-ta2', name: 'Revisar material de venta', projectId: 'demo-pr1', projectName: 'Lanzamiento de catálogo (ejemplo)', owner: 'Marketing', priority: 'Media', due: '2026-09-01', status: 'Pendiente', notes: 'Ejemplo local.', createdAt: '2026-08-21T10:00:00.000Z' },
          { id: 'demo-ta3', name: 'Preparar presentación', projectId: 'demo-pr1', projectName: 'Lanzamiento de catálogo (ejemplo)', owner: 'Diseño', priority: 'Baja', due: '2026-08-26', status: 'Terminada', notes: 'Ejemplo local.', createdAt: '2026-08-19T10:00:00.000Z' }
        ]
      }
    }
  };

  const genericValues = {
    email: 'contacto@ejemplo.test', tel: '999 000 000', url: 'https://ejemplo.test', date: '2026-08-30', number: '1250', textarea: 'Ejemplo local y ficticio para mostrar cómo se vería el resultado. Ajusta este contenido con los datos de tu negocio antes de usarlo.', text: 'Ejemplo operativo local'
  };

  const backupKey = `np_demo_backup_${appId}`;
  const genericKey = `np_demo_fields_${appId}`;
  const activeKey = `np_demo_active_${appId}`;
  const profile = CONFIG[appId];
  const isSensitiveAnalysis = new Set(['auditor-seo-basico', 'conversor-optimizador-imagenes']);

  const copy = () => profile
    ? 'Carga datos ficticios de esta herramienta. Tus datos locales actuales se guardan para poder restablecerlos cuando quieras.'
    : isSensitiveAnalysis.has(appId)
      ? 'Prepara un recorrido visual de los campos, sin analizar un sitio, archivo o dato real.'
      : 'Completa valores ficticios locales para mostrar el recorrido y el resultado de la herramienta.';

  const getBody = () => document.body;
  const setStatus = (message, state = '') => {
    const target = document.querySelector('.np-demo-status');
    if (target) { target.textContent = message; target.dataset.state = state; }
  };
  const safeParse = value => { try { return JSON.parse(value); } catch { return null; } };
  const dispatch = el => ['input', 'change', 'blur'].forEach(type => el.dispatchEvent(new Event(type, { bubbles: true })));

  function exampleForField(el) {
    const label = document.querySelector(`label[for="${CSS.escape(el.id || '')}"]`);
    const context = [
      el.closest('.op-field, .field, [class*="field"]')?.textContent,
      el.parentElement?.textContent,
      el.parentElement?.parentElement?.textContent
    ].filter(Boolean).join(' ');
    const hint = `${el.id || ''} ${el.name || ''} ${label?.textContent || ''} ${el.placeholder || ''} ${context}`.toLowerCase();
    if (el.tagName === 'TEXTAREA') return genericValues.textarea;
    if (el.type === 'email') return genericValues.email;
    if (el.type === 'tel') return genericValues.tel;
    if (el.type === 'url') return genericValues.url;
    if (el.type === 'date') return genericValues.date;
    if (el.type === 'number' || el.type === 'range') {
      if (/ruc|identificador/.test(hint)) return '20123456789';
      if (/tipo de cambio|exchange/.test(hint)) return '3.7';
      if (/margen|margin/.test(hint)) return '35';
      if (/igv|iva|impuesto|tax/.test(hint)) return '18';
      if (/descuento|discount/.test(hint)) return '10';
      if (/inter[eé]s|interest|tasa/.test(hint)) return '18';
      if (/plazo|meses|months/.test(hint)) return '12';
      if (/flete|env[ií]o|shipping/.test(hint)) return '25';
      if (/peso|weight/.test(hint)) return '2.5';
      if (/distancia|distance|\bkm\b/.test(hint)) return '12';
      if (/salario|sueldo|remuneraci[oó]n/.test(hint)) return '2400';
      if (/trabajador|employee/.test(hint)) return '3';
      if (/cantidad|qty|unidades|units/.test(hint)) return '12';
      if (/p\.?\s*unit|unitario|unit price/.test(hint)) return '149';
      if (/costo|cost/.test(hint)) return '100';
      if (/precio|price/.test(hint)) return '149';
      if (/presupuesto|budget/.test(hint)) return '1500';
      if (/cpc|clic|click/.test(hint)) return '0.75';
      if (/conversi[oó]n|conversion/.test(hint)) return '3.5';
      return genericValues.number;
    }
    if (/empresa|business|negocio|cliente|client/.test(hint)) return 'Empresa Ejemplo S.A.C.';
    if (/servicio|service|producto|product/.test(hint)) return 'Servicio de demostración';
    if (/ciudad|city/.test(hint)) return 'Lima';
    if (/nombre|name|t[ií]tulo|title/.test(hint)) return 'Proyecto de ejemplo';
    return genericValues.text;
  }

  function injectStylesheet() {
    if (document.querySelector('link[data-np-demo-style]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet'; link.href = './css/demo-experience.css'; link.dataset.npDemoStyle = 'true';
    document.head.append(link);
  }

  function resultTargets() {
    const selector = '[data-result], [data-demo-result], [data-visual-edit-component="ResultCard"], #result, #results, #output, #preview, #quotationPreview, #invoicePreview, #contractPreview, .result, .results, .output, .preview, .op-kpi, .op-pipeline';
    const direct = [...document.querySelectorAll(selector)];
    const semantic = [];
    const resultLanguage = /resultado|precio final|precio de venta|ganancia|impuesto|total|resumen|proyección|cotización|documento generado|contrato/i;
    document.querySelectorAll('strong, span, h2, h3, h4, p, small').forEach(label => {
      if (label.closest('.np-demo-bar, form, .op-form')) return;
      if (/^fórmula:/i.test((label.textContent || '').trim())) return;
      if (!resultLanguage.test(label.textContent || '')) return;
      let candidate = label.parentElement;
      while (candidate && candidate !== document.body) {
        const tag = candidate.tagName.toLowerCase();
        const className = typeof candidate.className === 'string' ? candidate.className : '';
        if (tag === 'article' || tag === 'section' || className.includes('rounded') || className.includes('card') || className.includes('result')) {
          semantic.push(candidate);
          break;
        }
        candidate = candidate.parentElement;
      }
    });
    return [...new Set([...direct, ...semantic])].slice(0, 9);
  }

  function decorateResults() {
    resultTargets().forEach(el => {
      if (!el.matches('.np-demo-bar') && !el.querySelector('input, textarea, select')) el.classList.add('np-demo-result');
    });
    document.querySelectorAll('.op-empty, .empty-state, [data-empty-state]').forEach(empty => {
      if (empty.querySelector('.np-demo-empty-tip')) return;
      const tip = document.createElement('p');
      tip.className = 'np-demo-empty-tip';
      tip.innerHTML = '¿No sabes por dónde empezar? <a href="#np-demo-bar">Carga el ejemplo local</a> y luego reemplázalo por tus propios datos.';
      empty.append(tip);
    });
  }

  function captureFields() {
    const values = {};
    document.querySelectorAll('input, textarea, select').forEach((el, index) => {
      if (!el.id && !el.name) return;
      values[el.id || `field-${index}`] = { value: el.value, checked: el.checked, type: el.type };
    });
    sessionStorage.setItem(genericKey, JSON.stringify(values));
  }

  function setNativeValue(el, value) {
    if (!el) return;
    const prototype = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(prototype, 'value')?.set;
    if (setter) setter.call(el, value); else el.value = value;
    dispatch(el);
  }

  function fieldByContext(pattern) {
    return [...document.querySelectorAll('input, textarea')].find(el => {
      const context = `${el.parentElement?.textContent || ''} ${el.closest('.op-field, .field, [class*="field"]')?.textContent || ''}`;
      return pattern.test(context);
    });
  }

  function fillQuoteExample() {
    captureFields();
    setNativeValue(fieldByContext(/empresa emisora/i), 'Empresa Ejemplo S.A.C.');
    setNativeValue(fieldByContext(/ruc|identificador/i), '20123456789');
    setNativeValue(fieldByContext(/tel[eé]fono.*whatsapp/i), '999 000 010');
    setNativeValue(fieldByContext(/nombre del cliente/i), 'Cliente de demostración');
    setNativeValue(fieldByContext(/correo del cliente/i), 'cliente@ejemplo.test');
    setNativeValue(fieldByContext(/tipo de cambio/i), '3.70');
    const description = document.querySelector('input[placeholder*="Descripción"]');
    const quantity = document.querySelector('input[placeholder="Cant."]');
    const unitPrice = document.querySelector('input[placeholder="0.00"]');
    const discount = document.querySelector('input[placeholder="0%"]');
    setNativeValue(description, 'Paquete de gestión operativa (ejemplo)');
    setNativeValue(quantity, '2');
    setNativeValue(unitPrice, '350');
    setNativeValue(discount, '0');
    document.querySelectorAll('textarea').forEach(textarea => {
      const context = `${textarea.placeholder || ''} ${textarea.parentElement?.textContent || ''}`.toLowerCase();
      setNativeValue(textarea, context.includes('pago') ? '50% de adelanto y 50% contra entrega. Ejemplo local.' : 'Cotización ficticia de demostración. Ajusta condiciones y alcance antes de usarla.');
    });
    getBody().classList.add('np-demo-active');
    window.setTimeout(decorateResults, 80);
    setStatus('Cotización local cargada con un servicio ficticio y total calculado. Ajusta los valores antes de usarla.', 'good');
  }

  function fillGeneric() {
    captureFields();
    document.querySelectorAll('input, textarea, select').forEach((el, index) => {
      if (el.disabled || el.type === 'file' || el.type === 'hidden' || el.closest('.np-demo-bar')) return;
      if (el.tagName === 'SELECT') {
        const option = [...el.options].find(option => option.value && !option.disabled);
        if (option) el.value = option.value;
      } else if (el.type === 'checkbox' || el.type === 'radio') {
        if (index < 3) el.checked = true;
      } else if (!el.value || el.type === 'number' || el.type === 'range') {
        el.value = exampleForField(el);
      }
      dispatch(el);
    });
    getBody().classList.add('np-demo-active');
    setStatus(isSensitiveAnalysis.has(appId) ? 'Recorrido preparado: usa tus propios datos para realizar un análisis real.' : 'Ejemplo local cargado. Revisa el resultado y reemplaza los valores por los de tu negocio.', 'good');
  }

  function restoreGeneric() {
    const saved = safeParse(sessionStorage.getItem(genericKey));
    if (!saved) return false;
    document.querySelectorAll('input, textarea, select').forEach((el, index) => {
      const value = saved[el.id || `field-${index}`];
      if (!value || el.closest('.np-demo-bar')) return;
      el.value = value.value;
      if ('checked' in value) el.checked = value.checked;
      dispatch(el);
    });
    sessionStorage.removeItem(genericKey);
    return true;
  }

  function makeBackup() {
    const current = {};
    profile.keys.forEach(key => { current[key] = localStorage.getItem(key); });
    localStorage.setItem(backupKey, JSON.stringify({ appId, savedAt: new Date().toISOString(), keys: current }));
  }

  function loadProfile() {
    if (localStorage.getItem(backupKey) === null) makeBackup();
    localStorage.setItem(profile.keys[0], JSON.stringify(profile.state));
    sessionStorage.setItem(activeKey, '1');
    location.reload();
  }

  function restoreProfile() {
    const backup = safeParse(localStorage.getItem(backupKey));
    if (!backup?.keys) return false;
    Object.entries(backup.keys).forEach(([key, value]) => value === null ? localStorage.removeItem(key) : localStorage.setItem(key, value));
    localStorage.removeItem(backupKey);
    sessionStorage.removeItem(activeKey);
    location.reload();
    return true;
  }

  function load() {
    if (profile) {
      const existing = safeParse(localStorage.getItem(profile.keys[0]));
      if (existing && !localStorage.getItem(backupKey) && !window.confirm('Este ejemplo local reemplazará temporalmente los datos visibles de esta herramienta. Se guardará una copia local para restablecerla cuando quieras. ¿Continuar?')) return;
      loadProfile();
      return;
    }
    if (appId === 'generador-cotizaciones') {
      fillQuoteExample();
      return;
    }
    fillGeneric();
  }

  function restore() {
    const restored = profile ? restoreProfile() : restoreGeneric();
    if (!profile) {
      getBody().classList.remove('np-demo-active');
      setStatus(restored ? 'Se restablecieron los valores que estaban en este formulario.' : 'No hay un ejemplo activo para restablecer.', restored ? 'good' : 'warning');
    }
  }

  function renderBar() {
    const main = document.querySelector('main, .op-main, .app-main') || document.body;
    if (document.querySelector('.np-demo-bar')) return;
    const bar = document.createElement('section');
    bar.className = 'np-demo-bar'; bar.id = 'np-demo-bar'; bar.setAttribute('aria-label', 'Modo de demostración local');
    bar.innerHTML = `<div class="np-demo-copy"><span class="np-demo-eyebrow">Ejemplo local</span><strong>Explora la herramienta antes de ingresar tus datos.</strong><p>${copy()}</p></div><div class="np-demo-actions"><button class="np-demo-button primary" type="button" data-np-demo-load>Cargar ejemplo</button><button class="np-demo-button" type="button" data-np-demo-reset>Restablecer</button></div>`;
    const status = document.createElement('p'); status.className = 'np-demo-status'; status.setAttribute('aria-live', 'polite');
    main.prepend(status); main.prepend(bar);
    bar.querySelector('[data-np-demo-load]').addEventListener('click', load);
    bar.querySelector('[data-np-demo-reset]').addEventListener('click', restore);
    if (profile && localStorage.getItem(backupKey)) {
      getBody().classList.add('np-demo-active');
      setStatus('Ejemplo local activo. Puedes seguir explorándolo o restablecer tus datos anteriores.', 'good');
    }
  }

  function ensureExperience() {
    injectStylesheet();
    renderBar();
    decorateResults();
  }

  function init() {
    ensureExperience();
    [120, 480, 1100, 2100].forEach(delay => window.setTimeout(ensureExperience, delay));
    const root = document.querySelector('#root, .op-shell') || document.body;
    const observer = new MutationObserver(() => {
      if (!document.querySelector('.np-demo-bar')) ensureExperience();
    });
    observer.observe(root, { childList: true, subtree: true });
    window.setTimeout(() => observer.disconnect(), 2800);
  }
  window.NPDemo = { load, restore, decorateResults };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true }); else init();
})();
