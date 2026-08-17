# Roadmap

Este roadmap refleja el estado funcional actual del proyecto. Las secciones históricas de subfases se integraron en las fases principales para evitar contradicciones y pendientes obsoletos.

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Fase 1 — Base técnica

**Estado:** completada.

Incluye:

- estructura del repositorio;
- FastAPI y Jinja2;
- Bootstrap y CSS propio;
- entorno virtual y dependencias;
- Git/GitHub;
- separación entre código, normativa, pruebas y documentación;
- reglas de formato y finales de línea.

## 2. Fase 2 — Asistente básico

**Estado:** completada y en mantenimiento.

Incluye:

- Paso 1 — datos personales y sistema previsional;
- Paso 2 — cuotas;
- Paso 3 — historial salarial y base para proyección;
- estado temporal en `sessionStorage`;
- invalidación de resultados dependientes;
- navegación directa entre pasos disponibles.

## 3. Fase 3 — Historial y proyección salarial

**Estado:** completada para el alcance actual.

Incluye:

- captura de historial anual;
- validación contra las cuotas del Paso 2;
- normalización salarial;
- salario constante;
- variación porcentual;
- salario futuro conocido;
- comparación de escenarios;
- línea temporal histórica/proyectada;
- precisión monetaria y formato de entrada.

**Mejora futura:** granularidad mensual cuando una regla legal o una importación oficial la requiera.

## 4. Fase 4 — Fechas, cuotas y retiro

**Estado:** completada para el alcance actual.

Incluye:

- edad exacta y fecha de referencia;
- fecha de evaluación separada del último mes con cuotas acreditadas y de las fechas de retiro;
- escenarios anticipados, edad de referencia, años adicionales y fecha personalizada;
- cierre del año actual antes de densidad futura;
- validación de horizonte salarial;
- selección explícita del escenario que alimenta Resultados.

**UX.3 implementado:** el Paso 5 solicita el último mes con cuotas acreditadas y deriva internamente la fecha de corte sin confundirla con la fecha de evaluación ni con los escenarios de retiro.

## 5. Fase 5 — Motores previsionales

**Estado:** completada para los tres motores generales principales.

### 5.1. SEBD

Implementado:

- Normal;
- Anticipada;
- Proporcional;
- Proporcional Anticipada;
- Indemnización por Vejez;
- máximos aplicables según las condiciones disponibles;
- factores anticipados versionados.

Pendiente fuera del motor general:

- monto mínimo indexado por fecha del artículo 192;
- regímenes especiales con reglas propias.

### 5.2. Subsistema Mixto

Implementado:

- Componente de Beneficio Definido;
- Componente de Ahorro Personal con saldo y divisor explícitos;
- pensión programada;
- devolución total del CAP;
- indemnización BD + devolución CAP;
- garantía de renta vitalicia;
- bono de reconocimiento como dato oficial/validado;
- transición operativa hacia SUCGS;
- integración visual.

Pendiente específico:

- reconstrucción reglamentaria completa del bono de reconocimiento;
- obtención/versionado de parámetros actuariales oficiales cuando la CSS publique una fuente utilizable;
- reconstrucción de cuenta CAP a partir de movimientos oficiales, no desde simples agregados anuales.

### 5.3. SUCGS

Implementado:

- componente contributivo del artículo 196;
- tabla de factores actuariales;
- capa solidaria de los artículos 194 y 195;
- Pensión Garantizada Solidaria;
- garantía de reemplazo mínimo del artículo 197;
- preevaluación de condiciones de cuotas y distribución;
- confirmación explícita de estabilidad salarial;
- integración visual.

Pendiente específico:

- reconstrucción completa del saldo desde aportes, conversión pre-reforma y rendimientos efectivos;
- actualización futura de factores actuariales y valores indexados cuando cambien oficialmente.

## 6. Fase 6 — Resultados, comparación y transparencia

**Estado:** completada para el alcance funcional actual.

### 6.1. Paso 6 por sistema

**Completado:**

- resultados SEBD;
- resultados Mixto;
- resultados SUCGS;
- desglose por componentes;
- separación de pensiones mensuales y pagos únicos;
- advertencias y datos no confirmados;
- fuentes normativas en backend.

### 6.2. Bloque 6F

**6F.1 — completado:**

- comparador transversal entre escenarios de retiro;
- comparación entre escenarios salariales;
- diferencias absolutas y porcentuales contra un escenario base;
- separación de pensión mensual y pago único;
- advertencias explícitas cuando Mixto o SUCGS reutilizan saldos constantes en fechas alternativas.

**6F.2 — completado:**

- trazabilidad transversal para SEBD, Mixto y SUCGS;
- datos utilizados y su origen;
- regla, fórmula, sustitución y resultado por paso;
- resultado final tipificado como mensual, pago único o pendiente;
- enlaces oficiales cargados desde `normativa/*.json`;
- vista colapsable `Ver cálculo completo` en el Paso 6.

**6F.3 — completado:**

- página `/metodologia`;
- jerarquía de fuentes y normativa por sistema;
- enlaces oficiales con nombres legibles;
- limitaciones e interpretaciones documentadas;
- recursos oficiales de verificación individual.

**6F.4 — completado:**

- contrato transversal común para SEBD, Mixto y SUCGS;
- estado homogéneo del cálculo;
- separación común entre pensión mensual y pago único;
- naturaleza de la prestación normalizada;
- comparador alimentado por el resumen transversal en lugar de extraer campos distintos de cada motor;
- resumen final unificado en el Paso 6;
- estructura preparada para persistencia e informes posteriores.

## 7. Fase 7 — Persistencia e informes

**Estado:** pendiente.

Previsto:

- SQLite;
- guardado voluntario de simulaciones;
- importación de datos cuando sea legal y técnicamente viable;
- informes PDF;
- exportación de resultados y metodología;
- manejo explícito de versiones normativas por fecha.

## 8. Fase 8 — Pulido de producto y accesibilidad

**Estado:** en ejecución.

Previsto:

- [x] identidad visible independiente bajo el nombre **Mi Retiro Proyectado**;
- [x] terminología pública estandarizada como **Asegurado(a) / Asegurados(as)**;
- [x] tipografía base unificada con jerarquía reservada a encabezados y valores importantes;
- [x] identidad visual profesional con portada orientada al Asegurado(a), sin aparentar ser una aplicación oficial;
- [x] temas claro, oscuro, alto contraste y seguimiento del sistema;
- [x] persistencia local de preferencia visual;
- [ ] revisión WCAG 2.2 ampliada con tecnologías de apoyo y matriz real de dispositivos;
- [x] estabilización visual de Oscuro y Alto contraste con tokens semánticos;
- [x] wizard, navegación rápida, tarjetas y footer adaptativos por tema;
- [x] foco visible, enlace de salto y base de navegación por teclado;
- [x] tamaños mínimos de objetivos táctiles y respeto a movimiento reducido;
- [x] pie de página compacto con autoría, aviso de independencia y acceso oficial;
- [x] enlace visible a Mi Caja Digital;
- [x] sección de Metodología y fuentes en la navegación;
- [x] responsive real para laptop, tablet y móvil;
- [x] navegación principal colapsada; UX.4.6b usa navegación dual sincronizada del wizard, con barra superior accesible durante pasos largos en PC/laptop y barra inferior al cierre del contenido;
- [x] tablas extensas con desplazamiento localizado y acciones de formulario adaptativas;
- [x] Paso 5 con último mes acreditado separado de evaluación y retiro.
- [x] UX.4.1 con semántica programática del wizard, regiones de estado y anuncios de validación;
- [x] ayudas contextuales accesibles y compactas para campos previsionales ambiguos, activadas por hover/foco con alternativa táctil;
- [x] captions accesibles para tablas, foco condicionado a desbordamiento y aviso de enlaces que abren otra pestaña;
- [x] selección de escenarios de retiro desde cualquier punto de una fila futura y remate visual de acciones auxiliares;
- [x] UX.4.2 con contraste corregido del paso activo en Claro y selección reforzada de filas de retiro en los tres temas;
- [x] UX.4.3 con errores de campo asociados, foco de recuperación, anuncios no duplicados y operación del radio de retiro con Enter;
- [x] remate UX.4.3 con `MutationObserver` idempotente y validación reactiva sin redisparar `invalid`;
- [x] remate UX.4.3 con mensajes de error inline visibles y sin dependencia del globo nativo del navegador;
- [x] UX.4.4: columna **Edad** en Historial salarial real y Proyección futura, derivada de la fecha de nacimiento y alineada con la convención de los comprobantes oficiales;
- [x] UX.4.4: detalle opcional del año actual con captura mensual/quincenal, estado parcial/completo y cuota acreditada por mes;
- [x] UX.4.4: separación entre salario disponible y salario con cuota acreditada, sincronización condicionada con el historial anual y derivación del último mes acreditado;
- [x] UX.4.4: bases de proyección manual, último mes completo, promedio del año actual, promedio de los últimos tres meses completos y promedio salarial por cuota acreditada;
- [x] UX.4.4: importación revisable desde PDF digital de Ficha Digital y comprobante de Mi Retiro Seguro, con vista previa editable y confirmación explícita antes de prellenar el asistente;
- [x] UX.4.4: Ficha Digital limitada al año calendario actual y formato monetario uniforme con separador de miles y dos decimales en las vistas previas;
- [ ] UX.4.4+: ampliar importadores a otros formatos exportables de Mi Caja Digital cuando exista un contrato estable y verificable;
- [x] UX.4.4: importar opcionalmente un comprobante PDF personal de Mi Retiro Seguro y comparar su referencia variable con el resultado actual cuando el contexto sea compatible;
- [x] UX.4.5: distinguir información acreditada y períodos proyectados como cálculo propio, independiente de la referencia PDF;
- [x] UX.4.5: tabla transversal de información acreditada vs proyección al retiro para SEBD, Mixto y SUCGS;
- [x] UX.4.5: referencia PDF comparada preferentemente contra la fotografía acreditada propia;
- [x] UX.4.5: cierre semántico de la comparación con caption, encabezados programáticos, estado textual y soporte de Alto contraste;
- [x] UX.4.6a: sistema visual transversal en `design-system.css` con paletas Claro/Oscuro modernizadas y Alto contraste preservado como opción secundaria de accesibilidad;
- [x] UX.4.6a: navegación pública simplificada, selector compacto de apariencia y footer global centrado con versión, Fuentes oficiales, autoría y copyright;
- [x] UX.4.6a: nueva página de Inicio orientada a beneficios, mockup sin resultados ficticios, tarjetas de capacidades y proceso guiado rematado en PC/laptop;
- [x] UX.4.6b: Paso 1 cerrado y validado en PC/laptop con Manual/PDF, identificación opcional, consentimiento de privacidad, Ficha Digital trasladada al Paso 3, navegación dual y CI remoto en verde;
- [x] UX.4.6c: Paso 2 cerrado y validado en PC/laptop con vista previa filtrada por etapa, nombres de secciones vinculados a sus pasos, cuota del año actual revisable, bloqueo por campo importado y un único círculo visual en ayudas contextuales;
- [x] UX.4.6d: cerrada y validada en PC/laptop tras R23; Pasos 1–3 integrados, Ficha Digital sincronizada con Cuotas/historial y acceso a Paso 4 sin navegación regresiva;
- [ ] UX.4.6e: revisar y cerrar **Paso 4 — Proyección salarial/laboral**, reutilizando los contratos visuales, de procedencia, navegación y validación ya consolidados;
- [ ] UX.4.6f: revisar y cerrar **Paso 5 — Escenarios de retiro**, incluyendo selección, coherencia temporal y dependencias con la proyección;
- [x] hardening pre-beta: validación defensiva común de PDFs, cabeceras de privacidad local y límites de texto/páginas;
- [x] regresión E2E pre-beta por API para SEBD, Mixto y SUCGS;
- [x] CI pre-beta definida para Python 3.13/3.14 y Node.js 24; primera validación remota de `main` completada en verde;
- [x] Dependabot ajustado para evitar falsos negativos por majors hardcodeados, limitar `pip` a dependencias directas y agrupar propuestas relacionadas sin auto-merge;
- [ ] validación manual ampliada opcional: teléfono Android por red local; tablet Android, iPhone/iPad, macOS y pantallas grandes quedan diferidos para beta/RC;
- [ ] privacidad pre-beta: servir Bootstrap localmente, formalizar respuesta a incidentes y solicitudes de derechos, verificar política de logs y someter los textos legales a revisión jurídica;
- [ ] UX.4.6g: exportación explícita y seleccionable desde Resultados, marcada como orientativa/no oficial y con opción de excluir identificadores;
- [x] respuesta temporal sin error para `/favicon.ico` mientras no se integran los iconos definitivos;
- [ ] integrar favicon e iconos definitivos de **Mi Retiro Proyectado** y retirar la respuesta temporal `204`.

## 9. Estado de validación

Estado técnico actual; la validación manual multidispositivo queda aplazada y las revisiones inmediatas se realizan en laptop/PC:

- **396 pruebas automatizadas** en `OK`;
- regresión SEBD real anonimizada;
- casos sintéticos de Mixto;
- casos sintéticos SUCGS;
- validaciones visuales de los tres motores integrados.



## 10. Camino a la primera beta

Antes de `v0.1.0-beta.1` se mantiene este orden de cierre:

1. completar cualquier validación manual remanente de UX.4.5 que todavía esté pendiente;
2. conservar UX.4.6a como rediseño visual cerrado y validado en PC/laptop, con la matriz multidispositivo diferida para beta/RC;
3. integrar favicon e iconos definitivos y retirar `/favicon.ico` temporal;
4. preparar el paquete portable para usuarios y validarlo en una instalación limpia;
5. revisar el estado remoto de CI/Dependabot después de los commits de cierre;
6. preparar GitHub para publicación y crear `v0.1.0-beta.1`.

La prueba manual en todos los tipos de dispositivos no es requisito de bloqueo para UX.4.5. La compatibilidad ampliada se tratará como matriz de beta/RC, priorizando los dispositivos realmente disponibles.

### Revisión 4 de UX.4.6b

Implementada, validada en PC/laptop y cerrada en `main`: términos ampliados, navegación dual superior/inferior, corrección de recortes de ayudas contextuales y eliminación de mensajes meta al final del documento de consentimiento. El cierre remoto quedó con CI verde en Python 3.13 y 3.14.

### Revisión 3 de UX.4.6c — cerrada

Implementada técnicamente: Paso 2 mantiene la separación entre cuotas acreditadas y cotización futura; la vista previa documental se filtra por etapa y etiqueta cada grupo con su paso de destino. El Paso 1 conserva la revisión completa y Cuotas muestra únicamente sus datos. Las ayudas contextuales mantienen un solo círculo visible alrededor de `i`. La suite de cierre quedó en **253 pruebas automatizadas en OK** y la revisión visual en PC/laptop fue completada antes de los commits de UX.4.6c.

### Revisión 5 de UX.4.6d — pendiente de validación visual

Implementada técnicamente: Paso 3 se concentra en tres secciones internas, elimina acciones duplicadas y rellenos masivos, reutiliza revisión documental contextual, normaliza la Ficha Digital con el mismo ciclo de revisión/edición/importación y finaliza con un resumen unificado. La suite de Revisión 2 alcanza **278 pruebas automatizadas en OK**. La revisión manual inmediata se limita a PC/laptop; la matriz multidispositivo continúa diferida para beta/RC.

### Revisión 6 de UX.4.6d — gestión de datos y privacidad

- [x] Menú **Opciones** únicamente en la navegación superior.
- [x] Limpieza por paso con invalidación descendente.
- [x] Reinicio completo conservando tema/aceptación.
- [x] Borrado local integral desde Fuentes/Privacidad.
- [x] Actualización del consentimiento a versión 2026-08-15.1.
- [x] Matriz completa de validación UX.4.6d repetida y cerrada antes de los commits.

### Revisión 7 de UX.4.6d — revisión de privacidad sin reconsentimiento

- [x] Revisar términos desde Fuentes sin navegar a Simular.
- [x] Modo revisión sin checkbox ni nueva aceptación.
- [x] Control `×` contextual en el modal.
- [x] Etiqueta **Repositorio: GitHub del proyecto** en Fuentes.
- [x] Regresión que mantiene **Opciones** fuera de la barra inferior.
- [ ] Repetir matriz completa de UX.4.6d antes del cierre y commits.

### Revisión 8 de UX.4.6d — estados y tablas

- [x] Recalcular estado al escribir cuotas o salario.
- [x] Separar `Falta salario`, `Faltan cuotas`, `Revisar`, `Parcial` y `Completo`.
- [x] Mostrar resumen anual inmediatamente después del análisis histórico.
- [x] Retirar scroll vertical innecesario con pocas filas visibles.
- [x] Normalizar el botón **Seleccionar archivo** en los tres temas.
- [x] Evitar que la ayuda del último mes desconfigure la alineación del modal de Ficha Digital.
- [x] Suite completa R8: **317 pruebas automatizadas en OK**.
- [x] Puntos 4, 5, 7, 8, 9, 13 y 18 revalidados durante el recorrido integral.
- [x] Puntos 20–30 absorbidos y completados dentro del recorrido integral de Pasos 1–3.

### Revisión 9 de UX.4.6d — reactividad y privacidad pendiente

- [x] Recalcular estados al escribir en cualquiera de los dos campos.
- [x] Retirar inmediatamente del filtro **Pendientes** una fila ya resuelta.
- [x] Eliminar carril vertical cuando la tabla corta no necesita scroll.
- [x] Permitir aceptar términos desde Fuentes cuando aún no existe consentimiento.
- [x] Definir `Esc` contextual y sustituir placeholders de identidad por ejemplos genéricos.
- [x] Puntos afectados y matriz 20–30 retesteados dentro del recorrido integral.
- [x] UX.4.6d cerrada y commits creados después de aprobación manual.
### Revisión 10 de UX.4.6d — simetría transversal de tablas

- [x] Aplicar `app-table-shell` a las tablas estáticas actuales.
- [x] Aplicar el mismo contrato a tablas dinámicas de Proyección y Línea temporal.
- [x] Normalizar radio, borde, superficie y encabezado para Claro, Oscuro y Alto contraste.
- [x] Extender detección accesible de scroll al contrato común.
- [x] Documentar qué reglas tabulares son globales y cuáles dependen de la semántica de cada tabla.
- [x] Historial anual y muestra de tablas/importaciones validados en Claro, Oscuro y Alto contraste.
- [x] Consentimiento desde Fuentes validado durante recorrido limpio 1–3.
- [x] Puntos 20–30 ejecutados y UX.4.6d cerrada antes de commits.



### Revisión 11 de UX.4.6d — scroll contenido y carga PDF

- [x] Eliminar botones/flechas nativos de scroll que invadían radios en Chromium/Windows.
- [x] Separar el track vertical/horizontal de las esquinas y adaptar el thumb a los tres temas.
- [x] Igualar altura exterior de **Seleccionar archivo** y **Analizar documento**.
- [x] R11 validada visualmente; puntos restantes completados posteriormente.

### Revisión 12 de UX.4.6d — scroll transversal y estado vacío

- [x] Extender el scrollbar temático a términos, modales, página y superficies desplazables comunes.
- [x] Reducir el radio de `app-table-shell` para integrar mejor el scroll interno.
- [x] Ocultar Historial salarial anual cuando **Pendientes** llegue a cero y mostrar un estado vacío.
- [x] Estabilizar el color de **Seleccionar archivo** al interactuar con el nombre del archivo.
- [x] Cubrir por regresión que Comparador mantiene `app-table-shell`.
- [x] Validar visualmente R12 y selector reforzado de R13.
- [x] Recorrido integral Pasos 1–3 y puntos funcionales restantes completados.


### Revisión 13 de UX.4.6d — selector de archivo estable

- [x] Neutralizar el hover heredado del input completo sobre **Seleccionar archivo**.
- [x] Proteger paleta en hover/focus y prefijo WebKit.
- [x] Mantener sin cambios motores, fórmulas y lógica previsional.
- [x] Validar manualmente el selector en los tres temas.
- [x] Recorrido limpio integral Pasos 1–3 completado, incluyendo puntos 20–30.
- [x] UX.4.6d cerrada y commits lógicos preparados después de aprobación manual.


### Revisión 14 de UX.4.6d — continuidad del formulario del Paso 1

- [x] Unificar Identificación personal e Información previsional básica en **Información personal** para captura manual.
- [x] Situar Sexo junto a Apellido de casada sin alterar su condición femenina/opcional.
- [x] Conservar IDs, importación de Mi Retiro Seguro y validaciones existentes.
- [x] Nueva disposición del Paso 1 validada visualmente.
- [x] Certificación integral Pasos 1–3 completada y UX.4.6d cerrada antes de commits.

### UX.4.6d R15 — recorrido integral de Pasos 1–3

**Estado:** en validación manual.

Paso 1 manual e importado ya fue validado durante el recorrido limpio. R15 corrige la diferenciación de controles bloqueados, desacopla el copy de importación del término PDF y corrige la limpieza de Cotización futura en Paso 2. El cierre de UX.4.6d requiere completar Paso 2, Paso 3, integración 1→3 y commits acumulados.

### UX.4.6d R16 — continuidad sin retrocesos

- [x] Integrar Ficha Digital dentro de Detalle salarial del año actual y colocar su cargador antes de la tabla mensual.
- [x] Revalidar automáticamente cuotas desde Paso 3 cuando los datos fuente siguen completos.
- [x] Evitar restaurar pasos posteriores con prerrequisitos inválidos.
- [x] R16 validada manualmente y recorrido Paso 2 → Paso 3 completado.
- [x] UX.4.6d cerrada con coherencia código/pruebas/documentación y commits acumulados.


### UX.4.6d R17 — auditoría Paso 1–3

Completada la revisión de coherencia entre comprobante, importación y pantallas: corrección visual de checkboxes proyectados, contexto 281/293, advertencia por historial anterior a fecha de ingreso, trazabilidad de campos editados y explicación de salario disponible frente a cuota acreditada. Pendiente únicamente la validación manual final de R17 y las pruebas de integración restantes antes de commits.

### UX.4.6d R18 — validación final Pasos 1–3
- [x] Contrato transversal de procedencia de datos.
- [x] Persistencia visual de importaciones tras F5 sin restaurar el file input.
- [x] Procedencia específica por campo en Paso 1 y Cuotas.
- [x] Indicador de procedencia en Ficha Digital/detalle mensual.
- [x] Puntos R17 restantes y estado persistente validados manualmente.
- [x] Revalidación silenciosa cubierta por regresión y restauración tras limpiar Paso 2 validada manualmente.
- [x] UX.4.6d cerrada y commits lógicos preparados antes de la siguiente fase.


### UX.4.6d R19 — sincronización del año actual
- [x] Derivar fila anual vigente desde el detalle mensual/quincenal.
- [x] Actualizar Paso 2 desde una casilla manual de cuota sin navegación regresiva.
- [x] Conservar separación entre salario disponible y salario acreditado.
- [x] Cubrir enero–junio con 6 cuotas/B/.8,883.50 y promedio B/.1,480.58.
- [x] Sincronización 5→6 y total 281→282 validada; protección de reversión/reducción cubierta por regresiones.
- [x] F5/limpieza de Paso 2, recorrido final 1→3 y commits acumulados completados.


### UX.4.6d R20 — vigencia de Ficha Digital y resumen auditable
- [x] Detectar último período de Ficha Digital usando metadata extraída del documento.
- [x] Advertir documentos con más de dos meses calendario de desfase sin bloquear la continuidad.
- [x] Ofrecer seleccionar una ficha más reciente o continuar con la actual.
- [x] Mostrar el último período detectado tras F5.
- [x] Exponer `resumen_detalle_anio_actual` dentro del Paso 3 y ocultarlo al invalidar.
- [x] R20 validada manualmente y recorrido limpio de cierre completado.
- [x] Coherencia final código/pruebas/documentación revisada y commits acumulados preparados.


### UX.4.6d R21
- [x] Advertir por cualquier Ficha Digital anterior al mes actual verificado.
- [x] Eliminar dependencia del reloj del navegador para vigencia.
- [x] Añadir fuente de fecha oficial con degradación conservadora.
- [x] Revalidar vigencia de importaciones persistidas.
- [x] Actualizar privacidad a 2026-08-16.1.
- [x] R21 validada manualmente; UX.4.6d cerrada y comprometida en Git.

### UX.4.6d — R22 / cierre de Paso 3
- Reconciliación defensiva de cuotas del detalle antes de analizar historial.
- Revalidación silenciosa de Paso 2 cuando la referencia cambia.
- Error explícito para cualquier diferencia real de cuotas.
- Revisión de redundancias del resumen: se conservan las 11 métricas por semántica distinta.
- [x] **Analizar historial → Continuar a proyección** validado manualmente y cierre Git completado.



### UX.4.6d — R23 / sincronización documental final de cuotas

- [x] Permitir que una Ficha Digital confirmada con más cuotas del año actual actualice Paso 2 y el total acumulado.
- [x] Revalidar Cuotas en segundo plano y conservar al usuario en Paso 3.
- [x] Evitar reducciones automáticas cuando una ficha contiene menos meses que la referencia vigente.
- [x] Cubrir la reconciliación al importar y al pulsar **Analizar historial** después de restauraciones/F5.
- [x] Caso 5→6 cuotas y acceso a Paso 4 validados manualmente antes del cierre/commits.


### Cierre final de UX.4.6d

- [x] Recorrido limpio desde consentimiento hasta Paso 4 completado en PC/laptop.
- [x] Caso final Ficha Digital 5→6 cuotas: 281→282 acumuladas y estimación de cierre 288 validada.
- [x] Historial 2026 derivado en 6 cuotas / B/.8,883.50 / Parcial y total histórico B/.205,164.64 validado.
- [x] Persistencia de importaciones y estado tras F5 validada sin intentar restaurar el `input[type=file]`.
- [x] Suite final: **396 pruebas automatizadas en OK**; `compileall`, `node --check` y `git diff --check` en OK.
- [x] Commits de cierre creados y publicados en `main`.

Siguiente secuencia UX recomendada: **UX.4.6e — Paso 4 · Proyección salarial/laboral**, **UX.4.6f — Paso 5 · Escenarios de retiro** y **UX.4.6g — Paso 6 · Resultados/exportación**.
