# Arquitectura

La aplicación sigue una arquitectura web local con separación explícita entre interfaz, servicios de integración, motores previsionales y parámetros normativos.

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Principios

1. **Una sola fuente de verdad para el cálculo:** las fórmulas viven en Python, no en JavaScript.
2. **Normativa versionada:** parámetros modificables se almacenan en `regulations/`.
3. **Datos reales y proyectados separados:** ninguna proyección reemplaza silenciosamente el historial.
4. **Resultados auditables:** los motores exponen valores intermedios, factores, advertencias y fuentes.
5. **Datos faltantes explícitos:** un parámetro oficial ausente produce un resultado pendiente, no una estimación inventada.
6. **Privacidad por defecto:** la sesión del asistente se conserva temporalmente en el navegador; no se persiste automáticamente información personal.
7. **Identidad y versión centralizadas:** nombre, descripción pública, autoría y enlace a Mi Caja Digital se definen en `app/core/config.py`; la versión de aplicación procede exclusivamente de `VERSION` mediante `app/core/version.py`. Ambos contratos permanecen separados de la normativa previsional.

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

regulations/
├── parametros_generales.json
├── sebd.json
├── mixto.json
└── sucgs.json

tests/
docs/
data/
VERSION
VERSIONING.md
GOVERNANCE.md
RELEASES.md
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

`app/models/simulacion.py` define contratos para:

- cuotas;
- historial;
- salario;
- proyección;
- línea temporal;
- retiro.

`app/models/pension.py` contiene contratos específicos de:

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

Carga los JSON versionados de `regulations/` y evita dispersar constantes legales por múltiples módulos.

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

El detalle reciente de UX.4.4 se procesa en `app/services/detalle_anio_actual.py`. Es una capa de normalización y consistencia, no un motor legal: separa salarios visibles, cuotas acreditadas y períodos parciales; cuando existe coherencia con el Paso 2 puede sincronizar el año actual del historial y aportar una base salarial para proyección.

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

Los archivos `regulations/*.json` contienen parámetros y metadatos de fuente.

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

Estado técnico de cierre de UX.4.6c Revisión 3: **253 pruebas automatizadas en OK**.

Ver [VALIDACION.md](VALIDACION.md).

## 10. Capa transversal 6F

6F.1 agrega:

- `app/models/comparacion.py` para solicitudes y salidas normalizadas;
- `app/services/comparador.py` para coordinar los tres motores sin replicar fórmulas;
- `POST /api/simulacion/comparar-escenarios`;
- `app/static/js/comparador.js` y la página `/comparar`.

6F.2 agrega `app/services/trazabilidad.py` y `app/models/trazabilidad.py`. El servicio no recalcula prestaciones: transforma resultados ya emitidos por los motores en una cadena auditable y obtiene las URLs oficiales desde `regulations/*.json`.

6F.3 agrega la metodología visible y los enlaces normativos clicables. 6F.4 agrega el contrato transversal de resultado final reutilizable por comparador, interfaz y futuros informes.

Toda la capa 6F consume resultados de los motores existentes; no crea una cuarta implementación de las fórmulas.

## Metodología y fuentes

La ruta `GET /metodologia` renderiza un catálogo transversal construido por `app/services/fuentes_normativas.py`. El servicio reutiliza las URLs de `regulations/*.json` y añade únicamente títulos, agrupación y alcance para la interfaz.

La trazabilidad conserva IDs estables para relacionar pasos con fuentes, pero `resultados.js` resuelve esos IDs contra `trazabilidad.fuentes` antes de mostrarlos. Los IDs internos no forman parte de la experiencia visible del Asegurado(a).

## Capa transversal de resultado final

`app/models/resultado_unificado.py` define el contrato común `ResumenPrestacionUnificada`. `app/services/resultado_unificado.py` adapta resultados ya calculados de SEBD, Mixto y SUCGS sin ejecutar fórmulas previsionales.

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

`app/services/referencia_mi_retiro_seguro.py` constituye una capa de extracción documental, no un motor previsional. El endpoint `POST /api/simulacion/referencia-mi-retiro-seguro` recibe un `UploadFile`, limita tamaño y tipo, lee el PDF en memoria con `pypdf` y devuelve un contrato revisable. Desde UX.4.6b puede incluir identificadores personales opcionales cuando el PDF los etiqueta de forma inequívoca; el código único del documento continúa excluido y el archivo no se persiste.

`app/static/js/referencia_mi_retiro_seguro.js` conserva el resumen extraído únicamente dentro del estado temporal de la pestaña. En Resultados compara esa referencia con `resumen_unificado`, reutilizando la semántica común de pensión mensual o pago único. El motor actual sigue siendo la fuente del resultado de Mi Retiro Proyectado; el PDF solo aporta una fotografía personal externa.


## Importación revisable de documentos oficiales

UX.4.4 centraliza en el Paso 1 dos entradas opcionales: `referencia_mi_retiro_seguro.py` y `ficha_digital.py`. Ambos servicios reciben bytes de PDF, extraen texto con `pypdf` y devuelven contratos sin persistir el archivo. La extracción es deliberadamente separada de la escritura del estado de simulación.

`app/static/js/importacion_datos_oficiales.js` mantiene el borrador detectado únicamente en memoria del navegador mientras la vista previa está abierta. La escritura en `sessionStorage` ocurre al confirmar. El comprobante puede prellenar `persona`, partes de `cuotas`, `historial` y `referencia_mi_retiro_seguro`; la Ficha Digital filtra desde el backend y conserva únicamente los salarios del año calendario actual; esos mismos registros pueden pasar al `detalle_anio_actual` después de la confirmación.

El importador no ejecuta motores legales ni valida elegibilidad. Después de la confirmación invalida resultados derivados para obligar a recalcular con los datos revisados. Las filas proyectadas del comprobante se mantienen fuera del historial real por defecto. Desde UX.4.6d R3, un mes detectado por Ficha Digital se incorpora con su casilla de cuota fijada como parte del registro documental confirmado; meses no presentes permanecen manuales.


### Alcance temporal y formato de la Ficha Digital

El parser `ficha_digital.py` descarta períodos de años distintos al año calendario actual antes de construir `ResumenFichaDigital`. De esta forma el frontend no recibe ni persiste contexto histórico que no vaya a utilizarse en el detalle mensual. Los campos monetarios editables de las vistas previas reutilizan `moneda.js`: se muestran con coma de miles y dos decimales, se editan sin separadores visuales y se normalizan de nuevo al salir del campo.


## UX.4.5 — doble integración sin duplicar motores

Los modelos integrados de SEBD, Mixto y SUCGS incorporan `modo_integracion`, con `PROYECTADO` como valor predeterminado y `SOLO_ACREDITADO` como fotografía alternativa. `app/services/resultados.py` ajusta el escenario seleccionado en modo acreditado para conservar la fecha/edad de retiro, fijar las cuotas al total real del historial y eliminar cuotas futuras. La construcción cronológica existente recibe entonces cero cuotas nuevas y no consume salarios proyectados.

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



## UX.4.6b — frontera de Datos personales e importación

La capa de presentación mantiene `simulacion.persona` en `sessionStorage` y agrega `modo_datos_personales` y `origen_persona`. Los identificadores opcionales no se envían a los motores previsionales: solo fecha de nacimiento, sexo, fecha de ingreso y sistema continúan alimentando las dependencias de cálculo correspondientes.

`app/templates/partials/importacion_datos_oficiales.html` queda dedicado a Mi Retiro Seguro en el Paso 1. `app/templates/partials/importacion_ficha_digital.html` contiene la importación salarial trasladada al Paso 3. Ambos reutilizan `app/static/js/importacion_datos_oficiales.js`, manteniendo una sola frontera HTTP por tipo de documento.

La navegación del wizard conserva selectores históricos por compatibilidad, pero UX.4.6b renderiza dos instancias `wizard-navigation-bar` sincronizadas por `data-wizard-*`: superior e inferior. En PC/laptop la barra superior utiliza `position: sticky` bajo el header dentro del mismo ancho de las tarjetas; la inferior permanece en el flujo normal al final del panel. Ninguna de las dos duplica lógica de negocio.


### UX.4.6b R2 — consentimiento y frontera de privacidad

`app/templates/partials/privacidad_consentimiento.html` y `app/static/js/privacidad.js` forman la puerta previa a la captura de datos en `/simulacion`. El consentimiento se versiona en `localStorage`; no contiene la simulación ni identificadores. La autorización activa se marca además en `sessionStorage`, por lo que una nueva sesión de pestaña vuelve a mostrar el modal aunque exista una aceptación histórica de la misma versión. Rechazar elimina el estado de simulación y la marca de consentimiento y vuelve a Inicio.

`sessionStorage` continúa siendo el almacén temporal de la simulación. La política de privacidad, la modalidad de origen y los identificadores no alteran la interfaz de los motores: solo los datos previsionales necesarios pasan a los servicios de cálculo.

La frontera HTTP aplica `Cache-Control: no-store` a `/api/simulacion/*`. Las cabeceras globales incluyen CSP, `nosniff`, denegación de framing, `Referrer-Policy` y `Permissions-Policy`. Mientras Bootstrap permanezca en jsDelivr, `base.html` usa Subresource Integrity; antes de la beta pública se recomienda servir Bootstrap desde `app/static/` para eliminar esa solicitud de tercero.

La página `/metodologia#privacidad-datos` expone al Asegurado(a) un resumen de privacidad y enlaces oficiales de la Ley 81 de 2019, Decreto Ejecutivo 285 de 2021 y ANTAI. La documentación extendida vive en `docs/POLITICA_PRIVACIDAD.md`, `docs/TERMINOS_USO_PRIVACIDAD.md` y `docs/CUMPLIMIENTO_LEY_81.md`.

### UX.4.6b R3 — consentimiento y navegación del asistente

La ruta `Simular` incorpora una puerta de consentimiento previa a la captura/importación. El documento visible es versionado y la casilla de aceptación solo se habilita después de alcanzar el final del contenido. El estado de aceptación se gestiona en el navegador y se invalida cuando cambia la versión del texto.

La navegación del wizard se renderiza dos veces dentro del mismo contenedor de ancho que las tarjetas: una barra superior y otra inferior. Ambos controles comparten `data-wizard-*` y son sincronizados por `navegacion_wizard.js`; no contienen lógica de negocio propia. En escritorio la barra superior puede usar `position: sticky` bajo el encabezado global para mantener accesibles Inicio/Anterior, selector de paso y acción primaria durante pasos largos.

Las ayudas contextuales del formulario pueden proyectarse fuera del borde de `.simulation-card` para evitar recortes por `overflow` cuando se abren cerca del final de la página.


### UX.4.6b R4 — cierre de lectura y criterio de contenido público

La detección de llegada al final del documento de privacidad continúa siendo una condición de interfaz para habilitar la casilla de consentimiento, pero no genera un bloque de “fin” ni un mensaje de “lectura completada”. Antes de llegar al final se conserva únicamente la ayuda necesaria para explicar por qué la casilla todavía está deshabilitada; al cumplirse el requisito, esa ayuda desaparece.

Como criterio transversal de presentación, las plantillas públicas deben limitar la redacción a información funcional, previsional, legal, de privacidad, seguridad o accesibilidad que ayude al usuario a operar o comprender el alcance del producto. Terminología de implementación, mensajes meta de desarrollo o posicionamientos ajenos al propósito de Mi Retiro Proyectado —por ejemplo presentarlo como recurso educativo/didáctico— no deben formar parte de la interfaz salvo que exista una función real que lo justifique.


## UX.4.6c — frontera de cuotas acreditadas e hipótesis futuras

El Paso 2 conserva `DatosCuotas` como contrato del backend, pero la interfaz distingue explícitamente **datos acreditados** y **supuestos de cotización futura**. La procedencia de los dos campos acreditados se conserva fuera del modelo legal, en `origen_campos_cuotas`, porque esa trazabilidad es una propiedad de la sesión/UI y no modifica el cálculo.

Cuando Mi Retiro Seguro confirma `cuotas_historicas`, `cuotas_totales` queda de solo lectura. `cuotas_anio_actual` queda protegido únicamente cuando el comprobante contiene una fila no proyectada del año calendario actual. Un campo ausente en el PDF permanece editable y se identifica como pendiente de captura manual. Esta regla evita convertir la importación documental en un bloqueo global del formulario.

Las barras superior e inferior del wizard son la única superficie de acción primaria del Paso 2. `navegacion_wizard.js` delega en `continuarDesdePasoCuotas()` cuando ya existe `resumen_cuotas`, eliminando la necesidad de botones duplicados dentro de la tarjeta.

El selector global de apariencia mantiene los mismos cuatro valores de estado, pero su representación visual pasa a SVG inline, sin depender de imágenes externas ni alterar la persistencia del tema.


### Revisión 2: modal compartido y pistas de campos

La vista previa de Mi Retiro Seguro deja de depender del panel donde fue renderizada: antes de abrirse se mueve a `body`, permitiendo reutilizar la misma instancia desde Cuotas y pasos posteriores aun cuando Datos personales esté oculto. `accesibilidad.js` incorpora además una capa transversal de pistas para campos editables de texto/número y conserva las ayudas extensas en iconos contextuales compactos.

## UX.4.6c R3 — vista previa documental contextual

El modal de Mi Retiro Seguro sigue siendo un componente único anexado a `body`, pero sus secciones declaran `data-preview-step`. `revisarComprobanteImportado(numeroPaso)` filtra la presentación sin duplicar estado ni parser: el Paso 1 usa la vista completa y los pasos posteriores muestran solo el subconjunto relevante.

La cuota acreditada del año actual se expone como campo de resumen en la sección del Paso 2. Si existe un registro anual no proyectado del año actual, ambos valores se sincronizan antes de confirmar para mantener coherencia entre Cuotas e Historial.

## Orquestación del Paso 3 — UX.4.6d

UX.4.6d mantiene los servicios backend separados, pero agrega una orquestación de interfaz para que el Paso 3 se comporte como una sola unidad:

```text
Barra superior/inferior
        ↓
analizarPasoHistorialCompleto()
        ├─ detalle_anio_actual.js → /api/simulacion/detalle-anio-actual (si aplica)
        ├─ historial_salarios.js → /api/simulacion/historial-salarial
        └─ simulacion.js → /api/simulacion/salario
        ↓
resultado-paso3 / habilitación del Paso 4
```

`historial_salarios.js` administra período, filas, filtros y análisis anual. `detalle_anio_actual.js` administra meses recientes y las bases automáticas. `importacion_datos_oficiales.js` conserva la procedencia por campo y el ciclo revisar/editar/importar. `navegacion_wizard.js` solo decide la acción visible y el acceso al siguiente paso; no ejecuta cálculo previsional por sí mismo.

El estado temporal añade `origen_campos_historial` y `origen_campos_detalle_anio_actual`. La presencia de origen bloquea únicamente el control correspondiente. Un valor ausente del documento no adquiere una marca de procedencia y permanece editable.

La eliminación de acciones internas y de paneles `Próximo paso...` reduce rutas paralelas de navegación: el progreso y las barras comunes son la superficie transversal del asistente.

### Coherencia Ficha Digital ↔ Paso 2 (R2)

`simulacion.cuotas.cuotas_anio_actual` pertenece al contrato funcional del Paso 2 y no es reescrito por la mera importación de Ficha Digital. `ficha_digital_importada` y `detalle_anio_actual` almacenan salarios/estado/cuota por mes. R3 marca y bloquea automáticamente la casilla de los meses documentales detectados. Desde R19, una **acción manual explícita** sobre una casilla editable del detalle sí puede actualizar la referencia agregada del Paso 2 porque representa información más reciente confirmada por el usuario; el total previo al año actual se conserva y los resúmenes dependientes se revalidan. Las tablas utilizan `data-row-imported`/`data-row-manual` como contrato visual transversal de procedencia.


### Procedencia visual de tablas — UX.4.6d R4

`data-row-imported` representa origen documental y utiliza tokens de selección/primarios (`--app-selected-bg`, `--app-selected-border`), no tokens de éxito. `data-row-manual` conserva la superficie normal. Las casillas documentales usan `data-imported-locked="true"` para mantener su estado marcado/bloqueado y una marca visual consistente entre temas.

### Casillas documentales robustas — UX.4.6d R5

Las casillas de cuota de Ficha Digital usan dos capas de estado: la propiedad nativa `checked` y metadata de procedencia `data-imported-locked`. La capa de procedencia actúa como fuente defensiva al restaurar sesiones generadas por revisiones anteriores y también controla la marca visual, evitando depender de diferencias de renderizado de checkboxes `disabled` entre navegadores y temas.

### Gestión de dependencias y borrado — UX.4.6d R6

`gestion_datos.js` centraliza acciones destructivas del asistente. El borrado por paso sigue una jerarquía de dependencias: limpiar un paso conserva únicamente etapas anteriores y reinicia el paso activo junto con todas las etapas posteriores. El reinicio integral reemplaza el estado por `crearSimulacionVacia()`. El borrado desde Fuentes/Privacidad elimina únicamente las claves locales propiedad de Mi Retiro Proyectado (simulación, consentimiento y tema), sin ejecutar `storage.clear()`.

La interfaz usa un único modal reutilizable de confirmación. La barra inferior no duplica acciones destructivas; el acceso **Opciones** vive en la barra superior sticky.

### Consulta global de privacidad — UX.4.6d R7

`partials/privacidad_consentimiento.html` pasa a incluirse desde `base.html` y `privacidad.js` se carga globalmente. El modal mantiene dos modos sobre una única fuente documental: **consentimiento**, exclusivo de la entrada a `/simulacion` cuando no existe una aceptación vigente, y **revisión**, invocable desde Fuentes sin cambiar la ruta actual.

El modo revisión oculta el footer de aceptación, no escribe ni borra consentimiento y permite cerrar con `×`. El mismo `×` durante el consentimiento inicial equivale a rechazar/abandonar la simulación para evitar que el modal pueda cerrarse dejando la captura de datos accesible sin consentimiento. La barra inferior del wizard no contiene gestión destructiva; `Opciones` permanece en la barra superior sticky.

### Estados y resumen inmediato del historial — UX.4.6d R8

La tabla anual calcula el estado de presentación exclusivamente en frontend, sin modificar el contrato de `DatosHistorialSalarial`: `PENDIENTE`, `FALTA_SALARIO`, `FALTAN_CUOTAS`, `REVISAR`, `SIN_COTIZACION`, `PARCIAL` y `COMPLETO`. El mismo evaluador alimenta el filtro **Pendientes**, evitando divergencia entre etiqueta y filtrado. El backend conserva la validación normativa/numérica definitiva.

Después de una respuesta válida de `/api/simulacion/historial-salarial`, la interfaz materializa un resumen local del bloque anual (referencia, identificadas, diferencia y total salarial) aun cuando la base salarial del Paso 3 siga pendiente. El resumen final del Paso 3 continúa siendo el que incorpora además la base mensual seleccionada.

El scroll vertical de tablas es adaptativo: un contenedor corto puede pasar a `table-scroll-compact`, mientras las tablas largas conservan el área desplazable y encabezado sticky. La capa visual global también normaliza el botón nativo de todo `input[type=file]`.

### Reactividad y privacidad contextual — UX.4.6d R9

El historial anual migra su actualización reactiva a delegación de eventos sobre `#historial-tabla-body`. La evaluación de estado, el filtro **Pendientes** y la invalidación de resultados derivados se ejecutan desde el mismo flujo, evitando listeners perdidos al regenerar filas.

El controlador global de privacidad conserva una sola instancia de modal y añade contexto de apertura (`simulacion` o `fuentes`). Esto permite reutilizar el mismo documento tanto para consentimiento pendiente como para consulta posterior, y resolver `×`/`Esc` según el contexto sin duplicar plantillas.

### Contrato transversal de tablas — UX.4.6d R10

La capa de presentación incorpora `app-table-shell` como frontera visual común. Las plantillas de Historial, Detalle del año actual, importaciones, Retiro, Resultados y Comparador declaran esta clase en sus contenedores; las tablas dinámicas de Proyección y Línea temporal la asignan al crear el wrapper en JavaScript.

El contrato no centraliza lógica de negocio. `historial_salarios.js` conserva sus estados/filtros reactivos, `detalle_anio_actual.js` conserva la semántica mensual y los motores permanecen intactos. La clase común únicamente normaliza geometría, paleta, encabezado y descubrimiento accesible del scroll.

Las fases futuras deben partir de este contrato antes de crear un nuevo estilo tabular.



### Scrollbar y carga documental — UX.4.6d R11

`app-table-shell` no solo define borde y radio: también es el propietario visual del scrollbar interno. En Chromium/Windows se ocultan los botones nativos del carril, el track permanece transparente y se separa de las esquinas; Firefox usa `scrollbar-color`/`scrollbar-width` equivalentes. La geometría no altera el `overflow` funcional específico de cada tabla.

Los importadores PDF comparten un contrato de fila de carga: el `input[type=file]` y la acción **Analizar documento** tienen la misma altura exterior y ancho de su columna. Este contrato se aplica tanto a Mi Retiro Seguro como a Ficha Digital y debe reutilizarse en importadores futuros.

### Scroll global y estado vacío de tablas — UX.4.6d R12

R12 generaliza la presentación de desplazamiento más allá de `app-table-shell`: `html`, cuerpos de modal, términos, navegación horizontal y contenedores tabulares comparten un thumb temático y supresión explícita de botones nativos cuando el navegador los expone. El scroll sigue siendo nativo, por lo que rueda, teclado, táctil y APIs de desplazamiento no cambian.

`app-table-shell` reduce su radio al token `--app-radius-md`, menor que el de las tarjetas, para integrar mejor el carril interno. El historial anual añade un estado vacío independiente: cuando el filtro **Pendientes** no tiene filas, el wrapper tabular se oculta y se muestra un mensaje de estado; no se renderiza una cabecera huérfana. El componente de archivo usa variables visuales propias y separa el hover del botón de la interacción sobre el nombre del archivo. Comparador continúa declarado con `app-table-shell`, cubierto por regresión.


### Selector de archivo estable — UX.4.6d R13

R13 corrige la interacción entre Bootstrap y el botón nativo de `input[type=file]`. En Chromium, el `:hover` del input puede activarse al pasar por el nombre del archivo y competir con `::file-selector-button`; por ello el componente común fija color, fondo y borde con una regla de prioridad explícita en estados base, hover y focus. No cambia la API de carga ni el procesamiento de PDFs.


### Paso 1 unificado — UX.4.6d R14

R14 modifica únicamente la composición de `simulacion.html` durante la certificación integral. El formulario `#bloque-datos-personales` conserva los mismos IDs y contratos JavaScript/API, pero agrupa la captura manual en una sola sección `informacion-personal-titulo`. `actualizarApellidoCasada()` continúa dependiendo exclusivamente de `sexo === "F"`; al mantenerse los identificadores originales no se requiere migración de estado, parser ni payload.

### Contrato R15 de campos bloqueados e importación documental

Los formularios comparten tokens `--app-field-locked-bg`, `--app-field-locked-border` y `--app-field-locked-text`. Los controles `readonly`/`disabled` se distinguen de los editables también mediante una señal lateral primaria; este contrato abarca formularios actuales y futuros.

La capa de presentación usa terminología neutral de **documento/comprobante**. La capa técnica mantiene actualmente validación y extracción PDF (`pypdf`, MIME/firma/límites). Si CSS cambia el layout o se incorpora otro formato, la adaptación debe ocurrir en el analizador/adapter y sus fixtures, no obligar a rediseñar el flujo de revisión.

El estado vacío de Paso 2 no presume continuidad futura: `continua_cotizando`, `cuotas_esperadas_cierre_anio` y `cuotas_esperadas_por_anio` quedan sin decisión/valor hasta interacción explícita.

### Dependencias no regresivas y jerarquía del Paso 3 — UX.4.6d R16

`analizarPasoHistorialCompleto()` ejecuta un *preflight* mediante `asegurarCuotasAnalizadasParaPaso3()`. Si `resumen_cuotas` existe, continúa normalmente. Si el resumen fue invalidado pero el formulario de Paso 2 sigue completo, `analizarCuotas()` se ejecuta de forma silenciosa y reconstruye el resumen sin cambiar de panel. Si faltan datos, la operación se detiene en Paso 3 y conserva todo el estado.

La restauración de `paso_actual` se normaliza contra `puedeAccederDirectamenteAPaso()` para no reabrir etapas cuyo prerrequisito fue limpiado. Esta regla complementa la invalidación descendente de R6.

En presentación, `detalle_anio_actual.html` incorpora el componente `importacion_ficha_digital.html`. La estructura conceptual queda **Historial anual → Detalle del año actual (incluye Ficha Digital y tabla mensual) → Base salarial**. No existe acoplamiento nuevo entre parser y motor; solo cambia la orquestación de interfaz.


### UX.4.6d R17 — semántica de procedencia documental

La capa de importación separa tres dimensiones que no deben inferirse entre sí: **procedencia**, **bloqueo** y **valor**. `data-imported-locked` expresa que el control no puede alterarse desde esa vista; no implica que un checkbox esté marcado. La marca visual depende del `checked` real.

La referencia de Mi Retiro Seguro conserva `cuotas_historicas` como fotografía acreditada y `total_cuotas_acumuladas` como dato documental independiente que puede incorporar proyección. La UI explica la diferencia sin sustituir una cifra por otra.

La sesión puede registrar `campos_editados_importacion_comprobante` para distinguir valores revisados/completados por el usuario de valores detectados originalmente. Esta metadata es de trazabilidad UX y no modifica los motores previsionales.

## UX.4.6d R18 — procedencia y restauración de importaciones

La capa cliente separa ahora tres conceptos: **valor**, **fuente/procedencia** y **archivo de origen**. El valor vive en el estado de simulación; la procedencia se conserva por campo mediante códigos de origen; y del archivo solo se guarda localmente el nombre como metadata de UX cuando se confirma una importación. Los bytes del documento no forman parte del estado serializado.

El componente común de procedencia convierte códigos de fuente en cuatro estados visibles: Detectado, Editado por ti, Completado manualmente y No detectado. Esta capa puede reutilizarse en Pasos 4–6 sin acoplarla a un parser específico.


### Sincronización mensual → anual en Paso 3 (R19)

`detalle_anio_actual.js` mantiene una proyección local de la fila anual vigente a partir de los registros visibles. `sincronizarFilaAnualDesdeDetalleLocal()` actualiza cuotas y salario sin ejecutar fórmulas previsionales; la API `detalle-anio-actual` continúa siendo la autoridad de validación y recalcula los mismos totales antes del análisis definitivo.

Cuando cambia una casilla manual, `sincronizarCuotasPaso2DesdeDetalle()` conserva la base de cuotas anterior al año actual mediante `cuotas_totales - cuotas_anio_actual`, reemplaza el conteo vigente por el confirmado en el detalle y marca `resumen_cuotas`/resultados posteriores como inválidos. `asegurarCuotasAnalizadasParaPaso3()` reconstruye el resumen mediante el servicio normal antes de validar historial. No se duplican fórmulas actuariales en JavaScript.


### Vigencia y auditoría del detalle actual — UX.4.6d R20

La respuesta de `ficha_digital.py` ya expone `anio_mas_reciente` y `mes_mas_reciente`. R20 reutiliza esos campos en `importacion_datos_oficiales.js` para calcular una diferencia de meses respecto de la fecha local del navegador. No se introduce un nuevo endpoint ni se almacena una copia del documento. La ventana de tolerancia es de dos meses calendario anteriores además del mes actual.

Si la ficha queda fuera de esa ventana, un modal intermedio exige una decisión explícita: seleccionar otro documento o continuar con el actual. Tras confirmar, la metadata del último período permanece visible en el estado persistente de importación y puede volver a evaluarse en una recarga posterior.

`detalle_anio_actual.js` sigue tomando como autoridad el `ResumenDetalleAnioActual` devuelto por el backend. R20 solo presenta esos campos en `detalle_anio_actual.html`; no duplica promedios ni totales en la capa cliente. Al invalidar el detalle, el resumen visible se oculta junto con el resumen persistido.


## UX.4.6d R21 — servicio de fecha de referencia

`app/services/fecha_referencia.py` encapsula la obtención de una fecha externa para controles de vigencia. Consulta por HTTPS únicamente encabezados de fecha de dominios oficiales de la CSS, cachea brevemente el resultado y devuelve `confiable=false` si no puede verificarlo. `POST /api/simulacion/ficha-digital` incorpora esa referencia a `ResumenFichaDigital` y `GET /api/sistema/fecha-referencia` permite revalidar importaciones persistidas tras F5. La UI no usa el reloj del navegador para decidir si una Ficha Digital es reciente.

### UX.4.6d R22 — reconciliación antes de validar Paso 3

La validación del detalle incorpora una etapa idempotente previa al payload: si existe confirmación manual de cuota o la referencia de Paso 2 ya deriva del detalle, se ejecuta la sincronización de cuotas y, solo cuando cambia la referencia, se reejecuta el servicio de cuotas en segundo plano. El servicio de detalle continúa siendo la fuente de los cálculos mensuales; esta capa únicamente garantiza consistencia de dependencias y mensajes accionables.



### UX.4.6d R23 — precedencia temporal de la Ficha Digital

El detalle mensual actúa como fuente documental más reciente únicamente cuando una Ficha Digital confirmada aporta **más** cuotas del año actual que la referencia agregada de Paso 2. La sincronización conserva `cuotas_previas_al_anio_actual = cuotas_totales - cuotas_anio_actual`, sustituye el componente corriente, registra procedencia `FICHA_DIGITAL_ACTUALIZADO` y revalida el servicio de Cuotas. Una ficha con menos meses no provoca degradación automática. La misma reconciliación se ejecuta defensivamente antes del payload de detalle para cubrir F5/restauraciones.
