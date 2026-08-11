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

### Cambiado

- Se separó la lógica de cálculo de la interfaz web.
- Se normalizaron comentarios y documentación del código Python, HTML, CSS y JavaScript.
- Se amplió el ancho del asistente y se mejoró la presentación de valores monetarios.
- Los resultados dependientes se invalidan cuando el usuario modifica datos que los originaron.
- El Paso 3 separa el historial real del salario actual utilizado como base de proyección.
- El salario anual proyectado se deriva del salario mensual visible redondeado para mantener consistencia monetaria.
- En años futuros con menos de 12 cuotas, el salario cotizado proyectado se limita a los meses/cuotas realmente proyectados.
- El historial real se muestra una sola vez aunque existan varios escenarios salariales futuros.

### Corregido

- Estructura de `base.html` después de una referencia Jinja inválida.
- Distribución de las tarjetas de equivalencias salariales para valores grandes.
- Ubicación del botón `Continuar a proyección` fuera del aviso informativo.
- Jerarquía HTML del Paso 4 para evitar que quedara anidado dentro del Paso 3.
- Duplicación accidental del componente de historial fuera del bloque principal de Jinja.
- Restauración de los scripts específicos de simulación e historial en `simulacion.html`.