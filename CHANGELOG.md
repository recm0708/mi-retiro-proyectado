# Changelog

Todos los cambios importantes realizados en este proyecto serán documentados en este archivo.

## [0.1.0] - En desarrollo

### Agregado

- Estructura inicial del proyecto.
- Configuración de FastAPI, Uvicorn y Jinja2.
- Interfaz web inicial con página de inicio, asistente de simulación y comparador provisional.
- Asistente de seis pasos con progreso visual.
- Paso 1 para datos personales y sistema previsional.
- Paso 2 para cuotas acreditadas y proyección preliminar.
- Endpoint `POST /api/simulacion/cuotas`.
- Paso 3 para historial salarial anual y salario actual para proyección.
- Componente modular `partials/historial_salarial.html`.
- Gestión del historial mediante `app/static/js/historial_salarios.js`.
- Endpoint `POST /api/simulacion/historial-salarial`.
- Servicio `historial_salarios.py` para validar años, cuotas y salarios históricos.
- Endpoint `POST /api/simulacion/salario`.
- Persistencia temporal del asistente mediante `sessionStorage`.
- Modelos Pydantic para cuotas, salarios y proyección salarial.
- Motor de proyección salarial con modalidades constante, porcentaje anual, salario futuro conocido y comparación de escenarios.
- Endpoint `POST /api/simulacion/proyeccion-salario`.
- Servicio `linea_tiempo.py` para integrar historial real y proyección futura.
- Endpoint `POST /api/simulacion/linea-tiempo`.
- Vista integrada del Paso 4 con historial real, año actual mixto y proyección por escenario.
- Interfaz inicial del Paso 4 — Proyección salarial.
- Estructura para motores SEBD, Mixto y SUCGS.
- Directorios de normativa, documentación técnica y casos de validación.
- Configuración inicial de Git y GitHub.
- Paso 5 para fechas y escenarios preliminares de retiro.
- Endpoint `POST /api/simulacion/retiro`.
- Carga versionada de parámetros generales desde `normativa/parametros_generales.json`.
- Utilidades monetarias comunes en `app/core/dinero.py`.
- Navegación rápida persistente para pasos largos del asistente.
- Pruebas automatizadas con `unittest` para precisión monetaria, proyección salarial, línea temporal y retiro.
- Archivo `.gitattributes` para normalizar finales de línea.
- Documento `docs/VALIDACION.md` y reglas para casos de prueba anonimizados.
- Metadatos de trazabilidad de la fuente oficial en `normativa/parametros_generales.json`.
- Parámetros específicos del SEBD en `normativa/sebd.json`, con trazabilidad de los artículos 178-181 y 192-193 del Texto Único vigente.
- Modelos jurídicos separados en `app/modelos/pension.py`.
- Primera implementación del motor de Pensión de Retiro por Vejez Normal del SEBD.
- Endpoint `POST /api/simulacion/sebd/normal`.
- Pruebas automatizadas del SEBD, incluida una regresión anonimizada que reproduce B/.741.59.
- Paso 6 visual para la primera integración de Pensión de Retiro por Vejez Normal del SEBD.
- Selección explícita del escenario de retiro que alimentará el cálculo final.
- Selector de escenario salarial en resultados cuando el Paso 4 contiene varias hipótesis.
- Servicio `app/servicios/resultados.py` para consolidar historial, proyección y retiro antes de invocar el motor legal.
- Endpoint `POST /api/simulacion/resultados/sebd-normal`.
- Pruebas de integración del Paso 6 para la regresión B/.741.59 y un escenario posterior a la edad de referencia.

- Cálculo de la Indemnización por Vejez del SEBD como prestación de pago único.
- Presentación específica en el Paso 6 de la mensualidad hipotética, factor de cotizaciones entre seis y pago único estimado.
- Pruebas automatizadas para 120 y 179 cuotas, transición SUCGS desde 01/03/2036 e integración del Paso 6.
- Limpieza semántica de la respuesta SEBD: los campos de pensión proporcional no aplicables a una Indemnización por Vejez ahora se entregan como `null`.
- Motor preliminar del Subsistema Mixto con separación explícita entre Componente de Beneficio Definido y Componente de Ahorro Personal.
- Parámetros versionados del Subsistema Mixto en `normativa/mixto.json`.
- Endpoint `POST /api/simulacion/mixto`.
- Cálculo del componente BD con participación salarial limitada a B/.500.00 mensuales y advertencia cuando el historial anual obliga a aproximar el tope mensual.
- Cálculo de pensión programada del CAP únicamente cuando se suministran saldo/bono y divisor actuarial; el motor no inventa parámetros actuariales faltantes.
- Transición operativa del Mixto hacia SUCGS desde 01/03/2032 documentada junto con la discrepancia interna del Texto Único.
- Cinco pruebas automatizadas iniciales del Subsistema Mixto.
- Paso 6D.2 del Subsistema Mixto con elección explícita entre pensión programada y devolución total del CAP cuando el artículo 187 la habilita.
- Modelado de la garantía del Seguro Colectivo de Renta Vitalicia como continuidad futura del pago CAP sin incrementar la pensión inicial.
- Separación de indemnización BD, devolución CAP y total de pagos únicos.
- Trazabilidad del bono de reconocimiento mediante indicador de confirmación oficial.
- Seis pruebas adicionales de devolución, garantía, decisión CAP e indemnización combinada; la suite alcanza 39 pruebas.

- Integración visual del Subsistema Mixto en el Paso 6, con entrada explícita de saldo CAP, bono, divisor actuarial y opción de prestación.
- Nuevo endpoint `POST /api/simulacion/resultados/mixto` para consolidar Pasos 1–5 con el motor Mixto.
- Presentación separada de componente BD, CAP, pensión mensual, pagos únicos, decisión CAP y garantía de renta vitalicia.
- Dos pruebas nuevas de integración del asistente con Mixto; la suite alcanza 41 pruebas.
- Navegación directa entre pasos ya disponibles mediante los indicadores superiores y un selector persistente `Ir a paso`, sin recorrer repetidamente el botón Anterior.
- Paso 6E.1 del SUCGS con parámetros versionados en `normativa/sucgs.json`, tabla actuarial del artículo 196, motor contributivo base y endpoints directos/integrados.
- Cinco pruebas automatizadas del SUCGS; la suite alcanza 46 pruebas.
- Paso 6E.2 del SUCGS con evaluación de los artículos 194 y 195, valores solidarios versionados y separación entre pensión contributiva, capa solidaria y pensión total definitiva.
- Pruebas de Pensión Garantizada Solidaria, Pensión de Beneficio Mínimo, casos con menos de 120 cuotas y superposición normativa en 240 cuotas.
- La suite completa alcanza 51 pruebas automatizadas.

### Cambiado

- Se separó la lógica de cálculo de la interfaz web.
- Se normalizaron comentarios y documentación del código Python, HTML, CSS y JavaScript.
- Se amplió el ancho del asistente y se mejoró la presentación de valores monetarios.
- La etiqueta `SUCGS` se presenta como `Sistema Único de Capitalización con Garantía Solidaria` en la selección y resultados para que el acrónimo sea comprensible.
- La barra persistente del Paso 6 reconoce correctamente tanto SEBD como Subsistema Mixto y reutiliza la acción de cálculo correspondiente.
- Los resultados dependientes se invalidan cuando el usuario modifica datos que los originaron.
- El Paso 3 separa el historial real del salario actual utilizado como base de proyección.
- Los cálculos monetarios conservan precisión interna y redondean a centavos con `ROUND_HALF_UP` al materializar cada resultado, evitando redondeos intermedios acumulativos.
- En años futuros con menos de 12 cuotas, el salario cotizado proyectado se limita a los meses/cuotas realmente proyectados.
- El historial real se muestra una sola vez aunque existan varios escenarios salariales futuros.
- Los campos monetarios editables usan separadores de miles y limitan la entrada a dos decimales.
- Los campos monetarios Saldo CAP y Bono de reconocimiento del Paso 6 Mixto ahora reutilizan la misma regla de miles y centavos; el valor actuarial permanece sin prefijo B/. porque es un factor/divisor y no una cantidad monetaria.
- El Paso 5 muestra explícitamente los datos heredados de pasos anteriores y advierte cuando el horizonte salarial no cubre todos los escenarios de retiro.
- La estimación de cuotas del Paso 5 respeta primero el cierre del año actual definido en el Paso 2 y aplica la densidad anual a partir del año siguiente.
- Los escenarios de retiro ya transcurridos permanecen visibles para comparación, pero no se seleccionan automáticamente para cálculo cuando el historial anual no permite reconstruir cuotas exactas a esa fecha.
- Los salarios futuros se incorporan al Paso 6 de forma trazable y se prorratea el último año proyectado cuando la fecha de retiro consume solo una parte de sus cuotas previstas.

### Corregido

- Estructura de `base.html` después de una referencia Jinja inválida.
- Distribución de las tarjetas de equivalencias salariales para valores grandes.
- Ubicación del botón `Continuar a proyección` fuera del aviso informativo.
- Jerarquía HTML del Paso 4 para evitar que quedara anidado dentro del Paso 3.
- Duplicación accidental del componente de historial fuera del bloque principal de Jinja.
- Restauración de los scripts específicos de simulación e historial en `simulacion.html`.
- Clasificación de años con cero cuotas en la línea temporal para mostrarlos como `SIN_COTIZACION`.
- Diferencias de un centavo provocadas por redondear el salario mensual antes de calcular el anual proyectado.
- Proyección de cuotas del Paso 5 que podía agregar cuotas al año actual aunque el usuario hubiera indicado que no esperaba más cuotas ese año.
- Artefactos visuales de punto flotante en campos salariales históricos.

### Paso 6C — modalidades SEBD

- Se agregó clasificación automática Normal / Anticipada / Proporcional / Proporcional Anticipada.
- Se incorporó identificación de posible Indemnización por Vejez y escenarios no elegibles.
- Se versionó la tabla mensual de factores de reducción de retiro anticipado.
- Se añadieron escenarios estándar -2 y -1 años en el Paso 5.
- Se añadió el endpoint general `POST /api/simulacion/sebd`.
- Se añadió el endpoint integrado `POST /api/simulacion/resultados/sebd`.
- El Paso 6 muestra la modalidad detectada y los factores por cuotas y edad.
- Se documentó el tratamiento de años calendario parciales dentro de los diez mejores años.
- La suite automatizada se amplió con pruebas de las cuatro modalidades y una integración anticipada femenina.

### Paso 6E.3 — garantía de reemplazo mínimo SUCGS
- Implementación backend del artículo 197 con preevaluación del mínimo anual de cuotas y de la distribución 50 % / 50 %.
- Cálculo del salario promedio base mensual a partir de salarios cotizados / meses cotizados, conforme a la definición general del artículo 1 numeral 41.
- Garantía completa del 60 % con 240 o más cuotas y garantía proporcional para requisitos inferiores modelados desde 120 cuotas.
- La condición de estabilidad salarial se mantiene como confirmación explícita y auditable; no se corrige automáticamente la redacción del numeral 3 del artículo 197.
- Cinco pruebas nuevas para garantía completa, proporcional, distribución insuficiente, estabilidad pendiente y años con menos de cinco cuotas.

### Paso 6E.4 — integración visual completa SUCGS

- El Paso 6 habilita el cálculo SUCGS desde la interfaz, sin depender de Swagger.
- El asistente reutiliza historial, trayectoria salarial y escenario de retiro de los Pasos 1–5.
- Se solicitan explícitamente saldo de Capitalización Solidaria, confirmación del saldo, valores solidarios vigentes y confirmaciones necesarias para el artículo 197.
- La interfaz separa componente contributivo, capa solidaria, garantía de reemplazo y pensión mensual total.
- La estabilidad salarial del artículo 197 se mantiene como condición triestado: confirmada, no cumple o pendiente.
- Se añade persistencia e invalidación del resultado SUCGS en `sessionStorage` y soporte en la navegación flotante.
- La suite de regresión alcanza 57 pruebas automatizadas.
