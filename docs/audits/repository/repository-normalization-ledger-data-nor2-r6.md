# NOR.2 R6 — migración del ledger y datos de alto impacto

**Base:** `ad9b3f3`

**Estado:** migración estructural aplicada y validada localmente; integración en `main` pendiente.

## Alcance

R6 normaliza el nombre del ledger estructurado utilizado por VER.2:

- origen: `data/revision_ledger_pre_1_0.json`;
- destino: `data/pre-1-0-revision-ledger.json`.

La revisión no altera el contenido del ledger, no modifica `VERSION`, no
incrementa Global ni revisión y no cambia el esquema JSON.

## Integridad previa al movimiento

- SHA-256:
  `f5e0020643b324119855693588469eb8c98a0abafdb8f6108d60d5fb03a2288e`;
- `schema_version`: **1**;
- `accepted_count`: **70**;
- entradas: **70**;
- Globales: **G001–G070**;
- siguiente Global declarado: **71**;
- siguiente candidato: `0.0.71.01-beta`.

El SHA-256 se verificó idéntico antes y después de `git mv`.

## Referencias detectadas en preflight

El preflight identificó **22 archivos versionados** con referencias al nombre
anterior.

Clasificación:

- **12 consumidores o referencias vivas:** actualizados o adaptados por R6;
- **10 referencias históricas intencionales:** conservadas sin reescritura.

Las referencias preservadas corresponden a `docs/archive/`, evidencias
`docs/audits/` de revisiones anteriores y regresiones cuyo propósito es
documentar o prohibir nombres históricos.

## Contrato de R6

R6 exige:

1. que la ruta anterior deje de existir;
2. que el nuevo ledger conserve exactamente el mismo contenido;
3. que `app/core/version_ledger.py` use la ruta nueva;
4. que el ledger continúe validando G001–G070 sin discontinuidades;
5. que no existan consumidores vivos de la ruta anterior;
6. que las evidencias históricas no sean reescritas para simular el estado
   actual;
7. que `VERSION` permanezca en `0.0.71.01-beta`.

## Siguiente revisión

**NOR.2 R7** revisará los artefactos locales heredados bajo `_entregas/`.


## Gate local previo al commit — 2026-08-25

Resultados observados:

- suite focal R6 y regresiones relacionadas:
  **46 pruebas + 3890 subtests — OK**;
- suite completa:
  **977 pruebas ejecutadas — OK**;
- `python -m pip check`:
  **OK**;
- `python -m compileall -q app tests`:
  **OK**;
- validación sintáctica de JavaScript mediante `node --check`:
  **OK**;
- `git diff --check`:
  **OK**;
- referencias obsoletas no justificadas:
  **0**;
- ruta anterior del ledger:
  **ausente**;
- ruta nueva:
  **presente**;
- SHA-256 preservado:
  `f5e0020643b324119855693588469eb8c98a0abafdb8f6108d60d5fb03a2288e`;
- entradas preservadas:
  **70, G001–G070**;
- `VERSION`:
  `0.0.71.01-beta`, sin cambios.

NOR.2 R6 permanece activo hasta su integración en `main`.
La siguiente revisión planificada es **NOR.2 R7 — artefactos locales**.
