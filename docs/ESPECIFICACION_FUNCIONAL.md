# Especificación funcional

## Flujo principal

La aplicación utiliza un asistente de seis pasos.

## Paso 1 — Datos personales

Datos:

- fecha de nacimiento;
- sexo;
- fecha de ingreso a la CSS, opcional;
- sistema previsional conocido o `No sé cuál tengo`.

La edad se calcula; no se solicita manualmente.

## Paso 2 — Cuotas

Datos:

- total de cuotas acreditadas;
- cuotas acreditadas en el año actual;
- continuidad de cotización;
- cuotas esperadas al cierre del año;
- cuotas esperadas por año futuro.

Resultados:

- cuotas reales;
- proyección al cierre;
- distancia preliminar respecto de 180 y 240 cuotas;
- tiempo aproximado según densidad futura.

Las cuotas del año actual ya están incluidas en el total real.

## Paso 3 — Historial salarial y salario actual

El Paso 3 separa:

1. **historial real:** cuotas y salario cotizado/reportado por año;
2. **salario actual:** remuneración vigente para la proyección.

Modos previstos:

- historial manual anual;
- continuar solo con salario actual cuando no exista información histórica suficiente;
- importación de Mi Retiro Seguro en una fase posterior.

En modo manual se generan años automáticamente, pero el usuario puede corregir el año inicial cuando una fuente histórica contenga registros anteriores.

Cada fila muestra:

- año;
- cuotas;
- salario;
- estado: completo, parcial o sin cotización.

Los campos monetarios:

- muestran separadores de miles al quedar formateados;
- admiten como máximo dos decimales;
- se validan nuevamente en backend.

El historial se contrasta con las cuotas del Paso 2. Una diferencia se informa al usuario.

El salario actual admite periodicidad semanal, quincenal, mensual o anual.

## Paso 4 — Proyección salarial

Modalidades implementadas:

1. salario constante;
2. porcentaje anual;
3. salario futuro conocido;
4. comparación de porcentajes.

La proyección:

- usa el salario normalizado del Paso 3;
- conserva precisión interna;
- redondea los resultados monetarios a centavos al materializarlos;
- mantiene el historial separado;
- representa de forma explícita años sin cotización;
- respeta el cierre de cuotas del año actual;
- repite únicamente la parte futura cuando hay varios escenarios.

## Paso 5 — Condiciones y escenarios de retiro

**Estado:** implementado en validación.

Datos heredados visibles:

- fecha de nacimiento;
- sexo;
- cuotas reales;
- cuotas del año actual y cierre esperado;
- continuidad;
- densidad de cuotas futuras.

Datos específicos:

- fecha de evaluación;
- fecha hasta la que están actualizadas las cuotas;
- escenarios de edad de referencia y años adicionales;
- fecha personalizada opcional.

Resultados:

- edad actual;
- edad de referencia;
- fecha exacta de referencia;
- días respecto de esa fecha;
- fecha y edad por escenario;
- cuotas adicionales y totales estimadas;
- estado temporal de la fecha.

La estimación de cuotas del año actual respeta primero el cierre definido en el Paso 2. La densidad anual futura se aplica después.

El Paso 5 también verifica que la proyección salarial cubra el año del escenario de retiro. Si no lo cubre, muestra una advertencia y ofrece regresar al Paso 4 para extender el horizonte. No extrapola salarios de forma silenciosa.

Estos escenarios no determinan todavía elegibilidad legal.

## Paso 6 — Resultados

**Primera capacidad implementada: SEBD normal.**

El Paso 5 permite seleccionar explícitamente el escenario futuro que alimentará Resultados. En el Paso 6:

- se muestra sistema, fecha, edad y cuotas estimadas del escenario elegido;
- si existen varios escenarios salariales del Paso 4, se selecciona cuál utilizar;
- se verifica elegibilidad para la Pensión de Retiro por Vejez Normal del SEBD;
- se seleccionan automáticamente los mejores años aplicables al salario base;
- se muestra la tasa base, bloques completos de cuotas excedentes e incrementos;
- se presentan monto antes del máximo, máximo aplicable y pensión mensual estimada;
- los años salariales proyectados quedan identificados como tales;
- las advertencias de integración y del motor normativo permanecen visibles.

Los motores Mixto, SUCGS y las demás modalidades SEBD continúan pendientes. Un escenario pasado no se calcula automáticamente con cuotas actuales porque el historial anual no permite reconstruir con precisión el total existente en una fecha histórica exacta.

## Reglas de experiencia de usuario

- `sessionStorage` conserva temporalmente la simulación;
- al cambiar un dato de origen se invalidan resultados dependientes;
- los datos reales y proyectados nunca se mezclan silenciosamente;
- los cálculos principales permanecen en Python;
- los pasos extensos disponen de navegación rápida `sticky`;
- la barra rápida reutiliza las acciones existentes y no duplica reglas;
- las advertencias de horizonte deben resolverse antes de utilizar un escenario en el cálculo final;
- una fecha de referencia no se presentará como derecho adquirido sin pasar por elegibilidad.

## Paso 6 — primera capacidad implementada

El backend puede calcular y explicar la modalidad normal del SEBD a partir de fecha de nacimiento, sexo, fecha de retiro, cuotas totales y registros salariales anuales.

La interfaz del Paso 6 ya integra la modalidad normal del SEBD, pero la aplicación sigue presentándola explícitamente como una estimación parcial del sistema mientras faltan las demás modalidades y motores.

## RF — Clasificación automática de la prestación SEBD

El Paso 6 deberá identificar automáticamente la modalidad jurídica general que corresponde al escenario seleccionado, sin exigir que el usuario conozca previamente su nombre.

Para SEBD se distinguen en esta fase:

- Pensión de Retiro por Vejez Normal;
- Anticipada;
- Proporcional;
- Proporcional Anticipada;
- posible Indemnización por Vejez;
- escenario todavía no elegible.

El resultado deberá mostrar los factores que expliquen la diferencia entre modalidades: cuotas/240 y/o reducción por edad.

Cuando corresponda `INDEMNIZACION`, el Paso 6 deberá cambiar la presentación de “pensión mensual” a “pago único estimado” y mostrar de forma auditable:

- mensualidad de pensión normal hipotética;
- meses/cuotas mensuales acreditados;
- divisor reglamentario 6;
- cociente de meses entre seis;
- pago único resultante;
- advertencia de que no se trata de una pensión vitalicia;
- transición a SUCGS desde el 01/03/2036.
