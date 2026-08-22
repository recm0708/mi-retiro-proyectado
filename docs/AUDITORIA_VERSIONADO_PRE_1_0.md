# Auditoría de versionado pre-1.0

**Proyecto:** Mi Retiro Proyectado  
**Bloque:** VER.2 — reconciliación de revisiones pre-1.0  
**Fecha:** 2026-08-21  
**Base auditada:** `main` en `7037addd44253e528c77460b678d2b3ccd540dd5`  
**Estado:** auditoría cerrada; implementación de la nueva política pendiente de gate

## 1. Objetivo

Reconstruir la secuencia real de estados aceptados del proyecto antes de continuar con DEV.2, sin convertir commits administrativos en revisiones, sin ocultar subfases históricas y sin reescribir tags ya publicados.

La auditoría parte de Git como evidencia primaria y cruza `RELEASES.md`, `CHANGELOG.md`, `docs/REGISTRO_CAMBIOS_HISTORICO.md`, bitácoras UX, auditorías de cierre, Pull Requests, gates de pruebas y decisiones ADR.

## 2. Problema detectado

La política anterior `0.0.N-beta` identificaba hitos formales, pero no permitía expresar de forma estable las revisiones internas aceptadas entre releases. Un primer intento de reconciliación hacia `0.0.30-beta` trató cada bloque UX posterior a PLAN.1 como una beta consecutiva. Una auditoría posterior intentó reconstruir un contador global de 163 revisiones, pero mezcló estados aceptados con commits `feat/test/docs`, checkpoints todavía pendientes de validación manual y candidatos locales.

Ambos enfoques se descartan. Ninguno llegó a `main`.

## 3. Regla contable definitiva

Una entrada incrementa el contador global únicamente cuando representa un **estado aceptado y auditable**.

Se aplican estas reglas:

1. Los 21 estados retrospectivos reconstruidos por GOV.1.1 (`0.0.1-beta` a `0.0.21-beta`) cuentan una vez cada uno. Los 80 commits que contienen no se vuelven a contar individualmente.
2. Una revisión interna cuenta cuando la evidencia la describe como cerrada, completada o validada y el proyecto avanza desde ese estado.
3. Un candidato explícitamente pendiente de validación, PR, CI, tag o revisión manual no cuenta por sí solo.
4. Un intento que falla su gate no consume número. La corrección conserva la identidad de la revisión hasta alcanzar aceptación.
5. Los commits lógicos `feat`, `test` y `docs` que materializan una misma revisión no son revisiones independientes.
6. PR, squash, CI y tag son evidencia de integración/cierre; no agregan otra revisión si representan el mismo estado.
7. Mantenimiento absorbido dentro de un bloque no suma una revisión salvo que haya sido declarado como checkpoint/hito independiente.
8. La documentación histórica conserva sus identificadores originales. No se inventan retrospectivamente nombres R que nunca existieron.
9. Los tags publicados permanecen inmutables y conservan su numeración histórica.

## 4. Resultado global

La base `7037addd` contiene **57 estados aceptados** según la regla anterior.

| Rango global | Alcance | Estados que cuentan |
|---|---|---:|
| G001–G021 | Estados retrospectivos `0.0.1-beta`–`0.0.21-beta` | 21 |
| G022 | GOV.1.2 — gobierno y primera versión formal | 1 |
| G023–G026 | GOV.1.3 R1–R4 | 4 |
| G027 | Prebloque transversal de firma e integridad Git/GitHub | 1 |
| G028 | GOV.1.4 — Developer Diagnostics | 1 |
| G029 | GOV.1.5 — seguridad, privacidad y transparencia | 1 |
| G030 | GOV.1.6 — controles GitHub | 1 |
| G031 | GOV.1.7 — licencia y distribución | 1 |
| G032 | GOV.1.8 — cierre integral de GOV.1 | 1 |
| G033–G041 | UX.4.6e — R1–R8 y cierre R9.2 | 9 |
| G042–G050 | PLAN.1 — R1, R2A, R2B1, R2B2, R2C, R3A, R3B1, R3B2 y R4.2 | 9 |
| G051–G053 | UX.4.6f — R1/R1.1 aceptadas en conjunto, R2 y cierre/hardening final | 3 |
| G054 | UX.4.6g — cierre del Paso 5 | 1 |
| G055–G056 | UX.4.6h — R1.2 aceptada y R1.3/cierre | 2 |
| G057 | UX.4.6i — R1.4/cierre | 1 |
| **Total** |  | **57** |

El detalle fila por fila se conserva en `docs/LEDGER_REVISIONES_PRE_1_0.md`.

## 5. Casos históricos que no se vuelven a contar

### UX.2.1

UX.2.1 existió como estabilización visual transversal: tema Oscuro más profundo, Alto contraste negro/blanco, tokens semánticos y remates de superficies/textos. La fase es parte real de la historia, pero no existe evidencia suficiente para asignarle un estado retrospectivo adicional separado de la reconstrucción GOV.1.1. Se documenta, pero **no incrementa de nuevo** el contador.

### UX.4.6a, UX.4.6b, UX.4.6c y UX.4.6d

Sus revisiones internas permanecen en las bitácoras históricas. El contador no suma cada R porque sus cierres aceptados ya están representados por G018, G019, G020 y G021 respectivamente:

- UX.4.6a culminó en el cierre validado de `0.0.18-beta`;
- UX.4.6b culminó en R4 y `0.0.19-beta`;
- UX.4.6c culminó en R3 y `0.0.20-beta`;
- UX.4.6d culminó inequívocamente en R23 y `0.0.21-beta`, con 396 pruebas en `OK`.

Contar además todos sus commits o revisiones intermedias duplicaría el mismo tramo histórico.

### GOV.1.1

GOV.1.1 reconstruyó y clasificó los 21 estados preexistentes. No crea G022 adicional: su resultado está representado por G001–G021. La primera versión formal nueva es GOV.1.2.

### Prebloque de firma e integridad

Los 23/23 tags auditados, reemisiones autorizadas, rulesets, PR de configuración, actualización controlada de `pypdf` y demás operaciones son evidencia interna de un único prebloque cerrado: G027.

### GOV.1.5 R1/R2 y hotfix de licencia

GOV.1.5 R1/R2 fueron incrementos internos que desembocaron en el cierre R3/PR #14; la evidencia de cierre independiente corresponde al bloque GOV.1.5 completo, G029. El hotfix de saltos de línea de licencia forma parte del cierre de GOV.1.7 y no crea otro estado.

### Mantenimiento post-GOV.1

La auditoría/saneamiento del repositorio posterior a `v0.0.24-beta` fue mantenimiento documental. No tuvo versión/tag propio y no se declara revisión independiente.

### UX.4.6e

El checkpoint de identidad pública pre-R8, R8.1 y R9.1 se conservan como evidencia. No incrementan el contador: el checkpoint pre-R8 fue explícitamente intermedio; R8.1 requirió hotfixes antes del cierre R8; R9.1 fue candidato local antes del cierre formal R9.2.

### PLAN.1

R4.1 fue candidato local de `0.0.26-beta`; el estado aceptado que incrementa el contador es R4.2 después de PR/CI, corrección del `SyntaxWarning`, revalidación y tag. PR #25 fue reconciliación documental post-tag y no agrega revisión.

### UX.4.6f

R1 no se cuenta separado de R1.1 porque ambas fueron aceptadas e integradas conjuntamente por PR #28 tras la validación manual. El mantenimiento de dependencias PR #29 fue mantenimiento post-R1, no una revisión UX independiente. R2 sí constituye un estado aceptado distinto, y el cierre/hardening posterior con gate `pre-commit` constituye otro estado material G053.

### UX.4.6g

R1.2, R1.3, R1.4, R1.4.2 y R1.4.3 son refinamientos internos preservados en la historia, pero el único cierre formal autónomo demostrado es R1/PR #32: G054.

### UX.4.6h

El primer candidato R1 falló por tres regresiones de gobierno/documentación. R1.1 corrige ese candidato, pero no se trata como cierre autónomo. R1.2 sí fue aceptada visualmente antes de cambiar el contrato de impresión; R1.3 crea el informe A4 independiente y cierra el bloque.

### UX.4.6i

La auditoría canónica documenta R1 → R1.2 → R1.3 → R1.4. No existe una sección, gate ni artefacto independiente que demuestre R1.1. Las referencias agregadas a `R1.1` en documentación viva son inconsistencias que VER.2 debe corregir. R1–R1.3 fueron refinamientos sucesivos; R1.4 es el cierre aceptado G057 con 841 pruebas.

## 6. Identificador revision-aware propuesto

La nueva familia beta usa:

```text
0.GG.RR.EE-beta
```

Donde:

- `G = revisión global aceptada`;
- `GG = G // 100`;
- `RR = G % 100`, siempre con dos dígitos;
- `EE = ordinal aceptado dentro del bloque/revisión funcional vigente`, con dos dígitos.

Ejemplos:

```text
G001, E01 -> 0.0.01.01-beta
G057, E01 -> 0.0.57.01-beta
G100, E03 -> 0.1.00.03-beta
G425, E12 -> 0.4.25.12-beta
```

Estos identificadores permiten auditar el ledger. **No renombran ni reemplazan retrospectivamente los tags históricos.**

La base actual `7037addd` corresponde conceptualmente a G057/E01. Si VER.2 R1 supera su gate y se integra, será el siguiente estado aceptado:

```text
G058 / E01 -> 0.0.58.01-beta
```

Un intento fallido de VER.2 R1 no consume G058.

## 7. Transición a versión oficial

PLAN.1 permanece vigente en este punto: la primera versión oficial objetivo sigue siendo:

```text
1.0.0.0
Build 000001
```

El cambio de familia beta no modifica el esquema oficial de cuatro componentes ni la independencia del Build.

## 8. Criterio de cierre de VER.2

Antes de aceptar G058 deben quedar completados:

- política `VERSIONING.md` revision-aware;
- validador de versión compatible con legacy histórico, nueva beta y versión oficial;
- ledger auditable y regresión automática contra deriva;
- corrección de referencias falsas/ambiguas de UX.4.6i R1.1;
- separación entre versión actual y versión histórica de revisión documental;
- README, ROADMAP, RELEASES, CHANGELOG, índice y plan maestro coherentes;
- suite completa, `pip check`, `compileall`, sintaxis JavaScript y `git diff --check` limpios;
- PR y CI requeridos en verde.

Solo después de ese cierre DEV.2 vuelve a ser el bloque funcional activo.