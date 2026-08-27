# DOC.1 R4 — saneamiento semántico de documentación viva post-G114

**Estado:** candidato G115/E04, no aceptado
**Base auditada:** `5c6d2db1d02e4482dde27cdfaf1503cf7cfe84cd`
**Versión canónica durante la revisión:** `0.1.14.01-beta` — G114/E01
**Siguiente candidato reservado:** `0.1.15.04-beta` — DOC.1 R4
**Fecha:** 2026-08-26
**Clasificación:** Auditoría documental / Estado vivo / Gobierno

## Objetivo

DOC.1 R4 sanea afirmaciones de estado vivo que quedaron desactualizadas después
de integrar, etiquetar y publicar G114/E01. La revisión no reescribe historia,
no sustituye evidencia de gates anteriores y no adelanta G115.

## Línea base

Antes de modificar documentación se verificó:

- `main` en `5c6d2db1d02e4482dde27cdfaf1503cf7cfe84cd`;
- working tree limpio;
- `VERSION = 0.1.14.01-beta`;
- `accepted_count = 114`;
- `next_global = 115`;
- `next_candidate = 0.1.15.04-beta`;
- `next_candidate_block = DOC.1`;
- 148 Markdown sin bloqueadores;
- 16 familias y 46 identificadores registrados.

El inventario semántico amplio produjo 313 coincidencias. Un segundo barrido
de precisión produjo 59 candidatos. Ninguna de esas cantidades se interpreta
automáticamente como número de errores: la revisión manual distingue estado
vivo, historia, evidencia contractual, ADR y pendientes reales de producto.

## Hallazgos vivos corregidos

Se corrigen exclusivamente superficies que todavía podían afirmar que:

- G113/E03 era el último tag revision-aware publicado;
- G114/E01 o su GitHub Release continuaban pendientes;
- PERSIST.1 seguía reservado como G114/E01;
- una sección denominada estado vigente conservaba una versión anterior;
- el ledger Markdown o el roadmap terminaban operativamente en G113/G114.

También se actualiza la evidencia de la promoción PR #95, el tag firmado
`v0.1.14.01-beta` y el GitHub Release prerelease correspondiente.

## Evidencia preservada

No se modernizan mecánicamente:

- `docs/archive/`;
- auditorías cerradas;
- entradas históricas de `CHANGELOG.md`;
- gates históricos de `docs/operations/validation.md`;
- ADR y decisiones que describen una versión válida en su momento;
- referencias históricas a candidatos fallidos o reservas posteriormente
  sustituidas cuando el contexto deja claro que pertenecen a aquel checkpoint;
- pendientes jurídicos, normativos, de accesibilidad, persistencia o producto
  que continúan siendo requisitos reales.

## Invariantes de candidato

Durante DOC.1 R4:

```text
VERSION                  0.1.14.01-beta
accepted_count           114
next_global              115
next_candidate           0.1.15.04-beta
next_candidate_block     DOC.1
G115/E04                 reservado, no aceptado
```

DOC.1 R4 no crea ni mueve tags y no publica `0.1.15.04-beta`. La promoción de
G115 solo puede ocurrir después de gate completo, commit firmado, PR/CI,
integración y revalidación post-merge.
