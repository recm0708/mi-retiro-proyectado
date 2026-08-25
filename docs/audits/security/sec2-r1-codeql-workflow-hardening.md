# SEC.2 R1 — CodeQL DOM hardening y normalización de workflows

**Estado:** en ejecución
**Clasificación:** auditoría / seguridad
**Revisión:** SEC.2 R1
**Fecha:** 2026-08-25
**Versión de aplicación revisada:** `0.0.71.01-beta`

## Objetivo

SEC.2 R1 inicia el hardening de seguridad posterior a NOR.2 y DOC.1 R2.

El alcance de esta revisión se concentra en dos hallazgos CodeQL de tipo
`DOM text reinterpreted as HTML` y en la normalización técnica de los nombres
visibles de GitHub Actions.

## Hallazgos CodeQL

CodeQL reportó dos sinks dinámicos en
`app/static/js/results_orchestration.js`, originalmente ubicados alrededor de
las líneas 1096 y 1167.

Ambos utilizaban `innerHTML` para construir partes del informe imprimible con
valores dinámicos.

La corrección sustituyó esos sinks por DOM API segura mediante:

- `document.createElement`;
- `textContent`;
- `document.createTextNode`;
- `append`.

Los tres usos restantes de `innerHTML` fueron revisados y se conservaron porque
contienen únicamente estructura y texto estático, sin interpolación dinámica.

## GitHub Actions

Los workflows propios quedaron normalizados con nombres técnicos en inglés:

- `Continuous Integration`;
- `Repository Governance Audit`;
- `Markdown Audit`;
- `Git Tag Signature Verification`.

## Regresión

Se agregó:

`tests/test_sec2_r1_codeql_workflow_hardening.py`

La regresión protege la ausencia de los dos sinks dinámicos y los nombres
canónicos de los workflows.

## Validación local integral

Hasta este checkpoint:

- pruebas focales SEC.2/UX: **30 pruebas + 4 subtests — OK**;
- regresión transversal posterior: **37 pruebas + 62 subtests — OK**;
- `node --check`: **OK**;
- auditor Markdown: **OK**;
- `git diff --check`: **OK**;
- suite completa `pytest`: **1043 pruebas + 4922 subtests — OK**;
- pre-commit integral: **1003 tests — OK**.

La revisión permanece abierta hasta completar PR, CI, CodeQL, integración
y verificación post-merge.
