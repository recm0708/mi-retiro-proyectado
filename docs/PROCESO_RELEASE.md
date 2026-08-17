# Proceso de release

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R4 — 2026-08-17
**Clasificación:** Gobierno / Release / Auditoría

Este procedimiento complementa `VERSIONING.md`, `RELEASES.md`, `CHANGELOG.md` y `GOVERNANCE.md`.

## 1. Principio

Un tag formal identifica un estado **cerrado, reproducible y validado**. No se etiqueta un árbol que todavía está pendiente de validación.

## 2. Precondiciones

Antes del cierre:

- hito funcional/técnico/documental terminado;
- código, pruebas y documentación coherentes;
- working tree controlado;
- versión anterior trazable;
- limitaciones conocidas actualizadas.

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
4. mover cambios notables de `Unreleased`/registrar cierre en `CHANGELOG.md`;
5. actualizar `RELEASES.md`;
6. actualizar `ROADMAP.md`;
7. actualizar tests de coherencia si el contrato evolucionó, sin fijar innecesariamente versiones históricas como estado eterno.

## 5. Validación del candidato de release

Después del incremento:

- repetir suite completa;
- repetir `git diff --check`;
- comprobar FastAPI/footer/README contra `VERSION`;
- comprobar changelog/releases;
- revisar que no existan logs, PDFs personales o secretos preparados para commit.

## 6. Commit de cierre

El cierre de versión debe quedar en uno o más commits lógicos **firmados**.

```powershell
git verify-commit HEAD
git log --show-signature -1
git status
```

El árbol debe quedar limpio y la firma debe verificarse.

## 7. Push y CI remota

Publicar el commit de cierre:

```powershell
git push origin main
```

Confirmar:

- `HEAD == origin/main`;
- GitHub Actions sobre el SHA de cierre;
- CI remota en **success**.

## 8. Tag formal

Solo después de confirmar CI remota verde se crea el **tag anotado y firmado**:

```powershell
git tag -s vX.Y.Z -m "Mi Retiro Proyectado vX.Y.Z"
git tag -v vX.Y.Z
git push origin vX.Y.Z
```

El tag debe apuntar al commit validado y usar una clave de `.github/allowed_signers`.

`.github/workflows/verificar-tags.yml` permite verificar tags futuros y auditar manualmente toda la colección.

## 9. Inmutabilidad

Después de la migración criptográfica del 2026-08-17, un tag publicado:

- no se mueve;
- no se reutiliza;
- no se elimina para ocultar historia;
- no se fuerza para ocultar una corrección posterior.

La única excepción histórica fue la reemisión firmada de `v0.0.22-beta` y `v0.0.23-beta`, ejecutada el 2026-08-17 preservando sus commits objetivo y documentando los objetos originales. Esa excepción no puede repetirse.

Una corrección posterior recibe un nuevo commit y, si corresponde, nueva versión.

## 10. GitHub Release

Durante la etapa interna puede existir únicamente tag formal.

Antes de beta pública se decidirá si cada tag publicable tendrá GitHub Release, notas y artefactos.

## 11. Evidencia de cierre

Registrar:

- versión;
- SHA;
- tag;
- fecha;
- resultado de pruebas;
- CI;
- limitaciones relevantes.

`RELEASES.md` es el registro documental; Git/GitHub son la evidencia primaria.

## 12. Fallo durante el cierre

Si falla una validación:

- no crear tag;
- corregir;
- repetir validación;
- no alterar evidencia previa ya publicada.

Si un problema se descubre después de publicar un tag, no se reescribe ese tag.
