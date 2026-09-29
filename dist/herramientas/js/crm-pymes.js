(function(){
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
