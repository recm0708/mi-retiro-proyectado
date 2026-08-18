# Dependencias y terceros

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.23-beta`
**Base documental:** GOV.1.3 R4 — 2026-08-17
**Revisión transversal:** GOV.1.5 R3 — 2026-08-18
**Clasificación:** Técnica / Terceros / Auditoría

Este inventario distingue dependencias directas, snapshot transitivo, recursos externos y servicios de red. La selección de licencia del proyecto continúa pendiente hasta GOV.1.7.

## 1. Dependencias Python directas

Las versiones corresponden al `requirements.txt` vigente. La estructura documental se originó en GOV.1.3 R4 y se mantiene actualizada durante el mantenimiento pre-beta.

| Dependencia | Versión | Finalidad en el proyecto | Licencia upstream verificada | Conexión/datos en el uso actual | Riesgo/revisión |
|---|---:|---|---|---|---|
| FastAPI | 0.141.1 | API local, rutas y middleware | MIT | Atiende solicitudes de la aplicación; no añade por sí sola un envío externo | Revisar cambios de framework/Starlette |
| Jinja2 | 3.1.6 | Plantillas HTML | BSD-3-Clause | Render local del servidor | Revisar autoescape/plantillas |
| Pydantic | 2.13.4 | Validación/modelos | MIT | Validación local de estructuras | Revisar cambios de esquema/core |
| python-multipart | 0.0.32 | Recepción multipart de archivos | Apache-2.0 | Procesa cargas recibidas por FastAPI | Sensible a frontera de upload |
| pypdf | 6.15.0 | Extracción y lectura controlada de PDF | BSD-3-Clause | Procesa PDF en memoria; sin red propia | Dependencia crítica de parser; actualización mayor validada con regresiones específicas |
| Uvicorn | 0.52.1 | Servidor ASGI | BSD-3-Clause | Sirve la aplicación; la red depende del modo de ejecución | Revisar configuración de despliegue |

Fuentes upstream de licencia verificadas documentalmente:

- FastAPI: PyPI/repositorio oficial;
- Jinja2: repositorio Pallets;
- Pydantic: PyPI/repositorio oficial;
- python-multipart: PyPI;
- pypdf: PyPI/repositorio oficial, licencia BSD-3-Clause;
- Uvicorn: PyPI.

La revisión definitiva de obligaciones de redistribución corresponde a GOV.1.7.

## 2. Snapshot transitivo

`requirements.txt` fija también dependencias transitivas para reproducibilidad.

R4 **no declara completado un inventario jurídico licencia-por-licencia de todas las transitivas**. Ese análisis es un requisito previo a elegir la licencia/distribución en GOV.1.7.

Dependabot propone actualizaciones directas permitidas; no existe auto-merge.

## 3. Bootstrap

La interfaz usa **Bootstrap 5.3.8**.

- licencia upstream: MIT;
- origen actual: `https://cdn.jsdelivr.net/`;
- carga con Subresource Integrity;
- el navegador realiza una solicitud al CDN;
- la solicitud de recurso no incluye intencionalmente el contenido de la simulación.

Servir Bootstrap localmente continúa como objetivo pre-beta para reducir dependencia de terceros.

## 4. Servicio oficial CSS para fecha

`app/servicios/fecha_referencia.py` puede consultar infraestructura oficial de la CSS mediante HTTPS para obtener el encabezado `Date`.

No se envía:

- PDF;
- cédula/NSS;
- salario;
- cuotas;
- resultado previsional.

No es una dependencia de software; se registra como **servicio externo operativo** porque afecta disponibilidad y exposición de metadata ordinaria de red.

## 5. GitHub

GitHub aloja el repositorio privado y ejecuta CI/Dependabot.

GitHub Actions utiliza actualmente:

- `actions/checkout@v7`;
- `actions/setup-python@v7`;
- `actions/setup-node@v7`.

Estas herramientas son de desarrollo/CI, no runtime del usuario final.

## 6. Node.js

Node 24 se usa en CI para `node --check`.

No forma parte del runtime Python de la aplicación.

## 6.1. Evaluación GOV.1.5 de terceros

La revisión de seguridad/privacidad clasifica:

- **jsDelivr:** tercero runtime temporal, con SRI, CSP y versión fija; riesgo residual aceptado para desarrollo local;
- **infraestructura CSS:** servicio externo operativo mínimo, sin envío de datos previsionales;
- **GitHub:** tercero de desarrollo/CI, fuera del flujo de simulación del usuario final.

La evaluación completa y los gates de despliegue se documentan en `EVALUACION_TERCEROS_DESPLIEGUE.md`.

Servir Bootstrap localmente sigue siendo la opción preferida antes de una publicación amplia o deberá existir una excepción explícita y revisada en el gate pre-beta.

## 7. Política de actualización

Antes de aceptar una actualización:

1. revisar release/changelog upstream;
2. ejecutar instalación reproducible y `pip check`;
3. ejecutar compilación;
4. ejecutar sintaxis JS cuando corresponda;
5. ejecutar suite completa;
6. revisar importadores si cambia `pypdf`/multipart;
7. actualizar este documento si cambia versión, licencia, función, riesgo o conexión.

Para `pypdf 6.15.0` se añadieron regresiones específicas sobre:

- versión instalada;
- roundtrip `PdfWriter` → `PdfReader`;
- rechazo controlado de PDFs digitales sin texto por ambos importadores;
- límites de páginas de Mi Retiro Seguro y Ficha Digital.

## 8. Licencia del proyecto

La existencia de dependencias permisivas no decide automáticamente la licencia de Mi Retiro Proyectado.

GOV.1.7 debe considerar:

- objetivos de distribución;
- obligaciones de avisos;
- dependencias transitivas;
- recursos de terceros;
- marcas;
- contenido normativo/documental.

No se crea un `LICENSE` vacío o provisional en R4.
