# Motor de cálculo

Este documento describe el flujo técnico de cálculo. Las reglas legales detalladas se documentan en [NORMATIVA.md](NORMATIVA.md) y sus fuentes oficiales en [FUENTES_NORMATIVAS.md](FUENTES_NORMATIVAS.md).

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Principio general

La aplicación separa cuatro capas:

1. **entrada del Asegurado(a)**;
2. **servicios de normalización/proyección**;
3. **motor previsional**;
4. **presentación del resultado**.

JavaScript no implementa las fórmulas legales principales. El cálculo se ejecuta en Python.

## 2. Precisión monetaria

Regla general:

- usar `Decimal` en operaciones sensibles;
- conservar precisión interna;
- redondear al materializar un importe;
- usar `ROUND_HALF_UP` a dos decimales salvo norma específica.

No se redondean valores intermedios para hacer coincidir artificialmente una cifra visible.

## 3. Cuotas

El análisis del Paso 2 recibe:

- cuotas totales;
- cuotas del año actual;
- continuidad;
- cuotas esperadas al cierre del año;
- densidad futura.

La proyección de retiro usa primero el cierre del año actual y aplica la densidad futura a partir del año siguiente. Esto evita añadir cuotas en el año actual contra lo declarado por el Asegurado(a).

## 4. Historial y salario actual

El historial anual almacena:

```text
año + cuotas + salario cotizado
```

El salario actual se almacena separadamente y se normaliza mediante un valor anual común.

Las periodicidades soportadas son semanal, quincenal, mensual y anual.

## 5. Proyección salarial

### 5.1. Salario constante

Mantiene el salario mensual normalizado durante el horizonte.

### 5.2. Porcentaje anual

Aplica crecimiento compuesto sin redondear el salario intermedio antes de tiempo.

### 5.3. Salario futuro conocido

Deriva una trayectoria anual coherente entre el salario actual y el valor objetivo.

### 5.4. Escenarios múltiples

Genera varias trayectorias futuras sobre un único historial real.

## 6. Línea temporal

El servicio combina:

- histórico real;
- año actual real/proyectado;
- futuro proyectado.

Si un año futuro tiene menos de 12 cuotas, el salario cotizado proyectado se limita a los meses/cuotas proyectados.

## 7. Escenarios de retiro

El motor de retiro calcula:

- fecha de referencia;
- edad exacta;
- meses desde el corte;
- cuotas nuevas;
- cuotas totales estimadas;
- cobertura del horizonte salarial.

Un escenario posterior al último año salarial proyectado queda advertido como incompleto hasta ampliar el Paso 4.

## 8. Integración con Resultados

Los servicios `resultados_*.py` consolidan los Pasos 1–5 antes de invocar un motor legal.

Responsabilidades:

- escoger el escenario de retiro seleccionado;
- escoger el escenario salarial;
- combinar historial y proyección hasta la fecha de retiro;
- identificar años proyectados;
- preparar cuotas antes/después de referencia cuando puedan determinarse;
- agregar advertencias de aproximación.

## 9. Motor SEBD

### 9.1. Clasificación

El clasificador general decide entre:

- Normal;
- Anticipada;
- Proporcional;
- Proporcional Anticipada;
- Indemnización por Vejez;
- No elegible;
- transición SUCGS cuando corresponda.

### 9.2. Salario base

Se seleccionan los mejores años requeridos por la modalidad/regla y se obtiene el promedio mensual correspondiente.

Con historial anual, un año parcial conserva su monto real y no se anualiza artificialmente.

### 9.3. Pensión Normal

Esquema general:

```text
tasa = 60 %
     + 1.25 puntos por cada bloque completo de 12 cuotas excedentes antes de referencia
     + 2 puntos por cada bloque completo de 12 cuotas posteriores a referencia y excedentes

pensión antes de límite = salario base × tasa
pensión = aplicar máximo cuando corresponda
```

La separación de cuotas antes/después de referencia no se infiere silenciosamente cuando el historial no tiene granularidad suficiente.

### 9.4. Anticipada

Después del cálculo base y límites:

```text
pensión anticipada = monto previo × factor mensual de edad
```

El factor se consulta en `normativa/sebd.json`.

### 9.5. Proporcional

```text
factor cuotas = cuotas / 240
pensión proporcional = monto base aplicable × factor cuotas
```

### 9.6. Proporcional Anticipada

Aplica tanto el factor de cuotas como el factor de edad.

### 9.7. Indemnización por Vejez

La salida es de pago único:

```text
mensualidad hipotética
× (meses/cuotas acreditados / 6)
= indemnización estimada
```

Los campos propios de pensión proporcional no aplicables se devuelven como `null`.

Desde 01/03/2036, el motor no calcula esta indemnización y deriva el caso al SUCGS según el artículo 186.

## 10. Motor del Subsistema Mixto

### 10.1. Componente BD

El motor transforma el historial al tramo participante del Mixto:

```text
salario considerado BD del año
= mínimo(salario cotizado del año, B/.500 × cuotas del año)
```

Con datos anuales, esta es una aproximación del límite mensual y se advierte al Asegurado(a).

Después se reutiliza la lógica de modalidad SEBD con parámetros propios del componente.

### 10.2. Componente CAP — pensión programada

```text
capital total = saldo CAP + bono aplicable
pensión CAP = capital total / valor actuarial
```

Si falta el valor actuarial, la pensión CAP permanece pendiente.

### 10.3. Opción CAP

- `PENSION_PROGRAMADA`: calcula renta mensual si están los datos.
- `DEVOLUCION_TOTAL`: produce pago único.
- `AUTO`: mantiene `decision_requerida = true` cuando corresponde escoger.

### 10.4. Resultado total

Cuando ambos componentes generan renta:

```text
pensión Mixto = pensión BD + pensión CAP
```

Cuando existe una devolución o indemnización, los pagos únicos se mantienen separados.

### 10.5. Garantía de renta vitalicia

La garantía del CAP no incrementa el monto inicial. Solo registra la continuidad futura del componente cuando se cumplen las condiciones de agotamiento del capital y supervivencia a la expectativa utilizada.

### 10.6. Transición

Hasta 29/02/2032 se permite cálculo Mixto según el alcance implementado. Desde 01/03/2032 el servicio devuelve transición a SUCGS conforme a la regla operativa versionada.

## 11. Motor SUCGS

### 11.1. Componente contributivo — artículo 196

```text
pensión contributiva
= saldo de Capitalización Solidaria / 1,000 × factor actuarial por edad
```

El factor se obtiene de `normativa/sucgs.json`.

### 11.2. Capa solidaria — artículos 194 y 195

El motor obtiene primero `pension_contributiva_mensual` y después determina si corresponde:

- mantener la contributiva;
- elevar a Beneficio Mínimo;
- elevar a Pensión Garantizada Solidaria.

Se conserva:

```text
pension_contributiva_mensual
pension_despues_componente_solidario
```

como resultados separados.

### 11.3. Artículo 197 — condiciones

La preevaluación verifica:

1. mínimo de cuotas por año activo;
2. total máximo de años sin cotización;
3. máximo de años sin cotización consecutivos;
4. distribución mínima de cuotas entre primeros 20 años y años restantes;
5. estabilidad salarial, cuando existe confirmación suficiente.

### 11.4. Salario promedio base

```text
salario promedio base mensual
= total de salarios cotizados / total de meses cotizados
```

### 11.5. Monto objetivo

Con garantía completa:

```text
objetivo = salario promedio base × 60 %
```

Cuando la implementación permite garantía proporcional para un requisito inferior:

```text
tasa proporcional = 60 % × cuotas / 240
objetivo = salario promedio base × tasa proporcional
```

### 11.6. Resultado final

Si la garantía puede evaluarse:

```text
pensión total
= máximo(pensión después de capa solidaria, monto objetivo art. 197)
```

Si una condición indispensable permanece pendiente, `pension_mensual_total_estimada` permanece `null`.

## 12. Limitaciones explícitas

El motor actual no debe ocultar estas limitaciones:

- historial anual en lugar de mensual para ciertas reglas;
- mínimo SEBD indexado no versionado por fecha;
- saldo CAP Mixto no reconstruido desde agregados anuales;
- divisor actuarial Mixto debe ser suministrado cuando corresponda;
- bono Mixto no se reconstruye automáticamente;
- saldo SUCGS no se reconstruye todavía desde todos los aportes/rendimientos;
- valores solidarios pueden requerir actualización por indexación;
- estabilidad salarial del artículo 197 puede requerir confirmación explícita;
- regímenes especiales no están cubiertos por el motor general.

## 13. Capa explicativa 6F.2

La función de 6F.2 es explicar, no recalcular. `app/servicios/trazabilidad.py` recibe los resultados integrados y construye una secuencia: dato → regla → fórmula → sustitución → resultado intermedio → redondeo/condición → resultado final.

La capa usa los valores ya producidos por SEBD, Mixto y SUCGS. Por diseño, una divergencia entre la traza y el motor debe corregirse en la traza; nunca se introduce una segunda fórmula legal en JavaScript.

Las fuentes enlazadas se leen de `normativa/sebd.json`, `normativa/mixto.json` y `normativa/sucgs.json`.

## 14. Resultado transversal 6F.4

`app/servicios/resultado_unificado.py` recibe el resultado integrado ya calculado y normaliza únicamente conceptos comunes:

- estado del cálculo;
- naturaleza de la prestación;
- pensión mensual;
- pago único;
- modalidad;
- escenario;
- decisión pendiente;
- datos no confirmados;
- advertencias.

No contiene fórmulas legales. El comparador y la interfaz pueden consumir este contrato común sin conocer la estructura interna específica de cada motor.

## 15. Estado del bloque 6F

6F.1–6F.4 están completados para el alcance actual: comparación, trazabilidad, metodología/fuentes y unificación transversal. Las ampliaciones posteriores deben reutilizar estas capas y no duplicar cálculos previsionales.

