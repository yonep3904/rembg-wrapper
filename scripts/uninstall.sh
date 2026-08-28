#!/usr/bin/env bash

set -euo pipefail

PROJECT_NAME="rembg-wrapper"
COMMAND_NAME="rembgwrap"

DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
BIN_HOME="${XDG_BIN_HOME:-$HOME/.local/bin}"

INSTALL_DIR="$DATA_HOME/$PROJECT_NAME"
BIN_PATH="$BIN_HOME/$COMMAND_NAME"

echo "Uninstalling $PROJECT_NAME..."
echo "  Install: $INSTALL_DIR"
echo "  Command: $BIN_PATH"
echo

removed=false

if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf "$INSTALL_DIR"
    echo "Removed: $INSTALL_DIR"
    removed=true
else
    echo "Not found: $INSTALL_DIR"
fi

if [[ -e "$BIN_PATH" || -L "$BIN_PATH" ]]; then
    rm -f "$BIN_PATH"
    echo "Removed: $BIN_PATH"
    removed=true
else
    echo "Not found: $BIN_PATH"
fi

echo

if [[ "$removed" == true ]]; then
    echo "Uninstalled successfully."
else
    echo "$PROJECT_NAME is not installed."
fi
