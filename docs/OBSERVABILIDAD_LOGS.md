# Observabilidad y Developer Diagnostics

**Estado:** Vigente — GOV.1.4 cerrado
**Versión de aplicación revisada:** `0.0.71.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica:** `0.0.23-beta`
**Fecha de cierre original:** 2026-08-17
**Última revisión documental:** PLAN.1 R2C — 2026-08-20
**Clasificación:** Técnica / Desarrollo / Privacidad


<!-- DOC1-R1-REVISION-MANUAL:START -->
## Nota de lectura post-MANT.1

La observabilidad de desarrollo conserva su alcance técnico después de MANT.1.

Estado vigente:

- Developer Diagnostics continúa como herramienta local de desarrollo.
- MANT.1 quedó cerrado operativamente en R7.
- DOC.1 R1 no cambia telemetría, logging, rutas ni comportamiento de ejecución.
- Las referencias a bloques siguientes deben leerse desde el estado documental vigente post-MANT.1.
<!-- DOC1-R1-REVISION-MANUAL:END -->

Mi Retiro Proyectado incorpora un mecanismo de diagnóstico **exclusivo de desarrollo**, desactivado por defecto. Su objetivo es depurar fallos, tiempos y dependencias técnicas sin convertir el log en una segunda base de datos de simulaciones.

## 1. Activación

Developer Diagnostics solo se activa con:

```powershell
$env:MRP_DEV_MODE = "1"
```

Cualquier otro valor, incluida la variable ausente, mantiene el diagnóstico desactivado. No existe un control de interfaz para activarlo.

El directorio puede sobrescribirse únicamente para desarrollo/pruebas:

```powershell
$env:MRP_DIAGNOSTIC_DIR = "C:\ruta\temporal"
```

Por defecto se usa:

```text
logs/diagnostico/
```

`logs/` está excluido por `.gitignore`.

## 2. Formato

Cada línea de `mrp-diagnostics.jsonl` es un objeto JSON independiente con esquema lógico `1`:

- `schema_version`;
- `timestamp` UTC;
- `level`;
- `event`;
- `component`;
- `app_version`;
- `correlation_id`;
- `duration_ms`;
- `outcome`;
- `metadata`.

La versión del esquema de diagnóstico es independiente de `VERSION`, de la normativa y de la política de privacidad.

## 3. Correlación

Cada operación observada usa un `correlation_id` aleatorio UUID4 sin guiones.

El identificador:

- se genera aleatoriamente;
- no deriva de cédula, NSS, nombre, fecha de nacimiento, salario, IP u otro dato del usuario;
- permite relacionar eventos técnicos de una misma operación;
- se devuelve como `X-Correlation-ID` únicamente cuando `MRP_DEV_MODE=1` y la ruta está instrumentada.

## 4. Middleware HTTP

R2 integra Developer Diagnostics en FastAPI.

El middleware:

- se omite completamente cuando el modo está apagado;
- llama a `call_next()` una sola vez;
- no lee el cuerpo de la solicitud;
- no serializa modelos Pydantic;
- clasifica la operación mediante etiquetas fijas;
- registra método, clase de operación, estado HTTP y duración;
- registra errores no controlados sin almacenar el mensaje original de la excepción;
- no registra literalmente rutas desconocidas: se agrupan como `http.other`;
- omite recursos estáticos y favicon para reducir ruido.

La observabilidad no ejecuta motores, servicios ni cálculos por segunda vez.

## 5. Operaciones observadas

Las etiquetas técnicas incluyen, entre otras:

```text
simulation.cuotas
simulation.historial
simulation.detalle_actual
simulation.proyeccion_salario
simulation.linea_tiempo
simulation.retiro
motor.sebd
motor.sebd.normal
motor.mixto
motor.sucgs
result.sebd
result.mixto
result.sucgs
result.compare
import.mi_retiro_seguro
import.ficha_digital
system.date_reference
system.health
```

Las etiquetas describen la operación, no sus valores de entrada ni de salida.

## 6. Consulta externa de fecha

`app/services/reference_date.py` registra metadata agregada cuando Developer Diagnostics está activo:

- cache `hit` o `miss`;
- cantidad de fuentes configuradas;
- cantidad de fuentes que respondieron;
- resultado `success`, `unavailable` o `inconsistent`;
- duración.

No registra:

- URL consultada;
- encabezados HTTP;
- fecha recibida;
- IP;
- mensaje de excepción;
- datos de la simulación.

Cuando la consulta ocurre dentro de una solicitud FastAPI, los eventos conservan el mismo `correlation_id` del request.

## 7. Prohibiciones de contenido

Los logs **no deben contener**:

- cuerpos de solicitudes o respuestas;
- campos Pydantic completos;
- nombre, apellido, cédula, NSS, correo o teléfono;
- fecha de nacimiento;
- salarios, montos de pensión, balances o resultados financieros;
- nombres/rutas de PDF;
- binario o texto extraído de documentos;
- headers HTTP completos;
- cookies;
- tokens o credenciales;
- mensajes originales de excepciones cuando puedan incluir datos de entrada.

La función de excepción persiste solo la **clase de excepción** y metadata técnica sanitizada.

La sanitización incorporada es una defensa adicional; el contrato principal sigue siendo **no pasar datos de negocio sensibles al logger**.

## 8. Rotación y retención local

El archivo vigente rota aproximadamente al superar 1 MiB.

Se conservan como máximo tres respaldos locales:

```text
mrp-diagnostics.jsonl
mrp-diagnostics.jsonl.1
mrp-diagnostics.jsonl.2
mrp-diagnostics.jsonl.3
```

No existe telemetría remota automática.

No existe envío de logs a OpenAI, GitHub, CSS ni a otro tercero.

## 9. Exportación controlada

`exportar_diagnostico()` crea un ZIP únicamente con los archivos JSONL diagnósticos reconocidos.

La exportación:

- exige `MRP_DEV_MODE=1`;
- no recorre el repositorio;
- no adjunta PDF;
- no adjunta bases de datos;
- no adjunta uploads;
- no adjunta archivos de sesión;
- no adjunta otros ficheros que coincidan casualmente en el mismo directorio.

No existe todavía un endpoint web de descarga.

## 10. Regresiones de GOV.1.4 R1/R2

R1/R2 incorporan trece pruebas específicas:

- modo apagado;
- modo activo;
- esquema JSONL;
- correlación;
- redacción;
- excepción sanitizada;
- rotación;
- exportación controlada;
- middleware apagado/activo;
- ausencia de doble cálculo;
- error HTTP no controlado;
- cache/consulta externa;
- protección por `.gitignore` y contrato documental.

Con una línea base previa de 474 pruebas, la suite esperada después de R2 fue:

```text
Ran 487 tests
OK
```

## 10.1. Revisión de seguridad GOV.1.5

GOV.1.5 revisa Developer Diagnostics como superficie propia del threat model y mantiene el contrato sin ampliar categorías de datos.

Riesgos residuales documentados:

- copia manual de un ZIP diagnóstico fuera de su ubicación controlada;
- metadata futura añadida sin revisión;
- lectura local por un equipo comprometido.

Toda ampliación del esquema debe reevaluar redacción, finalidad y riesgo.

## 11. Cierre GOV.1.4

GOV.1.4 quedó cerrado después de validar:

- 7/7 regresiones del núcleo de observabilidad;
- 6/6 regresiones de integración;
- 487/487 pruebas de la suite completa;
- compilación Python;
- sintaxis JavaScript;
- `git diff --check`;
- coherencia de README, Arquitectura, Índice, Seguridad/Privacidad, Transparencia, Limitaciones, Validación, Roadmap y Guía interna.

Históricamente, el siguiente bloque de gobierno fue GOV.1.5 — Seguridad, privacidad y transparencia.

GOV.1.4 no modificó fórmulas previsionales ni `VERSION`; en su cierre original la aplicación permanecía en `0.0.23-beta`.

> **Nota posterior — PLAN.1 R2C / 2026-08-20:** este documento fue revalidado sobre `0.0.25-beta` sin cambiar el contrato runtime de Developer Diagnostics. DEV.2 queda reservado para la futura interfaz de Centro de desarrollo y SEC.2 para el hardening asociado. La versión `0.0.23-beta` se conserva arriba únicamente como base histórica del cierre GOV.1.4.
