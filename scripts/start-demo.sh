#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if .venv/bin/python - <<'PY'
import socket
with socket.socket() as sock:
    raise SystemExit(0 if sock.connect_ex(('127.0.0.1',8000)) == 0 else 1)
PY
then
  echo 'El puerto 8000 ya está atendido. Abre Puertos → APF Builder.'
else
  nohup .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 >/tmp/apf-builder-server.log 2>&1 &
  echo 'APF Builder arrancando en el puerto 8000. Mantén el puerto privado en Codespaces.'
fi
