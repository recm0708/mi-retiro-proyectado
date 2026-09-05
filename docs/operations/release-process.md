# Proceso de release

**Estado:** Vigente
**Versión de aplicación:** `0.1.19.05-beta` — G119/E05 aceptado/publicado para DEV.2 R6; UX.5 R6 es candidato de cierre G120/E01 (`0.1.20.01-beta`), todavía no aceptado; UX.6 queda planificado sin Global preasignado.
**Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
**Último tag formal legacy:** `v0.0.26-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Base documental:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal:** REL.GOV.1 — gobierno de GitHub Releases — 2026-08-26
**Clasificación:** Gobierno / Release / Auditoría

<!-- DOC1-R1-POST-MANT1:START -->
## Estado post-MANT.1

El proceso formal de release permanece gobernado por `VERSION`, el ledger,
el manifiesto versionado y los gates de CI.

Estado vigente:

- `VERSION` materializa `0.1.19.05-beta` como G119/E05 para DEV.2 R6.
- DEV.2 R6 fue integrado mediante PR #111 / merge `bd2accb`.
- G119/E05 está publicado mediante `v0.1.19.05-beta`; G118/E04
  permanece preservado como publicación anterior.
- G120/E01 (`0.1.20.01-beta`) permanece reservado para el cierre UX.5 R6; UX.6 queda planificado después sin Global preasignado.
- La automatización no crea ni firma tags; esa frontera permanece local.
- El tag `v0.1.19.05-beta` fue creado de forma anotada y firmada
  después del merge de promoción y de la revalidación de `main`;
  el workflow de firma #17 y el GitHub Release prerelease quedaron
  publicados correctamente.
- Un Release existente incompatible falla cerrado y solo HTTP 404
  autoriza creación.

Todo release futuro requiere gate completo, PR/CI, documentación coherente,
tag firmado y evidencia reproducible.
<!-- DOC1-R1-POST-MANT1:END -->

Este procedimiento complementa `VERSIONING.md`, `RELEASES.md`, `CHANGELOG.md`, `GOVERNANCE.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `docs/governance/licensing-and-distribution.md`, `docs/archive/governance/pre-1-0-versioning-audit.md`, `docs/governance/pre-1-0-revision-ledger.md`, `docs/archive/governance/ver2-revision-decision-matrix.md`, `data/pre-1-0-revision-ledger.json` y `docs/governance/master-plan-to-1-0.md`.

## 1. Principio

Un tag formal identifica un estado **cerrado, reproducible y validado**. No se etiqueta un árbol que todavía está pendiente de validación.

La historia beta publicada conserva la familia legacy:

```text
0.0.N-beta
```

Los estados beta nuevos posteriores a VER.2 usan:

```text
0.GG.RR.EE-beta
```

La primera versión oficial objetivo usa cuatro componentes y se prevé inicialmente como `1.0.0.0`.

El identificador `Build` es independiente de `VERSION`. No se inventa ni se incrementa por commit; se materializa cuando REL.1 disponga de un proceso reproducible de generación de artefactos oficiales.

## 2. Qué constituye una revisión aceptada

Antes de preparar una nueva beta revision-aware debe verificarse que el cambio representa un **estado aceptado** según `VERSIONING.md` y el ledger.

No consumen un nuevo `G` por sí solos:

- commits separados de implementación, pruebas y documentación del mismo estado;
- candidatos sujetos a validación manual o automática;
- un intento que falla su gate;
- el PR, squash, CI o tag que únicamente materializa el mismo estado;
- un checkpoint que solo consolida estados ya contabilizados y deja pendiente la siguiente revisión funcional.

Sí puede consumir un nuevo `G` un estado de mantenimiento, seguridad, gobierno, dependencias o documentación cuando sea materialmente independiente, tenga evidencia propia de aceptación y constituya una configuración auditable distinta.

El candidato reserva el siguiente número global, pero ese número solo queda consumido después del cierre satisfactorio. Si falla, se corrige conservando el mismo identificador reservado.

La revisión funcional (`R#`) y el ordinal aceptado (`E##`) no se consideran equivalentes por definición. Cuando una revisión intermedia no consume Global, el ledger puede declarar `functional_revision`; el manifiesto de publicación usa ese valor para mostrar el nombre funcional correcto. DEV.2 R5 = G118/E04 y DEV.2 R6 = G119/E05 son precedentes
canónicos de revisiones funcionales cuyo ordinal aceptado difiere de la
revisión funcional. El candidato de cierre vigente es UX.5 R6 = G120/E01. R1–R5 fueron revisiones internas no aceptadas independientemente, por lo que el ordinal continúa siendo E01.

## 3. Precondiciones

Antes del cierre:

- hito funcional/técnico/documental terminado;
- código, pruebas y documentación dependiente coherentes;
- working tree controlado;
- versión anterior y último `G` aceptado trazables;
- siguiente `G` sin duplicados ni huecos en el ledger;
- limitaciones conocidas actualizadas cuando corresponda;
- licencia del proyecto coherente con el objetivo de distribución;
- `THIRD_PARTY_NOTICES.md` revisado si el artefacto incluye componentes de terceros.

## 4. Validación del hito antes del incremento

Ejecutar, como mínimo:

```powershell
python -m pip check
git diff --check
python -m compileall app

Get-ChildItem .\app\static\js\*.js | ForEach-Object {
    node --check $_.FullName
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

python -m unittest discover -s tests -q
```

No se registra como “validado” un conteo que no se haya ejecutado realmente.

Cuando una fase requiere validación manual, esa aceptación debe registrarse antes de declarar el estado cerrado.

## 5. Preparación del candidato

Cuando el alcance está listo para gate:

1. confirmar el último estado aceptado del ledger;
2. reservar el siguiente `G` y el `EE` correspondiente al bloque;
3. construir el identificador según `VERSIONING.md`;
4. actualizar `VERSION` como **candidato**;
5. actualizar únicamente las superficies de estado vigente y los documentos materialmente afectados;
6. no reescribir metadata histórica de documentos de dominio solo para copiar la versión nueva;
7. mantener los cambios bajo `Unreleased` mientras el estado no se haya integrado;
8. actualizar `roadmap.md`, ledger/auditoría y trazabilidad;
9. actualizar tests de coherencia sin fijar innecesariamente versiones históricas como estado eterno;
10. revisar licencia/terceros si el contenido distribuible cambió;
11. si se trata de un artefacto oficial, asignar Build únicamente con el mecanismo canónico de REL.1.

Durante esta etapa el número está reservado pero **no aceptado**.

## 6. Validación del candidato

Después de preparar `VERSION`:

- repetir suite completa;
- ejecutar `python -m pip check`;
- repetir `git diff --check`;
- comprobar `VERSION`, `APP_VERSION`, FastAPI y footer;
- ejecutar el validador del ledger estructurado y comprobar que preserve G001–G070 sin huecos ni duplicados;
- comprobar que `VERSION` corresponda al último estado aceptado o al candidato reservado del ledger mediante `python scripts/release_contract.py`;
- comprobar README, ROADMAP, SECURITY, CHANGELOG, RELEASES y proceso de release;
- comprobar que un candidato no se presente como tag/release ya publicado;
- revisar que no existan logs, PDFs personales o secretos preparados para commit;
- comprobar avisos/licencias de terceros cuando corresponda;
- para artefactos oficiales, comprobar correspondencia entre versión, Build, hashes y contenido reproducible.

## 7. Commit de cierre

El cierre de versión debe quedar en uno o más commits lógicos **firmados** en el flujo ordinario del mantenedor.

```powershell
git verify-commit HEAD
git log --show-signature -1
git status
```

El árbol debe quedar limpio y la firma debe verificarse cuando el commit haya sido creado desde el flujo local firmado.

Los commits técnicos producidos por integraciones autorizadas pueden existir durante el armado del candidato; el gate definitivo sigue siendo PR protegido, CI e integración verificada conforme a la política del repositorio.

## 8. Pull Request, integración y CI remota

`main` está protegida y no recibe pushes directos ordinarios.

Publicar la rama de trabajo:

```powershell
git push -u origin <rama>
```

Abrir un Pull Request hacia `main` y confirmar:

- rama actualizada respecto de `main`;
- check requerido `Repository Quality Gate` en **success**;
- check requerido `Python Compatibility` en **success**;
- conversaciones resueltas;
- ausencia de cambios no relacionados;
- evidencia local requerida disponible.

La migración de automatización post-G119 está cerrada. `Repository Quality
Gate` y `Python Compatibility` constituyen los required checks del ruleset de
`main`. `Dependency Security`, Visual/Accessibility y CodeQL complementan esos
controles cuando resultan aplicables al alcance del cambio.

La integración ordinaria se realiza mediante `Squash and merge`. El commit resultante en `main` debe cumplir los controles de firma/verificación exigidos por el ruleset.

Después de integrar:

```powershell
git switch main
git fetch origin --prune
git pull --ff-only origin main
```

Confirmar `HEAD == origin/main`, working tree limpio y revalidar el nuevo SHA de `main`.

Solo entonces el `G` reservado se considera **aceptado** y el ledger pasa de “candidato/reservado” a estado cerrado.

## 9. Tag formal

Solo después de integrar y revalidar se crea un tag, cuando el cierre determine que corresponde materializar ese estado como hito formal.

La etiqueta se deriva exactamente de `VERSION`:

```powershell
$version = (Get-Content .\VERSION).Trim()
git tag -s "v$version" -m "Mi Retiro Proyectado v$version"
git tag -v "v$version"
git push origin "v$version"
```

Ejemplos:

```text
v0.0.26-beta       # último tag legacy histórico
v0.0.71.01-beta    # tag histórico; reconciliado posteriormente como G087/E01
v0.1.09.01-beta    # G109/E01, primer release posterior a la reconciliación
v1.0.0.0
v1.0.0.1
```

No se crean tags revision-aware retrospectivos para G001–G070.

El tag debe apuntar al commit validado y usar una clave autorizada por la política vigente. La creación y firma del tag permanecen fuera de GitHub Actions y bajo control del mantenedor. `.github/workflows/verificar-tags.yml` verifica firma, contrato, correspondencia del tag y pertenencia del commit al historial de `main`; REL.GOV.1 R2 añade después un job separado de publicación.

## 10. Build oficial

`Build` no forma parte de `VERSION` ni del tag.

Para la primera versión oficial prevista:

```text
Versión 1.0.0.0
Build 000001
Tag v1.0.0.0
```

REL.1 definirá la fuente canónica del Build, su incremento monotónico, el empaquetado reproducible y la asociación inequívoca entre Build, commit, tag, hashes y artefactos.

Hasta entonces no se publica un Build ficticio.

## 11. Inmutabilidad

Después de la migración criptográfica del 2026-08-17, un tag publicado:

- no se mueve;
- no se reutiliza;
- no se elimina para ocultar historia;
- no se fuerza para ocultar una corrección posterior.

La única excepción histórica fue la reemisión firmada de `v0.0.22-beta` y `v0.0.23-beta`, ejecutada el 2026-08-17 preservando sus commits objetivo. Esa excepción no puede repetirse.

Una corrección posterior recibe un nuevo estado aceptado únicamente cuando supera el criterio contable y el gate aplicable.

## 12. GitHub Release

Desde REL.GOV.1, **todo tag formal nuevo** publicado después de esta política debe tener un GitHub Release asociado. Los tags históricos anteriores no se rellenan retroactivamente salvo decisión de auditoría explícita y basada en evidencia. Un estado aceptado que nunca tuvo tag no recibe un Release retroactivo por conveniencia: GitHub Release y tag formal se tratan como una unidad publicada.

### 12.1. Contrato de título

Para una beta revision-aware el título obligatorio es:

```text
Mi Retiro Proyectado v<VERSION> — GNNN/ENN
```

Ejemplo vigente:

```text
Mi Retiro Proyectado v0.1.09.01-beta — G109/E01
```

El título se obtiene con:

```powershell
python scripts\release_contract.py --print-title
```

La excepción histórica `v0.0.71.01-beta` conserva su tag original, pero sus metadatos de GitHub Release muestran **G087/E01** y explican que fue publicado originalmente como G071/E01.

### 12.2. Secciones obligatorias del cuerpo

Todo Release nuevo debe contener, en este orden lógico, las siguientes secciones:

1. `## Estado publicado`
2. `## Resumen`
3. `## Cambios principales`
4. `## Validación`
5. `## Evidencia`
6. `## Siguiente paso`

Dentro de **Estado publicado** se registran como mínimo versión, tag, G/E, commit objetivo y tipo de publicación. **Validación** debe conservar únicamente conteos realmente ejecutados. **Evidencia** debe identificar PR/merge, CI requerida y verificación del tag. **Siguiente paso** describe planificación, no una garantía de que el roadmap no pueda cambiar después.

La estructura de un archivo de notas puede validarse con:

```powershell
python scripts\release_contract.py --check-notes .\release-notes.md
```

### 12.3. Prerelease frente a release estable

- una versión terminada en `-beta` se publica con `--prerelease`;
- una versión oficial estable no se marca como prerelease;
- no se usa un Release beta como sustituto de una versión oficial;
- `Build` solo se incorpora cuando REL.1 defina el contrato reproducible correspondiente.

### 12.4. Creación controlada

REL.GOV.1 R2 mantiene la **creación y firma del tag como operación local del mantenedor**. GitHub Actions no crea ni firma tags.

Antes de la promoción se prepara `data/release-publication-manifest.json` con resumen, cambios, validación, evidencia y siguiente paso sustentados. El manifiesto debe corresponder a `VERSION`, al bloque/ordinal aceptado del ledger y al siguiente candidato real. Su contrato se valida con:

```powershell
python scripts\release_publication.py --check-manifest
```

Después de integrar, revalidar `main`, crear el tag anotado/firmado y ejecutar `git push origin "v$version"`, el workflow `.github/workflows/verificar-tags.yml` aplica dos fronteras de permisos:

1. **Verificar tag publicado** usa `contents: read` y valida firma SSH, `VERSION`, ledger, tag, commit objetivo y pertenencia al historial de `main`.
2. **Publicar GitHub Release** depende del job anterior y es el único que recibe `contents: write`.

El segundo job deriva del tag el commit publicado y el objeto de tag, renderiza las notas canónicas mediante `scripts/release_publication.py` y aplica semántica idempotente:

- solo un **HTTP 404** de la API de GitHub autoriza interpretar que el Release no existe y crearlo con `gh release create --verify-tag`;
- si existe (HTTP 200) y coincide exactamente en tag, título, draft/prerelease y cuerpo, termina en `OK` sin modificarlo;
- si existe pero difiere del contrato, falla cerrado y no lo reescribe automáticamente;
- errores de autenticación, permisos, rate limit, servidor, red o cualquier estado distinto de 200/404 fallan cerrado y **no** se reinterpretan como ausencia del Release.

Las versiones `-beta` se publican como prerelease; una versión estable omite esa marca. `.github/release.yml` continúa disponible para categorización asistida, pero no sustituye el manifiesto ni las notas auditables.

El flujo automático **no crea commits post-publicación** ni modifica `main` para cambiar frases temporales. La documentación viva evita declarar estados efímeros como “tag pendiente”; la evidencia primaria de publicación reside en Git/tag firmado, GitHub Release y el workflow correspondiente. Un operador puede usar `gh release create` manualmente solo como recuperación controlada si la automatización no está disponible, respetando exactamente el mismo contrato.

### 12.5. Edición y reconciliación posterior

Los metadatos de un GitHub Release pueden corregirse cuando haya errores de formato, redacción o una reconciliación histórica posterior. En ese caso:

- se usa `gh release edit`;
- **no** se mueve, elimina ni recrea el tag;
- no se cambia el commit objetivo del tag;
- una corrección semántica histórica debe indicar la denominación original y la reconciliada;
- los conteos de pruebas originales se conservan como evidencia histórica y no se sustituyen por los actuales;
- una edición puramente descriptiva del objeto GitHub Release no consume por sí sola un nuevo Global;
- si la corrección requiere cambios versionados en política, workflow, scripts, pruebas o documentación viva, esos cambios siguen la contabilidad revision-aware ordinaria.

### 12.6. Artefactos, privacidad y terceros

Si una futura GitHub Release incluye un instalador, ejecutable autocontenido, contenedor, ZIP o artefacto que incorpore físicamente dependencias de terceros, el Release debe incluir hashes reproducibles cuando correspondan y los textos de licencia, avisos y NOTICE aplicables al contenido realmente distribuido.

Nunca se adjuntan PDFs personales, logs con datos sensibles, secretos, `.env`, tokens, volcados de sesión ni archivos diagnósticos sin sanitizar.

## 13. Evidencia de cierre

Registrar como mínimo:

- identificador de versión;
- `G` y `EE` cuando aplique;
- SHA de rama y SHA integrado;
- PR;
- resultado de pruebas locales;
- CI requerida;
- tag y objeto tag si se publica;
- fecha;
- limitaciones relevantes;
- licencia del proyecto;
- inventario/avisos de terceros cuando el artefacto los incorpore;
- Build y hashes cuando exista un artefacto oficial.

`RELEASES.md` registra los hitos publicados; el ledger registra la secuencia de estados aceptados; Git/GitHub son la evidencia primaria.

## 14. Fallo durante el cierre

Si falla una validación:

- no consumir un nuevo `G`;
- no crear tag;
- corregir el mismo candidato;
- repetir validación;
- no alterar evidencia previa ya publicada.

Si un problema se descubre después de publicar un tag, no se reescribe ese tag. La corrección posterior se procesa como un nuevo candidato.

<!-- ANCLAS_HISTORICAS_VER2_PROCESO_CONSOLIDADAS -->

## Compatibilidad histórica preservada por VER.2

- El cierre formal usa tag anotado y firmado cuando corresponde publicar un hito.
- La política de tags conserva la inmutabilidad de `v0.0.25-beta` y `v0.0.26-beta`.
- Todo release con artefacto distribuible debe conservar inventario exacto del artefacto, avisos de terceros y correspondencia entre versión, Build, tag, hashes y contenido publicado.
- Los releases con artefactos distribuibles deben revisar licencias/NOTICE upstream antes de publicar.

## Reconciliación revision-aware antes de la próxima promoción

Antes de promover el siguiente candidato debe validarse que el ledger vivo
contenga G001–G110, que G111 sea el siguiente Global y que el snapshot histórico
G070 conserve su SHA-256. `v0.0.71.01-beta` no se mueve para corregir su
numeración histórica. REL.GOV.1 quedó aceptado como G110/E01 mediante PR #85 y merge `5cd1cea`.
La promoción post-merge no consume G111; DOC.2 continúa con G111/E01 (`0.1.11.01-beta`).

## Backfill histórico completado el 2026-08-26

REL.GOV.1 se aplicó también a los tags formales históricos ya existentes:

- inventario confirmado: **29 tags formales reales**;
- inventario final: **29 GitHub Releases**;
- `v0.0.1-beta`–`v0.0.26-beta` recibieron Releases retrospectivos administrativos;
- no se crearon tags nuevos para cubrir huecos inexistentes;
- la fecha del GitHub Release retrospectivo no sustituye la fecha histórica del hito ni del tag;
- ningún tag fue movido, borrado o recreado;
- el backfill de metadata no consume un Global.

La regla futura permanece: un nuevo tag formal debe publicarse con su GitHub Release conforme al contrato de esta guía.

## Replanificación operativa PLAN.2 R1

Después de publicar `v0.1.13.03-beta` (G113/E03), G114/E01
`0.1.14.01-beta` quedó reservado para PLAN.2 R1. Durante aquel candidato,
`VERSION` permaneció en `0.1.13.03-beta`. PLAN.2 R1 fue aceptado posteriormente
y su promoción formal publicó G114/E01.

La automatización práctica de publicación mediante GitHub CLI se evaluará en
REL.GOV.1 R2. El tag continúa creándose y verificándose localmente con firma
del mantenedor; la creación del GitHub Release debe ser reproducible mediante
comandos y un archivo de notas cuando la herramienta esté disponible.

La matriz viva de trabajo pendiente está en
`docs/governance/pre-1-0-pending-matrix.md`.

## Promoción G114/E01 — PLAN.2 R1

PLAN.2 R1 fue integrado mediante PR #94 / merge `7ded70c` y revalidado con
1103 pruebas, 148 Markdown y los checks remotos requeridos en `success`.

La promoción PR #95 / merge `5c6d2db` materializó `0.1.14.01-beta`
como G114/E01 después de la revalidación post-merge. El tag anotado y firmado
`v0.1.14.01-beta` fue creado sobre ese commit, verificado localmente y por
GitHub, y publicado junto con su GitHub Release prerelease. El workflow
`Git Tag Signature Verification` terminó en `success`; `v0.1.13.03-beta`
permanece preservado como publicación anterior.

El siguiente candidato queda reservado como DOC.1 R4:
G115/E04 (`0.1.15.04-beta`).
