# Matriz de trazabilidad

**Estado:** Vigente
**Versión de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01 promovida en R4
**Último tag formal legacy:** `v0.0.26-beta`
**Base histórica:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal:** VER.2 — 2026-08-21
**Clasificación:** Técnica / Auditoría


<!-- DOC1-R1-POST-MANT1:START -->
## Estado post-MANT.1

La trazabilidad vigente incorpora el cierre operativo de MANT.1 R7 y la apertura de DOC.1 R1.

Estado documental actual:

- MANT.1 R5H auditó nombres técnicos restantes.
- MANT.1 R6 validó funcionalmente el repositorio después de renombres.
- MANT.1 R7 cerró operativamente el bloque en `main`.
- DOC.1 R1 audita todos los Markdown y actualiza solo documentación vigente desalineada.
- `VERSION` se promueve en R4 a `0.0.71.01-beta` como VER.2 G071/E01.
- VER.2 permanece como reconciliación/candidato pendiente, no como versión publicada.

Esta matriz debe distinguir trazabilidad histórica de estado vigente.
<!-- DOC1-R1-POST-MANT1:END -->

Esta matriz conecta contratos críticos del producto con su fuente, decisión, implementación y evidencia de prueba. No sustituye `functional-specification.md` ni pretende afirmar cobertura granular completa de todos los RF históricos.

## 1. Convención

| Campo | Significado |
|---|---|
| ID | identificador estable dentro de esta matriz |
| Requisito/contrato | propiedad que el proyecto afirma |
| Fuente/criterio | norma, fuente o `N/A — técnico/UX` |
| ADR | decisión relevante |
| Implementación | archivos principales |
| Prueba | regresión principal |
| Estado | nivel actual de trazabilidad |

## 2. Núcleo trazable

| ID | Requisito/contrato | Fuente/criterio | ADR | Implementación | Prueba | Estado |
|---|---|---|---|---|---|---|
| TR-001 | Identidad independiente de la CSS | N/A — gobierno/producto | ADR-045 | `app/core/config.py`, `app/templates/base.html` | `tests/test_identidad_interfaz.py` | Verificado |
| TR-002 | `VERSION` es fuente canónica | N/A — gobierno | ADR-157, ADR-158 | `VERSION`, `app/core/version.py`, `app/core/config.py` | `tests/test_gov12_versionado.py` | Verificado |
| TR-003 | Datos históricos y proyectados permanecen separados | N/A — integridad de datos | ADR-006, ADR-073 | `app/services/timeline.py`, `app/services/results.py` | `tests/test_timeline.py`, `tests/test_results.py` | Verificado |
| TR-004 | Precisión monetaria usa `Decimal` en operaciones sensibles | N/A — técnico | ADR-016 | `app/core/money.py` | `tests/test_money.py` | Verificado |
| TR-005 | PDF se valida antes del parser y no se persiste por el endpoint | N/A — seguridad | ADR-074 | `app/core/pdf_files.py`, `app/main.py` | `tests/test_prebeta_e2e_hardening.py` | Verificado |
| TR-006 | Importación documental requiere vista previa/confirmación | N/A — UX/integridad | ADR-071 | `app/static/js/official_data_import.js` | `tests/test_ux44_importacion_oficial.py`, `tests/test_ux46b_paso1_datos_personales.py` | Verificado |
| TR-007 | Ficha Digital limita el contexto importado al año objetivo y reconcilia al alza sin reducir silenciosamente | N/A — integridad de datos | ADR-072, ADR-103, ADR-155, ADR-156 | `app/services/ficha_digital.py`, `app/static/js/official_data_import.js` | `tests/test_ux46d_revision23_ficha_updates_contributions.py` | Verificado |
| TR-008 | SEBD mantiene clasificación/modalidades y parámetros versionados | Ley 51 / reglamentos CSS | ADR-023 a ADR-026 | `app/engines/sebd.py`, `app/engines/sebd_modalidades.py`, `regulations/sebd.json` | `tests/test_sebd.py`, `tests/test_sebd_modalidades.py` | Verificado técnico |
| TR-009 | CAP Mixto no se reconstruye desde historial anual insuficiente | Ley 51 / normativa Mixto | ADR-027 a ADR-033 | `app/engines/mixto.py`, `regulations/mixto.json` | `tests/test_mixto.py`, `tests/test_mixto_prestaciones_cap.py` | Verificado técnico |
| TR-010 | SUCGS separa contributivo, capa solidaria y garantía | Ley 51, arts. documentados | ADR-036 a ADR-040 | `app/engines/sucgs.py`, `regulations/sucgs.json` | `tests/test_sucgs.py`, `tests/test_sucgs_capa_solidaria.py`, `tests/test_sucgs_reemplazo.py` | Verificado técnico |
| TR-011 | Trazabilidad explica el resultado y no recalcula | N/A — arquitectura/auditoría | ADR-042, ADR-043 | `app/models/traceability.py`, `app/services/traceability.py` | `tests/test_traceability.py` | Verificado |
| TR-012 | Resultado final usa contrato transversal común | N/A — arquitectura | ADR-044 | `app/models/unified_result.py`, `app/services/unified_result.py` | `tests/test_unified_result.py` | Verificado |
| TR-013 | Consentimiento es versionado y la sesión activa debe coincidir | Ley 81 / Decreto 285 como marco; control técnico interno | ADR-110, ADR-111, ADR-118 | `app/static/js/privacy.js` | `tests/test_ux46b_revision2_privacidad.py`, `tests/test_gov13_documentacion_r3.py` | Verificado técnico; revisión jurídica pendiente |
| TR-014 | APIs de simulación usan `no-store` y cabeceras defensivas | N/A — seguridad | ADR-074 | `app/main.py` | `tests/test_prebeta_e2e_hardening.py` | Verificado |
| TR-015 | CI reproduce instalación, sintaxis y suite en Python 3.13/3.14 | N/A — calidad | ADR-075, ADR-076 | `.github/workflows/ci.yml`, `.github/dependabot.yml` | `tests/test_prebeta_e2e_hardening.py` | Verificado |
| TR-016 | Documentación vigente y evidencia histórica están separadas | N/A — gobierno | ADR-158 + GOV.1.3 | `docs/README.md`, `docs/archive/` | `tests/test_gov13_documentacion.py`, `tests/test_gov13_documentacion_r2.py`, `tests/test_gov13_documentacion_r3.py` | Verificado |
| TR-017 | Decisiones del Paso 3 y valores derivados distinguen ausencia de decisión, cálculo automático y edición del usuario | N/A — UX/integridad | ADR-169 | `app/static/js/simulation.js`, `app/static/js/salary_history.js`, `app/static/js/current_year_detail.js`, `app/templates/simulation.html` | `tests/test_ux46f_r1_attachment_provenance_consistency.py` | Verificado UX.4.6f R1 |
| TR-018 | El análisis de adjuntos comunica estado ocupado, evita duplicados y reutiliza un contrato global accesible | N/A — UX/accesibilidad | ADR-170 | `app/static/js/attachment_processing.js`, `app/static/js/official_data_import.js`, `app/static/js/mi_retiro_seguro_reference.js` | `tests/test_ux46f_r1_attachment_provenance_consistency.py` | Verificado UX.4.6f R1 |
| TR-019 | Los datos documentales detectados quedan bloqueados en la vista principal y se corrigen desde la revisión editable; los no detectados siguen completables | N/A — UX/integridad | ADR-171 | `app/static/js/editable_provenance.js`, `app/static/css/design-system.css`, `app/static/css/editable-provenance.css`, `app/static/js/salary_history.js` | `tests/test_ux46f_r11_bloqueo_documental_vista_principal.py` | Verificado UX.4.6f R1.1 |
| TR-020 | La línea temporal valida coherencia Pasos 2–4, conserva salario mensual proyectado y distingue ausencia de cotización futura | N/A — técnico/integridad | ADR-172 | `app/models/simulation.py`, `app/services/timeline.py`, `app/static/js/timeline.js` | `tests/test_ux46f_r2_auditoria_paso4.py` | Verificado UX.4.6f R2 / PR #30 |
| TR-021 | Las hipótesis salariales compuestas, la selección explícita de porcentajes, el salario futuro conocido y la procedencia del horizonte son explícitas | N/A — técnico/UX | ADR-173 | `app/models/simulation.py`, `app/services/salary_projection.py`, `app/static/js/simulation.js`, `app/static/js/retirement.js`, `app/templates/simulation.html` | `tests/test_ux46f_r2_auditoria_paso4.py` | Verificado UX.4.6f R2 / PR #30 |
| TR-022 | Paso 5 deriva únicamente los escenarios posteriores cubiertos por Paso 4 y conserva las ediciones del usuario | N/A — técnico/UX | ADR-174 | `app/static/js/retirement.js`, `app/templates/partials/retirement.html`, `app/models/simulation.py` | `tests/test_ux46g_r1_retirement_scenarios.py` | Verificado UX.4.6g / PR #32 |
| TR-023 | Retiro anticipado se solicita explícitamente, bloquea fechas transcurridas y la fecha de evaluación solo se admite dentro de la banda estándar | Ley 51 / reglamento CSS para componente SEBD aplicable | ADR-175 | `app/services/retirement.py`, `app/engines/elegibilidad.py`, `regulations/sebd.json`, `app/static/js/retirement.js` | `tests/test_ux46g_r1_retirement_scenarios.py`, `tests/test_retirement.py` | Verificado UX.4.6g / PR #32 |
| TR-024 | Los controles de fecha validan año/calendario de forma transversal y Paso 5 muestra cobertura salarial de una fecha personalizada | N/A — técnico/UX | ADR-176 | `app/static/js/accessibility.js`, `app/static/css/accessibility.css`, `app/static/js/retirement.js`, `app/templates/partials/retirement.html` | `tests/test_ux46g_r1_retirement_scenarios.py` | Verificado UX.4.6g / PR #32 |
| TR-025 | Alineación y densidad visual de períodos y resumen de retiro | N/A — UX/responsive | ADR-177 | `app/templates/partials/salary_history.html`, `app/templates/simulation.html`, `app/templates/partials/retirement.html`, `app/static/css/design-system.css` | `tests/test_ux46g_r1_retirement_scenarios.py` | Verificado UX.4.6g / PR #32 |
| TR-026 | La guía pública explica cómo se transforman los datos de los Pasos 1–6 y los tres sistemas con parámetros versionados, fórmula general + sustitución numérica y términos definidos en contexto, sin duplicar motores; navbar, Metodología y Paso 6 enlazan sin transportar datos personales | N/A — transparencia/UX; normativa versionada existente | ADR-178 | `app/services/calculation_guide.py`, `app/templates/calculation_guide.html`, `app/static/css/calculation-guide.css`, `app/templates/base.html`, `app/static/js/results_orchestration.js`, `app/templates/methodology.html` | `tests/test_ux46i_r1_calculation_guide.py` | Verificado UX.4.6i / PR #34 |
| TR-027 | La beta revision-aware cuenta estados aceptados, preserva tags legacy y mantiene ledger continuo sin convertir commits/candidatos en revisiones | N/A — gobierno/versionado | ADR-179 | `VERSION`, `VERSIONING.md`, `app/core/version.py`, `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/governance/pre-1-0-revision-ledger.md` | `tests/test_ver2_version_revision_aware.py`, `tests/test_ver2_documentacion_vigente.py` | Verificado VER.2 G071/E01 en R4 |

## 3. Cobertura de RF

`functional-specification.md` conserva el ledger RF histórico. Esta matriz **no declara** que cada RF individual tenga ya una fila única requisito → ADR → archivo → test.

El estado actual es:

- contratos críticos: trazados en esta matriz;
- ledger RF: preservado;
- cobertura RF granular completa: **parcial / pendiente de ampliación**.

Esta declaración evita confundir preservación histórica con cobertura de prueba demostrada.

## 4. Mantenimiento

Una nueva fila debe usar una fuente normativa solo cuando exista relación real. Para UX, arquitectura, seguridad técnica o gobierno se utiliza `N/A — técnico/UX` o una descripción equivalente.

No se inventan artículos legales para completar la tabla.

Los estados `Candidato` deben promoverse a `Verificado` únicamente después del gate y cierre que corresponda. VER.2 debe actualizar TR-027 al integrar G071.

<!-- ANCLAS_HISTORICAS_VER2_MATRIZ -->

## Anclas históricas preservadas por VER.2

- Base histórica documental preservada: `0.0.23-beta`.
- VER.2 añade TR-027 sin eliminar la evidencia de GOV.1.3 R4 ni la matriz previa.
