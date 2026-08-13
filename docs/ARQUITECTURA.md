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
7. **Identidad centralizada:** nombre, descripción pública, autoría y enlace a Mi Caja Digital se definen en `app/core/config.py`, separados de la normativa previsional.

## 2. Estructura del repositorio

```text
app/
├── core/
│   ├── config.py
│   ├── constants.py
│   ├── dinero.py
│   └── normativa.py
├── modelos/
│   ├── comparacion.py
│   ├── pension.py
│   ├── resultado_unificado.py
│   ├── simulacion.py
│   └── trazabilidad.py
├── motores/
│   ├── elegibilidad.py
│   ├── sebd.py
│   ├── sebd_modalidades.py
│   ├── mixto.py
│   └── sucgs.py
├── servicios/
│   ├── comparador.py
│   ├── fuentes_normativas.py
│   ├── historial_salarios.py
│   ├── linea_tiempo.py
│   ├── proyeccion_cuotas.py
│   ├── proyeccion_salarios.py
│   ├── resultado_unificado.py
│   ├── resultados.py
│   ├── resultados_sebd.py
│   ├── resultados_mixto.py
│   ├── resultados_sucgs.py
│   ├── retiro.py
│   └── trazabilidad.py
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── design-system.css
│   │   └── accesibilidad.css
│   └── js/
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
- semántica accesible transversal y ayudas contextuales;
- gestión del foco y estados de validación visibles/no visuales;
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
Paso 3 — Historial + detalle reciente + base salarial
        ↓
Paso 4 — Proyección + línea temporal
        ↓
Paso 5 — Escenarios de retiro
        ↓
Paso 6 — Motor del sistema seleccionado
        ↓
Resultado + desglose + advertencias + fuente normativa
```

Cada paso posterior depende de información validada de los anteriores. Si el Asegurado(a) modifica un dato de origen, los resultados dependientes se invalidan.

El detalle reciente de UX.4.4 se procesa en `app/servicios/detalle_anio_actual.py`. Es una capa de normalización y consistencia, no un motor legal: separa salarios visibles, cuotas acreditadas y períodos parciales; cuando existe coherencia con el Paso 2 puede sincronizar el año actual del historial y aportar una base salarial para proyección.

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
POST /api/simulacion/detalle-anio-actual
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

Estado técnico actual después de UX.4.6a: **198 pruebas automatizadas**.

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

## Metodología y fuentes

La ruta `GET /metodologia` renderiza un catálogo transversal construido por `app/servicios/fuentes_normativas.py`. El servicio reutiliza las URLs de `normativa/*.json` y añade únicamente títulos, agrupación y alcance para la interfaz.

La trazabilidad conserva IDs estables para relacionar pasos con fuentes, pero `resultados.js` resuelve esos IDs contra `trazabilidad.fuentes` antes de mostrarlos. Los IDs internos no forman parte de la experiencia visible del Asegurado(a).

## Capa transversal de resultado final

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

## Apariencia y accesibilidad transversal

`app/templates/base.html` concentra navegación, control de apariencia, enlace de salto, región viva global y pie de página. `app/static/js/tema.js` resuelve la preferencia visual y la conserva en `localStorage`; no accede ni modifica el estado previsional del asistente.

La presentación CSS usa tres capas con responsabilidades distintas:

1. `app/static/css/style.css` — base histórica, reglas funcionales y responsive ya estabilizadas;
2. `app/static/css/design-system.css` — tokens y acabado visual transversal de UX.4.6a para Claro, Oscuro y componentes globales;
3. `app/static/css/accesibilidad.css` — ayudas contextuales, foco y estados accesibles con precedencia final.

Alto contraste conserva tokens explícitos dentro de la capa visual moderna y las reglas accesibles continúan prevaleciendo. Bootstrap resuelve controles estándar mediante `data-bs-theme`.

`app/static/js/accesibilidad.js` constituye una capa de presentación transversal: relaciona ayudas con controles, sincroniza semántica del wizard, prepara mensajes dinámicos, captions de tablas, foco de validación y avisos accesibles para enlaces externos. Las ayudas se abren mediante hover o foco y conservan clic como alternativa táctil. No calcula cuotas, salarios, edades ni prestaciones y no modifica el estado previsional guardado.

La accesibilidad base y UX.4.1 se implementan en la capa global para que Inicio, Simulación, Comparador y Metodología compartan comportamiento coherente sin duplicarlo en cada plantilla.


## UX.3 — adaptación responsive y dato mensual de cuotas

La presentación mantiene una única plantilla global y una sola hoja principal de estilos. UX.3 no introduce una aplicación móvil separada: `style.css` reorganiza navegación, tarjetas, formularios y acciones mediante breakpoints, mientras que las tablas extensas conservan su estructura dentro de contenedores desplazables. En anchos inferiores a 768 px, la navegación persistente del wizard pasa a la parte inferior y respeta las áreas seguras del dispositivo.

En el Paso 5, JavaScript captura `ultimo_mes_cuotas` con granularidad `YYYY-MM` y envía también la fecha técnica equivalente. El servicio de retiro vuelve a derivar y validar ese corte en Python; por tanto, la interfaz no se convierte en fuente de verdad para la regla temporal. `fecha_corte_cuotas` se conserva para compatibilidad con solicitudes y pruebas anteriores.

## Herramientas de desarrollo fuera del runtime

Las dependencias de ejecución Python continúan centralizadas en `requirements.txt`. Node.js LTS no forma parte del runtime ni se instala mediante `pip`; se usa únicamente como herramienta opcional para validaciones estáticas como `node --check`. Actualmente no existe una cadena de compilación frontend ni dependencias npm que requieran `package.json`.


## UX.4.3 — canal de errores y foco de recuperación

`app/static/js/accesibilidad.js` mantiene la semántica de validación separada de la lógica de negocio. La validación crea un mensaje inline visible asociado al campo mediante `aria-errormessage`; al corregirse el valor, se elimina tanto el mensaje como `aria-invalid`. Los errores generales generados por servicios o reglas del frontend permanecen en sus contenedores visibles existentes y reciben foco únicamente cuando pasan de ocultos a visibles.

La presentación nativa variable del navegador se suprime durante `invalid`; la aplicación conserva el bloqueo de envío, enfoca el primer control inválido y presenta su propio mensaje consistente. Esta capa evita duplicar anuncios urgentes: `role="alert"` es suficiente para errores críticos y no se combina con otra región `aria-live="assertive"`. Las advertencias no urgentes pueden usar `status/polite`. La tabla de retiro conserva el radio como único control enfocable de cada fila; Enter se añade como alternativa de teclado sin introducir un segundo tab stop en el `<tr>`.

El `MutationObserver` transversal observa inserciones y cambios de clase necesarios para componentes dinámicos. Toda mutación de clase realizada por funciones llamadas desde ese observador debe ser idempotente: antes de añadir una clase se verifica que no exista y antes de retirarla se verifica que esté presente. Esto evita realimentaciones infinitas del propio observador y protege el hilo principal del navegador. La limpieza de errores consulta `ValidityState.valid` para no redisparar `invalid` mediante `checkValidity()`.


## UX.4.4 — dato derivado de edad en presentación

`app/static/js/linea_tiempo.js` deriva la edad anual desde `simulacion.persona.fecha_nacimiento` únicamente para renderizar las tablas del Paso 4. No se añade un campo nuevo a los modelos ni a los endpoints de cálculo: la fecha de nacimiento continúa siendo la fuente única y la edad se recalcula como `año - año de nacimiento` al construir cada fila.


## Referencia PDF personal de Mi Retiro Seguro

`app/servicios/referencia_mi_retiro_seguro.py` constituye una capa de extracción documental, no un motor previsional. El endpoint `POST /api/simulacion/referencia-mi-retiro-seguro` recibe un `UploadFile`, limita tamaño y tipo, lee el PDF en memoria con `pypdf` y devuelve un contrato reducido sin identificadores personales directos.

`app/static/js/referencia_mi_retiro_seguro.js` conserva el resumen extraído únicamente dentro del estado temporal de la pestaña. En Resultados compara esa referencia con `resumen_unificado`, reutilizando la semántica común de pensión mensual o pago único. El motor actual sigue siendo la fuente del resultado de Mi Retiro Proyectado; el PDF solo aporta una fotografía personal externa.


## Importación revisable de documentos oficiales

UX.4.4 centraliza en el Paso 1 dos entradas opcionales: `referencia_mi_retiro_seguro.py` y `ficha_digital.py`. Ambos servicios reciben bytes de PDF, extraen texto con `pypdf` y devuelven contratos sin persistir el archivo. La extracción es deliberadamente separada de la escritura del estado de simulación.

`app/static/js/importacion_datos_oficiales.js` mantiene el borrador detectado únicamente en memoria del navegador mientras la vista previa está abierta. La escritura en `sessionStorage` ocurre al confirmar. El comprobante puede prellenar `persona`, partes de `cuotas`, `historial` y `referencia_mi_retiro_seguro`; la Ficha Digital filtra desde el backend y conserva únicamente los salarios del año calendario actual; esos mismos registros pueden pasar al `detalle_anio_actual` después de la confirmación.

El importador no ejecuta motores legales ni valida elegibilidad. Después de la confirmación invalida resultados derivados para obligar a recalcular con los datos revisados. Las filas proyectadas del comprobante se mantienen fuera del historial real por defecto y la presencia de salario en Ficha Digital nunca implica una cuota acreditada.


### Alcance temporal y formato de la Ficha Digital

El parser `ficha_digital.py` descarta períodos de años distintos al año calendario actual antes de construir `ResumenFichaDigital`. De esta forma el frontend no recibe ni persiste contexto histórico que no vaya a utilizarse en el detalle mensual. Los campos monetarios editables de las vistas previas reutilizan `moneda.js`: se muestran con coma de miles y dos decimales, se editan sin separadores visuales y se normalizan de nuevo al salir del campo.


## UX.4.5 — doble integración sin duplicar motores

Los modelos integrados de SEBD, Mixto y SUCGS incorporan `modo_integracion`, con `PROYECTADO` como valor predeterminado y `SOLO_ACREDITADO` como fotografía alternativa. `app/servicios/resultados.py` ajusta el escenario seleccionado en modo acreditado para conservar la fecha/edad de retiro, fijar las cuotas al total real del historial y eliminar cuotas futuras. La construcción cronológica existente recibe entonces cero cuotas nuevas y no consume salarios proyectados.

Los tres servicios de resultados reutilizan sus motores legales sin ramas de fórmula paralelas. El frontend solicita ambas fotografías, almacena cada una por separado en `sessionStorage` y las invalida conjuntamente cuando cambia una dependencia. La comparación con Mi Retiro Seguro consulta primero la fotografía acreditada guardada y solo recurre al resultado proyectado si todavía no existe aquella.


## Hardening previo a beta

La frontera HTTP valida los PDFs mediante `app/core/archivos_pdf.py` antes de delegar en `referencia_mi_retiro_seguro.py` o `ficha_digital.py`. La validación cubre extensión, MIME tolerado, tamaño, vacío y firma PDF; los parsers conservan límites independientes de páginas y texto extraído.

Un middleware transversal añade cabeceras defensivas que no modifican la semántica de los cálculos. Los endpoints de importación declaran `Cache-Control: no-store`.

La verificación continua vive en `.github/workflows/ci.yml` y trata el repositorio como una instalación limpia: instala `requirements.txt`, ejecuta `pip check`, compila Python, valida JavaScript y corre la suite. La primera ejecución remota de `main` quedó en verde sobre Python 3.13 y 3.14. Las regresiones de infraestructura validan la presencia de las Actions y el contrato del pipeline mediante patrones de versión, evitando fijar un major concreto.

`requirements.txt` continúa siendo el snapshot reproducible completo, pero distingue documentalmente las dependencias directas de las transitivas fijadas. `.github/dependabot.yml` limita las propuestas ordinarias de `pip` a las dependencias directas, agrupa actualizaciones minor/patch compatibles del runtime y agrupa GitHub Actions. `pypdf` queda fuera del grupo general para que los cambios de parser se revisen de forma individual. No existe auto-merge.

## UX.4.6a — sistema visual sin acoplamiento al motor

La capa `design-system.css` no forma parte del dominio previsional. Puede redefinir color, tipografía, superficies, controles, cards, navegación, footer, wizard, Comparador y Metodología/Fuentes, pero no contiene reglas de edad, cuotas, salario, elegibilidad ni prestación.

La página `index.html` utiliza un mockup puramente presentacional construido con HTML/CSS. El marcador `B/. —` evita presentar una cifra ficticia y no se vincula a ninguna respuesta del backend.

La simplificación de etiquetas del header es únicamente visual: `/`, `/simulacion`, `/comparar` y `/metodologia` continúan siendo las rutas reales. El footer consume `app_version` desde la configuración común y enlaza a la vista de Fuentes; Mi Caja Digital permanece en los flujos de verificación individual.
