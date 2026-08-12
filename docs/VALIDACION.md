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
python -m unittest discover -s tests -v
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
