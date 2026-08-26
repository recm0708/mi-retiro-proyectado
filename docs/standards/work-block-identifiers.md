# Identificadores de bloques de trabajo

**Proyecto:** Mi Retiro Proyectado
**Estándar:** NOR.1 R8
**Base auditada:** `7e81034ae05f5e588d07a0caf97e6fc79877dfb1` — G111/E01
**Registro canónico:** `data/work-block-registry.json`

## Propósito

Este estándar define cómo interpretar, reservar y crear identificadores de
programas, bloques, subfases y checkpoints. Evita reutilizar una sigla con otro
significado, inventar numeraciones y confundir revisiones internas con bloques.

## Conceptos

- **Familia:** prefijo semántico, como `UX`, `DOC`, `NOR` o `SEC`.
- **Bloque:** identificador registrado, como `DOC.2`, `DEV.2` o `UX.4.6h`.
- **Namespace/programa:** padre histórico, como `GOV.1`, `UX.4` y `UX.4.6`.
- **Revisión:** sufijo separado por espacio, por ejemplo `NOR.1 R8`; `R8` no es
  un bloque independiente.
- **Global:** contador `GNNN`; cuenta estados materiales aceptados, no nombres.
- **Edición:** `E##`; tampoco forma parte del identificador del bloque.

Los segmentos separados por puntos no tienen un significado universal. Su
lectura depende de la familia y del registro canónico.

## Familias canónicas

`GOV`, `UX`, `PLAN`, `DEV`, `MANT`, `DOC`, `VER`, `NOR`, `SEC`, `AUD`,
`REL`, `PERSIST`, `REP`, `A11Y`, `REV` y `QA`.

`AUD.SEC2` y `REL.GOV.1` son compuestos históricos explícitamente registrados.
No autorizan a crear compuestos nuevos por analogía.

## Etiquetas históricas no reutilizables

`LEGACY`, `INTEGRIDAD` y `POST-GOV` existen en el ledger por razones de
reconciliación histórica. No son familias disponibles para trabajo futuro.

## Reglas de asignación

1. Consultar primero `data/work-block-registry.json`.
2. Un identificador histórico o planificado queda reservado y no puede
   reasignarse a otro propósito.
3. Si el nuevo trabajo amplía el mismo alcance de un bloque existente, se
   prefiere una nueva revisión de ese bloque. `DOC.1 R2` es el precedente.
4. Reabrir un bloque exige demostrar el mismo alcance y una revisión no usada.
   Al materializarse, `EE` continúa el ordinal de estados aceptados del mismo bloque; no se reinicia a E01. Un bloque nuevo sí comienza en E01.
5. Un bloque nuevo solo se crea cuando ninguna identidad registrada cubre el
   alcance.
6. Antes de asignar un número nuevo se auditan registro, árbol vigente,
   historial Git, ledger, plan maestro y evidencia histórica.
7. No se rellenan huecos históricos de forma retroactiva.
8. Los compuestos requieren registro explícito.
9. `R1`, `R1.2`, `R4.2`, etc. son revisiones, nunca familias.
10. Un candidato fallido no consume Global.
11. `docs/archive/` conserva terminología histórica aunque difiera de la política
    vigente.

## Decisión NOR.1 R8

La auditoría posterior a DOC.2 demostró que:

- NOR.1 es la familia que define estándares determinísticos;
- la convención de nombres existente no regulaba identificadores de bloques;
- `NOR.1 R8` no estaba usado ni en el árbol G111 ni en mensajes Git;
- crear un identificador nuevo dentro de NOR, GOV o DOC sin necesidad semántica añadiría una identidad innecesaria.

G112/E07 (`0.1.12.07-beta`) quedó aceptado para **NOR.1 R8 — gobierno de
identificadores de bloques** después de PR #89 y la corrección ordinal PR #90.
La auditoría transversal **DOC.1 R3** quedó aceptada como G113/E03
(`0.1.13.03-beta`) mediante PR #92 / merge `40ae5c0`. PLAN.2 R1 y UX.5 se
registran explícitamente durante la replanificación post-G113. Al ser **PLAN.2**
un bloque nuevo sin revisiones aceptadas, el siguiente candidato comienza en
E01: G114/E01 (`0.1.14.01-beta`). PERSIST.1 permanece reservado para una etapa
posterior y no recibe un Global futuro anticipado.

## Control automático

```text
python scripts/audit_block_identifiers.py
```
