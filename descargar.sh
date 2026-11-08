#!/usr/bin/env bash
# Instala la plantilla Curiosidades con un solo comando:
#   curl -fsSL https://raw.githubusercontent.com/luigi6599/curiosidades-plantilla/main/descargar.sh | bash
set -e
URL_ZIP="${URL_ZIP:-https://github.com/luigi6599/curiosidades-plantilla/archive/refs/heads/main.zip}"
TMP="$(mktemp -d)"
curl -fsSL "$URL_ZIP" -o "$TMP/p.zip"
unzip -q "$TMP/p.zip" -d "$TMP"
bash "$TMP"/curiosidades-plantilla-main/instalar.sh "${1:-Curiosidades}"
