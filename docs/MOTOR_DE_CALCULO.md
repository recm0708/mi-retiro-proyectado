# Motor de cálculo

## Principio general

La lógica de cálculo debe permanecer separada de HTML y JavaScript. La interfaz captura y presenta; Python valida y calcula.

## Análisis preliminar de cuotas

Archivo:

```text
app/servicios/proyeccion_cuotas.py
```

Comportamiento actual:

- valida que las cuotas del año actual no superen el total acreditado;
- diferencia cuotas reales de cuotas futuras;
- si la persona no continuará cotizando, no agrega cuotas futuras;
- calcula faltantes preliminares para 180 y 240 cuotas;
- estima tiempo usando `cuotas_faltantes / cuotas_por_anio`.

Los umbrales actuales son preliminares y no sustituyen el futuro motor de elegibilidad legal.

## Análisis del historial salarial

Archivo:

```text
app/servicios/historial_salarios.py
```

Comportamiento actual:

- valida el rango de años;
- rechaza años duplicados;
- valida coherencia básica entre cuotas y salario reportado;
- clasifica registros como completos, parciales o sin cotización;
- detecta años sin registro;
- suma las cuotas introducidas;
- compara esa suma con las cuotas reales del Paso 2;
- calcula la diferencia de cuotas sin bloquear automáticamente el flujo;
- resume el total salarial histórico reportado.

Este análisis todavía trabaja a nivel anual. Los cálculos legales sensibles al mes o fecha exacta requerirán detalle mensual en una fase posterior.

## Normalización salarial

Archivo:

```text
app/servicios/proyeccion_salarios.py
```

Conversión a equivalente anual:

```text
semanal     = monto × 52
quincenal   = monto × 24
mensual     = monto × 12
anual       = monto
```

Las demás periodicidades se derivan del equivalente anual.

## Proyección por porcentaje

Se utiliza crecimiento compuesto:

```text
salario_año_n = salario_base × (1 + tasa)^n
```

El año inicial conserva el salario base.

## Salario futuro conocido

Cuando el usuario conoce un salario para un año futuro, se calcula una tasa anual compuesta equivalente que conecta el salario actual con el salario futuro:

```text
tasa = (salario_futuro / salario_actual)^(1 / años) - 1
```

La tasa obtenida se utiliza para construir la serie anual.

## Comparación de escenarios

La modalidad `ESCENARIOS` genera una serie independiente por cada porcentaje solicitado. El valor inicial sugerido actualmente es:

```text
0 %, 1 %, 2 %, 3 %
```

## Redondeo monetario

El salario mensual proyectado se redondea a dos decimales y el salario anual visible se calcula a partir de ese valor mensual redondeado multiplicado por 12. Esto mantiene coherencia entre cifras mostradas.

## Línea temporal histórica y proyectada

Archivo:

```text
app/servicios/linea_tiempo.py
```

Comportamiento actual:

- reutiliza los servicios de historial, cuotas, salario actual y proyección;
- mantiene separados valores históricos y proyectados;
- representa el año actual como `MIXTO` cuando existen cuotas reales y cuotas todavía estimadas;
- calcula el tramo salarial restante del año actual como salario mensual actual por cuotas/meses todavía proyectados;
- para años futuros, limita el salario cotizado proyectado a la cantidad de cuotas esperadas;
- genera una línea temporal independiente por escenario salarial.

La equivalencia provisional de una cuota futura con un mes cotizado se utiliza únicamente para planificación anual. Los cálculos legales sensibles a fechas exactas deberán utilizar detalle mensual.

## Pendiente

Faltan los motores legales de:

- elegibilidad;
- SEBD;
- Subsistema Mixto;
- SUCGS.

También falta incorporar proyecciones por meses y fechas exactas para decisiones legales sensibles al momento de cotización.