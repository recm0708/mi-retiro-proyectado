# Matriz interna de alineación con Ley 81 de 2019

**Estado:** Vigente como control interno
**Versión de aplicación revisada:** `0.0.71.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica:** `0.0.23-beta`
**Versión de privacidad revisada:** `2026-08-16.1`
**Base documental:** GOV.1.3 R3 — 2026-08-17
**Revisión transversal histórica:** GOV.1.5 R3 — 2026-08-18
**Última revisión documental:** PLAN.1 R3B1 — 2026-08-20
**Clasificación:** Privacidad / Cumplimiento interno
**Alcance:** No constituye certificación jurídica

La matriz sirve para detectar controles implementados y trabajo pendiente. Una fila “Implementado” significa que existe un control técnico/documental observable; no que un profesional jurídico haya certificado suficiencia legal.

## 1. Referencias

- Ley 81 de 26 de marzo de 2019;
- Decreto Ejecutivo 285 de 28 de mayo de 2021;
- orientaciones/preguntas frecuentes de ANTAI.

Fuentes: `regulatory-sources.md`.

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
| Derechos formales | Procedimiento interno documentado | Implementado documental GOV.1.5 |
| Portabilidad | Exportación estructurada | Pendiente de producto |
| Incidentes | Procedimiento interno documentado | Implementado documental GOV.1.5 |
| Logging/observabilidad | Contrato seguro + revisión threat model | Implementado base GOV.1.4/GOV.1.5 |
| TLS remoto | Obligatorio si existe despliegue remoto | Gate documentado; no aplica al localhost actual |
| Revisión jurídica | Revisión profesional | Pendiente antes de publicación de la primera versión oficial o de un cambio material del despliegue/tratamiento |

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

GOV.1.5 documenta el procedimiento interno, la verificación proporcional y el registro mínimo fuera de Git.

Los controles locales de borrado **no se presentan como sustituto** de ese procedimiento si en el futuro existe tratamiento remoto/persistente.

## 7. Pendientes obligatorios antes de la primera versión oficial

- revisión jurídica externa en REV.1;
- hardening y validación de un despliegue remoto concreto si se implementa;
- reevaluación de terceros antes de `1.0.0.0`;
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

`docs/archive/regulatory-privacy/CUMPLIMIENTO_LEY_81_PRE_GOV1_3_R3.md`
