"""Contract for Builder replies, separate from the owner's semantic answers.

Known text fields can be normalized without granting the model authority over
workflow state. Extra domain information becomes an unverified draft note.
"""
import json
from app.llm import ChatError

CONTROL_FIELDS={'status','confirmed','revision','index','action','approved','decisions','artifacts','instance_ready'}


def response_schema(topic):
    fields={key:{'type':['string','null']} for key,_,_ in topic['fields']}
    return {'type':'object','properties':{
        'answers':{'type':'object','properties':fields,'required':list(fields),'additionalProperties':False},
        'question':{'type':'string'},
        'notes':{'type':'array','items':{'type':'object','properties':{
            'kind':{'type':'string','enum':['source','clarification','pending']},'text':{'type':'string'}},
            'required':['kind','text'],'additionalProperties':False}}
    },'required':['answers','question','notes'],'additionalProperties':False}


def parse_response(content, topic, metadata):
    def fail(code, explanation):
        detail=dict(metadata,diagnostics=[code])
        raise ChatError(explanation,uncertain=not metadata.get('cost_known',False),metadata=detail,code=code)
    try:
        result=json.loads(content)
    except (ValueError,TypeError):
        fail('invalid_json','No he podido leer el resumen del proveedor. Tu mensaje queda guardado y el tema sigue abierto.')
    if not isinstance(result,dict) or not isinstance(result.get('answers'),dict):
        fail('invalid_envelope','El proveedor no devolvió los campos del resumen. Tu aportación sigue guardada; ninguna decisión se ha confirmado.')
    if CONTROL_FIELDS.intersection(result) or CONTROL_FIELDS.intersection(result['answers']):
        fail('control_field','La salida incluye cambios de estado que el modelo no puede realizar. El tema sigue abierto y tu mensaje queda guardado.')
    allowed={key:kind for key,_,kind in topic['fields']}
    answers,notes,diagnostics={},[],[]
    for key,value in result['answers'].items():
        if value is None:
            continue  # Structured Outputs uses null for unknown/unchanged fields.
        if key not in allowed:
            # Domain facts from compatible providers are notes, never state or answers.
            if isinstance(value,(str,list,dict)):
                note=value if isinstance(value,str) else json.dumps(value,ensure_ascii=False)
                notes.append({'kind':'pending','text':f'{key}: {note}'[:6000]})
                diagnostics.append('extra_domain_field')
                continue
            fail('invalid_extra_field','No he podido incorporar un dato del resumen. Tu mensaje queda guardado; el tema sigue abierto.')
        if isinstance(value,list) and allowed[key]=='textarea' and all(isinstance(item,str) for item in value):
            value='\n'.join(value)
            diagnostics.append('text_list_normalized')
        if key=='sources' and isinstance(value,(dict,list)):
            value=json.dumps(value,ensure_ascii=False,indent=2)
            diagnostics.append('source_structure_normalized')
        if not isinstance(value,str) or len(value)>6000:
            fail('invalid_field_type','Un campo del resumen llegó en un formato que no puedo incorporar. Tu mensaje queda guardado; puedes continuar la conversación o corregir el resumen.')
        answers[key]='' if value.strip().upper()=='UNKNOWN' else value
    if answers.get('sources'):
        notes.append({'kind':'source','text':answers['sources']})
    raw_notes=result.get('notes',[])
    if not isinstance(raw_notes,list) or len(raw_notes)>20:
        fail('invalid_notes','No he podido leer las notas de la respuesta. El tema sigue abierto y tu mensaje queda guardado.')
    for note in raw_notes:
        if not isinstance(note,dict) or note.get('kind') not in ('source','clarification','pending') or not isinstance(note.get('text'),str) or len(note['text'])>6000:
            fail('invalid_note','Una nota del proveedor tiene un formato inválido. Tu mensaje queda guardado; no se ha confirmado ninguna decisión.')
        if note['text'].strip():
            notes.append({'kind':note['kind'],'text':note['text']})
    question=result.get('question')
    if not isinstance(question,str) or not question.strip() or len(question)>6000:
        diagnostics.append('missing_question')
        question='He guardado tu aportación como borrador. Revisa los campos del tema; lo que falte sigue pendiente de aclaración.'
    return answers,dict(metadata,question=question,notes=notes,diagnostics=diagnostics)
