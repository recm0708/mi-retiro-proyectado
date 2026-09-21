# VER.2 R6 — Decisión del modelo revision-aware

**Issue propietaria:** #164
**Base inicial:** CP1 `69cc6b4ce2e59e7da7aba1c4dc764923cc8cca81`
**Enmienda vigente:** CP5.1 posterior a `8e8461c69c8e819d0b8ab7b953fb428adb6aabd6`
**Fecha inicial:** 2026-09-20
**Fecha de enmienda:** 2026-09-21
**Estado:** decisión arquitectónica vigente para implementación

## 1. Propósito

VER.2 R6 elimina ambigüedades entre versión visible, Global, Edition,
revisión funcional, correcciones materiales, mantenimiento, candidatos y
publicación.

CP2 definió inicialmente una familia prospectiva larga con `CCC` y `DDD`
codificados en el string. CP5.1 la sustituye antes de que llegue a publicarse
ningún identificador v2.

No se renombra ni reescribe ningún tag, Release o versión histórica.

## 2. Familias admitidas

La política reconoce cuatro familias:

1. legacy histórica: `0.0.N-beta`;
2. revision-aware v1 histórica: `0.<G_HI>.<G_LO>.<EE>-beta`;
3. revision-aware v2 prospectiva simplificada:
   `0.<GLOBAL>.<EDITION>.<CORRECTION>-beta`;
4. estable: `MAJOR.MINOR.PATCH.REVISION`.

La familia v2 comienza prospectivamente en G128. El primer ejemplo
aritméticamente posible, sin que constituya reserva, sería `0.128.2.0-beta`
si G128 fuese aceptado con Edition 2 y Correction 0.

## 3. Global

`GLOBAL` es el contador monotónico de estados materialmente distintos y
aceptados.

- checkpoint, commit, PR, squash, tag o intento fallido no consume Global;
- una fase planificada no reserva Global;
- el siguiente Global solo se asigna cuando existe un candidato material
  aceptable;
- G128 permanece libre mientras VER.2 R6 no llegue a ese punto.

En v1, el Global se codificaba como `G_HI` + `G_LO`. En v2 se escribe
directamente como entero decimal.

## 4. Revisión funcional y Edition

La revisión funcional (`R6`, `R1.1`, `R3B2`, etc.) permanece como metadata
semántica del bloque.

`EDITION` representa el ordinal de estados aceptados dentro del bloque.
Revisión funcional y Edition pueden divergir. La versión visible no intenta
duplicar la revisión funcional.

## 5. Correction

`CORRECTION` es el cuarto componente beta v2.

- `0`: estado ordinario de la línea aceptada;
- `1..999`: corrección material posterior de esa línea;
- una corrección previa a la aceptación del candidato no incrementa este
  componente;
- un intento fallido no lo incrementa;
- una corrección material aceptada consume además un nuevo Global;
- una nueva línea funcional reinicia Correction a `0`.

Los componentes v2 se escriben sin padding artificial.

Ejemplos sintéticos: `0.128.2.0-beta` y `0.129.2.1-beta`.

## 6. Mantenimiento de dependencias

El ordinal del ciclo MANT.2 permanece en ledger/registry como
`maintenance_ordinal`. No forma parte de `VERSION`.

MANT.2 R1/G123 y MANT.2 R2/G127 conservan íntegramente sus versiones v1,
tags y Releases históricos.

## 7. Intentos, checkpoints y subrevisiones

Un intento fallido o revertido:

- no consume Global;
- no incrementa Edition;
- no incrementa Correction;
- no incrementa `maintenance_ordinal`;
- permanece trazable mediante Git, PR, Issue o auditoría.

Un checkpoint firmado tampoco consume contadores por sí solo.

## 8. Fases insertadas dinámicamente

Una fase intermedia creada por #166 u otro control de gobierno se inserta
primero en el árbol, Issues y documentación pertinente. No recibe Global ni
VERSION hasta existir un candidato material aceptable.

## 9. Planos de estado

Se mantienen separados:

1. snapshot candidato/versionado;
2. estado operativo de rama/PR/merge;
3. estado publicado real: commit de `main`, tag firmado y GitHub Release.

El manifest es un `release-input` estable. Los hechos externos de publicación
se resuelven en runtime y no obligan a reescribir Releases históricos.

## 10. Ledger v2

El ledger conserva schema/formato, Global, bloque, Edition, revisión
funcional, `correction_ordinal`, `maintenance_ordinal`, evidencia, candidato
o `null` y `next_global`.

El estado vivo de workflow pertenece al registry, no al ledger.

## 11. Compatibilidad de parsers

Los parsers deben aceptar:

- legacy `0.0.N-beta`;
- revision-aware v1 histórica `0.<G_HI>.<G_LO>.<EE>-beta`;
- revision-aware v2 desde G128 `0.<GLOBAL>.<EDITION>.<CORRECTION>-beta`;
- estable de cuatro componentes.

La forma larga evaluada por CP2,
`0.<G_HI>.<G_LO>.<EE>.<CCC>.<DDD>-beta`, queda **supersedida antes de
publicación** y no constituye una familia válida prospectiva.

## 12. Transición estable

La primera versión oficial continúa prevista como `1.0.0.0`.

Semántica estable:

- `MAJOR`: generación incompatible o nueva generación del producto;
- `MINOR`: capacidades compatibles relevantes;
- `PATCH`: correcciones/mejoras compatibles;
- `REVISION`: hotfix o revisión puntual de ese patch.

No se presenta como SemVer estricto.

## 13. Build

Build es independiente de `VERSION`.

Formato de presentación previsto para artefactos oficiales: `Build 000001`.
No se incrementa por cada commit y no sustituye un cambio real de versión.

## 14. Compatibilidad histórica

Las versiones ya publicadas permanecen inmutables. En particular, G127/E02
continúa siendo `0.1.27.02-beta` con su tag y Release originales.

La adopción v2 solo afecta estados aceptados después de esta reforma.

## 15. Decisión sobre VER.2 R6

Este documento no reserva G128 ni fija todavía un candidato.

Si la auditoría final de VER.2 R6 determina que el siguiente estado aceptable
es G128/E02 sin corrección, entonces el candidato sería `0.128.2.0-beta`.

La asignación ocurrirá únicamente en el checkpoint de promoción correspondiente.
