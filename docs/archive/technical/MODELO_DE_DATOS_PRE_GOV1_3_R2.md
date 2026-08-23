# Modelo de datos

Los contratos principales se definen con Pydantic y están separados entre datos generales del asistente y datos/resultados previsionales.

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Ubicación

- `app/models/simulacion.py`: Pasos 1–5 y servicios comunes.
- `app/models/pension.py`: motores SEBD, Mixto, SUCGS y resultados integrados.

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

`ResumenReferenciaMiRetiroSeguro` conserva la referencia personal, filas anuales detectadas e identificadores opcionales etiquetados de forma inequívoca para revisión en UX.4.6b. `ResumenFichaDigital` contiene únicamente registros del año calendario actual mediante `RegistroFichaDigital` (`anio`, `mes`, `salario` y estado inicial del salario). Los períodos de años anteriores detectados en el PDF se descartan antes de construir el contrato.

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

`app/models/comparacion.py` define una capa normalizada que no sustituye los modelos de cada motor.

- `DatosComparacionEscenarios`: sistema, bloque integrado correspondiente, filtros de fechas de retiro y escenarios salariales.
- `FilaComparacionEscenario`: fecha, edad, cuotas, modalidad/prestación, pensión mensual, pago único, estado y diferencias contra la base.
- `ResumenComparacionEscenarios`: matriz completa, conteos, mejor pensión mensual comparable y advertencias globales.

Los pagos únicos y las pensiones mensuales permanecen en campos separados.


## 16. Trazabilidad 6F.2

`app/models/trazabilidad.py` define una representación transversal que no sustituye los modelos de cada motor:

- `DatoTrazabilidad`: dato, valor, origen y estado de confirmación;
- `PasoTrazabilidad`: regla, fórmula, sustitución, resultado, redondeo y fuentes;
- `FuenteTrazabilidad`: referencia oficial, artículos y URL;
- `ResumenTrazabilidadCalculo`: secuencia completa y resultado final tipificado.

Los modelos integrados `ResumenResultadoSEBD`, `ResumenResultadoMixto` y `ResumenResultadoSUCGS` incluyen `trazabilidad`. Esta propiedad es explicativa: el importe legal continúa proviniendo del campo `calculo` generado por el motor correspondiente.

## 17. Resultado transversal 6F.4

`app/models/resultado_unificado.py` incorpora `ResumenPrestacionUnificada` con campos comunes a los tres sistemas:

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
- El modelo excluye el código único del documento. Puede contener nombres, apellidos, cédula y número de Seguro Social opcionales cuando el PDF los identifica explícitamente. El PDF original no forma parte del estado de simulación.


## UX.4.5 — modo de integración del resultado

`DatosResultadoSEBD`, `DatosResultadoMixto` y `DatosResultadoSUCGS` aceptan `modo_integracion` con dos valores:

- `PROYECTADO`: usa el escenario completo de los Pasos 4–5;
- `SOLO_ACREDITADO`: conserva la fecha de retiro, usa `historial.cuotas_totales_referencia` como total de cuotas y no añade registros salariales proyectados.

Los resúmenes integrados devuelven también el modo utilizado para que la interfaz pueda almacenar y presentar ambas fotografías sin confundirlas.


## UX.4.6b — estado personal de la simulación

`simulacion.persona` puede contener: `primer_nombre`, `segundo_nombre`, `primer_apellido`, `segundo_apellido`, `apellido_casada`, `cedula`, `numero_seguro_social`, `fecha_nacimiento`, `sexo`, `fecha_ingreso_css` y `sistema`. Los siete primeros campos de identificación son opcionales para el cálculo.

El estado agrega:

- `modo_datos_personales`: `MANUAL` o `MI_RETIRO_SEGURO`;
- `origen_persona`: `MANUAL`, `MI_RETIRO_SEGURO` o `MI_RETIRO_SEGURO_EDITADO`.

`ResumenReferenciaMiRetiroSeguro` puede conservar `nombre_completo_detectado` como trazabilidad del texto original y, al mismo tiempo, devolver componentes descompuestos de forma conservadora. Los campos explícitos del documento prevalecen. Para nombres femeninos, el patrón final `de Apellido` puede poblar `apellido_casada`; la vista previa sigue siendo la autoridad de revisión antes de importar.


### Consentimiento de privacidad fuera del modelo previsional

La aceptación de privacidad no forma parte de `simulacion.persona` ni de los modelos Pydantic de cálculo. `privacidad.js` conserva en `localStorage` únicamente versión, estado de aceptación y fecha técnica de aceptación. El contenido de la simulación permanece en `sessionStorage`. Esta separación evita que un estado legal/de interfaz se mezcle con los contratos de los motores.


## UX.4.6c — trazabilidad de campos de cuotas

`DatosCuotas` no cambia su contrato con la API. UX.4.6c añade en el estado temporal del frontend `origen_campos_cuotas`, un mapa de procedencia por campo que actualmente puede identificar `cuotas_totales` y `cuotas_anio_actual` como `MI_RETIRO_SEGURO` o `MI_RETIRO_SEGURO_EDITADO`. La ausencia de una marca de origen significa que el valor es manual o todavía está pendiente.

Esta metadata no forma parte del cálculo legal ni se envía al endpoint de análisis de cuotas. Su finalidad es impedir ediciones accidentales de información documental ya confirmada y mantener habilitados únicamente los datos que el PDF no proporcionó.


### Vista previa contextual de cuotas — UX.4.6c R3

La referencia confirmada puede conservar en el estado temporal del frontend `cuotas_anio_actual` como valor auxiliar de revisión. Si el comprobante ya contiene un registro anual no proyectado para el año actual, ese valor se deriva del registro y se sincroniza al confirmar. Este campo auxiliar no modifica el contrato `DatosCuotas` de la API; sirve para mantener consistente la vista filtrada del Paso 2 con el historial importado.

## UX.4.6d — procedencia del historial y detalle reciente

UX.4.6d no altera los contratos Pydantic de `DatosHistorialSalarial`, `RegistroHistorialSalarial`, `DatosDetalleAnioActual` ni `DatosSalario`. La protección de datos importados se conserva como metadata temporal del frontend:

- `origen_campos_historial`: mapa `año -> campo -> origen` para `cuotas` y `salario_cotizado`;
- `origen_campos_detalle_anio_actual`: mapa `mes -> campo -> origen` para `cuota_acreditada`, `estado` y `salario_mensual`;
- los orígenes documentales actuales son `MI_RETIRO_SEGURO`, `MI_RETIRO_SEGURO_EDITADO`, `FICHA_DIGITAL` y `FICHA_DIGITAL_EDITADO`.

La ausencia de una marca de origen significa que el campo no fue confirmado por esa importación y puede continuar disponible para captura manual. Esta metadata controla edición y trazabilidad de interfaz; no modifica fórmulas ni se envía como entrada a los motores previsionales.

El cierre visual del Paso 3 se deriva de los resúmenes existentes (`resumen_historial`, `resumen_detalle_anio_actual`, `resumen_salario`) y no crea un cuarto modelo de cálculo.

### R2 — separación entre total acreditado y asignación mensual

- `simulacion.cuotas.cuotas_anio_actual`: referencia agregada de cuotas acreditadas del año actual. Puede proceder de Paso 2/Mi Retiro Seguro y, desde R23, ampliarse con una Ficha Digital confirmada que aporte más meses acreditados; una ficha con menos meses no la reduce automáticamente.
- `detalle_anio_actual.cuotas_anio_actual_referencia`: copia de referencia para validar coherencia mensual.
- `detalle_anio_actual.registros[*].cuota_acreditada`: estado mensual. En captura manual lo define el usuario; en registros detectados por Ficha Digital R3 queda marcado/bloqueado como parte de la importación confirmada. No sustituye el total del Paso 2.
- `origen_campos_cuotas.cuotas_anio_actual`: conserva su procedencia aunque se importe o retire una Ficha Digital.


### Metadatos de procedencia visual — UX.4.6d R4

Los metadatos `origen_campos_historial` y `origen_campos_detalle_anio_actual` determinan qué controles deben tratarse como documentales. En la UI, una casilla documental se restaura como marcada/bloqueada y una fila documental recibe `data-row-imported`. Estos atributos de presentación no cambian los contratos numéricos de historial, cuotas ni salario.

### Compatibilidad de casillas importadas — UX.4.6d R5

`data-imported-locked="true"` es metadata temporal de interfaz y no modifica el contrato Pydantic. Durante la lectura del detalle equivale a una cuota seleccionada para ese mes documental. Esto permite restaurar de forma segura simulaciones creadas antes de que la casilla importada se persistiera explícitamente como `true`.

### Invalidación por limpieza de pasos — UX.4.6d R6

La limpieza no añade campos al contrato Pydantic. Opera sobre el estado temporal del frontend y restablece grupos completos a sus valores iniciales. La dependencia es descendente: Paso 2 limpia cuotas y Pasos 3–6; Paso 3 limpia historial/detalle/base salarial y Pasos 4–6; Paso 4 limpia proyección y Pasos 5–6; Paso 5 limpia retiro/resultados; Paso 6 limpia únicamente configuraciones y resultados. Paso 1 equivale a una simulación vacía completa.

### Estados de presentación del historial — UX.4.6d R8

R8 no modifica `RegistroHistorialSalarial` ni los modelos Pydantic. Añade únicamente una clasificación de presentación en el navegador: `PENDIENTE`, `FALTA_SALARIO`, `FALTAN_CUOTAS`, `REVISAR`, `SIN_COTIZACION`, `PARCIAL` y `COMPLETO`. Esta clasificación sirve para feedback inmediato y filtrado, pero la aceptación definitiva de los registros continúa en `analizar_historial_salarial`.

### UX.4.6d R9 — sin cambios de contrato

R9 no modifica los modelos Pydantic ni las estructuras persistidas de historial, detalle o consentimiento. Los nuevos estados continúan siendo clasificación de presentación. La reactividad por delegación y el contexto del modal son metadata de interfaz y no alteran los datos previsionales.


### Metadata de revisión documental — UX.4.6d R17

La sesión puede conservar `campos_editados_importacion_comprobante: string[]` con IDs de controles modificados durante la revisión de Mi Retiro Seguro. Este arreglo no representa información previsional ni altera el contenido del documento original; permite que la UI distinga **Detectado**, **Editado por ti** y **Completado manualmente** al volver a revisar una importación confirmada.

`cuotas_historicas` y `total_cuotas_acumuladas` permanecen como conceptos independientes dentro de `referencia_mi_retiro_seguro`: el primero alimenta la fotografía acreditada del Paso 2 y el segundo puede incluir períodos proyectados del comprobante.

## UX.4.6d R18 — metadata de procedencia

El estado cliente incorpora `origen_campos_persona` y reutiliza los mapas de origen existentes para diferenciar fuente y edición por campo. Los códigos pueden incluir sufijos `DETECTADO`, `EDITADO`, `COMPLETADO_MANUAL` o `NO_DETECTADO`. `ficha_digital_importada` y `referencia_mi_retiro_seguro` pueden incluir `nombre_archivo_origen` como metadata de presentación; este campo no representa contenido documental ni ruta local.


## UX.4.6d R19 — cuotas actuales derivadas del detalle

Cuando el usuario modifica explícitamente una casilla manual del detalle del año actual, `simulacion.cuotas.cuotas_anio_actual` puede actualizarse con el conteo confirmado y `simulacion.cuotas.cuotas_totales` se recalcula como `cuotas_previas_al_anio_actual + cuotas_anio_actual`. `origen_campos_cuotas` registra `DETALLE_ANIO_ACTUAL_EDITADO` para conservar trazabilidad.

La fila vigente de `simulacion.historial` se materializa al analizar a partir del detalle: `cuotas` corresponde a meses marcados y `salario_cotizado` al total salarial de esos meses. Los salarios de meses no acreditados permanecen únicamente en `detalle_anio_actual`/`resumen_detalle_anio_actual`.


## UX.4.6d R20 — vigencia sin nuevo estado persistente

R20 no agrega campos al contrato Pydantic ni a `sessionStorage`. La vigencia se deriva dinámicamente de `ficha_digital_importada.anio_mas_reciente` y `mes_mas_reciente`, que ya existían en `ResumenFichaDigital`. `resumen_detalle_anio_actual` tampoco cambia de forma: sus valores existentes pasan a tener representación visible en el Paso 3.


## UX.4.6d R21 — metadata temporal de Ficha Digital

`ResumenFichaDigital` incorpora `fecha_referencia`, `fecha_referencia_confiable` y `fuente_fecha_referencia`. Estos campos no forman parte del cálculo salarial; documentan la referencia temporal con la que se evaluó la vigencia del archivo. La importación persistida conserva esta metadata y puede refrescarla mediante `/api/sistema/fecha-referencia`.


### Procedencia de cuotas actualizadas desde Ficha Digital (UX.4.6d R23)

Cuando una Ficha Digital confirmada amplía el conteo del año actual, `origen_campos_cuotas.cuotas_anio_actual` y `cuotas_totales` usan `FICHA_DIGITAL_ACTUALIZADO`. El total acumulado se deriva como `cuotas_previas_al_anio_actual + cuotas_confirmadas_en_detalle`; el detalle persiste además la nueva `cuotas_anio_actual_referencia`.
