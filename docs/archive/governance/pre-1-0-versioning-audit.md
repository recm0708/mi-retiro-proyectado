# Auditoría de versionado pre-1.0

**Proyecto:** Mi Retiro Proyectado
**Bloque:** VER.2 — reconciliación de revisiones pre-1.0
**Fecha de cierre contable de segunda pasada:** 2026-08-22
**Base auditada:** `main` en `7037addd44253e528c77460b678d2b3ccd540dd5`
**Estado:** auditoría contable cerrada en G070; materialización técnica y gate de VER.2 en curso

## 1. Objetivo

Reconstruir la secuencia real de estados aceptados del proyecto antes de continuar con DEV.2, sin convertir commits administrativos en revisiones, sin ocultar subfases históricas y sin reescribir tags ya publicados.

La auditoría parte de Git como evidencia primaria y cruza `RELEASES.md`, `CHANGELOG.md`, `docs/REGISTRO_CAMBIOS_HISTORICO.md`, bitácoras UX, auditorías de cierre, Pull Requests, gates de pruebas, decisiones ADR y conversaciones de desarrollo recuperadas.

La decisión fila por fila se conserva en `MATRIZ_DECISION_REVISIONES_VER2.md`. El resultado se materializa en `LEDGER_REVISIONES_PRE_1_0.md` y `data/revision_ledger_pre_1_0.json`.

## 2. Problema detectado

La política anterior `0.0.N-beta` identificaba hitos formales, pero no permitía expresar de forma estable las revisiones internas aceptadas entre releases. Un primer intento de reconciliación hacia `0.0.30-beta` trató los bloques UX posteriores a PLAN.1 como betas consecutivas. Después, un conteo de 163 revisiones mezcló estados aceptados con commits `feat/test/docs`, checkpoints todavía pendientes de validación y candidatos locales.

La primera pasada de VER.2 corrigió ese exceso pero comprimió demasiado el historial y propuso G057. Una segunda corrección provisional llevó a G060. Ambos conteos quedaron superados al aplicar de manera uniforme la misma regla a mantenimiento técnico, seguridad, gobierno, dependencias, checkpoints y cierres post-tag.

El resultado de la segunda pasada es **G070 como último estado aceptado antes de VER.2**.

## 3. Regla contable definitiva

Una entrada incrementa el contador global únicamente cuando representa un **estado materialmente distinto, aceptado y auditable**.

Se aplican estas reglas:

1. Los 21 estados retrospectivos reconstruidos por GOV.1.1 (`0.0.1-beta` a `0.0.21-beta`) cuentan una vez cada uno. Los 80 commits que contienen no se vuelven a contar individualmente.
2. Una revisión interna cuenta cuando la evidencia la describe como cerrada, completada o validada y el proyecto avanza desde ese estado.
3. Un candidato explícitamente pendiente de validación, PR, CI, tag o revisión manual no cuenta todavía como estado aceptado.
4. Un intento que falla su gate no consume un Global nuevo. La corrección conserva la identidad del candidato mientras no haya un estado aceptado diferente.
5. Los commits lógicos `feat`, `test` y `docs` que materializan una misma revisión no son revisiones independientes.
6. PR, squash, CI y tag son evidencia de integración/cierre; no agregan otra revisión cuando representan el mismo estado.
7. Un mantenimiento técnico, de seguridad, gobierno, dependencias o documentación **sí puede contar** cuando crea un estado independiente, validado y aceptado.
8. Un checkpoint que solo consolida estados ya contabilizados o deja expresamente pendiente la revisión funcional siguiente no cuenta otra vez.
9. La documentación histórica conserva sus identificadores originales. No se inventan retrospectivamente nombres R que nunca existieron.
10. Los tags publicados permanecen inmutables y conservan su numeración histórica.

## 4. Resultado global

La base `7037addd` contiene **70 estados aceptados** según la regla anterior.

| Rango global | Alcance | Estados que cuentan |
|---|---|---:|
| G001–G021 | Estados retrospectivos `0.0.1-beta`–`0.0.21-beta` | 21 |
| G022 | GOV.1.2 — gobierno y primera versión formal | 1 |
| G023–G026 | GOV.1.3 R1–R4 | 4 |
| G027–G031 | Prebloque transversal de firma e integridad Git/GitHub | 5 |
| G032 | GOV.1.4 — Developer Diagnostics | 1 |
| G033–G035 | GOV.1.5 R1–R3 | 3 |
| G036 | GOV.1.6 — controles GitHub | 1 |
| G037 | GOV.1.7 — licencia y distribución | 1 |
| G038 | Hotfix de formato de licencia | 1 |
| G039 | GOV.1.8 — cierre integral de GOV.1 | 1 |
| G040 | Saneamiento post-GOV.1 | 1 |
| G041–G050 | UX.4.6e — R1–R7, identidad/publicación, R8 y R9 | 10 |
| G051–G060 | PLAN.1 — R1, R2A, R2B1, R2B2, R2C, R3A, R3B1, R3B2, R4.1 y R4.2 | 10 |
| G061–G064 | UX.4.6f — R1/R1.1 conjunta, mantenimiento dependencias, R2 y hardening pre-commit | 4 |
| G065 | UX.4.6g — cierre del Paso 5 | 1 |
| G066–G068 | UX.4.6h — R1.1, R1.2 y R1.3 | 3 |
| G069–G070 | UX.4.6i — R1 y R1.4/cierre | 2 |
| **Total** |  | **70** |

El detalle fila por fila se conserva en `docs/LEDGER_REVISIONES_PRE_1_0.md` y `data/revision_ledger_pre_1_0.json`.

## 5. Decisiones históricas relevantes

### UX.2.1

UX.2.1 existió como estabilización visual transversal: tema Oscuro más profundo, Alto contraste negro/blanco, tokens semánticos y remates de superficies/textos. Sus regresiones forman parte del mismo rango Git reconstruido como `0.0.9-beta`. Se documenta dentro de G009, pero no incrementa otra vez el contador.

### UX.4.6a, UX.4.6b, UX.4.6c y UX.4.6d

Sus revisiones internas permanecen en las bitácoras históricas. Los cierres aceptados ya están representados por G018, G019, G020 y G021:

- UX.4.6a: cierre validado con 198 pruebas;
- UX.4.6b: R4, 233 pruebas y validación PC/laptop/CI;
- UX.4.6c: R3, 253 pruebas;
- UX.4.6d: R23, 396 pruebas y recorrido Pasos 1–3 aceptado.

En UX.4.6d, R1–R22 conservaban validaciones integrales pendientes, por lo que no se transforman retroactivamente en Globals aceptados.

### GOV.1.1

GOV.1.1 reconstruyó y clasificó los 21 estados preexistentes. No crea una fila adicional: su resultado está representado por G001–G021. GOV.1.2 es el siguiente estado nuevo.

### Prebloque de firma e integridad

La primera pasada lo comprimió en un único Global. La segunda pasada demuestra cinco estados sucesivos aceptados:

1. materialización criptográfica y auditoría de 23/23 tags;
2. PR #9 — CI v7 y protecciones GitHub, 470 pruebas;
3. PR #10 — corrección de rutas PowerShell/caracteres de control, 470 pruebas;
4. PR #11 — actualización controlada a `pypdf 6.15.0`, 474 pruebas;
5. PR #12 — cierre formal del prebloque, 474 pruebas y revisión final de PR pendientes.

Por eso ocupan G027–G031.

### GOV.1.5

R1 y R2 poseen identidad y cierre histórico propios, no son nombres retrospectivos inventados:

- R1 — modelo de amenazas, 7 regresiones específicas;
- R2 — derechos e incidentes, 8 regresiones adicionales y 502 pruebas antes de R3;
- R3 — PR #14, cierre del bloque con 512 pruebas.

Ocupan G033–G035.

### Hotfix de licencia y saneamiento post-GOV.1

El hotfix de licencia PR #16 se integró después del estado GOV.1.7, corrigió documentos y endureció su regresión manteniendo 530/530. Es un estado aceptado posterior y ocupa G038.

PR #18 se integró después de GOV.1 con 30 archivos modificados y 540/540: auditoría del repositorio, soporte, código de conducta y configuración pública. Es un mantenimiento de gobierno independiente y ocupa G040.

### UX.4.6e

Se cuentan R1–R7, el hito transversal de identidad visual/publicación PR #20, R8 y R9/cierre: diez estados G041–G050.

No se duplican:

- PR #19, porque consolida revisiones ya contabilizadas y deja R8 expresamente pendiente;
- R8.1, porque fue corregida antes de la aceptación funcional R8.2;
- el cierre documental de 652, porque materializa la misma R8 cuya validación funcional R8.2 alcanzó 644;
- PR #22, porque registra el cierre documental post-merge de R9 ya contabilizada.

### PLAN.1

La evidencia conserva R1, R2A, R2B1, R2B2, R2C, R3A, R3B1, R3B2, R4.1 y R4.2: diez estados G051–G060.

R4.1 alcanzó 720 pruebas, fue declarado cerrado y llegó a `main` por PR #23. Después el gate post-merge reveló un `SyntaxWarning`; R4.2/PR #24 corrigió ese estado y repitió 720 pruebas sin la advertencia antes del tag. Ambas son revisiones sucesivas aceptadas.

PR #25 es reconciliación documental post-tag y no suma otra fila.

### UX.4.6f

R1 y R1.1 se aceptaron conjuntamente por PR #28 con 743 pruebas y validación visual, por lo que ocupan una sola fila G061.

PR #29 actualizó `pypdf 6.16.1` y `uvicorn 0.52.3`, mantuvo 743 pruebas y pasó los tres checks requeridos: es mantenimiento técnico independiente, G062.

R2/PR #30 cerró la auditoría lógica y matemática con 756 pruebas: G063.

PR #31 no se duplica por su parte documental, pero sí crea un estado técnico posterior al añadir un gate `pre-commit` reproducible y cinco regresiones, alcanzando 762 pruebas: G064.

### UX.4.6g

PR #32 consolida el R1 completo y cierra el Paso 5 con 784 pruebas: G065. Los nombres R1.2/R1.3/R1.4/R1.4.2/R1.4.3 se preservan como refinamientos internos porque no se recuperó evidencia inequívoca de aceptación independiente entre ellos.

### UX.4.6h

R1 fue un candidato fallido y no consume Global. R1.1 corrigió ese estado y fue aceptada; R1.2 también fue aceptada; R1.3 creó el informe A4 y cerró el bloque con 812 pruebas/PR #33. Ocupan G066–G068.

### UX.4.6i

La secuencia canónica demostrable es:

```text
R1 → R1.2 → R1.3 → R1.4
```

No existe R1.1 independiente: las referencias a ese nombre corresponden a un hotfix documental dentro del gate R1.

R1 alcanzó el gate aceptado de 826 pruebas y ocupa G069. R1.2 y R1.3 están documentadas como refinamientos, pero no se recuperó aceptación diferenciada suficiente para consumir Globals separados. R1.4 cerró el bloque por PR #34 con 841 pruebas y ocupa G070.

## 6. Identificador revision-aware

La nueva familia beta usa:

```text
0.GG.RR.EE-beta
```

Donde:

- `G = revisión global aceptada`;
- `GG = G // 100`;
- `RR = G % 100`, siempre con dos dígitos;
- `EE = ordinal aceptado dentro del bloque vigente`, con dos dígitos.

Ejemplos:

```text
G001, E01 -> 0.0.01.01-beta
G070, E02 -> 0.0.70.02-beta
G071, E01 -> 0.0.71.01-beta
G100, E03 -> 0.1.00.03-beta
G425, E12 -> 0.4.25.12-beta
```

Estos identificadores permiten auditar el ledger. **No renombran ni reemplazan retrospectivamente los tags históricos.**

La base `7037addd` corresponde conceptualmente a G070/E02. VER.2 R1 usa como candidato:

```text
G071 / E01 -> 0.0.71.01-beta
```

Un intento fallido de VER.2 no convierte G071 en estado aceptado. La aceptación exige ledger estructurado válido, gate completo, PR/CI e integración.

## 7. Ledger estructurado

VER.2 materializa la reconstrucción en:

```text
data/revision_ledger_pre_1_0.json
```

El archivo declara:

- `accepted_count = 70`;
- G001–G070 contiguos y sin duplicados;
- `next_global_if_ver2_accepted = 71`;
- candidato `0.0.71.01-beta`;
- rango de tags legacy inmutables `v0.0.1-beta`–`v0.0.26-beta`;
- exclusiones históricas con motivo.

`app/core/version_ledger.py` valida esas invariantes y `tests/test_ver2_ledger_estructurado.py` protege el contrato.

## 8. Transición a versión oficial

PLAN.1 permanece vigente: la primera versión oficial objetivo sigue siendo:

```text
1.0.0.0
Build 000001
```

El cambio de familia beta no modifica el esquema oficial de cuatro componentes ni la independencia del Build.

## 9. Criterio de cierre de VER.2

Antes de aceptar G071 deben quedar completados:

- `VERSIONING.md` revision-aware;
- validador de versión compatible con legacy histórico, nueva beta y versión oficial;
- ledger Markdown y JSON auditable;
- validador del ledger y regresiones contra deriva;
- corrección de referencias falsas/ambiguas de UX.4.6i R1.1;
- separación entre versión actual y versión histórica de revisión documental;
- README, ROADMAP, RELEASES, CHANGELOG, índice y plan maestro coherentes;
- ausencia de referencias vigentes que congelen G057/G058/G060 o `0.0.58.01-beta`;
- suite completa, `pip check`, `compileall`, sintaxis JavaScript y `git diff --check` limpios;
- PR y CI requeridos en verde.

Solo después de ese cierre G071 queda aceptado y DEV.2 vuelve a ser el bloque funcional activo.
