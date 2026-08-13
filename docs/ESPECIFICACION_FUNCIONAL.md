# Especificación funcional

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

**RF-130.** Cada mes debe distinguir el salario disponible de la existencia de una cuota ya acreditada. La presencia de salario no puede implicar automáticamente que la cuota esté acreditada.

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

**RF-149.** La Ficha Digital no puede inferir una cuota acreditada a partir de la presencia de salario. La vista previa debe pedir confirmación independiente de cada cuota y, al confirmar, puede prellenar `cuotas_anio_actual` con la cantidad de meses marcados.

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

**RF-169.** El Paso 1 debe permitir elegir entre **Ingresarlos manualmente** e **Importar desde PDF**. La captura manual es la modalidad predeterminada y ambas presentaciones deben ser mutuamente excluyentes.

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
