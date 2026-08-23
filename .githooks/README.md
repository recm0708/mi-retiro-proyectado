# Hooks Git versionados

**Estado:** vigente
**Bloque:** MANT.1 R2 — documentación de scripts y hooks
**Clasificación:** técnica / mantenimiento local

**Origen:** MANT.1 R1 definió la auditoría inicial; MANT.1 R2 materializa esta documentación.

Esta carpeta contiene hooks de Git versionados por el proyecto. Su propósito es
mantener controles locales reproducibles entre clones sin depender de archivos
manuales dentro de `.git/hooks/`.

## Inventario

| Hook | Momento de ejecución | Propósito |
|---|---|---|
| `pre-commit` | Antes de crear un commit | Delegar en `scripts/validar_precommit.py` el gate local del repositorio. |

## Activación

Los hooks versionados se activan por clon mediante:

```powershell
.\scripts\configurar_hooks_git.ps1
```

Ese comando configura:

```text
core.hooksPath=.githooks
```

## Alcance

El hook `pre-commit` no implementa reglas de negocio y no modifica archivos. Su
responsabilidad es localizar Python y ejecutar el validador versionado del
proyecto.

## Límites

- No sustituye la CI remota.
- No evita que un usuario desactive hooks manualmente.
- No debe contener lógica previsional ni validaciones duplicadas de la aplicación.
- No debe depender de rutas absolutas del equipo local.
