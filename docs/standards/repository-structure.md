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
├── portals/
│   ├── asegurado/
│   └── developer/
├── services/
├── static/
│   ├── asegurado/
│   │   ├── css/
│   │   └── js/
│   ├── developer/
│   │   ├── css/
│   │   └── js/
│   └── shared/
│       ├── css/
│       ├── img/
│       │   └── brand/
│       └── js/
└── templates/
    ├── asegurado/
    │   └── partials/
    ├── developer/
    └── shared/
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
├── domain/
├── governance/
├── portals/
│   ├── asegurado/
│   └── developer/
├── regression/
├── repository/
├── security/
├── shared/
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

## Ownership de assets runtime

NOR.3 R5 materializa `app/static/shared/`, `app/static/asegurado/` y `app/static/developer/`. `style.css` queda en Asegurado después de retirar contratos transversales redundantes; Developer no depende de esa hoja. La marca runtime única vive en `shared/img/brand/`.

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

<!-- NOR3-R6-TEST-TAXONOMY -->

## NOR.3 R6 — Taxonomía de pruebas por ownership

La suite deja de ser plana y se distribuye en `domain`,
`portals/asegurado`, `portals/developer`, `shared`, `repository`,
`governance`, `security` y `regression`. `tests/validation_cases/`
permanece como soporte de casos de validación.

`tests/shared/` solo contiene contratos realmente multiportal. Las
pruebas de dominio, gobierno, seguridad o repositorio conservan un
propietario explícito aunque sean consumidas por más de una superficie.

<!-- NOR3-R7-DATA-SCRIPTS -->
## NOR.3 R7 — Ownership de data y scripts

`data/` deja de ser una colección plana:

```text
data/
├── audits/
└── governance/
```

- `data/governance/` contiene ledger, manifiesto de publicación, policy
  estructural y registro de bloques de trabajo.
- `data/audits/` contiene evidencia machine-readable derivada de auditorías
  históricas o de trazabilidad.
- `data/developer/` permanece local/ignorado; R7 no lo versiona ni lo elimina.
- `data/.gitkeep` deja de ser necesario porque `data/` contiene estructura real.

`scripts/` fue auditado en R7 y ya se encontraba semánticamente plano: todos
sus entry points versionados viven directamente bajo `scripts/`. R7 no agrega
anidamiento artificial ni mueve scripts sin una frontera funcional que lo
justifique.

<!-- NOR3-R8-CLOSURE -->
## NOR.3 R8 — cierre estructural

R8 congela como contrato verificable la estructura materializada por NOR.3
R1–R8:

- `app/portals/asegurado/` y `app/portals/developer/` separan ownership de
  backend;
- `app/templates/` y `app/static/` separan Asegurado, Developer y contratos
  realmente compartidos;
- `tests/` usa taxonomía por ownership y no admite módulos `test_*.py` planos
  en su raíz;
- `data/governance/` contiene estado/política versionados;
- `data/audits/` contiene evidencia machine-readable;
- `data/developer/` permanece local e ignorado;
- `scripts/` conserva entry points versionados planos; `node_modules/` es
  tooling local/ignorado;
- el candidato de cierre es G122/E01 (`0.1.22.01-beta`), todavía
  reservado/no aceptado hasta promoción, integración y revalidación.

La auditoría transversal completa de contenido documental y código no se
declara ejecutada por R8. Se realizará después de NOR.3 como fase propia,
posterior a la reconciliación de Issues y al saneamiento de
Dependabot/seguridad.
