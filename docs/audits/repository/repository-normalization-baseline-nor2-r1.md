# Línea base de normalización NOR.2 R1

**Proyecto:** Mi Retiro Proyectado

**Fase:** NOR.2 R1 — Auditoría de línea base

**Base:** `5100c7f`

**Estado:** auditoría de solo lectura; no ejecuta renombres ni movimientos.

## Objetivo

Medir el árbol versionado contra los estándares cerrados por NOR.1 antes de
realizar cualquier migración estructural.

La auditoría usa `git ls-files` como fuente de verdad para el árbol versionado y
separa incumplimientos mecánicos de casos que requieren clasificación humana por
compatibilidad, dominio o historia.

## Resumen

- Archivos versionados auditados: **416**.
- Directorios raíz fuera del conjunto canónico: **1**.
- Archivos raíz fuera de la lista convencional: **0**.
- Candidatos mecánicos Python: **0**.
- Candidatos mecánicos JavaScript: **0**.
- Candidatos mecánicos HTML/Jinja: **0**.
- Candidatos mecánicos CSS: **0**.
- Candidatos JSON/YAML: **2**.
- Markdown en `docs/` raíz que requiere clasificación: **79**.
- Nombres de código/assets que requieren revisión de idioma o excepción de dominio:
  **28**.

El inventario detallado se conserva en
`docs/audits/repository/repository-normalization-inventory-nor2-r1.txt`.

## Raíz

### Directorios fuera del conjunto canónico

- `assets`

### Archivos fuera de la lista convencional

- Ninguno.

Estos hallazgos son candidatos de revisión. R1 no elimina ni mueve elementos.

## Nomenclatura mecánica

### Python

- Ninguno.

### JavaScript

- Ninguno.

### HTML/Jinja

- Ninguno.

### CSS

- Ninguno.

### JSON/YAML

- `data/revision_ledger_pre_1_0.json`
- `regulations/general_parameters.json`

Las reglas mecánicas no intentan decidir si un nombre español corresponde a un
identificador oficial de dominio. Esa decisión se reserva a la matriz de
migración de NOR.2.

## Documentación en `docs/` raíz

Los siguientes documentos no cumplen directamente la convención técnica nueva de
lowercase/kebab-case o necesitan clasificación por su condición legacy/current:

- `docs/ADR_179_VERSIONADO_REVISION_AWARE.md`
- `docs/ARQUITECTURA.md`
- `docs/AUDITORIA_ARCHIVOS_R5F.md`
- `docs/AUDITORIA_CALCULOS.md`
- `docs/AUDITORIA_CARPETAS_R5E.md`
- `docs/AUDITORIA_DOCUMENTACION_R5G.md`
- `docs/AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md`
- `docs/AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md`
- `docs/AUDITORIA_GITHUB.md`
- `docs/AUDITORIA_MARKDOWN_POST_MANT1_DOC1_R1.md`
- `docs/AUDITORIA_NOMBRES_RESTANTES_R5H.md`
- `docs/AUDITORIA_PLAN1_R4_2026-08-20.md`
- `docs/AUDITORIA_REPOSITORIO_2026-08-18.md`
- `docs/AUDITORIA_UX46E_R7_2026-08-18.md`
- `docs/AUDITORIA_VER2_CONTEO_PROVISIONAL.md`
- `docs/AUDITORIA_VER2_SEGUNDA_PASADA.md`
- `docs/AUDITORIA_VERSIONADO_PRE_1_0.md`
- `docs/CIERRE_DOCUMENTAL_MARKDOWN_DOC1_R1.md`
- `docs/CIERRE_GOV1.md`
- `docs/CIERRE_OPERATIVO_POST_AUDITORIA_R7.md`
- `docs/COMO_SE_CALCULA.md`
- `docs/CONTEXTO_ACTUALIZACION_MARKDOWN_DOC1_R1.md`
- `docs/CUMPLIMIENTO_LEY_81.md`
- `docs/DECISIONES.md`
- `docs/DEPENDENCIAS_TERCEROS.md`
- `docs/DEV2_CENTRO_DESARROLLO.md`
- `docs/ESPECIFICACION_FUNCIONAL.md`
- `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md`
- `docs/EVALUACION_TERCEROS_DESPLIEGUE.md`
- `docs/FUENTES_NORMATIVAS.md`
- `docs/GESTION_DATOS_SIMULACION.md`
- `docs/GUIA_INTERNA_DESARROLLO.md`
- `docs/IDENTIDAD_VISUAL.md`
- `docs/INDICE.md`
- `docs/LEDGER_REVISIONES_PRE_1_0.md`
- `docs/LICENCIA_Y_DISTRIBUCION.md`
- `docs/LIMITACIONES_CONOCIDAS.md`
- `docs/LINEA_BASE_DOCUMENTAL_POST_MANT1_DOC1_R1.md`
- `docs/MATRIZ_DECISION_MARKDOWN_DOC1_R1.md`
- `docs/MATRIZ_DECISION_REVISIONES_VER2.md`
- `docs/MATRIZ_TRAZABILIDAD.md`
- `docs/MIGRACION_FIRMAS_GIT_2026-08-17.md`
- `docs/MODALIDADES_MIXTO.md`
- `docs/MODALIDADES_SEBD.md`
- `docs/MODALIDADES_SUCGS.md`
- `docs/MODELO_AMENAZAS.md`
- `docs/MODELO_DE_DATOS.md`
- `docs/MOTOR_DE_CALCULO.md`
- `docs/NORMATIVA.md`
- `docs/OBSERVABILIDAD_LOGS.md`
- `docs/PLAN_MAESTRO_HACIA_1_0.md`
- `docs/POLITICA_ESTRUCTURA_ARCHIVOS.md`
- `docs/POLITICA_PRIVACIDAD.md`
- `docs/PREPARACION_PUBLICA_GITHUB.md`
- `docs/PROCEDIMIENTO_DERECHOS_TITULAR.md`
- `docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md`
- `docs/PROCESO_RELEASE.md`
- `docs/REGISTRO_CAMBIOS_HISTORICO.md`
- `docs/REVISION_SOLO_SI_APLICA_DOC1_R1.md`
- `docs/ROADMAP.md`
- `docs/SEGURIDAD_PRIVACIDAD.md`
- `docs/TERMINOS_USO_PRIVACIDAD.md`
- `docs/TRANSPARENCIA.md`
- `docs/UX46H_R1_AUDITORIA_RESULTADOS.md`
- `docs/UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md`
- `docs/UX_4_6A_REDISENO_VISUAL.md`
- `docs/UX_4_6B_PASO1_DATOS_PERSONALES.md`
- `docs/UX_4_6C_PASO2_CUOTAS.md`
- `docs/UX_4_6D_PASO3_HISTORIAL.md`
- `docs/VALIDACION.md`
- `docs/VER2_R1_AUDITORIA_RECONCILIACION_POST_DOC1.md`
- `docs/VER2_R1_DECISION_OPERATIVA_POST_DOC1.md`
- `docs/VER2_R1_MATRIZ_DECISION_RECONCILIACION_POST_DOC1.md`
- `docs/VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md`
- `docs/VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md`
- `docs/VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md`
- `docs/VER2_R3_DECISION_VERSION_CANDIDATA_POST_R2.md`
- `docs/VER2_R4_PROMOCION_G071_E01.md`
- `docs/VER2_R5_ESTABILIZACION_POST_RELEASE.md`

No se renombran en R1. Su migración debe considerar enlaces, pruebas, índices,
historia y consumidores externos.

## Revisión de idioma y dominio

Candidatos detectados por tokens técnicos en español:

- `app/services/centro_desarrollo.py`
- `app/services/como_se_calcula.py`
- `app/services/detalle_anio_actual.py`
- `app/services/ficha_digital.py`
- `app/services/referencia_mi_retiro_seguro.py`
- `app/static/css/como-se-calcula.css`
- `app/static/css/procedencia-editable.css`
- `app/static/js/detalle_anio_actual.js`
- `app/static/js/procedencia_editable.js`
- `app/static/js/referencia_mi_retiro_seguro.js`
- `app/static/js/tema.js`
- `app/templates/como_se_calcula.html`
- `app/templates/comparar.html`
- `app/templates/dev_centro_desarrollo.html`
- `app/templates/metodologia.html`
- `app/templates/partials/detalle_anio_actual.html`
- `app/templates/partials/importacion_ficha_digital.html`
- `app/templates/partials/referencia_mi_retiro_seguro.html`
- `tests/test_dev2_centro_desarrollo.py`
- `tests/test_ux44_detalle_anio_actual.py`
- `tests/test_ux44_referencia_pdf.py`
- `tests/test_ux46d_revision18_procedencia_persistencia.py`
- `tests/test_ux46d_revision19_sincronizacion_actual.py`
- `tests/test_ux46d_revision23_ficha_actualiza_cuotas.py`
- `tests/test_ux46e_r81_procedencia_editable.py`
- `tests/test_ux46f_r1_consistencia_procedencia_adjuntos.py`
- `tests/test_ux46g_r1_escenarios_retiro.py`
- `tests/test_ux46i_r1_como_se_calcula.py`

Un candidato puede terminar en una de tres categorías:

1. **migrar** — nombre técnico genérico;
2. **conservar** — término oficial de dominio/producto con excepción documentada;
3. **posponer** — impacto demasiado alto para una revisión aislada.

## Candidatos críticos y referencias

| Ruta actual | Referencias exactas encontradas | Riesgo inicial |
| --- | ---: | --- |
| `app/services/centro_desarrollo.py` | 2 | Alto hasta revisar consumidores |
| `app/services/como_se_calcula.py` | 11 | Alto hasta revisar consumidores |
| `app/services/detalle_anio_actual.py` | 5 | Alto hasta revisar consumidores |
| `app/services/ficha_digital.py` | 7 | Alto hasta revisar consumidores |
| `app/services/referencia_mi_retiro_seguro.py` | 7 | Alto hasta revisar consumidores |
| `app/static/css/como-se-calcula.css` | 8 | Alto hasta revisar consumidores |
| `app/static/css/procedencia-editable.css` | 5 | Alto hasta revisar consumidores |
| `app/static/js/detalle_anio_actual.js` | 15 | Alto hasta revisar consumidores |
| `app/static/js/procedencia_editable.js` | 5 | Alto hasta revisar consumidores |
| `app/static/js/referencia_mi_retiro_seguro.js` | 8 | Alto hasta revisar consumidores |
| `app/static/js/tema.js` | 6 | Alto hasta revisar consumidores |
| `app/templates/como_se_calcula.html` | 9 | Alto hasta revisar consumidores |
| `app/templates/comparar.html` | 2 | Alto hasta revisar consumidores |
| `app/templates/dev_centro_desarrollo.html` | 2 | Alto hasta revisar consumidores |
| `app/templates/metodologia.html` | 10 | Alto hasta revisar consumidores |
| `data/revision_ledger_pre_1_0.json` | 78 | Alto hasta revisar consumidores |

El conteo usa `git grep -n -F <ruta> -- .`. Un valor bajo no implica bajo impacto
si la ruta participa en imports, carga de datos, release o contratos de pruebas.

## Artefactos locales heredados

| Directorio | Existe | Archivos locales | Bytes |
| --- | --- | ---: | ---: |
| `_entregas/` | Sí | 29 | 9874828 |
| `_deliverables/` | No | 0 | 0 |

R1 registra únicamente existencia y tamaño. No inspecciona contenido sensible ni
elimina artefactos locales.

## Decisiones de R1

- No renombrar todavía `data/revision_ledger_pre_1_0.json`.
- No renombrar en bloque servicios, JavaScript, plantillas ni CSS.
- No convertir automáticamente todos los Markdown históricos a lowercase.
- No eliminar `_entregas/`.
- No reanudar SEC.2.
- Construir en R2 la matriz de migración por candidato, impacto y orden de
  dependencias.

## Siguiente paso

**NOR.2 R2** debe convertir esta línea base en una matriz de decisión que indique
para cada candidato: ruta actual, ruta propuesta, tipo de excepción, consumidores,
pruebas afectadas, documentación afectada, riesgo y revisión en la que se
ejecutará la migración.
