# DEV.2 R1 — Centro de desarrollo

**Estado:** R1 integrado en `main` mediante PR #37.

DEV.2 R1 abre una superficie interna y local para revisar el estado técnico de
Developer Diagnostics sin alterar los cálculos previsionales, sin leer datos de
simulación y sin exponer información personal o financiera.

## Objetivo

Crear una página de Centro de desarrollo que permita confirmar, durante el
desarrollo local, si Developer Diagnostics está activo, qué esquema JSONL se usa,
cuál es el archivo diagnóstico esperado y si existe material suficiente para una
exportación ZIP sanitizada.

## Activación

Developer Diagnostics sigue desactivado por defecto. La activación local requiere:

```powershell
$env:MRP_DEV_MODE = "1"
```

Equivalente conceptual: `MRP_DEV_MODE=1`.

El directorio diagnóstico puede mantenerse por defecto bajo `logs/diagnostico/` o
configurarse con `MRP_DIAGNOSTIC_DIR` durante pruebas locales.

## Alcance de R1

Incluye:

- ruta interna `/dev/centro-desarrollo`;
- estado de `MRP_DEV_MODE`;
- versión de esquema de Developer Diagnostics;
- resumen no sensible del log vigente y sus rotaciones conocidas;
- indicación de disponibilidad de exportación ZIP sanitizada;
- advertencias explícitas de privacidad.

No incluye:

- lectura de cuerpos HTTP;
- lectura de PDFs, uploads, bases de datos o `sessionStorage`;
- nombres, cédulas, NSS, salarios, cuotas o montos de pensión;
- rutas absolutas locales del equipo;
- telemetría remota;
- cambios en los motores de cálculo;
- no cambia cálculos previsionales ni resultados;
- no cambia VERSION al abrir el bloque.

## Versionado

DEV.2 R1 **no cambia VERSION** ni `APP_VERSION`. La versión visible permanece en
`0.0.26-beta` después del cierre parcial de R1.

El cierre documental de R1 no crea tag ni promueve una versión revision-aware.
La promoción a una versión `0.GG.RR.EE-beta` queda reservada para un cierre
aceptado que explícitamente lo requiera conforme a la política vigente.

## Relación con GOV.1.4

GOV.1.4 ya implementó el núcleo de observabilidad y Developer Diagnostics. DEV.2
R1 no reescribe esa capa: solamente agrega una interfaz interna y pruebas de
seguridad sobre la capacidad existente.

## Nota de cierre DEV.2 R1

DEV.2 R1 fue integrado mediante PR #37 sobre `main` con el commit de squash
`06e2821`. El cierre abre la ruta interna `/dev/centro-desarrollo`, mantiene
`VERSION` y `APP_VERSION` en `0.0.26-beta`, no crea tag, no cambia motores
previsionales y deja como siguiente trabajo DEV.2 R2.

La validación local de cierre quedó en:

```text
python -m pytest tests\test_dev2_centro_desarrollo.py -q
4 passed

python -m pytest -q
868 passed, 695 subtests passed
```
