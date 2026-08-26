# NOR.1 R8 — auditoría de identificadores de bloques

**Clasificación:** Auditoría de repositorio / estándar
**Base auditada:** `7e81034ae05f5e588d07a0caf97e6fc79877dfb1`
**Versión:** `0.1.11.01-beta` — G111/E01
**Estado:** candidato; G112 no consumido

## Evidencia

El inventario automático se ejecutó sobre `main` limpio y registró:

- 459 archivos rastreados;
- `accepted_count=111`;
- G112 como siguiente Global;
- bloques canónicos desde G001 hasta DOC.2/G111;
- identificadores UX históricos absorbidos bajo la reconstrucción legacy;
- bloques futuros reservados por el plan maestro;
- falsos positivos como revisiones `R...`, nombres de licencia y otros tokens
  técnicos.

## Hallazgos

1. `R1.1`, `R1.2`, `R4.2`, `R8.2`, `R9.1`, etc. son revisiones, no familias.
2. `LEGACY`, `INTEGRIDAD` y `POST-GOV` son etiquetas históricas del ledger.
3. `UX.2.1`, `UX.3`, `UX.4.1`–`UX.4.6d` fueron subfases reales y no pueden
   reutilizarse.
4. `DOC.1 R2` demuestra que un bloque puede recibir una revisión posterior si
   conserva el mismo alcance.
5. NOR.1 define estándares; NOR.2 normaliza contra ellos.
6. El estándar anterior de nombres no cubría la taxonomía de bloques.
7. La búsqueda exacta previa a la implementación obtuvo `NOR.1 R8 = 0` tanto en
   el árbol como en mensajes Git.
8. `PERSIST.1`, `REP.1`, `A11Y.2`, `REV.1`, `QA.1` y `REL.1` ya están
   reservados por el plan maestro.

## Decisión

Clasificar el trabajo como **NOR.1 R8 — gobierno de identificadores de bloques
de trabajo**.

G112/E07 queda reservado para el candidato sin consumirse. Si NOR.1 R8 es
aceptado y promocionado, `PERSIST.1` continuará con el siguiente Global
disponible.

## Artefactos

- `docs/standards/work-block-identifiers.md`;
- `data/work-block-registry.json`;
- `scripts/audit_block_identifiers.py`;
- `tests/test_nor1_r8_work_block_identifiers.py`.

No se modifican tags históricos ni `docs/archive/` para reescribir terminología.

## Resultado de aceptación

NOR.1 R8 fue integrado mediante PR #89 y su ordinal revision-aware fue corregido antes de la aceptación mediante PR #90. El gate post-merge cerró con 1081 pruebas en `OK`, Markdown 145/145 y CI remota en `success`. La promoción formal materializa G112/E07 (`0.1.12.07-beta`).

La auditoría Markdown posterior se clasifica bajo la política resultante como **DOC.1 R3**, no como un bloque nuevo: amplía el alcance registrado de auditoría e integridad Markdown. Su candidato es G113/E03 (`0.1.13.03-beta`) y PERSIST.1 permanece como siguiente bloque funcional.
