# Guía interna de desarrollo

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.16.05-beta`
**Versión base histórica:** `0.0.23-beta`
**Base documental preservada:** GOV.1.3 R2 — 2026-08-17
**Revisión transversal vigente:** GOV.1.4 — 2026-08-17
**Clasificación:** Técnica / Interna

Esta guía contiene convenciones de ingeniería estables. Las bitácoras de fases anteriores viven en `docs/archive/`.

## 1. Identidad

- nombre visible: **Mi Retiro Proyectado**;
- naturaleza: herramienta independiente de la CSS;
- público visible: **Asegurado(a) / Asegurados(as)**;
- **Mi Retiro Seguro** se reserva para la herramienta oficial usada como fuente documental.

Identidad técnica: `app/core/config.py`.
Versión: archivo raíz `VERSION`.

## 2. Frontera entre interfaz y dominio

JavaScript puede validar interacción básica, administrar estado de pantalla, conservar la simulación temporal, coordinar importaciones y presentar resultados.

JavaScript no debe implementar fórmulas previsionales principales, introducir parámetros legales independientes ni modificar un monto calculado por Python para igualar una referencia.

## 3. Presentación

Las páginas heredan de `base.html`.

Capas CSS:

1. `style.css`;
2. `design-system.css`;
3. `accessibility.css`.

Usar tokens semánticos existentes antes de introducir colores literales.

## 4. Temas

Mantener Automático, Claro, Oscuro y Alto contraste.

Un componente nuevo debe revisarse como mínimo en Claro, Oscuro y Alto contraste.

## 5. Accesibilidad

Criterios mínimos:

- foco visible;
- etiquetas y nombres accesibles;
- errores inline asociados;
- no depender solo del color;
- objetivos táctiles adecuados;
- navegación por teclado;
- `prefers-reduced-motion`;
- tablas con semántica apropiada;
- un único `h1` por página.

## 6. Validación de formularios

`accessibility.js` administra la capa común de errores.

Las funciones llamadas por `MutationObserver` deben ser idempotentes y no duplicar estados.

## 7. Tablas

Reutilizar el contrato común (`app-table-shell` o equivalente vigente). No crear scrollbars o bordes ad hoc si existe un patrón común.

## 8. Importadores

Toda importación debe:

- usar la validación defensiva común de PDF;
- limitar tamaño y complejidad;
- procesar en memoria;
- presentar vista previa revisable;
- aplicar datos únicamente tras confirmación;
- conservar procedencia por campo cuando sea relevante;
- invalidar resultados dependientes;
- reutilizar `attachment_processing.js` para mostrar estado ocupado accesible, bloquear dobles ejecuciones y restaurar los controles al finalizar.

No versionar PDFs personales ni capturas identificativas.

## 9. Procedencia de datos

Un campo puede ser `Detectado`, `Editado por ti`, `Completado manualmente`, `Excluido por ti`, `No detectado` o `Calculado automáticamente`, según corresponda.

Una decisión del usuario no debe almacenarse mediante una opción predeterminada silenciosa. Los valores derivados deben exponer su procedencia y cambiar a `Editado por ti` cuando se modifiquen.

La procedencia es metadata de interfaz, no una fórmula.

## 10. Ficha Digital

El parser devuelve salarios del año más reciente detectado y no identidad personal.

La fecha externa se usa para vigencia. Si no se puede verificar, mostrar incertidumbre; no usar el reloj local como fuente silenciosa.

## 11. Estado e invalidación

La función de limpieza es descendente por dependencia.

Paso 3 puede reconciliar cuotas del año actual hacia Paso 2 cuando existe un dato más reciente confirmado.

Consultar `simulation-data-management.md`.

## 12. Privacidad y Developer Diagnostics

No introducir sin revisión:

- analítica;
- cookies no esenciales;
- persistencia remota;
- terceros;
- exportación automática de datos personales;
- sistemas paralelos de logging.

Developer Diagnostics está definido en `app/core/observability.py` y `observability-and-logs.md`.

Reglas obligatorias:

- apagado por defecto;
- activar solo con `MRP_DEV_MODE=1`;
- nunca registrar request/response bodies;
- nunca registrar PII, salarios, cuotas detalladas, montos, PDF, cookies o tokens;
- no registrar mensajes originales de excepciones potencialmente sensibles;
- usar correlation IDs aleatorios no derivados del usuario;
- observar una ejecución existente, nunca repetir un cálculo para obtener diagnóstico;
- cualquier metadata nueva debe ser técnica, acotada y revisable;
- no crear telemetría remota sin una decisión y revisión de privacidad separadas.

## 13. Seguridad HTTP

Mantener validación de archivos, `no-store` en API sensible y cabeceras defensivas.

`X-Correlation-ID` solo se usa con Developer Diagnostics activo.

Cambios de CSP, CDN o conectividad externa requieren actualización de seguridad/privacidad.

## 14. Versionado

No hardcodear la versión fuera de la fuente canónica.

El esquema de logs puede evolucionar independientemente mediante `schema_version`.

## 15. Documentación

Los documentos vigentes describen estado actual. No añadir un diario de revisiones si la información puede integrarse en la sección correspondiente.

Historia: `CHANGELOG.md`, `RELEASES.md`, `docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md`, `docs/archive/` y Git.

## 16. Validación antes de cierre

Cada clon de desarrollo debe activar una vez el gate de Git versionado:

```powershell
.\scripts\configure_git_hooks.ps1
```

`.githooks/pre-commit` delega en `scripts/validate_precommit.py`. Antes de permitir un commit comprueba que no se confirme directamente en `main`, que no existan cambios sin preparar ni archivos no rastreados y que pasen `git diff --cached --check`, `pip check`, compilación Python, sintaxis JavaScript y la suite completa. Un fallo devuelve código no cero y Git no crea el commit. `--no-verify` no se utiliza como vía normal para saltar este control.

El gate manual de cierre sigue siendo:

```powershell
python -m compileall app

Get-ChildItem .\app\static\js\*.js | ForEach-Object {
    node --check $_.FullName
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

python -m unittest discover -s tests -q
git diff --check
```

Después del staging:

```powershell
git diff --cached --stat
git diff --cached --check
```

## 17. Favicon e iconos

Mientras no exista el paquete gráfico definitivo, `/favicon.ico` puede responder 204 conforme a la implementación actual.

## 18. Dependencias

`requirements.txt` es el snapshot reproducible Python.

Node.js LTS se usa para validación sintáctica; no existe una cadena npm de runtime.

Dependabot no implica auto-merge.

## 19. Historia

La guía acumulativa anterior se conserva en:

`docs/archive/technical/GUIA_INTERNA_DESARROLLO_PRE_GOV1_3_R2.md`


### Regla R1.1 para datos documentales

- En vistas principales, un valor presente en la referencia documental original debe renderizarse con `readonly`/`disabled` y semántica visual de campo bloqueado.
- No habilitar edición directa de un dato detectado para simplificar una pantalla: la corrección se hace en **Revisar importación** y **Editar campos**.
- Un campo originalmente no detectado sí puede permanecer editable en la vista principal.
- Reutilizar `aplicarBloqueoVistaPrincipalPorProcedencia` o el helper equivalente y excluir explícitamente los modales de revisión.
- Mantener la misma franja de no edición y la misma iconografía de procedencia en Claro, Oscuro y Alto contraste.
- Los selectores que representan una decisión del usuario no deben inferirse de la existencia de datos importados salvo contrato documental explícito y trazado.
### Campos de fecha

Los nuevos controles `input[type=date]` no deben implementar validadores o anchos particulares salvo una necesidad funcional demostrada. `app/static/js/accessibility.js` aplica el contrato transversal de año de cuatro dígitos, calendario válido y límites técnicos por defecto; `app/static/css/accessibility.css` aplica la geometría compacta responsive. Si una superficie necesita un rango más estricto, debe declarar `min`/`max` en el propio control y la capa global lo conservará.

### Observadores del DOM

Toda normalización ejecutada desde un `MutationObserver` debe ser idempotente. Si la propia normalización modifica atributos incluidos en el filtro observado —por ejemplo `class`—, el observador debe suspenderse durante esa operación y reanudarse al finalizar para evitar ciclos de callbacks.

## Nombres de carpetas técnicas

Las carpetas técnicas nuevas deben usar nombres en inglés. Las rutas vigentes de
mayor impacto son `app/models/`, `app/engines/`, `app/services/`,
`regulations/`, `tests/validation_cases/` y `docs/archive/`. Cualquier renombre
debe actualizar imports, enlaces, pruebas y documentación antes del commit.
