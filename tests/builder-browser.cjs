const {chromium}=require('playwright');
(async()=>{
 const base=process.env.APF_TEST_URL||'http://127.0.0.1:8000';
 const browser=await chromium.launch({headless:true,...(process.env.APF_CHROMIUM_PATH?{executablePath:process.env.APF_CHROMIUM_PATH}:{})});
 try{
  const context=await browser.newContext({viewport:{width:1180,height:900}});
  const page=await context.newPage();let errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base,{waitUntil:'networkidle'});
  await page.locator('#session-name').fill('Proceso sintético de formación');
  await page.getByRole('button',{name:'Empezar con el Builder'}).click();
  const topics=['0 · Entender tu trabajo','1 · Comprobar viabilidad','1b · Perfil piloto','2 · Elegir el camino','3 · Reglas y casos','4 · Personas y controles','5 · Economía y línea base','6 · Conocimiento y revisión'];
  for(const title of topics){
   await page.getByRole('heading',{name:title,exact:true}).waitFor();
   await page.getByRole('button',{name:'Cargar ejemplo sintético para este tema'}).click();
   await page.getByRole('button',{name:'Presentar respuestas',exact:true}).click();
   await page.getByRole('button',{name:'Confirmar tema y continuar'}).click();
  }
  await page.getByRole('heading',{name:'7 · Revisar la instancia generada',exact:true}).waitFor();
  await page.getByRole('button',{name:'He revisado los documentos'}).click();
  await page.getByRole('button',{name:'Confirmar tema y continuar'}).click();
  await page.getByRole('button',{name:'Crear o abrir el caso supervisado'}).click();
  await page.locator('#first-run-link').waitFor();const href=await page.locator('#first-run-link').getAttribute('href');
  const task=await context.newPage();await task.goto(base+href);
  await task.getByRole('button',{name:'Aprobar propuesta'}).click();
  await task.locator('#detail').getByText('Integrada',{exact:true}).waitFor();
  await page.getByRole('button',{name:'Presentar respuestas',exact:true}).click();
  await page.getByRole('button',{name:'Confirmar tema y continuar'}).click();
  await page.getByRole('heading',{name:'9 · Entrega del piloto',exact:true}).waitFor();
  await page.getByRole('button',{name:'Cargar ejemplo sintético para este tema'}).click();
  await page.getByRole('button',{name:'Presentar respuestas',exact:true}).click();
  await page.getByRole('button',{name:'Confirmar tema y continuar'}).click();
  await page.getByRole('heading',{name:'Operar un caso',exact:true}).waitFor();
  await page.locator('#field-observation').fill('Falta contexto en las revisiones.');
  await page.locator('#field-change').fill('Evaluar cómo presentar las fuentes.');
  await page.locator('#field-metric').fill('Casos devueltos por fuente');
  await page.locator('#field-target').fill('Menos de dos casos devueltos');
  const date=new Date();date.setDate(date.getDate()+14);await page.locator('#field-due').fill(date.toISOString().slice(0,10));
  await page.getByRole('button',{name:'Registrar propuesta de mejora'}).click();
  await page.getByPlaceholder('Motivo de tu resolución').fill('Investigar con un proyecto acotado.');
  await page.getByRole('button',{name:'Aprobar proyecto de cambio'}).click();
  await page.getByRole('button',{name:'Abrir encuadre del proyecto de cambio'}).waitFor();
  await page.screenshot({path:'/tmp/apf-builder-poc.png',fullPage:true});
  if(errors.length)throw Error(errors.join('; '));
  const mobile=await context.newPage();await mobile.setViewportSize({width:390,height:844});await mobile.goto(base,{waitUntil:'networkidle'});
  if(await mobile.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Desbordamiento móvil');
  console.log('Builder: configuración, confirmaciones, prueba supervisada, entrega y resolución de mejora verificadas en navegador.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
