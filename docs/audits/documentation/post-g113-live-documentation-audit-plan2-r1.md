# Auditoría semántica de documentación viva post-G113 — PLAN.2 R1

**Estado:** candidato / evidencia de auditoría
**Versión base:** `0.1.13.03-beta` — G113/E03
**Snapshot base:** `277505af9263ceb738ef6d671fadf5f3334f38b6`
**Fecha:** 2026-08-26

## 1. Alcance

- Markdown rastreados en la base G113: **146**.
- Se recorre individualmente todo Markdown rastreado.
- `docs/archive/`, auditorías y plantillas se preservan como historia/contexto.
- Los bloqueadores semánticos automáticos se buscan solo en documentación VIVO/SOPORTE.
- PLAN.2 R1 agrega dos Markdown: esta auditoría y la matriz maestra.

### Clasificación de la base

- **VIVO:** 57
- **AUDITORIA:** 20
- **HISTORICO:** 64
- **PLANTILLA:** 1
- **SOPORTE:** 4

## 2. Criterios revisados

- último tag/release revision-aware vigente;
- publicación efectiva de G113/E03;
- reserva G114/E01 y bloque candidato;
- estados obsoletos de SEC.2;
- familia beta vigente frente a familia legacy;
- metadata transversal del plan maestro;
- preservación de anclas históricas.

## 3. Hallazgos automáticos remanentes

- **0 hallazgos bloqueantes automáticos** para las reglas semánticas post-G113 definidas por PLAN.2 R1.

## 4. Anclas contextuales preservadas

`next_candidate_block = PERSIST.1` puede aparecer en validaciones históricas de estados anteriores. No se sustituye mecánicamente.

- `docs/operations/validation.md:1105` — - ledger: `accepted_count=111`, `next_global=112`, `next_candidate=0.1.12.01-beta` y `next_candidate_block = PERSIST.1`;
- `docs/operations/validation.md:1126` — - la sección histórica de DOC.2 conserva `next_candidate_block = PERSIST.1` y `0.1.12.01-beta` porque ese era el estado al cerrar G111.
- `docs/operations/validation.md:1136` — - `next_candidate_block = PERSIST.1`;

## 5. Decisión

La documentación histórica no se moderniza en masa. PLAN.2 R1 corrige únicamente superficies vigentes que describen versión publicada, candidato actual, pendientes o limitaciones presentes.

Todo hallazgo remanente debe revisarse antes de staging/commit.
