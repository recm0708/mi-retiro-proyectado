# Auditoría MANT.1 R5H — nombres técnicos restantes

**Estado:** Candidato local validado
**Rama:** `mant/mant1-r5h-auditoria-nombres-restantes`
**Clasificación:** Mantenimiento técnico / trazabilidad de nombres

## 1. Objetivo

Esta revisión completa una segunda pasada sobre nombres técnicos restantes
después de MANT.1 R5E, R5F y R5G. El criterio aplicado no fue traducir todo
de forma automática, sino separar nombres operativos que convenía normalizar
de nombres de dominio, normativa o trazabilidad histórica que debían
conservarse.

## 2. Alcance aplicado

Se normalizaron nombres técnicos en:

- `.github/workflows/`;
- `app/core/`;
- `app/models/`;
- `app/services/`;
- `app/static/css/`;
- `app/static/js/`;
- `app/templates/`;
- `tests/`.

La revisión sincronizó imports, rutas de assets, referencias de plantillas,
documentación viva y pruebas automatizadas relacionadas.

## 3. Criterios de decisión

Se renombraron archivos cuando el nombre cumplía al menos uno de estos
criterios:

- módulo técnico transversal de aplicación;
- archivo estático cargado por plantillas;
- parcial de plantilla reutilizable;
- prueba técnica no ligada a una etiqueta histórica de UX, GOV, VER, DEV o MANT;
- workflow técnico de gobierno.

Se conservaron nombres cuando representaban:

- dominio normativo panameño;
- siglas de sistemas previsionales;
- evidencia histórica de revisiones anteriores;
- rutas públicas, identificadores, clases, ids, claves de almacenamiento o
  contratos que no debían alterarse dentro de esta revisión.

## 4. Destinos técnicos normalizados

Los destinos normalizados protegidos por la regresión R5H son:

- `.github/workflows/governance-audit.yml`
- `app/core/pdf_files.py`
- `app/core/money.py`
- `app/core/observability.py`
- `app/models/simulation.py`
- `app/models/traceability.py`
- `app/models/unified_result.py`
- `app/services/comparator.py`
- `app/services/contribution_projection.py`
- `app/services/mixto_results.py`
- `app/services/reference_date.py`
- `app/services/regulatory_sources.py`
- `app/services/results.py`
- `app/services/retirement.py`
- `app/services/salary_history.py`
- `app/services/salary_projection.py`
- `app/services/sebd_results.py`
- `app/services/sucgs_results.py`
- `app/services/timeline.py`
- `app/services/traceability.py`
- `app/services/unified_result.py`
- `app/static/css/accessibility.css`
- `app/static/css/results.css`
- `app/static/js/accessibility.js`
- `app/static/js/attachment_processing.js`
- `app/static/js/comparator.js`
- `app/static/js/currency.js`
- `app/static/js/data_management.js`
- `app/static/js/official_data_import.js`
- `app/static/js/privacy.js`
- `app/static/js/results.js`
- `app/static/js/results_orchestration.js`
- `app/static/js/retirement.js`
- `app/static/js/salary_history.js`
- `app/static/js/simulation.js`
- `app/static/js/timeline.js`
- `app/static/js/wizard_navigation.js`
- `app/templates/partials/data_management.html`
- `app/templates/partials/official_data_import.html`
- `app/templates/partials/privacy_consent.html`
- `app/templates/partials/results.html`
- `app/templates/partials/retirement.html`
- `app/templates/partials/salary_history.html`
- `app/templates/simulation.html`
- `tests/test_accessibility_themes.py`
- `tests/test_accessibility_ux4.py`
- `tests/test_money.py`
- `tests/test_timeline.py`
- `tests/test_unified_result.py`
- `tests/test_visual_identity_pre_r8.py`
- `tests/test_visual_stabilization.py`

## 5. Excepciones conservadas

Estas rutas se conservaron por dominio, semántica normativa o trazabilidad:

- `app/core/normativa.py`
- `app/services/centro_desarrollo.py`
- `app/services/referencia_mi_retiro_seguro.py`
- `app/templates/dev_centro_desarrollo.html`
- `app/templates/partials/referencia_mi_retiro_seguro.html`
- `regulations/mixto.json`
- `regulations/sebd.json`
- `regulations/sucgs.json`

## 6. Validación ejecutada

Validación local ejecutada durante R5H:

```powershell
python -m compileall app tests -q
python -m pytest -q --tb=short
python -m unittest discover -s tests -q
git diff --check
```

Resultado observado antes de documentar la revisión:

```text
924 passed, 4749 subtests passed
Ran 924 tests
OK
git diff --check: OK
```

## 7. Exclusiones explícitas

Esta revisión no cambia `VERSION`, `APP_VERSION`, motores de cálculo,
parámetros normativos, archivos JSON regulatorios, rutas públicas
funcionales, claves de almacenamiento, identificadores HTML, clases CSS
semánticas ni contenido de `_entregas/`.

## 8. Resultado

R5H deja sincronizada la nomenclatura técnica restante sin modificar la
lógica previsional. La trazabilidad de los renombres queda protegida por una
regresión específica y por la suite completa del proyecto.
