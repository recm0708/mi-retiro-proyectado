# REL.GOV.1 R2 — automatización gobernada de Releases

**Estado:** cerrado/aceptado como G117/E02; materialización formal gobernada por promoción post-merge
**Versión materializada por promoción:** `0.1.17.02-beta` — G117/E02
**Integración de aceptación:** `46c464ed2dd21f621d80e8dafc199fe56b4af710` — PR #103
**Clasificación:** Auditoría / Gobierno / Release

## Objetivo

Reducir el trabajo manual posterior a un tag formal sin transferir a GitHub Actions la creación ni la firma del tag.

## Baseline

G116/E05 fue publicado con tag firmado `v0.1.16.05-beta`, objeto `4b5902bf7a3d2b94fcad8a426652d7ad8b77a32c`, workflow de firma #14 en `success` y GitHub Release prerelease ID `378095836`.

La publicación de G116 mostró dos costes operativos: preparación manual de notas/`gh release create` y frases vivas de “publicación pendiente” que quedaron obsoletas inmediatamente después del Release.

## Diseño R2

- `data/release-publication-manifest.json` contiene contenido auditable y versionado de la publicación vigente.
- `scripts/release_publication.py` valida el manifiesto, deriva SHA del commit/objeto tag, renderiza las seis secciones canónicas y valida un Release existente.
- `.github/workflows/verificar-tags.yml` conserva un job de verificación con `contents: read`.
- La publicación usa un job separado que depende de la verificación y recibe `contents: write`.
- Solo HTTP 404 se interpreta como Release ausente y autoriza creación; HTTP 200 exige validar coincidencia exacta, y cualquier otro estado o fallo de transporte bloquea la publicación.
- No se crean ni firman tags desde Actions.
- No se crean commits post-publicación para reconciliar texto efímero.

## Estado contable

REL.GOV.1 R2 superó gate completo, commit firmado, PR #103, integración y revalidación post-merge. G117/E02 queda aceptado; esta promoción materializa el mismo estado y no consume G118.

## Gate integral de desarrollo

El gate integral de desarrollo de REL.GOV.1 R2 se ejecutó sobre la rama
`governance/rel-gov1-r2-release-automation`, manteniendo `VERSION` en
`0.1.16.05-beta` y G117/E02 como candidato reservado, no aceptado.

Resultados:

- `unittest discover`: **1157 tests OK**;
- `pytest`: **1197 passed / 5731 subtests passed**;
- `pip check`: sin dependencias rotas;
- `compileall app/scripts/tests`: OK;
- sintaxis JavaScript: **18 archivos OK**;
- auditoría Markdown: **159/159 OK**;
- clasificación Markdown: **58 VIVO / 24 AUDITORIA / 64 HISTORICO / 9 PLANTILLA / 4 SOPORTE**;
- auditoría de identificadores: **16 familias / 46 identificadores OK**;
- `release_publication.py --check-manifest`: manifiesto G116/E05 válido;
- `release_contract.py --json`: contrato coherente con G116/E05 y candidato G117/E02;
- integración real con GitHub: el cuerpo renderizado desde el tag firmado
  `v0.1.16.05-beta` coincide exactamente con el GitHub Release publicado;
- verificación idempotente del Release G116 real: OK;
- `git diff --cached --check`: OK;
- **19 archivos staged** y ningún cambio fuera del índice.

Este gate demuestra aptitud técnica de la implementación para pasar a commit
firmado y Pull Request de desarrollo. No constituye aceptación de G117/E02:
esa contabilidad solo puede avanzar después de integración, revalidación y
promoción formal conforme al proceso vigente.

## Aceptación post-merge

REL.GOV.1 R2 quedó integrado en `main` mediante PR #103 / squash
`46c464ed2dd21f621d80e8dafc199fe56b4af710`.

Revalidación:

- `unittest`: **1157 tests OK**;
- `pytest`: **1197 passed / 5731 subtests passed**;
- Markdown: **159/159 OK**;
- JavaScript: **18 archivos OK**;
- identificadores: **16 familias / 46 identificadores OK**;
- CI #273, gobernanza #112, Markdown Audit #59 y CodeQL #209: `success`;
- integración real contra el Release G116 existente: idempotencia `OK`;
- working tree post-merge: limpio.

La promoción G117/E02 actualiza versión, ledger, manifiesto y documentación.
La publicación formal usa el tag firmado `v0.1.17.02-beta`, creado localmente
únicamente después de integrar y revalidar la promoción.

## Gate final de promoción

Validación final ejecutada el 2026-08-28 sobre la rama de promoción:

- `unittest`: **1161 tests OK**;
- `pytest`: **1201 passed / 5721 subtests passed**;
- sin fallos en ambas suites.

Estos conteos corresponden al gate final de la promoción y no sustituyen los
conteos históricos del gate de desarrollo ni de la revalidación post-merge.
