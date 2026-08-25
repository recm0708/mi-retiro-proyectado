# Auditoría de reconciliación revision-aware posterior a G070

**Proyecto:** Mi Retiro Proyectado
**Fecha:** 2026-08-25
**Base histórica preservada:** `7037addd44253e528c77460b678d2b3ccd540dd5` — G070
**Commit auditado antes de remediación:** `4bd7d8d57c8ccf6229ff2e53493c996b29db14a2`
**Resultado contable:** G108 aceptado; G109 disponible
**Clasificación:** Auditoría / Gobierno / Versionado

## 1. Motivo

VER.2 reconstruyó 70 estados aceptados hasta el cierre de UX.4.6i en
`7037addd`. Después de esa base se ejecutaron DEV.2, MANT.1, DOC.1, VER.2,
NOR.1, NOR.2 y SEC.2. El ledger estructurado continuó congelado en G070 y
no incorporó esa evolución posterior.

Esta auditoría no reescribe G001–G070 ni mueve tags. Aplica la misma regla
de decisión definida por VER.2: cuenta estados materialmente distintos con
evidencia suficiente de aceptación y excluye candidatos, refinamientos del
mismo estado y checkpoints que solo sincronizan un cierre ya contabilizado.

Un punto decisivo es VER.2 R3: su decisión operativa declara expresamente que
**VER.2 R1, R2 y R3 son correcciones internas del mismo candidato G071/E01**,
que **no consumen G072** y que **no incrementan EE**. Por ello esas tres
revisiones no pueden contarse como Globales independientes. VER.2 R4 es la
aceptación única de ese candidato.

## 2. Resultado

Se identifican **38 estados aceptados adicionales** después de G070. Por tanto:

```text
G070 + 38 = G108
```

El siguiente Global disponible es G109. La auditoría/remediación post-SEC.2
queda reservada como candidato `AUD.SEC2 R1`:

```text
G109 / E01 -> 0.1.09.01-beta
```

El candidato no se considera aceptado hasta superar gate completo, commit
firmado, PR/CI e integración.

## 3. Estados aceptados reconstruidos

| Global | Bloque | Estado aceptado | Evidencia resumida |
|---:|---|---|---|
| G071 | DEV.2 | R1 — Centro de desarrollo y estado interno | commit 06e2821 / PR #37; apertura funcional DEV.2 |
| G072 | DEV.2 | R2 — visor diagnóstico seguro | commit 5451d18 / PR #39; visor y exportación diagnóstica |
| G073 | DEV.2 | R3 — autodiagnóstico técnico local | commit 9fb86af / PR #40; autodiagnóstico y regresiones |
| G074 | MANT.1 | R2 — documentación de scripts y hooks | commit 8fdc389 / PR #42; R1 queda como auditoría inicial absorbida |
| G075 | MANT.1 | R3 — encabezados YAML de GitHub | commit 9013aa3; regresión YAML |
| G076 | MANT.1 | R4 — limpieza de trazabilidad en encabezados operativos | commit e894bcc; regresión de encabezados |
| G077 | MANT.1 | R5A — comentarios internos en servicios Python | commit 46e51d5; regresión de comentarios Python |
| G078 | MANT.1 | R5B — comentarios en CSS y plantilla | commit 97b4984; regresión de comentarios CSS/Jinja |
| G079 | MANT.1 | R5C — comentarios en JavaScript complejo | commit 0b349ce; regresión de comentarios JavaScript |
| G080 | MANT.1 | R5D — política y plantillas por extensión | commit 77b413e; política y regresiones por extensión |
| G081 | MANT.1 | R5E — estandarización de nombres de carpetas | commit 42c2cea; migración de carpetas y regresiones |
| G082 | MANT.1 | R5F — normalización de nombres de archivos | commit ba6995e; migración de archivos y regresiones |
| G083 | MANT.1 | R5G — auditoría y consolidación documental | commit 9a8a795; índice/enlaces y regresión documental |
| G084 | MANT.1 | R5H — auditoría de nombres técnicos restantes | commit ab92677 / PR #53; normalización y regresiones |
| G085 | MANT.1 | R6 — auditoría funcional post-renombres | commit 9ac55ca / PR #54; validación funcional focalizada |
| G086 | DOC.1 | R1 — auditoría Markdown post-MANT.1 | commit d991890 / PR #56; auditoría y línea base documental |
| G087 | VER.2 | R4 — promoción controlada publicada como 0.0.71.01-beta | PR #60; commit cb1dc24; tag firmado v0.0.71.01-beta |
| G088 | NOR.1 | R1 — estándares de estructura y nomenclatura | commit firmado 67aae43 dentro de PR #62 |
| G089 | NOR.1 | R1.1 — estructura documental para auditorías e históricos | commit firmado 10e195d dentro de PR #62 |
| G090 | NOR.1 | R3 — clasificación documental inicial | commit firmado 8c26c60; squash f1489ef / PR #62 |
| G091 | NOR.1 | R4 — auditoría de nomenclatura | commit fc4b1ef / PR #63 |
| G092 | NOR.1 | R5 — auditoría de dependencias documentales | commit 4cf6b3d; evidencia documental |
| G093 | NOR.1 | R6 — estándares determinísticos consolidados | commit e33f594; gate previo a cierre |
| G094 | NOR.2 | R1 — línea base de normalización | commit c0e06ca / PR #67 |
| G095 | NOR.2 | R2 — matriz de migración | commit 4d4e56f; matriz aprobada |
| G096 | NOR.2 | R3 — migración de runtime y configuración | commit b037518; migración técnica |
| G097 | NOR.2 | R4 — normalización de documentación viva | commit 65b8fd9 / PR #70 |
| G098 | NOR.2 | R5 — archivo de documentación histórica | commit ad9b3f3 / PR #71 |
| G099 | NOR.2 | R6 — normalización de ledger y datos | commit 365ba5b / PR #72 |
| G100 | NOR.2 | R7 — depuración de artefactos locales | commit b8ffd39 / PR #73 |
| G101 | NOR.2 | R8 — auditoría integral de cierre | commit b4df9b7 / PR #74 |
| G102 | DOC.1 | R2 — auditoría integral Markdown post-NOR.2 | commit 46ca30e / PR #76 |
| G103 | SEC.2 | R1 — hardening CodeQL y workflows | commit e946af7 / PR #77 |
| G104 | SEC.2 | R2 — autenticación administrativa | commits firmados 92b1e8e y 287ff81 dentro de PR #79 |
| G105 | SEC.2 | R3 — protección centralizada de endpoints | commit firmado 771015d dentro de PR #79 |
| G106 | SEC.2 | R4 — auditoría y observabilidad administrativa | commit firmado 5006e28; squash d7a3b54 / PR #79 |
| G107 | SEC.2 | R5 — sesión administrativa web | commit 0966cd2 / PR #80 |
| G108 | SEC.2 | R6 — hardening de sesiones administrativas | commit 38da72f / PR #81 |

## 4. Estados revisados que no consumen Global

| Estado | Motivo de exclusión |
|---|---|
| DEV.2 R1 cierre documental | Sincroniza el R1 ya contabilizado. |
| DEV.2 R4 cierre formal | Checkpoint que agrupa R1–R3 sin nueva capacidad. |
| MANT.1 R1 | Auditoría inicial absorbida por la primera revisión aplicada R2. |
| MANT.1 R7 | Verificación de estabilidad posterior a R6; no introduce estado material nuevo. |
| VER.2 R1–R3 | La decisión R3 establece que son correcciones internas del mismo candidato G071/E01; no consumen G072 ni incrementan EE. |
| VER.2 R5 | Estabilización post-release; verifica el tag/estado sin cambiar runtime, contratos o versión. |
| NOR.1 R2 | Inventario generado dentro de R1.1; no existe revisión aceptada independiente. |
| NOR.1 R7 | Cierre/checkpoint; no añade un estándar nuevo posterior a R6. |
| NOR.2 R8 sincronización post-merge / PR #75 | Sincroniza el cierre R8 ya contabilizado. |
| SEC.2 R1 cierre documental / PR #78 | Materializa documentación del R1 ya contabilizado. |
| SEC.2 cierre formal `4bd7d8d` | Consolida R1–R6 sin añadir otro control de seguridad. |

## 5. Anomalía de `v0.0.71.01-beta`

El tag `v0.0.71.01-beta` es un artefacto formal publicado e inmutable. La
reconciliación cronológica sitúa la aceptación final de VER.2 R4 en **G087/E01**.
La diferencia se documenta, pero el tag **no se mueve, renombra, elimina ni
recrea**. La corrección del contador se aplica únicamente hacia adelante.

## 6. Evidencia y límites

La reconstrucción usa:

- historial Git/GitHub y commits firmados disponibles;
- Pull Requests que conservan commits internos cuando el squash de `main` los absorbió;
- `CHANGELOG.md`, documentación de cierre y auditorías versionadas;
- pruebas de regresión específicas;
- la regla histórica de VER.2 y, en particular, la decisión de R3 sobre G071/E01.

No se cuenta un estado solo porque exista un commit. Tampoco se inventa una
revisión ausente para rellenar numeración de fase.
