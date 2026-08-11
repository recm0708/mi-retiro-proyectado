# Arquitectura

## Objetivo

La aplicación utiliza una arquitectura web local separando presentación, API, modelos de datos, servicios de cálculo y futuros motores previsionales.

## Capas actuales

```text
Navegador
  ├── Jinja2 / HTML
  ├── Bootstrap / CSS
  └── JavaScript + sessionStorage
            ↓ HTTP/JSON
FastAPI
            ↓
Modelos Pydantic
            ↓
Servicios de cálculo
  ├── proyeccion_cuotas.py
  ├── historial_salarios.py
  ├── proyeccion_salarios.py
  └── linea_tiempo.py
            ↓
Motores previsionales futuros
  ├── elegibilidad.py
  ├── sebd.py
  ├── mixto.py
  └── sucgs.py
            ↓
Normativa versionada futura
```

## Responsabilidades

### Interfaz

- captura datos;
- controla la navegación del asistente;
- conserva temporalmente la simulación en `sessionStorage`;
- presenta respuestas de la API;
- invalida resultados cuando cambian datos de los que dependen.

### FastAPI

- expone páginas y endpoints;
- recibe modelos Pydantic;
- traduce errores de negocio a respuestas HTTP;
- delega los cálculos a servicios o motores.

### Modelos

`app/modelos/simulacion.py` define actualmente estructuras para:

- cuotas;
- historial salarial anual;
- salario actual;
- equivalencias salariales;
- configuración de proyección;
- registros anuales y escenarios.

### Servicios

Los servicios actuales realizan cálculos no específicos de un sistema legal completo:

- análisis preliminar de cuotas;
- validación y resumen del historial salarial;
- normalización salarial;
- proyección salarial;
- integración de historial y proyección en una línea temporal anual.

### Motores

Los motores SEBD, Mixto, SUCGS y elegibilidad todavía no contienen las fórmulas legales definitivas.

## Endpoints actuales

```text
GET  /
GET  /simulacion
GET  /comparar
GET  /salud
POST /api/simulacion/cuotas
POST /api/simulacion/historial-salarial
POST /api/simulacion/salario
POST /api/simulacion/proyeccion-salario
POST /api/simulacion/linea-tiempo
```

## Persistencia

Actualmente no existe persistencia permanente. `sessionStorage` conserva únicamente el estado temporal de la pestaña durante una simulación.
## Modularización del Paso 3

El historial salarial se mantiene en un parcial Jinja independiente (`templates/partials/historial_salarial.html`) y su comportamiento de interfaz se gestiona en `static/js/historial_salarios.js`. El archivo `simulacion.js` conserva la navegación general y el estado compartido del asistente.

## Modularización de la línea temporal

La presentación integrada del Paso 4 se gestiona en `static/js/linea_tiempo.js`. Este módulo consume `POST /api/simulacion/linea-tiempo` y evita duplicar el historial real en cada escenario futuro.
