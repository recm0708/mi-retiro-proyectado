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
| `release_publication.py` | Valida el manifiesto de publicación, genera notas canónicas desde evidencia versionada y comprueba la idempotencia de un GitHub Release existente. | Solo escribe el archivo de notas indicado explícitamente por `--render-notes` |

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

REL.GOV.1 R2 añade un manifiesto versionado de publicación. Durante preparación y diagnóstico puede validarse o renderizarse así:

```powershell
python scripts/release_publication.py --check-manifest
python scripts/release_publication.py --render-notes .\release-notes.md --tag "v$((Get-Content .\VERSION).Trim())"
```

La segunda operación requiere que el tag anotado exista localmente, porque obtiene de Git los SHA reales del commit publicado y del objeto de tag. En GitHub Actions esos datos se resuelven después de verificar la firma.

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

## `audit_block_identifiers.py`

Valida `data/work-block-registry.json` y detecta identificadores de familias conocidas que no estén registrados por NOR.1 R8. No modifica archivos.
