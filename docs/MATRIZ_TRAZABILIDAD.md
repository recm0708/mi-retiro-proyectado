# Matriz de trazabilidad

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.26-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R4 — 2026-08-17
**Clasificación:** Técnica / Auditoría

Esta matriz conecta contratos críticos del producto con su fuente, decisión, implementación y evidencia de prueba. No sustituye `ESPECIFICACION_FUNCIONAL.md` ni pretende afirmar cobertura granular completa de todos los RF históricos.

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
| TR-003 | Datos históricos y proyectados permanecen separados | N/A — integridad de datos | ADR-006, ADR-073 | `app/servicios/linea_tiempo.py`, `app/servicios/resultados.py` | `tests/test_linea_tiempo.py`, `tests/test_resultados.py` | Verificado |
| TR-004 | Precisión monetaria usa `Decimal` en operaciones sensibles | N/A — técnico | ADR-016 | `app/core/dinero.py` | `tests/test_dinero.py` | Verificado |
| TR-005 | PDF se valida antes del parser y no se persiste por el endpoint | N/A — seguridad | ADR-074 | `app/core/archivos_pdf.py`, `app/main.py` | `tests/test_prebeta_e2e_hardening.py` | Verificado |
| TR-006 | Importación documental requiere vista previa/confirmación | N/A — UX/integridad | ADR-071 | `app/static/js/importacion_datos_oficiales.js` | `tests/test_ux44_importacion_oficial.py`, `tests/test_ux46b_paso1_datos_personales.py` | Verificado |
| TR-007 | Ficha Digital limita el contexto importado al año objetivo y reconcilia al alza sin reducir silenciosamente | N/A — integridad de datos | ADR-072, ADR-103, ADR-155, ADR-156 | `app/servicios/ficha_digital.py`, `app/static/js/importacion_datos_oficiales.js` | `tests/test_ux46d_revision23_ficha_actualiza_cuotas.py` | Verificado |
| TR-008 | SEBD mantiene clasificación/modalidades y parámetros versionados | Ley 51 / reglamentos CSS | ADR-023 a ADR-026 | `app/motores/sebd.py`, `app/motores/sebd_modalidades.py`, `normativa/sebd.json` | `tests/test_sebd.py`, `tests/test_sebd_modalidades.py` | Verificado técnico |
| TR-009 | CAP Mixto no se reconstruye desde historial anual insuficiente | Ley 51 / normativa Mixto | ADR-027 a ADR-033 | `app/motores/mixto.py`, `normativa/mixto.json` | `tests/test_mixto.py`, `tests/test_mixto_prestaciones_cap.py` | Verificado técnico |
| TR-010 | SUCGS separa contributivo, capa solidaria y garantía | Ley 51, arts. documentados | ADR-036 a ADR-040 | `app/motores/sucgs.py`, `normativa/sucgs.json` | `tests/test_sucgs.py`, `tests/test_sucgs_capa_solidaria.py`, `tests/test_sucgs_reemplazo.py` | Verificado técnico |
| TR-011 | Trazabilidad explica el resultado y no recalcula | N/A — arquitectura/auditoría | ADR-042, ADR-043 | `app/modelos/trazabilidad.py`, `app/servicios/trazabilidad.py` | `tests/test_trazabilidad.py` | Verificado |
| TR-012 | Resultado final usa contrato transversal común | N/A — arquitectura | ADR-044 | `app/modelos/resultado_unificado.py`, `app/servicios/resultado_unificado.py` | `tests/test_resultado_unificado.py` | Verificado |
| TR-013 | Consentimiento es versionado y la sesión activa debe coincidir | Ley 81 / Decreto 285 como marco; control técnico interno | ADR-110, ADR-111, ADR-118 | `app/static/js/privacidad.js` | `tests/test_ux46b_revision2_privacidad.py`, `tests/test_gov13_documentacion_r3.py` | Verificado técnico; revisión jurídica pendiente |
| TR-014 | APIs de simulación usan `no-store` y cabeceras defensivas | N/A — seguridad | ADR-074 | `app/main.py` | `tests/test_prebeta_e2e_hardening.py` | Verificado |
| TR-015 | CI reproduce instalación, sintaxis y suite en Python 3.13/3.14 | N/A — calidad | ADR-075, ADR-076 | `.github/workflows/ci.yml`, `.github/dependabot.yml` | `tests/test_prebeta_e2e_hardening.py` | Verificado |
| TR-016 | Documentación vigente y evidencia histórica están separadas | N/A — gobierno | ADR-158 + GOV.1.3 | `docs/INDICE.md`, `docs/historico/` | `tests/test_gov13_documentacion.py`, `tests/test_gov13_documentacion_r2.py`, `tests/test_gov13_documentacion_r3.py` | Verificado |
| TR-017 | Decisiones del Paso 3 y valores derivados distinguen ausencia de decisión, cálculo automático y edición del usuario | N/A — UX/integridad | ADR-169 | `app/static/js/simulacion.js`, `app/static/js/historial_salarios.js`, `app/static/js/detalle_anio_actual.js`, `app/templates/simulacion.html` | `tests/test_ux46f_r1_consistencia_procedencia_adjuntos.py` | Verificado UX.4.6f R1 |
| TR-018 | El análisis de adjuntos comunica estado ocupado, evita duplicados y reutiliza un contrato global accesible | N/A — UX/accesibilidad | ADR-170 | `app/static/js/procesamiento_adjuntos.js`, `app/static/js/importacion_datos_oficiales.js`, `app/static/js/referencia_mi_retiro_seguro.js` | `tests/test_ux46f_r1_consistencia_procedencia_adjuntos.py` | Verificado UX.4.6f R1 |
| TR-019 | Los datos documentales detectados quedan bloqueados en la vista principal y se corrigen desde la revisión editable; los no detectados siguen completables | N/A — UX/integridad | ADR-171 | `app/static/js/procedencia_editable.js`, `app/static/css/design-system.css`, `app/static/css/procedencia-editable.css`, `app/static/js/historial_salarios.js` | `tests/test_ux46f_r11_bloqueo_documental_vista_principal.py` | Verificado UX.4.6f R1.1 |
| TR-020 | La línea temporal valida coherencia Pasos 2–4, conserva salario mensual proyectado y distingue ausencia de cotización futura | N/A — técnico/integridad | ADR-172 | `app/modelos/simulacion.py`, `app/servicios/linea_tiempo.py`, `app/static/js/linea_tiempo.js` | `tests/test_ux46f_r2_auditoria_paso4.py` | Candidato UX.4.6f R2 |
| TR-021 | Las hipótesis salariales compuestas, la selección explícita de porcentajes, el salario futuro conocido y la procedencia del horizonte son explícitas | N/A — técnico/UX | ADR-173 | `app/modelos/simulacion.py`, `app/servicios/proyeccion_salarios.py`, `app/static/js/simulacion.js`, `app/static/js/retiro.js`, `app/templates/simulacion.html` | `tests/test_ux46f_r2_auditoria_paso4.py` | Candidato UX.4.6f R2 |

## 3. Cobertura de RF

`ESPECIFICACION_FUNCIONAL.md` conserva el ledger RF histórico. R4 **no declara** que cada RF individual tenga ya una fila única requisito → ADR → archivo → test.

El estado actual es:

- contratos críticos: trazados en esta matriz;
- ledger RF: preservado;
- cobertura RF granular completa: **parcial / pendiente de ampliación**.

Esta declaración evita confundir preservación histórica con cobertura de prueba demostrada.

## 4. Mantenimiento

Una nueva fila debe usar una fuente normativa solo cuando exista relación real. Para UX, arquitectura, seguridad técnica o gobierno se utiliza `N/A — técnico/UX` o una descripción equivalente.

No se inventan artículos legales para completar la tabla.
