#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  printf '%s\n' 'Python 3 was not found on PATH.' >&2
  printf '%s\n' 'Install Python 3.10 or newer, close and reopen Git Bash, then verify with: python --version' >&2
  printf '%s\n' 'If Python is installed in a custom location, set PYTHON_BIN to its executable path.' >&2
  exit 127
fi
exec "$PYTHON_BIN" "$ROOT/scripts/pipeline.py" run "$@"

