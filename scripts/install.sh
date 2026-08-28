#!/usr/bin/env bash

set -euo pipefail

PROJECT_NAME="rembg-wrapper"
COMMAND_NAME="rembgwrap"

DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
BIN_HOME="${XDG_BIN_HOME:-$HOME/.local/bin}"

INSTALL_DIR="$DATA_HOME/$PROJECT_NAME"
BIN_PATH="$BIN_HOME/$COMMAND_NAME"

SCRIPT_DIR="$(
    cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1
    pwd
)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"


if ! command -v uv >/dev/null 2>&1; then
    echo "Error: uv is required but was not found."
    echo
    echo "Install uv first:"
    echo "  https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi


echo "Installing $PROJECT_NAME..."
echo "  Source:  $PROJECT_DIR"
echo "  Install: $INSTALL_DIR"
echo "  Command: $BIN_PATH"
echo


mkdir -p "$DATA_HOME"
mkdir -p "$BIN_HOME"

rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

cp -a "$PROJECT_DIR/." "$INSTALL_DIR/"

# Do not copy development environment.
rm -rf "$INSTALL_DIR/.venv"
rm -rf "$INSTALL_DIR/.git"


echo "Creating environment..."

uv sync \
    --project "$INSTALL_DIR" \
    --frozen


cat > "$BIN_PATH" <<EOF
#!/usr/bin/env bash
set -euo pipefail

exec uv run \
    --project "$INSTALL_DIR" \
    --frozen \
    rembgwrap "\$@"
EOF

chmod +x "$BIN_PATH"


echo
echo "Installed successfully."
echo
echo "Command:"
echo "  $COMMAND_NAME"
echo

if [[ ":$PATH:" != *":$BIN_HOME:"* ]]; then
    echo "Warning: $BIN_HOME is not in PATH."
    echo
    echo "Add this line to ~/.bashrc:"
    echo
    echo '  export PATH="$HOME/.local/bin:$PATH"'
    echo
    echo "Then run:"
    echo
    echo "  source ~/.bashrc"
fi
