# Gobierno de Issues, Pull Requests y continuidad

**Estado:** Vigente / NOR.3 R1-R2

**Issues de referencia:** #132, #135, #136, #137, #138, #139, #140 y #158.

## Principio de ownership

Todo trabajo material tiene un Issue propietario canónico. Se actualiza el
mismo Issue cuando el objetivo permanece estable. Se crea un derivado cuando
existe owner, fase, dependencia o criterio de cierre independiente.

## Estados operativos

Los estados conceptuales son `proposed`, `approved_not_started`, `blocked`,
`in_progress`, `validation`, `completed`, `superseded`, `deferred` y
`post_1_0`. El estado open/closed de GitHub no sustituye esta semántica.

## Convención de revisiones por pares

Dentro de un bloque material ya autorizado se trabaja por defecto en pares:

- `R1 + R2`;
- `R3 + R4`;
- `R5 + R6`;
- `R7 + R8`;
- y así sucesivamente cuando existan más revisiones.

El emparejamiento es operativo. Cada revisión conserva objetivo, checklist,
pruebas y evidencia propios. Un par puede compartir rama, working tree,
validación y PR cuando siga siendo auditable.

No se requiere nueva autorización únicamente para cruzar de una revisión a la
siguiente dentro del mismo bloque autorizado. El par se separa cuando exista
dependencia dura, validación manual pendiente, riesgo material, necesidad de
rollback independiente o pérdida de auditabilidad.

## Labels

La taxonomía canónica usa `planning`, `governance`, `architecture`,
`post-1.0`, `blocked`, `ui`, `accessibility`, `security`, `privacy`,
`documentation`, `tests`, `backend`, `regulations`, `dependencies`,
`github-actions` y `maintenance`.

No se crean sinónimos `ux`, `technical-debt`, `qa` o `testing` mientras `ui`,
`maintenance` y `tests` cubran esas funciones.

## Milestones

Durante NOR.3 se adopta la Opción C: **no usar Milestones**.

El repositorio no tiene Milestones y la agrupación ya está cubierta por Issues
umbrella, relaciones, labels, roadmap, registry, ledger y el versionado
Global/Edition.

## Issue Forms

Se conservan reporte de error, solicitud de mejora y consulta / soporte.

Se añaden:

- Plan / fase / trabajo diferido;
- Arquitectura / estructura;
- Hallazgo / deuda técnica;
- Revisión UX / superficie.

No se crea un Issue Form ordinario de Handoff. Los checkpoints se registran
preferentemente como comentario en el Issue activo.

## Checkpoints

Un checkpoint material registra fase/revisión, Issue activo, rama, HEAD/base,
PR, working tree, último paso, cambios aplicados, tests/checks, validación
manual, pendientes, decisiones abiertas, datos locales a preservar, comandos
que no deben repetirse, Issues derivados y siguiente paso exacto.

Nunca se incluyen secretos, contraseñas, tokens ni datos personales sensibles.

## Pull Requests

Todo PR material debe declarar umbrella, Issues implementados/parciales,
derivados, fase o par de revisiones, alcance incluido/excluido, criterio de
cierre, tests/checks, validación manual, documentación y riesgos.

`Closes #N` o `Fixes #N` solo se usan cuando el PR satisface todo el criterio
de cierre del Issue indicado.

## Fuente de verdad

- Issues: contrato vivo y continuidad.
- Comentarios: progreso y evidencia cronológica.
- Git/PR: implementación material.
- `VERSION` + Global/Edition: materialización aceptada.
- Roadmap/registry/ledger: planificación y trazabilidad de programa.
