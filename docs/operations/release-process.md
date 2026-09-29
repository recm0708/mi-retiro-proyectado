# Proceso de release

**Estado:** vigente
**Clasificación:** gobierno / publicación

## Propósito

Este documento define cómo un estado aceptado de Mi Retiro Proyectado pasa de
candidato versionado a estado integrado, tag firmado y GitHub Release.

La numeración se rige por [Política de versionado](../../VERSIONING.md). Este
procedimiento no mantiene una cronología de promociones: esa historia pertenece
a [Releases](../../RELEASES.md), Git, tags y GitHub Releases.

## Principios

- Un tag formal identifica un estado integrado y revalidado.
- Un candidato no se presenta como publicación antes de que exista el tag.
- Una fase planificada no recibe Global o `VERSION` por anticipado.
- El número candidato solo se materializa cuando existe un estado real que puede
  someterse al gate revision-aware.
- Un fallo previo a aceptación se corrige dentro del mismo candidato y no
  consume otro Global.
- Tags y Releases publicados no se mueven para ocultar cambios posteriores.
- GitHub Actions puede verificar y publicar metadata, pero no crea ni firma el
  tag del mantenedor.

## Autoridades

El cierre debe mantener coherentes:

- [`VERSION`](../../VERSION);
- [ledger Markdown](../governance/pre-1-0-revision-ledger.md);
- [ledger JSON](../../data/governance/pre-1-0-revision-ledger.json);
- [registro de bloques](../../data/governance/work-block-registry.json);
- [manifest de publicación](../../data/governance/release-publication-manifest.json);
- [Changelog](../../CHANGELOG.md);
- [Releases](../../RELEASES.md);
- documentación afectada por el cambio.

El ledger registra la secuencia de estados aceptados. El manifest es una entrada
estructurada para la publicación del estado materializado; no es un segundo
ledger ni un roadmap.

## Qué constituye un estado aceptable

Un mantenimiento técnico, cambio funcional, seguridad, dependencia, gobierno o
documentación puede producir una nueva beta cuando crea una configuración
materialmente distinta y auditable.

No crean otro estado por sí solos:

- commits separados de una misma revisión;
- checkpoints;
- un intento que todavía no supera gates;
- PR, squash, CI o tag que solo materializan el mismo estado;
- revalidaciones sin cambio material;
- trabajo meramente planificado.

La decisión contable se toma conforme a `VERSIONING.md` y al ledger.

## Precondiciones

Antes de materializar un candidato:

1. la fase tiene Issue propietaria y alcance aprobado;
2. sus dependencias de entrada están satisfechas;
3. el preflight transversal aplicable está vigente;
4. el último estado publicado/aceptado es trazable;
5. el siguiente Global aritmético no está reservado por planificación;
6. el árbol de trabajo no contiene cambios ajenos;
7. los riesgos y validaciones de la fase están definidos.

Una fase recién abierta puede trabajar sin tocar `VERSION` hasta que exista un
candidato material suficientemente completo para aplicar el contrato
revision-aware.

## Validación previa a la materialización

Como mínimo, y ampliando según el alcance:

```powershell
python -m pip check
git diff --check
python -m compileall app
python -m unittest discover -s tests -q
```

Para JavaScript modificado:

```powershell
Get-ChildItem .\app\static\js\*.js | ForEach-Object {
    node --check $_.FullName
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
```

Cuando el cambio es visual, interactivo, normativo, de seguridad o de
persistencia se añaden las validaciones específicas correspondientes.

Un conteo o resultado no se documenta como ejecutado si no existe evidencia de
su ejecución real.

## Materialización del candidato

Cuando el estado tiene contenido material verificable:

1. confirmar el último Global aceptado;
2. determinar Global/Edition/Correction según `VERSIONING.md`;
3. actualizar `VERSION` al identificador candidato;
4. registrar el candidato en ledger/registry/manifest según sus contratos;
5. actualizar únicamente documentación viva realmente afectada;
6. mantener cambios notables bajo `[Unreleased]` mientras no exista
   publicación;
7. ejecutar validadores estructurados;
8. comprobar que no se preasigna el Global posterior.

La materialización permite validar un identificador concreto, pero **no equivale
a integración ni publicación**.

## Manifest de publicación

`data/governance/release-publication-manifest.json` es el input
machine-readable del flujo de Release.

Debe declarar:

- versión y estado revision-aware que se está publicando;
- bloque/revisión;
- resumen;
- cambios principales;
- validación ejecutada;
- evidencia;
- siguiente Global aritmético y, solo si existe realmente, el siguiente
  candidato material.

### Snapshot y resolución runtime

El manifest usa:

- `snapshot_role = "release-input"`;
- `publication_resolution = "runtime"`.

Eso significa que commit publicado, objeto de tag y tipo de Release se resuelven
cuando el workflow procesa el tag, no se congelan como hechos futuros dentro del
manifest.

Campos como `publication_state`, `published_commit`, `tag_object`,
`release_id` o `published_at` no se escriben manualmente en el snapshot de
entrada.

### Regla de `next_step`

`next_step` describe **lo que viene después del estado que se está
publicando**.

Por tanto, su `description`:

- puede indicar que el siguiente Global continúa libre;
- puede describir una fase siguiente ya aprobada;
- puede declarar dependencias posteriores a la publicación;
- **no debe afirmar que el propio estado del manifest sigue pendiente de
  integración/publicación**, porque las notas se renderizan cuando el tag ya
  representa un estado publicado;
- no debe preasignar versión/bloque al siguiente Global cuando todavía no existe
  candidato material.

Esta regla evita que una nota generada correctamente bajo `## Estado publicado`
termine contradiciéndose en `## Siguiente paso`.

El contrato del manifest se valida con:

```powershell
python scripts/release_publication.py --check-manifest
```

## Validación del candidato

Después de materializar `VERSION`:

- ejecutar el Quality Gate completo;
- comprobar `VERSION`, aplicación y superficies que lo consumen;
- validar continuidad y unicidad del ledger;
- validar registry/manifest;
- ejecutar `python scripts/release_contract.py` según el modo aplicable;
- revisar README/roadmap/gobierno solo cuando realmente describan ese estado;
- comprobar que el candidato no se presenta como tag/Release ya publicado;
- revisar terceros/licencias si cambia el contenido distribuible;
- verificar que no se hayan preparado para commit secretos, datos personales,
  dumps o artefactos locales.

## Commit canónico

El estado final de la rama canónica se confirma con commit firmado por el
mantenedor.

```powershell
git verify-commit HEAD
git log --show-signature -1
git status
```

Los commits temporales de un workspace asistido no sustituyen el commit
canónico firmado ni se integran directamente a `main`.

## Pull Request e integración

`main` no recibe pushes directos ordinarios.

El Pull Request canónico debe:

- enlazar las Issues propietarias;
- declarar alcance y exclusiones;
- estar actualizado respecto de `main`;
- superar `Repository Quality Gate`;
- superar `Python Compatibility`;
- superar controles adicionales que apliquen;
- tener conversaciones resueltas;
- mantener fuera cambios no relacionados.

La integración ordinaria usa `Squash and merge`.

Después del merge:

```powershell
git switch main
git fetch origin --prune
git pull --ff-only origin main
git status
```

Se confirma que `HEAD == origin/main` y se revalida el SHA integrado antes de
crear el tag.

## Tag formal

El tag se deriva exactamente de `VERSION` y se crea **después** de integrar y
revalidar:

```powershell
$version = (Get-Content .\VERSION).Trim()
git tag -s "v$version" -m "Mi Retiro Proyectado v$version"
git tag -v "v$version"
git push origin "v$version"
```

Reglas:

- el tag apunta al commit integrado validado;
- usa una clave autorizada;
- todo tag nuevo debe verificarse antes de declarar publicación;
- un tag publicado no se mueve, reutiliza ni elimina para esconder una
  corrección posterior;
- una corrección posterior sigue el modelo revision-aware y recibe su propio
  estado cuando corresponde.

No se crean tags revision-aware retrospectivos únicamente para rellenar huecos
históricos del ledger.

## Verificación remota del tag

`.github/workflows/verificar-tags.yml` aplica dos fronteras:

1. **verificación**, con permisos de lectura, para firma, `VERSION`, ledger,
   tag, commit objetivo y pertenencia al historial de `main`;
2. **publicación del GitHub Release**, que solo se ejecuta después de superar la
   verificación y es la única parte que requiere escritura sobre Releases.

El workflow no sustituye la creación/firma local del tag.

## GitHub Release

Todo tag formal nuevo gobernado por este proceso debe tener un GitHub Release
coherente.

### Título

Para una beta revision-aware:

```text
Mi Retiro Proyectado v<VERSION> — GNNN/ENN
```

El título canónico puede obtenerse mediante:

```powershell
python scripts\release_contract.py --print-title
```

### Cuerpo

Las notas contienen, en orden lógico:

1. `## Estado publicado`;
2. `## Resumen`;
3. `## Cambios principales`;
4. `## Validación`;
5. `## Evidencia`;
6. `## Siguiente paso`.

`Estado publicado` incluye versión, tag, G/E, bloque, commit publicado, objeto
de tag y tipo de Release. Esos valores de publicación se resuelven contra el tag
real.

`Validación` conserva únicamente verificaciones realmente ejecutadas.

`Siguiente paso` describe futuro posterior a la publicación y respeta la regla
de no preasignación.

### Prerelease y estable

- una versión terminada en `-beta` se publica como prerelease;
- una versión oficial estable no se marca como prerelease;
- una beta no sustituye una versión oficial;
- Build solo aparece cuando exista el contrato reproducible de REL.1.

## Publicación idempotente

El workflow resuelve el tag, renderiza las notas mediante
`scripts/release_publication.py` y aplica un comportamiento cerrado:

- HTTP 404 permite crear un Release inexistente;
- HTTP 200 exige coincidencia exacta del Release existente;
- una diferencia de contrato provoca fallo en vez de reescritura automática;
- errores de autenticación, permisos, red, rate limit o servidor no se
  interpretan como “Release inexistente”.

La automatización no crea commits post-publicación para reescribir el snapshot
que produjo el tag.

## Corrección de metadata de un Release

Una edición descriptiva de un GitHub Release puede realizarse cuando exista una
razón explícita de formato o reconciliación, siempre que:

- no se mueva, elimine ni recree el tag;
- no cambie el commit objetivo del tag;
- no se sustituyan conteos históricos por resultados actuales;
- una reconciliación semántica conserve la denominación/contexto original
  necesario;
- la edición tenga trazabilidad en una Issue o auditoría apropiada.

Una edición de metadata, por sí sola, no consume Global. Si la corrección exige
cambios en scripts, workflows, tests o contratos versionados, esos cambios sí
siguen el ciclo revision-aware ordinario.

## Artefactos, privacidad y terceros

Si un Release distribuye instaladores, ejecutables, contenedores, ZIP u otros
artefactos que incorporen terceros, debe conservar:

- inventario exacto;
- hashes reproducibles cuando correspondan;
- licencias, avisos y NOTICE requeridos;
- correspondencia entre versión, Build, tag y contenido.

Nunca se adjuntan datos personales, PDFs previsionales, logs sensibles,
`.env`, tokens, secretos, cookies o dumps de sesión.

## Build oficial

Build es independiente de `VERSION` y del tag.

REL.1 definirá:

- fuente canónica;
- incremento monotónico;
- empaquetado reproducible;
- asociación entre Build, commit, tag, hashes y artefactos.

Hasta entonces no se publica un Build ficticio.

## Evidencia de cierre

Registrar como mínimo:

- versión;
- Global/Edition/Correction cuando aplique;
- SHA candidato y SHA integrado;
- Pull Request;
- validaciones locales;
- checks remotos;
- tag y objeto de tag;
- GitHub Release;
- limitaciones relevantes;
- inventario/licencias de terceros cuando correspondan;
- Build y hashes cuando existan artefactos oficiales.

`RELEASES.md` resume hitos publicados; el ledger conserva estados aceptados;
Git y GitHub son la evidencia primaria.

## Fallo durante el cierre

Si falla una validación antes de aceptación:

- no consumir otro Global;
- no crear tag;
- corregir el candidato;
- repetir el gate;
- no alterar evidencia previa publicada.

Si un defecto material se descubre después de publicar, no se reescribe el tag.
La corrección se procesa conforme al modelo revision-aware vigente.

## Compatibilidad histórica

Las familias legacy y revision-aware v1 ya publicadas permanecen inmutables.
Releases, auditorías y tags anteriores pueden conservar convenciones que eran
válidas en su momento.

La política prospectiva se aplica a nuevas publicaciones; no se moderniza la
historia únicamente para que su redacción coincida con el procedimiento actual.
