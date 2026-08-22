# Ledger de revisiones aceptadas pre-1.0

**Proyecto:** Mi Retiro Proyectado  
**Base auditada:** `7037addd44253e528c77460b678d2b3ccd540dd5`  
**Contador aceptado en la base:** **G070**  
**Siguiente Global disponible si VER.2 supera su gate:** **G071**

Este ledger registra los estados aceptados reconstruidos durante VER.2. La regla contable y las exclusiones se documentan en `MATRIZ_DECISION_REVISIONES_VER2.md` y `AUDITORIA_VERSIONADO_PRE_1_0.md`.

Los identificadores revision-aware son una reconstrucción de auditoría. **No existieron históricamente y no autorizan mover, recrear ni renombrar los tags `v0.0.1-beta`–`v0.0.26-beta`.**

## Convención

```text
0.GG.RR.EE-beta
```

- `G = GG × 100 + RR`;
- `RR` usa dos dígitos (`00`–`99`);
- `EE` es el ordinal del estado aceptado dentro del bloque, con dos dígitos;
- un candidato fallido no consume `G`;
- un PR/commit/tag no suma otra fila si solo materializa el mismo estado;
- un mantenimiento técnico, de seguridad, gobierno, dependencias o documentación puede consumir `G` si crea un estado materialmente distinto, validado y aceptado.

## Ledger G001–G070

| Global | ID revision-aware | Bloque / estado aceptado | Ancla histórica | Evidencia resumida |
|---:|---|---|---|---|
| G001 | `0.0.01.01-beta` | Estado retrospectivo 01 — base técnica | `0.0.1-beta` | GOV.1.1 / `RELEASES.md` |
| G002 | `0.0.02.01-beta` | Estado retrospectivo 02 — historial/proyección | `0.0.2-beta` | GOV.1.1 / `RELEASES.md` |
| G003 | `0.0.03.01-beta` | Estado retrospectivo 03 — retiro/precisión | `0.0.3-beta` | GOV.1.1 / `RELEASES.md` |
| G004 | `0.0.04.01-beta` | Estado retrospectivo 04 — SEBD/modalidades | `0.0.4-beta` | GOV.1.1 / `RELEASES.md` |
| G005 | `0.0.05.01-beta` | Estado retrospectivo 05 — Mixto/SUCGS | `0.0.5-beta` | GOV.1.1 / `RELEASES.md` |
| G006 | `0.0.06.01-beta` | Estado retrospectivo 06 — organización/normativa | `0.0.6-beta` | GOV.1.1 / `RELEASES.md` |
| G007 | `0.0.07.01-beta` | Estado retrospectivo 07 — comparador/trazabilidad | `0.0.7-beta` | GOV.1.1 / `RELEASES.md` |
| G008 | `0.0.08.01-beta` | UX.3 — responsive/corte mensual | `0.0.8-beta` | cierre retrospectivo |
| G009 | `0.0.09.01-beta` | Identidad/temas/accesibilidad, incluida UX.2.1 | `0.0.9-beta` | snapshot legado; UX.2.1 queda absorbida sin duplicación |
| G010 | `0.0.10.01-beta` | Mantenimiento técnico estructural | `0.0.10-beta` | cierre retrospectivo |
| G011 | `0.0.11.01-beta` | UX.4.1 — accesibilidad contextual | `0.0.11-beta` | cierre retrospectivo |
| G012 | `0.0.12.01-beta` | UX.4.2 — estados/selección visual | `0.0.12-beta` | cierre retrospectivo |
| G013 | `0.0.13.01-beta` | UX.4.3 — validación/teclado/estabilidad | `0.0.13-beta` | cierre retrospectivo |
| G014 | `0.0.14.01-beta` | UX.4.4 — edad/detalle/importación | `0.0.14-beta` | cierre retrospectivo |
| G015 | `0.0.15.01-beta` | UX.4.5 — acreditado vs. proyectado | `0.0.15-beta` | cierre retrospectivo |
| G016 | `0.0.16.01-beta` | Hardening PDF/privacidad/E2E/CI | `0.0.16-beta` | cierre retrospectivo |
| G017 | `0.0.17.01-beta` | Dependencias reproducibles | `0.0.17-beta` | cierre retrospectivo |
| G018 | `0.0.18.01-beta` | UX.4.6a — cierre rediseño visual | `0.0.18-beta` | 198 pruebas / cierre PC-laptop |
| G019 | `0.0.19.01-beta` | UX.4.6b — cierre Paso 1 | `0.0.19-beta` | R4 / 233 pruebas |
| G020 | `0.0.20.01-beta` | UX.4.6c — cierre Paso 2 | `0.0.20-beta` | R3 / 253 pruebas |
| G021 | `0.0.21.01-beta` | UX.4.6d — cierre Paso 3 | `0.0.21-beta` | R23 / 396 pruebas |
| G022 | `0.0.22.01-beta` | GOV.1.2 — gobierno y versionado formal | `v0.0.22-beta` | 403 pruebas |
| G023 | `0.0.23.01-beta` | GOV.1.3 R1 — estructura/histórico | base `0.0.22-beta` | 411 pruebas |
| G024 | `0.0.24.02-beta` | GOV.1.3 R2 — documentación técnica | base `0.0.22-beta` | 423 pruebas |
| G025 | `0.0.25.03-beta` | GOV.1.3 R3 — normativa/privacidad | base `0.0.22-beta` | 438 pruebas |
| G026 | `0.0.26.04-beta` | GOV.1.3 R4 — auditoría documental | `v0.0.23-beta` | 458 pruebas |
| G027 | `0.0.27.01-beta` | Integridad R1 — materialización criptográfica de tags | base `0.0.23-beta` | commit `685d056`; 23/23 firmas/objetos/targets |
| G028 | `0.0.28.02-beta` | Integridad R2 — CI v7 y protecciones GitHub | base `0.0.23-beta` | PR #9 / 470 pruebas |
| G029 | `0.0.29.03-beta` | Integridad R3 — corrección rutas PowerShell | base `0.0.23-beta` | PR #10 / 470 pruebas |
| G030 | `0.0.30.04-beta` | Integridad R4 — actualización `pypdf 6.15.0` | base `0.0.23-beta` | PR #11 / 474 pruebas |
| G031 | `0.0.31.05-beta` | Integridad R5 — cierre formal del prebloque | base `0.0.23-beta` | PR #12 / 474 pruebas / 0 PR pendientes |
| G032 | `0.0.32.01-beta` | GOV.1.4 — Developer Diagnostics | base `0.0.23-beta` | 487 pruebas |
| G033 | `0.0.33.01-beta` | GOV.1.5 R1 — modelo de amenazas | base `0.0.23-beta` | 7 regresiones / cierre original R1 |
| G034 | `0.0.34.02-beta` | GOV.1.5 R2 — derechos e incidentes | base `0.0.23-beta` | +8 regresiones / 502 pruebas antes de R3 |
| G035 | `0.0.35.03-beta` | GOV.1.5 R3 — cierre seguridad/privacidad/transparencia | base `0.0.23-beta` | PR #14 / 512 pruebas |
| G036 | `0.0.36.01-beta` | GOV.1.6 — controles GitHub | base `0.0.23-beta` | 522 pruebas |
| G037 | `0.0.37.01-beta` | GOV.1.7 — licencia/distribución | base `0.0.23-beta` | 530 pruebas |
| G038 | `0.0.38.02-beta` | GOV.1.7 — hotfix de formato de licencia | base `0.0.23-beta` | PR #16 / 530 pruebas |
| G039 | `0.0.39.01-beta` | GOV.1.8 — cierre integral GOV.1 | `v0.0.24-beta` | PR #17 / 540 pruebas |
| G040 | `0.0.40.01-beta` | Saneamiento post-GOV.1 | base `0.0.24-beta` | PR #18 / 540 pruebas / auditoría de repositorio |
| G041 | `0.0.41.01-beta` | UX.4.6e R1 — auditoría/patrón documental | base `0.0.24-beta` | R1 completada; avance explícito a R2 |
| G042 | `0.0.42.02-beta` | UX.4.6e R2 — Python/proyección salarial | base `0.0.24-beta` | 550 pruebas |
| G043 | `0.0.43.03-beta` | UX.4.6e R3 — JS/Web Storage | base `0.0.24-beta` | 558 pruebas |
| G044 | `0.0.44.04-beta` | UX.4.6e R4 — runtime/Jinja/CSS | base `0.0.24-beta` | 566 pruebas |
| G045 | `0.0.45.05-beta` | UX.4.6e R5 — coherencia visible/preparación pública | base `0.0.24-beta` | 576 pruebas |
| G046 | `0.0.46.06-beta` | UX.4.6e R6 — renumeración/metadata | base `0.0.24-beta` | 586 pruebas |
| G047 | `0.0.47.07-beta` | UX.4.6e R7 — auditoría transversal | base `0.0.24-beta` | 598 pruebas |
| G048 | `0.0.48.08-beta` | UX.4.6e — identidad visual oficial y publicación | base `0.0.24-beta` | PR #20 / 624 pruebas |
| G049 | `0.0.49.09-beta` | UX.4.6e R8 — validación funcional/procedencia | base `0.0.24-beta` | R8.2 644 / cierre documental 652 |
| G050 | `0.0.50.10-beta` | UX.4.6e R9 — cierre formal | `v0.0.25-beta` | PR #21/#22 / 660 pruebas |
| G051 | `0.0.51.01-beta` | PLAN.1 R1 — política/plan maestro | base `0.0.25-beta` | 665 pruebas |
| G052 | `0.0.52.02-beta` | PLAN.1 R2A | base `0.0.25-beta` | 670 pruebas |
| G053 | `0.0.53.03-beta` | PLAN.1 R2B1 | base `0.0.25-beta` | 676 pruebas |
| G054 | `0.0.54.04-beta` | PLAN.1 R2B2 | base `0.0.25-beta` | 684 pruebas |
| G055 | `0.0.55.05-beta` | PLAN.1 R2C | base `0.0.25-beta` | 689 pruebas |
| G056 | `0.0.56.06-beta` | PLAN.1 R3A | base `0.0.25-beta` | 695 pruebas |
| G057 | `0.0.57.07-beta` | PLAN.1 R3B1 | base `0.0.25-beta` | 702 pruebas |
| G058 | `0.0.58.08-beta` | PLAN.1 R3B2 | base `0.0.25-beta` | 710 pruebas |
| G059 | `0.0.59.09-beta` | PLAN.1 R4.1 — candidato local cerrado | base `0.0.25-beta` | PR #23 / 720 pruebas |
| G060 | `0.0.60.10-beta` | PLAN.1 R4.2 — higiene y cierre formal | `v0.0.26-beta` | PR #24 / 720 sin `SyntaxWarning` |
| G061 | `0.0.61.01-beta` | UX.4.6f R1/R1.1 — aceptación conjunta | base `0.0.26-beta` | PR #28 / 743 pruebas |
| G062 | `0.0.62.02-beta` | UX.4.6f — mantenimiento de dependencias post-R1 | base `0.0.26-beta` | PR #29 / `pypdf 6.16.1` + `uvicorn 0.52.3` / 743 pruebas |
| G063 | `0.0.63.03-beta` | UX.4.6f R2 — auditoría lógica/matemática | base `0.0.26-beta` | PR #30 / 756 pruebas |
| G064 | `0.0.64.04-beta` | UX.4.6f — hardening `pre-commit` y cierre documental | base `0.0.26-beta` | PR #31 / 762 pruebas |
| G065 | `0.0.65.01-beta` | UX.4.6g R1 — cierre Paso 5 | base `0.0.26-beta` | PR #32 / 784 pruebas |
| G066 | `0.0.66.01-beta` | UX.4.6h R1.1 — corrección aceptada | base `0.0.26-beta` | supera candidato R1 fallido |
| G067 | `0.0.67.02-beta` | UX.4.6h R1.2 — claridad/jerarquía | base `0.0.26-beta` | revisión aceptada |
| G068 | `0.0.68.03-beta` | UX.4.6h R1.3 — informe A4 y cierre Paso 6 | base `0.0.26-beta` | PR #33 / 812 pruebas |
| G069 | `0.0.69.01-beta` | UX.4.6i R1 — guía pública de cálculo | base `0.0.26-beta` | gate aceptado 826 pruebas |
| G070 | `0.0.70.02-beta` | UX.4.6i R1.4 — cierre Cómo se calcula | base `0.0.26-beta` | PR #34 / 841 pruebas |

## Estados preservados que no consumen Global

El ledger estructurado conserva también estas exclusiones para no perder historia:

- UX.2.1 como subfase real absorbida en G009;
- iteraciones no aceptadas independientemente de UX.4.6a–c;
- UX.4.6d R1–R22, cuyo cierre integral llegó en R23/G021;
- PR #19 como checkpoint pre-R8 que consolida estados ya contabilizados y deja R8 pendiente;
- UX.4.6e R8.1, corregida antes de R8.2;
- PR #22, cierre documental del estado R9 ya contabilizado;
- PR #25, reconciliación documental post-tag de PLAN.1 R4.2;
- UX.4.6f R1 por separado, porque R1/R1.1 se aceptaron conjuntamente;
- UX.4.6g R1.2/R1.3/R1.4/R1.4.2/R1.4.3, sin aceptación diferenciada demostrada;
- UX.4.6h R1, candidato fallido;
- UX.4.6i R1.1, inexistente como revisión independiente;
- UX.4.6i R1.2/R1.3, sin aceptación diferenciada demostrada;
- Pull Requests Dependabot cerrados o sustituidos que no constituyeron el estado finalmente aceptado.

## Próximo estado

VER.2 no consume G071 por existir como rama o PR draft. Solo si su ledger, validador, documentación, pruebas y CI quedan aceptados se incorpora:

| Global | ID revision-aware candidato | Bloque | Condición |
|---:|---|---|---|
| G071 | `0.0.71.01-beta` | VER.2 R1 — reconciliación revision-aware | ledger + validador + gate completo + PR/CI verde + integración |

Después de aceptar G071, DEV.2 puede volver a ser el bloque funcional activo.