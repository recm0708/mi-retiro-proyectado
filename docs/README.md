# Índice de documentación

**Estado:** vigente
**Versión de aplicación:** `0.1.17.02-beta` — G117/E02 aceptado para REL.GOV.1 R2; G118/E04 reservado para DEV.2 R5; ledger aceptado hasta G117
**Último tag formal legacy:** `v0.0.26-beta`
**Última actualización transversal:** promoción formal REL.GOV.1 R2 — G117/E02 aceptado; DEV.2 R5 candidato G118/E04 — 2026-08-28
**Cierres históricos preservados:** UX.4.6i / PR #34 — 841 pruebas; UX.4.6e R9 — `v0.0.25-beta`

Este archivo es el punto de entrada para la documentación técnica, funcional, normativa, de privacidad, validación y auditoría de Mi Retiro Proyectado.


## Estado de normalización del repositorio

**Estado actual:** NOR.1 R8, NOR.2, DOC.1 R2–R5, SEC.2, AUD.SEC2 R1, REL.GOV.1 R1–R2, DOC.2 y PLAN.2 R1 están cerrados/aceptados según corresponda. REL.GOV.1 R2 queda aceptado como G117/E02 (`0.1.17.02-beta`); DEV.2 R5 reserva G118/E04 como candidato actual.

Estado de la fase:

- **NOR.1:** cerrado en R8 y aceptado como G112/E07; su política de identificadores queda vigente.
- **NOR.2 R1:** cerrado; línea base integral del repositorio.
- **NOR.2 R2:** cerrado; matriz de decisión de migración.
- **NOR.2 R3:** cerrado; runtime y configuración técnica normalizados.
- **NOR.2 R4:** cerrado; documentación viva migrada a áreas canónicas.
- **NOR.2 R5:** cerrado; 36 documentos históricos consolidados en `docs/archive/`.
- **NOR.2 R6:** cerrado; ledger y datos de alto impacto normalizados.
- **NOR.2 R7:** cerrado; artefactos locales heredados migrados y depurados.
- **NOR.2 R8:** cerrado; auditoría integral y cierre formal integrados mediante PR #74.
- **DOC.1 R2:** cerrado; auditoría integral Markdown post-NOR.2 y controles permanentes incorporados.
- **DOC.1 R3:** cerrado/aceptado como G113/E03; normalizó 11 referencias inequívocas, formalizó la política de navegación documental y preservó rutas históricas/contractuales.
- **DOC.2 R1:** cerrado/aceptado como G111/E01; preserva la reconstrucción auditable del CHANGELOG y su evidencia histórica.
- **PLAN.2 R1:** cerrado/aceptado como G114/E01; formaliza la matriz maestra viva hacia 1.0.
- **DOC.1 R4:** cerrado/aceptado como G115/E04 mediante PR #96 / merge `9f51229`; saneamiento documental post-G113 completado.
- **DOC.1 R5:** cerrado/aceptado como G116/E05 mediante PR #101 / merge `6f4266d`; normalización documental integral post-G115 completada.
- **REL.GOV.1 R2:** cerrado/aceptado como G117/E02 mediante PR #103 / merge `46c464e`; automatización gobernada de Releases y checks completada.
- **DEV.2 R5:** candidato G118/E04 (`0.1.18.04-beta`) para Portal Developer y acceso.
- **SEC.2 R1–R6:** cerrados; CodeQL, autenticación, protección de endpoints, auditoría, sesión web y hardening configurable completados. AUD.SEC2 R1 corrigió el kill switch, alineó documentación/ledger y quedó aceptado como G109/E01.

Evidencia:

- **[SEC.2 R1 — CodeQL DOM hardening y normalización de workflows](audits/security/sec2-r1-codeql-workflow-hardening.md)** — hardening CodeQL y normalización de workflows SEC.2 R1.
- **[SEC.2 — Cierre integral y auditoría post-cierre de seguridad](audits/security/sec2-final-closure.md)** — cierre integral SEC.2 R1–R6 y matriz de controles.
- **[Auditoría integral de documentación Markdown post-SEC.2](audits/documentation/documentation-audit-post-sec2.md)** — auditoría individual de los 140 Markdown del snapshot post-SEC.2.

- **[Línea base de normalización NOR.2 R1](audits/repository/repository-normalization-baseline-nor2-r1.md)** — línea base R1.
- **[Matriz de decisión de migración NOR.2 R2](audits/repository/repository-normalization-migration-matrix-nor2-r2.md)** — matriz de migración R2.
- **[NOR.2 R3 — migración de runtime y configuración](audits/repository/repository-normalization-runtime-migration-nor2-r3.md)** — migración técnica R3.
- **[NOR.2 R4 — migración de documentación viva](audits/repository/repository-normalization-live-docs-nor2-r4.md)** — migración documental viva R4.
- **[NOR.2 R5 — archivo y consolidación de documentación histórica](audits/repository/repository-normalization-historical-docs-nor2-r5.md)** — consolidación de documentación histórica R5.
- **[NOR.2 R6 — migración del ledger y datos de alto impacto](audits/repository/repository-normalization-ledger-data-nor2-r6.md)** — normalización del ledger y datos de alto impacto R6.
- **[NOR.2 R7 — migración y depuración de artefactos locales](audits/repository/repository-normalization-local-artifacts-nor2-r7.md)** — migración y depuración de artefactos locales R7.
- **[Auditoría integral y cierre formal NOR.2 R8](audits/repository/repository-normalization-final-audit-nor2-r8.md)** — auditoría integral y gate de cierre R8.
- **[Auditoría integral Markdown post-NOR.2 — DOC.1 R2](audits/documentation/documentation-markdown-audit-doc1-r2.md)** — auditoría integral Markdown post-NOR.2 y controles permanentes de DOC.1 R2.
- **[Auditoría de referencias navegables Markdown — DOC.1 R3](audits/documentation/documentation-markdown-links-doc1-r3.md)** — auditoría conservadora de referencias navegables y evidencia de aceptación DOC.1 R3 / G113/E03.
- **[Auditoría semántica de documentación viva post-G113 — PLAN.2 R1](audits/documentation/post-g113-live-documentation-audit-plan2-r1.md)** — auditoría semántica de documentación viva al iniciar PLAN.2 R1.
- **[DOC.1 R4 — saneamiento semántico de documentación viva post-G114](audits/documentation/documentation-live-state-doc1-r4.md)** — auditoría DOC.1 R4 de estado vivo posterior a la publicación formal de G114/E01.
- **[Auditoría de normalización documental DOC.1 R5](audits/documentation/documentation-normalization-doc1-r5.md)** — normalización transversal, reconciliación post-G115, plantillas Markdown, endurecimiento del auditor y saneamiento de regresiones históricas.
- **[Reconstrucción del CHANGELOG histórico — DOC.2 R1](audits/documentation/changelog-reconstruction-doc2-r1.md)** — reconstrucción auditable DOC.2 R1 de 80 commits en 21 estados legacy.
- **[Estándares del repositorio](standards/README.md)** — estándares canónicos del repositorio.
- **[Plantillas del repositorio](templates/README.md)** — índice de plantillas técnicas por extensión y plantillas documentales por función.
## 1. Producto y alcance

- **[Mi Retiro Proyectado](../README.md)** — presentación, alcance, instalación y estado general.
- **[Especificación funcional](product/functional-specification.md)** — requisitos funcionales.
- **[Roadmap](governance/roadmap.md)** — estado actual y próximos hitos.
- **[Matriz maestra de pendientes hacia 1.0](governance/pre-1-0-pending-matrix.md)** — matriz maestra viva de pendientes hasta la primera versión oficial.
- **[Plan maestro hacia Mi Retiro Proyectado 1.0](governance/master-plan-to-1-0.md)** — secuencia transversal de 14 bloques hasta la primera versión oficial.
- **[Identidad visual de Mi Retiro Proyectado](product/visual-identity.md)** — logo oficial, activos canónicos, favicons y Social Preview.
- **[Cómo se calcula — contrato de transparencia](product/calculation-guide.md)** — contrato público de explicación de SEBD, Mixto y SUCGS sin duplicar motores.

## 2. Gobierno y versionado

- **[Gobierno del proyecto](../GOVERNANCE.md)** — gobierno del proyecto.
- **[Política de versionado](../VERSIONING.md)** — política legacy, beta revision-aware `0.GG.RR.EE-beta`, versión oficial de cuatro componentes y Build independiente.
- [`../VERSION`](../VERSION) — fuente canónica de la versión candidata de aplicación.
- **[Auditoría de versionado pre-1.0](archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md)** — auditoría del historial, criterio contable y exclusiones de VER.2.
- **[ADR-179 — El versionado beta usa un ledger de estados aceptados y no cuenta commits como revisiones](decisions/adr-179-revision-aware-versioning.md)** — decisión ADR del esquema revision-aware previo a `1.0.0.0`.
- **[VER.2 — Segunda pasada de auditoría cruzada](archive/governance/AUDITORIA_VER2_SEGUNDA_PASADA.md)** — bitácora de la segunda pasada y correcciones sobre la primera reconstrucción.
- **[VER.2 — Conteo de segunda pasada](archive/governance/AUDITORIA_VER2_CONTEO_PROVISIONAL.md)** — cierre del conteo de segunda pasada en G070 antes de VER.2.
- **[VER.2 — Matriz de decisión de revisiones aceptadas](archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md)** — decisión fila por fila sobre qué consume Global y por qué.
- **[Ledger de revisiones aceptadas pre-1.0](governance/pre-1-0-revision-ledger.md)** — ledger Markdown reconciliado G001–G116 y candidato reservado G117/E02 para REL.GOV.1 R2.
- **[Auditoría de reconciliación revision-aware posterior a G070](audits/governance/post-g070-revision-reconciliation.md)** — auditoría de reconstrucción G071–G108.
- [`pre-1-0-revision-ledger-g070.json`](archive/governance/pre-1-0-revision-ledger-g070.json) — snapshot histórico exacto G070.
- [`../data/pre-1-0-revision-ledger.json`](../data/pre-1-0-revision-ledger.json) — ledger machine-readable canónico de la reconstrucción.
- [`../app/core/version_ledger.py`](../app/core/version_ledger.py) — validador de continuidad, unicidad y codificación del ledger estructurado.
- **[Registro de versiones y estados del proyecto](../RELEASES.md)** — versiones, tags y reconstrucción histórica.
- **[Changelog](../CHANGELOG.md)** — cambios notables por versión.
- **[Guía de contribución](../CONTRIBUTING.md)** — flujo de contribución.
- **[Código de conducta](../CODE_OF_CONDUCT.md)** — normas de participación.
- **[Soporte](../SUPPORT.md)** — canales de soporte, privacidad y seguridad.
- **[Plan maestro hacia Mi Retiro Proyectado 1.0](governance/master-plan-to-1-0.md)** — dependencias y gates previos a `1.0.0.0`.
- **[Migración de firma criptográfica Git — 2026-08-17](archive/governance/MIGRACION_FIRMAS_GIT_2026-08-17.md)** — firma SSH y migración histórica controlada.
- [`../.github/allowed_signers`](../.github/allowed_signers) — claves públicas autorizadas.
- **[Auditoría de GitHub y controles de repositorio](archive/governance/AUDITORIA_GITHUB.md)** — controles GitHub, seguridad y auditoría automática.
- **[Preparación pública de GitHub](operations/github-public-repository.md)** — metadata, topics, labels, badges, Social Preview y seguridad del repositorio público.
- **[Auditoría integral del repositorio — 2026-08-18](archive/governance/AUDITORIA_REPOSITORIO_2026-08-18.md)** — auditoría integral local/remota post-GOV.1.
- **[Auditoría transversal UX.4.6e R7](archive/ux/AUDITORIA_UX46E_R7_2026-08-18.md)** — auditoría transversal de coherencia de UX.4.6e.
- **[Auditoría integral PLAN.1 R4](archive/governance/AUDITORIA_PLAN1_R4_2026-08-20.md)** — auditoría integral y gates R4.1/R4.2 de PLAN.1.
- **[Cierre GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta](archive/governance/CIERRE_GOV1.md)** — evidencia definitiva del cierre GOV.1.
- [`../LICENSE`](../LICENSE) — licencia propietaria de materiales originales.
- **[Licencia y estrategia de distribución](governance/licensing-and-distribution.md)** — evaluación y decisión de licencia.
- **[Avisos de terceros](../THIRD_PARTY_NOTICES.md)** — avisos de componentes de terceros.

## 3. Arquitectura

- **[Arquitectura](architecture/system-architecture.md)** — capas, módulos, endpoints y flujo.
- **[Auditoría de estructura por extensión](archive/technical/AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md)** — auditoría de política y plantillas por extensión.
- **[Auditoría de nombres de carpetas — MANT.1 R5E](archive/technical/AUDITORIA_CARPETAS_R5E.md)** — auditoría de nombres de carpetas técnicas y rutas sincronizadas.
- **[Auditoría MANT.1 R5F — nombres de archivos](archive/technical/AUDITORIA_ARCHIVOS_R5F.md)** — auditoría de nombres de archivos técnicos y referencias sincronizadas.
- **[Auditoría MANT.1 R5G — documentación vigente](archive/technical/AUDITORIA_DOCUMENTACION_R5G.md)** — auditoría de cobertura documental, índice y referencias internas.
- **[Modelo de datos](architecture/data-model.md)** — modelos y contratos.
- **[Gestión de datos de la simulación](product/simulation-data-management.md)** — estado local, limpieza, restauración e invalidación.
- **[Observabilidad y Developer Diagnostics](operations/observability-and-logs.md)** — Developer Diagnostics, esquema JSONL, correlación, redacción, retención y exportación.

## 4. Especificación funcional

- **[Especificación funcional](product/functional-specification.md)** — RF y comportamiento del producto.
- **[Guía interna de desarrollo](operations/development-guide.md)** — convenciones de ingeniería e interfaz.

## 5. Motores previsionales

- **[Motor de cálculo](architecture/calculation-engine.md)** — flujo común de cálculo.
- **[Modalidades de retiro por vejez — SEBD](regulatory/sebd-modalities.md)** — SEBD.
- **[Subsistema Mixto — diseño y alcance del motor](regulatory/mixto-modalities.md)** — Subsistema Mixto.
- **[Sistema Único de Capitalización con Garantía Solidaria (SUCGS)](regulatory/sucgs-modalities.md)** — SUCGS.

## 6. Normativa y fuentes

- **[Normativa](regulatory/regulatory-framework.md)** — interpretación y aplicación normativa.
- **[Fuentes normativas y enlaces oficiales](regulatory/regulatory-sources.md)** — catálogo de fuentes oficiales.
- `../regulations/*.json` — parámetros legales versionados.

## 7. Datos y trazabilidad

- **[Modelo de datos](architecture/data-model.md)** — contratos y procedencia.
- **[Gestión de datos de la simulación](product/simulation-data-management.md)** — ciclo de vida del estado local.
- **[Registro de decisiones técnicas](decisions/README.md)** — decisiones ADR históricas y vigentes.

## 8. Seguridad y privacidad

- **[Seguridad y privacidad](security/security-and-privacy.md)** — controles técnicos.
- **[Modelo de amenazas](security/threat-model.md)** — threat model y matriz de riesgos.
- **[Procedimiento de derechos del titular](security/data-subject-rights-procedure.md)** — ejercicio de derechos.
- **[Procedimiento de respuesta a incidentes de seguridad y privacidad](security/security-incident-procedure.md)** — incident response.
- **[Evaluación de terceros, despliegue y revisión pre-publicación](security/third-party-deployment-assessment.md)** — terceros, TLS y gates de despliegue.
- **[Política de privacidad y tratamiento de datos](security/privacy-policy.md)** — política pública vigente.
- **[Términos de uso, privacidad y tratamiento de datos](security/terms-and-privacy.md)** — términos y tratamiento de datos.
- **[Matriz interna de alineación con Ley 81 de 2019](regulatory/law-81-compliance.md)** — matriz interna de alineación.
- **[Observabilidad y Developer Diagnostics](operations/observability-and-logs.md)** — minimización y manejo local de logs diagnósticos.
- **[Política de seguridad](../SECURITY.md)** — política y canales privados de reporte responsable de vulnerabilidades.

La publicación del repositorio no elimina la revisión jurídica externa ni cualquier diseño de seguridad específico que requiera un futuro despliegue remoto de la aplicación.

## 9. Transparencia, auditoría y trazabilidad

- **[Transparencia del producto](product/transparency.md)** — fronteras de afirmación y transparencia pública.
- **[Matriz de trazabilidad](product/traceability-matrix.md)** — requisito/criterio → ADR → implementación → prueba → estado.
- **[Auditoría de cálculos](archive/technical/AUDITORIA_CALCULOS.md)** — reproducibilidad y revisión de resultados.
- **[UX.4.6h R1 — Auditoría del Paso 6: resultados y exportación](archive/ux/UX46H_R1_AUDITORIA_RESULTADOS.md)** — auditoría de resultados y coherencia visual de UX.4.6h.
- **[Limitaciones conocidas](product/known-limitations.md)** — límites técnicos, normativos y de despliegue.
- **[Dependencias y terceros](operations/third-party-dependencies.md)** — dependencias, licencias upstream, conexiones y riesgos.
- **[Proceso de release](operations/release-process.md)** — gates de cierre, versión, Build, CI y tags.
- **[Auditoría UX.4.6i R1 — Cómo se calcula](archive/ux/UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md)** — auditoría canónica de UX.4.6i; secuencia demostrada R1 → R1.2 → R1.3 → R1.4.

## 10. Validación y calidad

- **[Validación](operations/validation.md)** — estrategia y evidencias.
- [`../tests/test_ver2_ledger_estructurado.py`](../tests/test_ver2_ledger_estructurado.py) — regresiones del ledger JSON y sus invariantes.
- [`../tests/test_ver2_version_revision_aware.py`](../tests/test_ver2_version_revision_aware.py) — regresiones del esquema revision-aware.
- [`../tests/test_ver2_documentacion_vigente.py`](../tests/test_ver2_documentacion_vigente.py) — coherencia de superficies vigentes durante VER.2.
- **[Casos de validación](../tests/validation_cases/README.md)** — reglas de casos sintéticos/anonimizados.
- `../.github/workflows/ci.yml` — CI funcional.
- `../.github/workflows/governance-audit.yml` — auditoría automática de gobierno.
- `../.github/workflows/verificar-tags.yml` — verificación criptográfica de tags.
- `../.github/dependabot.yml` — mantenimiento de dependencias.

## 11. Desarrollo y contribución

- **[Guía de contribución](../CONTRIBUTING.md)** — flujo principal.
- **[Código de conducta](../CODE_OF_CONDUCT.md)** — reglas de convivencia y colaboración.
- **[Soporte](../SUPPORT.md)** — rutas de consulta y reporte.
- **[Guía interna de desarrollo](operations/development-guide.md)** — convenciones internas.
- **[DEV.2 R1/R2/R3/R4 — Centro de desarrollo](architecture/development-center.md)** — cierre documental del centro de desarrollo DEV.2.
- **[Política de estructura de archivos por extensión](standards/file-structure-by-extension.md)** — política vigente de estructura, nombres y ubicación de archivos.
- **[Estándar de código y comentarios](standards/code-and-comments.md)** — patrón permanente de comentarios y docstrings por tecnología.
- [`../.editorconfig`](../.editorconfig) — formato.
- [`../.gitattributes`](../.gitattributes) — normalización Git.
- [`../.gitignore`](../.gitignore) — exclusiones y protección de datos locales.

## 12. Historial de evolución

- **[Registro histórico de cambios](archive/governance/REGISTRO_CAMBIOS_HISTORICO.md)** — mapa cronológico.
- **[UX.4.6a — Rediseño visual integral y nueva página de Inicio](archive/ux/UX_4_6A_REDISENO_VISUAL.md)** — bitácora histórica del rediseño visual UX.4.6a.
- **[UX.4.6b — Simular / Paso 1 · Datos personales](archive/ux/UX_4_6B_PASO1_DATOS_PERSONALES.md)** — bitácora histórica del Paso 1 de UX.4.6b.
- **[UX.4.6c — Simular / Paso 2 · Cuotas](archive/ux/UX_4_6C_PASO2_CUOTAS.md)** — bitácora histórica del Paso 2 de UX.4.6c.
- **[UX.4.6d — Simular / Paso 3 · Historial](archive/ux/UX_4_6D_PASO3_HISTORIAL.md)** — bitácora histórica del Paso 3 de UX.4.6d.
- **[Archivo histórico de documentación](archive/README.md)** — reglas del archivo histórico.
- [Histórico UX](archive/ux) — bitácoras completas de UX.4.6a–d.
- [Histórico técnico](archive/technical) — snapshots técnicos previos.
- [Histórico de normativa, seguridad y privacidad](archive/regulatory-privacy) — snapshots normativos/privacidad previos.
- [Histórico de gobierno y decisiones](archive/governance) — snapshots de decisiones/gobierno.
- **[Changelog](archive/CHANGELOG_PRE_GOV1_3.md)** — snapshot del changelog acumulativo anterior a GOV.1.3.
- **[Roadmap](archive/ROADMAP_PRE_GOV1_3.md)** — snapshot del roadmap anterior a GOV.1.3.

Los archivos históricos documentan lo que se pensó, probó o decidió en un momento determinado. No deben interpretarse como contrato vigente si contradicen un documento actual.

## 13. Releases

- **[Registro de versiones y estados del proyecto](../RELEASES.md)** — registro formal y retrospectivo.
- **[Changelog](../CHANGELOG.md)** — cambios notables.
- **[Política de versionado](../VERSIONING.md)** — reglas de incremento y tags.
- **[Auditoría de versionado pre-1.0](archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md)** — reconciliación VER.2.
- **[Ledger de revisiones aceptadas pre-1.0](governance/pre-1-0-revision-ledger.md)** — contador global.
- [`../data/pre-1-0-revision-ledger.json`](../data/pre-1-0-revision-ledger.json) — representación estructurada del contador.
- **[Plan maestro hacia Mi Retiro Proyectado 1.0](governance/master-plan-to-1-0.md)** — gates hasta la primera versión oficial.

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

- **[Auditoría MANT.1 R5H — nombres técnicos restantes](archive/technical/AUDITORIA_NOMBRES_RESTANTES_R5H.md)** — Auditoría MANT.1 R5H de nombres técnicos restantes.

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

- **[Auditoría de reconciliación VER.2 R1](archive/governance/VER2_R1_AUDITORIA_RECONCILIACION_POST_DOC1.md)**
- **[Matriz de decisión VER.2 R1](archive/governance/VER2_R1_MATRIZ_DECISION_RECONCILIACION_POST_DOC1.md)**
- **[Decisión operativa VER.2 R1](archive/governance/VER2_R1_DECISION_OPERATIVA_POST_DOC1.md)**
## VER.2 R2 — Documentación viva post-R1

- **[Análisis de contradicciones VER.2 R2](archive/governance/VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md)**
- **[Propuesta de corrección de documentación viva VER.2 R2](archive/governance/VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md)**
- **[Cierre de documentación viva VER.2 R2](archive/governance/VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md)**
## VER.2 R3 — Decisión de versión candidata post-R2

- **[Decisión de versión candidata VER.2 R3](archive/governance/VER2_R3_DECISION_VERSION_CANDIDATA_POST_R2.md)**
## VER.2 R4 — Promoción controlada G071/E01

- **[Promoción controlada VER.2 R4 G071/E01](archive/governance/VER2_R4_PROMOCION_G071_E01.md)**

## VER.2 R5 — Estabilización post-release

- **[Estabilización post-release VER.2 R5](archive/governance/VER2_R5_ESTABILIZACION_POST_RELEASE.md)**


**SEC.2 R6:** hardening de sesión administrativa web preparado para despliegue interno controlado.

## NOR.1 R8 — Identificadores de bloques

- **[Identificadores de bloques de trabajo](standards/work-block-identifiers.md)** — política canónica de familias, bloques y revisiones.
- **[NOR.1 R8 — auditoría de identificadores de bloques](audits/repository/work-block-identifier-audit-nor1-r8.md)** — auditoría que justifica NOR.1 R8 y la reserva de G112.
