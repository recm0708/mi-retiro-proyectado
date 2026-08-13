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
- Paso 3 — historial salarial y salario actual;
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
- [ ] UX.4.6b: Revisión 4 del Paso 1 con Manual/PDF, campos obligatorios señalados, identificación opcional, parser revisable de nombre/apellido de casada, consentimiento de privacidad, Ficha Digital en Paso 3, ayudas/tablas transversales y navegación dual simétrica; implementación técnica lista, pendiente validación manual PC/laptop;
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

- **233 pruebas automatizadas** en `OK`;
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

Implementada técnicamente: términos ampliados con lectura completa antes de aceptar, navegación dual superior/inferior, corrección de recortes de ayudas contextuales y eliminación de mensajes meta al final del documento de consentimiento. El contenido público se restringe a información pertinente al propósito previsional, funcional y legal del producto. Pendiente validación manual en PC/laptop antes del cierre y commits.
