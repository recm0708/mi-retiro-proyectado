# Scripts del repositorio

**Estado:** vigente
**Clasificación:** técnica / mantenimiento local

Esta carpeta contiene automatizaciones versionadas para operar el repositorio de
forma reproducible. Los scripts aquí ubicados no implementan reglas previsionales,
no calculan pensiones y no modifican normativa.

## Inventario

| Archivo | Propósito | Modifica archivos del proyecto |
|---|---|---|
| `configure_git_hooks.ps1` | Configura `core.hooksPath=.githooks` para que Git use los hooks versionados del proyecto. | No |
| `validate_precommit.py` | Ejecuta el gate local antes de crear commits: estado Git, whitespace, dependencias, compilación Python, sintaxis JavaScript y pruebas. | No |

## Uso previsto

El script de configuración se ejecuta una vez por clon local:

```powershell
.\scripts\configure_git_hooks.ps1
```

Después de esa activación, Git ejecuta `.githooks/pre-commit` antes de cada
commit. El hook delega la validación en `scripts/validate_precommit.py`.

## Contrato de mantenimiento

Los scripts de esta carpeta deben cumplir estas reglas:

- usar rutas relativas a la raíz del repositorio;
- evitar rutas absolutas del equipo local;
- no modificar archivos fuente durante una validación;
- cancelar con código distinto de cero cuando una comprobación falla;
- explicar en comentarios el propósito, el alcance y los límites de cada script;
- mantenerse sincronizados con `docs/VALIDACION.md` y `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md`.

## Relación con CI

El gate local reduce errores antes del commit, pero no reemplaza GitHub Actions.
La integración de un Pull Request sigue dependiendo de los checks remotos
obligatorios del repositorio.
