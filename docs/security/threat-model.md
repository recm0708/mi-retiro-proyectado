# Modelo de amenazas

**Estado:** GOV.1.5 R1 — vigente como modelo técnico interno
**Versión de aplicación revisada:** `0.0.71.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Fecha de cierre original:** 2026-08-17
**Última revisión documental:** AUD.SEC2 R1 — 2026-08-25
**Clasificación:** Seguridad / Privacidad / Riesgo
**Revisión externa:** Pendiente antes de la primera versión oficial o de cualquier despliegue remoto que cambie el modelo de riesgo

Este documento modela amenazas observables para la arquitectura actual de Mi Retiro Proyectado. No constituye auditoría de penetración, certificación de seguridad, dictamen jurídico ni garantía de riesgo cero.

## 1. Alcance actual

El modelo cubre la aplicación en su **etapa beta y modo local soportado**:

- aplicación web servida por FastAPI;
- uso principal en `localhost`;
- navegador como contenedor del estado temporal de simulación;
- ausencia de cuentas de usuario final;
- sesión administrativa web temporal en memoria, habilitada solo mediante configuración explícita;
- ausencia de base de datos permanente de simulaciones;
- importación voluntaria de documentos PDF procesados en memoria;
- Developer Diagnostics local y apagado por defecto;
- consulta HTTPS mínima a infraestructura CSS para fecha de referencia;
- carga actual de Bootstrap desde jsDelivr;
- repositorio GitHub y CI como cadena de desarrollo, no como runtime del asegurado.

Un despliegue remoto, multiusuario o con persistencia cambia materialmente este modelo y exige una revisión antes de considerarse soportado.

## 2. Objetivos de seguridad

### Confidencialidad

Evitar divulgación innecesaria de:

- identidad opcional;
- fecha de nacimiento;
- historia salarial;
- cuotas;
- resultados previsionales;
- documentos seleccionados;
- metadata diagnóstica.

### Integridad

Evitar alteración no detectada de:

- parámetros normativos;
- código de motores;
- dependencias;
- documentos de entrada;
- resultados intermedios;
- versión y artefactos de release.

### Disponibilidad

Mantener degradación controlada cuando fallen:

- fuentes externas de fecha;
- recursos CDN;
- documentos incompatibles;
- entradas excesivas o malformadas.

### Trazabilidad

Poder reconstruir decisiones técnicas y fallos sin crear una segunda base de datos con información personal.

## 3. Activos

| Activo | Sensibilidad | Ubicación/vida actual | Objetivo principal |
|---|---|---|---|
| Datos de identidad opcionales | Alta | Estado temporal del navegador / request en memoria | Confidencialidad |
| Fecha de nacimiento, sexo, ingreso CSS | Alta | Estado temporal / modelos de request | Confidencialidad e integridad |
| Cuotas e historial salarial | Alta | Estado temporal / request en memoria | Confidencialidad e integridad |
| Resultados previsionales | Alta | Estado temporal / response | Confidencialidad e integridad |
| PDF seleccionado | Alta | Memoria durante importación | Confidencialidad e integridad |
| Estado de consentimiento | Media | `localStorage` + `sessionStorage` | Integridad |
| Preferencias visuales | Baja | `localStorage` | Disponibilidad/UX |
| Logs Developer Diagnostics | Media | `logs/diagnostico/` solo si se activa | Confidencialidad |
| Parámetros `regulations/*.json` | Alta para exactitud | Repositorio / runtime | Integridad |
| Código de motores y servicios | Alta para exactitud | Repositorio / runtime | Integridad |
| Dependencias Python/Bootstrap | Alta para cadena de suministro | Entorno / CDN | Integridad |
| Historial Git, tags y CI | Alta para auditoría | GitHub/local | Integridad y trazabilidad |
| Secreto y sesión administrativa | Alta | variable de entorno + memoria del proceso / cookie HttpOnly | Confidencialidad e integridad |

## 4. Fronteras de confianza

### F1 — Navegador ↔ FastAPI local

Cruzan datos de simulación y resultados.

Controles actuales:

- contratos Pydantic;
- validación de entrada;
- `Cache-Control: no-store` en API de simulación;
- `Content-Security-Policy` (CSP) y cabeceras defensivas;
- la simulación pública no usa cookie de autenticación; la superficie `/dev/` usa la cookie técnica administrativa `mrp_admin_session`, `HttpOnly`;
- sin persistencia automática de requests/responses.

### F2 — Archivo elegido ↔ Parser PDF

El documento es entrada no confiable aunque proceda de una fuente conocida.

Controles actuales:

- extensión/MIME/firma;
- tamaño máximo;
- límites de páginas;
- límites de texto;
- rechazo de cifrado/formato no procesable;
- procesamiento en memoria;
- revisión humana antes de aplicar datos.

### F3 — Runtime ↔ Sistema de archivos diagnóstico

Solo existe con `MRP_DEV_MODE=1`.

Controles actuales:

- modo apagado por defecto;
- JSONL sanitizado;
- prohibición de PII/valores financieros;
- rotación y retención acotada;
- directorio excluido de Git;
- exportación explícita y limitada.

### F4 — Backend ↔ Infraestructura CSS

Se utiliza para obtener una referencia temporal.

Controles actuales:

- HTTPS;
- no envío de PDF;
- no envío de identidad;
- no envío de salarios/cuotas/resultados;
- comportamiento conservador si no hay respuesta confiable.

### F5 — Navegador ↔ jsDelivr

Se solicita Bootstrap desde CDN.

Controles actuales:

- Subresource Integrity;
- `crossorigin`;
- CSP explícita.

Riesgo residual: disponibilidad del tercero y exposición de metadata ordinaria de red.

### F6 — Repositorio/CI ↔ Cadena de suministro

Incluye Git, GitHub, Actions y dependencias.

Controles actuales:

- commits/tags gobernados por firma;
- rulesets;
- PR obligatorio;
- CI requerida;
- Dependabot sin auto-merge;
- versiones Python fijadas en `requirements.txt`.

## 5. Matriz de amenazas

| ID | Amenaza | Superficie | Impacto | Probabilidad actual | Riesgo | Controles existentes | Riesgo residual / acción |
|---|---|---|---|---|---|---|---|
| T-01 | PDF malformado o deliberadamente hostil | Parser/importación | Alto | Media | Alto | límites de tamaño/páginas/texto, firma PDF, pypdf actualizado, pruebas | mantener revisión explícita de parser y dependencias |
| T-02 | Divulgación de datos por logging | Developer Diagnostics | Alto | Baja con modo apagado | Medio | `MRP_DEV_MODE=1`, sanitización, no bodies, no mensajes de excepción | revisar esquema cada vez que se añada metadata |
| T-03 | Exposición accidental al ejecutar fuera de localhost | Servidor ASGI | Alto | Baja en uso actual | Medio | diseño local documentado | cualquier bind público exige TLS, autenticación/controles y nuevo threat model |
| T-04 | XSS o inyección en contenido renderizado | Navegador/plantillas | Alto | Baja/Media | Medio | Jinja2, CSP, validación, sin HTML dinámico arbitrario previsto | revisar cambios que introduzcan HTML no confiable |
| T-05 | Dependencia/CDN comprometida o indisponible | Bootstrap/jsDelivr | Medio/Alto | Baja | Medio | SRI + CSP | servir recursos críticos localmente antes de `1.0.0.0`, salvo excepción revisada en SEC.2/REL.1 |
| T-06 | Alteración de normativa/código | Repositorio | Alto | Baja | Medio | firma, rulesets, PR, CI, historial | mantener revisión humana de cambios normativos |
| T-07 | Robo/lectura del estado del navegador por software local o extensión | Web Storage | Alto | Dependiente del equipo | Medio | `sessionStorage`, minimización, limpieza | el proyecto no controla un equipo ya comprometido |
| T-08 | Fuga de PDF por persistencia accidental | Importador | Alto | Baja | Medio | procesamiento en memoria; no persistencia del binario | reevaluar si se añade persistencia/exportación |
| T-09 | Fuente CSS caída, inconsistente o manipulada | Fecha externa | Medio | Media | Medio | HTTPS, comparación de respuestas, estado no confiable | no declarar vigencia cuando la referencia no es confiable |
| T-10 | Denegación de servicio por entradas excesivas | Upload/API | Medio | Media | Medio | límites de upload, páginas y texto | despliegue remoto requerirá límites adicionales/proxy |
| T-11 | CSRF contra sesión administrativa | `/dev/` | Medio | Baja en localhost | Bajo/Medio | `SameSite` configurable, logout POST, superficie deshabilitada por defecto y sin CORS permisivo | exigir revisión específica si se usa `SameSite=None` o despliegue remoto |
| T-12 | Clickjacking | UI | Medio | Baja | Bajo | `X-Frame-Options: DENY`, CSP `frame-ancestors 'none'` | mantener regresiones |
| T-13 | Exposición mediante caché HTTP | API de simulación | Alto | Baja | Bajo/Medio | `Cache-Control: no-store` | revisar nuevas rutas sensibles |
| T-14 | Manipulación de resultados en JavaScript | Presentación | Alto | Baja | Medio | fórmulas principales solo en Python, motores separados | no duplicar fórmulas de dominio en frontend |
| T-15 | Dependencia vulnerable o actualización incompatible | Python/Actions | Alto | Media | Medio | pins, `pip check`, CI, Dependabot, revisión controlada | evaluación explícita de actualizaciones mayores |

## 6. Amenazas fuera del control directo del producto

La arquitectura actual no puede proteger por sí sola contra:

- sistema operativo comprometido;
- navegador o extensión maliciosa con acceso local;
- malware que lea memoria/archivos del usuario;
- captura de pantalla por terceros;
- proxy corporativo o dispositivo que intercepte tráfico permitido;
- usuario que publique voluntariamente un documento o log.

Estas condiciones no se usan como excusa para reducir controles internos; delimitan la frontera técnica del producto.

## 7. Developer Diagnostics dentro del threat model

Developer Diagnostics se considera una superficie propia.

Reglas:

1. no activar por defecto;
2. no registrar cuerpos HTTP;
3. no registrar modelos completos;
4. no registrar PDF ni texto extraído;
5. no registrar nombre, cédula, NSS, fechas personales, salarios, cuotas detalladas o montos;
6. no registrar cookies, tokens o headers completos;
7. no persistir mensajes originales de excepción;
8. usar correlation IDs aleatorios;
9. conservar logs localmente;
10. reevaluar el esquema si se añade un nuevo campo.

Un log exportado deja de estar protegido por la ubicación original y debe tratarse como artefacto técnico potencialmente sensible aunque el contrato prohíba PII.

## 8. Terceros y conexiones externas

### jsDelivr

Riesgos considerados:

- disponibilidad;
- cadena de suministro;
- metadata ordinaria de red.

Control actual: SRI + CSP.

### CSS

Riesgos considerados:

- disponibilidad;
- inconsistencia temporal;
- metadata ordinaria de red del equipo/servidor que realiza la consulta.

La consulta no transporta datos de la simulación.

### GitHub

GitHub aloja código y ejecuta CI/Dependabot. No forma parte del flujo de datos de simulación del usuario final.

## 9. Privacidad por diseño

El threat model refuerza estas decisiones:

- identificadores personales no son necesarios para las fórmulas principales;
- no existe base de datos permanente de casos;
- el PDF se procesa en memoria;
- la importación requiere revisión;
- la simulación vive temporalmente en el navegador;
- la observabilidad evita datos de negocio;
- conexiones externas se minimizan y documentan.

## 10. Riesgo de despliegue

### Localhost

Es el escenario soportado por el modelo actual.

### LAN

No debe asumirse equivalente a localhost. Expone el servicio a otros equipos de la red y requiere revisión de bind, firewall, hosts permitidos y acceso.

### Internet

No se considera listo para exposición pública.

Antes de un despliegue remoto se debe revisar al menos:

- TLS obligatorio;
- terminación TLS/proxy;
- autenticación/autorización si existe información persistente o sesiones;
- CORS y CSRF según arquitectura real;
- límites de tasa y tamaño;
- protección de Host/header forwarding;
- gestión de secretos;
- retención y acceso a logs;
- backups/persistencia;
- monitoreo;
- incident response;
- proveedores;
- jurisdicción/transferencias;
- revisión jurídica.

## 11. Disparadores de revisión

Reabrir este modelo cuando cambie cualquiera de estos elementos:

- ejecución fuera de localhost;
- cuentas/autenticación;
- base de datos;
- guardado voluntario persistente;
- nube/sincronización;
- analítica o telemetría;
- nuevo tercero;
- nuevo formato de documento;
- OCR;
- exportación automática;
- nueva ruta que trate datos personales;
- cambio material en Developer Diagnostics;
- cambio de CDN/recursos externos;
- incidente de seguridad;
- vulnerabilidad material de dependencia;
- cambio normativo aplicable.

## 12. Criterio de severidad

La prioridad considera impacto y probabilidad dentro del escenario actual.

- **Alto:** puede comprometer datos o integridad del cálculo y requiere control antes de ampliar exposición.
- **Medio:** existe mitigación relevante, pero permanece riesgo residual o dependencia operativa.
- **Bajo:** el diseño actual reduce fuertemente la superficie; debe reevaluarse si cambia la arquitectura.

La clasificación es una herramienta interna de priorización, no una puntuación certificada.

## 13. Cierre de R2/R3 de GOV.1.5

Las revisiones posteriores completaron los elementos que este modelo había dejado abiertos:

- procedimiento de incidentes;
- procedimiento para derechos del titular;
- registro mínimo de solicitudes sin almacenamiento innecesario;
- revisión de terceros;
- criterios TLS/despliegue;
- revisión de Developer Diagnostics desde seguridad;
- frontera de revisión jurídica;
- actualización transversal de seguridad, privacidad, transparencia, cumplimiento, roadmap y validación.

Los documentos vigentes relacionados se enumeran en `README.md`. La revisión jurídica externa y cualquier hardening de un despliegue remoto concreto permanecen como gates previos a la primera versión oficial o al despliegue que los requiera.

La versión base de esta revisión técnica es `0.0.23-beta`; el cierre integral posterior de GOV.1 se materializó en `0.0.24-beta`.

> **Nota posterior — PLAN.1 R3B2 / 2026-08-20:** el estado vivo se revisó sobre `0.0.25-beta`. La terminología histórica de GOV.1.5 no se interpreta como una etapa actual “pre-beta”; el producto se encuentra en la línea beta `0.0.N-beta`.

## Revisión de amenaza administrativa post-SEC.2

SEC.2 R5/R6 introdujo una sesión administrativa temporal que no existía cuando
se redactó el modelo original. AUD.SEC2 R1 incorpora explícitamente:

- **T-16 — bypass del kill switch:** mitigado exigiendo `MRP_ADMIN_ENABLED=1`
  tanto en GET/POST de login como al aceptar cookie de sesión;
- **T-17 — robo/reutilización de sesión administrativa:** mitigado mediante ID
  aleatorio, `HttpOnly`, expiración por inactividad, vida absoluta, límite de
  sesiones y `Secure` configurable para HTTPS;
- **T-18 — inconsistencia multi-worker:** las sesiones viven en memoria del
  proceso; un despliegue multi-instancia requiere backend compartido y nueva
  revisión antes de declararse soportado.

La cookie administrativa no convierte la aplicación en un sistema de cuentas de
usuarios ni crea persistencia de simulaciones.
