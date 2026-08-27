# Plantillas del repositorio

Esta carpeta agrupa las plantillas canónicas utilizadas para crear archivos y
documentos nuevos sin duplicar reglas ni mezclar estructura técnica con
estructura editorial.

## Familias disponibles

- **[Plantillas de estructura por extensión](file-structure/README.md)** —
  estructura técnica mínima según el tipo o extensión del archivo.
- **[Plantillas documentales](documentation/README.md)** — estructuras
  semánticas para documentos Markdown según su función.

## Regla de elección

1. Si se crea un archivo por su **tipo técnico**, se consulta primero
   `file-structure/`.
2. Si el archivo es un documento Markdown, además se selecciona la plantilla de
   `documentation/` que corresponda a su función.
3. Las plantillas son puntos de partida: se eliminan secciones que no apliquen y
   no se conservan textos de ejemplo.
4. La documentación histórica y las auditorías no se modernizan únicamente para
   coincidir con el estado actual.
5. Las reglas canónicas prevalecen sobre cualquier ejemplo de plantilla.

Los estándares aplicables se encuentran en
**[Estándares de documentación](../standards/documentation-standards.md)** y
**[Política de estructura de archivos por extensión](../standards/file-structure-by-extension.md)**.
