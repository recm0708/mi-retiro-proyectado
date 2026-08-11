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

### Cambiado

- Se separó la lógica de cálculo de la interfaz web.
- Se normalizaron comentarios y documentación del código Python, HTML, CSS y JavaScript.
- Se amplió el ancho del asistente y se mejoró la presentación de valores monetarios.
- Los resultados dependientes se invalidan cuando el usuario modifica datos que los originaron.
- El Paso 3 separa el historial real del salario actual utilizado como base de proyección.
- Los cálculos monetarios conservan precisión interna y redondean a centavos con `ROUND_HALF_UP` al materializar cada resultado, evitando redondeos intermedios acumulativos.
- En años futuros con menos de 12 cuotas, el salario cotizado proyectado se limita a los meses/cuotas realmente proyectados.
- El historial real se muestra una sola vez aunque existan varios escenarios salariales futuros.
- Los campos monetarios editables usan separadores de miles y limitan la entrada a dos decimales.
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
