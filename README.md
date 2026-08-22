<p align="center">
  <img
    src="assets/brand/logos/logo-mark-512.png"
    alt="Logo de Mi Retiro Proyectado"
    width="132"
  >
</p>

# Mi Retiro Proyectado

[![Validación continua](https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/ci.yml)
[![Auditoría de gobernanza](https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/auditoria-gobernanza.yml/badge.svg?branch=main)](https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/auditoria-gobernanza.yml)
![Versión](https://img.shields.io/badge/versi%C3%B3n-0.0.71.01--beta-2563eb)
![Python](https://img.shields.io/badge/Python-3.13%20%7C%203.14-3776AB?logo=python&logoColor=white)
![Licencia](https://img.shields.io/badge/licencia-propietaria-6B7280)

Mi Retiro Proyectado es una aplicación web local e independiente para **estimar, explicar y comparar escenarios de retiro** de personas aseguradas de la Caja de Seguro Social (CSS) de Panamá.

> **No es una aplicación oficial de la CSS.** No emite certificaciones, no sustituye una resolución administrativa y sus resultados dependen de los datos suministrados, de las reglas implementadas y de la normativa aplicable a cada caso.

## Estado del proyecto

- **Versión candidata de VER.2:** `0.0.71.01-beta` — G071/E01; solo se considera aceptada después de ledger/validador, gate completo, PR/CI e integración.
- **Último estado aceptado reconstruido antes de VER.2:** G070/E02 — cierre UX.4.6i sobre `7037addd44253e528c77460b678d2b3ccd540dd5` con **841 pruebas en `OK`**.
- **Última versión formal legacy etiquetada:** `0.0.26-beta` — tag firmado e inmutable `v0.0.26-beta`.
- **Etapa:** desarrollo beta; repositorio de código público y ejecución de aplicación orientada actualmente a entorno local.
- **Programa GOV.1:** cerrado — Auditoría, Gobierno y Trazabilidad Pre-Beta.
- **Programa PLAN.1:** cerrado — Alineación maestra hacia la primera versión oficial.
- **PLAN.1:** cerrado en el esquema legacy `0.0.26-beta`; PR #23 y PR #24 integrados, **720 pruebas en `OK`** en el gate final y tag firmado `v0.0.26-beta` publicado.
- **Bloque transversal activo:** VER.2 — reconciliación revision-aware del historial pre-1.0.
- **Siguiente bloque funcional:** DEV.2 — Centro de desarrollo; no comienza hasta cerrar VER.2.

- **UX.4.6e:** cerrada históricamente en `0.0.25-beta`; la segunda auditoría distribuye R1–R7, identidad/publicación, R8 y R9/cierre en G041–G050.
- **UX.4.6f:** cerrado — R1/R1.1 integradas mediante PR #28, mantenimiento de dependencias por PR #29, R2 por PR #30 y hardening `pre-commit` por PR #31; **762 pruebas** en el último estado del tramo, G061–G064.
- **Mantenimiento post-R1:** `pypdf 6.16.1` y `Uvicorn 0.52.3` integrados mediante PR #29; PR Dependabot #26/#27 cerrados como sustituidos, con los tres checks requeridos en verde.
- **UX.4.6g:** cerrado — PR #32; selección contextual desde Paso 4, retiro anticipado explícito, +4 años, cobertura de fechas personalizadas, controles de fecha transversales y alineación visual final; **784 pruebas en `OK`**, G065.
- **UX.4.6h:** cerrado — R1 fue candidato fallido; R1.1, R1.2 y R1.3 son los estados aceptados G066–G068; PR #33 cerró el informe A4 con **812 pruebas**.
- **UX.4.6i:** cerrado — la secuencia demostrada es R1 → R1.2 → R1.3 → R1.4; R1 y R1.4 son los estados con aceptación diferenciada contabilizados G069–G070; PR #34 cerró la guía pública `/como-se-calcula` con **841 pruebas**. No existe una UX.4.6i R1.1 independiente.
- **Preparación pública del repositorio:** 21 labels y 20/20 topics configurados; `sebd-panama` adoptado como topic SEBD; Social Preview e identidad visual oficial configurados.
- **Seguridad del repositorio público:** Dependency graph, Dependabot, CodeQL Default setup, Secret Protection, Push protection y Private vulnerability reporting habilitados; revisión manual del 2026-08-19 sin alertas abiertas.
- **Primera versión oficial objetivo:** `1.0.0.0` con `Build 000001`, únicamente después de cerrar todos los gates definidos en el plan maestro.

La visibilidad pública del repositorio **no convierte una beta de desarrollo en versión oficial, no constituye un despliegue de producción y no modifica por sí sola la licencia vigente**.

La versión se obtiene exclusivamente del archivo [`VERSION`](VERSION). La política completa se documenta en [`VERSIONING.md`](VERSIONING.md). La reconciliación actual se audita en [`docs/AUDITORIA_VERSIONADO_PRE_1_0.md`](docs/AUDITORIA_VERSIONADO_PRE_1_0.md) y [`docs/MATRIZ_DECISION_REVISIONES_VER2.md`](docs/MATRIZ_DECISION_REVISIONES_VER2.md); el contador global se materializa en [`docs/LEDGER_REVISIONES_PRE_1_0.md`](docs/LEDGER_REVISIONES_PRE_1_0.md) y [`data/ledger_revisiones_pre_1_0.json`](data/ledger_revisiones_pre_1_0.json). La secuencia restante hacia 1.0 se mantiene en [`docs/PLAN_MAESTRO_HACIA_1_0.md`](docs/PLAN_MAESTRO_HACIA_1_0.md).

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
- parámetros normativos versionados en `normativa/`;
- separación explícita entre datos acreditados y proyectados;
- trazabilidad de fuentes, decisiones e hipótesis;
- datos faltantes explícitos en vez de parámetros inventados;
- procesamiento local y minimización de datos personales;
- observabilidad de desarrollo sin logging de PII ni valores financieros;
- pruebas automatizadas y CI antes de cerrar hitos;
- documentación como parte obligatoria de cada cambio;
- sincronización de código, pruebas, interfaz, normativa y documentación cuando un cambio altera contratos compartidos.

## Documentación

El punto de entrada de la documentación es [`docs/INDICE.md`](docs/INDICE.md).

Documentos principales:

- [`docs/ESPECIFICACION_FUNCIONAL.md`](docs/ESPECIFICACION_FUNCIONAL.md) — comportamiento funcional;
- [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) — arquitectura y componentes;
- [`docs/MODELO_DE_DATOS.md`](docs/MODELO_DE_DATOS.md) — contratos y estructuras;
- [`docs/MOTOR_DE_CALCULO.md`](docs/MOTOR_DE_CALCULO.md) — flujo técnico de cálculo;
- [`docs/COMO_SE_CALCULA.md`](docs/COMO_SE_CALCULA.md) — contrato de transparencia de la guía pública de cálculo;
- [`docs/NORMATIVA.md`](docs/NORMATIVA.md) — interpretación y aplicación normativa;
- [`docs/FUENTES_NORMATIVAS.md`](docs/FUENTES_NORMATIVAS.md) — fuentes oficiales;
- [`docs/IDENTIDAD_VISUAL.md`](docs/IDENTIDAD_VISUAL.md) — logo oficial, derivados, favicons y Social Preview;
- [`docs/OBSERVABILIDAD_LOGS.md`](docs/OBSERVABILIDAD_LOGS.md) — Developer Diagnostics, esquema y privacidad de logs;
- [`docs/VALIDACION.md`](docs/VALIDACION.md) — estrategia y evidencia de pruebas;
- [`docs/SEGURIDAD_PRIVACIDAD.md`](docs/SEGURIDAD_PRIVACIDAD.md) — controles técnicos de seguridad y privacidad;
- [`docs/MODELO_AMENAZAS.md`](docs/MODELO_AMENAZAS.md) — threat model vigente;
- [`docs/PROCEDIMIENTO_DERECHOS_TITULAR.md`](docs/PROCEDIMIENTO_DERECHOS_TITULAR.md) — ejercicio de derechos;
- [`docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md`](docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md) — respuesta a incidentes;
- [`docs/EVALUACION_TERCEROS_DESPLIEGUE.md`](docs/EVALUACION_TERCEROS_DESPLIEGUE.md) — terceros, TLS y gates de despliegue;
- [`SECURITY.md`](SECURITY.md) — reporte responsable de vulnerabilidades;
- [`docs/AUDITORIA_GITHUB.md`](docs/AUDITORIA_GITHUB.md) — controles GitHub y auditoría automática;
- [`docs/PREPARACION_PUBLICA_GITHUB.md`](docs/PREPARACION_PUBLICA_GITHUB.md) — metadata, topics, labels, badges, seguridad y mantenimiento del repositorio público;
- [`docs/AUDITORIA_REPOSITORIO_2026-08-18.md`](docs/AUDITORIA_REPOSITORIO_2026-08-18.md) — auditoría integral post-GOV.1 del repositorio;
- [`docs/AUDITORIA_UX46E_R7_2026-08-18.md`](docs/AUDITORIA_UX46E_R7_2026-08-18.md) — auditoría transversal de coherencia de UX.4.6e;
- [`docs/CIERRE_GOV1.md`](docs/CIERRE_GOV1.md) — auditoría final y decisión de cierre de GOV.1;
- [`docs/AUDITORIA_VERSIONADO_PRE_1_0.md`](docs/AUDITORIA_VERSIONADO_PRE_1_0.md) — criterio contable y reconciliación VER.2;
- [`docs/MATRIZ_DECISION_REVISIONES_VER2.md`](docs/MATRIZ_DECISION_REVISIONES_VER2.md) — decisiones de inclusión/exclusión del contador;
- [`docs/LEDGER_REVISIONES_PRE_1_0.md`](docs/LEDGER_REVISIONES_PRE_1_0.md) — secuencia global G001–G070 y candidato G071;
- [`data/ledger_revisiones_pre_1_0.json`](data/ledger_revisiones_pre_1_0.json) — ledger machine-readable;
- [`docs/LICENCIA_Y_DISTRIBUCION.md`](docs/LICENCIA_Y_DISTRIBUCION.md) — decisión de licencia y estrategia de distribución;
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) — avisos y obligaciones de terceros;
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — estado actual y próximos hitos;
- [`docs/PLAN_MAESTRO_HACIA_1_0.md`](docs/PLAN_MAESTRO_HACIA_1_0.md) — secuencia de 14 bloques hasta la primera versión oficial;
- [`docs/DECISIONES.md`](docs/DECISIONES.md) — decisiones ADR;
- [`docs/REGISTRO_CAMBIOS_HISTORICO.md`](docs/REGISTRO_CAMBIOS_HISTORICO.md) — mapa histórico de evolución;
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — reglas de participación y convivencia;
- [`SUPPORT.md`](SUPPORT.md) — rutas de soporte y reporte.

Los documentos de UX que funcionaban como bitácoras de revisión se conservan bajo `docs/historico/ux/`. Las rutas anteriores permanecen como índices de compatibilidad para no romper referencias existentes.

## Versiones e historia

`0.0.1-beta` a `0.0.21-beta` son **estados reconstruidos retrospectivamente** a partir del historial Git. No fueron tags publicados en sus fechas originales.

`0.0.22-beta` fue la primera versión formal adoptada bajo la política de GOV.1.2; `0.0.23-beta` cerró GOV.1.3; `0.0.24-beta` cerró integralmente GOV.1; `0.0.25-beta` cerró UX.4.6e; y `0.0.26-beta` cerró PLAN.1. Sus tags publicados permanecen firmados e inmutables.

Después de `v0.0.26-beta`, UX.4.6f–UX.4.6i continuaron históricamente sobre ese mismo valor de `VERSION`. VER.2 reconstruye todo el tramo sin inventar tags: el último estado aceptado de la base `7037addd` es **G070/E02**, cierre de UX.4.6i.

La nueva familia beta usa `0.GG.RR.EE-beta`. El candidato actual de reconciliación es `0.0.71.01-beta` (G071/E01). Solo se convierte en estado aceptado si supera el ledger/validador, gate completo, PR/CI e integración; no se crean tags revision-aware retrospectivos para G001–G070.

Objetivo de release estable:

```text
Versión 1.0.0.0
Build 000001
Tag v1.0.0.0
```

Consultar:

- [`RELEASES.md`](RELEASES.md) — versiones, rangos Git y releases formales;
- [`CHANGELOG.md`](CHANGELOG.md) — cambios notables por versión;
- [`docs/AUDITORIA_VERSIONADO_PRE_1_0.md`](docs/AUDITORIA_VERSIONADO_PRE_1_0.md) — criterio de reconciliación;
- [`docs/MATRIZ_DECISION_REVISIONES_VER2.md`](docs/MATRIZ_DECISION_REVISIONES_VER2.md) — matriz de decisiones contables;
- [`docs/LEDGER_REVISIONES_PRE_1_0.md`](docs/LEDGER_REVISIONES_PRE_1_0.md) — contador global pre-1.0;
- [`data/ledger_revisiones_pre_1_0.json`](data/ledger_revisiones_pre_1_0.json) — representación machine-readable;
- [`docs/REGISTRO_CAMBIOS_HISTORICO.md`](docs/REGISTRO_CAMBIOS_HISTORICO.md) — mapa cronológico para auditoría.

Git continúa siendo la evidencia primaria de autores, fechas, hashes y contenido histórico.

## Arquitectura resumida

```text
mi-retiro-proyectado/
├── app/
│   ├── core/
│   ├── modelos/
│   ├── motores/
│   ├── servicios/
│   ├── static/
│   ├── templates/
│   └── main.py
├── assets/
│   ├── brand/
│   └── social/
├── data/
├── docs/
│   └── historico/
├── normativa/
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
.\scripts\configurar_hooks_git.ps1
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

- [`docs/POLITICA_PRIVACIDAD.md`](docs/POLITICA_PRIVACIDAD.md);
- [`docs/TERMINOS_USO_PRIVACIDAD.md`](docs/TERMINOS_USO_PRIVACIDAD.md);
- [`docs/CUMPLIMIENTO_LEY_81.md`](docs/CUMPLIMIENTO_LEY_81.md);
- [`docs/OBSERVABILIDAD_LOGS.md`](docs/OBSERVABILIDAD_LOGS.md);
- [`tests/casos_validacion/README.md`](tests/casos_validacion/README.md).

## Gobierno y contribución

- [`GOVERNANCE.md`](GOVERNANCE.md) — responsabilidades y gobierno;
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — flujo de trabajo;
- [`VERSIONING.md`](VERSIONING.md) — versionado;
- [`.github/CODEOWNERS`](.github/CODEOWNERS) — propiedad de revisión;
- [`docs/DECISIONES.md`](docs/DECISIONES.md) — ADR;
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — normas de participación;
- [`SUPPORT.md`](SUPPORT.md) — rutas de soporte y reporte.

## Licencia

Los materiales originales de Mi Retiro Proyectado se mantienen bajo una **licencia propietaria pre-beta / todos los derechos reservados**. La disponibilidad pública del código fuente **no concede por sí sola permiso** para copiar, modificar, redistribuir, sublicenciar, explotar comercialmente o crear obras derivadas.

Consultar:

- [`LICENSE`](LICENSE);
- [`docs/LICENCIA_Y_DISTRIBUCION.md`](docs/LICENCIA_Y_DISTRIBUCION.md);
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

Las dependencias y materiales de terceros conservan sus propias licencias y derechos.

## Responsable del proyecto

**Rubén Enrique Cañizares Miranda — Panamá**

El proyecto mantiene una identidad independiente de la Caja de Seguro Social de Panamá.
