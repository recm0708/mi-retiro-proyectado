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
![Versión](https://img.shields.io/badge/versi%C3%B3n-0.1.19.05--beta-2563eb)
![Python](https://img.shields.io/badge/Python-3.13%20%7C%203.14-3776AB?logo=python&logoColor=white)
![Licencia](https://img.shields.io/badge/licencia-propietaria-6B7280)

Mi Retiro Proyectado es una aplicación web local e independiente para **estimar, explicar y comparar escenarios de retiro** de personas aseguradas de la Caja de Seguro Social (CSS) de Panamá.

> **No es una aplicación oficial de la CSS.** No emite certificaciones, no sustituye una resolución administrativa y sus resultados dependen de los datos suministrados, de las reglas implementadas y de la normativa aplicable a cada caso.

## Estado del proyecto

- **Versión canónica vigente:** `0.1.19.05-beta`, obtenida exclusivamente
  desde [`VERSION`](VERSION). Materializa DEV.2 R6 como G119/E05 después
  del desarrollo PR #111 / merge
  `bd2accbea421fc719d9330015533001039648d05` y de esta promoción.
- **Último estado funcional integrado en `main`:** DEV.2 R6 mediante
  PR #111 / merge `bd2accbea421fc719d9330015533001039648d05`.
- **Estado revision-aware reconciliado:** G119/E05 (`0.1.19.05-beta`)
  queda aceptado para DEV.2 R6; G120/E01 (`0.1.20.01-beta`) queda
  reservado para UX.5 R1.
- **Publicación revision-aware vigente durante esta promoción:**
  `v0.1.18.04-beta` (G118/E04), tag anotado y firmado sobre
  `290e84aab70a257e8b718d172e37365af49ef048`; `v0.1.17.02-beta`
  (G117/E02) permanece preservado como publicación histórica anterior.
  La publicación de `v0.1.19.05-beta` ocurre únicamente después del
  merge y revalidación de esta promoción.
- **Última versión formal legacy:** `0.0.26-beta`.
- **Etapa:** desarrollo beta; repositorio público y ejecución orientada
  actualmente a entorno local.
- **REL.GOV.1:** R1 y R2 permanecen cerrados/aceptados como G110/E01
  y G117/E02.
- **DEV.2:** R1–R3 permanecen aceptados históricamente; R4 fue un cierre
  documental sin Global independiente; R5 queda aceptado/publicado como
  G118/E04 y R6 queda aceptado como G119/E05.
- **UX.5:** R1 queda como candidato reservado G120/E01.
- **DOC.1:** R1–R5 cerrados; R6 permanece planificado para congelación
  documental final.
- **SEC.2:** R1–R6 cerrados; R7 permanece planificado después de las
  nuevas superficies UX/persistencia.
- **Primera versión oficial objetivo:** `1.0.0.0` con `Build 000001`.


La visibilidad pública del repositorio **no convierte una beta de desarrollo en versión oficial, no constituye un despliegue de producción y no modifica por sí sola la licencia vigente**.

La versión se obtiene exclusivamente del archivo [`VERSION`](VERSION). La política completa se documenta en [Política de versionado](VERSIONING.md). VER.2 publicó `v0.0.71.01-beta` bajo la denominación original G071/E01; la reconciliación posterior sitúa ese estado en G087/E01 sin alterar el tag, y su evidencia histórica quedó preservada por NOR.2. Los estándares vigentes del repositorio están en [Estándares del repositorio](docs/standards) y el cierre de la normalización se documenta en [Auditorías de normalización del repositorio](docs/audits/repository).

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

La aplicación dispone además de **Developer Diagnostics** y de un **Portal Developer** interno. Developer Diagnostics se activa con `MRP_DEV_MODE=1`; el acceso humano a `/dev` requiere la superficie administrativa habilitada y una cuenta Developer local. `MRP_ADMIN_SECRET`/`MRP_ADMIN_TOKEN` pertenecen exclusivamente al contrato técnico Bearer legado y no son requisito del login humano. Las capacidades Developer no constituyen telemetría de producto ni envían logs automáticamente a terceros.

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

El punto de entrada de la documentación es [Índice de documentación](docs/README.md).

Documentos principales:

- **[Especificación funcional](docs/product/functional-specification.md)** — comportamiento funcional;
- **[Arquitectura](docs/architecture/system-architecture.md)** — arquitectura y componentes;
- **[Modelo de datos](docs/architecture/data-model.md)** — contratos y estructuras;
- **[Motor de cálculo](docs/architecture/calculation-engine.md)** — flujo técnico de cálculo;
- **[Cómo se calcula — contrato de transparencia](docs/product/calculation-guide.md)** — contrato de transparencia de la guía pública de cálculo;
- **[Normativa](docs/regulatory/regulatory-framework.md)** — interpretación y aplicación normativa;
- **[Fuentes normativas y enlaces oficiales](docs/regulatory/regulatory-sources.md)** — fuentes oficiales;
- **[Identidad visual de Mi Retiro Proyectado](docs/product/visual-identity.md)** — logo oficial, derivados, favicons y Social Preview;
- **[Observabilidad y Developer Diagnostics](docs/operations/observability-and-logs.md)** — Developer Diagnostics, esquema y privacidad de logs;
- **[Validación](docs/operations/validation.md)** — estrategia y evidencia de pruebas;
- **[Seguridad y privacidad](docs/security/security-and-privacy.md)** — controles técnicos de seguridad y privacidad;
- **[Modelo de amenazas](docs/security/threat-model.md)** — threat model vigente;
- **[Procedimiento de derechos del titular](docs/security/data-subject-rights-procedure.md)** — ejercicio de derechos;
- **[Procedimiento de respuesta a incidentes de seguridad y privacidad](docs/security/security-incident-procedure.md)** — respuesta a incidentes;
- **[Evaluación de terceros, despliegue y revisión pre-publicación](docs/security/third-party-deployment-assessment.md)** — terceros, TLS y gates de despliegue;
- **[Política de seguridad](SECURITY.md)** — reporte responsable de vulnerabilidades;
- **[Auditoría de GitHub y controles de repositorio](docs/archive/governance/github-audit.md)** — controles GitHub y auditoría automática;
- **[Preparación pública de GitHub](docs/operations/github-public-repository.md)** — metadata, topics, labels, badges, Social Preview y seguridad del repositorio público;
- **[Auditoría integral del repositorio — 2026-08-18](docs/archive/governance/repository-audit-2026-08-18.md)** — auditoría integral post-GOV.1 del repositorio;
- **[Auditoría transversal UX.4.6e R7](docs/archive/ux/ux46e-r7-audit-2026-08-18.md)** — auditoría transversal de coherencia de UX.4.6e;
- **[Cierre GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta](docs/archive/governance/gov1-closeout.md)** — auditoría final y decisión de cierre de GOV.1;
- **[Auditoría de versionado pre-1.0](docs/archive/governance/pre-1-0-versioning-audit.md)** — criterio contable y reconciliación VER.2;
- **[VER.2 — Matriz de decisión de revisiones aceptadas](docs/archive/governance/ver2-revision-decision-matrix.md)** — decisiones de inclusión/exclusión del contador;
- **[Ledger de revisiones aceptadas pre-1.0](docs/governance/pre-1-0-revision-ledger.md)** — secuencia reconciliada G001–G119 y próximo candidato G120/E01 para UX.5 R1;
- [`data/pre-1-0-revision-ledger.json`](data/pre-1-0-revision-ledger.json) — ledger machine-readable;
- **[Identificadores de bloques de trabajo](docs/standards/work-block-identifiers.md)** — política canónica de identificadores de bloques;
- [`data/work-block-registry.json`](data/work-block-registry.json) — registro machine-readable de identificadores históricos, cerrados y planificados;
- **[Licencia y estrategia de distribución](docs/governance/licensing-and-distribution.md)** — decisión de licencia y estrategia de distribución;
- **[Avisos de terceros](THIRD_PARTY_NOTICES.md)** — avisos y obligaciones de terceros;
- **[Roadmap](docs/governance/roadmap.md)** — estado actual y próximos hitos;
- **[Matriz maestra de pendientes hacia 1.0](docs/governance/pre-1-0-pending-matrix.md)** — matriz maestra viva de trabajo pendiente hasta `1.0.0.0`;
- **[Plan maestro hacia Mi Retiro Proyectado 1.0](docs/governance/master-plan-to-1-0.md)** — secuencia de 14 bloques hasta la primera versión oficial;
- **[Registro de decisiones técnicas](docs/decisions/README.md)** — decisiones ADR;
- **[Registro histórico de cambios](docs/archive/governance/historical-change-registry.md)** — mapa histórico de evolución;
- **[Código de conducta](CODE_OF_CONDUCT.md)** — reglas de participación y convivencia;
- **[Soporte](SUPPORT.md)** — rutas de soporte y reporte.

La documentación vigente debe apuntar únicamente a rutas canónicas actuales. Las fases cerradas se preservan mediante Git y, cuando conservan valor documental independiente, bajo `docs/archive/`; NOR.2 no mantendrá stubs permanentes de rutas antiguas solo por compatibilidad documental.

## Versiones e historia

`0.0.1-beta` a `0.0.21-beta` son **estados reconstruidos retrospectivamente** a partir del historial Git. No fueron tags publicados en sus fechas originales.

`0.0.22-beta` fue la primera versión formal adoptada bajo la política de GOV.1.2; `0.0.23-beta` cerró GOV.1.3; `0.0.24-beta` cerró integralmente GOV.1; `0.0.25-beta` cerró UX.4.6e; y `0.0.26-beta` cerró PLAN.1. Sus tags publicados permanecen firmados e inmutables.

El 2026-08-26 se completó el backfill administrativo de GitHub Releases. Con las publicaciones formales posteriores hasta G118/E04, el repositorio cuenta actualmente con **37 tags formales reales** y **37 GitHub Releases**. Los Releases de `v0.0.1-beta`–`v0.0.26-beta` creados retrospectivamente no cambian la fecha histórica, firma ni commit objetivo de sus tags.

Después de `v0.0.26-beta`, UX.4.6f–UX.4.6i continuaron históricamente sobre ese mismo valor de `VERSION`. VER.2 reconstruye todo el tramo sin inventar tags: el último estado aceptado de la base `7037addd` es **G070/E02**, cierre de UX.4.6i.

La nueva familia beta usa `0.GG.RR.EE-beta`. VER.2 R4 promovió `0.0.71.01-beta` bajo la denominación original G071/E01 después de R1, R2 y R3; la reconciliación post-G070 sitúa el estado publicado en G087/E01 y conserva intacto el tag firmado `v0.0.71.01-beta`. No se crean tags revision-aware retrospectivos para G001–G070.

Objetivo de release estable:

```text
Versión 1.0.0.0
Build 000001
Tag v1.0.0.0
```

Consultar:

- **[Registro de versiones y estados del proyecto](RELEASES.md)** — versiones, rangos Git y releases formales;
- **[Changelog](CHANGELOG.md)** — cambios notables por versión;
- **[Auditoría de versionado pre-1.0](docs/archive/governance/pre-1-0-versioning-audit.md)** — criterio de reconciliación;
- **[VER.2 — Matriz de decisión de revisiones aceptadas](docs/archive/governance/ver2-revision-decision-matrix.md)** — matriz de decisiones contables;
- **[Ledger de revisiones aceptadas pre-1.0](docs/governance/pre-1-0-revision-ledger.md)** — contador global pre-1.0;
- [`data/pre-1-0-revision-ledger.json`](data/pre-1-0-revision-ledger.json) — representación machine-readable;
- **[Registro histórico de cambios](docs/archive/governance/historical-change-registry.md)** — mapa cronológico para auditoría.

Git continúa siendo la evidencia primaria de autores, fechas, hashes y contenido histórico.

## Arquitectura resumida

```text
mi-retiro-proyectado/
├── .githooks/
├── .github/
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
│   ├── archive/
│   ├── audits/
│   ├── decisions/
│   ├── governance/
│   ├── operations/
│   ├── product/
│   ├── regulatory/
│   ├── security/
│   ├── standards/
│   └── templates/
├── regulations/
├── scripts/
├── tests/
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── LICENSE
├── RELEASES.md
├── SECURITY.md
├── SUPPORT.md
├── THIRD_PARTY_NOTICES.md
├── VERSION
├── VERSIONING.md
└── requirements.txt
```

El árbol anterior representa únicamente rutas **versionadas y canónicas**. Elementos locales como `.venv/`, `_deliverables/`, caches y logs de diagnóstico no forman parte de la arquitectura versionada y no deben añadirse al README.

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

Para activar Developer Diagnostics y el Portal Developer en una sesión local de desarrollo:

```powershell
$env:MRP_DEV_MODE = "1"
$env:MRP_ADMIN_ENABLED = "1"
python -m uvicorn app.main:app --reload

# Solo si se necesita el contrato técnico Bearer legado:
# $env:MRP_ADMIN_SECRET = "<define-tu-secreto-local-no-versionado>"
```

Abrir el Portal Developer en:

```text
http://127.0.0.1:8000/dev
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

La simulación previsional no utiliza cuentas de usuario ni una base de datos permanente de simulaciones. El Portal Developer sí dispone de cuentas administrativas locales, separadas de los datos previsionales. Los documentos seleccionados para importación se procesan bajo los controles documentados y los originales personales no deben incorporarse al repositorio público.

Developer Diagnostics no debe registrar cuerpos HTTP, contenido PDF, identidad, salarios, cuotas detalladas, montos de pensión, cookies, tokens ni mensajes de excepción potencialmente sensibles. Los logs son locales, rotan y están excluidos de Git.

Los casos de validación versionados deben ser sintéticos o estar anonimizados de forma irreversible para el propósito de la prueba.

Consultar:

- **[Política de privacidad y tratamiento de datos](docs/security/privacy-policy.md)**;
- **[Términos de uso, privacidad y tratamiento de datos](docs/security/terms-and-privacy.md)**;
- **[Matriz interna de alineación con Ley 81 de 2019](docs/regulatory/law-81-compliance.md)**;
- **[Observabilidad y Developer Diagnostics](docs/operations/observability-and-logs.md)**;
- **[Casos de validación](tests/validation_cases/README.md)**.

## Gobierno y contribución

- **[Gobierno del proyecto](GOVERNANCE.md)** — responsabilidades y gobierno;
- **[Guía de contribución](CONTRIBUTING.md)** — flujo de trabajo;
- **[Política de versionado](VERSIONING.md)** — versionado;
- [`.github/CODEOWNERS`](.github/CODEOWNERS) — propiedad de revisión;
- **[Registro de decisiones técnicas](docs/decisions/README.md)** — ADR;
- **[Código de conducta](CODE_OF_CONDUCT.md)** — normas de participación;
- **[Soporte](SUPPORT.md)** — rutas de consulta y reporte.

## Licencia

Los materiales originales de Mi Retiro Proyectado se mantienen bajo una **licencia propietaria pre-beta / todos los derechos reservados**. La disponibilidad pública del código fuente **no concede por sí sola permiso** para copiar, modificar, redistribuir, sublicenciar, explotar comercialmente o crear obras derivadas.

Consultar:

- [`LICENSE`](LICENSE);
- **[Licencia y estrategia de distribución](docs/governance/licensing-and-distribution.md)**;
- **[Avisos de terceros](THIRD_PARTY_NOTICES.md)**.

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
python -m uvicorn app.main:app --reload

# Solo para el contrato técnico Bearer legado, si se necesita:
# $env:MRP_ADMIN_SECRET = "<define-tu-secreto-local-no-versionado>"
```

No existe una clave administrativa predeterminada ni una cuenta Developer
predeterminada en el repositorio. El acceso humano requiere una identidad
Developer local previamente provisionada. `MRP_ADMIN_SECRET`/`MRP_ADMIN_TOKEN` quedan reservados al contrato
técnico Bearer legado y **no autentican el login humano**. Ninguna credencial
debe publicarse, compartirse ni versionarse. `MRP_ADMIN_ENABLED` actúa como
kill switch: si no vale `1`, el Portal Developer permanece bloqueado aunque
exista una sesión anterior.

Accesos locales:

- aplicación: <http://127.0.0.1:8000>;
- Portal Developer humano: <http://127.0.0.1:8000/dev>;
- compatibilidad de entrada: <http://127.0.0.1:8000/dev/login>;
- acceso técnico legado: <http://127.0.0.1:8000/dev/centro-desarrollo>.

El login del navegador crea una sesión administrativa temporal mediante la
cookie técnica `mrp_admin_session`, `HttpOnly`, con `SameSite` configurable,
expiración por inactividad y límite absoluto. Para un despliegue interno HTTPS
debe configurarse `MRP_ADMIN_COOKIE_SECURE=1`. El cierre de sesión se realiza
mediante `POST /dev/logout`.

La activación de Developer Diagnostics no habilita por sí sola funciones
administrativas. SEC.2 mantiene además autenticación Bearer para clientes
técnicos, eventos de auditoría locales y prohibiciones de registrar secretos,
cookies o información sensible.
