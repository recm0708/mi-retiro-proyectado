# Política de estructura de archivos por extensión

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.19.05-beta`
**Checkpoint técnico:** Mantenibilidad previa a SEC.2
**Clasificación:** Técnica / Mantenibilidad

> Desde NOR.1, esta política conserva las reglas especializadas por extensión,
> pero la estructura, nomenclatura, raíz y ciclo de vida se subordinan a los
> estándares canónicos de `docs/standards/`.

Esta política define cómo deben estructurarse los archivos del proyecto según su
extensión. Su objetivo es que los archivos actuales y futuros mantengan una forma
predecible, revisable y homogénea sin convertir el código operativo en una
bitácora histórica.

La trazabilidad de revisiones, Pull Requests, bloques de trabajo o decisiones de
cierre pertenece a la documentación. Los archivos operativos deben explicar su
propósito, contrato, flujo, dependencias o riesgos técnicos permanentes.

## 1. Reglas transversales

1. Todo archivo textual nuevo debe tener una intención clara desde sus primeras
   líneas, salvo archivos cuyo formato no permita comentarios.
2. Los comentarios iniciales describen propósito y alcance permanente, no la
   revisión que los creó.
3. Los comentarios de sección se usan para separar responsabilidades internas.
4. Los comentarios de línea se reservan para decisiones no obvias, restricciones
   de formato o riesgos de modificación.
5. No se agregan comentarios que repitan literalmente una instrucción evidente.
6. Los archivos binarios no tienen encabezado textual; su propósito se documenta
   por nombre, ubicación y documentación asociada.
7. Los archivos de pruebas pueden conservar identificadores históricos cuando la
   prueba verifica una regresión o contrato de una revisión concreta.

## 2. Política por extensión

| Extensión o tipo | Encabezado esperado | Comentarios internos | Observaciones |
| --- | --- | --- | --- |
| `.md` | H1 único y descriptivo; metadata en negrita cuando aplique. | H2/H3 según la función documental; listas, tablas y bloques de código solo cuando aporten estructura real. | Contenido en español; enlaces a documentos con título humano; historia/auditorías se preservan; aplica `documentation-standards.md` y las plantillas documentales. |
| `.py` | Docstring de módulo con propósito permanente. | Docstrings en funciones/clases públicas y comentarios antes de lógica no obvia. | No usar encabezados de revisión en módulos operativos. |
| `.js` | `"use strict";` cuando aplique y bloque inicial con `Mi Retiro Proyectado —`, `Propósito` y `Alcance`. | Secciones para storage, eventos, API, renderizado e invalidación. | JavaScript no replica fórmulas previsionales. |
| `.css` | Bloque inicial con `Mi Retiro Proyectado —`, `Propósito` y `Alcance`. | Comentarios de sección para componentes, estados, temas y responsive. | No comentar cada regla evidente. |
| `.html` | En plantillas Jinja con `{% extends %}`, el `extends` se conserva al inicio. | Comentarios Jinja/HTML para secciones grandes, parciales y contratos visuales. | No anteponer comentarios al `<!DOCTYPE html>` de `base.html`. |
| `.yml` / `.yaml` | Comentarios iniciales de propósito y alcance. | Comentarios solo donde aclaren permisos, triggers, cadencia o matrices. | No cambiar acciones ni comandos por documentar. |
| `.json` / `.jsonc` | JSON no admite comentarios; JSONC puede usarlos cuando el contrato de la herramienta lo permita. | Documentar mediante nombres de claves y comentarios solo en JSONC cuando aporten contexto real. | Respetar primero el formato exigido por la herramienta; los archivos versionados mantienen LF. |
| `.ps1` | Comentarios `#` al inicio con propósito, entradas y alcance. | Comentarios antes de pasos destructivos, validaciones o decisiones de ruta. | Mantener comandos legibles y sin trazabilidad histórica operativa. |
| `.githook` / hooks sin extensión | Shebang si aplica y comentarios de responsabilidad. | Comentarios de flujo antes de validaciones o delegaciones. | El hook debe delegar lógica compleja a scripts versionados. |
| `.txt` | Comentarios iniciales si el formato los acepta; si no, contenido directo. | Estructura por bloques cuando sea inventario, lista o dependencia. | `requirements.txt` puede documentar grupos de dependencias. |
| `.gitignore` | Encabezado breve de propósito. | Secciones por tipo de artefacto excluido. | No excluir archivos fuente necesarios. |
| `.gitattributes` | Encabezado breve de normalización. | Secciones para texto, binarios y casos especiales. | Debe proteger finales de línea y archivos binarios. |
| `.editorconfig` | Sin comentarios obligatorios; declarar `root = true` y reglas generales. | Comentarios opcionales si una regla no es evidente. | Define estilo transversal del editor. |
| archivos sin extensión | Depende del contrato del archivo. | Comentarios solo si el formato los acepta. | `VERSION`, `LICENSE`, `CODEOWNERS` y firmas tienen reglas propias. |
| `.png` / `.ico` | No aplica encabezado textual. | No aplica. | Usar nombre descriptivo, carpeta correcta y documentación externa. |
| `.pdf` / `.xlsx` | No aplica encabezado textual. | No aplica. | Las fuentes oficiales preservadas usan nombre canónico, ubicación documental y entrada con SHA-256 en `docs/regulatory/sources/official/manifest.json`. |

## 3. Plantillas oficiales

Las plantillas técnicas viven en `docs/templates/file-structure/`. Cada plantilla usa la
extensión que representa cuando el formato lo permite. Markdown cuenta con
`template.md` como base técnica. Para archivos binarios se incluyen ejemplos mínimos
válidos y su uso se explica en el README de plantillas.

Los documentos Markdown requieren además una estructura acorde con su función. Las
variantes de documento vigente, estándar/política, auditoría/evidencia, registro
histórico y ADR viven en `docs/templates/documentation/`. La selección y uso de esas
plantillas se rige por `documentation-standards.md`.

## 4. Aplicación en archivos actuales

El primer ajuste de uniformidad se concentró en JavaScript y CSS de
`app/static/`, porque ahí existían encabezados funcionalmente equivalentes pero
con estilos diferentes. Python, YAML, scripts, hooks, JSON y archivos especiales
quedan cubiertos por la política y las plantillas sin reescritura masiva cuando
su estructura actual ya cumple su contrato.

NOR.2 revisó y normalizó los nombres y ubicaciones existentes contra las reglas
determinísticas de NOR.1 y quedó cerrado después de completar R1–R8.

## 5. Política de nombres de carpetas

Las reglas canónicas de nombres se definen en
`docs/standards/naming-conventions.md`.

Se mantienen como principios:

1. Los paquetes Python usan nombres técnicos en inglés.
2. Los parámetros normativos versionados viven en `regulations/`.
3. Los casos de validación viven en `tests/validation_cases/`.
4. El archivo histórico documental vive en `docs/archive/`.
5. Las carpetas convencionales externas no se renombran cuando pertenecen al
   ecosistema.
6. `_entregas/` es un nombre local heredado retirado por NOR.2 R7; permanece
   en `.gitignore` únicamente como protección contra reaparición accidental.
7. Los entregables y evidencias locales se ubican en `_deliverables/`, que no
   forma parte del árbol Git canónico.
8. Un renombre de carpeta exige actualizar imports, enlaces, rutas de pruebas,
   documentación, configuración y cualquier referencia textual que apunte a la
   ruta anterior.

La auditoría histórica aplicada queda documentada en
[Auditoría de nombres de carpetas — MANT.1 R5E](../archive/technical/folders-audit-r5e.md).

## 6. Regla para archivos futuros

Todo archivo nuevo debe escoger la plantilla más cercana, eliminar texto de
ejemplo, conservar la estructura de propósito/alcance y documentar solo
decisiones permanentes. Si una extensión nueva no tiene plantilla, primero se
debe registrar su política antes de agregar muchos archivos con ese formato.

La ubicación, nomenclatura y ciclo de vida se validan además contra
`docs/standards/`.
