# Evaluación de terceros, despliegue y revisión pre-publicación

**Estado:** Vigente — GOV.1.5 R3
**Versión de aplicación revisada:** `0.1.10.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Fecha de cierre interno original:** 2026-08-18
**Última revisión documental:** AUD.SEC2 R1 — 2026-08-25
**Clasificación:** Seguridad / Privacidad / Terceros / Despliegue
**Revisión jurídica externa:** Pendiente antes de la primera versión oficial o de un despliegue remoto

Este documento conserva la evaluación interna de terceros y despliegue cerrada en GOV.1.5 y actualiza su frontera futura. No declara que Mi Retiro Proyectado sea apto para exposición pública en Internet ni sustituye una revisión jurídica, de infraestructura o de seguridad externa.

## 1. Escenario soportado actualmente

El escenario soportado por la etapa beta actual es:

```text
navegador local → http://127.0.0.1:8000 → FastAPI/Uvicorn local
```

Uvicorn utiliza `127.0.0.1` como host predeterminado. Un `--host 0.0.0.0`, bind LAN, proxy inverso, contenedor publicado o exposición en Internet cambia la frontera de confianza y requiere una revisión de despliegue antes de considerarse soportado.

## 2. Inventario de terceros y conexiones

### jsDelivr / Bootstrap 5.3.8

Uso actual:

- CSS y JavaScript de Bootstrap;
- carga desde `cdn.jsdelivr.net`;
- versión fijada `5.3.8`;
- Subresource Integrity (SRI);
- `crossorigin="anonymous"`;
- dominio limitado por Content Security Policy.

Datos enviados intencionalmente por Mi Retiro Proyectado:

- **ningún dato de simulación**;
- **ningún PDF**;
- **ninguna cédula/NSS**;
- **ningún salario/cuota/resultado**.

Riesgo residual:

- disponibilidad del CDN;
- metadata ordinaria de red/navegador;
- dependencia de cadena de suministro.

Decisión histórica de GOV.1.5/GOV.1.8:

- riesgo aceptado temporalmente para desarrollo local;
- mantener SRI, versión fija y CSP;
- servir Bootstrap localmente sigue siendo la opción preferida antes de una distribución oficial amplia;
- SEC.2/REL.1 deben reevaluar esta excepción antes de `1.0.0.0`.

### Infraestructura oficial CSS para fecha de referencia

En este documento, la expresión **infraestructura CSS** se utiliza para referirse a esta fuente externa operativa.

Uso actual:

- consulta HTTPS mínima;
- lectura del encabezado HTTP `Date`;
- utilizada para evaluar vigencia de Ficha Digital.

No se envía:

- PDF;
- identidad;
- salario;
- cuotas;
- resultado previsional;
- estado de simulación.

Riesgos:

- disponibilidad;
- inconsistencia de respuestas;
- metadata ordinaria de red del equipo que realiza la consulta.

Control:

- resultado conservador cuando no existe referencia confiable;
- el servicio no se usa para transferir datos previsionales.

### GitHub

GitHub se utiliza para:

- repositorio;
- Pull Requests;
- GitHub Actions;
- Dependabot;
- auditoría de commits/tags.

GitHub **no forma parte del flujo runtime de la simulación**.

No deben subirse a GitHub:

- PDF personales;
- cédulas/NSS reales;
- historiales salariales reales;
- solicitudes de derechos reales;
- evidencia sensible de incidentes;
- logs diagnósticos reales con contenido sensible.

### Shields.io — badges del README

Uso actual:

- badges estáticos de versión, Python y licencia en `README.md`;
- solo afecta a la presentación del repositorio;
- no forma parte del runtime de la simulación.

No se envía intencionalmente:

- PDF;
- identidad;
- salario;
- cuotas;
- resultado previsional.

Riesgo residual: disponibilidad y metadata ordinaria asociada a la carga del recurso documental. El estado de CI y gobernanza usa badges propios de GitHub Actions.

## 3. TLS

### Localhost

El modo local actual utiliza HTTP en loopback. No se declara HSTS ni se fuerza HTTPS para desarrollo local.

### LAN o Internet

TLS pasa a ser obligatorio como requisito de diseño antes de considerar soportado un despliegue remoto.

Opciones técnicas posibles incluyen:

- terminación TLS en un proxy inverso confiable;
- HTTPS nativo de Uvicorn mediante certificado y clave;
- plataforma administrada que termine TLS de forma adecuada.

La elección concreta pertenece al diseño de despliegue futuro.

## 4. Certificados y secretos

En un despliegue remoto:

- certificados y claves privadas no se versionan;
- secretos no se incluyen en `.env` versionados;
- las claves deben almacenarse fuera del repositorio;
- la rotación debe estar definida;
- no deben aparecer en Developer Diagnostics;
- un secreto expuesto se trata como incidente.

## 5. Proxy y encabezados reenviados

Uvicorn puede utilizar `X-Forwarded-For` y `X-Forwarded-Proto` cuando está detrás de proxies.

Regla del proyecto:

- solo confiar en proxies/IP realmente controlados;
- preferir una lista explícita mediante configuración equivalente a `--forwarded-allow-ips`;
- no usar confianza global `"*"` salvo que la arquitectura demuestre que todos los valores llegan exclusivamente desde un proxy confiable que sanea los encabezados.

Confiar encabezados reenviados de clientes no confiables permite falsificar información de origen/esquema.

## 6. Host, CORS y CSRF

El diseño local no incorpora cuentas de usuario ni persistencia de simulaciones, pero SEC.2 sí añadió una sesión administrativa temporal en memoria y la cookie técnica `mrp_admin_session`.

AUD.SEC2 R1 confirma que `MRP_ADMIN_ENABLED` conserva prioridad, que el logout usa POST y que la cookie no sustituye estados 403. Si se amplía cualquiera de estos elementos:

- exposición remota;
- autenticación;
- cookies/sesión de servidor;
- base de datos;
- API consumida desde otro origen;

deben revisarse explícitamente:

- hosts permitidos;
- CORS;
- CSRF;
- cookies `Secure`, `HttpOnly` y `SameSite`;
- autenticación/autorización;
- rate limiting;
- límites de upload;
- protección de proxy/Host;
- política de sesión.

No se añadirá CORS permisivo `"*"` por comodidad.

## 7. Cabeceras defensivas actuales

El middleware vigente mantiene:

- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options: DENY`;
- `Referrer-Policy: no-referrer`;
- `Permissions-Policy` restrictiva;
- `Content-Security-Policy`;
- `Cache-Control: no-store` en `/api/simulacion/` y `/dev/`.

Estas cabeceras son defensa en profundidad. No reemplazan TLS, autenticación ni controles de infraestructura cuando exista un despliegue remoto.

## 8. Developer Diagnostics — revisión GOV.1.5

La revisión de seguridad confirma que el contrato definido en GOV.1.4 sigue siendo apropiado para desarrollo local:

- apagado por defecto;
- activación explícita `MRP_DEV_MODE=1`;
- no request/response bodies;
- no PDF/texto extraído;
- no PII;
- no valores financieros;
- no cookies/tokens;
- no mensajes originales de excepción potencialmente sensibles;
- correlation IDs aleatorios;
- rotación y retención acotada;
- exportación explícita.

Riesgo residual:

- un archivo exportado puede ser copiado fuera de su ubicación controlada;
- una futura metadata nueva podría introducir datos sensibles si no se revisa;
- un equipo local comprometido puede leer archivos locales.

Por ello, toda ampliación del esquema de logs reabre revisión de seguridad.

## 9. Revisión jurídica externa

GOV.1.5 completa la **preparación interna**, no la revisión jurídica profesional.

Antes de la primera versión oficial o de soportar un despliegue remoto deben entregarse para revisión, como mínimo:

- `privacy-policy.md`;
- `terms-and-privacy.md`;
- `law-81-compliance.md`;
- `data-subject-rights-procedure.md`;
- `security-incident-procedure.md`;
- `threat-model.md`;
- este documento;
- inventario real de terceros;
- arquitectura de despliegue prevista.

La revisión debe evaluar el tratamiento real del producto y no solo el texto documental.

## 10. Versión material de privacidad

La versión vigente sigue siendo:

```text
2026-08-16.1
```

Evaluación interna de GOV.1.5:

- no se introduce una nueva finalidad de tratamiento;
- no se añade una nueva categoría de datos personales;
- no se añade un nuevo destinatario de la simulación;
- no se crea persistencia remota;
- no se incorpora analítica/publicidad/perfilado;
- los procedimientos de derechos e incidentes formalizan controles;
- Developer Diagnostics ya estaba implementado y su contrato prohíbe datos personales/financieros.

Por estas razones **no se identifica internamente un cambio material que obligue por sí solo a incrementar la versión de privacidad**.

Esta conclusión no es certificación jurídica y debe revisarse si un profesional externo determina lo contrario.

## 11. Gates antes de exposición remota

No declarar un despliegue remoto como soportado hasta completar y evidenciar:

1. arquitectura de hosting;
2. TLS válido;
3. secretos fuera de Git;
4. proxy/forwarded headers confiables;
5. hosts/CORS/CSRF según arquitectura;
6. límites de tráfico/upload;
7. acceso y retención de logs;
8. procedimiento de incidentes operativo;
9. backups/persistencia si existen;
10. revisión de terceros;
11. revisión jurídica externa;
12. pruebas de seguridad del despliegue.

## 12. Cierre interno de GOV.1.5

Con R1, R2 y R3 quedaron documentados internamente:

- threat model;
- derechos del titular;
- incident response;
- revisión de logs;
- terceros;
- criterios TLS/despliegue;
- frontera de revisión jurídica.

La revisión jurídica externa y la preparación de un despliegue remoto siguen siendo **gates pendientes**, no tareas que se declaren realizadas sin evidencia.

> **Nota posterior — PLAN.1 R3A:** la expresión histórica “beta pública” deja de utilizarse como gate futuro vigente. El proyecto ya se encuentra en etapa beta `0.0.N-beta`; la frontera futura de producto es `1.0.0.0`. Esta aclaración no reescribe el cierre GOV.1.5.
