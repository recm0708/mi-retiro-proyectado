# Registro de versiones y estados del proyecto

**Fecha de reconstrucción histórica:** 2026-08-17  
**Fuente:** historial Git de `recm0708/calculadora-pension-css`

## 1. Naturaleza del registro

Las versiones `0.0.1-beta` a `0.0.21-beta` fueron asignadas retrospectivamente en GOV.1.1 para organizar estados funcionales que ya existían en Git. No fueron tags ni GitHub Releases publicados en sus fechas originales.

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
- regresiones para impedir divergencias entre archivo canónico, FastAPI y footer.
- validación final del hito con compilación Python, JavaScript válido, `git diff --check` limpio y **403 pruebas automatizadas en OK**;

El tag `v0.0.22-beta` se crea únicamente después de validar y confirmar el commit de cierre de GOV.1.2.

## 5. Próxima línea pública prevista

La primera beta pública objetivo mantiene la familia:

```text
0.1.0-beta.1
```

Su publicación depende de los criterios pre-beta documentados; no se deriva automáticamente por terminar GOV.1.
