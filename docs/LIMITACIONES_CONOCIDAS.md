# Limitaciones conocidas

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R4 — 2026-08-17
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

## 4. Normativa

- Existen valores sujetos a indexación.
- Hay fechas operativas temporales que deben revalidarse.
- La discrepancia Mixto 2032/2036 permanece documentada.
- Una ADR explica una interpretación técnica; no equivale a criterio jurídico vinculante.

## 5. Privacidad y seguridad

Pendientes antes de beta pública:

- revisión jurídica externa;
- threat model formal;
- procedimiento formal de incidentes;
- procedimiento de derechos del titular;
- evaluación de despliegue/TLS;
- revisión de proveedores.

## 6. Dependencias y red

Bootstrap se obtiene actualmente de jsDelivr, por lo que el navegador realiza una solicitud externa.

El backend puede consultar infraestructura CSS para fecha de referencia.

Las dependencias críticas deberán reevaluarse antes del empaquetado público.

## 7. Observabilidad

Developer Diagnostics todavía no existe. Se implementará en GOV.1.4.

R4 no crea un contrato ficticio de logs.

## 8. Trazabilidad

La matriz de R4 cubre contratos críticos, pero la trazabilidad **RF por RF** del ledger histórico completo aún es parcial.

No se debe interpretar el número de RF preservados como igual al número de requisitos con evidencia completa código/prueba.

## 9. Repositorio y distribución

- Los commits/tags actuales no se presentan como firmados criptográficamente por una política formal.
- `LICENSE` se mantiene deliberadamente pendiente hasta GOV.1.7.
- La política de divulgación de vulnerabilidades se completará en GOV.1.6/GOV.1.5 según corresponda.
- No existe aún una beta pública declarada.

## 10. Cierre de una limitación

Una limitación solo se retira cuando:

1. existe implementación o decisión que la resuelve;
2. hay prueba/evidencia suficiente;
3. la documentación dependiente fue actualizada;
4. el cambio queda trazable en Git.
