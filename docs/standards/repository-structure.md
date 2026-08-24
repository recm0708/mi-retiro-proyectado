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

Cada carpeta representa una responsabilidad específica.

## Carpeta app

Contiene el código fuente de la aplicación.

Ejemplo:

```text
app/
  core/
  engines/
  models/
  services/
  static/
  templates/
```

## Carpeta docs

Contiene documentación vigente del proyecto.

La documentación histórica o sustituida no debe mantenerse como documentación
actual si ya existe un documento oficial que la reemplaza.

## Carpeta tests

Contiene pruebas automatizadas y validaciones del proyecto.

## Historial

Cuando un documento sea reemplazado, Git conserva las versiones anteriores
mediante commits, ramas y Pull Requests.
