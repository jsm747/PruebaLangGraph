import io
import json
import httpx
import os
import tempfile
import unittest
import zipfile
from datetime import date,timedelta
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.env=patch.dict(os.environ,{'APF_DATA_DIR':self.tmp.name,'APF_BUILDER':'guided','APF_EXECUTOR':'simulated'})
        self.env.start()
    def tearDown(self):
        self.env.stop();self.tmp.cleanup()
    def start(self,c):
        r=c.post('/api/builder',json={'name':'Demo de formación'})
        self.assertEqual(r.status_code,201,r.text);return r.json()
    def present(self,c,s,answers=None):
        if answers is None: answers=s['example']
        r=c.post(f"/api/builder/{s['id']}/answer",json={'revision':s['revision'],'answers':answers})
        self.assertEqual(r.status_code,200,r.text);return r.json()
    def confirm(self,c,s):
        r=c.post(f"/api/builder/{s['id']}/confirm",json={'revision':s['revision']})
        self.assertEqual(r.status_code,200,r.text);return r.json()
    def until(self,c,s,topic):
        while s['topic']['id']!=topic:
            s=self.confirm(c,self.present(c,s))
        return s
    def activate(self,c):
        s=self.until(c,self.start(c),'generation')
        s=self.confirm(c,self.present(c,s,{}))
        task=c.post(f"/api/builder/{s['id']}/first-run").json()
        approval=c.post(f"/api/tasks/{task['id']}/review",json={'decision':'approve','note':'Revisado'})
        self.assertEqual(approval.status_code,200,approval.text)
        s=self.confirm(c,self.present(c,s,{'task_id':task['id']}))
        return self.confirm(c,self.present(c,s))
    def test_topic_needs_confirmation_and_survives_restart(self):
        with TestClient(app) as c:
            s=self.start(c);s=self.present(c,s)
            self.assertEqual(s['topic']['id'],'frame');self.assertEqual(s['confirmed'],{})
            old_revision=s['revision']
        with TestClient(app) as c:
            s=c.get(f"/api/builder/{s['id']}").json()
            self.assertTrue(s['draft']);s=self.confirm(c,s)
            self.assertEqual(s['topic']['id'],'viability')
            self.assertEqual(len(s['decisions']),1)
            stale=c.post(f"/api/builder/{s['id']}/confirm",json={'revision':old_revision})
            self.assertEqual(stale.status_code,409)
    def test_insufficient_answers_do_not_close_topic(self):
        with TestClient(app) as c:
            s=self.start(c);s=self.present(c,s,{'name':'Solo nombre'})
            self.assertTrue(s['errors']);self.assertFalse(s['draft'])
            self.assertEqual(c.post(f"/api/builder/{s['id']}/confirm",json={'revision':s['revision']}).status_code,409)
    def test_nogo_is_a_valid_outcome(self):
        with TestClient(app) as c:
            s=self.until(c,self.start(c),'viability')
            s=self.confirm(c,self.present(c,s,{'go':'no-go','reason':'No podemos verificar el resultado.'}))
            self.assertEqual(s['status'],'no-go')
            self.assertEqual(c.post(f"/api/builder/{s['id']}/first-run").status_code,409)
    def test_discovery_viability_needs_questions_and_leads_to_project(self):
        with TestClient(app) as c:
            s=self.until(c,self.start(c),'viability')
            data={'basis':'discovery','discovery_questions':'¿Qué reglas faltan y cómo se probarán?',
                  'representation':'Ficha de proyecto en texto','sources':'Referencia indicada por el propietario, sin verificar',
                  'invariant':'required-fields','go':'go','reason':'Explorar antes de activar el proceso.'}
            s=self.present(c,s,data)
            self.assertFalse(s['errors'],s['errors'])
            s=self.confirm(c,s)
            s=self.confirm(c,self.present(c,s))
            self.assertEqual(s['topic']['id'],'shape')
            s=self.present(c,s,{'path':'simple-process','complexity':'no','reason':'No debe admitirse todavía'})
            self.assertTrue(s['errors'])
            s=self.confirm(c,self.present(c,s,{'path':'project','complexity':'no','reason':'Definir las reglas y sus pruebas'}))
            self.assertEqual(s['status'],'project-required')
            brief=next(iter(s['artifacts'].values()))
            self.assertIn('¿Qué reglas faltan y cómo se probarán?',brief)
            self.assertIn('no a trabajo sin verificación',brief)

    def test_complex_process_requires_definition_project(self):
        with TestClient(app) as c:
            s=self.until(c,self.start(c),'shape')
            s=self.present(c,s,{'path':'simple-process','complexity':'yes','reason':'Varias áreas'})
            self.assertTrue(s['errors'])
            s=self.present(c,s,{'path':'complex-process','complexity':'yes','reason':'Varias áreas'})
            s=self.confirm(c,s)
            self.assertEqual(s['status'],'project-required')
            self.assertTrue(any('project-brief' in p for p in s['artifacts']))
    def test_supervised_case_and_handover_enable_local_instance(self):
        with TestClient(app) as c:
            s=self.until(c,self.start(c),'generation')
            self.assertGreater(len(s['artifacts']),8)
            self.assertEqual(c.post(f"/api/instances/{s['id']}/cases",json={'title':'A','data':'B'}).status_code,409)
            s=self.confirm(c,self.present(c,s,{}))
            task=c.post(f"/api/builder/{s['id']}/first-run").json()
            again=c.post(f"/api/builder/{s['id']}/first-run").json()
            self.assertEqual(task['id'],again['id'])
            self.assertEqual(task['contract']['definition_version'],1)
            self.assertEqual(c.post(f"/api/builder/{s['id']}/answer",json={'revision':s['revision'],'answers':{'task_id':task['id']}}).status_code,409)
            self.assertEqual(c.post(f"/api/tasks/{task['id']}/review",json={'decision':'approve','note':'Conforme'}).status_code,200)
            s=self.confirm(c,self.present(c,s,{'task_id':task['id']}))
            bad=self.present(c,s,{'signer':'Otra persona','accepted_limits':'Solo demo'})
            self.assertTrue(bad['errors'])
            s=self.confirm(c,self.present(c,bad))
            self.assertEqual(s['status'],'active-demo')
            task=c.post(f"/api/instances/{s['id']}/cases",json={'title':'Segundo caso','data':'Curso y motivo ficticios'}).json()
            self.assertEqual(task['status'],'proposed')
            exported=c.get(f"/api/builder/{s['id']}/export")
            self.assertEqual(exported.status_code,200)
            archive=zipfile.ZipFile(io.BytesIO(exported.content))
            self.assertIn('builder-session.json',archive.namelist())
            self.assertTrue(any('process-definition' in p for p in archive.namelist()))
    def test_improvement_needs_ruling_and_never_changes_definition(self):
        with TestClient(app) as c:
            s=self.activate(c)
            before=c.get(f"/api/builder/{s['id']}").json()['artifacts']
            data={'observation':'La revisión necesita contexto adicional','change':'Añadir criterio sobre fuentes',
                  'metric':'Casos devueltos por falta de fuente','target':'Menos de dos en cinco casos',
                  'due':(date.today()+timedelta(days=10)).isoformat()}
            p=c.post(f"/api/instances/{s['id']}/improvements",json=data)
            self.assertEqual(p.status_code,201,p.text);p=p.json()
            self.assertEqual(p['evidence']['integrated'],1)
            path=f"/api/instances/{s['id']}/improvements/{p['id']}/ruling"
            self.assertEqual(c.post(path,json={'decision':'approved','reason':' '}).status_code,409)
            r=c.post(path,json={'decision':'approved','reason':'Investigar mejora'}).json()
            self.assertIn('change_project',r)
            self.assertEqual(c.post(path,json={'decision':'approved','reason':'Otra vez'}).status_code,409)
            self.assertEqual(c.get(f"/api/builder/{s['id']}").json()['artifacts'],before)
            project=c.get('/api/builder/'+r['change_project']).json()
            self.assertEqual(project['intended_path'],'project')
    def test_optional_model_proposes_fields_but_cannot_confirm(self):
        config={'APF_BUILDER':'openai-compatible','APF_LLM_URL':'https://model.example.test/v1/chat/completions',
                'APF_LLM_MODEL':'test','APF_LLM_API_KEY':'dummy','APF_LLM_INPUT_USD_PER_MILLION':'1','APF_LLM_OUTPUT_USD_PER_MILLION':'1'}
        with patch.dict(os.environ,config):
            with TestClient(app) as c:
                s=self.start(c)
                response=httpx.Response(200,request=httpx.Request('POST',config['APF_LLM_URL']),json={
                    'choices':[{'message':{'content':json.dumps({'answers':s['example'],'question':'¿Es correcto este encuadre?'})}}],
                    'usage':{'prompt_tokens':100,'completion_tokens':50}})
                with patch('app.llm.httpx.post',return_value=response) as call:
                    r=c.post(f"/api/builder/{s['id']}/answer",json={'revision':0,'text':'Quiero revisar solicitudes sintéticas.'})
                    self.assertEqual(r.status_code,200,r.text);s=r.json()
                    self.assertEqual(s['confirmed'],{})
                    self.assertTrue(s['draft'])
                    self.assertEqual(s['history'][-1]['advice']['input_tokens'],100)
                    self.assertIn('Builder',call.call_args.kwargs['json']['messages'][0]['content'])
                    self.assertEqual(s['topic']['id'],'frame')
                    persisted=c.get('/api/builder/'+s['id']).json()
                    self.assertEqual(persisted['model_advice']['question'],'¿Es correcto este encuadre?')

    def test_registry_is_recovered_from_builder_checkpoint(self):
        with TestClient(app) as c:
            s=self.activate(c)
            app.state.service.conn.execute("UPDATE apf_instances SET status='configured-draft' WHERE id=?",(s['id'],))
            app.state.service.conn.commit()
        with TestClient(app) as c:
            row=app.state.service.conn.execute('SELECT status FROM apf_instances WHERE id=?',(s['id'],)).fetchone()
            self.assertEqual(row[0],'active-demo')

    def test_root_is_builder_and_previous_tasks_remain_accessible(self):
        with TestClient(app) as c:
            self.assertIn('Empezar con el Builder',c.get('/').text)
            self.assertIn('Crear propuesta',c.get('/tasks').text)

if __name__=='__main__': unittest.main()
