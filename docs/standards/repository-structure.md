# Estructura del repositorio

## Propósito

Define la organización oficial del repositorio y la ubicación permitida para
cada tipo de componente.

## Principios generales

- Cada archivo debe tener una ubicación definida.
- No se crean carpetas temporales dentro del repositorio principal.
- La raíz se reserva para archivos generales del proyecto.
- Código, documentación, datos, pruebas y evidencias deben permanecer separados.
- Git mantiene el historial de versiones anteriores.

## Estructura principal

La estructura esperada es:

```text
app/
data/
docs/
regulations/
scripts/
tests/
.github/
```

## Estructura documental

La carpeta `docs/` contiene documentación del proyecto y se organiza por
responsabilidad:

```text
docs/
├── standards/
├── audits/
└── archive/
```

### standards

Contiene políticas, estándares y reglas vigentes del repositorio.

### audits

Contiene evidencias y análisis de auditorías realizadas sobre el proyecto.

### archive

Contiene documentación histórica sustituida que ya no representa el estado
vigente.

## Historial

Cuando un documento sea reemplazado, Git conserva las versiones anteriores
mediante commits, ramas y Pull Requests.
