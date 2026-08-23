# Auditoría MANT.1 R5F — nombres de archivos

## Propósito

Esta auditoría documenta la revisión **MANT.1 R5F**, enfocada en normalizar nombres de archivos técnicos hacia una convención más clara y consistente en inglés, sin modificar la lógica funcional del cálculo de pensión ni los valores normativos.

## Alcance aplicado

En esta revisión se renombraron archivos de soporte técnico, configuración, datos estructurados y pruebas automatizadas cuando el nombre anterior estaba en español o no seguía la convención técnica adoptada.

## Renombres realizados

| Archivo anterior | Archivo nuevo | Motivo |
|---|---|---|
| `scripts/configurar_hooks_git.ps1` | `scripts/configure_git_hooks.ps1` | Normaliza nombre de script operativo en inglés. |
| `scripts/validar_precommit.py` | `scripts/validate_precommit.py` | Normaliza nombre del validador local de pre-commit. |
| `data/ledger_revisiones_pre_1_0.json` | `data/revision_ledger_pre_1_0.json` | Normaliza nombre del ledger estructurado de revisiones. |
| `regulations/parametros_generales.json` | `regulations/general_parameters.json` | Normaliza nombre del archivo de parámetros generales. |
| `tests/test_comparador.py` | `tests/test_comparator.py` | Normaliza nombre de prueba. |
| `tests/test_fuentes_normativas.py` | `tests/test_regulatory_sources.py` | Normaliza nombre de prueba. |
| `tests/test_proyeccion_salarios.py` | `tests/test_salary_projection.py` | Normaliza nombre de prueba. |
| `tests/test_resultados.py` | `tests/test_results.py` | Normaliza nombre de prueba. |
| `tests/test_resultados_mixto.py` | `tests/test_mixto_results.py` | Normaliza nombre de prueba. |
| `tests/test_resultados_modalidades.py` | `tests/test_modality_results.py` | Normaliza nombre de prueba. |
| `tests/test_resultados_sucgs.py` | `tests/test_sucgs_results.py` | Normaliza nombre de prueba. |
| `tests/test_retiro.py` | `tests/test_retirement.py` | Normaliza nombre de prueba. |
| `tests/test_trazabilidad.py` | `tests/test_traceability.py` | Normaliza nombre de prueba. |

## Exclusiones deliberadas

No se renombraron los archivos `regulations/mixto.json`, `regulations/sebd.json` ni `regulations/sucgs.json`, porque esos nombres representan modalidades o sistemas propios del dominio funcional de la aplicación.

Tampoco se renombraron archivos históricos con patrones como `UX46`, `VER2`, `revision` o `revision-aware`, porque preservan trazabilidad documental y se revisarán, si aplica, en una fase documental posterior.

## Referencias actualizadas

Se actualizaron referencias en documentación, scripts, hooks, pruebas y módulos de soporte para que apunten a los nombres nuevos.

## Validación esperada

La revisión debe pasar como mínimo:

- `python -m compileall app tests -q`
- `python -m pytest tests\test_mant1_scripts_hooks_documentados.py tests\test_precommit_guard.py -q`
- `python -m pytest tests\test_mant1_r5e_nombres_carpetas.py -q`
- `python -m pytest tests\test_mant1_r5f_nombres_archivos.py -q`

Antes del cierre del PR también debe ejecutarse la suite completa.

## Relación con SEC.2

Esta revisión forma parte del saneamiento técnico previo a **SEC.2**. El objetivo es llegar a la fase de seguridad con estructura, nombres, rutas y documentación base consistentes.
