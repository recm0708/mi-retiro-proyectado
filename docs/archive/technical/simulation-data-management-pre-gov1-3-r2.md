# Gestión de datos de la simulación

**Fase de origen:** UX.4.6d Revisión 6
**Estado:** implementada técnicamente; pendiente validación manual.

## Objetivo

Permitir que el usuario repita escenarios y controle la información local sin dejar resultados obsoletos ni depender de herramientas técnicas del navegador.

## Niveles de control

### Limpiar este paso

Conserva los pasos anteriores. Elimina el paso activo y todos los estados posteriores que dependen de él. Paso 1 equivale a reiniciar toda la simulación porque todos los pasos dependen de Datos personales.

### Reiniciar simulación

Restablece el estado completo del asistente a Paso 1. Conserva la preferencia visual y la aceptación vigente de Términos/Privacidad.

### Borrar datos de esta aplicación en este navegador

Disponible en Fuentes/Privacidad. Elimina la simulación, constancia local de aceptación y preferencia visual pertenecientes a Mi Retiro Proyectado y vuelve a Inicio. No utiliza operaciones globales de borrado del almacenamiento del origen.

## Matriz de dependencias

| Acción | Conserva | Elimina/invalida |
|---|---|---|
| Limpiar Paso 1 | privacidad/tema | Pasos 1–6 |
| Limpiar Paso 2 | Paso 1 | Pasos 2–6 |
| Limpiar Paso 3 | Pasos 1–2 | Pasos 3–6 |
| Limpiar Paso 4 | Pasos 1–3 | Pasos 4–6 |
| Limpiar Paso 5 | Pasos 1–4 | Pasos 5–6 |
| Limpiar Paso 6 | Pasos 1–5 | resultados/configuración de Paso 6 |
| Reiniciar simulación | privacidad/tema | Pasos 1–6 |
| Borrar datos del navegador | ninguna información local de la app | simulación, consentimiento y tema |

## Privacidad

La incorporación de estos controles exige actualizar el texto visible y documental de privacidad a la versión 2026-08-15.1. No cambia la finalidad previsional ni introduce persistencia remota; sí cambia la información suministrada al titular sobre conservación y eliminación.

## Relación con la consulta de privacidad

La consulta posterior de Términos/Privacidad desde Fuentes no es una acción de borrado ni de consentimiento. Abre el mismo documento vigente en modo lectura, no cambia la aceptación guardada y no modifica la simulación. El borrado local integral continúa siendo una acción separada y explícitamente destructiva.

## R15 — limpieza semántica de Cotización futura

**Limpiar Paso 2** elimina el objeto `cuotas`, sus orígenes y resultados dependientes. Después de recargar, la plantilla no debe reintroducir una decisión por defecto: **¿Continuarás cotizando?** vuelve a `Selecciona una opción` y los dos supuestos numéricos permanecen vacíos hasta una elección explícita. Si Paso 1 conserva una importación, la capa de compatibilidad no debe bloquear un campo de cuotas cuyo valor fue eliminado por la limpieza; solo reconstruye procedencia cuando el valor todavía existe.

## Restauración segura después de limpiar o invalidar — UX.4.6d R16

Además de limpiar dependencias descendentes, la restauración del asistente valida `paso_actual`. Si una sesión antigua o una invalidación conserva un número de paso posterior al último prerrequisito válido, la interfaz abre el último paso seguro. Esto evita restaurar Paso 3 sin cuotas analizadas, Paso 4 sin Paso 3 completo, etc.

La regla no borra información adicional: únicamente corrige qué panel puede mostrarse. Cuando una derivación anterior puede reconstruirse automáticamente —por ejemplo el resumen de cuotas requerido por Paso 3— se recalcula sin navegación regresiva.

## UX.4.6d R18 — metadata de importaciones

El estado temporal puede conservar `nombre_archivo_origen` para identificar visualmente una importación confirmada después de recargar la página. No se conserva el archivo original, su ruta local ni una copia binaria. `Limpiar este paso`, `Reiniciar simulación` y **Borrar datos de esta aplicación en este navegador** eliminan esta metadata junto con el estado al que pertenece.


## UX.4.6d R19 — actualización ascendente controlada desde Paso 3

La dependencia normal del asistente sigue siendo descendente, pero existe una excepción explícita: una casilla manual de **Cuota acreditada** en el detalle del año actual puede actualizar los dos campos agregados de cuotas del Paso 2 porque el usuario está confirmando información temporalmente más reciente. Esta actualización no restaura resultados posteriores; al contrario, invalida `resumen_cuotas`, historial, proyección, retiro y resultados para recalcularlos con el dato nuevo.

La excepción no aplica por cargar una Ficha Digital ni por escribir un salario: requiere una acción manual sobre la casilla de acreditación.


## R21 — metadata de fecha de referencia

La Ficha Digital puede conservar en la sesión la fecha y fuente con las que se verificó su vigencia. Esta metadata no es un dato previsional ni una copia del documento. Al restaurar la importación, la aplicación intenta refrescarla; si no hay fecha externa verificable, marca el estado como no confiable y conserva una advertencia.
