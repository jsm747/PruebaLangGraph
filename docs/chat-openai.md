# Chatbot Builder conectado a OpenAI

La interfaz incorpora una conversación persistente sobre el mismo grafo APF. Puede completar un tema con varios mensajes, hacer preguntas y proponer un resumen. El propietario sigue confirmando cada tema con un botón. El modelo no puede cerrar etapas ni modificar temas confirmados.

## Activación en tu Codespace desde el iPad

1. En tu cuenta de GitHub abre **Settings → Codespaces → Secrets → New secret**. Crea `APF_LLM_API_KEY`, introduce allí tu clave de API de OpenAI y autoriza `jsm747/PruebaLangGraph`. No pegues la clave en este chat, en la interfaz ni en comandos del historial. Utiliza el almacén de secretos.
2. Reinicia el Codespace para que reciba el secreto y abre una terminal nueva. Actualiza el repositorio con `git pull --ff-only`. Detén el servidor anterior si sigue ocupando el puerto 8000.
3. Desde la raíz del repositorio ejecuta:

   ```bash
   export APF_LLM_MODEL=gpt-4.1
   bash scripts/start-chat.sh
   ```

   `gpt-4.1` es un ejemplo para la PoC. Usa un modelo disponible en tu proyecto de API que admita Chat Completions y respuesta JSON. No se ha verificado desde esta tarea el acceso de tu cuenta a ningún modelo. El uso de la API se factura por separado de la suscripción de ChatGPT.
4. Abre el puerto 8000, manteniéndolo **Private**, y recarga la aplicación. La configuración mostrará proveedor y modelo, nunca la clave. **Configuración preparada** no prueba acceso: la primera petición se hace al enviar el mensaje.
5. Inicia o retoma una instancia. Escribe en **Tu mensaje**, por ejemplo: «Quiero organizar la revisión de solicitudes de formación. Hoy tardamos demasiado». Pulsa **Enviar al Builder**. Responde a su aclaración y, cuando el resumen sea correcto, pulsa **Confirmar tema y continuar**.

El script activa `APF_BUILDER=openai-compatible` y usa el endpoint de OpenAI por defecto. No activa el ejecutor de casos: `APF_EXECUTOR` sigue simulado mientras no se configure expresamente.

## Configuración

| Variable | Uso |
|---|---|
| `APF_LLM_API_KEY` | Credencial de servidor suministrada como secreto |
| `APF_LLM_MODEL` | Identificador de modelo disponible en el proyecto de API |
| `APF_LLM_PROVIDER` | `openai` por defecto en el script; también `azure` o `compatible` |
| `APF_LLM_URL` | Opcional para OpenAI; obligatorio para otros servicios: URL HTTPS completa de chat |
| `APF_LLM_MAX_OUTPUT_TOKENS` | Límite por respuesta; 4096 por defecto para el chat |
| `APF_LLM_REASONING_EFFORT` | Opcional: `low`, `medium` o `high`, solo si el modelo lo admite. No lo configures para gpt-4.1 |
| `APF_LLM_TOKEN_PARAMETER` | `max_completion_tokens` para OpenAI/Azure; `max_tokens` para compatibles; ajustable según el servicio |
| `APF_CHAT_MAX_TURNS` | Máximo de consultas al modelo por sesión de Builder; 50 por defecto |
| `APF_LLM_INPUT_USD_PER_MILLION`, `APF_LLM_OUTPUT_USD_PER_MILLION` | Tarifas opcionales para estimar el coste. Si faltan, se conservan tokens y el coste aparece desconocido |

Para Azure se usa cabecera `api-key`, y debes proporcionar el endpoint completo con la versión de API si tu servicio la requiere. Para OpenAI y servicios compatibles se usa `Authorization: Bearer`. No se permiten credenciales en la URL. La configuración del ejecutor de casos es independiente y sigue los requisitos de su adaptador.

## Conversación y límites

- Los mensajes, preguntas, respuestas parciales y resúmenes viven en el checkpoint del Builder y sobreviven a una recarga o reinicio. Solo el tema confirmado se convierte en decisión.
- El modelo recibe el mandato, el guion APF, las decisiones confirmadas, las respuestas parciales y un contexto acotado de mensajes del tema actual. No accede por sí mismo a documentos, herramientas o sistemas externos.
- Se conserva el texto del propietario; los patrones heurísticos de ingesta se aplican al contexto enviado al modelo. Usa datos sintéticos. Los filtros no garantizan anonimización o resistencia a inyecciones.
- El nodo de interpretación forma parte de LangGraph. Si se interrumpe una posible llamada, al reiniciar se registra el fallo sin volver a enviarla automáticamente. Un timeout o respuesta inválida puede haber consumido tokens; consulta el proveedor antes de repetir.
- No hay streaming token a token ni autenticación propia. Mantén el puerto privado en Codespaces. El límite de consultas y de tokens no es un presupuesto monetario garantizado.
- Este chat sigue siendo la PoC del Builder, no una implementación de todos los agentes APF. Generación, revisión de la primera prueba y entrega requieren acciones explícitas.

## Verificación

`python -m unittest discover -s tests -v` incluye memoria entre mensajes, conservación tras reiniciar, cierre solo humano, recuperación sin repetir llamadas y estado de configuración sin secretos. El proveedor se simula en las pruebas.

`tests/chat-browser.cjs` prueba el chat en navegador. Para repetirlo sin una cuenta de OpenAI puedes arrancar **solo como prueba** `PYTHONPATH=. APF_DATA_DIR=/tmp/apf-chat-test .venv/bin/python tests/serve_chat_fixture.py`; ese servidor escucha en 8126 y sustituye las respuestas HTTP del proveedor por datos de prueba. Apunta `APF_TEST_URL` a ese servidor al ejecutar Playwright. No confundir ese fixture con una conexión real.

La conexión real permanece pendiente de introducir el secreto de OpenAI en tu Codespace. No se han enviado peticiones reales a OpenAI durante la implementación.
