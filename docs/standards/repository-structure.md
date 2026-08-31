# Estructura del repositorio

## Propósito

Define la organización oficial del repositorio y la ubicación permitida para
cada tipo de componente.

## Principios generales

- Cada archivo debe tener una responsabilidad y una ubicación definidas.
- No se crean carpetas temporales versionadas dentro del repositorio principal.
- La raíz se reserva para archivos transversales del proyecto.
- Código, documentación, datos, pruebas y evidencias deben permanecer separados.
- Los artefactos locales no versionados se mantienen fuera del árbol canónico.
- Git conserva el historial de versiones anteriores.

## Estructura principal

La estructura principal canónica debe corresponder a directorios que tengan
contenido rastreado por Git y una responsabilidad permanente:

```text
.github/
├── ISSUE_TEMPLATE/
└── workflows/

.githooks/

app/
├── cli/
├── core/
├── engines/
├── models/
├── services/
├── static/
│   ├── css/
│   ├── img/
│   │   └── brand/
│   └── js/
└── templates/
    └── partials/

assets/
├── brand/
│   ├── icons/
│   ├── logos/
│   └── source/
└── social/

data/

docs/
├── architecture/
├── archive/
├── audits/
├── decisions/
├── governance/
├── operations/
├── product/
├── regulatory/
├── security/
├── standards/
└── templates/

regulations/
scripts/

tests/
└── validation_cases/
```

Responsabilidades principales:

- `.github/`: integración y gobierno específicos de GitHub;
- `.githooks/`: hooks Git versionados;
- `app/`: runtime de la aplicación;
- `assets/`: activos fuente y derivados de identidad visual que no pertenecen
  directamente al árbol estático del runtime;
- `data/`: datos estructurados versionables de gobierno y publicación;
- `docs/`: documentación viva, auditorías, archivo histórico, decisiones,
  estándares y plantillas;
- `regulations/`: parámetros normativos versionados;
- `scripts/`: automatización, auditoría y gates locales;
- `tests/`: regresiones y casos versionables de validación.

La estructura se contrasta contra `git ls-files`. La existencia física de un
directorio ignorado no lo convierte en parte de la arquitectura canónica.

Las carpetas de herramientas o ecosistemas conservan su nombre convencional
cuando cambiarlo rompería integración o semántica externa.

## Estructura documental

La carpeta `docs/` se organiza por responsabilidad. Las áreas estructurales
canónicas vigentes son:

```text
docs/
├── architecture/
├── archive/
├── audits/
├── decisions/
├── governance/
├── operations/
├── product/
├── regulatory/
├── security/
├── standards/
└── templates/
```

Estas áreas representan responsabilidades estables del repositorio. La
auditoría estructural final debe contrastarlas contra el árbol Git real y
corregir cualquier divergencia sin convertir carpetas temporales o locales
en estructura canónica.

### `architecture/`

Contiene arquitectura del sistema, modelos de datos, motores y contratos
técnicos internos.

### `decisions/`

Contiene el registro vivo de decisiones técnicas y ADR.

### `governance/`

Contiene planificación, roadmap, ledgers y contratos de gobierno del proyecto.

### `operations/`

Contiene guías de desarrollo, validación, observabilidad, releases,
dependencias y operación técnica.

### `product/`

Contiene especificaciones funcionales, transparencia, limitaciones,
identidad visual y comportamiento del producto.

### `regulatory/`

Contiene marco normativo, fuentes oficiales y documentación específica de
los sistemas previsionales.

### `security/`

Contiene privacidad, seguridad, threat model, procedimientos y evaluaciones
de riesgo.

### `standards/`

Contiene políticas, estándares y reglas canónicas vigentes del repositorio.

### `audits/`

Contiene auditorías y evidencia versionable. La evidencia bruta que contradiga
invariantes del repositorio o que solo tenga utilidad local no se versiona.

### `archive/`

Contiene documentación histórica que conserva valor de auditoría o contexto y
que ya no representa por sí sola el estado vigente.

### `templates/`

Contiene plantillas oficiales para tipos de archivo o documentación.

## Raíz

La política detallada de la raíz y de los artefactos locales se encuentra en
`root-and-local-artifacts.md`.

No se permiten en la raíz inventarios de auditoría, volcados temporales,
paquetes de entrega, copias de trabajo ni evidencia generada para una revisión.

## Historial

Cuando un documento o archivo sea sustituido, Git conserva las versiones
anteriores. La permanencia adicional bajo `docs/archive/` se justifica solo
cuando el artefacto histórico sigue siendo parte útil de la trazabilidad.
