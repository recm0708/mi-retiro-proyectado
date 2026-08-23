# Mi Retiro Proyectado — nombre del script.
#
# Propósito:
# - describir qué prepara, valida o automatiza este script.
#
# Alcance:
# - indicar entradas esperadas, archivos que toca y límites de ejecución.

Set-StrictMode -Version Latest

$ErrorActionPreference = "Stop"

# Validación defensiva antes de ejecutar operaciones que dependan de rutas.
$RaizRepositorio = Resolve-Path "."
Write-Output "Repositorio: $RaizRepositorio"
