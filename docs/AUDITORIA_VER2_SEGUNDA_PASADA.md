# VER.2 — Segunda pasada de auditoría cruzada

**Proyecto:** Mi Retiro Proyectado  
**Base auditada:** `main` en `7037addd44253e528c77460b678d2b3ccd540dd5`  
**Rama de trabajo:** `chore/ver2-revision-ledger`  
**Estado:** EN CURSO — prevalece sobre cualquier afirmación anterior de que G057/G058 ya estén ratificados.

## 1. Motivo de reapertura

La primera pasada de VER.2 reconstruyó un ledger G001–G057 y reservó G058 para el cierre de VER.2. La segunda revisión detectó que esa cifra todavía mezcla criterios contables distintos: en algunos bloques se cuentan revisiones internas aceptadas, en otros se cuenta únicamente el cierre del bloque y en al menos un caso se cuenta además un cierre documental/hardening posterior a un cierre funcional ya aceptado.

Por tanto:

- G057 es **provisional**;
- `0.0.58.01-beta` es **provisional**;
- no debe promocionarse `VERSION` ni crearse un tag revision-aware hasta cerrar esta auditoría;
- los tags históricos `v0.0.1-beta`–`v0.0.26-beta` permanecen inmutables.

## 2. Fuentes cruzadas

La segunda pasada utiliza, por orden de autoridad práctica:

1. historial Git y rangos documentados en `RELEASES.md`;
2. bitácoras preservadas en `docs/historico/ux/`;
3. `CHANGELOG.md`, `docs/REGISTRO_CAMBIOS_HISTORICO.md` y `docs/ROADMAP.md`;
4. Pull Requests integrados y sus gates;
5. pruebas y cifras de cierre registradas;
6. conversaciones de desarrollo recuperadas, en especial las continuaciones del proyecto donde se aceptaron visual y funcionalmente revisiones antes de su consolidación documental.

Un commit `feat/test/docs`, un PR, un squash o un tag no constituyen por sí mismos una revisión adicional.

## 3. Tramo anterior a UX.4.6d

La segunda pasada confirma que UX.4.6d no es el comienzo del tramo UX.4.6.

| Fase | Evidencia Git/documental | Cierre demostrado | Estado contable |
|---|---|---|---|
| UX.2.1 | aparece en changelog/documentación histórica como estabilización visual transversal: Oscuro más profundo, Alto contraste negro/blanco, tokens semánticos y remates visuales | fase histórica real; todavía debe determinarse si posee ancla independiente suficiente para consumir Global | PENDIENTE DE DECISIÓN |
| UX.4.6a | `429201a` → `11aefca`; bitácora `UX_4_6A_REDISENO_VISUAL.md` | PC/laptop aceptado; 198 pruebas; `compileall`, JS y `git diff --check` en verde | CIERRE REAL CONFIRMADO |
| UX.4.6b | `e6c2310` → `83a67ed`; bitácora `UX_4_6B_PASO1_DATOS_PERSONALES.md` | R4; PC/laptop aceptado; 233 pruebas; CI Python 3.13/3.14 en verde | CIERRE REAL CONFIRMADO |
| UX.4.6c | `e80d15e` → `2a69fb8`; bitácora `UX_4_6C_PASO2_CUOTAS.md` | R3; PC/laptop aceptado; 253 pruebas | CIERRE REAL CONFIRMADO |
| UX.4.6d | `05232df` → `7941f58`; bitácora `UX_4_6D_PASO3_HISTORIAL.md` | R23; 396 pruebas; Pasos 1–3 integrados y acceso correcto a Paso 4 | CIERRE REAL CONFIRMADO |

La reconstrucción histórica GOV.1.1 ya asignó `0.0.18-beta`, `0.0.19-beta`, `0.0.20-beta` y `0.0.21-beta` a los cuatro cierres UX.4.6a–d. La auditoría debe evitar contarlos dos veces, pero también debe conservar explícitamente sus nombres, revisiones finales y gates.

## 4. UX.4.6d — interpretación de R1–R23

La bitácora histórica conserva numerosos estados técnicos intermedios. Varias revisiones indican expresamente que la validación visual/funcional completa seguía pendiente. El cierre inequívoco se produce en R23, con 396 pruebas y validación integral.

Consecuencia provisional: R1–R22 deben preservarse como trazabilidad histórica, pero **no se deben convertir automáticamente en Globals**. Solo una evidencia independiente de aceptación material de una revisión intermedia podría cambiar esa decisión.

## 5. Inconsistencia detectada después de `0.0.26-beta`

### UX.4.6f

PR #30 registra que UX.4.6f R2 fue validada funcionalmente, integrada con **756/756 pruebas** y que UX.4.6f quedó cerrada, pasando el bloque funcional activo a UX.4.6g.

PR #31, posterior, se titula como cierre formal de UX.4.6f, pero su alcance principal es:

- cierre documental;
- activación formal de UX.4.6g;
- incorporación del gate local `pre-commit`;
- corrección de regresiones históricas que congelaban estados transitorios;
- 762 pruebas.

La primera pasada creó un Global adicional para PR #31. Esta decisión queda **reabierta**. Bajo un criterio centrado en revisiones de bloque explícitas, PR #31 parece evidencia/hardening posterior del mismo cierre R2 y no una nueva revisión UX.4.6f. Solo se mantendrá como Global independiente si la regla definitiva decide contar hitos técnicos transversales autónomos aun cuando no tengan R nueva.

## 6. Criterio que debe quedar uniforme

La segunda pasada no aceptará reglas diferentes según el bloque. La decisión final deberá responder igual para UX, GOV, PLAN y mantenimiento.

Una entrada candidata a Global deberá demostrar como mínimo:

1. identidad de revisión/hito distinguible de su estado anterior;
2. cambio material aceptado, no solo separación de commits por categoría;
3. gate satisfactorio o aceptación manual explícita cuando corresponda;
4. evidencia de que el proyecto avanzó desde ese estado;
5. ausencia de duplicación con PR/squash/tag/cierre documental que materialice el mismo estado.

Los candidatos fallidos, checkpoints explícitamente intermedios y cierres puramente documentales no consumen Global por defecto.

## 7. Bloques pendientes de reauditoría antes de fijar el número

Antes de ratificar el último Global deben revisarse de nuevo, con el mismo criterio:

- UX.2.1;
- GOV.1.3 R1–R4 y la consistencia con el tratamiento de GOV.1.5 R1/R2;
- prebloque de firma/integridad;
- UX.4.6e R1–R9.2;
- PLAN.1 R1–R4.2 y sus subdivisiones R2A/R2B1/R2B2/R2C/R3A/R3B1/R3B2;
- UX.4.6f R1/R1.1/R2 y PR #31;
- UX.4.6g refinamientos posteriores a R1;
- UX.4.6h R1 fallido, R1.1, R1.2 y R1.3;
- UX.4.6i R1/R1.2/R1.3/R1.4 y la referencia inconsistente a R1.1.

## 8. Estado operativo

Este archivo es una bitácora de auditoría de trabajo. Cuando termine la segunda pasada:

- `AUDITORIA_VERSIONADO_PRE_1_0.md` se reescribirá con el resultado definitivo;
- `LEDGER_REVISIONES_PRE_1_0.md` se regenerará con una única regla contable;
- se materializará el ledger estructurado en `data/` y su validador;
- se corregirán las regresiones históricas que congelan versiones vigentes;
- se eliminarán referencias a candidatos descartados;
- recién entonces se fijará el siguiente identificador revision-aware.
