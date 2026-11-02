#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "This build must run on macOS; PyInstaller cannot create a macOS app from Linux or Windows." >&2
    exit 1
fi

PYTHON_BIN="${PYTHON:-python3}"
if ! "$PYTHON_BIN" -c 'import tkinter' >/dev/null 2>&1; then
    echo "The selected Python has no Tk support. Install a macOS Python distribution with Tkinter, then retry." >&2
    exit 1
fi

VENV_DIR="${VENV_DIR:-.venv-macos}"
"$PYTHON_BIN" -m venv "$VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip
python -m pip install -r requirements-macos-build.txt

# Big Sur is macOS 11.0. Build on the target Mac/architecture for best compatibility.
export MACOSX_DEPLOYMENT_TARGET=11.0
python -m PyInstaller \
    --noconfirm \
    --clean \
    --distpath dist/macos \
    --workpath build/macos \
    epson_print_conf_macos.spec

APP_PATH="dist/macos/Epson Printer Configuration.app"
if [[ ! -d "$APP_PATH" ]]; then
    echo "PyInstaller completed, but the expected .app bundle was not created: $APP_PATH" >&2
    exit 1
fi

ARCH="$(uname -m)"
ARCHIVE="dist/macos/Epson-Printer-Configuration-macOS-${ARCH}.zip"
ditto -c -k --sequesterRsrc --keepParent "$APP_PATH" "$ARCHIVE"
echo "Built app: $APP_PATH"
echo "ZIP archive: $ARCHIVE"
echo "Architecture: $ARCH (native to this Mac)"
