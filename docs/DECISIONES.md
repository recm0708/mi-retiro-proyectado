# Registro de decisiones técnicas

Este documento registra decisiones de arquitectura, modelado, precisión y aplicación normativa. La numeración ADR es única y consecutiva; no se reutilizan identificadores.

- [Índice de documentación](INDICE.md)
- [Normativa implementada](NORMATIVA.md)
- [Fuentes normativas oficiales](FUENTES_NORMATIVAS.md)

Cuando una decisión interpreta una superposición, ambigüedad o limitación de datos, debe leerse junto con la fuente oficial correspondiente y no como una norma autónoma.

---

## ADR-001 — Aplicación web local

**Estado:** Aceptada

La aplicación se desarrollará inicialmente como una aplicación web ejecutada en localhost.

Esto permitirá utilizar la misma arquitectura posteriormente en un servidor web sin reconstruir el motor de cálculo.

---

## ADR-002 — FastAPI como backend

**Estado:** Aceptada

Se utilizará Python con FastAPI para la lógica del servidor y la exposición de los servicios internos de la aplicación.

---

## ADR-003 — Separación del motor de cálculo

**Estado:** Aceptada

Los cálculos previsionales serán independientes de la interfaz gráfica.

Existirán motores separados para:

- SEBD;
- Subsistema Mixto;
- SUCGS.

---

## ADR-004 — Normativa separada del código

**Estado:** Aceptada

Los parámetros legales que puedan modificarse no deberán quedar dispersos o codificados directamente dentro de los algoritmos.

Se mantendrán archivos de configuración versionados en el directorio `normativa/`.

---

## ADR-005 — Fechas reales

**Estado:** Aceptada

Los cálculos utilizarán fechas completas y no únicamente la diferencia entre años calendario.

Esto es necesario para determinar correctamente:

- edad cumplida;
- fecha de referencia;
- cuotas anteriores a la edad de referencia;
- cuotas posteriores a la edad de referencia.

---

## ADR-006 — Historial y proyección separados

**Estado:** Aceptada

La aplicación diferenciará permanentemente:

- datos históricos reales;
- datos proyectados.

Una proyección futura nunca deberá modificar o reemplazar silenciosamente información histórica.

---

## ADR-007 — GitHub como repositorio principal

**Estado:** Aceptada

GitHub será la fuente principal del proyecto.

Esto permitirá desarrollar indistintamente desde diferentes computadoras utilizando `git pull` y `git push`.
---

## ADR-008 — Estado temporal del asistente en `sessionStorage`

**Estado:** Aceptada

Durante la primera etapa del proyecto, los datos de una simulación en curso se conservarán temporalmente en `sessionStorage`.

Esto permite mantener la información al recargar la pestaña sin guardar automáticamente datos personales en una base de datos. Una futura persistencia permanente deberá ser una acción explícita del Asegurado(a).

---

## ADR-009 — API como frontera entre interfaz y cálculos

**Estado:** Aceptada

La interfaz JavaScript no implementará las fórmulas principales de cuotas, salarios o pensiones.

Los formularios enviarán datos a endpoints de FastAPI y Python será responsable de las validaciones y cálculos de negocio. JavaScript se limitará principalmente a navegación, estado temporal, presentación y comunicación con la API.

---

## ADR-010 — Normalización salarial mediante valor anual común

**Estado:** Aceptada

Los salarios ingresados como semanales, quincenales, mensuales o anuales se normalizan primero a un equivalente anual.

A partir de ese valor se obtienen las demás periodicidades, reduciendo conversiones encadenadas y manteniendo un criterio uniforme.

---

## ADR-011 — Proyecciones salariales por escenarios

**Estado:** Aceptada

El Paso 4 permitirá cuatro modalidades iniciales:

- salario constante;
- porcentaje anual;
- salario futuro conocido;
- comparación de varios porcentajes.

Las proyecciones son datos estimados y permanecerán diferenciadas de los datos salariales históricos.

---

## ADR-012 — Proyección anual no sustituye cálculos por fecha exacta

**Estado:** Aceptada

Las tablas salariales del Paso 4 utilizan años calendario para facilitar la planificación y comparación visual.

Estas tablas no se utilizarán por sí solas para decidir si una cuota o salario ocurrió antes o después de una fecha legal crítica. Los motores de elegibilidad y pensión utilizarán fechas y meses exactos cuando corresponda.
---

## ADR-013 — Historial anual separado del salario actual

**Estado:** Aceptada

El Paso 3 distinguirá explícitamente el historial salarial real de la remuneración actual utilizada para proyectar el futuro.

El historial anual almacenará cuotas y salario cotizado/reportado por año calendario. El salario actual conservará su periodicidad original y se normalizará para las proyecciones. Esta separación evita tratar un año parcial como si fuera un salario anual completo y mantiene trazabilidad entre datos reales y supuestos futuros.

---

## ADR-014 — Línea temporal única con separación entre realidad y proyección

**Estado:** Aceptada

El Paso 4 presentará el historial real una sola vez y separará explícitamente:

- años históricos;
- año actual con componentes real y proyectado;
- años completamente proyectados.

Cuando existan varios escenarios salariales, solo la parte futura se repetirá por escenario. Esto evita duplicar décadas de información histórica y reduce el riesgo de confundir datos reales con estimaciones.

---

## ADR-015 — Salario cotizado futuro proporcional a las cuotas proyectadas

**Estado:** Aceptada

Si un año futuro contiene menos de 12 cuotas proyectadas, el salario cotizado estimado no utilizará el salario anual completo. Se calculará a partir del salario mensual del escenario multiplicado por la cantidad de cuotas/meses proyectados.

Esta equivalencia anual es provisional y será refinada con detalle mensual cuando los motores de elegibilidad y pensión lo requieran.

---

## ADR-016 — Precisión monetaria con `Decimal` y redondeo al materializar

**Estado:** Aceptada

Los cálculos monetarios sensibles utilizarán `Decimal` para evitar artefactos binarios de punto flotante.

El criterio técnico general será conservar precisión durante las operaciones y redondear a centavos con `ROUND_HALF_UP` al materializar un importe. No se redondearán valores intermedios únicamente para forzar coincidencia con otra cifra visible.

Si una norma aplicable establece un método de redondeo distinto, esa regla normativa tendrá prioridad dentro del motor correspondiente.

---

## ADR-017 — El cierre del año actual precede a la densidad futura

**Estado:** Aceptada

La proyección de cuotas del Paso 5 respetará primero `cuotas_esperadas_cierre_anio` del Paso 2.

La densidad `cuotas_esperadas_por_anio` se utilizará para los años futuros y, cuando sea necesario, se prorrateará el año de retiro. Esto evita agregar cuotas en el año actual cuando el Asegurado(a) ya indicó que no espera nuevas acreditaciones antes de cerrarlo.

---

## ADR-018 — El horizonte salarial debe cubrir el escenario de retiro

**Estado:** Aceptada

Un escenario de retiro no se considerará completamente cubierto si su fecha se extiende más allá del último año de la proyección salarial.

La aplicación advertirá la inconsistencia y ofrecerá volver al Paso 4 para extender el horizonte. No se extrapolarán silenciosamente salarios sin confirmación del Asegurado(a).

---

## ADR-019 — Navegación rápida `sticky` sin duplicar lógica de negocio

**Estado:** Aceptada

Los pasos largos del asistente dispondrán de una barra de navegación rápida visible al desplazarse.

La barra delegará sus acciones en los formularios y botones existentes. No contendrá fórmulas ni validaciones previsionales paralelas, evitando duplicar lógica y manteniendo accesibles las acciones Anterior/Continuar/Analizar.

## ADR-020 — Clasificar explícitamente cuotas excedentes por edad de referencia

**Estado:** Aceptada

**Decisión:** el motor SEBD no inferirá silenciosamente, para retiros posteriores a la edad de referencia, qué cuotas excedentes corresponden al incremento de 1.25 % y cuáles al incremento de 2 %.

**Motivo:** la ley asigna porcentajes diferentes según el momento en que fueron aportadas. Cuando el historial anual no ofrece granularidad suficiente, el dato debe ser proporcionado o derivado por una capa con mejor detalle antes de ejecutar el cálculo definitivo.

---

## ADR-021 — Selección explícita del escenario que alimenta el Paso 6

**Estado:** Aceptada

El Paso 5 no enviará implícitamente el primer escenario disponible al cálculo de pensión. La persona debe disponer de una selección visible del escenario futuro que se utilizará en Resultados.

Los escenarios ya transcurridos permanecen visibles para comparación, pero no se seleccionan automáticamente mientras el proyecto solo disponga de historial anual. Reconstruir cuotas exactas en una fecha pasada requiere mayor granularidad.

---

## ADR-022 — Capa de integración entre el asistente y los motores legales

**Estado:** Aceptada

La transformación de historial real, salarios proyectados y cuotas estimadas en una entrada para el motor legal se realizará en Python mediante `app/servicios/resultados.py`.

JavaScript enviará el estado validado y presentará la respuesta, pero no decidirá fórmulas legales ni repartirá silenciosamente cuotas excedentes.

Cuando un año futuro solo se utiliza parcialmente hasta la fecha de retiro, el salario proyectado se prorrateará por las cuotas consumidas y se mostrará una advertencia de que se trata de una estimación.


## ADR-023 — Clasificación automática de modalidad SEBD

**Estado:** Aceptada

**Decisión:** el Asegurado(a) selecciona una fecha/escenario de retiro y la aplicación determina automáticamente si corresponde Normal, Anticipada, Proporcional, Proporcional Anticipada, posible Indemnización por Vejez o un escenario no elegible.

**Motivo:** evita que el Asegurado(a) tenga que conocer de antemano la denominación jurídica correcta y reduce inconsistencias entre edad, cuotas y modalidad seleccionada manualmente.

## ADR-024 — Años calendario parciales dentro de los mejores años

**Estado:** Aceptada

**Decisión:** no anualizar un año parcial. Se conserva su total cotizado y puede competir entre los mejores años por su total anual. Cuando se seleccionan diez años, la suma se lleva a promedio mensual sobre 120 meses.

**Motivo:** mantener el tratamiento del procedimiento reglamentario y evitar inventar salarios no cotizados.

## ADR-025 — Factores anticipados versionados por mes

**Estado:** Aceptada

**Decisión:** los factores de reducción de la banda anticipada se almacenan como parámetros normativos y no se interpolan en el motor.

**Motivo:** un factor reglamentario debe reproducirse desde una tabla versionada, no deducirse por aproximación matemática.


## ADR-026 — Indemnización por Vejez como pago único separado

**Estado:** Aceptada

La Indemnización por Vejez no se almacenará ni presentará como `pension_mensual_estimada`. El motor conservará por separado la mensualidad normal hipotética, el divisor reglamentario, el factor `meses cotizados / 6` y el pago único resultante.

El cociente entre meses acreditados y seis se calculará mediante división decimal directa, sin truncarlo a bloques enteros, porque el procedimiento reglamentario ordena dividir el total de meses registrados entre seis y multiplicar el resultado por la mensualidad hipotética.

Desde el 01/03/2036 el clasificador no calculará esta indemnización y derivará el escenario a la transición SUCGS prevista por el artículo 186.


## ADR-027 — No reconstruir el saldo CAP desde historial anual

**Estado:** Aceptada

El Componente de Ahorro Personal del Subsistema Mixto no se estimará acumulando porcentajes sobre el historial anual mientras no exista una regla versionada que permita reproducir la cuenta individual con sus movimientos y rendimientos.

Para calcular la pensión programada se exigirá el saldo ahorrado/capitalizado oficial o validado y el valor actuarial aplicable. Si el parámetro actuarial no está disponible, el motor mostrará el componente como pendiente en lugar de reutilizar factores del SUCGS.

**Motivo:** el CAP depende del saldo efectivo de la cuenta, su capitalización y parámetros actuariales adoptados periódicamente. Reconstruirlo con datos anuales produciría una precisión aparente no auditable.

---

## ADR-028 — Reutilizar clasificación SEBD en el componente BD del Mixto

**Estado:** Aceptada

El Componente de Beneficio Definido del Subsistema Mixto reutilizará el clasificador general de modalidades de retiro por vejez, pero con un historial salarial limitado a la participación propia del Mixto y con el máximo mensual específico del componente.

**Motivo:** las modalidades legales comparten estructura de edad/cuotas, mientras el salario participante y los límites monetarios del Mixto son distintos. Reutilizar el clasificador reduce duplicación sin confundir parámetros.

---

## ADR-029 — Frontera operativa del Mixto en 01/03/2032

**Estado:** Aceptada con discrepancia normativa documentada

Para determinar si un retiro continúa calculándose bajo el Subsistema Mixto, la aplicación utilizará 01/03/2032 como inicio de la transición a SUCGS, conforme al artículo 188 y al Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria.

El artículo 153 del Texto Único contiene una referencia a 01/03/2036 para asegurados del Subsistema Mixto. La aplicación no oculta ni corrige silenciosamente esa diferencia: la conserva en `normativa/mixto.json` y en `docs/NORMATIVA.md`.

**Motivo:** la lógica operativa del retiro debe seguir la disposición específica de cálculo y el reglamento aplicable, dejando trazabilidad de la inconsistencia textual para revisión jurídica futura.

---

## ADR-030 — La opción del CAP no se decide automáticamente

**Estado:** Aceptada

Cuando el artículo 187 habilite la devolución total del Componente de Ahorro Personal, el motor no escogerá silenciosamente entre pensión programada y devolución total.

La entrada `opcion_prestacion_cap` admite `AUTO`, `PENSION_PROGRAMADA` y `DEVOLUCION_TOTAL`. En `AUTO`, si ambas vías requieren una decisión del asegurado, el resultado quedará pendiente hasta que exista una selección expresa.

**Motivo:** la devolución es una facultad del asegurado y cambia la naturaleza del resultado entre renta mensual y pago único.

---

## ADR-031 — La garantía de renta vitalicia no incrementa la pensión inicial

**Estado:** Aceptada

La garantía del artículo 184 se modelará como continuidad futura del pago del CAP cuando el pensionado sobreviva la expectativa de vida utilizada y se extingan los fondos de su cuenta.

No se sumará un complemento a la pensión inicial. La salida conservará la pensión CAP programada, la condición de activación y la referencia al Seguro Colectivo de Renta Vitalicia.

**Motivo:** el seguro cubre el agotamiento posterior del capital; no constituye un aumento inicial de la prestación.

---

## ADR-032 — El bono de reconocimiento requiere un monto oficial o validado

**Estado:** Aceptada

La aplicación no reconstruirá automáticamente el bono de reconocimiento del artículo 183 a partir del historial anual. Aceptará un monto ya determinado y registrará si fue confirmado oficialmente.

Un bono mayor que cero que no esté marcado como confirmado permitirá mostrar un resultado provisional, pero impedirá considerar el cálculo Mixto como completo.

**Motivo:** la Ley define el derecho y la naturaleza del bono, pero la aplicación no dispone todavía de granularidad y reglas reglamentarias suficientes para reconstruir su valor individual con garantías de exactitud.

---

## ADR-033 — Pagos únicos y pensiones mensuales permanecen separados

**Estado:** Aceptada

Las indemnizaciones del componente BD y las devoluciones del CAP se almacenarán como pagos únicos independientes de `pension_mensual_total_estimada`.

Cuando ambos pagos únicos procedan, el motor podrá presentar un total de pagos únicos, pero nunca convertirlo en una pensión mensual.

**Motivo:** evita mezclar prestaciones de naturaleza y periodicidad diferentes en la API, la interfaz y futuros informes.

## ADR-034 — La interfaz Mixto consume el motor integrado y no replica fórmulas

**Estado:** Aceptada

El Paso 6 no implementará fórmulas previsionales Mixto en JavaScript. La interfaz recopila los datos explícitos del CAP y los datos ya validados del asistente, y los envía a `POST /api/simulacion/resultados/mixto`.

La clasificación de modalidad, la decisión pendiente, la pensión programada, las devoluciones, las indemnizaciones y la garantía provienen exclusivamente del backend.

**Motivo:** evita divergencia entre la API y la interfaz y conserva una única fuente de verdad para el cálculo legal.

---

## ADR-035 — Navegación directa condicionada entre pasos del asistente

**Estado:** Aceptada

Los indicadores de progreso y la barra persistente permitirán abrir directamente un paso anterior o posterior que siga teniendo satisfechos sus prerrequisitos. Los pasos no disponibles permanecerán deshabilitados hasta que se completen nuevamente los datos dependientes.

El salto directo reutiliza las funciones existentes de preparación de Historial, Proyección, Retiro y Resultados; no duplica validaciones ni reglas de cálculo.

**Motivo:** permite corregir o revisar datos sin presionar repetidamente `Anterior`, pero evita saltar a resultados que hayan quedado inválidos después de modificar información de origen.

## ADR-036 — Separar saldo SUCGS y garantías

**Estado:** Aceptada

**Decisión:** el SUCGS calcula el componente contributivo a partir de un saldo explícito y no reconstruye todavía ese saldo desde el historial anual. La pensión contributiva, la capa solidaria de los artículos 194 y 195 y la pensión total definitiva se mantienen como niveles separados.

**Motivo:** la reconstrucción del saldo depende del origen previsional del asegurado, aportes previos y posteriores a la reforma y rendimientos efectivos del Fondo Único Solidario. Además, el artículo 197 puede elevar el resultado después de la capa solidaria, por lo que no debe confundirse un resultado intermedio con la pensión definitiva.

## ADR-037 — Versionar referencias solidarias y permitir valores vigentes

**Estado:** Aceptada

**Decisión:** B/.144.00 y B/.265.00 se conservan en `normativa/sucgs.json` como referencias legales al 22/05/2025. El motor permite suministrar valores vigentes confirmados y advierte cuando utiliza las referencias base.

**Motivo:** el artículo 194 somete sus prestaciones a indexación y el artículo 195 establece la Pensión Garantizada Solidaria como un monto de al menos B/.265.00. Tratar esos importes como eternamente fijos produciría resultados desactualizados.

## ADR-038 — Prioridad del artículo 195 en el límite exacto de 240 cuotas

**Estado:** Aceptada

**Decisión:** cuando existen exactamente 240 cuotas y se cumple la edad de referencia, el motor aplica la Pensión Garantizada Solidaria del artículo 195 antes de la regla del numeral 2 del artículo 194.

**Motivo:** el numeral 2 del artículo 194 incluye literalmente hasta 240 cuotas, mientras el artículo 195 concede la Pensión Garantizada Solidaria desde 240 cuotas. La aplicación documenta esta superposición y usa el artículo 195 como regla específica de la garantía mínima, sin ocultar la interpretación adoptada.

## ADR-039 — Preevaluación conservadora del artículo 197

**Estado:** Aceptada

**Decisión:** automatizar las condiciones de número anual de cuotas y distribución temporal con historial anual completo; calcular el salario promedio base como salarios cotizados dividido entre meses cotizados; y exigir confirmación explícita para la estabilidad salarial.

**Motivo:** el artículo 197 formula de manera directa las dos primeras condiciones, mientras el numeral 3 contiene una redacción sobre variación del 30 % cuya aplicación operativa no debe ser corregida ni reinterpretada silenciosamente por la aplicación. La propia Ley dispone que la CSS implemente mecanismos de control. Hasta contar con una regla operativa oficial inequívoca, la confirmación de estabilidad permanece separada y auditable.

**Consecuencia:** `pension_mensual_total_estimada` solo se completa cuando la garantía puede determinarse o cuando una condición comprobada demuestra que no aplica.

## ADR-040 — Integrar SUCGS al Paso 6 sin duplicar fórmulas

**Estado:** Aceptada

**Decisión:** la interfaz SUCGS reutilizará los Pasos 1–5 y enviará al backend el historial, la línea temporal y el escenario de retiro seleccionados. JavaScript no implementará la fórmula del artículo 196 ni las garantías de los artículos 194, 195 y 197.

El año inicial usado para distribuir cuotas en el artículo 197 se tomará del inicio del historial declarado en el Paso 3. La confirmación de que ese historial cubre toda la vida laboral relevante permanecerá como una declaración explícita, y la estabilidad salarial conservará un estado pendiente cuando no exista confirmación suficiente.


## ADR-041 — El comparador coordina motores y no recalcula fórmulas

**Estado:** Aceptada

**Decisión:** la comparación transversal de 6F.1 construirá combinaciones de fecha de retiro y escenario salarial y delegará cada cálculo al servicio integrado SEBD, Mixto o SUCGS. La capa transversal solo normaliza resultados y calcula diferencias contra una combinación base.

Para Mixto y SUCGS, cuando se evalúe una fecha alternativa se reutilizarán explícitamente los saldos y parámetros específicos ingresados en el Paso 6 y se mostrará una advertencia de escenario hipotético con saldo constante. No se proyectarán silenciosamente cuentas CAP o de Capitalización Solidaria.

**Motivo:** evita una cuarta implementación de fórmulas previsionales y, al mismo tiempo, impide presentar como proyección actuarial un saldo futuro que la aplicación todavía no puede reconstruir con datos oficiales suficientes.


## ADR-042 — La trazabilidad explica resultados y no recalcula prestaciones

**Estado:** Aceptada

**Decisión:** `Ver cálculo completo` se construye en backend a partir del resultado ya emitido por cada motor. La capa transversal puede presentar datos, reglas, fórmulas, sustituciones, redondeos y fuentes, pero no vuelve a ejecutar ni replica la lógica jurídica del motor.

Los enlaces oficiales provienen de `normativa/*.json`; JavaScript solo renderiza la estructura recibida.

**Motivo:** evita inconsistencias entre la cifra mostrada y su explicación, permite reutilizar una misma estructura en SEBD, Mixto y SUCGS y permite reutilizar la metodología y los futuros informes sin crear una cuarta implementación de las fórmulas previsionales.

## ADR-043 — Las fuentes visibles usan nombres humanos y metadatos versionados

**Estado:** Aceptada

**Decisión:** los identificadores internos como `texto_unico`, `ley_462` o `reglamento_cccs` no se mostrarán literalmente al Asegurado(a). La interfaz resolverá cada identificador contra el catálogo de fuentes recibido del backend y presentará el título humano y, cuando exista, un enlace oficial.

La página `/metodologia` reutiliza las URLs versionadas de `normativa/*.json` y las agrupa por SEBD, Mixto y SUCGS. La capa de presentación puede añadir etiquetas y alcance, pero no sustituye la fuente normativa ni introduce reglas de cálculo.

**Motivo:** los IDs internos son adecuados para integrar servicios, pero no son una referencia jurídica legible. Mantener títulos humanos y enlaces oficiales mejora la auditabilidad sin duplicar URLs ni fórmulas en JavaScript.

## ADR-044 — Contrato transversal común para el resultado final

**Estado:** Aceptada

**Decisión:** los resultados integrados de SEBD, Mixto y SUCGS expondrán un `resumen_unificado` con la misma semántica para estado, naturaleza de la prestación, monto mensual, pago único, modalidad, escenario, datos no confirmados y advertencias.

El resumen transversal se construye después de ejecutar el motor y la trazabilidad. No recalcula importes ni sustituye `calculo`, que continúa siendo el desglose jurídico específico de cada sistema. El comparador debe consumir este contrato común cuando normalice filas.

**Motivo:** evita que la interfaz, el comparador y futuros informes mantengan tres interpretaciones distintas de conceptos equivalentes. También garantiza que una indemnización o devolución no pueda confundirse con una pensión mensual y que los estados pendientes o de transición conserven una interpretación homogénea.

## ADR-045 — Adoptar una identidad de producto independiente

**Estado:** Aceptada

**Decisión:** la aplicación se denomina **Mi Retiro Proyectado** en la interfaz, documentación y metadatos públicos.

**Motivo:** `Mi Retiro Seguro` es el nombre de una herramienta oficial de la CSS. Usar ese nombre con un sufijo como `v2` podría sugerir una versión oficial, sucesora o afiliada. El nombre adoptado mantiene el propósito previsional sin crear esa apariencia.

## ADR-046 — Denominar Asegurado(a) al público de la aplicación

**Estado:** Aceptada

**Decisión:** los textos visibles y la documentación funcional utilizan **Asegurado(a)** en singular y **Asegurados(as)** en plural para referirse a quienes realizan simulaciones.

**Motivo:** alinea la terminología con el dominio de seguridad social y evita usar `usuario` como denominación pública genérica.

## ADR-047 — Unificar la escala tipográfica visible

**Estado:** Aceptada

**Decisión:** párrafos, ayudas, controles, tablas y navegación comparten un tamaño base. Solo encabezados, valores previsionales relevantes y elementos compactos de estado pueden apartarse de esa escala.

**Motivo:** reduce variaciones arbitrarias de tamaño, mejora consistencia y conserva énfasis para montos y resultados que requieren atención.

## ADR-048 — Separar información del Asegurado(a) y documentación interna

**Estado:** Aceptada

**Decisión:** la interfaz no muestra nombres de subfases, rutas del repositorio, ADR, archivos `docs/*.md` ni identificadores técnicos. Esos elementos permanecen en la documentación de desarrollo.

**Motivo:** el Asegurado(a) necesita metodología, fuentes y resultados, no detalles de organización interna del proyecto.

## ADR-049 — Preferencia visual local e independiente de la simulación

**Estado:** Aceptada

**Decisión:** la aplicación ofrece los modos **Seguir sistema**, **Claro**, **Oscuro** y **Alto contraste**. La preferencia se conserva en `localStorage` con una clave propia y no forma parte del objeto previsional ni del estado de cálculo almacenado en `sessionStorage`.

**Motivo:** la apariencia es una preferencia del navegador, no un dato de la prestación. Separarla evita contaminar simulaciones y permite respetar la configuración del sistema operativo cuando el Asegurado(a) así lo elige.

## ADR-050 — Accesibilidad base transversal en la plantilla global

**Estado:** Aceptada

**Decisión:** la plantilla global incorpora enlace de salto al contenido, `aria-current` para navegación activa, foco visible, objetivos táctiles principales de al menos 44 px y respeto a `prefers-reduced-motion`. Las mejoras se aplican de forma transversal y no se duplican en cada pantalla.

**Motivo:** estas medidas reducen barreras de teclado, movilidad y sensibilidad al movimiento y constituyen una base verificable para la revisión WCAG 2.2 posterior.

## ADR-051 — Pie de página compacto como información legal global

**Estado:** Aceptada

**Decisión:** el pie de página utiliza dos líneas compactas: la primera concentra nombre, copyright, autor y reserva de derechos; la segunda concentra el aviso de independencia y el acceso a Mi Caja Digital. Se evita presentarlo como una tarjeta o bloque separado.

**Motivo:** el contenido legal debe estar siempre disponible sin competir visualmente con los resultados previsionales ni aumentar innecesariamente la altura de cada página.

## ADR-052 — Usar tokens semánticos para todos los colores visibles

**Estado:** Aceptada

**Decisión:** los componentes visibles deben consumir tokens semánticos de superficie, texto, borde, información, éxito, advertencia, neutral y selección. Los colores literales quedan limitados a la definición central de cada tema y no deben introducirse directamente en tarjetas, estados o alertas nuevas.

**Motivo:** evita que un componente diseñado para Claro conserve fondos o textos de bajo contraste al cambiar a Oscuro o Alto contraste y permite mantener una jerarquía cromática consistente en toda la aplicación.

## ADR-053 — Tratar Alto contraste como tema oscuro de contraste máximo

**Estado:** Aceptada

**Decisión:** Alto contraste utiliza fondo negro, texto blanco, bordes visibles y foco amarillo, con acciones primarias claramente diferenciadas. No se implementa como una variante clara con bordes más fuertes.

**Motivo:** un modo de alto contraste debe reducir ambigüedad visual y depender también de bordes y forma, no solamente de cambios de color sobre superficies claras.

## ADR-054 — Convertir Inicio en una portada orientada al Asegurado(a)

**Estado:** Aceptada

**Decisión:** la página de Inicio prioriza propósito, acción principal, sistemas cubiertos, capacidades, proceso de seis pasos y aviso breve de independencia. Se eliminan composiciones de maqueta que no ayudan a decidir qué hacer a continuación.

**Motivo:** la portada debe explicar en pocos segundos qué hace Mi Retiro Proyectado y cómo comenzar, sin exponer terminología de desarrollo ni competir con las pantallas de cálculo.

## ADR-055 — Reservar detalles de implementación para documentación interna

**Estado:** Aceptada

**Decisión:** expresiones sobre metadatos, rutas `normativa/*.json`, backend, endpoints, estructura del repositorio y mecanismos internos de carga no deben mostrarse al Asegurado(a). Cuando sea útil explicar una fuente, se presenta únicamente su nombre humano, alcance y enlace oficial.

**Motivo:** la trazabilidad jurídica es contenido del producto; el mecanismo técnico con el que se obtiene esa trazabilidad pertenece a mantenimiento y desarrollo.

## ADR-056 — Responsive por contenido y no por reducción indiscriminada

**Estado:** Aceptada

**Decisión:** UX.3 utiliza los breakpoints de Bootstrap como referencia, pero cada componente define su adaptación según su contenido. Las tablas extensas conservan un ancho mínimo legible y se desplazan dentro de su propio contenedor; las tarjetas, formularios y acciones sí se reorganizan en una sola columna cuando el ancho disponible lo requiere.

**Motivo:** comprimir todas las columnas hasta que entren en una pantalla móvil degrada la lectura y puede ocultar la relación entre datos. El desplazamiento localizado conserva la estructura de tablas previsionales sin provocar desbordamiento horizontal de toda la página.

## ADR-057 — Navegación persistente inferior en móvil

**Estado:** Aceptada

**Decisión:** en anchos menores de 768 px la navegación persistente del asistente se fija en la parte inferior, respeta las áreas seguras del dispositivo y mantiene la acción principal, retroceso y selector de paso. El progreso de seis pasos permanece arriba como una franja horizontal desplazable.

**Motivo:** una barra superior persistente consume demasiado espacio vertical en móvil y compite con encabezados y formularios. La barra inferior mantiene las acciones al alcance del pulgar sin eliminar la navegación directa entre pasos.

## ADR-058 — El Paso 5 solicita el último mes acreditado, no una fecha de retiro implícita

**Estado:** Aceptada

**Decisión:** la interfaz del Paso 5 separa tres conceptos: fecha de evaluación, último mes con cuotas acreditadas y fechas de retiro. El Asegurado(a) selecciona el último mes acreditado mediante un control mensual `YYYY-MM`. El servicio deriva la fecha técnica de corte al último día de ese mes; si el mes coincide con el de evaluación, la fecha se limita al propio día de evaluación. La fecha exacta anterior se conserva como campo de compatibilidad.

Los botones de la sección **Recursos oficiales para verificar información individual** conservan el texto **Abrir recurso oficial**, porque Mi Caja Digital es un recurso de consulta personal y no una fuente normativa utilizada por el motor. Su alineación visual sí se unifica con los demás botones de Metodología.

**Motivo:** preguntar por una fecha exacta de actualización podía confundirse con la fecha prevista de retiro y sugería una precisión diaria que el historial principal no posee. Trabajar con el último mes acreditado corresponde mejor a la granularidad disponible y mantiene clara la diferencia entre dato real, fecha de evaluación y escenario futuro.

## ADR-059 — Forzar LF para todo archivo de texto del repositorio

**Estado:** Aceptada

**Decisión:** `.gitattributes` utiliza `* text=auto eol=lf` como regla transversal. Los formatos binarios continúan marcados como `binary`. Cuando cambien estas reglas se ejecutará `git add --renormalize .` y se revisará el diff antes del commit.

**Motivo:** en Windows, `core.autocrlf` puede convertir a CRLF archivos de texto sin extensión que antes solo heredaban `text=auto`, como `.gitignore`. Forzar LF desde el repositorio elimina advertencias de conversión, evita diffs exclusivos por plataforma y mantiene coherencia con `.editorconfig`.

## ADR-060 — Responder temporalmente `/favicon.ico` sin crear un icono ficticio

**Estado:** Aceptada

**Decisión:** mientras los iconos definitivos no estén integrados, FastAPI responderá `204 No Content` a `/favicon.ico`, fuera del esquema OpenAPI y con `Cache-Control: no-store`. La ruta temporal se retirará cuando exista el favicon oficial y `base.html` lo declare explícitamente.

**Motivo:** los navegadores solicitan `/favicon.ico` de forma automática. Devolver `204` elimina el `404` de desarrollo sin versionar un recurso gráfico provisional ni favorecer que el navegador almacene permanentemente la ausencia de icono.

## ADR-061 — Mantener respaldos comprimidos fuera de la raíz y limitar `.gitkeep`

**Estado:** Aceptada

**Decisión:** los paquetes comprimidos de revisiones, entregas y respaldos históricos se conservarán fuera de la raíz del repositorio. Git y GitHub continúan siendo la historia principal del código versionado. Los archivos `.gitkeep` se utilizarán únicamente para directorios vacíos que necesiten existir en Git y se eliminarán cuando esas carpetas contengan archivos versionados reales.

No se reorganizarán rutas funcionales del proyecto únicamente por estética. Si una reorganización futura aporta un beneficio técnico suficiente, deberá modificar en la misma unidad de trabajo todos los imports, rutas, pruebas y documentos que dependan de la estructura anterior.

**Motivo:** separar respaldos locales de la copia de trabajo reduce ruido, evita incluir artefactos históricos en búsquedas o paquetes y mantiene el árbol del repositorio representativo del producto actual. Limitar `.gitkeep` evita archivos sin función una vez que el directorio ya está materializado por contenido real.
