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

## 5. Detalle salarial del año actual

UX.4.4 agrega contratos opcionales que no sustituyen el historial anual:

- `DatosDetalleAnioActual`: año, modo `MENSUAL`/`QUINCENAL`, referencia de cuotas del Paso 2 y meses disponibles;
- `RegistroDetalleAnioActual`: mes, cuota acreditada, estado del salario y valores mensual/quincenales;
- `ResumenDetalleAnioActual`: salario disponible, salario acreditado, cuotas identificadas, último mes acreditado, último mes completo, bases salariales sugeridas y promedio del salario acreditado por cuota.

Estados de salario reciente:

- `SIN_INFORMACION`;
- `PARCIAL`;
- `COMPLETO`.

La acreditación de cuota es una bandera independiente del estado salarial. Por ello un mes completo puede todavía no tener cuota acreditada y un mes parcial puede tener una cuota ya contabilizada en una fotografía histórica.

La sincronización con el historial anual solo se considera coherente cuando las cuotas marcadas en el detalle coinciden con `cuotas_anio_actual` del Paso 2.

## 6. Salario actual / base de proyección

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



### Importación revisable

`ResumenReferenciaMiRetiroSeguro` conserva la referencia personal y filas anuales detectadas sin identificadores directos innecesarios. `ResumenFichaDigital` contiene únicamente registros del año calendario actual mediante `RegistroFichaDigital` (`anio`, `mes`, `salario` y estado inicial del salario). Los períodos de años anteriores detectados en el PDF se descartan antes de construir el contrato.

En el navegador se distinguen dos estados adicionales: `importacion_comprobante_confirmada` y `importacion_ficha_digital_confirmada`. La detección previa a la confirmación no se persiste. Después de confirmar una Ficha Digital, los registros del año actual se traducen a `DatosDetalleAnioActual` y la marca `cuota_acreditada` procede exclusivamente de la decisión revisada por el Asegurado(a).


## 7. Proyección salarial

Los modelos de proyección representan:

- modalidad;
- año inicial/final;
- tasa anual cuando aplica;
- salario futuro conocido cuando aplica;
- escenarios múltiples.

La salida contiene registros anuales de proyección y conserva precisión interna hasta materializar importes.

## 8. Línea temporal

La línea temporal combina:

- histórico real;
- año actual con componente real y, si procede, componente proyectado;
- años futuros proyectados.

Cada registro identifica su origen para que Resultados pueda distinguir salario real de supuesto futuro.

## 9. Retiro

### 9.1. `DatosRetiro`

Incluye:

- fecha de nacimiento;
- sexo;
- fecha de evaluación;
- `ultimo_mes_cuotas` (`YYYY-MM`) como dato visible preferente en UX.3;
- `fecha_corte_cuotas` como fecha técnica exacta y campo de compatibilidad;
- cuotas informadas;
- cierre esperado del año actual;
- densidad futura;
- horizonte salarial;
- escenarios adicionales/personalizados.

Cuando `ultimo_mes_cuotas` está presente, el servicio convierte ese mes al último día calendario. Si corresponde al mismo mes de la fecha de evaluación, el corte se limita al día de evaluación. Esto evita fingir precisión diaria en un dato que el Asegurado(a) aporta con granularidad mensual.

### 9.2. `EscenarioRetiro`

Representa un escenario calculado con:

- etiqueta;
- fecha de retiro;
- edad;
- cuotas estimadas;
- cuotas nuevas desde el corte;
- meses desde el corte;
- cobertura del horizonte salarial;
- estado de selección/disponibilidad.

## 10. Modelos SEBD

### 10.1. `DatosCalculoSEBDNormal`

Entrada legal mínima para el cálculo normal.

### 10.2. `ResumenCalculoSEBDNormal`

Expone:

- elegibilidad;
- mejores años;
- salario base;
- tasa base e incrementos;
- límites;
- pensión mensual estimada;
- advertencias y fuente normativa.

### 10.3. `DatosCalculoSEBD`

Entrada general para clasificación de modalidad.

### 10.4. `ResumenCalculoSEBD`

Además de los campos comunes, puede contener:

- modalidad y tipo de prestación;
- factor proporcional de cuotas;
- factor de reducción por edad;
- indemnización: mensualidad hipotética, divisor, factor y pago único;
- campos `null` cuando una etapa no aplica a la modalidad.

### 10.5. Modelos de resultado integrado

`DatosResultadoSEBD*` y `ResumenResultadoSEBD*` unen Pasos 1–5 con el motor legal y agregan trazabilidad de escenario salarial/retiro.

## 11. Modelos del Subsistema Mixto

### 11.1. `DatosCalculoMixto`

Entrada principal del motor Mixto. Incluye:

- datos personales/retiro;
- cuotas;
- historial;
- saldo CAP;
- bono de reconocimiento;
- confirmación del bono;
- valor actuarial;
- opción de prestación CAP.

### 11.2. `AnioSeleccionadoMixtoBD`

Por año seleccionado para el componente BD:

- año;
- cuotas;
- salario cotizado original;
- salario considerado después del tope del componente.

### 11.3. `ResumenComponenteBeneficioDefinidoMixto`

Incluye:

- modalidad;
- salario base;
- tasa;
- máximo del componente;
- pensión mensual o indemnización BD;
- advertencia sobre aproximación anual del tope mensual.

### 11.4. `ResumenComponenteAhorroPersonalMixto`

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

### 11.5. `ResumenCalculoMixto`

Consolida:

- estado del sistema;
- modalidad del componente BD;
- componentes BD/CAP;
- pensión mensual total;
- pagos únicos BD/CAP/total;
- transición a SUCGS;
- advertencias y fuente normativa.

### 11.6. Resultado integrado Mixto

`DatosResultadoMixto` y `ResumenResultadoMixto` reutilizan historial, línea temporal y escenario de retiro del asistente antes de invocar el motor.

## 12. Modelos SUCGS

### 12.1. `DatosCalculoSUCGS`

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

### 12.2. `ResumenCalculoSUCGS`

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

### 12.3. Resultado integrado SUCGS

`DatosResultadoSUCGS` y `ResumenResultadoSUCGS` reciben el estado de los Pasos 1–5, consolidan el historial hasta el retiro y añaden años proyectados cuando corresponda.

## 13. Origen y confirmación de datos

Los modelos diferencian datos calculables de datos que requieren fuente oficial:

- saldo CAP;
- bono de reconocimiento;
- divisor actuarial Mixto;
- saldo de Capitalización Solidaria;
- valores solidarios vigentes cuando hayan sido indexados;
- estabilidad salarial art. 197 cuando no pueda deducirse con seguridad.

Las banderas de confirmación permiten mostrar una estimación sin fingir que un dato fue certificado por la CSS.

## 14. Evolución prevista para 6F

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


## 15. Comparación transversal — 6F.1

`app/modelos/comparacion.py` define una capa normalizada que no sustituye los modelos de cada motor.

- `DatosComparacionEscenarios`: sistema, bloque integrado correspondiente, filtros de fechas de retiro y escenarios salariales.
- `FilaComparacionEscenario`: fecha, edad, cuotas, modalidad/prestación, pensión mensual, pago único, estado y diferencias contra la base.
- `ResumenComparacionEscenarios`: matriz completa, conteos, mejor pensión mensual comparable y advertencias globales.

Los pagos únicos y las pensiones mensuales permanecen en campos separados.


## 16. Trazabilidad 6F.2

`app/modelos/trazabilidad.py` define una representación transversal que no sustituye los modelos de cada motor:

- `DatoTrazabilidad`: dato, valor, origen y estado de confirmación;
- `PasoTrazabilidad`: regla, fórmula, sustitución, resultado, redondeo y fuentes;
- `FuenteTrazabilidad`: referencia oficial, artículos y URL;
- `ResumenTrazabilidadCalculo`: secuencia completa y resultado final tipificado.

Los modelos integrados `ResumenResultadoSEBD`, `ResumenResultadoMixto` y `ResumenResultadoSUCGS` incluyen `trazabilidad`. Esta propiedad es explicativa: el importe legal continúa proviniendo del campo `calculo` generado por el motor correspondiente.

## 17. Resultado transversal 6F.4

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



### Referencia personal importada

- `RegistroReferenciaMiRetiroSeguro`: año, edad, tipo histórico/proyectado, salario anual y cuotas extraídos de una fila del comprobante.
- `ResumenReferenciaMiRetiroSeguro`: fecha del comprobante, datos mínimos de compatibilidad, sistema elegido, edad de retiro, cuotas históricas, naturaleza y monto estimado de prestación, total de cuotas acumuladas, filas anuales y advertencias.
- El modelo excluye nombre, cédula, número de seguro social ni código único del documento. El PDF original no forma parte del estado persistido.
