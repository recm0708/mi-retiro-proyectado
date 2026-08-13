# UX.4.6c — Simular / Paso 2 · Cuotas

**Estado:** Cerrada y validada en PC/laptop.

## Objetivo

Simplificar el Paso 2, distinguir información acreditada de supuestos futuros y extender al resto del asistente la regla de integridad adoptada para datos importados: **solo se bloquea lo que el documento realmente aportó; lo que falta permanece disponible para captura manual**.

## Cambios de interfaz

El contenido se divide en **Cuotas acreditadas** y **Cotización futura**. Se elimina el rótulo interno `Paso 2 de 6`, el cuadro redundante sobre proyección y los botones `Anterior / Analizar / Continuar` duplicados dentro de la tarjeta. Las barras superior e inferior concentran la navegación y la acción principal.

Todos los controles necesarios muestran el mismo contrato de campo obligatorio introducido en UX.4.6b. Cuando el usuario indica que no continuará cotizando, los dos campos futuros quedan deshabilitados y dejan de ser requeridos.

## Datos importados y datos faltantes

Mi Retiro Seguro puede aportar `cuotas_historicas` y, cuando existe una fila real del año actual, `cuotas_anio_actual`. UX.4.6c registra la procedencia de cada campo de manera independiente.

- Campo detectado y confirmado: solo lectura en Paso 2.
- Campo no detectado: editable y marcado como pendiente de captura manual.
- Supuestos futuros: siempre manuales.
- Corrección de un campo importado: volver a **Revisar importación** y usar el flujo de edición de la vista previa.

Este criterio se considera transversal y deberá aplicarse en UX.4.6d–UX.4.6g cuando los pasos consuman datos provenientes de documentos.

## Resultado

`Resumen preliminar` se reemplaza por **Situación de tus cuotas**. El resumen mantiene cuotas acreditadas, estimación al cierre y faltantes para 180/240 cuotas, pero usa textos dirigidos al Asegurado(a) y conserva la advertencia de que todavía no constituye un cálculo de pensión.

## Apariencia global

El control de apariencia reemplaza el símbolo circular abstracto por SVG inline: monitor para Sistema, sol para Claro, luna para Oscuro y contraste para Alto contraste. Las etiquetas textuales permanecen y los iconos son decorativos.

## Validación técnica de Revisión 3

- `python -m compileall app`: OK.
- `node --check app/static/js/*.js`: OK.
- `python -m unittest discover -s tests`: **253 pruebas en OK**.
- Revisión visual en PC/laptop: completada.


## Refinamientos de Revisión 2

- **Revisar importación** vuelve a abrir correctamente la vista previa desde Paso 2; el modal se desacopla del panel oculto donde fue renderizado inicialmente.
- Los mensajes dejan de hablar de valores “protegidos” y describen de forma neutral si un dato fue completado desde la importación o si debe completarse manualmente.
- La leyenda transversal se normaliza como `* Campo obligatorio`.
- Los campos editables de texto/número reciben pistas o ejemplos breves dentro del control; al existir un valor manual o importado la pista desaparece automáticamente.
- Se elimina la ayuda redundante debajo de `Cuotas esperadas por año futuro`, ya cubierta por la ayuda contextual.
- Los disparadores de ayuda muestran únicamente el icono `i`; el texto accesible continúa disponible mediante `aria-label`.
- El estado general de datos importados usa un icono de confirmación en lugar de un candado.


## Refinamientos de Revisión 3

- Se elimina el segundo círculo visual del control de ayuda: el área exterior sigue siendo clicable/enfocable, pero únicamente el icono `i` conserva contorno.
- La vista previa del comprobante queda organizada por destino: **Datos personales (Paso 1)**, **Información previsional básica (Paso 1)**, **Cuotas acreditadas (Paso 2)**, **Historial anual detectado (Paso 3)** y **Referencia de retiro y prestación (Pasos 5 y 6)**.
- Paso 1 conserva la revisión completa del comprobante. Desde Paso 2, **Revisar importación** muestra únicamente el bloque de cuotas correspondiente a esa etapa. El mismo contrato queda listo para reutilizarse en UX.4.6d–g.
- El bloque de Cuotas incluye total acreditado y cuota del año actual; si esta última proviene del registro anual del comprobante, se sincroniza con él al confirmar una edición.

## Cierre de UX.4.6c

UX.4.6c queda cerrada después de la validación visual en PC/laptop de la Revisión 3. Se confirmaron la captura manual, el bloqueo por campo de datos importados, la revisión contextual del comprobante desde el Paso 2, las ayudas con icono `i` de un solo contorno, la obligatoriedad accesible y la navegación superior/inferior sincronizada.

La suite completa de cierre alcanza **253 pruebas automatizadas en OK**. La revisión multidispositivo manual continúa diferida para beta/RC conforme al criterio vigente del proyecto.
