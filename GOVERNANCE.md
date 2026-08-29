# Gobierno del proyecto

**Proyecto:** Mi Retiro Proyectado
**Estado:** vigente desde GOV.1.2
**Fecha de adopción:** 2026-08-18
**Última revisión:** promoción formal DEV.2 R5 — G118/E04 aceptado; DEV.2 R6 candidato G119/E05 — 2026-08-28


<!-- DOC1-R1-POST-MANT1:START -->
## Estado de gobierno post-MANT.1

El gobierno vigente conserva la separación entre estado canónico, evidencia histórica y revisiones en curso.

Estado vigente:

- `VERSION` sigue siendo la fuente única de versión.
- `0.1.18.04-beta` es la versión canónica vigente y materializa G118/E04 (DEV.2 R5); G119/E05 queda reservado para DEV.2 R6.
- G117/E02 está publicado mediante el tag anotado y firmado `v0.1.17.02-beta` y su GitHub Release prerelease automatizado por REL.GOV.1 R2 después de integrar y revalidar la promoción. G116/E05 (`v0.1.16.05-beta`) permanece como publicación previa firmada e inmutable.
- `v0.0.71.01-beta` conserva su evidencia histórica reconciliada como G087/E01 y `v0.0.26-beta` permanece como tag legacy histórico.
- REL.GOV.1 R1 y R2 quedan cerrados/aceptados como G110/E01 y G117/E02.
- DOC.1 R1–R5, PLAN.2 R1, NOR.1, NOR.2, SEC.2 R1–R6 y AUD.SEC2 R1 permanecen cerrados/aceptados según su ledger.
- DEV.2 R5 queda aceptado como G118/E04 (`0.1.18.04-beta`) después de PR #107 / merge `bc97db0`; DEV.2 R6 queda como candidato G119/E05 (`0.1.19.05-beta`) y UX.5 continúa después conforme a la matriz maestra.
- PERSIST.1 permanece reservado para una etapa posterior.
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

GOV.1.6 añadió `.github/workflows/governance-audit.yml`. El job **Auditoría de gobernanza** usa permisos de solo lectura y no reemplaza los checks funcionales `Python 3.13` y `Python 3.14`. Tras su primera ejecución exitosa fue incorporado al ruleset de `main`; el conjunto requerido vigente contiene los tres checks.

Desde el 2026-08-17 la rama predeterminada está protegida mediante un ruleset activo que exige Pull Request, commits verificados, historial lineal, resolución de conversaciones, checks `Python 3.13` y `Python 3.14`, rama actualizada antes de integrar y bloqueo de eliminación y force push.

El rol `Repository admin` dispone únicamente de bypass mediante Pull Request para recuperación administrativa excepcional.

La integración ordinaria utiliza ramas de trabajo y `Squash and merge`; no se realizan pushes directos ordinarios a `main`.

Los tags `v*` están cubiertos por un ruleset activo que permite crear nuevas versiones, pero bloquea actualización, eliminación y force push de tags publicados.

## 7. Versiones y tags

La política aplicable está en `VERSIONING.md`.

- `VERSION` es la fuente canónica.
- Los tags formales empiezan con `v`.
- La familia `0.0.N-beta` es legacy histórica; los estados beta nuevos usan `0.GG.RR.EE-beta` conforme a VER.2 y al ledger reconciliado.
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

Antes de crear o reutilizar una sigla, fase o bloque se consultan `docs/standards/work-block-identifiers.md` y `data/work-block-registry.json`. Los identificadores históricos o planificados no se reasignan; `R...` identifica revisiones, no bloques.


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
