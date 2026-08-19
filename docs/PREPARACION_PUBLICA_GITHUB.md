# Preparación pública de GitHub

**Estado:** Vigente — preparación pre-beta
**Versión de aplicación revisada:** `0.0.24-beta`
**Fecha:** 2026-08-18
**Clasificación:** GitHub / Comunidad / Publicación

Este documento define la metadata y los controles de presentación que deben quedar listos antes de cambiar la visibilidad del repositorio. El repositorio puede permanecer privado durante esta preparación; ningún punto de esta guía sustituye los gates jurídicos, de seguridad, accesibilidad o despliegue de la primera beta pública.

## 1. Metadata About

- **Nombre:** `mi-retiro-proyectado`
- **Descripción:** `Aplicación web independiente y no oficial para estimar, explicar y comparar escenarios de retiro de la CSS de Panamá (SEBD, Mixto y SUCGS).`
- **Homepage:** sin URL pública hasta que exista un despliegue aprobado.
- **Visibilidad actual:** privada.

## 2. Topics aprobados

Los topics priorizan vocabulario en español y se mantienen en minúsculas, sin tildes y con guiones. Los nombres propios de tecnologías conservan su forma canónica. La lista objetivo es de **20 topics**:

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
- `sebd`

La evidencia manual de R6 confirmó **19/20 topics** configurados. `sebd` quedó pendiente porque la interfaz mostró una coincidencia distinta durante la captura. GitHub permite continuar escribiendo para crear un topic nuevo; debe intentarse el texto exacto `sebd` y confirmar la creación sin seleccionar otra sugerencia. Si la interfaz sigue impidiendo el alta exacta, se admite `sebd-panama` como alternativa específica y se documentará el valor final configurado. Nunca deben coexistir `sebd` y `sebd-panama`, para no exceder ni duplicar semántica.

Los nombres de topics son metadata pública de GitHub incluso cuando el repositorio es privado. La decisión de utilizarlos queda aceptada expresamente durante UX.4.6e.

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
| `normativa` | `fbca04` | Normativa y fuentes oficiales |
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

Las cinco convenciones finales conservan su nombre canónico en inglés porque forman parte del lenguaje habitual de GitHub; sus descripciones y la documentación del proyecto permanecen en español. Los formularios versionados aplican automáticamente `bug`, `enhancement` o `question` junto con `needs-triage`. Las labels deben existir en GitHub antes de esperar esa asignación automática.

## 4. Badges del README

El README muestra:

- estado de `Validación continua` sobre `main`;
- estado de `Auditoría de gobernanza` sobre `main`;
- versión formal;
- versiones Python soportadas;
- licencia propietaria.

Los badges de workflows usan GitHub Actions. Los badges estáticos de versión/Python/licencia usan Shields.io únicamente en el README y no forman parte del runtime de la simulación.

## 5. Issue Forms y Pull Requests

Los Issue Forms continúan separados en:

- Reporte de error;
- Solicitud de mejora;
- Consulta / soporte.

Las vulnerabilidades no deben publicarse en Issues y siguen `SECURITY.md`.

Los Pull Requests pueden recibir varias labels según alcance. Un PR transversal de UX puede usar, por ejemplo, `ui`, `documentation`, `tests` y `maintenance`. No se añade un workflow con permisos de escritura solo para autoetiquetar PRs; el etiquetado de PR es manual mientras el volumen de contribuciones sea bajo.

## 6. Social preview

Antes de la publicación amplia debe configurarse una imagen social oficial del proyecto. Objetivo recomendado para la pieza final: 1280 × 640 px, menos de 1 MB, con identidad Mi Retiro Proyectado y sin logos que impliquen afiliación oficial con la CSS.

La imagen de social preview se configura en GitHub Settings y no forma parte del runtime.

## 7. Funciones del repositorio

Configuración objetivo mientras no exista una necesidad distinta:

- Issues: habilitado;
- Wiki: deshabilitado;
- Projects: deshabilitado mientras no exista tablero operativo;
- Discussions: deshabilitado mientras Issues/Support cubran el flujo real;
- Squash merge: habilitado;
- merge commit: deshabilitado;
- rebase merge: deshabilitado;
- auto-merge: deshabilitado;
- update branch: habilitado.

## 8. Gate antes de cambiar a Public

Antes de hacer público el repositorio se debe revisar nuevamente:

1. que no existan secretos, datos personales ni documentos reales versionados;
2. Dependency graph, Dependabot y alertas;
3. secret scanning, push protection y code scanning según disponibilidad del plan/visibilidad;
4. `SECURITY.md`, licencia y avisos de terceros;
5. revisión jurídica externa pendiente;
6. auditoría ampliada de accesibilidad pendiente;
7. alcance funcional de la primera beta;
8. social preview y metadata final;
9. suite/CI completamente verdes.

## 9. Evidencia manual

Topics, labels, social preview, visibilidad y algunos settings no son impuestos por archivos del repositorio. La evidencia manual de R6 confirma 21 labels y 19 topics configurados; falta resolver el topic SEBD y, más adelante, el social preview. Todo debe comprobarse directamente en GitHub antes de declarar completada la preparación pública.
