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

**Estado:** en desarrollo — SEBD normal implementado en backend

- `parametros_generales.json`;
- cargador normativo;
- trazabilidad de edades generales;
- SEBD normal: fórmula base, elegibilidad y tope máximo implementados;
- pendiente completar mínimo indexado y modalidades SEBD proporcional/anticipada;
- pendiente Subsistema Mixto;
- pendiente SUCGS;
- pendiente transiciones;
- ampliar casos de validación anonimizados.

## Fase 6 — Resultados y comparación

**Estado:** en desarrollo; SEBD normal integrado en backend e interfaz

- Paso 6 visual para SEBD normal: implementado;
- selección explícita del escenario de retiro: implementada;
- selección de escenario salarial: implementada;
- elegibilidad SEBD normal y desglose: implementados;
- integración de salarios proyectados hasta la fecha de retiro: implementada con advertencias;
- SEBD proporcional y retiro anticipado: pendiente;
- Subsistema Mixto: pendiente;
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
- Indemnización por Vejez: clasificación implementada, monto pendiente;
- regímenes especiales: pendientes;
- Mixto: pendiente;
- SUCGS: pendiente.
