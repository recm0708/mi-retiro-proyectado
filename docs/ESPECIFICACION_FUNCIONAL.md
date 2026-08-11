# Especificación funcional

## Flujo principal

La aplicación utiliza un asistente de seis pasos.

## Paso 1 — Datos personales

Datos actuales:

- fecha de nacimiento;
- sexo;
- fecha de ingreso a la CSS, opcional;
- sistema previsional conocido o selección `No sé cuál tengo`.

La edad no se solicita manualmente; será calculada a partir de la fecha de nacimiento.

## Paso 2 — Cuotas

Datos actuales:

- total de cuotas acreditadas;
- cuotas acreditadas en el año actual;
- continuidad de cotización;
- cuotas esperadas al cierre del año;
- cuotas esperadas por año futuro.

Resultados actuales:

- cuotas reales;
- proyección al cierre del año;
- faltantes preliminares para 180 y 240 cuotas;
- tiempo aproximado para alcanzar esos umbrales según la proyección.

Las cuotas del año actual ya forman parte del total acreditado y no deben sumarse dos veces.

## Paso 3 — Historial salarial y salario actual

El Paso 3 mantiene separados dos conceptos:

1. **Historial real:** cuotas y salario cotizado/reportado por año calendario.
2. **Salario actual:** remuneración vigente que servirá como punto de partida para proyecciones futuras.

Modos previstos para proporcionar el historial:

- introducción manual anual;
- continuar solo con salario actual cuando no exista historial suficiente;
- importación desde Mi Retiro Seguro en una fase posterior.

En modo manual, la aplicación genera los años desde la fecha de ingreso a la CSS hasta el año actual. Cada fila contiene:

- año;
- cuotas;
- salario cotizado/reportado en ese año;
- estado visual: completo, parcial, sin cotización o pendiente.

El backend compara la suma de cuotas del historial con las cuotas reales informadas en el Paso 2. Una diferencia genera una advertencia, pero no bloquea automáticamente la simulación.

El salario actual puede ingresarse como semanal, quincenal, mensual o anual. La aplicación devuelve equivalentes en las cuatro periodicidades.

## Paso 4 — Proyección salarial

Modalidades previstas e implementadas en el motor:

1. mantener salario constante;
2. aplicar porcentaje anual;
3. indicar un salario futuro conocido;
4. comparar varios porcentajes.

La interfaz muestra el salario mensual normalizado del Paso 3 como valor base. Cuando existe historial manual validado, el resultado se presenta como una línea temporal dividida en tres zonas:

- historial real anterior al año actual;
- año actual, separando parte histórica y parte proyectada;
- años futuros, organizados por escenario salarial.

Cuando el usuario continúa sin historial completo, se conserva una vista de proyección futura con una advertencia de información limitada.

Los datos proyectados se almacenan separados de los datos reales.

## Paso 5 — Retiro

Pendiente.

Deberá combinar, entre otros elementos:

- fecha de nacimiento;
- sexo;
- sistema previsional;
- cuotas reales y futuras;
- salarios históricos y proyectados;
- fecha o edad de retiro evaluada.

## Paso 6 — Resultados

Pendiente.

Deberá presentar el cálculo estimado, supuestos, desglose, advertencias y comparaciones pertinentes.

## Reglas de experiencia de usuario

- los datos de una simulación en curso se conservan temporalmente;
- al cambiar un dato que alimenta un resultado, ese resultado se invalida;
- las proyecciones nunca deben presentarse como datos históricos reales;
- la interfaz no debe contener fórmulas legales principales duplicadas en JavaScript.