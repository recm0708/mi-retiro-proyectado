# Registro de versiones y estados del proyecto

**Fecha de reconstrucción histórica:** 2026-08-17
**Fuente:** historial Git de `recm0708/mi-retiro-proyectado`
**Revisión de planificación hacia 1.0:** 2026-08-20

## 1. Naturaleza del registro

Las versiones `0.0.1-beta` a `0.0.21-beta` fueron asignadas retrospectivamente en GOV.1.1 para organizar estados funcionales que ya existían en Git. No fueron tags ni GitHub Releases publicados en sus fechas originales. La migración criptográfica del 2026-08-17 autoriza materializarlas posteriormente como tags firmados, conservando explícitamente esa naturaleza retrospectiva.

Git conserva la evidencia primaria: hashes, fechas, autores, mensajes y contenido. Este documento añade una clasificación legible sin reescribir esa evidencia.

El commit raíz real es `a0a9e09` (`tipo: descripción del cambio`). Su mensaje es una anomalía histórica previa a la convención posterior y se conserva sin modificar.

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

## 3. Marcador histórico `0.1.0`

El repositorio nació con `0.1.0` escrito en la configuración, README y CHANGELOG. No existió un tag ni una GitHub Release que materializara ese número. GOV.1 lo clasifica como **marcador de desarrollo no publicado**.

No se elimina esta evidencia de la historia Git. El estado actual se corrige hacia una política explícita sin alterar commits antiguos.

## 4. Versiones formales desde GOV.1.2

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
- validación final del hito con compilación Python, JavaScript válido, `git diff --check` limpio y **403 pruebas automatizadas en OK**.

El tag formal asociado es `v0.0.22-beta`.

### `0.0.23-beta` — 2026-08-17

Segunda versión formal bajo `VERSIONING.md` y cierre de GOV.1.3.

Alcance del hito:

- R1: reorganización de documentos de entrada y archivo histórico;
- R2: consolidación de documentación técnica vigente;
- R3: consolidación normativa, seguridad y privacidad documental;
- R4: transparencia, matriz de trazabilidad, auditoría de cálculos, limitaciones conocidas, dependencias/terceros y proceso de release;
- `DECISIONES.md` indexado sin reescribir sus 158 ADR;
- ADR-086 registrada como anomalía histórica de metadata, sin asignarle retroactivamente un estado no documentado;
- regresiones antiguas de gobierno/documentación endurecidas para seguir la versión canónica.

Validación local del candidato de cierre:

- **458 pruebas automatizadas en `OK`**;
- compilación Python correcta;
- sintaxis JavaScript correcta;
- `git diff --check` limpio.

Tag formal asociado:

```text
v0.0.23-beta
```

### `0.0.24-beta` — 2026-08-18

Tercera versión formal bajo `VERSIONING.md` y **cierre integral del programa GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta**.

Alcance acumulado desde `0.0.23-beta`:

- firma SSH obligatoria de commits y tags nuevos;
- 23/23 tags históricos/formales auditados y rulesets de integridad;
- GitHub `main` protegido mediante PR, firmas, historial lineal y checks requeridos;
- actualización controlada a `pypdf 6.15.0`;
- GOV.1.4: Developer Diagnostics local, estructurado y sin telemetría remota;
- GOV.1.5: modelo de amenazas, derechos del titular, incidentes, terceros, TLS y gates pre-publicación;
- GOV.1.6: `SECURITY.md`, templates GitHub y workflow `Auditoría de gobernanza`;
- GOV.1.7: licencia propietaria pre-beta, avisos de terceros y estrategia de distribución;
- hotfix de formato de los documentos de licencia con regresión reforzada;
- GOV.1.8: auditoría transversal, cierre documental, versión formal y decisión de reanudar UX.4.6e.

Validación final de cierre:

- línea base previa: **530 pruebas en `OK`**;
- GOV.1.8 añadió **10 regresiones específicas**;
- suite integrada post-merge: **540 pruebas en `OK`**;
- compilación Python correcta;
- sintaxis JavaScript correcta;
- `git diff --check` limpio;
- checks remotos `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza` requeridos para el PR de cierre.

Tag formal asociado:

```text
v0.0.24-beta
```

El tag fue creado **después** de integrar el PR #17, sincronizar `main`, repetir la validación y confirmar CI remota verde. El objeto tag anotado y firmado `3cdf6f84804c1bb4bdda9e449eb0932528557aa3` apunta al commit `653900cebd84019fbbaa3ff3cfd91536ccab76eb`.

`0.0.24-beta` conserva el contexto histórico con el que se cerró GOV.1 y **no es una beta pública** según la terminología empleada en ese cierre.

### `0.0.25-beta` — 2026-08-19

Cuarta versión formal bajo `VERSIONING.md` y cierre de UX.4.6e.

Evidencia de cierre:

- `VERSION` y `APP_VERSION` apuntan a `0.0.25-beta`;
- R8 quedó cerrada funcionalmente y R9.1 alcanzó **660 pruebas en `OK`**, con `git diff --check` limpio;
- PR #21: `feat(ux): cerrar UX.4.6e y preparar 0.0.25-beta`;
- head validado: `a064bf745f4fb5e55e70f6ae3fd9b2bb80af8148`;
- checks requeridos del PR: `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza` en `success`;
- squash funcional integrado en `main`: `18e81e4ff58a1ad9622d366f7add10b7674f6e44`;
- PR #22 cerró la documentación final de release;
- commit final de `main`: `7affa00e2530aeede066c10ecfee8c6dbd49b10b`;
- validación local post-merge: **660 pruebas en `OK`**, compilación Python y sintaxis JavaScript correctas, `git diff --check` y working tree limpios;
- tag formal `v0.0.25-beta` con firma SSH válida;
- tag formal asociado: `v0.0.25-beta`;
- objeto tag remoto `303d4fe58b200a2c65120758ebe9d991e85b03c5`;
- el tag resuelve al commit final `7affa00e2530aeede066c10ecfee8c6dbd49b10b`.

No se declara una versión oficial de producto con este hito.

### `0.0.26-beta` — 2026-08-20 — cierre formal de PLAN.1

Quinta versión formal bajo `VERSIONING.md` y candidato local validado de cierre de PLAN.1.

Evidencia acumulada antes del cierre remoto:

- `v0.0.25-beta` permanece inmutable y continúa apuntando a `7affa00e2530aeede066c10ecfee8c6dbd49b10b`;
- R1–R3 de PLAN.1 cerraron progresivamente con 665, 670, 676, 684, 689, 695, 702 y finalmente **710 pruebas en `OK`**;
- R4.1 promueve `VERSION` y `APP_VERSION` a `0.0.26-beta`;
- la documentación viva se audita contra el candidato sin modificar motores, fórmulas ni normativa JSON;
- R4.1 fue validada localmente con **720 pruebas en `OK`**, `python -m compileall app`, validación de sintaxis JavaScript y `git diff --check` limpio.

Estado remoto y cierre:

- commit de PLAN.1 firmado: `7c50d989f5c6d266db26c9625367dd82e9895aba`;
- Pull Request #23: integrado por squash en `497097f720c98f6e5a7ed689cf91368011a96be1`;
- higiene pre-tag firmada: `d3436db4e06b96cf92bb6e0476c03b56b1e40ca8`;
- Pull Request #24: integrado por squash en `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`;
- checks `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza`: `success`;
- gate final post-merge: **720 pruebas en `OK`**, sin `SyntaxWarning`, compilación Python, sintaxis JavaScript y `git diff --check` correctos;
- tag formal: `v0.0.26-beta`;
- objeto tag firmado: `bfbb746b177ebcc577f7241fef4d6914f713739a`;
- target del tag: `b572796d68ff6fd91ce9944a0c6d1cf7d45753a0`;
- firma SSH local verificada con la clave autorizada del mantenedor.

`v0.0.26-beta` es inmutable y no debe moverse ni recrearse. La reconciliación documental posterior se registra en `[Unreleased]` y no altera el contenido del hito etiquetado.

## 5. Migración criptográfica de tags — materializada

El 2026-08-17 se materializaron `v0.0.1-beta` a `v0.0.21-beta` como tags retrospectivos firmados y se reemitieron una sola vez `v0.0.22-beta` y `v0.0.23-beta`.

La operación no reescribió commits históricos ni falseó fechas de creación.

Resultado de auditoría Git:

- 23/23 tags con firma SSH válida;
- 23/23 objetos tag presentes remotamente;
- 23/23 targets remotos comprobados;
- `v0.0.22-beta`: `31accfc9a6014367179c97cfe54c5a223be8988f` → `bda764edb84ccaeb610a629fca1283bbd97e69a4`, conservando `1222de61a6d2ca48fb8731fe4755f5b7eeef38f5`;
- `v0.0.23-beta`: `609edf4bfed33c64770c88fab401002cd90f8e66` → `06b9260dadbcb2f0a7711841e1fad228e1badee8`, conservando `07278f7a193ce964612d9697da57350691bf62c0`.

La materialización criptográfica está completada. Desde entonces los tags publicados son inmutables.

El tag posterior `v0.0.24-beta` fue creado ya bajo esta política y elevó el inventario a 24 tags firmados. `v0.0.25-beta` es el siguiente tag formal firmado y eleva el inventario formal vigente a 25 tags.

## 6. Línea oficial futura prevista

La etapa beta continúa con la convención:

```text
0.0.N-beta
```

Cuando todos los gates de producto estén cerrados, la primera versión oficial objetivo será:

```text
Versión 1.0.0.0
Build 000001
Tag v1.0.0.0
```

La planificación anterior que reservaba `0.1.0-beta.1` como futura primera beta pública queda sustituida por PLAN.1. Este cambio de planificación no reescribe la evidencia histórica de los documentos y versiones que la mencionaron mientras estaba vigente.

La transición a `1.0.0.0` no ocurre automáticamente por terminar un bloque concreto. Depende del cierre de la secuencia definida en `docs/PLAN_MAESTRO_HACIA_1_0.md`, incluidos los gates funcionales, de seguridad, accesibilidad, revisión y release.
