#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT/GPT-SoVITS"
source "$ROOT/.venv-gptsovits/bin/activate"
export GRADIO_SERVER_NAME="${GRADIO_SERVER_NAME:-127.0.0.1}"
exec python -u webui.py "${@:-zh_CN}"
