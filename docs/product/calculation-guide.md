# Cómo se calcula — contrato de transparencia

**Estado:** vigente
**Versión de aplicación revisada:** `0.1.10.01-beta`
**Sección pública:** `/como-se-calcula`
**Clasificación:** Producto / Transparencia / Normativa

## 1. Propósito

La sección pública **Cómo se calcula** permite comprender y reproducir manualmente el orden general de las reglas implementadas para SEBD, Subsistema Mixto y SUCGS.

No constituye un motor alternativo. Las fórmulas ejecutables continúan exclusivamente en Python; la vista pública describe el procedimiento y lee parámetros versionados desde `regulations/` por medio de `app/services/calculation_guide.py`.

## 2. Contrato común

El orden explicativo es:

```text
Datos personales
→ cuotas acreditadas y futuras
→ historial salarial y salario normalizado
→ proyección salarial y línea temporal
→ fecha/edad/cuotas del escenario de retiro
→ clasificación de modalidad
→ salario base / saldo aplicable
→ tasa o factor
→ fórmula
→ límites / garantías
→ resultado y advertencias
```

R1.2 hace visible la transformación intermedia: normalización semanal/quincenal/mensual/anual, cierre de cuotas del año actual, crecimiento compuesto, prorrateo del salario proyectado según cuotas previstas y estimación de cuotas hasta la fecha de retiro. Estas expresiones describen servicios existentes y no constituyen una segunda implementación ejecutable.

La trazabilidad individual del Paso 6 conserva el contrato complementario:

```text
dato → regla → fórmula → sustitución → resultado
```

La página pública explica el procedimiento general; no transporta datos personales ni recalcula una simulación.

## 3. SEBD

La guía documenta:

- edad de referencia por sexo desde parámetros generales;
- 240 cuotas de referencia y 180 cuotas como umbral proporcional modelado;
- selección de mejores años para el salario base;
- tasa base de 60 %;
- incrementos por bloques completos de 12 cuotas antes y después de la referencia;
- proporcionalidad por cuotas cuando corresponde;
- reducción anticipada por la tabla mensual versionada;
- máximos ordinario/ampliados;
- Indemnización por Vejez como pago único separado.

La fórmula explicativa central es:

```text
monto inicial = salario base × tasa de reemplazo
```

Los factores de modalidad se aplican únicamente cuando la clasificación los requiere.

## 4. Subsistema Mixto

La guía conserva separados:

```text
Componente de Beneficio Definido + Componente de Ahorro Personal
```

El BD usa parámetros propios del Mixto. El CAP requiere saldo, bono aplicable y valor actuarial individualizado. La pensión programada se explica como:

```text
(saldo CAP + bono aplicable) ÷ valor actuarial
```

No se reconstruye un saldo CAP real desde salarios anuales. La devolución total se mantiene como pago único y como decisión explícita cuando la regla aplicable la permite.

La frontera operativa versionada Mixto→SUCGS permanece visible; no se armoniza silenciosamente la discrepancia normativa documentada.

## 5. SUCGS

La guía presenta el cálculo por capas:

1. componente contributivo;
2. componente solidario;
3. garantía de reemplazo mínimo, cuando puede cerrarse.

El componente contributivo se explica como:

```text
saldo ÷ 1,000 × factor actuarial por edad
```

La tabla actuarial mostrada proviene de `regulations/sucgs.json`. Los valores monetarios solidarios son referencias versionadas y no se describen como vigentes indefinidamente.

La garantía del artículo 197 conserva sus condiciones evaluables y la estabilidad salarial sigue requiriendo confirmación explícita cuando corresponde.

## 6. Ejemplos

Los ejemplos visibles son ilustrativos y no contienen casos personales versionados. Un parámetro inventado para explicar una operación —por ejemplo, un divisor actuarial hipotético— debe marcarse expresamente como no oficial.

Los ejemplos no declaran elegibilidad ni reemplazan la evaluación de los motores.

## 7. Fuentes

Las fuentes oficiales no se duplican en la plantilla. La vista reutiliza `construir_catalogo_metodologia()` y enlaza a `/metodologia`, que obtiene URLs desde los JSON normativos versionados.

## 8. Vinculación con resultados

Después de obtener un resultado, el Paso 6 ofrece **Ver cómo se obtuvo este cálculo**. La acción dirige a la sección del sistema correspondiente sin transferir PII, salarios, cuotas ni montos personales en la URL.

El desglose individual con cifras reales permanece en **Ver cálculo completo** dentro del Paso 6.

## 9. Presentación y navegación

La navegación principal incluye un acceso directo **Cómo se calcula**. La página usa estado activo propio, separado de **Fuentes**.

Los importes monetarios visibles en esta guía se presentan como `B/.1,500.00`: separador de miles y dos decimales. Los factores técnicos conservan su precisión propia.

En escritorio amplio, la tabla SEBD de 24 factores usa ocho columnas para ocupar tres filas y la tabla SUCGS usa diez columnas para reducir su altura. En anchos menores ambas degradan de forma responsive. Los estilos dependen de tokens semánticos para funcionar en Claro, Oscuro y Alto contraste.

## 10. Mantenimiento

Un cambio en fórmula, factor, umbral, clasificación o fuente normativa debe revisar conjuntamente:

- motor Python;
- `regulations/*.json`;
- trazabilidad;
- sección pública Cómo se calcula;
- pruebas;
- documentación técnica/funcional relacionada.

La guía no puede adelantarse a una regla que el motor todavía no implemente ni presentar como oficial un parámetro pendiente de confirmación.
## R1.3 — fórmula, sustitución y vocabulario

Cada fórmula pública se conserva en forma general y puede ir seguida de una sustitución numérica marcada como **Ejemplo**. Estas cifras son ilustrativas: ayudan a leer el orden de operaciones, pero no reemplazan la sustitución personal que Paso 6 muestra en **Ver cálculo completo**.

La guía define los términos junto al sistema donde aparecen en lugar de mantener un glosario separado: SEBD aclara modalidad, salario base, tasa de reemplazo y factor de reducción; Mixto aclara componente, BD, CAP, saldo CAP, tasa resultante, pensión programada CAP, bono de reconocimiento, valor actuarial y prestación Mixto; SUCGS aclara saldo, componente contributivo, factor actuarial, capa solidaria, PGS, garantía de reemplazo, salario promedio base y valor mínimo universal.

También se hace visible la tasa anual equivalente utilizada cuando el usuario aporta un salario futuro conocido y la conversión de meses completos a cuotas en una fracción de año. La implementación continúa siendo explicativa: no ejecuta un segundo cálculo de pensión.

## Cierre de UX.4.6i

La etiqueta visible que acompaña cada sustitución numérica se normaliza como **Ejemplo**. La fórmula general permanece visible inmediatamente antes para mantener la distinción entre regla y sustitución.
