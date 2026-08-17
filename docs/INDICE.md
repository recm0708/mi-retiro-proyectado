# Índice de documentación

**Estado:** vigente
**Versión de aplicación revisada:** `0.0.22-beta`
**Última reorganización:** GOV.1.3 R3 — 2026-08-17

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
- [`../.github/CODEOWNERS`](../.github/CODEOWNERS) — responsables de revisión.

## 3. Arquitectura

- [`ARQUITECTURA.md`](ARQUITECTURA.md) — capas, módulos, endpoints y flujo.
- [`MODELO_DE_DATOS.md`](MODELO_DE_DATOS.md) — modelos y contratos.
- [`GESTION_DATOS_SIMULACION.md`](GESTION_DATOS_SIMULACION.md) — estado local, limpieza, restauración e invalidación.

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
- [`POLITICA_PRIVACIDAD.md`](POLITICA_PRIVACIDAD.md) — política pública vigente.
- [`TERMINOS_USO_PRIVACIDAD.md`](TERMINOS_USO_PRIVACIDAD.md) — términos y tratamiento de datos.
- [`CUMPLIMIENTO_LEY_81.md`](CUMPLIMIENTO_LEY_81.md) — matriz interna de alineación.

GOV.1.3 R3 consolidó este bloque como contrato documental vigente. La revisión jurídica externa y los procedimientos operativos pendientes continúan en GOV.1.5.

## 9. Observabilidad y auditoría

Documentación planificada durante GOV.1:

- `OBSERVABILIDAD_LOGS.md` — se creará junto con la implementación real de GOV.1.4;
- `TRANSPARENCIA.md` — previsto para GOV.1.3 R4;
- `MATRIZ_TRAZABILIDAD.md` — previsto para GOV.1.3 R4;
- `AUDITORIA_CALCULOS.md` — previsto para GOV.1.3 R4.

No se crean contratos de logging antes de implementar y validar su comportamiento real.

## 10. Validación y calidad

- [`VALIDACION.md`](VALIDACION.md) — estrategia y evidencias.
- [`../tests/casos_validacion/README.md`](../tests/casos_validacion/README.md) — reglas de casos sintéticos/anonimizados.
- `.github/workflows/ci.yml` — CI.
- `.github/dependabot.yml` — mantenimiento de dependencias.

## 11. Desarrollo y contribución

- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — flujo principal.
- [`GUIA_INTERNA_DESARROLLO.md`](GUIA_INTERNA_DESARROLLO.md) — convenciones internas.
- [`../.editorconfig`](../.editorconfig) — formato.
- [`../.gitattributes`](../.gitattributes) — normalización Git.
- [`../.gitignore`](../.gitignore) — exclusiones y protección de datos locales.

## 12. Historial de evolución

- [`REGISTRO_CAMBIOS_HISTORICO.md`](REGISTRO_CAMBIOS_HISTORICO.md) — mapa cronológico.
- [`historico/README.md`](historico/README.md) — reglas del archivo histórico.
- [`historico/ux/`](historico/ux/) — bitácoras completas de UX.4.6a–d.
- [`historico/tecnico/`](historico/tecnico/) — snapshots técnicos previos a GOV.1.3 R2.
- [`historico/normativa_privacidad/`](historico/normativa_privacidad/) — snapshots previos a GOV.1.3 R3.
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

Cuando una regla sea reemplazada, no se debe borrar su evidencia histórica. El documento vigente debe indicar qué regla la sustituye cuando esa relación sea relevante para auditoría.

## Regla de mantenimiento

Un cambio no obliga a editar todos los `.md`. Sí obliga a revisar todos los documentos que dependan del cambio y mantener coherencia entre:

- código;
- normativa versionada;
- pruebas;
- documentación vigente;
- fuentes oficiales;
- historial de decisiones.
