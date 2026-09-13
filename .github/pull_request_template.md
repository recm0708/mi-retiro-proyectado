## Resumen

Describe qué cambia y por qué.

## Issues y alcance

- Umbrella:
- Issues implementados:
- Issues parcialmente cubiertos:
- Issues derivados / remanentes:
- Fase o par de revisiones:
- Alcance incluido:
- Fuera de alcance:
- ¿Este PR satisface completamente el criterio de cierre del Issue principal?: Sí / No

> Usa `Closes #N` o `Fixes #N` solo cuando este PR satisface todo el criterio
> de cierre del Issue. No cierres automáticamente umbrellas ni Issues parciales.

## Validación

- [ ] Ejecuté `python scripts/quality_gate.py --full`.
- [ ] Revisé el diff staged antes del commit.
- [ ] Ejecuté validaciones específicas adicionales cuando el cambio lo requirió.
- [ ] Registré la validación manual pendiente o realizada.
- [ ] Si modifiqué tooling Node, revisé `npm audit --prefix scripts --audit-level=high`.

## Documentación

- [ ] Revisé y actualicé la documentación dependiente.
- [ ] `README.md`, `CHANGELOG.md`, `roadmap.md` y `validation.md` están coherentes cuando corresponde.
- [ ] No convertí un estado histórico transitorio en una regla permanente.
- [ ] Los remanentes están transferidos a un Issue existente o a un derivado con owner claro.

## Seguridad y privacidad

- [ ] No añadí datos personales reales, PDFs personales, secretos ni logs sensibles.
- [ ] Revisé seguridad/privacidad/threat model si cambia datos, logging, terceros, red o persistencia.
- [ ] Las vulnerabilidades sensibles se trataron conforme a `SECURITY.md`.

## Gobierno y versión

- [ ] `VERSION` se mantiene o cambia de forma deliberada conforme a `VERSIONING.md`.
- [ ] No preasigné Globales futuros sin aceptación material.
- [ ] El commit está firmado y puede verificarse.
- [ ] La rama está actualizada respecto de `main` antes del merge.
- [ ] La relación Issue ↔ rama ↔ PR ↔ documentación queda trazable.

## Riesgos y compatibilidad

Indica riesgos, wrappers de compatibilidad, rollback o dependencias relevantes.

## Notas para revisión

Indica limitaciones, validaciones manuales pendientes o decisiones que deban comprobarse.
