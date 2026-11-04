const $ = s => document.querySelector(s);
const labels = {queued:'En cola',armed:'Habilitada · en espera',executing:'En curso',proposed:'Pendiente de revisión',integrated:'Integrada',rejected:'Rechazada',blocked:'Bloqueada','amendment-pending':'Cambio pendiente'};
let selected = new URLSearchParams(location.search).get('task_id'), paused = false;
async function api(path, options = {}) {
  const response = await fetch(path, {headers:{'Content-Type':'application/json'}, ...options});
  const body = await response.json();
  if (!response.ok) throw new Error(typeof body.detail === 'string' ? body.detail : 'Revisa los campos introducidos.');
  return body;
}
function element(tag, text, className) {const el = document.createElement(tag); el.textContent = text; if (className) el.className = className; return el;}
function lines(value) { return value.split('\n').map(x => x.trim()).filter(Boolean); }
async function load() {
  const [tasks, control] = await Promise.all([api('/api/tasks'), api('/api/control')]); paused = control.paused;
  $('#executor-label').textContent = control.executor === 'simulated' ? 'El ejecutor está simulado.' : control.executor === 'openai-compatible' ? 'Hay un ejecutor de modelo configurado.' : 'Ejecutor desconocido.';
  $('#control-status').textContent = paused ? 'Nuevas ejecuciones pausadas' : 'Nuevas ejecuciones habilitadas';
  $('#control').textContent = paused ? 'Reanudar ejecuciones' : 'Pausar nuevas ejecuciones';
  $('#count').textContent = tasks.length;
  const list = $('#tasks'); list.replaceChildren();
  if (!tasks.length) list.append(element('div','Aún no hay tareas. Crea la primera para empezar.','empty'));
  tasks.forEach(task => {
    const button = element('button', '', 'task');
    const name = element('div', task.title); name.append(element('small', `Tarea · ${task.id.slice(0,8)} · ${task.contract.instance || 'versión anterior'}`));
    button.append(name, element('span', labels[task.status] || task.status, 'status'));
    button.addEventListener('click', () => show(task.id)); list.append(button);
  });
  if (selected) await show(selected);
}
async function show(id) {
  const task = await api('/api/tasks/' + encodeURIComponent(id)); selected = id;
  const d = $('#detail'); d.hidden = false; d.replaceChildren();
  d.append(element('div','03 / REVISIÓN','step'), element('h2',task.title), element('p',labels[task.status] || task.status));
  if (task.legacy) d.append(element('p','Esta tarea fue creada con la versión anterior y está disponible solo para consulta.'));
  if (task.contract.instance) d.append(element('p', `Instancia: ${task.contract.instance} · Serie: ${task.contract.series} · Intento: ${task.attempt}`));
  if (task.contract.scope) d.append(element('p', 'Alcance: ' + task.contract.scope.join(', ')));
  if (task.blocked_reason && task.status === 'blocked') d.append(element('p', 'Motivo: ' + task.blocked_reason));
  if (task.execution.backend) d.append(element('p', 'Ejecución: ' + task.execution.backend + (task.execution.cost_known ? ' · Coste estimado: ' + task.execution.cost_usd.toFixed(6) + ' USD' : ' · Coste pendiente de conciliación')));
  d.append(element('h3','Propuesta'), element('div',task.proposal || 'Todavía no hay propuesta.','proposal'));
  if (task.diff) { d.append(element('h3','Cambios propuestos'), element('div', task.diff, 'proposal diff')); }
  if (Object.keys(task.checks).length) {
    d.append(element('h3','Comprobaciones'));
    const list = element('ul','','checks');
    Object.entries(task.checks).forEach(([name,result]) => list.append(element('li', `${result.passed ? '✓' : '✕'} ${name}: ${result.passed ? 'correcta' : 'fallida'} — ${result.output}`)));
    d.append(list);
  }
  if (task.awaiting_review) {
    const label = element('label','Comentario de revisión (obligatorio para solicitar un cambio)'); label.htmlFor='note';
    const note = document.createElement('textarea'); note.id='note'; note.placeholder='Añade contexto para tu decisión...';
    const actions = element('div','','actions');
    for (const [choice,text,style] of [['approve','Aprobar propuesta',''],['amend','Solicitar cambio','secondary'],['reject','Rechazar','secondary']]) {
      const button = element('button',text,style);
      if (choice === 'approve' && Object.values(task.checks).some(x => !x.passed)) button.disabled = true;
      button.addEventListener('click',async () => {button.disabled=true; try {await api('/api/tasks/'+id+'/review',{method:'POST',body:JSON.stringify({decision:choice,note:note.value})}); await load();} catch(e){alert(e.message);button.disabled=false;}});
      actions.append(button);
    }
    d.append(label,note,actions);
  } else if (task.status === 'queued' && !task.legacy) {
    if (task.review_note) d.append(element('p','Último comentario: ' + task.review_note));
    const button = element('button','Habilitar de nuevo'); button.addEventListener('click', async () => {try {await api('/api/tasks/'+id+'/arm',{method:'POST'});await load();} catch(e){alert(e.message)}}); d.append(button);
  } else if (task.decision) d.append(element('p', 'Comentario: ' + (task.review_note || 'Sin comentario.')));
  d.append(element('h3','Actividad'));
  const events = element('ul','','events'); task.events.forEach(e => events.append(element('li',e))); d.append(events);
}
$('#create').addEventListener('submit', async e => {
  e.preventDefault(); const form=e.currentTarget; const button=form.querySelector('button'); button.disabled=true;
  const criteria = lines($('#criteria').value), scope = lines($('#scope').value), invariants = lines($('#invariants').value);
  const payload = {title:$('#title').value,description:$('#description').value,instance:$('#instance').value,series:$('#series').value || null,invariants};
  if (criteria.length) payload.criteria = criteria; if (scope.length) payload.scope = scope;
  try {const task=await api('/api/tasks',{method:'POST',body:JSON.stringify(payload)}); form.reset(); selected=task.id; await load();}
  catch(error){alert(error.message)} finally {button.disabled=false;}
});
$('#control').addEventListener('click', async () => {try {await api('/api/control/' + (paused ? 'resume' : 'pause'), {method:'POST'});await load();} catch(e){alert(e.message)}});
if(selected){document.querySelector('.layout').style.display='none';document.querySelector('.intro h1').textContent='Revisa la propuesta';const builder=new URLSearchParams(location.search).get('builder');if(builder)document.querySelector('main a').href='/?instance='+encodeURIComponent(builder);}
load().catch(e => {$('#tasks').textContent = 'No se pudieron cargar las tareas: ' + e.message;});
