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
│   ├── simulacion.py
│   └── pension.py
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
│   ├── resultados.py
│   └── retiro.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── partials/
└── main.py
```

La modalidad normal del SEBD ya dispone de motor legal e integración con el asistente. Las demás modalidades y sistemas continúan en preparación.

## Núcleo común

### `app/core/dinero.py`

Centraliza la conversión a `Decimal`, la validación de precisión y el redondeo monetario técnico. El criterio general actual es conservar precisión durante la operación y redondear a centavos con `ROUND_HALF_UP` al materializar un importe, salvo que una regla normativa específica exija otra cosa.

### `app/core/normativa.py`

Carga parámetros versionados desde `normativa/`. `parametros_generales.json` mantiene edades de referencia y metadatos comunes, mientras `sebd.json` contiene la primera parametrización específica del SEBD normal. Mixto, SUCGS y las demás modalidades se incorporarán conforme se verifiquen e implementen.

## Modelos

`app/modelos/simulacion.py` define estructuras Pydantic para:

- cuotas;
- historial salarial anual;
- salario actual y equivalencias;
- configuración y escenarios de proyección salarial;
- línea temporal histórica/proyectada;
- fechas y escenarios preliminares de retiro.

Los campos monetarios y porcentuales editables relevantes validan como máximo dos decimales en la frontera del backend.

`app/modelos/pension.py` define las entradas y salidas de los motores legales y de la capa de integración del Paso 6.

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
POST /api/simulacion/sebd/normal
POST /api/simulacion/resultados/sebd-normal
```

## Interfaz del asistente

El asistente conserva estado temporal en `sessionStorage`.

Los módulos principales del frontend son:

- `simulacion.js`: estado compartido, navegación y formularios generales;
- `historial_salarios.js`: historial anual;
- `linea_tiempo.js`: presentación integrada del Paso 4;
- `retiro.js`: Paso 5, escenarios de retiro y selección del escenario que alimenta Resultados;
- `resultados.js`: Paso 6, selección salarial, llamada al endpoint integrado y presentación del desglose SEBD;
- `moneda.js`: entrada/formato monetario con separadores de miles y máximo dos decimales;
- `navegacion_wizard.js`: barra de navegación rápida `sticky` para pasos extensos.

Los parciales Jinja `historial_salarial.html`, `retiro.html` y `resultados.html` mantienen modularizadas las secciones de mayor complejidad.

## Persistencia

No existe todavía persistencia permanente. `sessionStorage` conserva únicamente el estado temporal de la pestaña. SQLite y el guardado voluntario pertenecen a una fase posterior.

## Validación

La base actual utiliza:

```powershell
python -m compileall app
python -m unittest discover -s tests -v
```

además de pruebas manuales del flujo web. Los casos de validación reales deben anonimizarse y sus documentos originales no se versionan.

## Capa legal del Paso 6

El Paso 6 introduce una separación adicional:

```text
modelos/pension.py
        ↓
motores/elegibilidad.py
        ↓
motores/sebd.py
        ↓
API /api/simulacion/sebd/normal
```

Los parámetros legales se obtienen desde `normativa/sebd.json`; la interfaz no contiene porcentajes ni topes codificados directamente.

## Integración del Paso 6

La interfaz no construye directamente la entrada jurídica del motor. La capa de integración queda separada:

```text
Pasos 1–5 / sessionStorage
        ↓
partials/resultados.html + resultados.js
        ↓
POST /api/simulacion/resultados/sebd-normal
        ↓
servicios/resultados.py
        ↓
motores/sebd.py
```

`servicios/resultados.py` consolida el historial real, la línea temporal salarial y el escenario de retiro seleccionado. Cuando un retiro futuro corta un año proyectado, consume cronológicamente las cuotas disponibles y prorratea únicamente el salario asociado a las cuotas utilizadas.

El motor legal sigue siendo independiente de esta capa: recibe una estructura `DatosCalculoSEBDNormal` ya coherente y no depende de HTML, `sessionStorage` ni del flujo visual.

El Paso 5 incorpora una selección explícita del escenario que alimentará el Paso 6. Los escenarios pasados pueden mostrarse, pero no se usan automáticamente para reconstruir cuotas históricas a una fecha exacta cuando solo existe detalle anual.


## Extensión Paso 6C

La arquitectura SEBD queda dividida en dos niveles compatibles:

```text
sebd.py
└─ motor Normal validado y compatibilidad de regresión

sebd_modalidades.py
├─ clasificador aplicado al cálculo
├─ Anticipada
├─ Proporcional
└─ Proporcional Anticipada

resultados_sebd.py
└─ integra el escenario del asistente con el motor general
```

Los endpoints previos de SEBD Normal se conservan para regresión, mientras se añaden endpoints generales que permiten evolucionar el Paso 6 sin romper las pruebas existentes.
