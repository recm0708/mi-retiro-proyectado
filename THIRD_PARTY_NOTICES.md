# Avisos de terceros

**Proyecto:** Mi Retiro Proyectado
**Estado:** Vigente para el repositorio fuente y la beta actual
**Fecha:** 2026-08-18
**Última actualización del inventario:** 2026-08-31
**Versión de aplicación revisada:** `0.1.19.05-beta`
**Última revisión documental:** mantenimiento post-G119 — 2026-08-31

La licencia propietaria de Mi Retiro Proyectado **no relicencia** componentes de terceros.

## Dependencias directas Python

| Componente | Versión | Licencia upstream documentada |
| --- | ---: | --- |
| FastAPI | 0.141.1 | MIT |
| Jinja2 | 3.1.6 | BSD-3-Clause |
| Pydantic | 2.13.5 | MIT |
| python-multipart | 0.0.32 | Apache-2.0 |
| pypdf | 6.16.2 | BSD-3-Clause |
| Uvicorn | 0.52.4 | BSD-3-Clause |

## Recurso frontend

| Componente | Versión | Licencia upstream documentada |
| --- | ---: | --- |
| Bootstrap | 5.3.8 | MIT |

## Dependencias transitivas y artefactos

`requirements.txt` conserva un snapshot transitivo para reproducibilidad. Este archivo no sustituye licencias upstream ni pretende alterar sus términos.

Si una distribución futura incorpora físicamente dependencias, código minificado, wheels, binarios, contenedores u otros componentes, el proceso de release debe inventariar el artefacto real, conservar avisos de copyright y adjuntar licencias/NOTICE exigidos.

## Schemas locales de tooling

Para que Visual Studio Code pueda validar `.markdownlint-cli2.jsonc` sin depender de una descarga de red, el repositorio conserva bajo `.vscode/schemas/` copias fijadas de:

- `markdownlint-cli2` configuration schema `0.23.2`;
- `markdownlint` configuration schema `0.41.1`.

Ambos proyectos declaran licencia MIT. Las copias de sus licencias se conservan junto a los schemas y `SOURCES.txt` registra URL y SHA-256 del material upstream descargado. Estos archivos son tooling de desarrollo y no forman parte del runtime de Mi Retiro Proyectado.

## GitHub Actions

Los workflows usan actualmente, entre otras referencias versionadas, `actions/checkout@v7`, `actions/setup-python@v7`, `actions/setup-node@v7`, `actions/upload-artifact@v7`, `actions/dependency-review-action@v5` y `actions/labeler@v7`. Conservan sus licencias upstream y forman parte de la cadena de desarrollo/CI.

## Servicios externos

Shields.io se utiliza únicamente para badges estáticos del README (versión, Python y licencia); no forma parte del runtime ni recibe intencionalmente datos de la simulación.

jsDelivr, GitHub y la infraestructura CSS documentada en `docs/security/third-party-deployment-assessment.md` son terceros operativos. Este archivo no concede derechos sobre sus marcas, servicios o contenidos.

## Copias preservadas de fuentes oficiales

El repositorio conserva copias de determinadas publicaciones de la Caja de Seguro Social de Panamá, Gaceta Oficial de la República de Panamá y Autoridad Nacional de Transparencia y Acceso a la Información bajo `docs/regulatory/sources/official/`.

Esos PDF y XLSX son materiales oficiales de terceros. Su incorporación tiene fines de preservación, trazabilidad, revisión y consulta offline; **no son relicenciados** por la licencia propietaria de Mi Retiro Proyectado. `docs/regulatory/sources/official/manifest.json` conserva emisor, URL oficial, página de procedencia, nombre original, tamaño y SHA-256.

La URL oficial de origen continúa siendo la referencia canónica para comprobar vigencia y autenticidad.

## Regla de distribución

La decisión propietaria sobre materiales originales no elimina obligaciones de terceros. Antes de cualquier nueva release, publicación o distribución, el proceso de release debe comprobar el inventario real del artefacto y las obligaciones upstream aplicables.
