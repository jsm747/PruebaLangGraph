const $ = s => document.querySelector(s);
const labels = {queued:'En cola',executing:'En curso',proposed:'Pendiente de revisión',integrated:'Aprobada',rejected:'Rechazada',blocked:'Bloqueada'};
let selected = null;
async function api(path, options = {}) {
  const response = await fetch(path, {headers:{'Content-Type':'application/json'}, ...options});
  const body = await response.json();
  if (!response.ok) throw new Error(typeof body.detail === 'string' ? body.detail : 'Revisa los campos introducidos.');
  return body;
}
function element(tag, text, className) {const el = document.createElement(tag); el.textContent = text; if (className) el.className = className; return el;}
async function load() {
  const tasks = await api('/api/tasks');
  $('#count').textContent = tasks.length;
  const list = $('#tasks'); list.replaceChildren();
  if (!tasks.length) list.append(element('div','Aún no hay tareas. Crea la primera para empezar.','empty'));
  tasks.forEach(task => {
    const button = element('button', '', 'task');
    const name = element('div', task.title); name.append(element('small', `Tarea · ${task.id.slice(0,8)}`));
    button.append(name, element('span', labels[task.status] || task.status, 'status'));
    button.addEventListener('click', () => show(task.id)); list.append(button);
  });
  if (selected) await show(selected);
}
async function show(id) {
  const task = await api('/api/tasks/' + encodeURIComponent(id)); selected = id;
  const d = $('#detail'); d.hidden = false; d.replaceChildren();
  d.append(element('div','03 / REVISIÓN','step'), element('h2',task.title), element('p',labels[task.status] || task.status));
  d.append(element('h3','Propuesta'), element('div',task.proposal || 'Todavía no hay propuesta.','proposal'));
  if (task.awaiting_review) {
    const label = element('label','Comentario de revisión (opcional)'); label.htmlFor='note';
    const note = document.createElement('textarea'); note.id='note'; note.placeholder='Añade contexto para tu decisión...';
    const actions = element('div','','actions');
    for (const [choice,text,style] of [['approve','Aprobar propuesta',''],['reject','Rechazar','secondary']]) {
      const button = element('button',text,style);
      button.addEventListener('click',async () => {button.disabled=true; try {await api('/api/tasks/'+id+'/review',{method:'POST',body:JSON.stringify({decision:choice,note:note.value})}); await load();} catch(e){alert(e.message);button.disabled=false;}});
      actions.append(button);
    }
    d.append(label,note,actions);
  } else if (task.decision) d.append(element('p', 'Comentario: ' + (task.review_note || 'Sin comentario.')));
  d.append(element('h3','Actividad'));
  const events = element('ul','','events'); task.events.forEach(e => events.append(element('li',e))); d.append(events);
}
$('#create').addEventListener('submit', async e => {
  e.preventDefault(); const button=e.currentTarget.querySelector('button'); button.disabled=true;
  try {const task=await api('/api/tasks',{method:'POST',body:JSON.stringify({title:$('#title').value,description:$('#description').value})}); e.currentTarget.reset(); selected=task.id; await load();}
  catch(error){alert(error.message)} finally {button.disabled=false;}
});
load().catch(e => {$('#tasks').textContent = 'No se pudieron cargar las tareas: ' + e.message;});
