# NOR.3 R8 — Auditoría de cierre estructural

**Estado:** validation — candidato estructural listo para promoción
**Versión de aplicación:** `0.1.21.01-beta`
**Candidato reservado:** `0.1.22.01-beta` — G122/E01
**Bloque:** NOR.3 R1–R8
**Pull Request:** #162
**Base Git:** `b54b2d27e78d08e62d54873b749af1f99a6ce120`
**Fecha:** 2026-09-13
**Clasificación:** Auditoría / Repositorio / Cierre estructural

## 1. Alcance

Esta auditoría cierra el alcance estructural propio de NOR.3 R1–R8. Verifica
ownership, rutas, profundidad, portales, templates, assets, taxonomía de
pruebas, `data/`, `scripts/`, política machine-readable y documentación
estructural afectada por la fase.

No declara completada la auditoría transversal post-NOR.3 de todo el contenido
documental ni de todos los archivos de código. Esa revisión se ejecutará como
fase posterior después de reconciliar todos los Issues y sanear
Dependabot/alertas de seguridad.

## 2. Estado estructural consolidado

- Backend: App Asegurado y Portal Developer separados por ownership.
- Templates: Asegurado, Developer y shared diferenciados.
- Assets: Asegurado, Developer y shared diferenciados.
- Tests: 216 módulos `test_*.py` después de crear el contrato R8;
  no existen módulos `test_*.py` planos en `tests/`.
- Data versionado: 2 artefactos en `data/audits/` y 4 en
  `data/governance/`.
- `data/developer/`: estado local/ignorado, no versionado.
- Scripts versionables: 19 entry points planos.
- Markdown versionable: 170 documentos al materializar esta
  auditoría.
- Política: `data/governance/repository-structure-policy.json`.

## 3. Evidencia de revisiones

- R1–R2: inventario, contrato, policy y bootstrap de gobierno.
- R3–R4: portales backend y templates.
- R5–R6: assets por ownership y taxonomía de pruebas.
- R7: `data/`, auditoría de `scripts/`, consumidores reconciliados y FULL
  11/11 GREEN.
- R8: cierre documental/estructural, contrato permanente y preparación para
  promoción G122/E01.

El checkpoint firmado más reciente previo a R7–R8 es
`b54b2d27e78d08e62d54873b749af1f99a6ce120`.

## 4. Validación R7 heredada

R7 acreditó:

- Repository Quality Gate FULL: 11 PASS / 0 FAIL;
- `unittest`: 1574 pruebas OK;
- `pytest`: 1614 passed + 7708 subtests passed;
- JavaScript: 27 archivos válidos;
- integridad: 644 archivos versionables y 84 directorios canónicos;
- Markdown: 170 documentos sin bloqueantes;
- `git diff --check`: limpio.

Evidencia heredada/revalidada de R7 disponible al iniciar R8:

```text
El reporte JSON local de R7 no estaba disponible en Downloads. R8 v3 revalidó el árbol R7, el inventario de 215 módulos, el contrato data/scripts, HEAD/VERSION y git diff --check. El Quality Gate FULL integral se ejecutará nuevamente dentro del cierre R8 antes de conservar cualquier mutación.
```

## 5. Estado de promoción

G122/E01 (`0.1.22.01-beta`) permanece **reservado/no aceptado** durante
esta auditoría. R8 no modifica `VERSION`. Solo después de que este cierre quede
GREEN se prepara la promoción revision-aware, se repiten los gates y se crea
el commit firmado R7–R8/promoción dentro del PR #162.

La aceptación contable definitiva de G122/E01 ocurre después del merge y la
revalidación de `main`, conforme al proceso de release vigente.

## 6. Continuidad posterior

Después de cerrar NOR.3 se ejecutará, en este orden:

1. reconciliación integral de Issues;
2. auditoría/corrección de Pull Requests Dependabot y alertas abiertas/cerradas;
3. fase transversal de auditoría de documentación y código, incluyendo
   headers/docstrings/comentarios donde el formato y las políticas lo permitan;
4. replanificación maestra post-NOR.3 antes de iniciar PERSIST.1 u otro bloque.

Por tanto, la **auditoría transversal post-NOR.3** queda explícitamente
diferida y no se presenta como evidencia ya ejecutada por R8.
