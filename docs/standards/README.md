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

- `repository-structure.md` — estructura y responsabilidades.
- `naming-conventions.md` — reglas determinísticas de nombres.
- `file-standards.md` — requisitos mínimos por tipo de archivo.
- `documentation-standards.md` — documentación viva, histórica y referencias.
- `artifact-lifecycle.md` — creación, sustitución, archivo y eliminación.
- `root-and-local-artifacts.md` — raíz, evidencias y artefactos locales.

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

NOR.1 define las reglas.

NOR.2 auditará y normalizará el repositorio existente contra estas reglas antes
de reanudar la creación estructural profunda de SEC.2.
