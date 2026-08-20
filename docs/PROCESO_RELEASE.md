# Proceso de release

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.26-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Base documental:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal:** PLAN.1 R2B1 — versionado oficial futuro y Build — 2026-08-20
**Clasificación:** Gobierno / Release / Auditoría

Este procedimiento complementa `VERSIONING.md`, `RELEASES.md`, `CHANGELOG.md`, `GOVERNANCE.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `docs/LICENCIA_Y_DISTRIBUCION.md` y `docs/PLAN_MAESTRO_HACIA_1_0.md`.

## 1. Principio

Un tag formal identifica un estado **cerrado, reproducible y validado**. No se etiqueta un árbol que todavía está pendiente de validación.

Durante la etapa beta, la versión usa `0.0.N-beta`. La primera versión oficial objetivo usa cuatro componentes y se prevé inicialmente como `1.0.0.0`.

El identificador `Build` es independiente de `VERSION`. No se inventa ni se incrementa por commit; se materializa cuando REL.1 disponga de un proceso reproducible de generación de artefactos oficiales.

## 2. Precondiciones

Antes del cierre:

- hito funcional/técnico/documental terminado;
- código, pruebas y documentación coherentes;
- working tree controlado;
- versión anterior trazable;
- limitaciones conocidas actualizadas;
- licencia del proyecto coherente con el objetivo de distribución;
- `THIRD_PARTY_NOTICES.md` revisado si el artefacto incluye componentes de terceros.

## 3. Validación del hito antes del incremento

Ejecutar, como mínimo:

```powershell
git diff --check
python -m compileall app

Get-ChildItem .\app\static\js\*.js | ForEach-Object {
    node --check $_.FullName
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

python -m unittest discover -s tests -q
```

No se registra como “validado” un conteo que no se haya ejecutado realmente.

## 4. Preparación de la nueva versión

Cuando el hito está técnicamente validado:

1. asignar el número según `VERSIONING.md`;
2. actualizar `VERSION`;
3. actualizar metadata de documentos vigentes que declaran versión revisada;
4. mover cambios notables de `Unreleased` o registrar cierre en `CHANGELOG.md`;
5. actualizar `RELEASES.md`;
6. actualizar `ROADMAP.md`;
7. actualizar tests de coherencia si el contrato evolucionó, sin fijar innecesariamente versiones históricas como estado eterno;
8. revisar `LICENSE` y `docs/LICENCIA_Y_DISTRIBUCION.md`;
9. si se empaquetan dependencias, generar el inventario exacto del artefacto y adjuntar licencias/NOTICE upstream exigidos;
10. si se trata de un artefacto oficial, asignar el Build de acuerdo con el mecanismo canónico que se establecerá en REL.1.

## 5. Validación del candidato de release

Después del incremento:

- repetir suite completa;
- repetir `git diff --check`;
- comprobar FastAPI/footer/README contra `VERSION`;
- comprobar changelog/releases;
- revisar que no existan logs, PDFs personales o secretos preparados para commit;
- comprobar que el artefacto no omita avisos/licencias de terceros que distribuya;
- confirmar que ningún componente de tercero se presente como cubierto por `LICENSE` del proyecto;
- para artefactos oficiales, comprobar correspondencia entre versión, Build, hashes y contenido reproducible.

## 6. Commit de cierre

El cierre de versión debe quedar en uno o más commits lógicos **firmados**.

```powershell
git verify-commit HEAD
git log --show-signature -1
git status
```

El árbol debe quedar limpio y la firma debe verificarse.

## 7. Pull Request, integración y CI remota

`main` está protegida y no recibe pushes directos ordinarios.

Publicar la rama de trabajo:

```powershell
git push -u origin <rama>
```

Abrir un Pull Request hacia `main` y confirmar:

- commits de la rama firmados y verificados;
- checks requeridos `Python 3.13` y `Python 3.14` en **success**;
- check `Auditoría de gobernanza` en **success**;
- rama actualizada respecto de `main`;
- conversaciones resueltas;
- ausencia de cambios no relacionados.

La integración ordinaria se realiza mediante `Squash and merge`. El commit resultante en `main` debe aparecer como `Verified` en GitHub.

Después de integrar:

```powershell
git switch main
git fetch origin --prune
git pull --ff-only origin main
```

Confirmar `HEAD == origin/main`, working tree limpio y una ejecución de CI sobre el nuevo SHA de `main` en **success**.

## 8. Tag formal

Solo después de confirmar CI remota verde se crea el **tag anotado y firmado**.

La etiqueta se deriva exactamente de `VERSION`:

```powershell
$version = (Get-Content .\VERSION).Trim()
git tag -s "v$version" -m "Mi Retiro Proyectado v$version"
git tag -v "v$version"
git push origin "v$version"
```

Ejemplos válidos según la etapa:

```text
v0.0.25-beta
v0.0.26-beta
v1.0.0.0
v1.0.0.1
```

El tag debe apuntar al commit validado y usar una clave de `.github/allowed_signers`.

`.github/workflows/verificar-tags.yml` permite verificar tags futuros y auditar manualmente toda la colección.

## 9. Build oficial

`Build` no forma parte de `VERSION` ni del tag.

Para la primera versión oficial prevista:

```text
Versión 1.0.0.0
Build 000001
Tag v1.0.0.0
```

REL.1 definirá la fuente canónica del Build, su incremento monotónico, el empaquetado reproducible y la asociación inequívoca entre Build, commit, tag, hashes y artefactos.

Hasta entonces no se publica un Build ficticio.

## 10. Inmutabilidad

Después de la migración criptográfica del 2026-08-17, un tag publicado:

- no se mueve;
- no se reutiliza;
- no se elimina para ocultar historia;
- no se fuerza para ocultar una corrección posterior.

La única excepción histórica fue la reemisión firmada de `v0.0.22-beta` y `v0.0.23-beta`, ejecutada el 2026-08-17 preservando sus commits objetivo y documentando los objetos originales. Esa excepción no puede repetirse.

Una corrección posterior recibe un nuevo commit y, si corresponde, nueva versión.

## 11. GitHub Release

Durante la etapa beta puede existir únicamente un tag formal si el hito no distribuye un artefacto.

Antes de la primera versión oficial se decidirá qué tags requieren GitHub Release, notas y artefactos.

La planificación anterior hablaba de decidirlo «antes de beta pública»; esa expresión se conserva como contexto histórico, pero el gate vigente es REL.1 antes de `1.0.0.0`.

Si una futura GitHub Release incluye un instalador, ejecutable autocontenido, contenedor, ZIP o artefacto que incorpore físicamente dependencias de terceros, el release debe incluir los textos de licencia, avisos y NOTICE que correspondan al contenido realmente distribuido.

## 12. Evidencia de cierre

Registrar:

- versión;
- SHA;
- tag;
- fecha;
- resultado de pruebas;
- CI;
- limitaciones relevantes;
- licencia del proyecto;
- inventario/avisos de terceros cuando el artefacto los incorpore;
- Build y hashes cuando exista un artefacto oficial.

`RELEASES.md` es el registro documental; Git/GitHub son la evidencia primaria.

## 13. Fallo durante el cierre

Si falla una validación:

- no crear tag;
- corregir;
- repetir validación;
- no alterar evidencia previa ya publicada.

Si un problema se descubre después de publicar un tag, no se reescribe ese tag.
