# Arquitectura

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.26-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental:** GOV.1.4 — 2026-08-17
**Clasificación:** Técnica / Pública

Mi Retiro Proyectado es una aplicación web local basada en FastAPI, Jinja2 y JavaScript del navegador. La arquitectura separa presentación, contratos de datos, servicios de integración, motores previsionales, parámetros normativos y observabilidad de desarrollo.

[Índice](INDICE.md) · [Modelo de datos](MODELO_DE_DATOS.md) · [Motor](MOTOR_DE_CALCULO.md) · [Normativa](NORMATIVA.md) · [Observabilidad](OBSERVABILIDAD_LOGS.md)

## 1. Principios

1. **Fuente única del cálculo:** las fórmulas previsionales principales viven en Python.
2. **Normativa separada:** parámetros legales modificables se mantienen en `normativa/`.
3. **Histórico y proyección separados:** una estimación futura no sustituye silenciosamente información acreditada.
4. **Datos faltantes explícitos:** un parámetro que no puede determinarse no se inventa.
5. **Trazabilidad:** motores y servicios exponen advertencias, fuentes y resultados intermedios cuando corresponde.
6. **Procesamiento local por defecto:** el estado de simulación se conserva en el navegador y no existe persistencia permanente automática.
7. **Importación revisable:** extraer un PDF no equivale a confirmar ni calcular.
8. **Versión única:** `VERSION` es la fuente canónica consumida por `app/core/version.py`.
9. **Interfaz desacoplada:** JavaScript administra experiencia, estado temporal y comunicación HTTP; no constituye una segunda implementación de los motores.
10. **Observabilidad lateral:** Developer Diagnostics observa operaciones ya ejecutadas; no vuelve a invocar motores ni replica fórmulas.
11. **Minimización de logs:** los eventos técnicos no contienen cuerpos HTTP, documentos, identificadores ni valores financieros.
12. **Historia preservada:** la documentación vigente describe el contrato actual; bitácoras anteriores se conservan en `docs/historico/`.

## 2. Inventario relevante del paquete `app`

### Núcleo

- `app/core/archivos_pdf.py`
- `app/core/config.py`
- `app/core/constants.py`
- `app/core/dinero.py`
- `app/core/normativa.py`
- `app/core/observabilidad.py`
- `app/core/version.py`

### Modelos

- `app/modelos/comparacion.py`
- `app/modelos/pension.py`
- `app/modelos/resultado_unificado.py`
- `app/modelos/simulacion.py`
- `app/modelos/trazabilidad.py`

### Motores

- `app/motores/elegibilidad.py`
- `app/motores/mixto.py`
- `app/motores/sebd.py`
- `app/motores/sebd_modalidades.py`
- `app/motores/sucgs.py`

### Servicios principales

- `app/servicios/comparador.py`
- `app/servicios/detalle_anio_actual.py`
- `app/servicios/fecha_referencia.py`
- `app/servicios/ficha_digital.py`
- `app/servicios/fuentes_normativas.py`
- `app/servicios/historial_salarios.py`
- `app/servicios/linea_tiempo.py`
- `app/servicios/proyeccion_cuotas.py`
- `app/servicios/proyeccion_salarios.py`
- `app/servicios/referencia_mi_retiro_seguro.py`
- `app/servicios/resultado_unificado.py`
- `app/servicios/resultados.py`
- `app/servicios/resultados_mixto.py`
- `app/servicios/resultados_sebd.py`
- `app/servicios/resultados_sucgs.py`
- `app/servicios/retiro.py`
- `app/servicios/trazabilidad.py`

### Presentación JavaScript crítica

- `app/static/js/accesibilidad.js`
- `app/static/js/comparador.js`
- `app/static/js/detalle_anio_actual.js`
- `app/static/js/gestion_datos.js`
- `app/static/js/historial_salarios.js`
- `app/static/js/importacion_datos_oficiales.js`
- `app/static/js/linea_tiempo.js`
- `app/static/js/moneda.js`
- `app/static/js/navegacion_wizard.js`
- `app/static/js/privacidad.js`
- `app/static/js/referencia_mi_retiro_seguro.js`
- `app/static/js/resultados.js`
- `app/static/js/retiro.js`
- `app/static/js/simulacion.js`
- `app/static/js/tema.js`

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

`app/core/observabilidad.py` implementa el esquema JSONL, correlación aleatoria, redacción, rotación, retención y exportación controlada. El módulo no conoce modelos previsionales ni ejecuta cálculos.

### 3.2. Modelos (`app/modelos/`)

Pydantic define contratos HTTP y de dominio:

- `simulacion.py` — cuotas, historial, detalle del año actual, importaciones, salario, proyección, línea temporal y retiro;
- `pension.py` — contratos SEBD, Mixto, SUCGS y resultados integrados;
- `comparacion.py` — comparación transversal;
- `trazabilidad.py` — pasos y fuentes de cálculo;
- `resultado_unificado.py` — salida transversal común.

La metadata puramente visual y diagnóstica no se convierte automáticamente en modelo Pydantic de negocio.

### 3.3. Servicios (`app/servicios/`)

Los servicios normalizan, integran y coordinan cuotas, historial, detalle actual, proyección, retiro, importaciones, resultados, comparación y fecha externa.

`fecha_referencia.py` puede emitir eventos agregados de cache/consulta cuando Developer Diagnostics está activo. Esos eventos no incluyen URL, fecha recibida ni datos de simulación.

Los parsers documentales son **capas de entrada**, no motores previsionales.

### 3.4. Motores (`app/motores/`)

Los motores aplican las reglas previsionales ya modeladas:

- elegibilidad común;
- SEBD normal;
- modalidades SEBD;
- Subsistema Mixto;
- SUCGS.

No leen PDFs, `sessionStorage`, controles HTML ni logs. Developer Diagnostics no vuelve a invocarlos.

### 3.5. Presentación (`app/templates/`, `app/static/`)

Jinja2 genera las páginas y parciales. JavaScript administra el asistente, estado temporal, importaciones, procedencia, invalidación, llamadas HTTP y representación de resultados.

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
        ↓
Paso 5 — Escenarios de retiro
        ↓
Paso 6 — Resultado del sistema
        ↓
Comparación + trazabilidad + resumen unificado
```

Developer Diagnostics es transversal a las operaciones HTTP, no forma parte de este flujo de negocio y no altera sus resultados.

## 5. Estado temporal del navegador

La simulación se conserva en `sessionStorage`. La preferencia visual y la aceptación versionada de privacidad utilizan almacenamiento local según el contrato de interfaz.

La aplicación no intenta restaurar un `File` seleccionado después de recargar. Puede conservar metadata de una importación confirmada —por ejemplo procedencia o nombre visible del archivo—, nunca la ruta local ni el binario.

Consultar [GESTION_DATOS_SIMULACION.md](GESTION_DATOS_SIMULACION.md).

## 6. Importaciones documentales

### Mi Retiro Seguro

`app/servicios/referencia_mi_retiro_seguro.py` extrae una referencia personal revisable. El archivo original no se persiste.

### Ficha Digital

`app/servicios/ficha_digital.py` devuelve únicamente los registros del año más reciente detectado en la sección salarial del documento.

### Fecha de referencia

`app/servicios/fecha_referencia.py` intenta obtener el encabezado HTTP `Date` mediante HTTPS desde fuentes CSS configuradas. Si no obtiene una fecha consistente, devuelve un resultado no confiable.

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
| `/favicon.ico` |
| `/metodologia` |
| `/salud` |
| `/simulacion` |

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

Consultar [OBSERVABILIDAD_LOGS.md](OBSERVABILIDAD_LOGS.md).

## 10. Precisión

`app/core/dinero.py` centraliza operaciones monetarias sensibles con `Decimal` y materialización a centavos. Los factores actuariales no se formatean ni se tratan como importes monetarios.

Los importes no se incluyen en Developer Diagnostics.

## 11. Versionado

`VERSION` → `app/core/version.py` → `APP_VERSION` → FastAPI/Jinja2/footer.

El esquema de logs (`schema_version`) es un contrato técnico independiente de `VERSION`, normativa y privacidad.

## 12. Persistencia futura

La arquitectura actual no incluye una base de datos de simulaciones. La incorporación de almacenamiento permanente exige una decisión explícita, migraciones/versionado de esquema y revisión de privacidad.

Developer Diagnostics no debe utilizarse como sustituto de persistencia de simulaciones.

## 13. Historia de esta arquitectura

La versión acumulativa anterior a GOV.1.3 R2 se conserva en:

`docs/historico/tecnico/ARQUITECTURA_PRE_GOV1_3_R2.md`

Este documento describe el estado técnico vigente después de GOV.1.4.
