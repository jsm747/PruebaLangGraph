# PoC APF: Builder, operación supervisada y mejora local

El punto de entrada `/` es ahora el Builder. La anterior herramienta de tareas sigue disponible en `/tasks` para revisar propuestas.

## Probar desde un iPad con Codespaces

El repositorio incluye `.devcontainer/devcontainer.json`: al crear un Codespace nuevo prepara Python y arranca la aplicación en el puerto 8000. Mantén ese puerto privado y ábrelo desde la pestaña Puertos.

Si ya tenías el Codespace de la versión anterior, detén su servidor, ejecuta `git pull --ff-only` y vuelve a arrancar `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` con el entorno virtual activado. La configuración automática del contenedor requiere reconstruirlo; no es necesario hacerlo para probar la actualización manual.

1. Escribe el nombre del proceso y pulsa **Empezar con el Builder**.
2. Trabaja el tema mostrado. **Cargar ejemplo sintético** rellena solo ese tema; no confirma ninguna decisión.
3. **Presentar respuestas** valida los campos y muestra una propuesta. **Confirmar tema y continuar** registra la decisión y abre el siguiente tema. Una respuesta incompleta no avanza.
4. En generación, revisa los documentos y confirma. En primera prueba, crea el caso supervisado, abre su revisión en otra pestaña y apruébalo. Regresa al Builder, presenta su identificador y confirma el resultado.
5. Confirma la entrega con el mismo nombre que registraste como propietario. La instancia pasa a `active-demo`: es una demostración, no una certificación de preparación APF.
6. En el espacio de la instancia puedes crear casos y registrar observaciones con evidencia, una serie, un criterio y una fecha. Aprobar una mejora abre el encuadre de un proyecto de cambio; no modifica automáticamente las reglas vigentes.

Cada caso creado desde la instancia conserva `definition_version: 1`, los criterios acordados y la puerta humana L0. La versión no cambia al aprobar una propuesta de mejora.

## Estados y persistencia

El Builder usa un grafo LangGraph independiente con una interrupción por turno. Las respuestas son borradores hasta la confirmación explícita del usuario local. La revisión esperada de cada solicitud evita repetir confirmaciones antiguas. La sesión, las decisiones con anclas de revisión, los artefactos y el registro de instancias se conservan en SQLite. Al reiniciar se sincroniza el registro con el checkpoint del Builder.

Un `no-go` es un resultado válido. Un proyecto o proceso complejo termina en `project-required` con un encuadre, sin fingir que ya existe un proceso operativo. El ciclo completo del proyecto de definición por Architect, Critic y demás agentes es una entrega posterior.

## Chat con OpenAI

El chat por mensajes está documentado en [chat-openai.md](chat-openai.md). Utiliza un nodo de interpretación LangGraph, memoria de respuestas parciales y confirmación humana.

## Modo guiado y modo modelo

Por defecto `APF_BUILDER=guided`: no hay un LLM detrás de las preguntas ni se evalúa automáticamente la suficiencia semántica. Se aplica el guion por temas y se validan campos, fechas y condiciones estructurales. Una persona debe juzgar la calidad del contenido.

Opcionalmente, `APF_BUILDER=openai-compatible` activa interpretación de texto con el mandato y el guion reales del Builder. Usa `APF_LLM_URL`, `APF_LLM_MODEL`, `APF_LLM_API_KEY` y las tarifas documentadas en el README. La respuesta del modelo propone campos y preguntas; nunca confirma temas. Los tokens y las estimaciones de coste cuando se han configurado tarifas se registran en la historia de la sesión, pero todavía no hay presupuesto agregado, recuperación de costes inciertos o conciliación completa para el Builder. No lo actives sin revisar estas limitaciones y el servicio autorizado. No se ha probado contra un proveedor real.

El ejecutor de los casos conserva su configuración `APF_EXECUTOR`; permanece simulado por defecto. Una propuesta simulada demuestra el circuito técnico y no resuelve el negocio.

## Alcance comprobado y pendiente

Se puede recorrer un proceso simple desde su encuadre hasta un caso integrado y una mejora con resolución humana. Se generan una definición, plan de servicio, matriz de permisos, presupuesto, información, checklist, anexo de ejecutor, línea base y registros de las decisiones confirmadas. La checklist marca expresamente lo que no se ha demostrado.

No se ha implementado un agente Critic ni Auditor/Process Reviewer independientes en este recorrido. El panel de auditoría calcula recuentos de la aplicación; no evalúa calidad semántica. Las propuestas de mejora las registra una persona. No hay Distiller, agenda de revisión automática, autenticación corporativa, segregación, despliegue distribuido ni automatización completa del proyecto de cambio. El registro del piloto nombra responsables, pero no acredita su identidad o presencia.

Las fuentes declaradas se registran; no se verifica automáticamente acceso a documentos externos. `required-fields` es una comprobación de infraestructura (contrato, criterios y propuesta no vacíos), no una invariante ejecutable del dominio. Los cuatro presupuestos recogidos son configuración: el mensual se consulta al habilitar casos; no se afirma enforcement completo por caso/cadena ni gasto máximo garantizado por proveedor.

## Pruebas

```bash
python -m unittest discover -s tests -v
python regression/run.py
```

Con Playwright y Chromium disponibles, un servidor de prueba y `APF_TEST_URL` apuntando a él:

```bash
node tests/builder-browser.cjs
node tests/browser.cjs
```

Ambas pruebas crean datos sintéticos. El primer recorrido valida los temas, la primera prueba, la entrega y la resolución de una mejora. El segundo comprueba la revisión de propuestas y los controles existentes.

La viabilidad admite también preguntas de descubrimiento cuando el entregable operativo aún no se puede definir. Esa opción exige un proyecto en el paso de elección de camino; no habilita un proceso simple con criterios pendientes. Las referencias de la conversación se mantienen como notas no verificadas hasta su revisión, sin declararlas conocimiento normativo validado.
