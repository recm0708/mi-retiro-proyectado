# Auditoría de estructura por extensión

**Estado:** Vigente
**Aplicación revisada:** `0.0.26-beta`
**Checkpoint técnico:** Mantenibilidad previa a SEC.2
**Clasificación:** Técnica / Auditoría

Esta auditoría revisa archivos rastreados por Git y omite documentos Markdown
para concentrarse en código, configuración, datos, activos y soporte operativo.

## 1. Inventario por extensión

| Extensión o tipo | Cantidad | Observación |
|---|---:|---|
| `.py` | 160 | Todos los módulos revisados tienen docstring inicial. |
| `.png` | 22 | Activos binarios; no admiten encabezado textual. |
| `.js` | 18 | Requieren encabezado uniforme de propósito y alcance. |
| `.html` | 16 | Plantillas Jinja y parciales con comentarios de sección. |
| `.yml` | 8 | Workflows, Dependabot e Issue Forms con encabezados funcionales. |
| `.css` | 7 | Requieren encabezado uniforme de propósito y alcance. |
| `.json` | 5 | Datos normativos y ledger; JSON no permite comentarios. |
| sin extensión | 5 | VERSION, LICENSE, CODEOWNERS, firmas y marcadores especiales. |
| `.editorconfig` | 1 | Política editorial transversal. |
| `.gitignore` | 1 | Exclusiones del repositorio por secciones. |
| `.gitattributes` | 1 | Normalización de finales de línea y binarios. |
| `.txt` | 1 | Dependencias Python. |
| `.ps1` | 1 | Configuración local del hook versionado. |
| `.githook` | 1 | Hook local versionado. |
| `.ico` | 1 | Activo binario de icono. |

## 2. Hallazgos

- JavaScript ya contenía comentarios útiles, pero los encabezados mezclaban
  estilos decorativos, JSDoc y bloques de propósito.
- CSS también tenía intención técnica documentada, aunque con formatos de
  encabezado distintos entre hojas.
- YAML, PowerShell, hooks y archivos especiales ya estaban alineados con
  encabezados funcionales permanentes.
- JSON, PNG e ICO requieren documentación externa porque sus formatos no
  admiten encabezados textuales útiles.
- Python mantiene docstring inicial en los módulos revisados; las pruebas pueden
  mencionar revisiones cuando verifican contratos históricos.

## 3. Decisión de mantenimiento

La aplicación de uniformidad se limita inicialmente a `app/static/js/*.js` y
`app/static/css/*.css`, porque son archivos operativos de presentación con
inconsistencias visibles de encabezado. Las demás extensiones quedan protegidas
por política, plantillas y regresión sin reescritura innecesaria.
