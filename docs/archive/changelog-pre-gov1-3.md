### GOV.1.2 — Gobierno y versionado

- Se adopta `0.0.22-beta` como primera versión formal bajo una política explícita.
- `VERSION` pasa a ser la fuente canónica consumida por `app/core/version.py`, FastAPI y el footer.
- Se documentan 21 estados retrospectivos (`0.0.1-beta` a `0.0.21-beta`) sobre los 80 commits previos, sin crear tags retroactivos.
- Se incorporan `GOVERNANCE.md`, `VERSIONING.md`, `RELEASES.md` y `.github/CODEOWNERS`.
- La licencia permanece deliberadamente pendiente hasta GOV.1.7.
- Se añaden regresiones específicas para impedir divergencias entre versión canónica, configuración, API e interfaz.
- Validación técnica de GOV.1.2: compilación Python, sintaxis JavaScript, `git diff --check`, versión canónica/API/footer y **403 pruebas automatizadas en OK**.

### Cierre final UX.4.6d

- UX.4.6d queda cerrada tras R23 con recorrido manual integral de Pasos 1–3 en PC/laptop y acceso correcto a Paso 4.
- La suite final alcanza **396 pruebas automatizadas en OK**; compilación Python, sintaxis JavaScript y `git diff --check` quedaron sin incidencias.
- Se valida la sincronización Ficha Digital → Paso 2 → Historial para el caso 5→6 cuotas, la persistencia tras F5 y la navegación sin retrocesos.

# Changelog

### UX.4.6d — Simular / Paso 3 · Historial

### UX.4.6d — Revisión 20

- Ficha Digital evalúa la vigencia del último período salarial detectado respecto del mes actual. Se consideran recientes el mes actual y los dos meses calendario anteriores; períodos más antiguos requieren una decisión explícita antes de abrir la vista previa.
- Una Ficha Digital potencialmente desactualizada no se bloquea: el usuario puede **Seleccionar una ficha más reciente** o **Continuar con esta ficha** y completar manualmente los meses faltantes.
- La importación confirmada conserva visible el último período detectado después de F5 y advierte si, por el paso del tiempo, la ficha deja de considerarse reciente.
- El Paso 3 incorpora un **Resumen del detalle del año actual** visible con cuotas identificadas, salario disponible/acreditado, meses con información/completos, últimos períodos y promedios que ya calculaba el servicio.
- El resumen visible se oculta al invalidarse el detalle para evitar mostrar resultados obsoletos. La suite completa alcanza **379 pruebas automatizadas en OK**.

### UX.4.6d — Revisión 16

- Paso 3 revalida automáticamente el resumen de cuotas cuando los datos del Paso 2 siguen completos, sin navegación regresiva.
- Si las cuotas realmente están incompletas, Paso 3 conserva el trabajo y muestra una dependencia contextual en vez de redirigir por sorpresa.
- La restauración de sesión retrocede al último paso accesible cuando una limpieza o invalidación dejó guardado un paso posterior.
- Ficha Digital se integra dentro de **Detalle salarial del año actual** y el cargador queda inmediatamente antes de la tabla mensual que alimenta.
- Se agregan regresiones R16 para estructura, restauración y dependencia Paso 2 → Paso 3.

### UX.4.6d — Revisión 15

- Los campos `readonly`/`disabled` adoptan un contrato visual transversal que distingue con claridad valores editables y no editables en Claro, Oscuro y Alto contraste; además del fondo/borde, incorporan una señal lateral primaria para no depender solo del color.
- La interfaz de importación deja de presentar el formato como parte del concepto de producto: **Importar desde Mi Retiro Seguro**, **Selecciona el documento** y textos equivalentes sustituyen encabezados del tipo “PDF compatible”. El transporte actual continúa siendo PDF y conserva sus validaciones técnicas.
- Ficha Digital reutiliza la misma terminología neutral de documento y los mensajes de selección dejan de exigir que el usuario interprete la compatibilidad del layout.
- **Limpiar Paso 2** deja `Cotización futura` realmente vacía: no conserva `Sí`, `12` y `12`. En una simulación limpia no se presume continuidad; al seleccionar explícitamente Sí se mantienen los valores sugeridos de 12 como ayuda.
- La redacción visible de Términos/Privacidad y Metodología se alinea con el concepto de documentos importados sin cambiar finalidades ni versión jurídica.

### UX.4.6d — Revisión 14

- La captura manual del Paso 1 unifica Identificación e Información previsional bajo **Información personal**.
- **Sexo** queda junto a **Apellido de casada**, evitando recorrer el formulario para localizar el campo condicional.
- Se mantienen IDs, obligatoriedad, importación y lógica previsional. La suite quedó en **346 pruebas automatizadas en OK**.

### UX.4.6d — Revisión 13

- **Seleccionar archivo** conserva su paleta aunque Chromium/Bootstrap active `:hover` sobre el `input[type=file]` completo al pasar por el nombre del archivo.
- Se protege también foco y prefijo WebKit. La suite quedó en **343 pruebas automatizadas en OK**.

### UX.4.6d — Revisión 12

- Se extiende el scrollbar temático a términos, modales, página y superficies desplazables comunes, manteniendo rueda, teclado y táctil y suprimiendo los botones/flechas nativos cuando el motor los expone.
- `app-table-shell` reduce ligeramente su radio respecto de las tarjetas para integrar mejor el desplazamiento interno sin perder la geometría redondeada de la interfaz.
- El filtro **Pendientes** oculta completamente la tabla cuando no quedan filas y muestra un estado vacío; ya no se conserva una cabecera sin registros.
- **Seleccionar archivo** conserva su identidad visual cuando el puntero se desplaza por el nombre del archivo; el cambio de tono queda limitado al hover directo del botón nativo.
- Se verifica por regresión que Comparador continúa usando `app-table-shell`, de modo que el contrato transversal alcanza también una tabla posterior al asistente.
- La suite completa alcanza **340 pruebas automatizadas en OK** en R12.

### UX.4.6d — Revisión 11

- El scrollbar interno de `app-table-shell` deja de usar los botones/flechas nativos de Chromium/Windows y adopta un carril transparente con margen respecto de las esquinas redondeadas.
- El thumb de desplazamiento utiliza colores coherentes con Claro, Oscuro y Alto contraste sin invadir el borde de la tabla; las tablas cortas continúan sin carril vertical.
- El selector **Seleccionar archivo** y la acción **Analizar documento** comparten exactamente la misma altura exterior y ancho disponible en los importadores de Mi Retiro Seguro y Ficha Digital.
- El contrato R11 se aplica transversalmente a tablas e importadores actuales y futuros mediante `app-table-shell` y las clases comunes de carga PDF.
- La suite completa alcanza **335 pruebas automatizadas en OK** en R11.

### UX.4.6d — Revisión 10

- Se introduce `app-table-shell` como contrato visual común para tablas del asistente, importaciones, comparador, retiro, resultados, proyección y línea temporal.
- Las tablas actuales adoptan bordes redondeados simétricos con tarjetas y formularios; las tablas generadas por JavaScript usan el mismo contrato.
- Claro, Oscuro y Alto contraste reciben una superficie, borde y encabezado tabular coherentes con la paleta de cada tema sin cambiar la semántica de colores de estado/importación ya validada.
- La accesibilidad de contenedores desplazables reconoce `app-table-shell`, de modo que las tablas futuras heredan el mismo criterio de foco cuando exista scroll horizontal.
- Se documenta que reactividad, filtros, estados progresivos, bloqueo de campos y casillas importadas se aplican transversalmente solo cuando el significado de la tabla lo justifica; no se fuerzan sobre tablas meramente informativas.
- La suite completa alcanza **330 pruebas automatizadas en OK** en R10.

### UX.4.6d — Revisión 9

- El historial anual adopta eventos delegados sobre el `tbody` para que el estado de cada fila se recalcule al escribir cuotas o salario, independientemente del orden de captura o de regeneraciones de la tabla.
- El filtro **Pendientes** se reaplica en el mismo evento y una fila deja de mostrarse tan pronto deja de requerir acción.
- Las tablas cortas eliminan completamente el carril vertical de desplazamiento en escritorio; en pantallas estrechas se conserva únicamente el desplazamiento horizontal cuando haga falta.
- Desde Fuentes, si no existe consentimiento vigente, **Revisar términos de privacidad** abre el mismo documento en modo consentimiento; al aceptarlo, Simular no vuelve a solicitarlo mientras la versión siga vigente.
- `Esc` queda definido como cierre contextual del modal: en consulta/Fuentes cierra sin aceptar; en el consentimiento obligatorio de Simular impide continuar sin aceptación.
- Los placeholders de identidad dejan de usar nombres, apellidos o cédulas concretas y emplean ejemplos ficticios/genéricos.
- La suite completa alcanza **324 pruebas automatizadas en OK** en R9.

### UX.4.6d — Revisión 8

- La tabla anual del Paso 3 actualiza el estado en tiempo real al escribir tanto cuotas como salario y distingue **Pendiente**, **Falta salario**, **Faltan cuotas**, **Revisar**, **Sin cotización**, **Parcial** y **Completo**.
- El filtro **Pendientes** utiliza el estado semántico real de cada fila; una fila parcial válida deja de considerarse pendiente.
- Las tablas cortas dejan de reservar/desplegar desplazamiento vertical innecesario; el patrón `table-scroll-compact` queda disponible para tablas actuales y futuras.
- Tras analizar el historial anual se muestra un resumen local con cuotas de referencia, cuotas identificadas, diferencia y total salarial reportado, sin esperar a completar la base salarial.
- El botón nativo **Seleccionar archivo** adopta una superficie diferenciada basada en la paleta primaria en Claro, Oscuro y Alto contraste, aplicable globalmente a controles `input[type=file]`.
- La advertencia del último mes de Ficha Digital deja de insertarse debajo del selector de estado para no romper la alineación de la tabla; la orientación se conserva mediante texto accesible/contextual del control.
- La suite completa alcanza **317 pruebas automatizadas en OK** en R8.

### UX.4.6d — Revisión 7

- **Revisar términos de privacidad** desde Fuentes abre el documento legal en la misma página mediante un modo de consulta no disruptivo.
- Consultar los términos no modifica la aceptación vigente ni obliga a aceptarlos nuevamente.
- El modal de términos incorpora un control `×` superior: en modo consulta solo cierra la ventana; durante el consentimiento inicial, cerrar sin aceptar equivale a no continuar y vuelve a Inicio.
- El modal y `privacidad.js` pasan a ser recursos globales de la interfaz para permitir la consulta desde Fuentes sin navegar a Simular.
- En Fuentes se renombra el enlace del proyecto como **Repositorio: GitHub del proyecto**.
- Se refuerza por CSS y regresión que **Opciones** pertenece únicamente a la barra sticky superior y no a la navegación inferior.
- Se corrige una etiqueta `<section>` duplicada en el documento legal visible.

### UX.4.6d — Revisión 6

- Se incorpora **Opciones** en la navegación superior del asistente con **Limpiar este paso** y **Reiniciar simulación**.
- Limpiar un paso elimina sus datos e invalida de forma automática todos los cálculos posteriores que dependan de ellos.
- Reiniciar simulación elimina todos los datos/cálculos pero conserva apariencia y aceptación vigente de privacidad.
- Fuentes/Privacidad incorpora **Borrar datos de esta aplicación en este navegador**, que elimina también constancia local de aceptación y preferencia visual.
- El texto legal visible y los documentos de privacidad se actualizan a la versión **2026-08-15.1** para explicar conservación, eliminación y controles del titular.
- Se agregan regresiones para impedir resultados posteriores obsoletos después de una limpieza parcial.


- Revisión 4: las filas con procedencia documental dejan de usar verde de éxito y pasan a una señal azul derivada de la paleta primaria, consistente en Claro, Oscuro y Alto contraste.
- Revisión 4: las casillas de cuota procedentes de Ficha Digital se fuerzan visual y funcionalmente como marcadas/bloqueadas, incluso tras restaurar una simulación existente.
- Revisión 4: el verde queda reservado para estados semánticos de éxito/completitud, evitando confundir procedencia de datos con validación.
- La suite completa alcanza **286 pruebas automatizadas en OK** antes de repetir la validación visual integral del Paso 3.

- Revisión 3: los meses detectados automáticamente en Ficha Digital se incorporan con **Cuota acreditada** marcada y bloqueada; los meses no presentes en el documento permanecen disponibles para captura manual.
- Revisión 3: las filas con datos documentales usan un estado visual común de procedencia para distinguirlas de filas manuales en Historial anual, Detalle del año actual y vistas previas de importación.
- Revisión 3: las casillas cuya selección deriva directamente de una clasificación importada quedan bloqueadas; en el comprobante de Mi Retiro Seguro la pertenencia al historial real sigue la clasificación `HISTORICO` y no depende de una casilla modificable.
- Revisión 3: se mantiene el total de cuotas del Paso 2 como referencia agregada; si la cantidad de meses importados difiere, se muestra una advertencia de coherencia sin reescribir el Paso 2.
- La suite completa alcanza **282 pruebas automatizadas en OK** en Revisión 3; la validación visual PC/laptop continúa pendiente.

- El Paso 3 se reorganiza en historial anual, detalle del año actual y base salarial, con una sola acción principal desde las barras superior/inferior.
- Se eliminan acciones internas duplicadas, el relleno masivo de cuotas vacías, el botón manual de regeneración de años y los paneles `Próximo paso...`.
- La Ficha Digital adopta el ciclo Seleccionar PDF → Analizar → Modo revisión → Editar campos → Importar datos y conserva procedencia por mes/campo.
- Revisión 2: se corrige una regresión por la que confirmar una Ficha Digital podía reemplazar `cuotas_anio_actual` del Paso 2 con el número de casillas marcadas en la vista mensual. La Ficha Digital deja de redefinir cuotas acreditadas y usa el Paso 2 como referencia única.
- Revisión 2: quitar una Ficha Digital ya no elimina la procedencia de `cuotas_anio_actual` cuando ese dato proviene de Mi Retiro Seguro o captura manual del Paso 2.
- Revisión 2: el estado de la Ficha informa si la cantidad de meses marcados como acreditados coincide con el total del Paso 2, sin adivinar qué meses corresponden.
- Revisión 2: se alinea verticalmente `¿Deseas detallar el año actual?` con `Forma de captura`, y cuando existe una Ficha importada pero el detalle se desactiva se explica que sus salarios no se usarán hasta volver a activar el detalle.
- Revisión 2: el año actual con cuotas y salario pendiente deja de mostrarse como `B/.0.00`; se presenta vacío y la validación orienta a completar el total anual o activar la captura mensual/quincenal.
- La suite completa alcanza **278 pruebas automatizadas en OK** en Revisión 2; la validación visual PC/laptop sigue pendiente.

### UX.4.6c — Simular / Paso 2 · Cuotas

- El Paso 2 se reorganiza en **Cuotas acreditadas** y **Cotización futura** para separar datos ya registrados por la CSS de supuestos futuros.
- Los cinco controles conservan validación accesible y muestran el asterisco de obligatoriedad cuando corresponde; los dos campos de cuotas futuras dejan de ser obligatorios cuando el usuario indica que no continuará cotizando.
- Los valores de `cuotas_totales` y `cuotas_anio_actual` detectados y confirmados desde Mi Retiro Seguro quedan de solo lectura en el Paso 2. Si el PDF no aporta uno de ellos, únicamente ese campo permanece editable para captura manual.
- Se incorpora trazabilidad por campo mediante `origen_campos_cuotas`; una simulación previa a UX.4.6c puede reconstruir el origen a partir de la referencia PDF confirmada.
- El Paso 2 ofrece **Revisar importación** para volver a la vista previa del comprobante; la corrección no se realiza directamente sobre un dato importado dentro del formulario.
- Al indicar que no continuará cotizando, los campos futuros se deshabilitan, dejan de ser requeridos y muestran una explicación visible del estado.
- Se eliminan el `Paso 2 de 6` redundante, el cuadro amplio sobre proyección y los botones internos duplicados. Las barras superior e inferior del wizard concentran Analizar/Continuar.
- El resultado se presenta como **Situación de tus cuotas**, con lenguaje orientado al usuario y separación entre acreditado y estimado.
- El selector global de apariencia sustituye el símbolo circular abstracto por iconos SVG de sistema, sol, luna y contraste, también visibles dentro del menú.
- Revisión 2: se corrige la reapertura del modal de importación desde Cuotas y pasos posteriores moviendo los modales fuera de paneles ocultos antes de mostrarlos.
- Revisión 2: los mensajes de origen se simplifican a lenguaje orientado al usuario; se elimina la frase “protegidos contra edición” y se sustituye el candado visual por un estado de confirmación.
- Revisión 2: `* Campo obligatorio` se normaliza como leyenda transversal; las ayudas contextuales quedan como icono `i` sin la palabra visible `Info`.
- Revisión 2: los campos editables reciben pistas/ejemplos breves dentro del control; desaparecen automáticamente cuando existe un valor manual o importado, evitando duplicar ayudas visibles.
- Revisión 3: el disparador de ayuda conserva un único círculo visual alrededor de `i`; el botón exterior mantiene el área de foco/clic sin dibujar un segundo contorno.
- Revisión 3: **Revisar importación** abre una vista contextual por paso. Paso 1 conserva la vista completa; Paso 2 muestra únicamente las cuotas que corresponden a esa etapa, y el patrón queda preparado para Historial, Retiro y Resultados.
- Revisión 3: la vista previa se reorganiza como **Datos personales (Paso 1)**, **Información previsional básica (Paso 1)**, **Cuotas acreditadas (Paso 2)**, **Historial anual detectado (Paso 3)** y **Referencia de retiro y prestación (Pasos 5 y 6)**.
- Revisión 3: se expone de forma explícita la cuota acreditada del año actual dentro del bloque del Paso 2 y se sincroniza con el registro anual correspondiente cuando existe.
- La suite completa alcanza **253 pruebas automatizadas en OK** en la Revisión 3 y la validación visual en PC/laptop queda completada; UX.4.6c se cierra.

### UX.4.6b — Simular / Paso 1 · Datos personales

- El Paso 1 separa **captura manual** e **importación desde PDF** como modalidades mutuamente excluyentes, con captura manual seleccionada por defecto.
- Se agregan campos opcionales de identificación: primer/segundo nombre, primer/segundo apellido, apellido de casada, cédula y número de Seguro Social. Ninguno modifica las fórmulas previsionales.
- Fecha de nacimiento, sexo y sistema previsional muestran un asterisco semántico de **campo obligatorio** y conservan la validación accesible con borde/mensaje de error y foco sobre el primer campo inválido.
- El apellido de casada se muestra únicamente cuando el sexo seleccionado es femenino.
- La Ficha Digital sale del Paso 1 y se traslada al Paso 3, donde corresponde al historial salarial y al detalle del año actual.
- El cargador de Mi Retiro Seguro se compacta: selector de archivo y acción **Analizar documento** comparten altura y alineación, y el texto interno sobre memoria/motores se sustituye por un acceso breve a privacidad.
- La vista previa de Mi Retiro Seguro inicia bloqueada; **Editar campos** habilita cambios, **Finalizar edición** vuelve al modo revisión y **Importar datos** confirma la transferencia. Mientras existe una edición abierta, la importación permanece deshabilitada.
- El parser puede descomponer un nombre completo de forma conservadora y revisable; en nombres femeninos reconoce el patrón final `de Apellido` como apellido de casada cuando existe en el documento. Los campos explícitamente etiquetados por el PDF conservan prioridad.
- Se eliminan del modal los textos técnicos `Detectado = ...`, el aviso sobre nombre completo sin dividir y otros mensajes que no ayudan a tomar una decisión.
- Las filas de tablas reciben un hover global más perceptible y las ayudas contextuales cambian del círculo `?` a un botón compacto con icono `i`, con reposicionamiento vertical/horizontal para evitar recortes cerca del viewport o footer.
- `sessionStorage` conserva el origen del bloque personal como `MANUAL`, `MI_RETIRO_SEGURO` o `MI_RETIRO_SEGURO_EDITADO`; los documentos PDF continúan procesándose en memoria y no se persiste el archivo original.
- La navegación común del asistente usa dos barras sincronizadas y del mismo ancho que las tarjetas: una superior disponible durante pasos largos en PC/laptop y otra inferior al cierre del contenido. Ambas conservan Inicio/Anterior, salto directo, estado y acción primaria.
- Antes de capturar o importar datos, **Simular** presenta un consentimiento versionado de privacidad. Rechazarlo elimina el estado de simulación de la pestaña y devuelve a Inicio; aceptarlo habilita el flujo.
- La versión actual declara expresamente que no crea cookies, no integra analítica, publicidad ni rastreadores. Utiliza `sessionStorage` para la simulación y para la autorización activa de la pestaña; `localStorage` se limita a apariencia y constancia/versionado de la aceptación.
- Se añade una sección de privacidad en **Fuentes**, la Política de Privacidad, los Términos de uso y tratamiento de datos y una matriz interna de alineación con Ley 81 de 2019 / Decreto Ejecutivo 285 de 2021.
- El hardening incorpora `Cache-Control: no-store` en toda la API `/api/simulacion/`, Content Security Policy y Subresource Integrity para Bootstrap servido temporalmente por CDN. La localización de Bootstrap queda como acción pre-beta.
- Revisión 3: los términos visibles se amplían a 21 apartados en lenguaje comprensible; la casilla de aceptación permanece deshabilitada hasta llegar al final del documento y la política evita mostrar terminología técnica innecesaria al usuario.
- Revisión 3: la navegación del wizard pasa a un patrón dual y simétrico dentro del mismo ancho de las tarjetas: barra superior accesible durante pasos largos y barra inferior equivalente al cierre del paso.
- Revisión 3: las ayudas contextuales de la simulación pueden salir del borde de la tarjeta sin quedar recortadas.
- Revisión 4: se elimina del consentimiento el bloque visual **Fin de los términos** y el mensaje **Lectura completada**. Llegar al final sigue siendo requisito técnico para habilitar la casilla, pero la interfaz no añade mensajes meta una vez cumplido.
- Revisión 4: se formaliza que el texto público debe limitarse a contenido funcional, previsional, legal, de privacidad o de seguridad relevante para el usuario; no se presenta el producto como aplicación educativa, didáctica o pedagógica ni se muestran detalles internos sin utilidad práctica.
- UX.4.6b quedó **cerrada y validada en PC/laptop**, con commits por categorías y CI remoto en verde para Python 3.13 y 3.14. La suite de cierre fue de **233 pruebas automatizadas en OK**.

### UX.4.6a — rediseño visual integral y nueva página de Inicio

- Se incorpora `app/static/css/design-system.css` como capa transversal de presentación entre `style.css` y `accesibilidad.css`, sin modificar fórmulas ni contratos previsionales.
- La navegación pública se simplifica a **Inicio, Simular, Escenarios y Fuentes** conservando las rutas existentes.
- El selector visual se reemplaza por un menú compacto con **Automático, Claro y Oscuro** como opciones principales y **Alto contraste** dentro de Accesibilidad.
- El tema Claro adopta superficies más limpias y el tema Oscuro usa una base profunda casi negra; Alto contraste conserva negro/blanco, bordes explícitos y foco visible.
- La página de Inicio se rediseña alrededor de beneficios, sistemas contemplados, capacidades y proceso guiado; el mockup de resultado no presenta una pensión ficticia.
- El remate de PC/laptop reduce la escala del hero, mejora su interlineado, centra número/texto de los seis pasos y mantiene el aviso **Estimación orientativa** sobre la misma superficie del proceso.
- El footer se reorganiza en una composición centrada con producto, versión, aviso legal, **Fuentes oficiales**, autoría y copyright. Mi Caja Digital deja de duplicarse globalmente y permanece en los flujos de verificación individual.
- Las regresiones históricas de apariencia se actualizan al nuevo contrato visual y `tests/test_ux46a_redisenio_integral.py` añade trece comprobaciones específicas.
- La validación final de UX.4.6a alcanza **198 pruebas automatizadas en OK**, además de `compileall`, `node --check` y `git diff --check` sin incidencias. La revisión manual inmediata se cerró en PC/laptop; móvil, tablet y pantallas grandes quedan para beta/RC.

### Pre-beta — ajuste de CI y Dependabot

- La primera ejecución remota de `main` confirma CI verde en Python 3.13 y 3.14.
- Las regresiones del workflow dejan de exigir majors concretos de `actions/checkout`, `actions/setup-python` y `actions/setup-node`; validan el contrato de CI y permiten que Dependabot actualice esas Actions sin provocar falsos negativos.
- La regresión de `pypdf` deja de fijar `5.9.0` como valor eterno y pasa a exigir una única versión explícita `X.Y.Z`; la compatibilidad real continúa protegida por los tests de importación PDF.
- Dependabot limita las propuestas `pip` a las dependencias directas mantenidas por el proyecto, agrupa actualizaciones minor/patch compatibles del runtime y agrupa GitHub Actions en una sola propuesta. `pypdf` y los cambios major continúan sujetos a revisión individual.
- `requirements.txt` documenta qué paquetes son dependencias directas y qué líneas forman parte del snapshot transitivo reproducible.
- Se mantiene deshabilitado cualquier auto-merge: una actualización solo se acepta con CI verde y revisión explícita.

### Pre-beta — regresión E2E y hardening

- Se agrega regresión E2E por API para SEBD acreditado/proyectado, Mixto y SUCGS.
- Los dos importadores PDF comparten validación defensiva de extensión, MIME, tamaño, archivo vacío y firma `%PDF-` antes del parser.
- Se mantienen límites de páginas y se añaden límites de texto extraído para documentos anómalos.
- Las respuestas incorporan `nosniff`, bloqueo de framing, política de referrer y desactivación de cámara/micrófono/geolocalización; las importaciones usan `Cache-Control: no-store`.
- Se agrega CI para Python 3.13/3.14 y Node.js 24, con `pip check`, `compileall`, `node --check` y suite completa.
- Se agrega Dependabot semanal para `pip` y GitHub Actions.
- La suite alcanza **185 pruebas automatizadas**.


### UX.4.5 — información acreditada, proyección y cierre accesible

- El Paso 6 genera una segunda evaluación `SOLO_ACREDITADO` con la misma fecha de retiro pero sin añadir salarios ni cuotas futuras.
- SEBD reproduce de forma separada la fotografía acreditada y la proyección; el caso de regresión femenino conserva B/.741.59 acreditados frente a B/.769.42 cuando el escenario añade cinco cuotas a B/.1,500 mensuales.
- Mixto y SUCGS reutilizan la misma separación sin proyectar automáticamente sus saldos específicos; esos valores permanecen iguales en ambas fotografías.
- La interfaz incorpora una tabla accesible **Información acreditada y proyección al retiro**, con caption, encabezados de fila/columna, cuotas, pensión, pago único y diferencias.
- La referencia importada de Mi Retiro Seguro prefiere el cálculo propio acreditado cuando está disponible.
- Los resultados acreditados se almacenan e invalidan junto a su resultado proyectado correspondiente.
- Se refuerza el contraste de la tabla comparativa en Alto contraste y se revisa la semántica de los modales de importación.
- La suite alcanza **170 pruebas automatizadas**.

### UX.4.4 — edad anual y detalle salarial del año actual

- Historial salarial real incorpora la columna **Edad** inmediatamente después de Año.
- Proyección futura incorpora la misma columna para mantener continuidad entre datos históricos y estimaciones.
- La edad se deriva de la fecha de nacimiento ya guardada en el Paso 1 usando la convención de año calendario observada en los comprobantes de validación: `año - año de nacimiento`.
- El Paso 3 incorpora un detalle opcional del año actual con captura por total mensual o primera/segunda quincena.
- Cada mes diferencia salario disponible, estado completo/parcial y cuota ya acreditada; un salario puede existir sin que su cuota haya sido acreditada todavía.
- `POST /api/simulacion/detalle-anio-actual` valida el detalle, calcula totales disponibles/acreditados, último mes acreditado y bases salariales sugeridas.
- Cuando las cuotas marcadas coinciden con el Paso 2, el salario acreditado del detalle sincroniza la fila anual actual y el Paso 5 deriva automáticamente el último mes acreditado.
- La base de proyección puede continuar siendo manual o derivarse del último mes completo, del promedio de meses completos del año, de los últimos tres meses completos o del promedio salarial por cuota acreditada del año actual.
- El Paso 3 incorpora acceso contextual a Mi Caja Digital y centra esa acción dentro de su bloque.
- Se agrega carga opcional del comprobante PDF de Mi Retiro Seguro para extraer una referencia personal variable sin persistir el archivo ni exponer nombre, cédula o seguro social.
- El Paso 6 compara la referencia importada con la proyección actual únicamente cuando sistema, edad de retiro, persona y naturaleza de prestación son compatibles; si no, muestra ambas cifras sin fabricar una diferencia.
- La tabla temporal aumenta su ancho mínimo para conservar legibilidad con la columna adicional.
- La Ficha Digital importada se limita al año calendario actual; los salarios de años anteriores dejan de mostrarse y no se conservan en el estado de simulación.
- Los importes monetarios editables de las vistas previas usan separador de miles y exactamente dos decimales al mostrarse, reutilizando la utilidad monetaria común.
- La vista previa de Ficha Digital elimina las columnas redundantes Año y Aplicación porque todos sus registros pertenecen al año actual.
- La suite alcanza **161 pruebas automatizadas**.


Todos los cambios relevantes del proyecto se documentan aquí.

El proyecto todavía no ha publicado una versión estable; los cambios actuales se acumulan bajo **Unreleased** para la futura versión `0.1.0`.


## [Unreleased]

### Identidad y experiencia del producto

- La aplicación adopta el nombre visible **Mi Retiro Proyectado**.
- La identidad se centraliza en `app/core/config.py` para evitar nombres duplicados en plantillas y metadatos.
- La terminología pública usa **Asegurado(a)** y **Asegurados(as)** en lugar de `usuario` para referirse a quienes realizan simulaciones.
- Se eliminan de la interfaz etiquetas internas como `Paso 6F.1`, `Metodología 6F.2` y `Cierre funcional 6F.4`.
- La información sobre archivos `docs/*.md`, `regulations/*.json`, ADR y fases internas queda reservada a documentación de desarrollo.
- Se unifica el tamaño base de texto en formularios, ayudas, tablas, navegación y contenido explicativo; encabezados y valores previsionales mantienen jerarquía propia.
- El pie de página incorpora autoría, aviso de independencia y acceso directo a Mi Caja Digital.
- El acceso pendiente de importación se denomina `Importar desde Mi Caja Digital` para no presentar Mi Retiro Seguro como un recurso separado.
- Se agrega `docs/GUIA_INTERNA_DESARROLLO.md` con convenciones de marca, terminología y contenido exclusivamente técnico.
- Se agregan pruebas de regresión de identidad e interfaz.
- Se incorporan los modos **Seguir sistema**, **Claro**, **Oscuro** y **Alto contraste**, con persistencia local independiente de la simulación.
- Se añade enlace de salto al contenido, foco visible global, objetivos táctiles mínimos y respeto a movimiento reducido.
- El pie de página se compacta en dos líneas con copyright, aviso de independencia y acceso a Mi Caja Digital.
- La suite alcanza **96 pruebas automatizadas** después de añadir regresiones de mantenimiento técnico.
- UX.2.1 oscurece las superficies del modo Oscuro, convierte Alto contraste en un tema negro/blanco de contraste máximo y unifica colores semánticos para estados, alertas y badges.
- Se rediseña Inicio como portada del producto con propósito, sistemas contemplados, capacidades, proceso guiado y acciones principales.
- El wizard y la navegación rápida pasan a utilizar superficies adaptativas por tema en lugar de conservar fondos claros.
- Las tarjetas equivalentes alinean verticalmente sus contenidos y mantienen acciones al mismo nivel.
- Se elimina de Resultados la explicación técnica sobre `regulations/*.json`; la interfaz conserva únicamente la referencia oficial útil para el Asegurado(a).
- El footer evita partir el enlace a Mi Caja Digital y mantiene su segunda línea como una fila flexible compacta.
- El remate final de UX.2.1 centra únicamente los botones identificados en Inicio, Datos personales, Resultados y Metodología, sin alterar los botones que ya estaban correctos.
- En escritorios amplios, el aviso legal y `Abrir Mi Caja Digital` permanecen juntos en la segunda línea del footer.
- UX.3 adapta Inicio, navegación, formularios, tarjetas, Metodología, Comparador y resultados a laptop, tablet y móvil.
- En móvil, la navegación persistente del wizard se traslada a la parte inferior, respeta áreas seguras y mantiene retroceso, selector de paso y acción principal.
- Las tablas extensas conservan columnas legibles mediante desplazamiento horizontal dentro de su propio contenedor.
- El Paso 5 reemplaza la fecha exacta visible de actualización de cuotas por **Último mes con cuotas acreditadas**, separado de la fecha de evaluación y de las fechas de retiro.
- El backend deriva y valida la fecha técnica de corte desde el último mes acreditado y rechaza meses posteriores a la evaluación.
- Los dos botones de **Recursos oficiales para verificar información individual** reciben el mismo centrado visual que las demás acciones de Metodología y conservan `Abrir recurso oficial`, porque esos enlaces no son necesariamente fuentes normativas del cálculo.
- `.gitattributes` fuerza LF para todo archivo detectado como texto, incluidos archivos sin extensión, evitando advertencias de conversión LF/CRLF en Windows.
- `/favicon.ico` responde temporalmente con `204 No Content` y `Cache-Control: no-store` hasta integrar el favicon definitivo, eliminando el `404` del navegador sin inventar un icono provisional.
- UX.4.2 mantiene el número del paso activo en blanco cuando el tema efectivo es Claro, mejorando contraste sobre el círculo azul.
- La fila seleccionada de **Fechas y cuotas estimadas de retiro** refuerza su estado mediante fondo, contorno, radio y badge específicos para Claro, Oscuro y Alto contraste, con señal adicional de foco y soporte para colores forzados.
- La suite alcanza **112 pruebas automatizadas** con regresiones específicas de estados activos y selección perceptible.
- UX.4.3 asocia los errores de validación nativa con cada control mediante `aria-errormessage` y limpia ese estado cuando el dato vuelve a ser válido.
- Los errores dinámicos se enfocan al aparecer y usan `role="alert"` sin duplicar una segunda región viva `assertive`; las advertencias no urgentes pueden anunciarse como `status` de prioridad `polite`.
- El selector de escenario de retiro admite Enter sobre el radio, manteniendo la operación nativa con Espacio y flechas sin agregar un tab stop a toda la fila.
- Se corrige un ciclo de mutaciones de clase en la capa de accesibilidad que podía mantener ocupado el hilo principal y dejar las páginas públicas cargando indefinidamente; las mutaciones observadas pasan a ser idempotentes.
- La limpieza de errores usa `ValidityState.valid` en lugar de `checkValidity()`, evitando redisparar eventos `invalid` durante `input`/`change`.
- La suite alcanza **122 pruebas automatizadas** con regresiones específicas de UX.4.3 y su remate de estabilidad.
- UX.4.1 incorpora una capa global de accesibilidad mediante `accesibilidad.js` y `accesibilidad.css`, sin trasladar lógica previsional al frontend.
- Los campos que suelen generar dudas reciben ayudas contextuales desplegables y accesibles mediante `aria-expanded` y `aria-controls`.
- Los formularios marcan controles inválidos con `aria-invalid`, llevan el foco al primer campo que requiere corrección y anuncian el problema mediante una región viva global.
- El wizard relaciona pasos y paneles con regiones etiquetadas; las tablas reciben captions accesibles y sus contenedores desplazables pueden recibir foco cuando existe desbordamiento horizontal.
- Los enlaces que abren una pestaña nueva incorporan una indicación para lectores de pantalla sin añadir ruido visual.
- La suite alcanza **108 pruebas automatizadas** después del remate visual e interactivo de UX.4.1.
- Las ayudas contextuales pasan a un formato compacto tipo tooltip: aparecen con `hover` o foco de teclado y conservan clic como alternativa para interacción táctil.
- El selector del Paso 1 abrevia SUCGS como **Capitalización con Garantía Solidaria** sin cambiar la denominación jurídica utilizada en metodología, resultados o documentación normativa.
- La acción **Completar cuotas vacías con 12** recibe un tratamiento visual propio y distinguible en Claro, Oscuro y Alto contraste.
- En el Paso 5, cualquier punto de una fila de escenario futuro seleccionable activa el mismo escenario que su control de radio.
- En el Paso 6, la acción de cálculo SEBD se alinea con el selector de escenario salarial.
- Node.js LTS se documenta como herramienta opcional de desarrollo para `node --check`; no se incorpora como dependencia de `pip` ni como requisito de ejecución.

### Agregado

#### Cierre funcional 6F

- 6F.1: comparador transversal de escenarios de retiro y salario.
- 6F.2: `Ver cálculo completo` con trazabilidad de datos, regla, fórmula, sustitución y resultado.
- 6F.3: página `/metodologia`, enlaces normativos con nombres humanos y recursos oficiales de verificación.
- 6F.4: contrato transversal `resumen_unificado` para SEBD, Mixto y SUCGS.
- El comparador consume el contrato común en lugar de extraer montos con semánticas distintas de cada motor.
- El Paso 6 presenta un resumen final homogéneo que mantiene separadas mensualidades y pagos únicos.
- Al cierre funcional 6F.4, la suite alcanzó **69 pruebas automatizadas**.
- Mi Retiro Seguro deja de mostrarse como recurso independiente; la verificación individual queda centralizada en Mi Caja Digital junto con el régimen especial identificado.

#### Asistente y base técnica

- Aplicación web local con FastAPI, Jinja2, Bootstrap, CSS y JavaScript.
- Asistente de seis pasos para datos personales, cuotas, historial, proyección, retiro y resultados.
- Estado temporal de simulación en `sessionStorage`.
- Navegación directa entre pasos ya disponibles y barra persistente para flujos largos.
- Normalización salarial entre periodicidades y proyección por salario constante, porcentaje, salario futuro conocido o varios escenarios.
- Línea temporal que separa datos históricos, año actual y proyecciones futuras.
- Precisión monetaria basada en `Decimal` y `ROUND_HALF_UP` al materializar importes.
- Formato monetario con separadores de miles y máximo dos decimales en campos editables.
- Archivos normativos versionados en `regulations/`.
- Documentación técnica, funcional, normativa y de validación.

#### SEBD

- Motor de Pensión de Retiro por Vejez Normal.
- Clasificación automática de Normal, Anticipada, Proporcional y Proporcional Anticipada.
- Tabla mensual de factores de reducción para retiro anticipado.
- Cálculo de Indemnización por Vejez como pago único separado de una pensión mensual.
- Límites máximos ordinario y ampliados conforme a las condiciones implementadas.
- Endpoints directos e integrados para cálculo SEBD.
- Integración visual completa en el Paso 6.
- Regresiones automatizadas, incluida una validación anonimizada que reproduce B/.741.59.

#### Subsistema Mixto

- Motor separado para Componente de Beneficio Definido y Componente de Ahorro Personal.
- Tope de participación de B/.500.00 mensuales en el componente BD, con advertencia cuando el historial anual obliga a aproximar el tope mensual.
- Pensión programada del CAP cuando se suministran saldo y divisor actuarial aplicable.
- Opción explícita `AUTO / PENSION_PROGRAMADA / DEVOLUCION_TOTAL`.
- Devolución total del CAP como pago único cuando corresponde.
- Separación de indemnización BD, devolución CAP y total de pagos únicos.
- Bono de reconocimiento como dato oficial/validado, sin reconstrucción automática no sustentada.
- Garantía futura del Seguro Colectivo de Renta Vitalicia.
- Transición operativa Mixto → SUCGS desde 01/03/2032 con discrepancia normativa documentada.
- Endpoint integrado y presentación visual completa en el Paso 6.

#### SUCGS

- Motor contributivo del artículo 196 con tabla actuarial versionada.
- Fórmula `saldo / 1000 × factor de pensionamiento actuarial`.
- Capa solidaria de los artículos 194 y 195.
- Pensión Garantizada Solidaria y Beneficio Mínimo con valores legales versionados y posibilidad de suministrar valores vigentes confirmados.
- Garantía de reemplazo mínimo del artículo 197.
- Preevaluación del mínimo anual de cuotas y distribución temporal 50 % / 50 %.
- Salario promedio base mensual calculado desde salarios cotizados y meses cotizados.
- Estabilidad salarial del artículo 197 como condición explícita y auditable.
- Endpoints directos e integrados e interfaz completa en el Paso 6.

#### Comparación 6F.1

- Comparador transversal de escenarios de retiro y trayectorias salariales.
- Endpoint `POST /api/simulacion/comparar-escenarios` que reutiliza los servicios integrados SEBD, Mixto y SUCGS.
- Escenario base explícito y diferencias mensuales absolutas y porcentuales.
- Pagos únicos separados de pensiones mensuales dentro de la matriz comparativa.
- Advertencias de saldo constante para comparaciones hipotéticas Mixto y SUCGS.
- Página `/comparar` habilitada con selección de escenarios y tabla responsiva.

#### Pruebas

- Suite automatizada con **60 pruebas** después de 6F.1.
- Casos para precisión monetaria, proyecciones, línea temporal y retiro.
- Regresiones SEBD para modalidades e indemnización.
- Casos Mixto para pensión programada, devolución, garantías y pagos únicos.
- Casos SUCGS para componente contributivo, capa solidaria, garantía de reemplazo y condiciones que impiden aplicarla.

#### Documentación y repositorio

- `docs/INDICE.md` como mapa de la documentación.
- `docs/FUENTES_NORMATIVAS.md` con leyes, artículos, reglamentos, resoluciones y enlaces oficiales.
- Normalización de la numeración ADR en `docs/DECISIONES.md`.
- Reorganización del roadmap y de la documentación por capacidades actuales en lugar de acumulación histórica de subfases.
- Mejora de `.gitignore`, `.gitattributes`, `.editorconfig` y `CONTRIBUTING.md`.
- Los respaldos históricos y paquetes comprimidos de trabajo (`.zip`, `.7z`, `.rar`) se mantienen fuera de la raíz del repositorio; Git conserva la historia versionada y los paquetes locales quedan como respaldo secundario externo.
- Se eliminan archivos `.gitkeep` de directorios que ya contienen archivos versionados reales. `.gitkeep` se conserva únicamente cuando una carpeta vacía necesita existir en el repositorio.

### Cambiado

- JavaScript queda limitado a navegación, presentación, persistencia temporal y comunicación con la API; las fórmulas previsionales permanecen en Python.
- Los datos históricos y proyectados se mantienen diferenciados en todos los pasos.
- La proyección de cuotas respeta primero el cierre del año actual y luego la densidad futura.
- Los escenarios de retiro exigen cobertura suficiente del horizonte salarial o muestran una advertencia.
- Los resultados dependientes se invalidan cuando cambia un dato que los originó.
- `SUCGS` se presenta con su nombre completo en la interfaz.
- Saldo CAP y bono del Mixto reutilizan el formato monetario común; el divisor actuarial no lleva prefijo monetario porque no representa balboas.
- Los pagos únicos y las pensiones mensuales permanecen separados tanto en la API como en la interfaz.
- Los valores normativos sujetos a indexación o actualización no se tratan como constantes eternas.
- La documentación normativa centraliza enlaces oficiales y distingue ley, reglamento y comunicación operativa.

### Corregido

- Estructura Jinja y jerarquía HTML en los pasos del asistente.
- Duplicación accidental de componentes del historial.
- Restauración de scripts específicos de simulación e historial.
- Clasificación visual de años sin cotización.
- Diferencias de un centavo provocadas por redondeos intermedios.
- Proyección de cuotas que podía agregar meses al año actual contra la expectativa declarada por el Asegurado(a).
- Artefactos de punto flotante en campos monetarios.
- Semántica de campos no aplicables en la Indemnización por Vejez, usando `null` en lugar de valores numéricos engañosos.
- Navegación del Paso 6 para reconocer SEBD, Mixto y SUCGS sin tratar motores ya implementados como pendientes.
- Numeración duplicada y no consecutiva de ADR en la documentación.
- Secciones documentales obsoletas que seguían marcando como pendientes motores ya implementados.

### Pendiente para fases posteriores

- Preparación de estructura para informes y PDF.
- Persistencia voluntaria con SQLite.
- Pulido final de identidad visual, temas, accesibilidad y enlaces institucionales.

### 6F.3 — Metodología y fuentes

- Se agrega `/metodologia` como punto central de consulta de metodología, artículos, reglamentos, resoluciones y recursos oficiales.
- `Ver cálculo completo` deja de mostrar identificadores internos como `texto_unico` o `ley_462`; ahora presenta nombres humanos y enlaces oficiales.
- Se centraliza la presentación de fuentes de SEBD, Mixto y SUCGS reutilizando las URLs versionadas de `regulations/*.json`.
- Se documentan limitaciones conocidas, jerarquía de fuentes y recursos oficiales de verificación individual.

### UX.4.6d — Revisión 5

- Las casillas **Cuota acreditada** de meses importados desde Ficha Digital muestran el gancho de forma explícita y no dependen del pintado nativo de un checkbox deshabilitado.
- Un mes con salario/estado documental se reconoce como cuota importada aunque una sesión creada por una revisión anterior no conserve metadata específica de la casilla.
- La lectura del detalle y de la vista previa trata `data-imported-locked` como estado seleccionado, evitando discrepancias entre lo que se muestra y lo que se utiliza en la validación.
- Los meses no importados continúan con checkbox manual editable.
- La suite completa alcanza **290 pruebas automatizadas en OK** después de la corrección.


### UX.4.6d — Revisión 17

#### Corregido
- Las casillas bloqueadas de la vista previa ya no muestran un gancho solo por tener procedencia documental; el gancho depende del estado `checked` real.
- Las filas `Histórico + proyectado` y `Proyectado` dejan de parecer seleccionadas para el historial real cuando están excluidas por la clasificación automática.
- La procedencia visual de campos editados en la revisión del comprobante deja de mostrarse como `Detectado`.

#### Mejorado
- La vista previa diferencia las cuotas acreditadas del total acumulado que incluye períodos proyectados.
- Se advierte cuando el comprobante contiene años históricos anteriores a la fecha de ingreso CSS indicada, conservando los registros por provenir del documento.
- La incoherencia entre cuotas mensuales y Paso 2 explica que un salario puede estar disponible antes de que la cuota figure acreditada.
- Suite completa: **363 pruebas automatizadas en OK**.

## UX.4.6d — Revisión 18

### Añadido
- Contrato transversal de procedencia: **Detectado / Editado por ti / Completado manualmente / No detectado**.
- Procedencia por campo en Paso 1 y Paso 2; metadata de procedencia en Historial; indicador de procedencia en Ficha Digital y detalle mensual.
- Estado persistente visible de la importación tras F5/Ctrl+F5, incluyendo el nombre del documento confirmado cuando está disponible.

### Corregido
- Los campos no detectados en Paso 1 permanecen editables aunque exista una importación confirmada; solo datos confirmados/editados mediante la revisión quedan bloqueados en el formulario principal.
- Entrar en **Editar campos** de Ficha Digital ya no marca toda la importación como editada: la procedencia cambia únicamente cuando un control realmente se modifica.
- Limpiar Paso 3 elimina también metadata de edición de Ficha Digital.

### Privacidad
- Se conserva únicamente metadata local de visualización del nombre del documento junto con los datos ya confirmados en la sesión; no se conserva el archivo original ni se introduce persistencia remota. La versión de privacidad **2026-08-15.1** no cambia.


## UX.4.6d — Revisión 19

### Cambiado
- La fila del año actual del historial anual se sincroniza en tiempo real con las casillas **Cuota acreditada** y los salarios del detalle mensual/quincenal.
- Marcar o desmarcar manualmente una cuota del año actual actualiza también la referencia de Paso 2 sin obligar a navegar hacia atrás; el total acumulado conserva las cuotas anteriores al año vigente y suma el nuevo conteo confirmado.
- La procedencia de las cuotas recalculadas desde el detalle se registra como edición del usuario y los resúmenes dependientes se invalidan para revalidación segura.

### Corregido
- Paso 3 ya no exige volver a escribir manualmente el salario anual de 2026 cuando el mismo dato puede derivarse del detalle por meses.
- Un detalle con seis meses acreditados y salarios enero–junio produce 6 cuotas y B/.8,883.50 en la fila anual, en vez de conservar 5 cuotas o un salario vacío/desactualizado.
- Si una casilla está marcada pero su mes aún no tiene salario, la fila anual no presenta un total parcial engañoso: permanece en estado de salario pendiente hasta completar el dato.

### Validación
- Suite completa: **374 pruebas automatizadas en OK**.

## UX.4.6d — Revisión 22

### Corregido
- **Analizar historial** reconcilia las cuotas confirmadas manualmente en el detalle del año actual con Paso 2 antes de validar el payload, evitando bloqueos silenciosos después de restauraciones/F5 o eventos de interfaz perdidos.
- Si la referencia de Paso 2 cambia durante esa reconciliación, las cuotas se revalidan en segundo plano sin navegar hacia atrás.
- Una diferencia real entre las casillas de **Cuota acreditada** y Paso 2 ahora genera un error visible con ambos conteos y una instrucción concreta; ya no se limita a desplazar la pantalla hasta el detalle sin explicar la causa.

### Revisado
- Se conserva completo el **Resumen del detalle del año actual**: sus 11 métricas no son redundantes funcionalmente porque distinguen disponibilidad frente a acreditación, completitud frente a información parcial y las tres bases salariales automáticas.

### Validación
- Se añaden regresiones específicas de cierre de Paso 3 para reconciliación, revalidación silenciosa, mensaje explícito y contrato del resumen visible.
- Suite completa: **392 pruebas automatizadas en OK**.



## UX.4.6d — Revisión 23

### Corregido
- Una Ficha Digital confirmada con más cuotas del año actual que la fotografía previa del Paso 2 deja de bloquear **Analizar historial** con una diferencia artificial (por ejemplo, 6 frente a 5).
- La reconciliación previa al análisis reconoce ahora cuotas documentales bloqueadas de Ficha Digital además de cuotas añadidas manualmente.
- `cuotas_anio_actual_referencia` del detalle se actualiza junto con Paso 2 para evitar referencias persistidas obsoletas después de F5.

### Cambiado
- Si la ficha confirma un conteo superior, Paso 2 se actualiza hacia arriba y se revalida en segundo plano; si la ficha contiene menos cuotas que Paso 2, nunca se reduce automáticamente la referencia agregada.
- La importación informa cuando actualizó Paso 2 y muestra el nuevo total anual/acumulado.

### Validación
- Se agregan regresiones específicas para 5→6 cuotas por Ficha Digital, no degradación ante fichas incompletas y reconciliación defensiva del Paso 3.
