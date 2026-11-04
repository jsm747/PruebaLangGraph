# APF · prototipo local con LangGraph

Una primera prueba de un flujo de trabajo con revisión humana: una persona crea una tarea sintética, un ejecutor **simulado** prepara una propuesta, una comprobación básica la valida y LangGraph detiene la ejecución hasta que una persona la aprueba o rechaza. No se llama a ningún modelo real.

## Requisitos y arranque

Requiere Python 3.10 o superior. Desde la raíz del repositorio:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abre `http://127.0.0.1:8000` en el navegador de tu propia máquina. La documentación de la API está en `/docs`. Por defecto, el estado se guarda en `data/prototype.sqlite3` y sobrevive al reinicio del proceso. Puedes seleccionar otra carpeta con `APF_DATA_DIR`.

```bash
python -m unittest discover -s tests -v
```

## Alcance

- API FastAPI, interfaz web estática y un grafo LangGraph con checkpoints SQLite.
- Una tarea queda en `proposed` hasta recibir una decisión explícita; una aprobación pasa a `integrated` y un rechazo a `rejected`. Una tarea ya decidida no admite una segunda decisión.
- `integrated` significa que la propuesta fue aceptada en este prototipo: no publica contenido ni modifica sistemas externos. Para corregir una propuesta rechazada hay que crear otra tarea.
- Un único proceso atiende las operaciones; no se garantiza concurrencia entre varios workers. No hay autenticación, control de acceso ni conexión a un modelo real. No desplegarlo como servicio accesible por terceros ni introducir información real o sensible.
- Los checkpoints y el índice de tareas son persistentes, pero no hay recuperación automática completa ante interrupciones entre todas las operaciones, copias de seguridad ni garantía de exactamente una ejecución.

## Siguiente paso

Sustituir el generador simulado por un adaptador para un modelo autorizado, añadir identidad y permisos corporativos, y escoger almacenamiento, trazabilidad y despliegue según las herramientas disponibles. Mantener el límite humano del piloto hasta definir otra política.
