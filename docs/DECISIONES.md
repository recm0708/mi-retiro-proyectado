# Registro de decisiones técnicas

Este documento registra decisiones relevantes tomadas durante el desarrollo.

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

Esto permite mantener la información al recargar la pestaña sin guardar automáticamente datos personales en una base de datos. Una futura persistencia permanente deberá ser una acción explícita del usuario.

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

La densidad `cuotas_esperadas_por_anio` se utilizará para los años futuros y, cuando sea necesario, se prorrateará el año de retiro. Esto evita agregar cuotas en el año actual cuando el usuario ya indicó que no espera nuevas acreditaciones antes de cerrarlo.

---

## ADR-018 — El horizonte salarial debe cubrir el escenario de retiro

**Estado:** Aceptada

Un escenario de retiro no se considerará completamente cubierto si su fecha se extiende más allá del último año de la proyección salarial.

La aplicación advertirá la inconsistencia y ofrecerá volver al Paso 4 para extender el horizonte. No se extrapolarán silenciosamente salarios sin confirmación del usuario.

---

## ADR-019 — Navegación rápida `sticky` sin duplicar lógica de negocio

**Estado:** Aceptada

Los pasos largos del asistente dispondrán de una barra de navegación rápida visible al desplazarse.

La barra delegará sus acciones en los formularios y botones existentes. No contendrá fórmulas ni validaciones previsionales paralelas, evitando duplicar lógica y manteniendo accesibles las acciones Anterior/Continuar/Analizar.

