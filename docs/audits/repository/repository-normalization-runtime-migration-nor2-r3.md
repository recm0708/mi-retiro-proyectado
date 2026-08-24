# NOR.2 R3 — migración de runtime y configuración

**Base:** `4d4e56f`

**Estado:** migración técnica aplicada.

## Resultado

R3 materializa **28 movimientos Git** definidos en la matriz R2. Se normalizan
nombres internos de servicios Python, JavaScript, CSS, plantillas, pruebas y
configuración.

Las **URL públicas en español no cambian**. La normalización afecta nombres
técnicos internos, no contratos visibles de navegación.

`app/services/ficha_digital.py` se conserva como excepción explícita porque
**Ficha Digital** es un nombre de dominio/producto externo.

La evidencia histórica R1/R2 y los documentos ya clasificados para archivo no
se reescriben: deben conservar las rutas que existían cuando fueron producidos.

## Movimientos

| Ruta anterior | Ruta vigente |
| --- | --- |
| `app/services/centro_desarrollo.py` | `app/services/development_center.py` |
| `app/services/como_se_calcula.py` | `app/services/calculation_guide.py` |
| `app/services/detalle_anio_actual.py` | `app/services/current_year_detail.py` |
| `app/services/referencia_mi_retiro_seguro.py` | `app/services/mi_retiro_seguro_reference.py` |
| `app/static/css/como-se-calcula.css` | `app/static/css/calculation-guide.css` |
| `app/static/css/procedencia-editable.css` | `app/static/css/editable-provenance.css` |
| `app/static/js/detalle_anio_actual.js` | `app/static/js/current_year_detail.js` |
| `app/static/js/procedencia_editable.js` | `app/static/js/editable_provenance.js` |
| `app/static/js/referencia_mi_retiro_seguro.js` | `app/static/js/mi_retiro_seguro_reference.js` |
| `app/static/js/tema.js` | `app/static/js/theme.js` |
| `app/templates/como_se_calcula.html` | `app/templates/calculation_guide.html` |
| `app/templates/comparar.html` | `app/templates/comparison.html` |
| `app/templates/dev_centro_desarrollo.html` | `app/templates/dev_development_center.html` |
| `app/templates/metodologia.html` | `app/templates/methodology.html` |
| `app/templates/partials/detalle_anio_actual.html` | `app/templates/partials/current_year_detail.html` |
| `app/templates/partials/importacion_ficha_digital.html` | `app/templates/partials/ficha_digital_import.html` |
| `app/templates/partials/referencia_mi_retiro_seguro.html` | `app/templates/partials/mi_retiro_seguro_reference.html` |
| `tests/test_dev2_centro_desarrollo.py` | `tests/test_dev2_development_center.py` |
| `tests/test_ux44_detalle_anio_actual.py` | `tests/test_ux44_current_year_detail.py` |
| `tests/test_ux44_referencia_pdf.py` | `tests/test_ux44_pdf_reference.py` |
| `tests/test_ux46d_revision18_procedencia_persistencia.py` | `tests/test_ux46d_revision18_provenance_persistence.py` |
| `tests/test_ux46d_revision19_sincronizacion_actual.py` | `tests/test_ux46d_revision19_current_sync.py` |
| `tests/test_ux46d_revision23_ficha_actualiza_cuotas.py` | `tests/test_ux46d_revision23_ficha_updates_contributions.py` |
| `tests/test_ux46e_r81_procedencia_editable.py` | `tests/test_ux46e_r81_editable_provenance.py` |
| `tests/test_ux46f_r1_consistencia_procedencia_adjuntos.py` | `tests/test_ux46f_r1_attachment_provenance_consistency.py` |
| `tests/test_ux46g_r1_escenarios_retiro.py` | `tests/test_ux46g_r1_retirement_scenarios.py` |
| `tests/test_ux46i_r1_como_se_calcula.py` | `tests/test_ux46i_r1_calculation_guide.py` |
| `regulations/general_parameters.json` | `regulations/general-parameters.json` |

## Referencias actualizadas

- `app.services.centro_desarrollo` → **app.services.development_center** reemplazos en superficies vivas.
- `app.services.como_se_calcula` → **app.services.calculation_guide** reemplazos en superficies vivas.
- `app.services.detalle_anio_actual` → **app.services.current_year_detail** reemplazos en superficies vivas.
- `app.services.referencia_mi_retiro_seguro` → **app.services.mi_retiro_seguro_reference** reemplazos en superficies vivas.
- `centro_desarrollo.py` → **development_center.py** reemplazos en superficies vivas.
- `como_se_calcula.py` → **calculation_guide.py** reemplazos en superficies vivas.
- `detalle_anio_actual.py` → **current_year_detail.py** reemplazos en superficies vivas.
- `referencia_mi_retiro_seguro.py` → **mi_retiro_seguro_reference.py** reemplazos en superficies vivas.
- `como-se-calcula.css` → **calculation-guide.css** reemplazos en superficies vivas.
- `procedencia-editable.css` → **editable-provenance.css** reemplazos en superficies vivas.
- `detalle_anio_actual.js` → **current_year_detail.js** reemplazos en superficies vivas.
- `procedencia_editable.js` → **editable_provenance.js** reemplazos en superficies vivas.
- `referencia_mi_retiro_seguro.js` → **mi_retiro_seguro_reference.js** reemplazos en superficies vivas.
- `tema.js` → **theme.js** reemplazos en superficies vivas.
- `como_se_calcula.html` → **calculation_guide.html** reemplazos en superficies vivas.
- `comparar.html` → **comparison.html** reemplazos en superficies vivas.
- `dev_centro_desarrollo.html` → **dev_development_center.html** reemplazos en superficies vivas.
- `metodologia.html` → **methodology.html** reemplazos en superficies vivas.
- `partials/detalle_anio_actual.html` → **partials/current_year_detail.html** reemplazos en superficies vivas.
- `partials/importacion_ficha_digital.html` → **partials/ficha_digital_import.html** reemplazos en superficies vivas.
- `partials/referencia_mi_retiro_seguro.html` → **partials/mi_retiro_seguro_reference.html** reemplazos en superficies vivas.
- `test_dev2_centro_desarrollo.py` → **test_dev2_development_center.py** reemplazos en superficies vivas.
- `test_ux44_detalle_anio_actual.py` → **test_ux44_current_year_detail.py** reemplazos en superficies vivas.
- `test_ux44_referencia_pdf.py` → **test_ux44_pdf_reference.py** reemplazos en superficies vivas.
- `test_ux46d_revision18_procedencia_persistencia.py` → **test_ux46d_revision18_provenance_persistence.py** reemplazos en superficies vivas.
- `test_ux46d_revision19_sincronizacion_actual.py` → **test_ux46d_revision19_current_sync.py** reemplazos en superficies vivas.
- `test_ux46d_revision23_ficha_actualiza_cuotas.py` → **test_ux46d_revision23_ficha_updates_contributions.py** reemplazos en superficies vivas.
- `test_ux46e_r81_procedencia_editable.py` → **test_ux46e_r81_editable_provenance.py** reemplazos en superficies vivas.
- `test_ux46f_r1_consistencia_procedencia_adjuntos.py` → **test_ux46f_r1_attachment_provenance_consistency.py** reemplazos en superficies vivas.
- `test_ux46g_r1_escenarios_retiro.py` → **test_ux46g_r1_retirement_scenarios.py** reemplazos en superficies vivas.
- `test_ux46i_r1_como_se_calcula.py` → **test_ux46i_r1_calculation_guide.py** reemplazos en superficies vivas.
- `general_parameters.json` → **general-parameters.json** reemplazos en superficies vivas.

## Garantías

- cero rutas origen de los 28 movimientos permanecen en el árbol;
- todas las rutas destino existen;
- imports Python del runtime usan los nuevos módulos;
- plantillas y recursos estáticos usan los nuevos nombres;
- `regulations/general-parameters.json` sustituye la ruta técnica anterior;
- las URL `/como-se-calcula`, `/comparar`, `/metodologia` y
  `/dev/centro-desarrollo` permanecen estables;
- `VERSION` no cambia;
- SEC.2 continúa pausado.

## Siguiente revisión

**NOR.2 R4** migrará la documentación viva hacia las áreas canónicas definidas
en R2 y actualizará enlaces de manera atómica.
