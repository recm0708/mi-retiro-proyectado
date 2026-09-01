# Auditoría integral de documentación Markdown post-SEC.2

**Proyecto:** Mi Retiro Proyectado
**Snapshot base:** `4bd7d8d57c8ccf6229ff2e53493c996b29db14a2`
**Fecha:** 2026-08-25
**Inventario versionado auditado:** 445 archivos; 140 Markdown
**Clasificación base:** 57 vivos, 14 auditorías, 64 históricos, 1 plantilla, 4 soporte
**Estado:** auditoría completada; correcciones preparadas en AUD.SEC2 R1
**Clasificación:** Auditoría / Documentación / Gobierno

## 1. Criterio

La revisión no agrega “SEC.2” indiscriminadamente a toda la documentación. Cada
Markdown del snapshot se evalúa según su responsabilidad:

- los documentos **vivos** deben describir correctamente el estado actual cuando
  dependen materialmente de seguridad, gobierno, versionado o rutas cambiadas;
- las **auditorías** conservan lo observado en su momento;
- los **históricos** no se reescriben para aparentar actualidad;
- las **plantillas** y archivos de **soporte** solo cambian si su contrato fue
  afectado.

Además del auditor automático `scripts/audit_markdown.py`, se revisaron estado de
fases, referencias de versión/ledger, seguridad administrativa, cookies, rutas
del Centro de desarrollo, clasificación documental y coherencia con código y
pruebas.

## 2. Hallazgos transversales

1. SEC.2 estaba cerrado en R1–R6, pero varias superficies vivas todavía mostraban
   R1/R4 o SEC.2 como pendiente.
2. `docs/security/sec2-closure.md` estaba clasificado como vivo aunque es evidencia
   de cierre; se mueve a `docs/audits/security/sec2-final-closure.md`.
3. El README no mostraba los enlaces directos de `/dev/login` y
   `/dev/centro-desarrollo` ni explicaba que no existe una clave predeterminada.
4. Threat model, privacidad y despliegue todavía asumían ausencia de cookie/sesión
   administrativa, contradiciendo R5/R6.
5. El ledger vivo seguía detenido en G070/G071; la reconciliación separada
   reconstruye G071–G108 y reserva G109 sin modificar todavía `VERSION`.
6. Los documentos regulatorios, motores, modalidades y otros dominios no afectados
   por SEC.2 fueron revisados y se preservan sin cambios.

## 3. Resultado por archivo — 140/140

| # | Archivo | Clasificación base | Decisión |
| ---: | --- | --- | --- |
| 1 | `.githooks/README.md` | SOPORTE | SIN CAMBIO — soporte operativo sin contrato afectado por SEC.2. |
| 2 | `.github/pull_request_template.md` | SOPORTE | SIN CAMBIO — soporte operativo sin contrato afectado por SEC.2. |
| 3 | `CHANGELOG.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 4 | `CODE_OF_CONDUCT.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 5 | `CONTRIBUTING.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 6 | `GOVERNANCE.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 7 | `README.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 8 | `RELEASES.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 9 | `SECURITY.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 10 | `SUPPORT.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 11 | `THIRD_PARTY_NOTICES.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 12 | `VERSIONING.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 13 | `docs/README.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 14 | `docs/architecture/calculation-engine.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 15 | `docs/architecture/data-model.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 16 | `docs/architecture/development-center.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 17 | `docs/architecture/system-architecture.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 18 | `docs/archive/CHANGELOG_PRE_GOV1_3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 19 | `docs/archive/README.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 20 | `docs/archive/ROADMAP_PRE_GOV1_3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 21 | `docs/archive/governance/AUDITORIA_GITHUB.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 22 | `docs/archive/governance/AUDITORIA_MARKDOWN_POST_MANT1_DOC1_R1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 23 | `docs/archive/governance/AUDITORIA_PLAN1_R4_2026-08-20.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 24 | `docs/archive/governance/AUDITORIA_REPOSITORIO_2026-08-18.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 25 | `docs/archive/governance/AUDITORIA_VER2_CONTEO_PROVISIONAL.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 26 | `docs/archive/governance/AUDITORIA_VER2_SEGUNDA_PASADA.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 27 | `docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 28 | `docs/archive/governance/CIERRE_DOCUMENTAL_MARKDOWN_DOC1_R1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 29 | `docs/archive/governance/CIERRE_GOV1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 30 | `docs/archive/governance/CONTEXTO_ACTUALIZACION_MARKDOWN_DOC1_R1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 31 | `docs/archive/governance/DECISIONES_PRE_GOV1_3_R4.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 32 | `docs/archive/governance/LINEA_BASE_DOCUMENTAL_POST_MANT1_DOC1_R1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 33 | `docs/archive/governance/MATRIZ_DECISION_MARKDOWN_DOC1_R1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 34 | `docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 35 | `docs/archive/governance/MIGRACION_FIRMAS_GIT_2026-08-17.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 36 | `docs/archive/governance/README.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 37 | `docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 38 | `docs/archive/governance/REVISION_SOLO_SI_APLICA_DOC1_R1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 39 | `docs/archive/governance/VER2_R1_AUDITORIA_RECONCILIACION_POST_DOC1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 40 | `docs/archive/governance/VER2_R1_DECISION_OPERATIVA_POST_DOC1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 41 | `docs/archive/governance/VER2_R1_MATRIZ_DECISION_RECONCILIACION_POST_DOC1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 42 | `docs/archive/governance/VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 43 | `docs/archive/governance/VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 44 | `docs/archive/governance/VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 45 | `docs/archive/governance/VER2_R3_DECISION_VERSION_CANDIDATA_POST_R2.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 46 | `docs/archive/governance/VER2_R4_PROMOCION_G071_E01.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 47 | `docs/archive/governance/VER2_R5_ESTABILIZACION_POST_RELEASE.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 48 | `docs/archive/regulatory-privacy/CUMPLIMIENTO_LEY_81_PRE_GOV1_3_R3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 49 | `docs/archive/regulatory-privacy/FUENTES_NORMATIVAS_PRE_GOV1_3_R3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 50 | `docs/archive/regulatory-privacy/MODALIDADES_MIXTO_PRE_GOV1_3_R3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 51 | `docs/archive/regulatory-privacy/MODALIDADES_SEBD_PRE_GOV1_3_R3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 52 | `docs/archive/regulatory-privacy/MODALIDADES_SUCGS_PRE_GOV1_3_R3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 53 | `docs/archive/regulatory-privacy/NORMATIVA_PRE_GOV1_3_R3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 54 | `docs/archive/regulatory-privacy/POLITICA_PRIVACIDAD_PRE_GOV1_3_R3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 55 | `docs/archive/regulatory-privacy/README.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 56 | `docs/archive/regulatory-privacy/SEGURIDAD_PRIVACIDAD_PRE_GOV1_3_R3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 57 | `docs/archive/regulatory-privacy/TERMINOS_USO_PRIVACIDAD_PRE_GOV1_3_R3.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 58 | `docs/archive/technical/ARQUITECTURA_PRE_GOV1_3_R2.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 59 | `docs/archive/technical/AUDITORIA_ARCHIVOS_R5F.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 60 | `docs/archive/technical/AUDITORIA_CALCULOS.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 61 | `docs/archive/technical/AUDITORIA_CARPETAS_R5E.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 62 | `docs/archive/technical/AUDITORIA_DOCUMENTACION_R5G.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 63 | `docs/archive/technical/AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 64 | `docs/archive/technical/AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 65 | `docs/archive/technical/AUDITORIA_NOMBRES_RESTANTES_R5H.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 66 | `docs/archive/technical/CIERRE_OPERATIVO_POST_AUDITORIA_R7.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 67 | `docs/archive/technical/ESPECIFICACION_FUNCIONAL_PRE_GOV1_3_R2.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 68 | `docs/archive/technical/GESTION_DATOS_SIMULACION_PRE_GOV1_3_R2.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 69 | `docs/archive/technical/GUIA_INTERNA_DESARROLLO_PRE_GOV1_3_R2.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 70 | `docs/archive/technical/MODELO_DE_DATOS_PRE_GOV1_3_R2.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 71 | `docs/archive/technical/MOTOR_DE_CALCULO_PRE_GOV1_3_R2.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 72 | `docs/archive/technical/README.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 73 | `docs/archive/technical/VALIDACION_PRE_GOV1_3_R2.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 74 | `docs/archive/ux/AUDITORIA_UX46E_R7_2026-08-18.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 75 | `docs/archive/ux/README.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 76 | `docs/archive/ux/UX46H_R1_AUDITORIA_RESULTADOS.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 77 | `docs/archive/ux/UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 78 | `docs/archive/ux/UX_4_6A_REDISENO_VISUAL.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 79 | `docs/archive/ux/UX_4_6B_PASO1_DATOS_PERSONALES.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 80 | `docs/archive/ux/UX_4_6C_PASO2_CUOTAS.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 81 | `docs/archive/ux/UX_4_6D_PASO3_HISTORIAL.md` | HISTÓRICO | SIN CAMBIO — evidencia histórica preservada; no se moderniza retroactivamente. |
| 82 | `docs/audits/documentation/documentation-classification-nor1-r3.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 83 | `docs/audits/documentation/documentation-dependency-audit-nor1-r5.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 84 | `docs/audits/documentation/documentation-markdown-audit-doc1-r2.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 85 | `docs/audits/repository/naming-audit-nor1-r4.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 86 | `docs/audits/repository/repository-normalization-baseline-nor2-r1.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 87 | `docs/audits/repository/repository-normalization-final-audit-nor2-r8.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 88 | `docs/audits/repository/repository-normalization-historical-docs-nor2-r5.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 89 | `docs/audits/repository/repository-normalization-ledger-data-nor2-r6.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 90 | `docs/audits/repository/repository-normalization-live-docs-nor2-r4.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 91 | `docs/audits/repository/repository-normalization-local-artifacts-nor2-r7.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 92 | `docs/audits/repository/repository-normalization-migration-matrix-nor2-r2.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 93 | `docs/audits/repository/repository-normalization-runtime-migration-nor2-r3.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 94 | `docs/audits/repository/repository-standards-closure-nor1-r7.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 95 | `docs/audits/security/sec2-r1-codeql-workflow-hardening.md` | AUDITORÍA | SIN CAMBIO — evidencia de auditoría preservada en su contexto original. |
| 96 | `docs/decisions/README.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 97 | `docs/decisions/adr-179-revision-aware-versioning.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 98 | `docs/governance/licensing-and-distribution.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 99 | `docs/governance/master-plan-to-1-0.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 100 | `docs/governance/pre-1-0-revision-ledger.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 101 | `docs/governance/roadmap.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 102 | `docs/operations/development-guide.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 103 | `docs/operations/github-public-repository.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 104 | `docs/operations/observability-and-logs.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 105 | `docs/operations/release-process.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 106 | `docs/operations/third-party-dependencies.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 107 | `docs/operations/validation.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 108 | `docs/product/calculation-guide.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 109 | `docs/product/functional-specification.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 110 | `docs/product/known-limitations.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 111 | `docs/product/simulation-data-management.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 112 | `docs/product/traceability-matrix.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 113 | `docs/product/transparency.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 114 | `docs/product/visual-identity.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 115 | `docs/regulatory/law-81-compliance.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 116 | `docs/regulatory/mixto-modalities.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 117 | `docs/regulatory/regulatory-framework.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 118 | `docs/regulatory/regulatory-sources.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 119 | `docs/regulatory/sebd-modalities.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 120 | `docs/regulatory/sucgs-modalities.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 121 | `docs/security/data-subject-rights-procedure.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 122 | `docs/security/privacy-policy.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 123 | `docs/security/sec2-closure.md` | VIVO | MOVER — evidencia de cierre fuera de documentación viva hacia `docs/audits/security/sec2-final-closure.md`. |
| 124 | `docs/security/security-and-privacy.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 125 | `docs/security/security-incident-procedure.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 126 | `docs/security/terms-and-privacy.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 127 | `docs/security/third-party-deployment-assessment.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 128 | `docs/security/threat-model.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 129 | `docs/standards/README.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 130 | `docs/standards/artifact-lifecycle.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 131 | `docs/standards/code-and-comments.md` | VIVO | ACTUALIZAR — estado vigente, seguridad, versionado o trazabilidad materialmente afectados por SEC.2/AUD.SEC2. |
| 132 | `docs/standards/documentation-standards.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 133 | `docs/standards/file-standards.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 134 | `docs/standards/file-structure-by-extension.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 135 | `docs/standards/naming-conventions.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 136 | `docs/standards/repository-structure.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 137 | `docs/standards/root-and-local-artifacts.md` | VIVO | SIN CAMBIO — documento vivo revisado; su dominio/contrato no depende materialmente de SEC.2 ni de la reconciliación. |
| 138 | `docs/templates/file-structure/README.md` | PLANTILLA | SIN CAMBIO — plantilla sin dependencia material del cierre SEC.2. |
| 139 | `scripts/README.md` | SOPORTE | SIN CAMBIO — soporte operativo sin contrato afectado por SEC.2. |
| 140 | `tests/validation_cases/README.md` | SOPORTE | SIN CAMBIO — soporte operativo sin contrato afectado por SEC.2. |

## 4. Resultado de clasificación

La clasificación base de 140 Markdown queda completamente cubierta por esta
matriz. La remediación añade esta auditoría y la auditoría de reconciliación de
gobierno; el movimiento del cierre SEC.2 es neutro en cantidad. Por ello el árbol
de trabajo contiene 142 Markdown antes de cualquier documentación adicional de
la futura promoción G109.

No se eliminaron documentos históricos para reducir el conteo. Los cambios se
limitan a documentos vivos materialmente afectados y a la reclasificación del
cierre SEC.2.

## 5. Gate

Antes del commit firmado deben ejecutarse en el `.venv` del repositorio:

```powershell
python scripts/audit_markdown.py
python -m pip check
python -m compileall app
Get-ChildItem .\app\static\js\*.js | ForEach-Object { node --check $_.FullName }
python -m unittest discover -s tests -q
git diff --check
```

AUD.SEC2 R1 no se considera G109 aceptado hasta superar este gate, PR/CI e
integración a `main`.
