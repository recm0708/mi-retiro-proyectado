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