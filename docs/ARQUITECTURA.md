# Arquitectura

## Principios

La aplicación mantiene separadas cuatro responsabilidades:

1. **Interfaz:** Jinja2, HTML, CSS y JavaScript capturan datos y presentan resultados.
2. **API:** FastAPI valida la frontera entre interfaz y backend.
3. **Servicios y motores:** Python concentra cálculos, validaciones y reglas de negocio.
4. **Normativa:** los parámetros legales versionables se mantienen fuera de la presentación y de los algoritmos cuando corresponde.

Los datos históricos reales y los datos proyectados permanecen diferenciados durante todo el flujo.

## Estructura principal

```text
app/
├── core/
│   ├── config.py
│   ├── constants.py
│   ├── dinero.py
│   └── normativa.py
├── modelos/
│   └── simulacion.py
├── motores/
│   ├── elegibilidad.py
│   ├── sebd.py
│   ├── mixto.py
│   └── sucgs.py
├── servicios/
│   ├── historial_salarios.py
│   ├── linea_tiempo.py
│   ├── proyeccion_cuotas.py
│   ├── proyeccion_salarios.py
│   └── retiro.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── partials/
└── main.py
```

Los motores previsionales legales todavía están en preparación; los servicios actuales resuelven captura, normalización, proyección y escenarios preliminares.

## Núcleo común

### `app/core/dinero.py`

Centraliza la conversión a `Decimal`, la validación de precisión y el redondeo monetario técnico. El criterio general actual es conservar precisión durante la operación y redondear a centavos con `ROUND_HALF_UP` al materializar un importe, salvo que una regla normativa específica exija otra cosa.

### `app/core/normativa.py`

Carga parámetros versionados desde `normativa/`. Actualmente se utiliza `parametros_generales.json` para edades de referencia y otros metadatos generales. Los parámetros específicos de SEBD, Mixto y SUCGS se incorporarán conforme se implementen sus motores.

## Modelos

`app/modelos/simulacion.py` define estructuras Pydantic para:

- cuotas;
- historial salarial anual;
- salario actual y equivalencias;
- configuración y escenarios de proyección salarial;
- línea temporal histórica/proyectada;
- fechas y escenarios preliminares de retiro.

Los campos monetarios y porcentuales editables relevantes validan como máximo dos decimales en la frontera del backend.

## Servicios

### Cuotas

`proyeccion_cuotas.py` analiza cuotas acreditadas, cierre esperado del año y densidad anual futura. Sus referencias de 180 y 240 cuotas siguen siendo preliminares hasta que el motor legal determine la prestación aplicable.

### Historial

`historial_salarios.py` valida años, cuotas y salarios históricos, clasifica años completos, parciales o sin cotización y contrasta la suma de cuotas con el Paso 2.

### Proyección salarial

`proyeccion_salarios.py` normaliza periodicidades y genera escenarios salariales manteniendo precisión interna. Los importes mensual y anual se derivan desde el valor preciso y se redondean de forma independiente al presentarse.

### Línea temporal

`linea_tiempo.py` integra historial, año actual y futuro sin sobrescribir información real. Los años con cero cuotas se representan explícitamente como `SIN_COTIZACION`.

### Retiro

`retiro.py` calcula edad, fecha de referencia y escenarios por fecha exacta. La estimación de cuotas:

- respeta primero el cierre del año actual indicado en el Paso 2;
- aplica después la densidad anual futura;
- mantiene visible que se trata de una aproximación cuando no existe detalle mensual;
- verifica si la proyección salarial alcanza el horizonte de retiro seleccionado.

Este servicio no determina por sí mismo la elegibilidad legal.

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
POST /api/simulacion/retiro
```

## Interfaz del asistente

El asistente conserva estado temporal en `sessionStorage`.

Los módulos principales del frontend son:

- `simulacion.js`: estado compartido, navegación y formularios generales;
- `historial_salarios.js`: historial anual;
- `linea_tiempo.js`: presentación integrada del Paso 4;
- `retiro.js`: Paso 5 y escenarios de retiro;
- `moneda.js`: entrada/formato monetario con separadores de miles y máximo dos decimales;
- `navegacion_wizard.js`: barra de navegación rápida `sticky` para pasos extensos.

Los parciales Jinja `historial_salarial.html` y `retiro.html` mantienen modularizadas las secciones de mayor complejidad.

## Persistencia

No existe todavía persistencia permanente. `sessionStorage` conserva únicamente el estado temporal de la pestaña. SQLite y el guardado voluntario pertenecen a una fase posterior.

## Validación

La base actual utiliza:

```powershell
python -m compileall app
python -m unittest discover -s tests -v
```

además de pruebas manuales del flujo web. Los casos de validación reales deben anonimizarse y sus documentos originales no se versionan.
