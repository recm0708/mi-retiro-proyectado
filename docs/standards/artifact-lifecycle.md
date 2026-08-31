# Ciclo de vida de archivos y componentes

## Propósito

Define cuándo crear, modificar, mover, archivar o eliminar archivos y
componentes.

## Creación

Antes de crear un archivo se debe verificar:

- necesidad real;
- ausencia de un archivo existente que cumpla la misma función;
- ubicación correcta;
- nombre correcto;
- clasificación como versionado o local;
- relación con documentación y pruebas existentes.

## Modificación

Se modifica el archivo canónico cuando la responsabilidad permanece siendo la
misma.

No se crea una copia con sufijos informales para evitar editar el archivo
vigente.

## Movimiento o renombrado

Antes de mover o renombrar se identifican:

- imports;
- enlaces;
- configuración;
- pruebas;
- rutas públicas;
- referencias documentales.

Después del cambio se busca la ruta anterior y se ejecutan las validaciones
correspondientes.

## Sustitución

Un archivo nuevo puede sustituir uno anterior cuando incorpora la información
válida y mejora la estructura del proyecto.

El archivo sustituido sale del árbol actual salvo que exista una justificación
documentada para conservarlo en `docs/archive/`.

## Eliminación

Eliminar un archivo del repositorio actual no elimina su historial.

Git permite consultar versiones anteriores mediante commits, pull requests,
ramas y etiquetas.

No se conserva basura estructural únicamente por temor a perder historia.

## Artefactos locales

Los archivos de trabajo, paquetes, volcados, logs y evidencias no versionables
se mantienen fuera del árbol canónico o en directorios locales ignorados según
`root-and-local-artifacts.md`.

## Aplicación

NOR.1 define estas reglas.

NOR.2 las aplicó durante la auditoría y normalización del repositorio existente.

Las reconciliaciones posteriores deben reutilizarlas para decidir de forma
explícita si un artefacto se mantiene, modifica, mueve, archiva o elimina.
