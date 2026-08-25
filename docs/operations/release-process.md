# Proceso de release

**Estado:** Vigente
**Versión de aplicación:** `0.0.71.01-beta` — VER.2 G071/E01 promovida en R4
**Último estado aceptado antes de VER.2:** G070/E02 — cierre UX.4.6i
**Último tag formal legacy:** `v0.0.26-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Base documental:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal:** VER.2 — versionado revision-aware — 2026-08-22
**Clasificación:** Gobierno / Release / Auditoría


<!-- DOC1-R1-POST-MANT1:START -->
## Estado post-MANT.1

El cierre de MANT.1 R7 no constituye release formal ni cambia la versión canónica.

Para una release posterior se mantiene el criterio vigente:

- `VERSION` debe ser la fuente única.
- `0.0.71.01-beta` queda promovido en `VERSION` durante R4, pero no debe tratarse como tag publicado mientras no exista cierre formal post-merge.
- El último tag formal vigente sigue siendo `v0.0.26-beta` hasta crear y verificar `v0.0.71.01-beta`.
- MANT.1 se considera cerrado como mantenimiento técnico/documental.
- DOC.1 R1 actualiza documentación Markdown, pero no habilita por sí solo una release.

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
- comprobar que `0.0.71.01-beta` siga identificado como candidato reservado mientras VER.2 no esté integrado;
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
v0.0.71.01-beta    # candidato VER.2, solo si corresponde etiquetarlo tras cierre
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

Durante la etapa beta puede existir únicamente un tag formal si el hito no distribuye un artefacto.

Antes de la primera versión oficial se decidirá qué tags requieren GitHub Release, notas y artefactos.

Si una futura GitHub Release incluye un instalador, ejecutable autocontenido, contenedor, ZIP o artefacto que incorpore físicamente dependencias de terceros, el release debe incluir los textos de licencia, avisos y NOTICE que correspondan al contenido realmente distribuido.

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
