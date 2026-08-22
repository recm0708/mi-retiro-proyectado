# VER.2 — Matriz de decisión de revisiones aceptadas

**Proyecto:** Mi Retiro Proyectado  
**Base auditada:** `main` en `7037addd44253e528c77460b678d2b3ccd540dd5`  
**Rama:** `chore/ver2-revision-ledger`  
**Estado:** SEGUNDA PASADA RESUELTA EN LO CONTABLE; pendiente materialización del ledger y gates.

## 1. Regla de decisión

Una revisión consume contador global cuando existe evidencia suficiente de un **estado materialmente distinto y aceptado**. La aceptación puede demostrarse mediante gate técnico satisfactorio, validación manual explícita, integración controlada o combinación de esas señales.

No se cuenta otra vez el mismo estado por separar implementación, pruebas y documentación en varios commits. Tampoco se cuentan candidatos fallidos, cambios que seguían expresamente pendientes de validación o operaciones de tag/squash que no alteran materialmente el estado ya aceptado.

Los mantenimientos técnicos, de seguridad, dependencias, gobierno o documentación **sí cuentan** cuando producen un estado independiente, validado y aceptado. No es requisito que tengan una etiqueta `R1/R2`; tampoco basta con que exista un PR o un commit.

Un checkpoint que solo agrupa revisiones ya contabilizadas o deja explícitamente pendiente la revisión funcional siguiente no suma otra fila. Un hito transversal separado —por ejemplo, identidad oficial/publicación o un mantenimiento de dependencias integrado entre revisiones— sí puede hacerlo si cambia materialmente el estado auditable.

## 2. Estados históricos hasta `0.0.21-beta`

| Estado | Cuenta | Motivo |
|---|---|---|
| Estados retrospectivos `0.0.1-beta`–`0.0.21-beta` | SÍ, 21 estados | GOV.1.1 reconstruyó 80 commits en 21 snapshots históricos; cada snapshot ya representa su unidad contable legado. |
| UX.2.1 | NO adicional | Subfase real incluida en el rango histórico de `0.0.9-beta`; crear otra fila duplicaría el mismo snapshot. Debe aparecer como subfase de ese estado. |
| UX.4.6a revisiones internas previas al cierre | NO adicional | La bitácora conserva iteraciones, pero el estado inequívocamente aceptado es el cierre con 198 pruebas. |
| UX.4.6b R1–R3 | NO adicional | R4 es el cierre demostrado con 233 pruebas y validación PC/laptop/CI. No se demostró aceptación independiente previa equivalente. |
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

La primera pasada comprimió todo el prebloque en una sola fila. La segunda pasada confirma cinco estados materiales e integrados consecutivamente.

| Estado | Cuenta | Evidencia |
|---|---|---|
| Materialización criptográfica y cierre de 23/23 tags | SÍ | commit `685d056…`; 23/23 firmas/objetos/targets verificados y primer commit nuevo `Verified`. |
| CI v7 + rulesets/protecciones GitHub | SÍ | PR #9 integrado; 470/470 pruebas; compilación, JS y `diff --check` limpios. |
| Corrección de rutas PowerShell/caracteres de control | SÍ | PR #10 integrado después del estado #9; añade regresión específica y conserva 470/470. |
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
| Hotfix de formato de licencia | SÍ | PR #16 fue integrado **después** del estado GOV.1.7; corrigió documentos y endureció la regresión con 530/530. |
| GOV.1.8 — cierre integral GOV.1 | SÍ | PR #17; 540 pruebas; `v0.0.24-beta`. |
| Saneamiento post-GOV.1 | SÍ | PR #18 integrado sobre el cierre GOV.1; 30 archivos, 540/540, auditoría del repositorio, soporte/código de conducta y configuración pública. |

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
| PR #19 — checkpoint técnico pre-R8 | NO adicional | Consolida trabajo ya representado por R2–R7 y deja expresamente R8 funcional pendiente. El gate 604 no crea una revisión nueva del producto. |
| Identidad visual oficial + publicación del repositorio / PR #20 | SÍ | Hito transversal independiente: activos oficiales, `brand.css`, favicons/Social Preview, repositorio público y seguridad revalidada; 624 pruebas. No duplica R2–R7 ni R8. |
| R8.1 | NO | Estado intermedio que todavía presentó defectos de `MutationObserver`/checkboxes. |
| R8.2 / R8 funcional | SÍ | 644 pruebas y validación funcional satisfactoria; el posterior cierre documental a 652 materializa la misma R8. |
| R9.1 / R9.2 | SÍ una sola vez | R9.1 alcanzó 660 y dejó el estado candidato; R9.2 materializó PR/CI/tag del mismo cierre. |
| PR #22 — cierre documental final | NO adicional | Registra evidencia post-merge/release de R9 ya contabilizada; no introduce una revisión material nueva. |

**Decisión:** UX.4.6e aporta **diez estados aceptados**: R1–R7, identidad/publicación, R8 y R9/cierre.

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
| R4.1 | SÍ | 720/720, compilación/JS/diff limpios y R4.1 fue declarado cerrado antes de iniciar R4.2; PR #23 materializó ese estado en `main`. |
| R4.2 / higiene pre-tag | SÍ | El post-merge reveló `SyntaxWarning`; PR #24 corrigió ese estado, repitió 720 sin warning y permitió el tag firmado. Es una revisión posterior real, no una mera operación de tag. |
| PR #25 — reconciliación documental post-tag | NO adicional | Registra el tag y el cierre ya materializado por R4.2; no introduce otra revisión independiente. |

**Decisión:** PLAN.1 aporta **diez revisiones aceptadas**.

## 8. UX.4.6f

| Estado | Cuenta | Evidencia / decisión |
|---|---|---|
| R1 | NO adicional | Gate automático 734 superado, pero la validación visual originó R1.1 antes de la aceptación conjunta. |
| R1.1 — aceptación conjunta R1/R1.1 | SÍ | 743/743, validación visual y PR #28. |
| Mantenimiento de dependencias post-R1 | SÍ | PR #29 integrado; `pypdf 6.16.1` + `uvicorn 0.52.3`, 743 pruebas y tres checks. |
| R2 — auditoría lógica/matemática | SÍ | PR #30; 756/756; cierre funcional del Paso 4. |
| Cierre/hardening `pre-commit` | SÍ | PR #31 añade un gate reproducible, cinco regresiones y llega a 762/762. La parte documental no duplica R2, pero el `pre-commit` sí constituye cambio técnico material posterior. |

**Decisión:** UX.4.6f aporta **cuatro estados aceptados**.

## 9. UX.4.6g

| Estado | Cuenta | Evidencia / decisión |
|---|---|---|
| R1 completo / cierre Paso 5 | SÍ | PR #32, 784/784 y validación funcional/visual. |
| R1.2 / R1.3 / R1.4 / R1.4.2 / R1.4.3 | NO adicional | La búsqueda cruzada no recupera aceptación diferenciada antes de la revisión siguiente; el PR #32 las consolida como refinamientos del único R1 aceptado. |

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
| R1.2 | NO adicional | Changelog documenta el refinamiento y objetivo 832, pero la búsqueda cruzada no recupera aceptación independiente antes de R1.3. |
| R1.3 | NO adicional | Changelog documenta el refinamiento y objetivo 840, pero la búsqueda cruzada no recupera aceptación independiente antes de R1.4. |
| R1.4 | SÍ | cierre PR #34, 841/841, Python/JS/diff correctos y transición a DEV.2. |

## 12. Conteo resultante de la segunda pasada

| Tramo | Estados que consumen Global |
|---|---:|
| Legado `0.0.1`–`0.0.21` | 21 |
| GOV.1.2 | 1 |
| GOV.1.3 | 4 |
| Prebloque firma/integridad | 5 |
| GOV.1.4 | 1 |
| GOV.1.5 | 3 |
| GOV.1.6 | 1 |
| GOV.1.7 | 1 |
| Hotfix licencia | 1 |
| GOV.1.8 | 1 |
| Saneamiento post-GOV.1 | 1 |
| UX.4.6e | 10 |
| PLAN.1 | 10 |
| UX.4.6f | 4 |
| UX.4.6g | 1 |
| UX.4.6h | 3 |
| UX.4.6i | 2 |
| **Total aceptado antes de VER.2** | **70** |

El último estado aceptado antes de VER.2 es, por tanto, **G070**.

La secuencia desde G022 queda:

- G022 GOV.1.2;
- G023–G026 GOV.1.3 R1–R4;
- G027–G031 prebloque firma/integridad;
- G032 GOV.1.4;
- G033–G035 GOV.1.5 R1–R3;
- G036 GOV.1.6;
- G037 GOV.1.7;
- G038 hotfix licencia;
- G039 GOV.1.8;
- G040 saneamiento post-GOV.1;
- G041–G050 UX.4.6e;
- G051–G060 PLAN.1;
- G061–G064 UX.4.6f;
- G065 UX.4.6g;
- G066–G068 UX.4.6h;
- G069–G070 UX.4.6i.

## 13. Consecuencia para VER.2

Los conteos G057 y G060 quedan **formalmente superados** por esta segunda pasada.

Si la materialización del ledger, las regresiones, el JSON estructurado y el gate de VER.2 no descubren otra inconsistencia histórica, el cierre aceptado de VER.2 consumirá **G071**. Hasta ese momento `VERSION` no debe tratarse como promovida definitivamente.

## 14. Próximo paso

1. regenerar `LEDGER_REVISIONES_PRE_1_0.md` con G001–G070 y filas de exclusión;
2. crear el ledger machine-readable en `data/`;
3. implementar su validador y regresiones;
4. corregir documentación/regresiones que aún congelen G057/G058 o `0.0.58.01-beta`;
5. definir candidato G071 solo después de que el ledger sea autoconsistente;
6. ejecutar gate completo y CI antes de integrar PR #35.
