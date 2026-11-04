#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -z "${APF_LLM_API_KEY:-}" ]]; then
  echo 'Falta APF_LLM_API_KEY. Añádela como secreto de Codespaces y reinicia el Codespace. No pegues la clave en el chat.' >&2
  exit 1
fi
export APF_BUILDER=openai-compatible
export APF_LLM_PROVIDER="${APF_LLM_PROVIDER:-openai}"
export APF_LLM_MODEL="${APF_LLM_MODEL:-gpt-4.1}"
.venv/bin/python - <<'PY'
from app.llm import ChatConfig
config=ChatConfig.read()
print(f'Chat configurado: {config.provider}, modelo {config.model}. La conexión se comprobará al enviar un mensaje.')
PY
exec .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
