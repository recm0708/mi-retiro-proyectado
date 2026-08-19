# Auditoría de GitHub y controles de repositorio

**Estado:** Vigente — GOV.1.6 cerrado / revalidado en GOV.1.8
**Versión de aplicación revisada:** `0.0.24-beta`
**Fecha:** 2026-08-18
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

## 6. Dependencias y alertas

Controles adoptados: Dependency graph, Dependabot alerts, Dependabot security updates y revisión humana sin auto-merge.

La disponibilidad de code scanning, secret scanning u otras funciones depende del plan/visibilidad. No se declaran controles que GitHub no tenga habilitados.

## 7. Auditoría automática GOV.1.6

`.github/workflows/auditoria-gobernanza.yml` ejecuta las regresiones GOV.1.6 y `git diff --check` en Python 3.14 con permisos de solo lectura. No duplica la suite funcional completa de `ci.yml`.

## 8. Revisión manual periódica

Antes de una beta pública y cuando cambie la configuración, revisar rulesets, métodos de merge, permisos de Actions, checks requeridos, Dependabot, visibilidad, opciones de seguridad, CODEOWNERS y canal de vulnerabilidades.

## 9. Evidencia de cierre GOV.1

Evidencia remota de cierre y auditoría post-GOV.1:

- repositorio privado;
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

Los settings internos del ruleset que no expone el conector se consideran evidencia manual del mantenedor y deben revisarse nuevamente antes de una beta pública.

## 10. Metadatos y funciones del repositorio

La normalización post-GOV.1 adopta estas decisiones mientras el repositorio permanezca privado:

- nombre objetivo: `mi-retiro-proyectado`;
- descripción: “Aplicación web independiente y no oficial para estimar, explicar y comparar escenarios de retiro de la CSS de Panamá (SEBD, Mixto y SUCGS).”;
- Issues: habilitado;
- Wiki: deshabilitado para evitar una segunda fuente documental fuera de `docs/`;
- Projects: deshabilitado mientras no exista un tablero de trabajo utilizado;
- Discussions: deshabilitado por ahora;
- topics: sin publicar mientras no exista decisión expresa, porque los nombres de topics son públicos incluso en repositorios privados.

El cambio de nombre conserva la historia del repositorio; los clones locales deben actualizar `origin` al nuevo URL. Las referencias históricas que documentan nombres de artefactos reales anteriores al rename no se reescriben.

## 11. Límite de afirmación

Los archivos versionados no pueden imponer por sí solos settings alojados en GitHub. Los cambios de ruleset/settings requieren verificación en GitHub antes de declarar el hito cerrado.
