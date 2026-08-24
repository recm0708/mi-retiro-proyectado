# NOR.2 R4 — migración de documentación viva

**Base:** `b037518`

**Estado:** migración documental viva aplicada.

## Resultado

R4 migra **41 documentos vivos** hacia las áreas canónicas definidas por R2 y
consolida **2 estándares heredados** dentro de `docs/standards/`. En total se
materializan **43 movimientos Git**.

La migración no conserva stubs de compatibilidad. Git mantiene el historial y
R5 tratará los documentos históricos que R2 clasificó como `ARCHIVAR`.

Los enlaces Markdown de documentos movidos se recalculan desde su nueva
ubicación y las referencias técnicas vivas se actualizan a las rutas canónicas.

## Estructura viva

- `docs/architecture/`
- `docs/decisions/`
- `docs/governance/`
- `docs/operations/`
- `docs/product/`
- `docs/regulatory/`
- `docs/security/`
- `docs/standards/`
- `docs/README.md`

## Movimientos

| Ruta heredada | Ruta canónica |
| --- | --- |
| `docs/ADR_179_VERSIONADO_REVISION_AWARE.md` | `docs/decisions/adr-179-revision-aware-versioning.md` |
| `docs/ARQUITECTURA.md` | `docs/architecture/system-architecture.md` |
| `docs/COMO_SE_CALCULA.md` | `docs/product/calculation-guide.md` |
| `docs/CUMPLIMIENTO_LEY_81.md` | `docs/regulatory/law-81-compliance.md` |
| `docs/DECISIONES.md` | `docs/decisions/README.md` |
| `docs/DEPENDENCIAS_TERCEROS.md` | `docs/operations/third-party-dependencies.md` |
| `docs/DEV2_CENTRO_DESARROLLO.md` | `docs/architecture/development-center.md` |
| `docs/ESPECIFICACION_FUNCIONAL.md` | `docs/product/functional-specification.md` |
| `docs/EVALUACION_TERCEROS_DESPLIEGUE.md` | `docs/security/third-party-deployment-assessment.md` |
| `docs/FUENTES_NORMATIVAS.md` | `docs/regulatory/regulatory-sources.md` |
| `docs/GESTION_DATOS_SIMULACION.md` | `docs/product/simulation-data-management.md` |
| `docs/GUIA_INTERNA_DESARROLLO.md` | `docs/operations/development-guide.md` |
| `docs/IDENTIDAD_VISUAL.md` | `docs/product/visual-identity.md` |
| `docs/INDICE.md` | `docs/README.md` |
| `docs/LEDGER_REVISIONES_PRE_1_0.md` | `docs/governance/pre-1-0-revision-ledger.md` |
| `docs/LICENCIA_Y_DISTRIBUCION.md` | `docs/governance/licensing-and-distribution.md` |
| `docs/LIMITACIONES_CONOCIDAS.md` | `docs/product/known-limitations.md` |
| `docs/MATRIZ_TRAZABILIDAD.md` | `docs/product/traceability-matrix.md` |
| `docs/MODALIDADES_MIXTO.md` | `docs/regulatory/mixto-modalities.md` |
| `docs/MODALIDADES_SEBD.md` | `docs/regulatory/sebd-modalities.md` |
| `docs/MODALIDADES_SUCGS.md` | `docs/regulatory/sucgs-modalities.md` |
| `docs/MODELO_AMENAZAS.md` | `docs/security/threat-model.md` |
| `docs/MODELO_DE_DATOS.md` | `docs/architecture/data-model.md` |
| `docs/MOTOR_DE_CALCULO.md` | `docs/architecture/calculation-engine.md` |
| `docs/NORMATIVA.md` | `docs/regulatory/regulatory-framework.md` |
| `docs/OBSERVABILIDAD_LOGS.md` | `docs/operations/observability-and-logs.md` |
| `docs/PLAN_MAESTRO_HACIA_1_0.md` | `docs/governance/master-plan-to-1-0.md` |
| `docs/POLITICA_PRIVACIDAD.md` | `docs/security/privacy-policy.md` |
| `docs/PREPARACION_PUBLICA_GITHUB.md` | `docs/operations/github-public-repository.md` |
| `docs/PROCEDIMIENTO_DERECHOS_TITULAR.md` | `docs/security/data-subject-rights-procedure.md` |
| `docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md` | `docs/security/security-incident-procedure.md` |
| `docs/PROCESO_RELEASE.md` | `docs/operations/release-process.md` |
| `docs/ROADMAP.md` | `docs/governance/roadmap.md` |
| `docs/SEGURIDAD_PRIVACIDAD.md` | `docs/security/security-and-privacy.md` |
| `docs/TERMINOS_USO_PRIVACIDAD.md` | `docs/security/terms-and-privacy.md` |
| `docs/TRANSPARENCIA.md` | `docs/product/transparency.md` |
| `docs/UX_4_6A_REDISENO_VISUAL.md` | `docs/product/user-interface.md` |
| `docs/UX_4_6B_PASO1_DATOS_PERSONALES.md` | `docs/product/workflow-step-1-personal-data.md` |
| `docs/UX_4_6C_PASO2_CUOTAS.md` | `docs/product/workflow-step-2-contributions.md` |
| `docs/UX_4_6D_PASO3_HISTORIAL.md` | `docs/product/workflow-step-3-salary-history.md` |
| `docs/VALIDACION.md` | `docs/operations/validation.md` |
| `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md` | `docs/standards/code-and-comments.md` |
| `docs/POLITICA_ESTRUCTURA_ARCHIVOS.md` | `docs/standards/file-structure-by-extension.md` |

## Garantías de R4

- 43 rutas heredadas dejan de existir;
- 43 rutas canónicas existen;
- los 2 estándares especializados quedan indexados en `docs/standards/README.md`;
- los enlaces Markdown locales de documentación viva deben resolver;
- las superficies vivas no conservan rutas completas heredadas;
- `VERSION` permanece en `0.0.71.01-beta`;
- SEC.2 continúa pausado.

## Siguiente revisión

**NOR.2 R5** archivará o retirará de la raíz de `docs/` las auditorías, cierres y
documentos históricos definidos por la matriz R2.

### Gate local previo al commit — 2026-08-24

Resultados observados después de completar la migración y sanear las regresiones documentales:

- suite completa: **963 pruebas ejecutadas — OK**;
- gate amplio documental R4: **113 pruebas + 229 subtests — OK**;
- regresiones finales saneadas: **71 pruebas + 83 subtests — OK**;
- contrato específico NOR.2 R4: **7 pruebas + 54 subtests — OK**;
- `python -m compileall -q app`: **OK**;
- validación sintáctica de JavaScript mediante `node --check`: **OK**;
- `git diff --check`: **OK**;
- `VERSION` permanece en `0.0.71.01-beta`.

Este resultado valida localmente la rama R4 antes del commit y del gate remoto. R4
permanece activo hasta su integración en `main`; R5 es la siguiente revisión.
