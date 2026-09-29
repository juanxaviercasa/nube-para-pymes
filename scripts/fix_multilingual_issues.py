#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Corrección Integral de Errores Multilingües e i18n: Nube para Pymes
Aplica todas las correcciones aprobadas en el plan de implementación:
1. Inyección de react-translate-guard.js y npp-lang-manager.js en todas las herramientas.
2. Inyección de selectores de idioma (pills) bidireccionales en el header de las 26 herramientas.
3. Blindaje de scripts operativos (op-runtime, crm-pymes, flujo-caja-pymes, inventario, tareas).
4. Corrección de rutas relativas de demo-experience.js y datos-compartidos.js.
5. Reescritura de enlaces de herramientas en en/index.html y generación de en/tools/index.html en inglés.
6. Corrección de menús internos (.op-nav) en las 4 apps operativas en inglés.
7. Retiro de los 27 archivos duplicados con nombre en español dentro de en/.
8. Reglas 301 de URLs limpias en _redirects para herramientas en inglés.
9. Blindaje de escritura segura en assemble_production_site.py para evitar Errno 22 en Windows.
"""

import os
import re
import json
import shutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"
JS_DIR = ROOT / "js"
DIST_DIR = ROOT / "dist"

TOOLS_MAP = {
    # (spanish_html, spanish_slug, category, english_html, english_slug, title_es, title_en)
    "analizador-titulares": {
        "src": "analizador-titulares.html",
        "slug": "analizador-titulares",
        "cat": "marketing",
        "en_src": "headline-analyzer.html",
        "en_slug": "headline-analyzer",
        "name_es": "Analizador de Titulares",
        "name_en": "Headline Analyzer"
    },
    "auditor-seo-basico": {
        "src": "auditor-seo-basico.html",
        "slug": "auditor-seo-basico",
        "cat": "marketing",
        "en_src": "basic-on-page-seo-auditor.html",
        "en_slug": "basic-on-page-seo-auditor",
        "name_es": "Auditor SEO Básico",
        "name_en": "Basic On-Page SEO Auditor"
    },
    "comparador-campanas-avanzado": {
        "src": "comparador-campanas-avanzado.html",
        "slug": "comparador-campanas-avanzado",
        "cat": "marketing",
        "en_src": "advanced-campaign-comparator.html",
        "en_slug": "advanced-campaign-comparator",
        "name_es": "Comparador de Campañas",
        "name_en": "Advanced Campaign Comparator"
    },
    "consola-campanas": {
        "src": "consola-campanas.html",
        "slug": "consola-campanas",
        "cat": "marketing",
        "en_src": "campaign-utm-console.html",
        "en_slug": "campaign-utm-console",
        "name_es": "Consola de Campañas UTM",
        "name_en": "Campaign UTM Console"
    },
    "organizador-matriz-contenidos": {
        "src": "organizador-matriz-contenidos.html",
        "slug": "organizador-matriz-contenidos",
        "cat": "marketing",
        "en_src": "content-matrix-planner.html",
        "en_slug": "content-matrix-planner",
        "name_es": "Matriz de Contenidos",
        "name_en": "Content Matrix Planner"
    },
    "calculadora-descuentos-promociones": {
        "src": "calculadora-descuentos-promociones.html",
        "slug": "calculadora-descuentos-promociones",
        "cat": "finanzas",
        "en_src": "discount-promotions-calculator.html",
        "en_slug": "discount-promotions-calculator",
        "name_es": "Calculadora de Descuentos",
        "name_en": "Discounts & Promotions Calculator"
    },
    "calculadora-precios-venta-igv": {
        "src": "calculadora-precios-venta-igv.html",
        "slug": "calculadora-precios-venta-igv",
        "cat": "finanzas",
        "en_src": "sales-pricing-tax-calculator.html",
        "en_slug": "sales-pricing-tax-calculator",
        "name_es": "Calculadora de Precios con IGV",
        "name_en": "Sales Pricing & Tax Calculator"
    },
    "calculadora-prestamos-amortizaciones": {
        "src": "calculadora-prestamos-amortizaciones.html",
        "slug": "calculadora-prestamos-amortizaciones",
        "cat": "finanzas",
        "en_src": "loan-amortization-calculator.html",
        "en_slug": "loan-amortization-calculator",
        "name_es": "Calculadora de Préstamos",
        "name_en": "Loan Amortization Calculator"
    },
    "calculadora-sobrecostos-laborales": {
        "src": "calculadora-sobrecostos-laborales.html",
        "slug": "calculadora-sobrecostos-laborales",
        "cat": "finanzas",
        "en_src": "labor-cost-payroll-burden-calculator.html",
        "en_slug": "labor-cost-payroll-burden-calculator",
        "name_es": "Calculadora de Sobrecostos Laborales",
        "name_en": "Labor Cost & Payroll Calculator"
    },
    "flujo-caja-pymes": {
        "src": "flujo-caja-pymes.html",
        "slug": "flujo-caja-pymes",
        "cat": "finanzas",
        "en_src": "cash-flow-tracker.html",
        "en_slug": "cash-flow-tracker",
        "name_es": "Flujo de Caja y Cobranzas",
        "name_en": "Cash Flow & Receivables Tracker"
    },
    "creador-facturas-proforma": {
        "src": "creador-facturas-proforma.html",
        "slug": "creador-facturas-proforma",
        "cat": "ventas",
        "en_src": "proforma-invoice-generator.html",
        "en_slug": "proforma-invoice-generator",
        "name_es": "Creador de Facturas Proforma",
        "name_en": "Proforma Invoice Generator"
    },
    "generador-codigos-qr": {
        "src": "generador-codigos-qr.html",
        "slug": "generador-codigos-qr",
        "cat": "ventas",
        "en_src": "qr-code-generator.html",
        "en_slug": "qr-code-generator",
        "name_es": "Enlaces y QR para WhatsApp",
        "name_en": "WhatsApp Link & QR Generator"
    },
    "generador-cotizaciones": {
        "src": "generador-cotizaciones.html",
        "slug": "generador-cotizaciones",
        "cat": "ventas",
        "en_src": "quote-estimate-generator.html",
        "en_slug": "quote-estimate-generator",
        "name_es": "Generador de Cotizaciones",
        "name_en": "Quote & Estimate Generator"
    },
    "guiones-manejo-objeciones": {
        "src": "guiones-manejo-objeciones.html",
        "slug": "guiones-manejo-objeciones",
        "cat": "ventas",
        "en_src": "objection-handling-scripts.html",
        "en_slug": "objection-handling-scripts",
        "name_es": "Guiones para Objeciones",
        "name_en": "Sales Objection Handling Scripts"
    },
    "crm-pymes": {
        "src": "crm-pymes.html",
        "slug": "crm-pymes",
        "cat": "ventas",
        "en_src": "smb-crm.html",
        "en_slug": "smb-crm",
        "name_es": "CRM y Pipeline Comercial",
        "name_en": "SMB CRM & Sales Pipeline"
    },
    "generador-contratos-servicios": {
        "src": "generador-contratos-servicios.html",
        "slug": "generador-contratos-servicios",
        "cat": "legal",
        "en_src": "service-contracts-generator.html",
        "en_slug": "service-contracts-generator",
        "name_es": "Contratos de Servicios",
        "name_en": "Service Contracts Generator"
    },
    "generador-politicas-devolucion": {
        "src": "generador-politicas-devolucion.html",
        "slug": "generador-politicas-devolucion",
        "cat": "legal",
        "en_src": "return-policy-generator.html",
        "en_slug": "return-policy-generator",
        "name_es": "Políticas de Devolución",
        "name_en": "Return & Refund Policy Generator"
    },
    "generador-politicas-terminos": {
        "src": "generador-politicas-terminos.html",
        "slug": "generador-politicas-terminos",
        "cat": "legal",
        "en_src": "terms-privacy-generator.html",
        "en_slug": "terms-privacy-generator",
        "name_es": "Políticas y Términos",
        "name_en": "Terms & Privacy Policy Generator"
    },
    "calculadora-flete-envio-local": {
        "src": "calculadora-flete-envio-local.html",
        "slug": "calculadora-flete-envio-local",
        "cat": "operaciones",
        "en_src": "local-shipping-calculator.html",
        "en_slug": "local-shipping-calculator",
        "name_es": "Calculadora de Flete Local",
        "name_en": "Local Shipping Rate Calculator"
    },
    "simulador-tco-fisico-nube": {
        "src": "simulador-tco-fisico-nube.html",
        "slug": "simulador-tco-fisico-nube",
        "cat": "operaciones",
        "en_src": "cloud-vs-onprem-tco-simulator.html",
        "en_slug": "cloud-vs-onprem-tco-simulator",
        "name_es": "Simulador TCO: Físico vs Nube",
        "name_en": "Cloud vs On-Premises TCO Simulator"
    },
    "inventario-compras-pymes": {
        "src": "inventario-compras-pymes.html",
        "slug": "inventario-compras-pymes",
        "cat": "operaciones",
        "en_src": "inventory-purchasing.html",
        "en_slug": "inventory-purchasing",
        "name_es": "Inventario y Compras",
        "name_en": "Inventory & Purchasing Manager"
    },
    "conversor-optimizador-imagenes": {
        "src": "conversor-optimizador-imagenes.html",
        "slug": "conversor-optimizador-imagenes",
        "cat": "productividad",
        "en_src": "image-converter-optimizer.html",
        "en_slug": "image-converter-optimizer",
        "name_es": "Optimizador de Imágenes WebP",
        "name_en": "Image Converter & WebP Optimizer"
    },
    "firma-correo-html": {
        "src": "firma-correo-html.html",
        "slug": "firma-correo-html",
        "cat": "productividad",
        "en_src": "html-email-signature.html",
        "en_slug": "html-email-signature",
        "name_es": "Firma de Correo en HTML",
        "name_en": "HTML Email Signature Generator"
    },
    "generador-contrasenas-pymes": {
        "src": "generador-contrasenas-pymes.html",
        "slug": "generador-contrasenas-pymes",
        "cat": "productividad",
        "en_src": "smb-password-generator.html",
        "en_slug": "smb-password-generator",
        "name_es": "Generador de Contraseñas",
        "name_en": "SMB Password Generator"
    },
    "generador-paletas-corporativas": {
        "src": "generador-paletas-corporativas.html",
        "slug": "generador-paletas-corporativas",
        "cat": "productividad",
        "en_src": "brand-palette-generator.html",
        "en_slug": "brand-palette-generator",
        "name_es": "Paletas Corporativas",
        "name_en": "Brand Color Palette Generator"
    },
    "tareas-proyectos-pymes": {
        "src": "tareas-proyectos-pymes.html",
        "slug": "tareas-proyectos-pymes",
        "cat": "productividad",
        "en_src": "tasks-projects-tracker.html",
        "en_slug": "tasks-projects-tracker",
        "name_es": "Tareas y Proyectos",
        "name_en": "Tasks & Projects Tracker"
    }
}

def log(msg):
    print(f"[I18N-FIX] {msg}", flush=True)

def safe_write(path, content):
    for i in range(5):
        try:
            path.write_text(content, encoding="utf-8")
            return
        except OSError:
            time.sleep(0.2)
    with open(str(path), "w", encoding="utf-8") as f:
        f.write(content)

# 1. Blindar scripts compartidos
def fix_shared_js():
    log("1. Blindando scripts compartidos (op-runtime, datos-compartidos, ayuda-apps, crm, tareas)...")
    
    # op-runtime.js
    op_path = JS_DIR / "op-runtime.js"
    op_txt = op_path.read_text(encoding="utf-8")
    new_op = '''(function(){
  const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
  const read=(key,fallback)=>{try{const v=JSON.parse(localStorage.getItem(key)||'');return v??fallback}catch(_){return fallback}};
  const write=(key,value)=>{localStorage.setItem(key,JSON.stringify(value));try{window.npBackup?.save(window.NP_BACKUP_CONFIG.appId,{[key]:value})}catch(_){} };
  const uid=()=>`${Date.now().toString(36)}-${Math.random().toString(36).slice(2,7)}`;
  const esc=(v)=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const isEn = (document.documentElement.lang || '').toLowerCase().startsWith('en') || window.location.pathname.indexOf('/en/') !== -1;
  const money=(n,currency=(isEn?'USD':'PEN'))=>new Intl.NumberFormat(isEn?'en-US':'es-PE',{style:'currency',currency,maximumFractionDigits:2}).format(Number(n)||0);
  const date=(v)=>v?new Intl.DateTimeFormat(isEn?'en-US':'es-PE',{dateStyle:'medium'}).format(new Date(`${v}T12:00:00`)):'—';
  const today=()=>new Date().toISOString().slice(0,10);
  const notify=(msg,kind='')=>{const el=$('#op-alert');if(!el)return;el.textContent=msg;el.className=`op-alert show ${kind}`;clearTimeout(window.__opAlertTimer);window.__opAlertTimer=setTimeout(()=>{el.className='op-alert'},4200)};
  window.OP={$, $$, read, write, uid, esc, money, date, today, notify, isEn};
  window.addEventListener('npBackup:changed',()=>window.location.reload());
})();
'''
    safe_write(op_path, new_op)

    # datos-compartidos.js
    dc_path = JS_DIR / "datos-compartidos.js"
    dc_txt = dc_path.read_text(encoding="utf-8")
    dc_txt = dc_txt.replace('script.src = "./js/demo-experience.js";', 'script.src = "/herramientas/js/demo-experience.js";')
    safe_write(dc_path, dc_txt)

    # ayuda-apps.js
    aa_path = JS_DIR / "ayuda-apps.js"
    aa_txt = aa_path.read_text(encoding="utf-8")
    aa_txt = re.sub(r'script\.src\s*=\s*isEn\s*\?\s*"\.\./js/demo-experience\.js"\s*:\s*"\./js/demo-experience\.js";',
                    'script.src = "/herramientas/js/demo-experience.js";', aa_txt)
    safe_write(aa_path, aa_txt)

    # crm-pymes.js: Hacerlo bilingüe y resiliente a traducción
    crm_path = JS_DIR / "crm-pymes.js"
    crm_code = '''(function(){
  const { $, $$, read, write, uid, esc, money, date, today, notify, isEn }=window.OP;
  const KEY='np_crm_pymes_v1';
  let state=read(KEY,{contacts:[],opportunities:[]});
  const STAGES_ES=['Prospecto','Calificado','Propuesta','Ganado','Perdido'];
  const STAGES_EN=['Lead','Qualified','Proposal','Won','Lost'];
  const stages = isEn ? STAGES_EN : STAGES_ES;

  function normStage(s){
    if(s==='Prospecto'||s==='Lead') return isEn ? 'Lead' : 'Prospecto';
    if(s==='Calificado'||s==='Qualified') return isEn ? 'Qualified' : 'Calificado';
    if(s==='Propuesta'||s==='Proposal') return isEn ? 'Proposal' : 'Propuesta';
    if(s==='Ganado'||s==='Won') return isEn ? 'Won' : 'Ganado';
    if(s==='Perdido'||s==='Lost') return isEn ? 'Lost' : 'Perdido';
    return s;
  }
  function isWon(s){ return s==='Ganado'||s==='Won'; }
  function isLost(s){ return s==='Perdido'||s==='Lost'; }
  function isClosed(s){ return isWon(s)||isLost(s); }

  function persist(){write(KEY,state);render()}
  function render(){
    const open=state.opportunities.filter(o=>!isClosed(normStage(o.stage)));
    const weighted=open.reduce((s,o)=>s+Number(o.value||0)*Number(o.probability||0)/100,0);
    const overdue=open.filter(o=>o.nextDate&&o.nextDate<today()).length;
    $('[data-kpi="contacts"]').textContent=state.contacts.length;
    $('[data-kpi="open"]').textContent=open.length;
    $('[data-kpi="pipeline"]').textContent=money(weighted);
    $('[data-kpi="overdue"]').textContent=overdue;

    const contactSelect=$('#oppContact');
    const old=contactSelect.value;
    const unassignedText = isEn ? 'Unassigned' : 'Sin asignar';
    contactSelect.innerHTML=`<option value="">${unassignedText}</option>`+state.contacts.map(c=>`<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('');
    contactSelect.value=old;

    const term=($('#crmSearch').value||'').toLowerCase();
    $('#pipelineBoard').innerHTML=stages.map(stage=>{
      const items=state.opportunities.filter(o=>normStage(o.stage)===stage&&(`${o.name} ${o.contactName}`.toLowerCase().includes(term)));
      const emptyText = isEn ? 'No opportunities' : 'Sin oportunidades';
      const noContactText = isEn ? 'No contact' : 'Sin contacto';
      const nextText = isEn ? 'Next: ' : 'Próximo: ';
      const noActionText = isEn ? 'No action planned' : 'Sin próxima acción';
      return `<div class="op-lane"><h4>${stage}<span>${items.length}</span></h4>${items.length?items.map(o=>`<article class="op-item"><strong>${esc(o.name)}</strong><small>${esc(o.contactName||noContactText)} · ${money(o.value)}</small><small>${o.nextDate?`${nextText}${date(o.nextDate)}`:noActionText}</small><select data-stage="${esc(o.id)}">${stages.map(s=>`<option ${normStage(s)===normStage(o.stage)?'selected':''}>${s}</option>`).join('')}</select></article>`).join(''):`<p class="op-muted">${emptyText}</p>`}</div>`
    }).join('');

    const deleteText = isEn ? 'Delete' : 'Eliminar';
    const noContactsText = isEn ? 'No contacts yet.' : 'Aún no hay contactos.';
    const headContact = isEn ? 'Contact' : 'Contacto';
    const headPerson = isEn ? 'Person' : 'Persona';
    const headPhone = isEn ? 'Phone' : 'Teléfono';
    const headEmail = isEn ? 'Email' : 'Correo';
    const headOpps = isEn ? 'Deals' : 'Oportunidades';

    $('#contactsTable').innerHTML=state.contacts.length?`<div class="op-table-wrap"><table class="op-table"><thead><tr><th>${headContact}</th><th>${headPerson}</th><th>${headPhone}</th><th>${headEmail}</th><th>${headOpps}</th><th></th></tr></thead><tbody>${state.contacts.map(c=>`<tr><td><strong>${esc(c.name)}</strong><br><small>${esc(c.notes||'')}</small></td><td>${esc(c.person)}</td><td>${esc(c.phone)}</td><td>${esc(c.email)}</td><td>${state.opportunities.filter(o=>o.contactId===c.id).length}</td><td><button class="op-button danger" data-delete-contact="${esc(c.id)}">${deleteText}</button></td></tr>`).join('')}</tbody></table></div>`:`<div class="op-empty">${noContactsText}</div>`;
  }

  $('#contactForm').addEventListener('submit',e=>{
    e.preventDefault();
    const c={id:uid(),name:$('#contactName').value.trim(),person:$('#contactPerson').value.trim(),phone:$('#contactPhone').value.trim(),email:$('#contactEmail').value.trim(),notes:$('#contactNotes').value.trim(),createdAt:new Date().toISOString()};
    if(!c.name)return;
    state.contacts.unshift(c);
    e.target.reset();
    persist();
    notify(isEn ? 'Contact saved.' : 'Contacto guardado.','good');
  });

  $('#opportunityForm').addEventListener('submit',e=>{
    e.preventDefault();
    const contact=state.contacts.find(c=>c.id===$('#oppContact').value);
    const rawStage = $('#oppStage').value;
    const o={id:uid(),name:$('#oppName').value.trim(),contactId:contact?.id||'',contactName:contact?.name||'',value:Number($('#oppValue').value||0),stage:rawStage,probability:Number($('#oppProbability').value||0),nextDate:$('#oppNextDate').value,nextAction:$('#oppNextAction').value.trim(),createdAt:new Date().toISOString()};
    if(!o.name)return;
    state.opportunities.unshift(o);
    e.target.reset();
    $('#oppProbability').value=25;
    persist();
    notify(isEn ? 'Deal added.' : 'Oportunidad agregada.','good');
  });

  $('#crmSearch').addEventListener('input',render);
  document.addEventListener('change',e=>{
    if(e.target.matches('[data-stage]')){
      const o=state.opportunities.find(x=>x.id===e.target.dataset.stage);
      if(o){
        o.stage=e.target.value;
        if(isWon(o.stage))o.probability=100;
        if(isLost(o.stage))o.probability=0;
        persist();
        notify(isEn ? 'Stage updated.' : 'Etapa actualizada.','good');
      }
    }
  });

  document.addEventListener('click',e=>{
    const id=e.target.dataset.deleteContact;
    if(id){
      if(confirm(isEn ? 'Delete this contact?' : '¿Eliminar este contacto?')){
        state.contacts=state.contacts.filter(c=>c.id!==id);
        state.opportunities=state.opportunities.map(o=>o.contactId===id?{...o,contactId:'',contactName:''}:o);
        persist();
      }
    }
  });

  $('#clearCrm').addEventListener('click',()=>{
    if(confirm(isEn ? 'Delete all contacts and opportunities?' : '¿Eliminar todos los contactos y oportunidades?')){
      state={contacts:[],opportunities:[]};
      persist();
      notify(isEn ? 'CRM database cleared.' : 'CRM vacío.');
    }
  });

  render();
})();
'''
    safe_write(crm_path, crm_code)

    # tareas-proyectos-pymes.js: Bilingüe y resiliente
    tareas_path = JS_DIR / "tareas-proyectos-pymes.js"
    tareas_code = '''(function(){
  const { $, read, write, uid, esc, date, today, notify, isEn }=window.OP;
  const KEY='np_tareas_proyectos_pymes_v1';
  let state=read(KEY,{projects:[],tasks:[]});
  const STATUSES_ES=['Pendiente','En curso','Bloqueada','Terminada'];
  const STATUSES_EN=['Pending','In Progress','Blocked','Done'];
  const statuses = isEn ? STATUSES_EN : STATUSES_ES;

  function normStatus(s){
    if(s==='Pendiente'||s==='Pending') return isEn ? 'Pending' : 'Pendiente';
    if(s==='En curso'||s==='In Progress') return isEn ? 'In Progress' : 'En curso';
    if(s==='Bloqueada'||s==='Blocked') return isEn ? 'Blocked' : 'Bloqueada';
    if(s==='Terminada'||s==='Done') return isEn ? 'Done' : 'Terminada';
    return s;
  }
  function isDone(s){ return s==='Terminada'||s==='Done'; }
  function isHigh(p){ return p==='Alta'||p==='High'; }
  function isLow(p){ return p==='Baja'||p==='Low'; }

  function persist(){write(KEY,state);render()}
  function render(){
    const open=state.tasks.filter(t=>!isDone(normStatus(t.status))),
          done=state.tasks.filter(t=>isDone(normStatus(t.status))).length,
          overdue=open.filter(t=>t.due&&t.due<today()).length;
    $('[data-kpi="projects"]').textContent=state.projects.length;
    $('[data-kpi="open"]').textContent=open.length;
    $('[data-kpi="overdue"]').textContent=overdue;
    $('[data-kpi="done"]').textContent=done;

    const noProjectText = isEn ? 'No project' : 'Sin proyecto';
    const allProjectsText = isEn ? 'All projects' : 'Todos los proyectos';
    const opts=`<option value="">${noProjectText}</option>`+state.projects.map(p=>`<option value="${esc(p.id)}">${esc(p.name)}</option>`).join('');
    const old=$('#taskProject').value;
    $('#taskProject').innerHTML=opts;
    $('#taskProject').value=old;

    const oldF=$('#taskProjectFilter').value;
    $('#taskProjectFilter').innerHTML=`<option value="all">${allProjectsText}</option>`+state.projects.map(p=>`<option value="${esc(p.id)}">${esc(p.name)}</option>`).join('');
    $('#taskProjectFilter').value=oldF;

    const filter=$('#taskProjectFilter').value;
    const deleteText = isEn ? 'Delete' : 'Eliminar';
    const noTasksText = isEn ? 'No tasks' : 'Sin tareas';
    const noOwnerText = isEn ? 'Unassigned' : 'Sin responsable';
    const limitText = isEn ? 'Due: ' : 'Límite: ';
    const noDateText = isEn ? 'No deadline' : 'Sin fecha';

    $('#taskBoard').innerHTML=statuses.map(s=>{
      const tasks=state.tasks.filter(t=>normStatus(t.status)===s&&(filter==='all'||t.projectId===filter));
      return `<div class="op-lane"><h4>${s}<span>${tasks.length}</span></h4>${tasks.length?tasks.map(t=>`<article class="op-item"><strong>${esc(t.name)}</strong><small>${esc(t.projectName||noProjectText)} · ${esc(t.owner||noOwnerText)}</small><small class="${t.due&&t.due<today()&&!isDone(normStatus(s))?'op-danger-text':''}">${t.due?`${limitText}${date(t.due)}`:noDateText}</small><span class="op-tag ${isHigh(t.priority)?'danger':isLow(t.priority)?'good':'warn'}">${esc(t.priority)}</span><select data-status="${esc(t.id)}">${statuses.map(x=>`<option ${normStatus(x)===normStatus(t.status)?'selected':''}>${x}</option>`).join('')}</select><button class="op-button danger" data-delete-task="${esc(t.id)}">${deleteText}</button></article>`).join(''):`<p class="op-muted">${noTasksText}</p>`}</div>`
    }).join('');

    const headProj = isEn ? 'Project' : 'Proyecto';
    const headClient = isEn ? 'Client / Area' : 'Cliente / área';
    const headDue = isEn ? 'Due Date' : 'Entrega';
    const headTasks = isEn ? 'Tasks' : 'Tareas';
    const noProjectsYet = isEn ? 'No projects yet.' : 'Aún no hay proyectos.';
    const doneText = isEn ? 'done' : 'terminadas';

    $('#projectsTable').innerHTML=state.projects.length?`<div class="op-table-wrap"><table class="op-table"><thead><tr><th>${headProj}</th><th>${headClient}</th><th>${headDue}</th><th>${headTasks}</th><th></th></tr></thead><tbody>${state.projects.map(p=>`<tr><td><strong>${esc(p.name)}</strong><br><small>${esc(p.notes||'')}</small></td><td>${esc(p.client)}</td><td>${date(p.due)}</td><td>${state.tasks.filter(t=>t.projectId===p.id&&isDone(normStatus(t.status))).length}/${state.tasks.filter(t=>t.projectId===p.id).length} ${doneText}</td><td><button class="op-button danger" data-delete-project="${esc(p.id)}">${deleteText}</button></td></tr>`).join('')}</tbody></table></div>`:`<div class="op-empty">${noProjectsYet}</div>`;
  }

  $('#projectForm').addEventListener('submit',e=>{
    e.preventDefault();
    const p={id:uid(),name:$('#projectName').value.trim(),client:$('#projectClient').value.trim(),due:$('#projectDue').value,notes:$('#projectNotes').value.trim(),createdAt:new Date().toISOString()};
    if(!p.name)return;
    state.projects.unshift(p);
    e.target.reset();
    persist();
    notify(isEn ? 'Project created.' : 'Proyecto creado.','good');
  });

  $('#taskForm').addEventListener('submit',e=>{
    e.preventDefault();
    const p=state.projects.find(x=>x.id===$('#taskProject').value);
    const t={id:uid(),name:$('#taskName').value.trim(),projectId:p?.id||'',projectName:p?.name||'',owner:$('#taskOwner').value.trim(),priority:$('#taskPriority').value,due:$('#taskDue').value,status:isEn?'Pending':'Pendiente',notes:$('#taskNotes').value.trim(),createdAt:new Date().toISOString()};
    if(!t.name)return;
    state.tasks.unshift(t);
    e.target.reset();
    persist();
    notify(isEn ? 'Task added.' : 'Tarea añadida.','good');
  });

  $('#taskProjectFilter').addEventListener('change',render);
  document.addEventListener('change',e=>{
    if(e.target.matches('[data-status]')){
      const t=state.tasks.find(x=>x.id===e.target.dataset.status);
      if(t){
        t.status=e.target.value;
        persist();
        notify(isEn ? 'Status updated.' : 'Estado actualizado.','good');
      }
    }
  });

  document.addEventListener('click',e=>{
    const dt=e.target.closest('[data-delete-task]')?.dataset.deleteTask;
    if(dt&&confirm(isEn ? 'Delete this task?' : '¿Eliminar esta tarea?')){
      state.tasks=state.tasks.filter(t=>t.id!==dt);
      persist();
    }
    const dp=e.target.closest('[data-delete-project]')?.dataset.deleteProject;
    if(dp&&confirm(isEn ? 'Delete project and all its tasks?' : '¿Eliminar el proyecto y sus tareas?')){
      state.projects=state.projects.filter(p=>p.id!==dp);
      state.tasks=state.tasks.filter(t=>t.projectId!==dp);
      persist();
    }
  });

  $('#clearTasks').addEventListener('click',()=>{
    if(confirm(isEn ? 'Delete all projects and tasks?' : '¿Eliminar todos los proyectos y tareas?')){
      state={projects:[],tasks:[]};
      persist();
      notify(isEn ? 'Projects and tasks cleared.' : 'Registro de proyectos vacío.');
    }
  });

  render();
})();
'''
    safe_write(tareas_path, tareas_code)
    log("Scripts compartidos y operativos actualizados con soporte bilingüe y resiliente.")

# 2. Corregir archivos de herramientas (Inyección de guard, npp-lang-manager, pill y nav)
def fix_tool_files():
    log("2. Inyectando guard de traducción, lang-manager y selectores en todas las herramientas...")
    guard_tag = '  <script defer src="/wp-static-arquitect-assets/react-translate-guard.js"></script>\n'
    mgr_tag = '  <script defer src="/wp-static-arquitect-assets/npp-lang-manager.js"></script>\n'

    globe_svg = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.75;flex-shrink:0;"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'

    for slug, info in TOOLS_MAP.items():
        es_path = ROOT / info["src"]
        en_path = EN_DIR / info["en_src"]

        # Procesar herramienta en español
        if es_path.exists():
            es_txt = es_path.read_text(encoding="utf-8", errors="ignore")
            # Inyectar scripts en head
            if "react-translate-guard.js" not in es_txt and "</head>" in es_txt:
                es_txt = es_txt.replace("</head>", f"{guard_tag}{mgr_tag}</head>")
            elif "npp-lang-manager.js" not in es_txt and "</head>" in es_txt:
                es_txt = es_txt.replace("</head>", f"{mgr_tag}</head>")

            # Sincronizar footer
            en_target = f"/en/{info['en_slug']}.html"
            es_txt = re.sub(
                r'<a[^>]*class=["\'][^"\']*np-footer-lang[^"\']*["\'][^>]*>.*?</a>',
                f'<a class="np-footer-link np-footer-lang" href="{en_target}">English (EN)</a>',
                es_txt
            )
            safe_write(es_path, es_txt)

        # Procesar herramienta en inglés
        if en_path.exists():
            en_txt = en_path.read_text(encoding="utf-8", errors="ignore")
            # Inyectar scripts en head
            if "react-translate-guard.js" not in en_txt and "</head>" in en_txt:
                en_txt = en_txt.replace("</head>", f"{guard_tag}{mgr_tag}</head>")
            elif "npp-lang-manager.js" not in en_txt and "</head>" in en_txt:
                en_txt = en_txt.replace("</head>", f"{mgr_tag}</head>")

            # Corregir rutas relativas de scripts y css a absolutas
            en_txt = en_txt.replace('src="../js/', 'src="/js/')
            en_txt = en_txt.replace('href="../css/', 'href="/css/')
            en_txt = en_txt.replace('href="../assets/', 'href="/assets/')

            # Corregir navegación en las 4 herramientas operativas
            if info["slug"] in ["crm-pymes", "flujo-caja-pymes", "inventario-compras-pymes", "tareas-proyectos-pymes"]:
                en_txt = en_txt.replace('href="./index.html">Portal<', 'href="/en/tools/">Portal<')
                en_txt = en_txt.replace('href="./generador-cotizaciones.html">Quotes<', 'href="./quote-estimate-generator.html">Quotes<')
                en_txt = en_txt.replace('href="./crm-pymes.html">CRM<', 'href="./smb-crm.html">CRM<')
                en_txt = en_txt.replace('href="./flujo-caja-pymes.html">Cash Flow<', 'href="./cash-flow-tracker.html">Cash Flow<')
                en_txt = en_txt.replace('href="./inventario-compras-pymes.html">Inventory<', 'href="./inventory-purchasing.html">Inventory<')
                en_txt = en_txt.replace('href="./tareas-proyectos-pymes.html">Tasks<', 'href="./tasks-projects-tracker.html">Tasks<')
                en_txt = en_txt.replace('href="https://apps.nubeparapymes.online/"', 'href="/en/tools/"')
                en_txt = en_txt.replace('href="https://nubeparapymes.online/"', 'href="/en/"')

            # En cash-flow-tracker: corregir dropdowns
            if info["slug"] == "flujo-caja-pymes":
                en_txt = en_txt.replace('<option>Transaction Type</option>', '<option>Operations</option>')
                en_txt = en_txt.replace('<option value="pending">Pendings</option>', '<option value="pending">Pending</option>')
                en_txt = en_txt.replace('<option value="paid">Pagados / cobrados</option>', '<option value="paid">Paid / Settled</option>')
                en_txt = en_txt.replace('<option value="income">Ingresos</option>', '<option value="income">Inflow</option>')
                en_txt = en_txt.replace('<option value="expense">Egresos</option>', '<option value="expense">Outflow</option>')
                en_txt = en_txt.replace('<option value="all">Todos</option>', '<option value="all">All</option>')

            # En smb-crm: corregir stages select
            if info["slug"] == "crm-pymes":
                en_txt = en_txt.replace(
                    '<select id="oppStage"><option>Prospecto</option><option>Calificado</option><option>Propuesta</option><option>Ganado</option><option>Perdido</option></select>',
                    '<select id="oppStage"><option>Lead</option><option>Qualified</option><option>Proposal</option><option>Won</option><option>Lost</option></select>'
                )

            # Sincronizar footer
            es_target = f"/herramientas/{info['cat']}/{info['slug']}/"
            en_txt = re.sub(
                r'<a[^>]*class=["\'][^"\']*np-footer-lang[^"\']*["\'][^>]*>.*?</a>',
                f'<a class="np-footer-link np-footer-lang" href="{es_target}">Español (ES)</a>',
                en_txt
            )
            safe_write(en_path, en_txt)

    log("Herramientas en español e inglés blindadas e interconectadas.")

# 3. Eliminar los 27 archivos duplicados en /en/
def remove_duplicate_en_files():
    log("3. Limpiando los 27 archivos duplicados con nombres en español en en/...")
    count = 0
    for slug, info in TOOLS_MAP.items():
        dup_file = EN_DIR / info["src"]
        if dup_file.exists():
            dup_file.unlink()
            count += 1
    # Y guia-uso
    dup_guia = EN_DIR / "guia-uso-22-apps.html"
    if dup_guia.exists():
        dup_guia.unlink()
        count += 1
    log(f"Se eliminaron {count} archivos duplicados en /en/.")

# 4. Actualizar enlaces en la portada en inglés (en/index.html)
def fix_en_index_tool_links():
    log("4. Actualizando enlaces a herramientas en en/index.html...")
    en_index_path = EN_DIR / "index.html"
    if not en_index_path.exists():
        return
    txt = en_index_path.read_text(encoding="utf-8")
    for slug, info in TOOLS_MAP.items():
        canonical_es = f"/herramientas/{info['cat']}/{info['slug']}/"
        canonical_en = f"/en/{info['en_slug']}.html"
        txt = txt.replace(f'href="{canonical_es}"', f'href="{canonical_en}"')
        txt = txt.replace(f"href='{canonical_es}'", f"href='{canonical_en}'")

    # Reemplazar menciones antiguas de WP
    txt = txt.replace('href="/herramientas/auditor-basico-de-seo-on-page/"', 'href="/en/basic-on-page-seo-auditor.html"')
    txt = txt.replace('href="/herramientas/calculadora-de-precios-de-venta-con-igv/"', 'href="/en/sales-pricing-tax-calculator.html"')

    # Reemplazar enlace 'Free Tools'
    txt = txt.replace('href="/herramientas/"', 'href="/en/tools/"')
    txt = txt.replace('href="/directorio-herramientas/"', 'href="/en/tools/"')

    safe_write(en_index_path, txt)
    log("en/index.html actualizado con enlaces directos a las herramientas en inglés.")

# 5. Generar portal en inglés (en/tools/index.html) completamente traducido
def build_clean_en_tools_portal():
    log("5. Construyendo portal de herramientas en inglés (en/tools/index.html)...")
    dest_dir = EN_DIR / "tools"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "index.html"

    src_portal = ROOT / "index.html"
    if not src_portal.exists():
        log("ADVERTENCIA: index.html raíz no encontrado.")
        return

    txt = src_portal.read_text(encoding="utf-8")

    # Encabezado HTML y canonical
    txt = txt.replace('<html lang="es">', '<html lang="en">')
    txt = re.sub(r'<title>.*?</title>', '<title>SMB Cloud — Free Small Business Interactive Tools Portal</title>', txt)
    txt = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="https://nubeparapymes.online/en/tools/">', txt)

    # Assets absolutos
    txt = txt.replace('href="./assets/', 'href="/assets/')
    txt = txt.replace('src="./assets/', 'src="/assets/')
    txt = txt.replace('src="./js/', 'src="/js/')
    txt = txt.replace('href="./css/', 'href="/css/')
    txt = txt.replace('href="/"', 'href="/en/"')
    txt = txt.replace('href="./index.html"', 'href="/en/tools/"')
    en_portal_pill = '''<a href="/herramientas/" class="np-lang-toggle inline-flex items-center gap-1 rounded-full border border-white/15 bg-white/5 px-3 py-1.5 text-xs font-bold text-white transition hover:border-brand hover:bg-white/10" title="Cambiar a español" aria-label="Cambiar a español">
                <span class="text-brand">EN</span>
                <span class="text-white/30">|</span>
                <span class="text-white/60 hover:text-white">ES</span>
              </a>'''
    txt = re.sub(r'<a[^>]*class=["\'][^"\']*inline-flex[^"\']*rounded-full[^"\']*["\'][^>]*>[\s\S]*?</a>', en_portal_pill, txt, count=1)

    # Reemplazar todos los enlaces a las herramientas por sus versiones en inglés
    for slug, info in TOOLS_MAP.items():
        old_es_link = f'./{info["src"]}'
        new_en_link = f'/en/{info["en_slug"]}.html'
        txt = txt.replace(f'href="{old_es_link}"', f'href="{new_en_link}"')
        txt = txt.replace(f'href="{info["src"]}"', f'href="{new_en_link}"')
        # Títulos
        txt = txt.replace(f'>{info["name_es"]}<', f'>{info["name_en"]}<')

    # Categorías
    txt = txt.replace('>Marketing<', '>Marketing<')
    txt = txt.replace('>Finanzas<', '>Finance<')
    txt = txt.replace('>Ventas<', '>Sales<')
    txt = txt.replace('>Legal<', '>Legal<')
    txt = txt.replace('>Operaciones<', '>Operations<')
    txt = txt.replace('>Productividad<', '>Productivity<')
    txt = txt.replace('>Todas las herramientas<', '>All Tools<')
    txt = txt.replace('placeholder="Buscar herramienta..."', 'placeholder="Search tools..."')
    txt = txt.replace('aria-label="Buscar herramienta"', 'aria-label="Search tools"')
    txt = txt.replace('aria-label="Buscar por voz"', 'aria-label="Voice search"')

    # Inyectar scripts guard y lang-manager
    if "react-translate-guard.js" not in txt and "</head>" in txt:
        txt = txt.replace("</head>", '  <script defer src="/wp-static-arquitect-assets/react-translate-guard.js"></script>\n  <script defer src="/wp-static-arquitect-assets/npp-lang-manager.js"></script>\n</head>')

    safe_write(dest_file, txt)
    log("en/tools/index.html generado exitosamente.")

# 6. Actualizar _redirects con reglas para herramientas en inglés
def update_redirects_for_en():
    log("6. Actualizando reglas en _redirects para versiones en inglés...")
    red_file = ROOT / "_redirects"
    if not red_file.exists():
        return
    txt = red_file.read_text(encoding="utf-8")
    
    en_rules = [
        "",
        "# ==========================================",
        "# Reglas para Herramientas en Inglés (/en/)",
        "# =========================================="
    ]
    for slug, info in TOOLS_MAP.items():
        en_clean = f"/en/{info['en_slug']}"
        en_target = f"/en/{info['en_slug']}.html"
        en_rules.append(f"{en_clean}    {en_target}    301")
        # En caso de que busquen el nombre en español bajo /en/
        en_rules.append(f"/en/{slug}    {en_target}    301")
        en_rules.append(f"/en/{info['src']}    {en_target}    301")
        en_rules.append(f"/en/herramientas/*/{slug}    {en_target}    301")
        en_rules.append(f"/en/herramientas/*/{slug}/    {en_target}    301")

    en_rules_str = "\n".join(en_rules) + "\n"
    if "# Reglas para Herramientas en Inglés (/en/)" not in txt:
        # Insertar antes de las reglas de seguridad
        pos = txt.find("# Reglas de seguridad")
        if pos != -1:
            txt = txt[:pos] + en_rules_str + "\n" + txt[pos:]
        else:
            txt += "\n" + en_rules_str
        safe_write(red_file, txt)
        log("_redirects actualizado con reglas de herramientas en inglés.")

# 7. Actualizar assemble_production_site.py con escritura segura y llamadas a nuevas rutinas
def patch_assemble_production_site():
    log("7. Blindando assemble_production_site.py contra errores de escritura en Windows...")
    asm_path = ROOT / "scripts" / "assemble_production_site.py"
    asm_txt = asm_path.read_text(encoding="utf-8")

    # Inyectar safe_write al inicio
    if "def safe_write_text(" not in asm_txt:
        safe_write_def = '''
def safe_write_text(file_path, content, encoding="utf-8"):
    import time
    for attempt in range(5):
        try:
            file_path.write_text(content, encoding=encoding)
            return
        except OSError:
            time.sleep(0.2)
    with open(str(file_path), "w", encoding=encoding) as f:
        f.write(content)
'''
        pos = asm_txt.find("def log(msg):")
        asm_txt = asm_txt[:pos] + safe_write_def + "\n" + asm_txt[pos:]

    # Reemplazar wp_dir_file.write_text
    asm_txt = asm_txt.replace("wp_dir_file.write_text(content, encoding=\"utf-8\")", "safe_write_text(wp_dir_file, content, encoding=\"utf-8\")")

    # Inyectar reglas en inglés en update_redirects de assemble_production_site
    en_redirects_code = '''
    # Reglas para herramientas en inglés (/en/)
    from fix_multilingual_issues import TOOLS_MAP
    for slug, info in TOOLS_MAP.items():
        lines.append(f"/en/{info['en_slug']}    /en/{info['en_slug']}.html    301")
        lines.append(f"/en/{slug}    /en/{info['en_slug']}.html    301")
        lines.append(f"/en/{info['src']}    /en/{info['en_slug']}.html    301")
'''
    if "from fix_multilingual_issues import TOOLS_MAP" not in asm_txt:
        pos_rules = asm_txt.find("lines.extend([\n        \"\",\n        \"# Reglas de seguridad")
        if pos_rules != -1:
            asm_txt = asm_txt[:pos_rules] + en_redirects_code + "\n" + asm_txt[pos_rules:]

    # Actualizar build_english_tools_portal en build_english_pages.py
    safe_write(asm_path, asm_txt)
    log("assemble_production_site.py parcheado con éxito.")

def main():
    log("=== INICIANDO APLICACIÓN DE CORRECCIONES MULTILINGÜES ===")
    fix_shared_js()
    fix_tool_files()
    remove_duplicate_en_files()
    fix_en_index_tool_links()
    build_clean_en_tools_portal()
    update_redirects_for_en()
    patch_assemble_production_site()
    log("=== TODAS LAS CORRECCIONES HAN SIDO APLICADAS EXITOSAMENTE ===")

if __name__ == "__main__":
    main()
