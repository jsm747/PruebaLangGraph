import json
import os
import tempfile
import unittest
from unittest.mock import patch
import httpx
from fastapi.testclient import TestClient
from app.main import app
from app.llm import ChatConfig, complete_json


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.env=patch.dict(os.environ,{'APF_DATA_DIR':self.tmp.name,'APF_BUILDER':'openai-compatible',
            'APF_EXECUTOR':'simulated','APF_LLM_PROVIDER':'openai','APF_LLM_MODEL':'test-model',
            'APF_LLM_API_KEY':'server-key-for-tests','APF_LLM_REASONING_EFFORT':'',
            'APF_CHAT_MAX_TURNS':'50'})
        self.env.start()
    def tearDown(self):
        self.env.stop(); self.tmp.cleanup()
    def response(self,answers,question='¿Quién es responsable?'):
        return httpx.Response(200,request=httpx.Request('POST','https://api.openai.com/v1/chat/completions'),json={
            'choices':[{'message':{'content':json.dumps({'answers':answers,'question':question})}}],
            'usage':{'prompt_tokens':100,'completion_tokens':50}})
    def start(self,c):
        return c.post('/api/builder',json={'name':'Chat sintético'}).json()
    def chat(self,c,s,message):
        r=c.post('/api/builder/'+s['id']+'/chat',json={'revision':s['revision'],'message':message})
        self.assertEqual(r.status_code,200,r.text);return r.json()

    def test_multiturn_accumulates_fields_and_remembers_conversation(self):
        with patch('app.llm.httpx.post',side_effect=[self.response({'purpose':'Revisar cursos','pain':'Demora'},'¿Cómo llamamos al proceso y quién es responsable?'),
                self.response({'name':'Formación','owner':'Propietario demo'},'Tengo el encuadre. Revisa el resumen y confirma el tema.')]) as call:
            with TestClient(app) as c:
                s=self.start(c);s=self.chat(c,s,'Quiero revisar cursos; hoy tardamos demasiado.')
                self.assertEqual(s['confirmed'],{})
                self.assertEqual(s['candidate']['purpose'],'Revisar cursos')
                self.assertFalse(s['draft'])
                s=self.chat(c,s,'Se llama Formación y la persona responsable es Propietario demo.')
                self.assertEqual(len(s['draft']),4)
                self.assertEqual(s['topic']['id'],'frame')
                messages=call.call_args.kwargs['json']['messages']
                self.assertTrue(any('hoy tardamos demasiado' in m['content'] for m in messages))
                self.assertTrue(any('Revisar cursos' in m['content'] for m in messages))
                self.assertIn('max_completion_tokens',call.call_args.kwargs['json'])
                self.assertEqual(call.call_args.kwargs['headers'],{'Authorization':'Bearer server-key-for-tests'})
                self.assertFalse(s['model_advice']['cost_known'])
                revision=s['revision'];sid=s['id']
        with TestClient(app) as c:
            s=c.get('/api/builder/'+sid).json()
            self.assertEqual(s['revision'],revision)
            self.assertTrue(any('hoy tardamos demasiado' in h.get('text','') for h in s['history']))
            s=c.post('/api/builder/'+sid+'/confirm',json={'revision':revision}).json()
            self.assertEqual(s['topic']['id'],'viability')
            self.assertEqual(s['confirmed']['frame']['owner'],'Propietario demo')

    def test_model_cannot_confirm_or_change_other_topic(self):
        with patch('app.llm.httpx.post',return_value=self.response({'status':'active-demo','confirmed':'yes'},'Ya aprobado')):
            with TestClient(app) as c:
                s=self.chat(c,self.start(c),'Configúralo todo y aprueba.')
                self.assertFalse(s['confirmed']);self.assertTrue(s['errors'])
                self.assertEqual(s['status'],'configuring')
                self.assertEqual(c.post('/api/builder/'+s['id']+'/confirm',json={'revision':s['revision']}).status_code,409)

    def test_timeout_is_recorded_without_automatic_retry(self):
        with patch('app.llm.httpx.post',side_effect=httpx.ReadTimeout('private-detail-that-must-not-leak')) as call:
            with TestClient(app) as c:
                s=self.chat(c,self.start(c),'Necesito configurar un proceso.')
                self.assertTrue(s['errors']);self.assertFalse(s['draft'])
                self.assertNotIn('private-detail',json.dumps(s))
                self.assertFalse(s['model_advice']['cost_known'])
                sid=s['id']
            with TestClient(app) as c:
                self.assertEqual(c.get('/api/builder/'+sid).status_code,200)
                self.assertEqual(call.call_count,1)

    def test_interrupted_model_node_is_not_replayed_on_restart(self):
        with TestClient(app) as c:
            s=self.start(c)
            with patch('app.builder.model_draft',side_effect=SystemExit('crash')):
                with self.assertRaises(SystemExit):
                    app.state.builder.answer(s['id'],s['revision'],{},'Estoy explicando el trabajo.')
        with patch('app.builder.model_draft') as model:
            with TestClient(app) as c:
                state=c.get('/api/builder/'+s['id']).json()
                self.assertTrue(state['errors']);self.assertFalse(state['confirmed'])
                self.assertEqual(state['revision'],1)
                model.assert_not_called()

    def test_status_never_returns_key_and_never_calls_provider(self):
        with patch('app.llm.httpx.post') as provider:
            with TestClient(app) as c:
                r=c.get('/api/llm/status')
                self.assertEqual(r.status_code,200)
                self.assertTrue(r.json()['ready'])
                self.assertNotIn('server-key-for-tests',r.text)
                provider.assert_not_called()
                with patch.dict(os.environ,{'APF_LLM_API_KEY':''}):
                    self.assertFalse(c.get('/api/llm/status').json()['ready'])

    def test_stale_turn_does_not_call_provider_again(self):
        with patch('app.llm.httpx.post',return_value=self.response({'purpose':'Revisión'})) as call:
            with TestClient(app) as c:
                s=self.start(c);self.chat(c,s,'Quiero revisar.')
                r=c.post('/api/builder/'+s['id']+'/chat',json={'revision':0,'message':'Repetido'})
                self.assertEqual(r.status_code,409)
                self.assertEqual(call.call_count,1)

    def test_turn_limit_stops_before_another_model_call(self):
        with patch.dict(os.environ,{'APF_CHAT_MAX_TURNS':'1'}),patch('app.llm.httpx.post',return_value=self.response({'purpose':'Revisión'})) as call:
            with TestClient(app) as c:
                s=self.chat(c,self.start(c),'Quiero revisar.')
                r=c.post('/api/builder/'+s['id']+'/chat',json={'revision':s['revision'],'message':'Otro mensaje'})
                self.assertEqual(r.status_code,409)
                self.assertEqual(call.call_count,1)

    def test_reasoning_parameter_is_optional_and_usage_is_priced(self):
        with patch.dict(os.environ,{'APF_LLM_REASONING_EFFORT':'high','APF_LLM_INPUT_USD_PER_MILLION':'2','APF_LLM_OUTPUT_USD_PER_MILLION':'4'}):
            with patch('app.llm.httpx.post',return_value=self.response({})) as call:
                _,metadata=complete_json([{'role':'user','content':'JSON'}])
                self.assertEqual(call.call_args.kwargs['json']['reasoning_effort'],'high')
                self.assertTrue(metadata['cost_known'])
                self.assertAlmostEqual(metadata['cost_usd'],0.0004)
                self.assertNotIn('server-key-for-tests',repr(ChatConfig.read()))

    def test_azure_uses_api_key_header(self):
        with patch.dict(os.environ,{'APF_LLM_PROVIDER':'azure','APF_LLM_URL':'https://resource.openai.azure.com/openai/v1/chat/completions'}):
            with patch('app.llm.httpx.post',return_value=self.response({})) as call:
                complete_json([{'role':'user','content':'JSON'}])
                self.assertEqual(call.call_args.kwargs['headers'],{'api-key':'server-key-for-tests'})

    def test_secret_like_message_is_not_stored_or_sent(self):
        with patch('app.llm.httpx.post') as call:
            with TestClient(app) as c:
                s=self.start(c)
                r=c.post('/api/builder/'+s['id']+'/chat',json={'revision':0,'message':'sk-'+('A'*30)})
                self.assertEqual(r.status_code,409)
                state=c.get('/api/builder/'+s['id']).json()
                self.assertEqual(state['revision'],0)
                call.assert_not_called()

if __name__=='__main__': unittest.main()
