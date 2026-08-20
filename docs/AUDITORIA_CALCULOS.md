# Auditoría de cálculos

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.26-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R4 — 2026-08-17
**Clasificación:** Técnica / Auditoría

Este documento define qué evidencia permite reproducir y revisar un cálculo de Mi Retiro Proyectado sin convertir la capa de auditoría en un segundo motor.

## 1. Principio

La prestación se calcula en los motores correspondientes.

La auditoría:

- registra contexto;
- identifica versión;
- conserva entradas/supuestos;
- revisa trazabilidad;
- compara resultados reproducidos.

**No recalcula fórmulas por una implementación paralela.**

## 2. Evidencia mínima de reproducción

Para reproducir un resultado se debe conocer, como mínimo:

1. commit Git o estado exacto del código;
2. versión de aplicación de `VERSION`;
3. sistema previsional;
4. versión/metadata de los JSON normativos aplicables;
5. entradas históricas;
6. datos acreditados del año actual;
7. escenario salarial;
8. escenario/fecha de retiro;
9. datos individualizados adicionales de Mixto/SUCGS cuando procedan;
10. resultado y advertencias.

## 3. Trazabilidad de cálculo existente

`ResumenTrazabilidadCalculo` contiene actualmente:

- `version_metodologia` (valor inicial `1.0`);
- sistema;
- tipo de prestación;
- datos utilizados;
- pasos;
- resultado final;
- tipo de resultado;
- fuentes;
- advertencias.

Los pasos pueden registrar regla, fórmula, sustitución, resultado y redondeo.

## 4. Límite actual del objeto de trazabilidad

El objeto de trazabilidad actual **no incorpora por sí mismo**:

- versión de aplicación;
- SHA del commit;
- hash criptográfico de `normativa/*.json`;
- identificador persistente del cálculo.

Por tanto, la reproducibilidad completa exige relacionar la respuesta con el estado del repositorio/ejecución.

GOV.1.4 podrá aportar correlación operacional; R4 no inventa un sistema de logs antes de implementarlo.

## 5. Normativa

Para una auditoría normativa se deben conservar:

- nombre del archivo JSON;
- campo `version` o metadata equivalente;
- fuente oficial asociada;
- fecha crítica utilizada;
- ADR si existe una interpretación.

Cuando una cifra sea indexable o temporal, debe verificarse su vigencia para la fecha calculada.

## 6. Datos

Los datos de entrada se clasifican como:

- acreditados/históricos;
- importados y confirmados;
- manuales;
- proyectados;
- individualizados no inferibles.

No debe presentarse un supuesto futuro como dato acreditado.

## 7. Redondeo

La auditoría debe comprobar el criterio de `Decimal`/redondeo definido por el motor y ADR-016.

La cifra visible a dos decimales no autoriza a redondear artificialmente operaciones intermedias para forzar coincidencia.

## 8. Procedimiento de reproducción

1. posicionar el repositorio en el commit objetivo;
2. verificar `VERSION`;
3. instalar `requirements.txt`;
4. registrar metadata normativa;
5. usar entradas sintéticas o autorizadas;
6. ejecutar el endpoint/servicio correspondiente;
7. conservar resultado y `ResumenTrazabilidadCalculo`;
8. comparar dato por dato y paso por paso;
9. registrar cualquier divergencia como incidencia, no como ajuste silencioso.

## 9. Casos personales

No se versionan PDFs o identificadores reales para reproducibilidad.

Una propiedad descubierta con un caso real debe convertirse en fixture sintético/anonimizado.

## 10. Criterio de auditabilidad

Un resultado se considera técnicamente reproducible solo si el auditor puede identificar:

- código;
- parámetros;
- entradas;
- supuesto;
- método;
- salida.

La coincidencia con una herramienta externa puede ser evidencia comparativa, pero no sustituye esos elementos.
