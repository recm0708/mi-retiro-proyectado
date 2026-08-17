# Arquitectura

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R2 — 2026-08-17
**Clasificación:** Técnica / Pública

Mi Retiro Proyectado es una aplicación web local basada en FastAPI, Jinja2 y JavaScript del navegador. La arquitectura separa presentación, contratos de datos, servicios de integración, motores previsionales y parámetros normativos.

[Índice](INDICE.md) · [Modelo de datos](MODELO_DE_DATOS.md) · [Motor](MOTOR_DE_CALCULO.md) · [Normativa](NORMATIVA.md)

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
10. **Historia preservada:** la documentación vigente describe el contrato actual; bitácoras anteriores se conservan en `docs/historico/`.

## 2. Inventario actual del paquete `app`

La siguiente lista se deriva del árbol local existente al aplicar GOV.1.3 R2.

- `app/core/__init__.py`
- `app/core/archivos_pdf.py`
- `app/core/config.py`
- `app/core/constants.py`
- `app/core/dinero.py`
- `app/core/normativa.py`
- `app/core/version.py`
- `app/modelos/__init__.py`
- `app/modelos/comparacion.py`
- `app/modelos/pension.py`
- `app/modelos/resultado_unificado.py`
- `app/modelos/simulacion.py`
- `app/modelos/trazabilidad.py`
- `app/motores/__init__.py`
- `app/motores/elegibilidad.py`
- `app/motores/mixto.py`
- `app/motores/sebd.py`
- `app/motores/sebd_modalidades.py`
- `app/motores/sucgs.py`
- `app/servicios/__init__.py`
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
- validación defensiva de archivos PDF.

`app/core/version.py` lee `VERSION`; `app/core/config.py` consume ese valor y expone identidad pública. Los parámetros previsionales no se definen allí.

### 3.2. Modelos (`app/modelos/`)

Pydantic define contratos HTTP y de dominio:

- `simulacion.py` — cuotas, historial, detalle del año actual, importaciones, salario, proyección, línea temporal y retiro;
- `pension.py` — contratos SEBD, Mixto, SUCGS y resultados integrados;
- `comparacion.py` — comparación transversal;
- `trazabilidad.py` — pasos y fuentes de cálculo;
- `resultado_unificado.py` — salida transversal común.

La metadata puramente visual del navegador no se convierte automáticamente en modelo Pydantic.

### 3.3. Servicios (`app/servicios/`)

Los servicios normalizan, integran y coordinan:

- cuotas e historial;
- detalle salarial del año actual;
- proyección salarial y línea temporal;
- escenarios de retiro;
- extracción de Mi Retiro Seguro y Ficha Digital;
- verificación de fecha externa;
- preparación de resultados por sistema;
- comparación, trazabilidad y catálogo de fuentes.

Los parsers documentales son **capas de entrada**, no motores previsionales.

### 3.4. Motores (`app/motores/`)

Los motores aplican las reglas previsionales ya modeladas:

- elegibilidad común;
- SEBD normal;
- modalidades SEBD;
- Subsistema Mixto;
- SUCGS.

No leen PDFs, `sessionStorage` ni controles HTML.

### 3.5. Presentación (`app/templates/`, `app/static/`)

Jinja2 genera las páginas y parciales. JavaScript:

- administra el asistente;
- conserva el estado temporal;
- coordina importaciones y confirmaciones;
- aplica procedencia y bloqueos de interfaz;
- invalida resultados dependientes;
- llama a la API;
- representa resultados y advertencias.

CSS se separa entre base, sistema visual y accesibilidad.

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

Una modificación ascendente invalida los resultados dependientes. Existe una reconciliación ascendente controlada desde el detalle del año actual hacia las cuotas agregadas cuando el dato más reciente lo justifica; no se utiliza para conservar resultados obsoletos.

## 5. Estado temporal del navegador

La simulación se conserva en `sessionStorage`. La preferencia visual y la aceptación versionada de privacidad utilizan almacenamiento local según el contrato de interfaz.

La aplicación no intenta restaurar un `File` seleccionado después de recargar. Puede conservar metadata de una importación confirmada —por ejemplo procedencia o nombre visible del archivo—, nunca la ruta local ni el binario.

Consultar [GESTION_DATOS_SIMULACION.md](GESTION_DATOS_SIMULACION.md).

## 6. Importaciones documentales

### Mi Retiro Seguro

`app/servicios/referencia_mi_retiro_seguro.py` extrae una referencia personal revisable. Puede devolver identificadores opcionales solo cuando el documento los permite determinar; el archivo original no se persiste.

Las filas distinguen `HISTORICO`, `HISTORICO_PROYECTADO` y `PROYECTADO`. El total acreditado y el total acumulado que puede incluir proyección permanecen conceptos diferentes.

### Ficha Digital

`app/servicios/ficha_digital.py` devuelve únicamente los registros del **año más reciente detectado** en la sección salarial del documento. No utiliza el reloj local para escoger ese año.

El contrato de salida contiene año, mes, salario y estado salarial. La asignación de una cuota al detalle mensual ocurre en la capa de estado/interfaz cuando se confirma la importación; no se agrega un campo de cuota al modelo `RegistroFichaDigital`.

### Fecha de referencia

`app/servicios/fecha_referencia.py` intenta obtener el encabezado HTTP `Date` mediante HTTPS desde fuentes CSS configuradas. Si no obtiene una fecha consistente, devuelve un resultado no confiable y la interfaz adopta una conducta conservadora.

No se envían datos de la simulación durante esa consulta.

## 7. API actual

El inventario se deriva de los decoradores FastAPI presentes en `app/main.py` al aplicar R2.

| Método | Ruta |
|---|---|
| `GET` | `/favicon.ico` |
| `GET` | `/` |
| `GET` | `/simulacion` |
| `GET` | `/comparar` |
| `GET` | `/metodologia` |
| `POST` | `/api/simulacion/cuotas` |
| `POST` | `/api/simulacion/historial-salarial` |
| `POST` | `/api/simulacion/detalle-anio-actual` |
| `POST` | `/api/simulacion/referencia-mi-retiro-seguro` |
| `POST` | `/api/simulacion/ficha-digital` |
| `GET` | `/api/sistema/fecha-referencia` |
| `POST` | `/api/simulacion/salario` |
| `POST` | `/api/simulacion/proyeccion-salario` |
| `POST` | `/api/simulacion/linea-tiempo` |
| `POST` | `/api/simulacion/retiro` |
| `POST` | `/api/simulacion/sebd/normal` |
| `POST` | `/api/simulacion/resultados/sebd-normal` |
| `POST` | `/api/simulacion/sebd` |
| `POST` | `/api/simulacion/resultados/sebd` |
| `POST` | `/api/simulacion/mixto` |
| `POST` | `/api/simulacion/resultados/mixto` |
| `POST` | `/api/simulacion/sucgs` |
| `POST` | `/api/simulacion/resultados/sucgs` |
| `POST` | `/api/simulacion/comparar-escenarios` |
| `GET` | `/salud` |

Los endpoints bajo `/api/simulacion/` reciben `Cache-Control: no-store`.

## 8. Cabeceras defensivas

El middleware global establece actualmente:

- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options: DENY`;
- `Referrer-Policy: no-referrer`;
- `Permissions-Policy` restrictiva;
- CSP explícita;
- `Cache-Control: no-store` en servicios de simulación.

La CSP actual permite temporalmente recursos Bootstrap desde jsDelivr. La evaluación de terceros y el cierre pre-beta de esa decisión pertenecen a GOV.1.5.

## 9. Precisión

`app/core/dinero.py` centraliza operaciones monetarias sensibles con `Decimal` y materialización a centavos. Los factores actuariales no se formatean ni se tratan como importes monetarios.

## 10. Versionado

`VERSION` → `app/core/version.py` → `APP_VERSION` → FastAPI/Jinja2/footer.

La versión normativa, la versión jurídica de privacidad y la futura versión de esquema de logs son contratos independientes.

## 11. Persistencia futura

La arquitectura actual no incluye una base de datos de simulaciones. La incorporación de SQLite u otro almacenamiento permanente exige una decisión explícita, migraciones/versionado de esquema y una revisión de privacidad.

## 12. Historia de esta arquitectura

La versión anterior, que acumulaba descripciones cronológicas de UX.3–UX.4.6d, se conserva en:

`docs/historico/tecnico/ARQUITECTURA_PRE_GOV1_3_R2.md`

Ese snapshot es evidencia histórica; este documento describe el estado técnico vigente.
