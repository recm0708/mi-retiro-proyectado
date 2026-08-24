# Índice de documentación

**Estado:** vigente
**Versión de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01 promovida en R4
**Último tag formal legacy:** `v0.0.26-beta`
**Última actualización transversal:** NOR.1 R7 — cierre de estándares y preparación de NOR.2 — 2026-08-24
**Cierres históricos preservados:** UX.4.6i / PR #34 — 841 pruebas; UX.4.6e R9 — `v0.0.25-beta`

Este archivo es el punto de entrada para la documentación técnica, funcional, normativa, de privacidad, validación y auditoría de Mi Retiro Proyectado.


## Estado de normalización del repositorio

- **NOR.1:** cierre en R7; define el contrato estructural y de nomenclatura.
- **NOR.2:** siguiente fase; aplicará esos estándares al árbol existente.
- **SEC.2:** permanece pausado hasta completar NOR.2.
- [`standards/README.md`](standards/README.md) — índice de estándares canónicos.
- [`audits/repository/repository-standards-closure-nor1-r7.md`](audits/repository/repository-standards-closure-nor1-r7.md) — evidencia y gate de transición NOR.1 → NOR.2.

## 1. Producto y alcance

- [`../README.md`](../README.md) — presentación, alcance, instalación y estado general.
- [`ESPECIFICACION_FUNCIONAL.md`](ESPECIFICACION_FUNCIONAL.md) — requisitos funcionales.
- [`ROADMAP.md`](ROADMAP.md) — estado actual y próximos hitos.
- [`PLAN_MAESTRO_HACIA_1_0.md`](PLAN_MAESTRO_HACIA_1_0.md) — secuencia transversal de 14 bloques hasta la primera versión oficial.
- [`IDENTIDAD_VISUAL.md`](IDENTIDAD_VISUAL.md) — logo oficial, activos canónicos, favicons y Social Preview.
- [`COMO_SE_CALCULA.md`](COMO_SE_CALCULA.md) — contrato público de explicación de SEBD, Mixto y SUCGS sin duplicar motores.

## 2. Gobierno y versionado

- [`../GOVERNANCE.md`](../GOVERNANCE.md) — gobierno del proyecto.
- [`../VERSIONING.md`](../VERSIONING.md) — política legacy, beta revision-aware `0.GG.RR.EE-beta`, versión oficial de cuatro componentes y Build independiente.
- [`../VERSION`](../VERSION) — fuente canónica de la versión candidata de aplicación.
- [`AUDITORIA_VERSIONADO_PRE_1_0.md`](AUDITORIA_VERSIONADO_PRE_1_0.md) — auditoría del historial, criterio contable y exclusiones de VER.2.
- [`ADR_179_VERSIONADO_REVISION_AWARE.md`](ADR_179_VERSIONADO_REVISION_AWARE.md) — decisión ADR del esquema revision-aware previo a `1.0.0.0`.
- [`AUDITORIA_VER2_SEGUNDA_PASADA.md`](AUDITORIA_VER2_SEGUNDA_PASADA.md) — bitácora de la segunda pasada y correcciones sobre la primera reconstrucción.
- [`AUDITORIA_VER2_CONTEO_PROVISIONAL.md`](AUDITORIA_VER2_CONTEO_PROVISIONAL.md) — cierre del conteo de segunda pasada en G070 antes de VER.2.
- [`MATRIZ_DECISION_REVISIONES_VER2.md`](MATRIZ_DECISION_REVISIONES_VER2.md) — decisión fila por fila sobre qué consume Global y por qué.
- [`LEDGER_REVISIONES_PRE_1_0.md`](LEDGER_REVISIONES_PRE_1_0.md) — ledger Markdown G001–G070 y candidato G071.
- [`../data/revision_ledger_pre_1_0.json`](../data/revision_ledger_pre_1_0.json) — ledger machine-readable canónico de la reconstrucción.
- [`../app/core/version_ledger.py`](../app/core/version_ledger.py) — validador de continuidad, unicidad y codificación del ledger estructurado.
- [`../RELEASES.md`](../RELEASES.md) — versiones, tags y reconstrucción histórica.
- [`../CHANGELOG.md`](../CHANGELOG.md) — cambios notables por versión.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — flujo de contribución.
- [`../CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md) — normas de participación.
- [`../SUPPORT.md`](../SUPPORT.md) — canales de soporte, privacidad y seguridad.
- [`PLAN_MAESTRO_HACIA_1_0.md`](PLAN_MAESTRO_HACIA_1_0.md) — dependencias y gates previos a `1.0.0.0`.
- [`MIGRACION_FIRMAS_GIT_2026-08-17.md`](MIGRACION_FIRMAS_GIT_2026-08-17.md) — firma SSH y migración histórica controlada.
- [`../.github/allowed_signers`](../.github/allowed_signers) — claves públicas autorizadas.
- [`AUDITORIA_GITHUB.md`](AUDITORIA_GITHUB.md) — controles GitHub, seguridad y auditoría automática.
- [`PREPARACION_PUBLICA_GITHUB.md`](PREPARACION_PUBLICA_GITHUB.md) — metadata, topics, labels, badges, Social Preview y seguridad del repositorio público.
- [`AUDITORIA_REPOSITORIO_2026-08-18.md`](AUDITORIA_REPOSITORIO_2026-08-18.md) — auditoría integral local/remota post-GOV.1.
- [`AUDITORIA_UX46E_R7_2026-08-18.md`](AUDITORIA_UX46E_R7_2026-08-18.md) — auditoría transversal de coherencia de UX.4.6e.
- [`AUDITORIA_PLAN1_R4_2026-08-20.md`](AUDITORIA_PLAN1_R4_2026-08-20.md) — auditoría integral y gates R4.1/R4.2 de PLAN.1.
- [`CIERRE_GOV1.md`](CIERRE_GOV1.md) — evidencia definitiva del cierre GOV.1.
- [`../LICENSE`](../LICENSE) — licencia propietaria de materiales originales.
- [`LICENCIA_Y_DISTRIBUCION.md`](LICENCIA_Y_DISTRIBUCION.md) — evaluación y decisión de licencia.
- [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) — avisos de componentes de terceros.

## 3. Arquitectura

- [`ARQUITECTURA.md`](ARQUITECTURA.md) — capas, módulos, endpoints y flujo.
- [`AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md`](AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md) — auditoría de política y plantillas por extensión.
- [`AUDITORIA_CARPETAS_R5E.md`](AUDITORIA_CARPETAS_R5E.md) — auditoría de nombres de carpetas técnicas y rutas sincronizadas.
- [`AUDITORIA_ARCHIVOS_R5F.md`](AUDITORIA_ARCHIVOS_R5F.md) — auditoría de nombres de archivos técnicos y referencias sincronizadas.
- [`AUDITORIA_DOCUMENTACION_R5G.md`](AUDITORIA_DOCUMENTACION_R5G.md) — auditoría de cobertura documental, índice y referencias internas.
- [`MODELO_DE_DATOS.md`](MODELO_DE_DATOS.md) — modelos y contratos.
- [`GESTION_DATOS_SIMULACION.md`](GESTION_DATOS_SIMULACION.md) — estado local, limpieza, restauración e invalidación.
- [`OBSERVABILIDAD_LOGS.md`](OBSERVABILIDAD_LOGS.md) — Developer Diagnostics, esquema JSONL, correlación, redacción, retención y exportación.

## 4. Especificación funcional

- [`ESPECIFICACION_FUNCIONAL.md`](ESPECIFICACION_FUNCIONAL.md) — RF y comportamiento del producto.
- [`GUIA_INTERNA_DESARROLLO.md`](GUIA_INTERNA_DESARROLLO.md) — convenciones de ingeniería e interfaz.

## 5. Motores previsionales

- [`MOTOR_DE_CALCULO.md`](MOTOR_DE_CALCULO.md) — flujo común de cálculo.
- [`MODALIDADES_SEBD.md`](MODALIDADES_SEBD.md) — SEBD.
- [`MODALIDADES_MIXTO.md`](MODALIDADES_MIXTO.md) — Subsistema Mixto.
- [`MODALIDADES_SUCGS.md`](MODALIDADES_SUCGS.md) — SUCGS.

## 6. Normativa y fuentes

- [`NORMATIVA.md`](NORMATIVA.md) — interpretación y aplicación normativa.
- [`FUENTES_NORMATIVAS.md`](FUENTES_NORMATIVAS.md) — catálogo de fuentes oficiales.
- `../regulations/*.json` — parámetros legales versionados.

## 7. Datos y trazabilidad

- [`MODELO_DE_DATOS.md`](MODELO_DE_DATOS.md) — contratos y procedencia.
- [`GESTION_DATOS_SIMULACION.md`](GESTION_DATOS_SIMULACION.md) — ciclo de vida del estado local.
- [`DECISIONES.md`](DECISIONES.md) — decisiones ADR históricas y vigentes.

## 8. Seguridad y privacidad

- [`SEGURIDAD_PRIVACIDAD.md`](SEGURIDAD_PRIVACIDAD.md) — controles técnicos.
- [`MODELO_AMENAZAS.md`](MODELO_AMENAZAS.md) — threat model y matriz de riesgos.
- [`PROCEDIMIENTO_DERECHOS_TITULAR.md`](PROCEDIMIENTO_DERECHOS_TITULAR.md) — ejercicio de derechos.
- [`PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md`](PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md) — incident response.
- [`EVALUACION_TERCEROS_DESPLIEGUE.md`](EVALUACION_TERCEROS_DESPLIEGUE.md) — terceros, TLS y gates de despliegue.
- [`POLITICA_PRIVACIDAD.md`](POLITICA_PRIVACIDAD.md) — política pública vigente.
- [`TERMINOS_USO_PRIVACIDAD.md`](TERMINOS_USO_PRIVACIDAD.md) — términos y tratamiento de datos.
- [`CUMPLIMIENTO_LEY_81.md`](CUMPLIMIENTO_LEY_81.md) — matriz interna de alineación.
- [`OBSERVABILIDAD_LOGS.md`](OBSERVABILIDAD_LOGS.md) — minimización y manejo local de logs diagnósticos.
- [`../SECURITY.md`](../SECURITY.md) — política y canales privados de reporte responsable de vulnerabilidades.

La publicación del repositorio no elimina la revisión jurídica externa ni cualquier diseño de seguridad específico que requiera un futuro despliegue remoto de la aplicación.

## 9. Transparencia, auditoría y trazabilidad

- [`TRANSPARENCIA.md`](TRANSPARENCIA.md) — fronteras de afirmación y transparencia pública.
- [`MATRIZ_TRAZABILIDAD.md`](MATRIZ_TRAZABILIDAD.md) — requisito/criterio → ADR → implementación → prueba → estado.
- [`AUDITORIA_CALCULOS.md`](AUDITORIA_CALCULOS.md) — reproducibilidad y revisión de resultados.
- [`UX46H_R1_AUDITORIA_RESULTADOS.md`](UX46H_R1_AUDITORIA_RESULTADOS.md) — auditoría de resultados y coherencia visual de UX.4.6h.
- [`LIMITACIONES_CONOCIDAS.md`](LIMITACIONES_CONOCIDAS.md) — límites técnicos, normativos y de despliegue.
- [`DEPENDENCIAS_TERCEROS.md`](DEPENDENCIAS_TERCEROS.md) — dependencias, licencias upstream, conexiones y riesgos.
- [`PROCESO_RELEASE.md`](PROCESO_RELEASE.md) — gates de cierre, versión, Build, CI y tags.
- [`UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md`](UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md) — auditoría canónica de UX.4.6i; secuencia demostrada R1 → R1.2 → R1.3 → R1.4.

## 10. Validación y calidad

- [`VALIDACION.md`](VALIDACION.md) — estrategia y evidencias.
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
- [`GUIA_INTERNA_DESARROLLO.md`](GUIA_INTERNA_DESARROLLO.md) — convenciones internas.
- [`DEV2_CENTRO_DESARROLLO.md`](DEV2_CENTRO_DESARROLLO.md) — cierre documental del centro de desarrollo DEV.2.
- [`POLITICA_ESTRUCTURA_ARCHIVOS.md`](POLITICA_ESTRUCTURA_ARCHIVOS.md) — política vigente de estructura, nombres y ubicación de archivos.
- [`ESTANDAR_CODIGO_Y_COMENTARIOS.md`](ESTANDAR_CODIGO_Y_COMENTARIOS.md) — patrón permanente de comentarios y docstrings por tecnología.
- [`../.editorconfig`](../.editorconfig) — formato.
- [`../.gitattributes`](../.gitattributes) — normalización Git.
- [`../.gitignore`](../.gitignore) — exclusiones y protección de datos locales.

## 12. Historial de evolución

- [`REGISTRO_CAMBIOS_HISTORICO.md`](REGISTRO_CAMBIOS_HISTORICO.md) — mapa cronológico.
- [`UX_4_6A_REDISENO_VISUAL.md`](UX_4_6A_REDISENO_VISUAL.md) — auditoría histórica de rediseño visual UX.4.6a.
- [`UX_4_6B_PASO1_DATOS_PERSONALES.md`](UX_4_6B_PASO1_DATOS_PERSONALES.md) — auditoría histórica del Paso 1 de UX.4.6b.
- [`UX_4_6C_PASO2_CUOTAS.md`](UX_4_6C_PASO2_CUOTAS.md) — auditoría histórica del Paso 2 de UX.4.6c.
- [`UX_4_6D_PASO3_HISTORIAL.md`](UX_4_6D_PASO3_HISTORIAL.md) — auditoría histórica del Paso 3 de UX.4.6d.
- [`archive/README.md`](archive/README.md) — reglas del archivo histórico.
- [`archive/ux/`](archive/ux/) — bitácoras completas de UX.4.6a–d.
- [`archive/technical/`](archive/technical/) — snapshots técnicos previos.
- [`archive/regulatory-privacy/`](archive/regulatory-privacy/) — snapshots normativos/privacidad previos.
- [`archive/governance/`](archive/governance/) — snapshots de decisiones/gobierno.
- [`archive/CHANGELOG_PRE_GOV1_3.md`](archive/CHANGELOG_PRE_GOV1_3.md) — snapshot del changelog acumulativo anterior a GOV.1.3.
- [`archive/ROADMAP_PRE_GOV1_3.md`](archive/ROADMAP_PRE_GOV1_3.md) — snapshot del roadmap anterior a GOV.1.3.

Los archivos históricos documentan lo que se pensó, probó o decidió en un momento determinado. No deben interpretarse como contrato vigente si contradicen un documento actual.

## 13. Releases

- [`../RELEASES.md`](../RELEASES.md) — registro formal y retrospectivo.
- [`../CHANGELOG.md`](../CHANGELOG.md) — cambios notables.
- [`../VERSIONING.md`](../VERSIONING.md) — reglas de incremento y tags.
- [`AUDITORIA_VERSIONADO_PRE_1_0.md`](AUDITORIA_VERSIONADO_PRE_1_0.md) — reconciliación VER.2.
- [`LEDGER_REVISIONES_PRE_1_0.md`](LEDGER_REVISIONES_PRE_1_0.md) — contador global.
- [`../data/revision_ledger_pre_1_0.json`](../data/revision_ledger_pre_1_0.json) — representación estructurada del contador.
- [`PLAN_MAESTRO_HACIA_1_0.md`](PLAN_MAESTRO_HACIA_1_0.md) — gates hasta la primera versión oficial.

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

- [AUDITORIA_NOMBRES_RESTANTES_R5H.md](AUDITORIA_NOMBRES_RESTANTES_R5H.md) — Auditoría MANT.1 R5H de nombres técnicos restantes.

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

- [Auditoría de reconciliación VER.2 R1](VER2_R1_AUDITORIA_RECONCILIACION_POST_DOC1.md)
- [Matriz de decisión VER.2 R1](VER2_R1_MATRIZ_DECISION_RECONCILIACION_POST_DOC1.md)
- [Decisión operativa VER.2 R1](VER2_R1_DECISION_OPERATIVA_POST_DOC1.md)
## VER.2 R2 — Documentación viva post-R1

- [Análisis de contradicciones VER.2 R2](VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md)
- [Propuesta de corrección de documentación viva VER.2 R2](VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md)
- [Cierre de documentación viva VER.2 R2](VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md)
## VER.2 R3 — Decisión de versión candidata post-R2

- [Decisión de versión candidata VER.2 R3](VER2_R3_DECISION_VERSION_CANDIDATA_POST_R2.md)
## VER.2 R4 — Promoción controlada G071/E01

- [Promoción controlada VER.2 R4 G071/E01](VER2_R4_PROMOCION_G071_E01.md)

## VER.2 R5 — Estabilización post-release

- [Estabilización post-release VER.2 R5](VER2_R5_ESTABILIZACION_POST_RELEASE.md)
