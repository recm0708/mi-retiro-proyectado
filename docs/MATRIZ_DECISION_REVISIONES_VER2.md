# VER.2 — Matriz de decisión de revisiones aceptadas

**Proyecto:** Mi Retiro Proyectado  
**Base auditada:** `main` en `7037addd44253e528c77460b678d2b3ccd540dd5`  
**Rama:** `chore/ver2-revision-ledger`  
**Estado:** EN CURSO — esta matriz prevalece sobre los conteos provisionales anteriores mientras se resuelven los casos ambiguos.

## 1. Regla de decisión

Una revisión consume contador global cuando existe evidencia suficiente de un **estado materialmente distinto y aceptado**. La aceptación puede demostrarse mediante gate técnico satisfactorio, validación manual explícita, integración controlada o combinación de esas señales.

No se cuenta otra vez el mismo estado por separar implementación, pruebas y documentación en varios commits. Tampoco se cuentan candidatos fallidos, cambios que seguían expresamente pendientes de validación o operaciones de tag/squash que no alteran materialmente el estado ya aceptado.

Los mantenimientos técnicos, de seguridad, dependencias, gobierno o documentación **sí pueden contar** cuando producen un estado independiente, validado y aceptado. No es requisito que tengan una etiqueta `R1/R2`; tampoco basta con que exista un PR o un commit.

## 2. Estados históricos hasta `0.0.21-beta`

| Estado | Cuenta | Motivo |
|---|---|---|
| Estados retrospectivos `0.0.1-beta`–`0.0.21-beta` | SÍ, 21 estados | GOV.1.1 reconstruyó 80 commits en 21 snapshots históricos; cada snapshot ya representa su unidad contable legado. |
| UX.2.1 | NO adicional | Subfase real incluida en el rango histórico de `0.0.9-beta`; crear otra fila duplicaría el mismo snapshot. Debe aparecer como subfase de ese estado. |
| UX.4.6a revisiones internas previas al cierre | NO adicional | La bitácora conserva iteraciones, pero el estado inequívocamente aceptado es el cierre con 198 pruebas. |
| UX.4.6b R1–R3 | NO adicional por ahora | R4 es el cierre demostrado con 233 pruebas y validación PC/laptop/CI. No se ha demostrado un snapshot aceptado independiente para cada iteración anterior. |
| UX.4.6c R1–R2 | NO adicional | R3 es el cierre demostrado con 253 pruebas y validación visual; R1/R2 fueron refinamientos conducentes al mismo cierre. |
| UX.4.6d R1–R22 | NO adicional | La bitácora repite que la validación integral seguía pendiente. R23 es el cierre inequívoco con 396 pruebas y recorrido Pasos 1–3 aceptado. |

## 3. GOV.1.2 y GOV.1.3

| Estado | Cuenta | Evidencia |
|---|---|---|
| GOV.1.2 — gobierno/versionado formal | SÍ | `0.0.22-beta`, 403 pruebas y tag formal. Los commits de implementación/documentación son una misma revisión. |
| GOV.1.3 R1 | SÍ | 411 pruebas / progreso explícito a R2. |
| GOV.1.3 R2 | SÍ | 423 pruebas / cierre propio. |
| GOV.1.3 R3 | SÍ | 438 pruebas / cierre propio. |
| GOV.1.3 R4 | SÍ | 458 pruebas / cierre de GOV.1.3 y `0.0.23-beta`. |

## 4. Prebloque transversal de firma e integridad Git/GitHub

La primera pasada comprimió todo el prebloque en una sola fila. La segunda pasada confirma varios estados materiales e integrados consecutivamente.

| Estado | Cuenta | Evidencia |
|---|---|---|
| Materialización criptográfica y cierre de 23/23 tags | SÍ | commit `685d056…`; 23/23 firmas/objetos/targets verificados y primer commit nuevo `Verified`. |
| CI v7 + rulesets/protecciones GitHub | SÍ | PR #9 integrado; 470/470 pruebas; compilación, JS y `diff --check` limpios. |
| Corrección de rutas PowerShell/caracteres de control | SÍ | PR #10 integrado después del estado #9; añade regresión específica y conserva 470/470. Es mantenimiento posterior aceptado, no arreglo previo a la aceptación de #9. |
| Actualización controlada `pypdf 6.15.0` | SÍ | PR #11 integrado; 474/474, `pip check`, importadores y contratos de terceros sincronizados. |
| Cierre formal del prebloque | SÍ | PR #12 integrado; 474/474, revisión remota final y 0 PR pendientes. |

**Decisión:** el prebloque aporta **cinco estados aceptados**, no uno.

## 5. GOV.1.4–GOV.1.8 y mantenimientos asociados

| Estado | Cuenta | Evidencia |
|---|---|---|
| GOV.1.4 — Developer Diagnostics | SÍ | 487 pruebas, integración y cierre. |
| GOV.1.5 R1 — modelo de amenazas | SÍ | documento declara cierre original R1; 7 regresiones específicas. |
| GOV.1.5 R2 — derechos/incidentes | SÍ | documentos declaran cierre original R2; 8 regresiones adicionales; suite 502 antes de R3. |
| GOV.1.5 R3 — cierre seguridad/privacidad/transparencia | SÍ | PR #14, 512 pruebas, bloque cerrado. |
| GOV.1.6 — controles GitHub | SÍ | 522 pruebas antes de GOV.1.7; estado diferenciado aunque PR #15 integre más de un bloque. |
| GOV.1.7 — licencia/distribución | SÍ | 530 pruebas; estado diferenciado. |
| Hotfix de formato de licencia | SÍ | PR #16 fue integrado **después** del estado GOV.1.7; corrigió documentos y endureció la regresión con 530/530. Es mantenimiento aceptado posterior, no candidato fallido previo al merge. |
| GOV.1.8 — cierre integral GOV.1 | SÍ | PR #17; 540 pruebas; `v0.0.24-beta`. |
| Saneamiento post-GOV.1 | SÍ | PR #18 integrado sobre el cierre GOV.1; 30 archivos, 540/540, auditoría del repositorio, soporte/código de conducta y configuración pública. Es un hito documental/de gobierno independiente. |

## 6. UX.4.6e

| Estado | Cuenta | Evidencia / decisión |
|---|---|---|
| R1 — auditoría integral y patrón documental | SÍ | conversación de desarrollo confirma R1 completada y avance a R2. |
| R2 | SÍ | 550 pruebas, compilación/JS/diff limpios. |
| R3 | SÍ | 558 pruebas. |
| R4 | SÍ | 566 pruebas. |
| R5 | SÍ | 576 pruebas. |
| R6 | SÍ | 586 pruebas. |
| R7 | SÍ | 598 pruebas. |
| PR #19 — checkpoint técnico pre-R8 | EN REVISIÓN | Fue integrado con 604/604 y cambios materiales, pero se declaró expresamente checkpoint previo a R8. Debe decidirse si el contador revision-aware incluye checkpoints aceptados de `main` aunque no cierren una R. |
| PR #20 — identidad visual/publicación pre-R8 | EN REVISIÓN | Hito independiente, integrado y validado con 624 pruebas; no cerró R8. Puede corresponder a mantenimiento transversal aceptado. |
| R8.1 | NO | Estado intermedio que todavía presentó defectos de `MutationObserver`/checkboxes. |
| R8.2 / R8 funcional | SÍ | 644 pruebas y validación funcional satisfactoria; la documentación posterior elevó el gate a 652 sin constituir por sí sola una nueva R. |
| R9.1 / R9.2 | SÍ una sola vez | R9.1 alcanzó 660 y preparó candidato; R9.2 materializó PR/CI/tag del mismo cierre. No se duplica el contenido por el proceso remoto. |
| PR #22 — cierre documental final | EN REVISIÓN | Materializa la evidencia post-merge y release sin runtime. Se decidirá con la misma regla aplicada a PR #25 y otros cierres post-tag. |

## 7. PLAN.1

| Estado | Cuenta | Evidencia / decisión |
|---|---|---|
| R1 | SÍ | 665 pruebas. |
| R2A | SÍ | 670. |
| R2B1 | SÍ | 676. |
| R2B2 | SÍ | 684. |
| R2C | SÍ | 689. |
| R3A | SÍ | 695. |
| R3B1 | SÍ | 702. |
| R3B2 | SÍ | 710. |
| R4.1 | EN REVISIÓN | Estado `0.0.26-beta` con 720 pruebas fue integrado mediante PR #23 y existió en `main` antes de detectar `SyntaxWarning`. Puede ser estado aceptado propio. |
| R4.2 / higiene pre-tag | SÍ | PR #24 corrigió el defecto, repitió 720 sin warning y permitió el tag firmado. |
| PR #25 — reconciliación documental post-tag | EN REVISIÓN | 720/720, documentación del tag/cierre y reactivación UX.4.6f. Aplicar la misma regla que PR #22. |

La primera pasada contó nueve estados y absorbió R4.1/R4.2. La evidencia muestra que R4.1 llegó a `main` mediante PR #23 antes del correctivo #24, por lo que no debe descartarse como simple candidato local sin resolver esta distinción.

## 8. UX.4.6f

| Estado | Cuenta | Evidencia / decisión |
|---|---|---|
| R1 | NO adicional | Gate automático 734 superado, pero la validación visual originó R1.1 antes de la aceptación conjunta. |
| R1.1 — aceptación conjunta R1/R1.1 | SÍ | 743/743, validación visual y PR #28. |
| Mantenimiento de dependencias post-R1 | SÍ | PR #29 integrado; `pypdf 6.16.1` + `uvicorn 0.52.3`, 743 pruebas y tres checks; estado técnico independiente. |
| R2 — auditoría lógica/matemática | SÍ | PR #30; 756/756; cierre funcional del Paso 4. |
| Cierre/hardening `pre-commit` | SÍ | PR #31 añade un gate reproducible, cinco regresiones y llega a 762/762. Aunque parte del PR es cierre documental, el mecanismo `pre-commit` es un cambio técnico material posterior a R2. |

## 9. UX.4.6g

| Estado | Cuenta | Evidencia / decisión |
|---|---|---|
| R1 completo / cierre Paso 5 | SÍ | PR #32, 784/784 y validación funcional/visual. |
| R1.2 / R1.3 / R1.4 / R1.4.2 / R1.4.3 | NO adicional por ahora | Son refinamientos documentados dentro del R1 consolidado. Falta evidencia independiente de aceptación entre cada estado antes de avanzar. Si aparece, se reabrirá la decisión. |

## 10. UX.4.6h

| Estado | Cuenta | Evidencia |
|---|---|---|
| R1 | NO | Candidato que reveló tres regresiones; fue sustituido antes de aceptación. |
| R1.1 | SÍ | Corrección aceptada que permitió continuar. |
| R1.2 | SÍ | Revisión aceptada de claridad/jerarquía. |
| R1.3 | SÍ | Informe A4 y cierre; 812 pruebas / PR #33. |

## 11. UX.4.6i

| Estado | Cuenta | Evidencia / decisión |
|---|---|---|
| R1 | SÍ | Gate 826 después del hotfix documental; estado funcional diferenciado. |
| supuesto R1.1 | NO | No existe como revisión independiente; corresponde al hotfix documental del gate de R1. |
| R1.2 | EN REVISIÓN | Changelog registra cambios y objetivo 832; todavía falta evidencia inequívoca de aceptación independiente. |
| R1.3 | EN REVISIÓN | Changelog registra cambios y objetivo 840; todavía falta evidencia inequívoca de aceptación independiente. |
| R1.4 | SÍ | cierre PR #34, 841/841, Python/JS/diff correctos y transición a DEV.2. |

## 12. Consecuencia para los conteos provisionales

`G057` fue descartado. El posterior `G060` también debe considerarse **superado como cifra provisional**, porque todavía comprimía cinco estados del prebloque en uno y omitía mantenimientos aceptados como PR #16, PR #18 y PR #29; además había excluido el hardening técnico de PR #31.

No se publica un nuevo `Gn` hasta resolver las filas `EN REVISIÓN` con un criterio idéntico para checkpoints, cierres post-tag y refinamientos internos.

## 13. Próximo paso de auditoría

1. resolver PR #19/#20/#22 y PLAN.1 R4.1/PR #25 con una regla transversal de «estado aceptado en main»;
2. agotar la búsqueda de aceptación independiente de UX.4.6g refinamientos y UX.4.6i R1.2/R1.3;
3. reconstruir el contador completo desde G001 sin huecos;
4. generar ledger Markdown + JSON machine-readable;
5. implementar validador y regresiones de versionado;
6. solo entonces definir el Global del cierre VER.2 y la versión candidata correspondiente.
