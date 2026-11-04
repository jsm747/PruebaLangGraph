const {chromium}=require('playwright');
(async()=>{
 const base=process.env.APF_TEST_URL||'http://127.0.0.1:8000';
 const browser=await chromium.launch({headless:true,...(process.env.APF_CHROMIUM_PATH?{executablePath:process.env.APF_CHROMIUM_PATH}:{})});
 try{
  const page=await browser.newPage({viewport:{width:1024,height:768}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base,{waitUntil:'networkidle'});
  await page.locator('#session-name').fill('Chat de ejemplo');await page.getByRole('button',{name:'Empezar con el Builder'}).click();
  await page.locator('#chat-input').fill('Quiero revisar solicitudes de formación y hoy tardamos demasiado.');
  await page.getByRole('button',{name:'Enviar al Builder',exact:true}).click();
  await page.locator('#chat-log').getByText('¿Cómo se llama el proceso y quién es responsable?',{exact:true}).waitFor();
  if(await page.getByRole('button',{name:'Confirmar tema y continuar'}).count())throw Error('Confirmación prematura');
  await page.locator('#chat-input').fill('Se llama Formación y la responsable es Persona demo.');
  await page.getByRole('button',{name:'Enviar al Builder',exact:true}).click();
  await page.locator('.draft').getByText('Persona demo',{exact:true}).waitFor();
  await page.reload({waitUntil:'networkidle'});
  await page.locator('#chat-log').getByText('Quiero revisar solicitudes de formación y hoy tardamos demasiado.',{exact:true}).waitFor();
  await page.getByRole('button',{name:'Confirmar tema y continuar'}).click();
  await page.getByRole('heading',{name:'1 · Comprobar viabilidad',exact:true}).waitFor();
  await page.locator('#chat-input').fill('Sí, las reglas están en el reglamento europeo Capítulo III, Sección 1, artículo 6, junto con el anexo III.');
  await page.getByRole('button',{name:'Enviar al Builder',exact:true}).click();
  await page.locator('#chat-log').getByText('Registro esa referencia como pendiente de contrastar.',{exact:false}).waitFor();
  await page.locator('.source-notes summary').click();
  await page.locator('.source-notes').getByText('artículo 6',{exact:false}).first().waitFor();
  if(await page.getByRole('button',{name:'Confirmar tema y continuar'}).count())throw Error('La referencia no completa por sí sola la viabilidad');
  if((await page.locator('#chat-log').innerText()).includes('no respeta el tema'))throw Error('La fuente pertinente se ha rechazado por formato');
  await page.reload({waitUntil:'networkidle'});
  await page.locator('.source-notes summary').waitFor();
  await page.screenshot({path:'/tmp/apf-chat-poc.png',fullPage:true});
  await page.setViewportSize({width:390,height:844});
  if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Desbordamiento móvil');
  if(errors.length)throw Error(errors.join('; '));
  console.log('Chat: conversación, confirmación, referencia del AI Act sin rechazo de formato y notas persistentes correctas.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
