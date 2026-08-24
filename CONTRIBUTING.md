# Guía de contribución


<!-- DOC1-R1-POST-MANT1:START -->
## Estado de contribución post-MANT.1

La contribución al proyecto debe leerse desde la línea base documental posterior a MANT.1 R7.

Estado vigente:

- MANT.1 quedó cerrado operativamente en R7.
- DOC.1 R1 está activo para sincronizar documentación Markdown vigente.
- `VERSION` permanece sincronizado con la versión canónica vigente del árbol; en VER.2 R4 se promueve a `0.0.71.01-beta`.
- VER.2 permanece como reconciliación/candidato pendiente, no como versión publicada.
- Todo cambio debe mantener sincronizados código, pruebas, documentación y evidencia aplicable.
<!-- DOC1-R1-POST-MANT1:END -->

Este documento define el flujo mínimo para modificar Mi Retiro Proyectado sin perder trazabilidad técnica, normativa, documental o de pruebas.

## 1. Antes de comenzar

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

No aplicar un paquete de cambios sobre modificaciones locales no revisadas.

Toda participación en issues, Pull Requests o revisiones debe respetar [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Para dudas de uso, reportes, privacidad o seguridad, consultar primero [`SUPPORT.md`](SUPPORT.md).

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
- Comentarios y docstrings siguen [`docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md`](docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md); explican intención y contratos, no la sintaxis obvia.

## 3. Fuente de versión

`VERSION` es la única fuente canónica de versión de aplicación.

No escribir versiones independientes en:

- `app/core/config.py`;
- plantillas;
- JavaScript;
- motores;
- documentación que pretenda definir una segunda fuente.

Consultar [`VERSIONING.md`](VERSIONING.md).

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

## 6. Documentación como parte del cambio

Actualizar únicamente los documentos afectados, pero hacerlo **antes del cierre** del cambio.

Mapa general:

- `README.md` — presentación y estado general;
- `CHANGELOG.md` — cambios notables por versión;
- `RELEASES.md` — releases, tags y reconstrucción de versiones;
- `docs/INDICE.md` — mapa documental;
- `docs/ROADMAP.md` — presente y futuro;
- `docs/ESPECIFICACION_FUNCIONAL.md` — requisitos vigentes y su estado;
- `docs/ARQUITECTURA.md` — arquitectura real;
- `docs/MODELO_DE_DATOS.md` — contratos;
- `docs/MOTOR_DE_CALCULO.md` — flujo matemático;
- `docs/NORMATIVA.md` y `docs/FUENTES_NORMATIVAS.md` — reglas y fuentes;
- `docs/DECISIONES.md` — ADR;
- `docs/VALIDACION.md` — estrategia/evidencia de pruebas;
- `docs/archive/` — evidencia histórica que no describe el estado vigente.
- `CODE_OF_CONDUCT.md` — normas de participación;
- `SUPPORT.md` — canales y límites de soporte.
- `docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md` — patrón de comentarios, docstrings y documentación de runtime.

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
4. actualización de `docs/NORMATIVA.md`;
5. actualización de `docs/FUENTES_NORMATIVAS.md`;
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

Los originales de validación permanecen fuera de Git. Consultar [`tests/validation_cases/README.md`](tests/validation_cases/README.md).

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

Node.js LTS es una herramienta auxiliar para `node --check`; no forma parte del runtime y no justifica un `package.json` mientras no existan dependencias npm reales.

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

Los tags publicados no se mueven. La excepción histórica única documentada en `docs/MIGRACION_FIRMAS_GIT_2026-08-17.md` ya fue ejecutada y no puede reutilizarse.

## 16. Gobierno

Consultar:

- [`GOVERNANCE.md`](GOVERNANCE.md);
- [`VERSIONING.md`](VERSIONING.md);
- [`.github/CODEOWNERS`](.github/CODEOWNERS);
- [`docs/DECISIONES.md`](docs/DECISIONES.md);
- [`docs/INDICE.md`](docs/INDICE.md).
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md);
- [`SUPPORT.md`](SUPPORT.md).
