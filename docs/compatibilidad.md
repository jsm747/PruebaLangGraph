# Comparación con el piloto original

La PoC incluye ahora un grafo de configuración del Builder con confirmaciones y un panel local de mejora. Véase [alcance y límites de ese recorrido](poc-builder.md). El resto de la tabla distingue los mecanismos operativos de una implementación completa de APF.

Referencia: `jsm747/jsm747-apf-pilot` en `78008e0da6f3040888c136fe5fff4e72510b1b8f`, especialmente `protocol/protocol.yml`, `scripts/orch.py`, los workflows de roles y `platform/substrate-binding.md`. Esta tabla describe la implementación local, no una certificación de equivalencia de seguridad o de producción.

| Requisito / mecanismo | Situación en el prototipo |
|---|---|
| R1 · Contrato de tarea | **Parcial.** Contrato, instancia, serie, criterios, invariantes, alcance y siguiente tarea; validación de campos al crear. API local, no Issue Form. |
| R2 · Estado y hechos materializados | **Parcial.** Estados y actividad persistidos en SQLite/checkpoints. No hay identidad verificada ni enforcement equivalente de autores de cada hecho. |
| R3 · Orquestador | **Parcial.** Cola por serie, pausa, modificación, siguiente tarea y recuperación al reiniciar. Un solo proceso; sin reconciliador periódico, timeouts equivalentes ni dos relanzamientos garantizados. |
| R4 · Propuesta e integración | **Parcial.** Propuesta, decisión y artefacto local versionado; se detectan propuestas obsoletas. Con visor local de diferencias; sin PR, merge corporativo ni rollback. |
| R5 · Alcance | **Implementado para propuestas de archivos.** Se compara el alcance declarado con los cambios usando el comprobador original; el adaptador de modelo no puede escribir fuera del contrato. |
| R6 · Comprobaciones | **Implementado para estos cuatro controles.** La promoción requiere `append-only`, `citations`, `layer` y `scope` en verde, y se vuelven a ejecutar al aprobar. |
| R7 · Decisiones y clasificación | **Pendiente.** Se incluye y prueba el router determinista original, pero no está conectado al grafo y no existe clasificador. Se mantiene la aprobación humana L0. |
| R8 · Sesiones y telemetría | **Parcial.** Registro local por sesión; el adaptador opcional conserva modelo, tokens y coste estimado si el proveedor informa el uso. Sin eventos de herramientas, OpenTelemetry completo ni cobertura de todos los fallos. |
| R9 · Modelo, fallback y override | **Parcial.** Simulador y adaptador opcional a chat compatible; configuración por variables. Sin fallback automático ni equivalencia con las sesiones de Claude Code. |
| R10 · Actor, herramientas y registro | **Pendiente.** La revisión es local sin autenticar; no hay identidad por rol ni sandbox de herramientas. El adaptador de modelo solo devuelve JSON y no ejecuta herramientas. |
| R11 · Decisiones append-only y citas | **Implementado para propuestas sobre el almacén local.** Se usan los scripts originales y los artefactos existentes como base. |
| R12 · Un escritor por capa | **Parcial.** Se usa el mapa y comprobador originales para el rol `executor`; no existen todavía los otros roles operativos ni identidad real vinculada al rol. |
| R13 · Aislamiento y clasificación | **Pendiente.** Sin separación corporativa de corpus o identidades. Solo datos sintéticos en local. |
| R14 · Colas separadas | **Parcial.** Hay tareas y propuestas de mejora local separadas; auditoría y revisión por agentes siguen pendientes. |
| R15 · Aprobaciones y digest | **Parcial.** Decisiones de temas y de mejoras con motivos y criterios persistidos. Sin aprobación autenticada, directorio, límites por rol ni digest corporativo. |
| R16 · Liveness independiente | **Pendiente.** No hay monitor independiente; la recuperación se intenta al arrancar. |
| R17 · Presupuesto | **Parcial.** Límite mensual previo a la sesión, costes estimados para el adaptador y bloqueo por coste desconocido. Sin límite monetario garantizado por el proveedor, gestión corporativa de presupuestos o conciliación por interfaz. |
| R18 · Efectos externos | **Parcial.** No hay herramientas para publicar o escribir en otros sistemas. El adaptador de modelo, si se configura, envía contexto al endpoint elegido. |
| R19 · Directorio y escalada humana | **Pendiente.** No hay directorio, suplentes, avisos ni SLA. |
| R20 · Ingesta y auditoría | **Parcial.** Patrones de enmascaramiento y avisos de inyección adaptados del original, aplicados antes del ejecutor. No son exhaustivos; sin auditoría resistente a manipulación. |
| R21 · Registro | **Parcial.** Valida estado y fechas del archivo copiado y de las instancias creadas por el Builder. No integra un registro empresarial ni gobierna identidades. |

El banco original ejecuta **25 casos deterministas**. Sus ocho casos de roles no son ejecutados por `regression/run.py`, aunque la salida diga `0 pending`; se ejecutaban en el workflow de Claude. Las pruebas locales adicionales cubren el grafo, la revisión, la recuperación, los controles y el adaptador con respuestas simuladas. No se han ejecutado los tests de integración que crean issues, ramas o PR en GitHub.
