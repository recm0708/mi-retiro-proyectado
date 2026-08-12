# Roadmap

## Fase 1 — Base técnica

**Estado:** completada

- estructura del repositorio;
- entorno virtual y dependencias;
- FastAPI y Jinja2;
- Bootstrap y CSS propio;
- Git/GitHub;
- documentación inicial.

## Fase 2 — Asistente básico

**Estado:** completada / mantenimiento

- Paso 1 — Datos personales;
- Paso 2 — Cuotas;
- Paso 3 — historial anual y salario actual;
- validación del historial;
- `sessionStorage`;
- invalidación de resultados dependientes.

## Fase 3 — Historial y proyección salarial

**Estado:** implementada en validación final

- captura y análisis del historial;
- normalización salarial;
- cuatro modalidades de proyección;
- escenarios personalizados;
- línea temporal histórica/proyectada;
- precisión monetaria con `Decimal`;
- formato de entrada con separadores de miles y máximo dos decimales;
- clasificación explícita de años sin cotización;
- pruebas automatizadas de precisión y línea temporal.

Pendiente de cierre manual:

- repetir caso femenino real después de las correcciones;
- prueba corta del caso masculino.

## Fase 4 — Fechas, cuotas y retiro

**Estado:** implementada en validación

- cálculo de edad y fecha de referencia;
- fecha de evaluación separada de fecha de corte de cuotas;
- Paso 5 — Retiro;
- escenarios +0/+1/+2/+3/+5 y fecha personalizada;
- cierre del año actual respetado antes de densidad futura;
- advertencia cuando la proyección salarial no cubre el retiro;
- navegación rápida `sticky`;
- pruebas automatizadas femenina y masculina.

Pendiente:

- validación manual integrada;
- detalle mensual cuando un motor legal lo requiera;
- motor legal de elegibilidad.

## Fase 5 — Motores previsionales

**Estado:** en desarrollo — SEBD implementado y base backend del Subsistema Mixto en validación

- `parametros_generales.json`;
- cargador normativo;
- trazabilidad de edades generales;
- SEBD normal: fórmula base, elegibilidad y tope máximo implementados;
- pendiente completar mínimo indexado y modalidades SEBD proporcional/anticipada;
- Subsistema Mixto 6D.1: BD, CAP explícito y transición backend implementados en validación;
- pendiente SUCGS;
- pendiente transiciones;
- ampliar casos de validación anonimizados.

## Fase 6 — Resultados y comparación

**Estado:** en desarrollo; modalidades generales SEBD e indemnización integradas

- Paso 6 visual para SEBD normal: implementado;
- selección explícita del escenario de retiro: implementada;
- selección de escenario salarial: implementada;
- elegibilidad SEBD normal y desglose: implementados;
- integración de salarios proyectados hasta la fecha de retiro: implementada con advertencias;
- SEBD proporcional y retiro anticipado: pendiente;
- Subsistema Mixto: base backend 6D.1 implementada; integración del asistente, bono, garantías y casos incompletos pendientes;
- SUCGS: pendiente;
- comparador global entre modalidades/escenarios: pendiente;
- gráficos de resultados: pendiente.

## Fase 7 — Persistencia e informes

**Estado:** pendiente

- SQLite;
- guardado voluntario;
- importación de datos cuando sea viable;
- informes PDF;
- accesibilidad y despliegue.

## Actualización Paso 6C

**SEBD general:** implementado en validación.

- clasificación automática de modalidad: implementada;
- Normal: implementada y regresionada;
- Anticipada: implementada;
- Proporcional: implementada;
- Proporcional Anticipada: implementada;
- factores anticipados mensuales: versionados;
- Indemnización por Vejez: clasificación, cálculo de pago único e interfaz implementados;
- regímenes especiales: pendientes;
- Mixto: pendiente;
- SUCGS: pendiente.


## Actualización Paso 6D.1

**Subsistema Mixto — base backend:** implementado en validación.

- `normativa/mixto.json`: creado;
- cargador normativo Mixto: implementado;
- Componente de Beneficio Definido: implementado con tope de participación B/.500.00;
- advertencia por aproximación anual del tope mensual: implementada;
- Componente de Ahorro Personal con saldo y divisor actuarial explícitos: implementado;
- ausencia de parámetros actuariales: no se suple con valores inventados;
- suma BD + CAP: implementada únicamente cuando ambos componentes están disponibles;
- transición Mixto → SUCGS desde 01/03/2032: implementada;
- opción explícita SUCGS: respetada;
- pruebas automatizadas iniciales: implementadas;
- integración visual con Paso 6: pendiente;
- cálculo reglamentario del bono de reconocimiento: pendiente;
- devolución del CAP e indemnización combinada para escenarios con menos de 180 cuotas: pendiente;
- garantía/seguro colectivo después del agotamiento del CAP: pendiente;
- obtención/versionado del valor actuarial oficial vigente: pendiente;
- SUCGS: pendiente.

## Actualización Paso 6D.2

**Subsistema Mixto — prestaciones CAP complementarias:** implementado en backend y en validación.

- elección explícita `AUTO / PENSION_PROGRAMADA / DEVOLUCION_TOTAL`: implementada;
- devolución total CAP del artículo 187: implementada;
- indemnización BD + devolución CAP como pagos únicos separados: implementada;
- pensión proporcional BD + devolución CAP: implementada;
- garantía de renta vitalicia del artículo 184: modelada como continuidad futura;
- referencia histórica de prima 0.93 %: documentada y excluida del cálculo individual;
- bono de reconocimiento: entrada trazable; cálculo automático continúa pendiente;
- integración visual del Mixto en Paso 6: implementada en 6D.3;
- SUCGS: pendiente.

## Actualización Paso 6D.3

**Subsistema Mixto — integración visual:** implementado en validación.

- endpoint integrado `POST /api/simulacion/resultados/mixto`: implementado;
- consolidación de Pasos 1–5 con el motor Mixto: implementada;
- captura explícita de saldo CAP, bono, divisor actuarial y opción CAP: implementada;
- presentación separada de BD, CAP, pensión mensual y pagos únicos: implementada;
- decisión CAP pendiente visible y recalculable: implementada;
- garantía de renta vitalicia visible cuando aplica: implementada;
- persistencia temporal de configuración y resultado Mixto en la sesión: implementada;
- SUCGS: pendiente.

## Actualización Paso 6E.3

**SUCGS — componente contributivo + capa solidaria:** implementado en backend.

- `normativa/sucgs.json`: tabla actuarial y referencias solidarias versionadas;
- fórmula `saldo / 1000 × factor actuarial`: implementada y validada;
- artículos 194 y 195: implementados con clasificación explícita de prestaciones y complemento solidario;
- valores B/.144.00 y B/.265.00: tratados como referencias legales sustituibles por valores vigentes confirmados;
- superposición exacta de 240 cuotas entre artículos 194 y 195: documentada y resuelta priorizando el artículo 195;
- artículo 197: implementado en backend con preevaluación conservadora;
- integración visual completa del SUCGS: implementada en 6E.4;
- el saldo se recibe explícitamente y no se reconstruye todavía desde el historial salarial.

## Actualización Paso 6E.4

**SUCGS — integración visual:** implementada.

Estado actual de motores principales:

- SEBD: motor e integración visual implementados;
- Subsistema Mixto: motor e integración visual implementados;
- SUCGS: componente contributivo, capa solidaria, garantía de reemplazo e integración visual implementados.

Siguiente bloque: comparación transversal, transparencia del cálculo y cierre funcional del Paso 6 antes del pulido general de UX/accesibilidad.
