/* Conversation view for the same persisted Builder graph; no credentials in JS. */
let llmConfig = {enabled:false,ready:false};
async function loadLlmStatus() {
  llmConfig = await api('/api/llm/status');
  let panel = document.querySelector('#llm-configuration');
  if (!panel) {
    panel = el('details','','llm-configuration'); panel.id='llm-configuration';
    document.querySelector('.intro').after(panel);
  }
  panel.replaceChildren();
  const ready=llmConfig.enabled && llmConfig.ready;
  panel.append(el('summary', ready ? `Chat preparado · ${llmConfig.provider} · ${llmConfig.model}` : 'Configurar el chat con OpenAI'));
  panel.append(el('p',ready ? 'La configuración está preparada. La conexión se verifica al enviar un mensaje; no se envían peticiones al consultar este estado.' : llmConfig.message || 'Activa APF_BUILDER=openai-compatible y reinicia el servidor.'));
  panel.append(el('p','En GitHub: tu cuenta → Settings → Codespaces → Secrets → New secret. Crea APF_LLM_API_KEY y autoriza este repositorio. Reinicia el Codespace para recibir el secreto.'));
  panel.append(el('p','La clave permanece en el servidor. El chat usa la API de OpenAI, con su facturación independiente de ChatGPT.'));
  panel.append(el('pre','export APF_LLM_MODEL=gpt-4.1\nbash scripts/start-chat.sh'));
  panel.append(el('p','gpt-4.1 es un ejemplo de modelo: utiliza un identificador disponible en tu proyecto de API. El script comprueba la configuración, pero no verifica acceso al modelo.'));
  panel.append(button('Actualizar estado de configuración',loadLlmStatus,true));
}
function conversation(root,state) {

  const section=el('section','','chat-section');
  section.append(el('h3','Conversación con el Builder'));
  const log=el('div','','chat-log'); log.id='chat-log'; log.setAttribute('role','log'); log.setAttribute('aria-label','Conversación del Builder');
  for(const item of state.history) {
    if(!item.text)continue;
    const msg=el('article','',item.role==='owner'?'chat-message owner-message':'chat-message builder-message');
    msg.append(el('strong',item.role==='owner'?'Tú':'Builder'),el('div',item.text));
    log.append(msg);
  }
  section.append(log);
  if((state.notes||[]).length){
    const notes=el('details','','source-notes');notes.append(el('summary','Fuentes y notas pendientes de verificar'));
    notes.append(el('p','Son borradores de la conversación. El sistema no ha consultado ni verificado estos documentos.'));
    for(const note of state.notes) notes.append(el('p',note.text));
    section.append(notes);
  }
  const form=el('form');form.id='chat-form';
  const label=el('label','Tu mensaje');label.htmlFor='chat-input';
  const input=el('textarea');input.id='chat-input';input.maxLength=12000;input.required=true;
  input.placeholder='Cuéntame con tus palabras lo que necesitas, o responde a la pregunta del Builder…';
  const send=el('button','Enviar al Builder');send.type='submit';
  const status=el('p','','chat-turn-status');status.setAttribute('role','status');status.setAttribute('aria-live','polite');
  if(!llmConfig.ready || !llmConfig.enabled || state.mode!=='openai-compatible'){send.disabled=true;status.textContent='Completa la configuración del LLM y actualiza su estado antes de enviar.';}
  if(['generation','first_run','handover'].includes(state.topic?.id)){send.disabled=true;status.textContent='Este paso requiere la revisión explícita que aparece debajo.';}
  form.append(label,input,send,status);
  form.onsubmit=e=>{e.preventDefault();act(async()=>{
    const text=input.value.trim();if(!text)return;
    send.disabled=true;input.disabled=true;status.textContent='El Builder está preparando su respuesta…';
    try{
      current=await api('/api/builder/'+state.id+'/chat','POST',{revision:state.revision,message:text});
      await render(current);await sessions();
      document.querySelector('#chat-log')?.scrollTo(0,document.querySelector('#chat-log').scrollHeight);
    }finally{send.disabled=false;input.disabled=false;status.textContent='';}
  });};
  section.append(form);root.append(section);requestAnimationFrame(()=>{log.scrollTop=log.scrollHeight;});
}
