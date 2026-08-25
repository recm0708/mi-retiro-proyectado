# DOC.1 R1 — Línea base documental post-MANT.1

## Propósito

Esta línea base fija el estado documental vigente después del cierre operativo de MANT.1 R7.

DOC.1 R1 existe para revisar todos los archivos Markdown del repositorio, distinguir documentación vigente de evidencia histórica y actualizar únicamente los documentos que quedaron desalineados después de MANT.1.

## Estado canónico

- Versión canónica de la aplicación: `0.0.26-beta`.
- Fuente única de versión: `VERSION`.
- Último cierre integrado en `main`: `MANT.1 R7 — cierre operativo post-auditoría`.
- PR de cierre MANT.1 R7: `#55`.
- Commit squash post-MANT.1 R7 en `main`: `57078f2`.
- Estado de MANT.1: cerrado operativamente después de R5H, R6 y R7.
- Estado de VER.2: reconciliación revision-aware pendiente; `0.0.71.01-beta` se conserva como candidato, no como versión publicada.
- Tag formal vigente: `v0.0.26-beta`.
- Próximo trabajo documental: DOC.1 R1, auditoría integral de Markdown post-MANT.1.

## Validaciones observadas

- Suite completa local post-R7: `939 passed`.
- Gate `pre-commit` observado durante R7: `928 tests OK`.
- Archivos protegidos sin cambios durante R7:
  - `VERSION`
  - `app/core/version.py`
  - `app/core/config.py`
  - `regulations/`
  - `data/`
  - `_entregas/`

## Criterio de actualización Markdown

- Se revisan todos los archivos `.md` del repositorio.
- Se actualiza documentación vigente cuando expresa estados ya superados o ambiguos.
- Se preserva documentación histórica archivada bajo `docs/archive/`.
- Se preservan auditorías, ADR y documentos de cierre como evidencia del momento en que fueron escritos.
- No se reescriben fórmulas previsionales, parámetros normativos, versión canónica ni entregables.
