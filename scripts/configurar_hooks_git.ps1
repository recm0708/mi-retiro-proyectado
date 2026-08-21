$ErrorActionPreference = "Stop"

$repoRoot = (& git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($repoRoot)) {
    throw "No se pudo determinar la raíz del repositorio Git."
}

Set-Location $repoRoot

$hook = Join-Path $repoRoot ".githooks\pre-commit"
$guard = Join-Path $repoRoot "scripts\validar_precommit.py"

if (-not (Test-Path -LiteralPath $hook -PathType Leaf)) {
    throw "Falta el hook versionado: .githooks/pre-commit"
}

if (-not (Test-Path -LiteralPath $guard -PathType Leaf)) {
    throw "Falta el validador versionado: scripts/validar_precommit.py"
}

& git config --local core.hooksPath .githooks
if ($LASTEXITCODE -ne 0) {
    throw "No se pudo configurar core.hooksPath."
}

$configurado = (& git config --local --get core.hooksPath).Trim()
if ($configurado -ne ".githooks") {
    throw "core.hooksPath no quedó configurado correctamente. Valor actual: $configurado"
}

Write-Host "Gate pre-commit activado para este clon: $repoRoot"
Write-Host "Git rechazará el commit si el árbol no es reproducible o falla alguna validación."
