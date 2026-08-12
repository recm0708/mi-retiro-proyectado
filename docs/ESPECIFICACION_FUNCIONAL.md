# Especificación funcional

La aplicación guía al usuario por seis pasos y calcula una prestación estimada según el sistema previsional seleccionado. Este documento describe el comportamiento funcional actual y el trabajo que queda para 6F.

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
- SEBD — Beneficio Definido;
- Subsistema Mixto;
- SUCGS — Sistema Único de Capitalización con Garantía Solidaria.

La aplicación debe mostrar el nombre completo de siglas que puedan no ser conocidas por el usuario.

### 2.2. Paso 2 — Cuotas

**RF-005.** Registrar cuotas totales acreditadas.

**RF-006.** Registrar cuotas del año actual incluidas en el total.

**RF-007.** Registrar si el usuario espera continuar cotizando.

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

**RF-019.** Separar fecha de evaluación y fecha de corte de cuotas.

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

**RF-049.** Cuando `AUTO` requiera una decisión del asegurado, mantener el resultado pendiente.

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

## 10. Fuera del alcance inmediato

Quedan para fases posteriores:

- persistencia permanente;
- importaciones oficiales automatizadas;
- informes PDF;
- regímenes especiales no implementados;
- reconstrucción completa de cuentas CAP/SUCGS desde movimientos mensuales oficiales;
- identidad visual final, temas y revisión integral WCAG 2.2.

### RF-077 — Página transversal de metodología y fuentes

**Implementado en 6F.3.** La aplicación ofrece una página permanente de metodología y fuentes que permite consultar la jerarquía normativa, los artículos utilizados por sistema, los reglamentos y resoluciones relacionados y los recursos oficiales de verificación.

### RF-078 — Etiquetas humanas para fuentes de trazabilidad

**Implementado en 6F.3.** Los identificadores técnicos de fuentes permanecen internos. `Ver cálculo completo` muestra títulos comprensibles y enlaces oficiales cuando están disponibles.

### RF-079 — Contrato transversal de resultado final

**Implementado en 6F.4.** Los resultados integrados de SEBD, Mixto y SUCGS deben exponer un resumen común con estado del cálculo, naturaleza de la prestación, pensión mensual, pago único, modalidad, escenario y advertencias, sin recalcular la prestación ni borrar el desglose específico de cada motor.
