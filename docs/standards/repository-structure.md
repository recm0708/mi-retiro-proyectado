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

La estructura versionada esperada utiliza, cuando correspondan:

```text
.github/
.githooks/
app/
data/
docs/
regulations/
scripts/
tests/
```

Las carpetas de herramientas o ecosistemas conservan su nombre convencional
cuando el cambio rompería integración o semántica externa.

## Estructura documental

La carpeta `docs/` se organiza por responsabilidad. Las áreas estructurales
canónicas son:

```text
docs/
├── archive/
├── audits/
├── standards/
└── templates/
```

Pueden existir áreas adicionales de documentación viva cuando NOR.2 demuestre
que representan una responsabilidad estable y no una clasificación artificial.

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
