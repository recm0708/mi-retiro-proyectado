# Gobierno del proyecto

**Proyecto:** Mi Retiro Proyectado
**Estado:** vigente desde GOV.1.2
**Fecha de adopción:** 2026-08-18
**Última revisión de estado:** VER.2 R6/#164 en ejecución sobre G127/E02 publicado (`0.1.27.02-beta`); G128 libre — 2026-09-21

<!-- NOR3-G122-PROMOTION:START -->
## Registro histórico — promoción G122-E01 post-NOR.3

> **Checkpoint histórico preservado.** Este bloque describe el estado inmediatamente posterior a la integración de NOR.3 y anterior a MANT.2 R1 / MANT.1 R8. No representa el estado vigente del repositorio; las secciones vigentes posteriores de este documento tienen precedencia.

- `VERSION` materializa `0.1.22.01-beta` para NOR.3 R8 / G122-E01.
- NOR.3 R1–R8 quedó integrado/aceptado mediante PR #162 / merge
  `b97cf61763479b80b8e8724b878089e8bb20fa00`.
- La revalidación automática de `main` quedó GREEN: Repository Quality Gate,
  Visual & Accessibility y CodeQL finalizaron en `success`.
- G123 es el siguiente Global disponible, pero **no tiene candidato ni bloque
  preasignado**.
- PERSIST.1 permanece planificado y no iniciado, sin Global preasignado.
- `v0.1.21.01-beta` / G121/E01 permanece como última publicación revision-aware
  hasta completar el tag/release firmado de G122/E01.
- `v0.1.22.01-beta` queda pendiente de creación/firma local y de la
  verificación/publicación gobernada por REL.GOV.1.
<!-- NOR3-G122-PROMOTION:END -->

<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:START -->
## Estado vigente post-G127 / VER.2 R6 en curso

MANT.2 R2/#206 está cerrado, integrado y publicado como **G127/E02**
(`0.1.27.02-beta`) sobre
`main@2df33a5c24d1c7cea1a6db91539a92da02c91500`, mediante PR #207,
tag firmado `v0.1.27.02-beta` y GitHub Release prerelease 392412590.

El preflight #166 posterior a G127/E02 quedó **CLEAN** y habilitó
VER.2 R6/#164.

VER.2 R6/#164 está en ejecución mediante la rama
`ver/ver2-r6-revision-aware` y el Draft PR #208. CP1–CP6A-R1 están
cerrados y auditados remotamente.

**G128 permanece libre** y sin candidato, bloque ni `VERSION` preasignados.

La continuidad material vigente es:

1. **cerrar CP6B documental de VER.2 R6**;
2. **auditoría/candidato final de VER.2 R6**;
3. **DOC.4 R1 / #171** después de publicar VER.2;
4. **#142** y derivados funcionales obligatorios;
5. **PERSIST.1 / #130 → REP.1 / #143 → DEPLOY.1 / #157**;
6. **UX.7→UX.x / #129** bajo #189;
7. **SEC.2 R7 → rendimiento → A11Y.2 → REV.1 → #153 → DOC.1 R6 → QA.1 → REL.1**.

Un MANT.2 R3+ solo se inserta si #166 detecta trabajo material nuevo.
<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:END -->


<!-- DOC1-R1-POST-MANT1:START -->
## Estado de gobierno vigente

- `VERSION` sigue siendo la fuente única y materializa `0.1.27.02-beta`
  para MANT.2 R2 / G127-E02 publicado.
- G126/E01 / PLAN.2 R2 y G125/E01 / DOC.3 R1 permanecen como publicaciones
  históricas anteriores.
- MANT.2 R2/#206 está cerrado/publicado; #204/#205 quedaron sustituidos por
  PR #207.
- El preflight post-G127 #166 quedó CLEAN.
- VER.2 R6/#164 está en ejecución mediante Draft PR #208.
- G128 permanece libre y `current_candidate` sigue sin asignar.
- DOC.4/#171 queda después de VER.2; #142/derivados preceden PERSIST.1.
- El programa UX se gobierna por #129: baseline UX.7–UX.32, expansión UX.33+
  y sincronización visual multiportal obligatoria mediante #189.
- Todo tag formal futuro exige integración, revalidación, firma y publicación
  gobernada conforme a REL.GOV.1 y #166.
<!-- DOC1-R1-POST-MANT1:END -->

## 1. Propósito

Este documento define quién mantiene el proyecto, cómo se adoptan decisiones y qué controles mínimos deben cumplirse antes de integrar cambios. Su finalidad es facilitar mantenimiento, revisión independiente y auditoría.

## 2. Mantenimiento actual

El mantenedor y responsable de revisión actual del repositorio es:

- **Rubén Enrique Cañizares Miranda** (`@recm0708`).

`.github/CODEOWNERS` refleja esta responsabilidad técnica. CODEOWNERS no constituye una certificación jurídica ni una aprobación de la Caja de Seguro Social de Panamá.

## 3. Principios de gobierno

1. **Trazabilidad:** todo cambio relevante debe poder rastrearse desde Git hasta código, pruebas y documentación.
2. **Separación normativa:** las decisiones técnicas no deben presentarse como requisitos legales sin una fuente oficial.
3. **Transparencia:** no se introducen comportamientos deliberadamente ocultos al modelo documental y de auditoría del proyecto.
4. **Privacidad por defecto:** observabilidad y pruebas no justifican almacenar datos personales reales innecesarios.
5. **Reproducibilidad:** una afirmación técnica importante debe poder verificarse mediante código, prueba, fuente o procedimiento documentado.
6. **Historia preservada:** una decisión sustituida se marca como tal; no se elimina para aparentar que nunca existió.
7. **Independencia institucional:** el proyecto no debe presentarse como producto oficial de la CSS.
8. **Sincronización transversal:** cuando evoluciona un contrato compartido, se revisan conjuntamente código, pruebas, interfaz, normativa, documentación y evidencia de release que dependan de él.
9. **Issues verificables:** toda Issue nueva debe incluir un checklist real de trabajo y cierre que permanezca actualizado hasta resolver o transferir todos sus puntos aplicables.

## 4. Tipos de cambio

### 4.1. Funcionalidad y UX

Requieren:

- implementación;
- regresiones automatizadas cuando sean razonables;
- validación manual cuando el comportamiento sea visual o interactivo;
- actualización de documentación dependiente.

### 4.2. Motores y normativa

Todo cambio de fórmula, parámetro, fecha, tabla o interpretación previsional requiere:

- fuente oficial identificable;
- prueba de regresión;
- actualización de `regulations/` cuando corresponda;
- documentación técnica/normativa;
- ADR cuando exista interpretación o decisión no trivial.

### 4.3. Seguridad, privacidad y observabilidad

Requieren revisión de:

- datos tratados;
- datos registrados;
- retención;
- exposición externa;
- mensajes de error;
- documentación pública y técnica;
- pruebas de no regresión.

### 4.4. Gobierno y releases

Cambios en versionado, licencia, gobernanza, CI o proceso de publicación deben quedar documentados y no pueden depender únicamente de una convención oral.

### 4.5. Ciclo de vida obligatorio de Issues

Toda Issue nueva, ya sea creada manualmente, mediante Issue Forms, automatización
o asistencia programática, debe contener al menos un checklist Markdown real con
elementos `- [ ]` / `- [x]`.

El checklist debe representar trabajo verificable y, cuando aplique, cubrir:

- condiciones y dependencias de entrada;
- implementación o trabajo principal;
- pruebas, gates y evidencia;
- documentación, trazabilidad e Issues derivadas;
- criterio de cierre.

Una casilla solo pasa a `[x]` cuando exista evidencia suficiente de que el punto
quedó completado. Una Issue material se cierra cuando todos sus puntos
aplicables y su criterio de cierre estén completos. Si aparece trabajo fuera de
alcance, debe transferirse a un owner/Issue explícito antes del cierre.

Las Issues transversales o recurrentes pueden permanecer abiertas mientras
exista trabajo recurrente pendiente, pero cada ejecución debe actualizar su
checklist y conservar evidencia del resultado.

Los Issue Forms versionados bajo `.github/ISSUE_TEMPLATE/` deben pregenerar un
checklist de trabajo/cierre. Los guards del repositorio protegen este contrato
para impedir que nuevas plantillas vuelvan a crear Issues sin seguimiento.

## 5. Decisiones

Las decisiones relevantes se documentan mediante ADR consecutivos en `docs/decisions/README.md`.

Un ADR puede estar:

- vigente;
- sustituido parcialmente;
- sustituido;
- rechazado, cuando resulte útil conservar la alternativa evaluada.

Una decisión antigua no se borra solo porque una revisión posterior cambie el criterio.

## 6. Integración a `main`

Antes de integrar un hito cerrado se exige, como mínimo:

```powershell
python -m compileall app
python -m unittest discover -s tests -q
git diff --check
```

Para JavaScript modificado se valida además `node --check`.

Desde la migración criptográfica del 2026-08-17, todo commit nuevo debe incorporar **firma criptográfica SSH**. Antes del push se verifica con:

```powershell
git verify-commit HEAD
git log --show-signature -1
```

La CI remota debe permanecer en verde.

GOV.1.6 introdujo históricamente
`.github/workflows/governance-audit.yml` y el check
**Auditoría de gobernanza** como control independiente. La migración
post-G119 absorbió ese contrato, junto con CI y Markdown, dentro del gate
canónico después de demostrar equivalencia remota en GitHub.

### Automatización canónica post-G119

El ruleset vigente de `main` exige `Repository Quality Gate` y
`Python Compatibility`.

`Repository Quality Gate` centraliza validación técnica, documental, de
integridad y política de Pull Requests. `Python Compatibility` preserva la
compatibilidad con Python 3.13.

`Dependency Security`, `Visual & Accessibility` y CodeQL permanecen como
controles complementarios. `verificar-tags.yml` continúa separado por su
contrato específico de firma y publicación.

Los workflows legacy `ci.yml`, `governance-audit.yml` y
`markdown-audit.yml` fueron retirados después de migrar el ruleset, sin abrir
una ventana de desprotección. CodeQL permanece independiente.

La migración final quedó integrada mediante PR #117. El mantenimiento
coordinado PR #118 actualizó la pareja Pydantic/Pydantic Core, Dependency
Review y la agrupación de Dependabot sin modificar `VERSION`, el ledger ni el
manifiesto de publicación. Estos cambios son mantenimiento posterior a
G119/E05 y no consumen G120/E01.

La rama predeterminada está protegida mediante un ruleset activo que exige Pull Request, commits verificados, historial lineal, resolución de conversaciones, los checks `Repository Quality Gate` y `Python Compatibility`, rama actualizada antes de integrar y bloqueo de eliminación y force push.

El rol `Repository admin` dispone únicamente de bypass mediante Pull Request para recuperación administrativa excepcional.

La integración ordinaria utiliza ramas de trabajo y `Squash and merge`; no se realizan pushes directos ordinarios a `main`.

Los tags `v*` están cubiertos por un ruleset activo que permite crear nuevas versiones, pero bloquea actualización, eliminación y force push de tags publicados.

## 7. Versiones y tags

La política aplicable está en `VERSIONING.md`.

- `VERSION` es la fuente canónica.
- Los tags formales empiezan con `v`.
- La familia `0.0.N-beta` es legacy histórica y la revision-aware v1 publicada permanece inmutable; los estados beta prospectivos desde G128 usan `0.<GLOBAL>.<EDITION>.<CORRECTION>-beta` conforme a VER.2.
- Ancla histórica v1: la política anterior decía que los estados beta nuevos usan `0.GG.RR.EE-beta`; esa formulación se conserva solo para regresión histórica y queda sustituida prospectivamente por v2 desde G128.
- La primera versión oficial objetivo es `1.0.0.0`, después de cerrar todos los gates del plan maestro.
- Las versiones oficiales usan `MAYOR.MENOR.PARCHE.REVISIÓN`; la cuarta posición identifica una revisión/hotfix.
- El Build es un identificador independiente de seis dígitos para artefactos oficiales reproducibles; no forma parte de `VERSION` ni del tag y no se incrementa por commit.
- La planificación histórica `0.1.0-beta.1` deja de ser un objetivo vigente; las evidencias históricas que la mencionan se preservan.
- `0.0.1-beta` a `0.0.21-beta` fueron reconstruidas documentalmente y posteriormente materializadas como tags retrospectivos firmados sin aparentar existencia histórica.
- `v0.0.22-beta` y `v0.0.23-beta` fueron reemitidos una sola vez como objetos firmados sin cambiar sus commits objetivo; esa excepción ya fue consumida.
- Después de la migración, todo commit nuevo y todo tag nuevo deben estar firmados. `v0.0.24-beta` y `v0.0.25-beta` fueron creados bajo esta política y se verificaron correctamente.
- La fuente canónica y asignación del Build se definirán en REL.1; hasta entonces no se publica un Build ficticio.
- La clave privada nunca se versiona.
- Desde REL.GOV.1, todo tag formal nuevo debe tener un GitHub Release asociado con título canónico, cuerpo mínimo auditable y estado prerelease/estable coherente con `VERSION`.
- `docs/operations/release-process.md` es la política canónica de publicación; `.github/release.yml` solo asiste la categorización automática y `scripts/release_contract.py` valida el contrato local de VERSION/ledger/tag/título/notas.
- La edición de metadatos de un Release histórico puede corregir formato o reconciliación sin mover ni recrear su tag; toda corrección semántica debe conservar la denominación original como evidencia.

## 8. Propiedad y revisión de áreas críticas

Antes de crear o reutilizar una sigla, fase o bloque se consultan `docs/standards/work-block-identifiers.md` y `data/governance/work-block-registry.json`. Los identificadores históricos o planificados no se reasignan; `R...` identifica revisiones, no bloques.

Mientras exista un único mantenedor, `@recm0708` revisa todo el repositorio. Se consideran especialmente críticas:

- `regulations/`;
- `app/engines/`;
- `app/core/`;
- documentación de seguridad, privacidad, normativa y auditoría;
- `.github/`;
- archivos de versionado y publicación.

Cuando existan nuevos mantenedores, CODEOWNERS deberá granularizar estas responsabilidades.

## 9. Licencia

GOV.1.7 adopta una **licencia propietaria pre-beta / todos los derechos reservados** para los materiales originales del proyecto.

La denominación histórica de esa decisión de licencia se conserva. PLAN.1 no cambia la licencia: la etapa funcional actual se identifica como beta y cualquier relicencia sigue requiriendo una decisión separada.

- `LICENSE` define el alcance de esos materiales;
- `THIRD_PARTY_NOTICES.md` separa componentes upstream;
- `docs/governance/licensing-and-distribution.md` registra alternativas y motivo de la decisión;
- la disponibilidad del código no concede derechos de reutilización o explotación comercial;
- una futura relicencia abierta requiere decisión expresa y derechos suficientes sobre contribuciones incorporadas.

La revisión jurídica externa previa a publicación pública/comercial continúa siendo un gate.

## 10. Incidentes y vulnerabilidades

`SECURITY.md` es la política vigente para reportar vulnerabilidades. No deben abrirse como issues públicos vulnerabilidades con detalles explotables, credenciales, datos personales o evidencia sensible.

El repositorio mantiene Dependency graph, Dependabot alerts y Dependabot security updates activos. Dependabot no sustituye revisión humana, pruebas de regresión ni la decisión explícita del mantenedor.

Las plantillas `.github/ISSUE_TEMPLATE/` separan errores ordinarios, solicitudes de mejora y consultas de soporte; `.github/pull_request_template.md` estandariza el contexto mínimo de integración. `CODE_OF_CONDUCT.md` define las normas de participación y `SUPPORT.md` enruta soporte, privacidad y seguridad. `docs/archive/governance/github-audit.md` registra los controles versionados y los settings que requieren verificación periódica en GitHub.

## 11. Cambios a este documento

Toda modificación sustancial de gobierno debe:

- quedar registrada en Git;
- explicar su motivo;
- actualizar documentos relacionados;
- respetar el historial anterior.

<!-- NOR3-GOV-BOOTSTRAP:START -->
## Gobierno durable de Issues y Pull Requests

La convención canónica de Issues, checkpoints, labels, revisiones por pares,
Milestones y Pull Requests se mantiene en
[`docs/governance/github-issues-pr-governance.md`](docs/governance/github-issues-pr-governance.md).

Durante NOR.3 se aplica por defecto la ejecución `R1+R2`, `R3+R4`, `R5+R6`
y `R7+R8` dentro de un bloque ya autorizado, preservando evidencia individual
por revisión y separando el par cuando la auditabilidad o el riesgo lo exijan.
<!-- NOR3-GOV-BOOTSTRAP:END -->
