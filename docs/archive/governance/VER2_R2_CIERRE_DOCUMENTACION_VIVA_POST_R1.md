# VER.2 R2 — Cierre de documentación viva post-R1

- **Fecha local de generación:** 2026-08-23T22:18:13
- Rama: `ver/ver2-r2-documentacion-viva-post-r1`
- HEAD base: `b34d0bf`
- Base: `b34d0bf VER.2 R1 — auditoría de reconciliación post-DOC.1 (#57)`

## 1. Objetivo

Cerrar la revisión de documentación viva priorizada por VER.2 R1, separando referencias legacy, candidato VER.2 y estados revision-aware reconstruidos.

## 2. Decisiones aplicadas

- `docs/ARQUITECTURA.md`: se aclara que `0.0.26-beta` es versión visible/canónica legacy y no candidato VER.2.
- `README.md`: se preserva la explicación histórica de G070/E02 porque no crea tags retroactivos ni publica versión nueva.
- `RELEASES.md`: se aclara que el candidato `0.0.71.01-beta` no está publicado, no sustituye `VERSION = 0.0.26-beta` y no crea tag formal.

## 3. Estado canónico preservado

- `VERSION` permanece en `0.0.26-beta`.
- `v0.0.26-beta` permanece como último tag formal.
- `0.0.71.01-beta` permanece como candidato VER.2 G071/E01 no publicado.
- G001–G070 permanecen como estados aceptados reconstruidos, sin tags retroactivos.

## 4. Restricciones respetadas

- No se modifica `VERSION`.
- No se modifica `app/core/version.py`.
- No se modifica `app/core/config.py`.
- No se modifica `regulations/`, `data/` ni `_entregas/`.
- No se crean tags.
- No se publica `0.0.71.01-beta`.

## 5. Salida recomendada

VER.2 R2 deja la documentación viva lista para una siguiente fase de validación/cierre, manteniendo separado el estado legacy visible del candidato revision-aware.
