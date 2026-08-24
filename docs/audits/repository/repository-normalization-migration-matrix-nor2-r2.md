# Matriz de decisión de migración NOR.2 R2

**Proyecto:** Mi Retiro Proyectado

**Fase:** NOR.2 R2 — Matriz de decisión

**Base integrada:** `c0e06ca`

**Estado:** decisión previa a migraciones estructurales.

## Propósito

Convertir la línea base de R1 en un plan ejecutable que deje el árbol vigente
con documentación y rutas actuales, preservando la historia mediante Git,
`docs/archive/` y evidencia de auditoría cuando exista valor real de trazabilidad.

## Regla de estado actual

El árbol operativo no mantendrá archivos obsoletos únicamente para conservar una
ruta anterior.

Cuando un documento sea sustituido:

1. el documento vigente adopta la ruta canónica nueva;
2. todas las referencias vivas se actualizan de manera atómica;
3. Git conserva la historia anterior;
4. `docs/archive/` conserva una copia adicional solo cuando el documento cerrado
   mantiene valor de auditoría o contexto;
5. no se crean stubs de compatibilidad permanentes salvo obligación técnica
   demostrada.

Esta regla aplica también al `README.md` raíz: debe representar el estado real
del proyecto durante NOR.2 y volverá a auditarse en el gate de cierre.

## Hallazgos heredados de R1

- Archivos versionados auditados: **416**.
- Markdown raíz de `docs/` por clasificar: **79**.
- Candidatos de idioma/dominio: **28**.
- JSON/YAML candidatos: **2**.
- Directorio raíz señalado por la allowlist mecánica de R1: `assets/`.
- Directorio local heredado: `_entregas/`.

## Decisiones globales

| Elemento | Decisión | Destino/resultado | Revisión | Justificación |
| --- | --- | --- | --- | --- |
| `README.md` | **MIGRAR** | `README.md` actualizado | R2 + R8 | Es la portada pública y no puede conservar estados cerrados como activos. |
| `assets/` | **CONSERVAR COMO EXCEPCIÓN** | `assets/` | R2 | Responsabilidad transversal de identidad/repositorio; está permitida por la regla de raíz de NOR.1 aunque no apareciera en la allowlist mecánica de R1. |
| `_entregas/` | **MIGRAR LOCAL** | `_deliverables/` o evidencia externa | R7 | Revisar 29 archivos antes de mover o retirar; no borrar evidencia útil. |
| `docs/` raíz actual | **CONSOLIDAR** | áreas vivas + `audits/` + `archive/` | R4–R5 | Separar estado vigente de fases cerradas y reducir ruido documental. |

## Estructura documental viva objetivo

NOR.2 propone como responsabilidades estables adicionales permitidas por
`docs/standards/repository-structure.md`:

```text
docs/
├── README.md
├── architecture/
├── decisions/
├── governance/
├── operations/
├── product/
├── regulatory/
├── security/
├── standards/
├── audits/
├── archive/
└── templates/
```

Las seis áreas nuevas contienen únicamente documentación viva. Los documentos
de fases cerradas no permanecen allí.

## Documentación: 79 candidatos de R1

| Ruta actual | Decisión | Ruta/área objetivo | Revisión | Criterio |
| --- | --- | --- | --- | --- |
| `docs/ADR_179_VERSIONADO_REVISION_AWARE.md` | **MIGRAR** | `docs/decisions/adr-179-revision-aware-versioning.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/ARQUITECTURA.md` | **MIGRAR** | `docs/architecture/system-architecture.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/COMO_SE_CALCULA.md` | **MIGRAR** | `docs/product/calculation-guide.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/CUMPLIMIENTO_LEY_81.md` | **MIGRAR** | `docs/regulatory/law-81-compliance.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/DECISIONES.md` | **MIGRAR** | `docs/decisions/README.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/DEPENDENCIAS_TERCEROS.md` | **MIGRAR** | `docs/operations/third-party-dependencies.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/DEV2_CENTRO_DESARROLLO.md` | **MIGRAR** | `docs/architecture/development-center.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/ESPECIFICACION_FUNCIONAL.md` | **MIGRAR** | `docs/product/functional-specification.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/EVALUACION_TERCEROS_DESPLIEGUE.md` | **MIGRAR** | `docs/security/third-party-deployment-assessment.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/FUENTES_NORMATIVAS.md` | **MIGRAR** | `docs/regulatory/regulatory-sources.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/GESTION_DATOS_SIMULACION.md` | **MIGRAR** | `docs/product/simulation-data-management.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/GUIA_INTERNA_DESARROLLO.md` | **MIGRAR** | `docs/operations/development-guide.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/IDENTIDAD_VISUAL.md` | **MIGRAR** | `docs/product/visual-identity.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/INDICE.md` | **MIGRAR** | `docs/README.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/LEDGER_REVISIONES_PRE_1_0.md` | **MIGRAR** | `docs/governance/pre-1-0-revision-ledger.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/LICENCIA_Y_DISTRIBUCION.md` | **MIGRAR** | `docs/governance/licensing-and-distribution.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/LIMITACIONES_CONOCIDAS.md` | **MIGRAR** | `docs/product/known-limitations.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/MATRIZ_TRAZABILIDAD.md` | **MIGRAR** | `docs/product/traceability-matrix.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/MODALIDADES_MIXTO.md` | **MIGRAR** | `docs/regulatory/mixto-modalities.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/MODALIDADES_SEBD.md` | **MIGRAR** | `docs/regulatory/sebd-modalities.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/MODALIDADES_SUCGS.md` | **MIGRAR** | `docs/regulatory/sucgs-modalities.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/MODELO_AMENAZAS.md` | **MIGRAR** | `docs/security/threat-model.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/MODELO_DE_DATOS.md` | **MIGRAR** | `docs/architecture/data-model.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/MOTOR_DE_CALCULO.md` | **MIGRAR** | `docs/architecture/calculation-engine.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/NORMATIVA.md` | **MIGRAR** | `docs/regulatory/regulatory-framework.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/OBSERVABILIDAD_LOGS.md` | **MIGRAR** | `docs/operations/observability-and-logs.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/PLAN_MAESTRO_HACIA_1_0.md` | **MIGRAR** | `docs/governance/master-plan-to-1-0.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/POLITICA_PRIVACIDAD.md` | **MIGRAR** | `docs/security/privacy-policy.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/PREPARACION_PUBLICA_GITHUB.md` | **MIGRAR** | `docs/operations/github-public-repository.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/PROCEDIMIENTO_DERECHOS_TITULAR.md` | **MIGRAR** | `docs/security/data-subject-rights-procedure.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md` | **MIGRAR** | `docs/security/security-incident-procedure.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/PROCESO_RELEASE.md` | **MIGRAR** | `docs/operations/release-process.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/ROADMAP.md` | **MIGRAR** | `docs/governance/roadmap.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/SEGURIDAD_PRIVACIDAD.md` | **MIGRAR** | `docs/security/security-and-privacy.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/TERMINOS_USO_PRIVACIDAD.md` | **MIGRAR** | `docs/security/terms-and-privacy.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/TRANSPARENCIA.md` | **MIGRAR** | `docs/product/transparency.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/UX_4_6A_REDISENO_VISUAL.md` | **MIGRAR** | `docs/product/user-interface.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/UX_4_6B_PASO1_DATOS_PERSONALES.md` | **MIGRAR** | `docs/product/workflow-step-1-personal-data.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/UX_4_6C_PASO2_CUOTAS.md` | **MIGRAR** | `docs/product/workflow-step-2-contributions.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/UX_4_6D_PASO3_HISTORIAL.md` | **MIGRAR** | `docs/product/workflow-step-3-salary-history.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/VALIDACION.md` | **MIGRAR** | `docs/operations/validation.md` | R4 | Documento vivo; actualizar contenido y todas sus referencias. |
| `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md` | **CONSOLIDAR** | `docs/standards/` | R4 | Su contenido útil se integra al estándar canónico; el original deja de ser documentación viva. |
| `docs/POLITICA_ESTRUCTURA_ARCHIVOS.md` | **CONSOLIDAR** | `docs/standards/` | R4 | Su contenido útil se integra al estándar canónico; el original deja de ser documentación viva. |
| `docs/AUDITORIA_GITHUB.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/AUDITORIA_MARKDOWN_POST_MANT1_DOC1_R1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/AUDITORIA_PLAN1_R4_2026-08-20.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/AUDITORIA_REPOSITORIO_2026-08-18.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/AUDITORIA_VER2_CONTEO_PROVISIONAL.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/AUDITORIA_VER2_SEGUNDA_PASADA.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/AUDITORIA_VERSIONADO_PRE_1_0.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/CIERRE_DOCUMENTAL_MARKDOWN_DOC1_R1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/CIERRE_GOV1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/CONTEXTO_ACTUALIZACION_MARKDOWN_DOC1_R1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/LINEA_BASE_DOCUMENTAL_POST_MANT1_DOC1_R1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/MATRIZ_DECISION_MARKDOWN_DOC1_R1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/MATRIZ_DECISION_REVISIONES_VER2.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/MIGRACION_FIRMAS_GIT_2026-08-17.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/REGISTRO_CAMBIOS_HISTORICO.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/REVISION_SOLO_SI_APLICA_DOC1_R1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/VER2_R1_AUDITORIA_RECONCILIACION_POST_DOC1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/VER2_R1_DECISION_OPERATIVA_POST_DOC1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/VER2_R1_MATRIZ_DECISION_RECONCILIACION_POST_DOC1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/VER2_R3_DECISION_VERSION_CANDIDATA_POST_R2.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/VER2_R4_PROMOCION_G071_E01.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/VER2_R5_ESTABILIZACION_POST_RELEASE.md` | **ARCHIVAR** | `docs/archive/governance/` | R5 | Fase/auditoría cerrada; conservar valor histórico fuera de docs vivo. |
| `docs/AUDITORIA_ARCHIVOS_R5F.md` | **ARCHIVAR** | `docs/archive/technical/` | R5 | Evidencia técnica cerrada; Git y archive preservan trazabilidad. |
| `docs/AUDITORIA_CALCULOS.md` | **ARCHIVAR** | `docs/archive/technical/` | R5 | Evidencia técnica cerrada; Git y archive preservan trazabilidad. |
| `docs/AUDITORIA_CARPETAS_R5E.md` | **ARCHIVAR** | `docs/archive/technical/` | R5 | Evidencia técnica cerrada; Git y archive preservan trazabilidad. |
| `docs/AUDITORIA_DOCUMENTACION_R5G.md` | **ARCHIVAR** | `docs/archive/technical/` | R5 | Evidencia técnica cerrada; Git y archive preservan trazabilidad. |
| `docs/AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md` | **ARCHIVAR** | `docs/archive/technical/` | R5 | Evidencia técnica cerrada; Git y archive preservan trazabilidad. |
| `docs/AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md` | **ARCHIVAR** | `docs/archive/technical/` | R5 | Evidencia técnica cerrada; Git y archive preservan trazabilidad. |
| `docs/AUDITORIA_NOMBRES_RESTANTES_R5H.md` | **ARCHIVAR** | `docs/archive/technical/` | R5 | Evidencia técnica cerrada; Git y archive preservan trazabilidad. |
| `docs/CIERRE_OPERATIVO_POST_AUDITORIA_R7.md` | **ARCHIVAR** | `docs/archive/technical/` | R5 | Evidencia técnica cerrada; Git y archive preservan trazabilidad. |
| `docs/AUDITORIA_UX46E_R7_2026-08-18.md` | **ARCHIVAR** | `docs/archive/ux/` | R5 | Evidencia UX cerrada; no representa estado operativo actual. |
| `docs/UX46H_R1_AUDITORIA_RESULTADOS.md` | **ARCHIVAR** | `docs/archive/ux/` | R5 | Evidencia UX cerrada; no representa estado operativo actual. |
| `docs/UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md` | **ARCHIVAR** | `docs/archive/ux/` | R5 | Evidencia UX cerrada; no representa estado operativo actual. |

## Código, assets de runtime, plantillas y pruebas

| Ruta actual | Decisión | Ruta objetivo | Revisión | Criterio |
| --- | --- | --- | --- | --- |
| `app/services/centro_desarrollo.py` | **MIGRAR** | `app/services/development_center.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/services/como_se_calcula.py` | **MIGRAR** | `app/services/calculation_guide.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/services/detalle_anio_actual.py` | **MIGRAR** | `app/services/current_year_detail.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/services/referencia_mi_retiro_seguro.py` | **MIGRAR** | `app/services/mi_retiro_seguro_reference.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/static/css/como-se-calcula.css` | **MIGRAR** | `app/static/css/calculation-guide.css` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/static/css/procedencia-editable.css` | **MIGRAR** | `app/static/css/editable-provenance.css` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/static/js/detalle_anio_actual.js` | **MIGRAR** | `app/static/js/current_year_detail.js` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/static/js/procedencia_editable.js` | **MIGRAR** | `app/static/js/editable_provenance.js` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/static/js/referencia_mi_retiro_seguro.js` | **MIGRAR** | `app/static/js/mi_retiro_seguro_reference.js` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/static/js/tema.js` | **MIGRAR** | `app/static/js/theme.js` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/templates/como_se_calcula.html` | **MIGRAR** | `app/templates/calculation_guide.html` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/templates/comparar.html` | **MIGRAR** | `app/templates/comparison.html` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/templates/dev_centro_desarrollo.html` | **MIGRAR** | `app/templates/dev_development_center.html` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/templates/metodologia.html` | **MIGRAR** | `app/templates/methodology.html` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/templates/partials/detalle_anio_actual.html` | **MIGRAR** | `app/templates/partials/current_year_detail.html` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/templates/partials/importacion_ficha_digital.html` | **MIGRAR** | `app/templates/partials/ficha_digital_import.html` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/templates/partials/referencia_mi_retiro_seguro.html` | **MIGRAR** | `app/templates/partials/mi_retiro_seguro_reference.html` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `tests/test_dev2_centro_desarrollo.py` | **MIGRAR** | `tests/test_dev2_development_center.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `tests/test_ux44_detalle_anio_actual.py` | **MIGRAR** | `tests/test_ux44_current_year_detail.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `tests/test_ux44_referencia_pdf.py` | **MIGRAR** | `tests/test_ux44_pdf_reference.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `tests/test_ux46d_revision18_procedencia_persistencia.py` | **MIGRAR** | `tests/test_ux46d_revision18_provenance_persistence.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `tests/test_ux46d_revision19_sincronizacion_actual.py` | **MIGRAR** | `tests/test_ux46d_revision19_current_sync.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `tests/test_ux46d_revision23_ficha_actualiza_cuotas.py` | **MIGRAR** | `tests/test_ux46d_revision23_ficha_updates_contributions.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `tests/test_ux46e_r81_procedencia_editable.py` | **MIGRAR** | `tests/test_ux46e_r81_editable_provenance.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `tests/test_ux46f_r1_consistencia_procedencia_adjuntos.py` | **MIGRAR** | `tests/test_ux46f_r1_attachment_provenance_consistency.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `tests/test_ux46g_r1_escenarios_retiro.py` | **MIGRAR** | `tests/test_ux46g_r1_retirement_scenarios.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `tests/test_ux46i_r1_como_se_calcula.py` | **MIGRAR** | `tests/test_ux46i_r1_calculation_guide.py` | R3 | Nombre técnico; preservar términos oficiales cuando formen parte del identificador de dominio. |
| `app/services/ficha_digital.py` | **CONSERVAR COMO EXCEPCIÓN** | `app/services/ficha_digital.py` | R3 | Conservar: «Ficha Digital» es nombre de dominio/producto externo; el archivo ya cumple snake_case. |

## Datos y configuración

| Ruta actual | Decisión | Ruta objetivo | Revisión | Criterio |
| --- | --- | --- | --- | --- |
| `data/revision_ledger_pre_1_0.json` | **MIGRAR** | `data/pre-1-0-revision-ledger.json` | R6 | Alto impacto: actualizar consumidores, pruebas, release, documentación y ledger en una sola migración. |
| `regulations/general_parameters.json` | **MIGRAR** | `regulations/general-parameters.json` | R3 | Normalización kebab-case con actualización atómica de referencias. |

## Regresiones de estado histórico

| Prueba | Decisión | Resultado | Revisión | Criterio |
| --- | --- | --- | --- | --- |
| `tests/test_doc1_r1_auditoria_markdown_post_mant1.py` | **MIGRAR** | La evidencia DOC.1 conserva su fotografía histórica; `README.md` valida únicamente el estado vigente. | R2 | Una regresión cerrada no debe obligar a reintroducir estados obsoletos en documentación viva. |
| `tests/test_ver2_documentacion_vigente.py` | **MIGRAR** | Separar reglas históricas del PR de promoción del estado post-release vigente. | R2/R4 | El tag puede estar publicado hoy aunque la regla histórica establezca que no se crea dentro del PR de promoción. |

- `tests/test_dev2_r4_cierre_final.py`: la evidencia DEV.2 conserva su cierre R4; README solo declara DEV.2 cerrado.
- `tests/test_gov18_cierre_gobierno.py`: GOV.1.8 y las referencias históricas sustituidas se validan en `docs/CIERRE_GOV1.md`, no en README.
- `tests/test_ux46i_r1_como_se_calcula.py`: la secuencia UX.4.6i y su transición a DEV.2 se validan en roadmap/plan/guía; README solo refleja el estado vigente.

Estas pruebas permanecen útiles, pero NOR.2 elimina de ellas cualquier contrato
que fuerce a la documentación viva a representar una fase ya cerrada.

## Orden de ejecución

### R3 — runtime y configuración de bajo/medio impacto

- servicios Python;
- JavaScript;
- CSS;
- plantillas;
- pruebas asociadas;
- `regulations/general_parameters.json`;
- actualización atómica de imports/rutas/referencias.

### R4 — documentación viva

- crear las áreas vivas estables;
- migrar y actualizar los documentos canónicos;
- convertir `docs/INDICE.md` en `docs/README.md`;
- consolidar políticas duplicadas en `docs/standards/`;
- actualizar enlaces en README, documentación y pruebas.

### R5 — historia y auditorías cerradas

- mover documentación de fases cerradas fuera de `docs/` vivo;
- usar `docs/archive/` cuando el contexto histórico siga siendo útil;
- evitar duplicados que ya estén representados por Git o por una evidencia
  canónica equivalente;
- eliminar del árbol vigente copias sustituidas sin valor independiente.

### R6 — ledger y datos de alto impacto

- migrar `data/revision_ledger_pre_1_0.json`;
- actualizar `app/core/version_ledger.py`;
- actualizar pruebas, release/versionado y documentación;
- verificar continuidad y contenido del ledger después del cambio.

### R7 — artefactos locales

- revisar `_entregas/` archivo por archivo;
- migrar lo vigente a `_deliverables/` cuando corresponda;
- mover evidencia temporal fuera del repositorio cuando corresponda;
- retirar únicamente elementos demostrados como prescindibles.

### R8 — cierre integral NOR.2

Gate obligatorio:

- `README.md` actualizado;
- `docs/README.md` actualizado;
- `CHANGELOG.md`, roadmap, plan maestro y validación sincronizados;
- arquitectura y estructura de carpetas reales;
- cero enlaces vivos a rutas migradas;
- cero imports vivos a módulos migrados;
- cero documentos actuales que declaren como activas fases cerradas;
- inventario final del árbol;
- suite completa local;
- CI y auditoría de gobernanza en verde;
- merge a `main`.

**NOR.2 no se considera cerrado si falla cualquiera de estos puntos.**

## Estado de SEC.2

SEC.2 permanece pausado hasta completar R8 y verificar el árbol integrado en
`main`.
