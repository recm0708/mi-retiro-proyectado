# Auditoría UX.4.6i R1 — Cómo se calcula

**Estado:** candidato para validación
**Fecha:** 2026-08-21
**Versión:** `0.0.26-beta`

## Objetivo

Crear una sección pública que explique el procedimiento de SEBD, Mixto y SUCGS con suficiente detalle para comprender el orden de operaciones, sin crear un segundo motor de cálculo.

## Hallazgos de entrada

Antes de esta revisión la aplicación ya disponía de:

- motores Python separados para SEBD, Mixto y SUCGS;
- trazabilidad individual en Paso 6 con dato, regla, fórmula, sustitución y resultado;
- catálogo público de metodología y fuentes oficiales;
- parámetros versionados en `regulations/`;
- documentación técnica de modalidades y limitaciones.

La información estaba distribuida y no existía una página pública única orientada a reproducir el procedimiento.

## Decisiones de R1

1. Se incorpora la ruta pública `/como-se-calcula`.
2. `app/services/como_se_calcula.py` únicamente expone parámetros versionados; no calcula prestaciones.
3. La plantilla explica flujo, variables, modalidades, fórmulas descriptivas, tablas versionadas, ejemplos y limitaciones.
4. La página reutiliza el catálogo de fuentes oficial existente.
5. El Paso 6 enlaza al sistema correspondiente mediante fragmento `#sebd`, `#mixto` o `#sucgs`; no incluye datos personales en la URL.
6. Metodología y fuentes incorpora una entrada visible a la nueva guía.
7. Los ejemplos son ilustrativos y cualquier parámetro hipotético se identifica como no oficial.

## Cobertura funcional

### SEBD

- 240/180 cuotas;
- salario base y mejores años;
- tasa base e incrementos por bloques;
- normal, anticipada, proporcional, proporcional anticipada e indemnización;
- máximos versionados;
- tabla mensual de reducción anticipada;
- ejemplo completo.

### Mixto

- BD + CAP;
- tope y parámetros propios del BD;
- fórmula descriptiva del CAP;
- decisión entre pensión programada/devolución cuando corresponde;
- transición a SUCGS;
- dato actuarial no inferible;
- ejemplo ilustrativo con divisor expresamente hipotético.

### SUCGS

- componente contributivo;
- tabla actuarial por edad;
- capa solidaria;
- PGS/mínimo como referencias versionadas;
- garantía de reemplazo del artículo 197 y condiciones modeladas;
- estabilidad salarial como confirmación explícita;
- ejemplo contributivo completo.

## Límites

R1 no modifica motores ni normativa. Tampoco intenta reproducir un resultado personal fuera del Paso 6. La futura revisión normativa/jurídica REV.1 conserva la responsabilidad de validar el alcance legal antes de la primera versión oficial.

## Validación requerida

Automática:

- ruta y renderizado;
- fuente de parámetros desde `regulations/`;
- ausencia de imports de motores en el servicio explicativo;
- cobertura de los tres sistemas;
- vínculo desde Paso 6 y desde Metodología;
- accesibilidad/estructura responsive básica;
- documentación y trazabilidad.

Manual:

- Claro, Oscuro y Alto contraste;
- escritorio y ancho móvil;
- navegación por anclas;
- legibilidad de fórmulas/tablas desplegables;
- enlace desde un resultado SEBD y, cuando se validen esos sistemas, Mixto/SUCGS.

## R1.2 — hallazgos de validación visual y ajuste

La primera revisión manual confirmó que R1 renderiza la guía y sus tres sistemas, pero detectó cuatro brechas de producto:

1. la página no aparecía como destino propio en la navegación principal y heredaba el estado activo de Fuentes;
2. el flujo general nombraba los Pasos 1–6 sin explicar suficientemente cómo cuotas, salarios, proyección y fecha de retiro se transforman antes del resultado;
3. los importes de la guía no mostraban separador de miles;
4. las tablas desplegables de factores podían usar mejor el ancho disponible.

R1.2 corrige esas cuatro brechas. La explicación del flujo se contrastó con `contribution_projection.py`, `salary_history.py`, `salary_projection.py`, `timeline.py` y `retirement.py`; por ello muestra operaciones que ya ejecuta el producto: cuotas restantes del año, normalización salarial, crecimiento compuesto, prorrateo salarial según cuotas y estimación de cuotas hasta la fecha de retiro.

La tabla SEBD pasa a ocho columnas en escritorio —24 factores en tres filas— y SUCGS a diez columnas —46 factores en cinco filas aproximadas—. Las reglas responsive reducen columnas progresivamente. La capa visual sigue usando tokens semánticos y agrega foco visible para no depender del tema Oscuro observado en las capturas.

R1.2 añade seis regresiones. Gate objetivo acumulado: **832 pruebas**.
## R1.3 — segunda validación visual

La revisión manual detectó que algunas separaciones verticales seguían demasiado cerradas —especialmente título de clasificación frente a tabla, nota final de ejemplos y franja de fuentes— y que una fórmula textual por sí sola no era suficiente para una persona sin familiaridad previsional. También se identificó ambigüedad potencial en siglas como BD y CAP y en conceptos como tasa resultante, saldo CAP, pensión programada CAP, factor actuarial y PGS.

R1.3 mantiene cada fórmula general y añade una sustitución numérica claramente rotulada, incorpora definiciones breves dentro de la sección donde se usa el término y ajusta espaciado mediante tokens del sistema visual. Se añadieron además las expresiones que ya usa el producto para la tasa equivalente de salario futuro conocido y para convertir meses completos en cuotas de una fracción de año.

La recomendación para el asistente Pasos 1–6 es reutilizar posteriormente una capa única de ayuda contextual para términos previsionales, en vez de duplicar glosarios extensos en cada pantalla. Este refinamiento no se aplica todavía al wizard dentro de R1.3.

R1.3 añade ocho regresiones. Gate objetivo acumulado: **840 pruebas**.
## Cierre funcional

La validación manual de R1–R1.4 confirmó la navegación principal, la explicación del recorrido de datos de los Pasos 1–6, los tres sistemas previsionales, las tablas de factores, la terminología definida en contexto, los ejemplos sustituidos y la jerarquía/espaciado de la guía. R1.4 adopta **Ejemplo** como etiqueta breve y uniforme para cada sustitución numérica.

La guía permanece explicativa: no sustituye la trazabilidad personal de Paso 6 ni introduce un segundo motor. La futura reutilización de definiciones dentro del wizard se tratará como ayuda contextual transversal, sin recargar los formularios.

**Gate de cierre:** 841 pruebas, compilación Python, sintaxis JavaScript y `git diff --check` limpios.

**Siguiente bloque:** DEV.2 — Centro de desarrollo.
