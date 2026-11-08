# Instala la plantilla Curiosidades con un solo comando (PowerShell):
#   iwr https://raw.githubusercontent.com/luigi6599/curiosidades-plantilla/main/descargar.ps1 | iex
param([string]$Dest = ".\Curiosidades", [string]$UrlZip = "https://github.com/luigi6599/curiosidades-plantilla/archive/refs/heads/main.zip")
$tmp = Join-Path $env:TEMP ("curio_" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $tmp | Out-Null
Invoke-WebRequest $UrlZip -OutFile "$tmp\p.zip"
Expand-Archive "$tmp\p.zip" -DestinationPath $tmp
& "$tmp\curiosidades-plantilla-main\instalar.ps1" -Dest $Dest
