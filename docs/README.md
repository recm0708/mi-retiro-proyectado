# Índice de documentación

**Estado:** vigente
**Versión de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01 promovida en R4
**Último tag formal legacy:** `v0.0.26-beta`
**Última actualización transversal:** SEC.2 R6 — cierre de hardening administrativo y preparación HTTPS interno — 2026-08-25
**Cierres históricos preservados:** UX.4.6i / PR #34 — 841 pruebas; UX.4.6e R9 — `v0.0.25-beta`

Este archivo es el punto de entrada para la documentación técnica, funcional, normativa, de privacidad, validación y auditoría de Mi Retiro Proyectado.


## Estado de normalización del repositorio

**Estado actual:** NOR.2, DOC.1 R2 y SEC.2 R1 están cerrados. SEC.2 quedó cerrado después de completar R1-R6. Los controles futuros de despliegue productivo se gestionarán bajo el bloque correspondiente.

Estado de la fase:

- **NOR.1:** cerrado en R7; estándares determinísticos establecidos.
- **NOR.2 R1:** cerrado; línea base integral del repositorio.
- **NOR.2 R2:** cerrado; matriz de decisión de migración.
- **NOR.2 R3:** cerrado; runtime y configuración técnica normalizados.
- **NOR.2 R4:** cerrado; documentación viva migrada a áreas canónicas.
- **NOR.2 R5:** cerrado; 36 documentos históricos consolidados en `docs/archive/`.
- **NOR.2 R6:** cerrado; ledger y datos de alto impacto normalizados.
- **NOR.2 R7:** cerrado; artefactos locales heredados migrados y depurados.
- **NOR.2 R8:** cerrado; auditoría integral y cierre formal integrados mediante PR #74.
- **DOC.1 R2:** cerrado; auditoría integral Markdown post-NOR.2 y controles permanentes incorporados.
- **SEC.2 R1:** cerrado; hardening CodeQL y normalización técnica de workflows completados.

Evidencia:

- [`audits/security/sec2-r1-codeql-workflow-hardening.md`](audits/security/sec2-r1-codeql-workflow-hardening.md) — hardening CodeQL y normalización de workflows SEC.2 R1.

- [`audits/repository/repository-normalization-baseline-nor2-r1.md`](audits/repository/repository-normalization-baseline-nor2-r1.md) — línea base R1.
- [`audits/repository/repository-normalization-migration-matrix-nor2-r2.md`](audits/repository/repository-normalization-migration-matrix-nor2-r2.md) — matriz de migración R2.
- [`audits/repository/repository-normalization-runtime-migration-nor2-r3.md`](audits/repository/repository-normalization-runtime-migration-nor2-r3.md) — migración técnica R3.
- [`audits/repository/repository-normalization-live-docs-nor2-r4.md`](audits/repository/repository-normalization-live-docs-nor2-r4.md) — migración documental viva R4.
- [`audits/repository/repository-normalization-historical-docs-nor2-r5.md`](audits/repository/repository-normalization-historical-docs-nor2-r5.md) — consolidación de documentación histórica R5.
- [`audits/repository/repository-normalization-ledger-data-nor2-r6.md`](audits/repository/repository-normalization-ledger-data-nor2-r6.md) — normalización del ledger y datos de alto impacto R6.
- [`audits/repository/repository-normalization-local-artifacts-nor2-r7.md`](audits/repository/repository-normalization-local-artifacts-nor2-r7.md) — migración y depuración de artefactos locales R7.
- [`audits/repository/repository-normalization-final-audit-nor2-r8.md`](audits/repository/repository-normalization-final-audit-nor2-r8.md) — auditoría integral y gate de cierre R8.
- [`audits/documentation/documentation-markdown-audit-doc1-r2.md`](audits/documentation/documentation-markdown-audit-doc1-r2.md) — auditoría integral Markdown post-NOR.2 y controles permanentes de DOC.1 R2.
- [`standards/README.md`](standards/README.md) — estándares canónicos del repositorio.
## 1. Producto y alcance

- [`../README.md`](../README.md) — presentación, alcance, instalación y estado general.
- [`functional-specification.md`](product/functional-specification.md) — requisitos funcionales.
- [`roadmap.md`](governance/roadmap.md) — estado actual y próximos hitos.
- [`master-plan-to-1-0.md`](governance/master-plan-to-1-0.md) — secuencia transversal de 14 bloques hasta la primera versión oficial.
- [`visual-identity.md`](product/visual-identity.md) — logo oficial, activos canónicos, favicons y Social Preview.
- [`calculation-guide.md`](product/calculation-guide.md) — contrato público de explicación de SEBD, Mixto y SUCGS sin duplicar motores.

## 2. Gobierno y versionado

- [`../GOVERNANCE.md`](../GOVERNANCE.md) — gobierno del proyecto.
- [`../VERSIONING.md`](../VERSIONING.md) — política legacy, beta revision-aware `0.GG.RR.EE-beta`, versión oficial de cuatro componentes y Build independiente.
- [`../VERSION`](../VERSION) — fuente canónica de la versión candidata de aplicación.
- [`AUDITORIA_VERSIONADO_PRE_1_0.md`](archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md) — auditoría del historial, criterio contable y exclusiones de VER.2.
- [`adr-179-revision-aware-versioning.md`](decisions/adr-179-revision-aware-versioning.md) — decisión ADR del esquema revision-aware previo a `1.0.0.0`.
- [`AUDITORIA_VER2_SEGUNDA_PASADA.md`](archive/governance/AUDITORIA_VER2_SEGUNDA_PASADA.md) — bitácora de la segunda pasada y correcciones sobre la primera reconstrucción.
- [`AUDITORIA_VER2_CONTEO_PROVISIONAL.md`](archive/governance/AUDITORIA_VER2_CONTEO_PROVISIONAL.md) — cierre del conteo de segunda pasada en G070 antes de VER.2.
- [`MATRIZ_DECISION_REVISIONES_VER2.md`](archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md) — decisión fila por fila sobre qué consume Global y por qué.
- [`pre-1-0-revision-ledger.md`](governance/pre-1-0-revision-ledger.md) — ledger Markdown G001–G070 y candidato G071.
- [`../data/pre-1-0-revision-ledger.json`](../data/pre-1-0-revision-ledger.json) — ledger machine-readable canónico de la reconstrucción.
- [`../app/core/version_ledger.py`](../app/core/version_ledger.py) — validador de continuidad, unicidad y codificación del ledger estructurado.
- [`../RELEASES.md`](../RELEASES.md) — versiones, tags y reconstrucción histórica.
- [`../CHANGELOG.md`](../CHANGELOG.md) — cambios notables por versión.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — flujo de contribución.
- [`../CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md) — normas de participación.
- [`../SUPPORT.md`](../SUPPORT.md) — canales de soporte, privacidad y seguridad.
- [`master-plan-to-1-0.md`](governance/master-plan-to-1-0.md) — dependencias y gates previos a `1.0.0.0`.
- [`MIGRACION_FIRMAS_GIT_2026-08-17.md`](archive/governance/MIGRACION_FIRMAS_GIT_2026-08-17.md) — firma SSH y migración histórica controlada.
- [`../.github/allowed_signers`](../.github/allowed_signers) — claves públicas autorizadas.
- [`AUDITORIA_GITHUB.md`](archive/governance/AUDITORIA_GITHUB.md) — controles GitHub, seguridad y auditoría automática.
- [`github-public-repository.md`](operations/github-public-repository.md) — metadata, topics, labels, badges, Social Preview y seguridad del repositorio público.
- [`AUDITORIA_REPOSITORIO_2026-08-18.md`](archive/governance/AUDITORIA_REPOSITORIO_2026-08-18.md) — auditoría integral local/remota post-GOV.1.
- [`AUDITORIA_UX46E_R7_2026-08-18.md`](archive/ux/AUDITORIA_UX46E_R7_2026-08-18.md) — auditoría transversal de coherencia de UX.4.6e.
- [`AUDITORIA_PLAN1_R4_2026-08-20.md`](archive/governance/AUDITORIA_PLAN1_R4_2026-08-20.md) — auditoría integral y gates R4.1/R4.2 de PLAN.1.
- [`CIERRE_GOV1.md`](archive/governance/CIERRE_GOV1.md) — evidencia definitiva del cierre GOV.1.
- [`../LICENSE`](../LICENSE) — licencia propietaria de materiales originales.
- [`licensing-and-distribution.md`](governance/licensing-and-distribution.md) — evaluación y decisión de licencia.
- [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) — avisos de componentes de terceros.

## 3. Arquitectura

- [`system-architecture.md`](architecture/system-architecture.md) — capas, módulos, endpoints y flujo.
- [`AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md`](archive/technical/AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md) — auditoría de política y plantillas por extensión.
- [`AUDITORIA_CARPETAS_R5E.md`](archive/technical/AUDITORIA_CARPETAS_R5E.md) — auditoría de nombres de carpetas técnicas y rutas sincronizadas.
- [`AUDITORIA_ARCHIVOS_R5F.md`](archive/technical/AUDITORIA_ARCHIVOS_R5F.md) — auditoría de nombres de archivos técnicos y referencias sincronizadas.
- [`AUDITORIA_DOCUMENTACION_R5G.md`](archive/technical/AUDITORIA_DOCUMENTACION_R5G.md) — auditoría de cobertura documental, índice y referencias internas.
- [`data-model.md`](architecture/data-model.md) — modelos y contratos.
- [`simulation-data-management.md`](product/simulation-data-management.md) — estado local, limpieza, restauración e invalidación.
- [`observability-and-logs.md`](operations/observability-and-logs.md) — Developer Diagnostics, esquema JSONL, correlación, redacción, retención y exportación.

## 4. Especificación funcional

- [`functional-specification.md`](product/functional-specification.md) — RF y comportamiento del producto.
- [`development-guide.md`](operations/development-guide.md) — convenciones de ingeniería e interfaz.

## 5. Motores previsionales

- [`calculation-engine.md`](architecture/calculation-engine.md) — flujo común de cálculo.
- [`sebd-modalities.md`](regulatory/sebd-modalities.md) — SEBD.
- [`mixto-modalities.md`](regulatory/mixto-modalities.md) — Subsistema Mixto.
- [`sucgs-modalities.md`](regulatory/sucgs-modalities.md) — SUCGS.

## 6. Normativa y fuentes

- [`regulatory-framework.md`](regulatory/regulatory-framework.md) — interpretación y aplicación normativa.
- [`regulatory-sources.md`](regulatory/regulatory-sources.md) — catálogo de fuentes oficiales.
- `../regulations/*.json` — parámetros legales versionados.

## 7. Datos y trazabilidad

- [`data-model.md`](architecture/data-model.md) — contratos y procedencia.
- [`simulation-data-management.md`](product/simulation-data-management.md) — ciclo de vida del estado local.
- [`README.md`](decisions/README.md) — decisiones ADR históricas y vigentes.

## 8. Seguridad y privacidad

- [`security-and-privacy.md`](security/security-and-privacy.md) — controles técnicos.
- [`threat-model.md`](security/threat-model.md) — threat model y matriz de riesgos.
- [`data-subject-rights-procedure.md`](security/data-subject-rights-procedure.md) — ejercicio de derechos.
- [`security-incident-procedure.md`](security/security-incident-procedure.md) — incident response.
- [`third-party-deployment-assessment.md`](security/third-party-deployment-assessment.md) — terceros, TLS y gates de despliegue.
- [`privacy-policy.md`](security/privacy-policy.md) — política pública vigente.
- [`terms-and-privacy.md`](security/terms-and-privacy.md) — términos y tratamiento de datos.
- [`law-81-compliance.md`](regulatory/law-81-compliance.md) — matriz interna de alineación.
- [`observability-and-logs.md`](operations/observability-and-logs.md) — minimización y manejo local de logs diagnósticos.
- [`../SECURITY.md`](../SECURITY.md) — política y canales privados de reporte responsable de vulnerabilidades.

La publicación del repositorio no elimina la revisión jurídica externa ni cualquier diseño de seguridad específico que requiera un futuro despliegue remoto de la aplicación.

## 9. Transparencia, auditoría y trazabilidad

- [`transparency.md`](product/transparency.md) — fronteras de afirmación y transparencia pública.
- [`traceability-matrix.md`](product/traceability-matrix.md) — requisito/criterio → ADR → implementación → prueba → estado.
- [`AUDITORIA_CALCULOS.md`](archive/technical/AUDITORIA_CALCULOS.md) — reproducibilidad y revisión de resultados.
- [`UX46H_R1_AUDITORIA_RESULTADOS.md`](archive/ux/UX46H_R1_AUDITORIA_RESULTADOS.md) — auditoría de resultados y coherencia visual de UX.4.6h.
- [`known-limitations.md`](product/known-limitations.md) — límites técnicos, normativos y de despliegue.
- [`third-party-dependencies.md`](operations/third-party-dependencies.md) — dependencias, licencias upstream, conexiones y riesgos.
- [`release-process.md`](operations/release-process.md) — gates de cierre, versión, Build, CI y tags.
- [`UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md`](archive/ux/UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md) — auditoría canónica de UX.4.6i; secuencia demostrada R1 → R1.2 → R1.3 → R1.4.

## 10. Validación y calidad

- [`validation.md`](operations/validation.md) — estrategia y evidencias.
- [`../tests/test_ver2_ledger_estructurado.py`](../tests/test_ver2_ledger_estructurado.py) — regresiones del ledger JSON y sus invariantes.
- [`../tests/test_ver2_version_revision_aware.py`](../tests/test_ver2_version_revision_aware.py) — regresiones del esquema revision-aware.
- [`../tests/test_ver2_documentacion_vigente.py`](../tests/test_ver2_documentacion_vigente.py) — coherencia de superficies vigentes durante VER.2.
- [`../tests/validation_cases/README.md`](../tests/validation_cases/README.md) — reglas de casos sintéticos/anonimizados.
- `../.github/workflows/ci.yml` — CI funcional.
- `../.github/workflows/governance-audit.yml` — auditoría automática de gobierno.
- `../.github/workflows/verificar-tags.yml` — verificación criptográfica de tags.
- `../.github/dependabot.yml` — mantenimiento de dependencias.

## 11. Desarrollo y contribución

- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — flujo principal.
- [`../CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md) — reglas de convivencia y colaboración.
- [`../SUPPORT.md`](../SUPPORT.md) — rutas de consulta y reporte.
- [`development-guide.md`](operations/development-guide.md) — convenciones internas.
- [`development-center.md`](architecture/development-center.md) — cierre documental del centro de desarrollo DEV.2.
- [`file-structure-by-extension.md`](standards/file-structure-by-extension.md) — política vigente de estructura, nombres y ubicación de archivos.
- [`code-and-comments.md`](standards/code-and-comments.md) — patrón permanente de comentarios y docstrings por tecnología.
- [`../.editorconfig`](../.editorconfig) — formato.
- [`../.gitattributes`](../.gitattributes) — normalización Git.
- [`../.gitignore`](../.gitignore) — exclusiones y protección de datos locales.

## 12. Historial de evolución

- [`REGISTRO_CAMBIOS_HISTORICO.md`](archive/governance/REGISTRO_CAMBIOS_HISTORICO.md) — mapa cronológico.
- [`UX_4_6A_REDISENO_VISUAL.md`](archive/ux/UX_4_6A_REDISENO_VISUAL.md) — bitácora histórica del rediseño visual UX.4.6a.
- [`UX_4_6B_PASO1_DATOS_PERSONALES.md`](archive/ux/UX_4_6B_PASO1_DATOS_PERSONALES.md) — bitácora histórica del Paso 1 de UX.4.6b.
- [`UX_4_6C_PASO2_CUOTAS.md`](archive/ux/UX_4_6C_PASO2_CUOTAS.md) — bitácora histórica del Paso 2 de UX.4.6c.
- [`UX_4_6D_PASO3_HISTORIAL.md`](archive/ux/UX_4_6D_PASO3_HISTORIAL.md) — bitácora histórica del Paso 3 de UX.4.6d.
- [`archive/README.md`](archive/README.md) — reglas del archivo histórico.
- [`archive/ux/`](archive/ux) — bitácoras completas de UX.4.6a–d.
- [`archive/technical/`](archive/technical) — snapshots técnicos previos.
- [`archive/regulatory-privacy/`](archive/regulatory-privacy) — snapshots normativos/privacidad previos.
- [`archive/governance/`](archive/governance) — snapshots de decisiones/gobierno.
- [`archive/CHANGELOG_PRE_GOV1_3.md`](archive/CHANGELOG_PRE_GOV1_3.md) — snapshot del changelog acumulativo anterior a GOV.1.3.
- [`archive/ROADMAP_PRE_GOV1_3.md`](archive/ROADMAP_PRE_GOV1_3.md) — snapshot del roadmap anterior a GOV.1.3.

Los archivos históricos documentan lo que se pensó, probó o decidió en un momento determinado. No deben interpretarse como contrato vigente si contradicen un documento actual.

## 13. Releases

- [`../RELEASES.md`](../RELEASES.md) — registro formal y retrospectivo.
- [`../CHANGELOG.md`](../CHANGELOG.md) — cambios notables.
- [`../VERSIONING.md`](../VERSIONING.md) — reglas de incremento y tags.
- [`AUDITORIA_VERSIONADO_PRE_1_0.md`](archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md) — reconciliación VER.2.
- [`pre-1-0-revision-ledger.md`](governance/pre-1-0-revision-ledger.md) — contador global.
- [`../data/pre-1-0-revision-ledger.json`](../data/pre-1-0-revision-ledger.json) — representación estructurada del contador.
- [`master-plan-to-1-0.md`](governance/master-plan-to-1-0.md) — gates hasta la primera versión oficial.

## Clasificación documental

Los documentos vigentes pueden utilizar los estados:

- **Vigente**
- **Borrador**
- **Pendiente de revisión externa**
- **Parcialmente sustituido**
- **Sustituido**
- **Histórico**

## Regla de mantenimiento

Un cambio no obliga a editar todos los `.md`. Sí obliga a revisar todos los documentos que dependan del cambio y mantener coherencia entre código, normativa versionada, pruebas, documentación vigente, fuentes oficiales e historial de decisiones.

La metadata de versión de revisión de un documento de dominio puede conservar su base histórica aunque `VERSION` avance; solo las superficies que declaran el estado vigente deben seguir la versión canónica actual.

<!-- ANCLAS_HISTORICAS_VER2_INDICE_CONSOLIDADAS -->

## Compatibilidad histórica preservada por VER.2

- **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno** queda preservado como cierre histórico de gobierno.
- UX.4.6e R9.2 queda preservado como cierre histórico asociado a `0.0.25-beta`.
- La familia `0.0.N-beta` permanece como línea legacy histórica hasta `v0.0.26-beta`.
- **Versión candidata de aplicación:** `0.0.26-beta` — referencia legacy preservada para las regresiones históricas de PLAN.1.
- El contrato histórico mantiene versiones oficiales de cuatro componentes para la línea estable futura.
- GOV.1.3 R3 preservó el snapshot archive/regulatory-privacy/ como evidencia histórica normativa y de privacidad.

- [AUDITORIA_NOMBRES_RESTANTES_R5H.md](archive/technical/AUDITORIA_NOMBRES_RESTANTES_R5H.md) — Auditoría MANT.1 R5H de nombres técnicos restantes.

## MANT.1 R6 — Auditoría funcional post-renombres

- `AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md`: auditoría funcional posterior a los renombres técnicos de MANT.1 R5. Verifica rutas, plantillas, assets, contratos frontend/backend, formularios, cargas de archivo y estructura HTML renderizada.

## MANT.1 R7 — Cierre operativo post-auditoría

- `CIERRE_OPERATIVO_POST_AUDITORIA_R7.md`: cierre operativo posterior a R5H/R6. Verifica estado de ramas, evidencias documentales, pruebas focalizadas y protección de archivos sensibles.

## DOC.1 R1 — Auditoría integral Markdown post-MANT.1

- `AUDITORIA_MARKDOWN_POST_MANT1_DOC1_R1.md`: inventario integral de archivos Markdown posterior al cierre de MANT.1.
- `MATRIZ_DECISION_MARKDOWN_DOC1_R1.md`: clasificación de Markdown en actualizar, revisar, preservar histórico, preservar auditoría cerrada o sin cambio inicial.
- `CONTEXTO_ACTUALIZACION_MARKDOWN_DOC1_R1.md`: extracción de contexto para documentos candidatos antes de actualizarlos.
- `LINEA_BASE_DOCUMENTAL_POST_MANT1_DOC1_R1.md`: línea base documental vigente para sincronizar README, roadmap, validación, versionado y demás documentos vivos post-MANT.1.
- `REVISION_SOLO_SI_APLICA_DOC1_R1.md`: revisión de documentos de soporte o política general marcados como actualizar solo si aplica; no requirieron cambios materiales.
- `CIERRE_DOCUMENTAL_MARKDOWN_DOC1_R1.md`: cierre formal de DOC.1 R1 con alcance revisado, evidencia generada, límites respetados y validación documental.
## VER.2 R1 — Reconciliación post-DOC.1

- [Auditoría de reconciliación VER.2 R1](archive/governance/VER2_R1_AUDITORIA_RECONCILIACION_POST_DOC1.md)
- [Matriz de decisión VER.2 R1](archive/governance/VER2_R1_MATRIZ_DECISION_RECONCILIACION_POST_DOC1.md)
- [Decisión operativa VER.2 R1](archive/governance/VER2_R1_DECISION_OPERATIVA_POST_DOC1.md)
## VER.2 R2 — Documentación viva post-R1

- [Análisis de contradicciones VER.2 R2](archive/governance/VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md)
- [Propuesta de corrección de documentación viva VER.2 R2](archive/governance/VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md)
- [Cierre de documentación viva VER.2 R2](archive/governance/VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md)
## VER.2 R3 — Decisión de versión candidata post-R2

- [Decisión de versión candidata VER.2 R3](archive/governance/VER2_R3_DECISION_VERSION_CANDIDATA_POST_R2.md)
## VER.2 R4 — Promoción controlada G071/E01

- [Promoción controlada VER.2 R4 G071/E01](archive/governance/VER2_R4_PROMOCION_G071_E01.md)

## VER.2 R5 — Estabilización post-release

- [Estabilización post-release VER.2 R5](archive/governance/VER2_R5_ESTABILIZACION_POST_RELEASE.md)


**SEC.2 R6:** hardening de sesión administrativa web preparado para despliegue interno controlado.
