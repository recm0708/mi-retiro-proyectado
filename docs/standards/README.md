# Estándares del repositorio

**Proyecto:** Mi Retiro Proyectado
**Fase:** NOR.1 — Definición de estándares del repositorio

## Propósito

Esta carpeta contiene los documentos canónicos que establecen las reglas de
organización, nomenclatura y mantenimiento del repositorio.

El objetivo es que cualquier archivo, carpeta, documento, componente de código,
prueba o evidencia creada en el futuro siga una estructura uniforme y que NOR.2
pueda auditar el árbol existente contra reglas determinísticas.

## Alcance

Los estándares definidos aquí aplican a:

- estructura de carpetas;
- nombres de archivos;
- documentación;
- código fuente;
- archivos de configuración;
- datos;
- pruebas;
- evidencias;
- raíz del repositorio;
- artefactos locales no versionados;
- procesos de reemplazo y migración.

## Documentos canónicos

- [Estructura del repositorio](repository-structure.md) — estructura y responsabilidades.
- [Convenciones de nombres](naming-conventions.md) — reglas determinísticas de nombres.
- [Estándares de archivos](file-standards.md) — requisitos mínimos por tipo de archivo.
- [Estándares de documentación](documentation-standards.md) — documentación viva, histórica y referencias.
- [Política de estilo y lint de Markdown](markdown-style-and-lint.md) — reglas de markdownlint, excepciones acotadas y prevención para documentación nueva.
- [Ciclo de vida de archivos y componentes](artifact-lifecycle.md) — creación, sustitución, archivo y eliminación.
- [Raíz y artefactos locales](root-and-local-artifacts.md) — raíz, evidencias y artefactos locales.
- [Identificadores de bloques de trabajo](work-block-identifiers.md) — familias, bloques, revisiones y reglas de asignación.

Cuando una política técnica anterior contradiga estos documentos, prevalece el
estándar NOR.1 más reciente. Las reglas especializadas no contradictorias
continúan vigentes.

## Idioma de la documentación

El contenido de los documentos del proyecto se redacta en español.

Se conservan términos técnicos en su idioma original cuando corresponda, por
ejemplo: GitHub, Python, FastAPI, workflow, commit, branch, pull request, API,
framework y runtime.

Los nombres técnicos de archivos, carpetas y rutas mantienen la convención
definida por este estándar.

## Aplicación

NOR.1 consolidó en R7 la definición inicial de las reglas y quedó cerrado
definitivamente en R8/G112-E07 al incorporar el gobierno canónico de
identificadores de bloques de trabajo.

NOR.2 auditó y normalizó el repositorio existente contra estas reglas y quedó
cerrado después de completar R1–R8. SEC.2 quedó cerrado después de R1–R6;
AUD.SEC2 R1 aplicó nuevamente estos estándares al saneamiento post-cierre.

DOC.1 R2, ya cerrado, incorporó `scripts/audit_markdown.py` como control
permanente. En el estado vigente, su ejecución forma parte del
`Repository Quality Gate`; `Python Compatibility` se conserva como required
check independiente y la evidencia histórica del antiguo workflow Markdown no
se reescribe.

## Estándares especializados consolidados en NOR.2 R4

- [Estándar de código y comentarios](code-and-comments.md) — comentarios, docstrings y documentación interna por tipo de código.
- [Política de estructura de archivos por extensión](file-structure-by-extension.md) — estructura interna y comentarios permitidos por extensión.

Estos documentos complementan los estándares determinísticos de NOR.1 y no
restablecen las rutas heredadas de la raíz de `docs/`.
