# NOR.2 R5 — archivo y consolidación de documentación histórica

**Base:** `65b8fd9`

**Estado:** migración histórica aplicada y validada localmente.

## Resultado estructural

R5 traslada **36 documentos cerrados** desde la raíz de `docs/` hacia
`docs/archive/`, respetando la clasificación definida por NOR.2 R2:

- gobierno/versionado: **25**;
- técnico: **8**;
- UX: **3**.

Los archivos movidos conservan su contenido histórico. No se crean stubs de
compatibilidad y Git preserva la historia del movimiento.

## Movimientos

| Origen | Destino |
| --- | --- |
| `docs/AUDITORIA_GITHUB.md` | `docs/archive/governance/AUDITORIA_GITHUB.md` |
| `docs/AUDITORIA_MARKDOWN_POST_MANT1_DOC1_R1.md` | `docs/archive/governance/AUDITORIA_MARKDOWN_POST_MANT1_DOC1_R1.md` |
| `docs/AUDITORIA_PLAN1_R4_2026-08-20.md` | `docs/archive/governance/AUDITORIA_PLAN1_R4_2026-08-20.md` |
| `docs/AUDITORIA_REPOSITORIO_2026-08-18.md` | `docs/archive/governance/AUDITORIA_REPOSITORIO_2026-08-18.md` |
| `docs/AUDITORIA_VER2_CONTEO_PROVISIONAL.md` | `docs/archive/governance/AUDITORIA_VER2_CONTEO_PROVISIONAL.md` |
| `docs/AUDITORIA_VER2_SEGUNDA_PASADA.md` | `docs/archive/governance/AUDITORIA_VER2_SEGUNDA_PASADA.md` |
| `docs/AUDITORIA_VERSIONADO_PRE_1_0.md` | `docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md` |
| `docs/CIERRE_DOCUMENTAL_MARKDOWN_DOC1_R1.md` | `docs/archive/governance/CIERRE_DOCUMENTAL_MARKDOWN_DOC1_R1.md` |
| `docs/CIERRE_GOV1.md` | `docs/archive/governance/CIERRE_GOV1.md` |
| `docs/CONTEXTO_ACTUALIZACION_MARKDOWN_DOC1_R1.md` | `docs/archive/governance/CONTEXTO_ACTUALIZACION_MARKDOWN_DOC1_R1.md` |
| `docs/LINEA_BASE_DOCUMENTAL_POST_MANT1_DOC1_R1.md` | `docs/archive/governance/LINEA_BASE_DOCUMENTAL_POST_MANT1_DOC1_R1.md` |
| `docs/MATRIZ_DECISION_MARKDOWN_DOC1_R1.md` | `docs/archive/governance/MATRIZ_DECISION_MARKDOWN_DOC1_R1.md` |
| `docs/MATRIZ_DECISION_REVISIONES_VER2.md` | `docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md` |
| `docs/MIGRACION_FIRMAS_GIT_2026-08-17.md` | `docs/archive/governance/MIGRACION_FIRMAS_GIT_2026-08-17.md` |
| `docs/REGISTRO_CAMBIOS_HISTORICO.md` | `docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md` |
| `docs/REVISION_SOLO_SI_APLICA_DOC1_R1.md` | `docs/archive/governance/REVISION_SOLO_SI_APLICA_DOC1_R1.md` |
| `docs/VER2_R1_AUDITORIA_RECONCILIACION_POST_DOC1.md` | `docs/archive/governance/VER2_R1_AUDITORIA_RECONCILIACION_POST_DOC1.md` |
| `docs/VER2_R1_DECISION_OPERATIVA_POST_DOC1.md` | `docs/archive/governance/VER2_R1_DECISION_OPERATIVA_POST_DOC1.md` |
| `docs/VER2_R1_MATRIZ_DECISION_RECONCILIACION_POST_DOC1.md` | `docs/archive/governance/VER2_R1_MATRIZ_DECISION_RECONCILIACION_POST_DOC1.md` |
| `docs/VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md` | `docs/archive/governance/VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md` |
| `docs/VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md` | `docs/archive/governance/VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md` |
| `docs/VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md` | `docs/archive/governance/VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md` |
| `docs/VER2_R3_DECISION_VERSION_CANDIDATA_POST_R2.md` | `docs/archive/governance/VER2_R3_DECISION_VERSION_CANDIDATA_POST_R2.md` |
| `docs/VER2_R4_PROMOCION_G071_E01.md` | `docs/archive/governance/VER2_R4_PROMOCION_G071_E01.md` |
| `docs/VER2_R5_ESTABILIZACION_POST_RELEASE.md` | `docs/archive/governance/VER2_R5_ESTABILIZACION_POST_RELEASE.md` |
| `docs/AUDITORIA_ARCHIVOS_R5F.md` | `docs/archive/technical/AUDITORIA_ARCHIVOS_R5F.md` |
| `docs/AUDITORIA_CALCULOS.md` | `docs/archive/technical/AUDITORIA_CALCULOS.md` |
| `docs/AUDITORIA_CARPETAS_R5E.md` | `docs/archive/technical/AUDITORIA_CARPETAS_R5E.md` |
| `docs/AUDITORIA_DOCUMENTACION_R5G.md` | `docs/archive/technical/AUDITORIA_DOCUMENTACION_R5G.md` |
| `docs/AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md` | `docs/archive/technical/AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md` |
| `docs/AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md` | `docs/archive/technical/AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md` |
| `docs/AUDITORIA_NOMBRES_RESTANTES_R5H.md` | `docs/archive/technical/AUDITORIA_NOMBRES_RESTANTES_R5H.md` |
| `docs/CIERRE_OPERATIVO_POST_AUDITORIA_R7.md` | `docs/archive/technical/CIERRE_OPERATIVO_POST_AUDITORIA_R7.md` |
| `docs/AUDITORIA_UX46E_R7_2026-08-18.md` | `docs/archive/ux/AUDITORIA_UX46E_R7_2026-08-18.md` |
| `docs/UX46H_R1_AUDITORIA_RESULTADOS.md` | `docs/archive/ux/UX46H_R1_AUDITORIA_RESULTADOS.md` |
| `docs/UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md` | `docs/archive/ux/UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md` |

## Índices históricos

R5 actualiza los README de `docs/archive/`, `governance/`, `technical/` y
`ux/` para distinguir navegación vigente de evidencia histórica y retirar
referencias obsoletas a `docs/INDICE.md` o a stubs de compatibilidad.

## Siguiente revisión

**NOR.2 R6**: migración del ledger/datos de alto impacto.

## Gate local previo al commit — 2026-08-24

La revisión NOR.2 R5 quedó validada localmente con los siguientes resultados observados:

- suite completa: **971 pruebas ejecutadas — OK**;
- contrato específico NOR.2 R5: **8 pruebas + 40 subtests — OK**;
- `python -m compileall -q app`: **OK**;
- validación sintáctica de JavaScript mediante `node --check`: **OK**;
- `git diff --check`: **OK**;
- rutas antiguas R5 inspeccionadas: **36**;
- referencias vivas obsoletas hacia esas rutas: **0**;
- Markdown inspeccionados en la auditoría de duplicados: **124**;
- grupos con contenido idéntico: **0**;
- `VERSION` permanece en `0.0.71.01-beta`.

Los 36 documentos históricos se conservan una sola vez bajo `docs/archive/`.
No se restauran rutas antiguas ni se crean stubs de compatibilidad.

NOR.2 R5 permanece activo hasta integrarse en `main`; **NOR.2 R6** es la
siguiente revisión.
