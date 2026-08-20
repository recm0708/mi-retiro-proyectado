# Auditoría de GitHub y controles de repositorio

**Estado:** Vigente — GOV.1.6 cerrado / revalidado en GOV.1.8 y publicación del repositorio
**Versión de aplicación revisada:** `0.0.26-beta`
**Versión base histórica:** `0.0.24-beta`
**Fecha base:** 2026-08-18
**Revalidación:** 2026-08-19
**Clasificación:** Gobierno / GitHub / CI / Auditoría

## 1. Controles versionados

- `.github/CODEOWNERS`;
- `.github/allowed_signers`;
- `.github/dependabot.yml`;
- `.github/ISSUE_TEMPLATE/bug_report.yml`;
- `.github/ISSUE_TEMPLATE/feature_request.yml`;
- `.github/ISSUE_TEMPLATE/question.yml`;
- `.github/ISSUE_TEMPLATE/config.yml`;
- `.github/pull_request_template.md`;
- `.github/workflows/ci.yml`;
- `.github/workflows/verificar-tags.yml`;
- `.github/workflows/auditoria-gobernanza.yml`;
- `SECURITY.md`;
- `CODE_OF_CONDUCT.md`;
- `SUPPORT.md`.

## 2. Estado esperado de `main`

- Pull Request obligatorio;
- commits verificados;
- historial lineal;
- conversaciones resueltas;
- checks `Python 3.13` y `Python 3.14`;
- rama actualizada antes de integrar;
- eliminación y force push bloqueados;
- bypass administrativo solo mediante Pull Request para recuperación excepcional.

El cierre GOV.1.8 confirma el conjunto operativo esperado de checks requeridos:

- `Python 3.13`;
- `Python 3.14`;
- `Auditoría de gobernanza`.

La promoción del tercer check fue realizada durante el cierre GOV.1.6/GOV.1.7 y quedó revalidada mediante los PR #15, #16 y #17 con ejecución exitosa del flujo de cierre.

## 3. Tags

El ruleset `v*` permite crear nuevos tags y bloquea actualización, eliminación y force push. Los tags nuevos permanecen firmados.

## 4. Pull Requests

El flujo ordinario es rama → PR → checks → `Squash and merge`. Merge commit y rebase merge ordinarios permanecen deshabilitados; la rama remota integrada puede eliminarse automáticamente.

## 5. GitHub Actions

- permisos de solo lectura cuando sean suficientes;
- Actions no debe aprobar PR por defecto;
- workflows del proyecto usan `permissions: contents: read`;
- acciones oficiales vigentes `@v7`;
- no usar `pull_request_target` para ejecutar código no confiable de un PR;
- no imprimir secretos ni datos personales en logs.

## 6. Dependencias, análisis y secretos

Controles actualmente habilitados en el repositorio público:

- Dependency graph;
- Dependabot alerts;
- Dependabot security updates;
- CodeQL con **Default setup**;
- Secret Protection / secret scanning;
- Push protection;
- Private vulnerability reporting;
- Copilot Autofix para hallazgos CodeQL.

La revisión manual del 2026-08-19 registró **0 alertas abiertas** en Code scanning, Secret scanning y Dependabot.

Automatic dependency submission, Grouped security updates y AI findings (Preview) permanecen deshabilitados de forma deliberada. Dependabot malware alerts no se activa para el ecosistema actual.

## 7. Auditoría automática GOV.1.6

`.github/workflows/auditoria-gobernanza.yml` ejecuta las regresiones GOV.1.6 y `git diff --check` en Python 3.14 con permisos de solo lectura. No duplica la suite funcional completa de `ci.yml`.

## 8. Revisión manual periódica

Antes de una beta pública de producto y cuando cambie la configuración, revisar rulesets, métodos de merge, permisos de Actions, checks requeridos, Dependabot, visibilidad, opciones de seguridad, CODEOWNERS, Social Preview y canal de vulnerabilidades.

La guía operativa vigente de metadata, topics, labels, Social Preview, visibilidad y seguridad pública se mantiene en `PREPARACION_PUBLICA_GITHUB.md`.

## 9. Evidencia histórica de cierre GOV.1

Esta sección conserva el estado observado durante el cierre GOV.1 y **no describe la visibilidad actual**.

Evidencia remota de cierre y auditoría post-GOV.1:

- repositorio privado en el momento del cierre GOV.1;
- `main` como única rama remota persistente después de limpieza;
- `Squash and merge` habilitado;
- merge commit, rebase merge y auto-merge deshabilitados;
- actualización de rama permitida;
- PR #15 fusionado con `Python 3.13`, `Python 3.14` y `Auditoría de gobernanza` en `success`;
- PR #16 fusionado con los mismos tres checks en `success`;
- PR #17 fusionado como cierre GOV.1, con commit final `653900cebd84019fbbaa3ff3cfd91536ccab76eb`;
- `v0.0.24-beta` publicado como tag anotado y firmado, objeto `3cdf6f84804c1bb4bdda9e449eb0932528557aa3`;
- 24/24 tags verificados localmente con firma SSH válida en la auditoría post-GOV.1;
- cero Pull Requests abiertos al inicio de GOV.1.8 y sin PR abiertos al realizar la auditoría post-GOV.1.

Los settings internos del ruleset que no expone el conector se consideran evidencia manual del mantenedor.

## 10. Metadatos y funciones vigentes del repositorio

- nombre: `mi-retiro-proyectado`;
- descripción: “Aplicación web independiente y no oficial para estimar, explicar y comparar escenarios de retiro de la CSS de Panamá (SEBD, Mixto y SUCGS).”;
- visibilidad actual: **pública**;
- Issues: habilitado;
- Wiki: deshabilitado para evitar una segunda fuente documental fuera de `docs/`;
- Projects: deshabilitado mientras no exista un tablero de trabajo utilizado;
- Discussions: deshabilitado mientras Issues/Support cubran el flujo real;
- topics: 20/20, con `sebd-panama`;
- labels: 21;
- README: badges de CI/gobernanza, versión, Python, licencia y logo oficial;
- Social Preview: configurado y conservado en `assets/social/github-social-preview.png`;
- identidad oficial: versionada bajo `assets/brand/` y documentada en `IDENTIDAD_VISUAL.md`.

El cambio de nombre conserva la historia del repositorio; los clones locales deben usar el URL actual. Las referencias históricas que documentan nombres de artefactos reales anteriores al rename no se reescriben.

La guía operativa y de mantenimiento de estos metadatos se conserva en `PREPARACION_PUBLICA_GITHUB.md`.

## 11. Revalidación pública del 2026-08-19

Después de cambiar la visibilidad a pública se confirmó manualmente:

- CodeQL Default setup operativo;
- Secret Protection habilitado;
- Push protection habilitado;
- Private vulnerability reporting habilitado;
- Dependabot/Dependency graph activos;
- cero alertas abiertas en los tres paneles revisados;
- Social Preview oficial cargado;
- configuración de merge sin cambios respecto al modelo protegido.

La visibilidad pública del repositorio **no equivale a una beta pública de la aplicación ni a un despliegue remoto aprobado**.

## 12. Límite de afirmación

Los archivos versionados no pueden imponer por sí solos settings alojados en GitHub. Los cambios de ruleset/settings requieren verificación en GitHub antes de declarar un hito cerrado.

Los controles habilitados no prueban invulnerabilidad ni sustituyen una auditoría externa de seguridad.
