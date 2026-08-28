# ADR-179 — El versionado beta usa un ledger de estados aceptados y no cuenta commits como revisiones

**Estado:** Aceptada; reconciliada por AUD.SEC2 R1 y materializada hasta G109/E01 sin reescribir tags publicados.
**Fecha:** 2026-08-21
**Ámbito:** Gobierno / Versionado / Release / Trazabilidad

## Contexto

La familia histórica `0.0.N-beta` permitió identificar hitos formales, pero después de `v0.0.26-beta` varias fases completas continuaron sobre el mismo valor de `VERSION`. Un primer intento de reconciliación pretendió avanzar a `0.0.30-beta`; una auditoría posterior calculó 163 revisiones al usar en algunos tramos commits `feat/test/docs` y checkpoints todavía no aceptados como sustitutos de revisiones reales.

La segunda auditoría cruzada demostró que ambos criterios deformaban la historia:

- un mismo estado funcional podía estar materializado por varios commits lógicos;
- candidatos pendientes de validación no debían consumir numeración;
- un PR, squash, CI o tag podía ser evidencia del mismo estado y no una revisión adicional;
- UX.2.1 y las revisiones internas de UX.4.6a–d debían conservarse sin duplicar los 21 estados retrospectivos ya reconstruidos por GOV.1.1;
- UX.4.6i contenía referencias agregadas a R1.1 sin sección, gate ni artefacto independiente que la sustentara.

## Decisión

Durante la etapa beta se adopta un **contador global de estados aceptados** y un ordinal de estado aceptado dentro del bloque vigente.

La familia para estados nuevos es:

```text
0.GG.RR.EE-beta
```

Donde:

- `G = GG × 100 + RR` es el contador global;
- `RR` usa dos dígitos;
- `EE` usa dos dígitos y representa el ordinal aceptado dentro del bloque;
- un candidato fallido no consume `G`;
- los commits `feat/test/docs` de la misma revisión no consumen números adicionales;
- PR, squash, CI y tag son evidencia de aceptación, no revisiones por sí mismos.

La formulación inicial de esta ADR situó provisionalmente `7037addd44253e528c77460b678d2b3ccd540dd5` en **G057** y reservó G058/E01. La segunda pasada de VER.2 corrigió posteriormente esa base a **G070**; AUD.SEC2 R1 mantiene ambas evidencias, reconcilia los estados aceptados posteriores hasta **G108** y queda aceptado a su vez como **G109/E01** mediante PR #83.

Los identificadores revision-aware reconstruidos son de auditoría y no autorizan tags retroactivos. Los tags legacy `v0.0.1-beta`–`v0.0.26-beta` permanecen firmados e inmutables; no se crean tags revision-aware retrospectivos.

La primera versión oficial continúa siendo `1.0.0.0` con `Build 000001` después de los gates del plan maestro.

## Regla de metadata documental

Se separan dos conceptos:

1. **versión vigente de la aplicación**, cuya fuente canónica es `VERSION`;
2. **versión en la que un documento de dominio fue revisado**, que puede conservarse como metadata histórica de ese documento.

Por tanto, un incremento de `VERSION` no obliga a modificar todos los `.md`; obliga a revisar y actualizar únicamente los documentos que dependen materialmente del cambio y las superficies que declaran estado vigente.

## Consecuencias

- `VERSIONING.md` acepta la familia legacy, la revision-aware y la futura versión oficial;
- `app/core/version.py` construye y descompone la familia revision-aware;
- `docs/governance/pre-1-0-revision-ledger.md` se convierte en registro canónico del contador global pre-1.0;
- `docs/archive/governance/pre-1-0-versioning-audit.md` conserva el razonamiento, inclusiones y exclusiones;
- los tags históricos no se reescriben;
- el contador global no puede derivarse solo del número de commits;
- DEV.2 puede cerrarse como bloque funcional independiente antes del cierre final de VER.2, siempre que no promueva versión revision-aware, no cree tag y documente la separación entre avance funcional y cierre contable;
- una futura discrepancia entre ledger, `VERSION` y documentación vigente debe fallar mediante regresiones automáticas.

## Alternativas descartadas

### Continuar `0.0.N-beta`

Descartada porque vuelve a ocultar las revisiones aceptadas entre hitos y no resuelve la trazabilidad posterior a `v0.0.26-beta`.

### Usar cada commit como revisión

Descartada porque un mismo estado aceptado se materializa frecuentemente mediante commits separados de implementación, pruebas y documentación.

### Contar toda etiqueta R mencionada

Descartada porque algunas R fueron candidatos pendientes, intentos fallidos o refinamientos integrados dentro de un único cierre aceptado.

### Retaggear toda la historia

Descartada porque falsearía la publicación histórica y rompería la política de inmutabilidad de tags.

## Evidencia relacionada

- `VERSIONING.md`;
- `docs/archive/governance/pre-1-0-versioning-audit.md`;
- `docs/governance/pre-1-0-revision-ledger.md`;
- `RELEASES.md`;
- `docs/archive/governance/historical-change-registry.md`;
- bitácoras y auditorías UX/GOV/PLAN conservadas;
- PR #35 de VER.2.

## Reconciliación 2026-08-25 — AUD.SEC2 R1

La promoción `v0.0.71.01-beta` se realizó sobre un ledger cuya base canónica
terminaba en G070 y que no había incorporado estados aceptados de DEV.2,
MANT.1 y DOC.1 ya existentes antes de VER.2. La reconstrucción completa,
extendida después a NOR.1, NOR.2, DOC.1 R2 y SEC.2, fija el árbol `4bd7d8d` en
**G108**.

El estado promovido históricamente como `0.0.71.01-beta` corresponde por orden
cronológico a **G087**. El tag publicado permanece inmutable: no se mueve, no se
borra y no se sustituye. La corrección se aplica al ledger y a la numeración
futura. G109/E01 (`0.1.09.01-beta`) quedó aceptado para AUD.SEC2 R1 mediante PR #83 y merge `ec1842d`; la sincronización post-merge materializa ese mismo estado en `VERSION` y no consume G110.

Evidencia: `docs/audits/governance/post-g070-revision-reconciliation.md` y el
snapshot G070 preservado en
`docs/archive/governance/pre-1-0-revision-ledger-g070.json`.
