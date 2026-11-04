"""APF Builder topics: one topic and one explicit owner confirmation at a time."""
from datetime import date, timedelta

TOPICS = [
 {"id":"frame", "title":"0 · Entender tu trabajo", "question":"Cuéntame para qué sirve este trabajo, qué falla hoy y quién es responsable del resultado.", "fields":[
  ("name","Nombre del proceso","text"),("purpose","Qué resultado buscas","textarea"),("pain","Qué falla o cuesta hoy","textarea"),("owner","Propietario del proceso (persona)","text")]},
 {"id":"viability", "title":"1 · Comprobar viabilidad", "question":"¿Cómo sabremos que un resultado es correcto? Define al menos tres criterios comprobables y las fuentes que se pueden utilizar.", "fields":[
  ("criteria","Criterios verificables, uno por línea","textarea"),("representation","Forma comparable del entregable","text"),("sources","Fuentes autorizadas para la prueba","textarea"),("invariant","Comprobación ejecutable del prototipo","invariant"),("go","¿Continuamos?","go"),("reason","Razón de la decisión de viabilidad","textarea")]},
 {"id":"profile", "title":"1b · Perfil piloto", "question":"Delimitemos el piloto: datos sintéticos, decisión humana L0, fecha de fin y controles pendientes. Nombra a la persona que revisará la configuración.", "fields":[
  ("pilot_end","Fin del piloto","date"),("scope","Volumen y personas de la prueba","textarea"),("reviewer","Persona que revisa la configuración","text"),("deferred","Controles aplazados y sus limitaciones","textarea")]},
 {"id":"shape", "title":"2 · Elegir el camino", "question":"¿El trabajo termina o se repite? Si las reglas aún requieren investigación, varias áreas o sistemas, o riesgo alto, hay que definirlo mediante un proyecto.", "fields":[
  ("path","Camino","path"),("complexity","¿Hay alguna condición de complejidad?","yesno"),("reason","Por qué este camino encaja","textarea")]},
 {"id":"rules", "title":"3 · Reglas y casos", "question":"Describe casos típicos y difíciles. Escribe reglas con identificadores que el ejecutor pueda citar y especifica lo que nunca debe decidir solo.", "fields":[
  ("case_types","Tipos de caso","textarea"),("rules","Reglas, una por línea: R1: ...","textarea"),("mandatory_human","Situaciones que requieren siempre una persona","textarea"),("exceptions","Quién decide cuando falta una regla","textarea")]},
 {"id":"people", "title":"4 · Personas y controles", "question":"¿Quién revisa cada propuesta y con qué plazo? Explicita también las limitaciones de suplencia y separación de funciones de esta prueba.", "fields":[
  ("gatekeeper","Persona que aprueba los casos","text"),("sla_hours","Plazo de revisión (horas)","number"),("ladder","Suplencia y escalada, o limitación aceptada","textarea"),("risk_contact","Responsable de riesgo o revisión pendiente","text")]},
 {"id":"economics", "title":"5 · Economía y línea base", "question":"Registra cómo se hace hoy y qué gastarías como máximo. Las cifras estimadas deben identificarse como tales.", "fields":[
  ("baseline","Tiempo, coste y calidad actuales; indica si son estimaciones","textarea"),("session_usd","Límite por sesión (USD)","number"),("case_usd","Límite por caso (USD)","number"),("version_usd","Límite por versión o cadena (USD)","number"),("period_usd","Límite por periodo (USD)","number")]},
 {"id":"knowledge", "title":"6 · Conocimiento y revisión", "question":"¿Qué conocimiento se puede usar y quién lo mantiene? En esta PoC el Distiller permanece desactivado y solo se utilizan fuentes sintéticas declaradas.", "fields":[
  ("knowledge_owner","Responsable de las fuentes y habilidades","text"),("retention","Conservación de registros y fuentes","textarea"),("review_date","Primera revisión del proceso","date"),("cadence","Cadencia de auditoría y revisión","text")]},
 {"id":"generation", "title":"7 · Revisar la instancia generada", "question":"Revisa los documentos, las decisiones y la checklist. Confirmarlos habilita una prueba supervisada; no acredita preparación corporativa.", "fields":[]},
 {"id":"first_run", "title":"8 · Primera prueba supervisada", "question":"Ejecuta un caso sintético, revisa la propuesta y toma una decisión humana. Después comprobaremos su resultado y leeremos juntos el registro.", "fields":[("task_id","Identificador del caso supervisado","text")]},
 {"id":"handover", "title":"9 · Entrega del piloto", "question":"Confirma la entrega de esta instancia de demostración y la próxima revisión. Los controles corporativos pendientes siguen visibles.", "fields":[("signer","Nombre del propietario que confirma","text"),("accepted_limits","Limitaciones pendientes que aceptas para esta prueba","textarea")]},
]

EXAMPLES = {
 "frame":{"name":"Revisión de solicitudes de formación", "purpose":"Preparar una propuesta sobre solicitudes sintéticas de cursos internos.", "pain":"La revisión manual exige comprobar siempre los mismos campos.", "owner":"Responsable de formación (demo)"},
 "viability":{"criteria":"Cada propuesta identifica el curso y el solicitante sintético.\nCada propuesta cita al menos una regla.\nCada propuesta queda pendiente de decisión humana.", "representation":"Markdown con campos y reglas identificables", "sources":"Catálogo y solicitudes ficticias preparados para la prueba.", "invariant":"required-fields", "go":"go", "reason":"Podemos comparar los campos y conservar la decisión humana."},
 "profile":{"pilot_end":"2027-01-31", "scope":"Un propietario local y cinco solicitudes sintéticas.", "reviewer":"Revisor del framework (demo)", "deferred":"Identidad corporativa, segregación real, avisos y límites económicos completos pendientes."},
 "shape":{"path":"simple-process", "complexity":"no", "reason":"Trabajo recurrente con reglas explícitas, un equipo y sin efectos externos."},
 "rules":{"case_types":"Solicitud de curso interno con identificador, curso y motivo.", "rules":"R1: Si faltan el curso o el motivo, proponer completar los datos.\nR2: Si los campos están presentes, preparar una recomendación para revisión.\nF1: No comunicar ni ejecutar decisiones fuera de la plataforma.", "mandatory_human":"Todos los casos del piloto son L0 y requieren decisión humana.", "exceptions":"El propietario resuelve los casos no cubiertos y registra su motivo."},
 "people":{"gatekeeper":"Responsable de formación (demo)", "sla_hours":"24", "ladder":"Una sola persona en la demo; sin suplente ni escalada automática. Segregación no demostrada.", "risk_contact":"Revisión corporativa pendiente; solo datos sintéticos."},
 "economics":{"baseline":"Estimación: diez minutos por solicitud; aún sin medición de errores ni coste monetario.", "session_usd":"1", "case_usd":"3", "version_usd":"5", "period_usd":"15"},
 "knowledge":{"knowledge_owner":"Responsable de formación (demo)", "retention":"Conservar registros de la prueba hasta doce meses después de terminar el piloto.", "review_date":"2026-11-20", "cadence":"Auditoría tras cinco casos; revisión del propietario cada dos semanas."},
 "handover":{"signer":"Responsable de formación (demo)", "accepted_limits":"Demo sin identidad corporativa, ejecutor simulado por defecto y revisión humana de todos los casos."},
}


def validate(topic, answers, confirmed):
    errors = []
    expected = {field[0] for field in topic["fields"]}
    if set(answers) - expected:
        errors.append("Hay campos que no pertenecen al tema actual.")
    for key, label, kind in topic["fields"]:
        if topic['id']=='viability' and answers.get('go')=='no-go' and key not in ('go','reason'):
            continue
        if not isinstance(answers.get(key), str) or not answers[key].strip():
            errors.append(f"Falta: {label}.")
        elif len(answers[key]) > 6000:
            errors.append(f"El campo {label} es demasiado largo.")
    if errors:
        return errors
    tid = topic["id"]
    if tid == "viability":
        if answers["go"] not in ("go","no-go"):
            errors.append("Elige go o no-go.")
        if answers["go"] == "go" and len([x for x in answers["criteria"].splitlines() if x.strip()]) < 3:
            errors.append("Indica al menos tres criterios comprobables.")
        if answers["go"] == "go" and answers["invariant"] != "required-fields":
            errors.append("La PoC solo implementa la comprobación required-fields; no declara ejecutables otras invariantes.")
    if tid == "shape":
        if answers["path"] not in ("simple-process","project","complex-process") or answers["complexity"] not in ("yes","no"):
            errors.append("Elige un camino y una condición de complejidad válidos.")
        elif answers["path"] == "simple-process" and answers["complexity"] == "yes":
            errors.append("Una condición de complejidad exige un proyecto de definición.")
    if tid == "rules" and not any(line.strip().startswith("R1:") for line in answers["rules"].splitlines()):
        errors.append("Identifica al menos la primera regla como R1: ...")
    for key in ("pilot_end","review_date"):
        if key in answers:
            try:
                value = date.fromisoformat(answers[key])
                if value <= date.today():
                    errors.append(f"{key} debe ser una fecha futura.")
                end = confirmed.get("profile",{}).get("pilot_end")
                if key == "review_date" and end and answers[key] > end:
                    errors.append("La revisión debe ocurrir antes de terminar el piloto.")
            except ValueError:
                errors.append(f"Fecha inválida: {key}.")
    for key in ("sla_hours","session_usd","case_usd","version_usd","period_usd"):
        if key in answers:
            try:
                if not 0 < float(answers[key]) < 1_000_000:
                    errors.append(f"Valor positivo inválido: {key}.")
            except ValueError:
                errors.append(f"Número inválido: {key}.")
    if tid == "economics" and not errors:
        if not float(answers["session_usd"]) <= float(answers["case_usd"]) <= float(answers["version_usd"]) <= float(answers["period_usd"]):
            errors.append("Los presupuestos deben cumplir sesión ≤ caso ≤ versión/cadena ≤ periodo.")
    if tid == "handover" and answers["signer"] != confirmed["frame"]["owner"]:
        errors.append("Debe confirmar la persona indicada como propietaria del proceso.")
    return errors

EXAMPLES["profile"]["pilot_end"]=(date.today()+timedelta(days=90)).isoformat()
EXAMPLES["knowledge"]["review_date"]=(date.today()+timedelta(days=14)).isoformat()
