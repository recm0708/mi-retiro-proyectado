# SEC.2 — Cierre integral y auditoría post-cierre de seguridad

**Proyecto:** Mi Retiro Proyectado
**Estado:** SEC.2 cerrado; saneamiento post-cierre en AUD.SEC2 R1
**Alcance completado:** SEC.2 R1–R6
**Snapshot auditado:** `4bd7d8d57c8ccf6229ff2e53493c996b29db14a2`
**Fecha de reconciliación:** 2026-08-25
**Clasificación:** Auditoría / Seguridad / Evidencia de cierre

## 1. Objetivo

SEC.2 estableció y endureció los controles aplicables a la arquitectura beta
actual sin modificar motores previsionales ni parámetros normativos. Esta
evidencia registra el cierre R1–R6 y la auditoría posterior que detectó una
regresión del kill switch administrativo antes de abrir DOC.2.

## 2. Revisiones cerradas

- **R1:** hardening CodeQL y normalización de workflows.
- **R2:** autenticación administrativa y gestión del secreto externo.
- **R3:** protección centralizada de endpoints administrativos.
- **R4:** auditoría y observabilidad de accesos sin registrar credenciales.
- **R5:** login web y sesión administrativa temporal.
- **R6:** expiración, límite de sesiones y atributos de cookie configurables para
  despliegue interno HTTPS.

El commit `4bd7d8d` consolidó el cierre formal sin constituir una revisión de
seguridad adicional a R1–R6.

## 3. Matriz del alcance maestro SEC.2

| Área del plan | Estado al cierre | Evidencia / decisión |
|---|---|---|
| Autenticación y sesiones administrativas | Implementado | `app/core/admin_security.py`, `app/core/admin_session.py`, `/dev/login` |
| Gestión de secretos | Implementado | `MRP_ADMIN_SECRET`; compatibilidad `MRP_ADMIN_TOKEN`; ningún secreto fijo en Git |
| Kill switch administrativo | Corregido post-cierre | `MRP_ADMIN_ENABLED=1` requerido para login y reutilización de sesión; regresión AUD.SEC2 R1 |
| CSP y cabeceras defensivas | Implementado antes de SEC.2 y conservado | middleware HTTP; regresiones de privacidad/seguridad |
| CORS | No se habilita CORS permisivo | La arquitectura local no requiere consumo cross-origin; cualquier ampliación exige revisión |
| CSRF | Evaluado para la superficie real | sesión admin `SameSite` configurable; logout POST; reevaluación obligatoria si `SameSite=None` o despliegue remoto |
| Seguridad de archivos/PDF | Implementado antes de SEC.2 y conservado | firma/MIME/tamaño/páginas/texto y procesamiento en memoria |
| Permisos y artefactos locales | Implementado por gobierno/NOR.2 | logs y entregables locales excluidos; secretos fuera de Git |
| Endurecimiento del servidor | Parcial para localhost / condicionado a despliegue | localhost soportado; proxy, Host, TLS y rate limiting se revisan para una topología remota concreta |
| Bootstrap/CDN | Riesgo residual documentado | Bootstrap fijado con SRI+CSP; servir localmente se reevalúa antes de distribución oficial en REL.1 |
| Dependencias | Implementado como control continuo | pins, `pip check`, Dependabot, CI y revisión explícita de parser PDF |
| SBOM/inventario | Inventario disponible; SBOM final diferido | `requirements.txt`/`THIRD_PARTY_NOTICES.md`; SBOM de artefacto oficial corresponde a REL.1 |
| Seguridad de persistencia | No aplicable a simulaciones actuales | no existe base de datos ni guardado servidor de simulaciones; PERSIST.1 deberá reabrir el control |
| Cifrado de datos persistentes | No aplicable actualmente | no existe persistencia de simulaciones; PERSIST.1 definirá cifrado/protección si se incorpora |
| Despliegue remoto | Evaluado, no declarado listo para Internet | `third-party-deployment-assessment.md`, `threat-model.md`; R6 prepara cookie Secure para HTTPS interno |
| Multi-instancia | No soportado todavía | sesiones admin viven en memoria; despliegue multi-worker requiere backend compartido y nueva revisión |

## 4. Hallazgo AUD.SEC2 R1

La auditoría posterior al cierre encontró que `POST /dev/login` podía crear una
sesión cuando `MRP_ADMIN_ENABLED` no estaba activo y que el fallback de cookie en
`/dev/centro-desarrollo` podía sustituir respuestas `403`. Además, logout
modificaba estado mediante GET.

La remediación del paquete AUD.SEC2 R1:

1. exige `administracion_activa()` también en POST `/dev/login`;
2. exige autenticación configurada en GET y POST del login;
3. admite fallback de cookie únicamente frente a ausencia de Bearer (`401`) y
   solo si administración y autenticación siguen activas;
4. no permite que una sesión sustituya un `403` de política;
5. cambia logout a `POST /dev/logout`;
6. aplica `Cache-Control: no-store` a `/dev/`;
7. agrega regresiones específicas para estos contratos.

## 5. Cookie administrativa

`mrp_admin_session` es una cookie **técnica**, no una cookie de analítica,
publicidad o perfilado. Su contrato vigente es:

- `HttpOnly=true`;
- `SameSite` configurable, `lax` por defecto;
- `Secure` configurable y obligatorio para HTTPS interno;
- `max-age` asociado al timeout de inactividad;
- identificador aleatorio sin datos personales ni datos previsionales;
- sesión mantenida solo en memoria del proceso.

La aplicación no contiene una clave administrativa predeterminada. La credencial
la define el operador mediante `MRP_ADMIN_SECRET` fuera del repositorio.

## 6. Validación

El cierre R6 registró **1028 pruebas en OK**. Durante AUD.SEC2 R1, la suite focal
SEC.2 del paquete ejecutó **33 pruebas en OK** antes de preparar la integración.
El gate integral definitivo debe ejecutarse con las dependencias pinneadas del
`.venv` del repositorio y repetirse después del merge.

## 7. Resultado y frontera

SEC.2 permanece **cerrado en R1–R6**; AUD.SEC2 R1 es una remediación/auditoría
post-cierre y no se denomina artificialmente “R7”. El bloque no declara la
aplicación lista para Internet, no incorpora persistencia de simulaciones y no
sustituye REV.1 ni REL.1.

La reconciliación revision-aware sitúa el snapshot de cierre `4bd7d8d` en G108.
G109/E01 (`0.1.09.01-beta`) queda reservado para AUD.SEC2 R1 y solo será aceptado
después de gate, commit firmado, PR/CI e integración.


## Addendum de aceptación AUD.SEC2 R1

La remediación post-cierre fue aceptada mediante PR #83 y merge `ec1842dac10a5395fb594223d31092fdee3cdfc1`. AUD.SEC2 R1 queda materializado como G109/E01 (`0.1.09.01-beta`) sin reabrir SEC.2. G110/E01 queda disponible para DOC.2.
