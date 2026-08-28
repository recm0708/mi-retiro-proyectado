# Modelo de datos

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.17.02-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R2 — 2026-08-17
**Actualización de estado frontend:** UX.4.6f R1.1 — bloqueo documental y decisión explícita de historial — 2026-08-20
**Clasificación:** Técnica / Pública

Los contratos de cálculo se definen con Pydantic. El estado visual y de navegación del navegador se documenta por separado porque no todo campo de `sessionStorage` pertenece al dominio previsional.

[Índice](../README.md) · [Arquitectura](system-architecture.md) · [Gestión de datos](../product/simulation-data-management.md)

## 1. Módulos de modelos

- `app/models/simulation.py` — datos de Pasos 1–5 e importaciones.
- [`app/models/pension.py`](../../app/models/pension.py) — motores y resultados por sistema.
- [`app/models/comparacion.py`](../../app/models/comparacion.py) — comparación transversal.
- `app/models/traceability.py` — trazabilidad de cálculo.
- `app/models/unified_result.py` — resumen transversal.

## 2. Convenciones

- fechas de API: ISO cuando se serializan;
- cuotas: enteros mensuales;
- importes editables: máximo dos decimales;
- `null`: dato no disponible/no aplicable cuando cero podría inducir a error;
- pagos mensuales y pagos únicos: campos separados;
- datos históricos y proyectados: no se mezclan silenciosamente;
- procedencia visual: metadata del frontend, salvo cuando un modelo específico expone una fuente explícita;
- una referencia documental original y una copia de trabajo pueden coexistir en `sessionStorage` sin alterar el contrato Pydantic del parser.

## 3. Cuotas

### `DatosCuotas`

Contiene:

- `cuotas_totales`;
- `cuotas_anio_actual`;
- `continua_cotizando`;
- `cuotas_esperadas_cierre_anio`;
- `cuotas_esperadas_por_anio`.

`cuotas_anio_actual` ya forma parte de `cuotas_totales`.

### `ResumenCuotas`

Expone:

- cuotas reales;
- proyección restante y cierre del año;
- faltantes para umbrales modelados;
- aproximaciones temporales cuando pueden calcularse.

El frontend puede reconciliar `cuotas_anio_actual` con el detalle del Paso 3 cuando existe una confirmación más reciente, pero el endpoint de cuotas continúa recibiendo el mismo contrato Pydantic.

## 4. Historial salarial

### `RegistroHistorialSalarial`

Representa:

```text
año + cuotas + salario_cotizado
```

`salario_cotizado` es el total reportado para ese año; un año parcial no se anualiza por definición del modelo.

### `DatosHistorialSalarial`

Incluye período, `cuotas_totales_referencia` y registros.

### `ResumenHistorialSalarial`

Incluye totales, diferencia de cuotas, años faltantes, salarios reportados y registros normalizados con estado.

## 5. Detalle salarial del año actual

### `RegistroDetalleAnioActual`

Campos principales:

- mes;
- `cuota_acreditada`;
- estado `SIN_INFORMACION` / `PARCIAL` / `COMPLETO`;
- salario mensual o dos quincenas.

### `DatosDetalleAnioActual`

Incluye:

- año;
- modo `MENSUAL` o `QUINCENAL`;
- `cuotas_anio_actual_referencia`;
- registros mensuales.

### `ResumenDetalleAnioActual`

Expone, entre otros:

- cuotas identificadas;
- coherencia con la referencia;
- último mes acreditado;
- último mes salarial completo;
- salario disponible;
- salario acreditado;
- cantidad de meses con información/completos;
- bases salariales sugeridas.

**Salario disponible** y **salario acreditado** son métricas distintas.

## 6. Mi Retiro Seguro

### `RegistroReferenciaMiRetiroSeguro`

Contiene año, edad, clasificación histórica/proyectada, salario anual y cuotas.

Tipos:

- `HISTORICO`;
- `HISTORICO_PROYECTADO`;
- `PROYECTADO`.

### `ResumenReferenciaMiRetiroSeguro`

Puede contener identificadores personales opcionales, datos previsionales, sistema, referencia de prestación, cuotas históricas, total acumulado, registros y advertencias.

`cuotas_historicas` y `total_cuotas_acumuladas` no son sinónimos: el segundo puede incluir proyección propia del comprobante.

El monto del comprobante es una referencia externa; no forma parte de las fórmulas de Mi Retiro Proyectado.

## 7. Ficha Digital

### `RegistroFichaDigital`

El parser entrega:

- año;
- mes;
- salario;
- estado salarial.

**No contiene `cuota_acreditada`.** La cuota mensual se materializa en `RegistroDetalleAnioActual` cuando el frontend aplica una importación confirmada.

Esta separación resuelve una ambigüedad de documentación anterior: detectar un salario en el parser y decidir cómo queda representado dentro del detalle del asistente son operaciones distintas.

### `ResumenFichaDigital`

Contiene:

- registros del año más reciente detectado;
- año/mes más reciente;
- fecha de referencia externa opcional;
- indicador de confiabilidad;
- fuente de la fecha;
- advertencias.

El parser selecciona el año más reciente del documento cuando no se le suministra un año controlado. No usa el reloj local como fuente implícita.

### `ResumenFechaReferencia`

Representa `fecha`, `confiable` y `fuente`.


### Estado frontend de procedencia y copia de trabajo

Los resúmenes Pydantic de Mi Retiro Seguro y Ficha Digital describen lo detectado por el backend. El navegador puede añadir estado temporal para permitir ajustes posteriores a la confirmación sin reinterpretar el parser.

Campos/estructuras de frontend relevantes:

- `referencia_mi_retiro_seguro_original`: fotografía original confirmada;
- `referencia_mi_retiro_seguro`: copia de trabajo del comprobante;
- `ficha_digital_importada_original`: fotografía original de Ficha Digital;
- `ficha_digital_importada`: copia de trabajo de la Ficha;
- `periodos_excluidos_importacion_ficha`: períodos detectados que el usuario decidió no usar;
- `origen_campos_persona`, `origen_campos_cuotas`, `origen_campos_historial` y `origen_campos_detalle_anio_actual`: metadata de procedencia;
- `origen_historial_anio_inicio` y `origen_proyeccion_anio_fin`: procedencia de valores derivados/editables;
- `modo_historial`, `detalle_anio_actual_habilitado` y `origen_salario_proyeccion` conservan ausencia de decisión (`""`/`null`) hasta que exista una selección explícita o una derivación documental válida.

Estos campos no cambian el documento fuente ni los modelos Pydantic recibidos desde la API. Son estado de interfaz serializable de la simulación.

## 8. Salario y proyección

### `DatosSalario` / `ResumenSalario`

Periodicidades:

- semanal;
- quincenal;
- mensual;
- anual.

El resumen ofrece equivalencias normalizadas.

### `DatosProyeccionSalario`

Modalidades:

- `CONSTANTE`;
- `PORCENTAJE`;
- `FUTURO_CONOCIDO`;
- `ESCENARIOS`.

La proyección no reescribe el historial real. `PORCENTAJE` y `ESCENARIOS` aplican composición anual. `escenarios_porcentajes` inicia como lista vacía: la aplicación no inventa tasas de comparación y exige que el Asegurado(a) las indique cuando selecciona `ESCENARIOS`. En `FUTURO_CONOCIDO`, la tasa equivalente se deriva únicamente hasta el año objetivo; si el horizonte continúa, el salario objetivo se mantiene constante para no inferir una tasa posterior no declarada.

## 9. Línea temporal y retiro

Los modelos de línea temporal combinan historia y proyección conservando su origen. `RegistroLineaTiempo.salario_mensual_proyectado` transporta la referencia mensual del escenario sin reconstruirla desde el salario cotizado prorrateado; es opcional para conservar compatibilidad con registros históricos que no contienen proyección. El estado `PROYECTADO_SIN_COTIZACION` distingue un año futuro cubierto por la trayectoria salarial pero con cero cuotas previstas.

`DatosRetiro` y `ResumenRetiro` manejan escenarios temporales, cuotas y cobertura salarial. El flujo visible usa `ultimo_mes_cuotas` como dato mensual preferente y conserva la fecha técnica derivada cuando corresponde.

## 10. Modelos previsionales

[`app/models/pension.py`](../../app/models/pension.py) contiene entradas y salidas para:

- SEBD normal y clasificador general;
- Subsistema Mixto;
- SUCGS;
- resultados integrados de los tres sistemas.

Los campos no aplicables permanecen diferenciados de un resultado igual a cero.

Los resultados integrados soportan dos fotografías:

- `PROYECTADO`;
- `SOLO_ACREDITADO`.

## 11. Resultado transversal

`ResumenPrestacionUnificada` normaliza, sin recalcular:

- sistema;
- escenario;
- fecha/edad/cuotas;
- modalidad;
- estado;
- naturaleza;
- pensión mensual;
- pago único;
- decisiones pendientes;
- datos no confirmados;
- advertencias.

El detalle específico continúa en el resultado del motor.

## 12. Comparación y trazabilidad

`DatosComparacionEscenarios` y `ResumenComparacionEscenarios` permiten comparar escenarios sin implementar una cuarta fórmula.

`ResumenTrazabilidadCalculo` representa la secuencia explicativa de datos, reglas, fórmulas, sustituciones, resultados y fuentes.

## 13. Estado del frontend

La simulación del navegador incorpora datos que no son modelos Pydantic, por ejemplo:

- `paso_actual`;
- modalidad de captura;
- confirmación de importaciones;
- mapas de procedencia por campo;
- nombres visibles de archivos importados;
- resultados almacenados por fotografía;
- configuración específica de Paso 6.

Estos campos administran continuidad y presentación. Solo los contratos requeridos por un endpoint se envían al backend.

## 14. Procedencia

La procedencia puede distinguir estados como detectado, editado y completado manualmente. Su finalidad es evitar presentar un dato manual como documental y controlar edición en interfaz.

La procedencia no altera por sí sola una fórmula previsional.

## 15. Historia

La versión acumulativa anterior se conserva en:

`docs/archive/technical/data-model-pre-gov1-3-r2.md`


### UX.4.6f R1.1 — decisión explícita de disponibilidad del historial

El estado frontend incorpora `modo_historial_confirmado_usuario: bool`. Su valor inicial es `false`; solo cambia a `true` cuando el Asegurado(a) selecciona explícitamente una opción de **Disponibilidad del historial** o confirma el flujo equivalente. Importar registros desde Mi Retiro Seguro no establece este indicador y no responde el selector por el usuario.

El bloqueo de un campo documental en la vista principal se decide comparando contra `referencia_mi_retiro_seguro_original` o `ficha_digital_importada_original`. La procedencia vigente puede cambiar, pero la fotografía original determina si el dato fue detectado y, por tanto, si debe permanecer bloqueado fuera del modal de revisión.

### UX.4.6g R1 — selección contextual de retiro

`DatosRetiro.anios_adicionales` ya no presupone una banda completa de escenarios: su valor por defecto es `[0]`, correspondiente a la edad de referencia. El frontend conserva de forma temporal `preferencias_retiro` con `anios_adicionales`, `incluir_fecha_evaluacion`, `origen` (`SUGERIDO_PASO4` o `EDITADO_USUARIO`) y `anio_fin_proyeccion_origen`.

`incluir_fecha_evaluacion_como_retiro` pertenece a la solicitud del Paso 5 y solo materializa un escenario `EVALUACION` cuando la fecha de evaluación está dentro de la banda anticipada estándar. La preferencia visual no sustituye la clasificación legal que realiza el Paso 6.
