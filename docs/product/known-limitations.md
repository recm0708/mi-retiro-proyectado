# Limitaciones conocidas

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.11.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Base documental preservada:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal histórica:** GOV.1.5 R3 — 2026-08-18
**Última revisión documental:** PLAN.1 R2C — 2026-08-20
**Clasificación:** Pública / Técnica / Riesgo

Este registro enumera limitaciones conocidas que deben permanecer visibles hasta que una fase posterior las elimine o sustituya.

## 1. Modelo previsional

### Granularidad histórica

Parte del historial se modela por año. Una fuente oficial mensual puede producir diferencias en años parciales o reglas sensibles a fechas.

### Mixto

El saldo CAP y parámetros actuariales individualizados no se reconstruyen automáticamente desde un resumen salarial anual.

### SUCGS

El saldo de capitalización solidaria se suministra explícitamente cuando no puede reconstruirse con fidelidad.

### Regímenes especiales

El motor general no cubre automáticamente todo régimen especial de asegurado.

## 2. Importación documental

- Solo se procesa PDF digital con texto extraíble.
- No existe OCR como fallback productivo.
- Un documento escaneado puede no ser analizable.
- Los layouts oficiales futuros pueden requerir actualización del parser.
- Ficha Digital se utiliza para el detalle reciente definido por el contrato actual, no como importador universal de toda la historia.

## 3. Fechas externas

La comprobación de fecha de Ficha depende de obtener una referencia HTTP confiable desde infraestructura oficial configurada.

Si no puede verificarse, la aplicación adopta un estado conservador y solicita revisión; no garantiza disponibilidad de la fuente externa.

Developer Diagnostics solo registra estado de cache, cantidades, outcome y duración; no elimina esta dependencia operativa.

## 4. Normativa

- Existen valores sujetos a indexación.
- Hay fechas operativas temporales que deben revalidarse.
- La discrepancia Mixto 2032/2036 permanece documentada.
- Una ADR explica una interpretación técnica; no equivale a criterio jurídico vinculante.

## 5. Privacidad y seguridad

Pendientes antes de la primera versión oficial:

- revisión jurídica externa;
- hardening y pruebas de un despliegue remoto concreto si se decide implementarlo;
- decisión final sobre servir Bootstrap localmente o aceptar explícitamente el tercero;
- cierre de SEC.2 y revisión de los controles de seguridad que dependan del alcance final.

La revisión jurídica externa continúa como un único gate; no se duplica por aparecer en más de un documento de gobierno.

## 6. Dependencias y red

Bootstrap se obtiene actualmente de jsDelivr, por lo que el navegador realiza una solicitud externa.

El backend puede consultar infraestructura CSS para fecha de referencia.

Las dependencias críticas deberán reevaluarse antes del empaquetado de la primera versión oficial.

## 7. Observabilidad

Developer Diagnostics existe desde GOV.1.4, pero tiene un alcance deliberadamente limitado:

- solo se activa con `MRP_DEV_MODE=1`;
- no es analítica de producto;
- no existe telemetría remota automática;
- no captura cuerpos HTTP ni valores de simulación;
- no sustituye un sistema productivo de monitoreo;
- la exportación diagnóstica es local y explícita;
- la política de retención es local y acotada por rotación, no por un servicio central.

Un despliegue remoto futuro debe reevaluar ubicación, permisos, retención, acceso y protección de logs.

## 8. Trazabilidad

La matriz de R4 cubre contratos críticos, pero la trazabilidad **RF por RF** del ledger histórico completo aún es parcial.

No se debe interpretar el número de RF preservados como igual al número de requisitos con evidencia completa código/prueba.

## 9. Repositorio y distribución

- Los commits y tags nuevos del mantenedor están sujetos a la política de firma SSH y los tags publicados son inmutables bajo ruleset.
- `LICENSE` adopta una política propietaria pre-beta; una publicación pública/comercial mantiene pendiente revisión jurídica externa y verificación de avisos de terceros.
- `SECURITY.md` define el canal y la política de divulgación responsable; la disponibilidad de funciones avanzadas de GitHub depende del plan/visibilidad del repositorio.
- La aplicación permanece en la línea beta `0.0.N-beta`; **no existe todavía una versión oficial declarada**.
- La visibilidad pública del repositorio no equivale a un despliegue productivo ni a la liberación de `1.0.0.0`.

## 10. Cierre de una limitación

Una limitación solo se retira cuando:

1. existe implementación o decisión que la resuelve;
2. hay prueba/evidencia suficiente;
3. la documentación dependiente fue actualizada;
4. el cambio queda trazable en Git.
