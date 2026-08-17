# Gestión de datos de la simulación

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R2 — 2026-08-17
**Clasificación:** Técnica / Privacidad

Este documento describe el ciclo de vida actual del estado local del asistente.

## 1. Almacenamiento actual

La simulación en curso utiliza `sessionStorage`.

Claves relevantes del frontend:

- `calculadoraPensionCSS.simulacion`;
- `calculadoraPensionCSS.privacidadConsentimientoSesion`.

`localStorage` conserva estados que deben sobrevivir a una pestaña/sesión:

- `calculadoraPensionCSS.privacidadConsentimiento`;
- `mi-retiro-proyectado-tema`.

No existe una base de datos permanente de simulaciones en la versión actual.

## 2. Limpiar un paso

**Limpiar este paso** conserva los pasos anteriores y elimina/invalida el paso activo y sus dependencias posteriores.

| Paso limpiado | Conserva | Elimina/invalida |
|---|---|---|
| 1 — Datos personales | privacidad/tema | Pasos 1–6 |
| 2 — Cuotas | Paso 1 | Pasos 2–6 |
| 3 — Historial | Pasos 1–2 | Pasos 3–6 |
| 4 — Proyección | Pasos 1–3 | Pasos 4–6 |
| 5 — Retiro | Pasos 1–4 | Pasos 5–6 |
| 6 — Resultados | Pasos 1–5 | resultados y configuración de Paso 6 |

Paso 1 equivale funcionalmente a crear una simulación vacía porque todos los pasos posteriores dependen de Datos personales.

## 3. Reiniciar simulación

El reinicio:

- crea una simulación vacía;
- vuelve a `/simulacion`;
- conserva la preferencia de apariencia;
- conserva la aceptación vigente de privacidad;
- no conserva resultados ni importaciones de la simulación anterior.

## 4. Borrar datos de la aplicación en el navegador

La acción de borrado integral elimina las claves propias de:

- simulación;
- consentimiento de sesión;
- consentimiento local;
- apariencia.

Después navega a Inicio.

No ejecuta una limpieza global del almacenamiento del dominio ni borra datos ajenos a Mi Retiro Proyectado.

## 5. Invalidación descendente

Las dependencias principales son:

```text
Persona
  ↓
Cuotas
  ↓
Historial / detalle / salario
  ↓
Proyección / línea temporal
  ↓
Retiro
  ↓
Resultados
```

Un cambio relevante invalida los resúmenes posteriores para impedir mostrar resultados calculados con un estado anterior.

## 6. Reconciliación ascendente controlada

Existe una excepción deliberada a la dirección descendente: el Paso 3 puede aportar información más reciente sobre cuotas del año actual.

### Captura manual

Una modificación explícita de una casilla mensual de **Cuota acreditada** puede recalcular:

- `cuotas_anio_actual`;
- `cuotas_totales`, conservando las cuotas anteriores al año vigente.

El resumen de cuotas se invalida/revalida antes de continuar.

### Ficha Digital confirmada

Cuando una Ficha Digital confirmada identifica **más** cuotas del año actual que la referencia vigente, la aplicación puede ampliar el total del Paso 2 y su referencia del detalle.

Una Ficha con menos meses **no reduce automáticamente** una cifra superior ya acreditada. La discrepancia se comunica para revisión.

Esta regla sustituye cualquier descripción histórica que presentara el total del Paso 2 como inmutable frente a una Ficha Digital posterior.

## 7. Historial del año vigente

Cuando el detalle mensual está habilitado:

- la cantidad anual se deriva de las casillas acreditadas;
- el salario anual acreditado suma únicamente los meses marcados;
- salarios conocidos sin cuota permanecen disponibles para análisis reciente, pero no se convierten en salario histórico acreditado;
- una cuota sin salario suficiente mantiene el análisis pendiente.

## 8. Restauración

Al recargar:

- la aplicación restaura el estado serializable de la simulación;
- una importación confirmada puede conservar procedencia, edición y nombre visible del archivo;
- el `input[type=file]` nativo queda vacío;
- no se restaura ni se almacena la ruta local del archivo;
- si `paso_actual` ya no cumple prerrequisitos, se corrige al último paso accesible;
- resúmenes derivados pueden recalcularse silenciosamente cuando los datos de origen continúan completos.

## 9. Ficha Digital y vigencia

La importación puede conservar:

- año/mes más reciente;
- fecha externa usada como referencia;
- confiabilidad de esa fecha;
- fuente técnica.

Al restaurar una importación, la interfaz puede volver a consultar la fecha de referencia.

Una Ficha cuyo último período sea anterior al mes actual **verificado** requiere advertencia. Si no existe fecha externa confiable, no se usa el reloj local como reemplazo silencioso; se solicita revisión consciente.

## 10. Privacidad de archivos

Los archivos PDF se leen para su análisis y no se guardan como parte del estado de simulación.

El navegador solo conserva los datos confirmados y metadata necesaria para continuidad de interfaz.

## 11. Resultados por fotografía

Paso 6 puede conservar por separado resultados:

- proyectados;
- solo acreditados.

Una invalidación de datos de origen elimina ambas fotografías dependientes.

## 12. Historia

La versión anterior se conserva en:

`docs/historico/tecnico/GESTION_DATOS_SIMULACION_PRE_GOV1_3_R2.md`
