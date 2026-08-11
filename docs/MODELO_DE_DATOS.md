# Modelo de datos

## Ubicación actual

Los modelos Pydantic se encuentran en:

```text
app/modelos/simulacion.py
```

## Cuotas

### `DatosCuotas`

Contiene:

- `cuotas_totales`;
- `cuotas_anio_actual`;
- `continua_cotizando`;
- `cuotas_esperadas_cierre_anio`;
- `cuotas_esperadas_por_anio`.

### `ResumenCuotas`

Contiene cuotas reales, cuotas proyectadas al cierre, faltantes para umbrales preliminares y tiempo aproximado.

## Historial salarial

### `RegistroHistorialSalarial`

Representa un año calendario y contiene:

- `anio`;
- `cuotas`;
- `salario_cotizado`.

`salario_cotizado` es el total reportado durante ese año y no debe confundirse con un salario anualizado de doce meses.

### `RegistroHistorialNormalizado`

Agrega el estado del registro:

```text
SIN_COTIZACION
HISTORICO_PARCIAL
HISTORICO_COMPLETO
```

### `DatosHistorialSalarial`

Contiene:

- año inicial y final;
- total de cuotas reales usado como referencia;
- registros anuales.

### `ResumenHistorialSalarial`

Contiene, entre otros datos:

- cuotas sumadas;
- diferencia respecto del total de referencia;
- indicador de coincidencia;
- años sin registro;
- total de salarios reportados;
- último año con cuotas;
- último salario cotizado.

## Salario actual

### `DatosSalario`

Contiene:

- `monto`;
- `periodicidad`.

Periodicidades admitidas:

```text
SEMANAL
QUINCENAL
MENSUAL
ANUAL
```

### `ResumenSalario`

Conserva el monto y periodicidad originales y agrega equivalentes semanal, quincenal, mensual y anual.

## Proyección salarial

### `DatosProyeccionSalario`

Contiene:

- salario mensual base;
- año inicial;
- año final;
- modalidad;
- porcentaje anual opcional;
- salario futuro conocido opcional;
- año del salario futuro opcional;
- lista de porcentajes para comparación.

Modalidades:

```text
CONSTANTE
PORCENTAJE
FUTURO_CONOCIDO
ESCENARIOS
```

### `ProyeccionSalarioAnual`

Representa una fila anual con:

- año;
- salario mensual;
- salario anual;
- crecimiento acumulado respecto de la base.

### `EscenarioProyeccionSalario`

Agrupa una tasa anual y sus registros anuales.

### `ResumenProyeccionSalario`

Agrupa la modalidad, período y uno o varios escenarios.

## Línea temporal histórica y proyectada

### `RegistroLineaTiempo`

Separa por año:

- cuotas históricas;
- salario histórico;
- cuotas proyectadas;
- salario proyectado;
- cuotas esperadas al cierre;
- salario esperado al cierre;
- estado del registro.

Estados actuales:

```text
HISTORICO
HISTORICO_PARCIAL
MIXTO
PROYECTADO
PENDIENTE
```

### `EscenarioLineaTiempo`

Agrupa una línea temporal completa para una hipótesis salarial.

### `DatosLineaTiempo`

Integra historial, cuotas, salario actual y parámetros de proyección.

### `ResumenLineaTiempo`

Devuelve el período histórico, el año actual, el final de la proyección y los escenarios integrados.

## Evolución prevista

El modelo deberá ampliarse para incorporar:

- períodos mensuales de cotización;
- fechas de referencia;
- escenarios de retiro;
- resultados por sistema previsional;
- desglose de componentes de pensión.