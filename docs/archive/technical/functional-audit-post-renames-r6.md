# MANT.1 R6 — Auditoría funcional post-renombres

## Objetivo

Esta auditoría valida que los renombres técnicos aplicados en MANT.1 R5 no dejaron referencias funcionales rotas en la aplicación.

El alcance se limita a rutas, plantillas, archivos estáticos, contratos frontend/backend, formularios, cargas de archivo y estructura HTML renderizada. No modifica fórmulas, parámetros normativos, versiones oficiales ni entregables.

## Alcance revisado

Se revisaron los siguientes frentes:

1. Plantillas Jinja2, parciales y referencias a archivos estáticos.
2. Rutas FastAPI utilizadas desde JavaScript y HTML.
3. Enlaces internos, anchors y enlaces dinámicos controlados.
4. Páginas principales renderizadas con `TestClient`.
5. Estructura HTML: `id`, `label for`, `aria-labelledby`, `aria-describedby`, `aria-controls`, `data-bs-target` y anclas internas.
6. Métodos HTTP usados por `fetch`.
7. Contratos JSON entre JavaScript y modelos Pydantic.
8. Contratos `multipart/form-data` entre `FormData` del frontend y `UploadFile = File(...)` del backend.

## Resultado

La auditoría no encontró rupturas funcionales reales posteriores a los renombres.

Los falsos positivos detectados fueron revisados y clasificados como controlados:

- Rutas antiguas `app/static/img/icons` y `app/static/img/.gitkeep`: no se usan en runtime; las pruebas verifican que ya no existan.
- `/como-se-calcula#${ancla}`: ruta dinámica válida; las anclas `sebd`, `mixto` y `sucgs` existen en la plantilla.
- `{{ url_for(...) }}`: referencias dinámicas de Jinja2 cubiertas por smoke test de assets renderizados.
- `{{ fuente.url }}`, `{{ recurso.url }}` y `{{ mi_caja_digital_url }}`: enlaces externos controlados con `target="_blank"` y `rel="noopener noreferrer"`.
- Endpoints de importación PDF: usan `FormData` y coinciden con `UploadFile = File(...)` en backend.
- Payloads `datos` y `solicitud`: se construyen mediante funciones previas antes de `JSON.stringify(...)`, no como objetos literales inmediatos.

## Validaciones ejecutadas

Se ejecutaron correctamente:

- `python -m compileall app tests`
- `python -m pytest`
- `python -m unittest discover -s tests`
- `git diff --check`

Resultado de pruebas:

- `pytest`: 928 passed.
- `unittest`: 928 tests OK.

## Archivos protegidos

Durante esta auditoría no se modificaron:

- `VERSION`
- `app/core/version.py`
- `app/core/config.py`
- `regulations/`
- `data/`
- `_entregas/`

## Conclusión

MANT.1 R6 confirma que la aplicación mantiene coherencia funcional después de los renombres técnicos de MANT.1 R5. Las rutas, plantillas, assets, contratos de API, formularios y estructura HTML renderizada permanecen alineados.
