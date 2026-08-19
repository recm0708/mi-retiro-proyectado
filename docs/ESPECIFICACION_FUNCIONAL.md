# Especificación funcional

**Estado:** Vigente con registro RF histórico integrado
**Versión de aplicación revisada:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R2 — 2026-08-17
**Clasificación:** Funcional / Auditoría

Este documento tiene dos capas:

1. **Contrato funcional vigente consolidado**, que describe el comportamiento actual.
2. **Registro cronológico RF preservado**, que mantiene los identificadores históricos sin renumerarlos.

Cuando una descripción cronológica antigua contradiga el contrato consolidado o una regla posterior explícitamente identificada, prevalece la regla vigente más reciente. La trazabilidad RF completa se ampliará en GOV.1.3 R4.

## 1. Alcance vigente

Mi Retiro Proyectado permite capturar/revisar datos, construir escenarios y estimar prestaciones para los tres sistemas generales implementados:

- SEBD;
- Subsistema Mixto;
- SUCGS.

La herramienta es independiente de la CSS y no sustituye una determinación oficial.

## 2. Asistente de seis pasos

### Paso 1 — Datos personales

Debe permitir:

- captura manual;
- importación revisable de Mi Retiro Seguro;
- identificación opcional;
- fecha de nacimiento, sexo y sistema como datos necesarios para continuar;
- apellido de casada opcional/condicionado;
- consentimiento vigente de privacidad antes de tratar datos del asistente.

Solo los campos realmente aportados por un documento pueden quedar con procedencia documental/bloqueo aplicable.

### Paso 2 — Cuotas

Debe distinguir:

- cuotas acreditadas;
- cuotas del año actual;
- continuidad futura;
- cierre esperado del año;
- densidad futura.

Los supuestos futuros requieren una decisión explícita. Limpiar Paso 2 elimina esa decisión y sus valores.

Una importación puede completar campos de cuotas por procedencia; los campos no detectados siguen manuales.

### Paso 3 — Historial y salario reciente

Debe permitir:

- historial anual;
- detalle opcional mensual/quincenal del año actual;
- Ficha Digital;
- bases salariales manuales/derivadas;
- separación entre salario disponible y acreditado.

Una cuota manual del detalle puede actualizar el agregado del Paso 2. Una Ficha Digital confirmada puede **aumentar** la referencia de cuotas del año actual si identifica más meses; no debe reducir automáticamente una referencia superior.

### Paso 4 — Proyección

Debe construir:

- salario constante;
- variación porcentual;
- salario futuro conocido;
- escenarios porcentuales;
- línea temporal separando real y proyectado.

### Paso 5 — Retiro

Debe construir escenarios de retiro usando fechas, cuotas y horizonte salarial. El último mes acreditado se maneja con granularidad mensual visible.

### Paso 6 — Resultados

Debe:

- ejecutar el motor correspondiente;
- separar pensión mensual y pago único;
- mostrar advertencias/datos no confirmados;
- ofrecer trazabilidad;
- generar un resumen transversal;
- soportar fotografía proyectada y solo acreditada;
- alimentar el comparador sin duplicar fórmulas.

## 3. Importación de Mi Retiro Seguro

El archivo se analiza sin persistirlo.

La vista previa debe permitir revisar y, cuando corresponda, editar antes de confirmar.

La aplicación debe diferenciar:

- `HISTORICO`;
- `HISTORICO_PROYECTADO`;
- `PROYECTADO`.

Las cuotas históricas acreditadas no deben confundirse con un total acumulado que incluya proyección.

El monto esperado del comprobante es una referencia, no una constante del motor.

## 4. Ficha Digital

El backend extrae salarios del **año más reciente detectado** en el documento.

La respuesta del parser no expone identificadores personales.

La vigencia se compara con una fecha externa verificable.

Si el último período es anterior al mes actual verificado, debe advertirse. Si la fecha externa no puede verificarse, la interfaz debe adoptar una conducta conservadora y permitir decidir conscientemente.

## 5. Gestión de datos

Debe existir:

- limpiar paso;
- reiniciar simulación;
- borrar datos locales de la aplicación.

Toda acción destructiva requiere confirmación cuando existen datos. El borrado integral debe invalidar la aceptación local de privacidad y provocar una nueva presentación de las condiciones; si no se aceptan, el siguiente ingreso a Simular debe continuar bloqueado hasta obtener una aceptación vigente. Los identificadores pre-beta solo pueden reconocerse para su eliminación defensiva, nunca para restaurar o migrar estado.

La invalidación es descendente salvo las reconciliaciones controladas del año actual descritas anteriormente.

## 6. Privacidad

La simulación es temporal y local en la versión actual.

No se deben versionar documentos personales ni incorporar PII real a logs/fixtures/documentación.

El consentimiento y la apariencia se mantienen separados del modelo previsional.

## 7. Accesibilidad y apariencia

La aplicación mantiene:

- Claro;
- Oscuro;
- Alto contraste;
- Automático.

Debe conservar navegación por teclado, foco visible, mensajes accesibles, tablas coherentes y semántica del wizard.

## 8. Comparador, metodología y fuentes

Las páginas públicas deben reutilizar resultados/fuentes ya calculados/cargados, sin implementar nuevas reglas previsionales.

Los enlaces visibles deben usar nombres humanos, no IDs internos de normativa.

## 9. Reglas de precedencia RF conocidas

### RF-318 → sustituido por RF-322

RF-318 admitía como reciente una Ficha Digital del mes actual o de hasta dos meses anteriores.

**Estado:** Sustituido.

RF-322 establece el contrato vigente: cualquier último período anterior al mes actual verificado requiere advertencia.

### RF-324 y RF-325

**Estado:** Vigentes.

La fecha de referencia se intenta obtener por HTTPS desde infraestructura CSS sin enviar datos de simulación. Si falla, no se clasifica el documento como reciente usando un fallback local silencioso.

### RF-327

**Estado:** Vigente.

El parser de Ficha Digital usa el año más reciente detectado en el documento cuando no recibe un año explícito.

### RF-328 / RF-329

**Estado:** Vigentes.

La confirmación manual del detalle puede reconciliar cuotas del Paso 2 y revalidar el resumen sin navegación regresiva.

### RF-332 a RF-336

**Estado:** Vigentes; refinan la reconciliación documental.

Una Ficha Digital confirmada puede ampliar las cuotas del año actual cuando aporta más meses; una cifra inferior no reduce automáticamente una referencia superior.

## 10. Registro RF

Los identificadores RF existentes no se renumeran ni se reutilizan.

El contenido cronológico previo se conserva íntegramente a continuación como registro de evolución. Los encabezados de revisión dentro del anexo describen el momento en que surgió cada requisito y **no significan que todas las reglas históricas sigan vigentes simultáneamente**.

---

# Anexo A — Registro cronológico RF preservado

La aplicación guía al Asegurado(a) por seis pasos y calcula una prestación estimada según el sistema previsional seleccionado. Este documento describe el comportamiento funcional vigente y las mejoras de producto posteriores al cierre de la Fase 6.

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Alcance

La aplicación debe:

- recopilar datos personales y previsionales;
- validar cuotas e historial;
- construir proyecciones salariales y de retiro;
- determinar la modalidad aplicable;
- calcular SEBD, Mixto o SUCGS según corresponda;
- distinguir pensiones mensuales de pagos únicos;
- mostrar advertencias cuando falten datos oficiales o exista una limitación del modelo;
- conservar trazabilidad normativa.

No debe presentarse como una herramienta oficial de la CSS ni emitir una certificación de derechos.

## 2. Flujo principal de seis pasos

### 2.1. Paso 1 — Datos personales y sistema previsional

**RF-001.** Registrar fecha de nacimiento.

**RF-002.** Registrar sexo para determinar edad de referencia cuando la norma lo requiera.

**RF-003.** Registrar fecha de ingreso a la CSS cuando se conozca.

**RF-004.** Seleccionar sistema actual:

- No sé cuál tengo;
- SEBD — Subsistema Exclusivamente de Beneficio Definido;
- Subsistema Mixto;
- SUCGS — Capitalización con Garantía Solidaria.

La aplicación debe mostrar el nombre completo de siglas que puedan no ser conocidas por el Asegurado(a).

### 2.2. Paso 2 — Cuotas

**RF-005.** Registrar cuotas totales acreditadas.

**RF-006.** Registrar cuotas del año actual incluidas en el total.

**RF-007.** Registrar si el Asegurado(a) espera continuar cotizando.

**RF-008.** Registrar cuotas esperadas al cierre del año actual y densidad futura.

El análisis debe mantener separado el total histórico de la proyección futura.

### 2.3. Paso 3 — Historial salarial y salario actual

**RF-009.** Permitir historial anual de cuotas y salario cotizado/reportado.

**RF-010.** Validar la suma de cuotas del historial contra el Paso 2.

**RF-011.** Permitir años sin cotización y años parciales.

**RF-012.** Registrar salario actual como semanal, quincenal, mensual o anual y normalizarlo para proyección.

### 2.4. Paso 4 — Proyección salarial

**RF-013.** Permitir salario constante.

**RF-014.** Permitir variación porcentual anual.

**RF-015.** Permitir salario futuro conocido y derivar una trayectoria coherente.

**RF-016.** Permitir comparación de varios escenarios salariales.

**RF-017.** Construir una línea temporal que identifique claramente:

- histórico;
- año actual real/proyectado;
- futuro proyectado.

### 2.5. Paso 5 — Escenarios de retiro

**RF-018.** Calcular edad exacta y fecha de referencia.

**RF-019.** Separar fecha de evaluación, último mes con cuotas acreditadas, fecha técnica de corte y fechas de retiro.

**RF-020.** Construir escenarios anticipados, edad de referencia, años adicionales y fecha personalizada.

**RF-021.** Respetar primero las cuotas esperadas al cierre del año actual antes de aplicar densidad futura.

**RF-022.** Advertir cuando el horizonte salarial no cubra la fecha de retiro.

**RF-023.** Permitir seleccionar explícitamente el escenario que alimentará Resultados.

### 2.6. Paso 6 — Resultados

**RF-024.** Mostrar sistema, escenario de retiro, fecha, edad y cuotas estimadas.

**RF-025.** Solicitar solo los datos específicos del sistema que no puedan deducirse de los pasos anteriores.

**RF-026.** Invocar el motor correspondiente en backend.

**RF-027.** Mostrar una prestación mensual, un pago único o ambos según la naturaleza jurídica del resultado.

**RF-028.** Mostrar advertencias de datos proyectados, parámetros no confirmados o reglas pendientes.

**RF-029.** Invalidar resultados cuando cambie un dato de origen.

## 3. Requisitos de navegación y experiencia

**RF-030.** Permitir volver directamente a un paso ya disponible mediante los indicadores superiores.

**RF-031.** Mantener un selector persistente `Ir a paso` en flujos largos.

**RF-032.** No permitir saltar a un paso cuyos prerrequisitos no estén satisfechos.

**RF-033.** Conservar temporalmente la simulación en `sessionStorage` sin persistir datos personales de forma permanente por defecto.

**RF-034.** Los campos monetarios editables deben usar separadores de miles y máximo dos decimales.

**RF-035.** Los factores/divisores actuariales no deben presentarse con símbolo monetario.

## 4. Requisitos del motor SEBD

**RF-036.** Clasificar automáticamente:

- Normal;
- Anticipada;
- Proporcional;
- Proporcional Anticipada;
- Indemnización por Vejez;
- no elegible/transición cuando corresponda.

**RF-037.** Calcular el salario base con los años requeridos por la regla implementada.

**RF-038.** Aplicar tasa base e incrementos por bloques completos de cuotas según el momento de cotización.

**RF-039.** Aplicar factores de anticipación versionados por mes.

**RF-040.** Mantener la Indemnización por Vejez como pago único separado.

**RF-041.** Aplicar límites máximos cuando se cumplen las condiciones disponibles.

**RF-042.** No aplicar silenciosamente un mínimo indexado del artículo 192 sin un valor vigente versionado.

## 5. Requisitos del Subsistema Mixto

**RF-043.** Calcular el Componente de Beneficio Definido usando el tramo salarial participante del Mixto.

**RF-044.** Advertir cuando el tope mensual de B/.500 deba aproximarse a partir de datos anuales.

**RF-045.** Solicitar saldo CAP en lugar de reconstruirlo artificialmente desde el historial anual.

**RF-046.** Permitir bono de reconocimiento e indicar si fue confirmado oficialmente.

**RF-047.** Calcular pensión programada solo cuando se dispone del valor actuarial aplicable.

**RF-048.** Permitir `AUTO`, `PENSION_PROGRAMADA` o `DEVOLUCION_TOTAL`.

**RF-049.** Cuando `AUTO` requiera una decisión del Asegurado(a), mantener el resultado pendiente.

**RF-050.** Separar devolución CAP, indemnización BD y total de pagos únicos.

**RF-051.** Modelar la garantía de renta vitalicia como continuidad futura del CAP, no como aumento inicial.

**RF-052.** Aplicar la transición operativa Mixto → SUCGS desde la fecha versionada, dejando documentada cualquier discrepancia normativa.

## 6. Requisitos del SUCGS

**RF-053.** Solicitar saldo de Capitalización Solidaria y su confirmación oficial.

**RF-054.** Calcular el componente contributivo mediante saldo, divisor legal y factor actuarial por edad.

**RF-055.** Mantener la tabla actuarial fuera de la interfaz y versionada en `normativa/sucgs.json`.

**RF-056.** Evaluar la capa solidaria del artículo 194.

**RF-057.** Evaluar la Pensión Garantizada Solidaria del artículo 195.

**RF-058.** Permitir reemplazar valores legales de referencia por valores vigentes confirmados cuando la norma esté indexada.

**RF-059.** Preevaluar las condiciones objetivas del artículo 197 con historial anual completo.

**RF-060.** Mantener la estabilidad salarial del artículo 197 como condición explícita cuando no pueda deducirse con seguridad.

**RF-061.** Completar la pensión total cuando la garantía de reemplazo pueda evaluarse o cuando se determine que no aplica.

## 7. Requisitos de transparencia normativa

**RF-062.** Todo motor debe devolver una referencia normativa legible.

**RF-063.** Los parámetros legales modificables deben estar versionados fuera del código de presentación.

**RF-064.** Las ambigüedades o decisiones interpretativas deben quedar registradas en `docs/DECISIONES.md`.

**RF-065.** La documentación debe enlazar a las fuentes oficiales utilizadas.

**RF-066.** Una comunicación operativa temporal debe identificarse como tal y no presentarse como sustituto de una ley o reglamento.

## 8. Requisitos de precisión y consistencia

**RF-067.** Los importes sensibles deben usar `Decimal` cuando exista riesgo de error binario.

**RF-068.** El redondeo general debe materializarse a centavos con `ROUND_HALF_UP`, salvo norma específica.

**RF-069.** Los resultados intermedios no deben redondearse arbitrariamente para forzar una coincidencia visual.

**RF-070.** Los datos históricos y proyectados deben mantenerse distinguibles en API e interfaz.

## 9. Bloque 6F — cierre funcional y transparencia

**RF-071.** Comparación transversal entre escenarios de retiro. **Implementado en 6F.1.**

**RF-072.** Comparación entre escenarios salariales. **Implementado en 6F.1.**

La comparación debe reutilizar los motores existentes, conservar un escenario base, separar pensiones mensuales de pagos únicos y advertir cuando un saldo específico se reutiliza como hipótesis para una fecha alternativa.

**RF-073.** Vista `Ver cálculo completo` con dato → regla → fórmula → sustitución → resultado intermedio → redondeo/límite → resultado final. **Implementado en 6F.2.**

**RF-074.** Enlaces clicables a la fuente normativa aplicable desde Resultados o una vista de metodología. **Implementado en 6F.2–6F.3.**

**RF-075.** Página o sección de Metodología y fuentes. **Implementado en 6F.3.**

**RF-076.** Estructura de salida reutilizable por futuros informes PDF. **Implementado como contrato transversal en 6F.4.**

**RF-077.** Mantener una página permanente de metodología y fuentes con jerarquía normativa, artículos por sistema y recursos oficiales de verificación. **Implementado.**

**RF-078.** Mantener los identificadores técnicos de fuentes exclusivamente como IDs internos; la interfaz debe mostrar títulos humanos y enlaces oficiales. **Implementado.**

**RF-079.** Exponer un resumen común de resultado final para SEBD, Mixto y SUCGS con estado, naturaleza, pensión mensual, pago único, modalidad, escenario y advertencias. **Implementado.**

## 10. Identidad y terminología de producto

**RF-080.** La aplicación debe presentarse bajo el nombre **Mi Retiro Proyectado** y conservar una declaración visible de independencia respecto de la CSS.

**RF-081.** La persona que realiza una simulación debe denominarse **Asegurado(a)** y, en plural, **Asegurados(as)** en la interfaz y documentación funcional.

**RF-082.** La interfaz debe usar un tamaño tipográfico base común para contenido, controles, ayudas, tablas y navegación; los encabezados y valores previsionales relevantes pueden usar tamaños diferenciados.

**RF-083.** La interfaz no debe exponer nombres de subfases, ADR, rutas del repositorio, nombres de archivos técnicos ni identificadores internos de fuentes.

**RF-084.** La interfaz debe ofrecer los modos visuales **Seguir sistema**, **Claro**, **Oscuro** y **Alto contraste**.

**RF-085.** La preferencia visual debe persistirse en `localStorage` sin mezclarse con los datos previsionales guardados en `sessionStorage`.

**RF-086.** La navegación principal debe incluir un mecanismo para saltar directamente al contenido y señalar la página activa mediante semántica accesible.

**RF-087.** Los controles interactivos principales deben mantener foco visible, objetivos táctiles de al menos 44 px de altura y respetar `prefers-reduced-motion`.

**RF-088.** El pie de página debe presentar en formato compacto el nombre del producto, copyright, aviso de independencia y acceso a Mi Caja Digital.

## 11. UX.2.1 — estabilización visual y contenido público

**RF-089.** Los temas Oscuro y Alto contraste deben adaptar fondos, textos secundarios, tarjetas, tablas, alertas, badges, wizard y navegación rápida sin conservar superficies claras o textos de bajo contraste.

**RF-090.** Los estados visuales de información, éxito, advertencia, neutral y proyección deben usar colores semánticos definidos por tema y no colores literales por componente.

**RF-091.** La página de Inicio debe funcionar como portada del producto: explicar propósito, sistemas contemplados, capacidades principales, proceso de seis pasos y acciones para iniciar una simulación o consultar metodología.

**RF-092.** La interfaz no debe mostrar detalles de implementación como rutas `normativa/*.json`, nombres de endpoints, backend, repositorio o mecanismos internos de carga de fuentes.

**RF-093.** Las tarjetas equivalentes de métricas, metodología y recursos deben mantener alineación vertical y ubicación de acciones consistente dentro de una misma fila visual.

## 12. UX.3 — responsive y precisión del corte de cuotas

**RF-094.** La interfaz debe adaptarse a laptop, tablet y móvil sin provocar desplazamiento horizontal de toda la página.

**RF-095.** La navegación principal colapsada debe conservar enlaces, estado de página activa, selector de tema y objetivos táctiles adecuados en tablet y móvil.

**RF-096.** Las tablas previsionales extensas deben conservar columnas legibles mediante desplazamiento horizontal dentro de su propio contenedor cuando el ancho disponible no sea suficiente.

**RF-097.** En móvil, la navegación persistente del asistente debe situarse en la parte inferior, respetar las áreas seguras del dispositivo y mantener retroceso, selector de paso y acción principal.

**RF-098.** Las acciones principales de formularios y resultados deben reorganizarse a ancho completo en móvil cuando una disposición horizontal reduzca su legibilidad o superficie táctil.

**RF-099.** El Paso 5 debe distinguir explícitamente la fecha de evaluación, el último mes con cuotas acreditadas y la fecha de cada escenario de retiro.

**RF-100.** Cuando se informe `ultimo_mes_cuotas`, el servicio debe derivar una fecha técnica de corte al último día del mes; si coincide con el mes de evaluación, no puede superar la fecha de evaluación. Un mes posterior al de evaluación debe rechazarse.

**RF-101.** Los recursos de consulta individual que no constituyen fuentes normativas del cálculo deben conservar la denominación **recurso oficial** en la interfaz, aunque compartan tratamiento visual con los botones de fuentes oficiales.

## 13. UX.4.1 — accesibilidad semántica y ayudas contextuales

**RF-102.** La plantilla global debe exponer landmarks y regiones de estado identificables, y el asistente debe relacionar cada control de paso con el panel que gobierna.

**RF-103.** Los campos previsionales que puedan confundirse con conceptos cercanos deben disponer de ayuda contextual breve, opcional y operable mediante puntero y teclado. La ayuda debe aparecer con `hover` o foco, conservar una alternativa de clic para interacción táctil y no sustituir la etiqueta ni duplicar reglas de negocio.

**RF-104.** Cuando un control requerido sea inválido, la interfaz debe identificarlo programáticamente mediante `aria-invalid`, mover el foco al primer campo que requiere corrección y anunciar que existe un dato por revisar.

**RF-105.** Los mensajes de error y advertencia generados dinámicamente deben usar regiones vivas apropiadas y conservar su contenido visible como fuente principal de información.

**RF-106.** Las tablas previsionales deben disponer de una descripción programática mediante `caption`; cuando un contenedor tenga desplazamiento horizontal real, debe poder recibir foco para permitir navegación por teclado.

**RF-107.** Los enlaces que abran una pestaña nueva deben informar ese comportamiento a tecnologías de apoyo sin añadir texto visual repetitivo.

**RF-108.** La capa de accesibilidad del frontend no debe calcular, reinterpretar ni modificar cuotas, salarios, fechas legales, modalidades o prestaciones; únicamente mejora interacción, semántica y comprensión de los datos solicitados.

**RF-109.** En la tabla de escenarios de retiro, una fila correspondiente a una fecha futura seleccionable debe poder activarse haciendo clic en cualquier área no interactiva de la fila; el control de radio permanece como control semántico y de teclado.

**RF-110.** Las acciones auxiliares que modifican datos masivamente, como completar cuotas vacías con 12, deben distinguirse visualmente de controles secundarios neutros en Claro, Oscuro y Alto contraste.

**RF-111.** En el bloque SEBD de Resultados, la acción de calcular o recalcular debe quedar alineada con el control de escenario salarial al que acompaña en disposiciones de escritorio.

## 14. UX.4.2 — estados activos y selección perceptible

**RF-112.** Cuando el tema efectivo sea Claro, el número del paso activo debe conservar texto blanco sobre el círculo primario para mantener contraste suficiente. El ajuste debe aplicarse a cualquier paso que se encuentre activo y no alterar la combinación ya validada en Oscuro y Alto contraste.

**RF-113.** La fila seleccionada de la tabla de escenarios de retiro debe distinguirse mediante señales redundantes: fondo, contorno de fila, realce del control de radio y badge de estado. Estas señales deben definirse por tema y no depender exclusivamente del color de fondo.

**RF-114.** El foco de teclado sobre el control de selección de retiro debe reforzar visualmente la fila asociada y, cuando el sistema operativo active colores forzados, la selección debe respetar los colores de resaltado del sistema.


## 15. UX.4.3 — errores, foco y operación por teclado

**RF-115.** Cuando la validación nativa de un control falle, el campo debe quedar marcado con `aria-invalid` y disponer de un mensaje programáticamente asociado mediante `aria-errormessage`, sin reemplazar la ayuda contextual o descriptiva ya existente.

**RF-116.** Al corregirse un control inválido o reiniciarse el formulario, la asociación de error y el estado `aria-invalid` deben retirarse para evitar mensajes obsoletos.

**RF-117.** Los errores dinámicos de una operación deben usar una única semántica urgente, recibir foco programático cuando pasan de ocultos a visibles y mostrar un foco perceptible; no deben combinar `role="alert"` con una segunda región `aria-live="assertive"` redundante.

**RF-118.** Las advertencias dinámicas no urgentes pueden utilizar `role="status"` y `aria-live="polite"`; si una advertencia se declara explícitamente urgente como `alert`, no debe duplicar otra región viva.

**RF-119.** Los controles de selección de escenarios de retiro deben conservar la operación nativa con teclado y aceptar Enter como alternativa sobre el radio, sin convertir toda la fila en un segundo control enfocable.

**RF-120.** Las páginas públicas principales deben conservar un único `h1` como encabezado principal de la vista; los encabezados internos del wizard y resultados continúan desde niveles subordinados.

**RF-121.** La capa de accesibilidad dinámica no debe generar ciclos de mutación sobre las clases que observa. Las actualizaciones de clase ejecutadas desde el observador deben ser idempotentes para mantener la interfaz disponible.

**RF-122.** La limpieza reactiva de errores durante `input` y `change` debe consultar el estado de validez sin redisparar el evento `invalid`.

**RF-123.** Todo control inválido debe mostrar un mensaje de error visible junto al campo, además de mantener la asociación programática mediante `aria-errormessage`; el color o el borde no pueden ser la única señal de error.

**RF-124.** La presentación de errores de campo no debe depender del globo nativo del navegador. La aplicación puede suprimir esa presentación durante `invalid` siempre que conserve la validación, el bloqueo de avance, el foco sobre el primer campo inválido y el mensaje accesible propio.

## 16. UX.4.4 — edad por año en la línea temporal

**RF-125.** Las tablas **Historial salarial real** y **Proyección futura** del Paso 4 deben mostrar una columna **Edad** asociada a cada año calendario presentado.

**RF-126.** La edad anual se deriva de la fecha de nacimiento ya capturada en el Paso 1 mediante la convención `año mostrado - año de nacimiento`, que representa la edad que el Asegurado(a) cumple durante ese año. Si la fecha de nacimiento no está disponible o no es válida, la interfaz debe mostrar una raya en lugar de inventar un valor.

**RF-127.** La edad anual es un dato derivado de presentación y no puede modificar salarios, cuotas, elegibilidad, fechas de retiro ni resultados de los motores previsionales.


## 17. UX.4.4 — detalle salarial del año actual

**RF-128.** El Paso 3 debe permitir activar opcionalmente un detalle del año calendario actual sin obligar al Asegurado(a) a abandonar el historial anual existente.

**RF-129.** El detalle debe admitir captura como total mensual o como primera/segunda quincena. En modo mensual el Asegurado(a) identifica si el salario es completo o parcial; en modo quincenal el estado se deriva de las quincenas disponibles.

**RF-130.** Cada mes debe distinguir salario, estado y cuota. En captura manual estos datos son independientes; cuando el mes procede de una Ficha Digital confirmada, UX.4.6d R3 fija la casilla de cuota como parte del registro documental y la protege contra edición directa.

**RF-131.** El servicio del detalle debe calcular por separado salario total disponible y salario asociado a meses con cuota acreditada, además de identificar el último mes acreditado y el último mes con salario completo.

**RF-132.** La cantidad de meses marcados con cuota acreditada debe contrastarse con `cuotas_anio_actual` del Paso 2. Si no coincide, la aplicación debe mostrar la discrepancia y no derivar silenciosamente un corte de cuotas.

**RF-133.** Cuando las cuotas coincidan, el salario acreditado del detalle puede sincronizar la fila anual actual del historial y el Paso 5 puede derivar automáticamente `ultimo_mes_cuotas`. El campo debe permanecer editable cuando no existe un detalle coherente.

**RF-134.** La base salarial de proyección debe poder ser manual o derivarse mediante: último mes completo, promedio de meses completos del año actual, promedio de los últimos tres meses completos o promedio del salario acreditado por cuota del año actual. Las tres primeras bases usan únicamente meses completos; la última representa explícitamente el cociente entre salario acreditado y cuotas acreditadas y debe identificarse como tal.

**RF-135.** Una base salarial automática modifica exclusivamente la proyección futura y no debe reemplazar salarios históricos acreditados. El Paso 4 debe informar el origen de la base utilizada.

**RF-136.** La interfaz debe enlazar a Mi Caja Digital para consulta manual y puede analizar una Ficha Digital PDF cuando exista texto estructurado reconocible. El análisis no debe aplicar datos hasta que el Asegurado(a) revise y confirme la vista previa.


## 18. UX.4.4 — referencia personal desde comprobante PDF

**RF-137.** El Paso 1 debe permitir cargar opcionalmente un comprobante digital PDF de Mi Retiro Seguro sin convertirlo en requisito para completar una simulación.

**RF-138.** El PDF debe procesarse en memoria. El contrato no debe incluir el código único del documento; desde UX.4.6b puede incluir identificadores personales opcionales solo cuando el documento los etiqueta de forma inequívoca y siempre sujetos a revisión antes de importarlos.

**RF-139.** La referencia importada debe extraer dinámicamente, cuando estén disponibles, fecha del comprobante, sistema elegido, edad de retiro elegida, cuotas históricas, naturaleza de la prestación, monto estimado y registros anuales. No se permite usar un monto fijo procedente de un caso de validación.

**RF-140.** Un PDF que no corresponda al comprobante compatible, no contenga texto extraíble, esté protegido o exceda los límites del importador debe rechazarse con un mensaje visible sin afectar el resto de la simulación.

**RF-141.** El análisis inicial del comprobante no debe alterar la simulación. Después de una confirmación explícita en la vista previa, los datos detectados pueden prellenar persona, cuotas e historial seleccionado; la referencia monetaria continúa separada de los motores y no puede ajustar sus fórmulas.

**RF-142.** El Paso 6 debe mostrar referencia importada, resultado actual y diferencia solo cuando la comparación sea compatible en persona, sistema, edad de retiro y naturaleza económica de la prestación. Cuando no lo sea, debe conservar ambas cifras y explicar por qué no se calcula una diferencia.

**RF-143.** La interfaz debe explicar que el comprobante y la simulación actual pueden corresponder a fechas de corte o supuestos distintos y que una diferencia no implica por sí misma un error de cálculo.


## 19. Fuera del alcance inmediato

Quedan para fases posteriores:

- persistencia permanente;
- importaciones oficiales automatizadas;
- informes PDF;
- regímenes especiales no implementados;
- reconstrucción completa de cuentas CAP/SUCGS desde movimientos mensuales oficiales;
- auditoría integral WCAG 2.2 y pruebas asistidas con tecnologías de apoyo;
- revisión visual cruzada de todos los temas en formularios y resultados extensos.


## 19. UX.4.4 — importación revisable de documentos oficiales

**RF-144.** El Paso 1 debe concentrar únicamente la importación opcional del **Comprobante de Mi Retiro Seguro**. La **Ficha Digital** pertenece al Paso 3 por tratarse de información salarial del año actual.

**RF-145.** Analizar un comprobante debe abrir una vista previa inicialmente bloqueada. Ningún dato detectado puede escribirse en la simulación hasta que el Asegurado(a) pulse una acción explícita de confirmación. La edición se habilita únicamente mediante **Editar campos**; cancelar o cerrar conserva intactos los datos existentes.

**RF-146.** La vista previa del comprobante debe permitir revisar y, tras una acción explícita de edición, corregir identificación personal, fecha de nacimiento, sexo, fecha de ingreso, sistema, cuotas históricas, edad de retiro, monto de referencia, fecha del comprobante, prestación y filas anuales detectadas.

**RF-147.** Las filas anuales `HISTORICO` pueden proponerse para el historial real. Las filas `PROYECTADO` deben quedar excluidas por defecto y las filas `HISTORICO_PROYECTADO` no pueden asumirse reales sin decisión explícita.

**RF-148.** La Ficha Digital debe extraer de la sección **Salarios del último año** únicamente los registros que pertenezcan al año calendario actual cuando el PDF contenga texto digital reconocible. La vista previa debe permitir corregir mes, salario y estado completo/parcial.

**RF-149.** La Ficha Digital debe marcar automáticamente como confirmados los meses detectados con salario/estado utilizables. La casilla de cuota de esos registros queda marcada y bloqueada; los meses ausentes permanecen disponibles para captura manual. La prohibición original de modificar `cuotas_anio_actual` queda **sustituida parcialmente por RF-332** para una ficha confirmada que aporte un conteo superior.

**RF-150.** Los registros de la Ficha Digital del año actual pueden prellenar el detalle mensual del Paso 3. Los registros de años anteriores no se muestran, no se utilizan y no se conservan en el estado importado.

**RF-151.** Los importadores deben procesar archivos en memoria, rechazar formatos no compatibles y evitar persistir documentos o identificadores directos innecesarios. La interfaz debe informar qué datos quedan pendientes para captura manual.

**RF-152.** Todo importe monetario editable en las vistas previas de importación debe mostrarse con separador de miles y exactamente dos decimales, reutilizando la normalización monetaria común de la aplicación.


## 20. UX.4.5 — origen acreditado y proyección al retiro

**RF-123.** El Paso 6 debe poder evaluar la prestación en la fecha de retiro seleccionada usando únicamente salarios y cuotas ya acreditados, sin añadir períodos futuros.

**RF-124.** La proyección principal debe continuar incorporando las cuotas y salarios futuros del escenario seleccionado, manteniendo ambos resultados separados.

**RF-125.** La comparación entre ambas fotografías debe exponer pensión mensual, pago único, cuotas consideradas y períodos salariales proyectados, y solo calcular una diferencia monetaria cuando exista el mismo tipo de monto en ambas columnas.

**RF-126.** La comparación acreditada/proyectada debe funcionar sin necesidad de cargar un comprobante PDF. Cuando exista una referencia de Mi Retiro Seguro compatible, su comparación preferirá la fotografía acreditada propia.

**RF-127.** En Mixto y SUCGS, los saldos y parámetros específicos que no pueden proyectarse de forma fiable se mantendrán constantes entre ambas fotografías y se informará esta limitación.

**RF-128.** La tabla comparativa debe disponer de caption accesible, encabezados programáticos de fila/columna y estado textual que no dependa únicamente del color.


## 21. Pre-beta — regresión E2E y hardening

**RF-153.** Los importadores PDF deben validar extensión, tipo MIME compatible, tamaño máximo, archivo no vacío y firma PDF antes de iniciar extracción de texto.

**RF-154.** Los documentos importados deben continuar procesándose en memoria y sus respuestas no deben habilitar caché del navegador.

**RF-155.** La aplicación debe devolver errores controlados para PDF corrupto, protegido, ajeno al formato esperado, con exceso de páginas o texto anómalo, sin exponer trazas internas.

**RF-156.** Las rutas integradas de SEBD, Mixto y SUCGS deben disponer de regresiones E2E por API con resultados controlados.

**RF-157.** La validación continua debe cubrir instalación de dependencias, coherencia de paquetes, compilación Python, sintaxis JavaScript y suite completa en las versiones de Python soportadas para la beta.

**RF-158.** Las respuestas HTML deben incluir cabeceras defensivas de bajo riesgo contra sniffing de tipos, framing y exposición innecesaria de referrer/permisos del navegador.

**RF-159.** Las regresiones de infraestructura deben verificar la presencia y el contrato funcional de las GitHub Actions necesarias sin fijar permanentemente su major; una actualización de Action solo debe fallar si rompe el pipeline o una validación real.

**RF-160.** La vigilancia de dependencias debe distinguir paquetes directos de transitivos fijados, agrupar propuestas relacionadas cuando sea seguro y mantener revisión explícita sin auto-merge.


## 22. UX.4.6a — rediseño visual integral

**RF-161.** La modernización visual debe ser transversal a Inicio, Simulación, Comparador y Fuentes sin modificar fórmulas, contratos previsionales, rutas ni datos persistidos.

**RF-162.** La presentación debe cargar `style.css` como base histórica, `design-system.css` como capa de sistema visual y `accesibilidad.css` como remate accesible con precedencia final.

**RF-163.** El control de apariencia debe ofrecer **Automático**, **Claro** y **Oscuro** como opciones principales, mantener **Alto contraste** dentro de Accesibilidad y conservar la preferencia exclusivamente en `localStorage`.

**RF-164.** La navegación pública debe usar las etiquetas **Inicio**, **Simular**, **Escenarios** y **Fuentes** sin alterar las rutas existentes.

**RF-165.** La página de Inicio debe priorizar beneficios, tareas, sistemas contemplados y el proceso guiado. No debe exponer detalles de implementación de los motores ni presentar una pensión ficticia dentro de recursos visuales o mockups.

**RF-166.** El footer global debe identificar producto y versión, declarar la independencia de la CSS, enlazar a Fuentes oficiales y mostrar autoría/copyright. Mi Caja Digital debe permanecer en los puntos de verificación individual y no duplicarse globalmente en el footer.

**RF-167.** Botones, controles, cards, tablas, alertas, acordeones, wizard y superficies de páginas internas deben reutilizar tokens semánticos compatibles con Claro, Oscuro y Alto contraste.

**RF-168.** El cierre inmediato de UX.4.6a requiere validación manual en PC/laptop y regresiones automatizadas en verde. La validación específica en móvil, tablet, macOS y pantallas grandes puede diferirse para beta/RC mientras se conserven las reglas responsive existentes y no exista una incidencia conocida.


## 23. UX.4.6b — Simular / Paso 1 · Datos personales

**RF-169.** El Paso 1 debe permitir elegir entre **Ingresarlos manualmente** e **Importar desde Mi Retiro Seguro**. La captura manual es la modalidad predeterminada y ambas presentaciones deben ser mutuamente excluyentes.

**RF-170.** La identificación personal puede incluir primer nombre, segundo nombre, primer apellido, segundo apellido, apellido de casada, número de cédula y número de Seguro Social. Estos campos son opcionales y no pueden alterar las fórmulas previsionales.

**RF-171.** El apellido de casada debe mostrarse únicamente cuando el sexo sea femenino y permanecer opcional.

**RF-172.** En modo PDF, el formulario principal no debe mostrarse antes de confirmar una importación. Después de confirmarla puede mostrarse como resumen bloqueado; cualquier corrección de datos importados debe realizarse desde la vista previa mediante **Editar campos**.

**RF-173.** El parser de Mi Retiro Seguro debe priorizar campos explícitamente etiquetados. Cuando el documento solo exponga un nombre completo, puede descomponerlo de forma conservadora y revisable; para nombres femeninos debe reconocer un sufijo final `de Apellido` como apellido de casada cuando exista.

**RF-174.** La Ficha Digital debe renderizarse en el Paso 3 y no en el Paso 1. Su contrato salarial, confirmación de cuotas y límites del año actual se mantienen sin cambios funcionales.

**RF-175.** La navegación común de los seis pasos debe disponer de una barra superior y otra inferior visualmente simétricas, sincronizadas desde la misma lógica. En PC/laptop la superior puede mantenerse visible bajo el encabezado durante pasos largos; la inferior permanece en el flujo normal al final del contenido.

**RF-176.** El estado temporal debe distinguir el origen personal `MANUAL`, `MI_RETIRO_SEGURO` o `MI_RETIRO_SEGURO_EDITADO`. El PDF original no se guarda y los identificadores confirmados permanecen únicamente en la sesión de la pestaña.

**RF-177.** En modalidad PDF no se puede continuar si faltan fecha de nacimiento, sexo o sistema previsional; la interfaz debe indicar que esos campos se completan mediante la revisión editable del documento.


### UX.4.6b Revisión 2 — privacidad, validación y consistencia transversal

**RF-178.** Fecha de nacimiento, sexo y sistema previsional deben mostrar un indicador visual de campo obligatorio, acompañado de una alternativa textual accesible. Al intentar continuar con un requerido inválido, se conserva borde/estado de error, mensaje inline asociado y foco sobre el primer campo inválido.

**RF-179.** Antes de ingresar o importar datos en `Simular`, la aplicación debe presentar un consentimiento informado y versionado que explique categorías de datos, finalidades, conservación, derechos, contacto y tecnologías de almacenamiento utilizadas.

**RF-180.** Si el usuario rechaza el tratamiento, la aplicación debe eliminar el estado temporal de simulación de la pestaña y volver a Inicio. Un cambio material de la política debe provocar una nueva solicitud de aceptación.

**RF-181.** Mientras la aplicación no cree cookies, analítica, publicidad ni rastreadores, no debe mostrar un banner de cookies que sugiera lo contrario. Debe informar de forma separada el uso de `sessionStorage` y `localStorage`. Cualquier cookie no esencial futura requiere consentimiento granular previo.

**RF-182.** El cargador PDF debe presentar selector y acción de análisis con altura/alineación coherentes. La vista previa debe eliminar lenguaje técnico innecesario y no mostrar leyendas redundantes sobre `Detectado/No detectado` ni avisos de nombre completo sin dividir.

**RF-183.** Las tablas interactivas deben ofrecer un hover suficientemente perceptible en Claro, Oscuro y Alto contraste. Las ayudas contextuales deben utilizar un botón compacto con icono `i`, sin texto visible redundante, y reposicionarse cuando su panel pudiera recortarse por los bordes del viewport o por contenido inferior.

**RF-184.** La futura exportación desde Resultados debe generarse solo por acción explícita, identificar el contenido como estimación orientativa/no oficial, permitir seleccionar información relevante y ofrecer la posibilidad de excluir identificadores personales. No debe subirse automáticamente a servicios externos.

**RF-185.** La vista pública de Fuentes debe incluir el marco de protección de datos aplicable al producto —Ley 81 de 2019, Decreto Ejecutivo 285 de 2021 y orientación oficial de ANTAI— y acceso a la política/condiciones de tratamiento vigentes.


**RF-186.** La casilla de aceptación de términos debe permanecer deshabilitada hasta que el usuario alcance el final del documento visible. La aplicación no debe añadir un bloque **Fin de los términos** ni mostrar un mensaje **Lectura completada**; al cumplirse el requisito se habilita la casilla y desaparece la ayuda previa de desplazamiento.

**RF-187.** Todos los pasos de Simular deben compartir dos barras visualmente simétricas y sincronizadas, con Inicio/Anterior, selector directo de paso, estado y acción primaria. En escritorio la superior puede mantenerse visible bajo el encabezado; la inferior permanece al final del contenido.

**RF-188.** Los textos visibles de la aplicación deben estar vinculados a su finalidad previsional o a necesidades funcionales, legales, de privacidad, seguridad y accesibilidad. No deben presentar Mi Retiro Proyectado como aplicación educativa, didáctica o pedagógica ni exponer detalles internos que no ayuden al usuario a tomar una acción o comprender el alcance del producto.


## 24. UX.4.6c — Simular / Paso 2 · Cuotas

**RF-189.** El Paso 2 debe separar visualmente las cuotas ya acreditadas de los supuestos de cotización futura.

**RF-190.** `cuotas_totales`, `cuotas_anio_actual` y `continua_cotizando` son obligatorios. `cuotas_esperadas_cierre_anio` y `cuotas_esperadas_por_anio` son obligatorios solo cuando el Asegurado(a) indica que continuará cotizando.

**RF-191.** Un campo acreditado confirmado desde Mi Retiro Seguro debe quedar de solo lectura en el Paso 2. Un campo no detectado por el PDF debe permanecer editable para captura manual.

**RF-192.** La interfaz debe informar de forma visible si un valor proviene del PDF o si quedó pendiente de captura manual, sin exponer terminología interna de persistencia.

**RF-193.** La corrección de un dato importado debe realizarse desde la vista previa del comprobante, no editando directamente el campo protegido en el Paso 2.

**RF-194.** Los supuestos de cotización futura no se deben bloquear por la existencia de un PDF, porque representan decisiones futuras que el documento no determina por el Asegurado(a).

**RF-195.** Si `continua_cotizando = false`, los controles de cuotas futuras deben quedar deshabilitados, no requeridos y acompañados de una explicación visible.

**RF-196.** Las barras superior e inferior del wizard deben ser la única acción primaria de Analizar/Continuar para el Paso 2; no se deben renderizar botones equivalentes dentro de la tarjeta.

**RF-197.** El resultado del Paso 2 debe diferenciar cuotas acreditadas y estimación al cierre y declarar que todavía no constituye un cálculo de pensión.

**RF-198.** El selector de apariencia debe representar Sistema, Claro, Oscuro y Alto contraste mediante iconografía SVG reconocible sin sustituir sus etiquetas textuales accesibles.


**RF-199.** Desde cualquier paso que consuma datos importados, la acción de revisar la importación debe abrir la misma vista previa aunque el componente original se haya renderizado dentro de otro panel del wizard.

**RF-200.** Las leyendas de obligatoriedad deben usar de forma uniforme `* Campo obligatorio`. Cuando una obligación dependa de otra respuesta, el asterisco y el atributo `required` se actualizarán dinámicamente sin cambiar la redacción general de la leyenda.

**RF-201.** Los campos editables de texto o número deben ofrecer una pista breve o ejemplo cuando ayude a entender el formato esperado. La pista debe desaparecer de forma nativa al existir un valor y no debe duplicar una ayuda contextual equivalente debajo del campo.

**RF-202.** Las ayudas contextuales deben mostrar únicamente el icono `i` en la interfaz, conservando un nombre accesible mediante `aria-label`.

**RF-203.** Los estados de datos importados deben describirse en lenguaje neutral, por ejemplo “Dato completado desde la importación”, evitando mensajes técnicos como “protegido contra edición” o referencias innecesarias al mecanismo interno.


**RF-204.** La vista previa de Mi Retiro Seguro debe estar agrupada por destino funcional y mostrar en los títulos el paso correspondiente: Datos personales e Información previsional básica en Paso 1, Cuotas acreditadas en Paso 2, Historial anual en Paso 3 y referencia de retiro/prestación en Pasos 5 y 6.

**RF-205.** El Paso 1 es la única excepción que puede mostrar la vista previa completa. Cuando **Revisar importación** se invoque desde un paso posterior, solo deben mostrarse los datos aplicables a ese paso.

**RF-206.** La sección del Paso 2 debe presentar tanto el total de cuotas acreditadas como las cuotas acreditadas del año actual. Cuando estas últimas provengan de un registro anual del comprobante, la edición confirmada debe mantenerse sincronizada con ese registro.

**RF-207.** El disparador de ayuda contextual debe conservar una sola circunferencia visible alrededor del icono `i`; el área exterior de interacción no debe dibujar un segundo contorno.

## UX.4.6d — requisitos del Paso 3 · Historial

**RF-208.** El Paso 3 debe denominarse **Historial salarial y base para proyección** y organizarse en tres secciones internas: historial anual, detalle del año actual y base salarial.

**RF-209.** Las barras comunes superior e inferior deben ser la única acción primaria del Paso 3; no se renderizarán botones internos equivalentes para analizar historial, validar detalle, analizar salario, retroceder o continuar.

**RF-210.** `Analizar historial` debe validar el detalle del año actual cuando esté habilitado, el historial anual cuando el modo lo requiera y la base salarial. Si una sección falla, la interfaz debe dirigir la atención a esa sección y no habilitar el avance al Paso 4.

**RF-211.** Cuando el Paso 3 quede completo, ambas barras deben cambiar a **Continuar a proyección** y permitir el acceso al Paso 4.

**RF-212.** El historial anual no debe ofrecer una acción que complete automáticamente años vacíos con 12 cuotas. Un año sin información debe permanecer pendiente.

**RF-213.** El período histórico debe usar el año de ingreso a la CSS como referencia cuando exista, permitir corregir el año inicial y tratar el año calendario actual como año final sin requerir una acción manual de regeneración.

**RF-214.** La tabla histórica debe permitir filtrar Todos/Pendientes y representar cada fila como Pendiente, Parcial, Completo o Sin cotización según cuotas y salario disponibles.

**RF-215.** Si una fila histórica empieza a completarse, cuotas y salario anual reportado deben validarse conjuntamente. Una fila totalmente vacía continúa representando un año pendiente.

**RF-216.** Cuotas o salarios anuales confirmados desde Mi Retiro Seguro deben quedar de solo lectura por campo en el Paso 3. Un campo ausente del documento debe permanecer editable.

**RF-217.** Desde el Paso 3, **Revisar importación** de Mi Retiro Seguro debe mostrar únicamente **Historial anual detectado (Paso 3)**; la revisión completa permanece exclusiva del Paso 1.

**RF-218.** El cargador de Ficha Digital debe usar la misma secuencia de interacción documental establecida para Mi Retiro Seguro y no mostrar explicaciones técnicas sobre almacenamiento local dentro del formulario.

**RF-219.** La vista previa de Ficha Digital debe abrir en modo revisión con controles bloqueados. `Editar campos` habilita cambios, `Finalizar edición` vuelve a bloquearlos e `Importar datos` aplica la revisión confirmada.

**RF-220.** La Ficha Digital solo debe aportar datos del año calendario actual. Los meses/campos efectivamente importados quedan bloqueados en el detalle principal; meses o valores no disponibles permanecen editables.

**RF-221.** El enlace **Abrir Mi Caja Digital** debe concentrarse en el bloque de Ficha Digital del Paso 3 y no duplicarse en el detalle del año actual.

**RF-222.** Cuando la base salarial sea manual, monto y periodicidad son obligatorios. Cuando provenga de una opción automática válida, el monto se muestra de solo lectura y la periodicidad se fija como mensual.

**RF-223.** El Paso 3 debe finalizar con un resumen unificado de cuotas de referencia, cuotas identificadas, diferencia, total salarial reportado y base mensual seleccionada.

**RF-224.** Las plantillas del asistente no deben incluir paneles **Próximo paso...**; la navegación común es la única superficie que anticipa y ejecuta el avance.

**RF-225.** Los estados de origen de historial y detalle reciente deben conservarse en metadata del frontend separada de los contratos de cálculo, con procedencia por año/campo o mes/campo según corresponda.

**RF-226.** La regla original impedía a Ficha Digital modificar `cuotas_anio_actual`; desde R23 queda **sustituida parcialmente por RF-332 a RF-335**. Quitar una Ficha Digital no debe borrar arbitrariamente una referencia de cuotas vigente, y una ficha con menos meses no puede reducir Paso 2 de forma automática.

**RF-227.** Si la cantidad de meses importados con cuota marcada difiere del total del Paso 2, la interfaz debe informar la diferencia y ofrecer revisar ambos valores sin sobrescribir el total agregado del Paso 2.

**RF-228.** Cuando exista una Ficha Digital importada y el usuario desactive el detalle del año actual, la interfaz debe indicar que los salarios mensuales importados no se usarán mientras permanezca seleccionado el total anual del historial.

**RF-229.** `¿Deseas detallar el año actual?` y `Forma de captura` deben mantener alineación superior consistente aunque una de las columnas muestre una nota de procedencia adicional.

**RF-230.** Si el año actual tiene cuotas acreditadas pero el salario anual sigue pendiente y no proviene de una fuente confirmada, el campo debe mostrarse vacío en lugar de `0.00`; el mensaje de validación debe orientar a completar el total anual o activar la captura mensual/quincenal.

**RF-231.** Una casilla que representa un estado derivado directamente de un documento confirmado debe quedar fijada y no puede desmarcarse desde la pantalla principal. Esta regla no se aplica a casillas que representan decisiones del usuario.

**RF-232.** En Ficha Digital, todo mes detectado con salario y estado utilizables debe presentarse con **Cuota acreditada** marcada y bloqueada; los meses no detectados permanecen manuales.

**RF-233.** Las filas con datos documentales confirmados deben distinguirse visualmente mediante un patrón común reutilizable en las tablas de los Pasos 1–6 y futuras vistas equivalentes.

**RF-234.** En la vista previa de Mi Retiro Seguro, la casilla de inclusión en historial real debe quedar determinada por la clasificación del registro: `HISTORICO` marcado, cualquier otra clasificación no marcada; el usuario corrige la clasificación mediante **Editar campos**, no la casilla directamente.


**RF-235.** Las filas que mezclen procedencia documental y captura manual deben usar una señal de origen basada en la paleta primaria, reservando verde para estados semánticos de éxito/completitud.

**RF-236.** Toda casilla que represente un valor documental confirmado debe mostrarse marcada y bloqueada; su marca debe permanecer visible en Claro, Oscuro y Alto contraste.

**RF-237.** No se añadirán casillas de selección a tablas que no requieran una decisión o estado booleano real; la procedencia de una fila se expresará mediante estilo, bloqueo de campos y metadatos accesibles.

**RF-238.** En el detalle salarial del año actual, todo mes importado desde Ficha Digital con salario/estado utilizable debe mostrar **Cuota acreditada** seleccionada y bloqueada. La marca debe seguir visible en Claro, Oscuro y Alto contraste incluso si el navegador atenúa controles deshabilitados.

**RF-239.** La lectura del detalle y de la vista previa debe interpretar una casilla con procedencia documental bloqueada como seleccionada, aunque una sesión antigua no conserve el estado nativo `checked`. Los meses sin procedencia documental continúan bajo captura manual.


### UX.4.6d R6 — gestión de datos del asistente

**RF-240.** La barra superior del asistente debe incluir un menú **Opciones** con acciones para limpiar el paso activo y reiniciar la simulación.

**RF-241.** Limpiar un paso debe conservar los pasos anteriores y eliminar/inutilizar todos los datos y resultados del paso activo y posteriores.

**RF-242.** Si el paso activo no contiene datos, la aplicación debe informar el estado sin abrir una confirmación destructiva innecesaria.

**RF-243.** Reiniciar simulación debe crear un estado vacío en Paso 1 y conservar la preferencia visual y la aceptación vigente de privacidad.

**RF-244.** Fuentes/Privacidad debe permitir borrar los datos locales de Mi Retiro Proyectado en el navegador, incluyendo simulación, consentimiento y apariencia.

**RF-245.** Toda acción destructiva con datos debe requerir confirmación explícita y describir su alcance antes de ejecutarse.

**RF-246.** La barra inferior no debe duplicar acciones destructivas; debe mantener únicamente navegación y acción principal del paso.

**RF-247.** La versión vigente de Términos/Privacidad debe describir de forma comprensible las diferencias entre limpiar un paso, reiniciar la simulación y borrar los datos locales de la aplicación.

### UX.4.6d R7 — consulta posterior de privacidad

**RF-248.** El botón **Revisar términos de privacidad** de Fuentes debe abrir el documento legal en la misma página y no navegar a Simular.

**RF-249.** La consulta posterior debe ocultar los controles de aceptación/rechazo, conservar la aceptación vigente y no solicitar una nueva aceptación por el solo hecho de revisar el texto.

**RF-250.** El modal de Términos/Privacidad debe mostrar un control `×` en la esquina superior derecha. En modo revisión cierra el modal; en el consentimiento inicial debe impedir continuar sin aceptación y devolver a Inicio.

**RF-251.** El modal y su controlador deben estar disponibles globalmente desde `base.html`, manteniendo una única instancia y evitando IDs o scripts duplicados en Simular.

**RF-252.** El menú **Opciones** del asistente debe existir exclusivamente en la barra superior sticky; la barra inferior conserva solo atrás, selector de paso, estado y acción principal.

### UX.4.6d — Revisión 8

**RF-253.** El estado visual de una fila del historial anual debe recalcularse al modificar cuotas o salario y distinguir, como mínimo, pendiente, falta de salario, falta de cuotas, revisar, sin cotización, parcial y completo.

**RF-254.** El filtro **Pendientes** debe usar la misma evaluación semántica de estado; una fila parcial válida o completa no debe aparecer como pendiente.

**RF-255.** Cuando una tabla muestre cuatro o menos filas visibles, la interfaz debe evitar un scroll vertical artificial; las tablas extensas deben conservar desplazamiento interno. Este patrón será reutilizable por pasos y tablas futuras.

**RF-256.** Después de analizar correctamente el historial anual, el Paso 3 debe mostrar de inmediato cuotas de referencia, cuotas identificadas, diferencia y total salarial reportado, aunque la base salarial todavía esté pendiente.

**RF-257.** Todo control `input[type=file]` debe distinguir visualmente el botón **Seleccionar archivo** con un tratamiento coherente de la paleta primaria en Claro, Oscuro y Alto contraste.

**RF-258.** Los mensajes contextuales de tablas no deben desplazar verticalmente un control respecto de las filas equivalentes; la orientación del último mes de Ficha Digital debe conservarse sin alterar la alineación de la columna de estado.

### UX.4.6d — Revisión 9

**RF-259.** El estado visual del historial debe actualizarse en tiempo real al modificar cuotas o salario, sin depender del orden de captura.

**RF-260.** Con el filtro **Pendientes** activo, una fila que deje de ser pendiente debe ocultarse inmediatamente y el contador debe actualizarse sin cambiar manualmente de filtro.

**RF-261.** Un contenedor tabular con pocas filas visibles no debe mostrar flechas, pista o thumb de desplazamiento vertical cuando no existe contenido que desplazar.

**RF-262.** Si desde Fuentes se abren los términos sin existir consentimiento vigente, el modal debe permitir completar lectura y aceptación en esa misma página; dicha aceptación debe ser reconocida posteriormente por Simular.

**RF-263.** La tecla `Esc` debe cerrar de forma contextual el modal de privacidad sin activar la animación de modal estático: en Fuentes/consulta simplemente cierra; en Simular sin aceptación no habilita el formulario.

**RF-264.** Los placeholders de identidad y ejemplos de captura deben ser ficticios y genéricos, sin reutilizar información personal de casos reales.

**RF-265.** Toda tabla visible de la aplicación debe utilizar el contrato `app-table-shell` o un componente equivalente que preserve borde, radio, superficie y adaptación temática comunes.

**RF-266.** Las tablas generadas dinámicamente por JavaScript deben adoptar el mismo contrato visual que las tablas renderizadas por plantilla.

**RF-267.** Claro, Oscuro y Alto contraste deben conservar geometría tabular equivalente; Alto contraste debe reforzar el borde sin depender de sombras.

**RF-268.** Los contenedores tabulares comunes deben participar en la detección accesible de desplazamiento horizontal y recibir foco únicamente cuando exista desbordamiento real.

**RF-269.** Reactividad de filas, filtros de pendientes, estados progresivos y bloqueo de casillas importadas deben reutilizarse en tablas futuras solo cuando el dato representado tenga la misma semántica funcional.

**RF-270.** Una nueva tabla no debe introducir radios, bordes o paletas ad hoc si puede reutilizar `app-table-shell` y los tokens visuales del sistema.



### UX.4.6d — Revisión 11

**RF-271.** Toda tabla con scroll interno y contrato `app-table-shell` debe mantener carril y thumb visualmente dentro de la geometría redondeada; en navegadores Chromium no deben aparecer botones/flechas que invadan las esquinas.

**RF-272.** La representación del scrollbar debe conservar contraste suficiente en Claro, Oscuro y Alto contraste sin modificar las dimensiones ni el significado funcional de la tabla.

**RF-273.** En todo importador PDF, **Seleccionar archivo** y **Analizar documento** deben compartir la misma altura exterior y alineación vertical.

**RF-274.** Las reglas RF-271 a RF-273 deben reutilizarse por componentes comunes en tablas e importadores futuros, evitando estilos locales que vuelvan a introducir asimetrías.

### UX.4.6d — Revisión 12

**RF-275.** Términos, modales, página y superficies tabulares desplazables deben compartir un scrollbar temático coherente con Claro, Oscuro y Alto contraste sin alterar el mecanismo nativo de desplazamiento.

**RF-276.** Cuando Chromium/Windows exponga botones o flechas del scrollbar, el estilo común debe suprimirlos para evitar que sobresalgan de la geometría del componente.

**RF-277.** `app-table-shell` debe usar un radio específico menor que las tarjetas y conservar bordes/encabezados simétricos en los tres temas.

**RF-278.** Si el filtro **Pendientes** del historial anual tiene cero filas visibles, la tabla y sus encabezados deben ocultarse y mostrarse un estado vacío accesible.

**RF-279.** El botón **Seleccionar archivo** debe conservar su tratamiento visual al pasar el puntero por el nombre del archivo; el hover diferenciado se aplica únicamente sobre el botón de selección.

**RF-280.** Comparador y las tablas posteriores que usan el contrato común deben conservar `app-table-shell`; las reglas funcionales específicas solo se añaden cuando su semántica lo requiera.


### UX.4.6d — Revisión 13

**RF-281.** Todo `input[type=file]` debe mantener el color, fondo y borde definidos por la paleta de la aplicación aunque el puntero esté sobre el nombre del archivo y el navegador active `:hover` sobre el control completo.

**RF-282.** El comportamiento anterior debe conservarse en Claro, Oscuro y Alto contraste y en estados de foco; no debe depender de soporte específico para hover sobre `::file-selector-button`.


### UX.4.6d — Revisión 14

**RF-283.** La modalidad manual del Paso 1 debe presentar los campos de identidad y previsión dentro de un único bloque visible denominado **Información personal**, evitando dos secciones que obliguen a recorrer el formulario para completar datos relacionados.

**RF-284.** El control **Sexo** debe aparecer antes de **Apellido de casada** y ambos deben compartir la misma zona lógica del formulario; al seleccionar Femenino, Apellido de casada debe mostrarse inmediatamente y continuar siendo opcional.

**RF-285.** La reorganización visual del Paso 1 no debe modificar obligatoriedad, procedencia, contratos de importación de Mi Retiro Seguro ni fórmulas previsionales.

### UX.4.6d — Revisión 15

**RF-286.** Todo campo de formulario no editable debe diferenciarse perceptiblemente de uno editable en Claro, Oscuro y Alto contraste mediante un contrato visual común.

**RF-287.** La diferenciación de RF-286 no debe depender solo del color y debe aplicarse a controles importados, calculados o deshabilitados cuando compartan la misma semántica de no edición.

**RF-288.** Los encabezados y ayudas de importación deben identificar la fuente/documento y no denominar la modalidad por el formato PDF; la validación técnica del formato actual permanece independiente.

**RF-289.** Ficha Digital y Mi Retiro Seguro deben reutilizar el mismo lenguaje de selección y análisis de documento.

**RF-290.** Al limpiar Paso 2, `continua_cotizando`, `cuotas_esperadas_cierre_anio` y `cuotas_esperadas_por_anio` deben volver al estado vacío y no reaparecer por valores predeterminados de plantilla.

**RF-291.** Una simulación nueva no debe presumir continuidad futura; los supuestos de 12 cuotas pueden sugerirse únicamente después de que el usuario seleccione explícitamente que continuará cotizando.

### UX.4.6d — Revisión 16

**RF-292.** Al analizar Paso 3, si `resumen_cuotas` no existe pero los controles de Paso 2 continúan completos, la aplicación debe revalidar cuotas automáticamente sin cambiar el paso visible.

**RF-293.** Si los datos de Paso 2 están incompletos, Paso 3 debe conservar todos sus datos y mostrar una indicación contextual; no debe navegar automáticamente hacia atrás.

**RF-294.** Al restaurar una simulación, un `paso_actual` que ya no cumpla sus prerrequisitos debe reducirse al último paso accesible.

**RF-295.** Ficha Digital debe renderizarse dentro de **Detalle salarial del año actual**, después de sus controles de modalidad y antes de la tabla mensual.

**RF-296.** La reorganización de R16 no puede modificar parser, fórmulas, motores previsionales ni el significado de los datos importados/bloqueados.


### UX.4.6d — Revisión 17

**RF-297.** Un checkbox documental bloqueado debe conservar su valor booleano real; solo un control `checked` puede mostrar el gancho de selección.

**RF-298.** En la vista previa del historial, `HISTORICO` se propone para historial real; `HISTORICO_PROYECTADO` y `PROYECTADO` deben permanecer sin seleccionar por defecto aunque sus controles estén bloqueados.

**RF-299.** Si el comprobante contiene un total de cuotas acumuladas superior a las cuotas históricas/acreditadas por incluir proyección, la interfaz debe explicar ambas cifras y Paso 2 debe conservar la acreditada.

**RF-300.** Si el historial detectado contiene años anteriores a la fecha de ingreso CSS del mismo documento, la aplicación debe conservar los registros y mostrar una advertencia revisable.

**RF-301.** Los campos modificados dentro de **Editar campos** deben conservar metadata de edición y no presentarse posteriormente como si hubieran sido detectados literalmente.

**RF-302.** La incoherencia entre cuotas mensuales identificadas y cuotas del año actual debe mostrar ambos valores y explicar la diferencia entre salario disponible y cuota acreditada.

**RF-303.** R17 no modifica fórmulas, motores previsionales ni la separación entre historial real y proyección; corrige trazabilidad y comunicación de datos.

### UX.4.6d — Revisión 18

**RF-304.** Los campos que mezclen importación y captura manual deben poder representar **Detectado**, **Editado por ti**, **Completado manualmente** y **No detectado** mediante un contrato común reutilizable.

**RF-305.** Un campo no detectado por un documento no puede quedar bloqueado únicamente porque la importación esté confirmada; debe continuar editable hasta que el usuario lo complete o lo confirme desde la revisión.

**RF-306.** La procedencia debe conservarse por campo cuando sea posible; entrar en modo edición sin modificar un control no debe convertirlo en “Editado por ti”.

**RF-307.** Después de F5/Ctrl+F5, una importación confirmada debe conservar sus datos, acciones de revisión/eliminación y una identificación visual del documento, aunque el `input[type=file]` nativo aparezca vacío.

**RF-308.** La aplicación no debe intentar restaurar programáticamente el archivo seleccionado ni almacenar su ruta local; solo puede conservar metadata necesaria para la continuidad visual.

**RF-309.** Ficha Digital y el detalle del año actual deben distinguir registros detectados/editados de períodos completados manualmente o todavía no detectados.

**RF-310.** Limpiar un paso debe eliminar también la metadata de procedencia/edición perteneciente a ese paso y a los posteriores que se invaliden.


### UX.4.6d — Revisión 19

**RF-311.** Cuando el detalle del año actual esté habilitado, la fila anual del año vigente debe derivar automáticamente su número de cuotas de las casillas **Cuota acreditada** del detalle.

**RF-312.** El salario anual del año vigente debe ser la suma de los salarios correspondientes a meses con cuota acreditada; salarios conocidos sin cuota marcada permanecen disponibles para análisis reciente pero no se suman al historial acreditado.

**RF-313.** La fila anual derivada debe actualizarse reactivamente al escribir salarios, completar quincenas o cambiar una casilla manual, y debe mostrar `Parcial` mientras el año tenga entre 1 y 11 cuotas con salario coherente.

**RF-314.** Cambiar manualmente una casilla de cuota del año actual debe actualizar `cuotas_anio_actual` y `cuotas_totales` del Paso 2 conservando las cuotas anteriores al año vigente, sin navegación automática hacia atrás.

**RF-315.** Las cuotas actualizadas desde el detalle deben conservar procedencia de edición del usuario, invalidar resúmenes dependientes y ser revalidadas por los servicios existentes antes de permitir continuar.

**RF-316.** Si una cuota marcada carece de salario, la sincronización anual no debe presentar un total parcial como válido; la fila debe continuar pendiente y el servicio mensual debe rechazar el análisis hasta completar el salario.


### UX.4.6d — Revisión 20

**RF-317.** El importador de Ficha Digital debe evaluar el último período detectado frente al mes actual antes de abrir la vista previa.

**RF-318.** Se considerará reciente una Ficha Digital cuyo último período corresponda al mes actual o a uno de los dos meses calendario anteriores; períodos más antiguos deben generar una advertencia de vigencia.

**RF-319.** La advertencia de vigencia no debe bloquear la importación: debe ofrecer **Seleccionar una ficha más reciente** y **Continuar con esta ficha**.

**RF-320.** Una importación de Ficha Digital confirmada debe mostrar su último período detectado también después de F5; si deja de cumplir la ventana de vigencia, debe mostrarse una advertencia no destructiva sin volver a pedir el archivo.

**RF-321.** El Paso 3 debe mostrar un resumen visible de `resumen_detalle_anio_actual` con cuotas identificadas, salarios disponible/acreditado, meses con información/completos, últimos períodos y promedios utilizados por las bases automáticas; el resumen debe ocultarse al invalidar el detalle.


### UX.4.6d — Revisión 21

**RF-322.** Toda Ficha Digital cuyo último período detectado sea anterior al mes actual verificado debe mostrar advertencia de vigencia; no existe tolerancia automática de uno o dos meses.

**RF-323.** La decisión de vigencia no puede depender del reloj del navegador ni de una fecha local manipulable del equipo.

**RF-324.** El backend debe intentar obtener una fecha de referencia por HTTPS desde infraestructura oficial de la CSS sin enviar datos de simulación.

**RF-325.** Si no se puede verificar una fecha externa, la aplicación debe mostrar una advertencia conservadora y permitir escoger otra ficha o continuar; no debe clasificar la ficha como reciente por fallback local.

**RF-326.** La metadata de fecha de referencia debe persistir junto con la importación y revalidarse al restaurar una Ficha Digital confirmada.

**RF-327.** El parser de Ficha Digital no debe depender de `date.today()` para escoger el año de los registros cuando la llamada no suministre un año explícito; debe usar el año más reciente detectado en el documento.

**RF-328.** Antes de validar el detalle del año actual, la aplicación debe reconciliar con Paso 2 una confirmación manual de cuota vigente cuando esa confirmación sea la fuente más reciente.

**RF-329.** Si la reconciliación modifica las cuotas de Paso 2, el resumen de cuotas debe revalidarse automáticamente sin abandonar Paso 3.

**RF-330.** Si después de la reconciliación las cuotas del detalle no coinciden con Paso 2, debe mostrarse un error visible que indique ambos conteos y explique que los salarios conocidos pueden conservarse aunque una cuota no esté acreditada.

**RF-331.** El resumen visible del detalle del año actual debe conservar las métricas necesarias para diferenciar salario disponible/acreditado, información completa/parcial y las bases automáticas soportadas.



### UX.4.6d — Revisión 23

**RF-332.** Si una Ficha Digital confirmada identifica más cuotas acreditadas del año actual que Paso 2, la aplicación debe actualizar `cuotas_anio_actual` al nuevo conteo y recalcular `cuotas_totales` conservando las cuotas previas al año vigente.

**RF-333.** La actualización documental de RF-332 debe revalidar el resumen de Cuotas en segundo plano sin navegar hacia atrás y debe informar al usuario del cambio aplicado.

**RF-334.** Una Ficha Digital con menos cuotas que la referencia vigente del Paso 2 no debe reducirla automáticamente; debe conservarse la cifra superior y mostrarse una advertencia de coherencia.

**RF-335.** La reconciliación defensiva de **Analizar historial** debe reconocer tanto cuotas manuales confirmadas como cuotas documentales bloqueadas de una Ficha Digital cuando estas amplían la referencia del Paso 2.

**RF-336.** Al sincronizar cuotas desde el detalle, `detalle_anio_actual.cuotas_anio_actual_referencia` debe actualizarse junto con Paso 2 para que F5/restauración no reintroduzca una referencia obsoleta.
