# Motor de cálculo

## Principio general

La lógica de cálculo permanece separada de HTML y JavaScript. La interfaz captura y presenta; Python valida y calcula.

Los motores legales definitivos de SEBD, Subsistema Mixto y SUCGS todavía no forman parte de esta etapa.

## Precisión monetaria y redondeo

Archivo común:

```text
app/core/dinero.py
```

Criterio técnico general:

1. convertir valores monetarios relevantes a `Decimal`;
2. conservar precisión durante las operaciones;
3. evitar redondear valores intermedios únicamente para hacer coincidir cifras visibles;
4. materializar importes monetarios a dos decimales con `ROUND_HALF_UP`;
5. permitir que una regla normativa específica sustituya este criterio dentro del motor legal correspondiente.

Ejemplo de proyección:

```text
B/. 1,331.90 mensuales
→ B/. 15,982.80 anuales
→ crecimiento 1 %
→ B/. 16,142.628
→ resultado monetario: B/. 16,142.63
```

El salario mensual visible del mismo escenario puede ser B/. 1,345.22. No se vuelve a multiplicar ese valor ya redondeado por 12 para obtener el anual, porque introduciría un redondeo intermedio.

Los campos monetarios editables se limitan a dos decimales tanto en frontend como en la validación del backend.

## Análisis preliminar de cuotas

Archivo:

```text
app/servicios/proyeccion_cuotas.py
```

Comportamiento actual:

- valida que las cuotas del año actual no superen el total acreditado;
- diferencia cuotas reales de cuotas futuras;
- respeta las cuotas esperadas al cierre del año;
- si la persona no continuará cotizando, no agrega cuotas futuras;
- calcula faltantes preliminares para 180 y 240 cuotas;
- estima tiempo usando la densidad anual futura.

Los umbrales de 180 y 240 son referencias del asistente. La elegibilidad definitiva dependerá del sistema y prestación que determine el motor legal.

## Historial salarial

Archivo:

```text
app/servicios/historial_salarios.py
```

El servicio:

- valida el rango de años;
- rechaza años duplicados;
- valida coherencia entre cuotas y salario;
- clasifica registros como completos, parciales o sin cotización;
- detecta años sin registro;
- suma cuotas y salarios con precisión controlada;
- compara las cuotas identificadas con las cuotas reales del Paso 2.

El historial continúa siendo anual. Cuando una regla legal dependa del mes exacto, el motor correspondiente deberá utilizar una fuente con mayor granularidad o una aproximación explícitamente identificada.

## Normalización salarial

Archivo:

```text
app/servicios/proyeccion_salarios.py
```

Conversión mediante equivalente anual:

```text
semanal     = monto × 52
quincenal   = monto × 24
mensual     = monto × 12
anual       = monto
```

Las demás periodicidades se derivan del equivalente anual preciso.

## Proyección por porcentaje

Se utiliza crecimiento compuesto:

```text
salario_año_n = salario_base × (1 + tasa)^n
```

El año inicial conserva el salario base.

Los importes mensual y anual visibles se redondean de forma independiente desde el valor preciso del escenario.

## Salario futuro conocido

Cuando el usuario conoce un salario para un año futuro, se obtiene la tasa anual compuesta equivalente:

```text
tasa = (salario_futuro / salario_actual)^(1 / años) - 1
```

La tasa se utiliza para construir la serie anual. La implementación futura podrá aumentar aún más la precisión interna de esta modalidad si el motor legal lo necesita.

## Comparación de escenarios

La modalidad `ESCENARIOS` genera una serie independiente por porcentaje. La sugerencia inicial es:

```text
0 %, 1 %, 2 %, 3 %
```

Los porcentajes introducidos admiten como máximo dos decimales.

## Línea temporal histórica y proyectada

Archivo:

```text
app/servicios/linea_tiempo.py
```

La línea temporal:

- mantiene separados valores históricos y proyectados;
- usa `SIN_COTIZACION` cuando un año histórico tiene cero cuotas;
- representa el año actual como histórico, parcial o mixto según corresponda;
- respeta las cuotas esperadas al cierre del año actual;
- limita el salario futuro al número de cuotas proyectadas;
- conserva la precisión anual producida por el motor salarial.

La equivalencia provisional entre una cuota futura y un mes cotizado se utiliza para planificación cuando no existe detalle mensual.

## Escenarios de retiro

Archivo:

```text
app/servicios/retiro.py
```

El servicio trabaja con fechas exactas para edad y fecha de referencia.

### Fecha de evaluación y fecha de corte de cuotas

Son conceptos distintos:

- **fecha de evaluación:** día en que se analiza la situación previsional;
- **fecha de corte de cuotas:** día hasta el cual se consideran actualizadas las cuotas reales informadas.

### Cuotas futuras

La estimación evita aplicar directamente la densidad anual al resto del año actual. Primero respeta:

```text
cuotas restantes año actual =
max(cuotas esperadas al cierre - cuotas ya acreditadas este año, 0)
```

A partir del siguiente año se aplica `cuotas_esperadas_por_anio`, prorrateando el año de retiro cuando la fecha evaluada cae dentro del año.

Por tanto, si el usuario tiene 5 cuotas en 2026 y espera cerrar 2026 con 5, un retiro en noviembre de 2026 no agrega tres cuotas artificiales.

### Horizonte salarial

Cada escenario de retiro se compara con `anio_fin_proyeccion_salarial`.

Si una fecha de retiro excede ese horizonte:

- el backend devuelve una advertencia;
- la interfaz ofrece ajustar el Paso 4;
- no se extiende silenciosamente el salario con una hipótesis no confirmada.

## Pendiente

Faltan los motores legales completos de:

- elegibilidad;
- SEBD;
- Subsistema Mixto;
- SUCGS.

También queda pendiente incorporar detalle mensual/importación cuando sea necesario para reglas sensibles al mes exacto.
