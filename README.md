<p align="center">
  <img
    src="assets/brand/logos/logo-mark-512.png"
    alt="Logo de Mi Retiro Proyectado"
    width="132"
  >
</p>

<h1 align="center">Mi Retiro Proyectado</h1>

<p align="center">
  <a href="https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/quality-gate.yml"><img alt="Repository Quality Gate" src="https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/quality-gate.yml/badge.svg?branch=main"></a>
  <a href="https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/dependency-security.yml"><img alt="Dependency Security" src="https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/dependency-security.yml/badge.svg?branch=main"></a>
  <a href="https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/visual-a11y.yml"><img alt="Visual & Accessibility" src="https://github.com/recm0708/mi-retiro-proyectado/actions/workflows/visual-a11y.yml/badge.svg?branch=main"></a>
</p>

<p align="center">
  <img alt="Versión 0.129.3.0-beta" src="https://img.shields.io/badge/versi%C3%B3n-0.129.3.0--beta-2563eb">
  <img alt="Python 3.13 y 3.14" src="https://img.shields.io/badge/Python-3.13%20%7C%203.14-3776AB?logo=python&logoColor=white">
  <img alt="Licencia propietaria" src="https://img.shields.io/badge/licencia-propietaria-6B7280">
</p>

Mi Retiro Proyectado es una aplicación web para **estimar, explicar y comparar
escenarios de retiro** de personas aseguradas de la Caja de Seguro Social
(CSS) de Panamá. El proyecto se ejecuta localmente, mantiene sus reglas
previsionales y fuentes versionadas y busca hacer explícitos los supuestos,
datos utilizados y resultados de cada simulación.

> **Mi Retiro Proyectado no es una aplicación oficial de la CSS.** Sus
> resultados son estimaciones informativas: no emiten certificaciones, no
> sustituyen resoluciones administrativas y dependen de los datos suministrados,
> de las reglas implementadas y de la normativa aplicable a cada caso.

## Estado del proyecto

- **Etapa:** desarrollo beta.
- **Versión de desarrollo:** `0.129.3.0-beta`, definida por [`VERSION`](VERSION).
- **Compatibilidad de desarrollo:** Python 3.13 y 3.14.
- **Modelo de ejecución:** aplicación web local; el repositorio público no
  representa por sí mismo un despliegue de producción.
- **Objetivo de primera versión oficial:** `1.0.0.0`.

La política de numeración, aceptación y publicación se mantiene en
[Política de versionado](VERSIONING.md). El historial de estados publicados se
conserva en [Releases](RELEASES.md), [Changelog](CHANGELOG.md), Git, tags y
GitHub Releases; el README no replica esa cronología.

## Qué permite hacer

La experiencia principal usa un asistente de seis pasos para:

1. registrar datos personales y previsionales necesarios para la simulación;
2. revisar cuotas acreditadas y supuestos de cotización futura;
3. construir y validar el historial salarial y la información importada;
4. proyectar escenarios salariales;
5. configurar escenarios de retiro;
6. calcular, explicar y comparar resultados.

Los motores generales implementados cubren:

- **SEBD — Subsistema Exclusivamente de Beneficio Definido**;
- **Subsistema Mixto**;
- **SUCGS — Sistema Único de Capitalización con Garantía Solidaria**.

La cobertura exacta, las reglas aplicadas, las limitaciones y las fuentes se
documentan en [Especificación funcional](docs/product/functional-specification.md),
[Motor de cálculo](docs/architecture/calculation-engine.md),
[Marco normativo](docs/regulatory/regulatory-framework.md) y
[Limitaciones conocidas](docs/product/known-limitations.md).

El repositorio también incluye herramientas internas de desarrollo, entre ellas
Developer Diagnostics y el Portal Developer. Esas superficies no forman parte
de la experiencia previsional pública y su contrato técnico se documenta en
[Centro de desarrollo](docs/architecture/development-center.md) y
[Observabilidad y logs](docs/operations/observability-and-logs.md).

## Principios del proyecto

- fórmulas previsionales centralizadas en Python;
- parámetros normativos versionados en `regulations/`;
- distinción explícita entre datos acreditados, importados y proyectados;
- trazabilidad de fuentes, decisiones e hipótesis;
- datos faltantes visibles en lugar de parámetros inventados;
- procesamiento local y minimización de datos personales;
- protección de secretos, PII y datos financieros en logs y pruebas;
- pruebas automatizadas y gates reproducibles antes de integrar cambios;
- documentación, normativa, código y pruebas sincronizados cuando comparten un
  mismo contrato.

## Inicio rápido

### Requisitos

- Git;
- Python compatible con el proyecto;
- PowerShell para los ejemplos de Windows;
- Node.js LTS cuando se ejecute el gate completo de desarrollo.

### Clonar y preparar el entorno

```powershell
git clone https://github.com/recm0708/mi-retiro-proyectado.git
cd mi-retiro-proyectado

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements-dev.txt
```

`requirements-dev.txt` incluye las dependencias de runtime definidas en
`requirements.txt`.

### Ejecutar la aplicación

```powershell
python -m uvicorn app.main:app --reload
```

Abrir <http://127.0.0.1:8000> en el navegador.

Las funciones administrativas y de diagnóstico permanecen desactivadas o
protegidas según su configuración. No se incluyen credenciales predeterminadas
en el repositorio. Para trabajar con esas superficies, consulta
[Centro de desarrollo](docs/architecture/development-center.md).

## Validación

El gate local completo es:

```powershell
python scripts/quality_gate.py --full
```

En un clon nuevo puede configurarse el hook Git versionado con:

```powershell
.\scripts\configure_git_hooks.ps1
```

Cuando se modifique el tooling Node de automatización también debe revisarse:

```powershell
npm audit --prefix scripts --audit-level=high
```

GitHub Actions complementa el gate local con compatibilidad de Python,
seguridad de dependencias, política de Pull Requests, verificaciones de
repositorio y controles visuales/de accesibilidad cuando corresponda.

## Documentación

El índice canónico y el mapa de autoridades se encuentran en
[Documentación de Mi Retiro Proyectado](docs/README.md).

Puntos de entrada principales:

| Necesidad | Documento |
| --- | --- |
| Comportamiento funcional | [Especificación funcional](docs/product/functional-specification.md) |
| Cómo se calcula | [Guía de cálculo](docs/product/calculation-guide.md) |
| Arquitectura | [Arquitectura del sistema](docs/architecture/system-architecture.md) |
| Modelo de datos | [Modelo de datos](docs/architecture/data-model.md) |
| Normativa | [Marco normativo](docs/regulatory/regulatory-framework.md) |
| Fuentes oficiales | [Fuentes regulatorias](docs/regulatory/regulatory-sources.md) |
| Seguridad y privacidad | [Seguridad y privacidad](docs/security/security-and-privacy.md) |
| Desarrollo local | [Guía de desarrollo](docs/operations/development-guide.md) |
| Validación | [Validación](docs/operations/validation.md) |
| Releases | [Proceso de release](docs/operations/release-process.md) |
| Gobierno | [Gobierno del proyecto](GOVERNANCE.md) |
| Versionado | [Política de versionado](VERSIONING.md) |
| Roadmap | [Roadmap](docs/governance/roadmap.md) |
| Estándares | [Estándares del repositorio](docs/standards/README.md) |

La documentación viva describe contratos vigentes. La evidencia cerrada se
mantiene en auditorías, registros explícitamente acumulativos, Git y, cuando
conserva valor independiente, en `docs/archive/`.

## Privacidad y seguridad

La simulación previsional se diseña para procesamiento local y no requiere una
base permanente de simulaciones de usuarios. El Portal Developer mantiene su
estado administrativo local separado de los datos previsionales.

No deben versionarse documentos personales, credenciales, cookies, tokens,
salarios reales, historiales identificables ni otros datos sensibles. Los casos
de validación versionados deben ser sintéticos o estar anonimizados de forma
irreversible para su finalidad de prueba.

Referencias:

- [Política de privacidad](docs/security/privacy-policy.md);
- [Términos de uso y privacidad](docs/security/terms-and-privacy.md);
- [Seguridad y privacidad](docs/security/security-and-privacy.md);
- [Modelo de amenazas](docs/security/threat-model.md);
- [Política de seguridad y reporte de vulnerabilidades](SECURITY.md).

## Contribución y soporte

Antes de proponer cambios consulta:

- [Guía de contribución](CONTRIBUTING.md);
- [Gobierno del proyecto](GOVERNANCE.md);
- [Estándares del repositorio](docs/standards/README.md);
- [Soporte](SUPPORT.md);
- [Código de conducta](CODE_OF_CONDUCT.md).

## Licencia

Los materiales originales de Mi Retiro Proyectado se distribuyen bajo una
**licencia propietaria / todos los derechos reservados**. La disponibilidad
pública del código fuente no concede por sí sola permiso para copiar,
modificar, redistribuir, sublicenciar, explotar comercialmente o crear obras
derivadas.

Consulta [`LICENSE`](LICENSE),
[Licencia y estrategia de distribución](docs/governance/licensing-and-distribution.md)
y [Avisos de terceros](THIRD_PARTY_NOTICES.md).

## Responsable

**Rubén Enrique Cañizares Miranda — Panamá**

Mi Retiro Proyectado mantiene una identidad independiente de la Caja de Seguro
Social de Panamá.
