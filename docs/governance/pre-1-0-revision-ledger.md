# Ledger de revisiones aceptadas pre-1.0

**Proyecto:** Mi Retiro Proyectado
**Base auditada:** `7037addd44253e528c77460b678d2b3ccd540dd5`
**Contador histórico en la base `7037addd`:** **G070**
**Contador aceptado reconciliado al commit `46c464e`:** **G117**
**Siguiente Global disponible:** **G118**
**Siguiente candidato disponible:** `0.1.18.04-beta` — DEV.2 R5 (Portal Developer y acceso)


<!-- DOC1-R1-REVISION-MANUAL:START -->
## Nota de lectura vigente — reconciliación post-SEC.2

La segunda pasada de VER.2 reconstruyó correctamente G001–G070 sobre la base
`7037addd`, pero el ledger dejó de incorporar estados aceptados posteriores a esa
base. La auditoría integral post-SEC.2 del 2026-08-25 reconstruye esa franja sin
reescribir los primeros 70 estados.

Estado vigente de la contabilidad:

- G001–G070 permanecen exactamente como reconstrucción histórica de VER.2.
- G071–G108 registran estados materialmente distintos aceptados después de
  `7037addd`, desde DEV.2 hasta SEC.2 R6.
- G109 registra AUD.SEC2 R1 ya aceptado mediante PR #83 y merge `ec1842d`.
- El tag publicado `v0.0.71.01-beta` se conserva inmutable. Su cadena de versión
  fue promovida antes de contabilizar los estados DEV.2, MANT.1 y DOC.1 R1 que
  ya existían después de `7037addd`; por eso queda documentada como una
  **anomalía histórica de numeración**. La reconciliación vigente sitúa el estado
  materializado por ese tag en G087/E01 sin modificar la evidencia publicada.
- `VERSION` está sincronizado en `0.1.17.02-beta` después de aceptar REL.GOV.1 R2 como G117/E02 mediante PR #103 / merge `46c464e`; G118/E04 (`0.1.18.04-beta`) queda reservado para DEV.2 R5.
- G110/E01 (`0.1.10.01-beta`) quedó aceptado para REL.GOV.1 mediante PR #85 y merge `5cd1cea`.
- G111/E01 (`0.1.11.01-beta`) permanece aceptado para DOC.2. G112/E07 (`0.1.12.07-beta`) queda aceptado para NOR.1 R8 después de PR #89 / PR #90; G113/E03 (`0.1.13.03-beta`) queda aceptado para DOC.1 R3 mediante PR #92 / merge `40ae5c0`; G114/E01 (`0.1.14.01-beta`) queda aceptado para PLAN.2 R1 mediante PR #94 / merge `7ded70c`; G115/E04 (`0.1.15.04-beta`) queda aceptado para DOC.1 R4 mediante PR #96 / merge `9f51229` y publicado mediante PR #97 / merge `87fa8e9`; G116/E05 (`0.1.16.05-beta`) queda aceptado para DOC.1 R5 mediante PR #101 / merge `6f4266d`; G117/E02 (`0.1.17.02-beta`) queda aceptado para REL.GOV.1 R2 mediante PR #103 / merge `46c464e`. G118/E04 (`0.1.18.04-beta`) queda reservado para DEV.2 R5.
<!-- DOC1-R1-REVISION-MANUAL:END -->

Este ledger registra los estados aceptados reconstruidos durante VER.2 y su reconciliación posterior. La regla contable histórica y las exclusiones originales se conservan en `docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md` y `docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md`; la ampliación post-G070 se justifica en `docs/audits/governance/post-g070-revision-reconciliation.md`.

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

## Reconciliación G071–G108

Estos estados se reconstruyen cronológicamente desde el árbol posterior a `7037addd`.
El detalle de inclusión/exclusión está en `docs/audits/governance/post-g070-revision-reconciliation.md`.

| Global | ID revision-aware | Bloque / estado aceptado | Ancla histórica | Evidencia resumida |
|---:|---|---|---|---|
| G071 | `0.0.71.01-beta` | DEV.2 R1 — Centro de desarrollo y estado interno | `0.0.26-beta` | commit 06e2821 / PR #37; apertura funcional DEV.2 |
| G072 | `0.0.72.02-beta` | DEV.2 R2 — visor diagnóstico seguro | `0.0.26-beta` | commit 5451d18 / PR #39; visor y exportación diagnóstica |
| G073 | `0.0.73.03-beta` | DEV.2 R3 — autodiagnóstico técnico local | `0.0.26-beta` | commit 9fb86af / PR #40; autodiagnóstico y regresiones |
| G074 | `0.0.74.01-beta` | MANT.1 R2 — documentación de scripts y hooks | `0.0.26-beta` | commit 8fdc389 / PR #42; R1 queda como auditoría inicial absorbida |
| G075 | `0.0.75.02-beta` | MANT.1 R3 — encabezados YAML de GitHub | `0.0.26-beta` | commit 9013aa3; regresión YAML |
| G076 | `0.0.76.03-beta` | MANT.1 R4 — limpieza de trazabilidad en encabezados operativos | `0.0.26-beta` | commit e894bcc; regresión de encabezados |
| G077 | `0.0.77.04-beta` | MANT.1 R5A — comentarios internos en servicios Python | `0.0.26-beta` | commit 46e51d5; regresión de comentarios Python |
| G078 | `0.0.78.05-beta` | MANT.1 R5B — comentarios en CSS y plantilla | `0.0.26-beta` | commit 97b4984; regresión de comentarios CSS/Jinja |
| G079 | `0.0.79.06-beta` | MANT.1 R5C — comentarios en JavaScript complejo | `0.0.26-beta` | commit 0b349ce; regresión de comentarios JavaScript |
| G080 | `0.0.80.07-beta` | MANT.1 R5D — política y plantillas por extensión | `0.0.26-beta` | commit 77b413e; política y regresiones por extensión |
| G081 | `0.0.81.08-beta` | MANT.1 R5E — estandarización de nombres de carpetas | `0.0.26-beta` | commit 42c2cea; migración de carpetas y regresiones |
| G082 | `0.0.82.09-beta` | MANT.1 R5F — normalización de nombres de archivos | `0.0.26-beta` | commit ba6995e; migración de archivos y regresiones |
| G083 | `0.0.83.10-beta` | MANT.1 R5G — auditoría y consolidación documental | `0.0.26-beta` | commit 9a8a795; índice/enlaces y regresión documental |
| G084 | `0.0.84.11-beta` | MANT.1 R5H — auditoría de nombres técnicos restantes | `0.0.26-beta` | commit ab92677 / PR #53; normalización y regresiones |
| G085 | `0.0.85.12-beta` | MANT.1 R6 — auditoría funcional post-renombres | `0.0.26-beta` | commit 9ac55ca / PR #54; validación funcional focalizada |
| G086 | `0.0.86.01-beta` | DOC.1 R1 — auditoría Markdown post-MANT.1 | `0.0.26-beta` | commit d991890 / PR #56; auditoría y línea base documental |
| G087 | `0.0.87.01-beta` | VER.2 R4 — promoción controlada publicada como 0.0.71.01-beta | `v0.0.71.01-beta` | PR #60; commit cb1dc24; tag firmado v0.0.71.01-beta |
| G088 | `0.0.88.01-beta` | NOR.1 R1 — estándares de estructura y nomenclatura | `0.0.71.01-beta` | commit firmado 67aae43 dentro de PR #62 |
| G089 | `0.0.89.02-beta` | NOR.1 R1.1 — estructura documental para auditorías e históricos | `0.0.71.01-beta` | commit firmado 10e195d dentro de PR #62 |
| G090 | `0.0.90.03-beta` | NOR.1 R3 — clasificación documental inicial | `0.0.71.01-beta` | commit firmado 8c26c60; squash f1489ef / PR #62 |
| G091 | `0.0.91.04-beta` | NOR.1 R4 — auditoría de nomenclatura | `0.0.71.01-beta` | commit fc4b1ef / PR #63 |
| G092 | `0.0.92.05-beta` | NOR.1 R5 — auditoría de dependencias documentales | `0.0.71.01-beta` | commit 4cf6b3d; evidencia documental |
| G093 | `0.0.93.06-beta` | NOR.1 R6 — estándares determinísticos consolidados | `0.0.71.01-beta` | commit e33f594; gate previo a cierre |
| G094 | `0.0.94.01-beta` | NOR.2 R1 — línea base de normalización | `0.0.71.01-beta` | commit c0e06ca / PR #67 |
| G095 | `0.0.95.02-beta` | NOR.2 R2 — matriz de migración | `0.0.71.01-beta` | commit 4d4e56f; matriz aprobada |
| G096 | `0.0.96.03-beta` | NOR.2 R3 — migración de runtime y configuración | `0.0.71.01-beta` | commit b037518; migración técnica |
| G097 | `0.0.97.04-beta` | NOR.2 R4 — normalización de documentación viva | `0.0.71.01-beta` | commit 65b8fd9 / PR #70 |
| G098 | `0.0.98.05-beta` | NOR.2 R5 — archivo de documentación histórica | `0.0.71.01-beta` | commit ad9b3f3 / PR #71 |
| G099 | `0.0.99.06-beta` | NOR.2 R6 — normalización de ledger y datos | `0.0.71.01-beta` | commit 365ba5b / PR #72 |
| G100 | `0.1.00.07-beta` | NOR.2 R7 — depuración de artefactos locales | `0.0.71.01-beta` | commit b8ffd39 / PR #73 |
| G101 | `0.1.01.08-beta` | NOR.2 R8 — auditoría integral de cierre | `0.0.71.01-beta` | commit b4df9b7 / PR #74 |
| G102 | `0.1.02.02-beta` | DOC.1 R2 — auditoría integral Markdown post-NOR.2 | `0.0.71.01-beta` | commit 46ca30e / PR #76 |
| G103 | `0.1.03.01-beta` | SEC.2 R1 — hardening CodeQL y workflows | `0.0.71.01-beta` | commit e946af7 / PR #77 |
| G104 | `0.1.04.02-beta` | SEC.2 R2 — autenticación administrativa | `0.0.71.01-beta` | commits firmados 92b1e8e y 287ff81 dentro de PR #79 |
| G105 | `0.1.05.03-beta` | SEC.2 R3 — protección centralizada de endpoints | `0.0.71.01-beta` | commit firmado 771015d dentro de PR #79 |
| G106 | `0.1.06.04-beta` | SEC.2 R4 — auditoría y observabilidad administrativa | `0.0.71.01-beta` | commit firmado 5006e28; squash d7a3b54 / PR #79 |
| G107 | `0.1.07.05-beta` | SEC.2 R5 — sesión administrativa web | `0.0.71.01-beta` | commit 0966cd2 / PR #80 |
| G108 | `0.1.08.06-beta` | SEC.2 R6 — hardening de sesiones administrativas | `0.0.71.01-beta` | commit 38da72f / PR #81 |
| G109 | `0.1.09.01-beta` | AUD.SEC2 R1 — auditoría y remediación integral post-SEC.2 | `0.1.09.01-beta` | PR #83 / merge `ec1842d`; 1040 pruebas; CI Python 3.13/3.14 + Markdown/gobernanza en success |
| G110 | `0.1.10.01-beta` | REL.GOV.1 R1 — gobierno y normalización de GitHub Releases | `0.1.10.01-beta` | PR #85 / merge `5cd1cea`; 1054 pruebas; CI Python 3.13/3.14 + Markdown/gobernanza en success |
| G111 | `0.1.11.01-beta` | DOC.2 R1 — reconstrucción auditable del CHANGELOG histórico | `0.1.11.01-beta` | PR #87 / merge `1041b59`; 1066 pruebas; Markdown 143/143; CI Python 3.13/3.14 + Markdown/gobernanza en success |
| G112 | `0.1.12.07-beta` | NOR.1 R8 — gobierno de identificadores de bloques de trabajo | `0.1.12.07-beta` | PR #89 / merge `cc6695b`; PR #90 / merge `2de10b5`; 1081 pruebas; Markdown 145/145; CI en success |
| G113 | `0.1.13.03-beta` | DOC.1 R3 — referencias navegables Markdown y política de presentación | `0.1.13.03-beta` | PR #92 / merge `40ae5c0`; 1092 pruebas; Markdown 146/146; CI Python 3.13/3.14 + Markdown/gobernanza en success |
| G114 | `0.1.14.01-beta` | PLAN.2 R1 — replanificación maestra final hacia 1.0 | `0.1.14.01-beta` | PR #94 / merge `7ded70c`; 1103 pruebas; Markdown 148/148; CI Python 3.13/3.14 + Markdown/gobernanza en success |
| G115 | `0.1.15.04-beta` | DOC.1 R4 — saneamiento documental post-G113 y reconciliación del estado vivo tras G114 | `0.1.15.04-beta` | PR #96 / merge `9f51229`; 1114 pruebas; Markdown 149/149; auditor de identificadores OK; validaciones locales limpias |
| G116 | `0.1.16.05-beta` | DOC.1 R5 — normalización documental integral post-G115 | `0.1.16.05-beta` | PR #101 / merge `6f4266d`; 1127 pruebas unittest; pytest 1167/5587 subtests; Markdown 158/158; checks remotos en success |
| G117 | `0.1.17.02-beta` | REL.GOV.1 R2 — automatización gobernada de Releases y checks | `0.1.17.02-beta` | PR #103 / merge `46c464e`; 1157 unittest; pytest 1197/5731 subtests; Markdown 159/159; CI #273, gobernanza #112, Markdown #59 y CodeQL #209 en success |

### Anomalía histórica del tag `v0.0.71.01-beta`

La publicación de `v0.0.71.01-beta` ocurrió durante VER.2 R4. La decisión VER.2 R3
establece que R1, R2 y R3 son correcciones internas del mismo candidato y no
consumen G072 ni incrementan EE. Al reconstruir además los estados materiales
posteriores a G070, la aceptación final de VER.2 R4 corresponde a **G087/E01**.
El tag no se mueve, elimina ni recrea: se conserva como evidencia publicada y la
discrepancia se corrige únicamente hacia adelante.

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

REL.GOV.1 R2 superó gate local, PR #103, integración y revalidación post-merge; esta promoción materializa ese mismo estado como G117/E02 (`0.1.17.02-beta`) sin consumir un Global adicional.

| Global | ID revision-aware candidato | Bloque | Condición |
|---:|---|---|---|
| G118 | `0.1.18.04-beta` | DEV.2 R5 — Portal Developer y acceso | crear `/dev`, diferenciar sesión web/Bearer, rediseñar `/dev/login`, no persistir secretos, gate completo + commit firmado + PR/CI + integración |

G118 permanece reservado y **no se considera aceptado** mientras DEV.2 R5 siga siendo candidato. `VERSION` queda en `0.1.17.02-beta` y `accepted_count` en 117 durante ese trabajo.

PERSIST.1 permanece planificado como etapa posterior de la matriz maestra y no tiene un Global preasignado.

Los tags `v0.0.71.01-beta`, `v0.1.09.01-beta`, `v0.1.13.03-beta`, `v0.1.14.01-beta`, `v0.1.15.04-beta` y `v0.1.16.05-beta` permanecen publicados e inmutables conforme a su evidencia. G117/E02 queda aceptado para REL.GOV.1 R2; su publicación formal usa el tag firmado `v0.1.17.02-beta` y el GitHub Release gobernado únicamente después de integrar y revalidar la promoción. G118/E04 permanece reservado para DEV.2 R5.
