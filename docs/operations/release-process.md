# Proceso de release

**Estado:** Vigente
**Versión de aplicación:** `0.1.10.01-beta` — REL.GOV.1 R1 / G110-E01 promovida post-merge
**Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
**Último tag formal legacy:** `v0.0.26-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Base documental:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal:** REL.GOV.1 — gobierno de GitHub Releases — 2026-08-26
**Clasificación:** Gobierno / Release / Auditoría


<!-- DOC1-R1-POST-MANT1:START -->
## Estado post-MANT.1

El cierre de MANT.1 R7 no constituye release formal ni cambia la versión canónica.

Para una release posterior se mantiene el criterio vigente:

- `VERSION` debe ser la fuente única.
- `0.1.10.01-beta` es la versión canónica vigente y materializa G110/E01; G109/E01 permanece publicado e inmutable.
- `v0.0.71.01-beta` fue publicado originalmente bajo la denominación VER.2 G071/E01; la reconciliación post-G070 sitúa ese estado cronológicamente en **G087/E01** sin mover el tag.
- `v0.0.26-beta` permanece como tag legacy histórico e inmutable.
- VER.2, MANT.1, DOC.1 R1, NOR.1 y NOR.2 están cerrados.
- DOC.1 R2 está cerrado como auditoría Markdown posterior a NOR.2 y no crea por sí solo una release.
- SEC.2 quedó cerrado después de R1–R6. AUD.SEC2 R1 fue aceptado mediante PR #83 como G109/E01 y `v0.1.09.01-beta` quedó publicado. REL.GOV.1 quedó aceptado mediante PR #85 como G110/E01 (`0.1.10.01-beta`); DOC.2 continúa con G111/E01 (`0.1.11.01-beta`).

Todo release futuro requiere gate completo, PR/CI, actualización documental coherente, tag y evidencia reproducible.
<!-- DOC1-R1-POST-MANT1:END -->

Este procedimiento complementa `VERSIONING.md`, `RELEASES.md`, `CHANGELOG.md`, `GOVERNANCE.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `docs/governance/licensing-and-distribution.md`, `docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md`, `docs/governance/pre-1-0-revision-ledger.md`, `docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md`, `data/pre-1-0-revision-ledger.json` y `docs/governance/master-plan-to-1-0.md`.

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
- checks requeridos `Python 3.13` y `Python 3.14` en **success**;
- check `Auditoría de gobernanza` en **success**;
- conversaciones resueltas;
- ausencia de cambios no relacionados;
- evidencia local requerida disponible.

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

El tag debe apuntar al commit validado y usar una clave autorizada por la política vigente. `.github/workflows/verificar-tags.yml` permite verificar tags futuros y auditar la colección.

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

El tag debe existir, estar firmado, publicado y apuntar al SHA validado **antes** de crear el Release. El flujo recomendado es:

```powershell
$version = (Get-Content .\VERSION).Trim()
$title = python scripts\release_contract.py --print-title
python scripts\release_contract.py --check-tag "v$version"
python scripts\release_contract.py --check-notes .\release-notes.md

gh release create "v$version" `
  --repo recm0708/mi-retiro-proyectado `
  --title "$title" `
  --prerelease `
  --verify-tag `
  --notes-file .\release-notes.md
```

Para una versión estable se omite `--prerelease`. `.github/release.yml` configura la categorización de **Generate release notes**, pero no sustituye estas secciones ni la evidencia manual obligatoria.

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
