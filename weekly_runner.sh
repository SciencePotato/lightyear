#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
source venv/bin/activate
python3 weekly_writers_main.py "$@"
