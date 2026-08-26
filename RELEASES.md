# Registro de versiones y estados del proyecto

**Fecha de reconstrucción histórica:** 2026-08-17
**Fuente:** historial Git de `recm0708/mi-retiro-proyectado`
**Revisión de planificación hacia 1.0:** 2026-08-20
**Reconciliación revision-aware:** 2026-08-22


<!-- DOC1-R1-POST-MANT1:START -->
## Promoción G113/E03 — post-merge de DOC.1 R3

- Estado aceptado: G113/E03 (`0.1.13.03-beta`).
- Evidencia de aceptación: PR #92 / merge `40ae5c0`, 1092 pruebas post-merge, Markdown 146/146, auditor de identificadores en `OK` y checks remotos requeridos en `success`.
- Esta sincronización materializa G113 ya aceptado y **no consume G114**.
- Tras publicar G113/E03, la reserva no consumida G114/E01 (`0.1.14.01-beta`) se reasigna a PLAN.2 R1 para formalizar la replanificación; PERSIST.1 permanece en la matriz posterior.
- Promoción final: PR #93 / merge `277505a`; tag firmado `v0.1.13.03-beta`, verificación criptográfica y GitHub Release prerelease publicados y preservados.

## Promoción G112/E07 — post-merge de NOR.1 R8

- Estado aceptado: G112/E07 (`0.1.12.07-beta`).
- Evidencia de aceptación: PR #89 / merge `cc6695b`, corrección ordinal PR #90 / merge `2de10b5`, 1081 pruebas post-merge, Markdown 145/145 y checks remotos en `success`.
- Esta sincronización materializa G112 ya aceptado y **no consume G113**.
- G113/E03 (`0.1.13.03-beta`) fue reservado para DOC.1 R3 y quedó aceptado posteriormente mediante PR #92.
- Promoción final: PR #91 / merge `02c3763`; tag firmado `v0.1.12.07-beta` y GitHub Release prerelease publicados y preservados.

## Promoción G111/E01 — post-merge de DOC.2 R1

- Estado aceptado: G111/E01 (`0.1.11.01-beta`).
- Evidencia de aceptación: PR #87, merge `1041b59`, 1066 pruebas post-merge, Markdown 143/143 y checks remotos Python 3.13/3.14 + Markdown/gobernanza en `success`.
- Esta sincronización materializa el G111 ya aceptado y **no consume G112**.
- G112/E07 (`0.1.12.07-beta`) fue reservado para NOR.1 R8 y quedó aceptado posteriormente.
- Promoción final: PR #88, merge `7e81034`, revalidación post-merge de 1070 pruebas en `OK`; tag firmado `v0.1.11.01-beta` y GitHub Release prerelease publicados.

## Promoción G110/E01 — post-merge de REL.GOV.1 R1

- Estado aceptado: G110/E01 (`0.1.10.01-beta`).
- Evidencia de aceptación: PR #85, merge `5cd1cea`, 1054 pruebas locales y checks remotos Python 3.13/3.14 + Markdown/gobernanza en `success`.
- Esta sincronización materializa el G110 ya aceptado y **no consume G111**.
- Siguiente Global disponible entonces: G111/E01 (`0.1.11.01-beta`) para DOC.2.
- Promoción final: PR #86, merge `cef373a`, revalidación post-merge de 1058 pruebas en `OK`; tag firmado `v0.1.10.01-beta` y GitHub Release prerelease publicados.

## Promoción G109/E01 — post-merge de AUD.SEC2 R1

- Estado aceptado: G109/E01 (`0.1.09.01-beta`).
- Evidencia de aceptación de AUD.SEC2 R1: PR #83, merge `ec1842d`, 1040 pruebas locales y checks remotos requeridos en `success`.
- Evidencia de promoción: PR #84, merge `6de6f32`, 1044 pruebas locales, CI Python 3.13/3.14 y auditorías Markdown/gobernanza en `success`.
- Esta sincronización materializó el G109 ya aceptado y **no consumió G110**.
- G110/E01 (`0.1.10.01-beta`) fue reservado para REL.GOV.1 y quedó aceptado posteriormente.
- Tag y GitHub Release formal `v0.1.09.01-beta`: publicados y preservados; no se mueve `v0.0.71.01-beta`.

## Estado post-MANT.1

Después de `v0.0.26-beta`, el repositorio integró trabajo funcional, técnico, documental y de gobierno hasta completar VER.2, NOR.2 y los checkpoints transversales previos a PERSIST.1.

Estado vigente:

- Último tag formal publicado: `v0.1.13.03-beta` (G113/E03), firmado, verificado y asociado a GitHub Release prerelease.
- Último tag formal legacy: `v0.0.26-beta`.
- Versión canónica en `VERSION`: `0.1.13.03-beta` (G113/E03).
- `v0.0.71.01-beta` conserva su denominación histórica original y se reconcilia como G087/E01 sin alterar el tag.
- MANT.1, NOR.1 R8, NOR.2 y DOC.1 R1–R3 están cerrados.
- DOC.2 permanece aceptado/publicado como G111/E01; NOR.1 R8 como G112/E07 y DOC.1 R3 como G113/E03.
- G114/E01 queda reservado para PLAN.2 R1; PERSIST.1 y REP.1 permanecen planificados posteriormente según la matriz maestra viva.
- SEC.2 quedó cerrado después de R1–R6 y AUD.SEC2 R1 permanece aceptado como G109/E01.

Este documento no crea una release nueva; registra el estado formal ya alcanzado por el repositorio.
<!-- DOC1-R1-POST-MANT1:END -->

## 1. Naturaleza del registro

Las versiones `0.0.1-beta` a `0.0.21-beta` fueron asignadas retrospectivamente en GOV.1.1 para organizar estados funcionales que ya existían en Git. No fueron tags ni GitHub Releases publicados en sus fechas originales. La migración criptográfica del 2026-08-17 permitió materializarlas posteriormente como tags firmados, conservando explícitamente esa naturaleza retrospectiva.

Git conserva la evidencia primaria: hashes, fechas, autores, mensajes y contenido. Este documento añade una clasificación legible sin reescribir esa evidencia.

El commit raíz real es `a0a9e09` (`tipo: descripción del cambio`). Su mensaje es una anomalía histórica previa a la convención posterior y se conserva sin modificar.

VER.2 añade una segunda capa de auditoría: `docs/governance/pre-1-0-revision-ledger.md` y `data/pre-1-0-revision-ledger.json` reconstruyen los **estados aceptados** como G001–G070 sobre la base `7037addd44253e528c77460b678d2b3ccd540dd5`. Esos identificadores revision-aware no sustituyen versiones/tags históricos ni autorizan tags retroactivos. `0.0.71.01-beta` fue publicada originalmente como VER.2 G071/E01. La reconciliación posterior determinó que su estado corresponde cronológicamente a G087/E01; el tag y su commit objetivo permanecen inmutables.

## 2. Estados retrospectivos

| Versión | Fecha de cierre | Rango Git | Commits | Hito |
|---|---|---|---:|---|
| `0.0.1-beta` | 2026-08-10 | `a0a9e09` → `13ce028` | 6 | Base técnica, FastAPI, primera interfaz, asistente, cuotas, salario y documentación inicial. |
| `0.0.2-beta` | 2026-08-11 | `ae45943` → `eafe54d` | 3 | Historial salarial, proyección y línea temporal. |
| `0.0.3-beta` | 2026-08-11 | `a7e1ed4` → `78e5188` | 4 | Retiro, precisión monetaria, pruebas y protección de datos de validación. |
| `0.0.4-beta` | 2026-08-11 | `563d6c4` → `2d4dfd0` | 7 | Motor SEBD, modalidades e Indemnización por Vejez. |
| `0.0.5-beta` | 2026-08-11 | `d41682c` → `8a7e381` | 3 | Motores Mixto y SUCGS. |
| `0.0.6-beta` | 2026-08-11 | `fa5348f` → `e087d6e` | 4 | Organización del repositorio, centralización normativa y casos de validación. |
| `0.0.7-beta` | 2026-08-12 | `c442ec2` → `e956ea9` | 4 | Comparador, trazabilidad, resultado unificado y cierre funcional de Fase 6. |
| `0.0.8-beta` | 2026-08-12 | `6d4c2d8` → `d599ee2` | 3 | UX.3: responsive y precisión del corte mensual de cuotas. |
| `0.0.9-beta` | 2026-08-12 | `376a967` → `e6b02dc` | 4 | Identidad, temas, accesibilidad y terminología pública. |
| `0.0.10-beta` | 2026-08-12 | `3f2f5d7` → `8feb682` | 6 | Mantenimiento técnico: LF, favicon temporal, estructura y respaldos. |
| `0.0.11-beta` | 2026-08-12 | `c2da494` → `1f350f6` | 3 | UX.4.1: accesibilidad y ayudas contextuales. |
| `0.0.12-beta` | 2026-08-12 | `5607cc1` → `6e6b33b` | 3 | UX.4.2: estados activos y selección perceptible. |
| `0.0.13-beta` | 2026-08-12 | `b671c9a` → `9f849d0` | 2 | UX.4.3: validación accesible, teclado, errores y estabilidad. |
| `0.0.14-beta` | 2026-08-13 | `5ca39ac` → `f4a0d45` | 6 | UX.4.4: edad anual, detalle salarial e importación documental. |
| `0.0.15-beta` | 2026-08-13 | `88a1d14` → `3430f2e` | 3 | UX.4.5: información acreditada frente a proyectada y cierre accesible. |
| `0.0.16-beta` | 2026-08-13 | `338db37` → `6f138da` | 4 | Hardening PDF, privacidad, regresión E2E, CI y Dependabot. |
| `0.0.17-beta` | 2026-08-13 | `488aff5` → `e55190b` | 3 | Estrategia reproducible de dependencias pre-beta. |
| `0.0.18-beta` | 2026-08-13 | `429201a` → `11aefca` | 3 | UX.4.6a: rediseño visual integral. |
| `0.0.19-beta` | 2026-08-13 | `e6c2310` → `83a67ed` | 3 | UX.4.6b: Paso 1, datos personales, privacidad e importación. |
| `0.0.20-beta` | 2026-08-13 | `e80d15e` → `2a69fb8` | 3 | UX.4.6c: Paso 2, cuotas e importación contextual. |
| `0.0.21-beta` | 2026-08-17 | `05232df` → `7941f58` | 3 | UX.4.6d: Paso 3, Ficha Digital, sincronización de Pasos 1–3 y cierre integral. |

**Total reconstruido:** 80 commits en 21 estados documentales.

### Backfill administrativo de GitHub Releases — 2026-08-26

- se conservaron exactamente los **29 tags formales reales** del repositorio;
- se completaron GitHub Releases para los 26 tags legacy `v0.0.1-beta`–`v0.0.26-beta`;
- junto con `v0.0.71.01-beta`, `v0.1.09.01-beta` y `v0.1.10.01-beta`, el inventario queda en **29 tags ↔ 29 Releases**;
- los Releases retrospectivos son metadata administrativa: no mueven, borran ni recrean tags y no falsean sus fechas históricas;
- no se creó `v0.0.0-beta` ni `v0.0.00.00-beta` porque esos tags no existen;
- esta regularización no consume un Global revision-aware.

## 3. Marcador histórico `0.1.0`

El repositorio nació con `0.1.0` escrito en la configuración, README y CHANGELOG. No existió un tag ni una GitHub Release que materializara ese número. GOV.1 lo clasifica como **marcador de desarrollo no publicado**.

No se elimina esta evidencia de la historia Git. El estado actual se corrige hacia una política explícita sin alterar commits antiguos.

## 4. Versiones formales legacy desde GOV.1.2

### `0.0.22-beta` — 2026-08-17

Primera versión adoptada conscientemente bajo `VERSIONING.md`.

Alcance del hito:

- política formal de gobierno;
- política formal de versionado;
- archivo canónico `VERSION`;
- carga centralizada de versión en Python;
- CODEOWNERS;
- registro histórico de releases/estados;
- regresiones para impedir divergencias entre archivo canónico, FastAPI y footer;
- validación final con compilación Python, JavaScript válido, `git diff --check` limpio y **403 pruebas automatizadas en OK**.

El tag formal asociado es `v0.0.22-beta`.

### `0.0.23-beta` — 2026-08-17

Segunda versión formal y cierre de GOV.1.3.

Alcance del hito:

- R1: reorganización de documentos de entrada y archivo histórico;
- R2: consolidación de documentación técnica vigente;
- R3: consolidación normativa, seguridad y privacidad documental;
- R4: transparencia, matriz de trazabilidad, auditoría de cálculos, limitaciones conocidas, dependencias/terceros y proceso de release;
- `README.md` indexado sin reescribir sus 158 ADR;
- ADR-086 registrada como anomalía histórica de metadata;
- regresiones antiguas de gobierno/documentación endurecidas para seguir la versión canónica.

Validación de cierre:

- **458 pruebas automatizadas en `OK`**;
- compilación Python correcta;
- sintaxis JavaScript correcta;
- `git diff --check` limpio.

Tag formal asociado: `v0.0.23-beta`.

### `0.0.24-beta` — 2026-08-18

Tercera versión formal y **cierre integral del programa GOV.1**.

Alcance acumulado:

- firma SSH de commits/tags nuevos y 23/23 tags auditados;
- protección GitHub mediante PR, firmas, historial lineal y checks requeridos;
- actualización controlada a `pypdf 6.15.0`;
- GOV.1.4 Developer Diagnostics;
- GOV.1.5 seguridad/privacidad/transparencia;
- GOV.1.6 controles GitHub;
- GOV.1.7 licencia/distribución;
- GOV.1.8 auditoría transversal y cierre.

Validación final:

- línea base previa: **530 pruebas**;
- suite integrada post-merge: **540 pruebas en `OK`**;
- compilación Python, JavaScript y `git diff --check` correctos;
- checks remotos Python 3.13, Python 3.14 y Auditoría de gobernanza.

Tag formal: `v0.0.24-beta`. El objeto tag anotado y firmado `3cdf6f84804c1bb4bdda9e449eb0932528557aa3` apunta al commit `653900cebd84019fbbaa3ff3cfd91536ccab76eb`.

### `0.0.25-beta` — 2026-08-19

Cuarta versión formal y cierre de UX.4.6e.

Evidencia:

- R9.1 alcanzó **660 pruebas en `OK`**;
- PR #21 integró el cierre funcional por squash;
- PR #22 completó la documentación final;
- `main` final: `7affa00e2530aeede066c10ecfee8c6dbd49b10b`;
- validación post-merge: **660 pruebas**, compilación/sintaxis y `git diff --check` limpios;
- tag firmado `v0.0.25-beta`;
- objeto tag `303d4fe58b200a2c65120758ebe9d991e85b03c5`;
- target final `7affa00e2530aeede066c10ecfee8c6dbd49b10b`.

No se declara una versión oficial de producto con este hito.

### `0.0.26-beta` — 2026-08-20 — cierre formal de PLAN.1

Quinta versión formal legacy.

Evidencia acumulada:

- `v0.0.25-beta` permanece inmutable;
- R1–R3 cerraron progresivamente con 665, 670, 676, 684, 689, 695, 702 y **710 pruebas**;
- R4.1 promovió `VERSION`/`APP_VERSION` a `0.0.26-beta` y cerró localmente con **720 pruebas**;
- commit firmado: `7c50d989f5c6d266db26c9625367dd82e9895aba`;
- PR #23 integrado por squash en `497097f720c98f6e5a7ed689cf91368011a96be1`;
- higiene pre-tag `d3436db4e06b96cf92bb6e0476c03b56b1e40ca8`;
- Pull Request #24 integrado por squash en `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`;
- checks Python 3.13, Python 3.14 y Auditoría de gobernanza en `success`;
- gate final post-merge: **720 pruebas en `OK`** sin `SyntaxWarning`;
- tag formal: `v0.0.26-beta`;
- objeto tag firmado: `bfbb746b177ebcc577f7241fef4d6914f713739a`;
- target: `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`.

`v0.0.26-beta` es inmutable y no debe moverse ni recrearse.

La segunda pasada de VER.2 reconoce dentro de PLAN.1 diez estados aceptados G051–G060: R1, R2A, R2B1, R2B2, R2C, R3A, R3B1, R3B2, R4.1 y R4.2. Esta granularidad revision-aware no crea ni mueve tags históricos.

## 5. Reconstrucción histórica del estado posterior a `v0.0.26-beta` y del candidato VER.2

> **Contexto histórico:** este apartado conserva el estado de VER.2 antes de su cierre
> formal. Las referencias siguientes a candidato, tag pendiente, merge futuro o
> revalidación pendiente describen aquel momento y no el estado actual. VER.2 fue
> posteriormente integrado y `v0.0.71.01-beta` quedó publicado como tag formal.


UX.4.6f, UX.4.6g, UX.4.6h y UX.4.6i se desarrollaron y cerraron históricamente **sin publicar un tag adicional y manteniendo `VERSION = 0.0.26-beta`**. VER.2 no inventa releases retroactivas para esos bloques; su posición se reconstruye en el ledger como G061–G070.

`0.0.71.01-beta` queda promovido en `VERSION` como VER.2 G071/E01 durante R4; no mueve `v0.0.26-beta`, no crea tag dentro del PR y requiere merge, revalidación post-merge y firma antes de declarar publicado `v0.0.71.01-beta`.

La base inmediatamente anterior a VER.2 es:

```text
7037addd44253e528c77460b678d2b3ccd540dd5
G070 / E02 — cierre UX.4.6i — 841 pruebas
```

VER.2 usa como **candidato**, no como release publicada:

```text
0.0.71.01-beta
G071 / E01
```

Mientras el PR de VER.2 no supere el gate completo y se integre:

- G071 queda promovido en `VERSION` durante R4;
- no existe tag `v0.0.71.01-beta` hasta completar merge, revalidación post-merge y firma;
- `v0.0.26-beta` continúa siendo el último tag formal legacy hasta ese cierre;
- no se crean tags revision-aware retrospectivos para G001–G070.

Si VER.2 se integra satisfactoriamente, `0.0.71.01-beta` pasa a ser el primer estado nuevo gobernado por la familia revision-aware. La creación de su tag, si corresponde al cierre, se realizará únicamente después de merge y revalidación.

La distribución del contador aceptado hasta G070 se conserva de forma auditable en `docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md`, `docs/governance/pre-1-0-revision-ledger.md` y `data/pre-1-0-revision-ledger.json`; los intentos fallidos, refinamientos sin aceptación independiente y checkpoints absorbidos se preservan como evidencia sin consumir un `G` adicional.

## 6. Migración criptográfica de tags — materializada

El 2026-08-17 se materializaron `v0.0.1-beta` a `v0.0.21-beta` como tags retrospectivos firmados y se reemitieron una sola vez `v0.0.22-beta` y `v0.0.23-beta`.

La operación no reescribió commits históricos ni falseó fechas de creación.

Resultado de auditoría Git:

- 23/23 tags con firma SSH válida;
- 23/23 objetos tag presentes remotamente;
- 23/23 targets remotos comprobados;
- `v0.0.22-beta`: `31accfc9a6014367179c97cfe54c5a223be8988f` → `bda764edb84ccaeb610a629fca1283bbd97e69a4`, conservando `1222de61a6d2ca48fb8731fe4755f5b7eeef38f5`;
- `v0.0.23-beta`: `609edf4bfed33c64770c88fab401002cd90f8e66` → `06b9260dadbcb2f0a7711841e1fad228e1badee8`, conservando `07278f7a193ce964612d9697da57350691bf62c0`.

Desde entonces los tags publicados son inmutables. `v0.0.24-beta`, `v0.0.25-beta` y `v0.0.26-beta` fueron creados posteriormente bajo la política formal y elevan el inventario a 26 tags firmados legacy/retrospectivos.

## 7. Línea beta revision-aware y versión oficial futura

Después de VER.2, los estados beta nuevos usan:

```text
0.GG.RR.EE-beta
```

La familia `0.0.N-beta` queda preservada como historia publicada y no continúa incrementándose.

Cuando todos los gates de producto estén cerrados, la primera versión oficial objetivo será:

```text
Versión 1.0.0.0
Build 000001
Tag v1.0.0.0
```

La planificación anterior que reservaba `0.1.0-beta.1` como futura primera beta pública queda sustituida. Ese cambio no reescribe la evidencia histórica de los documentos y versiones que la mencionaron mientras estaba vigente.

La transición a `1.0.0.0` depende del cierre de la secuencia definida en `docs/governance/master-plan-to-1-0.md`, incluidos gates funcionales, de seguridad, accesibilidad, revisión y release.

<!-- ANCLAS_HISTORICAS_VER2_RELEASES_CONSOLIDADAS -->

## Compatibilidad histórica preservada por VER.2

- PLAN.1 preserva evidencia del Pull Request #23 y del cierre posterior con `v0.0.26-beta`.
- UX.4.6e R9.2 fue integrado mediante `18e81e4ff58a1ad9622d366f7add10b7674f6e44` y conserva sus tags legacy inmutables.

## 6. Línea oficial futura prevista

La línea oficial futura prevista permanece orientada a `1.0.0.0` con Build independiente. Las betas legacy y revision-aware no son la primera versión oficial.
- `0.0.24-beta` no es una beta pública; conserva el cierre interno de GOV.1 antes de los hitos UX y PLAN posteriores.

## Reconciliación post-G070 — 2026-08-25

La auditoría integral posterior a SEC.2 determinó que el ledger publicado con
VER.2 se detuvo materialmente en G070 antes de contabilizar estados aceptados de
DEV.2, MANT.1, DOC.1, NOR.1, NOR.2 y SEC.2. La reconstrucción basada en commits,
PR y gates reales sitúa `4bd7d8d` en **G108**. AUD.SEC2 R1 fue aceptado después
mediante PR #83 y merge `ec1842d` como **G109/E01**; G110/E01 quedó posteriormente consumido por REL.GOV.1 mediante PR #85; G111/E01 queda disponible
para DOC.2. El tag `v0.0.71.01-beta` permanece publicado e inmutable; su número
no se reescribe aunque el estado que materializó se corresponda cronológicamente
con G087.
