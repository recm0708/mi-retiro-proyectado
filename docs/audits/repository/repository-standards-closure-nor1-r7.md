# Cierre de estándares del repositorio NOR.1 R7

**Proyecto:** Mi Retiro Proyectado

**Fase:** NOR.1 R7 — Cierre y preparación de NOR.2

**Estado de esta revisión:** candidato de cierre condicionado a gate local, CI y
merge.

## Objetivo

Cerrar NOR.1 después de definir, auditar y endurecer las reglas estructurales que
NOR.2 utilizará para normalizar el repositorio existente.

NOR.1 no ejecuta la normalización masiva. Su resultado es el contrato contra el
que NOR.2 debe auditar nombres, ubicaciones, documentación, evidencias,
artefactos locales y referencias.

## Resultado acumulado R1–R7

NOR.1 deja establecidos:

- estructura canónica del repositorio;
- estructura documental por responsabilidad;
- convenciones determinísticas de nombres;
- requisitos por tipo de archivo;
- ciclo de vida de archivos y componentes;
- reglas para documentación vigente, auditorías e históricos;
- política de raíz y artefactos locales;
- ubicación canónica de evidencias versionables;
- tratamiento de evidencia bruta reproducible;
- inventarios de estructura, nomenclatura y documentación;
- análisis de dependencias documentales;
- regresiones automáticas para proteger los estándares.

## Evidencia principal

NOR.1 conserva como evidencia versionada, entre otros:

- `docs/audits/repository/repository-structure-inventory-nor1-r2.txt`;
- `docs/audits/repository/naming-audit-nor1-r4.md`;
- `docs/audits/repository/nor1-r4-directory-inventory.txt`;
- `docs/audits/documentation/documentation-inventory-nor1-r3.txt`;
- `docs/audits/documentation/documentation-classification-nor1-r3.md`;
- `docs/audits/documentation/documentation-dependency-audit-nor1-r5.md`;
- `docs/audits/documentation/nor1-r5-documentation-inventory.txt`;
- `docs/standards/`.

El volcado bruto de dependencias documentales generado en R5 permanece como
evidencia local reproducible porque su contenido reintroducía literalmente rutas
legacy protegidas por regresiones.

## Gate previo observado

Antes de R7, NOR.1 R6 cerró localmente con:

- `git diff --check` sin errores;
- pruebas NOR.1: `5 passed`;
- pruebas NOR.1 + MANT.1 R5E: `9 passed, 19 subtests passed`;
- gate `pre-commit` completo;
- suite completa: `933 tests OK`;
- GitHub Actions en verde;
- PR #65 integrado por squash.

R7 debe considerarse cerrado únicamente después de repetir el gate aplicable,
obtener CI satisfactoria e integrar su Pull Request.

## Contrato de transición

Al integrarse R7:

1. NOR.1 queda cerrado como fase de definición y preparación.
2. NOR.2 pasa a ser la siguiente fase de normalización del repositorio.
3. NOR.2 debe aplicar los estándares de `docs/standards/` al árbol existente.
4. NOR.2 puede mover, renombrar, consolidar o retirar elementos cuando exista
   evidencia suficiente y todas las referencias se sincronicen.
5. SEC.2 permanece pausado hasta completar NOR.2.

## Alcance obligatorio de NOR.2

NOR.2 deberá revisar, como mínimo:

- raíz versionada;
- carpetas técnicas;
- archivos de código;
- JavaScript, CSS y plantillas;
- documentación vigente;
- auditorías e históricos;
- pruebas y nombres de regresiones;
- archivos de datos y configuración;
- `data/revision_ledger_pre_1_0.json`;
- directorio local heredado `_entregas/`;
- referencias cruzadas, imports, enlaces y rutas;
- duplicados, sustituidos y artefactos que no deban permanecer en el árbol
  actual.

## Regla de migración

Una migración de NOR.2 no se considera terminada mientras exista cualquiera de
estas condiciones:

- referencias vigentes a una ruta anterior;
- imports rotos;
- enlaces Markdown obsoletos;
- pruebas que dependan del nombre sustituido sin justificación histórica;
- documentos actuales que describan una estructura anterior;
- archivos sustituidos conservados sin razón documental;
- evidencia temporal en una ubicación canónica incorrecta.

## Elementos fuera de alcance de NOR.1 R7

R7 no modifica:

- fórmulas previsionales;
- motores de cálculo;
- parámetros regulatorios;
- versión de aplicación;
- rutas públicas funcionales;
- contratos JSON de dominio;
- comportamiento visible de la aplicación;
- SEC.2.

## Criterio de cierre

NOR.1 se considera formalmente cerrado cuando R7:

1. supera las pruebas focales;
2. supera el gate completo;
3. supera los workflows requeridos;
4. se integra a `main`.

Después de ese punto, cualquier corrección estructural detectada debe ejecutarse
bajo NOR.2, salvo un hotfix estrictamente necesario para reparar el propio
contrato de estándares.
