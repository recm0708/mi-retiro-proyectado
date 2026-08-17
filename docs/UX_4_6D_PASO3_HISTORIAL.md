# UX.4.6d — Simular / Paso 3 · Historial

**Estado:** Revisión 5 implementada técnicamente; pendiente validación visual y funcional completa en PC/laptop.

## 1. Objetivo

Reducir la carga y las acciones duplicadas del Paso 3 sin crear un nuevo paso global. La fase unifica historial anual, detalle reciente y base salarial bajo una sola acción de validación, manteniendo la procedencia de datos importados y evitando asumir información que el usuario o los documentos no han aportado.

## 2. Estructura visible

El Paso 3 queda dividido en:

1. **Historial salarial anual** — período, tabla anual, filtros y revisión de datos importados;
2. **Detalle salarial del año actual** — captura mensual/quincenal y Ficha Digital opcional;
3. **Base salarial para proyección** — base manual o derivada de información reciente validada.

No se agrega un séptimo paso. Las barras superior e inferior siguen mostrando `Paso 3 · Historial`.

## 3. Acción unificada

Las barras comunes son la única acción primaria. `Analizar historial` valida el detalle del año actual cuando está habilitado, el historial anual cuando se usa y la base salarial. Si todo queda coherente, ambas barras cambian a `Continuar a proyección`. Los botones internos previos se eliminan.

## 4. Historial anual

- se elimina `Completar cuotas vacías con 12`;
- se elimina `Generar / actualizar años`;
- el año final es el año calendario actual y se muestra dentro de `Período del historial`;
- cambiar el año inicial regenera la tabla;
- se añaden filtros **Todos** y **Pendientes**;
- una fila sin cuotas o salario se considera **Pendiente**;
- un año completamente vacío sigue representando información no disponible;
- la columna monetaria se denomina **Salario anual reportado**.

## 5. Datos importados de Mi Retiro Seguro

La procedencia se conserva por año/campo en `origen_campos_historial`. Cuotas o salario confirmados desde el comprobante quedan de solo lectura; un campo que el documento no aportó permanece editable. Desde Paso 3, **Revisar importación** muestra únicamente `Historial anual detectado (Paso 3)`.

## 6. Ficha Digital

La Ficha Digital adopta el mismo lenguaje y secuencia del importador principal:

`Seleccionar PDF → Analizar documento → Modo revisión → Editar campos (opcional) → Finalizar edición → Importar datos`.

Los meses/campos confirmados quedan marcados en `origen_campos_detalle_anio_actual` y no se editan directamente en la pantalla principal. Información ausente permanece disponible para captura manual. El enlace a Mi Caja Digital se concentra en este bloque.

## 7. Base salarial

Se conservan las cinco alternativas existentes: manual, último mes completo, promedio de meses completos del año actual, promedio de los últimos tres meses completos y promedio del salario acreditado por cuota.

En modo manual, salario y periodicidad son obligatorios. En modo automático, el monto es de solo lectura y la periodicidad es mensual. Se elimina el cuadro que explicaba internamente la conservación del origen.

## 8. Resumen y navegación

Al completar el paso se muestra un único resumen con:

- cuotas de referencia;
- cuotas identificadas;
- diferencia;
- total salarial reportado;
- base mensual seleccionada.

También se eliminan de todo el asistente los paneles `Próximo paso...`, porque el progreso, el selector y las barras ya proporcionan esa orientación.

## 9. Privacidad e integridad

UX.4.6d no introduce una nueva finalidad de tratamiento ni almacenamiento permanente. La Revisión 6 amplía los controles de conservación y eliminación local, por lo que actualiza el texto de privacidad a la versión **2026-08-15.1**. La Ficha Digital continúa limitada al año calendario actual. Desde Revisión 3, cada mes que el documento detecta con salario/estado utilizable se incorpora como registro confirmado, con la casilla de cuota marcada y bloqueada; los meses ausentes conservan captura manual.

## 10. Validación técnica de Revisión 1

- `python -m compileall app`: **OK**;
- `node --check app/static/js/*.js`: **OK**;
- `python -m unittest discover -s tests`: **273 pruebas en OK**;
- regresiones específicas de UX.4.6d: **20**.

## 11. Pendiente antes del cierre

La Revisión 2 debe ser validada visual y funcionalmente en PC/laptop. Se revisarán importación total/parcial/manual, Ficha Digital, filtros, campos bloqueados/pendientes, bases salariales, resumen unificado, navegación superior/inferior y los tres temas. La matriz manual de otros dispositivos continúa diferida para beta/RC.

## 12. Revisión 2 — coherencia entre Ficha Digital, cuotas y año actual

La revisión visual detectó una regresión funcional: al confirmar una Ficha Digital, el frontend reemplazaba `cuotas_anio_actual` del Paso 2 por la cantidad de casillas mensuales marcadas en la vista previa. Si el usuario importaba salarios pero no confirmaba cuotas por mes, el Paso 2 podía quedar en cero aunque Mi Retiro Seguro hubiera aportado, por ejemplo, cinco cuotas acreditadas. El historial anual conservaba esas cinco cuotas y aparecía una diferencia artificial.

R2 establece que:

- en R2 el Paso 2 conservaba el total acreditado como referencia inmutable; desde R23 una Ficha Digital confirmada puede ampliarlo cuando aporta más cuotas del año actual, sin permitir reducciones silenciosas;
- Ficha Digital no modifica ni elimina ese total;
- en R2 las casillas mensuales eran confirmables manualmente; este criterio queda sustituido por R3 para los meses efectivamente detectados por la Ficha Digital;
- si la cantidad mensual importada no coincide con Paso 2, se muestra una advertencia de coherencia sin redefinir el total agregado;
- el usuario puede mantener el detalle del año actual o usar un total anual manual;
- si el detalle se desactiva con una Ficha importada, la interfaz explica que esos salarios no se usarán;
- sin Ficha Digital siguen disponibles captura mensual y quincenal;
- un año actual con cuotas y salario pendiente se muestra vacío, no como `0.00`.

También se corrige la alineación vertical de `¿Deseas detallar el año actual?` y `Forma de captura`.

## 13. Validación técnica de Revisión 2

- `python -m compileall app`: **OK**;
- `node --check app/static/js/*.js`: **OK**;
- `python -m unittest discover -s tests`: **278 pruebas en OK**;
- se agregan cinco regresiones específicas para R2 y se actualiza la prueba histórica de importación de Ficha Digital.

La revisión visual en PC/laptop continúa pendiente antes del cierre de UX.4.6d.

## 14. Revisión 3 — casillas importadas y procedencia visual

R3 establece un contrato transversal para tablas del asistente:

- los meses detectados automáticamente en Ficha Digital se muestran con **Cuota acreditada** marcada y bloqueada;
- enero–mayo, por ejemplo, quedan protegidos cuando son registros importados, mientras junio–agosto permanecen manuales si el documento no los contiene;
- una fila con cualquier dato documental confirmado recibe una presentación visual diferenciada de una fila manual;
- el patrón se aplica al historial anual, detalle del año actual y vistas previas de importación, y queda disponible para Pasos 4–6 cuando exista una tabla equivalente;
- en Mi Retiro Seguro, la casilla que determina si una fila pertenece al historial real queda fijada por la clasificación `HISTORICO`; una fila proyectada no puede transformarse en histórica marcando/desmarcando una casilla;
- el total `cuotas_anio_actual` del Paso 2 sigue siendo la referencia agregada y Ficha Digital no lo reescribe.

La diferenciación visual no sustituye el bloqueo funcional: una fila importada usa además controles de solo lectura/deshabilitados donde corresponda.

## 15. Validación técnica de Revisión 3

- `python -m compileall app`: **OK**;
- `node --check app/static/js/*.js`: **OK**;
- `python -m unittest discover -s tests`: **282 pruebas en OK**;
- se actualizan regresiones históricas cuya expectativa de confirmación manual de cuotas quedó sustituida por la regla de importación automática aprobada en R3.


## 16. Revisión 4 — procedencia visual y casillas importadas

La procedencia documental deja de representarse con verde. Ese color se reserva para estados semánticos de éxito o completitud. Las filas con datos importados usan ahora una señal azul derivada de la paleta primaria, con fondo tenue y borde lateral, manteniendo el mismo significado en Claro, Oscuro y Alto contraste.

Toda casilla de cuota cuyo origen sea Ficha Digital confirmada se fuerza a `checked`, `disabled` y `data-imported-locked="true"`. De esta forma, una restauración de sesión o una diferencia de estilos del navegador no puede hacer que un dato documental confirmado parezca manual o sin seleccionar.

Las filas manuales conservan la superficie normal. El patrón `data-row-imported` / `data-row-manual` continúa siendo transversal para futuras tablas del asistente, pero no se añadirán casillas artificiales a tablas que no las necesiten.

## 17. Validación técnica de Revisión 4

- `python -m compileall app`: OK.
- `node --check app/static/js/*.js`: OK.
- `python -m unittest discover -s tests -v`: **286 pruebas, OK**.
- Validación visual PC/laptop: pendiente de repetición completa.

## 18. Revisión 5 — marca inequívoca de cuotas importadas

La Revisión 5 corrige el caso observado en el que una fila de Ficha Digital aparecía con procedencia importada y campos bloqueados, pero el checkbox **Cuota acreditada** se dibujaba sin gancho. Para evitar diferencias entre navegadores y sesiones creadas por revisiones anteriores:

- un mes importado con salario/estado utilizable fuerza `checked`, `aria-checked` y metadata `data-imported-locked`;
- la marca visual se pinta por procedencia documental y no depende del estilo nativo de un control deshabilitado;
- la lectura del detalle considera la metadata documental equivalente a una cuota seleccionada;
- los meses ausentes del PDF mantienen casillas manuales normales.

La matriz completa de UX.4.6d debe repetirse después de validar esta corrección puntual.

## 19. Validación técnica de Revisión 5

- `python -m compileall app`: **OK**.
- validación de sintaxis `node --check` para `app/static/js/*.js`: **OK**.
- `python -m unittest discover -s tests -q`: **290 pruebas, OK**.
- la validación visual y funcional completa en PC/laptop permanece pendiente antes del cierre de UX.4.6d.

## Revisión 6 — gestión de datos del asistente

Antes de repetir la matriz completa de pruebas se incorpora una función transversal solicitada durante la validación: **Opciones** en la barra superior con **Limpiar este paso** y **Reiniciar simulación**. La limpieza es dependiente del paso e invalida toda etapa posterior; el reinicio integral vuelve a Paso 1 y conserva tema/aceptación.

Fuentes/Privacidad añade **Borrar datos de esta aplicación en este navegador**, que elimina también la constancia local de aceptación y la preferencia visual. Como el alcance informado al usuario cambia materialmente, Términos/Privacidad se versionan como **2026-08-15.1** y se solicita nuevamente su aceptación.

La Revisión 6 permanece pendiente de validación manual en PC/laptop junto con la matriz completa del Paso 3 antes de cualquier commit.

## Revisión 7 — consulta de privacidad y cierre contextual

Durante la validación de R6 se confirmó limpieza por paso, reinicio integral y borrado local. Se observó que **Revisar términos de privacidad** navegaba a Paso 1 y provocaba un nuevo consentimiento; R7 corrige ese comportamiento con un modal global en modo consulta que permanece en Fuentes, no altera la aceptación vigente y puede cerrarse mediante `×`.

El mismo control `×` está disponible en el consentimiento inicial, pero allí cerrar sin aceptar equivale a no continuar y vuelve a Inicio. La navegación inferior permanece sin **Opciones**; la barra sticky superior es la única superficie para acciones destructivas. La validación completa de UX.4.6d continúa pendiente.
La Revisión 7 eleva la suite completa a **311 pruebas automatizadas en OK**. La aprobación visual/funcional completa de UX.4.6d continúa pendiente antes de los commits.

## Revisión 8 — estados progresivos, resumen local y tablas

Durante la matriz manual, las filas 2024/2025 conservaban el rótulo **Pendiente** aun después de completar cuotas y salario, aunque el filtro ya infería correctamente que no estaban pendientes. R8 unifica ambas lecturas mediante un solo evaluador de estado.

Estados visibles:

- **Pendiente:** cuotas y salario todavía vacíos;
- **Falta salario:** existe cantidad de cuotas pero falta el monto anual;
- **Faltan cuotas:** existe salario pero falta la cantidad de cuotas;
- **Revisar:** combinación introducida incoherente o fuera de rango;
- **Sin cotización:** cuotas 0 y salario 0;
- **Parcial:** entre 1 y 11 cuotas con salario válido;
- **Completo:** 12 cuotas con salario válido.

Al terminar el análisis histórico se muestra, dentro de la misma sección, un resumen con cuotas de referencia, cuotas identificadas, diferencia y total salarial. El resumen integral del Paso 3 se conserva para incorporar posteriormente la base mensual elegida.

El filtro de tablas cortas deja de mostrar scroll vertical cuando hay cuatro o menos filas visibles. Se retira además `scrollbar-gutter: stable` de los contenedores tabulares para no reservar una barra cuando no existe desbordamiento. El patrón `table-scroll-compact` queda disponible para tablas equivalentes actuales y futuras.

Todo `input[type=file]` hereda un tratamiento primario común para **Seleccionar archivo** en los tres temas. En la vista previa de Ficha Digital se elimina el texto inline bajo el estado del último mes que desplazaba esa celda; la misma orientación queda disponible como ayuda contextual/accesible sin romper la cuadrícula.

La matriz manual 1–19 queda parcialmente ejecutada. Antes de continuar con 20–30 se revalidarán específicamente 4, 5, 7, 8, 9, 13 y 18. Los cambios reservados de consentimiento desde Fuentes sin aceptación previa, tecla `Esc` y ejemplos genéricos se mantienen para la revisión posterior a la matriz.

Validación técnica R8: **317 pruebas automatizadas en OK**; compilación Python y sintaxis JavaScript correctas.

## Revisión 9 — reactividad definitiva, scroll corto y consentimiento contextual

La prueba manual de R8 confirmó que el evaluador de estados era correcto, pero los listeners instalados por fila no se reflejaban de forma fiable durante la edición de la tabla regenerada. R9 cambia a delegación de eventos sobre el `tbody`, de modo que escribir cuotas o salario —en cualquier orden— recalcula inmediatamente la fila y reaplica el filtro **Pendientes**. Una fila resuelta deja de aparecer en ese filtro sin cambiar manualmente de vista.

El modo compacto de tabla elimina completamente el carril vertical en escritorio cuando hay pocas filas visibles. En pantallas estrechas se conserva solo la capacidad de desplazamiento horizontal si la anchura lo requiere.

R9 incorpora además los refinamientos reservados: si Fuentes abre términos sin aceptación vigente, el mismo modal ofrece lectura/consentimiento y esa aceptación habilita posteriormente Simular; `Esc` usa el mismo comportamiento contextual que el cierre `×`; y los placeholders de identidad y montos de ejemplo se sustituyen por datos ficticios/genéricos.

La matriz 20–30 continúa pendiente después del retesteo de estos cambios.

## Revisión 10 — simetría transversal de tablas

Después de validar correctamente la reactividad de R9, R10 extiende el sistema visual de tablas sin modificar motores, fórmulas ni contratos previsionales:

- `Historial salarial anual` adopta la misma geometría redondeada que tarjetas y formularios;
- todas las tablas actuales de importación, detalle mensual, proyección, línea temporal, retiro, resultados y comparación usan `app-table-shell`;
- las tablas generadas dinámicamente reciben el mismo wrapper desde JavaScript;
- Claro, Oscuro y Alto contraste mantienen la misma estructura y ajustan únicamente superficie/borde/encabezado;
- la accesibilidad de scroll reconoce el nuevo contrato común;
- las mejoras funcionales anteriores se clasifican por semántica: procedencia documental es global donde exista importación; estados/filtro Pendientes son propios de tablas editables que realmente tengan un estado pendiente; casillas bloqueadas solo corresponden a valores booleanos importados.

La prueba integral de consentimiento desde Fuentes queda pendiente para el recorrido limpio de Pasos 1–3. Los puntos 20–30 de la matriz funcional de Paso 3 continúan pendientes después de verificar visualmente R10.

Validación técnica R10: **330 pruebas automatizadas en OK**, compilación Python y sintaxis JavaScript correctas.



## Revisión 11 — scrollbars contenidos y simetría de carga PDF

Después de validar la geometría común de R10, se detectó que el scrollbar nativo de tablas extensas todavía podía superponerse visualmente al radio derecho, especialmente por los botones/flechas superior e inferior de Chromium/Windows. R11 mantiene `app-table-shell` como contenedor desplazable pero personaliza su scrollbar: elimina esas flechas, usa track transparente con margen respecto de las esquinas y adapta el thumb a Claro, Oscuro y Alto contraste. Las tablas cortas conservan la eliminación reactiva del carril introducida previamente.

R11 también unifica la altura exterior de **Seleccionar archivo** y **Analizar documento** en los importadores de Mi Retiro Seguro y Ficha Digital. La regla queda disponible para cualquier importador PDF futuro.

La prueba de una tabla posterior/Comparador indicada en R10 continúa pendiente junto con el recorrido integral de consentimiento y los puntos 20–30.

Validación técnica R11: **335 pruebas automatizadas en OK**, compilación Python y sintaxis JavaScript correctas.

## Revisión 12 — scroll transversal, estado vacío y carga estable

La validación manual de R11 confirmó la mejora del thumb, pero mostró que algunas superficies seguían exhibiendo piezas nativas diferentes y que el radio grande de tabla competía visualmente con el carril. R12 extiende el scrollbar temático a términos, modales, página y otras superficies desplazables, manteniendo el scroll nativo. `app-table-shell` pasa a usar `--app-radius-md`, por debajo del radio de las tarjetas, para integrar mejor el desplazamiento sin perder simetría.

Cuando el filtro **Pendientes** llega a cero, Historial salarial anual ya no mantiene una cabecera vacía: el wrapper se oculta y aparece el estado `No hay años pendientes por completar.`. El patrón queda disponible para tablas filtrables futuras cuando semánticamente corresponda.

El botón **Seleccionar archivo** deja de cambiar por el hover sobre el nombre del archivo; conserva su tratamiento de paleta y solo responde visualmente al hover directo del botón. Comparador continúa utilizando `app-table-shell` y se incorpora una regresión que protege esa adopción transversal.

Validación técnica R12: **340 pruebas automatizadas en OK**, compilación Python y sintaxis JavaScript correctas. Permanecen pendientes la revisión visual de R12, los puntos 20–30 y el recorrido integral de consentimiento antes de cerrar UX.4.6d.


## Revisión 13 — selector de archivo estable y preparación del recorrido integral

La validación manual de R12 confirmó correctamente scrollbars temáticos en tablas, vistas previas y Términos/Privacidad; los tres temas; estado vacío de **Pendientes**; reaparición reactiva de filas incompletas; y geometría de Comparador. El único fallo persistente fue **Seleccionar archivo**, cuyo color aún podía cambiar al pasar el puntero por el nombre del archivo.

R13 refuerza el componente global de carga contra la cascada de Bootstrap/Chromium. El botón nativo conserva color, fondo y borde de la paleta de la aplicación en estado base, hover y focus; no se modifica procesamiento de PDFs, estado del wizard, fórmulas ni motores.

Validación técnica R13: **343 pruebas automatizadas en OK**. Antes del cierre se hará una prueba manual breve del selector y, a continuación, un recorrido limpio integral de Pasos 1–3 que absorberá los puntos 20–30 aún pendientes y validará funciones, cálculos, importaciones, errores, consentimiento, limpieza, temas y resúmenes.


## Revisión 14 — continuidad del Paso 1 durante el recorrido integral

La validación manual confirmó R13. Al comenzar el recorrido limpio desde Paso 1 se detectó una fricción previa a los cálculos: Sexo estaba en la sección previsional inferior y el campo condicional Apellido de casada aparecía en la identificación superior. R14 unifica la captura manual bajo **Información personal** y coloca Sexo inmediatamente antes de Apellido de casada.

El ajuste no cambia motores, fórmulas, payloads, procedencia documental ni parser de Mi Retiro Seguro. Se conservan los mismos IDs y `actualizarApellidoCasada()`; la vista previa automática mantiene su agrupación por destino porque la fricción afecta a la captura manual. La siguiente validación continuará desde este nuevo layout y después cubrirá todo Paso 1, Paso 2 y Paso 3.

Validación técnica R14: **346 pruebas automatizadas en OK** después de adaptar regresiones históricas y añadir protección específica de jerarquía/orden del formulario.

## Revisión 15 — campos bloqueados, documentos y limpieza de cuotas

El recorrido integral confirmó los 20 controles de Paso 1 manual/importado. Antes de continuar con Paso 2 se introducen tres ajustes transversales: controles no editables claramente diferenciados en los tres temas; copy de importación desacoplado de “PDF compatible” y reutilizable por Ficha Digital; y estado realmente vacío de Cotización futura después de limpiar Paso 2. Los motores, parsers y fórmulas no cambian. Validación técnica R15: **350 pruebas automatizadas en OK**, compilación Python y sintaxis JavaScript correctas.

La validación continúa con Paso 2 y, posteriormente, Paso 3 y la integración completa 1→3 antes de cerrar UX.4.6d y preparar los commits.

## Revisión 16 — jerarquía del Paso 3 y dependencia de cuotas

Durante el recorrido integral se observó un flujo innecesariamente regresivo: una sesión podía llegar a Paso 3 con `resumen_cuotas` invalidado y **Analizar historial** exigía volver a Paso 2 aunque los valores de cuotas siguieran disponibles. R16 añade un preflight que revalida esas cuotas de forma silenciosa cuando el formulario continúa completo. Si realmente falta información, Paso 3 no se pierde ni navega hacia atrás; presenta la dependencia y conserva la captura.

La restauración también se protege contra `paso_actual` obsoleto después de limpiezas/invalidationes. El asistente abre el último paso que todavía cumple sus prerrequisitos.

Visualmente, Ficha Digital deja de estar entre las grandes subsecciones del Paso 3. Se integra dentro de **Detalle salarial del año actual**, después de la elección de detalle/forma de captura y antes de la tabla mensual. El orden final queda **Historial salarial anual → Detalle salarial del año actual (Ficha Digital + detalle mensual/quincenal) → Base salarial para proyección → Resumen**.

R16 no modifica motores, fórmulas ni parser; solo orquestación, restauración y estructura de interfaz. Validación técnica: **356 pruebas automatizadas en OK** antes de la comprobación manual.


## Revisión 17 — auditoría documental Paso 1–3

La auditoría con el comprobante real confirmó que Paso 2 utiliza correctamente 281 cuotas acreditadas aunque el documento muestre 293 acumuladas al sumar una fila proyectada de 2027. Asimismo, el historial anual 1992–2026 conserva 281 cuotas y sustituye el monto híbrido/proyectado de 2026 por el salario acreditado derivado de Ficha Digital cuando el detalle mensual coincide.

Se corrigió una anomalía puramente visual heredada de R5: `data-imported-locked` forzaba el gancho de cualquier checkbox bloqueado. Esto hacía parecer seleccionadas las filas `HISTORICO_PROYECTADO` y `PROYECTADO` en la vista previa, aunque la lógica ya las excluía. R17 fuerza el gancho únicamente si `checked=true`.

También se añade trazabilidad de edición, contexto de cuotas proyectadas, advertencia no bloqueante para historial anterior a la fecha de ingreso CSS indicada y una explicación precisa cuando el detalle mensual contiene más cuotas marcadas que Paso 2.

## Revisión 18 — procedencia transversal y continuidad tras recarga

La auditoría manual confirmó que un salario conocido —por ejemplo junio— puede existir sin que la cuota correspondiente deba considerarse acreditada todavía. R18 mantiene esa separación y añade trazabilidad visible para diferenciar **Detectado**, **Editado por ti**, **Completado manualmente** y **No detectado**. En el detalle mensual, un período manual con salario/estado pasa a Completado manualmente; un mes vacío permanece No detectado. Ficha Digital identifica registros detectados y aquellos realmente editados durante la revisión.

R18 también corrige la percepción de que una importación “se pierde” tras F5. El `input[type=file]` se vacía inevitablemente por seguridad del navegador, pero la simulación conserva los datos confirmados, la metadata del nombre del documento y las acciones Revisar/Quitar importación. El usuario no necesita adjuntar otra vez el archivo para continuar usando esos datos. No se conservan bytes ni rutas locales.


## Revisión 19 — sincronización reactiva del año actual

La validación manual confirmó un caso real: Mi Retiro Seguro/Ficha Digital podía contener cinco cuotas hasta mayo, mientras el usuario ya conocía y confirmaba junio. El detalle mensual calculaba correctamente seis registros, pero la fila 2026 del historial anual continuaba con el valor anterior o exigía completar de nuevo el salario anual.

R19 elimina esa doble captura. Con detalle activo, la fila 2026 deriva sus cuotas de las casillas acreditadas y el salario anual de esos mismos meses. Para el caso enero–junio `1,486.88 + 1,555.51 + 1,381.01 + 1,565.83 + 1,331.90 + 1,562.37`, la fila muestra **6 cuotas, B/.8,883.50 y Parcial**.

Marcar junio manualmente también actualiza Paso 2 desde 5/281 a 6/282 conservando las 276 cuotas anteriores al año actual. La acción es explícita porque la propia casilla significa “Cuota acreditada”; el cambio se registra como edición del usuario y los resúmenes se revalidan sin retroceder de pantalla. Si julio/agosto se confirman más adelante, el mismo mecanismo incrementa el conteo y total anual automáticamente.

El promedio por cuota acreditada del caso de seis meses pasa a **B/.1,480.58**; el valor B/.1,464.23 correspondía únicamente al escenario anterior de cinco cuotas enero–mayo.


## Revisión 20 — vigencia de Ficha Digital y resumen visible

El recorrido final confirmó que una Ficha Digital puede ser válida para completar el Paso 3 aunque no sea la más reciente disponible. R20 evita tratar ambas ideas como equivalentes. La aplicación compara el último período salarial detectado con el mes local actual; el mes actual y los dos anteriores se consideran suficientemente recientes para no interrumpir el flujo. Un documento más antiguo muestra una advertencia previa a la vista de revisión con dos acciones explícitas: **Seleccionar una ficha más reciente** o **Continuar con esta ficha**. La segunda opción conserva toda la capacidad de completar manualmente meses faltantes.

La decisión no añade persistencia del archivo. Tras confirmar, `anio_mas_reciente`/`mes_mas_reciente` ya existentes permiten mostrar **Último período detectado** junto a **Importación vigente**, incluso después de F5.

R20 también hace visible el resumen del detalle del año actual que hasta R19 solo alimentaba internamente las bases automáticas. El nuevo bloque muestra cuotas identificadas, salarios disponible/acreditado, meses con información/completos, último mes completo, último mes con cuota, último salario completo y los tres promedios. Las cifras siguen procediendo del servicio backend; la UI únicamente las presenta y las oculta al invalidar el detalle.

Validación técnica R20: **379 pruebas automatizadas en OK**, `python -m compileall app` y `node --check app/static/js/*.js` correctos.


## Revisión 21 — vigencia mensual con fecha externa verificable

La prueba manual de R20 mostró que una ficha de mayo advertía en agosto, pero una de junio no, porque R20 toleraba hasta dos meses y usaba `new Date()` en el cliente. R21 elimina ambas condiciones: cualquier período anterior al mes actual verificado requiere decisión y la referencia temporal procede del backend, que intenta obtener el encabezado de fecha de infraestructura oficial de la CSS por HTTPS. Si no puede verificarla, la UX entra en `FECHA_NO_VERIFICADA` y pide revisar/continuar; nunca declara la ficha reciente por un reloj local no confiable.

La importación persistida revalida la referencia después de F5. El parser también deja de usar `date.today()` como criterio implícito y, sin un año explícito, extrae el año más reciente presente en el documento. R21 actualiza la privacidad a **2026-08-16.1** por la nueva consulta de red, sin enviar información de la simulación.

## Revisión 22 — cierre sin bloqueos silenciosos

La prueba final detectó que **Analizar historial** podía regresar visualmente al detalle del año actual sin explicar el motivo. R22 hace la reconciliación de cuotas manuales justo antes de validar el payload y revalida Paso 2 en segundo plano cuando esa reconciliación cambia la referencia. Esto protege restauraciones/F5 y cualquier caso donde el evento de la casilla no haya persistido el ajuste antes de pulsar la acción principal.

Si aun así existe una diferencia real, el detalle muestra un error explícito con las cuotas identificadas y las registradas en Paso 2; el scroll solo dirige al mensaje.

Se revisó el bloque **Resumen del detalle del año actual**. Se mantienen sus 11 métricas: salario disponible y acreditado divergen cuando existe salario aún no acreditado; meses con información y completos divergen con períodos parciales; último mes completo y último mes con cuota pueden diferir; y los tres promedios corresponden a las tres bases automáticas ofrecidas al usuario. Por ello no se considera redundancia removible.

Validación técnica R22: **392 pruebas automatizadas en OK**, compilación Python y validación sintáctica JavaScript correctas.


## Revisión 23 — una Ficha Digital posterior puede actualizar Paso 2

La validación con una Ficha Digital más reciente reveló que R22 solo reconciliaba casillas manuales. Cuando los seis meses confirmados procedían del documento y por tanto estaban bloqueados, `detallePuedeReconciliarCuotasPaso2()` descartaba esas casillas y Paso 2 permanecía en cinco cuotas, provocando exactamente el error `6 vs 5`.

R23 distingue precedencia temporal y procedencia: una Ficha Digital confirmada que aporta **más cuotas** que Paso 2 amplía automáticamente la referencia del año actual, conserva las cuotas anteriores al año vigente y revalida Cuotas en segundo plano. Si una ficha aporta menos meses, no se reduce la referencia superior de Paso 2. La reconciliación se ejecuta tanto al confirmar la ficha como defensivamente al analizar el detalle, y actualiza también `detalle_anio_actual.cuotas_anio_actual_referencia` para persistencia/F5.
