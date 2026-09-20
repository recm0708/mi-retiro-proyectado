# Transparencia del producto

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.26.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Base documental preservada:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal vigente:** MANT.2 R2/#206 — inserción post-G126 por #204/#205 — 2026-09-20
**Clasificación:** Pública / Auditoría

<!-- DOC1-R1-REVISION-MANUAL:START -->
## Nota de lectura vigente

- G121/E01 permanece publicado mediante `v0.1.21.01-beta`.
- UX.6 R1–R8 permanece cerrado/publicado con revisión funcional R8.
- UX.6 no altera reglas previsionales ni convierte Developer Diagnostics en
  telemetría de producto.
- Administración Developer y su auditoría permanecen separadas de simulación.
- NOR.3 R1–R8 permanece cerrado/publicado como G122/E01 mediante PR #162 /
  merge `b97cf61763479b80b8e8724b878089e8bb20fa00` y tag firmado
  `v0.1.22.01-beta`.
- MANT.2 R1/G123 y MANT.1 R8/G124 permanecen publicados.
- DOC.3 R1/#154 está cerrado/publicado como G125/E01 mediante
  `v0.1.25.01-beta`.
- PLAN.2 R2/#155 está cerrado/publicado como G126/E01 (`0.1.26.01-beta`).
- MANT.2 R2/#206 está activo sin Global/VERSION preasignados.
- G127 permanece libre y sin candidato.
- VER.2 R6/#164 espera el cierre/publicación de MANT.2 R2 y un #166 limpio.
- PERSIST.1 permanece detrás de VER.2 → DOC.4 → #142/derivados.
<!-- DOC1-R1-REVISION-MANUAL:END -->

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

El repositorio de código es público bajo la licencia vigente del proyecto.

## 2. Qué no es

La aplicación:

- no es un sistema oficial de la Caja de Seguro Social;
- no certifica cuotas, salarios, saldos o derechos;
- no emite resoluciones;
- no sustituye una determinación administrativa;
- no constituye asesoría jurídica individual;
- no garantiza que un resultado estimado coincida con una futura determinación oficial;
- no se convierte en una versión oficial ni en un despliegue de producción únicamente porque su repositorio sea público.

## 3. Datos acreditados y proyectados

El producto conserva como conceptos distintos:

- datos históricos/acreditados;
- información importada y confirmada;
- supuestos manuales;
- proyecciones futuras;
- referencias personales externas.

Una referencia de Mi Retiro Seguro no calibra ni corrige automáticamente los motores. Sirve para comparación contextual cuando los supuestos son compatibles.

## 4. Normativa

Los parámetros legales se versionan en `regulations/*.json` y se relacionan con `regulatory-framework.md` y `regulatory-sources.md`.

Los JSON son configuración auditable de la implementación, no una reproducción con fuerza jurídica propia.

Las discrepancias identificadas se documentan; no se armonizan silenciosamente.

## 5. Explicabilidad del cálculo

`app/models/traceability.py` y `app/services/traceability.py` describen datos utilizados, origen, reglas, fórmulas mostrables, sustituciones, resultados intermedios, fuentes y advertencias.

La capa de trazabilidad **no vuelve a calcular** la prestación. Developer Diagnostics tampoco recalcula: observa la operación ya ejecutada.

La ruta pública `/como-se-calcula` explica el orden de operaciones de SEBD, Mixto y SUCGS con parámetros leídos desde `regulations/*.json`. La guía no ejecuta motores ni reconstruye el resultado personal: la sustitución con cifras del Asegurado(a) permanece en la trazabilidad del Paso 6. Los ejemplos son ilustrativos y cualquier parámetro hipotético se identifica como no oficial.

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

La visibilidad pública del código **no autoriza versionar documentos personales reales, credenciales, secretos ni evidencia sensible**.

Consultar `privacy-policy.md`, `security-and-privacy.md` y `observability-and-logs.md`.

## 7. Validación

Las pruebas automatizadas demuestran contratos técnicos concretos. No demuestran por sí solas:

- suficiencia jurídica;
- seguridad absoluta;
- exactitud de datos personales externos;
- equivalencia universal con cálculos oficiales.

GOV.1.4 dispone de regresiones específicas para observabilidad y GOV.1.5 completó internamente el threat model formal.

La redacción histórica indicaba que la revisión jurídica externa continuaba pendiente antes de una beta pública de producto. PLAN.1 sustituyó ese hito de publicación: la revisión externa permanece pendiente como gate previo a la primera versión oficial.

## 8. Trazabilidad documental

La matriz `traceability-matrix.md` relaciona contratos críticos con fuente o criterio, ADR, implementación, prueba y estado.

La matriz **no afirma todavía cobertura individual completa de todos los RF históricos**.

## 9. Estado beta y repositorio público

El producto permanece en **desarrollo beta** bajo la familia revision-aware `0.GG.RR.EE-beta`; la familia `0.0.N-beta` se conserva únicamente como historia legacy.

El repositorio de código es público desde el 2026-08-19. Esa decisión:

- mejora la transparencia técnica y permite colaboración bajo las reglas del repositorio;
- no cambia por sí sola `VERSION`;
- no modifica la licencia propietaria;
- no constituye un despliegue remoto de la aplicación;
- no declara una versión oficial de producto;
- no elimina los gates jurídicos, funcionales, de accesibilidad, seguridad ni despliegue pendientes.

Como evidencia del checkpoint anterior se conserva la formulación: **no declara completada la primera beta pública de producto**. PLAN.1 sustituyó posteriormente esa meta por la transición directa desde la línea beta `0.0.N-beta` hacia `1.0.0.0`.

Como evidencia histórica también se conserva la formulación **“cierre de UX.4.6e y del alcance funcional UX.4.6f–h”**, que en aquella revisión describía trabajo todavía pendiente. Esa frase se mantiene únicamente para preservar la trazabilidad documental y **ya no representa el estado vigente**.

UX.4.6e–UX.4.6i, DEV.2, SEC.2 R1–R6, AUD.SEC2 R1, DOC.2,
NOR.1 R8, DOC.1 R3–R5, PLAN.2 R1, REL.GOV.1 R2, UX.5, UX.6,
NOR.3 R1–R8, MANT.2 R1 y MANT.1 R8 están cerrados.

Estados revision-aware recientes publicados:

- UX.5 R6 — G120/E01 — `v0.1.20.01-beta`;
- UX.6 R8 — G121/E01 — `v0.1.21.01-beta`;
- NOR.3 R8 — G122/E01 — `v0.1.22.01-beta`;
- MANT.2 R1 — G123/E01 — `v0.1.23.01-beta`;
- MANT.1 R8 — G124/E13 — `v0.1.24.13-beta`.

Estado material actual:

- DOC.3 R1/#154 está cerrado/integrado/publicado como G125/E01
  (`0.1.25.01-beta`);
- PLAN.2 R2/#155 está cerrado/integrado/publicado como G126/E01 (`0.1.26.01-beta`);
- MANT.2 R2/#206 está activo sin Global/VERSION preasignados;
- G127 permanece como siguiente Global disponible, libre y sin candidato;
- VER.2 R6/#164 será la siguiente fase material después de publicar MANT.2 R2 y repetir #166 limpio;
- DOC.4 R1/#171 se ejecutará después de VER.2 y antes de #142;
- #142 y cualquier derivado funcional obligatorio preceden PERSIST.1;
- PERSIST.1 → REP.1 → DEPLOY.1 preceden la ola UX.7→UX.x;
- #129/#189 gobiernan la revisión UX dinámica y la sincronización visual
  multiportal;
- revisión jurídica externa previa a la primera versión oficial continúa
  pendiente;
- SEC.2 R7 realizará el hardening final después del cierre real de la ola UX;
- la configuración pública de GitHub requiere la revalidación final prevista
  antes de 1.0;
- la aptitud para distribución oficial todavía no está declarada.

## 10. Identidad

La marca visible de Mi Retiro Proyectado utiliza activos propios versionados bajo `assets/brand/`.

El Social Preview y el logo oficial incluyen señales de identidad independiente. No se utilizan logos oficiales de la CSS como identidad del producto.

Consultar `visual-identity.md`.

## 11. Regla de transparencia

Cuando el proyecto no pueda demostrar una propiedad, debe documentarla como pendiente, aproximación, limitación, supuesto o decisión interpretativa.

No se utilizará una cifra, etiqueta o prueba para crear una precisión aparente superior a la evidencia disponible.
