# Política estructural del repositorio

**Estado:** Vigente / NOR.3 R2

**Issue propietario:** #128

**Política machine-readable:** `data/repository-structure-policy.json`

## Objetivo

Convertir las decisiones del inventario NOR.3 R1 en guardas reproducibles sin
forzar todavía los movimientos físicos reservados para R3–R8.

La política se consume desde `scripts/audit_repository_integrity.py`, que ya
forma parte de `scripts/quality_gate.py`. Por tanto, una violación estructural
bloqueante se propaga automáticamente al Quality Gate.

## Raíces autorizadas

Se autorizan `.githooks/`, `.github/`, `.vscode/`, `app/`, `assets/`, `data/`,
`docs/`, `regulations/`, `scripts/` y `tests/`.

Una raíz nueva requiere decisión estructural explícita y actualización de la
política en el mismo lote.

## Entry points y rutas requeridas

Se protegen, entre otros, `app/main.py`, `app/cli/admin.py`,
`scripts/quality_gate.py`, `scripts/audit_repository_integrity.py`,
`requirements.txt`, `requirements-dev.txt` y `VERSION`.

## Datos locales protegidos

`data/developer/` se considera estado local de una fase futura y no debe
versionarse durante NOR.3. También se bloquean logs, temporales, parches,
archivos comprimidos y bases SQLite/DB accidentales.

## Profundidad

NOR.3 no adopta una profundidad máxima ciega. El inventario R1 observó 16
archivos en profundidad 6, todos dentro de fuentes regulatorias oficiales.
Se usa una base de profundidad 5 y se permiten explícitamente hasta 6 niveles
solo para:

- `docs/regulatory/sources/official/pensions/normative/`;
- `docs/regulatory/sources/official/pensions/reference/`;
- `docs/regulatory/sources/official/privacy/normative/`.

Estas excepciones existen por procedencia y semántica, no para eludir el gate.

## Ownership futuro

La política registra, pero todavía no exige físicamente, los namespaces
`app/portals/asegurado` y `app/portals/developer`. Su enforcement se activa
cuando R3–R5 materialicen backend/templates/assets.

## Regla de mantenimiento

Toda migración estructural posterior debe actualizar en el mismo lote rutas,
consumidores, política machine-readable, auditor, pruebas y documentación.
No se aceptan excepciones silenciosas.
