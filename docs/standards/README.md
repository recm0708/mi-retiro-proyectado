# Estándares del repositorio

**Estado:** vigente
**Clasificación:** estándar / navegación

## Propósito

Esta carpeta reúne las reglas canónicas para organizar, nombrar, documentar,
mantener y retirar artefactos del repositorio.

Los estándares se aplican al estado actual del árbol y deben mantenerse como
contratos durables. Las fases que originaron una regla se conservan en Git,
auditorías o documentación histórica cuando esa procedencia siga siendo
relevante; no es necesario repetir su cronología en este índice.

## Alcance

Los estándares cubren:

- estructura de carpetas;
- nombres de archivos y componentes;
- documentación;
- código y comentarios;
- archivos de configuración;
- datos versionados;
- pruebas;
- evidencias;
- raíz del repositorio;
- artefactos locales no versionados;
- creación, sustitución, migración, archivo y eliminación de artefactos;
- identificadores de bloques de trabajo.

## Documentos canónicos

- [Estructura del repositorio](repository-structure.md) — organización y
  responsabilidades de las áreas canónicas.
- [Convenciones de nombres](naming-conventions.md) — reglas para nombres de
  archivos, carpetas y componentes.
- [Estándares de archivos](file-standards.md) — requisitos mínimos por tipo de
  archivo.
- [Estándares de documentación](documentation-standards.md) — clasificación,
  autoridad, mantenimiento, historia y referencias documentales.
- [Política de estilo y lint de Markdown](markdown-style-and-lint.md) — formato,
  markdownlint y excepciones acotadas.
- [Ciclo de vida de archivos y componentes](artifact-lifecycle.md) — creación,
  sustitución, archivo y eliminación.
- [Raíz y artefactos locales](root-and-local-artifacts.md) — contenido permitido
  en raíz y tratamiento de elementos locales.
- [Estándar de código y comentarios](code-and-comments.md) — comentarios,
  docstrings y documentación interna.
- [Estructura de archivos por extensión](file-structure-by-extension.md) —
  organización interna y comentarios permitidos según extensión.
- [Identificadores de bloques de trabajo](work-block-identifiers.md) — familias,
  bloques, revisiones y asignación de identificadores.

## Autoridad y aplicación

Cada estándar tiene autoridad sobre el tema que declara en su propósito. Si dos
documentos parecen definir la misma regla, debe eliminarse la duplicación o
declararse expresamente cuál es la autoridad principal.

Las políticas especializadas pueden complementar una regla general, pero no
contradecirla silenciosamente. Una excepción debe tener alcance mínimo,
justificación explícita y, cuando corresponda, una validación reproducible.

Los controles automatizados que implementen estos estándares forman parte del
contrato, pero el texto canónico de la regla permanece en la documentación
correspondiente. Los auditores y pruebas no deben obligar a documentos vivos a
conservar cronologías o frases históricas que no formen parte de su función.

## Idioma

La documentación del proyecto se redacta en español. Los términos técnicos se
mantienen en su forma oficial cuando resulte más preciso, por ejemplo: GitHub,
Python, FastAPI, workflow, commit, branch, pull request, API, framework y
runtime.

Los nombres técnicos de archivos, carpetas y rutas siguen sus convenciones
específicas y no se traducen solo por razones de idioma.

## Mantenimiento

Cuando cambie un estándar:

1. se actualiza la autoridad canónica;
2. se revisan los documentos dependientes;
3. se ajustan auditores o pruebas que implementen la regla;
4. se actualizan plantillas si el cambio afecta nuevos artefactos;
5. se conserva evidencia histórica fuera del documento vivo cuando sea
   necesaria para trazabilidad.

El índice general de documentación y su mapa de autoridades se encuentran en
[Documentación de Mi Retiro Proyectado](../README.md).
