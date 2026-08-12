# Arquitectura

La aplicación sigue una arquitectura web local con separación explícita entre interfaz, servicios de integración, motores previsionales y parámetros normativos.

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Principios

1. **Una sola fuente de verdad para el cálculo:** las fórmulas viven en Python, no en JavaScript.
2. **Normativa versionada:** parámetros modificables se almacenan en `normativa/`.
3. **Datos reales y proyectados separados:** ninguna proyección reemplaza silenciosamente el historial.
4. **Resultados auditables:** los motores exponen valores intermedios, factores, advertencias y fuentes.
5. **Datos faltantes explícitos:** un parámetro oficial ausente produce un resultado pendiente, no una estimación inventada.
6. **Privacidad por defecto:** la sesión del asistente se conserva temporalmente en el navegador; no se persiste automáticamente información personal.

## 2. Estructura del repositorio

```text
app/
├── core/
│   ├── config.py
│   ├── constants.py
│   ├── dinero.py
│   └── normativa.py
├── modelos/
│   ├── pension.py
│   └── simulacion.py
├── motores/
│   ├── elegibilidad.py
│   ├── sebd.py
│   ├── sebd_modalidades.py
│   ├── mixto.py
│   └── sucgs.py
├── servicios/
│   ├── comparador.py
│   ├── historial_salarios.py
│   ├── linea_tiempo.py
│   ├── proyeccion_cuotas.py
│   ├── proyeccion_salarios.py
│   ├── resultados.py
│   ├── resultados_sebd.py
│   ├── resultados_mixto.py
│   ├── resultados_sucgs.py
│   └── retiro.py
├── static/
├── templates/
└── main.py

normativa/
├── parametros_generales.json
├── sebd.json
├── mixto.json
└── sucgs.json

tests/
docs/
data/
```

## 3. Capas de la aplicación

### 3.1. Presentación

Ubicación:

- `app/templates/`
- `app/static/css/`
- `app/static/js/`

Responsabilidades:

- formularios;
- navegación entre pasos;
- formato visual;
- estado temporal en `sessionStorage`;
- envío de solicitudes a FastAPI;
- representación de resultados y advertencias.

No debe contener fórmulas previsionales independientes del backend.

### 3.2. API

`app/main.py` expone las vistas HTML y los endpoints de cálculo.

La API actúa como frontera entre la interfaz y los servicios/motores.

### 3.3. Modelos

`app/modelos/simulacion.py` define contratos para:

- cuotas;
- historial;
- salario;
- proyección;
- línea temporal;
- retiro.

`app/modelos/pension.py` contiene contratos específicos de:

- SEBD;
- Subsistema Mixto;
- SUCGS;
- resultados integrados.

### 3.4. Servicios de integración

Los servicios transforman el estado de los Pasos 1–5 en entradas coherentes para cada motor.

Ejemplos:

- `historial_salarios.py`: valida y normaliza historial;
- `proyeccion_salarios.py`: construye escenarios;
- `linea_tiempo.py`: combina realidad y proyección;
- `retiro.py`: genera escenarios de retiro y cuotas futuras;
- `resultados_sebd.py`: prepara entrada SEBD;
- `resultados_mixto.py`: prepara entrada Mixto;
- `resultados_sucgs.py`: prepara entrada SUCGS.

### 3.5. Motores legales

Los motores reciben datos ya consolidados y aplican las reglas previsionales:

- `sebd.py`: cálculo normal base;
- `sebd_modalidades.py`: clasificación y modalidades generales SEBD;
- `mixto.py`: BD + CAP, opciones, pagos únicos y transición;
- `sucgs.py`: componente contributivo, capa solidaria y garantía de reemplazo.

### 3.6. Núcleo común

#### `app/core/dinero.py`

Centraliza:

- conversión segura a `Decimal`;
- materialización a centavos;
- `ROUND_HALF_UP`;
- utilidades comunes de precisión monetaria.

#### `app/core/normativa.py`

Carga los JSON versionados de `normativa/` y evita dispersar constantes legales por múltiples módulos.

## 4. Flujo de datos del asistente

```text
Paso 1 — Datos personales
        ↓
Paso 2 — Cuotas
        ↓
Paso 3 — Historial + salario actual
        ↓
Paso 4 — Proyección + línea temporal
        ↓
Paso 5 — Escenarios de retiro
        ↓
Paso 6 — Motor del sistema seleccionado
        ↓
Resultado + desglose + advertencias + fuente normativa
```

Cada paso posterior depende de información validada de los anteriores. Si el usuario modifica un dato de origen, los resultados dependientes se invalidan.

## 5. Navegación y estado temporal

El asistente utiliza `sessionStorage` para preservar temporalmente:

- datos de los pasos;
- escenarios construidos;
- selección de retiro;
- configuración específica Mixto/SUCGS;
- último resultado calculado.

La navegación permite abrir directamente pasos ya disponibles mediante:

- indicadores superiores;
- selector persistente `Ir a paso`.

Un paso posterior permanece deshabilitado si sus prerrequisitos dejaron de ser válidos.

## 6. Endpoints actuales

### 6.1. Vistas

```text
GET /
GET /simulacion
GET /comparar
GET /salud
```

### 6.2. Servicios comunes

```text
POST /api/simulacion/cuotas
POST /api/simulacion/historial-salarial
POST /api/simulacion/salario
POST /api/simulacion/proyeccion-salario
POST /api/simulacion/linea-tiempo
POST /api/simulacion/retiro
```

### 6.3. SEBD

```text
POST /api/simulacion/sebd/normal
POST /api/simulacion/resultados/sebd-normal
POST /api/simulacion/sebd
POST /api/simulacion/resultados/sebd
```

### 6.4. Mixto

```text
POST /api/simulacion/mixto
POST /api/simulacion/resultados/mixto
```

### 6.5. SUCGS

```text
POST /api/simulacion/sucgs
POST /api/simulacion/resultados/sucgs
```

## 7. Arquitectura normativa

Los archivos `normativa/*.json` contienen parámetros y metadatos de fuente.

La documentación se divide entre:

- [NORMATIVA.md](NORMATIVA.md): cómo se aplica/versiona cada regla;
- [FUENTES_NORMATIVAS.md](FUENTES_NORMATIVAS.md): enlaces oficiales y mapa de artículos;
- [DECISIONES.md](DECISIONES.md): criterios adoptados ante ambigüedad o decisiones de diseño.

## 8. Precisión y representación monetaria

La lógica monetaria se ejecuta con `Decimal` cuando corresponde. JavaScript puede formatear valores para presentación, pero no debe alterar el resultado legal calculado en Python.

Los valores actuariales que son factores/divisores no se presentan como importes monetarios.

## 9. Pruebas

La validación automatizada usa `unittest` y cubre:

- utilidades monetarias;
- proyección;
- línea temporal;
- retiro;
- SEBD;
- Mixto;
- SUCGS;
- servicios integrados.

Estado después del cierre 6F.4: **69 pruebas**.

Ver [VALIDACION.md](VALIDACION.md).

## 10. Capa transversal 6F

6F.1 agrega:

- `app/modelos/comparacion.py` para solicitudes y salidas normalizadas;
- `app/servicios/comparador.py` para coordinar los tres motores sin replicar fórmulas;
- `POST /api/simulacion/comparar-escenarios`;
- `app/static/js/comparador.js` y la página `/comparar`.

6F.2 agrega `app/servicios/trazabilidad.py` y `app/modelos/trazabilidad.py`. El servicio no recalcula prestaciones: transforma resultados ya emitidos por los motores en una cadena auditable y obtiene las URLs oficiales desde `normativa/*.json`.

6F.3 agrega la metodología visible y los enlaces normativos clicables. 6F.4 agrega el contrato transversal de resultado final reutilizable por comparador, interfaz y futuros informes.

Toda la capa 6F consume resultados de los motores existentes; no crea una cuarta implementación de las fórmulas.

## Metodología 6F.3

La ruta `GET /metodologia` renderiza un catálogo transversal construido por `app/servicios/fuentes_normativas.py`. El servicio reutiliza las URLs de `normativa/*.json` y añade únicamente títulos, agrupación y alcance para la interfaz.

La trazabilidad 6F.2 conserva IDs estables para relacionar pasos con fuentes, pero `resultados.js` resuelve esos IDs contra `trazabilidad.fuentes` antes de mostrarlos. Los IDs internos no forman parte de la experiencia visible del usuario.

## Capa transversal de resultado final — 6F.4

`app/modelos/resultado_unificado.py` define el contrato común `ResumenPrestacionUnificada`. `app/servicios/resultado_unificado.py` adapta resultados ya calculados de SEBD, Mixto y SUCGS sin ejecutar fórmulas previsionales.

Flujo:

```text
Motor específico
    ↓
Resultado integrado del sistema
    ↓
Trazabilidad 6F.2
    ↓
Resumen unificado 6F.4
    ↓
Paso 6 / Comparador / futuras exportaciones
```

`calculo` conserva siempre el detalle jurídico completo. `resumen_unificado` existe para semántica transversal y no puede convertirse en una cuarta capa de cálculo.

