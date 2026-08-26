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
| `audit_markdown.py` | Audita la documentación Markdown versionada: formato, metadata, versión vigente, idioma, enlaces locales y stubs de compatibilidad. | No |
| `validate_precommit.py` | Ejecuta el gate local antes de crear commits: estado Git, whitespace, auditoría Markdown, dependencias, compilación Python, sintaxis JavaScript y pruebas. | No |
| `release_contract.py` | Valida el contrato revision-aware de VERSION/ledger/tag/título/notas para tags y GitHub Releases futuros. | No |

## Uso previsto

El script de configuración se ejecuta una vez por clon local:

```powershell
.\scripts\configure_git_hooks.ps1
```

Después de esa activación, Git ejecuta `.githooks/pre-commit` antes de cada
commit. El hook delega la validación en `scripts/validate_precommit.py`.

El auditor documental también puede ejecutarse directamente:

```powershell
python scripts/audit_markdown.py
```

El contrato de publicación puede inspeccionarse antes de crear un tag o Release:

```powershell
python scripts/release_contract.py --json
python scripts/release_contract.py --print-title
python scripts/release_contract.py --check-tag "v$((Get-Content .\VERSION).Trim())"
```

Para validar un archivo de notas de Release:

```powershell
python scripts/release_contract.py --check-notes .\release-notes.md
```

El mismo auditor forma parte del gate local, por lo que una infracción Markdown
bloqueante impide crear el commit.

## Contrato de mantenimiento

Los scripts de esta carpeta deben cumplir estas reglas:

- usar rutas relativas a la raíz del repositorio;
- evitar rutas absolutas del equipo local;
- no modificar archivos fuente durante una validación;
- cancelar con código distinto de cero cuando una comprobación falla;
- explicar en comentarios el propósito, el alcance y los límites de cada script;
- mantenerse sincronizados con `docs/operations/validation.md` y `docs/standards/code-and-comments.md`.

## Relación con CI

El gate local reduce errores antes del commit, pero no reemplaza GitHub Actions.
La integración de un Pull Request sigue dependiendo de los checks remotos
obligatorios del repositorio.
