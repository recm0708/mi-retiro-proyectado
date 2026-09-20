# VER.2 R6 — Auditoría de entrada

**Issue propietaria:** #164
**Políticas transversales:** #166 y #203
**Fecha:** 2026-09-20
**Rama:** `ver/ver2-r6-revision-aware`

## 1. Baseline publicado verificado

La revisión comienza exclusivamente después del cierre y publicación de
MANT.2 R2 como G127/E02.

- `main`: `2df33a5c24d1c7cea1a6db91539a92da02c91500`;
- `VERSION`: `0.1.27.02-beta`;
- tag firmado/verificado: `v0.1.27.02-beta`;
- objeto del tag: `7bb7720b820d68e54e559b6b4e8ecd826537631f`;
- commit publicado: `2df33a5c24d1c7cea1a6db91539a92da02c91500`;
- GitHub Release prerelease: `392412590`;
- PR #207: integrado por squash y cerrado;
- Issue #206: cerrada/publicada.

La auditoría remota de entrada confirmó además cero Pull Requests abiertos
y, antes de crear la rama de VER.2, únicamente `main` como rama remota.

## 2. Preflight #166

La ejecución fresca posterior a la publicación de G127/E02 quedó registrada
como `CLEAN`.

Su evidencia incluye:

- 0 Pull Requests abiertos;
- 0 Pull Requests Dependabot abiertos;
- 0 ramas `dependabot/*`;
- 0 Dependabot alerts abiertos mediante API autenticada;
- `pip check`: PASS;
- `pip-audit --strict`: sin vulnerabilidades conocidas;
- `main == origin/main`;
- working tree limpio;
- ramas locales/remotas saneadas;
- ausencia de trabajo material nuevo que obligue a insertar MANT.2 R3.

Por tanto, VER.2 R6 queda habilitada.

## 3. Estado revision-aware de entrada

El ledger estructurado registra:

- `accepted_count = 127`;
- `next_global = 128`;
- `next_candidate = null`;
- `next_candidate_block = null`.

G128 es únicamente el siguiente Global aritméticamente disponible. No existe
candidato, bloque, edición ni `VERSION` preasignados.

## 4. Hallazgo heredado: candidato frente a publicación

La realidad remota demuestra que G127/E02 ya está publicado, pero distintas
superficies versionadas conservan todavía semántica congelada del momento
candidato.

Entre las superficies observadas se encuentran:

- `data/governance/work-block-registry.json`;
- `data/governance/release-publication-manifest.json`;
- `VERSIONING.md`;
- `GOVERNANCE.md`;
- `docs/governance/roadmap.md`;
- `docs/governance/master-plan-to-1-0.md`;
- `docs/governance/pre-1-0-pending-matrix.md`;
- `docs/operations/release-process.md`.

Ejemplos del drift son estados como `accepted_pending_publication` y textos
que todavía describen G127/E02 como pendiente de integración o publicación.

Este hallazgo no constituye trabajo nuevo de dependencias. Pertenece
directamente al alcance de #164, que exige distinguir de forma determinística
el estado candidato congelado del estado posteriormente publicado sin
reescribir la historia ni alterar Releases históricas.

## 5. Superficies técnicas iniciales

La revisión deberá evaluar, como mínimo:

- `app/core/version.py`;
- `app/core/version_ledger.py`;
- `scripts/release_contract.py`;
- `scripts/release_readiness.py`;
- `scripts/release_publication.py`;
- ledger Markdown y JSON;
- work-block registry;
- release-publication manifest;
- `VERSIONING.md` y `GOVERNANCE.md`;
- roadmap, master plan y pending matrix;
- release process;
- regresiones y guards de gobierno/versionado.

El formato vigente de entrada continúa siendo `0.GG.RR.EE-beta`. Esta
auditoría no presupone cuál será el modelo final de VER.2 R6.

## 6. Fronteras del checkpoint

Este primer checkpoint:

- no modifica `VERSION`;
- no materializa ni reserva G128;
- no cambia ledger, registry ni manifest;
- no inicia DOC.4/#171–#174;
- no inicia #142;
- no inicia PERSIST.1/#130;
- no inicia ninguna UX;
- documenta únicamente el baseline y el hallazgo que guiarán los siguientes
  checkpoints de VER.2 R6.

La rama y el Draft PR constituyen superficies de trabajo conforme a #203;
los commits intermedios no equivalen a estados revision-aware aceptados.
