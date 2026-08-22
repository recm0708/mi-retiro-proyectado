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
| UX.2.1 | `tests/test_estabilizacion_visual.py` se incorporó dentro del rango histórico de `0.0.9-beta` y se identifica expresamente como regresión de UX.2.1; ese mismo rango agrupa identidad, temas, accesibilidad y terminología | fase histórica real, pero no existe un snapshot aceptado separado fuera del rango ya asignado a `0.0.9-beta` | **ABSORBIDA EN G009; NO SUMA OTRO GLOBAL** |
| UX.4.6a | `429201a` → `11aefca`; bitácora `UX_4_6A_REDISENO_VISUAL.md` | PC/laptop aceptado; 198 pruebas; `compileall`, JS y `git diff --check` en verde | CIERRE REAL CONFIRMADO |
| UX.4.6b | `e6c2310` → `83a67ed`; bitácora `UX_4_6B_PASO1_DATOS_PERSONALES.md` | R4; PC/laptop aceptado; 233 pruebas; CI Python 3.13/3.14 en verde | CIERRE REAL CONFIRMADO |
| UX.4.6c | `e80d15e` → `2a69fb8`; bitácora `UX_4_6C_PASO2_CUOTAS.md` | R3; PC/laptop aceptado; 253 pruebas | CIERRE REAL CONFIRMADO |
| UX.4.6d | `05232df` → `7941f58`; bitácora `UX_4_6D_PASO3_HISTORIAL.md` | R23; 396 pruebas; Pasos 1–3 integrados y acceso correcto a Paso 4 | CIERRE REAL CONFIRMADO |

La reconstrucción histórica GOV.1.1 ya asignó `0.0.18-beta`, `0.0.19-beta`, `0.0.20-beta` y `0.0.21-beta` a los cuatro cierres UX.4.6a–d. La auditoría debe evitar contarlos dos veces, pero también debe conservar explícitamente sus nombres, revisiones finales y gates.

### Decisión UX.2.1

UX.2.1 no se elimina ni se oculta. Debe aparecer como subfase histórica de G009. La evidencia Git muestra que sus regresiones se incorporaron en la misma secuencia `376a967` → `74fbd29` → `7ed97ff` → `e6b02dc` ya reconstruida como `0.0.9-beta`. Crear un Global adicional duplicaría un mismo estado retrospectivo.

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

La primera pasada creó un Global adicional para PR #31. La evidencia de la segunda pasada favorece **no contarlo como una nueva revisión UX.4.6f**: R2 ya había sido aceptada funcionalmente y declarada cerrada; PR #31 materializa hardening y cierre documental posterior sin crear R nueva. Esta decisión se mantendrá salvo que la auditoría transversal obligue a contar como Global todo hito técnico independiente, criterio que actualmente se descarta por inflar el contador con mantenimiento.

## 6. GOV.1.5 — error concreto de la primera pasada

La primera pasada contó GOV.1.5 únicamente como un cierre global de bloque. La documentación vigente demuestra que R1 y R2 no son nombres retrospectivos inventados:

- `MODELO_AMENAZAS.md` declara **GOV.1.5 R1**, con **fecha de cierre original 2026-08-17**;
- `PROCEDIMIENTO_DERECHOS_TITULAR.md` declara **GOV.1.5 R2**, vigente como procedimiento interno, con **fecha de cierre original 2026-08-18**;
- `VALIDACION.md` registra 7 regresiones de R1, 8 de R2 y una suite validada de 502 pruebas antes de R3;
- PR #14 integra R3 y cierra el bloque completo con 512 pruebas.

Por coherencia con GOV.1.3 y con las revisiones explícitas aceptadas de UX.4.6e/PLAN.1, **R1 y R2 deben conservar Globals propios** junto con R3/cierre. Este hallazgo invalida el total 57 aun si no apareciera ningún otro ajuste.

La numeración exacta se recalculará solo al terminar todos los bloques para evitar renumerar el ledger varias veces durante la auditoría.

## 7. PLAN.1 — criterio de aceptación confirmado, cierre sin doble conteo

`AUDITORIA_PLAN1_R4_2026-08-20.md` registra gates locales diferenciados para R1, R2A, R2B1, R2B2, R2C, R3A, R3B1 y R3B2: 665, 670, 676, 684, 689, 695, 702 y 710 pruebas respectivamente, con `VERSION` todavía en `0.0.25-beta` hasta R4.

R4.1 promueve el candidato `0.0.26-beta` con 720 pruebas. R4.2 no introduce una nueva revisión funcional de PLAN.1: es el gate remoto/higiene pre-tag que corrige el `SyntaxWarning`, repite las mismas 720 pruebas y permite crear el tag firmado. PR #25 es reconciliación documental post-tag y no suma revisión.

Consecuencia: las subrevisiones explícitas y aceptadas R1–R3B2 pueden conservar identidad propia; el cierre R4 se cuenta una sola vez, no como R4.1 + R4.2 + PR #25.

## 8. Pull Requests #1–#8 y mantenimiento Dependabot temprano

La numeración de PR no representa revisiones de producto. La auditoría confirma que los PR tempranos de Dependabot no deben inflar el ledger:

- #1, #2 y #3 fueron propuestas automáticas de `actions/*` y se cerraron sin merge;
- la evidencia de validación del prebloque registra que #7 y #8 fueron sustituidos por cambios controlados del mantenedor;
- #4, #5 y #6 se cerraron sin merge para preservar combinaciones compatibles y el snapshot transitivo reproducible.

Por tanto, estos PR no consumen Globals. La adopción efectiva posterior de Actions v7, `pypdf` y protecciones GitHub se evalúa por el hito aceptado al que pertenecen, no por el número de Pull Request.

## 9. UX.4.6e — R1 sí existió; checkpoints pre-R8 no duplican revisiones

La referencia cruzada con las conversaciones confirma que R1 fue el diagnóstico integral y la definición del patrón documental por tecnología. R1 quedó marcada como completada y se avanzó explícitamente a R2. No se recuperó un número de pruebas propio de R1, por lo que su evidencia es de aceptación/progresión y no de gate numérico independiente.

A partir de R2, `VALIDACION.md` aporta gates diferenciados: R2 550, R3 558, R4 566, R5 576, R6 586, R7 598 y cierre documental de R8 652. La cifra 644 corresponde a R8.1/R8.2 funcional antes del cierre documental; 624 corresponde al checkpoint de identidad/publicación previo a continuar R8. Ninguna de esas cifras intermedias crea por sí sola otra revisión adicional.

R9.1 alcanzó 660 pruebas y promovió el candidato `0.0.25-beta`; R9.2 materializó el cierre remoto/documental del mismo estado. Para evitar doble conteo, R9 consume un solo Global de cierre.

Consecuencia provisional: la estructura de nueve estados de UX.4.6e de la primera pasada —R1, R2, R3, R4, R5, R6, R7, R8 y R9/cierre— se mantiene, pero se corrigen las descripciones y evidencias.

## 10. UX.4.6h — la primera pasada omitió R1.1

La referencia cruzada de las conversaciones establece esta secuencia:

- R1 existió como candidato, pero falló al revelar tres regresiones: **no consume Global**;
- R1.1 fue la corrección que permitió superar ese estado fallido y continuar: **sí es revisión aceptada**;
- R1.2 quedó aceptada;
- R1.3 quedó aceptada y cerró el bloque con 812 pruebas.

Por tanto, UX.4.6h debe aportar **tres** estados aceptados —R1.1, R1.2 y R1.3—, no los dos que aparecen en el ledger de primera pasada. R1 fallida permanece documentada solo como evidencia.

## 11. UX.4.6i — corregir la falsa R1.1 y conservar solo aceptación demostrable

La secuencia histórica demostrable es:

```text
R1 → R1.2 → R1.3 → R1.4
```

No existe una R1.1 independiente: la referencia a R1.1 corresponde a un hotfix documental de dos fallos históricos durante el gate de R1 y no a una revisión diferenciada de UX.4.6i.

R1 llegó a un gate de 826 pruebas después de corregir esos fallos y constituye un estado aceptado. Para R1.2 y R1.3 la documentación describe cambios y objetivos de 832/840 en el changelog, pero la referencia cruzada de conversaciones no recuperó una aceptación verbal o gate intermedio inequívoco separado. R1.4 sí constituye el cierre demostrado: PR #34, 841/841, compilación Python, sintaxis JavaScript y `git diff --check` correctos, seguido de DEV.2.

Aplicando criterio conservador, la segunda pasada cuenta de momento **R1 y R1.4**, no R1.2/R1.3, salvo que aparezca evidencia adicional de aceptación independiente durante el resto de la auditoría.

## 12. Criterio uniforme en consolidación

La segunda pasada no aceptará reglas diferentes según el bloque. La decisión final deberá responder igual para UX, GOV, PLAN y mantenimiento.

Una entrada candidata a Global deberá demostrar como mínimo:

1. identidad de revisión/hito distinguible de su estado anterior;
2. cambio material aceptado, no solo separación de commits por categoría;
3. gate satisfactorio o aceptación manual explícita cuando corresponda;
4. evidencia de que el proyecto avanzó desde ese estado;
5. ausencia de duplicación con PR/squash/tag/cierre documental que materialice el mismo estado.

Reglas derivadas hasta ahora:

- una revisión explícita con cierre/gate propio puede contar aunque posteriormente se integre junto con otras;
- un candidato fallido no cuenta;
- un checkpoint declarado intermedio no cuenta;
- un PR de documentación, tag, squash o higiene que solamente materializa un estado ya aceptado no cuenta de nuevo;
- mantenimiento de dependencias/CI no cuenta por el mero hecho de producir un commit o PR; solo podría contar si fue definido y aceptado como hito transversal autónomo del plan;
- una subfase ya absorbida dentro de un estado retrospectivo no se duplica;
- ante evidencia incompleta se usa el criterio conservador: una revisión nombrada no se cuenta sin aceptación diferenciada demostrable.

## 13. Bloques todavía pendientes antes de fijar el número

Antes de ratificar el último Global deben revisarse de nuevo, con el mismo criterio:

- prebloque de firma/integridad y sus mantenimientos internos, para confirmar que solo consume su cierre transversal;
- confirmación final de GOV.1.5 R1/R2/R3 en la secuencia global;
- confirmación final de UX.4.6e y PLAN.1 contra el ledger recalculado;
- UX.4.6f R1/R1.1/R2 y exclusión definitiva de PR #31;
- UX.4.6g refinamientos posteriores a R1;
- búsqueda residual de evidencia independiente para UX.4.6i R1.2/R1.3;
- recálculo global completo G001→Gn sin huecos ni duplicados.

## 14. Estado operativo

Este archivo es una bitácora de auditoría de trabajo. Cuando termine la segunda pasada:

- `AUDITORIA_VERSIONADO_PRE_1_0.md` se reescribirá con el resultado definitivo;
- `LEDGER_REVISIONES_PRE_1_0.md` se regenerará con una única regla contable;
- se materializará el ledger estructurado en `data/` y su validador;
- se corregirán las regresiones históricas que congelan versiones vigentes;
- se eliminarán referencias a candidatos descartados;
- recién entonces se fijará el siguiente identificador revision-aware.
