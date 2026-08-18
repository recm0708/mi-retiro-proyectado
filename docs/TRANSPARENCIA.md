# Transparencia del producto

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.23-beta`
**Base documental preservada:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal vigente:** GOV.1.5 R3 — 2026-08-18
**Clasificación:** Pública / Auditoría

Mi Retiro Proyectado es una herramienta independiente de estimación previsional. Este documento delimita qué puede afirmarse sobre el producto y qué debe permanecer explícitamente como aproximación, limitación o pendiente.

## 1. Qué es

La aplicación permite:

- organizar datos previsionales;
- diferenciar información acreditada de supuestos futuros;
- ejecutar motores SEBD, Mixto y SUCGS dentro del alcance documentado;
- comparar escenarios;
- explicar resultados mediante una capa de trazabilidad;
- vincular fuentes y decisiones de implementación;
- disponer de diagnóstico técnico local de desarrollo mediante Developer Diagnostics.

## 2. Qué no es

La aplicación:

- no es un sistema oficial de la Caja de Seguro Social;
- no certifica cuotas, salarios, saldos o derechos;
- no emite resoluciones;
- no sustituye una determinación administrativa;
- no constituye asesoría jurídica individual;
- no garantiza que un resultado estimado coincida con una futura determinación oficial.

## 3. Datos acreditados y proyectados

El producto conserva como conceptos distintos:

- datos históricos/acreditados;
- información importada y confirmada;
- supuestos manuales;
- proyecciones futuras;
- referencias personales externas.

Una referencia de Mi Retiro Seguro no calibra ni corrige automáticamente los motores. Sirve para comparación contextual cuando los supuestos son compatibles.

## 4. Normativa

Los parámetros legales se versionan en `normativa/*.json` y se relacionan con `NORMATIVA.md` y `FUENTES_NORMATIVAS.md`.

Los JSON son configuración auditable de la implementación, no una reproducción con fuerza jurídica propia.

Las discrepancias identificadas se documentan; no se armonizan silenciosamente.

## 5. Explicabilidad del cálculo

`app/modelos/trazabilidad.py` y `app/servicios/trazabilidad.py` describen datos utilizados, origen, reglas, fórmulas mostrables, sustituciones, resultados intermedios, fuentes y advertencias.

La capa de trazabilidad **no vuelve a calcular** la prestación. Developer Diagnostics tampoco recalcula: observa la operación ya ejecutada.

## 6. Privacidad

La simulación actual está diseñada para ejecución local y no utiliza una base de datos permanente de casos.

Las conexiones externas vigentes están documentadas:

- jsDelivr para Bootstrap;
- infraestructura oficial CSS para consulta mínima de fecha de referencia cuando corresponde.

Developer Diagnostics:

- está apagado por defecto;
- es local;
- no es analítica de producto;
- no envía logs automáticamente a terceros;
- prohíbe registrar PII, PDF y valores financieros.

Consultar `POLITICA_PRIVACIDAD.md`, `SEGURIDAD_PRIVACIDAD.md` y `OBSERVABILIDAD_LOGS.md`.

## 7. Validación

Las pruebas automatizadas demuestran contratos técnicos concretos. No demuestran por sí solas:

- suficiencia jurídica;
- seguridad absoluta;
- exactitud de datos personales externos;
- equivalencia universal con cálculos oficiales.

GOV.1.4 dispone de regresiones específicas para observabilidad, pero la revisión jurídica y el threat model formal continúan pendientes.

## 8. Trazabilidad documental

La matriz `MATRIZ_TRAZABILIDAD.md` relaciona contratos críticos con fuente o criterio, ADR, implementación, prueba y estado.

La matriz **no afirma todavía cobertura individual completa de todos los RF históricos**.

## 9. Estado pre-beta

El producto permanece en desarrollo interno pre-beta.

GOV.1.4 y GOV.1.5 están cerrados internamente. GOV.1.5 incorpora threat model, procedimientos de derechos/incidentes y evaluación de terceros/despliegue. Continúan pendientes:

- revisión jurídica externa antes de beta pública;
- hardening específico si se decide un despliegue remoto;
- controles GitHub/documentación adicionales de GOV.1.6;
- licencia de distribución en GOV.1.7;
- auditoría final GOV.1.8;
- declaración de aptitud para despliegue público.

## 10. Regla de transparencia

Cuando el proyecto no pueda demostrar una propiedad, debe documentarla como pendiente, aproximación, limitación, supuesto o decisión interpretativa.

No se utilizará una cifra, etiqueta o prueba para crear una precisión aparente superior a la evidencia disponible.
