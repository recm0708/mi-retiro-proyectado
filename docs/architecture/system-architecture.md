# Arquitectura

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.17.02-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental:** GOV.1.4 — 2026-08-17
**Última actualización técnica:** AUD.SEC2 R1 — sesión administrativa y kill switch — 2026-08-25
**Última actualización de mantenimiento:** MANT.1 R5E — estandarización de nombres de carpetas — 2026-08-23
**Clasificación:** Técnica / Pública


<!-- DOC1-R1-POST-MANT1:START -->
## Estado arquitectónico post-MANT.1

La arquitectura vigente conserva el mismo alcance funcional y normativo. MANT.1 no cambió fórmulas, motores previsionales, rutas públicas, selectores funcionales, parámetros de `regulations/`, datos ni entregables.

Cierre técnico relevante:

- R5E consolidó nombres de carpetas técnicas.
- R5F consolidó nombres de archivos técnicos.
- R5G reforzó la documentación base.
- R5H auditó nombres técnicos restantes.
- R6 validó funcionalmente el repositorio después de los renombres.
- R7 cerró operativamente MANT.1 sobre `main`.

La documentación arquitectónica debe leerse desde esta base: MANT.1, DOC.1, NOR.1 y NOR.2 están cerrados; SEC.2 cerró R1–R6. AUD.SEC2 R1 corrige la prioridad del kill switch administrativo, el fallback de sesión y logout sin modificar la arquitectura previsional.
<!-- DOC1-R1-POST-MANT1:END -->

Mi Retiro Proyectado es una aplicación web local basada en FastAPI, Jinja2 y JavaScript del navegador. La arquitectura separa presentación, contratos de datos, servicios de integración, motores previsionales, parámetros normativos y observabilidad de desarrollo.

MANT.1 R1 dejó la auditoría inicial de mantenibilidad, MANT.1 R2 documenta
la infraestructura local de scripts/hooks que protege commits reproducibles antes
de los checks remotos y MANT.1 R3 documenta los YAML de GitHub sin cambiar CI,
Issue Forms ni Dependabot. MANT.1 R4 limpia encabezados operativos para separar
comentarios permanentes de trazabilidad histórica. MANT.1 R5A inicia la revisión
de comentarios internos en servicios Python de aplicación, MANT.1 R5B cubre CSS
y plantilla de la guía pública, MANT.1 R5C documenta JavaScript complejo sin
alterar lógica, storage, selectores ni contratos de datos, MANT.1 R5D formaliza política/plantillas por extensión con uniformidad de encabezados JS/CSS y MANT.1 R5E estandariza nombres de carpetas técnicas en inglés sin cambiar contratos funcionales. Este mantenimiento no
introduce nuevas capas de producto.

[Índice](../README.md) · [Modelo de datos](data-model.md) · [Motor](calculation-engine.md) · [Normativa](../regulatory/regulatory-framework.md) · [Observabilidad](../operations/observability-and-logs.md) · [Política de estructura](../standards/file-structure-by-extension.md) · [Auditoría de carpetas](../archive/technical/AUDITORIA_CARPETAS_R5E.md)

## 1. Principios

1. **Fuente única del cálculo:** las fórmulas previsionales principales viven en Python.
2. **Normativa separada:** parámetros legales modificables se mantienen en `regulations/`.
3. **Histórico y proyección separados:** una estimación futura no sustituye silenciosamente información acreditada.
4. **Datos faltantes explícitos:** un parámetro que no puede determinarse no se inventa.
5. **Trazabilidad:** motores y servicios exponen advertencias, fuentes y resultados intermedios cuando corresponde.
6. **Procesamiento local por defecto:** el estado de simulación se conserva en el navegador y no existe persistencia permanente automática.
7. **Importación revisable:** extraer un PDF no equivale a confirmar ni calcular.
8. **Versión única:** `VERSION` es la fuente canónica consumida por `app/core/version.py`.
9. **Interfaz desacoplada:** JavaScript administra experiencia, estado temporal y comunicación HTTP; no constituye una segunda implementación de los motores.
10. **Observabilidad lateral:** Developer Diagnostics observa operaciones ya ejecutadas; no vuelve a invocar motores ni replica fórmulas.
11. **Minimización de logs:** los eventos técnicos no contienen cuerpos HTTP, documentos, identificadores ni valores financieros.
12. **Historia preservada:** la documentación vigente describe el contrato actual; bitácoras anteriores se conservan en `docs/archive/`.

## 2. Inventario relevante del paquete `app`

### Núcleo

- `app/core/pdf_files.py`
- `app/core/config.py`
- [`app/core/constants.py`](../../app/core/constants.py)
- `app/core/money.py`
- `app/core/normativa.py`
- `app/core/observability.py`
- `app/core/version.py`

### Modelos

- [`app/models/comparacion.py`](../../app/models/comparacion.py)
- [`app/models/pension.py`](../../app/models/pension.py)
- `app/models/unified_result.py`
- `app/models/simulation.py`
- `app/models/traceability.py`

### Motores

- [`app/engines/elegibilidad.py`](../../app/engines/elegibilidad.py)
- `app/engines/mixto.py`
- `app/engines/sebd.py`
- [`app/engines/sebd_modalidades.py`](../../app/engines/sebd_modalidades.py)
- `app/engines/sucgs.py`

### Servicios principales

- `app/services/comparator.py` — construye matrices retiro × salario sin recalcular fórmulas fuera de los servicios integrados
- `app/services/calculation_guide.py` — estructura parámetros normativos para la guía pública sin ejecutar motores
- `app/services/current_year_detail.py` — normaliza salarios mensuales/quincenales y separa salario visible de cuota acreditada
- `app/services/reference_date.py`
- `app/services/ficha_digital.py` — extrae salarios recientes desde PDF en memoria con límites de seguridad y minimización
- `app/services/regulatory_sources.py` — arma catálogo metodológico de fuentes oficiales desde parámetros versionados
- `app/services/salary_history.py`
- `app/services/timeline.py`
- `app/services/contribution_projection.py`
- `app/services/salary_projection.py`
- `app/services/mi_retiro_seguro_reference.py`
- `app/services/unified_result.py`
- `app/services/results.py`
- `app/services/mixto_results.py`
- `app/services/sebd_results.py`
- `app/services/sucgs_results.py`
- `app/services/retirement.py`
- `app/services/traceability.py` — transforma resultados ya calculados en pasos explicables y fuentes auditables

### Presentación CSS y plantillas documentadas

- `app/static/css/calculation-guide.css` — delimita responsabilidades visuales de la guía pública: hero, navegación, fórmulas, tablas, fuentes, accesibilidad y responsive.
- `app/templates/calculation_guide.html` — organiza comentarios Jinja por recorrido general, sistemas previsionales, fuentes y cierre sin modificar el HTML renderizado.

### Presentación JavaScript crítica

- `app/static/js/accessibility.js`
- `app/static/js/comparator.js` — matriz retiro × salario, advertencias y diferencias sin recalcular pensiones.
- `app/static/js/current_year_detail.js`
- `app/static/js/data_management.js` — limpieza controlada de pasos, invalidación descendente y borrado limitado a claves propias.
- `app/static/js/salary_history.js`
- `app/static/js/official_data_import.js` — borradores revisables de Mi Retiro Seguro/Ficha Digital, vigencia y confirmación explícita.
- `app/static/js/timeline.js`
- `app/static/js/currency.js`
- `app/static/js/wizard_navigation.js`
- `app/static/js/privacy.js` — consentimiento versionado, sesión autorizada y borrado defensivo de datos propios.
- `app/static/js/attachment_processing.js` — estado global accesible y exclusión de dobles ejecuciones durante análisis de archivos.
- `app/static/js/mi_retiro_seguro_reference.js`
- `app/static/js/results.js` — contratos de cálculo, comparación acreditado/proyectado, trazabilidad y salida por sistema.
- `app/static/js/results_orchestration.js` — decisiones de Paso 6, transición Mixto/SUCGS, enlace contextual e impresión sin duplicar fórmulas.
- `app/static/js/retirement.js`
- `app/static/js/simulation.js` — estado temporal, navegación de pasos, validación progresiva y dependencias entre módulos.
- `app/static/js/theme.js`

## 3. Capas

### 3.1. Núcleo (`app/core/`)

Responsabilidades:

- identidad/configuración técnica;
- versión canónica;
- precisión monetaria;
- carga de normativa;
- constantes comunes;
- validación defensiva de archivos PDF;
- Developer Diagnostics.

`app/core/observability.py` implementa el esquema JSONL, correlación aleatoria, redacción, rotación, retención y exportación controlada. El módulo no conoce modelos previsionales ni ejecuta cálculos.

### 3.2. Modelos (`app/models/`)

Pydantic define contratos HTTP y de dominio:

- `simulation.py` — cuotas, historial, detalle del año actual, importaciones, salario, proyección, línea temporal y retiro;
- `pension.py` — contratos SEBD, Mixto, SUCGS y resultados integrados;
- `comparacion.py` — comparación transversal;
- `traceability.py` — pasos y fuentes de cálculo;
- `unified_result.py` — salida transversal común.

La metadata puramente visual y diagnóstica no se convierte automáticamente en modelo Pydantic de negocio.

### 3.3. Servicios (`app/services/`)

Los servicios normalizan, integran y coordinan cuotas, historial, detalle actual, proyección, retiro, importaciones, resultados, comparación y fecha externa. `calculation_guide.py` es una capa de presentación: lee parámetros versionados para explicar el procedimiento, pero no importa ni ejecuta motores previsionales.

`reference_date.py` puede emitir eventos agregados de cache/consulta cuando Developer Diagnostics está activo. Esos eventos no incluyen URL, fecha recibida ni datos de simulación.

Los parsers documentales son **capas de entrada**, no motores previsionales.

### 3.4. Motores (`app/engines/`)

Los motores aplican las reglas previsionales ya modeladas:

- elegibilidad común;
- SEBD normal;
- modalidades SEBD;
- Subsistema Mixto;
- SUCGS.

No leen PDFs, `sessionStorage`, controles HTML ni logs. Developer Diagnostics no vuelve a invocarlos.

### 3.5. Presentación (`app/templates/`, `app/static/`)

Jinja2 genera las páginas y parciales. JavaScript administra el asistente, estado temporal, importaciones, procedencia, invalidación, llamadas HTTP y representación de resultados. La ruta pública `/como-se-calcula` usa `calculation_guide.html` y `calculation-guide.css` para explicar el procedimiento general sin convertir la página en una calculadora paralela.

JavaScript no implementa fórmulas previsionales principales ni un segundo sistema de logging de datos de negocio.

## 4. Flujo funcional

```text
Paso 1 — Datos personales
        ↓
Paso 2 — Cuotas
        ↓
Paso 3 — Historial + detalle actual + base salarial
        ↓
Paso 4 — Proyección salarial + línea temporal
        ↓  valida coherencia de cuotas/historial y conserva referencia mensual proyectada
Paso 5 — Escenarios de retiro
        ↓
Paso 6 — Resultado del sistema
        ↓
Comparación + trazabilidad + resumen unificado
```

Developer Diagnostics es transversal a las operaciones HTTP, no forma parte de este flujo de negocio y no altera sus resultados.

La frontera `timeline.py` vuelve a validar la coherencia entre el historial confirmado y las cuotas de Paso 2 antes de materializar el año actual o el futuro. Los modelos separan la referencia mensual proyectada del salario cotizado prorrateado y permiten distinguir años futuros sin cotización prevista. Paso 5 puede solicitar una ampliación del horizonte; esa acción vuelve a Paso 4 con procedencia explícita y resultados anteriores invalidados.

## 5. Estado temporal del navegador

La simulación se conserva en `sessionStorage`. La preferencia visual y la aceptación versionada de privacidad utilizan almacenamiento local según el contrato de interfaz.

La aplicación no intenta restaurar un `File` seleccionado después de recargar. Puede conservar metadata de una importación confirmada —por ejemplo procedencia o nombre visible del archivo—, nunca la ruta local ni el binario.

Consultar [Gestión de datos de la simulación](../product/simulation-data-management.md).

## 6. Importaciones documentales

### Mi Retiro Seguro

`app/services/mi_retiro_seguro_reference.py` extrae una referencia personal revisable. El archivo original no se persiste.

### Ficha Digital

`app/services/ficha_digital.py` devuelve únicamente los registros del año más reciente detectado en la sección salarial del documento.

### Fecha de referencia

`app/services/reference_date.py` intenta obtener el encabezado HTTP `Date` mediante HTTPS desde fuentes CSS configuradas. Si no obtiene una fecha consistente, devuelve un resultado no confiable.

La observabilidad asociada registra solo cantidades, estado de cache, outcome y duración.

## 7. API y middleware

`app/main.py` contiene el middleware global de seguridad y Developer Diagnostics.

Cuando `MRP_DEV_MODE` no vale `1`, la observabilidad no escribe logs ni añade `X-Correlation-ID`.

Cuando está activa:

1. genera un correlation ID aleatorio;
2. ejecuta `call_next()` exactamente una vez;
3. registra operación técnica, método, estado y duración;
4. conserva el mismo correlation ID para eventos internos de esa solicitud;
5. no registra request body ni response body.

Los endpoints bajo `/api/simulacion/` continúan recibiendo `Cache-Control: no-store`.

## 7.1. Inventario de rutas FastAPI

El siguiente inventario se deriva de los decoradores vigentes en `app/main.py`. Se conserva explícitamente para auditoría documental iniciada en GOV.1.3 R2 y actualizada por GOV.1.4.

| Ruta |
|---|
| `/` |
| `/api/simulacion/comparar-escenarios` |
| `/api/simulacion/cuotas` |
| `/api/simulacion/detalle-anio-actual` |
| `/api/simulacion/ficha-digital` |
| `/api/simulacion/historial-salarial` |
| `/api/simulacion/linea-tiempo` |
| `/api/simulacion/mixto` |
| `/api/simulacion/proyeccion-salario` |
| `/api/simulacion/referencia-mi-retiro-seguro` |
| `/api/simulacion/resultados/mixto` |
| `/api/simulacion/resultados/sebd` |
| `/api/simulacion/resultados/sebd-normal` |
| `/api/simulacion/resultados/sucgs` |
| `/api/simulacion/retiro` |
| `/api/simulacion/salario` |
| `/api/simulacion/sebd` |
| `/api/simulacion/sebd/normal` |
| `/api/simulacion/sucgs` |
| `/api/sistema/fecha-referencia` |
| `/comparar` |
| `/dev/login` |
| `/dev/logout` |
| `/como-se-calcula` |
| `/favicon.ico` |
| `/metodologia` |
| `/salud` |
| `/simulacion` |


## 7.2. Automatización local de calidad

La raíz del repositorio contiene automatización local de calidad separada del
runtime de la aplicación:

- `.githooks/pre-commit` actúa como delegador Git antes de cada commit;
- `scripts/configure_git_hooks.ps1` activa los hooks versionados por clon;
- `scripts/validate_precommit.py` ejecuta el gate local reproducible.

Esta capa no participa en el flujo HTTP, no modifica cálculos previsionales, no
lee datos personales de simulación y no reemplaza GitHub Actions. Su objetivo es
impedir commits locales cuando el árbol preparado no corresponde a un estado
validado del repositorio.

## 8. Cabeceras defensivas

El middleware global mantiene:

- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options: DENY`;
- `Referrer-Policy: no-referrer`;
- `Permissions-Policy` restrictiva;
- CSP explícita;
- `Cache-Control: no-store` en servicios de simulación.

`X-Correlation-ID` es una cabecera diagnóstica de desarrollo y solo se añade cuando Developer Diagnostics está activo.

## 9. Persistencia de logs

Los logs se escriben localmente en `logs/diagnostico/` por defecto, directorio excluido de Git.

No existe envío remoto automático. La exportación diagnóstica empaqueta únicamente los JSONL conocidos y requiere activación explícita de desarrollo.

Consultar [Observabilidad y Developer Diagnostics](../operations/observability-and-logs.md).

## 10. Precisión

`app/core/money.py` centraliza operaciones monetarias sensibles con `Decimal` y materialización a centavos. Los factores actuariales no se formatean ni se tratan como importes monetarios.

Los importes no se incluyen en Developer Diagnostics.

## 11. Versionado

`VERSION` → `app/core/version.py` → `APP_VERSION` → FastAPI/Jinja2/footer.

El esquema de logs (`schema_version`) es un contrato técnico independiente de `VERSION`, normativa y privacidad.

## 12. Persistencia futura

La arquitectura actual no incluye una base de datos de simulaciones. La incorporación de almacenamiento permanente exige una decisión explícita, migraciones/versionado de esquema y revisión de privacidad.

Developer Diagnostics no debe utilizarse como sustituto de persistencia de simulaciones.

## 13. Historia de esta arquitectura

La versión acumulativa anterior a GOV.1.3 R2 se conserva en:

`docs/archive/technical/ARQUITECTURA_PRE_GOV1_3_R2.md`

Este documento describe el estado técnico vigente después de GOV.1.4.


## UX.4.6f R1.1 — bloqueo documental en superficies principales

`editable_provenance.js` separa tres conceptos: **fotografía documental original**, **copia de trabajo** y **capacidad de edición de la superficie actual**. En los paneles principales, un control cuyo valor existía en la fotografía original se aplica mediante `readonly` o `disabled` y la clase visual `field-imported-readonly`; los modales de revisión quedan excluidos de este helper para permitir el ciclo explícito **Editar campos → confirmar**.

El patrón se reutiliza en datos personales, cuotas, historial anual y detalle del año actual. La franja primaria del sistema visual funciona en Claro, Oscuro y Alto contraste y acompaña, pero no reemplaza, la semántica nativa de bloqueo. Los valores automáticos derivados no se confunden con datos documentales y mantienen sus reglas específicas de edición.

### UX.4.6g R1 — frontera de escenarios de retiro

Paso 5 mantiene dos capas separadas: `app/static/js/retirement.js` propone y conserva la selección visible, mientras `app/services/retirement.py` construye fechas/cuotas sin decidir elegibilidad. Las sugerencias posteriores se derivan de la cobertura de Paso 4; las elecciones anticipadas requieren acción explícita. `app/engines/elegibilidad.py` y los motores de prestaciones continúan siendo la frontera jurídica para determinar modalidad y factores.
### Contrato transversal de fechas

`app/static/js/accessibility.js` aplica de forma idempotente validación y clase visual a todos los `input[type=date]`, incluidos controles dinámicos. `app/static/css/accessibility.css` define la geometría compacta común. Las superficies pueden declarar límites `min`/`max` más restrictivos; la capa transversal solo aporta valores por defecto cuando faltan. Paso 5 consume este contrato y añade exclusivamente la explicación de cobertura contra el horizonte salarial.

## 14. Guía pública de cálculo

`/como-se-calcula` es una superficie pública de transparencia. `app/services/calculation_guide.py` lee parámetros de `regulations/*.json` y los entrega a `app/templates/calculation_guide.html`; no ejecuta `app/engines/` ni construye resultados individuales.

El Paso 6 enlaza a la sección del sistema correspondiente mediante anclas públicas (`#sebd`, `#mixto`, `#sucgs`) sin transportar datos personales, salarios, cuotas ni montos en la URL. Las sustituciones numéricas del caso individual permanecen en la trazabilidad de resultados.

La guía reutiliza el catálogo de fuentes de `app/services/regulatory_sources.py`. Por tanto, una modificación normativa o de fórmula exige revisar en conjunto motor, JSON versionado, trazabilidad, guía pública y pruebas relacionadas.

## DEV.2 — Centro de desarrollo

La ruta interna `/dev/centro-desarrollo` muestra una superficie local de desarrollo para revisar el estado técnico de Developer Diagnostics. Esta vista no ejecuta cálculos previsionales, no lee cuerpos HTTP, no procesa PDFs, no muestra rutas absolutas del equipo y no expone identidad, salarios, cuotas ni montos de pensión.

DEV.2 quedó cerrado documentalmente en R4 después de integrar R1, R2 y R3. R1 abrió la ruta interna, R2 añadió el visor diagnóstico seguro y la exportación ZIP sanitizada, R3 añadió el autodiagnóstico técnico local y R4 sincroniza la documentación viva del bloque.

La ruta usa `MRP_DEV_MODE` solo como indicador de activación diagnóstica, conserva `0.0.26-beta` como versión visible/canónica legacy, no la trata como candidato VER.2, no añade rutas públicas nuevas, no modifica motores previsionales, no crea tags y no adelanta el cierre transversal de VER.2.

## Política de estructura por extensión

La arquitectura documental de mantenibilidad incorpora una política por extensión
en `docs/standards/file-structure-by-extension.md`. Esa política separa archivos
operativos, documentación histórica, configuración, datos JSON y activos binarios.

Las plantillas oficiales se ubican en `docs/templates/file-structure/` y
funcionan como contrato inicial para archivos futuros. Las plantillas no agregan
capas de ejecución; solo estandarizan encabezados, propósito, alcance y
comentarios internos cuando el formato lo permite.


## SEC.2 R6 — Control de sesión administrativa

La autenticación administrativa separa la validación inicial mediante secreto del mantenimiento de sesión web temporal. La sesión no almacena datos personales y se invalida por expiración o revocación.

## Reconciliación de la superficie administrativa post-SEC.2

La arquitectura administrativa mantiene dos formas de acceso sobre la misma
credencial externa: Bearer para clientes técnicos y login web que materializa
una sesión temporal en memoria. `MRP_ADMIN_ENABLED` conserva prioridad sobre
ambas. La sesión web no es una cuenta de usuario ni una persistencia de
simulaciones y sus cookies nunca forman parte de Developer Diagnostics.

AUD.SEC2 R1 corrige la ruta POST de login para respetar el kill switch, limita
el fallback de sesión a errores 401, convierte logout en POST y extiende
`Cache-Control: no-store` a `/dev/`.
