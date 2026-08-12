# Modelo de datos

Los contratos principales se definen con Pydantic y están separados entre datos generales del asistente y datos/resultados previsionales.

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Ubicación

- `app/modelos/simulacion.py`: Pasos 1–5 y servicios comunes.
- `app/modelos/pension.py`: motores SEBD, Mixto, SUCGS y resultados integrados.

## 2. Criterios generales

- Fechas: formato ISO `YYYY-MM-DD` en API.
- Cuotas: enteros mensuales cuando el modelo representa cuotas acreditadas/proyectadas.
- Importes: se convierten a `Decimal` dentro de la lógica monetaria sensible aunque la representación externa de Pydantic pueda materializarse como número JSON.
- Campos no aplicables: `null`, no `0`, cuando cero podría confundirse con un valor matemático real.
- Pagos mensuales y pagos únicos: campos separados.
- Datos históricos y proyectados: estructuras y banderas de origen separadas.

## 3. Datos de cuotas

### 3.1. `DatosCuotas`

Representa la entrada del Paso 2:

- cuotas totales acreditadas;
- cuotas del año actual incluidas en el total;
- continuidad de cotización;
- cuotas esperadas al cierre del año actual;
- cuotas esperadas por año futuro.

### 3.2. `ResumenCuotas`

Devuelve:

- total informado;
- cuotas pendientes del año actual según expectativa;
- densidad futura;
- advertencias de consistencia.

## 4. Historial salarial

### 4.1. `RegistroHistorialSalarial`

Por año:

- año;
- cuotas;
- salario cotizado/reportado.

### 4.2. `DatosHistorialSalarial`

Agrupa registros y metadatos necesarios para validar el historial contra el Paso 2.

### 4.3. Resúmenes normalizados

El servicio de historial produce totales, clasifica años y conserva el origen real de los datos.

Estados habituales:

- cotización completa;
- cotización parcial;
- sin cotización.

## 5. Salario actual

Los modelos de salario conservan:

- monto original;
- periodicidad original;
- equivalentes normalizados;
- valor anual común utilizado para proyección.

Periodicidades soportadas:

- semanal;
- quincenal;
- mensual;
- anual.

## 6. Proyección salarial

Los modelos de proyección representan:

- modalidad;
- año inicial/final;
- tasa anual cuando aplica;
- salario futuro conocido cuando aplica;
- escenarios múltiples.

La salida contiene registros anuales de proyección y conserva precisión interna hasta materializar importes.

## 7. Línea temporal

La línea temporal combina:

- histórico real;
- año actual con componente real y, si procede, componente proyectado;
- años futuros proyectados.

Cada registro identifica su origen para que Resultados pueda distinguir salario real de supuesto futuro.

## 8. Retiro

### 8.1. `DatosRetiro`

Incluye:

- fecha de nacimiento;
- sexo;
- fecha de evaluación;
- fecha de corte de cuotas;
- cuotas informadas;
- cierre esperado del año actual;
- densidad futura;
- horizonte salarial;
- escenarios adicionales/personalizados.

### 8.2. `EscenarioRetiro`

Representa un escenario calculado con:

- etiqueta;
- fecha de retiro;
- edad;
- cuotas estimadas;
- cuotas nuevas desde el corte;
- meses desde el corte;
- cobertura del horizonte salarial;
- estado de selección/disponibilidad.

## 9. Modelos SEBD

### 9.1. `DatosCalculoSEBDNormal`

Entrada legal mínima para el cálculo normal.

### 9.2. `ResumenCalculoSEBDNormal`

Expone:

- elegibilidad;
- mejores años;
- salario base;
- tasa base e incrementos;
- límites;
- pensión mensual estimada;
- advertencias y fuente normativa.

### 9.3. `DatosCalculoSEBD`

Entrada general para clasificación de modalidad.

### 9.4. `ResumenCalculoSEBD`

Además de los campos comunes, puede contener:

- modalidad y tipo de prestación;
- factor proporcional de cuotas;
- factor de reducción por edad;
- indemnización: mensualidad hipotética, divisor, factor y pago único;
- campos `null` cuando una etapa no aplica a la modalidad.

### 9.5. Modelos de resultado integrado

`DatosResultadoSEBD*` y `ResumenResultadoSEBD*` unen Pasos 1–5 con el motor legal y agregan trazabilidad de escenario salarial/retiro.

## 10. Modelos del Subsistema Mixto

### 10.1. `DatosCalculoMixto`

Entrada principal del motor Mixto. Incluye:

- datos personales/retiro;
- cuotas;
- historial;
- saldo CAP;
- bono de reconocimiento;
- confirmación del bono;
- valor actuarial;
- opción de prestación CAP.

### 10.2. `AnioSeleccionadoMixtoBD`

Por año seleccionado para el componente BD:

- año;
- cuotas;
- salario cotizado original;
- salario considerado después del tope del componente.

### 10.3. `ResumenComponenteBeneficioDefinidoMixto`

Incluye:

- modalidad;
- salario base;
- tasa;
- máximo del componente;
- pensión mensual o indemnización BD;
- advertencia sobre aproximación anual del tope mensual.

### 10.4. `ResumenComponenteAhorroPersonalMixto`

Incluye:

- saldo CAP;
- bono;
- confirmación del bono;
- capital total;
- valor actuarial;
- opción solicitada;
- decisión pendiente;
- pensión programada;
- devolución disponible y pago único;
- garantía de renta vitalicia y condición de activación.

### 10.5. `ResumenCalculoMixto`

Consolida:

- estado del sistema;
- modalidad del componente BD;
- componentes BD/CAP;
- pensión mensual total;
- pagos únicos BD/CAP/total;
- transición a SUCGS;
- advertencias y fuente normativa.

### 10.6. Resultado integrado Mixto

`DatosResultadoMixto` y `ResumenResultadoMixto` reutilizan historial, línea temporal y escenario de retiro del asistente antes de invocar el motor.

## 11. Modelos SUCGS

### 11.1. `DatosCalculoSUCGS`

Entrada directa con:

- fecha de nacimiento;
- sexo;
- fecha de retiro;
- cuotas;
- saldo de Capitalización Solidaria;
- confirmación del saldo;
- valores solidarios vigentes/confirmados;
- inicio e historial laboral para artículo 197;
- confirmación de historial completo;
- estado de estabilidad salarial.

### 11.2. `ResumenCalculoSUCGS`

Separa tres niveles:

1. `pension_contributiva_mensual`;
2. `pension_despues_componente_solidario`;
3. `pension_mensual_total_estimada`.

También expone:

- edad y factor actuarial;
- divisor legal;
- tipo de prestación solidaria;
- complemento solidario;
- condiciones del artículo 197;
- cuotas de primeros 20 años/restantes;
- salario promedio base;
- tasa mínima;
- monto objetivo y complemento de garantía;
- estado de cálculo completo;
- advertencias y fuente normativa.

### 11.3. Resultado integrado SUCGS

`DatosResultadoSUCGS` y `ResumenResultadoSUCGS` reciben el estado de los Pasos 1–5, consolidan el historial hasta el retiro y añaden años proyectados cuando corresponda.

## 12. Origen y confirmación de datos

Los modelos diferencian datos calculables de datos que requieren fuente oficial:

- saldo CAP;
- bono de reconocimiento;
- divisor actuarial Mixto;
- saldo de Capitalización Solidaria;
- valores solidarios vigentes cuando hayan sido indexados;
- estabilidad salarial art. 197 cuando no pueda deducirse con seguridad.

Las banderas de confirmación permiten mostrar una estimación sin fingir que un dato fue certificado por la CSS.

## 13. Evolución prevista para 6F

El modelo transversal deberá poder representar una secuencia auditable común a los tres sistemas:

```text
dato de entrada
→ regla normativa
→ fórmula
→ sustitución numérica
→ resultado intermedio
→ redondeo
→ límite/garantía
→ resultado final
```

Esta estructura se diseñará para reutilizarse en la interfaz comparativa y en futuros informes PDF.


## Comparación transversal — 6F.1

`app/modelos/comparacion.py` define una capa normalizada que no sustituye los modelos de cada motor.

- `DatosComparacionEscenarios`: sistema, bloque integrado correspondiente, filtros de fechas de retiro y escenarios salariales.
- `FilaComparacionEscenario`: fecha, edad, cuotas, modalidad/prestación, pensión mensual, pago único, estado y diferencias contra la base.
- `ResumenComparacionEscenarios`: matriz completa, conteos, mejor pensión mensual comparable y advertencias globales.

Los pagos únicos y las pensiones mensuales permanecen en campos separados.


## 11. Trazabilidad 6F.2

`app/modelos/trazabilidad.py` define una representación transversal que no sustituye los modelos de cada motor:

- `DatoTrazabilidad`: dato, valor, origen y estado de confirmación;
- `PasoTrazabilidad`: regla, fórmula, sustitución, resultado, redondeo y fuentes;
- `FuenteTrazabilidad`: referencia oficial, artículos y URL;
- `ResumenTrazabilidadCalculo`: secuencia completa y resultado final tipificado.

Los modelos integrados `ResumenResultadoSEBD`, `ResumenResultadoMixto` y `ResumenResultadoSUCGS` incluyen `trazabilidad`. Esta propiedad es explicativa: el importe legal continúa proviniendo del campo `calculo` generado por el motor correspondiente.

## Resultado transversal 6F.4

`app/modelos/resultado_unificado.py` incorpora `ResumenPrestacionUnificada` con campos comunes a los tres sistemas:

- sistema y nombre visible;
- escenario de retiro y salarial;
- fecha, edad y cuotas;
- modalidad/código;
- estado del resultado;
- naturaleza de la prestación;
- pensión mensual estimada;
- pago único estimado;
- decisión requerida;
- datos no confirmados;
- advertencias.

Los modelos `ResumenResultadoSEBD`, `ResumenResultadoMixto` y `ResumenResultadoSUCGS` incluyen ahora `resumen_unificado`. El desglose específico continúa en `calculo` y la explicación en `trazabilidad`.

