# Instala la plantilla Curiosidades en la carpeta indicada (por defecto .\Curiosidades).
param([string]$Dest = ".\Curiosidades")
$aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -ItemType Directory -Force -Path "$Dest\scripts","$Dest\ejemplo","$Dest\shorts" | Out-Null
Copy-Item "$aqui\CLAUDE.md" $Dest -Force
Copy-Item "$aqui\scripts\*.py" "$Dest\scripts" -Force
Copy-Item "$aqui\ejemplo\proyecto.json" "$Dest\ejemplo" -Force
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { Write-Host "AVISO: instala ffmpeg (con libass) antes de montar." }
pip install --quiet faster-whisper numpy
Write-Host "Plantilla instalada en $Dest. Abre Claude en esa carpeta y sigue las instrucciones de CLAUDE.md."
