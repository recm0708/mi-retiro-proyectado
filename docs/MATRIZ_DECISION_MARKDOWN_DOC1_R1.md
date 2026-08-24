# DOC.1 R1 — Matriz de decisión Markdown post-MANT.1

## Resumen

- Total Markdown evaluados: `107`

- `ACTUALIZAR`: `15`
- `PRESERVAR_AUDITORIA_CERRADA`: `25`
- `PRESERVAR_HISTORICO`: `27`
- `REVISAR_MANUALMENTE`: `8`
- `REVISAR_SOLO_SI_APLICA`: `7`
- `SIN_CAMBIO_INICIAL`: `25`

## Criterio

- `ACTUALIZAR`: documento vigente que debe quedar alineado al cierre de MANT.1 R7.
- `REVISAR_MANUALMENTE`: documento vigente con señales automáticas; se inspecciona antes de editar.
- `PRESERVAR_AUDITORIA_CERRADA`: evidencia de auditorías, cierres o ADR; no se reescribe como estado vigente.
- `PRESERVAR_HISTORICO`: documentación archivada; se conserva como evidencia histórica.
- `REVISAR_SOLO_SI_APLICA`: soporte o política general; solo se edita si hay desfase real.
- `SIN_CAMBIO_INICIAL`: sin señales automáticas suficientes.

## Matriz

| Decisión | Archivo | Primera línea | Señales | Motivo |
|---|---|---|---|---|
| `REVISAR_SOLO_SI_APLICA` | `.githooks/README.md` | # Hooks Git versionados | — | Documento de soporte; actualizar solo si contiene instrucciones obsoletas. |
| `REVISAR_SOLO_SI_APLICA` | `.github/pull_request_template.md` | ## Resumen | — | Documento de soporte; actualizar solo si contiene instrucciones obsoletas. |
| `ACTUALIZAR` | `CHANGELOG.md` | # Changelog | Siguiente bloque funcional, Siguiente bloque, 0\.0\.71\.01-beta, VER\.2, MANT\.1, R5H, R6, R7 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `REVISAR_SOLO_SI_APLICA` | `CODE_OF_CONDUCT.md` | # Código de conducta | — | Documento raíz vigente, pero sin señal fuerte de desfase operativo. |
| `ACTUALIZAR` | `CONTRIBUTING.md` | # Guía de contribución | — | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/ADR_179_VERSIONADO_REVISION_AWARE.md` | # ADR-179 — El versionado beta usa un ledger de estados aceptados y no cuenta commits como revisiones | VER\.2 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_HISTORICO` | `docs/archive/CHANGELOG_PRE_GOV1_3.md` | ### GOV.1.2 — Gobierno y versionado | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/governance/DECISIONES_PRE_GOV1_3_R4.md` | # Registro de decisiones técnicas | R6, R7 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/governance/README.md` | # Histórico de gobierno y decisiones | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/README.md` | # Archivo histórico de documentación | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/regulatory-privacy/CUMPLIMIENTO_LEY_81_PRE_GOV1_3_R3.md` | # Matriz interna de alineación con Ley 81 de 2019 | R6, R7 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/regulatory-privacy/FUENTES_NORMATIVAS_PRE_GOV1_3_R3.md` | # Fuentes normativas y enlaces oficiales | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/regulatory-privacy/MODALIDADES_MIXTO_PRE_GOV1_3_R3.md` | # Subsistema Mixto — diseño y alcance del motor | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/regulatory-privacy/MODALIDADES_SEBD_PRE_GOV1_3_R3.md` | # Modalidades de retiro por vejez — SEBD | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/regulatory-privacy/MODALIDADES_SUCGS_PRE_GOV1_3_R3.md` | # Sistema Único de Capitalización con Garantía Solidaria (SUCGS) | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/regulatory-privacy/NORMATIVA_PRE_GOV1_3_R3.md` | # Normativa | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/regulatory-privacy/POLITICA_PRIVACIDAD_PRE_GOV1_3_R3.md` | # Política de privacidad y tratamiento de datos | R6 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/regulatory-privacy/README.md` | # Histórico de normativa, seguridad y privacidad | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/regulatory-privacy/SEGURIDAD_PRIVACIDAD_PRE_GOV1_3_R3.md` | # Seguridad y privacidad | R6, R7 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/regulatory-privacy/TERMINOS_USO_PRIVACIDAD_PRE_GOV1_3_R3.md` | # Términos de uso, privacidad y tratamiento de datos | R6 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/ROADMAP_PRE_GOV1_3.md` | # Roadmap | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/technical/ARQUITECTURA_PRE_GOV1_3_R2.md` | # Arquitectura | R6, R7 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/technical/ESPECIFICACION_FUNCIONAL_PRE_GOV1_3_R2.md` | # Especificación funcional | R6, R7 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/technical/GESTION_DATOS_SIMULACION_PRE_GOV1_3_R2.md` | # Gestión de datos de la simulación | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/technical/GUIA_INTERNA_DESARROLLO_PRE_GOV1_3_R2.md` | # Guía interna de desarrollo | R6 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/technical/MODELO_DE_DATOS_PRE_GOV1_3_R2.md` | # Modelo de datos | R6 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/technical/MOTOR_DE_CALCULO_PRE_GOV1_3_R2.md` | # Motor de cálculo | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/technical/README.md` | # Histórico técnico pre-GOV.1.3 R2 | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/technical/VALIDACION_PRE_GOV1_3_R2.md` | # Validación | Siguiente bloque, R6, R7 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/ux/UX_4_6A_REDISENO_VISUAL.md` | # UX.4.6a — Rediseño visual integral y nueva página de Inicio | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/ux/UX_4_6B_PASO1_DATOS_PERSONALES.md` | # UX.4.6b — Simular / Paso 1 · Datos personales | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/ux/UX_4_6C_PASO2_CUOTAS.md` | # UX.4.6c — Simular / Paso 2 · Cuotas | — | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `PRESERVAR_HISTORICO` | `docs/archive/ux/UX_4_6D_PASO3_HISTORIAL.md` | # UX.4.6d — Simular / Paso 3 · Historial | R6, R7 | Evidencia histórica archivada; no debe reescribirse como estado vigente. |
| `ACTUALIZAR` | `docs/ARQUITECTURA.md` | # Arquitectura | VER\.2, MANT\.1 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_ARCHIVOS_R5F.md` | # Auditoría MANT.1 R5F — nombres de archivos | MANT\.1 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_CALCULOS.md` | # Auditoría de cálculos | — | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_CARPETAS_R5E.md` | # Auditoría de nombres de carpetas — MANT.1 R5E | MANT\.1 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_DOCUMENTACION_R5G.md` | # Auditoría MANT.1 R5G — documentación vigente | MANT\.1 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md` | # Auditoría de estructura por extensión | — | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md` | # MANT.1 R6 — Auditoría funcional post-renombres | MANT\.1, R6 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_GITHUB.md` | # Auditoría de GitHub y controles de repositorio | — | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_MARKDOWN_POST_MANT1_DOC1_R1.md` | # DOC.1 R1 — Inventario Markdown post-MANT.1 | Siguiente bloque, VER\.2, MANT\.1, R5H, R6, R7 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_NOMBRES_RESTANTES_R5H.md` | # Auditoría MANT.1 R5H — nombres técnicos restantes | MANT\.1, R5H | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_PLAN1_R4_2026-08-20.md` | # Auditoría integral PLAN.1 R4 | Siguiente bloque funcional, Siguiente bloque | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_REPOSITORIO_2026-08-18.md` | # Auditoría integral del repositorio — 2026-08-18 | R7 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_UX46E_R7_2026-08-18.md` | # Auditoría transversal UX.4.6e R7 | R6, R7 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_VER2_CONTEO_PROVISIONAL.md` | # VER.2 — Conteo de segunda pasada | VER\.2 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_VER2_SEGUNDA_PASADA.md` | # VER.2 — Segunda pasada de auditoría cruzada | todavía pendiente, VER\.2, R6, R7 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/AUDITORIA_VERSIONADO_PRE_1_0.md` | # Auditoría de versionado pre-1.0 | todavía pendiente, 0\.0\.71\.01-beta, VER\.2, R7 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/CIERRE_GOV1.md` | # Cierre GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta | R6 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/CIERRE_OPERATIVO_POST_AUDITORIA_R7.md` | # MANT.1 R7 — Cierre operativo post-auditoría | MANT\.1, R5H, R6, R7 | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `SIN_CAMBIO_INICIAL` | `docs/COMO_SE_CALCULA.md` | # Cómo se calcula — contrato de transparencia | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/CUMPLIMIENTO_LEY_81.md` | # Matriz interna de alineación con Ley 81 de 2019 | — | Sin señales automáticas suficientes. |
| `REVISAR_MANUALMENTE` | `docs/DECISIONES.md` | # Registro de decisiones técnicas | R6, R7 | Documento vigente con señales de estado/versionado que pueden requerir ajuste. |
| `SIN_CAMBIO_INICIAL` | `docs/DEPENDENCIAS_TERCEROS.md` | # Dependencias y terceros | — | Sin señales automáticas suficientes. |
| `REVISAR_MANUALMENTE` | `docs/DEV2_CENTRO_DESARROLLO.md` | # DEV.2 R1/R2/R3/R4 — Centro de desarrollo | VER\.2 | Documento vigente con señales de estado/versionado que pueden requerir ajuste. |
| `ACTUALIZAR` | `docs/ESPECIFICACION_FUNCIONAL.md` | # Especificación funcional | R6, R7 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `REVISAR_MANUALMENTE` | `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md` | # Estándar de código y comentarios | MANT\.1 | Documento vigente con señales de estado/versionado que pueden requerir ajuste. |
| `SIN_CAMBIO_INICIAL` | `docs/EVALUACION_TERCEROS_DESPLIEGUE.md` | # Evaluación de terceros, despliegue y revisión pre-publicación | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/FUENTES_NORMATIVAS.md` | # Fuentes normativas y enlaces oficiales | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/GESTION_DATOS_SIMULACION.md` | # Gestión de datos de la simulación | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/GUIA_INTERNA_DESARROLLO.md` | # Guía interna de desarrollo | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/IDENTIDAD_VISUAL.md` | # Identidad visual de Mi Retiro Proyectado | — | Sin señales automáticas suficientes. |
| `ACTUALIZAR` | `docs/INDICE.md` | # Índice de documentación | 0\.0\.71\.01-beta, VER\.2, MANT\.1, R5H, R6, R7 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `REVISAR_MANUALMENTE` | `docs/LEDGER_REVISIONES_PRE_1_0.md` | # Ledger de revisiones aceptadas pre-1.0 | 0\.0\.71\.01-beta, VER\.2, R6, R7 | Documento vigente con señales de estado/versionado que pueden requerir ajuste. |
| `SIN_CAMBIO_INICIAL` | `docs/LICENCIA_Y_DISTRIBUCION.md` | # Licencia y estrategia de distribución | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/LIMITACIONES_CONOCIDAS.md` | # Limitaciones conocidas | — | Sin señales automáticas suficientes. |
| `REVISAR_MANUALMENTE` | `docs/MATRIZ_DECISION_REVISIONES_VER2.md` | # VER.2 — Matriz de decisión de revisiones aceptadas | VER\.2, R6, R7 | Documento vigente con señales de estado/versionado que pueden requerir ajuste. |
| `ACTUALIZAR` | `docs/MATRIZ_TRAZABILIDAD.md` | # Matriz de trazabilidad | 0\.0\.71\.01-beta, VER\.2 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/MIGRACION_FIRMAS_GIT_2026-08-17.md` | # Migración de firma criptográfica Git — 2026-08-17 | — | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `SIN_CAMBIO_INICIAL` | `docs/MODALIDADES_MIXTO.md` | # Subsistema Mixto — diseño y alcance del motor | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/MODALIDADES_SEBD.md` | # Modalidades de retiro por vejez — SEBD | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/MODALIDADES_SUCGS.md` | # Sistema Único de Capitalización con Garantía Solidaria (SUCGS) | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/MODELO_AMENAZAS.md` | # Modelo de amenazas | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/MODELO_DE_DATOS.md` | # Modelo de datos | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/MOTOR_DE_CALCULO.md` | # Motor de cálculo | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/NORMATIVA.md` | # Normativa | — | Sin señales automáticas suficientes. |
| `REVISAR_MANUALMENTE` | `docs/OBSERVABILIDAD_LOGS.md` | # Observabilidad y Developer Diagnostics | Siguiente bloque | Documento vigente con señales de estado/versionado que pueden requerir ajuste. |
| `ACTUALIZAR` | `docs/PLAN_MAESTRO_HACIA_1_0.md` | # Plan maestro hacia Mi Retiro Proyectado 1.0 | Siguiente bloque funcional, Siguiente bloque, 0\.0\.71\.01-beta, VER\.2 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `SIN_CAMBIO_INICIAL` | `docs/POLITICA_ESTRUCTURA_ARCHIVOS.md` | # Política de estructura de archivos por extensión | — | Sin señales automáticas suficientes. |
| `REVISAR_MANUALMENTE` | `docs/POLITICA_PRIVACIDAD.md` | # Política de privacidad y tratamiento de datos | R6 | Documento vigente con señales de estado/versionado que pueden requerir ajuste. |
| `SIN_CAMBIO_INICIAL` | `docs/PREPARACION_PUBLICA_GITHUB.md` | # Preparación pública de GitHub | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/PROCEDIMIENTO_DERECHOS_TITULAR.md` | # Procedimiento de derechos del titular | — | Sin señales automáticas suficientes. |
| `SIN_CAMBIO_INICIAL` | `docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md` | # Procedimiento de respuesta a incidentes de seguridad y privacidad | — | Sin señales automáticas suficientes. |
| `ACTUALIZAR` | `docs/PROCESO_RELEASE.md` | # Proceso de release | todavía pendiente, 0\.0\.71\.01-beta, VER\.2 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `SIN_CAMBIO_INICIAL` | `docs/REGISTRO_CAMBIOS_HISTORICO.md` | # Registro histórico de cambios | — | Sin señales automáticas suficientes. |
| `ACTUALIZAR` | `docs/ROADMAP.md` | # Roadmap | Bloque transversal activo, 0\.0\.71\.01-beta, VER\.2, MANT\.1, R6, R7 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `SIN_CAMBIO_INICIAL` | `docs/SEGURIDAD_PRIVACIDAD.md` | # Seguridad y privacidad | — | Sin señales automáticas suficientes. |
| `REVISAR_SOLO_SI_APLICA` | `docs/templates/file-structure/README.md` | # Plantillas de estructura por extensión | — | Documento de soporte; actualizar solo si contiene instrucciones obsoletas. |
| `SIN_CAMBIO_INICIAL` | `docs/TERMINOS_USO_PRIVACIDAD.md` | # Términos de uso, privacidad y tratamiento de datos | — | Sin señales automáticas suficientes. |
| `REVISAR_MANUALMENTE` | `docs/TRANSPARENCIA.md` | # Transparencia del producto | todavía pendiente | Documento vigente con señales de estado/versionado que pueden requerir ajuste. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/UX46H_R1_AUDITORIA_RESULTADOS.md` | # UX.4.6h R1 — Auditoría del Paso 6: resultados y exportación | Siguiente bloque | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md` | # Auditoría UX.4.6i R1 — Cómo se calcula | Siguiente bloque | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/UX_4_6A_REDISENO_VISUAL.md` | # UX.4.6a — Rediseño visual integral y nueva página de Inicio | — | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/UX_4_6B_PASO1_DATOS_PERSONALES.md` | # UX.4.6b — Simular / Paso 1 · Datos personales | — | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/UX_4_6C_PASO2_CUOTAS.md` | # UX.4.6c — Simular / Paso 2 · Cuotas | — | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `PRESERVAR_AUDITORIA_CERRADA` | `docs/UX_4_6D_PASO3_HISTORIAL.md` | # UX.4.6d — Simular / Paso 3 · Historial | — | Documento de auditoría/cierre; preservar como evidencia del momento. |
| `ACTUALIZAR` | `docs/VALIDACION.md` | # Validación | MANT\.1, R5H, R6, R7 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `ACTUALIZAR` | `GOVERNANCE.md` | # Gobierno del proyecto | — | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `ACTUALIZAR` | `README.md` | <p align="center"> | Bloque transversal activo, Bloque transversal pendiente, Siguiente bloque funcional, Siguiente bloque, todavía pendiente, pendiente de integración final, 0\.0\. | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `ACTUALIZAR` | `RELEASES.md` | # Registro de versiones y estados del proyecto | 0\.0\.71\.01-beta, VER\.2 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `REVISAR_SOLO_SI_APLICA` | `scripts/README.md` | # Scripts del repositorio | — | Documento de soporte; actualizar solo si contiene instrucciones obsoletas. |
| `ACTUALIZAR` | `SECURITY.md` | # Política de seguridad | 0\.0\.71\.01-beta, VER\.2 | Documento vigente de entrada, estado, proceso o trazabilidad. |
| `REVISAR_SOLO_SI_APLICA` | `SUPPORT.md` | # Soporte | — | Documento raíz vigente, pero sin señal fuerte de desfase operativo. |
| `SIN_CAMBIO_INICIAL` | `tests/validation_cases/README.md` | # Casos de validación | — | Sin señales automáticas suficientes. |
| `REVISAR_SOLO_SI_APLICA` | `THIRD_PARTY_NOTICES.md` | # Third-party notices | — | Documento raíz vigente, pero sin señal fuerte de desfase operativo. |
| `ACTUALIZAR` | `VERSIONING.md` | # Política de versionado | 0\.0\.71\.01-beta, VER\.2 | Documento vigente de entrada, estado, proceso o trazabilidad. |
