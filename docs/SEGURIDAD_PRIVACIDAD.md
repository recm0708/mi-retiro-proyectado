# Seguridad y privacidad

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.22-beta`
**Revisión documental:** GOV.1.3 R3 — 2026-08-17
**Clasificación:** Seguridad / Privacidad / Técnica
**Revisión externa:** Pendiente antes de beta pública

Este documento describe controles técnicos existentes. No constituye una auditoría de seguridad externa.

## 1. Modelo de ejecución

La aplicación está diseñada actualmente para ejecución local.

- FastAPI procesa cálculos;
- el navegador mantiene el estado de simulación;
- no existe base de datos permanente de simulaciones;
- no existen cuentas de usuario.

Un despliegue remoto cambia el modelo de amenazas y requiere revisión específica.

## 2. Datos en Web Storage

La simulación se guarda en `sessionStorage`.

El consentimiento utiliza dos piezas:

- `localStorage`: versión, aceptación y fecha técnica;
- `sessionStorage`: marca que activa esa aceptación para la sesión/pestaña actual.

La apariencia se recuerda en `localStorage`.

## 3. Archivos importados

Los PDF:

- se leen en memoria;
- no se persisten por los endpoints de importación;
- se someten a controles de extensión/MIME/firma/tamaño;
- tienen límites de páginas/texto;
- no deben entrar al repositorio si contienen datos personales reales.

La metadata de continuidad puede conservar el nombre visible del archivo, nunca su ruta local ni el binario.

## 4. Identificadores

Mi Retiro Seguro puede devolver identificadores opcionales cuando el parser los reconoce.

Ficha Digital no expone identidad en su contrato salarial.

Los identificadores no forman parte del cálculo previsional principal.

## 5. Cabeceras HTTP

El middleware actual establece:

- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options: DENY`;
- `Referrer-Policy: no-referrer`;
- `Permissions-Policy` restrictiva;
- Content Security Policy.

Las respuestas bajo `/api/simulacion/` usan `Cache-Control: no-store`.

## 6. Recursos externos

Bootstrap 5.3.8 se carga actualmente desde **cdn.jsdelivr.net** con Subresource Integrity y `crossorigin`.

Esto produce una conexión técnica del navegador al CDN y puede revelar metadatos ordinarios de red.

Servir dependencias críticas localmente continúa como objetivo pre-beta.

## 7. Verificación externa de fecha

El backend puede consultar por HTTPS infraestructura oficial de la CSS para leer el encabezado HTTP `Date`.

La solicitud:

- no incluye PDF;
- no incluye identidad;
- no incluye salarios/cuotas/resultados;
- puede exponer a la infraestructura consultada metadatos normales de red del servidor que ejecuta la aplicación.

Si la consulta falla, no se sustituye silenciosamente por la fecha local.

## 8. Cookies y seguimiento

La aplicación no implementa cookies propias de publicidad, analítica, seguimiento ni perfilado.

Tampoco incorpora actualmente herramientas de analítica/telemetría de producto.

La existencia de solicitudes a recursos externos se documenta por separado y no debe confundirse con inexistencia de conexiones de red.

## 9. Registros

En la versión actual no existe todavía el sistema de Developer Diagnostics de GOV.1.4.

Hasta implementarlo:

- no debe introducirse logging informal de PII;
- no deben registrarse cuerpos de PDF;
- no deben registrarse salarios/historial/identificadores;
- las trazas de error no deben exponerse al usuario final.

GOV.1.4 definirá el contrato real de observabilidad.

## 10. Gestión local

La interfaz implementa:

- limpiar paso;
- reiniciar simulación;
- borrar datos de la aplicación en este navegador.

El borrado integral elimina únicamente claves propiedad de Mi Retiro Proyectado.

## 11. CI y dependencias

CI ejecuta instalación/validación, `compileall`, sintaxis JavaScript y suite `unittest`.

Dependabot propone actualizaciones; no existe auto-merge.

Las actualizaciones de `pypdf` requieren revisión explícita de importadores.

## 12. Pendientes pre-beta

- threat model formal;
- procedimiento de incidentes;
- procedimiento de derechos del titular;
- revisión de logs/despliegue;
- servir dependencias críticas localmente cuando sea viable;
- TLS obligatorio para un servicio remoto;
- revisión de proveedores/terceros;
- revisión jurídica de textos;
- configuración endurecida de producción.

Estos pendientes pertenecen principalmente a GOV.1.5 y GOV.1.6.

## 13. Frontera de afirmación

Este documento registra controles observables en el repositorio.

No afirma:

- invulnerabilidad;
- certificación de seguridad;
- cumplimiento jurídico certificado;
- idoneidad automática para Internet.

## 14. Historia

`docs/historico/normativa_privacidad/SEGURIDAD_PRIVACIDAD_PRE_GOV1_3_R3.md`
