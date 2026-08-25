# Auditoría integral Markdown post-NOR.2 — DOC.1 R2

**Estado:** cerrado
**Clasificación:** auditoría / evidencia documental
**Revisión:** DOC.1 R2
**Fecha:** 2026-08-24
**Versión de aplicación revisada:** `0.0.71.01-beta`

## Propósito

Esta auditoría revisa de forma integral la documentación Markdown del repositorio
después del cierre de NOR.2. Su objetivo es comprobar que el árbol documental
actual cumple los estándares consolidados de documentación, conserva
correctamente la evidencia histórica y dispone de controles permanentes que
eviten regresiones.

## Alcance

La revisión comprende todos los archivos Markdown versionados y distingue entre:

- documentación vigente;
- auditorías y evidencias;
- documentación histórica;
- plantillas;
- documentación técnica de soporte.

La auditoría considera estructura Markdown, metadata, versión documentada,
vigencia semántica, idioma, enlaces locales, rutas retiradas, stubs de
compatibilidad y preservación de la verdad histórica.

## Línea base

Antes de crear este informe permanente, el árbol auditado contenía **137**
archivos Markdown:

- **56** documentos vigentes;
- **12** auditorías o evidencias;
- **64** documentos históricos;
- **1** plantilla;
- **4** documentos técnicos de soporte.

La auditoría automática final de esa línea base no reportó problemas
bloqueantes.

## Hallazgos y correcciones

### Inventario inicial

La primera inspección de DOC.1 R2 encontró **141** archivos Markdown
versionados. El análisis inicial identificó:

- **34** incidencias relacionadas con metadata;
- **12** estados vigentes potencialmente desactualizados;
- **50** enlaces locales rotos;
- **1** incidencia de formato;
- **0** coincidencias concluyentes de prosa inglesa mediante el heurístico
  automático.

Los resultados fueron revisados manualmente antes de aplicar correcciones para
evitar modificar evidencia histórica válida.

### Metadata y vigencia documental

Se normalizó la metadata de documentación vigente para distinguir entre la
versión actualmente revisada y las bases históricas preservadas. También se
corrigieron etiquetas ambiguas o duplicadas y se actualizaron estados que
todavía presentaban como activas fases ya cerradas.

Las referencias históricas a versiones, candidatos, fases y estados anteriores
se conservaron cuando describían correctamente el momento documentado.

### Rutas de compatibilidad retiradas

Se identificaron cuatro documentos que existían únicamente como stubs de
compatibilidad:

- `docs/product/user-interface.md`;
- `docs/product/workflow-step-1-personal-data.md`;
- `docs/product/workflow-step-2-contributions.md`;
- `docs/product/workflow-step-3-salary-history.md`.

Las referencias vigentes fueron redirigidas hacia la documentación histórica
correspondiente y los cuatro stubs fueron retirados. Las pruebas conservan
referencias negativas únicamente para verificar que esas rutas no reaparezcan.

Después de esta corrección, el inventario físico pasó de **141** a **137**
archivos Markdown.

### Documentación histórica

La revisión confirmó que los enlaces rotos encontrados principalmente bajo
`docs/archive/` representan rutas válidas del estado histórico registrado y no
deben modernizarse mecánicamente.

También se corrigieron únicamente aspectos de formato en metadata histórica
cuando la semántica original debía preservarse.

### Controles permanentes incorporados

DOC.1 R2 incorpora `scripts/audit_markdown.py` como auditor permanente de la
documentación Markdown. El control quedó integrado en:

- `scripts/validate_precommit.py`;
- el gate local de pre-commit;
- `.github/workflows/markdown-audit.yml`;
- pruebas de regresión específicas en `tests/test_markdown_audit.py`.

El auditor verifica estructura Markdown, metadata, coherencia de versión,
enlaces locales según clasificación, stubs de compatibilidad, idioma de forma
conservadora y bloques de código Markdown sin cerrar.

Las reglas permanentes correspondientes también quedaron formalizadas en
`docs/standards/documentation-standards.md`.

## Estado previo al gate final

La revisión documental y sus regresiones focales quedaron completadas antes del
gate integral de cierre.

A este checkpoint:

- los cuatro stubs documentales residuales fueron retirados;
- la documentación vigente quedó reconciliada con `0.0.71.01-beta`;
- la evidencia histórica conserva su semántica original;
- el estándar documental quedó ampliado con reglas de metadata, enlaces
  históricos, compatibilidad y auditoría automática;
- `scripts/audit_markdown.py` está integrado al validador local;
- existe una regresión específica del auditor;
- existe un workflow dedicado de GitHub Actions;
- roadmap, plan maestro, validación, trazabilidad y CHANGELOG están
  sincronizados con DOC.1 R2;
- SEC.2 permanece habilitado como siguiente bloque, pero todavía no se inicia
  formalmente.

El estado de esta evidencia permanece **en ejecución** hasta completar la suite
integral, pre-commit, PR, CI, integración y verificación post-merge.

## Gate integral local

Después de reconciliar las regresiones documentales afectadas por la
normalización, la suite completa quedó en:

- **1041 pruebas aprobadas**;
- **4876 subtests aprobados**;
- **0 fallos**;
- auditor Markdown: **OK**;
- `git diff --check`: **OK**.

Durante este gate se detectaron y corrigieron regresiones que conservaban
contratos textuales anteriores sobre metadata, estado de SEC.2, publicación de
VER.2 y estructura del registro ADR. También se confirmó que
`docs/decisions/README.md` consolida ADR-001–ADR-178, mientras ADR-179 permanece
como documento independiente.

El pre-commit integral quedó superado: auditor Markdown, dependencias, compilación
Python, sintaxis de los 18 archivos JavaScript y **1001 tests de `unittest`**
quedaron en **OK**. El inventario preparado contiene **138 archivos Markdown**,
incluidos **13 documentos de auditoría**.

Solo permanecen pendientes los gates remotos de PR, CI, integración y
verificación post-merge.
