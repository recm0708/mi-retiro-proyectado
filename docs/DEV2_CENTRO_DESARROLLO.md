# DEV.2 R1 — Centro de desarrollo

**Estado:** En desarrollo.

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

DEV.2 R1 **no cambia VERSION** ni `APP_VERSION` al abrir el bloque. La versión
visible permanece en `0.0.26-beta` hasta que exista un cierre aceptado y se decida
la promoción conforme a la política revision-aware de VER.2.

Si el cierre de DEV.2 R1 queda aceptado, el candidato esperado bajo la nueva
política sería `G072 / E01 → 0.0.72.01-beta`, sin crear tags retroactivos.

## Relación con GOV.1.4

GOV.1.4 ya implementó el núcleo de observabilidad y Developer Diagnostics. DEV.2
R1 no reescribe esa capa: solamente agrega una interfaz interna y pruebas de
seguridad sobre la capacidad existente.
