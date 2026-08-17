# Guía interna de desarrollo

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.22-beta`
**Revisión documental:** GOV.1.3 R2 — 2026-08-17
**Clasificación:** Técnica / Interna

Esta guía contiene convenciones de ingeniería estables. Las bitácoras de fases anteriores viven en `docs/historico/`.

## 1. Identidad

- nombre visible: **Mi Retiro Proyectado**;
- naturaleza: herramienta independiente de la CSS;
- público visible: **Asegurado(a) / Asegurados(as)**;
- **Mi Retiro Seguro** se reserva para la herramienta oficial usada como fuente documental.

Identidad técnica: `app/core/config.py`.
Versión: archivo raíz `VERSION`.

## 2. Frontera entre interfaz y dominio

JavaScript puede:

- validar interacción básica;
- administrar estado de pantalla;
- conservar la simulación temporal;
- coordinar importaciones;
- presentar resultados.

JavaScript no debe:

- implementar fórmulas previsionales principales;
- introducir parámetros legales independientes;
- modificar un monto calculado por Python para igualar una referencia.

## 3. Presentación

Las páginas heredan de `base.html`.

Capas CSS:

1. `style.css` — base y reglas funcionales históricas;
2. `design-system.css` — sistema visual vigente;
3. `accesibilidad.css` — remates accesibles con precedencia final.

Usar tokens semánticos existentes antes de introducir colores literales.

## 4. Temas

Mantener:

- Automático;
- Claro;
- Oscuro;
- Alto contraste.

Un componente nuevo debe revisarse como mínimo en Claro, Oscuro y Alto contraste.

La preferencia de tema no forma parte del cálculo.

## 5. Accesibilidad

Criterios mínimos:

- foco visible;
- etiquetas y nombres accesibles;
- errores inline asociados;
- no depender solo del color;
- objetivos táctiles adecuados;
- navegación por teclado;
- `prefers-reduced-motion`;
- tablas con caption/semántica y foco solo si existe desbordamiento;
- un único `h1` por página.

Las mejoras automáticas no sustituyen una auditoría WCAG con tecnologías de apoyo.

## 6. Validación de formularios

`accesibilidad.js` administra la capa común de errores.

Reglas:

- `aria-invalid` solo mientras el control sea inválido;
- mensaje inline enlazado;
- evitar duplicar `role="alert"` y anuncios assertive equivalentes;
- usar `ValidityState.valid` en validación reactiva cuando no se desea disparar `invalid`;
- funciones llamadas por `MutationObserver` deben ser idempotentes.

## 7. Tablas

Reutilizar el contrato común (`app-table-shell` o equivalente vigente).

No crear bordes, radios o scrollbars ad hoc si existe un patrón común.

El scroll interno solo debe aparecer cuando exista desbordamiento real.

## 8. Importadores

Toda importación debe:

- usar la validación defensiva común de PDF;
- limitar tamaño y complejidad;
- procesar en memoria;
- presentar vista previa revisable;
- aplicar datos únicamente tras confirmación;
- conservar procedencia por campo cuando sea relevante;
- invalidar resultados dependientes.

No versionar PDFs personales ni capturas identificativas.

## 9. Procedencia de datos

Un campo puede ser:

- detectado;
- editado;
- completado manualmente;
- no detectado.

No bloquear un campo solo porque exista una importación confirmada; el bloqueo depende de que ese campo tenga procedencia documental aplicable.

La procedencia es metadata de interfaz, no una fórmula.

## 10. Ficha Digital

El parser devuelve salarios del año más reciente detectado y no identidad personal.

La fecha externa se usa para vigencia. Si no se puede verificar, mostrar incertidumbre; no usar el reloj local como fuente silenciosa.

Al aplicar la importación al detalle, respetar la reconciliación vigente de cuotas y nunca reducir silenciosamente una referencia superior.

## 11. Estado e invalidación

La función de limpieza es descendente por dependencia.

Paso 3 puede reconciliar cuotas del año actual hacia Paso 2 cuando existe un dato más reciente confirmado. Esa excepción debe invalidar/revalidar lo posterior.

Consultar `GESTION_DATOS_SIMULACION.md`.

## 12. Privacidad

No introducir sin revisión:

- telemetría;
- analítica;
- cookies no esenciales;
- persistencia remota;
- logging de PII;
- terceros;
- exportación automática.

GOV.1.4 definirá Developer Diagnostics; hasta entonces no crear un sistema paralelo de logs sin contrato.

## 13. Seguridad HTTP

Mantener validación de archivos, `no-store` en API sensible y cabeceras defensivas.

Cambios de CSP, CDN o conectividad externa requieren actualización de seguridad/privacidad.

## 14. Versionado

No hardcodear la versión fuera de la fuente canónica.

Consultar `VERSIONING.md`.

## 15. Documentación

Los documentos vigentes describen estado actual. No añadir al final un diario de `R1`, `R2`, `R3` si la información puede integrarse en la sección correspondiente.

Historia:

- `CHANGELOG.md`;
- `RELEASES.md`;
- `docs/REGISTRO_CAMBIOS_HISTORICO.md`;
- `docs/historico/`;
- Git.

## 16. Validación antes de cierre

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

Al integrar recursos definitivos:

- usar `app/static/img/`;
- actualizar `base.html`;
- retirar la ruta temporal;
- actualizar regresiones y documentación.

## 18. Dependencias

`requirements.txt` es el snapshot reproducible Python.

Node.js LTS se usa actualmente para validación sintáctica; no existe una cadena npm de runtime.

Dependabot no implica auto-merge.

## 19. Historia

La guía acumulativa anterior se conserva en:

`docs/historico/tecnico/GUIA_INTERNA_DESARROLLO_PRE_GOV1_3_R2.md`
