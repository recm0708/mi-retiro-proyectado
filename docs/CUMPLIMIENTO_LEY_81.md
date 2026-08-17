# Matriz interna de alineación con Ley 81 de 2019

**Estado:** Vigente como control interno
**Versión de aplicación revisada:** `0.0.23-beta`
**Versión de privacidad revisada:** `2026-08-16.1`
**Revisión documental:** GOV.1.3 R3 — 2026-08-17
**Clasificación:** Privacidad / Cumplimiento interno
**Alcance:** No constituye certificación jurídica

La matriz sirve para detectar controles implementados y trabajo pendiente. Una fila “Implementado” significa que existe un control técnico/documental observable; no que un profesional jurídico haya certificado suficiencia legal.

## 1. Referencias

- Ley 81 de 26 de marzo de 2019;
- Decreto Ejecutivo 285 de 28 de mayo de 2021;
- orientaciones/preguntas frecuentes de ANTAI.

Fuentes: `FUENTES_NORMATIVAS.md`.

## 2. Matriz vigente

| Área | Control actual | Estado |
|---|---|---|
| Información previa | Documento visible antes de tratar datos en Simular | Implementado |
| Lectura | Casilla bloqueada hasta llegar al final | Implementado |
| Consentimiento | Aceptación explícita/versionada y activa por sesión | Implementado |
| Rechazo | Impide entrar a Simular sin aceptación | Implementado |
| Finalidad | Simulación/proyección/comparación/explicación | Documentado |
| Minimización | Identificadores opcionales; parsers limitados | Implementado base |
| Revisión de importación | Vista previa + confirmación | Implementado |
| Conservación | Simulación temporal; sin BD permanente | Implementado |
| Eliminación local | Limpiar/reiniciar/borrar datos locales | Implementado |
| Cookies propias de seguimiento | No implementadas | Verificado por contrato/pruebas |
| Recursos externos | jsDelivr + consulta fecha CSS documentados | Implementado documental |
| Seguridad HTTP | `no-store`, CSP y cabeceras | Implementado base |
| Acceso/rectificación local | Edición/revisión en UI | Implementado base |
| Derechos formales | Procedimiento interno completo | Pendiente GOV.1.5 |
| Portabilidad | Exportación estructurada | Pendiente de producto |
| Incidentes | Procedimiento formal | Pendiente GOV.1.5 |
| Logging/observabilidad | Contrato seguro de logs | Pendiente GOV.1.4 |
| TLS remoto | Obligatorio si existe despliegue remoto | Pendiente de despliegue |
| Revisión jurídica | Revisión profesional | Pendiente antes de publicación |

## 3. Inventario de necesidad

| Dato | Necesidad en cálculo | Observación |
|---|---|---|
| Nombres/apellidos | No | Identificación voluntaria |
| Cédula | No | Identificación voluntaria |
| NSS | No | Identificación voluntaria |
| Fecha nacimiento | Sí | Edad/fechas |
| Sexo | Sí en reglas modeladas | Edad/condiciones |
| Fecha ingreso CSS | Funcional | Contexto |
| Sistema | Sí | Motor |
| Cuotas | Sí | Prestación |
| Salarios/historial | Sí según motor | Base/proyección |
| Escenarios | Sí para proyección | Predictivo |
| Resultados | Derivado | Explicación |

## 4. Consentimiento

La versión vigente en código y documentos es `2026-08-16.1`.

El registro local no basta por sí solo: el frontend exige también una marca de la misma versión en la sesión activa.

## 5. Conexiones externas

### jsDelivr

Se utiliza para Bootstrap con SRI.

No se envía el contenido de la simulación como parte de esa solicitud de recurso.

### CSS

El backend puede leer el encabezado `Date` de infraestructura oficial para evaluar vigencia de Ficha Digital.

No transmite categorías previsionales.

## 6. Derechos del titular

ANTAI publica como derechos fundamentales:

- acceso;
- rectificación;
- cancelación;
- oposición;
- portabilidad.

R3 documenta el marco. El procedimiento interno, verificación y evidencia de atención se implementarán en GOV.1.5.

Los controles locales de borrado **no se presentan como sustituto** de ese procedimiento si en el futuro existe tratamiento remoto/persistente.

## 7. Pendientes obligatorios pre-beta pública

- procedimiento de derechos;
- procedimiento de incidentes;
- threat model;
- revisión de logs;
- terceros/proveedores;
- TLS/despliegue;
- revisión jurídica;
- reevaluación si se incorporan cuentas, nube, telemetría o analítica.

## 8. Criterio de cambio de versión de privacidad

Debe evaluarse una nueva versión cuando cambien materialmente:

- finalidad;
- categorías de datos;
- conservación;
- destinatarios;
- servicios externos relevantes;
- seguimiento/analítica.

La reorganización editorial de R3 no cambia por sí sola `2026-08-16.1`.

## 9. Historia

`docs/historico/normativa_privacidad/CUMPLIMIENTO_LEY_81_PRE_GOV1_3_R3.md`
