#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then echo "Python 3.10+ not found on PATH; install it and restart Git Bash." >&2; exit 127; fi
exec "$PYTHON_BIN" "$ROOT/scripts/pipeline.py" stage collector-podcast "$@"


