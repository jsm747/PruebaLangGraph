# APF · PoC de Builder e instancias con LangGraph

La entrada de la aplicación es un **Builder por temas** basado en el guion APF 0.4.1: encuadre, viabilidad, perfil, camino, reglas, personas, economía, conocimiento, generación, primera prueba y entrega. Cada tema requiere una confirmación explícita. La instancia resultante permite operar casos L0 y registrar propuestas de mejora con resolución humana.

Empieza con [el recorrido de la PoC](docs/poc-builder.md). Por defecto es modo **guiado sin modelo** y el ejecutor es simulado. Las fuentes declaradas y los responsables son datos aportados por el usuario local, no verificaciones corporativas. No se afirma preparación completa APF ni equivalencia de todos sus agentes. La [comparación de requisitos](docs/compatibilidad.md) y el [alcance del Builder](docs/poc-builder.md#alcance-comprobado-y-pendiente) detallan lo pendiente.

En GitHub Codespaces el archivo `.devcontainer/devcontainer.json` prepara el entorno y arranca la aplicación, con el puerto 8000 reenviado. Mantén el puerto privado. El proceso se ejecuta en el Codespace; GitHub almacena el código. No requiere GitHub Actions.

## Requisitos y arranque

Necesitas Python 3.10 o superior y Git instalado y disponible en el `PATH` (los controles originales comparan árboles Git temporales).

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abre `http://127.0.0.1:8000` en el navegador de tu propia máquina. La API interactiva está en `/docs`. El estado se guarda por defecto en `data/prototype.sqlite3`; puedes elegir otra carpeta con `APF_DATA_DIR`. Reiniciar conserva tareas, propuestas, decisiones, artefactos y pausa.

**Uso exclusivamente local con datos sintéticos:** no hay inicio de sesión ni control de acceso. No expongas el servidor a la red ni introduzcas información personal, de clientes o confidencial. Una aprobación identifica únicamente al usuario local de prueba; no acredita una identidad humana corporativa.

## Flujo de casos (después del Builder o en `/tasks`)

1. Crea una tarea con contrato y criterios; por defecto pertenece a la instancia sintética `readiness-test` y se habilita al crearla. En la interfaz puedes indicar una serie, invariantes y alcance. La API también admite `next_item` y creación sin habilitar (`auto_arm: false`).
2. El servicio comprueba que la instancia del registro tenga estado permitido y no haya vencido. Respeta la pausa global, el presupuesto registrado y una tarea activa por serie. Las habilitadas esperan hasta que se libere la serie.
3. El ejecutor recibe las entradas filtradas y genera una propuesta de archivos. Se ejecutan los cuatro controles originales: `append-only`, `citations`, `layer` y `scope`, usando un repositorio Git temporal.
4. Se muestra la propuesta y cada resultado. Una persona puede aprobar, rechazar o solicitar un cambio. Un control rojo impide aprobar. El rechazo devuelve la tarea a la cola; se puede habilitar otra vez. Un cambio se entrega al ejecutor y requiere una nueva revisión.
5. Una aprobación integra los archivos en el almacén local, con versión y sin sobrescribir un artefacto modificado desde la propuesta. También habilita la siguiente tarea indicada. No se publican archivos ni se modifica otro sistema.

La copia sintética de `instances/readiness-test/` aporta al ejecutor los documentos y registros de decisión de partida; los artefactos aprobados en SQLite tienen prioridad sobre esa copia. La instancia `readiness-test` y las fechas proceden del piloto original. No deben interpretarse como un registro corporativo real; el registro se copia en [registry/instances.json](registry/instances.json).

## Modelos opcionales

Para conversar con el Builder configura `APF_BUILDER=openai-compatible`, además de las variables `APF_LLM_*` de abajo. Sus propuestas siguen requiriendo tu confirmación. Consulta las limitaciones de presupuesto y validación semántica en [el recorrido](docs/poc-builder.md#modo-guiado-y-modo-modelo).

### Ejecutor con un modelo compatible, opcional

El adaptador `openai-compatible` permite una llamada de chat con respuesta JSON estructurada. Carga el mandato y la habilidad del ejecutor del framework fijado y, si existe, el anexo de la instancia. Solo puede proponer archivos del alcance; el mecanismo ejecuta los controles y espera una aprobación. **No ejecuta herramientas ni reproduce las sesiones completas de Claude Code.**

Actívalo únicamente cuando tengas un servicio autorizado y sus precios. Configura las variables en el entorno seguro que uses para arrancar el servidor; no guardes claves en el repositorio:

```text
APF_EXECUTOR=openai-compatible
APF_LLM_URL=https://<servicio-autorizado>/v1/chat/completions
APF_LLM_MODEL=<modelo>
APF_LLM_API_KEY=<credencial>
APF_LLM_INPUT_USD_PER_MILLION=<precio-de-entrada>
APF_LLM_OUTPUT_USD_PER_MILLION=<precio-de-salida>
APF_LLM_MAX_OUTPUT_TOKENS=2048
```

El servicio debe admitir `messages`, `response_format: json_object`, `max_tokens` y devolver `usage.prompt_tokens` y `usage.completion_tokens`. Se transmiten el contrato filtrado y los archivos integrados de la misma instancia, además del mandato y anexo. Los filtros son heurísticos y no garantizan eliminar todos los datos sensibles o instrucciones maliciosas.

El coste se estima a partir de los tokens informados y los precios configurados. Antes de la llamada se compara una estimación con el límite por sesión; **no es un límite de gasto garantizado por el proveedor**. El presupuesto mensual se comprueba antes de cada nueva sesión. Si una respuesta o llamada falla y su coste puede ser desconocido, se bloquean nuevas sesiones de esa instancia hasta que se concilie el registro. La conciliación todavía no tiene interfaz. El adaptador se ha probado con respuestas controladas, no contra un servicio corporativo real.

## Verificación

```bash
python -m unittest discover -s tests -v
python regression/run.py
```

Para repetir la prueba opcional de la interfaz necesitas Node.js, Playwright y Chromium. Instala Playwright fuera del código versionado (por ejemplo, `npm install --no-save --package-lock=false playwright` y `npx playwright install chromium`), arranca el servidor con una carpeta `APF_DATA_DIR` de prueba y ejecuta `node tests/browser.cjs`. Si usas Chromium del sistema, indica su ruta mediante `APF_CHROMIUM_PATH`. La prueba crea y aprueba tareas sintéticas en el servidor seleccionado.

El segundo comando conserva el banco del original: ejecuta 12 casos del router y 13 de los controles. Su línea `0 pending` no significa que se hayan ejecutado los ocho casos de roles: esos requerían sesiones reales de Claude en GitHub Actions y no los ejecuta este runner.

## Límites de esta versión

- El Builder tiene su propio grafo guiado o con interpretación opcional por modelo; del ciclo operativo solo el rol `executor` está conectado al grafo. La copia de `framework/` contiene los demás mandatos y plantillas, pero no los implementa como agentes operativos.
- No hay aprobación autenticada, aislamiento de credenciales por rol, ejecución segura de herramientas, integración con sistemas corporativos, avisos, ni despliegue distribuido. No hay garantía de ejecución exactamente una vez.
- La cola, el bloqueo por serie y la recuperación están diseñados para **un único proceso y worker**. La recuperación se hace al iniciar o al reanudar; no hay reconciliador periódico ni las mismas garantías de recuperación que en GitHub Actions.
- El registro de costes y la telemetría son simplificados; no sustituyen los límites, eventos de herramientas ni la observabilidad de sesiones del piloto original. La simulación registra coste cero por no efectuar llamadas.
- El router original está disponible en `scripts/route.py` y se prueba con su banco, pero no está conectado al flujo de tareas. El prototipo mantiene la decisión humana L0.
- Las tareas creadas por la primera versión del prototipo se conservan para consulta, sin reanudación automática bajo el nuevo grafo.

## Procedencia

Los archivos de `framework/`, `regression/`, `protocol/`, `registry/`, `config/` y los comprobadores indicados en `scripts/` proceden del checkout del piloto en el commit `78008e0da6f3040888c136fe5fff4e72510b1b8f`. El framework incluido es la copia fijada 0.4.1 documentada en [framework/PINNED.md](framework/PINNED.md). El código de `app/` es la adaptación local a LangGraph.
