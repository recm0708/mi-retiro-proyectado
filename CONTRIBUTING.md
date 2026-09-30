# Guía de contribución

**Estado:** vigente

Este documento define el flujo mínimo para modificar Mi Retiro Proyectado sin
perder trazabilidad técnica, normativa, documental o de pruebas.

## Antes de comenzar

1. Identifica la Issue propietaria del trabajo.
2. Si comienza una fase/revisión material en un chat nuevo, completa primero el
   gate de briefing y aprobación definido en [Gobierno](GOVERNANCE.md).
3. Consulta [Gobierno de Issues y Pull Requests](docs/governance/github-issues-pr-governance.md)
   para checkpoints, revisión y cierre.
4. Verifica que el workspace local esté limpio y actualizado.

```powershell
git switch main
git fetch origin
git pull --ff-only origin main
git status
```

El trabajo ordinario se realiza en una rama específica:

```powershell
git switch -c <tipo>/<descripcion>
```

No apliques un lote de cambios sobre modificaciones locales no revisadas.

## Entorno de desarrollo

La instalación, herramientas y ejecución local se documentan en
[Guía de desarrollo](docs/operations/development-guide.md).

Para un entorno nuevo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

El entorno virtual, caches, logs y datos Developer locales no se versionan.

## Principios obligatorios

- Las fórmulas previsionales principales viven en Python.
- JavaScript no duplica motores legales.
- Los parámetros normativos modificables se mantienen en `regulations/` o en
  una fuente aislada y documentada.
- Datos acreditados, importados y proyectados permanecen diferenciados.
- Pagos únicos y pensiones mensuales permanecen separados.
- Un dato oficial desconocido no se inventa.
- Toda interpretación normativa relevante se vincula a una fuente y, cuando
  corresponda, a una ADR.
- Los documentos personales reales no se versionan.
- Código, pruebas, documentación y datos estructurados que compartan un contrato
  se actualizan en la misma unidad de trabajo.
- Comentarios y docstrings siguen
  [Estándar de código y comentarios](docs/standards/code-and-comments.md).

## Versionado

[`VERSION`](VERSION) es la única fuente canónica de versión de aplicación.

No se crean copias independientes de la versión en código, plantillas,
JavaScript, motores o documentación. La política completa se encuentra en
[Política de versionado](VERSIONING.md).

Una Issue o fase futura no reserva un Global o versión solo por estar
planificada.

## Documentación

Antes de editar documentación consulta el
[índice y mapa de autoridades](docs/README.md).

Reglas básicas:

- cada documento mantiene una función clara;
- una misma política o contrato vigente tiene una sola autoridad principal;
- la documentación viva describe el estado actual;
- la historia se conserva en Git, registros acumulativos, ADR, auditorías o
  `docs/archive/` según su función;
- no se añaden cronologías a un documento vivo solo para satisfacer una prueba
  histórica;
- movimientos o renombres deben actualizar enlaces, consumidores y regresiones
  documentales relacionadas.

Los estándares específicos están en
[Estándares de documentación](docs/standards/documentation-standards.md).

## Flujo de cambios

Antes de editar y antes del staging:

```powershell
git status
git diff
git diff --check
```

Agrupa cambios por propósito. Evita `git add .` cuando existan modificaciones
heterogéneas o archivos locales que deban revisarse.

Mensajes de commit típicos:

```text
feat(ux): describir cambio funcional
fix(data): corregir reconciliación
test(ux): agregar regresiones
docs(gov): actualizar documentación
chore(gov): ajustar configuración
refactor(core): reorganizar implementación
```

## Validación

Configura una vez por clon los hooks versionados:

```powershell
.\scripts\configure_git_hooks.ps1
git config --local --get core.hooksPath
```

El gate técnico local canónico es:

```powershell
python scripts/quality_gate.py --full
```

Cuando el alcance lo requiera, añade validaciones focales, por ejemplo:

- pruebas manuales de navegador para comportamiento visual/interactivo;
- `node --check` para JavaScript modificado;
- `npm audit --prefix scripts --audit-level=high` para tooling Node;
- comprobaciones regulatorias o de seguridad específicas.

Las pruebas automatizadas no sustituyen una revisión jurídica, actuarial ni una
auditoría de accesibilidad con tecnologías de apoyo cuando esas revisiones sean
necesarias.

## Staging y firma

Después del staging:

```powershell
git diff --cached --stat
git diff --cached --check
```

Los commits canónicos deben estar firmados. La configuración del mantenedor usa
firma SSH y debe permitir:

```powershell
git verify-commit HEAD
git log --show-signature -1
```

No uses `--no-verify` para eludir un gate fallido en el flujo ordinario.

## Pull Request

`main` está protegida. El flujo ordinario es rama → commit firmado → push →
Pull Request → checks requeridos → revisión → `Squash and merge`.

Todo PR material debe declarar:

- Issue(s) propietaria(s);
- alcance y exclusiones;
- validación ejecutada;
- documentación afectada;
- riesgos o remanentes;
- criterio de cierre.

Una corrección fuera de alcance se transfiere a otra Issue en lugar de
incorporarse silenciosamente.

## Normativa

Un cambio de fórmula, parámetro legal, tabla actuarial, fecha de transición o
criterio de elegibilidad incluye, según corresponda:

1. fuente oficial verificable;
2. fecha o versión de la fuente;
3. actualización de `regulations/*.json`;
4. actualización de las autoridades regulatorias;
5. pruebas;
6. ADR cuando exista interpretación o ambigüedad;
7. changelog/release cuando aplique.

Una nota de prensa no sustituye una ley, reglamento o resolución disponible
como fuente formal.

## Datos personales y seguridad

No se versionan nombres reales usados como casos, cédulas, NSS, direcciones,
correos personales de terceros, documentos previsionales, capturas con
identificadores, credenciales, tokens ni logs sensibles.

Los casos de prueba versionados deben ser sintéticos o estar anonimizados de
forma irreversible para su finalidad.

Cualquier cambio que introduzca persistencia, telemetría, cookies, logging,
servicios remotos, terceros o nuevos datos personales requiere revisión conjunta
de seguridad, privacidad, arquitectura y documentación.

## Dependencias

Dependabot no autoriza auto-merge. Las actualizaciones de dependencias se
revisan contra la rama principal actualizada y deben superar los gates
aplicables. Parsers, seguridad, normativa y tooling de publicación pueden
requerir validación adicional.

## Cierre y publicación

Antes de cerrar una Issue o fase:

1. completa el checklist aplicable;
2. ejecuta las validaciones acordadas;
3. verifica documentación y trazabilidad;
4. transfiere remanentes fuera de alcance;
5. confirma que no se preasignaron versiones futuras;
6. integra solo cuando el candidato sea aceptable.

Tags y GitHub Releases se crean únicamente según
[Proceso de release](docs/operations/release-process.md). Los tags publicados no
se mueven ni se reutilizan.

## Conducta y soporte

Toda participación se rige por [Código de conducta](CODE_OF_CONDUCT.md).

Para instalación, errores, consultas, privacidad o seguridad consulta
[Soporte](SUPPORT.md) antes de publicar información sensible.
