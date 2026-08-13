# Seguridad y privacidad

Este documento resume las defensas técnicas aplicables a la primera beta de **Mi Retiro Proyectado**. No sustituye una auditoría de seguridad externa ni convierte la aplicación en un servicio remoto multiusuario.

## 1. Modelo de ejecución

La primera beta está diseñada para ejecutarse localmente. Los datos del asistente permanecen en el navegador mediante `sessionStorage` y los cálculos se realizan contra la API local de FastAPI.

No existe persistencia de simulaciones en base de datos en esta versión.

## 2. Documentos personales importados

Los comprobantes de Mi Retiro Seguro y la Ficha Digital:

- se leen en memoria;
- no se guardan en el sistema de archivos por los endpoints de importación;
- no se incorporan al repositorio;
- no deben aparecer en fixtures de pruebas reales;
- se reducen a los campos operativos necesarios antes de devolver información al frontend.

Los contratos del importador excluyen identificadores directos que no sean necesarios para la simulación.

## 3. Validación defensiva de PDF

Antes de invocar `pypdf`, la capa HTTP valida:

- extensión `.pdf`;
- tipo MIME compatible (`application/pdf`, genérico binario o ausente cuando el navegador no informa uno específico);
- archivo no vacío;
- límite de tamaño por importador;
- cabecera `%PDF-` dentro del primer KiB.

Los parsers mantienen además límites de páginas y de texto extraído. Los errores de parsing se convierten en mensajes controlados y no exponen trazas internas al Asegurado(a).

## 4. Cabeceras del navegador

Las respuestas incorporan defensas de bajo riesgo compatibles con la aplicación local:

- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options: DENY`;
- `Referrer-Policy: no-referrer`;
- `Permissions-Policy` sin cámara, micrófono ni geolocalización.

Las respuestas de los dos importadores PDF usan `Cache-Control: no-store`.

No se incorpora todavía una política CSP estricta porque la interfaz actual debe revisarse previamente para eliminar o inventariar dependencias y fragmentos inline sin romper el producto.

## 5. CI y dependencias

`.github/workflows/ci.yml` ejecuta en cada `push` y `pull_request` sobre `main`:

- instalación limpia de dependencias;
- `pip check`;
- `compileall`;
- `node --check` para todos los JavaScript;
- suite completa de `unittest`.

La matriz cubre Python 3.13 y 3.14. Node.js se usa únicamente como herramienta de validación estática del frontend.

`.github/dependabot.yml` solicita revisiones semanales, pero evita actualizar transitivas fijadas de forma aislada. Para `pip` se permiten propuestas ordinarias únicamente sobre `fastapi`, `Jinja2`, `pydantic`, `python-multipart`, `pypdf` y `uvicorn`; las minor/patch compatibles del runtime se agrupan y `pypdf` queda separado para revisión específica. Las GitHub Actions se agrupan en una sola propuesta. La aceptación de cualquier actualización continúa requiriendo CI verde y revisión explícita; no existe auto-merge.

## 6. Datos sensibles y registros

No deben añadirse a logs, documentación pública, commits ni fixtures:

- nombre completo del Asegurado(a);
- cédula;
- número de seguro social;
- PDFs personales originales;
- capturas de Mi Caja Digital con identificadores;
- códigos únicos o QR personales.

Los casos reales de validación deben anonimizarse o transformarse en fixtures sintéticos antes de versionarse.

## 7. Límites de esta beta

Esta fase no afirma resistencia contra cargas hostiles a nivel de un servicio expuesto a Internet. Antes de desplegar la aplicación como servicio público remoto harían falta controles adicionales de infraestructura, límites de concurrencia, observabilidad, política CSP completa, revisión de dependencias y una evaluación de amenazas acorde al entorno de despliegue.
