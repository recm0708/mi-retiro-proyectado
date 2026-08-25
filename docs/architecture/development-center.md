# DEV.2 R1/R2/R3/R4 — Centro de desarrollo

**Estado general:** DEV.2 cerrado documentalmente en R4.

**Estado R1:** integrado en `main` mediante PR #37.

**Estado R1 documental:** integrado en `main` mediante PR #38.

**Estado R2:** integrado en `main` mediante PR #39.

**Estado R3:** integrado en `main` mediante PR #40.


<!-- DOC1-R1-REVISION-MANUAL:START -->
## Nota de lectura post-MANT.1

DEV.2 queda preservado como bloque funcional cerrado. Sus referencias a VER.2 o a bloques posteriores se conservan como trazabilidad del momento en que fue documentado.

Estado vigente:

- DEV.2 está cerrado y no es el bloque activo actual.
- MANT.1 quedó cerrado operativamente en R7.
- DOC.1 R1 está cerrado.
- NOR.1 y NOR.2 están cerrados.
- DOC.1 R2 está cerrado como revisión documental integral posterior a NOR.2.
- `VERSION` permanece en `0.0.71.01-beta`.
- SEC.2 quedó cerrado después de R1–R6; AUD.SEC2 R1 corrige el kill switch y el contrato de sesión web sin reabrir DEV.2.
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

Developer Diagnostics sigue desactivado por defecto. La activación local requiere:

```powershell
$env:MRP_DEV_MODE = "1"
```

Equivalente conceptual: `MRP_DEV_MODE=1`.

El directorio diagnóstico puede mantenerse por defecto bajo `logs/diagnostico/` o
configurarse con `MRP_DIAGNOSTIC_DIR` durante pruebas locales.

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

## Estado vigente post-SEC.2

El Centro de desarrollo usa `/dev/login` para acceso web y
`/dev/centro-desarrollo` como superficie protegida. `MRP_ADMIN_ENABLED=1` es un
kill switch obligatorio y `MRP_ADMIN_SECRET` se define fuera del repositorio;
no existe contraseña predeterminada. El login crea una sesión temporal en
memoria con cookie `mrp_admin_session` `HttpOnly`, expiración por inactividad y
límite absoluto. El logout usa `POST /dev/logout` y las respuestas `/dev/`
marcan `Cache-Control: no-store`.

Una cookie válida solo sustituye la ausencia de Bearer (`401`) cuando la
administración está habilitada y el secreto sigue configurado. Nunca sustituye
un `403` causado por administración deshabilitada o configuración incompleta.
Para HTTPS interno se activa `MRP_ADMIN_COOKIE_SECURE=1`; multi-instancia exige
un backend compartido de sesiones antes de considerarse soportado.
