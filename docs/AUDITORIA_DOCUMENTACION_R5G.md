# Auditoría MANT.1 R5G — documentación vigente

## Propósito

Esta auditoría documenta la revisión **MANT.1 R5G**, enfocada en coherencia documental, referencias internas, cobertura del índice y preparación del cierre de mantenimiento antes de **SEC.2**.

## Alcance aplicado

La revisión se limita a documentación vigente, índices, referencias internas y evidencia de validación. No modifica lógica funcional, cálculo de pensión, valores normativos, `VERSION`, `APP_VERSION`, `SEC.2` ni `_entregas/`.

## Resultado de auditoría

La revisión temporal no detectó enlaces Markdown rotos en la documentación vigente revisada.

También identificó coincidencias con expresiones de dominio que no representan rutas obsoletas. Por ejemplo, expresiones como normativa/privacidad, normativa/código o revisión normativa/jurídica se conservan porque describen áreas de revisión y no carpetas del repositorio.

## Excepciones históricas

Las auditorías **R5E** y **R5F** conservan nombres anteriores como evidencia del cambio realizado. Esos documentos no deben interpretarse como referencias vigentes a rutas activas.

## Correcciones aplicadas

Se actualizó `docs/INDICE.md` para incluir documentos raíz que existían en `docs/` pero no estaban listados en el índice documental.

## Validación esperada

La revisión debe pasar como mínimo:

- `python -m pytest tests\test_mant1_r5g_documentacion.py -q`
- `python -m pytest tests\test_ver2_documentacion_vigente.py -q`
- `python -m pytest tests\test_ux46e_estandar_runtime.py -q`
- `python -m pytest -q`
- `python -m unittest discover -s tests -q`

## Relación con SEC.2

R5G deja la documentación base más navegable antes de la fase de seguridad. El cierre transversal de MANT.1 debe consolidarse en una revisión posterior antes de iniciar **SEC.2**.
