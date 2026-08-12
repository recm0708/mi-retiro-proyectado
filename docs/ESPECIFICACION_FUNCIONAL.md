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

Los motores SEBD, Subsistema Mixto y SUCGS disponen ya de integración con el Paso 6 en las capacidades documentadas para cada subfase. Un escenario pasado no se calcula automáticamente con cuotas actuales porque el historial anual no permite reconstruir con precisión el total existente en una fecha histórica exacta.

## Reglas de experiencia de usuario

- `sessionStorage` conserva temporalmente la simulación;
- al cambiar un dato de origen se invalidan resultados dependientes;
- los datos reales y proyectados nunca se mezclan silenciosamente;
- los cálculos principales permanecen en Python;
- los pasos extensos disponen de navegación rápida `sticky`;
- el usuario puede abrir directamente cualquier paso que conserve sus prerrequisitos mediante los indicadores superiores o el selector `Ir a paso`;
- los pasos cuyo estado haya quedado inválido por cambios anteriores permanecen deshabilitados hasta ser recalculados;
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


## RF — Motor preliminar del Subsistema Mixto

La aplicación deberá poder recibir una entrada independiente para el Subsistema Mixto con:

- fecha de nacimiento y sexo;
- fecha de retiro;
- cuotas totales;
- distribución de cuotas excedentes antes/después de la referencia cuando sea necesaria;
- historial anual de cuotas y salario;
- sistema seleccionado (`MIXTO` o `SUCGS`);
- saldo de ahorro personal, cuando esté disponible;
- bono de reconocimiento, cuando corresponda;
- valor actuarial oficial de expectativa de vida, cuando esté disponible.

El resultado deberá:

1. verificar primero si la fecha y opción permiten todavía un cálculo bajo Mixto;
2. calcular por separado el Componente de Beneficio Definido;
3. limitar la participación salarial del BD a B/.500.00 mensuales;
4. advertir cuando el historial anual obliga a aproximar un tope que jurídicamente es mensual;
5. calcular el CAP solo con saldo y divisor actuarial explícitos;
6. no reutilizar factores actuariales de SUCGS para el CAP;
7. sumar ambos componentes únicamente cuando ambos cálculos estén disponibles;
8. identificar de forma separada una transición a SUCGS;
9. mantener visibles las fuentes normativas y las limitaciones de datos.

La selección individual de cambio de sistema antes de la fecha límite operativa no se determinará automáticamente en esta subfase. La interfaz podrá mostrar información general, pero la elegibilidad específica para ejercer una opción deberá implementarse cuando las reglas operativas estén totalmente reconciliadas.

## Requisitos funcionales Mixto — 6D.2

- RF-MIX-06: cuando el artículo 187 permita devolución del CAP, la aplicación deberá solicitar una elección expresa y no asumirla automáticamente.
- RF-MIX-07: la devolución del CAP deberá mostrarse como pago único separado de cualquier pensión mensual.
- RF-MIX-08: si el componente BD produce indemnización y el CAP se devuelve, deberán mostrarse ambos pagos únicos y su suma.
- RF-MIX-09: la garantía del Seguro Colectivo de Renta Vitalicia deberá explicarse como continuidad futura del CAP después del agotamiento de los fondos, no como incremento inicial.
- RF-MIX-10: un bono de reconocimiento ingresado pero no confirmado oficialmente deberá marcar el resultado como provisional.
- RF-MIX-11: las primas históricas de seguros colectivos podrán mostrarse como trazabilidad, pero no utilizarse para reconstruir saldos individuales sin normativa vigente y movimientos de cuenta.

### Integración visual Mixto — Paso 6D.3

Cuando el sistema seleccionado sea `MIXTO`, el Paso 6 debe:

- permitir seleccionar el escenario salarial construido en el Paso 4;
- solicitar saldo CAP, bono, confirmación del bono, valor actuarial y tratamiento del CAP;
- mantener `AUTO` como opción que puede exigir decisión expresa;
- mostrar por separado pensión mensual y pagos únicos;
- identificar visualmente los componentes BD y CAP;
- informar si el resultado está completo, pendiente de decisión o incompleto por falta de datos;
- mostrar la garantía de renta vitalicia únicamente cuando el motor la declare aplicable;
- conservar fuentes y advertencias devueltas por el backend.

## RF — cálculo SUCGS por capas

La aplicación debe calcular el componente contributivo base del SUCGS usando el saldo acumulado informado y el factor actuarial versionado por edad. Después debe evaluar los artículos 194 y 195, distinguiendo el complemento solidario, la Pensión de Beneficio Mínimo, la Pensión de Beneficio Solidario y la Pensión Garantizada Solidaria cuando corresponda.

La API debe mantener separados `pension_contributiva_mensual`, `pension_despues_componente_solidario` y `pension_mensual_total_estimada`. La última cifra solo debe completarse cuando la garantía del artículo 197 pueda determinarse o cuando se compruebe que no aplica.

### RF — garantía de reemplazo mínimo SUCGS

La aplicación debe preevaluar el artículo 197 con trazabilidad de: años con menos de cinco cuotas, total y racha de años sin cotización, cuotas en los primeros veinte años y en los restantes, salario promedio base mensual y condición de estabilidad salarial. No debe reinterpretar automáticamente la regla de estabilidad del 30 %; mientras no exista una aplicación operativa inequívoca, debe requerirse confirmación explícita.

### Integración visual SUCGS — Paso 6E.4

Cuando el sistema seleccionado sea `SUCGS`, el Paso 6 debe permitir seleccionar el escenario salarial, introducir el saldo de Capitalización Solidaria, confirmar su procedencia oficial, revisar los valores solidarios vigentes y declarar si el historial cubre toda la vida laboral relevante para el artículo 197. La condición de estabilidad salarial debe admitir tres estados: confirmada, no cumple o pendiente.

El resultado debe presentar por separado la pensión contributiva, el complemento solidario, el resultado después de los artículos 194 y 195, la evaluación del artículo 197, el complemento de garantía y la pensión mensual total cuando el cálculo pueda cerrarse.
