# MANT.1 R8 — Auditoría y decisión de consolidación de scripts y tests

**Estado:** evidencia de ejecución / decisión técnica de MANT.1 R8
**Issue propietario:** #163
**Rama de trabajo:** `maintenance/mant1-r8-auditoria-consolidacion`
**Baseline auditado:** `ebafa9dd899c2c69e68de70f3a163ffffb874bdc`
**VERSION de entrada:** `0.1.23.01-beta`
**Fecha:** 2026-09-14

## Objetivo

MANT.1 R8 auditó `scripts/` y `tests/` para determinar si existían wrappers,
one-shots, reconciliadores o pruebas redundantes que pudieran consolidarse o
retirarse sin perder responsabilidad vigente, evidencia histórica o cobertura.

La regla aplicada fue conservadora: ninguna fusión o eliminación se autoriza
solo por antigüedad, semejanza nominal o pertenencia a una fase cerrada.

## Scripts

La línea base contiene **16 scripts operativos**. La auditoría de consumidores
confirmó referencias reales para todos ellos y no encontró wrappers históricos
prohibidos G122/G123 versionados.

Decisión:

- **CONSERVAR:** 16;
- **CONSOLIDAR:** 0;
- **RETIRAR:** 0;
- **MOVER:** 0.

La estructura plana de `scripts/` continúa siendo adecuada; no existe una razón
operativa demostrada para crear subdirectorios adicionales.

La tabla inicial de `scripts/README.md` tenía cinco omisiones:

- `audit_action_references.py`;
- `audit_block_identifiers.py`;
- `audit_external_links.py`;
- `audit_signed_tags.py`;
- `visual_a11y_audit.mjs`.

MANT.1 R8 sincroniza esa tabla con los 16 scripts operativos y añade una
regresión permanente de paridad entre el inventario documentado y los archivos
operativos presentes.

## Tests

La línea base previa al nuevo guard de labels tenía **218 módulos** `test_*.py`.
MANT.1 R8 incorpora `tests/governance/test_github_label_taxonomy.py`, por lo
que el inventario vigente pasa a **219 módulos**.

La auditoría semántica V2 examinó los 219 módulos y **1,633 funciones
`test_*`**. Resultado estructural:

- duplicados AST exactos: **0**;
- grupos estructuralmente equivalentes: **0**;
- módulos sin funciones `test_*`: **0**;
- pares con similitud contractual mayor o igual a 0.80: **2**.

Los dos pares similares fueron:

1. `test_g115_promotion_post_merge.py` /
   `test_g116_promotion_post_merge.py`;
2. `test_g119_promotion_post_merge.py` /
   `test_g120_promotion_post_merge.py`.

No son duplicados: cada archivo protege su propio Global, bloque, ordinal,
VERSION histórica, evidencia de PR/merge y publicación. Ambos pares se
conservan.

## Revisión de módulos históricos

El clasificador heurístico marcó 45 módulos de `tests/governance/` como
`HISTORICO_REVISAR`. La revisión por responsabilidad mostró que esa categoría
mezclaba guards permanentes con regresiones históricas protegidas.

Distribución de esos 45 módulos por familia nominal:

| Familia | Módulos | Decisión |
| --- | ---: | --- |
| DOC | 5 | Conservar |
| Gobierno / infraestructura | 18 | Conservar |
| PLAN | 10 | Conservar |
| UX.4.6e | 4 | Conservar |
| VER.2 | 8 | Conservar |

Ejemplos de contratos permanentes que no deben retirarse:

- `test_git_history_attestation.py`: manifiesto HIST, frontera de firmas y
  contraste con Git real;
- `test_doc1_r5_markdown_auditor.py`: comportamiento actual de
  `scripts/audit_markdown.py`;
- `test_plan1_guard_referencias_historicas.py`: impide que planificación
  sustituida vuelva a aparecer como objetivo prospectivo;
- `test_ux46e_auditoria_coherencia.py`: higiene transversal, enlaces,
  docstrings, almacenamiento web y trazabilidad ADR;
- `test_ver2_version_revision_aware.py`: constructor, parser y validez del
  esquema revision-aware vigente.

Ejemplo de regresión histórica protegida:

- `test_ver2_r4_promocion_g071_e01.py`: preserva la evidencia de G071/E01 y
  las reglas de publicación sin congelar la VERSION actual.

## Promociones G109–G123

Los 15 módulos de promoción G109–G123 se conservan. La auditoría inicial no
detectó huellas estructurales idénticas y la revisión semántica confirmó
responsabilidades específicas por estado aceptado.

G123 permanece separado porque además protege el estado vivo de MANT.2 R1,
las dependencias materializadas y la disponibilidad de G124 sin candidato
preasignado.

## Matriz final

| Acción | Scripts | Tests |
| --- | ---: | ---: |
| CONSERVAR | 16 | 219 |
| CONSOLIDAR | 0 | 0 |
| RETIRAR | 0 | 0 |
| REVISAR pendiente | 0 | 0 |

La ausencia de eliminaciones es el resultado de la auditoría, no una excepción
al alcance de MANT.1 R8: no se demostró redundancia con cobertura equivalente
que justificara reducir código o pruebas.

## `tests/validation_cases/`

`tests/validation_cases/` se mantiene como datos/evidencia de validación. No se
convierte artificialmente en una nueva carpeta de módulos de pruebas.

## Gobierno y labels relacionado

La misma revisión detectó deriva entre las superficies de labels y una
configuración histórica de GitHub Release. MANT.1 R8 reconcilia:

- 16 labels canónicos de ownership/superficie;
- 12 labels suplementarios de GitHub;
- 28 labels remotos activos en total;
- Issue Forms y `.github/labeler.yml`;
- `.github/release.yml`;
- documentación operativa;
- un guard automatizado de taxonomía.

No se crean los sinónimos `ux`, `technical-debt`, `qa` o `testing`.

## Estado protegido

Esta auditoría no autoriza modificar motores previsionales, normativa,
persistencia local, `VERSION`, ledger, registry ni manifest. Durante la
auditoría semántica el working tree no recibió cambios adicionales.

G124 permanece como siguiente Global disponible, sin candidato ni VERSION
preasignados hasta que MANT.1 R8 supere su validación integral.

## Nota de promoción G124/E13

La matriz de 219 módulos corresponde al corpus auditado antes de materializar
la promoción. G124/E13 añade posteriormente un único guard
`tests/governance/test_g124_mant1_r8_promotion.py`; por tanto el inventario
final pasa a 220 módulos sin alterar la conclusión de auditoría ni introducir
una nueva familia funcional de pruebas.

La revalidación final post-materialización de G124/E13 cerró el Quality Gate FULL en **11 PASS / 0 FAIL**, con **1600 unittest OK** y **pytest 1640 passed + 7782 subtests**.
