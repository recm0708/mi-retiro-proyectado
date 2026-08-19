# Seguridad y privacidad

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.23-beta`
**Base documental preservada:** GOV.1.3 R3 — 2026-08-17
**Revisión transversal vigente:** GOV.1.5 R3 — 2026-08-18
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

Los identificadores no forman parte del cálculo previsional principal ni de Developer Diagnostics.

## 5. Cabeceras HTTP

El middleware actual establece:

- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options: DENY`;
- `Referrer-Policy: no-referrer`;
- `Permissions-Policy` restrictiva;
- Content Security Policy.

Las respuestas bajo `/api/simulacion/` usan `Cache-Control: no-store`.

Cuando `MRP_DEV_MODE=1`, las operaciones instrumentadas pueden añadir `X-Correlation-ID`, generado aleatoriamente y no derivado del usuario.

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

Developer Diagnostics registra únicamente metadata agregada de cache, cantidad de fuentes, outcome y duración; no registra URL, fecha recibida ni encabezados.

## 8. Cookies y seguimiento

La aplicación no implementa cookies propias de publicidad, analítica, seguimiento ni perfilado.

Tampoco incorpora herramientas de analítica o telemetría de producto.

Developer Diagnostics es una herramienta local de desarrollo y no un mecanismo de seguimiento de usuarios.

## 9. Developer Diagnostics

GOV.1.4 define un sistema estructurado de diagnóstico que:

- está desactivado por defecto;
- requiere `MRP_DEV_MODE=1`;
- escribe JSONL local bajo `logs/diagnostico/` por defecto;
- usa correlation IDs aleatorios;
- rota aproximadamente a 1 MiB y conserva hasta tres respaldos;
- no realiza telemetría remota automática;
- permite exportación ZIP explícita solo de los JSONL reconocidos.

Está prohibido registrar:

- cuerpos de solicitudes/respuestas;
- contenido o texto extraído de PDF;
- nombre, cédula, NSS, correo o teléfono;
- fecha de nacimiento;
- salarios, cuotas detalladas, balances o montos de pensión;
- cookies, tokens o credenciales;
- mensajes originales de excepciones potencialmente sensibles.

La sanitización automática es defensa adicional y no autoriza a pasar datos sensibles al logger.

Consultar `OBSERVABILIDAD_LOGS.md`.

## 10. Gestión local

La interfaz implementa:

- limpiar paso;
- reiniciar simulación;
- borrar datos de la aplicación en este navegador.

El borrado integral elimina únicamente claves propiedad de Mi Retiro Proyectado. Los logs diagnósticos, cuando se han activado explícitamente, son archivos locales de desarrollo y se gestionan por separado.

## 11. CI y dependencias

CI ejecuta instalación/validación, `compileall`, sintaxis JavaScript y suite `unittest`.

Dependabot propone actualizaciones; no existe auto-merge.

Las actualizaciones de `pypdf` requieren revisión explícita de importadores.

## 12. Pendientes pre-beta

GOV.1.5 completó internamente el threat model, los procedimientos de derechos/incidentes, la revisión de logs y la evaluación de terceros/TLS. Permanecen pendientes, según el alcance final de publicación:

- servir dependencias críticas localmente cuando corresponda;
- revisión jurídica externa de textos, privacidad, licencia y publicación;
- hardening y configuración de producción para un despliegue remoto concreto;
- auditoría de seguridad adicional si cambia la arquitectura, persistencia, red o modelo multiusuario.

## 12.1. Cierre interno GOV.1.5

Documentos de control vigentes:

- `MODELO_AMENAZAS.md`;
- `PROCEDIMIENTO_DERECHOS_TITULAR.md`;
- `PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md`;
- `EVALUACION_TERCEROS_DESPLIEGUE.md`;
- `OBSERVABILIDAD_LOGS.md`.

La aplicación continúa orientada a localhost. Un despliegue LAN/Internet exige diseño específico, TLS y nueva revisión de seguridad.

La revisión jurídica externa **no se declara completada**.

## 13. Frontera de afirmación

Este documento registra controles observables en el repositorio.

No afirma:

- invulnerabilidad;
- certificación de seguridad;
- cumplimiento jurídico certificado;
- idoneidad automática para Internet.

## 14. Historia

`docs/historico/normativa_privacidad/SEGURIDAD_PRIVACIDAD_PRE_GOV1_3_R3.md`
