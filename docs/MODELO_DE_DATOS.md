# Modelo de datos

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R2 — 2026-08-17
**Actualización de estado frontend:** UX.4.6e R8 — procedencia editable — 2026-08-19
**Clasificación:** Técnica / Pública

Los contratos de cálculo se definen con Pydantic. El estado visual y de navegación del navegador se documenta por separado porque no todo campo de `sessionStorage` pertenece al dominio previsional.

[Índice](INDICE.md) · [Arquitectura](ARQUITECTURA.md) · [Gestión de datos](GESTION_DATOS_SIMULACION.md)

## 1. Módulos de modelos

- `app/modelos/simulacion.py` — datos de Pasos 1–5 e importaciones.
- `app/modelos/pension.py` — motores y resultados por sistema.
- `app/modelos/comparacion.py` — comparación transversal.
- `app/modelos/trazabilidad.py` — trazabilidad de cálculo.
- `app/modelos/resultado_unificado.py` — resumen transversal.

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
- `origen_campos_persona`, `origen_campos_cuotas`, `origen_campos_historial` y `origen_campos_detalle_anio_actual`: metadata de procedencia.

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

La proyección no reescribe el historial real.

## 9. Línea temporal y retiro

Los modelos de línea temporal combinan historia y proyección conservando su origen.

`DatosRetiro` y `ResumenRetiro` manejan escenarios temporales, cuotas y cobertura salarial. El flujo visible usa `ultimo_mes_cuotas` como dato mensual preferente y conserva la fecha técnica derivada cuando corresponde.

## 10. Modelos previsionales

`app/modelos/pension.py` contiene entradas y salidas para:

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

`docs/historico/tecnico/MODELO_DE_DATOS_PRE_GOV1_3_R2.md`
