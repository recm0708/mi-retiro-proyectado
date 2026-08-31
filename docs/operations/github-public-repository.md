# Preparación pública de GitHub

**Estado:** Completada para visibilidad pública — mantenimiento vigente
**Versión de aplicación revisada:** `0.1.19.05-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base del checkpoint público:** `0.0.24-beta`
**Fecha de preparación original:** 2026-08-18
**Revalidación pública:** 2026-08-19
**Última revisión documental:** mantenimiento post-G119 — 2026-08-31
**Clasificación:** GitHub / Comunidad / Publicación

Este documento conserva la preparación realizada antes del cambio de visibilidad y registra el estado vigente después de convertir el repositorio en público. La publicación del **repositorio de código** no equivale a declarar una versión oficial de la aplicación, ni constituye por sí sola un despliegue de producción, ni sustituye los gates jurídicos, de accesibilidad, alcance funcional o seguridad.

> **Nota histórica:** el checkpoint pre-R8 se documentó originalmente como una publicación del repositorio que **no equivalía a declarar una beta pública de la aplicación**. PLAN.1 aclara posteriormente que la línea `0.0.N-beta` ya constituye la etapa beta de desarrollo; la frontera futura relevante es la primera versión oficial `1.0.0.0`.

## 1. Metadata About

- **Nombre:** `mi-retiro-proyectado`
- **Descripción:** `Aplicación web independiente y no oficial para estimar, explicar y comparar escenarios de retiro de la CSS de Panamá (SEBD, Mixto y SUCGS).`
- **Homepage:** sin URL de aplicación pública hasta que exista un despliegue aprobado.
- **Visibilidad actual:** pública.
- **Licencia:** propietaria pre-beta / todos los derechos reservados; la visibilidad pública del código no concede derechos adicionales de reutilización.

## 2. Topics aprobados

Los topics priorizan vocabulario en español y se mantienen en minúsculas, sin tildes y con guiones. Los nombres propios de tecnologías conservan su forma canónica. La lista vigente es de **20 topics**:

- `accesibilidad`
- `caja-seguro-social`
- `calculadora-pension`
- `estimacion-previsional`
- `fastapi`
- `jubilacion`
- `panama`
- `pension`
- `pensiones-panama`
- `planificacion-retiro`
- `prevision-social`
- `proyeccion-retiro`
- `proyeccion-salarial`
- `python`
- `retiro`
- `seguridad-social`
- `seguridad-social-panama`
- `sistema-mixto`
- `sucgs`
- `sebd-panama`

La evidencia manual confirmó **20/20 topics** configurados. La interfaz de GitHub no permitió crear el identificador exacto `sebd`, por lo que se adoptó de forma definitiva `sebd-panama` como topic específico para el Subsistema Exclusivamente de Beneficio Definido. `sebd` no forma parte de la taxonomía final y no debe coexistir con `sebd-panama`, para evitar duplicidad semántica.

## 3. Taxonomía de labels

Las labels clasifican Issues y Pull Requests; no se asignan a commits. Los commits se identifican mediante mensaje, firma, checks, PR asociado y tags cuando corresponda. La taxonomía vigente contiene **21 labels**.

| Label | Color | Uso |
|---|---|---|
| `bug` | `d73a4a` | Error o regresión reproducible |
| `enhancement` | `a2eeef` | Mejora o nueva capacidad |
| `question` | `d876e3` | Consulta o soporte |
| `documentation` | `0075ca` | Documentación |
| `tests` | `1d76db` | Pruebas y calidad |
| `maintenance` | `cfd3d7` | Refactor, mantenimiento o deuda técnica |
| `dependencies` | `0366d6` | Dependencias |
| `github-actions` | `000000` | Workflows y automatización GitHub |
| `ui` | `7057ff` | Interfaz y experiencia de usuario |
| `backend` | `0e8a16` | API, servicios y motores |
| `regulations` | `fbca04` | Normativa y fuentes oficiales |
| `privacy` | `b60205` | Privacidad y tratamiento de datos |
| `security` | `8b0000` | Seguridad y vulnerabilidades |
| `accessibility` | `5319e7` | Accesibilidad |
| `needs-triage` | `ededed` | Pendiente de clasificación inicial |
| `blocked` | `24292f` | Bloqueado por una dependencia o decisión |
| `duplicate` | `cfd3d7` | Duplicado de otro Issue o Pull Request |
| `good first issue` | `7057ff` | Apropiado para una primera contribución |
| `help wanted` | `008672` | Se necesita colaboración adicional |
| `invalid` | `e4e669` | No válido, no aplicable o no reproducible |
| `wontfix` | `ffffff` | No se continuará trabajando en este cambio |

Las cinco convenciones finales conservan su nombre canónico en inglés porque forman parte del lenguaje habitual de GitHub; sus descripciones y la documentación del proyecto permanecen en español. Los formularios versionados aplican automáticamente `bug`, `enhancement` o `question` junto con `needs-triage`.

## 4. Badges del README

El README muestra de forma centrada:

- estado de `Repository Quality Gate` sobre `main`;
- estado de `Dependency Security` sobre `main`;
- estado de `Visual & Accessibility` sobre `main`;
- versión formal;
- versiones Python soportadas;
- licencia propietaria.

`Repository Quality Gate` contiene además el check `Python Compatibility`,
que preserva la validación de Python 3.13 mientras el gate canónico completo se
ejecuta con Python 3.14.

Los badges de workflows usan GitHub Actions. Los badges estáticos de
versión/Python/licencia usan Shields.io únicamente en el README y no forman
parte del runtime de la simulación.

## 5. Issue Forms y Pull Requests

Los Issue Forms continúan separados en:

- Reporte de error;
- Solicitud de mejora;
- Consulta / soporte.

Las vulnerabilidades explotables no deben publicarse en Issues. El repositorio tiene habilitado **Private vulnerability reporting** y conserva el canal alternativo documentado en `SECURITY.md`.

Los Pull Requests pueden recibir varias labels según alcance. Un PR transversal de UX puede usar, por ejemplo, `ui`, `documentation`, `tests` y `maintenance`. `.github/workflows/pr-labeler.yml` reutiliza la taxonomía canónica existente mediante `actions/labeler@v7`. El workflow utiliza `pull_request_target` sin checkout ni ejecución de código del PR, con `contents: read` y `pull-requests: write`. `sync-labels: false` preserva las etiquetas añadidas manualmente.

## 6. Social Preview e identidad visual

El Social Preview oficial está configurado en GitHub y su copia versionada se conserva en:

`assets/social/github-social-preview.png`

Contrato de la pieza:

- 1280 × 640 px;
- PNG;
- menos de 1 MiB;
- identidad propia de Mi Retiro Proyectado;
- aviso visible de herramienta independiente/no oficial;
- sin logos de la CSS ni elementos que impliquen afiliación oficial.

La identidad canónica y sus derivados se documentan en `docs/product/visual-identity.md`.

## 7. Funciones del repositorio

Configuración vigente mientras no exista una necesidad distinta:

- Issues: habilitado;
- Wiki: deshabilitado;
- Projects: deshabilitado mientras no exista tablero operativo;
- Discussions: deshabilitado mientras Issues/Support cubran el flujo real;
- Squash merge: habilitado;
- merge commit: deshabilitado;
- rebase merge: deshabilitado;
- auto-merge: deshabilitado;
- update branch: habilitado.

## 7.1. Tags y GitHub Releases

REL.GOV.1 añade un contrato específico de publicación sin modificar la visibilidad ni la licencia del repositorio:

- todo tag formal nuevo posterior a esta política debe tener GitHub Release asociado;
- `.github/release.yml` categoriza notas generadas por GitHub, pero no sustituye el cuerpo auditable requerido;
- `scripts/release_contract.py` valida VERSION, ledger, tag, título y secciones mínimas de las notas;
- `scripts/release_publication.py` valida el manifiesto versionado, renderiza notas canónicas y comprueba idempotencia/fail-closed frente a un Release existente;
- `.github/workflows/verificar-tags.yml` conserva la firma local del tag, verifica firma/contrato/commit con permisos de lectura y publica el GitHub Release en un job separado con `contents: write` solo después de superar la verificación;
- una beta terminada en `-beta` se marca como prerelease;
- no se crean GitHub Releases retroactivos para estados que nunca tuvieron tag formal;
- una edición descriptiva de un Release histórico no autoriza mover, borrar ni recrear su tag.

El formato canónico completo vive en `docs/operations/release-process.md`.

<!-- AUTOMATION-POST-G119:START -->
## 7.2. Automatización post-G119

La capa de automatización incorpora:

- `Repository Quality Gate`;
- `Dependency Security`;
- `Scheduled Repository Health`;
- `PR Auto Labeler`;
- `Visual & Accessibility`.

`verificar-tags.yml` permanece separado porque posee triggers y permisos de
publicación diferentes.

`quality-gate.yml` centraliza validaciones técnicas, PR Policy, Repository
Health y Release Readiness.

`dependency-security.yml` audita vulnerabilidades Python/npm, referencias de
Actions y Dependency Review.

`scheduled-health.yml` ejecuta comprobaciones periódicas, incluidos enlaces
externos y auditoría de tags firmados.

`visual-a11y.yml` levanta temporalmente FastAPI y Chromium, ejecuta Playwright
con axe y conserva screenshots y reportes como artifacts. Las violaciones axe
son inicialmente informativas; los fallos operativos sí fallan el job.

Los workflows históricos `ci.yml`, `governance-audit.yml` y
`markdown-audit.yml` continúan temporalmente en paralelo. No deben retirarse ni
cambiarse los required checks hasta demostrar equivalencia remota y migrar el
ruleset sin una ventana de protección.
<!-- AUTOMATION-POST-G119:END -->

## 8. Gate de seguridad ejecutado al cambiar a Public

El 2026-08-19 se revalidó manualmente el repositorio después de cambiar su visibilidad a pública.

Controles confirmados:

- Dependency graph habilitado;
- Dependabot alerts habilitado;
- Dependabot security updates habilitado;
- CodeQL con **Default setup**;
- Secret Protection / secret scanning habilitado;
- Push protection habilitado;
- Private vulnerability reporting habilitado;
- Copilot Autofix habilitado para hallazgos CodeQL;
- AI findings en Preview mantenido deshabilitado;
- Automatic dependency submission mantenido deshabilitado;
- Dependabot malware alerts mantenido deshabilitado para el ecosistema actual;
- Grouped security updates mantenido deshabilitado.

La revisión manual del mismo día registró **0 alertas abiertas** en Code scanning, Secret scanning y Dependabot.

Este gate no equivale a una auditoría externa de seguridad y no elimina los pendientes de revisión jurídica, accesibilidad ampliada o hardening de un futuro despliegue remoto.

## 9. Evidencia manual y mantenimiento

Topics, labels, Social Preview, visibilidad y parte de los settings de seguridad no son impuestos por archivos versionados. La evidencia manual del mantenedor confirma:

- repositorio público;
- 21 labels;
- 20/20 topics, incluido `sebd-panama`;
- Social Preview configurado;
- controles de seguridad del apartado 8 habilitados;
- cero alertas abiertas durante la revalidación del 2026-08-19.

Estos valores deben revisarse nuevamente cuando cambie la configuración del repositorio o antes de la primera versión oficial.

La apertura pública del repositorio permanece separada de la decisión futura de empaquetar, distribuir o desplegar `1.0.0.0`.
