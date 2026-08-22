# VER.2 — Conteo provisional de segunda pasada

**Estado:** documento de trabajo; no sustituye todavía al ledger canónico.  
**Base:** `main` en `7037addd44253e528c77460b678d2b3ccd540dd5`.  
**Criterio:** solo estados reales, diferenciados y aceptados; candidatos fallidos, checkpoints intermedios, commits por categoría, PR documentales y materializaciones del mismo estado no consumen Global adicional.

## 1. Punto de partida descartado

La primera pasada proponía **G057** como último estado aceptado. La segunda pasada demuestra que ese total no es estable.

## 2. Ajustes confirmados respecto de la primera pasada

| Ajuste | Delta |
|---|---:|
| GOV.1.5: R1 y R2 tienen cierre original propio antes de R3/cierre; la primera pasada había contado todo el bloque como una sola fila | +2 |
| UX.4.6f: PR #31 es hardening/cierre documental posterior a R2 ya aceptada y cerrada; no es revisión nueva | -1 |
| UX.4.6h: R1 falló; R1.1, R1.2 y R1.3 fueron aceptadas. La primera pasada solo había contado R1.2/R1.3 | +1 |
| UX.4.6i: R1 llegó a gate aceptado de 826 después de un hotfix documental no independiente; R1.4 es el cierre de 841. La primera pasada solo había contado R1.4 | +1 |
| UX.2.1: fase real absorbida en el estado retrospectivo G009, sin duplicación | 0 |
| UX.4.6e: se mantienen nueve estados R1–R9/cierre; checkpoints 604/624 y R8.1/R8.2 no crean filas extra | 0 |
| PLAN.1: se mantienen R1–R3B2 y un único cierre R4; R4.1/R4.2/PR #25 no triplican el cierre | 0 |
| UX.4.6g: un único cierre formal R1 con 784 pruebas; R1.2/R1.3/R1.4.3 son refinamientos del mismo cierre y no estados aceptados independientes | 0 |

**Delta neto confirmado hasta este punto: +3.**

Por tanto, el contador de trabajo pasa provisionalmente de **G057 a G060**.

## 3. Secuencia provisional desde GOV.1.5

La renumeración de trabajo, todavía no canónica, queda así:

| Global provisional | Estado |
|---:|---|
| G029 | GOV.1.5 R1 — modelo de amenazas |
| G030 | GOV.1.5 R2 — derechos/incidentes y procedimientos |
| G031 | GOV.1.5 R3 — cierre seguridad/privacidad/transparencia |
| G032 | GOV.1.6 — controles GitHub |
| G033 | GOV.1.7 — licencia/distribución |
| G034 | GOV.1.8 — cierre GOV.1 |
| G035–G043 | UX.4.6e — R1, R2, R3, R4, R5, R6, R7, R8 y R9/cierre |
| G044–G052 | PLAN.1 — R1, R2A, R2B1, R2B2, R2C, R3A, R3B1, R3B2 y R4/cierre |
| G053 | UX.4.6f R1/R1.1 — aceptación conjunta |
| G054 | UX.4.6f R2 — cierre lógico/funcional del Paso 4 |
| — | PR #31 — hardening/documentación; no consume Global |
| G055 | UX.4.6g R1 — cierre Paso 5 |
| G056 | UX.4.6h R1.1 — corrección aceptada del candidato fallido R1 |
| G057 | UX.4.6h R1.2 — revisión aceptada |
| G058 | UX.4.6h R1.3 — cierre Paso 6, 812 pruebas |
| G059 | UX.4.6i R1 — estado aceptado tras gate 826 |
| G060 | UX.4.6i R1.4 — cierre Cómo se calcula, 841 pruebas |

## 4. Exclusiones tardías confirmadas

- UX.4.6h R1: candidato fallido, no consume.
- UX.4.6i R1.1: no existe como revisión independiente; fue un hotfix documental durante el gate de R1.
- UX.4.6i R1.2/R1.3: existen como nombres de refinamiento, pero todavía no hay evidencia suficiente de aceptación diferenciada para consumir Global bajo criterio conservador.
- UX.4.6g R1.2/R1.3/R1.4.3: refinamientos internos del único cierre formal R1; no consumen Global.
- PR #31 y PR #25: materialización/hardening/documentación del estado ya aceptado; no consumen Global.
- PR Dependabot #1–#8 cerrados o sustituidos: no consumen Global.

## 5. Consecuencia provisional para VER.2

Si la revisión residual no aporta ni elimina otro estado aceptado, el siguiente Global disponible para el cierre real de VER.2 sería:

```text
G061
```

El identificador revision-aware exacto **no se promueve todavía** y `VERSION` no debe modificarse hasta regenerar el ledger completo, materializar el JSON machine-readable, corregir regresiones históricas y obtener gate/CI verde.
