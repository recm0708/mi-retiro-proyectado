# UX.4.6h R1 — Auditoría del Paso 6: resultados y exportación

## Estado y objetivo

UX.4.6h inicia después del cierre de UX.4.6g mediante el PR #32. El objetivo de R1 es endurecer la **orquestación del resultado** sin reescribir los motores previsionales existentes: SEBD, Subsistema Mixto y SUCGS continúan calculándose en Python y el frontend solo decide qué entrada explícita se utiliza, qué resultado puede mostrarse y qué información debe comunicarse al Asegurado(a).

La primera versión oficial sigue siendo posterior al cierre de los 14 bloques del plan maestro. `VERSION` permanece en `0.0.26-beta`.

## Hallazgos de la auditoría

### 1. Selección silenciosa del escenario salarial

El Paso 4 puede producir una o varias trayectorias salariales. Antes de R1, el Paso 6 utilizaba la primera alternativa cuando no había una elección guardada. Eso podía convertir el orden de una lista en una decisión previsional implícita.

Contrato R1:

- con **un solo** escenario salarial, se utiliza automáticamente y se explica que es la única alternativa disponible;
- con **varios** escenarios, el control inicia en `Seleccione una opción` hasta que exista una elección explícita;
- una elección previa válida se conserva.

### 2. Resultados obsoletos visibles después de editar entradas

El Paso 6 ya invalidaba resultados específicos al modificar datos, pero algunas superficies transversales podían permanecer visibles: resumen unificado, comparación de origen de datos, comparación con Mi Retiro Seguro, trazabilidad y futura acción de impresión.

R1 aplica una invalidación transversal antes de recalcular y cuando cambia cualquier dato dependiente. La interfaz no debe presentar simultáneamente una configuración nueva y un resultado anterior.

### 3. Transición Subsistema Mixto → SUCGS

El motor Mixto ya identifica escenarios cuya fecha debe resolverse bajo SUCGS y devuelve `TRANSICION_SUCGS`. R1 no modifica esa regla ni cambia silenciosamente el sistema del Paso 1.

Cuando el motor devuelve una transición válida, la interfaz ofrece **Preparar cálculo SUCGS** para el mismo escenario. El Asegurado(a) debe completar o confirmar los datos exclusivos del SUCGS antes de calcular. La ruta no inventa saldos ni valores individuales.

### 4. Referencias legales del SUCGS

`regulations/sucgs.json`, versión `2025-05-22`, conserva B/.144.00 como `valor_minimo_universal_referencia` y B/.265.00 como `pension_garantizada_solidaria_base`. La propia normativa versionada indica que, si no se suministran valores vigentes confirmados, la aplicación utiliza esas referencias legales.

Por tanto R1 deja de rotular ambos campos como “vigente” de manera categórica. Se muestran como **referencias legales versionadas al 22/05/2025** y la confirmación oficial sigue siendo una decisión explícita.

### 5. Bono de reconocimiento del Mixto

El motor ya trata B/.0.00 como un valor neutro: no se incorpora bono al capital y no requiere una confirmación ficticia. R1 hace visible esa interpretación. Un monto mayor que cero solo debe marcarse como confirmado cuando proceda de información oficial.

### 6. Lenguaje del resumen final

El texto “esta fila usa la misma semántica...” describía la implementación, no el resultado. R1 sustituye ese lenguaje por una explicación funcional: mensualidades y pagos únicos se muestran separados para evitar confundir naturalezas económicas diferentes.

## Copia imprimible y límite con REP.1

UX.4.6h R1 incorpora una acción básica **Imprimir / Guardar como PDF** usando `window.print()`. Es una copia de la vista de resultados, no un generador de informe formal.

La copia imprimible:

- identifica aplicación/versión, sistema, escenario de retiro, fecha/edad y momento de generación;
- oculta navegación y controles de entrada;
- conserva las superficies de resultados visibles y la trazabilidad;
- expande el detalle de trazabilidad en impresión;
- declara que no es resolución ni certificación de la CSS.

Quedan reservados para **REP.1**: arquitectura de informes PDF, formatos seleccionables, metadatos finales, protección de datos de exportación, artefactos reproducibles y demás requisitos formales de distribución.

## Arquitectura de R1

La lógica nueva vive en `app/static/js/resultados_orquestacion.js`. Esta capa:

- no implementa fórmulas previsionales;
- envuelve únicamente funciones de preparación/invalidación ya existentes;
- conserva los contratos de `resultados.js` y de los servicios Python;
- se activa solo cuando existe el panel del Paso 6;
- carga `app/static/css/resultados.css` únicamente para la simulación.

La carga temprana del módulo permite instalar los contratos antes de la inicialización del Paso 6 sin modificar el archivo grande de integración de motores.

## Validación de R1

Se añaden 16 regresiones específicas en `tests/test_ux46h_r1_resultados_exportacion.py` para fijar:

1. carga de la orquestación;
2. carga del CSS solo con Paso 6;
3. no interferencia en otras páginas;
4. selección explícita con varios escenarios;
5. selección automática explicada cuando existe uno solo;
6. conservación de elecciones previas;
7. invalidación de resumen/traza/exportación;
8. ocultamiento preventivo antes de recalcular;
9. transición Mixto→SUCGS explícita;
10. no reescritura silenciosa del sistema personal;
11. cálculo SUCGS permitido desde una transición Mixto validada;
12. rótulos SUCGS como referencias legales;
13. explicación del bono Mixto igual a cero;
14. lenguaje orientado al usuario en el resumen;
15. impresión nativa identificada como copia no oficial;
16. hoja de impresión que oculta configuración y expande trazabilidad.

Con la base de 784 pruebas al cierre de UX.4.6g, el gate candidato de R1 es **800 pruebas**.

## Validación manual prevista

La revisión manual debe cubrir, al menos:

- SEBD con un único escenario salarial;
- SEBD con múltiples escenarios salariales y elección explícita;
- desaparición de resultados viejos al cambiar una entrada;
- Mixto con datos CAP faltantes, bono cero y bono mayor que cero;
- transición Mixto→SUCGS en un escenario posterior al corte normativo implementado;
- SUCGS con referencias legales sin confirmar y con valores oficiales confirmados;
- impresión/Guardar como PDF en Claro, Oscuro y Alto contraste;
- comportamiento responsive y navegación por teclado de las acciones nuevas.

## Corrección de gate R1.1

La primera ejecución local del candidato R1 detectó tres regresiones de gobierno/documentación, no fallos matemáticos de los motores:

- un comentario Jinja incluía el identificador cronológico `UX.4.6h`, prohibido por el contrato de comentarios runtime;
- una regresión histórica de UX.4.6f seguía exigiendo que UX.4.6g fuera el bloque activo, aunque ese bloque ya estaba cerrado;
- README había avanzado a UX.4.6h mientras ROADMAP y el plan maestro todavía describían UX.4.6g como activo.

R1.1 corrige los tres puntos sin alterar entradas, fórmulas, motores, resultados previsionales ni el alcance de impresión definido en R1. El gate esperado permanece en **800 pruebas**.

## Refinamiento visual y de claridad R1.2

La revisión manual del primer resultado SEBD confirmó que el cálculo y la trazabilidad funcionan, pero detectó información redundante o poco útil para el Asegurado(a). R1.2 no modifica motores, fórmulas, cuotas, salarios seleccionados ni montos.

Cambios de presentación:

- la comparación **Información acreditada y proyección al retiro** explica que la diferencia representa el efecto de añadir cotizaciones futuras sobre la misma fecha de retiro y elimina detalle técnico sobre saldos internos de otros sistemas;
- la comparación con Mi Retiro Seguro explica los motivos de incompatibilidad en lenguaje natural; cuando la causa es la edad, muestra la edad del comprobante y la del escenario actual;
- la alerta SEBD deja de repetir el nombre de la modalidad y pasa a indicar si el escenario es calculable; la modalidad exacta permanece en la tarjeta **Modalidad determinada**;
- **Factores de la modalidad** se oculta en la Pensión de Retiro por Vejez Normal y solo se conserva para Anticipada, Proporcional o Proporcional Anticipada;
- un año que contiene simultáneamente información acreditada y salario futuro se rotula **Histórico + proyectado**, evitando clasificar todo el año como puramente proyectado;
- las tablas cortas de comparación no muestran scroll vertical innecesario;
- el selector salarial reutiliza la ayuda ya existente en vez de presentar dos mensajes consecutivos;
- la fecha de retiro dentro de la trazabilidad se presenta como `DD/MM/YYYY`, conservando ISO únicamente en los contratos internos;
- se retira el botón **Anterior** local del final del Paso 6 porque la navegación global superior e inferior ya ofrece esa acción;
- los estados textuales del resumen usan una jerarquía tipográfica menor que el monto de pensión, reforzando el resultado económico principal.

R1.2 añade 6 regresiones específicas y eleva el gate candidato de 800 a **806 pruebas**.

## Refinamiento R1.3 — salida imprimible

La validación manual mostró que imprimir directamente el DOM del Paso 6 generaba una salida demasiado extensa y visualmente equivalente a la página web. R1.3 cambia el contrato: antes de invocar `window.print()` se construye un documento A4 independiente, orientado a lectura y archivo, con tipografía contenida y secciones compactas.

La salida incluye, cuando existan: identificación del escenario, resumen de la prestación, comparación acreditado/proyectado, referencia personal importada, resultado específico del sistema, advertencias, fuentes y trazabilidad. La interfaz, los controles, la navegación y el enlace de salto no forman parte del documento.

La cantidad de páginas no se fija de forma rígida: depende del sistema, del historial y de la información disponible. El objetivo es evitar paginación artificial y mantener una extensión razonable; para el caso SEBD de validación se espera aproximadamente entre tres y cinco páginas.

La acción continúa usando la capacidad nativa de impresión del navegador. La generación de un PDF propio, descarga controlada, metadatos finales y formatos exportables permanecen reservados a REP.1.

## Cierre funcional de UX.4.6h

La validación manual del cierre confirmó el flujo SEBD de extremo a extremo en el Paso 6: contexto de retiro, selección salarial, resumen de prestación, comparación acreditada/proyectada, referencia personal, modalidad determinada, salario base, construcción de tasa, límites, advertencias, fuentes y trazabilidad.

En el caso de validación visible se observaron, entre otros, 346 cuotas al retiro, salario base mensual B/.1,484.47, tasa de reemplazo 73.75 % y pensión mensual estimada B/.1,094.80; la comparación acreditada conserva 282 cuotas y B/.741.59. Estos valores se registran como evidencia de coherencia de la interfaz y no sustituyen casos normativos adicionales.

R1.2 fue aceptado visualmente después de eliminar redundancias, mejorar jerarquía y distinguir correctamente datos históricos/proyectados. R1.3 mejoró de forma sustancial la salida de impresión al sustituir la copia directa del DOM por un informe A4 independiente.

La acción de impresión sigue delegando el guardado al navegador/sistema operativo. La aplicación llega al selector nativo de destino y al diálogo de guardado; la generación y descarga directa de un PDF controlado por la aplicación no forma parte de UX.4.6h y permanece explícitamente reservada a REP.1.

Los contratos Mixto, SUCGS, transición Mixto→SUCGS, selección múltiple e invalidación de resultados quedan protegidos por regresiones automáticas específicas de este bloque. La auditoría integral de cierre QA.1 volverá a recorrer los sistemas antes de la primera versión oficial.

**Gate de cierre:** 812 pruebas, compilación Python, sintaxis JavaScript y `git diff --check` limpios. UX.4.6h se considera formalmente cerrable únicamente cuando el pre-commit complete ese gate sin errores.

**Siguiente bloque:** UX.4.6i — Cómo se calcula.
