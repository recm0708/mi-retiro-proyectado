# Third-party notices

**Proyecto:** Mi Retiro Proyectado
**Estado:** GOV.1.7 — vigente para el repositorio fuente pre-beta
**Fecha:** 2026-08-18

La licencia propietaria de Mi Retiro Proyectado **no relicencia** componentes de terceros.

## Dependencias directas Python

| Componente | Versión | Licencia upstream documentada |
|---|---:|---|
| FastAPI | 0.141.1 | MIT |
| Jinja2 | 3.1.6 | BSD-3-Clause |
| Pydantic | 2.13.4 | MIT |
| python-multipart | 0.0.32 | Apache-2.0 |
| pypdf | 6.15.0 | BSD-3-Clause |
| Uvicorn | 0.52.1 | BSD-3-Clause |

## Recurso frontend

| Componente | Versión | Licencia upstream documentada |
|---|---:|---|
| Bootstrap | 5.3.8 | MIT |

## Dependencias transitivas y artefactos

`requirements.txt` conserva un snapshot transitivo para reproducibilidad. Este archivo no sustituye licencias upstream ni pretende alterar sus términos.

Si una distribución futura incorpora físicamente dependencias, código minificado, wheels, binarios, contenedores u otros componentes, el proceso de release debe inventariar el artefacto real, conservar avisos de copyright y adjuntar licencias/NOTICE exigidos.

## GitHub Actions

Los workflows usan actualmente `actions/checkout@v7`, `actions/setup-python@v7` y `actions/setup-node@v7`. Conservan sus licencias upstream y forman parte de la cadena de desarrollo/CI.

## Servicios externos

jsDelivr, GitHub y la infraestructura CSS documentada en `docs/EVALUACION_TERCEROS_DESPLIEGUE.md` son terceros operativos. Este archivo no concede derechos sobre sus marcas, servicios o contenidos.

## Regla de distribución

La decisión propietaria sobre materiales originales no elimina obligaciones de terceros. GOV.1.8 debe comprobar el inventario real de cualquier artefacto candidato a beta pública.
