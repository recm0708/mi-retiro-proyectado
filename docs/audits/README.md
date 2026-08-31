# Auditorías y evidencias

**Estado:** vigente como índice de evidencias versionadas
**Clasificación:** Auditoría / Evidencia / Navegación

## Propósito

Este directorio contiene auditorías y evidencias versionadas que conservan trazabilidad durable de decisiones, normalizaciones, validaciones y cierres del proyecto.

Una auditoría preserva el estado que examinó. No debe interpretarse automáticamente como descripción del estado vigente de la aplicación.

Para conocer el estado actual se consulta primero [el índice general de documentación](../README.md).

## Áreas

### Documentación

- [Reconciliación integral de documentación post-G119](documentation/post-g119-documentation-reconciliation.md) — sincronización documental, normativa y estructural posterior a G119/E05.

Auditorías de estructura, clasificación, referencias, estado vivo y normalización documental.

- [Reconstrucción del CHANGELOG histórico — DOC.2 R1](documentation/changelog-reconstruction-doc2-r1.md)
- [Auditoría integral de documentación Markdown post-SEC.2](documentation/documentation-audit-post-sec2.md)
- [Clasificación documental NOR.1 R3](documentation/documentation-classification-nor1-r3.md)
- [Auditoría de dependencias documentales NOR.1 R5](documentation/documentation-dependency-audit-nor1-r5.md)
- [DOC.1 R4 — saneamiento semántico de documentación viva post-G114](documentation/documentation-live-state-doc1-r4.md)
- [Auditoría integral Markdown post-NOR.2 — DOC.1 R2](documentation/documentation-markdown-audit-doc1-r2.md)
- [Auditoría de referencias navegables Markdown — DOC.1 R3](documentation/documentation-markdown-links-doc1-r3.md)
- [Auditoría de normalización documental DOC.1 R5](documentation/documentation-normalization-doc1-r5.md)
- [Auditoría semántica de documentación viva post-G113 — PLAN.2 R1](documentation/post-g113-live-documentation-audit-plan2-r1.md)

### Gobierno y versionado

Auditorías de reconciliación revision-aware y gobierno de Releases.

- [Auditoría de reconciliación revision-aware posterior a G070](governance/post-g070-revision-reconciliation.md)
- [REL.GOV.1 R2 — automatización gobernada de Releases](governance/rel-gov1-r2-release-automation.md)

### Repositorio

Auditorías de normalización, nomenclatura, estructura y artefactos del repositorio.

- [Auditoría de nomenclatura NOR.1 R4](repository/naming-audit-nor1-r4.md)
- [Línea base de normalización NOR.2 R1](repository/repository-normalization-baseline-nor2-r1.md)
- [Auditoría integral y cierre formal NOR.2 R8](repository/repository-normalization-final-audit-nor2-r8.md)
- [NOR.2 R5 — archivo y consolidación de documentación histórica](repository/repository-normalization-historical-docs-nor2-r5.md)
- [NOR.2 R6 — migración del ledger y datos de alto impacto](repository/repository-normalization-ledger-data-nor2-r6.md)
- [NOR.2 R4 — migración de documentación viva](repository/repository-normalization-live-docs-nor2-r4.md)
- [NOR.2 R7 — migración y depuración de artefactos locales](repository/repository-normalization-local-artifacts-nor2-r7.md)
- [Matriz de decisión de migración NOR.2 R2](repository/repository-normalization-migration-matrix-nor2-r2.md)
- [NOR.2 R3 — migración de runtime y configuración](repository/repository-normalization-runtime-migration-nor2-r3.md)
- [Cierre de estándares del repositorio NOR.1 R7](repository/repository-standards-closure-nor1-r7.md)
- [NOR.1 R8 — auditoría de identificadores de bloques](repository/work-block-identifier-audit-nor1-r8.md)

### Seguridad

Auditorías de hardening, CodeQL y cierre de controles de seguridad.

- [SEC.2 — Cierre integral y auditoría post-cierre de seguridad](security/sec2-final-closure.md)
- [SEC.2 R1 — CodeQL DOM hardening y normalización de workflows](security/sec2-r1-codeql-workflow-hardening.md)

## Regla de conservación

Las evidencias de esta carpeta no se reescriben para aparentar vigencia posterior. Cuando una auditoría queda superada por otra revisión, se conserva como evidencia histórica salvo que se demuestre que es un duplicado exacto o un residuo sin valor documental.

## Nuevas auditorías

Las auditorías nuevas deben seguir [los estándares de documentación](../standards/documentation-standards.md), [las convenciones de nombres](../standards/naming-conventions.md) y [el ciclo de vida de archivos](../standards/artifact-lifecycle.md).
