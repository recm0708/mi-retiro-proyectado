# Calculadora de Pensión CSS

Aplicación web para estimar y comparar pensiones de jubilación de la Caja de Seguro Social de Panamá.

El proyecto contempla los distintos sistemas y subsistemas previsionales y permitirá realizar proyecciones considerando edad, cuotas, historial salarial, continuidad laboral y escenarios de crecimiento salarial. Los cálculos legales definitivos se incorporarán únicamente después de consolidar y versionar la normativa aplicable.

## Sistemas contemplados

- Subsistema Exclusivamente de Beneficio Definido (SEBD)
- Subsistema Mixto
- Sistema Único de Capitalización con Garantía Solidaria (SUCGS)

## Objetivos principales

La aplicación busca permitir al usuario:

- registrar sus datos previsionales;
- calcular su edad y fechas de referencia;
- registrar cuotas históricas y proyectar cuotas futuras;
- registrar historial anual de cuotas y salario cotizado/reportado;
- ingresar el salario actual como semanal, quincenal, mensual o anual;
- normalizar el salario actual a diferentes periodicidades;
- proyectar salarios futuros mediante distintos escenarios;
- combinar historial real, año actual parcial y proyección futura en una línea temporal;
- determinar si cumple requisitos para una prestación;
- calcular pensiones según el sistema correspondiente;
- estimar cuándo alcanzará determinados requisitos de cuotas;
- comparar edades de retiro y años adicionales de trabajo;
- visualizar la evolución estimada de la pensión;
- generar informes de resultados;
- mantener separados los datos históricos de los datos proyectados.

## Estado actual del desarrollo

La versión `0.1.0` se encuentra en desarrollo.

El asistente está organizado en seis pasos:

1. **Datos personales:** implementado.
2. **Cuotas:** implementado con análisis preliminar mediante API.
3. **Historial:** implementado en validación. Incluye captura anual de cuotas y salario cotizado/reportado, validación contra las cuotas reales del Paso 2, formato monetario controlado y salario actual normalizado para proyección.
4. **Proyección:** implementado en validación. Incluye salario constante, variación porcentual, salario futuro conocido, comparación de escenarios, precisión monetaria sin redondeos intermedios y línea temporal que separa historial real, año actual y futuro proyectado.
5. **Retiro:** implementado en validación. Calcula edad y fecha de referencia, escenarios adicionales, cuotas futuras estimadas respetando el cierre del año actual y verifica si la proyección salarial cubre el horizonte de retiro.
6. **Resultados:** integración implementada para las modalidades generales del SEBD y para el Subsistema Mixto. Permite seleccionar un escenario de retiro, escoger el escenario salarial, verificar la prestación aplicable y mostrar el desglose del cálculo.

El SEBD ya cubre Normal, Anticipada, Proporcional, Proporcional Anticipada e Indemnización por Vejez. El Subsistema Mixto dispone de backend e integración visual para su Componente de Beneficio Definido, Componente de Ahorro Personal cuando se suministran parámetros oficiales y transición operativa hacia SUCGS. SUCGS dispone del componente contributivo del artículo 196, la capa solidaria de los artículos 194 y 195, la garantía de reemplazo mínimo del artículo 197 y su integración visual completa en el Paso 6.

El asistente permite volver directamente a pasos ya disponibles desde los indicadores de progreso o desde el selector persistente `Ir a paso`; un paso posterior se deshabilita si sus prerrequisitos dejaron de ser válidos después de una edición.

## API disponible

Actualmente FastAPI expone:

```text
GET  /
GET  /simulacion
GET  /comparar
GET  /salud
POST /api/simulacion/cuotas
POST /api/simulacion/historial-salarial
POST /api/simulacion/salario
POST /api/simulacion/proyeccion-salario
POST /api/simulacion/linea-tiempo
POST /api/simulacion/retiro
POST /api/simulacion/sebd/normal
POST /api/simulacion/resultados/sebd-normal
POST /api/simulacion/sebd
POST /api/simulacion/resultados/sebd
POST /api/simulacion/mixto
POST /api/simulacion/resultados/mixto
POST /api/simulacion/sucgs
POST /api/simulacion/resultados/sucgs
```

La documentación automática está disponible en `/docs` durante la ejecución local.

## Tecnologías

Implementadas actualmente:

- Python
- FastAPI
- Uvicorn
- Pydantic
- Jinja2
- HTML
- CSS
- JavaScript
- Bootstrap
- `sessionStorage` para el estado temporal del asistente

Previstas para fases posteriores:

- Chart.js
- SQLite
- generación de informes PDF

## Estructura general

```text
calculadora-pension-css/
├── app/
│   ├── core/
│   ├── modelos/
│   ├── motores/
│   ├── servicios/
│   ├── static/
│   ├── templates/
│   └── main.py
├── data/
├── docs/
├── normativa/
├── tests/
├── .editorconfig
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
└── requirements.txt
```

## Instalación

### 1. Clonar el repositorio

```powershell
git clone https://github.com/recm0708/calculadora-pension-css.git
cd calculadora-pension-css
```

### 2. Crear un entorno virtual

```powershell
python -m venv .venv
```

### 3. Activarlo en PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

## Ejecución

Con el entorno virtual activado:

```powershell
python -m uvicorn app.main:app --reload
```

Abrir en el navegador:

```text
http://127.0.0.1:8000
```

Documentación automática de la API:

```text
http://127.0.0.1:8000/docs
```

## Validación rápida

Para verificar sintaxis y los casos automatizados disponibles:

```powershell
python -m compileall app
python -m unittest discover -s tests -v
```

Después se deben validar manualmente las rutas principales y el flujo del asistente en el navegador. Los casos reales utilizados para contrastar resultados se mantienen anonimizados y sus documentos originales no se versionan.

## Precisión monetaria

Los cálculos monetarios utilizan `Decimal` en las operaciones donde la precisión es relevante. El criterio técnico actual es conservar precisión durante el cálculo y redondear a centavos con `ROUND_HALF_UP` cuando se materializa un resultado monetario. Una regla normativa específica podrá sustituir este criterio en el motor que corresponda.

Los campos monetarios editables muestran separadores de miles y admiten como máximo dos decimales.

## Motor SEBD en desarrollo

El backend ya incorpora la primera modalidad legal del Paso 6: Pensión de Retiro por Vejez Normal del Subsistema Exclusivamente de Beneficio Definido.

La implementación actual calcula los diez mejores años, tasa básica del 60 %, bloques completos de doce cuotas adicionales antes y después de la edad de referencia y los límites máximos aplicables. El monto mínimo indexado por fecha se mantiene pendiente de versionar antes de considerar completo el motor.

La API provisional de esta modalidad está disponible en:

```text
POST /api/simulacion/sebd/normal
```

## Documentación técnica

Los documentos de `docs/` registran progresivamente:

- arquitectura;
- especificación funcional;
- modelo de datos;
- motores de cálculo;
- normativa;
- decisiones técnicas;
- hoja de ruta;
- validación y casos de prueba.

La documentación debe actualizarse cuando un cambio funcional o arquitectónico lo amerite; no es necesario modificar todos los archivos `.md` en cada commit.

## Privacidad

El repositorio no debe contener:

- nombres reales de asegurados utilizados para pruebas;
- números de cédula;
- números de Seguro Social;
- comprobantes privados;
- PDFs personales;
- bases de datos reales;
- información confidencial.

Los casos utilizados para validar los cálculos deberán estar anonimizados. Las convenciones y casos técnicos se documentan en `docs/VALIDACION.md`.

## Advertencia

Esta aplicación genera estimaciones con fines informativos, educativos y de planificación.

Los resultados no constituyen una certificación ni determinación oficial de una pensión.

La determinación oficial de prestaciones corresponde exclusivamente a la Caja de Seguro Social de Panamá.

## Paso 6C — modalidades SEBD

El motor SEBD ya clasifica automáticamente la modalidad aplicable al escenario de retiro entre Normal, Anticipada, Proporcional y Proporcional Anticipada. También identifica escenarios de posible Indemnización por Vejez y situaciones que todavía no cumplen una prestación calculable.

Endpoints generales añadidos:

```text
POST /api/simulacion/sebd
POST /api/simulacion/resultados/sebd
```

Los endpoints específicos de SEBD Normal se conservan para compatibilidad y pruebas de regresión.

La explicación funcional y las fórmulas se resumen en `docs/MODALIDADES_SEBD.md`.

## Paso 6C.2 — Indemnización por Vejez

El motor SEBD calcula también la **Indemnización por Vejez** cuando el escenario alcanza la edad de referencia con menos de 180 cuotas y la fecha es anterior al 1 de marzo de 2036.

Esta prestación se presenta separada de las pensiones mensuales porque es un **pago único**. El cálculo parte de la mensualidad de Pensión de Retiro por Vejez Normal que hipotéticamente habría correspondido y la multiplica por el cociente entre los meses/cuotas mensuales acreditados y seis.

La interfaz del Paso 6 muestra de forma independiente la mensualidad hipotética, el factor `cuotas / 6`, la fórmula aplicada y el pago único estimado. Desde el 1 de marzo de 2036 el clasificador deriva estos casos a la transición SUCGS prevista por la normativa vigente.

En la respuesta de la API, los campos exclusivos de pensión proporcional se expresan como `null` durante una Indemnización por Vejez para indicar que no aplican, en lugar de devolver un cero que pueda interpretarse como un factor utilizado.


## Paso 6D.1 — base del Subsistema Mixto

El backend incorpora una primera implementación controlada del Subsistema Mixto mediante:

```text
POST /api/simulacion/mixto
POST /api/simulacion/resultados/mixto
POST /api/simulacion/sucgs
POST /api/simulacion/resultados/sucgs
```

El cálculo separa estrictamente:

- **Componente de Beneficio Definido (BD):** reutiliza la clasificación legal de retiro por vejez y limita la participación salarial a B/.500.00 mensuales. Cuando solo existe historial anual, el tope mensual se aproxima como `B/.500.00 × cuotas del año` y se emite una advertencia.
- **Componente de Ahorro Personal (CAP):** solo calcula la pensión programada cuando se proporciona el saldo ahorrado/capitalizado y el valor actuarial oficial aplicable. La aplicación no reconstruye todavía el saldo individual a partir del historial anual y no reutiliza factores del SUCGS.
- **Transición:** para el cálculo de retiro, esta fase utiliza como frontera operativa el 01/03/2032 conforme al artículo 188 y al Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria. La discrepancia con la fecha 01/03/2036 que aparece en el artículo 153 se conserva documentada.

Los valores de prueba del divisor actuarial son deliberadamente sintéticos. No deben interpretarse como parámetros vigentes de la CSS.

La explicación técnica y normativa de esta fase se encuentra en `docs/MODALIDADES_MIXTO.md`.

## Paso 6D.2 — devolución y garantía del CAP Mixto

El motor Mixto distingue ahora entre **pensión programada** y **devolución total** del Componente de Ahorro Personal cuando el artículo 187 habilita esta última. La aplicación no escoge automáticamente por el usuario: si existe más de una vía y se utiliza `AUTO`, el resultado queda pendiente hasta una decisión expresa.

También se modela la garantía del Seguro Colectivo de Renta Vitalicia del artículo 184 como continuidad futura de la pensión CAP cuando se agotan los fondos después de superar la expectativa de vida utilizada; esta garantía no incrementa la pensión inicial.

Los pagos únicos del componente BD y del CAP permanecen separados de las pensiones mensuales. El bono de reconocimiento puede ingresarse como dato, pero un monto no confirmado oficialmente mantiene el resultado en estado provisional.

## Paso 6D.3 — integración visual del Subsistema Mixto

El Paso 6 habilita ahora el Subsistema Mixto desde el asistente, sin depender de Swagger. La interfaz reutiliza el historial, la línea temporal salarial y el escenario de retiro de los Pasos 1–5, y solicita de forma explícita los datos del CAP que no pueden deducirse del historial anual:

- saldo ahorrado y capitalizado;
- bono de reconocimiento y su estado de confirmación;
- valor actuarial aplicable, cuando se dispone de él;
- opción `AUTO`, `PENSION_PROGRAMADA` o `DEVOLUCION_TOTAL`.

El resultado visual mantiene separados el componente BD, el CAP, la pensión mensual total, los pagos únicos y la garantía de renta vitalicia. Cuando falta un dato oficial o existe una decisión CAP pendiente, la interfaz muestra el resultado como incompleto en lugar de completar la cifra silenciosamente.

Endpoint integrado:

```text
POST /api/simulacion/resultados/mixto
```

## SUCGS — subfase 6E.3

El motor del Sistema Único de Capitalización con Garantía Solidaria calcula el **Componente Contributivo de Capitalización Solidaria** del artículo 196 cuando se proporciona un saldo acumulado a la fecha de retiro. La fórmula versionada es `saldo / 1000 × factor de pensionamiento actuarial por edad`.

La subfase 6E.3 conserva el **Componente Solidario No Contributivo** del artículo 194 y la **Pensión Garantizada Solidaria** del artículo 195, y añade la garantía de reemplazo mínimo del artículo 197. Los valores B/.144.00 y B/.265.00 se conservan como referencias legales versionadas al 22/05/2025; cuando existan valores vigentes confirmados pueden suministrarse explícitamente.

El saldo no se reconstruye automáticamente desde salarios históricos: esa reconstrucción depende del origen del asegurado, aportes anteriores y posteriores a la reforma y rendimientos efectivos del Fondo Único Solidario. Para el artículo 197, las condiciones de cuotas y distribución se preevalúan con historial anual completo; la estabilidad salarial exige confirmación expresa. Cuando las tres condiciones pueden cerrarse, `pension_mensual_total_estimada` contiene el resultado definitivo del motor SUCGS.

## Paso 6E.4 — integración visual completa del SUCGS

El SUCGS ya puede calcularse desde el Paso 6 del asistente. La interfaz reutiliza historial, proyección y escenario de retiro, solicita el saldo de Capitalización Solidaria y las confirmaciones que no pueden deducirse automáticamente, y presenta de forma separada el componente contributivo, la capa solidaria y la garantía de reemplazo del artículo 197.

La integración no duplica fórmulas en JavaScript. El backend consolida los registros reales y proyectados hasta la fecha de retiro y entrega el resultado explicable del motor SUCGS. La suite de regresión del proyecto alcanza 57 pruebas automatizadas.
