(function(){
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
