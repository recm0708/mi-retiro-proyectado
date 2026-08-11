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

`TipoEscenarioRetiro` incorpora también `ANTICIPADO` y el Paso 5 admite escenarios estándar `-2` y `-1` años respecto de la edad de referencia.
