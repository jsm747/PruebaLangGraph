"""Browser-test fixture only: controlled HTTP responses, no model network calls.
Run from the repo root: python -m tests.serve_chat_fixture (namespace package).
"""
import json
import os
from unittest.mock import patch
import httpx
import uvicorn


def fake_response(url, *, json: dict, headers, timeout):
    user=[m['content'] for m in json['messages'] if m['role']=='user'][-1]
    if 'artículo 6' in user:
        reference='Capítulo III, Sección 1, artículo 6, junto con el anexo III'
        answers={'sources':[{'reference':reference}],'legal_reference':reference}
        question='Registro esa referencia como pendiente de contrastar. ¿Qué debería contener la ficha de clasificación de cada caso?'
    elif 'Se llama' in user:
        answers={'name':'Formación','owner':'Persona demo'}
        question='He preparado el encuadre. Revisa el resumen y confirma el tema.'
    else:
        answers={'purpose':'Revisar solicitudes de formación','pain':'Tardamos demasiado.'}
        question='¿Cómo se llama el proceso y quién es responsable?'
    output=__import__('json').dumps({'answers':answers,'question':question})
    return httpx.Response(200,request=httpx.Request('POST',url),json={
        'choices':[{'message':{'content':output}}],'usage':{'prompt_tokens':100,'completion_tokens':50}})


if __name__=='__main__':
    os.environ.update(APF_BUILDER='openai-compatible',APF_LLM_PROVIDER='openai',APF_LLM_MODEL='test-fixture',APF_LLM_API_KEY='dummy-fixture')
    with patch('app.llm.httpx.post',side_effect=fake_response):
        uvicorn.run('app.main:app',host='127.0.0.1',port=8126)
