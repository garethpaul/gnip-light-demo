#!/usr/bin/env sh
set -eu

PYTHON=${PYTHON:-python3}

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    printf 'check-python3: Python command not found: %s\n' "$PYTHON" >&2
    exit 1
fi

python_major=$("$PYTHON" -c 'import sys; sys.stdout.write(str(sys.version_info[0]))' 2>/dev/null || true)
if [ "$python_major" != "3" ]; then
    printf 'check-python3: Python 3 is required: %s\n' "$PYTHON" >&2
    exit 1
fi
