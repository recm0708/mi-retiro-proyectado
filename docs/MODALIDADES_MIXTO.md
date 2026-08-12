# Subsistema Mixto — diseño y alcance del motor

## Propósito

Este documento describe la implementación progresiva del Subsistema Mixto dentro del Paso 6 de la Calculadora de Pensión CSS.

La finalidad es mantener separados los dos componentes que forman la prestación y evitar cálculos aparentemente exactos cuando falten datos de la cuenta individual o parámetros actuariales oficiales.

## Fuentes normativas de referencia

La implementación se basa principalmente en:

- Texto Único de la Ley 51 de 2005 con reformas hasta la Ley 462 de 2025, Gaceta Oficial 30284-B de 22 de mayo de 2025;
- artículos 155 y 178–188 para ámbito, retiro y componentes del Mixto;
- artículos 192 y 193 para mínimos/máximos aplicables al componente definido;
- Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria, Resolución 57,805-2025-J.D.;
- Reglamento de Incorporación al Subsistema Mixto;
- Reglamento de Seguros Colectivos del Componente de Ahorro Personal del Subsistema Mixto.

Cuando exista una discrepancia entre disposiciones o comunicaciones operativas, el proyecto la documentará expresamente.

## Estructura de la prestación

La pensión bajo Mixto se modela como:

```text
Pensión Mixto
=
Componente de Beneficio Definido
+
Componente de Ahorro Personal
```

Ambos componentes se calculan y presentan de forma separada antes de producir el total.

## 1. Componente de Beneficio Definido

### Salario participante

La participación del componente definido está limitada a B/.500.00 mensuales.

Con detalle mensual, el cálculo debe aplicar el límite mes por mes.

La versión 6D.1 dispone solo de historial anual en el asistente. Por tanto usa una aproximación:

```text
salario considerado BD del año
=
min(
  salario cotizado/reportado del año,
  B/.500.00 × cuotas acreditadas del año
)
```

Cuando esta aproximación recorta un salario, la salida marca:

```text
usa_aproximacion_anual_tope_mensual = true
```

y genera una advertencia.

### Modalidad

La clasificación de edad/cuotas se reutiliza desde el motor general SEBD:

- Normal;
- Anticipada;
- Proporcional;
- Proporcional Anticipada.

La reutilización no implica que los importes máximos sean iguales. El componente BD del Mixto aplica su máximo propio de B/.500.00 mensuales.

### Orden de cálculo

En la primera implementación:

```text
1. formar historial participante BD;
2. seleccionar base salarial;
3. determinar tasa e incrementos;
4. obtener monto previo al máximo;
5. limitar el componente a B/.500.00;
6. aplicar factor proporcional, si corresponde;
7. aplicar factor de edad, si corresponde.
```

El mínimo indexado continúa pendiente de versionarse por fecha.

## 2. Componente de Ahorro Personal

### Dato principal

El motor no reconstruye el saldo actual sumando porcentajes al historial salarial.

Necesita el saldo ahorrado y capitalizado de la cuenta individual cuando esté disponible por una fuente oficial o verificable.

### Bono de reconocimiento

Cuando corresponda, el bono de reconocimiento se suma de manera separada al saldo:

```text
capital total =
saldo ahorro personal
+
bono de reconocimiento
```

6D.1 acepta un monto de bono ya determinado. Todavía no calcula el bono desde sus reglas reglamentarias.

### Pensión programada

La fórmula implementada es:

```text
pensión programada CAP =
capital total
/
valor actuarial de expectativa de vida
```

El valor actuarial depende de la expectativa de vida, tabla de mortalidad y tasa de descuento aplicables.

La aplicación no ha versionado aún un divisor actuarial oficial vigente. Por ello, si no se proporciona el valor:

```text
calculo_disponible = false
```

y no se calcula un total Mixto.

### Sin máximo propio

El CAP se conserva sin un máximo mensual artificial en el modelo.

## 3. Resultado total

Solo cuando ambos componentes mensuales están disponibles:

```text
pensión_mensual_total_estimada =
pensión_BD
+
pensión_programada_CAP
```

Si el CAP está incompleto, el BD puede mostrarse, pero el total queda pendiente.

## 4. Transición hacia SUCGS

La implementación operativa de retiro usa:

```text
Hasta 29/02/2032 → posible cálculo Mixto
Desde 01/03/2032 → transición SUCGS
```

Esta fecha se fundamenta en el artículo 188 y el reglamento de incorporación al componente contributivo de capitalización solidaria.

El artículo 153 del Texto Único contiene también una fecha 01/03/2036 para asegurados del Mixto. Esta discrepancia queda registrada en los parámetros y documentación; no se modifica silenciosamente el texto legal.

## 5. Opción de sistema en 2026

El reglamento original de 2025 registró 17/03/2026 como fecha límite de opción. Comunicaciones oficiales de la CSS en 2026 utilizan 18/08/2026 como fecha límite operativa.

6D.1 conserva ambos datos para trazabilidad y no decide automáticamente si una persona específica tiene derecho a ejercer la opción.

## 6. Prestaciones aún pendientes

La primera subfase no considera completo el Subsistema Mixto. Quedan pendientes:

- integración del Mixto con el Paso 6 visual;
- cálculo reglamentario del bono de reconocimiento;
- tratamiento combinado de indemnización del BD y devolución del CAP;
- devolución del ahorro cuando no se alcance una pensión;
- garantía mediante seguros colectivos y continuidad de pago cuando se agote el CAP;
- parámetros actuariales oficiales versionados;
- regímenes y casos especiales;
- transición completa y comparación con SUCGS.

## 7. Principio de transparencia

La aplicación debe diferenciar siempre:

```text
dato oficial/ingresado
dato proyectado
parámetro normativo versionado
valor sintético de prueba
cálculo no disponible
```

Un resultado parcial del componente BD no se presentará como pensión total Mixto si el CAP no puede calcularse.

## 8. Paso 6D.2 — opciones, devolución y garantía del CAP

### Opción explícita del asegurado

La entrada `opcion_prestacion_cap` admite:

```text
AUTO
PENSION_PROGRAMADA
DEVOLUCION_TOTAL
```

Cuando el asegurado alcanza la edad de referencia sin cumplir los requisitos de la Pensión de Retiro por Vejez Normal, el artículo 187 permite solicitar la devolución total de la suma ahorrada y capitalizada en la cuenta. La aplicación no toma esa decisión por el usuario.

Si `AUTO` encuentra una devolución disponible, devuelve:

```text
decision_requerida = true
calculo_disponible = false
```

hasta que se elija una vía.

### Devolución total del CAP

Cuando procede y se elige `DEVOLUCION_TOTAL`:

```text
devolucion_pago_unico_estimado = capital_total_considerado
pension_programada_mensual = null
```

La salida indica que se trata de un pago único. Las primas del Seguro Colectivo de Renta Vitalicia no se agregan a la devolución porque el reglamento las considera parte del aporte de solidaridad.

### Indemnización del BD + devolución CAP

Con menos de 180 cuotas a la edad de referencia, el componente BD puede producir la Indemnización por Vejez del artículo 186. Si además se solicita la devolución del CAP, ambos importes se conservan por separado:

```text
pago_unico_bd_estimado
pago_unico_cap_estimado
pago_unico_total_estimado
```

No se genera una pensión mensual total en esa ruta.

### Pensión proporcional + devolución CAP

Con 180–239 cuotas a la edad de referencia, el componente BD puede producir una pensión proporcional. Si el usuario elige la devolución total del CAP, la salida conserva:

- la pensión mensual BD;
- el pago único de devolución CAP;
- sin inventar una renta mensual CAP.

### Garantía de renta vitalicia

El artículo 184 y el artículo 10 del Reglamento de Seguros Colectivos establecen que, si el pensionado sobrevive la expectativa de vida utilizada para determinar la pensión CAP y se agotan los fondos, el Seguro Colectivo de Renta Vitalicia continúa pagando mensualmente la suma correspondiente al CAP hasta la muerte.

La garantía:

```text
NO aumenta la pensión inicial
NO se suma como complemento inmediato
SÍ conserva la continuidad futura del pago CAP bajo la condición legal
```

La prima histórica de 0.93 % se conserva únicamente como referencia normativa de la edición reglamentaria actualizada a junio de 2020. No se utiliza para reconstruir saldos individuales ni para descontar nuevamente el capital ingresado.

### Bono de reconocimiento

El artículo 183 reconoce un bono a determinados asegurados que ingresaron voluntariamente al Mixto desde el SEBD y reunían las condiciones legales correspondientes.

6D.2 no calcula ese bono automáticamente. Si se introduce un monto mayor que cero, el modelo registra además si fue confirmado oficialmente. Un bono no confirmado deja el total como provisional.

## 9. Estado después de 6D.2

Implementado en backend:

- componente BD de pensión;
- indemnización del componente BD;
- pensión programada CAP;
- devolución total CAP;
- decisión explícita entre alternativas cuando procede;
- garantía de renta vitalicia como continuidad futura;
- separación de pagos únicos y mensuales;
- trazabilidad del bono de reconocimiento;
- transición Mixto → SUCGS.

Pendiente:

- integración visual del Mixto en el Paso 6;
- importación/lectura del saldo CAP oficial;
- obtención de divisor actuarial vigente desde una fuente pública versionable;
- cálculo automático del bono de reconocimiento si se documenta una regla reproducible;
- SUCGS y comparación final entre sistemas.

## Integración visual 6D.3

La interfaz del Paso 6 consume `POST /api/simulacion/resultados/mixto`. El historial, las cuotas y el escenario de retiro se heredan del asistente; los datos propios del CAP se solicitan de forma explícita.

La presentación separa cuatro resultados posibles:

```text
pensión mensual BD
pensión programada CAP
pago único BD
pago único CAP
```

La pensión mensual total solo suma rentas mensuales. El total de pagos únicos solo suma prestaciones de pago único. Una decisión CAP pendiente se muestra como tal y no produce un total mensual ficticio.
