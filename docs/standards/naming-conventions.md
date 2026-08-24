# Convenciones de nombres

## Propósito

Establece reglas determinísticas para nombrar carpetas, archivos, documentos,
pruebas y evidencias nuevas.

NOR.2 utilizará estas reglas para identificar nombres existentes que requieren
normalización.

## Reglas transversales

Salvo nombres impuestos por un ecosistema o estándar externo:

- usar caracteres ASCII;
- usar minúsculas;
- no usar espacios;
- no usar tildes ni `ñ` en rutas técnicas;
- no agregar versiones informales como `final`, `nuevo`, `v2` o `copia`;
- usar un solo separador según el tipo definido en este documento;
- utilizar nombres descriptivos de la responsabilidad permanente.

## Carpetas

### Paquetes importables y carpetas ligadas a Python

Usan inglés técnico y `snake_case`.

Ejemplos:

```text
validation_cases/
calculation_engine/
```

### Carpetas documentales, de recursos o no importables

Usan inglés técnico y `kebab-case` cuando necesitan varias palabras.

Ejemplos:

```text
regulatory-privacy/
file-structure/
```

Las carpetas de una sola palabra permanecen en minúsculas:

```text
services/
models/
templates/
audits/
```

### Carpetas convencionales externas

No se renombran cuando el nombre pertenece al ecosistema:

```text
.github/
.githooks/
.venv/
.pytest_cache/
.git/
```

## Código Python

Los módulos `.py` usan inglés técnico y `snake_case`.

Ejemplos:

```text
salary_projection.py
reference_date.py
regulatory_sources.py
```

Los archivos de prueba usan:

```text
test_<contrato_o_componente>.py
```

Los acrónimos oficiales de dominio se escriben en minúsculas dentro del nombre
del archivo cuando formen parte de una ruta técnica.

## JavaScript y plantillas HTML/Jinja

Los archivos propiedad de la aplicación usan `snake_case` cuando el nombre tiene
más de una palabra.

Ejemplos:

```text
salary_history.js
results_orchestration.js
current_year_detail.html
```

Los nombres convencionales de entrada, como `index.html` o `base.html`, se
conservan.

## CSS

Las hojas de estilo propiedad de la aplicación usan `kebab-case` cuando el
nombre tiene más de una palabra.

Ejemplos:

```text
design-system.css
high-contrast.css
```

## JSON, YAML y archivos de configuración

Se respeta primero la convención exigida por la herramienta o ecosistema.

Cuando el proyecto controla completamente el nombre y no existe una convención
externa, se usa inglés técnico, minúsculas y `kebab-case`.

Los nombres oficiales contenidos dentro de datos normativos no se traducen por
esta regla.

## Documentación Markdown

Los documentos internos nuevos bajo carpetas técnicas de `docs/` usan inglés
técnico y `kebab-case`.

Ejemplos:

```text
repository-structure.md
naming-conventions.md
documentation-dependency-audit-nor1-r5.md
```

El contenido permanece en español.

Los nombres convencionales del ecosistema GitHub y de la raíz se conservan,
entre ellos:

```text
README.md
CHANGELOG.md
CONTRIBUTING.md
CODE_OF_CONDUCT.md
GOVERNANCE.md
SECURITY.md
SUPPORT.md
RELEASES.md
VERSIONING.md
THIRD_PARTY_NOTICES.md
```

## Auditorías y evidencias

Una evidencia versionada nueva usa esta estructura general:

```text
<subject>-<artifact>-<phase>-r<revision>.<ext>
```

Ejemplos:

```text
naming-audit-nor1-r4.md
documentation-inventory-nor1-r5.txt
```

Si una fase no utiliza una revisión separada, se documenta la excepción en la
auditoría correspondiente y no se inventa un sufijo.

## Idioma y excepciones de dominio

Los nombres técnicos genéricos se expresan en inglés.

Se conservan sin traducción:

- nombres oficiales de tecnologías;
- nombres de estándares;
- acrónimos oficiales;
- nombres propios del producto;
- identificadores regulatorios cuya traducción alteraría la trazabilidad;
- contratos externos que dependan del nombre exacto.

Una palabra española de uso genérico no se convierte en excepción únicamente
porque ya exista en el repositorio. NOR.2 decidirá su migración considerando
imports, rutas públicas, enlaces, pruebas y compatibilidad.

## Renombrados

Un renombrado debe:

1. localizar referencias e imports;
2. evaluar contratos públicos o externos;
3. ejecutar el movimiento con Git;
4. actualizar código, pruebas, configuración y documentación;
5. buscar la ruta anterior;
6. ejecutar pruebas focales y suite completa;
7. cerrar la migración sin aliases innecesarios salvo compatibilidad justificada.
