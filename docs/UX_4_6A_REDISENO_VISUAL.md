# UX.4.6a — Rediseño visual integral y nueva página de Inicio

## Estado

**Cerrada y validada en PC/laptop. Aprobada para consolidación mediante commits de cierre.**

La revisión manual fue aceptada después del remate visual final. Los documentos transversales del proyecto quedaron sincronizados y la suite completa se ejecutó con 198 pruebas en `OK` antes de preparar los commits.

La validación específica en tablet, móvil, macOS y pantallas grandes permanece diferida para la ronda beta/RC. Las reglas responsive existentes de UX.3 se conservan y la nueva capa visual incorpora adaptaciones defensivas, pero esas vistas no bloquean esta revisión.

## Objetivo

Modernizar la presentación de **Mi Retiro Proyectado** sin modificar fórmulas previsionales, contratos de los motores ni criterios normativos. La interfaz debe sentirse como un producto web coherente y no como una colección de formularios técnicos.

UX.4.6a agrupa en una sola fase:

1. sistema visual global;
2. navegación, selector de apariencia y footer;
3. nueva página de Inicio;
4. unificación visual del asistente, comparador y Metodología/Fuentes.

## Sistema visual

Se incorpora `app/static/css/design-system.css` como capa visual explícita. El orden de carga es:

1. `style.css` — base histórica y reglas funcionales/responsive existentes;
2. `design-system.css` — tokens y presentación UX.4.6a;
3. `accesibilidad.css` — remates de accesibilidad que deben conservar precedencia.

Esta separación permite revisar el rediseño sin reescribir de forma masiva la hoja histórica justo antes de la beta. Una consolidación futura podrá retirar reglas visuales redundantes después de estabilizar la interfaz.

### Paleta clara

- fondo general: `#f7f9fc`;
- superficie principal: `#ffffff`;
- texto principal: `#0f172a`;
- texto secundario: `#475569`;
- primario: `#2563eb`.

### Paleta oscura

- fondo general: `#070b12`;
- superficie principal: `#0d1420`;
- superficie secundaria: `#101a29`;
- texto principal: `#f8fafc`;
- texto secundario: `#b8c2d6`;
- primario: `#60a5fa`.

El modo Alto contraste no se elimina. Conserva la base negro/blanco ya validada y recibe reglas específicas para los nuevos componentes.

## Apariencia y accesibilidad

El antiguo `select` visible con cuatro opciones se sustituye por un control compacto de apariencia. El menú presenta primero:

- Automático;
- Claro;
- Oscuro.

**Alto contraste** se mantiene en un bloque secundario denominado **Accesibilidad**. La preferencia continúa almacenándose únicamente en `localStorage`, no forma parte de la simulación y sigue respetando `prefers-color-scheme` cuando el modo es Automático.

El JavaScript conserva compatibilidad defensiva con el antiguo `#selector-tema` durante actualizaciones parciales, aunque la plantilla nueva ya no lo utiliza.

## Navegación principal

La navegación pública se simplifica a:

- Inicio;
- Simular;
- Escenarios;
- Fuentes.

Los nombres de las rutas y endpoints no cambian. El cambio es exclusivamente de etiqueta visible.

La marca del header utiliza un marcador temporal **MR** generado con HTML/CSS. No sustituye los iconos definitivos del producto; se retirará o reemplazará cuando se integre el paquete gráfico oficial antes de la beta.

## Footer

El footer deja de duplicar el acceso a Mi Caja Digital. Ese recurso continúa disponible dentro de los flujos donde aporta contexto individual y en la sección correspondiente de recursos oficiales.

El pie global conserva:

- nombre del producto;
- declaración de herramienta independiente;
- advertencia de que no sustituye la determinación oficial de la CSS;
- acceso a Fuentes oficiales;
- versión de la aplicación;
- autoría y copyright.

## Nueva página de Inicio

La portada se orienta a beneficios y tareas del Asegurado(a), no a detalles de implementación.

### Hero

Mensaje principal:

> Proyecta tu jubilación con información clara, útil y comparable.

La llamada principal abre la simulación y la secundaria lleva a fuentes oficiales.

### Vista ilustrativa

La columna derecha muestra un mockup construido exclusivamente con HTML/CSS. No usa un monto ficticio: la pensión aparece como `B/. —` y se indica expresamente que el resultado se calcula con los datos del usuario.

El mockup comunica las tres dimensiones principales de la experiencia:

- cuotas acreditadas y futuras;
- historial y escenario salarial;
- comparación de fechas de retiro.

### Sistemas contemplados

Se mantienen SEBD, Mixto y SUCGS, pero el texto público explica qué puede revisar el usuario en lugar de describir la existencia de motores internos.

### Capacidades

La portada resume tres tareas:

- revisar cuotas;
- proyectar salario;
- comparar escenarios.

### Proceso guiado

Se conserva la secuencia de seis pasos y se presenta con una jerarquía visual más ligera.

### Aviso orientativo

El cierre de la portada mantiene explícitamente que la herramienta no sustituye la determinación oficial de la Caja de Seguro Social de Panamá.

## Remate visual de la revisión en PC/laptop

La revisión manual identificó tres ajustes finales antes del cierre:

- reducir ligeramente el tamaño del título principal y aumentar su interlineado para evitar una composición demasiado apretada entre líneas;
- centrar horizontalmente el número y el nombre de cada uno de los seis pasos respecto de su tarjeta;
- mantener el aviso **Estimación orientativa** sobre la misma superficie del bloque de proceso para evitar un corte cromático que pareciera atravesar la tarjeta;
- reorganizar el footer en una composición centrada, con nombre y versión como identidad superior, aviso legal compacto y una línea final con **Fuentes oficiales**, autoría y copyright.

Estos cambios son exclusivamente de presentación y no modifican navegación, contratos de datos, persistencia ni cálculos.

## Componentes transversales

La nueva capa visual unifica:

- botones primarios, secundarios y auxiliares;
- `input`, `select`, radios y checks;
- foco visible;
- cards y métricas;
- alertas semánticas;
- tablas;
- acordeones;
- wizard y barra rápida;
- Comparador;
- Metodología/Fuentes.

No se alteran IDs utilizados por JavaScript ni contratos de formularios en las páginas internas.

## Regresiones automatizadas añadidas

`tests/test_ux46a_redisenio_integral.py` incorpora trece comprobaciones estructurales:

1. orden de carga `style.css` → `design-system.css` → `accesibilidad.css`;
2. navegación pública abreviada;
3. Alto contraste como opción secundaria, no eliminada;
4. actualización del estado del selector de apariencia;
5. footer legal sin duplicar Mi Caja Digital;
6. portada orientada a beneficios y mockup sin cifra ficticia;
7. tokens principales del tema Claro;
8. tokens principales del tema Oscuro;
9. lenguaje visual común para controles y tarjetas;
10. adaptación explícita de componentes nuevos a Alto contraste;
11. escala e interlineado final del hero y centrado de los seis pasos;
12. continuidad visual entre proceso y aviso orientativo;
13. footer final centrado con versión y acceso a Fuentes oficiales.

También deben actualizarse las regresiones históricas que esperaban el antiguo selector, el antiguo footer y el texto anterior de Inicio.

Partiendo de las **185 pruebas** existentes, las trece regresiones nuevas elevan la suite a **198 pruebas automatizadas**. La ejecución completa confirmó `Ran 198 tests` y `OK`, sin regresiones adicionales.

## Revisión manual final en PC/laptop

La revisión de cierre comprobó como mínimo:

- header, marca, navegación y menú de apariencia;
- Claro y Oscuro en Inicio;
- Alto contraste para confirmar que sigue operativo aunque sea secundario;
- nueva portada completa y ausencia de texto cortado;
- footer en Inicio y páginas internas;
- Pasos 1 a 6 del asistente, prestando atención a cards, inputs, botones, tablas y barra rápida;
- Comparador de escenarios;
- Metodología/Fuentes, incluidos botones `Abrir fuente oficial` y `Abrir recurso oficial`;
- que Mi Caja Digital continúe accesible en los puntos funcionales correspondientes aunque ya no esté en el footer;
- que no cambien cálculos ni datos persistidos por el rediseño.

## Criterio de cierre

UX.4.6a se considera cerrada porque:

1. la revisión visual en PC/laptop fue aceptada;
2. se incorporaron las correcciones finales de hero, pasos, aviso orientativo y footer;
3. `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `DECISIONES.md`, `ESPECIFICACION_FUNCIONAL.md`, `ARQUITECTURA.md`, `GUIA_INTERNA_DESARROLLO.md`, `VALIDACION.md`, `INDICE.md` y las convenciones de contribución afectadas quedaron sincronizados;
4. `compileall`, `node --check`, suite completa y `git diff --check` quedaron en verde;
5. el estado está listo para commits finales por categoría, manteniendo separados implementación visual, regresiones y documentación.
