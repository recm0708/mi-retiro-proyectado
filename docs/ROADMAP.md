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
- fecha de evaluación separada de fecha de corte de cuotas;
- escenarios anticipados, edad de referencia, años adicionales y fecha personalizada;
- cierre del año actual antes de densidad futura;
- validación de horizonte salarial;
- selección explícita del escenario que alimenta Resultados.

**Mejora futura:** permitir definir con mayor detalle el último mes o fecha de cotización cuando sea necesario distinguir solicitud, retiro y último aporte.

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

**Estado:** en desarrollo.

### 6.1. Paso 6 por sistema

**Completado:**

- resultados SEBD;
- resultados Mixto;
- resultados SUCGS;
- desglose por componentes;
- separación de pensiones mensuales y pagos únicos;
- advertencias y datos no confirmados;
- fuentes normativas en backend.

### 6.2. Bloque 6F — siguiente trabajo

Pendiente:

- comparador transversal entre escenarios de retiro;
- comparación entre escenarios salariales;
- diferencias absolutas y porcentuales;
- metodología visible desde la interfaz;
- botón o panel **Ver cálculo completo**;
- cadena auditable: dato → regla → fórmula → sustitución → resultado intermedio → redondeo → límite/garantía → resultado final;
- enlaces clicables a las fuentes normativas aplicables;
- preparación del resultado estructurado para informes futuros.

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

**Estado:** reservada para después de 6F.

Previsto:

- identidad visual profesional inspirada en el contexto institucional sin aparentar ser una aplicación oficial;
- temas claro, oscuro, alto contraste y seguimiento del sistema;
- persistencia de preferencia visual;
- revisión WCAG 2.2;
- foco visible y navegación por teclado;
- tamaños de objetivos táctiles adecuados;
- pie de página con autoría, aviso de independencia y fuentes;
- enlace visible a Mi Caja Digital;
- sección de Metodología y fuentes en la navegación;
- mejoras responsivas y móviles.

## 9. Estado de validación

Antes del bloque 6F:

- **57 pruebas automatizadas** en `OK`;
- regresión SEBD real anonimizada;
- casos sintéticos de Mixto;
- casos sintéticos SUCGS;
- validaciones visuales de los tres motores integrados.
