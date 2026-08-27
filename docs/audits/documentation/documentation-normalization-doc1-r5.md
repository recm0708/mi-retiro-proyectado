# Auditoría de normalización documental DOC.1 R5

**Estado:** candidato validado localmente; no aceptado
**Fecha:** 2026-08-27
**Versión de aplicación revisada:** `0.1.15.04-beta`
**Bloque:** DOC.1 R5
**Candidato revision-aware:** G116/E05 (`0.1.16.05-beta`)
**Clasificación:** auditoría / documentación / gobierno

## Objetivo

Validar integralmente la normalización documental previa a la aceptación de
DOC.1 R5, sin consumir G116 ni modificar la versión publicada G115/E04.

## Base auditada

- rama de trabajo: `docs/doc1-r5-documentation-normalization`;
- base publicada: `87fa8e98688c1e3951cc405eb4b280d558d1c8a6`;
- `VERSION`: `0.1.15.04-beta`;
- `accepted_count`: `115`;
- siguiente Global disponible: `G116`;
- candidato reservado: `DOC.1 R5 / G116/E05 / 0.1.16.05-beta`;
- REL.GOV.1 R2 permanece como siguiente checkpoint planificado sin Global
  preasignado.

## Alcance ejecutado

DOC.1 R5 normaliza referencias navegables Markdown, reconcilia el estado vivo
posterior a la publicación de G115, completa la política y las plantillas para
`.md`, endurece el auditor Markdown y corrige regresiones históricas que
convertían snapshots anteriores en obligaciones sobre el estado vigente.

La primera pasada humanizó `196` etiquetas de documentos Markdown y `6`
referencias inequívocas de directorio. La pasada de presentación aplicó formato
de índice únicamente donde correspondía. La reconciliación posterior eliminó
las referencias vivas a la reserva G116/E02 y conservó exclusivamente las
menciones históricas contextualizadas.

## Plantillas y estándar Markdown

La cobertura de plantillas se amplió con una base técnica `template.md` y una
familia semántica para:

- documento vigente;
- estándar o política;
- auditoría o evidencia;
- registro histórico;
- ADR.

Antes de incorporar esta familia, el inventario rastreado contenía `149`
Markdown y una sola plantilla Markdown. El gate pre-evidencia registra:

- Markdown auditados: `157`;
- VIVO: `58`;
- AUDITORIA: `22`;
- HISTORICO: `64`;
- PLANTILLA: `9`;
- SOPORTE: `4`.

La presente evidencia se incorpora después de ese conteo y, una vez añadida al
índice Git, incrementará AUDITORIA y el total Markdown en una unidad.

## Auditor Markdown

`scripts/audit_markdown.py` incorpora dos controles nuevos:

- `ETIQUETA_DOCUMENTAL_TECNICA`: detecta etiquetas de ruta/nombre `.md` en
  listas navegables activas cuando corresponde un título humano;
- `CANDIDATO_REVISION_AWARE_OBSOLETO`: detecta reservas vivas del Global actual
  que contradigan el candidato machine-readable.

El control del candidato se aplica al auditar el repositorio completo. Las
pruebas unitarias aisladas de `audit_file()` permanecen desacopladas del ledger
para poder ejecutarse sobre repositorios temporales mínimos.

## Preservación histórica

Las regresiones heredadas de DOC.1 R1, VER.2 R1–R4, DOC.2 R1, NOR.1 R8 y
PLAN.2 R1 fueron ajustadas para proteger hechos históricos sin congelar como
estado actual una versión, un número de Releases o un candidato posterior.

Las referencias permitidas a la antigua reserva G116/E02 son:

- `CHANGELOG.md:15:- Ledger al publicar G115: G116/E02 (`0.1.16.02-beta`) quedó reservado para REL.GOV.1 R2; DOC.1 R5 replanifica posteriormente esa reserva no consumida como G116/E05 (`0.1.16.05-beta`).`
- `RELEASES.md:15:- La reserva G116/E02 para REL.GOV.1 R2 fue la planificación vigente al publicar G115; DOC.1 R5 reasigna posteriormente el Global todavía no consumido a G116/E05 (`0.1.16.05-beta`). REL.GOV.1 R2 permanece a continuación sin Global preasignado.`
- `tests/test_doc1_r5_markdown_auditor.py:88:                "G116/E02 (`0.1.16.02-beta`)."`
- `tests/test_doc1_r5_markdown_auditor.py:119:                        "Al publicar G115, G116/E02 "`
- `tests/test_doc1_r5_markdown_auditor.py:120:                        "(`0.1.16.02-beta`) quedó reservado."`

No se detectaron referencias vivas adicionales a esa reserva.

## Gates ejecutados

- `unittest discover`: **1127 tests / OK / 3.831 s**;
- `pytest`: **1167 passed / 5587 subtests passed / 6.35 s**;
- `python -m compileall app tests scripts -q`: **OK**;
- `python -m pip check`: **No broken requirements found**;
- JavaScript con `node --check`: **18 archivos / OK**;
- auditor Markdown: **157/157 OK**;
- auditor de bloques: **16 familias / 46 identificadores / OK**;
- `release_contract.py --json`: **G115/E04 vigente; G116/E05 DOC.1 candidato**;
- `git diff --check`: **OK**;
- `git diff --cached --check`: **OK**.

## Resumen del cambio local previo a esta evidencia

```text
 CHANGELOG.md                                       |   6 +-
 CODE_OF_CONDUCT.md                                 |   8 +-
 CONTRIBUTING.md                                    |  20 +-
 GOVERNANCE.md                                      |   8 +-
 README.md                                          | 124 ++++-----
 RELEASES.md                                        |  10 +-
 SECURITY.md                                        |   6 +-
 SUPPORT.md                                         |   6 +-
 VERSIONING.md                                      |   6 +-
 data/pre-1-0-revision-ledger.json                  |   6 +-
 data/work-block-registry.json                      |  18 +-
 docs/README.md                                     | 260 +++++++++----------
 docs/architecture/calculation-engine.md            |   2 +-
 docs/architecture/development-center.md            |   2 +-
 docs/architecture/system-architecture.md           |   4 +-
 docs/decisions/README.md                           |   2 +-
 docs/governance/master-plan-to-1-0.md              |  12 +-
 docs/governance/pre-1-0-pending-matrix.md          |  51 ++--
 docs/governance/pre-1-0-revision-ledger.md         |   8 +-
 docs/governance/roadmap.md                         |  11 +-
 docs/operations/release-process.md                 |   6 +-
 docs/operations/validation.md                      |   4 +-
 docs/product/traceability-matrix.md                |   4 +-
 docs/standards/README.md                           |   4 +-
 docs/standards/documentation-standards.md          |  34 +++
 docs/standards/file-structure-by-extension.md      |  16 +-
 docs/templates/README.md                           |  28 ++
 docs/templates/documentation/README.md             |  27 ++
 docs/templates/documentation/adr.md                |  34 +++
 docs/templates/documentation/audit-evidence.md     |  42 +++
 docs/templates/documentation/historical-record.md  |  28 ++
 docs/templates/documentation/live-document.md      |  37 +++
 docs/templates/documentation/standard-policy.md    |  30 +++
 docs/templates/file-structure/README.md            |   4 +
 docs/templates/file-structure/template.md          |  30 +++
 scripts/audit_markdown.py                          | 284 +++++++++++++++++++++
 .../test_doc1_r1_auditoria_markdown_post_mant1.py  |  26 +-
 tests/test_doc1_r5_markdown_auditor.py             | 130 ++++++++++
 tests/test_doc1_r5_markdown_standards.py           |  80 ++++++
 tests/test_doc2_r1_changelog_reconstruction.py     |   4 +-
 tests/test_g115_promotion_post_merge.py            |  50 +++-
 tests/test_mant1_r5d_politica_extensiones.py       |   2 +
 tests/test_nor1_r8_work_block_identifiers.py       |  10 +-
 tests/test_plan2_r1_master_pending_matrix.py       |  11 +-
 tests/test_release_governance_contract.py          |  14 +-
 tests/test_ver2_r1_reconciliacion_post_doc1.py     |   4 +-
 tests/test_ver2_r2_documentacion_viva_post_r1.py   |  18 +-
 ...t_ver2_r3_decision_version_candidata_post_r2.py |   4 +-
 tests/test_ver2_r4_promocion_g071_e01.py           |   8 +-
 tests/validation_cases/README.md                   |   2 +-
 50 files changed, 1190 insertions(+), 355 deletions(-)
```

## Resultado

El candidato DOC.1 R5 supera los gates locales funcionales, documentales,
estructurales y de gobierno ejecutados en esta auditoría.

Esta evidencia **no constituye aceptación de G116**, no modifica `VERSION`, no
crea tag ni GitHub Release y no preasigna un Global a REL.GOV.1 R2. La
aceptación depende todavía del commit firmado, Pull Request, checks remotos,
integración y procedimiento de promoción aplicable.
