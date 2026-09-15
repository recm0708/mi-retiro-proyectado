# DOC.3 R1 — auditoría documental integral post-G124

**Estado:** en progreso; sin candidato Global preasignado
**Base auditada:** `f9d181ceaaf4824bf8807d9237d0e19e71d3b29c`
**Versión canónica de entrada:** `0.1.24.13-beta` — G124/E13 / MANT.1 R8
**Publicación de entrada:** `v0.1.24.13-beta` publicada como prerelease
**Rama:** `docs/doc3-r1-auditoria-documental`
**Issue propietario:** #154
**Preflight de entrada:** #166 `CLEAN / NO MANT.2 R2`
**Fecha:** 2026-09-14
**Clasificación:** Auditoría documental / Estado vivo / Gobierno / Trazabilidad

## Objetivo

DOC.3 R1 audita integralmente el corpus documental y la metadata viva después
del cierre y publicación de MANT.1 R8/G124. La revisión busca contradicciones
entre documentación, gobierno, versionado, estructura, Issues y publicación sin
modernizar mecánicamente evidencia histórica válida.

DOC.3 R1 se inició sin reservar G125. Durante la apertura:

```text
VERSION                  0.1.24.13-beta
accepted_count           124
next_global              125
next_candidate           null
G125                      disponible, no asignado
DOC.3 R1                  in_progress
PLAN.2 R2                 no iniciado
VER.2 R6                  no iniciado
PERSIST.1                 no iniciado / bloqueado
```

## Alcance operativo confirmado — seis frentes

DOC.3 R1 se ejecuta mediante seis frentes complementarios. Los cinco primeros
responden directamente al objetivo de auditoría documental integral; el sexto
convierte los hallazgos objetivamente verificables en controles permanentes para
reducir recurrencia.

### 1. Estado vigente

Reconciliar en todas las superficies vivas:

- versión publicada vigente;
- último Global aceptado/publicado;
- fase material activa;
- siguiente Global disponible;
- candidato actual, si existe;
- secuencia de fases pendientes.

La representación correcta de entrada es:

```text
G124/E13                 publicado
DOC.3 R1/#154            in_progress
G125                      disponible, no asignado
PLAN.2 R2/#155           no iniciado
VER.2 R6/#164            no iniciado
PERSIST.1/#130           no iniciado / bloqueado
```

### 2. Trazabilidad de gobierno

Cruzar `VERSION`, ledger, registry, manifest, roadmap, master plan, pending
matrix, Issues, Pull Requests, tags y Releases para impedir que existan dos o
más verdades actuales incompatibles.

### 3. Estructura documental

Revisar clasificación VIVO/AUDITORÍA/HISTÓRICO/PLANTILLA/SOPORTE, índices,
huérfanos, stubs, duplicados, rutas, enlaces locales, anchors y referencias.

### 4. Historia preservada

No modernizar mecánicamente auditorías, cierres, entradas históricas de
CHANGELOG/RELEASES, ADR ni evidencia válida. Una afirmación antigua puede
conservarse si su contexto deja claro que describe aquel checkpoint y no el
estado presente.

### 5. Coherencia semántica

Detectar contradicciones materiales aunque la estructura y los enlaces sean
válidos. Ejemplos de esta revisión: una superficie viva no puede decir que G124
está pendiente de publicación cuando el Release ya existe, ni presentar DOC.3
como fase futura cuando #154 está en ejecución.

### 6. Cierre reproducible

Convertir en pruebas, guards o Quality Gate todo control que pueda comprobarse
de forma objetiva. La revisión humana/LLM se conserva para la semántica que no
pueda reducirse de forma segura a una regla determinística.

## Preflight de entrada

Antes de iniciar la fase se verificó:

- `main = f9d181ceaaf4824bf8807d9237d0e19e71d3b29c`;
- `VERSION = 0.1.24.13-beta`;
- G124/E13 publicado mediante `v0.1.24.13-beta`;
- 0 Pull Requests abiertos;
- 0 Pull Requests Dependabot abiertos;
- 0 Dependabot alerts abiertos mediante consulta fresca autenticada;
- re-ejecución de `Dependency Security` en `success`;
- `pip-audit --strict`: sin vulnerabilidades conocidas;
- `npm audit --prefix scripts --audit-level=high`: 0 vulnerabilidades;
- referencias externas de GitHub Actions: OK;
- rama de MANT.1 retirada; el inventario remoto previo a DOC.3 contenía solo
  `main`.

No apareció trabajo material nuevo de dependencias, por lo que no corresponde
insertar MANT.2 R2 antes de DOC.3.

## Baseline automatizado G124

El usuario ejecutó la batería inicial el 2026-09-14. Debido a que PowerShell
procesó el `else` en una entrada separada, el cambio a la rama DOC.3 no ocurrió;
`git status` confirmó `On branch main`. La ejecución se conserva por tanto como
**baseline limpio de G124**, no como validación de la rama de trabajo.

Resultados:

- Markdown auditado: 172 archivos;
- clasificación: 62 VIVO, 33 AUDITORÍA, 64 HISTÓRICO, 9 PLANTILLA y 4 SOPORTE;
- Markdown bloqueante: 0;
- archivos Git/versionables: 651;
- directorios canónicos/README: 84/84;
- enlaces locales rotos: 0;
- documentos vivos huérfanos: 0;
- stubs triviales: 0;
- grupos duplicados exactos/normalizados: 0/0;
- violaciones estructurales/policy/profundidad: 0;
- enlaces externos: 44 descubiertos/evaluados, 33 OK, 11 restringidos, 0 rotos;
- identificadores: 16 familias y 52 identificadores;
- `unittest`: 1600 OK;
- `pytest`: 1640 passed + 7810 subtests passed;
- Quality Gate FULL: 11 PASS / 0 FAIL.

Conclusión del baseline: DOC.3 parte de un G124 estructuralmente limpio. La
deriva confirmada hasta este punto es principalmente **semántica y de
sincronización de estado**, no de integridad física del repositorio.

## Metodología de clasificación

Cada coincidencia se clasifica antes de corregirse:

1. **estado vivo:** debe describir el presente y se corrige cuando existe deriva;
2. **evidencia histórica:** conserva el estado válido de su checkpoint y no se
   moderniza;
3. **contrato machine-readable:** se modifica solo cuando la semántica del campo
   está demostrada y sus pruebas se reconcilian conjuntamente;
4. **pendiente real:** se conserva aunque use versiones o fases anteriores como
   contexto;
5. **prueba histórica o regression-aware:** no se cambia solo para hacerla
   coincidir con el presente; se revisa si indebidamente protege texto vivo
   obsoleto.

## Hallazgo A — deriva de publicación de G124

G124/E13 ya está cerrado y publicado, pero varias superficies vivas todavía lo
describen como aceptado localmente y/o con publicación formal pendiente.

Superficies confirmadas en la primera pasada:

- `README.md`;
- `SECURITY.md`;
- `docs/README.md`;
- `docs/governance/roadmap.md`;
- `docs/governance/master-plan-to-1-0.md`;
- `docs/governance/pre-1-0-pending-matrix.md`;
- `docs/operations/release-process.md`;
- `docs/operations/validation.md`;
- `docs/product/traceability-matrix.md`;
- `docs/decisions/README.md`.

Corrección requerida: las secciones de estado vivo deben reconocer que
`v0.1.24.13-beta` ya está publicada, sin alterar bloques históricos que documenten
el estado anterior al tag/release.

## Hallazgo B — DOC.3 todavía descrito como fase futura

Después de iniciar #154, algunas superficies vivas todavía presentan DOC.3 R1
como “la siguiente fase material” o como trabajo que comenzará después de
publicar G124. Se confirmaron al menos:

- `VERSIONING.md`;
- `docs/README.md`;
- `docs/product/transparency.md`;
- `docs/decisions/README.md`;
- `docs/governance/pre-1-0-revision-ledger.md`;
- `docs/governance/roadmap.md`;
- `docs/governance/master-plan-to-1-0.md`;
- `docs/governance/pre-1-0-pending-matrix.md`.

La corrección viva debe declarar DOC.3 R1 como `in_progress`, mantener PLAN.2 R2,
VER.2 R6 y PERSIST.1 sin iniciar y conservar G125 sin candidato.

## Hallazgo C — estado machine-readable posterior a MANT.1

### Estado detectado al inicio de R1

`data/governance/work-block-registry.json` y
`data/governance/pre-1-0-revision-ledger.json` contenían el estado:

```text
unassigned_pending_post_mant1_r8
```

El valor dejó de describir literalmente el momento operativo cuando DOC.3 R1
pasó a `in_progress`. `next_candidate` continuaba siendo `null`, por lo que el
hallazgo no autorizaba convertir DOC.3 automáticamente en candidato G125.

También se observó `planning_issue = 155` en `current_candidate` y un campo
separado `documentation_audit_issue = 154`. La revisión confirmó que el `155`
representa la replanificación maestra posterior y no el owner de la fase activa.

### Resolución aplicada en Punto 2

La reconciliación separa explícitamente **fase activa** y **candidato Global**:

- `current_candidate.state = "unassigned"`;
- `global_revision`, `revision_aware` y `block` permanecen `null`;
- `next_global_available = 125`;
- `planning_issue = 155` se conserva;
- registry y ledger incorporan `active_phase` para `DOC.3 R1/#154`;
- `active_phase.state = "in_progress"`;
- DOC.3 conserva `global_refs: []`;
- G125 continúa disponible sin candidato ni VERSION preasignados;
- `release-publication-manifest.json` permanece como snapshot de publicación de
  G124/MANT.1 R8 y no se usa para representar la fase activa.

La etiqueta temporal original se conserva únicamente en esta auditoría como
evidencia del estado detectado al inicio de DOC.3 R1.

## Hallazgo D — pruebas que fijan estado vivo obsoleto

La auditoría encontró pruebas que protegen valores nacidos durante el cierre de
G124 y que deben revisarse para separar historia de contrato vivo.

Casos confirmados:

- `tests/governance/test_g124_mant1_r8_promotion.py` exige en la matriz el texto
  `Cerrado/aceptado localmente G124/E13`, que ya no es el estado publicado;
- varias regresiones históricas exigen
  el estado temporal descrito en el Hallazgo C dentro del registry vigente al inicio de R1.

Estas pruebas no se eliminan. Las regresiones que consultan archivos canónicos
vigentes se actualizan para proteger el estado semántico actual `unassigned`, sin
alterar los checkpoints históricos que documentan cuándo surgió la etiqueta
`unassigned_pending_post_mant1_r8`.

Además, DOC.3 R1 incorpora una regresión propia que verifica simultáneamente:

- G124 como último Global aceptado;
- G125 disponible y no asignado;
- DOC.3 R1/#154 como fase activa `in_progress`;
- `planning_issue = 155` preservado;
- manifest de publicación todavía asociado a G124/MANT.1 R8.

## Evidencia que se preserva

No se moderniza mecánicamente:

- `docs/archive/`;
- auditorías cerradas bajo `docs/audits/`;
- entradas históricas publicadas de `CHANGELOG.md`;
- bloques de promoción anteriores en `RELEASES.md` y ledger Markdown cuando su
  contexto identifica claramente el checkpoint histórico;
- ADR y decisiones que documenten correctamente el estado válido en su fecha;
- referencias a G124 como “siguiente Global” dentro de evidencia cerrada de
  G123, cuando el contexto histórico sea inequívoco.

## Punto 1 — estado vigente cerrado

La reconciliación del estado vivo quedó materializada en el commit
`2112b1d` (`docs(doc3): reconcilia estado vivo post-G124`) y superó el
Repository Quality Gate pre-commit con 10 PASS / 0 FAIL y 1600 unittest OK.

El contrato vigente consolidado es:

```text
último publicado        G124/E13 — v0.1.24.13-beta
fase activa             DOC.3 R1/#154
siguiente Global        G125 disponible
candidato G125          ninguno
fase posterior          PLAN.2 R2/#155
luego                   VER.2 R6/#164
bloqueado detrás        PERSIST.1/#130
```

Los bloques inequívocamente históricos se preservan aunque contengan lenguaje
que fue correcto antes de la publicación de G124.

## Invariantes de R1

Durante la auditoría inicial:

- `VERSION` no cambia;
- G125 no se reserva;
- no se inicia PLAN.2 R2/#155;
- no se inicia VER.2 R6/#164;
- no se inicia PERSIST.1/#130;
- MANT.2 R2 solo se insertaría si un preflight posterior detecta trabajo material
  nuevo de dependencias;
- DOC.1 R6/#147 permanece como freeze documental final independiente.

<!-- DOC3-R1-SEMANTIC-CHECKPOINT:START -->
## Checkpoint semántico — estado vivo e historia preservada

**Fecha:** 2026-09-14
**Base estructural:** `6998736`
**Estado:** validado, pendiente de commit/publicación en la rama DOC.3

La auditoría semántica posterior al saneamiento estructural distinguió estado vivo,
checkpoints históricos embebidos y registros históricos canónicos. El cierre de este
checkpoint aplica las siguientes decisiones:

- los 11 bloques `NOR3-G122-PROMOTION` conservan íntegramente sus hechos, pero se
  presentan de forma inequívoca como **registro histórico** y no como estado vigente;
- `docs/product/functional-specification.md` queda reconciliado con
  `0.1.24.13-beta` / G124/E13, DOC.3 R1/#154 en ejecución y G125 disponible sin
  candidato, bloque ni `VERSION` preasignados;
- PERSIST.1 permanece bloqueado por `#154 → #155 → #164`;
- `CHANGELOG.md`, `RELEASES.md`, `docs/archive/**`, auditorías cerradas y demás
  snapshots históricos no se modernizan mecánicamente;
- `VERSION` y `data/governance/release-publication-manifest.json` permanecen
  intactos en G124/E13 hasta que exista un candidato material real.

Validación previa al commit:

- auditores canónicos Markdown, integridad del repositorio e identificadores: PASS;
- 24 regresiones dirigidas: **24 OK**;
- `git diff --check`: limpio;
- semántica viva reconciliada y checkpoint G122 preservado como historia.
<!-- DOC3-R1-SEMANTIC-CHECKPOINT:END -->

<!-- DOC3-R1-MARKDOWN-FINAL:START -->
## Limpieza Markdown final ? 173/173

**Fecha:** 2026-09-14
**Estado:** validado antes de la promoci?n material de DOC.3 R1

La pasada final se ejecut? sobre los **173 archivos Markdown versionados** y
normaliz? ?nicamente reglas objetivas de formato:

- 23 archivos requirieron normalizaci?n autom?tica en esta pasada;
- 2 l?neas con whitespace final fueron corregidas;
- 212 l?neas en blanco excedentes fueron eliminadas conforme a MD012;
- 1 final de archivo fue normalizado;
- los bloques de c?digo se preservaron sin modificar su contenido;
- las superficies hist?ricas modificadas por esta limpieza se verificaron
  contra `HEAD` y solo contienen diferencias de whitespace/MD012;
- `scripts/audit_markdown.py` finaliz? sin problemas bloqueantes;
- integridad del repositorio: 0 enlaces locales rotos, 0 documentos vivos
  hu?rfanos, 0 stubs triviales, 0 duplicados exactos/normalizados y 0
  violaciones de profundidad;
- inventario de identificadores: 16 familias / 52 identificadores;
- `git diff --check`: limpio.

`markdownlint-cli2` no est? instalado como comando local/global en el entorno y
DOC.3 no incorpora dependencias ?nicamente para ejecutar esta comprobaci?n. El
auditor can?nico del repositorio permanece como gate obligatorio de Markdown.
<!-- DOC3-R1-MARKDOWN-FINAL:END -->

<!-- DOC3-R1-DEFERRED-DOC4:START -->
## Hallazgo diferido con owner — DOC.4 R1

Durante DOC.3 R1 se confirmó que la coherencia y validez estructural no
garantizan por sí solas que cada documento contenga únicamente información
pertinente a su función. El saneamiento de contenido por responsabilidad se
transfiere a una fase posterior y no se absorbe en DOC.3:

- **#171 — DOC.4 R1:** reingeniería documental canónica current-state-only;
- **#172 — Lote A:** revisión y reescritura 1:1 de todos los Markdown;
- **#173 — Lote B:** poda, fusión, renombre, movimiento y eliminación del árbol;
- **#174 — Lote C:** revisión por extensión de artefactos textuales no ejecutables.

DOC.4 permanece `approved_not_started`, sin Global ni `VERSION` preasignados.
PLAN.2 R2/#155 debe decidir su posición exacta y sincronizar el árbol definitivo
antes de que DOC.4 pueda iniciar. El código ejecutable del aplicativo queda fuera
de DOC.4 salvo referencias mínimas afectadas por cambios documentales.
<!-- DOC3-R1-DEFERRED-DOC4:END -->

<!-- DOC3-R1-G125-MATERIALIZATION:START -->
## Materialización revision-aware — G125/E01

**Fecha:** 2026-09-15
**Estado:** aceptado localmente / publicación pendiente

DOC.3 R1 se materializa como **G125/E01 (`0.1.25.01-beta`)** después de cerrar
sus seis frentes, completar la limpieza Markdown 173/173 y superar el preflight
final #166.

Evidencia previa a materialización:

- Quality Gate FULL: **11 PASS / 0 FAIL**;
- `unittest`: **1603 OK**;
- `pytest`: **1643 passed + 7824 subtests**;
- Markdown: **173** archivos sin bloqueantes;
- JavaScript: **27** archivos válidos;
- identificadores: **16 familias / 53 identificadores**;
- integridad: **653** archivos versionables, **84/84** README canónicos,
  **0** enlaces locales rotos y **0** documentos vivos huérfanos;
- preflight #166: **0 PRs**, **0 Dependabot alerts**, **0 PRs Dependabot**;
- `pip-audit --strict`: sin vulnerabilidades conocidas;
- `npm audit --prefix scripts --audit-level=high`: 0 vulnerabilidades.

La publicación definitiva requiere PR/merge, revalidación de `main`, tag
firmado y GitHub Release prerelease. PLAN.2 R2/#155 permanece sin iniciar.
<!-- DOC3-R1-G125-MATERIALIZATION:END -->
