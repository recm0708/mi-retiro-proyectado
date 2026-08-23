# Registro histórico de cambios

**Clasificación:** Histórico / Auditoría
**Fuente primaria:** historial Git
**Fecha de reconstrucción inicial:** 2026-08-17
**Versión formal vigente al crear este registro:** `0.0.22-beta`

Este documento ofrece un mapa cronológico legible de la evolución del proyecto. No sustituye `RELEASES.md`, el changelog ni los commits.

## 1. Regla de interpretación

Las versiones `0.0.1-beta` a `0.0.21-beta` fueron asignadas retrospectivamente durante GOV.1.1. Sirven para agrupar estados reales del repositorio, pero no fueron tags publicados en sus fechas originales.

La migración criptográfica posterior permitió materializarlas como tags retrospectivos firmados sin cambiar los commits ni la semántica histórica.

El 2026-08-17 se materializaron efectivamente `v0.0.1-beta` a `v0.0.21-beta`. Esos tags no existieron en sus fechas históricas de cierre. En la misma operación se reemitieron una sola vez `v0.0.22-beta` y `v0.0.23-beta` como objetos firmados, preservando exactamente sus commits objetivo.

`0.0.22-beta` es la primera versión formal adoptada deliberadamente bajo `VERSIONING.md`.

## 2. Cronología retrospectiva

| Versión | Fecha | Rango Git | Hito |
|---|---|---|---|
| `0.0.1-beta` | 2026-08-10 | `a0a9e09` → `13ce028` | Base técnica, FastAPI, primera interfaz, asistente, cuotas, salario y documentación inicial. |
| `0.0.2-beta` | 2026-08-11 | `ae45943` → `eafe54d` | Historial salarial, proyección y línea temporal. |
| `0.0.3-beta` | 2026-08-11 | `a7e1ed4` → `78e5188` | Retiro, precisión monetaria, pruebas y protección de datos de validación. |
| `0.0.4-beta` | 2026-08-11 | `563d6c4` → `2d4dfd0` | Motor SEBD, modalidades e Indemnización por Vejez. |
| `0.0.5-beta` | 2026-08-11 | `d41682c` → `8a7e381` | Motores Mixto y SUCGS. |
| `0.0.6-beta` | 2026-08-11 | `fa5348f` → `e087d6e` | Organización, normativa y casos de validación. |
| `0.0.7-beta` | 2026-08-12 | `c442ec2` → `e956ea9` | Comparador, trazabilidad, resultado unificado y cierre funcional de Fase 6. |
| `0.0.8-beta` | 2026-08-12 | `6d4c2d8` → `d599ee2` | UX.3: responsive y precisión del corte mensual. |
| `0.0.9-beta` | 2026-08-12 | `376a967` → `e6b02dc` | Identidad, temas, accesibilidad y terminología. |
| `0.0.10-beta` | 2026-08-12 | `3f2f5d7` → `8feb682` | Mantenimiento técnico de estructura y finales de línea. |
| `0.0.11-beta` | 2026-08-12 | `c2da494` → `1f350f6` | UX.4.1: accesibilidad y ayudas contextuales. |
| `0.0.12-beta` | 2026-08-12 | `5607cc1` → `6e6b33b` | UX.4.2: estados activos y selección. |
| `0.0.13-beta` | 2026-08-12 | `b671c9a` → `9f849d0` | UX.4.3: errores, teclado, foco y estabilidad. |
| `0.0.14-beta` | 2026-08-13 | `5ca39ac` → `f4a0d45` | UX.4.4: edad anual, detalle salarial e importación documental. |
| `0.0.15-beta` | 2026-08-13 | `88a1d14` → `3430f2e` | UX.4.5: acreditado frente a proyectado. |
| `0.0.16-beta` | 2026-08-13 | `338db37` → `6f138da` | Hardening, privacidad, E2E, CI y Dependabot. |
| `0.0.17-beta` | 2026-08-13 | `488aff5` → `e55190b` | Dependencias reproducibles pre-beta. |
| `0.0.18-beta` | 2026-08-13 | `429201a` → `11aefca` | UX.4.6a: rediseño visual integral. |
| `0.0.19-beta` | 2026-08-13 | `e6c2310` → `83a67ed` | UX.4.6b: Paso 1, privacidad e importación. |
| `0.0.20-beta` | 2026-08-13 | `e80d15e` → `2a69fb8` | UX.4.6c: Paso 2 y cuotas. |
| `0.0.21-beta` | 2026-08-17 | `05232df` → `7941f58` | UX.4.6d: Paso 3, Ficha Digital e integración Pasos 1–3. |

Total reconstruido en GOV.1.1: **80 commits en 21 estados documentales**.

## 3. Primera versión formal

### `0.0.22-beta` — 2026-08-17

GOV.1.2 introdujo:

- gobierno formal;
- versionado formal;
- `VERSION` como fuente canónica;
- CODEOWNERS;
- registro de releases;
- regresiones de coherencia de versión.

Tag publicado:

```text
v0.0.22-beta
```

La validación registrada para el cierre fue de 403 pruebas automatizadas en `OK`, además de compilación Python, sintaxis JavaScript y comprobaciones Git.

## 4. Segunda versión formal

### `0.0.23-beta` — 2026-08-17

GOV.1.3 cerró la reorganización y alineación integral de documentación mediante cuatro revisiones:

- R1 — estructura, documentos de entrada e histórico;
- R2 — contratos técnicos vigentes;
- R3 — normativa, seguridad y privacidad documental;
- R4 — transparencia, auditoría y trazabilidad.

La suite de cierre validó **458 pruebas automatizadas en `OK`**.

Tag formal asociado:

```text
v0.0.23-beta
```

## 5. Migración criptográfica Git — completada

Después del cierre de `0.0.23-beta` se adoptó firma SSH para nuevos commits y tags.

Los tags retrospectivos conservan fecha real de materialización y describen por separado la fecha histórica del hito. `v0.0.22-beta` y `v0.0.23-beta` conservaron sus commits objetivo durante la reemisión firmada única. Esa excepción ya fue consumida y los tags publicados son inmutables.

Consultar `MIGRACION_FIRMAS_GIT_2026-08-17.md`.

## 6. Bitácoras UX preservadas

La evolución detallada de UX.4.6 se conserva en:

- `archive/ux/UX_4_6A_REDISENO_VISUAL.md`;
- `archive/ux/UX_4_6B_PASO1_DATOS_PERSONALES.md`;
- `archive/ux/UX_4_6C_PASO2_CUOTAS.md`;
- `archive/ux/UX_4_6D_PASO3_HISTORIAL.md`.

Es normal que estos documentos contengan estados intermedios contradictorios con el estado final: esa contradicción forma parte de la secuencia histórica.

## 7. Programa GOV.1

- GOV.1.1 — reconstrucción histórica;
- GOV.1.2 — gobierno y versionado;
- GOV.1.3 — reorganización y auditoría documental — cerrada en `0.0.23-beta`;
- GOV.1.4 — observabilidad y Developer Diagnostics;
- GOV.1.5 — seguridad, privacidad y transparencia;
- GOV.1.6 — controles GitHub;
- GOV.1.7 — licencia;
- GOV.1.8 — auditoría final y cierre.

GOV.1.4 a GOV.1.8 quedaron cerrados formalmente el 2026-08-18 y se materializaron conjuntamente en `0.0.24-beta`.

## 8. Tercera versión formal

### `0.0.24-beta` — 2026-08-18

Esta versión cerró integralmente GOV.1 e incorporó, desde la base `0.0.23-beta`:

- firma e integridad Git/GitHub;
- Developer Diagnostics;
- seguridad, privacidad, threat model y procedimientos;
- controles GitHub y auditoría automática;
- licencia propietaria pre-beta y avisos de terceros;
- auditoría final GOV.1.8 y reanudación de UX.4.6e.

La validación final registró **540 pruebas automatizadas en `OK`**, compilación Python correcta, sintaxis JavaScript correcta, `git diff --check` limpio y los checks remotos requeridos en verde.

Tag formal asociado:

```text
v0.0.24-beta
```

El tag es anotado y firmado y apunta al commit de cierre `653900cebd84019fbbaa3ff3cfd91536ccab76eb`. La auditoría post-GOV.1 verificó 24/24 tags con firma SSH válida sin reescribir commits históricos.

## 9. Fuentes de auditoría

Orden recomendado:

1. historial Git;
2. `RELEASES.md`;
3. `CHANGELOG.md`;
4. `docs/DECISIONES.md`;
5. este registro;
6. `docs/archive/`;
7. pruebas y resultados de CI asociados a cada cierre.
