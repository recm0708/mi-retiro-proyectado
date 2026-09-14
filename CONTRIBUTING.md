# Guía de contribución


<!-- NOR3-G122-PROMOTION:START -->
## Estado post-NOR.3 / promoción G122-E01

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
## Secuencia intermedia obligatoria post-NOR.3

G123/MANT.2 R1 está publicado como `v0.1.23.01-beta` y permanece preservado
como el estado material inmediatamente anterior.

MANT.1 R8 / Issue #163 se materializa como **G124/E13**
(`0.1.24.13-beta`). El ordinal E13 continúa la historia propia de MANT.1:
G074–G085 ya ocupan E01–E12; la revisión funcional vigente es R8.

La aceptación local se sustenta en la auditoría de 16 scripts operativos y
219 módulos de pruebas pre-promoción, la reconciliación de 28 labels, el
Quality Gate FULL 11 PASS / 0 FAIL y el preflight final #166 sin trabajo
Dependabot pendiente. La publicación formal de G124 requiere todavía
PR/merge, revalidación de `main`, tag firmado y GitHub Release prerelease.

Después de publicar G124/MANT.1 R8 y antes de iniciar PERSIST.1, la continuidad
material queda fijada así:

1. **DOC.3 R1 — Issue #154:** auditoría documental integral.
2. **PLAN.2 R2 — Issue #155:** replanificación maestra hacia 1.0.
3. **VER.2 R6 — Issue #164:** reforma del versionado beta y del componente
   futuro dedicado a fases MANT.2/Dependabot.
4. **PERSIST.1 — Issue #130:** bloqueado hasta completar toda la secuencia.

G125 queda únicamente como siguiente Global disponible y no se asigna por
adelantado. Antes de iniciar cada fase futura se repite el preflight #166;
un lote material nuevo de dependencias inserta MANT.2 R2+.
<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:END -->

<!-- DOC1-R1-POST-MANT1:START -->
## Estado de contribución vigente

- `VERSION` está sincronizado en `0.1.22.01-beta` (G122/E01).
- `v0.1.21.01-beta` / G121/E01 permanece publicado como estado anterior.
- UX.6 R1–R8 permanece cerrado/publicado como G121/E01.
- NOR.3 R1–R8 queda integrado/aceptado como G122/E01 mediante PR #162
  / merge `b97cf61763479b80b8e8724b878089e8bb20fa00`.
- G123 queda disponible sin candidato ni bloque preasignado.
- PERSIST.1 permanece planificado, no iniciado y sin Global preasignado.
- UX.7/UX.8 permanecen planificados y no iniciados.
- Los cambios de seguridad deben conservar sus regresiones.
- Código, pruebas, documentación y evidencia deben permanecer sincronizados.
<!-- DOC1-R1-POST-MANT1:END -->

Este documento define el flujo mínimo para modificar Mi Retiro Proyectado sin perder trazabilidad técnica, normativa, documental o de pruebas.

La creación o edición de tags/GitHub Releases se rige adicionalmente por `docs/operations/release-process.md`. No se improvisan títulos ni cuerpos de Release; para estados revision-aware se usa `scripts/release_contract.py` como validador local.

## 1. Antes de comenzar

Si un cambio requiere nombrar una fase, bloque o checkpoint, validar `docs/standards/work-block-identifiers.md` y ejecutar `python scripts/audit_block_identifiers.py` antes de proponer el identificador.

Actualizar primero la rama predeterminada:

```powershell
git switch main
git fetch origin
git pull --ff-only origin main
```

Comprobar que la copia de trabajo esté limpia:

```powershell
git status
```

Crear una rama específica antes de modificar:

```powershell
git switch -c <tipo>/<descripcion>
```

El entorno de referencia, las herramientas obligatorias para los gates y las utilidades opcionales usadas durante el desarrollo se documentan en [Guía interna de desarrollo — Entorno y herramientas](docs/operations/development-guide.md#18-entorno-y-herramientas-de-desarrollo). Las versiones observadas allí describen el equipo de mantenimiento y no convierten editores o clientes gráficos en dependencias de ejecución.

No aplicar un paquete de cambios sobre modificaciones locales no revisadas.

Toda participación en issues, Pull Requests o revisiones debe respetar [Código de conducta](CODE_OF_CONDUCT.md). Para dudas de uso, reportes, privacidad o seguridad, consultar primero [Soporte](SUPPORT.md).

## 2. Principios obligatorios

- Las fórmulas previsionales principales viven en Python.
- JavaScript no debe duplicar motores legales.
- Los parámetros normativos modificables deben residir en `regulations/` o estar aislados y documentados.
- Datos acreditados y proyectados permanecen diferenciados.
- Pagos únicos y pensiones mensuales permanecen separados.
- Un dato oficial desconocido no se inventa.
- Toda interpretación normativa relevante debe ser trazable a una fuente y, cuando corresponda, a un ADR.
- Los documentos personales reales no se versionan.
- Código, pruebas y documentación se actualizan dentro de la misma unidad de trabajo.
- Comentarios y docstrings siguen [Estándar de código y comentarios](docs/standards/code-and-comments.md); explican intención y contratos, no la sintaxis obvia.

## 3. Fuente de versión

`VERSION` es la única fuente canónica de versión de aplicación.

No escribir versiones independientes en:

- `app/core/config.py`;
- plantillas;
- JavaScript;
- motores;
- documentación que pretenda definir una segunda fuente.

Consultar [Política de versionado](VERSIONING.md).

## 4. Flujo de cambios

Antes de editar:

```powershell
git status
git diff
```

Después de editar, revisar únicamente los archivos afectados y agruparlos por propósito. Evitar `git add .` como hábito cuando existan cambios heterogéneos.

Ejemplos de tipos de commit:

```text
feat(ux): describir cambio funcional
fix(data): corregir reconciliación
test(ux): agregar regresiones
docs(gov): actualizar documentación
chore(gov): ajustar configuración
refactor(core): reorganizar implementación
```

Los commits deben ser legibles de forma independiente y no deben ocultar cambios no relacionados.

`main` está protegida. El flujo ordinario es rama de trabajo → commit firmado → push de la rama → Pull Request → checks requeridos → `Squash and merge`. No se usa `git push origin main` como flujo normal.

Cuando `main` exige firmas verificadas, el PR que se integre mediante squash debe ser creado por el mantenedor que realizará esa integración, salvo recuperación administrativa excepcional documentada.

## 5. Validación mínima

El repositorio incluye un gate `pre-commit` versionado. Debe activarse **una sola vez por cada clon local**:

```powershell
.\scripts\configure_git_hooks.ps1
git config --local --get core.hooksPath
```

Con el hook activo, `git commit` se cancela automáticamente si se intenta confirmar directamente en `main`, si existen cambios rastreados sin preparar o archivos no rastreados, si falla `git diff --cached --check`, `pip check`, la compilación Python, la sintaxis JavaScript o cualquier prueba de la suite completa. El objetivo es que las pruebas se ejecuten contra el mismo árbol que se pretende confirmar.

`git commit --no-verify` no forma parte del flujo ordinario del proyecto y no debe usarse para eludir un gate fallido. Una excepción de recuperación requeriría justificación explícita y validación equivalente antes de publicar la rama.

Ejecutar además antes de cerrar un bloque:

```powershell
python -m compileall app

Get-ChildItem .\app\static\js\*.js | ForEach-Object {
    node --check $_.FullName
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

python -m unittest discover -s tests -q
git diff --check
```

Si el cambio modifica comportamiento visible, realizar además las pruebas manuales pertinentes en navegador.

Las pruebas automatizadas no sustituyen una auditoría WCAG con tecnologías de apoyo ni una revisión jurídica.

<!-- AUTOMATION-POST-G119:START -->
### Gate canónico y automatización post-G119

Las herramientas Python de desarrollo se instalan con
`python -m pip install -r requirements-dev.txt`.

El cierre técnico local usa como contrato canónico:

```powershell
python scripts/quality_gate.py --full
```

El hook conserva las barreras específicas del clon y delega el gate técnico en
`quality_gate.py --pre-commit`. En Pull Requests, `Repository Quality Gate`
añade política de rama, firmas humanas autorizadas e integridad del repositorio.

`VERSION`, `data/governance/pre-1-0-revision-ledger.json` y
`data/governance/release-publication-manifest.json` se consideran estado revision-aware
coordinado: un cambio de promoción debe tratarlos de forma coherente.

El tooling npm versionado bajo `scripts/package.json` y
`scripts/package-lock.json` existe exclusivamente para automatización visual y
de accesibilidad; no forma parte del runtime de la aplicación.

La automatización verifica, pero no crea commits o tags firmados ni autoriza
auto-merge. Esas decisiones permanecen bajo control del mantenedor.
<!-- AUTOMATION-POST-G119:END -->

## 6. Documentación como parte del cambio

Actualizar únicamente los documentos afectados, pero hacerlo **antes del cierre** del cambio.

Mapa general:

- `README.md` — presentación y estado general;
- `CHANGELOG.md` — cambios notables por versión;
- `RELEASES.md` — releases, tags y reconstrucción de versiones;
- `docs/README.md` — mapa documental;
- `docs/governance/roadmap.md` — presente y futuro;
- `docs/governance/pre-1-0-pending-matrix.md` — matriz maestra viva de pendientes y orden de trabajo hacia `1.0.0.0`;
- `docs/product/functional-specification.md` — requisitos vigentes y su estado;
- `docs/architecture/system-architecture.md` — arquitectura real;
- `docs/architecture/data-model.md` — contratos;
- `docs/architecture/calculation-engine.md` — flujo matemático;
- `docs/regulatory/regulatory-framework.md` y `docs/regulatory/regulatory-sources.md` — reglas y fuentes;
- `docs/decisions/README.md` — ADR;
- `docs/operations/validation.md` — estrategia/evidencia de pruebas;
- `docs/archive/` — evidencia histórica que no describe el estado vigente.
- `CODE_OF_CONDUCT.md` — normas de participación;
- `SUPPORT.md` — canales y límites de soporte.
- `docs/standards/code-and-comments.md` — patrón de comentarios, docstrings y documentación de runtime.

No añadir una nueva revisión cronológica al final de un documento vigente cuando el cambio puede integrarse en su estructura actual.

## 7. Documentación histórica

La documentación histórica se conserva, no se elimina para “limpiar” el repositorio.

Reglas:

- no editar una bitácora histórica para hacerla parecer vigente;
- corregir el estado actual en el documento vigente;
- si una regla histórica fue sustituida, conservar la evidencia y marcar la relación de sustitución en la documentación vigente;
- Git continúa siendo la evidencia primaria.

## 8. Normativa

Todo cambio de fórmula, parámetro legal, tabla actuarial, fecha de transición o criterio de elegibilidad debe incluir, según corresponda:

1. fuente oficial verificable;
2. fecha o versión de la fuente;
3. actualización de `regulations/*.json`;
4. actualización de `docs/regulatory/regulatory-framework.md`;
5. actualización de `docs/regulatory/regulatory-sources.md`;
6. pruebas;
7. ADR cuando exista interpretación, ambigüedad o conflicto;
8. entrada de changelog/release cuando corresponda.

No usar una nota de prensa como sustituto de una ley o reglamento cuando la norma formal esté disponible.

## 9. Datos personales y casos de validación

Está prohibido versionar datos personales reales no anonimizados.

No incorporar:

- nombres completos reales;
- cédulas;
- números de Seguro Social;
- direcciones, teléfonos o correos de personas usadas como casos;
- PDFs personales originales;
- capturas con identificadores;
- códigos únicos o QR personales;
- cuerpos de solicitudes o logs con datos previsionales sensibles.

Los originales de validación permanecen fuera de Git. Consultar [Casos de validación](tests/validation_cases/README.md).

## 10. Importaciones documentales

Toda carga de PDF debe reutilizar la validación defensiva común cuando corresponda.

La detección automática debe permanecer revisable. Un valor no detectado no puede presentarse como dato documental confirmado. La metadata de procedencia no debe alterar silenciosamente el significado jurídico del dato.

## 11. Seguridad y privacidad

Cualquier cambio que añada:

- un dato personal;
- una nueva finalidad;
- persistencia;
- telemetría;
- analítica;
- cookies;
- logging de datos;
- servicios remotos;
- terceros;
- exportaciones;

debe revisar conjuntamente la documentación de privacidad, seguridad, modelo de datos, arquitectura, especificación y validación.

No introducir telemetría o registro de datos sensibles de forma silenciosa.

## 12. Formato

- Python: 4 espacios.
- HTML/CSS/JavaScript/JSON/YAML: 2 espacios.
- Markdown: títulos jerárquicos, líneas sin espacios finales y estructura orientada al estado vigente.
- JSON normativo: JSON estándar sin comentarios.
- Texto versionado: LF.

`.editorconfig` y `.gitattributes` definen estas reglas.

## 13. Dependencias

`requirements.txt` contiene dependencias Python reproducibles.

Node.js 24 continúa fuera del runtime. El repositorio sí mantiene `scripts/package.json` y `scripts/package-lock.json` porque Playwright y axe-core son dependencias reales de automatización y accesibilidad.

Dependabot no reemplaza la revisión humana ni autoriza auto-merge. Los PR de dependencias deben revisarse contra `main` actualizado, ejecutar CI y recibir validación adicional cuando afecten parsers, seguridad, normativa o infraestructura de publicación.

## 14. Revisión antes de commit

Antes de cada commit:

```powershell
git status
git diff
git diff --check
```

Después del staging:

```powershell
git diff --cached --stat
git diff --cached --check
```

La configuración del mantenedor debe mantener `gpg.format=ssh`, `commit.gpgSign=true` y `tag.gpgSign=true`.

Después de crear un commit:

```powershell
git verify-commit HEAD
git log --show-signature -1
```

No confirmar cambios si la firma exigida no puede verificarse.

El hook local es una barrera adicional y no sustituye los checks requeridos del Pull Request. Si el hook falla, Git debe dejar el commit sin crear; primero se corrige la causa y después se vuelve a ejecutar `git commit`.

## 15. Cierre y publicación

Un hito formal solo se etiqueta cuando validaciones, documentación, `VERSION`, changelog/release y CI están correctos y el commit de cierre firmado ya existe.

El tag se crea y verifica firmado:

```powershell
git tag -s vX.Y.Z -m "Mi Retiro Proyectado vX.Y.Z"
git tag -v vX.Y.Z
```

Los tags publicados no se mueven. La excepción histórica única documentada en `docs/archive/governance/git-signature-migration-2026-08-17.md` ya fue ejecutada y no puede reutilizarse.

## 16. Gobierno

Consultar:

- [Gobierno del proyecto](GOVERNANCE.md);
- [Política de versionado](VERSIONING.md);
- [`.github/CODEOWNERS`](.github/CODEOWNERS);
- [Registro de decisiones técnicas](docs/decisions/README.md);
- [Índice de documentación](docs/README.md).
- [Código de conducta](CODE_OF_CONDUCT.md);
- [Soporte](SUPPORT.md).

<!-- NOR3-GOV-BOOTSTRAP:START -->
## Issues y revisiones por pares

Antes de abrir trabajo material, identifica el Issue propietario y consulta
[`docs/governance/github-issues-pr-governance.md`](docs/governance/github-issues-pr-governance.md).

Los bloques con revisiones consecutivas se ejecutan por defecto en pares
(`R1+R2`, `R3+R4`, etc.) cuando no exista una frontera técnica que requiera
separación. Todo PR material debe declarar Issues, alcance, validación,
documentación y remanentes.
<!-- NOR3-GOV-BOOTSTRAP:END -->
