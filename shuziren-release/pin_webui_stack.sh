#!/usr/bin/env bash
# Gradio 4.44 + 新版 Starlette 可能触发首页模板错误。
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$ROOT/.venv-gptsovits/bin/activate"
pip install 'starlette==0.41.3' 'fastapi==0.115.6'
