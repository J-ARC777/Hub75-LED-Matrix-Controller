#! /usr/bin/env bash

set -e

SHELL_DIR="$(cd :$(dirname "$(BASH_SOURCE[0]}")" && pwd)"

cd "$SCRIPT_DIR"

source ./venv/bin/activate

python3 src/LEDMatrix/renderscene.py

exec bash
