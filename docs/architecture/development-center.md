# DEV.2 R1/R2/R3/R4/R5/R6 — Centro de desarrollo

**Estado general:** DEV.2 R1–R4 preservados; R5 integrado, aceptado y publicado como G118/E04; R6 integrado mediante PR #111 / merge `bd2accb` y aceptado/publicado como G119/E05.

**Estado R1:** integrado en `main` mediante PR #37.

**Estado R1 documental:** integrado en `main` mediante PR #38.

**Estado R2:** integrado en `main` mediante PR #39.

**Estado R3:** integrado en `main` mediante PR #40.


<!-- DOC1-R1-REVISION-MANUAL:START -->
## Nota de lectura post-MANT.1

DEV.2 conserva su historia R1–R5 y queda cerrado funcionalmente después de R6.

Estado vigente:

- R1–R4 quedan preservados.
- R5 está integrado mediante PR #107 / merge `bc97db0`, aceptado como G118/E04
  y publicado mediante `v0.1.18.04-beta`.
- R6 está integrado mediante PR #111 / merge `bd2accb` y se materializa
  como G119/E05 (`0.1.19.05-beta`).
- G120/E01 (`0.1.20.01-beta`) queda reservado para UX.5 R1.
- La sesión humana Developer permanece separada del contrato Bearer técnico.
- SEC.2 R1–R6 permanece cerrado y SEC.2 R7 se mantiene planificado para
  el hardening posterior a las nuevas superficies.
<!-- DOC1-R1-REVISION-MANUAL:END -->

DEV.2 abre y cierra una superficie interna y local para revisar el estado técnico
de Developer Diagnostics sin alterar los cálculos previsionales, sin leer datos
de simulación y sin exponer información personal o financiera.

DEV.2 no cambia cálculos, motores previsionales, normativa, resultados ni
flujos públicos de simulación.

## Objetivo

Crear una página de Centro de desarrollo que permita confirmar, durante el
desarrollo local, si Developer Diagnostics está activo, qué esquema JSONL se usa,
cuál es el archivo diagnóstico esperado, qué eventos recientes son visibles de
forma segura, si existe material suficiente para una exportación ZIP sanitizada y
qué componentes locales requieren atención.

El cierre R4 consolida la documentación viva del bloque después de integrar R1,
R2 y R3. No introduce comportamiento funcional nuevo.

## Activación

Developer Diagnostics y la superficie administrativa siguen desactivados por
defecto. Para utilizar el Portal Developer en un entorno local se requiere una
activación explícita:

```powershell
$env:MRP_DEV_MODE = "1"
$env:MRP_ADMIN_ENABLED = "1"

$env:MRP_ADMIN_SECRET = "<secreto-local-no-versionado>"
```

`MRP_ADMIN_SECRET` se define fuera del repositorio únicamente para el
contrato técnico Bearer legado y no constituye la credencial del login humano.
Developer Diagnostics requiere `MRP_DEV_MODE=1`. El directorio diagnóstico
puede mantenerse por defecto bajo `logs/diagnostico/` o configurarse con
`MRP_DIAGNOSTIC_DIR` durante pruebas locales.

## Alcance de R1

Incluye:

- ruta interna `/dev/centro-desarrollo`;
- estado de `MRP_DEV_MODE`;
- versión de esquema de Developer Diagnostics;
- resumen no sensible del log vigente y sus rotaciones conocidas;
- indicación de disponibilidad de exportación ZIP sanitizada;
- advertencias explícitas de privacidad.

No incluye:

- lectura de cuerpos HTTP;
- lectura de PDFs, uploads, bases de datos o `sessionStorage`;
- nombres, cédulas, NSS, salarios, cuotas o montos de pensión;
- rutas absolutas locales del equipo;
- telemetría remota;
- cambios en los motores de cálculo;
- cambios en cálculos previsionales o resultados;
- cambio de VERSION al abrir el bloque.

## Alcance de R2

DEV.2 R2 añade un visor diagnóstico seguro y un servicio interno de exportación
ZIP controlada sobre los archivos JSONL ya conocidos por Developer Diagnostics.

Incluye:

- lectura acotada del archivo `mrp-diagnostics.jsonl` y sus rotaciones esperadas;
- normalización de eventos recientes para la interfaz local;
- conteo visible de eventos por nivel operacional;
- exposición de `correlation_id` solo cuando existe y sin derivarlo de datos del usuario;
- metadata limitada a operación, método HTTP, código de estado y tipo de excepción;
- conteo de líneas JSONL inválidas sin mostrar su contenido;
- servicio `exportar_zip_diagnostico_sanitizado()` para generar el ZIP permitido;
- regresiones específicas para visor, privacidad y exportación.

## Alcance de R3

DEV.2 R3 añade un autodiagnóstico técnico local sobre el Centro de desarrollo y
Developer Diagnostics, sin introducir autenticación administrativa fuerte ni
cambios de seguridad que correspondan a SEC.2.

Incluye:

- estado global del autodiagnóstico técnico;
- verificación de `MRP_DEV_MODE`;
- verificación del directorio diagnóstico sin mostrar rutas absolutas;
- prueba controlada de lectura/escritura solo cuando Developer Diagnostics está activo;
- estado del log JSONL vigente;
- estado de rotaciones conocidas;
- estado lógico de exportación ZIP sanitizada;
- estado del visor de eventos;
- verificación declarativa de controles de privacidad;
- tabla de resultados por componente con estado, detalle y acción sugerida;
- regresiones específicas para privacidad, permisos controlados y renderizado.

## Alcance de R4

DEV.2 R4 cierra documentalmente el bloque funcional y sincroniza las superficies
vivas que todavía podían presentar DEV.2 como pendiente o no iniciado.

Incluye:

- cierre consolidado de `docs/architecture/development-center.md`;
- sincronización de `README.md`;
- sincronización de `CHANGELOG.md`;
- sincronización de `docs/architecture/system-architecture.md`;
- sincronización de `docs/decisions/adr-179-revision-aware-versioning.md`;
- regresión documental `tests/test_dev2_r4_cierre_final.py`;
- conservación explícita de VER.2 como cierre transversal posterior.

No incluye:

- rutas públicas nuevas;
- autenticación administrativa fuerte;
- sesiones administrativas;
- descarga HTTP directa desde la interfaz;
- cambios de CSP, CORS, CSRF, secretos o cifrado;
- almacenamiento persistente de diagnósticos;
- integración con cuentas, usuarios o roles;
- cambios en motores previsionales;
- cambios en fórmulas, normativa o resultados;
- creación o movimiento de tags.

Esos puntos quedan reservados para revisiones posteriores de seguridad,
despliegue o release, según corresponda.

## Alcance de R5

DEV.2 R5 reabre el bloque para separar el acceso humano al Portal Developer del
contrato técnico Bearer y establecer una entrada canónica independiente de la
navegación previsional pública.

Incluye:

- `/dev` como entrada humana canónica del Portal Developer;
- sesión web mediante cookie `mrp_admin_session` `HttpOnly`, acotada a
  `Path=/dev`;
- validación directa de la sesión web para superficies HTML, sin provocar
  primero un rechazo Bearer;
- conservación de `Authorization: Bearer <token>` para acceso técnico
  programático autorizado;
- compatibilidad de `GET /dev/login` mediante redirección a `/dev`;
- compatibilidad de `/dev/centro-desarrollo`, conservando Bearer para clientes
  técnicos y dirigiendo el navegador autenticado a `/dev`;
- shell visual `dev_base.html` separado de la navegación pública, gestión de
  datos de simulación y consentimiento de privacidad de la aplicación;
- login integrado con los temas Claro, Oscuro, Automático y Alto contraste;
- eliminación de identificadores internos de revisión de la interfaz visible;
- clasificación diagnóstica explícita de `dev.portal`, `dev.login` y
  `dev.logout`;
- `Cache-Control: no-store` tanto en `/dev` como en sus subrutas;
- regresiones específicas de sesión web, compatibilidad Bearer, privacidad,
  cookie y shell Developer.

R5 no añade todavía páginas Developer independientes para diagnóstico, eventos,
archivos, mantenimiento o privacidad. Tampoco expone descarga HTTP del ZIP ni
operaciones destructivas sobre logs. Esas capacidades corresponden al rediseño
posterior DEV.2 R6 y deberán conservar autenticación administrativa, auditoría y
confirmación reforzada para acciones destructivas.

La credencial administrativa no se persiste en `localStorage`,
`sessionStorage`, query string ni documentación visible. El JavaScript del
Portal Developer solo gestiona interacción visual del formulario.

### Validación y aceptación de R5

La validación local previa a integración quedó en:

```text
1172 unittest OK
1211 pytest passed / 5747 subtests passed
19 JavaScript con sintaxis válida
pip check OK
compileall OK
Markdown Audit OK
16 familias / 46 identificadores OK
git diff --check limpio
```

Durante el desarrollo, `VERSION` permaneció en `0.1.17.02-beta`. Después de
PR #107 / merge `bc97db0` y sus validaciones, esta promoción materializa
G118/E04 como `0.1.18.04-beta`; G119/E05 (`0.1.19.05-beta`) queda reservado
para DEV.2 R6.

## Alcance implementado: DEV.2 R6

R6 no duplica la aplicación previsional pública. Evoluciona únicamente el Portal Developer a una arquitectura multipágina:

- `/dev` como dashboard compacto;
- `/dev/diagnostico` con detalle técnico y actualización;
- `/dev/eventos` con filtros, búsqueda y detalle seguro;
- `/dev/archivos` con inventario y descarga real del ZIP diagnóstico;
- `/dev/mantenimiento` con uso de disco, rotaciones, limpieza controlada y revocación de sesiones cuando corresponda;
- `/dev/privacidad` para controles técnicos de privacidad y seguridad.

Las operaciones destructivas de mantenimiento actúan únicamente sobre superficies permitidas, aplican autorización RBAC y CSRF, revalidan contraseña cuando corresponde y registran evidencia sanitizada sin secretos ni datos previsionales.

## Contrato operativo vigente de DEV.2 R6

Esta sección describe el estado operativo vigente después de publicar
DEV.2 R6 como G119/E05. Las secciones R1-R5 anteriores conservan el contexto
histórico de cómo evolucionó el bloque.

### Activación y almacenamiento

El Portal Developer permanece deshabilitado por defecto.

La activación humana mínima en desarrollo local es:

```powershell
$env:MRP_ADMIN_ENABLED = "1"
```

Developer Diagnostics requiere adicionalmente:

```powershell
$env:MRP_DEV_MODE = "1"
```

`MRP_ADMIN_SECRET` y `MRP_ADMIN_TOKEN` no son credenciales del login humano.
Se reservan exclusivamente para el contrato técnico Bearer legado.

Las identidades Developer se almacenan localmente en SQLite. La ruta
predeterminada es:

```text
data/developer/portal.sqlite3
```

Puede cambiarse mediante `MRP_DEVELOPER_STORE_PATH`.

Esta base no contiene datos de simulación previsional. Mantiene únicamente
estado administrativo, entre otros:

- identificador estable de la cuenta;
- nombre de usuario;
- nombre visible;
- rol;
- hash Argon2id de contraseña;
- revisión de seguridad;
- estado activo/inactivo;
- condición de cambio obligatorio de contraseña;
- metadata administrativa;
- hash del código de recuperación cuando corresponde.

La cuenta Owner es única y está protegida contra eliminación,
desactivación, degradación de rol o promoción de otra cuenta a Owner.

### Variables de entorno del Portal Developer

| Variable | Valor predeterminado | Función |
| --- | --- | --- |
| `MRP_ADMIN_ENABLED` | desactivado | Kill switch principal del Portal Developer. |
| `MRP_DEV_MODE` | desactivado | Activa Developer Diagnostics; no habilita por sí solo el Portal Developer. |
| `MRP_ADMIN_SECRET` | sin valor | Secreto del contrato técnico Bearer legado; no autentica cuentas humanas. |
| `MRP_ADMIN_TOKEN` | sin valor | Compatibilidad para el contrato técnico Bearer legado. |
| `MRP_ADMIN_SESSION_MINUTES` | `30` | Tiempo máximo de inactividad de una sesión administrativa. |
| `MRP_ADMIN_SESSION_MAX_HOURS` | `8` | Duración absoluta máxima de una sesión administrativa. |
| `MRP_ADMIN_MAX_SESSIONS` | `5` | Límite configurable de sesiones administrativas activas. |
| `MRP_ADMIN_COOKIE_SECURE` | desactivado | Debe habilitarse cuando el Portal Developer se sirve mediante HTTPS. |
| `MRP_ADMIN_COOKIE_SAMESITE` | `lax` | Política `SameSite` de la cookie `mrp_admin_session`. |
| `MRP_DEVELOPER_STORE_PATH` | `data/developer/portal.sqlite3` | Ubicación del almacén SQLite administrativo local. |
| `MRP_DIAGNOSTIC_DIR` | `logs/diagnostico/` | Permite sobrescribir el directorio local de Developer Diagnostics. |

Las rutas de datos Developer, diagnósticos y secretos son artefactos locales
y no deben incorporarse al contenido versionado normal del repositorio.

### Rutas implementadas

| Ruta | Responsabilidad vigente |
| --- | --- |
| `/dev` | Entrada humana canónica y dashboard del Portal Developer. |
| `/dev/login` | Compatibilidad de entrada y procesamiento del acceso humano. |
| `/dev/logout` | Cierre de sesión mediante POST. |
| `/dev/diagnostico` | Estado técnico y autodiagnóstico Developer. |
| `/dev/eventos` | Consulta de eventos diagnósticos sanitizados. |
| `/dev/archivos` | Inventario seguro de archivos diagnósticos reconocidos. |
| `/dev/archivos/exportar` | Exportación explícita del ZIP diagnóstico sanitizado. |
| `/dev/mantenimiento` | Estado y operaciones de mantenimiento autorizadas. |
| `/dev/mantenimiento/limpiar-sesiones` | Limpieza controlada de sesiones según permisos. |
| `/dev/mantenimiento/revocar-sesiones` | Revocación reforzada de sesiones administrativas. |
| `/dev/privacidad` | Controles técnicos de privacidad y seguridad del portal. |
| `/dev/perfil` | Perfil de la identidad Developer autenticada. |
| `/dev/perfil/password` | Cambio seguro de la contraseña propia. |
| `/dev/acceso-tecnico` | Explicación y separación del acceso técnico Bearer. |
| `/dev/centro-desarrollo` | Superficie técnica legacy preservada para compatibilidad autorizada. |

Las superficies humanas utilizan sesión web y RBAC deny-by-default.
Las operaciones sensibles aplican CSRF y, cuando corresponde,
revalidación de contraseña y confirmación explícita.

### Roles

El modelo vigente define cuatro roles:

- `owner`;
- `admin`;
- `operator`;
- `auditor`.

Owner es único y protegido.

Admin dispone de atribuciones amplias, pero no puede alterar las invariantes
protegidas del Owner.

Operator y Auditor reciben únicamente los permisos explícitamente asignados.

Una acción sin permiso reconocido se deniega por defecto.

### Sesiones y revisión de seguridad

La cookie humana es `mrp_admin_session`, `HttpOnly` y limitada a
`Path=/dev`.

La sesión queda vinculada a una identidad Developer y a su revisión de
seguridad persistente.

Un cambio de contraseña, una revocación u otra operación que incremente
esa revisión invalida las sesiones anteriores cuando posteriormente se
contrasta su estado persistente.

`MRP_ADMIN_ENABLED` prevalece sobre cualquier sesión existente:
si el kill switch está desactivado, una cookie anterior no puede reactivar
la superficie administrativa.

### Frontera de datos

El Portal Developer y su SQLite administrativo están separados de los datos
de simulación previsional.

No deben almacenarse en el portal:

- cédulas o NSS;
- salarios o cuotas previsionales;
- montos de pensión;
- contenido de PDF;
- cookies o tokens dentro de logs;
- secretos Bearer;
- contraseñas en texto claro;
- códigos de recuperación en texto claro.

Las contraseñas y el código de recuperación Owner se persisten únicamente
como hashes Argon2id.

## Versionado

DEV.2 R1/R2/R3/R4 **no cambia VERSION** ni `APP_VERSION`. La versión visible
permanece en `0.0.26-beta` durante este tramo.

DEV.2 R4 no cambia VERSION. DEV.2 R4 no crea tag.

DEV.2 R4 no cambia `APP_VERSION`, no promueve `0.GG.RR.EE-beta`, no consume
una revisión revision-aware y no adelanta `1.0.0.0` ni `Build 000001`.

La promoción a una versión `0.GG.RR.EE-beta` queda reservada para el cierre
posterior de VER.2, cuando el ledger y la documentación de versionado se alineen
de forma sincrónica.

## Relación con GOV.1.4

GOV.1.4 ya implementó el núcleo de observabilidad y Developer Diagnostics. DEV.2
no reescribe esa capa: agrega una interfaz interna, visor seguro, autodiagnóstico
local y pruebas de seguridad sobre la capacidad existente.

## Relación con VER.2

DEV.2 queda cerrado como bloque funcional independiente. VER.2 permanece como el
cierre transversal pendiente de versionado revision-aware, ledger, documentación
contable y promoción de versión cuando corresponda.

## Nota de cierre DEV.2 R1

DEV.2 R1 fue integrado mediante PR #37 sobre `main` con el commit de squash
`06e2821`. El cierre abre la ruta interna `/dev/centro-desarrollo`, mantiene
`VERSION` y `APP_VERSION` en `0.0.26-beta`, no crea tag, no cambia motores
previsionales y deja como siguiente trabajo DEV.2 R2.

La validación local de cierre quedó en:

```text
python -m pytest tests\test_dev2_development_center.py -q
4 passed

python -m pytest -q
868 passed, 695 subtests passed
```

## Nota de integración DEV.2 R2

DEV.2 R2 fue integrado mediante PR #39 sobre `main` con el commit de squash
`5451d18`. El cierre agregó visor diagnóstico seguro y exportación ZIP
sanitizada controlada, manteniendo `VERSION` y `APP_VERSION` en `0.0.26-beta`.

La validación local de cierre quedó en:

```text
python -m pytest tests\test_dev2_r2_visor_diagnostico.py -q
4 passed

python -m pytest -q
874 passed, 695 subtests passed
```

## Nota de integración DEV.2 R3

DEV.2 R3 fue integrado mediante PR #40 sobre `main` con el commit de squash
`9fb86af`. El cierre agregó autodiagnóstico técnico local, manteniendo `VERSION`
y `APP_VERSION` en `0.0.26-beta`.

La validación local de cierre quedó en:

```text
python -m pytest tests\test_dev2_r3_autodiagnostico.py -q
4 passed

python -m pytest tests\test_dev2_development_center.py tests\test_dev2_r1_cierre_documental.py tests\test_dev2_r2_visor_diagnostico.py tests\test_dev2_r3_autodiagnostico.py -q
14 passed

python -m pytest -q
878 passed, 695 subtests passed
```

## Validación esperada de DEV.2 R4

```text
python -m pytest tests\test_dev2_r4_cierre_final.py -q
4 passed

python -m pytest tests\test_dev2_development_center.py tests\test_dev2_r1_cierre_documental.py tests\test_dev2_r2_visor_diagnostico.py tests\test_dev2_r3_autodiagnostico.py tests\test_dev2_r4_cierre_final.py -q
18 passed

python -m pytest -q
882 passed, 695 subtests passed
```


## SEC.2 R6 — Sesión administrativa web endurecida

El Centro de desarrollo utiliza una sesión administrativa temporal posterior a la validación inicial. La sesión usa cookie HttpOnly configurable, expiración por inactividad y controles preparados para despliegue HTTPS interno.

## Estado vigente post-SEC.2 / DEV.2 R6

El acceso humano utiliza `/dev` como entrada canónica, identidad Developer
persistente y sesiones asociadas a una revisión de seguridad.
`MRP_ADMIN_ENABLED=1` continúa como kill switch obligatorio. Las contraseñas
humanas se almacenan mediante Argon2id y no existe una contraseña predeterminada.
La cookie `mrp_admin_session` es `HttpOnly`, queda limitada a `Path=/dev`,
expira por inactividad y mantiene un límite absoluto de sesión. El logout usa
`POST /dev/logout`; `/dev` y sus subrutas reciben `Cache-Control: no-store`.

El contrato Bearer se conserva de forma separada para clientes técnicos
autorizados y utiliza `MRP_ADMIN_SECRET`/`MRP_ADMIN_TOKEN` exclusivamente en
esa superficie. Una sesión humana válida nunca anula el kill switch. Las
operaciones sensibles aplican RBAC, CSRF y revalidación cuando corresponde.
Para HTTPS interno se activa `MRP_ADMIN_COOKIE_SECURE=1`.
