# Normativa

Este documento describe **cómo la aplicación interpreta, versiona y aplica** las reglas normativas. Para enlaces oficiales y catálogo de leyes, reglamentos y resoluciones, consultar [FUENTES_NORMATIVAS.md](FUENTES_NORMATIVAS.md).

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Fuente base del proyecto

La fuente legal consolidada es el **Texto Único de la Ley 51 de 2005, Orgánica de la Caja de Seguro Social**, con reformas incorporadas hasta la Ley 462 de 2025, publicado en la **Gaceta Oficial 30284-B de 22 de mayo de 2025**.

Enlaces oficiales:

- [Normativa de la Ley Orgánica — CSS](https://www.css.gob.pa/normativas-ley-organica/)
- [Texto Único de la Ley 51 — PDF CSS](https://www.css.gob.pa/wp-content/uploads/2025/05/TEXTO-UNICO-DE-LA-LEY-51-DE-2005-CSS-GACETA-OFICIAL-22-5-25.pdf)
- [Gaceta Oficial 30284-B — PDF](https://www.gacetaoficial.gob.pa/pdfTemp/30284_B/GacetaNo_30284b_20250522.pdf)

## 2. Regla de implementación normativa

La aplicación distingue entre:

- **regla legal**: proviene de ley o Texto Único;
- **desarrollo reglamentario**: proviene de resolución o reglamento de la CSS;
- **parámetro versionado**: valor almacenado en `normativa/*.json` con fecha y fuente;
- **dato oficial individual**: saldo, bono, divisor o confirmación que debe provenir del Asegurado(a)/CSS y no puede deducirse con seguridad;
- **decisión de implementación**: criterio técnico adoptado cuando hay una ambigüedad o superposición normativa; debe quedar registrado en `docs/DECISIONES.md`.

No se deben ocultar conflictos entre fuentes ni convertir una comunicación operativa temporal en una regla legal permanente.

## 3. Archivos normativos versionados

| Archivo | Alcance |
|---|---|
| `normativa/parametros_generales.json` | Edades de referencia y metadatos generales. |
| `normativa/sebd.json` | Reglas SEBD, factores anticipados, límites e indemnización. |
| `normativa/mixto.json` | Componente BD, CAP, devolución, seguros y transición. |
| `normativa/sucgs.json` | Tabla actuarial, capa solidaria y garantía de reemplazo. |

Los valores sujetos a actualización deben conservar fecha de referencia y no tratarse como constantes eternas.

## 4. Parámetros generales

Actualmente se versionan:

- edad de referencia femenina: **57 años**;
- edad de referencia masculina: **62 años**;
- fuente consolidada y fecha de Gaceta;
- anticipación operativa de solicitud utilizada por la aplicación cuando corresponda.

Los motores usan fechas completas; no se decide elegibilidad únicamente restando años calendario.

## 5. SEBD

### 5.1. Artículos principales

La implementación general se apoya en los artículos **178, 179, 180, 181, 186, 192 y 193**.

Resumen funcional:

- **Arts. 178–179:** condiciones generales y edad de referencia.
- **Art. 180:** salario base sobre los diez mejores años.
- **Art. 181:** modalidades generales, 240 cuotas de referencia, tasa base de 60 %, incrementos por cuotas y factores de anticipación.
- **Art. 186:** Indemnización por Vejez y transición desde 01/03/2036.
- **Art. 192:** monto mínimo sujeto a actualización.
- **Art. 193:** topes máximos y condiciones para límites ampliados.

### 5.2. Salario base y años parciales

El historial actual es anual. Un año parcial no se anualiza artificialmente: conserva el salario efectivamente cotizado y puede competir como año calendario dentro de la selección reglamentaria. Cuando se seleccionan diez años, el total se lleva a promedio mensual sobre 120 meses según el criterio implementado.

Esta limitación se documenta porque el detalle mensual oficial puede producir diferencias en casos irregulares.

### 5.3. Retiro anticipado

`normativa/sebd.json` almacena la tabla mensual de factores de reducción utilizada por el motor. La fuente reglamentaria se mantiene en la sección **Reglamento para el Cálculo de Prestaciones Económicas** de la página oficial de Prestaciones Económicas de la CSS.

- [Normativa de Prestaciones Económicas — CSS](https://www.css.gob.pa/normativa-prestaciones-economicas/)
- [Resolución 39,302-2007-J.D. — CSS](https://w3.css.gob.pa/wp-content/wdocs/Resolucion%20%2039%2C302-2007-J.D..pdf)

### 5.4. Monto mínimo del artículo 192

El valor base B/.265.00 no se aplica automáticamente como si fuera el valor vigente para cualquier fecha. La ley dispone ajuste anual; por ello el motor advierte cuando no existe un mínimo indexado versionado para la fecha evaluada.

### 5.5. Máximos del artículo 193

El motor conserva:

- máximo ordinario: B/.1,500.00;
- nivel ampliado a B/.2,000.00 con requisitos de cuotas/promedio;
- nivel ampliado a B/.2,500.00 con requisitos superiores de cuotas/promedio.

Las comparaciones de requisitos usan `>=` cuando la norma establece un mínimo.

### 5.6. Indemnización por Vejez

La Indemnización por Vejez se modela como **pago único**, no como pensión mensual.

Flujo:

1. calcular la mensualidad hipotética que habría correspondido;
2. dividir los meses/cuotas acreditados entre seis;
3. multiplicar ese cociente por la mensualidad hipotética;
4. conservar el resultado en un campo de pago único.

Desde **01/03/2036**, el clasificador deja de aplicar esta indemnización y deriva el caso a la transición SUCGS prevista por el artículo 186.

## 6. Subsistema Mixto

### 6.1. Fuentes principales

El motor utiliza los artículos **155 y 178–188**, además de los artículos 192 y 193 cuando resultan concordantes con el componente definido.

Reglamentos principales:

- [Reglamento de Incorporación al Subsistema Mixto](https://w3.css.gob.pa/wp-content/wdocs/REGLAMENTO%20DE%20INCORPORACION%20AL%20SUBSISTEMA%20MIXTO.pdf)
- [Resolución 39,470-2007-J.D.](https://w3.css.gob.pa/wp-content/wdocs/RES%2039470-2007-JD.pdf)
- [Resolución 41,055-2009-J.D.](https://w3.css.gob.pa/wp-content/wdocs/RES%2041%2C055-2009-J.D..pdf)
- [Reglamento de Seguros Colectivos del CAP](https://www.css.gob.pa/wp-content/uploads/2023/10/REGLAMENTO-DE-SEGUROS-COLECTIVOS-DEL-COMPONENTE-DE-AHORRO-PERSONAL-DEL-SUBSISTEMA-MIXTO-actualizado.pdf)
- [Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria](https://www.css.gob.pa/wp-content/uploads/2025/07/REGLAMENTO-DE-INCORPORACION-AL-CCCS.pdf)

### 6.2. Componente de Beneficio Definido

El salario participante del componente se limita a **B/.500.00 mensuales**. Como el historial de la aplicación es anual, la aproximación actual limita el salario anual participante a `B/.500 × cuotas del año` y muestra una advertencia cuando este criterio sustituye un detalle mensual real.

Las modalidades de edad/cuotas reutilizan el clasificador general SEBD, pero con parámetros y topes propios del Mixto.

### 6.3. Componente de Ahorro Personal

La pensión programada se calcula a partir de:

- saldo ahorrado y capitalizado informado;
- bono de reconocimiento cuando corresponde;
- valor actuarial de expectativa de vida aplicable.

La aplicación **no reconstruye el saldo CAP** acumulando porcentajes sobre salarios anuales ni reutiliza los factores actuariales del SUCGS.

### 6.4. Bono de reconocimiento

El artículo 183 se conserva como regla separada. La aplicación acepta un monto oficial o validado y registra si fue confirmado. No reconstruye todavía el bono individual desde el historial anual.

### 6.5. Seguro Colectivo de Renta Vitalicia

El artículo 184 y el reglamento de seguros colectivos se modelan como una garantía futura: si el pensionado sobrevive la expectativa de vida utilizada y se agota el capital, el seguro continúa pagando el componente CAP según las condiciones reglamentarias.

La referencia histórica de prima del reglamento se conserva para trazabilidad, pero no se vuelve a descontar de un saldo oficial suministrado por el Asegurado(a).

### 6.6. Devolución del CAP

Cuando el artículo 187 habilita la devolución total, la aplicación no decide por el Asegurado(a). `AUTO` deja la decisión pendiente; `PENSION_PROGRAMADA` y `DEVOLUCION_TOTAL` representan elecciones explícitas.

La devolución es un **pago único** y no se suma como si fuera una mensualidad.

### 6.7. Transición Mixto → SUCGS

La implementación utiliza como frontera operativa:

- último día de cálculo bajo Mixto: **29/02/2032**;
- inicio de cálculo bajo SUCGS: **01/03/2032**.

Esta decisión se fundamenta en el artículo 188 y en el artículo 5 del Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria.

El artículo 153 del Texto Único contiene una referencia distinta a **01/03/2036** para asegurados del Mixto. La aplicación conserva esta discrepancia en documentación y parámetros; no la corrige silenciosamente.

### 6.8. Fecha operativa de opción en 2026

La Resolución 57,805-2025-J.D. publicada en 2025 contiene originalmente 17/03/2026. Comunicaciones oficiales posteriores de la CSS utilizan **18/08/2026** como fecha límite operativa para quienes cumplan los requisitos de cambio.

- [CSS — fecha clave del 18 de agosto](https://prensa.css.gob.pa/2026/07/10/css-intensifica-jornadas-de-capacitacion-sobre-mi-retiro-seguro-ante-la-fecha-clave-del-18-de-agosto/)
- [CSS — cuenta regresiva hacia el 18 de agosto](https://prensa.css.gob.pa/2026/07/13/cuenta-regresiva-hacia-el-18-de-agosto-asegurados-deben-decidir-su-futuro-pensional/)

Esta fecha debe revalidarse cuando se use fuera del contexto temporal de 2026.

## 7. SUCGS

### 7.1. Artículos principales

El motor utiliza los artículos **152, 153 y 194–198**, además del artículo 1 numeral 41 para la definición de salario promedio base utilizada en la garantía de reemplazo.

### 7.2. Componente contributivo — artículo 196

Fórmula versionada:

```text
pensión contributiva mensual
= saldo de capitalización solidaria / 1000 × factor actuarial de la edad
```

La tabla de factores se almacena en `normativa/sucgs.json`. La ley dispone actualización periódica, por lo que el motor no debe tratarlos como inmutables fuera de su versión.

### 7.3. Componente Solidario No Contributivo — artículo 194

La aplicación versiona como referencias legales:

- valor mínimo universal: B/.144.00;
- edad de referencia de la capa solidaria: 65 años;
- reglas por cantidad de cuotas.

Como el artículo prevé indexación, el motor permite introducir valores vigentes confirmados.

### 7.4. Pensión Garantizada Solidaria — artículo 195

Con edad de referencia y al menos 240 cuotas, el motor compara el resultado contributivo con la referencia de la Pensión Garantizada Solidaria.

Existe una superposición literal en 240 cuotas entre el artículo 194 y el artículo 195. La implementación prioriza el artículo 195 como regla específica de garantía mínima y registra la decisión en `docs/DECISIONES.md`.

### 7.5. Garantía de reemplazo mínimo — artículo 197

La aplicación preevalúa automáticamente:

- mínimo anual de cuotas;
- cantidad total y consecutiva de años sin cotización;
- distribución temporal mínima 50 % / 50 %;
- salario promedio base mensual.

La condición de estabilidad salarial se conserva como confirmación explícita porque el numeral 3 y los mecanismos de control institucional no permiten una inferencia segura con el historial anual actual.

Cuando todas las condiciones pueden determinarse, la pensión total es el mayor valor entre:

- resultado previo después de la capa solidaria; y
- monto objetivo de la garantía de reemplazo.

Para requisitos inferiores a 240 cuotas, la aplicación modela una garantía proporcional desde el umbral documentado de 120 cuotas. Esta es una **decisión de implementación conservadora** y no se presenta como una transcripción literal independiente del artículo 197.

## 8. Regímenes especiales

El motor general no cubre todavía todos los regímenes especiales. Por ejemplo, trabajadores estacionales agrícolas y de la construcción tienen reglas propias.

- [CSS — Pensión por Vejez para Trabajadores Estacionales Agrícolas y de la Construcción](https://www.css.gob.pa/pension-por-vejez-para-los-trabajadores-estacionales-agricolas-y-de-la-construccion/)

Antes de incorporar un régimen especial se debe crear una fuente versionada, pruebas independientes y una forma de identificar el tipo de Asegurado(a).

## 9. Redondeo y valores monetarios

El criterio técnico general de la aplicación es:

- cálculo con `Decimal`;
- precisión conservada durante operaciones;
- materialización a centavos con `ROUND_HALF_UP`;
- prioridad de cualquier regla normativa específica de redondeo cuando exista.

## 10. Mantenimiento normativo

Cuando cambie una fuente:

1. verificar la publicación oficial;
2. registrar fecha y URL;
3. modificar el JSON normativo sin destruir la versión histórica que pueda ser necesaria;
4. actualizar pruebas;
5. actualizar `FUENTES_NORMATIVAS.md`;
6. registrar un ADR cuando exista una decisión interpretativa;
7. reflejar el cambio en `CHANGELOG.md`.

La aplicación debe favorecer resultados **auditables y conservadores** frente a una precisión aparente basada en parámetros inventados.

## Presentación de fuentes en la interfaz

Los enlaces normativos continúan versionados en `normativa/*.json`. La interfaz no debe duplicar URLs en JavaScript. `app/servicios/fuentes_normativas.py` transforma esos metadatos en un catálogo humano para `/metodologia`, mientras la trazabilidad resuelve los IDs internos a títulos y enlaces oficiales.
