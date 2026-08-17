# Mi Retiro Proyectado

Mi Retiro Proyectado es una aplicación web local e independiente para **estimar, explicar y comparar escenarios de retiro** de personas aseguradas de la Caja de Seguro Social (CSS) de Panamá.

> **No es una aplicación oficial de la CSS.** No emite certificaciones, no sustituye una resolución administrativa y sus resultados dependen de los datos suministrados, de las reglas implementadas y de la normativa aplicable a cada caso.

## Estado del proyecto

- **Versión formal vigente:** `0.0.23-beta`
- **Etapa:** desarrollo interno pre-beta
- **Programa activo:** GOV.1 — Auditoría, Gobierno y Trazabilidad Pre-Beta
- **Bloque activo:** GOV.1.4 — Observabilidad y Developer Diagnostics
- **Primera beta pública objetivo:** familia `0.1.0-beta.1`

La versión se obtiene exclusivamente del archivo [`VERSION`](VERSION). La política completa se documenta en [`VERSIONING.md`](VERSIONING.md).

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

## Principios de diseño

El proyecto aplica estos criterios:

- fórmulas previsionales en Python, no duplicadas en JavaScript;
- parámetros normativos versionados en `normativa/`;
- separación explícita entre datos acreditados y proyectados;
- trazabilidad de fuentes, decisiones e hipótesis;
- datos faltantes explícitos en vez de parámetros inventados;
- procesamiento local y minimización de datos personales;
- pruebas automatizadas y CI antes de cerrar hitos;
- documentación como parte obligatoria de cada cambio.

## Documentación

El punto de entrada de la documentación es [`docs/INDICE.md`](docs/INDICE.md).

Documentos principales:

- [`docs/ESPECIFICACION_FUNCIONAL.md`](docs/ESPECIFICACION_FUNCIONAL.md) — comportamiento funcional;
- [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) — arquitectura y componentes;
- [`docs/MODELO_DE_DATOS.md`](docs/MODELO_DE_DATOS.md) — contratos y estructuras;
- [`docs/MOTOR_DE_CALCULO.md`](docs/MOTOR_DE_CALCULO.md) — flujo técnico de cálculo;
- [`docs/NORMATIVA.md`](docs/NORMATIVA.md) — interpretación y aplicación normativa;
- [`docs/FUENTES_NORMATIVAS.md`](docs/FUENTES_NORMATIVAS.md) — fuentes oficiales;
- [`docs/VALIDACION.md`](docs/VALIDACION.md) — estrategia y evidencia de pruebas;
- [`docs/SEGURIDAD_PRIVACIDAD.md`](docs/SEGURIDAD_PRIVACIDAD.md) — controles técnicos de seguridad y privacidad;
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — estado actual y próximos hitos;
- [`docs/DECISIONES.md`](docs/DECISIONES.md) — decisiones ADR;
- [`docs/REGISTRO_CAMBIOS_HISTORICO.md`](docs/REGISTRO_CAMBIOS_HISTORICO.md) — mapa histórico de evolución.

Los documentos de UX que funcionaban como bitácoras de revisión se conservan bajo `docs/historico/ux/`. Las rutas anteriores permanecen como índices de compatibilidad para no romper referencias existentes.

## Versiones e historia

`0.0.1-beta` a `0.0.21-beta` son **estados reconstruidos retrospectivamente** a partir del historial Git. No fueron tags publicados en sus fechas originales.

`0.0.22-beta` es la primera versión formal adoptada bajo la política de GOV.1.2 y dispone del tag:

```text
v0.0.22-beta
```

`0.0.23-beta` cierra GOV.1.3 después de la reorganización integral, la consolidación normativa/privacidad y la incorporación de la capa de auditoría documental y trazabilidad. Su tag formal asociado es:

```text
v0.0.23-beta
```

Consultar:

- [`RELEASES.md`](RELEASES.md) — versiones, rangos Git y releases formales;
- [`CHANGELOG.md`](CHANGELOG.md) — cambios notables por versión;
- [`docs/REGISTRO_CAMBIOS_HISTORICO.md`](docs/REGISTRO_CAMBIOS_HISTORICO.md) — mapa cronológico para auditoría.

Git continúa siendo la evidencia primaria de autores, fechas, hashes y contenido histórico.

## Arquitectura resumida

```text
calculadora-pension-css/
├── app/
│   ├── core/
│   ├── modelos/
│   ├── motores/
│   ├── servicios/
│   ├── static/
│   ├── templates/
│   └── main.py
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
- Node.js LTS es opcional para validación sintáctica de JavaScript y no forma parte del runtime.

Clonar:

```powershell
git clone https://github.com/recm0708/calculadora-pension-css.git
cd calculadora-pension-css
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

Ejecutar:

```powershell
python -m uvicorn app.main:app --reload
```

Abrir:

```text
http://127.0.0.1:8000
```

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

La versión actual no dispone de cuentas de usuario ni de una base de datos permanente de simulaciones. Los documentos seleccionados para importación se procesan bajo los controles documentados y los originales personales no deben incorporarse al repositorio.

Los casos de validación versionados deben ser sintéticos o estar anonimizados de forma irreversible para el propósito de la prueba.

Consultar:

- [`docs/POLITICA_PRIVACIDAD.md`](docs/POLITICA_PRIVACIDAD.md);
- [`docs/TERMINOS_USO_PRIVACIDAD.md`](docs/TERMINOS_USO_PRIVACIDAD.md);
- [`docs/CUMPLIMIENTO_LEY_81.md`](docs/CUMPLIMIENTO_LEY_81.md);
- [`tests/casos_validacion/README.md`](tests/casos_validacion/README.md).

## Gobierno y contribución

- [`GOVERNANCE.md`](GOVERNANCE.md) — responsabilidades y gobierno;
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — flujo de trabajo;
- [`VERSIONING.md`](VERSIONING.md) — versionado;
- [`.github/CODEOWNERS`](.github/CODEOWNERS) — propiedad de revisión;
- [`docs/DECISIONES.md`](docs/DECISIONES.md) — ADR.

## Licencia

**El proyecto todavía no ha adoptado una licencia de distribución o reutilización.**

La decisión formal está reservada para GOV.1.7. Hasta que exista un archivo `LICENSE` explícito, la publicación del código en GitHub no debe interpretarse como una concesión automática de derechos de copia, modificación, redistribución o uso comercial más allá de lo permitido por la ley aplicable o por autorización expresa del titular.

## Responsable del proyecto

**Rubén Enrique Cañizares Miranda — Panamá**

El proyecto mantiene una identidad independiente de la Caja de Seguro Social de Panamá.
