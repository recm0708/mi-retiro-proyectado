# Reconstrucción del CHANGELOG histórico — DOC.2 R1

**Estado:** candidato local; pendiente de gate, commit firmado, PR/CI y merge
**Versión vigente durante la revisión:** `0.1.10.01-beta` — G110/E01
**Candidato reservado:** G111/E01 (`0.1.11.01-beta`) — **no consumido**
**Clasificación:** Documentación / Auditoría / Historial
**Fecha:** 2026-08-26

## Objetivo

Reconstruir de forma detallada y auditable las entradas `0.0.1-beta`–`0.0.21-beta` de `CHANGELOG.md` sin inventar características, fechas, pruebas, tags o estados que no estén respaldados por el repositorio.

## Fuentes

La reconstrucción usa, en este orden:

1. historial Git real;
2. rangos y conteos canónicos de `RELEASES.md`;
3. `docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md`;
4. snapshots históricos de `CHANGELOG.md` conservados por Git;
5. documentación, ADR y pruebas presentes en los rangos cuando sirven de contexto.

Git continúa siendo la evidencia primaria.

## Método

Para cada estado retrospectivo se verifica el tag, el commit de cierre, la continuidad respecto del estado anterior y el número esperado de commits. Los sujetos se conservan literalmente y se agrupan solo por el prefijo convencional del commit (`feat`, `fix`, `docs`, `test`, etc.).

La clasificación no cambia el significado histórico del commit. Los mensajes atípicos se conservan como `Otros cambios`.

## Matriz de control

| Versión | Fecha | Rango Git | Commits | Hito |
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

**Resultado:** 21 estados y **80 commits únicos**.

## Naturaleza retrospectiva

`0.0.1-beta`–`0.0.21-beta` no fueron versiones publicadas en sus fechas históricas. GOV.1.1 asignó esos estados retrospectivamente y la migración criptográfica del 2026-08-17 materializó sus tags sin reescribir commits.

El 2026-08-26 se completó además un backfill administrativo de GitHub Releases. El repositorio pasó a tener **29 tags formales ↔ 29 GitHub Releases**. Esos objetos Release retrospectivos no cambian la fecha histórica del hito, el commit objetivo ni la firma de los tags.

## Anomalía del commit raíz

El commit raíz `a0a9e09` conserva el mensaje `tipo: descripción del cambio`. DOC.2 no lo corrige ni le atribuye una intención no demostrada; lo registra como anomalía histórica.

## Artefactos

- `CHANGELOG.md` — reconstrucción legible detallada;
- `data/doc2-legacy-changelog-evidence.json` — evidencia machine-readable de los 80 commits;
- `tests/test_doc2_r1_changelog_reconstruction.py` — regresiones de integridad;
- documentación viva — sincronización del estado G110 y de Releases.

## Límites

DOC.2 R1 no:

- cambia `VERSION`;
- modifica el ledger aceptado;
- consume G111 antes del merge;
- cambia código de aplicación, motores o normativa;
- mueve/recrea tags;
- convierte la fecha administrativa de un Release retrospectivo en fecha histórica.

## Gate de aceptación

Antes de declarar DOC.2 cerrado:

1. evidencia estructurada: 21/21 estados y 80/80 commits;
2. regresiones DOC.2 en `OK`;
3. suite completa en `OK`;
4. `pip check`;
5. auditoría Markdown;
6. compilación Python;
7. sintaxis JavaScript;
8. `git diff --check`;
9. commit firmado;
10. PR/CI y merge;
11. revalidación post-merge.

Solo después de esa aceptación podrá G111/E01 materializarse en `VERSION`.
