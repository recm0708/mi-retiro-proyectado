# Modelo de datos

## Ubicación

Los modelos Pydantic se encuentran en:

```text
app/modelos/simulacion.py
```

## Precisión de entrada

Los campos monetarios y porcentuales editables relevantes validan un máximo de dos decimales en el backend. La interfaz aplica la misma restricción para ofrecer retroalimentación inmediata, pero Python conserva la validación autoritativa.

## Cuotas

### `DatosCuotas`

Contiene:

- `cuotas_totales`;
- `cuotas_anio_actual`;
- `continua_cotizando`;
- `cuotas_esperadas_cierre_anio`;
- `cuotas_esperadas_por_anio`.

### `ResumenCuotas`

Contiene cuotas reales, cierre proyectado, faltantes preliminares y estimaciones de tiempo.

## Historial salarial

### `RegistroHistorialSalarial`

Representa un año calendario:

- `anio`;
- `cuotas`;
- `salario_cotizado`.

`salario_cotizado` es el total reportado durante ese año, no un salario anualizado de doce meses.

### `RegistroHistorialNormalizado`

Estados:

```text
SIN_COTIZACION
HISTORICO_PARCIAL
HISTORICO_COMPLETO
```

### `DatosHistorialSalarial`

Contiene rango de años, cuotas de referencia y registros.

### `ResumenHistorialSalarial`

Incluye:

- cuotas sumadas;
- diferencia respecto de referencia;
- indicador de coincidencia;
- años sin registro;
- total salarial reportado;
- último año con cuotas;
- último salario cotizado.

## Salario actual

### `DatosSalario`

Contiene monto y periodicidad:

```text
SEMANAL
QUINCENAL
MENSUAL
ANUAL
```

### `ResumenSalario`

Conserva la entrada original y agrega equivalentes semanal, quincenal, mensual y anual.

## Proyección salarial

### `DatosProyeccionSalario`

Contiene:

- salario mensual base;
- año inicial y final;
- modalidad;
- porcentaje anual opcional;
- salario futuro conocido opcional;
- año del salario futuro;
- lista de porcentajes para escenarios.

Modalidades:

```text
CONSTANTE
PORCENTAJE
FUTURO_CONOCIDO
ESCENARIOS
```

### `ProyeccionSalarioAnual`

Registra año, salario mensual, salario anual y crecimiento acumulado.

### `EscenarioProyeccionSalario`

Agrupa una tasa y sus registros.

### `ResumenProyeccionSalario`

Agrupa modalidad, período y escenarios.

## Línea temporal

### `RegistroLineaTiempo`

Separa por año:

- cuotas históricas;
- salario histórico;
- cuotas proyectadas;
- salario proyectado;
- cuotas al cierre;
- salario al cierre;
- estado.

Estados:

```text
HISTORICO
HISTORICO_PARCIAL
SIN_COTIZACION
MIXTO
PROYECTADO
PENDIENTE
```

### `DatosLineaTiempo`

Integra historial, cuotas, salario actual y proyección.

### `ResumenLineaTiempo`

Devuelve período y escenarios integrados.

## Retiro

### `DatosRetiro`

Contiene:

- `fecha_nacimiento`;
- `sexo`;
- `fecha_corte`;
- `fecha_corte_cuotas`;
- `cuotas_reales`;
- `cuotas_anio_actual`;
- `continua_cotizando`;
- `cuotas_esperadas_cierre_anio`;
- `cuotas_esperadas_por_anio`;
- `anio_fin_proyeccion_salarial`;
- `anios_adicionales`;
- `fecha_retiro_personalizada`.

La fecha de evaluación y la fecha de corte de cuotas se mantienen separadas porque un reporte puede estar actualizado hasta un día anterior al de la simulación.

### `EscenarioRetiro`

Representa una fecha posible y contiene:

- tipo y nombre;
- fecha de retiro;
- edad en esa fecha;
- meses calendario desde el corte de cuotas;
- cuotas adicionales estimadas;
- cuotas totales estimadas;
- indicador de fecha transcurrida.

### `ResumenRetiro`

Incluye:

- fecha de evaluación;
- fecha de corte de cuotas;
- edad actual;
- edad y fecha de referencia;
- situación respecto de la referencia;
- escenarios;
- método de estimación;
- año final de la proyección salarial;
- indicador de cobertura del horizonte;
- advertencias.

El resumen no equivale a una decisión legal de elegibilidad.

## Evolución prevista

El modelo deberá ampliarse para incorporar:

- detalle mensual de cotización cuando sea necesario;
- determinación legal de elegibilidad;
- resultados por sistema previsional;
- desglose de componentes de pensión;
- persistencia voluntaria.

## Modelos del motor SEBD

`app/modelos/pension.py` incorpora:

- `DatosCalculoSEBDNormal`;
- `AnioSeleccionadoSEBD`;
- `ResumenCalculoSEBDNormal`.

El resultado conserva por separado elegibilidad, edad, cuotas, años utilizados para la base salarial, porcentajes adicionales, límite máximo y advertencias normativas.

## Modelos de integración del Paso 6

`app/modelos/pension.py` también incorpora:

- `DatosResultadoSEBDNormal`;
- `ResumenResultadoSEBDNormal`.

`DatosResultadoSEBDNormal` recibe la fecha de nacimiento y sexo, el historial anual validado, la línea temporal salarial, el resumen de retiro, la fecha de retiro seleccionada y el nombre del escenario salarial.

`ResumenResultadoSEBDNormal` conserva:

- el escenario de retiro efectivamente utilizado;
- el escenario salarial utilizado;
- los años proyectados incorporados al cálculo;
- advertencias propias de la integración;
- el `ResumenCalculoSEBDNormal` producido por el motor legal.

El estado temporal de `sessionStorage` incorpora además:

- `escenario_retiro_seleccionado`;
- `escenario_salarial_seleccionado`;
- `resultado_sebd_normal`.

Estos campos se invalidan cuando cambian datos de origen de los Pasos 1–5.


## Modelos generales SEBD

`app/modelos/pension.py` incorpora:

- `DatosCalculoSEBD`;
- `ResumenCalculoSEBD`;
- `DatosResultadoSEBD`;
- `ResumenResultadoSEBD`.

El resumen general añade, entre otros, `modalidad`, `tipo_prestacion`, `factor_proporcional_cuotas`, `factor_reduccion_edad`, `meses_anticipacion_referencia` y `calculo_disponible`.

En modalidades donde un campo no tiene significado jurídico o matemático, la API usa `null` en vez de un cero artificial. En particular, la Indemnización por Vejez devuelve `factor_proporcional_cuotas = null` y `monto_despues_factor_proporcional = null`, porque el factor proporcional corresponde a las pensiones proporcionales y no al pago único.

Para `modalidad = INDEMNIZACION`, `ResumenCalculoSEBD` utiliza campos separados de la pensión mensual:

- `indemnizacion_mensualidad_hipotetica`;
- `indemnizacion_factor_cuotas`;
- `indemnizacion_divisor_cuotas`;
- `indemnizacion_pago_unico_estimado`.

En este caso `pension_mensual_estimada` permanece en `None`, evitando que un pago único se interprete como renta mensual.

`TipoEscenarioRetiro` incorpora también `ANTICIPADO` y el Paso 5 admite escenarios estándar `-2` y `-1` años respecto de la edad de referencia.


## Modelos del Subsistema Mixto

`app/modelos/pension.py` incorpora los modelos preliminares:

- `DatosCalculoMixto`;
- `AnioSeleccionadoMixtoBD`;
- `ResumenComponenteBeneficioDefinidoMixto`;
- `ResumenComponenteAhorroPersonalMixto`;
- `ResumenCalculoMixto`.

### `DatosCalculoMixto`

Mantiene separados los datos generales del retiro y los datos específicos del CAP:

- `sistema_seleccionado`: `MIXTO` o `SUCGS`;
- `saldo_ahorro_personal`: saldo efectivo de la cuenta cuando esté disponible;
- `bono_reconocimiento`: suma adicional aplicable al CAP;
- `valor_actuarial_expectativa_vida`: divisor oficial utilizado para convertir capital en pensión programada.

Los campos CAP son opcionales para permitir analizar el componente BD aun cuando el usuario todavía no tenga disponibles todos los parámetros actuariales.

### Componente BD

`AnioSeleccionadoMixtoBD` conserva simultáneamente:

- salario cotizado original;
- salario considerado por el componente BD después de aplicar el límite de participación;
- cuotas del año.

Esto permite auditar cuánto del salario anual se utiliza en la parte definida.

### Componente CAP

`ResumenComponenteAhorroPersonalMixto` conserva:

- saldo de ahorro personal;
- bono de reconocimiento;
- capital total considerado;
- valor actuarial;
- pensión programada;
- advertencias de datos faltantes.

No se modela un máximo mensual para este componente.

### Resumen Mixto

`ResumenCalculoMixto` distingue:

- sistema solicitado;
- estado del sistema;
- vigencia temporal del cálculo Mixto;
- modalidad de retiro;
- disponibilidad de cada componente;
- pensión mensual total únicamente cuando ambos componentes están disponibles;
- advertencias y fuente normativa.

## Extensión del modelo Mixto — 6D.2

`DatosCalculoMixto` incorpora:

```text
opcion_prestacion_cap:
  AUTO | PENSION_PROGRAMADA | DEVOLUCION_TOTAL

bono_reconocimiento_confirmado_oficialmente: bool
```

`ResumenComponenteBeneficioDefinidoMixto` diferencia:

```text
tipo_prestacion
pension_mensual_estimada
indemnizacion_mensualidad_hipotetica
indemnizacion_pago_unico_estimado
```

`ResumenComponenteAhorroPersonalMixto` incorpora:

```text
decision_requerida
devolucion_total_disponible
devolucion_pago_unico_estimado
garantia_renta_vitalicia_aplica
garantia_monto_mensual
garantia_condicion_activacion
prima_renta_vitalicia_pct_referencia
prima_renta_vitalicia_es_referencia_historica
```

`ResumenCalculoMixto` conserva separadamente:

```text
pension_mensual_total_estimada
pago_unico_bd_estimado
pago_unico_cap_estimado
pago_unico_total_estimado
```

La separación evita interpretar una devolución o indemnización como una renta mensual.

## Modelos de integración Mixto — Paso 6D.3

`DatosResultadoMixto` consolida:

```text
fecha_nacimiento
sexo
historial
linea_tiempo
resumen_retiro
fecha_retiro_seleccionada
escenario_salarial_nombre
saldo_ahorro_personal
bono_reconocimiento
bono_reconocimiento_confirmado_oficialmente
valor_actuarial_expectativa_vida
opcion_prestacion_cap
```

`ResumenResultadoMixto` conserva el escenario elegido, los años proyectados incluidos, las advertencias de integración y el `ResumenCalculoMixto` completo del motor.

## Modelos SUCGS 6E.3

`DatosCalculoSUCGS` recibe el saldo del Componente Contributivo de Capitalización Solidaria, valores solidarios opcionales y, para el artículo 197, el año inicial de vida laboral, el historial anual completo y la confirmación de estabilidad salarial.

`ResumenCalculoSUCGS` separa:

- `pension_contributiva_mensual`;
- `tipo_prestacion_solidaria`;
- `complemento_solidario_mensual`;
- `pension_despues_componente_solidario`;
- `pension_mensual_total_estimada`.

El último campo se completa cuando el artículo 197 puede evaluarse o cuando una condición comprobada determina que la garantía no aplica. Si faltan datos indispensables para cerrar la garantía, permanece `null`.

Campos principales agregados para el artículo 197:

- `condicion_minimo_cuotas_anuales_*`;
- `condicion_distribucion_cuotas_*`;
- `condicion_estabilidad_salarial_*`;
- `salario_promedio_base_mensual`;
- `tasa_reemplazo_minima_pct_aplicable`;
- `garantia_reemplazo_monto_objetivo`;
- `garantia_reemplazo_complemento_mensual`;
- `garantia_reemplazo_aplica`.

## Integración SUCGS — Paso 6E.4

`DatosResultadoSUCGS` incorpora ahora `historial`, `linea_tiempo`, `resumen_retiro`, `fecha_retiro_seleccionada` y `escenario_salarial_nombre`, además de los datos específicos del SUCGS. El año inicial de vida laboral usado por la integración se obtiene del inicio del historial del Paso 3; la aplicación no lo sustituye silenciosamente por la fecha de ingreso a la CSS.

`historial_laboral_completo_confirmado` expresa una confirmación del usuario distinta de la mera ausencia de huecos técnicos en el rango anual. `ResumenResultadoSUCGS` conserva el escenario salarial, los años proyectados incorporados y las advertencias de integración junto con el resultado jurídico del motor.
