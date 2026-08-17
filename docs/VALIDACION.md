# Validación

La validación combina pruebas automatizadas, casos sintéticos controlados y regresiones anonimizadas contra resultados conocidos.

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Objetivo

Las pruebas deben detectar regresiones en:

- precisión monetaria;
- cuotas y fechas;
- proyección salarial;
- línea temporal;
- modalidades SEBD;
- componentes Mixto;
- capas SUCGS;
- servicios integrados del Paso 6.

## 2. Comandos de validación

Antes de consolidar cambios:

```powershell
python -m compileall app
Get-ChildItem .\app\static\js\*.js | ForEach-Object { node --check $_.FullName }
python -m unittest discover -s tests -v
git diff --check
```

Estado antes del bloque 6F:

```text
Ran 57 tests
OK
```

El número de pruebas puede aumentar; lo importante es que la suite completa finalice en `OK`.

## 3. Cobertura automatizada actual

Archivos principales:

```text
tests/test_dinero.py
tests/test_proyeccion_salarios.py
tests/test_linea_tiempo.py
tests/test_retiro.py
tests/test_accesibilidad_ux4.py
tests/test_ux46a_redisenio_integral.py

tests/test_sebd.py
tests/test_sebd_modalidades.py
tests/test_indemnizacion_vejez.py
tests/test_resultados.py
tests/test_resultados_modalidades.py

tests/test_mixto.py
tests/test_mixto_prestaciones_cap.py
tests/test_resultados_mixto.py

tests/test_sucgs.py
tests/test_sucgs_capa_solidaria.py
tests/test_sucgs_reemplazo.py
tests/test_resultados_sucgs.py
```

## 4. Reglas para casos reales

Los documentos personales originales no se versionan.

Si una regresión deriva de un caso real:

1. conservar el original fuera de Git;
2. extraer únicamente los valores necesarios;
3. anonimizar fechas o datos cuando sea posible sin destruir la propiedad matemática que se prueba;
4. versionar solo el caso sintético/anonimizado;
5. documentar qué propiedad debe reproducirse.

Ver [tests/casos_validacion/README.md](../tests/casos_validacion/README.md).

## 5. Regresión SEBD anonimizada principal

Existe una regresión femenina anonimizada que reproduce una pensión mensual de:

```text
B/.741.59
```

Propiedades controladas:

- 281 cuotas históricas;
- diez mejores años conocidos;
- salario base aproximado de B/.1,163.28;
- tres bloques completos de 12 cuotas excedentes;
- tasa resultante de 63.75 %.

Esta regresión protege el cálculo normal y su precisión monetaria.

## 6. Caso masculino de edad de referencia

Se valida al menos:

- fecha de nacimiento masculina;
- edad de referencia de 62 años;
- fecha exacta de referencia;
- comportamiento de escenarios de retiro.

No se fuerza una coincidencia monetaria con una estimación oficial cuando el historial mensual necesario no está disponible.

## 7. Caso maestro sintético del asistente

Para pruebas visuales transversales se utiliza un caso sintético estable.

Datos base:

```text
Fecha de nacimiento: 16/11/1969
Sexo: femenino
Fecha de ingreso: 01/11/2001
Cuotas históricas al corte: 297
Cuotas 2026 al corte: 7
Cierre esperado 2026: 12
Cuotas futuras por año: 12
Salario mensual: B/.1,000.00
Proyección: constante
Retiro de referencia: 16/11/2026
Cuotas estimadas al retiro: 300
```

El historial sintético suma 297 cuotas y B/.297,000.00 de salario cotizado acumulado, con 2 cuotas en 2001 y años completos posteriores.

## 8. Validación SEBD del caso maestro

Con 300 cuotas y salario base B/.1,000.00:

```text
cuotas excedentes = 60
bloques de 12 = 5
incremento = 6.25 puntos porcentuales
tasa total = 66.25 %
pensión = B/.662.50
```

Resultado patrón:

```text
B/.662.50 mensuales
```

## 9. Validación Mixto del caso maestro

Datos específicos sintéticos:

```text
Saldo CAP: B/.100,000.00
Bono: B/.5,000.00
Bono confirmado: sí
Valor actuarial sintético: 200
Opción CAP: pensión programada
```

Resultado controlado:

```text
Componente BD: B/.331.25
Componente CAP: B/.525.00
Pensión total: B/.856.25
```

El valor actuarial 200 es **sintético para pruebas** y no representa un divisor oficial general.

También se validan:

- CAP sin divisor → cálculo incompleto;
- 200 cuotas + `AUTO` → decisión pendiente;
- 200 cuotas + devolución → B/.20,000.00 como pago único y B/.250.00 mensuales de BD;
- menos de 180 cuotas → indemnización BD y devolución CAP separadas;
- transición a SUCGS desde 01/03/2032.

## 10. Validación SUCGS — componente contributivo

Caso controlado:

```text
Edad: 57
Saldo: B/.100,000.00
Factor: 4.77
Divisor: 1,000
```

Resultado:

```text
100,000 / 1,000 × 4.77 = B/.477.00
```

## 11. Validación SUCGS — capa solidaria

### 11.1. Contributiva superior a garantía

```text
Contributiva: B/.477.00
Resultado después de capa solidaria: B/.477.00
```

### 11.2. Pensión Garantizada Solidaria

```text
Saldo: B/.40,000.00
Contributiva: B/.190.80
Referencia PGS: B/.265.00
Complemento: B/.74.20
Resultado: B/.265.00
```

### 11.3. Beneficio Mínimo a los 65

```text
Saldo: B/.20,000.00
Factor a 65: 5.44
Contributiva: B/.108.80
Valor mínimo universal: B/.144.00
Complemento: B/.35.20
Resultado: B/.144.00
```

## 12. Validación SUCGS — artículo 197

### 12.1. Garantía completa

Caso sintético equilibrado de 240 cuotas:

```text
Cuotas primeros 20 años: 120
Cuotas años restantes: 120
Salario promedio base: B/.1,000.00
Tasa mínima: 60 %
Objetivo: B/.600.00
Resultado contributivo previo: B/.477.00
Complemento: B/.123.00
Pensión total: B/.600.00
```

### 12.2. Garantía proporcional

Caso sintético de 180 cuotas:

```text
Cuotas por tramo: 90 / 90
Tasa proporcional: 45 %
Salario promedio base: B/.1,000.00
Objetivo: B/.450.00
Resultado previo: B/.144.00
Complemento: B/.306.00
Pensión total: B/.450.00
```

### 12.3. Distribución insuficiente

Caso de 240 cuotas con distribución 180 / 60:

```text
Condición 50/50: no cumple
Garantía art. 197: no aplica
Pensión final conservada: B/.477.00
```

### 12.4. Estabilidad pendiente

Si las condiciones objetivas cumplen pero la estabilidad salarial permanece sin confirmar:

```text
garantia_reemplazo_evaluada = false
calculo_total_disponible = false
pension_mensual_total_estimada = null
```

La aplicación no debe suponer el cumplimiento.

## 13. Validación visual del Paso 6

Antes de 6F se ha validado manualmente que:

- SEBD muestra modalidad, pensión y desglose;
- Mixto muestra BD, CAP, pensión mensual, pagos únicos y garantía;
- SUCGS muestra componente contributivo, capa solidaria, condiciones del artículo 197 y pensión total;
- los importes usan formato monetario coherente;
- los factores actuariales no se presentan como balboas;
- la navegación directa entre pasos funciona.

## 14. Criterios para nuevas pruebas

Toda nueva fórmula o interpretación normativa debe incluir al menos:

- caso positivo;
- caso límite;
- caso donde no aplica;
- caso de dato faltante cuando la ausencia sea legalmente relevante.

Si una corrección responde a un error encontrado manualmente, debe añadirse una regresión automatizada antes de cerrar el cambio.


## Comparador 6F.1

La suite incorpora `tests/test_comparador.py` con tres regresiones transversales:

1. SEBD reproduce B/.741.59 como base y B/.765.67 en +1 año, con diferencia de B/.24.08.
2. Mixto normaliza B/.856.25 como pensión mensual y mantiene separado cualquier pago único.
3. SUCGS normaliza el caso maestro de B/.477.00 como resultado mensual completo.

Estado después de 6F.1: **60 pruebas automatizadas en OK**.


## 12. Validación 6F.2

La suite contiene **63 pruebas**. `tests/test_trazabilidad.py` valida tres cadenas explicativas:

1. SEBD normal: salario base, tasa y resultado mensual;
2. Mixto: separación BD/CAP y suma mensual;
3. SUCGS: fórmula saldo ÷ 1,000 × factor y evaluación del artículo 197.

También se verifica que las fuentes expuestas por la trazabilidad utilicen URLs oficiales `https://` cargadas desde los JSON normativos.

## Validación 6F.3

Se valida que el catálogo incluya SEBD, Mixto y SUCGS, que sus fuentes tengan URLs HTTPS y títulos legibles y que `/metodologia` responda correctamente incluyendo el Texto Único, la Resolución 57,805-2025-J.D. y el acceso a Mi Caja Digital.

## Validación 6F.4

La suite queda en **83 pruebas automatizadas**. `tests/test_resultado_unificado.py` valida el contrato transversal en tres situaciones:

1. SEBD: una Indemnización por Vejez se normaliza como **pago único** y no como pensión mensual;
2. Mixto: una decisión pendiente del CAP conserva `DECISION_REQUERIDA` y no finge un cálculo completo;
3. SUCGS: el caso completo de B/.477.00 se conserva como **pensión mensual** sin pago único.

Las pruebas integradas existentes de SEBD, Mixto y SUCGS también comprueban que los servicios anexen `resumen_unificado` sin modificar las cifras de regresión validadas. El comparador consume este resumen común y continúa calculando diferencias sin replicar fórmulas previsionales.



## 14. Identidad y contenido visible

`tests/test_identidad_interfaz.py` protege la capa pública frente a regresiones de presentación:

- nombre visible `Mi Retiro Proyectado`;
- ausencia del nombre anterior;
- ausencia de etiquetas de subfase en páginas públicas;
- uso de `Asegurado(a) / Asegurados(as)`;
- separación entre información normativa útil y rutas técnicas del repositorio;
- pie de página con aviso de independencia y acceso a Mi Caja Digital.

Estas pruebas no validan fórmulas previsionales; complementan las regresiones de motor verificando la presentación destinada al Asegurado(a).

## Validación de apariencia y accesibilidad base

La suite incluye regresiones que verifican la presencia de los cuatro modos visuales, persistencia local de la preferencia, enlace de salto al contenido, semántica de página activa, footer compacto, foco visible, movimiento reducido y altura mínima de objetivos táctiles.

La validación automatizada no sustituye la revisión visual manual en los cuatro temas ni una auditoría WCAG con tecnologías de apoyo.


## Validación UX.3 — responsive y último mes acreditado

La suite queda en **96 pruebas automatizadas** después de incorporar las regresiones de mantenimiento técnico posteriores a UX.3.

`tests/test_responsive_ux3.py` protege:

- navegación persistente inferior en móvil y respeto a áreas seguras;
- progreso horizontal desplazable;
- tablas extensas con ancho mínimo y desplazamiento localizado;
- acciones de formularios a ancho completo en móvil;
- selector mensual `ultimo_mes_cuotas`;
- conservación de la denominación `Abrir recurso oficial` para recursos que no son fuente normativa.

`tests/test_retiro.py` incorpora tres regresiones adicionales:

1. un último mes anterior deriva al último día calendario del mes;
2. el mes actual nunca genera una fecha de corte posterior a la evaluación;
3. un mes futuro se rechaza.

La revisión manual inmediata se realiza en laptop/PC. La comprobación específica en móvil, tablet y pantallas grandes se mantiene pendiente para una ronda posterior de validación multidispositivo.

## Mantenimiento técnico posterior a UX.3

`tests/test_mantenimiento_tecnico.py` protege dos condiciones de infraestructura:

1. `.gitattributes` debe forzar `eol=lf` para todo archivo detectado como texto, incluidos archivos sin extensión;
2. `/favicon.ico` debe responder `204 No Content` mientras no exista el favicon definitivo, evitando un `404` sin introducir un icono provisional.

Con estas dos regresiones, la suite completa alcanza **96 pruebas automatizadas**.

## Validación UX.4.1 — semántica y ayudas contextuales

La suite completa alcanza **108 pruebas automatizadas**. `tests/test_accesibilidad_ux4.py` conserva siete regresiones base que verifican:

1. carga global de `accesibilidad.css` y `accesibilidad.js`;
2. landmark de navegación, región viva global y descripción del selector de tema;
3. catálogo de ayudas contextuales para campos previsionales ambiguos;
4. marcado `aria-invalid`, anuncio y foco del primer control inválido;
5. relación semántica entre progreso, controles y paneles del wizard;
6. captions de tablas y foco de contenedores cuando existe desplazamiento horizontal;
7. estilos de ayudas, alto contraste y controles inválidos.

Cuando Node.js LTS está instalado en el equipo de desarrollo, se valida adicionalmente la sintaxis de `app/static/js/accesibilidad.js` y `app/static/js/retiro.js` con `node --check`. Esta comprobación es auxiliar: Node.js no es requisito de ejecución de FastAPI ni forma parte de `requirements.txt`. Las regresiones verifican presencia y contrato de la capa accesible, pero no sustituyen una auditoría manual con lector de pantalla.

La revisión visual inmediata de UX.4.1 se realizó en PC/laptop. Se comprobaron los temas visuales, ayudas contextuales, navegación del asistente, selección de escenarios y alineación de Resultados. La revisión específica en móvil/tablet y la auditoría con tecnologías de apoyo permanecen diferidas para el cierre integral de WCAG 2.2.

### Remate visual de UX.4.1

`tests/test_ux4_remate_visual.py` agrega cinco regresiones adicionales:

1. nombre abreviado de SUCGS en el selector del Paso 1;
2. tratamiento semántico propio para **Completar cuotas vacías con 12**;
3. selección de un escenario futuro desde cualquier punto de su fila;
4. alineación de la acción SEBD con el selector salarial;
5. tooltip contextual compacto operable mediante hover y foco.

Con estas regresiones la suite completa queda en **108 pruebas automatizadas**.

## Validación UX.4.2 — estados activos y selección perceptible

La suite alcanza **112 pruebas automatizadas**. `tests/test_ux42_estados_visuales.py` añade cuatro regresiones de presentación:

1. el paso activo usa número blanco cuando el tema efectivo es Claro;
2. la fila seleccionada de retiro dispone de tokens específicos para Claro, Oscuro y Alto contraste;
3. la selección refuerza fondo, contorno, radio y badge de `Fecha futura`;
4. el foco de teclado sobre el radio resalta la fila asociada y existe una adaptación para `forced-colors`.

Estas regresiones protegen la estructura CSS, pero la percepción final del contraste y de la jerarquía de selección se revisa manualmente en PC/laptop antes del cierre de UX.4.2. La ronda multidispositivo continúa diferida.


## Validación UX.4.3 — errores, foco y teclado

La suite alcanza **124 pruebas automatizadas**. `tests/test_ux43_formularios_teclado.py` añade doce regresiones:

1. los errores nativos crean un mensaje asociado mediante `aria-errormessage`;
2. el estado inválido y su mensaje se eliminan cuando el control vuelve a ser válido o el formulario se reinicia;
3. los errores dinámicos usan `role="alert"` sin una segunda región `assertive`;
4. una alerta general recibe foco únicamente cuando pasa de oculta a visible y no desplaza un campo que ya se está corrigiendo;
5. las advertencias no urgentes pueden usar `status/polite`;
6. el foco programático de mensajes dispone de contorno visible también en Alto contraste;
7. el radio de escenarios de retiro acepta Enter sin convertir la fila completa en un tab stop adicional;
8. Inicio, Simulación, Comparador y Metodología conservan un único `h1`;
9. las clases añadidas desde la sincronización observada se protegen contra escrituras redundantes para evitar ciclos del `MutationObserver`;
10. la limpieza reactiva consulta `ValidityState.valid` y no usa `checkValidity()` para evitar redisparar `invalid`;
11. el mensaje específico de un control inválido es visible y no usa `visually-hidden`;
12. el manejador `invalid` suprime el globo nativo y mantiene el mensaje inline propio asociado.

Además de las pruebas unitarias, el remate de estabilidad se verifica con un navegador Chromium real contra `/simulacion`, comprobando que el documento termina de cargar y que el proceso no queda atrapado en un ciclo de mutaciones. La validación manual inmediata de UX.4.3 se mantiene en PC/laptop e incluye provocar campos obligatorios vacíos en los Pasos 1 y 2 para confirmar que el mensaje inline aparece, el foco llega al primer control inválido y el estado se limpia al corregirlo. La comprobación con lector de pantalla, móvil/tablet y otras tecnologías de apoyo sigue reservada para la ronda integral de cierre WCAG 2.2.


## Validación UX.4.4 — edad anual en historial y proyección

La suite alcanzaba **128 pruebas automatizadas** al incorporar la edad anual. `tests/test_ux44_edad_linea_tiempo.py` protege cuatro condiciones:

1. la edad anual se deriva de `persona.fecha_nacimiento` y del año de cada fila;
2. Historial salarial real contiene la columna **Edad** entre Año y Cuotas;
3. Proyección futura contiene la columna **Edad** entre Año y Cuotas proyectadas;
4. la tabla conserva un ancho mínimo legible y `/simulacion` continúa cargando el recurso de línea temporal.

La validación manual debe contrastar al menos los casos de referencia disponibles contra sus comprobantes oficiales. Para el caso femenino de nacimiento en 1969, 1992 debe mostrar 23 y 2027 debe mostrar 58; para el caso masculino de nacimiento en 1966, 1986 debe mostrar 20 y 2028 debe mostrar 62. Los documentos originales con datos personales permanecen fuera del repositorio.


## Validación UX.4.4 — detalle salarial del año actual

La suite alcanza **138 pruebas automatizadas**. `tests/test_ux44_detalle_anio_actual.py` añade diez regresiones:

1. salario disponible y salario con cuota acreditada se totalizan por separado;
2. la captura quincenal deriva correctamente un mes parcial o completo;
3. las bases sugeridas usan únicamente meses completos;
4. una diferencia entre cuotas marcadas y Paso 2 se informa sin inventar un mes;
5. `POST /api/simulacion/detalle-anio-actual` responde con el último mes acreditado normalizado;
6. la interfaz ofrece captura mensual/quincenal, acceso a Mi Caja Digital y continuidad con la importación confirmada desde el Paso 1;
7. la base salarial permite último mes completo, promedio del año actual y promedio de tres meses completos;
8. un detalle coherente sincroniza el salario acreditado con la fila anual actual;
9. el Paso 5 deriva el último mes acreditado únicamente cuando las cuotas coinciden;
10. `/simulacion` carga el módulo `detalle_anio_actual.js`.

La validación manual en PC/laptop debe ejecutar al menos dos fotografías del mismo año: una con el último mes **parcial** y otra con ese mismo mes ya **completo**, confirmando que cambia el salario disponible. Desde UX.4.6d R3, los meses importados desde Ficha Digital deben aparecer con su casilla de cuota marcada y bloqueada; los meses no importados permanecen manuales.

Los valores personales utilizados para esas comprobaciones permanecen fuera del repositorio.


## Validación UX.4.4 — referencia PDF personal y comparación dinámica

La suite alcanzaba **147 pruebas automatizadas** antes del cierre del flujo de importación revisable. `tests/test_ux44_referencia_pdf.py` añade nueve regresiones y se amplía la cobertura del detalle salarial:

1. el parser extrae una referencia femenina sintética con monto, cuotas, edad, sistema y filas anuales;
2. un segundo caso con valores diferentes demuestra que el importador no depende de un monto único;
3. un documento ajeno al formato esperado se rechaza;
4. el contrato de salida no contiene el código único del documento; UX.4.6b permite identificadores opcionales únicamente cuando aparecen etiquetados y los protege con revisión explícita;
5. el endpoint rechaza archivos que no sean PDF;
6. la interfaz ofrece carga PDF opcional y declara que no existe un monto predeterminado;
7. la comparación usa el monto extraído, el resultado actual, sistema y edad para decidir si puede calcular una diferencia;
8. código de producción del importador y la comparación no contiene hardcodeados los montos de los comprobantes de validación;
9. `pypdf` queda versionado y el botón **Abrir Mi Caja Digital** se centra dentro de su bloque.

Además, el detalle salarial comprueba `promedio_por_cuota_acreditada`; para una fotografía con B/.6,659.50 y cinco cuotas el valor esperado es B/.1,331.90.

En validación manual se deben probar al menos dos comprobantes personales distintos fuera del repositorio. Se confirma que el PDF femenino y el masculino usados durante el desarrollo son reconocidos dinámicamente, pero esos archivos y sus identificadores personales no se versionan. También se verifica que una edad o sistema distinto muestre la referencia sin calcular una diferencia engañosa.


## Validación UX.4.4 — importación revisable y Ficha Digital

La suite alcanza **161 pruebas automatizadas**. `tests/test_ux44_importacion_oficial.py` reúne catorce regresiones que verifican:

1. extracción sintética únicamente de los salarios del año calendario actual y detección del período más reciente;
2. rechazo de texto que no contiene la sección esperada;
3. rechazo del endpoint cuando el archivo no es PDF;
4. ubicación de ambos importadores en el Paso 1 y retiro de la carga de comprobante del Paso 3;
5. presencia de dos vistas previas modales editables y confirmación explícita;
6. prellenado confirmado de persona, cuotas, historial seleccionado y referencia del comprobante;
7. exclusión por defecto de filas proyectadas del historial real;
8. ausencia de inferencia automática de cuotas desde salarios de Ficha Digital y aplicación mensual solo al año actual;
9. corrección visual del `input[type=file]` y soporte de temas/alto contraste en los modales;
10. carga del módulo de importación y disponibilidad del endpoint `/api/simulacion/ficha-digital`;
11. descarte de períodos de años anteriores en el contrato de Ficha Digital;
12. error explícito cuando el documento no contiene salarios del año calendario actual;
13. formato monetario de miles y dos decimales en comprobante y Ficha Digital;
14. eliminación de columnas redundantes de año/aplicación en la vista previa de Ficha Digital.

La validación manual de cierre de UX.4.4 debe comprobar en PC/laptop:

- analizar un comprobante sin que cambie ningún campo antes de confirmar;
- editar al menos un valor en la vista previa y confirmar que ese valor corregido pase al asistente;
- comprobar que filas `Proyectado` no estén marcadas para historial real por defecto;
- cancelar una segunda importación y verificar que el estado anterior permanezca intacto;
- importar una Ficha Digital digital, corregir el último mes a `Parcial` cuando corresponda y marcar solo cuotas realmente acreditadas;
- confirmar que la vista previa de Ficha Digital muestre únicamente los salarios del año actual y que no aparezcan períodos de años anteriores;
- confirmar que salarios y monto de referencia se muestren con coma de miles y dos decimales;
- revisar Claro, Oscuro y Alto contraste, incluido el selector de archivo sin hueco inferior;
- volver a ejecutar un caso SEBD completo y luego un documento deliberadamente incompatible para confirmar la comparación `No comparable`.

Los documentos personales reales permanecen fuera del repositorio.


## Validación UX.4.5 — información acreditada, proyección y cierre accesible

La suite alcanza **170 pruebas automatizadas**. `tests/test_ux45_cierre_resultados_accesibilidad.py` añade nueve regresiones específicas:

1. la fotografía SEBD `SOLO_ACREDITADO` del caso controlado conserva 281 cuotas, salario base B/.1,163.28 y pensión B/.741.59 sin períodos futuros;
2. el mismo escenario en `PROYECTADO`, con cinco cuotas futuras y B/.1,500 mensuales, conserva B/.769.42;
3. el frontend solicita una segunda evaluación acreditada para SEBD, Mixto y SUCGS;
4. `sessionStorage` mantiene resultados acreditados separados y los invalida con sus dependencias;
5. la comparación acreditada/proyectada existe sin depender de un PDF;
6. la tabla incluye caption y encabezados programáticos de fila/columna;
7. la referencia PDF prefiere la fotografía acreditada propia;
8. los modales de importación conservan títulos y cierres accesibles;
9. la comparación utiliza estilos compatibles con Alto contraste y números tabulares.

La validación manual obligatoria de UX.4.5 se realiza en PC/laptop y debe comprobar: cálculo SEBD con ambas fotografías, un caso Mixto y uno SUCGS, navegación por teclado, reapertura de resultados guardados y temas Claro/Oscuro/Alto contraste. Si se dispone de un teléfono Android, puede añadirse una prueba real por red local. Tablet Android, iPhone/iPad, macOS y pantallas muy grandes quedan diferidos para la ronda beta/RC; su ausencia no bloquea el cierre mientras las regresiones responsive permanezcan en verde y no exista una incidencia conocida.


## Validación pre-beta — E2E y hardening

La suite alcanza **185 pruebas automatizadas**. `tests/test_prebeta_e2e_hardening.py` añade 15 regresiones centradas en la frontera real de la API:

- SEBD acreditado B/.741.59 y proyección B/.769.42 por endpoint integrado;
- Mixto controlado B/.856.25 por endpoint integrado;
- SUCGS controlado B/.600.00 por endpoint integrado;
- cabeceras defensivas en HTML;
- rechazo de extensión falsa, MIME incompatible, archivo vacío y contenido sin firma PDF;
- rechazo por exceso de tamaño antes de parsear;
- distinción entre un PDF estructuralmente válido pero ajeno y un archivo que ni siquiera es PDF;
- conservación del límite de páginas;
- `Cache-Control: no-store` en importaciones.

La validación local del entorno de desarrollo incluye `compileall` y `node --check` sobre todos los JavaScript. La instalación realmente limpia y `pip check` quedan además automatizados en `.github/workflows/ci.yml`; su resultado remoto debe verificarse después de commitear/pushear el workflow.


## Validación pre-beta — ajuste CI/Dependabot

La primera ejecución remota del workflow de `main` se completó correctamente en Python 3.13 y 3.14. Las ejecuciones rojas posteriores correspondieron a PR automáticos de Dependabot y permitieron identificar dos falsos negativos de las regresiones: el test de CI exigía literalmente `actions/setup-node@v6` y el test de PDF exigía `pypdf==5.9.0`, aunque los pasos previos y las regresiones funcionales de esos PR habían avanzado correctamente.

La corrección mantiene **185 pruebas automatizadas** y cambia el criterio de esas regresiones:

- `checkout`, `setup-python` y `setup-node` deben existir con un major explícito, pero el major no se congela en el test;
- el workflow continúa obligado a cubrir Python 3.13/3.14, Node.js 24, `pip check`, `compileall`, `node --check` y la suite;
- `pypdf` debe aparecer exactamente una vez con pin `X.Y.Z`; la compatibilidad la determinan los tests de ambos importadores;
- Dependabot solo vigila de forma ordinaria las dependencias directas declaradas por el proyecto, agrupa minor/patch compatibles del runtime y agrupa GitHub Actions;
- `pypdf` y actualizaciones major permanecen bajo revisión individual;
- no se configura auto-merge.

Después de aplicar este bloque, la validación local debe repetir `compileall`, `node --check` para todos los JavaScript, suite completa y `git diff --check`. Tras el siguiente `push`, el workflow de `main` debe permanecer verde; los PR existentes de Dependabot que ya no correspondan a la estrategia nueva pueden cerrarse o dejar que Dependabot los reevalúe, sin fusionarlos mientras estén rojos.

## Validación UX.4.6a — rediseño visual integral

El cierre de UX.4.6a deja la suite en **198 pruebas automatizadas, todas en `OK`**. `tests/test_ux46a_redisenio_integral.py` aporta trece regresiones específicas:

1. orden de carga `style.css` → `design-system.css` → `accesibilidad.css`;
2. navegación pública abreviada;
3. Alto contraste conservado como opción secundaria de Accesibilidad;
4. actualización del estado del control de apariencia;
5. footer legal sin duplicar Mi Caja Digital;
6. Inicio orientado a beneficios y mockup sin resultado ficticio;
7. tokens principales del tema Claro;
8. tokens principales del tema Oscuro;
9. lenguaje visual común para controles y tarjetas;
10. adaptación explícita de los componentes nuevos a Alto contraste;
11. escala/interlineado final del hero y centrado de los seis pasos;
12. continuidad visual entre el proceso guiado y **Estimación orientativa**;
13. footer final centrado con versión y acceso a Fuentes oficiales.

Las regresiones históricas de identidad, temas y estabilización visual se actualizaron para comprobar el nuevo contrato sin conservar selectores o clases retiradas.

### Cierre manual en PC/laptop

La revisión manual inmediata fue aceptada después del remate final. Se verificaron:

- hero de Inicio con escala e interlineado corregidos;
- centrado del número y texto de los seis pasos;
- continuidad de superficie en el bloque **Estimación orientativa**;
- footer centrado con versión, Fuentes oficiales y copyright;
- menú de apariencia con Claro, Oscuro y Alto contraste;
- conservación del comportamiento general del asistente y páginas internas.

La ejecución de cierre confirmó:

```text
python -m compileall app
# OK

node --check app/static/js/*.js
# OK

python -m unittest discover -s tests -v
Ran 198 tests
OK

git diff --check
# sin salida
```

La validación específica en móvil, tablet, macOS y pantallas grandes permanece diferida para la matriz beta/RC y no bloquea este cierre.



## Validación UX.4.6b — Simular / Paso 1 · Datos personales

La Revisión 2 deja la suite en **223 pruebas automatizadas en `OK`**. Las regresiones específicas cubren:

1. modalidad manual predeterminada y alternativa PDF;
2. siete campos opcionales de identificación;
3. asterisco y semántica accesible de fecha de nacimiento, sexo y sistema;
4. apellido de casada condicionado a sexo femenino;
5. exclusión visual mutua entre captura manual e importación;
6. traslado de Ficha Digital al Paso 3;
7. barra común después de los paneles y con `position: static`;
8. ausencia de acciones duplicadas dentro del formulario del Paso 1;
9. cargador PDF compacto y acción de análisis condicionada a archivo;
10. vista previa bloqueada, edición explícita y bloqueo de importación durante edición;
11. continuidad bloqueada cuando faltan datos previsionales obligatorios;
12. extracción de identificadores explícitos;
13. descomposición conservadora de nombre completo y patrón femenino `de Apellido`;
14. trazabilidad del origen manual/importado/editado;
15. consentimiento versionado antes de la captura y retorno a Inicio al rechazar;
16. ausencia de cookies/analítica/rastreadores en el contrato actual y separación entre `sessionStorage`/`localStorage`;
17. `Cache-Control: no-store` en la API de simulación, CSP y SRI;
18. hover transversal de tablas y icono contextual `i` reposicionable;
19. sección pública de privacidad y fuentes oficiales;
20. permanencia de la importación de Ficha Digital en Paso 3.

Las regresiones históricas de UX.3, UX.4.1, UX.4.4 y UX.4.5 se actualizan al nuevo contrato sin eliminar sus garantías de responsive, validación accesible, importación revisable y separación acreditado/proyectado.

### Validación manual de cierre — completada

UX.4.6b fue revisada y aprobada en PC/laptop antes de sus commits de cierre. La lista utilizada fue:

- primera entrada a **Simular**: modal de privacidad visible antes de capturar datos;
- **No acepto** vuelve a Inicio y **Aceptar y continuar** habilita el flujo;
- reapertura/versión del consentimiento sin perder coherencia;
- selección Manual/PDF y cambio entre modalidades;
- asteriscos de campos obligatorios y borde/mensaje/foco al intentar continuar vacíos;
- apellido de casada para Femenino y ocultación para Masculino;
- cargador PDF compacto y botón **Analizar documento** alineado;
- comprobante con `Anabel Estela Miranda Madrid de Cañizares`: revisión de nombres, apellidos y apellido de casada;
- vista previa inicialmente bloqueada, **Editar campos**, **Finalizar edición** e **Importar datos**;
- ausencia de leyendas redundantes retiradas;
- hover de filas suficientemente perceptible;
- ayuda mediante icono `i` de Sistema previsional sin recorte cerca del footer/viewport;
- fila de NSS alineada sin espacio vertical excesivo;
- barra al final del Paso 1 sin superposición;
- Ficha Digital únicamente en Paso 3;
- sección de Privacidad en Fuentes;
- Claro, Oscuro y Alto contraste.

La matriz móvil/tablet/macOS/pantallas grandes continúa diferida para beta/RC.


### Validación adicional UX.4.6b Revisión 3

Comprobar en PC/laptop:

1. el modal de términos contiene los apartados de objeto, responsable, marco legal, datos, finalidad, consentimiento, custodia, terceros, cookies, derechos, resultados, incidentes y cambios;
2. la casilla **He leído y acepto...** inicia deshabilitada y solo se habilita al llegar al final del texto;
3. **Aceptar y continuar** no puede activarse sin lectura completada y casilla marcada;
4. los textos visibles no contienen `sessionStorage` ni `localStorage`;
5. la barra superior e inferior tienen el mismo ancho que las tarjetas del asistente y muestran el mismo paso/acción;
6. la barra superior permanece accesible en escritorio durante pasos largos sin invadir el ancho del contenido;
7. la ayuda contextual de Sistema previsional no queda recortada por tarjeta, navegación o footer.

La validación técnica de UX.4.6b Revisión 3 ejecutó **232 pruebas automatizadas en OK**, además de `compileall` y validación de sintaxis JavaScript.


### Validación adicional UX.4.6b Revisión 4

Comprobar en PC/laptop:

1. la casilla **He leído y acepto...** continúa deshabilitada hasta alcanzar el final del documento;
2. al llegar al final se habilita la casilla sin mostrar un bloque **Fin de los términos**;
3. no aparece el mensaje **Lectura completada. Marca la casilla para aceptar y continuar.**;
4. antes de alcanzar el final, la ayuda de desplazamiento explica por qué la casilla está deshabilitada y desaparece al cumplirse el requisito;
5. las plantillas públicas no posicionan Mi Retiro Proyectado como aplicación educativa, didáctica o pedagógica;
6. navegación superior/inferior, términos, Manual/PDF, campos obligatorios y ayuda mediante icono `i` conservan el comportamiento validado en R3.

La validación técnica de UX.4.6b Revisión 4 ejecutó **233 pruebas automatizadas en OK**, además de `compileall`, validación de sintaxis JavaScript y revisión de espacios finales.


## Validación UX.4.6c — Simular / Paso 2 · Cuotas

### Regresiones automatizadas

La Revisión 3 amplía `tests/test_ux46c_cuotas.py` con cobertura de filtrado por paso, rotulado de secciones, cuotas del año actual y eliminación del doble círculo visual. La suite completa debe finalizar con **253 pruebas automatizadas en OK**.

Se protege que:

1. el Paso 2 separe cuotas acreditadas y cotización futura;
2. los campos obligatorios mantengan indicador y validación accesible;
3. `cuotas_totales` y `cuotas_anio_actual` se bloqueen solo si fueron detectados y confirmados desde Mi Retiro Seguro;
4. un dato ausente en el PDF permanezca editable y muestre que debe completarse manualmente;
5. la procedencia se conserve por campo en `origen_campos_cuotas`;
6. quitar la importación elimine las marcas de origen;
7. la corrección de datos importados vuelva a la vista previa documental;
8. no existan acciones duplicadas dentro del Paso 2;
9. la navegación común continúe al Paso 3 sin depender de un botón duplicado;
10. la obligatoriedad de las cuotas futuras se desactive cuando no se continuará cotizando;
11. el resumen use lenguaje orientado al usuario;
12. el selector de apariencia use iconos SVG semánticos;
13. los estados importado/faltante tengan estilos diferenciados;
14. el modal de importación se desacople de paneles ocultos antes de abrirse;
15. la leyenda visible sea exactamente `* Campo obligatorio`;
16. los campos editables tengan pistas breves que desaparezcan al existir un valor;
17. las ayudas contextuales no muestren la palabra visible `Info`.

### Revisión manual PC/laptop pendiente

La validación visual de cierre de UX.4.6c en PC/laptop comprobó en Claro, Oscuro y Alto contraste:

- PDF con ambos campos de cuotas detectados: ambos deben quedar protegidos;
- PDF con solo uno de los dos campos: únicamente el detectado debe quedar protegido y el faltante debe poder completarse;
- captura completamente manual: ambos campos deben permanecer editables;
- **Revisar importación** debe abrir nuevamente la vista previa del comprobante sin dejar únicamente el fondo oscurecido;
- `¿Continuarás cotizando? = No` debe desactivar cuotas futuras y retirar sus asteriscos dinámicos;
- las barras superior e inferior deben mostrar la misma acción y el mismo estado;
- después de analizar, la acción principal debe cambiar de **Analizar cuotas** a **Continuar al historial**;
- los iconos Sistema/Claro/Oscuro/Contraste deben coincidir con la apariencia seleccionada.

### Comprobaciones específicas de Revisión 3

- Desde Paso 1, **Revisar importación** muestra todos los grupos del comprobante.
- Desde Paso 2, la misma acción muestra únicamente **Cuotas acreditadas (Paso 2)**.
- El bloque del Paso 2 contiene total de cuotas y cuotas acreditadas del año actual.
- Los encabezados de la vista previa identifican el paso de destino de cada grupo.
- El icono de ayuda muestra una sola circunferencia visual y conserva foco/hover/teclado.


### Cierre confirmado de UX.4.6c

- Revisión visual PC/laptop: **completada**.
- Suite completa: **253 pruebas automatizadas en OK**.
- `git diff --check`: debe permanecer sin incidencias antes del commit.
- Revisión manual móvil/tablet/pantallas grandes: diferida para beta/RC.

## Validación UX.4.6d — Simular / Paso 3 · Historial

La Revisión 1 agregó `tests/test_ux46d_historial.py` con **20 regresiones específicas**. La Revisión 2 añadió cinco regresiones para la coherencia entre Ficha Digital, cuotas del Paso 2, detalle del año actual, alineación y salario pendiente. La Revisión 3 agregó cobertura para casillas importadas bloqueadas, clasificación automática del comprobante y diferenciación visual entre filas importadas/manuales. La Revisión 4 incorpora paleta primaria para procedencia. La Revisión 5 endurece la marca visible y la lectura semántica de casillas documentales, incluyendo compatibilidad con estados restaurados de revisiones anteriores. La suite completa alcanza **290 pruebas automatizadas en OK**. La validación visual completa debe repetirse antes del cierre.

Cobertura específica:

1. título y tres secciones internas del Paso 3;
2. ausencia del `Paso 3 de 6` redundante dentro de la tarjeta;
3. eliminación de acciones primarias internas duplicadas;
4. acción unificada `analizarPasoHistorialCompleto`;
5. cambio de navegación a `Continuar a proyección` solo cuando el paso está completo;
6. eliminación de `Completar cuotas vacías con 12`;
7. período histórico regenerado desde el año inicial sin botón manual;
8. filtros Todos/Pendientes y estados de fila;
9. placeholders y nombre `Salario anual reportado`;
10. bloqueo por campo del historial importado;
11. revisión contextual de Mi Retiro Seguro desde Paso 3;
12. cargador simétrico de Ficha Digital;
13. ausencia de textos técnicos de almacenamiento en el formulario;
14. vista previa Ficha en modo revisión y edición explícita;
15. procedencia por mes/campo en el detalle del año actual;
16. concentración de `Abrir Mi Caja Digital` en el importador;
17. base manual obligatoria frente a base automática de solo lectura;
18. resumen unificado del Paso 3;
19. eliminación transversal de paneles `Próximo paso...`;
20. estilos diferenciados para campos importados, hover y resumen.

### Revisión manual pendiente de UX.4.6d R2

En PC/laptop se debe comprobar, como mínimo:

- historial totalmente importado, parcialmente importado y completamente manual;

- importar una Ficha Digital sin marcar cuotas mensuales y verificar que el total del Paso 2 no cambie;
- comprobar que quitar la Ficha tampoco elimina la procedencia de las cuotas del Paso 2;
- verificar el aviso cuando las cuotas mensuales identificadas no coinciden con Paso 2;
- alternar Sí/No en detalle del año actual y confirmar que la Ficha queda inactiva de forma explícita cuando se usa total anual;
- comprobar que un salario anual actual pendiente se muestre vacío y no `0.00`;
- confirmar la alineación superior de los dos selectores del detalle;
- filtro **Pendientes** en una tabla larga;
- edición de año inicial y actualización automática del período;
- apertura de **Revisar importación** mostrando solo Historial anual detectado;
- Ficha Digital: selección, análisis, modo revisión, edición voluntaria e importación;
- meses importados bloqueados y meses ausentes editables;
- coincidencia/no coincidencia de cuotas del año actual;
- base salarial manual y las cuatro bases automáticas cuando existan datos suficientes;
- una sola acción principal en las barras superior/inferior;
- resumen final y avance al Paso 4;
- Claro, Oscuro y Alto contraste.

La validación móvil/tablet/pantallas grandes continúa diferida para beta/RC.

### Validación específica UX.4.6d Revisión 3

1. Importar una Ficha Digital con enero–mayo y comprobar que esas cinco filas aparecen visualmente diferenciadas.
2. Confirmar que las cinco casillas **Cuota acreditada** están marcadas y no pueden desmarcarse ni en revisión ni en el detalle principal.
3. Confirmar que junio–agosto, cuando no estén en el PDF, permanecen con casilla editable y campos disponibles.
4. Verificar que el total de cuotas del Paso 2 no cambia por confirmar o quitar la Ficha Digital.
5. Si el número de meses importados difiere del Paso 2, verificar la advertencia de coherencia.
6. En Mi Retiro Seguro, comprobar que las filas `HISTORICO` aparecen seleccionadas para historial real y la casilla no es editable; cambiar la clasificación mediante **Editar campos** debe actualizar el estado automáticamente.
7. Verificar la diferenciación visual de filas importadas/manuales en Claro, Oscuro y Alto contraste.
8. Repetir la matriz funcional de R2 completa antes de aceptar la revisión.


### Validación específica UX.4.6d Revisión 4

1. Verificar que las filas importadas usen una señal azul/primaria en Claro y Oscuro, sin fondos verdes de procedencia.
2. Verificar que Alto contraste mantenga la misma semántica con fondo seleccionado y contorno de alto contraste.
3. Importar Ficha Digital con meses detectados y comprobar que sus casillas de cuota aparezcan marcadas y bloqueadas.
4. Confirmar que el gancho siga visible cuando la casilla está deshabilitada.
5. Confirmar que meses no importados conserven casilla manual editable.
6. Repetir después de recargar/restaurar la simulación para comprobar persistencia del estado.
7. Repetir la matriz completa de 24 puntos de UX.4.6d antes del cierre.

### Validación específica UX.4.6d Revisión 5

1. Importar una Ficha Digital con meses detectados y comprobar que cada fila importada muestra **Cuota acreditada** con gancho visible.
2. Confirmar que esas casillas no pueden desmarcarse en el detalle principal ni en la vista previa.
3. Confirmar que los meses no importados mantienen checkbox vacío y editable.
4. Recargar/restaurar una simulación creada en revisiones anteriores y verificar que los meses documentales recuperan igualmente la marca.
5. Repetir la comprobación en Claro, Oscuro y Alto contraste.
6. Después de este control visual, repetir la matriz funcional completa de UX.4.6d antes del cierre.

### Validación específica UX.4.6d Revisión 6

1. Con datos en Paso 3, **Limpiar este paso** debe conservar Pasos 1–2, borrar historial/Ficha Digital/detalle/base salarial y bloquear nuevamente Pasos 4–6.
2. Limpiar Paso 2 debe conservar Paso 1 y borrar Paso 2–6.
3. Limpiar Paso 6 debe conservar Pasos 1–5 y eliminar únicamente configuraciones/resultados.
4. **Reiniciar simulación** debe volver a Paso 1 vacío conservando el tema y sin volver a pedir términos dentro de la misma aceptación vigente.
5. **Borrar datos de esta aplicación en este navegador** desde Fuentes/Privacidad debe volver a Inicio y provocar que el siguiente ingreso a Simular solicite nuevamente términos y utilice el tema predeterminado/sistema.
6. Confirmar que la barra inferior no contiene acciones destructivas.
7. Confirmar que términos versión 2026-08-15.1 describen los tres niveles de eliminación.
8. Después de validar estos controles, repetir la matriz funcional completa de UX.4.6d desde una simulación limpia.

### Validación específica UX.4.6d Revisión 7

Hallazgos de R6:

1. Primera entrada a Simular mostró correctamente los términos vigentes.
2. Limpiar Paso 3 conservó Pasos 1–2 e invalidó posteriores.
3. Reiniciar simulación volvió a Paso 1 vacío sin repetir términos y conservó tema.
4. Borrado local desde Fuentes volvió a Inicio y provocó nuevo consentimiento/tema predeterminado al regresar a Simular.
5. Se aclaró que el menú **Opciones** visible durante scroll corresponde a la barra sticky superior; la barra inferior no debe contenerlo.
6. Se detectó que **Revisar términos de privacidad** navegaba a Simular y exigía aceptar de nuevo.

Validar R7:

1. Desde Fuentes, **Revisar términos de privacidad** debe abrir el modal sin cambiar de URL/página.
2. La consulta debe ocultar checkbox, **No acepto** y **Aceptar y continuar**.
3. Cerrar con `×` debe volver exactamente a Fuentes sin modificar consentimiento.
4. Entrar de nuevo a Simular después de esa consulta no debe pedir términos nuevamente si la aceptación sigue vigente.
5. En un consentimiento realmente requerido, `×` debe volver a Inicio y no permitir acceso al formulario sin aceptar.
6. En Fuentes debe mostrarse **Repositorio: GitHub del proyecto**.
7. Confirmar que solo la barra sticky superior posee **Opciones**; la inferior no lo renderiza.
8. Después, repetir la matriz funcional completa de UX.4.6d desde una simulación limpia.
Resultado técnico de R7: **311 pruebas automatizadas en OK**, compilación Python y validación sintáctica JavaScript correctas.

### Validación específica UX.4.6d Revisión 8

R8 se origina durante la ejecución manual de los puntos 1–19 de la matriz. Se confirmaron los flujos principales y se detectaron cuatro refinamientos: estado visual estático, resumen anual poco visible, scroll innecesario con una sola fila y desalineación de la advertencia del último mes. También se solicita distinguir visualmente el botón **Seleccionar archivo** en todos los cargadores.

Antes de continuar con los puntos 20–30 se debe revalidar:

1. con `12` cuotas y salario vacío, la fila cambia de `Pendiente` a **Falta salario**;
2. al completar el salario, 12 cuotas pasan a **Completo** y 1–11 cuotas a **Parcial**;
3. el filtro **Pendientes** muestra solo filas que requieren acción y una sola fila no presenta scroll vertical innecesario;
4. un historial `12 + 12 + 5` con salarios `12,000.00 + 14,400.00 + 7,321.13` muestra inmediatamente `29`, `29`, `0` y `B/.33,721.13`;
5. **Seleccionar archivo** usa el nuevo tratamiento visual en Claro, Oscuro y Alto contraste;
6. el último mes de la vista previa de Ficha Digital permanece alineado con las demás filas al entrar en **Editar campos**.

Después de este retesteo deben ejecutarse los puntos 20–30 y los refinamientos ya reservados para la revisión final (consentimiento desde Fuentes cuando aún no existe aceptación, tecla `Esc` y placeholders genéricos).

Resultado técnico de R8: **317 pruebas automatizadas en OK**, compilación Python y validación sintáctica JavaScript correctas.

### Validación específica UX.4.6d Revisión 9

R9 se origina porque R8 todavía mostraba dos problemas durante la prueba manual: la pista vertical de scroll seguía visible con una sola fila y el estado/filtro no reaccionaban mientras se escribía. También se incorporan los refinamientos de privacidad y placeholders que estaban reservados para el cierre.

Retestar antes de continuar con el punto 20:

1. Con cuotas vacías y salario vacío: **Pendiente**.
2. Escribir primero cuotas positivas: **Falta salario**; completar salario: **Parcial** o **Completo** según cuotas.
3. Escribir primero salario positivo: **Faltan cuotas**; completar cuotas: estado final correspondiente.
4. Con filtro **Pendientes** activo, una fila debe desaparecer en el mismo instante en que deja de requerir acción y el contador debe disminuir.
5. Con una sola fila visible no deben aparecer flechas, thumb ni carril vertical de scroll.
6. Desde Fuentes sin consentimiento vigente, revisar términos debe mostrar el flujo de aceptación; después de aceptar, Simular no debe volver a pedirlo.
7. `Esc` en Fuentes/consulta cierra el modal; `Esc` en el consentimiento obligatorio de Simular no permite entrar al formulario sin aceptar.
8. Verificar que los placeholders de nombres, apellidos, cédula y NSS sean genéricos.

Después de este retesteo continúan pendientes los puntos 20–30 de la matriz de UX.4.6d.

### Validación específica UX.4.6d Revisión 10

R10 no cambia motores ni fórmulas. Su objetivo es convertir la geometría tabular en un contrato transversal y asegurar que los patrones previos se reutilicen únicamente cuando su semántica corresponda.

Antes de continuar con los puntos 20–30:

1. verificar que **Historial salarial anual** tenga esquinas redondeadas simétricas en Claro, Oscuro y Alto contraste;
2. verificar que encabezado, borde y superficie pertenezcan a la paleta del tema sin cambiar los colores semánticos de `Completo`, `Parcial`, advertencias o procedencia documental;
3. revisar la tabla mensual de Ficha Digital y su vista previa: deben conservar la misma geometría redondeada;
4. revisar al menos una tabla de un paso posterior o comparador para confirmar que `app-table-shell` no rompe scroll horizontal;
5. con una tabla horizontalmente desplazable, confirmar que el contenedor recibe foco accesible; sin desbordamiento no debe añadirse tabulación innecesaria;
6. confirmar que los comportamientos ya aprobados de R9 (estados reactivos, filtro Pendientes y ausencia de carril vertical corto) permanecen intactos.

La prueba de consentimiento pendiente desde Fuentes se realizará durante el recorrido limpio Pasos 1–3. Después se ejecutan los puntos 20–30.

Resultado técnico R10: **330 pruebas automatizadas en OK**; `compileall` y `node --check` correctos.



### Validación específica UX.4.6d Revisión 11

R11 no modifica motores, fórmulas, estados tabulares ni procedencia documental. Antes de continuar con los puntos 20–30 validar:

1. en Historial anual, detalle mensual y ambas vistas previas de importación, un scrollbar vertical necesario no debe mostrar flechas superior/inferior ni atravesar las esquinas redondeadas;
2. una tabla corta debe continuar sin carril vertical;
3. el thumb debe conservar contraste adecuado en Claro, Oscuro y Alto contraste;
4. el scroll horizontal, cuando exista, debe mantener el mismo criterio en las esquinas inferiores;
5. **Seleccionar archivo** y **Analizar documento** deben tener exactamente la misma altura exterior en Mi Retiro Seguro y Ficha Digital;
6. el nuevo estilo no debe alterar los ganchos importados, los bloqueos ni la alineación de celdas.

Resultado técnico R11: **335 pruebas automatizadas en OK**; `compileall` y `node --check` correctos.

### Validación específica UX.4.6d Revisión 12

R12 no modifica motores, fórmulas, cuotas ni salarios. Validar en PC/laptop:

1. Historial anual, Ficha Digital y vistas previas con suficientes filas: el thumb debe respetar el borde y no deben aparecer botones/flechas nativos visibles.
2. Abrir Términos y una vista previa: el scrollbar debe usar el mismo lenguaje temático que las tablas.
3. Repetir Claro, Oscuro y Alto contraste verificando contraste del thumb y dimensiones estables.
4. Activar **Pendientes** con cero filas: la tabla y los encabezados deben ocultarse y aparecer `No hay años pendientes por completar.`
5. En un selector PDF, mover el puntero por **Seleccionar archivo** y por el nombre del archivo: el botón no debe regresar al estilo anterior por hover del contenedor.
6. Verificar Comparador solo a nivel visual/scroll cuando esté disponible, sin adelantar la validación funcional de su fase.

Resultado técnico R12: **340 pruebas automatizadas en OK**; `compileall` y `node --check` correctos. Después de esta validación continúan los puntos 20–30 y el recorrido integral pendiente.


### Validación específica UX.4.6d Revisión 13

R12 quedó validada manualmente en scrollbars, estados vacíos, temas y Comparador a nivel visual; el único fallo persistente fue el cambio de color de **Seleccionar archivo** al pasar por el nombre del archivo. R13 corrige exclusivamente esa cascada visual.

Validar antes del recorrido integral:

1. en Mi Retiro Seguro y Ficha Digital, mover el puntero por el botón, por el nombre del archivo y fuera del control; la paleta del botón no debe regresar al estilo Bootstrap;
2. repetir Claro, Oscuro y Alto contraste;
3. comprobar foco por teclado y selección de archivo sin pérdida de contraste;
4. confirmar que **Analizar documento** conserva la altura ya validada.

Después ejecutar un recorrido limpio completo de Pasos 1–3: consentimiento desde Fuentes y Simular, captura manual/importada, Cuotas, Historial anual, Ficha Digital, detalle mensual/quincenal, bases salariales, limpieza/reinicio, persistencia temporal, errores y resúmenes. Los puntos 20–30 de la matriz original quedan integrados dentro de ese recorrido.

Resultado técnico R13: **343 pruebas automatizadas en OK**; `compileall` y `node --check` correctos.


### Validación específica UX.4.6d Revisión 14

R13 quedó validada manualmente en Mi Retiro Seguro/Ficha Digital y en Claro, Oscuro y Alto contraste. R14 reorganiza únicamente el Paso 1 manual para continuar la certificación integral.

Validar al iniciar el siguiente bloque:

1. existe un único encabezado **Información personal** en la captura manual; no aparecen `Identificación personal` ni `Información previsional básica` como secciones separadas;
2. Primer/Segundo nombre y Primer/Segundo apellido permanecen opcionales;
3. al seleccionar **Femenino**, **Apellido de casada** aparece inmediatamente junto a Sexo; al seleccionar Masculino vuelve a ocultarse y limpiarse;
4. Fecha de nacimiento, Sexo y Sistema previsional conservan `*` y validación obligatoria;
5. Cédula, NSS y Fecha de ingreso CSS continúan opcionales;
6. cambiar a importación PDF y confirmar datos conserva el mismo contrato de bloqueo/procedencia previo;
7. Claro, Oscuro y Alto contraste mantienen alineación y espaciado sin cambios funcionales.

Resultado técnico esperado R14: **346 pruebas automatizadas en OK**; `compileall` y `node --check` correctos. Después de validar este bloque continúa el recorrido funcional completo del Paso 1 y posteriormente Pasos 2–3.

## UX.4.6d R15 — campos bloqueados, importación y limpieza Paso 2

Validar antes de continuar el recorrido:

1. en Paso 1 importado, comparar un campo bloqueado con uno editable en Claro, Oscuro y Alto contraste; deben distinguirse por superficie/borde y señal lateral;
2. confirmar **Importar desde Mi Retiro Seguro**, **Importar información desde Mi Retiro Seguro** y **Selecciona el documento**, sin “PDF compatible” en encabezados/ayudas principales;
3. confirmar la misma terminología de selección en Ficha Digital;
4. en Paso 2 con datos, usar **Limpiar este paso** y verificar que `¿Continuarás cotizando?` regrese a `Selecciona una opción` y ambos campos de cuotas futuras queden vacíos/deshabilitados; si Paso 1 conserva un comprobante importado, los campos de cuotas que fueron limpiados no deben quedar vacíos y bloqueados por una procedencia reconstruida;
5. elegir Sí y verificar que los campos se habilitan y pueden recibir/sugerir 12; elegir No y verificar la lógica existente de cierre actual/0 futuras;
6. revalidar los tres temas y que Paso 1 importado continúe bloqueando únicamente los datos documentales.

R15 añade cuatro regresiones específicas; después se ejecuta compilación Python, sintaxis JS y suite completa.

Resultado técnico R15: **350 pruebas automatizadas en OK**; `compileall` y `node --check` correctos.

## UX.4.6d R16 — flujo Paso 2 → Paso 3 y jerarquía de Ficha Digital

Validar manualmente:

1. con Paso 2 analizado, importar Ficha Digital y analizar Paso 3 sin navegación hacia atrás;
2. invalidar únicamente `resumen_cuotas` manteniendo los controles de Paso 2 completos: Paso 3 debe revalidar en segundo plano y continuar;
3. dejar realmente incompleto Paso 2 y comprobar que Paso 3 conserva sus datos y muestra una dependencia contextual sin redirección automática;
4. limpiar Paso 2 con una sesión que antes estaba en Paso 3 y recargar: debe abrir el último paso accesible, no restaurar un Paso 3 imposible;
5. confirmar el orden **Historial anual → Detalle del año actual → Ficha Digital → tabla mensual → Base salarial**;
6. importar Ficha Digital y comprobar que la tabla mensual resultante aparece inmediatamente después del bloque de carga/revisión dentro de Detalle;
7. revalidar Claro, Oscuro y Alto contraste sin cambios en bloqueos, checkboxes o scrollbars.

Resultado técnico previo a validación manual R16: **356 pruebas automatizadas en OK**.


### UX.4.6d R17 — auditoría de datos del caso real

Caso documental utilizado para regresión:

- cuotas históricas acreditadas: **281**;
- total acumulado mostrado por el comprobante al incluir proyección: **293**;
- 2026: `HISTORICO_PROYECTADO`, 5 cuotas;
- 2027: `PROYECTADO`, 12 cuotas;
- historial detectado desde 1992 frente a fecha de ingreso CSS 23/07/1997.

Validaciones automatizadas:

- una casilla bloqueada no se pinta marcada salvo `checked=true`;
- 2026/2027 permanecen excluidos por defecto de la selección de historial real;
- el parser emite advertencia por registros previos a la fecha de ingreso sin descartarlos;
- el parser no inventa apellido de casada cuando el documento no lo aporta;
- la vista previa diferencia 281 acreditadas de 293 acumuladas con proyección;
- la revisión distingue campos detectados y campos editados/completados manualmente;
- la advertencia mensual explica salario disponible vs. cuota acreditada.

Resultado de suite tras R17: `python -m unittest discover -s tests -q` → **363 pruebas OK**.

## UX.4.6d R18 — procedencia y persistencia

Validación automatizada: **370 pruebas en OK**.

Pruebas manuales pendientes para cierre:
1. Confirmar en Mi Retiro Seguro los estados Detectado/Editado/Completado manualmente/No detectado y que un dato no detectado siga editable.
2. Confirmar procedencia visible en Paso 2, Historial, Ficha Digital y detalle mensual.
3. Importar ambos documentos, ejecutar F5 y Ctrl+F5 y comprobar que el selector nativo queda vacío pero aparece **Importación vigente**, con Revisar/Quitar importación operativos y sin perder datos.
4. Validar 2026 Histórico + proyectado y 2027 Proyectado sin gancho; contexto 281 frente a 293; advertencia 1992 frente a 23/07/1997.
5. Registrar junio B/.1,562.37 como salario conocido separando la casilla de cuota acreditada; julio sin información; agosto puede registrarse como parcial cuando solo se disponga de una quincena.
6. Completar las pruebas R16 de revalidación silenciosa del Paso 2 y limpiar Paso 2 + recargar.


## UX.4.6d R19 — sincronización del detalle con historial y Paso 2

Validación automatizada: **374 pruebas en OK**.

Caso controlado enero–junio 2026:
- salarios: 1,486.88; 1,555.51; 1,381.01; 1,565.83; 1,331.90; 1,562.37;
- seis casillas acreditadas;
- total disponible/acreditado esperado: **B/.8,883.50**;
- promedio seis meses y promedio por cuota acreditada: **B/.1,480.58**;
- promedio últimos tres completos (abril–junio): **B/.1,486.70**.

Pruebas manuales de cierre R19:
1. Con enero–mayo importados, agregar junio B/.1,562.37 sin marcar cuota: la fila anual permanece en 5 cuotas/B/.7,321.13 y el salario de junio solo aumenta `total_salario_disponible`.
2. Marcar la casilla de junio: la fila 2026 debe cambiar inmediatamente a **6 / B/.8,883.50 / Parcial**.
3. Paso 2 debe actualizarse sin navegación a **6 cuotas este año / 282 totales** y mostrar procedencia de edición; al analizar, su estimación al cierre continúa en 288 si se mantienen 12 esperadas.
4. Analizar Paso 3 debe producir historial con 282 cuotas de referencia/identificadas y diferencia 0; total salarial histórico esperado: **B/.205,164.64**.
5. Desmarcar junio debe revertir la referencia a 5/281 y la fila anual a 5/B/.7,321.13.
6. Marcar una cuota sin salario debe mantener la fila anual en estado de salario pendiente y bloquear el análisis del detalle.
7. Verificar que julio/agosto vacíos no bloquean el Paso 3 mientras no estén marcados como cuota.
8. Repetir F5 con importaciones vigentes y completar finalmente la prueba R16 de Limpiar Paso 2 + recargar.


## UX.4.6d R20 — vigencia de Ficha Digital y resumen visible

Validación automatizada: **379 pruebas en OK**.

Pruebas manuales de cierre:
1. En agosto de 2026, analizar una Ficha Digital cuyo último período sea mayo de 2026: debe aparecer **Revisa la vigencia de la Ficha Digital** antes de la vista previa.
2. Elegir **Continuar con esta ficha**: debe abrir la vista previa normal y permitir importar/completar meses faltantes.
3. Repetir y elegir **Seleccionar una ficha más reciente**: debe cerrar la advertencia y devolver el foco al selector para elegir otro documento.
4. Tras confirmar una ficha desactualizada y ejecutar F5, debe conservarse **Importación vigente** y mostrarse el último período detectado sin exigir volver a adjuntar el archivo.
5. Una ficha con último período dentro de los dos meses anteriores no debe interponer la advertencia de desactualización.
6. Después de validar el detalle del año actual debe aparecer **Resumen del detalle del año actual** con las cifras devueltas por el servicio.
7. Modificar cualquier dato del detalle debe ocultar el resumen anterior hasta volver a validar, evitando cifras obsoletas.
8. Verificar Claro, Oscuro y Alto contraste para modal de vigencia, metadata persistente y tarjetas de resumen.


## UX.4.6d R21 — vigencia mensual y fecha verificable

1. Con fecha actual verificada en agosto de 2026, una Ficha Digital de junio de 2026 debe mostrar **Revisa la vigencia de la Ficha Digital**.
2. Una ficha de julio de 2026 también debe advertir; ya no existe tolerancia de dos meses.
3. Una ficha cuyo último período sea agosto de 2026 puede abrir la vista previa sin advertencia de desactualización.
4. La lógica JavaScript de vigencia no debe contener `new Date()` ni depender del reloj del navegador.
5. Si la consulta externa de fecha falla, debe aparecer un mensaje de fecha no verificada y las opciones para seleccionar otra ficha o continuar.
6. Después de F5, una Ficha Digital persistida debe reconsultar la fecha de referencia y actualizar su indicador de vigencia sin pedir nuevamente el archivo.
7. La suite automatizada debe simular fuentes de fecha; no requiere Internet para pasar.
8. La versión de términos/privacidad visible debe ser **2026-08-16.1** y solicitar nueva aceptación respecto de la versión anterior.

## UX.4.6d R22 — cierre del análisis del Paso 3

Validaciones automatizadas añadidas:
1. La reconciliación de cuotas manuales ocurre antes de construir el payload del detalle.
2. Si cambia la referencia, Paso 2 se revalida en segundo plano sin navegación.
3. `cuotas_coinciden=false` deja un error explícito con ambos conteos y orientación accionable.
4. El resumen visible mantiene las 11 métricas semánticamente distintas.

Prueba manual final:
- con 6 cuotas enero–junio, B/.8,883.50 acreditados y base B/.1,500 mensual, **Analizar historial** debe completar Paso 3; si existe una diferencia real debe mostrar el motivo, nunca solo desplazar al detalle.
- al quedar listo, las barras deben cambiar a **Continuar a proyección** y permitir entrar al Paso 4.

Resultado automatizado R22: `python -m unittest discover -s tests -q` → **392 pruebas OK**; `python -m compileall app` y `node --check app/static/js/*.js` → OK.


## UX.4.6d R23 — Ficha Digital más reciente frente a Paso 2

Validar un escenario donde Mi Retiro Seguro deja `cuotas_anio_actual=5` y una Ficha Digital posterior contiene 6 meses confirmados:

1. confirmar la Ficha Digital; Paso 2 debe actualizarse a 6 cuotas del año y el total acumulado debe conservar las cuotas previas al año vigente (ejemplo 281→282);
2. el resumen de Cuotas debe revalidarse sin abandonar Paso 3;
3. **Analizar historial** no debe volver a producir `6 vs 5`;
4. una ficha con menos cuotas que Paso 2 no debe reducir la referencia automáticamente;
5. después de F5, `cuotas_anio_actual_referencia` debe continuar sincronizada.

Regresiones automatizadas: `test_ux46d_revision23_ficha_actualiza_cuotas.py` más cobertura histórica R22 adaptada al nuevo contrato.
