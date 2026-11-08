#!/usr/bin/env bash
# Instala la plantilla Curiosidades en la carpeta actual (o en la que pases como argumento).
set -e
DEST="${1:-Curiosidades}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$DEST"/{scripts,ejemplo,shorts}
cp "$AQUI/CLAUDE.md" "$DEST/"
cp "$AQUI"/scripts/*.py "$DEST/scripts/"
cp "$AQUI"/ejemplo/proyecto.json "$DEST/ejemplo/"
command -v ffmpeg >/dev/null || echo "AVISO: instala ffmpeg (con libass) antes de montar."
pip install --quiet --break-system-packages faster-whisper numpy 2>/dev/null || pip install --quiet faster-whisper numpy
echo "Plantilla instalada en $DEST. Abre Claude en esa carpeta y sigue las instrucciones de CLAUDE.md."
