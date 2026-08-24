# Clasificación documental NOR.1 R3

## Información general

Proyecto: Mi Retiro Proyectado

Fase:
NOR.1 R3 — Clasificación documental inicial

## Objetivo

Clasificar la documentación existente del repositorio para aplicar las
políticas definidas en NOR.1 sin perder trazabilidad histórica.

Esta clasificación no realiza movimientos ni eliminaciones. Define las acciones
futuras que deberán ejecutarse durante la normalización documental.

## Categorías definidas

### Documentación vigente

Documentos que representan el estado actual del proyecto y deben permanecer
en la estructura principal de docs/.

Acción:
Mantener y actualizar referencias cuando sea necesario.

### Auditorías

Documentos que registran revisiones, validaciones, análisis o controles
realizados durante el desarrollo.

Acción:
Migrar progresivamente hacia docs/audits/ según su naturaleza.

Clasificación inicial:

- repository: auditorías de estructura, nombres y repositorio.
- documentation: auditorías documentales.
- functional: auditorías funcionales.
- ux: auditorías de experiencia de usuario.

### Histórico

Documentación correspondiente a versiones anteriores, fases cerradas o estados
previos del proyecto.

Acción:
Mantener en docs/archive/ conservando trazabilidad mediante Git.

### Plantillas

Archivos utilizados como base para creación de nuevos componentes.

Acción:
Mantener en docs/templates/.

## Hallazgos iniciales

Se identifican documentos con sufijos históricos:

- PRE_GOV1_3
- POST
- R1, R2, R5, R6, R7
- ADD

Estos identificadores no se eliminan automáticamente porque forman parte de la
historia del proyecto.

## Reglas de migración

Antes de mover o renombrar cualquier documento:

1. Revisar referencias internas.
2. Actualizar índices y enlaces Markdown.
3. Validar rutas en documentación relacionada.
4. Usar movimientos compatibles con Git.
5. Ejecutar pruebas y auditorías posteriores.

## Estado

Documento creado como guía de clasificación NOR.1 R3.

Pendiente:
Aplicación gradual de movimientos y renombrados durante NOR.2.
