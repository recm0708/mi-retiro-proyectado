# Seguridad y privacidad

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.17.02-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Base documental preservada:** GOV.1.3 R3 — 2026-08-17
**Revisión transversal histórica:** repositorio público y controles GitHub — 2026-08-19
**Última revisión documental:** AUD.SEC2 R1 — 2026-08-25
**Clasificación:** Seguridad / Privacidad / Técnica
**Revisión externa:** Pendiente antes de la primera versión oficial o de cualquier despliegue remoto que cambie el modelo de riesgo

Este documento describe controles técnicos existentes. No constituye una auditoría de seguridad externa.

## 1. Modelo de ejecución

La aplicación está diseñada actualmente para ejecución local.

- FastAPI procesa cálculos;
- el navegador mantiene el estado de simulación;
- no existe base de datos permanente de simulaciones;
- no existen cuentas de usuario.

La visibilidad pública del repositorio no cambia este modelo de ejecución. Un despliegue remoto cambia el modelo de amenazas y requiere revisión específica.

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

Servir dependencias críticas localmente continúa como objetivo antes de la primera versión oficial y se revisará específicamente en SEC.2/REL.1.

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

La superficie administrativa sí utiliza `mrp_admin_session`, una cookie técnica `HttpOnly` de sesión temporal cuando `MRP_ADMIN_ENABLED=1`. No transporta información previsional; `SameSite` es configurable y `Secure` debe activarse en HTTPS interno.

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

Consultar `observability-and-logs.md`.

## 10. Gestión local

La interfaz implementa:

- limpiar paso;
- reiniciar simulación;
- borrar datos de la aplicación en este navegador.

El borrado integral elimina únicamente claves propiedad de Mi Retiro Proyectado. Puede reconocer identificadores pre-beta conocidos exclusivamente para purgarlos, sin leerlos ni migrarlos. Al eliminar la constancia de consentimiento, la interfaz vuelve a presentar las condiciones desde Inicio y Simular sigue bloqueado mientras no exista una aceptación vigente. Los logs diagnósticos, cuando se han activado explícitamente, son archivos locales de desarrollo y se gestionan por separado.

## 11. CI, dependencias y seguridad del repositorio público

CI ejecuta instalación/validación, `compileall`, sintaxis JavaScript y suite `unittest`.

Dependabot propone actualizaciones; no existe auto-merge.

Las actualizaciones de `pypdf` requieren revisión explícita de importadores.

Después de convertir el repositorio en público se confirmaron:

- Dependency graph;
- Dependabot alerts;
- Dependabot security updates;
- CodeQL con Default setup;
- Secret Protection / secret scanning;
- Push protection;
- Private vulnerability reporting.

La revisión manual del 2026-08-19 mostró cero alertas abiertas en Code scanning, Secret scanning y Dependabot. Este resultado es una evidencia puntual, no una garantía permanente; los paneles deben seguir revisándose.

## 12. Pendientes antes de la primera versión oficial

GOV.1.5 completó internamente el threat model, los procedimientos de derechos/incidentes, la revisión de logs y la evaluación de terceros/TLS. Permanecen pendientes, según el alcance final de producto:

- servir dependencias críticas localmente cuando corresponda;
- revisión jurídica externa de textos, privacidad, licencia y publicación de producto;
- hardening y configuración de producción para un despliegue remoto concreto;
- auditoría de seguridad adicional si cambia la arquitectura, persistencia, red o modelo multiusuario;
- REV.1 y la revisión jurídica/seguridad final en los términos definidos por el plan maestro; SEC.2 ya está cerrado después de R1–R6.

## 12.1. Cierre interno GOV.1.5

Documentos de control vigentes:

- `threat-model.md`;
- `data-subject-rights-procedure.md`;
- `security-incident-procedure.md`;
- `third-party-deployment-assessment.md`;
- `observability-and-logs.md`.

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

La revisión de GOV.1.5 se originó sobre `0.0.23-beta`. La posterior apertura pública del repositorio y PLAN.1 no reescriben ese cierre; actualizan únicamente el estado vivo y los gates futuros.

`docs/archive/regulatory-privacy/security-and-privacy-pre-gov1-3-r3.md`

## Controles administrativos post-SEC.2

`MRP_ADMIN_ENABLED` es la condición primaria de disponibilidad de la superficie
administrativa. El secreto se obtiene de `MRP_ADMIN_SECRET` (o compatibilidad
`MRP_ADMIN_TOKEN`) y nunca se versiona. AUD.SEC2 R1 garantiza que el login POST
y las sesiones existentes respeten el kill switch, que el logout sea POST y que
`/dev/` use `Cache-Control: no-store`.
