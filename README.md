<p align="center">
  <img
    src="assets/brand/logos/logo-mark-512.png"
    alt="Logo de Mi Retiro Proyectado"
    width="132"
  >
</p>

# Mi Retiro Proyectado

[![Validación continua](https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/ci.yml)
[![Auditoría de gobernanza](https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/governance-audit.yml/badge.svg?branch=main)](https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/governance-audit.yml)
![Versión](https://img.shields.io/badge/versi%C3%B3n-0.1.11.01--beta-2563eb)
![Python](https://img.shields.io/badge/Python-3.13%20%7C%203.14-3776AB?logo=python&logoColor=white)
![Licencia](https://img.shields.io/badge/licencia-propietaria-6B7280)

Mi Retiro Proyectado es una aplicación web local e independiente para **estimar, explicar y comparar escenarios de retiro** de personas aseguradas de la Caja de Seguro Social (CSS) de Panamá.

> **No es una aplicación oficial de la CSS.** No emite certificaciones, no sustituye una resolución administrativa y sus resultados dependen de los datos suministrados, de las reglas implementadas y de la normativa aplicable a cada caso.

## Estado del proyecto

- **Versión canónica vigente:** `0.1.11.01-beta`, obtenida exclusivamente desde [`VERSION`](VERSION). Materializa G111/E01 después de DOC.2 R1 y está publicada mediante el tag firmado/GitHub Release `v0.1.11.01-beta`.
- **Última promoción integrada en `main`:** G111/E01 en `7e81034` (PR #88), posterior al cierre DOC.2 R1 en `1041b59` (PR #87).
- **Estado de SEC.2:** cerrado después de R1–R6; AUD.SEC2 R1 corrigió la regresión del kill switch administrativo, alineó documentación/ledger y quedó aceptado como G109.
- **Estado revision-aware reconciliado:** G111/E01 (`0.1.11.01-beta`) aceptado para DOC.2; G112/E07 (`0.1.12.07-beta`) queda reservado para NOR.1 R8 como checkpoint transversal previo a PERSIST.1.
- **Último tag revision-aware publicado:** `v0.1.11.01-beta` (G111/E01), firmado, verificado y asociado a GitHub Release prerelease; los tags anteriores permanecen preservados.
- **Última versión formal legacy:** `0.0.26-beta` — tag firmado e inmutable `v0.0.26-beta`.
- **Etapa:** desarrollo beta; repositorio público y ejecución orientada actualmente a entorno local.
- **GOV.1, PLAN.1, DEV.2, MANT.1, DOC.1 R1, NOR.2 y DOC.1 R2:** cerrados; NOR.1 conserva su cierre aceptado en R7 y está reabierto únicamente como candidato R8, todavía sin aceptar.
- **NOR.2:** cerrado después de R1–R8; sus evidencias históricas permanecen preservadas.
- **SEC.2:** R1–R6 cerrados: hardening CodeQL, autenticación administrativa, protección centralizada, auditoría, sesión web y endurecimiento configurable para HTTPS interno.
- **DOC.2:** cerrado en R1 y aceptado como G111/E01 mediante PR #87; la promoción post-merge materializa `0.1.11.01-beta` sin consumir G112. Antes de PERSIST.1 se ejecuta NOR.1 R8; G112 queda reservado para ese checkpoint sin consumirse durante el candidato.
- **Primera versión oficial objetivo:** `1.0.0.0` con `Build 000001`, únicamente después de cerrar todos los gates definidos en el plan maestro.

La visibilidad pública del repositorio **no convierte una beta de desarrollo en versión oficial, no constituye un despliegue de producción y no modifica por sí sola la licencia vigente**.

La versión se obtiene exclusivamente del archivo [`VERSION`](VERSION). La política completa se documenta en [`VERSIONING.md`](VERSIONING.md). VER.2 publicó `v0.0.71.01-beta` bajo la denominación original G071/E01; la reconciliación posterior sitúa ese estado en G087/E01 sin alterar el tag, y su evidencia histórica quedó preservada por NOR.2. Los estándares vigentes del repositorio están en [`docs/standards/`](docs/standards) y el cierre de la normalización se documenta en [`docs/audits/repository/`](docs/audits/repository).

## Capacidades implementadas

La aplicación dispone de un asistente de seis pasos para:

1. registrar datos personales y previsionales;
2. analizar cuotas acreditadas y supuestos de cotización futura;
3. construir y revisar historial salarial, detalle del año actual e información proveniente de documentos compatibles;
4. proyectar escenarios salariales;
5. construir escenarios de retiro;
6. calcular, explicar y comparar resultados previsionales.

Los tres motores generales principales implementados son:

- **SEBD — Subsistema Exclusivamente de Beneficio Definido**;
- **Subsistema Mixto**;
- **SUCGS — Sistema Único de Capitalización con Garantía Solidaria**.

El alcance jurídico y matemático exacto de cada motor se encuentra en la documentación normativa y técnica. No debe asumirse que el motor general cubre regímenes especiales no documentados.

La aplicación dispone además de **Developer Diagnostics** para desarrollo. Está desactivado por defecto y solo se activa mediante `MRP_DEV_MODE=1`; no constituye telemetría de producto ni envía logs automáticamente a terceros.

## Principios de diseño

El proyecto aplica estos criterios:

- fórmulas previsionales en Python, no duplicadas en JavaScript;
- parámetros normativos versionados en `regulations/`;
- separación explícita entre datos acreditados y proyectados;
- trazabilidad de fuentes, decisiones e hipótesis;
- datos faltantes explícitos en vez de parámetros inventados;
- procesamiento local y minimización de datos personales;
- observabilidad de desarrollo sin logging de PII ni valores financieros;
- pruebas automatizadas y CI antes de cerrar hitos;
- documentación como parte obligatoria de cada cambio;
- sincronización de código, pruebas, interfaz, normativa y documentación cuando un cambio altera contratos compartidos.

## Documentación

El punto de entrada de la documentación es [`docs/README.md`](docs/README.md).

Documentos principales:

- [`docs/product/functional-specification.md`](docs/product/functional-specification.md) — comportamiento funcional;
- [`docs/architecture/system-architecture.md`](docs/architecture/system-architecture.md) — arquitectura y componentes;
- [`docs/architecture/data-model.md`](docs/architecture/data-model.md) — contratos y estructuras;
- [`docs/architecture/calculation-engine.md`](docs/architecture/calculation-engine.md) — flujo técnico de cálculo;
- [`docs/product/calculation-guide.md`](docs/product/calculation-guide.md) — contrato de transparencia de la guía pública de cálculo;
- [`docs/regulatory/regulatory-framework.md`](docs/regulatory/regulatory-framework.md) — interpretación y aplicación normativa;
- [`docs/regulatory/regulatory-sources.md`](docs/regulatory/regulatory-sources.md) — fuentes oficiales;
- [`docs/product/visual-identity.md`](docs/product/visual-identity.md) — logo oficial, derivados, favicons y Social Preview;
- [`docs/operations/observability-and-logs.md`](docs/operations/observability-and-logs.md) — Developer Diagnostics, esquema y privacidad de logs;
- [`docs/operations/validation.md`](docs/operations/validation.md) — estrategia y evidencia de pruebas;
- [`docs/security/security-and-privacy.md`](docs/security/security-and-privacy.md) — controles técnicos de seguridad y privacidad;
- [`docs/security/threat-model.md`](docs/security/threat-model.md) — threat model vigente;
- [`docs/security/data-subject-rights-procedure.md`](docs/security/data-subject-rights-procedure.md) — ejercicio de derechos;
- [`docs/security/security-incident-procedure.md`](docs/security/security-incident-procedure.md) — respuesta a incidentes;
- [`docs/security/third-party-deployment-assessment.md`](docs/security/third-party-deployment-assessment.md) — terceros, TLS y gates de despliegue;
- [`SECURITY.md`](SECURITY.md) — reporte responsable de vulnerabilidades;
- [`docs/archive/governance/AUDITORIA_GITHUB.md`](docs/archive/governance/AUDITORIA_GITHUB.md) — controles GitHub y auditoría automática;
- [`docs/operations/github-public-repository.md`](docs/operations/github-public-repository.md) — metadata, topics, labels, badges, Social Preview y seguridad del repositorio público;
- [`docs/archive/governance/AUDITORIA_REPOSITORIO_2026-08-18.md`](docs/archive/governance/AUDITORIA_REPOSITORIO_2026-08-18.md) — auditoría integral post-GOV.1 del repositorio;
- [`docs/archive/ux/AUDITORIA_UX46E_R7_2026-08-18.md`](docs/archive/ux/AUDITORIA_UX46E_R7_2026-08-18.md) — auditoría transversal de coherencia de UX.4.6e;
- [`docs/archive/governance/CIERRE_GOV1.md`](docs/archive/governance/CIERRE_GOV1.md) — auditoría final y decisión de cierre de GOV.1;
- [`docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md`](docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md) — criterio contable y reconciliación VER.2;
- [`docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md`](docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md) — decisiones de inclusión/exclusión del contador;
- [`docs/governance/pre-1-0-revision-ledger.md`](docs/governance/pre-1-0-revision-ledger.md) — secuencia reconciliada G001–G111 y próximo candidato G112;
- [`data/pre-1-0-revision-ledger.json`](data/pre-1-0-revision-ledger.json) — ledger machine-readable;
- [`docs/standards/work-block-identifiers.md`](docs/standards/work-block-identifiers.md) — política canónica de identificadores de bloques;
- [`data/work-block-registry.json`](data/work-block-registry.json) — registro machine-readable de identificadores históricos, cerrados y planificados;
- [`docs/governance/licensing-and-distribution.md`](docs/governance/licensing-and-distribution.md) — decisión de licencia y estrategia de distribución;
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) — avisos y obligaciones de terceros;
- [`docs/governance/roadmap.md`](docs/governance/roadmap.md) — estado actual y próximos hitos;
- [`docs/governance/master-plan-to-1-0.md`](docs/governance/master-plan-to-1-0.md) — secuencia de 14 bloques hasta la primera versión oficial;
- [`docs/decisions/README.md`](docs/decisions/README.md) — decisiones ADR;
- [`docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md`](docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md) — mapa histórico de evolución;
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — reglas de participación y convivencia;
- [`SUPPORT.md`](SUPPORT.md) — rutas de soporte y reporte.

La documentación vigente debe apuntar únicamente a rutas canónicas actuales. Las fases cerradas se preservan mediante Git y, cuando conservan valor documental independiente, bajo `docs/archive/`; NOR.2 no mantendrá stubs permanentes de rutas antiguas solo por compatibilidad documental.

## Versiones e historia

`0.0.1-beta` a `0.0.21-beta` son **estados reconstruidos retrospectivamente** a partir del historial Git. No fueron tags publicados en sus fechas originales.

`0.0.22-beta` fue la primera versión formal adoptada bajo la política de GOV.1.2; `0.0.23-beta` cerró GOV.1.3; `0.0.24-beta` cerró integralmente GOV.1; `0.0.25-beta` cerró UX.4.6e; y `0.0.26-beta` cerró PLAN.1. Sus tags publicados permanecen firmados e inmutables.

El 2026-08-26 se completó el backfill administrativo de GitHub Releases: los **30 tags formales reales** del repositorio cuentan con **30 GitHub Releases**. Los Releases de `v0.0.1-beta`–`v0.0.26-beta` creados retrospectivamente no cambian la fecha histórica, firma ni commit objetivo de sus tags.

Después de `v0.0.26-beta`, UX.4.6f–UX.4.6i continuaron históricamente sobre ese mismo valor de `VERSION`. VER.2 reconstruye todo el tramo sin inventar tags: el último estado aceptado de la base `7037addd` es **G070/E02**, cierre de UX.4.6i.

La nueva familia beta usa `0.GG.RR.EE-beta`. VER.2 R4 promovió `0.0.71.01-beta` bajo la denominación original G071/E01 después de R1, R2 y R3; la reconciliación post-G070 sitúa el estado publicado en G087/E01 y conserva intacto el tag firmado `v0.0.71.01-beta`. No se crean tags revision-aware retrospectivos para G001–G070.

Objetivo de release estable:

```text
Versión 1.0.0.0
Build 000001
Tag v1.0.0.0
```

Consultar:

- [`RELEASES.md`](RELEASES.md) — versiones, rangos Git y releases formales;
- [`CHANGELOG.md`](CHANGELOG.md) — cambios notables por versión;
- [`docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md`](docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md) — criterio de reconciliación;
- [`docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md`](docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md) — matriz de decisiones contables;
- [`docs/governance/pre-1-0-revision-ledger.md`](docs/governance/pre-1-0-revision-ledger.md) — contador global pre-1.0;
- [`data/pre-1-0-revision-ledger.json`](data/pre-1-0-revision-ledger.json) — representación machine-readable;
- [`docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md`](docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md) — mapa cronológico para auditoría.

Git continúa siendo la evidencia primaria de autores, fechas, hashes y contenido histórico.

## Arquitectura resumida

```text
mi-retiro-proyectado/
├── app/
│   ├── core/
│   ├── engines/
│   ├── models/
│   ├── services/
│   ├── static/
│   ├── templates/
│   └── main.py
├── assets/
│   ├── brand/
│   └── social/
├── data/
├── docs/
│   ├── README.md
│   ├── architecture/
│   ├── decisions/
│   ├── governance/
│   ├── operations/
│   ├── product/
│   ├── regulatory/
│   ├── security/
│   ├── standards/
│   ├── audits/
│   ├── archive/
│   └── templates/
├── regulations/
├── tests/
├── .github/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── RELEASES.md
├── VERSION
├── VERSIONING.md
└── requirements.txt
```

## Instalación para desarrollo local

Requisitos principales:

- Python compatible con el proyecto;
- Git;
- PowerShell en los ejemplos de Windows;
- Node.js LTS para el gate de desarrollo y la validación sintáctica de JavaScript; no forma parte del runtime de la aplicación.

Clonar:

```powershell
git clone https://github.com/recm0708/mi-retiro-proyectado.git
cd mi-retiro-proyectado
```

Crear el entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

Activar una sola vez por clon el gate que protege la creación de commits:

```powershell
.\scripts\configure_git_hooks.ps1
```

Ejecutar:

```powershell
python -m uvicorn app.main:app --reload
```

Abrir:

```text
http://127.0.0.1:8000
```

Para activar Developer Diagnostics en una sesión de desarrollo:

```powershell
$env:MRP_DEV_MODE = "1"
python -m uvicorn app.main:app --reload
```

No se recomienda mantener `MRP_DEV_MODE=1` como configuración ordinaria de ejecución.

## Validación mínima

Antes de cerrar un cambio:

```powershell
python -m compileall app
Get-ChildItem .\app\static\js\*.js | ForEach-Object {
    node --check $_.FullName
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
python -m unittest discover -s tests -q
git diff --check
```

La CI del repositorio ejecuta validaciones equivalentes sobre las versiones de Python soportadas por el proyecto.

## Privacidad y datos personales

La versión actual no dispone de cuentas de usuario ni de una base de datos permanente de simulaciones. Los documentos seleccionados para importación se procesan bajo los controles documentados y los originales personales no deben incorporarse al repositorio público.

Developer Diagnostics no debe registrar cuerpos HTTP, contenido PDF, identidad, salarios, cuotas detalladas, montos de pensión, cookies, tokens ni mensajes de excepción potencialmente sensibles. Los logs son locales, rotan y están excluidos de Git.

Los casos de validación versionados deben ser sintéticos o estar anonimizados de forma irreversible para el propósito de la prueba.

Consultar:

- [`docs/security/privacy-policy.md`](docs/security/privacy-policy.md);
- [`docs/security/terms-and-privacy.md`](docs/security/terms-and-privacy.md);
- [`docs/regulatory/law-81-compliance.md`](docs/regulatory/law-81-compliance.md);
- [`docs/operations/observability-and-logs.md`](docs/operations/observability-and-logs.md);
- [`tests/validation_cases/README.md`](tests/validation_cases/README.md).

## Gobierno y contribución

- [`GOVERNANCE.md`](GOVERNANCE.md) — responsabilidades y gobierno;
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — flujo de trabajo;
- [`VERSIONING.md`](VERSIONING.md) — versionado;
- [`.github/CODEOWNERS`](.github/CODEOWNERS) — propiedad de revisión;
- [`docs/decisions/README.md`](docs/decisions/README.md) — ADR;
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — normas de participación;
- [`SUPPORT.md`](SUPPORT.md) — rutas de consulta y reporte.

## Licencia

Los materiales originales de Mi Retiro Proyectado se mantienen bajo una **licencia propietaria pre-beta / todos los derechos reservados**. La disponibilidad pública del código fuente **no concede por sí sola permiso** para copiar, modificar, redistribuir, sublicenciar, explotar comercialmente o crear obras derivadas.

Consultar:

- [`LICENSE`](LICENSE);
- [`docs/governance/licensing-and-distribution.md`](docs/governance/licensing-and-distribution.md);
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

Las dependencias y materiales de terceros conservan sus propias licencias y derechos.

## Responsable del proyecto

**Rubén Enrique Cañizares Miranda — Panamá**

El proyecto mantiene una identidad independiente de la Caja de Seguro Social de Panamá.

## Anclas históricas preservadas por pruebas de regresión

Las siguientes líneas se conservan como compatibilidad histórica de pruebas anteriores. No reemplazan el estado vigente declarado en la sección **Estado del proyecto**.


- **DOC.1 R1:** cerrado — auditoría Markdown post-MANT.1 preservada como hito histórico.
- **DOC.1 R2:** cerrado — auditoría integral Markdown post-NOR.2 preservada como hito histórico.
- **GOV.1:** cerrado.
- **PLAN.1:** cerrado.
- **DEV.2:** cerrado.
- **NOR.1:** cerrado en R7; referencia histórica del cierre de estándares.
- **NOR.2 R2:** cerrado; referencia histórica de la matriz de migración.
- **NOR.2 R3:** cerrado; referencia histórica de la migración técnica.
- **NOR.2 R4:** cerrado; referencia histórica de la migración documental viva.
- **NOR.2 R5:** cerrado; referencia histórica del archivo documental.
- **NOR.2 R6:** cerrado; referencia histórica del checkpoint de ledger G070.
- **NOR.2 R7:** cerrado; referencia histórica de artefactos locales.
- **NOR.2 R8:** cerrado; referencia histórica del cierre integral.
- **SEC.2:** R1 cerrado; hardening CodeQL del informe imprimible y normalización técnica de GitHub Actions completados. Esta línea es una ancla histórica; el estado vigente es SEC.2 R1–R6 cerrado.
- **G071/E01 promovido en `VERSION`:** declaración histórica de VER.2 R4; AUD.SEC2 R1 documenta la reconciliación posterior que sitúa ese estado en G087 sin alterar el tag publicado.

- **Bloque transversal activo:** VER.2 — ancla histórica previa a DOC.1 R1; el estado vigente actual lo define la línea base post-MANT.1.
- **Bloque transversal pendiente:** VER.2 — ancla histórica previa al cierre post-MANT.1; el estado vigente lo define DOC.1 R1 y la línea base documental.
- **Siguiente bloque funcional:** DEV.2 — ancla histórica de cierre DEV.2; DEV.2 queda preservado como bloque funcional cerrado.
- repositorio de código público — formulación histórica preservada; el estado vigente usa repositorio público y ejecución local.
- 21 labels y 20/20 topics configurados.
- 21 labels y 20/20 topics.
- **720 pruebas en `OK`** — evidencia histórica PLAN.1.
- **841 pruebas** — evidencia histórica UX.4.6i / DEV.2.
- **UX.4.6f:** cerrado — evidencia histórica del cierre funcional UX.4.6f.
- R1 → R1.2 → R1.3 → R1.4 — secuencia histórica UX.4.6i.
- **Versión histórica VER.2:** `0.0.71.01-beta` — publicada originalmente como G071/E01 y reconciliada posteriormente como G087/E01; el tag firmado `v0.0.71.01-beta` permanece inmutable.
- `sebd-panama` adoptado.
- tag firmado `v0.0.26-beta` publicado.
- Social Preview e identidad visual oficial configurados.
- referencia histórica preservada.

<!-- ANCLAS_HISTORICAS_VER2_README_CONSOLIDADAS -->

## Compatibilidad histórica preservada por VER.2

Estas referencias conservan evidencia de regresiones históricas sin cambiar el estado vigente de VER.2.

- **Versión candidata de VER.2:** `0.0.26-beta` — referencia legacy preservada para las pruebas históricas previas a la reconciliación revision-aware.
- **GOV.1.8:** Auditoría final y cierre pre-beta de gobierno preservado como cierre histórico del programa GOV.1.
- **GOV.1.4:** Observabilidad y Developer Diagnostics cerrado.
- **GOV.1.5:** Seguridad, privacidad y transparencia cerrado internamente.
- **GOV.1.7:** Licencia propietaria pre-beta.
- **UX.4.6e:** cerrada en `0.0.25-beta`; R8/R9 quedan preservadas como cierre funcional y documental histórico antes de los bloques UX.4.6f–UX.4.6i.
- UX.4.6e R9.1 se conserva como candidato local histórico validado con 660 pruebas en `OK`.
- PR #21 integrado por squash preserva el cierre histórico de UX.4.6e R9.2 en `0.0.25-beta`.
- Tag histórico `v0.0.25-beta` preservado como cierre formal de UX.4.6e.
- **PLAN.1:** cerrado en `0.0.26-beta`; PR #23 y PR #24 preservan el cierre legacy antes de la reconciliación revision-aware.
- `0.1.0-beta.1` se conserva como referencia histórica previa a PLAN.1; VER.2 no la reactiva como familia vigente.
- Badge histórico preservado: `img.shields.io/badge/versi%C3%B3n-0.0.26--beta`.


## Developer Diagnostics y acceso al portal de desarrollo

Developer Diagnostics es una capacidad exclusiva de desarrollo local. Permanece
desactivada por defecto y no forma parte de una telemetría de usuarios.

Inicio normal de la aplicación:

```powershell
python -m uvicorn app.main:app --reload
```

Acceso local:

```text
http://127.0.0.1:8000
```

Activación temporal de diagnósticos y de la superficie administrativa:

```powershell
$env:MRP_DEV_MODE = "1"
$env:MRP_ADMIN_ENABLED = "1"
$env:MRP_ADMIN_SECRET = "<define-tu-secreto-local-no-versionado>"
python -m uvicorn app.main:app --reload
```

No existe una clave administrativa predeterminada en el repositorio. El valor
que el operador asigne a `MRP_ADMIN_SECRET` es la credencial de ese entorno y
**no debe publicarse, compartirse ni versionarse**. `MRP_ADMIN_ENABLED` actúa
como kill switch: si no vale `1`, el login y el Centro de desarrollo quedan
bloqueados aunque exista un secreto o una sesión anterior.

Accesos locales:

- aplicación: <http://127.0.0.1:8000>;
- login administrativo: <http://127.0.0.1:8000/dev/login>;
- Centro de desarrollo: <http://127.0.0.1:8000/dev/centro-desarrollo>.

El login del navegador crea una sesión administrativa temporal mediante la
cookie técnica `mrp_admin_session`, `HttpOnly`, con `SameSite` configurable,
expiración por inactividad y límite absoluto. Para un despliegue interno HTTPS
debe configurarse `MRP_ADMIN_COOKIE_SECURE=1`. El cierre de sesión se realiza
mediante `POST /dev/logout`.

La activación de Developer Diagnostics no habilita por sí sola funciones
administrativas. SEC.2 mantiene además autenticación Bearer para clientes
técnicos, eventos de auditoría locales y prohibiciones de registrar secretos,
cookies o información sensible.
