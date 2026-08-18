# Changelog

Este archivo registra **cambios notables por versión**. No sustituye el historial Git, `RELEASES.md` ni las bitácoras históricas conservadas en `docs/historico/`.

Las versiones `0.0.1-beta` a `0.0.21-beta` fueron reconstruidas retrospectivamente en GOV.1.1 a partir del historial real. `0.0.22-beta` es la primera versión formal adoptada bajo la política de GOV.1.2.

## [Unreleased]

### GOV.1.4 — Observabilidad y Developer Diagnostics

- incorporado modo exclusivo de desarrollo mediante `MRP_DEV_MODE=1`, desactivado por defecto;
- añadido logging estructurado JSONL con esquema propio, timestamps UTC, niveles, categorías, duración, resultado y correlation IDs aleatorios;
- añadida redacción defensiva y prohibición explícita de registrar cuerpos HTTP, PDF, identificadores, salarios, montos, cookies, tokens o mensajes de excepción potencialmente sensibles;
- añadidas rotación local, retención acotada y exportación diagnóstica controlada sin telemetría remota;
- integrado middleware FastAPI sin doble ejecución de cálculos y con `X-Correlation-ID` solo en modo de desarrollo;
- instrumentada la consulta externa de fecha con metadata agregada de cache/resultado, sin URLs, fechas recibidas ni datos de simulación;
- añadidas 13 regresiones específicas de observabilidad; la suite completa alcanza **487 pruebas en `OK`**;
- sincronizada la documentación transversal y cerrado formalmente GOV.1.4;
- `VERSION` permanece en `0.0.23-beta`.


### Gobierno e integridad Git

- adoptada firma SSH Ed25519 para commits y tags nuevos;
- añadido registro público de firmantes autorizados;
- materializados y auditados 23/23 tags firmados de `v0.0.1-beta` a `v0.0.23-beta`;
- ejecutada la reemisión única de `v0.0.22-beta` y `v0.0.23-beta`, preservando `1222de61a6d2ca48fb8731fe4755f5b7eeef38f5` y `07278f7a193ce964612d9697da57350691bf62c0`;
- añadido workflow de verificación de firmas de tags;
- añadidas regresiones de política de firma y trazabilidad histórica;
- primer commit nuevo firmado confirmado por GitHub como `Verified` y CI #23 en `success`;
- verificados 23/23 objetos y targets remotos sin reescritura de commits históricos;
- activado ruleset inmutable para tags `v*`: permite nuevas versiones y bloquea actualización, eliminación y force push de tags publicados;
- activado ruleset de la rama predeterminada con Pull Request obligatorio, firmas verificadas, historial lineal, resolución de conversaciones y checks Python 3.13/3.14;
- configurada la integración mediante `Squash and merge` y la eliminación automática de ramas remotas integradas;
- endurecidos los permisos de GitHub Actions y restringido el uso a acciones propias y oficiales de GitHub;
- activados Dependency graph, Dependabot alerts y Dependabot security updates;
- Dependabot revisado con 0 vulnerabilidades abiertas al habilitar las alertas;
- migradas las GitHub Actions vigentes de `@v6` a `@v7` en todos los workflows actuales.
- corregidas rutas PowerShell documentales afectadas por un carácter de control y añadida regresión preventiva;
- cerrado formalmente el prebloque transversal de firma e integridad Git/GitHub tras completar rulesets, configuración de Actions, Dependabot y auditoría de PR;
- verificado el cierre remoto con 0 Pull Requests abiertos y flujo protegido por rama, firma, PR, CI requerida y squash.

### Dependencias y seguridad

- preparado el salto controlado de `pypdf` `5.9.0` a `6.15.0`;
- añadidas cuatro regresiones específicas sobre versión instalada, `PdfReader`/`PdfWriter`, rechazo controlado de PDFs sin texto y límites de páginas de ambos importadores;
- la aceptación exige instalación reproducible desde `requirements.txt`, `pip check`, suite completa, compilación Python, sintaxis JavaScript y `git diff --check`;
- `VERSION` permanece en `0.0.23-beta`;
- PR de Dependabot `#7` cerrado como sustituido por la actualización controlada; `#6`, `#5` y `#4` cerrados para preservar compatibilidad y el snapshot transitivo reproducible.

## [0.0.23-beta] — 2026-08-17

### GOV.1.3 — Auditoría y reorganización documental

- GOV.1.3 R1 completada y validada con reorganización de documentos de entrada y preservación histórica.
- Separación entre documentación vigente y documentación histórica.
- Reorganización del índice documental.
- Simplificación de README y CONTRIBUTING.
- Conversión del roadmap en un documento de presente/futuro.
- Conservación de bitácoras UX bajo `docs/historico/ux/`.
- Incorporación de regresiones para proteger la estructura documental.
- Validación R1: compilación Python, sintaxis JavaScript, git diff --check, 411 pruebas automatizadas en OK y 8/8 regresiones específicas de documentación.
- GOV.1.3 R2 completada: consolidación de Arquitectura, Modelo de datos, Gestión de datos, Motor, Especificación funcional, Guía interna y Validación.
- Validación R2: compilación Python, sintaxis JavaScript y `git diff --check` sin errores; 423 pruebas automatizadas en `OK`, incluidas 12/12 regresiones específicas de R2 y 8/8 regresiones documentales de R1.
- GOV.1.3 R3 completada: consolidación normativa, modalidades, seguridad, privacidad, términos y matriz interna de alineación con Ley 81; se preserva la versión material de privacidad `2026-08-16.1`.
- Validación R3: compilación Python, sintaxis JavaScript y `git diff --check` sin errores; 438 pruebas automatizadas en `OK`, incluidas 15/15 regresiones específicas de R3, 12/12 de R2 y 8/8 de R1.
- La regresión documental de R2 se endureció para preservar su evidencia de cierre en `CHANGELOG.md` sin depender del estado evolutivo de `VALIDACION.md`.

- GOV.1.3 R4 completada: transparencia, matriz de trazabilidad, auditoría de cálculos, limitaciones conocidas, dependencias/terceros, proceso de release e índice auditable de 158 ADR.
- ADR-086 se conserva como anomalía histórica de metadata sin inventar un estado retroactivo.
- Validación R4 y cierre GOV.1.3: 458 pruebas automatizadas en `OK`, compilación Python, sintaxis JavaScript y `git diff --check` sin errores.

## [0.0.22-beta] — 2026-08-17

Primera versión formal gobernada por `VERSIONING.md`.

### Añadido

- archivo canónico `VERSION`;
- `app/core/version.py`;
- `GOVERNANCE.md`;
- `VERSIONING.md`;
- `RELEASES.md`;
- `.github/CODEOWNERS`;
- regresiones específicas de gobierno/versionado.

### Verificado

- versión canónica, FastAPI y footer sincronizados;
- compilación Python;
- sintaxis JavaScript;
- `git diff --check`;
- 403 pruebas automatizadas en `OK`;
- tag formal `v0.0.22-beta`.

## Estados retrospectivos 0.0.1-beta a 0.0.21-beta

> Estos números son una reconstrucción documental. Los rangos exactos de commits están en `RELEASES.md`.

### [0.0.21-beta] — 2026-08-17

UX.4.6d: cierre del Paso 3, Ficha Digital, reconciliación de cuotas e integración Pasos 1–3.

### [0.0.20-beta] — 2026-08-13

UX.4.6c: cierre del Paso 2, cuotas e importación contextual por campo.

### [0.0.19-beta] — 2026-08-13

UX.4.6b: Paso 1, datos personales, consentimiento, privacidad e importación de Mi Retiro Seguro.

### [0.0.18-beta] — 2026-08-13

UX.4.6a: rediseño visual integral, nueva página de Inicio y sistema visual transversal.

### [0.0.17-beta] — 2026-08-13

Estrategia reproducible de dependencias y mantenimiento pre-beta.

### [0.0.16-beta] — 2026-08-13

Hardening de PDFs, privacidad, regresiones E2E, CI y Dependabot.

### [0.0.15-beta] — 2026-08-13

UX.4.5: comparación entre información acreditada y proyección, con cierre accesible.

### [0.0.14-beta] — 2026-08-13

UX.4.4: edad anual, detalle salarial del año actual e importación documental revisable.

### [0.0.13-beta] — 2026-08-12

UX.4.3: validación accesible, recuperación de foco, teclado y estabilidad del frontend.

### [0.0.12-beta] — 2026-08-12

UX.4.2: estados activos y selección perceptible.

### [0.0.11-beta] — 2026-08-12

UX.4.1: accesibilidad semántica y ayudas contextuales.

### [0.0.10-beta] — 2026-08-12

Mantenimiento técnico de finales de línea, estructura, respaldos y favicon temporal.

### [0.0.9-beta] — 2026-08-12

Identidad de producto, temas, accesibilidad base y terminología pública.

### [0.0.8-beta] — 2026-08-12

UX.3: responsive y precisión del corte mensual de cuotas.

### [0.0.7-beta] — 2026-08-12

Comparador, trazabilidad, resultado unificado y cierre funcional de Fase 6.

### [0.0.6-beta] — 2026-08-11

Organización del repositorio, centralización normativa y casos de validación.

### [0.0.5-beta] — 2026-08-11

Motores del Subsistema Mixto y SUCGS.

### [0.0.4-beta] — 2026-08-11

Motor SEBD, modalidades e Indemnización por Vejez.

### [0.0.3-beta] — 2026-08-11

Retiro, precisión monetaria, pruebas y protección de datos de validación.

### [0.0.2-beta] — 2026-08-11

Historial salarial, proyección y línea temporal.

### [0.0.1-beta] — 2026-08-10

Base técnica, FastAPI, primera interfaz, asistente, cuotas, salario y documentación inicial.

## Evidencia histórica

Para una auditoría completa consultar, en este orden:

1. `RELEASES.md` — rangos Git y clasificación de versiones;
2. `docs/REGISTRO_CAMBIOS_HISTORICO.md` — mapa cronológico;
3. `docs/historico/` — bitácoras y snapshots anteriores;
4. `docs/DECISIONES.md` — ADR;
5. historial Git — evidencia primaria e inmutable de cada cambio versionado.
