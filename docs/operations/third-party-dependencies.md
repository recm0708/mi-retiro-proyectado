# Dependencias y terceros

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.19.05-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Base documental:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal histórica:** GOV.1.5 R3 — 2026-08-18
**Última revisión documental:** mantenimiento post-G119 — 2026-08-31
**Clasificación:** Técnica / Terceros / Auditoría

Este inventario distingue dependencias directas, snapshot transitivo, recursos externos y servicios de red. GOV.1.7 adopta una licencia propietaria para materiales originales sin relicenciar dependencias upstream.

## 1. Dependencias Python directas

Las versiones corresponden al `requirements.txt` vigente. La estructura documental se originó en GOV.1.3 R4 y se mantiene actualizada durante la etapa beta.

| Dependencia | Versión | Finalidad en el proyecto | Licencia upstream verificada | Conexión/datos en el uso actual | Riesgo/revisión |
|---|---:|---|---|---|---|
| FastAPI | 0.141.1 | API local, rutas y middleware | MIT | Atiende solicitudes de la aplicación; no añade por sí sola un envío externo | Revisar cambios de framework/Starlette |
| Jinja2 | 3.1.6 | Plantillas HTML | BSD-3-Clause | Render local del servidor | Revisar autoescape/plantillas |
| Pydantic | 2.13.4 | Validación/modelos | MIT | Validación local de estructuras | Revisar cambios de esquema/core |
| python-multipart | 0.0.32 | Recepción multipart de archivos | Apache-2.0 | Procesa cargas recibidas por FastAPI | Sensible a frontera de upload |
| pypdf | 6.16.2 | Extracción y lectura controlada de PDF | BSD-3-Clause | Procesa PDF en memoria; sin red propia | Dependencia crítica de parser; mantener regresiones específicas en cada actualización |
| Uvicorn | 0.52.4 | Servidor ASGI | BSD-3-Clause | Sirve la aplicación; la red depende del modo de ejecución | Revisar configuración de despliegue |

Fuentes upstream de licencia verificadas documentalmente:

- FastAPI: PyPI/repositorio oficial;
- Jinja2: repositorio Pallets;
- Pydantic: PyPI/repositorio oficial;
- python-multipart: PyPI;
- pypdf: PyPI/repositorio oficial, licencia BSD-3-Clause;
- Uvicorn: PyPI.

GOV.1.7 documenta obligaciones base en `../THIRD_PARTY_NOTICES.md`; un artefacto futuro que incorpore dependencias requiere inventario de licencias del paquete real antes de publicarse.

## 2. Snapshot transitivo

`requirements.txt` fija también dependencias transitivas para reproducibilidad.

El snapshot transitivo mejora reproducibilidad, pero **no constituye por sí solo un inventario jurídico del artefacto distribuido**. Un paquete autocontenido futuro debe inventariar lo que realmente incorpora.

Dependabot propone actualizaciones directas permitidas; no existe auto-merge.

<!-- AUTOMATION-POST-G119:START -->
## 2.1. Tooling de desarrollo y automatización

El runtime Python continúa definido por `requirements.txt`. Las herramientas de
desarrollo y automatización se mantienen separadas:

- `pytest 9.1.1` mediante `requirements-dev.txt`;
- `playwright 1.62.1` mediante `scripts/package.json`;
- `@axe-core/playwright 4.13.0` mediante `scripts/package.json`;
- `pip-audit 2.10.1` instalado de forma reproducible por
  `dependency-security.yml`.

Playwright, axe-core y sus paquetes npm son tooling de CI/desarrollo. No se
cargan en el navegador del usuario ni forman parte del servidor FastAPI.

Dependabot cubre Python, GitHub Actions y el ecosistema npm de `/scripts`.
`Dependency Security` complementa esas actualizaciones con auditoría de
vulnerabilidades Python/npm y referencias externas de GitHub Actions.
<!-- AUTOMATION-POST-G119:END -->

## 3. Bootstrap

La interfaz usa **Bootstrap 5.3.8**.

- licencia upstream: MIT;
- origen actual: `https://cdn.jsdelivr.net/`;
- carga con Subresource Integrity;
- el navegador realiza una solicitud al CDN;
- la solicitud de recurso no incluye intencionalmente el contenido de la simulación.

Servir Bootstrap localmente continúa como objetivo antes de la primera versión oficial para reducir dependencia de terceros, salvo que SEC.2/REL.1 documenten y acepten expresamente una estrategia diferente.

## 4. Servicio oficial CSS para fecha

`app/services/reference_date.py` puede consultar infraestructura oficial de la CSS mediante HTTPS para obtener el encabezado `Date`.

No se envía:

- PDF;
- cédula/NSS;
- salario;
- cuotas;
- resultado previsional.

No es una dependencia de software; se registra como **servicio externo operativo** porque afecta disponibilidad y exposición de metadata ordinaria de red.

## 5. GitHub

GitHub aloja el repositorio público y ejecuta CI/Dependabot.

GitHub Actions utiliza, entre otras referencias versionadas:

- `actions/checkout@v7`;
- `actions/setup-python@v7`;
- `actions/setup-node@v7`;
- `actions/upload-artifact@v7`;
- `actions/dependency-review-action@v4`;
- `actions/labeler@v7`.

Las referencias externas declaradas mediante `uses:` se auditan con
`scripts/audit_action_references.py`.

Estas herramientas son de desarrollo/CI, no runtime del usuario final.

## 5.1. Shields.io

El README utiliza Shields.io para renderizar badges estáticos de versión, versiones Python y licencia.

- no forma parte del runtime de Mi Retiro Proyectado;
- no interviene en cálculos, importaciones ni tratamiento de datos;
- la relación existe únicamente al visualizar la documentación del repositorio;
- no se envía intencionalmente información de la simulación.

Los badges de estado de CI y gobernanza se sirven directamente desde GitHub Actions.

## 6. Node.js

Node 24 se usa en CI para `node --check` y para el tooling reproducible
Playwright/axe de `scripts/package.json`.

La cadena npm está limitada a automatización y no forma parte del runtime
Python ni del frontend entregado al usuario.

## 6.1. Evaluación GOV.1.5 de terceros

La revisión de seguridad/privacidad clasifica:

- **jsDelivr:** tercero runtime temporal, con SRI, CSP y versión fija; riesgo residual aceptado para desarrollo local;
- **infraestructura CSS:** servicio externo operativo mínimo, sin envío de datos previsionales;
- **GitHub:** tercero de desarrollo/CI, fuera del flujo de simulación del usuario final.

La evaluación completa y los gates de despliegue se documentan en `third-party-deployment-assessment.md`.

Servir Bootstrap localmente sigue siendo la opción preferida antes de `1.0.0.0`, salvo que exista una excepción explícita, revisada y documentada en SEC.2/REL.1.

## 7. Política de actualización

Antes de aceptar una actualización:

1. revisar release/changelog upstream;
2. ejecutar instalación reproducible y `pip check`;
3. ejecutar compilación;
4. ejecutar sintaxis JS cuando corresponda;
5. ejecutar suite completa;
6. revisar importadores si cambia `pypdf`/multipart;
7. actualizar este documento si cambia versión, licencia, función, riesgo o conexión.

### 7.1. Mantenimiento pre-G118

El mantenimiento pre-G118 actualiza las dos dependencias directas propuestas por Dependabot sin consumir un Global ni modificar `VERSION`:

- `pypdf 6.16.1` → `6.16.2`: actualización patch con correcciones upstream de robustez y extracción/transformación PDF. Se conservan las regresiones específicas del proyecto para versión instalada, roundtrip `PdfWriter` → `PdfReader`, rechazo controlado de PDF sin texto y límites de páginas de ambos importadores.
- `Uvicorn 0.52.3` → `0.52.4`: actualización patch que corrige upstream la duplicación del encabezado `Date` en handshakes WebSocket con `websockets-sansio`; no modifica la configuración de despliegue de Mi Retiro Proyectado.

Los guards de inventario obtienen la versión esperada desde `requirements.txt` y exigen que esta documentación y `THIRD_PARTY_NOTICES.md` permanezcan sincronizados con el pin vigente.

### 7.2. Antecedente histórico G062

La actualización a `pypdf 6.16.1` conservó las regresiones específicas introducidas con `6.15.0`. El salto `6.15.0` → `6.16.1` incorporó correcciones upstream de seguridad y robustez relacionadas con ciclos e iteraciones limitadas durante el procesamiento PDF.

La actualización `Uvicorn 0.52.1` → `0.52.3` se integró como mantenimiento minor/patch del servidor ASGI y quedó preservada como evidencia histórica de G062.

## 8. Licencia del proyecto

La denominación histórica de GOV.1.7 es **licencia propietaria pre-beta / todos los derechos reservados**. PLAN.1 no modifica sus términos: la licencia propietaria continúa vigente durante la etapa beta actual.

Las dependencias directas documentadas son MIT, BSD-3-Clause o Apache-2.0 y no se relicencian. Una distribución debe conservar los avisos y textos upstream exigidos por los componentes efectivamente incluidos.

Consultar:

- `../LICENSE`;
- `../THIRD_PARTY_NOTICES.md`;
- `licensing-and-distribution.md`.

Un instalador, ejecutable autocontenido o contenedor futuro debe generar su inventario real antes del release.
