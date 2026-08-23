# DEV.2 R1/R2 — Centro de desarrollo

**Estado:** R1 integrado en `main` mediante PR #37.

**Estado R2:** en desarrollo sobre la rama `dev/dev2-r2-visor-diagnostico`.

DEV.2 abre una superficie interna y local para revisar el estado técnico de
Developer Diagnostics sin alterar los cálculos previsionales, sin leer datos de
simulación y sin exponer información personal o financiera.

## Objetivo

Crear una página de Centro de desarrollo que permita confirmar, durante el
desarrollo local, si Developer Diagnostics está activo, qué esquema JSONL se usa,
cuál es el archivo diagnóstico esperado, qué eventos recientes son visibles de
forma segura y si existe material suficiente para una exportación ZIP sanitizada.

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

## Alcance de R2

DEV.2 R2 añade un visor diagnóstico seguro y un servicio interno de exportación
ZIP controlada sobre los archivos JSONL ya conocidos por Developer Diagnostics.

Incluye:

- lectura acotada del archivo `mrp-diagnostics.jsonl` y sus rotaciones esperadas;
- normalización de eventos recientes para la interfaz local;
- conteo visible de eventos por nivel operacional;
- exposición de `correlation_id` solo cuando existe y sin derivarlo de datos del usuario;
- metadata limitada a operación, método HTTP, código de estado y tipo de excepción;
- conteo de líneas JSONL inválidas sin mostrar su contenido;
- servicio `exportar_zip_diagnostico_sanitizado()` para generar el ZIP permitido;
- regresiones específicas para visor, privacidad y exportación.

No incluye todavía:

- autenticación administrativa fuerte;
- sesiones administrativas;
- panel de filtros interactivos avanzados;
- descarga HTTP directa desde la interfaz;
- autodiagnóstico completo de componentes;
- cambios de CSP, CORS, CSRF, secretos o cifrado.

Esos puntos quedan reservados para revisiones posteriores de DEV.2 o para SEC.2,
según corresponda.

## Versionado

DEV.2 R1/R2 **no cambia VERSION** ni `APP_VERSION`. La versión visible permanece
en `0.0.26-beta` durante este tramo.

El cierre documental de R1 no creó tag ni promovió una versión revision-aware. La
promoción a una versión `0.GG.RR.EE-beta` queda reservada para el cierre posterior
de VER.2, cuando el ledger y la documentación de versionado se alineen de forma
sincrónica.

## Relación con GOV.1.4

GOV.1.4 ya implementó el núcleo de observabilidad y Developer Diagnostics. DEV.2
no reescribe esa capa: agrega una interfaz interna, visor seguro y pruebas de
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

## Validación esperada de DEV.2 R2

```text
python -m pytest tests\test_dev2_r2_visor_diagnostico.py -q
4 passed

python -m pytest -q
874 passed, 695 subtests passed
```
