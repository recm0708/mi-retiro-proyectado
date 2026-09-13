# Política estructural del repositorio

**Estado:** Vigente / NOR.3 R2, enforcement físico activado en R5

**Issue propietario:** #128

**Política machine-readable:** `data/governance/repository-structure-policy.json`

## Objetivo

Convertir las decisiones del inventario NOR.3 R1 en guardas reproducibles.
R5 activa el enforcement físico de backend/templates/assets ya materializados,
mientras R6–R8 completan tests, data y cierre integral.

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

## Ownership materializado

R3–R5 hacen exigible el ownership de portales, templates y assets. `app/static/shared/`
contiene contratos multiportal; `app/static/asegurado/` pertenece a la experiencia
pública y `app/static/developer/` al Portal Developer. La marca runtime vive en
`app/static/shared/img/brand/`.

## Regla de mantenimiento

Toda migración estructural posterior debe actualizar en el mismo lote rutas,
consumidores, política machine-readable, auditor, pruebas y documentación.
No se aceptan excepciones silenciosas.

<!-- NOR3-R6-TEST-TAXONOMY -->

## NOR.3 R6 — Contrato de pruebas

La política estructural activa una taxonomía de pruebas verificable. No
se permiten módulos `test_*.py` directamente en `tests/`; cada módulo
debe tener un único owner semántico. El helper HTTP común reside en
`tests/shared/` y el discovery recursivo continúa siendo el mecanismo
canónico.
