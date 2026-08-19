# Índice de documentación

**Estado:** vigente
**Versión de aplicación revisada:** `0.0.24-beta`
**Última actualización transversal:** saneamiento de repositorio post-GOV.1 — 2026-08-18

Este archivo es el punto de entrada para la documentación técnica, funcional, normativa, de privacidad, validación y auditoría de Mi Retiro Proyectado.

## 1. Producto y alcance

- [`../README.md`](../README.md) — presentación, alcance, instalación y estado general.
- [`ESPECIFICACION_FUNCIONAL.md`](ESPECIFICACION_FUNCIONAL.md) — requisitos funcionales.
- [`ROADMAP.md`](ROADMAP.md) — estado actual y próximos hitos.

## 2. Gobierno y versionado

- [`../GOVERNANCE.md`](../GOVERNANCE.md) — gobierno del proyecto.
- [`../VERSIONING.md`](../VERSIONING.md) — política de versiones.
- [`../VERSION`](../VERSION) — fuente canónica de versión.
- [`../RELEASES.md`](../RELEASES.md) — versiones, tags y reconstrucción histórica.
- [`../CHANGELOG.md`](../CHANGELOG.md) — cambios notables por versión.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — flujo de contribución.
- [`../CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md) — normas de participación.
- [`../SUPPORT.md`](../SUPPORT.md) — canales de soporte, privacidad y seguridad.
- [`MIGRACION_FIRMAS_GIT_2026-08-17.md`](MIGRACION_FIRMAS_GIT_2026-08-17.md) — firma SSH y migración histórica controlada.
- [`../.github/allowed_signers`](../.github/allowed_signers) — claves públicas autorizadas.
- [`AUDITORIA_GITHUB.md`](AUDITORIA_GITHUB.md) — controles GitHub y auditoría automática.
- [`AUDITORIA_REPOSITORIO_2026-08-18.md`](AUDITORIA_REPOSITORIO_2026-08-18.md) — auditoría integral local/remota post-GOV.1.
- [`CIERRE_GOV1.md`](CIERRE_GOV1.md) — evidencia definitiva del cierre GOV.1.
- [`../LICENSE`](../LICENSE) — licencia propietaria de materiales originales.
- [`LICENCIA_Y_DISTRIBUCION.md`](LICENCIA_Y_DISTRIBUCION.md) — evaluación y decisión de licencia.
- [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) — avisos de componentes de terceros.

## 3. Arquitectura

- [`ARQUITECTURA.md`](ARQUITECTURA.md) — capas, módulos, endpoints y flujo.
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
- `../normativa/*.json` — parámetros legales versionados.

## 7. Datos y trazabilidad

- [`MODELO_DE_DATOS.md`](MODELO_DE_DATOS.md) — contratos y procedencia.
- [`GESTION_DATOS_SIMULACION.md`](GESTION_DATOS_SIMULACION.md) — ciclo de vida del estado local.
- [`DECISIONES.md`](DECISIONES.md) — decisiones ADR.

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
- [`../SECURITY.md`](../SECURITY.md) — política y canal de reporte responsable de vulnerabilidades.

GOV.1.3 R3 consolidó originalmente el bloque normativo, de seguridad y privacidad; GOV.1.4 actualiza únicamente el contrato de observabilidad.

GOV.1.5 completa los procedimientos internos; la revisión jurídica externa y cualquier diseño de despliegue remoto permanecen como gates pre-publicación.

## 9. Transparencia, auditoría y trazabilidad

- [`TRANSPARENCIA.md`](TRANSPARENCIA.md) — fronteras de afirmación y transparencia pública.
- [`MATRIZ_TRAZABILIDAD.md`](MATRIZ_TRAZABILIDAD.md) — requisito/criterio → ADR → implementación → prueba → estado.
- [`AUDITORIA_CALCULOS.md`](AUDITORIA_CALCULOS.md) — reproducibilidad y revisión de resultados.
- [`LIMITACIONES_CONOCIDAS.md`](LIMITACIONES_CONOCIDAS.md) — límites técnicos, normativos y de despliegue.
- [`DEPENDENCIAS_TERCEROS.md`](DEPENDENCIAS_TERCEROS.md) — dependencias, licencias upstream, conexiones y riesgos.
- [`PROCESO_RELEASE.md`](PROCESO_RELEASE.md) — gates de cierre, versión, CI y tags.

## 10. Validación y calidad

- [`VALIDACION.md`](VALIDACION.md) — estrategia y evidencias.
- [`../tests/casos_validacion/README.md`](../tests/casos_validacion/README.md) — reglas de casos sintéticos/anonimizados.
- `../.github/workflows/ci.yml` — CI funcional.
- `../.github/workflows/auditoria-gobernanza.yml` — auditoría automática de gobierno.
- `../.github/workflows/verificar-tags.yml` — verificación criptográfica de tags.
- `.github/dependabot.yml` — mantenimiento de dependencias.

## 11. Desarrollo y contribución

- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — flujo principal.
- [`../CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md) — reglas de convivencia y colaboración.
- [`../SUPPORT.md`](../SUPPORT.md) — rutas de consulta y reporte.
- [`GUIA_INTERNA_DESARROLLO.md`](GUIA_INTERNA_DESARROLLO.md) — convenciones internas.
- [`../.editorconfig`](../.editorconfig) — formato.
- [`../.gitattributes`](../.gitattributes) — normalización Git.
- [`../.gitignore`](../.gitignore) — exclusiones y protección de datos locales.

## 12. Historial de evolución

- [`REGISTRO_CAMBIOS_HISTORICO.md`](REGISTRO_CAMBIOS_HISTORICO.md) — mapa cronológico.
- [`historico/README.md`](historico/README.md) — reglas del archivo histórico.
- [`historico/ux/`](historico/ux/) — bitácoras completas de UX.4.6a–d.
- [`historico/tecnico/`](historico/tecnico/) — snapshots técnicos previos.
- [`historico/normativa_privacidad/`](historico/normativa_privacidad/) — snapshots normativos/privacidad previos.
- [`historico/gobierno/`](historico/gobierno/) — snapshots de decisiones/gobierno.
- [`historico/CHANGELOG_PRE_GOV1_3.md`](historico/CHANGELOG_PRE_GOV1_3.md) — snapshot del changelog acumulativo anterior a GOV.1.3.
- [`historico/ROADMAP_PRE_GOV1_3.md`](historico/ROADMAP_PRE_GOV1_3.md) — snapshot del roadmap anterior a GOV.1.3.

Los archivos históricos documentan lo que se pensó, probó o decidió en un momento determinado. No deben interpretarse como contrato vigente si contradicen un documento actual.

## 13. Releases

- [`../RELEASES.md`](../RELEASES.md) — registro formal y retrospectivo.
- [`../CHANGELOG.md`](../CHANGELOG.md) — cambios notables.
- [`../VERSIONING.md`](../VERSIONING.md) — reglas de incremento y tags.

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
