# ADR-179 — El versionado beta usa un ledger de estados aceptados y no cuenta commits como revisiones

**Estado:** Aceptada; actualizada documentalmente por DEV.2 R4 sin promover versión ni tag.
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

La base `7037addd44253e528c77460b678d2b3ccd540dd5` queda auditada en **G057**. VER.2 R1 reserva **G058/E01**, es decir `0.0.58.01-beta`, y solo lo consume después del gate completo e integración.

Los identificadores revision-aware de G001–G057 son de auditoría. Los tags legacy `v0.0.1-beta`–`v0.0.26-beta` permanecen firmados e inmutables; no se crean tags revision-aware retrospectivos.

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
- `docs/AUDITORIA_VERSIONADO_PRE_1_0.md` conserva el razonamiento, inclusiones y exclusiones;
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
- `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`;
- `docs/governance/pre-1-0-revision-ledger.md`;
- `RELEASES.md`;
- `docs/REGISTRO_CAMBIOS_HISTORICO.md`;
- bitácoras y auditorías UX/GOV/PLAN conservadas;
- PR #35 de VER.2.
