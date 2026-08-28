# Gestión de datos de la simulación

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.17.02-beta`
**Versión base documental:** `0.0.23-beta`
**Revisión documental base:** GOV.1.3 R2 — 2026-08-17
**Actualización vigente:** UX.4.6e R8 — procedencia editable y control documental — 2026-08-19
**Clasificación:** Técnica / Privacidad

Este documento describe el ciclo de vida actual del estado local del asistente.

## 1. Almacenamiento actual

La simulación en curso utiliza `sessionStorage`.

Claves relevantes del frontend:

- `miRetiroProyectado.simulacion`;
- `miRetiroProyectado.privacidadConsentimientoSesion`.

`localStorage` conserva estados que deben sobrevivir a una pestaña/sesión:

- `miRetiroProyectado.privacidadConsentimiento`;
- `miRetiroProyectado.tema`.

No existe una base de datos permanente de simulaciones en la versión actual.

Las claves usan el namespace `miRetiroProyectado.*` como contrato técnico único.
La transición desde identificadores pre-beta anteriores es deliberadamente
disruptiva: no existe fallback ni migración porque el cambio se ejecuta antes de
la beta pública y se aceptó descartar el estado local de pruebas existente.

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

También purga identificadores pre-beta conocidos exclusivamente durante esta operación destructiva. Esas claves antiguas **no se leen, restauran ni migran**: se reconocen solo para impedir que una aceptación o estado residual sobreviva al borrado solicitado por el usuario.

Después navega a Inicio con una solicitud explícita de volver a mostrar los términos. Si el usuario cierra esa consulta sin aceptar y luego entra a Simular, la ausencia de consentimiento obliga a abrir nuevamente el modal antes de habilitar el asistente.

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

Una Ficha con menos meses **no reduce automáticamente** una cifra superior ya acreditada. La discrepancia se comunica para revisión. Esta regla no impide una reducción posterior causada por una **exclusión explícita del usuario**: en ese caso la aplicación identifica el período como `Excluido por ti`, reconcilia los agregados y conserva el valor documental original como referencia.

Esta regla sustituye cualquier descripción histórica que presentara el total del Paso 2 como inmutable frente a una Ficha Digital posterior.

## 7. Historial del año vigente

Cuando el detalle mensual está habilitado:

- la cantidad anual se deriva de las casillas acreditadas;
- el salario anual acreditado suma únicamente los meses marcados;
- salarios conocidos sin cuota permanecen disponibles para análisis reciente, pero no se convierten en salario histórico acreditado;
- una cuota sin salario suficiente mantiene el análisis pendiente;
- un período importado puede excluirse explícitamente de la simulación sin borrar su referencia documental;
- reincluir un período restaura su participación y, si no existen otras modificaciones, su estado `Detectado`.

## 8. Restauración

Al recargar:

- la aplicación restaura el estado serializable de la simulación;
- una importación confirmada puede conservar procedencia, edición y nombre visible del archivo;
- la fotografía original y la copia de trabajo confirmada pueden conservarse por separado para explicar ajustes posteriores;
- las exclusiones explícitas de períodos se restauran con la simulación;
- el `input[type=file]` nativo queda vacío;
- no se restaura ni se almacena la ruta local del archivo;
- si `paso_actual` ya no cumple prerrequisitos, se corrige al último paso accesible;
- resúmenes derivados pueden recalcularse silenciosamente cuando los datos de origen continúan completos.


## 8.1. Procedencia editable y referencias documentales

Una importación confirmada no vuelve inmutable el dato para la simulación.

El estado local puede conservar:

- una fotografía original del resumen detectado;
- una copia de trabajo que alimenta los campos confirmados;
- mapas de procedencia por campo;
- identificadores de campos editados;
- períodos de Ficha Digital excluidos explícitamente.

La fotografía original no se reescribe cuando el usuario cambia la copia de trabajo. Esto permite distinguir:

- lo que decía el documento;
- lo que el usuario completó o modificó;
- lo que la simulación utiliza finalmente.

Los estados visibles son `Detectado`, `Editado por ti`, `Completado manualmente`, `Excluido por ti`, `No detectado` y, para valores derivados por una regla de interfaz, `Calculado automáticamente`.

Un aviso de ajuste solo permanece visible mientras exista al menos una modificación, complemento o exclusión activa en el bloque correspondiente. El texto enumera únicamente las categorías realmente activas; revertir todos los cambios de ese bloque oculta el aviso.

Los controles que exigen una decisión del Asegurado(a) mantienen `""` o `null` mientras no exista selección. No se usa una alternativa visualmente preseleccionada para completar silenciosamente el estado. Una importación confirmada puede derivar una decisión únicamente cuando el origen sea inequívoco y trazable.

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

El indicador global de análisis de adjuntos es estado efímero de interfaz: deshabilita temporalmente los controles, evita ejecuciones duplicadas y no añade persistencia del archivo.

## 11. Resultados por fotografía

Paso 6 puede conservar por separado resultados:

- proyectados;
- solo acreditados.

Una invalidación de datos de origen elimina ambas fotografías dependientes.

## 12. Historia

La versión anterior se conserva en:

`docs/archive/technical/GESTION_DATOS_SIMULACION_PRE_GOV1_3_R2.md`


### Decisiones de historial en R1.1

`modo_historial_confirmado_usuario` evita inferir una decisión a partir de la mera existencia de registros importados. Mi Retiro Seguro puede poblar `historial`, `origen_campos_historial` y el año inicial temporal sin establecer `modo_historial`; el selector permanece vacío hasta una acción explícita. Al limpiar desde Paso 3, tanto `modo_historial` como el indicador de confirmación vuelven a su estado vacío.

La edición de valores originalmente detectados se realiza dentro del modal y actualiza la copia de trabajo, mientras la referencia `*_original` continúa determinando procedencia y bloqueo en la vista principal.

### UX.4.6g R1 — preferencias temporales de retiro

`preferencias_retiro` conserva exclusivamente en el estado temporal del navegador la selección visible del Paso 5: `anios_adicionales`, `incluir_fecha_evaluacion`, `origen` y `anio_fin_proyeccion_origen`. `SUGERIDO_PASO4` identifica una propuesta derivada del horizonte salarial; `EDITADO_USUARIO` impide que sincronizaciones automáticas posteriores pisen una selección manual. Esta estructura no es un dato oficial de la CSS ni sustituye `retiro`, que contiene la solicitud efectivamente analizada por el backend.
