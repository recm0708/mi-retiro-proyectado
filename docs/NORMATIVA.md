# Normativa

## Estado

La capa normativa **general** ya comenzó a implementarse.

Actualmente existen:

```text
normativa/parametros_generales.json
app/core/normativa.py
```

El archivo JSON mantiene parámetros generales versionados y el módulo Python concentra su lectura.

Los parámetros implementados de SEBD, Mixto y SUCGS se encuentran versionados en archivos específicos dentro de `normativa/`. Los valores sujetos a actualización o a determinación individual continúan identificados explícitamente como tales.

## Fuente base actual

Como referencia oficial general se utiliza el Texto Único de la Ley 51 de 2005, Orgánica de la Caja de Seguro Social, con las reformas indicadas por la CSS, incluida la Ley 462 de 2025.

La página oficial de la CSS identifica ese Texto Único en la Gaceta Oficial 30284-B de 22 de mayo de 2025.

Para la pensión por vejez, la página oficial de la CSS publica actualmente como referencias generales:

- 57 años para mujeres;
- 62 años para hombres;
- posibilidad de presentar la solicitud con tres meses de anticipación;
- 240 cuotas para la pensión por vejez normal indicada en esa página.

Estas referencias generales no sustituyen la evaluación de transiciones, tipos de prestación, subsistemas ni excepciones.

## Parámetros implementados

`normativa/parametros_generales.json` contiene actualmente:

- versión de la fuente;
- identificación de la fuente oficial;
- Gaceta Oficial de referencia;
- edades de referencia por sexo;
- anticipación general publicada para solicitud.

Los umbrales preliminares de 180 y 240 cuotas utilizados en el Paso 2 todavía no constituyen por sí solos un motor de elegibilidad.

## Regla de implementación

Antes de implementar una fórmula legal definitiva se deberá:

1. identificar la fuente aplicable;
2. registrar vigencia y versión;
3. documentar el parámetro o regla;
4. crear o actualizar casos de validación;
5. implementar la lógica en el motor correspondiente;
6. separar, cuando corresponda, reglas generales, transiciones y excepciones.

## Estructura prevista

```text
normativa/
├── parametros_generales.json
├── sebd.json
├── mixto.json
├── sucgs.json
├── factores_actuariales.json
└── transiciones.json
```

Los archivos se crearán solo cuando los parámetros estén suficientemente verificados. No se añadirán valores legales especulativos.

JSON estándar no admite comentarios; la explicación y trazabilidad se mantendrán en este documento y en la documentación de cada motor.

## Redondeo

El criterio técnico general del proyecto es `Decimal` + `ROUND_HALF_UP` a centavos al materializar un importe.

Si una norma, reglamento, tabla actuarial o procedimiento oficial aplicable establece una regla distinta para un cálculo específico, esa regla tendrá prioridad dentro de ese motor y deberá documentarse.

## Parámetros SEBD versionados

Se incorporó:

```text
normativa/sebd.json
```

La primera versión registra reglas verificadas del Texto Único publicado en la Gaceta Oficial 30284-B de 22 de mayo de 2025:

- artículos 178 y 179: condiciones generales y edad de referencia;
- artículo 180: promedio mensual de los diez mejores años;
- artículo 181: 240 cuotas de referencia, tasa básica del 60 %, incremento de 1.25 % por cada doce cuotas completas excedentes anteriores a la edad de referencia e incremento de 2 % por cada doce cuotas completas posteriores;
- artículo 192: monto mínimo base de B/.265.00 sujeto a ajuste anual;
- artículo 193: máximo ordinario de B/.1,500.00 y niveles ampliados de B/.2,000.00 y B/.2,500.00 cuando se cumplen las condiciones de cuotas y promedios salariales indicadas por la ley.

El monto mínimo indexado no se considera todavía un parámetro definitivo porque debe relacionarse con la fecha de cálculo. Esta limitación queda visible en la salida del motor.

## Modalidades SEBD incorporadas en Paso 6C

El artículo 181 del Texto Único vigente distingue cuatro modalidades generales de Pensión de Retiro por Vejez para el SEBD y el componente de Beneficio Definido del Subsistema Mixto:

- **Normal:** edad de referencia o superior y 240 cuotas o más.
- **Anticipada:** hasta dos años antes de la edad de referencia y 240 cuotas o más.
- **Proporcional:** edad de referencia o superior, con 180 a 239 cuotas.
- **Proporcional Anticipada:** hasta dos años antes de la edad de referencia, con 180 a 239 cuotas.

La modalidad anticipada aplica un factor de reducción después de calcular la base, incrementos y límites que correspondan. La modalidad proporcional multiplica el resultado limitado por `cuotas / 240`. La proporcional anticipada aplica ambos factores en ese orden.

Para la banda anticipada, `normativa/sebd.json` versiona la tabla mensual de factores del Reglamento para el Cálculo de Prestaciones Económicas (Resolución 39,302-2007-J.D.) y conserva como anclas los valores expresamente recogidos por la Ley para uno y dos años de anticipación: `0.9128` y `0.8342`.

La CSS mantiene publicado el Reglamento para el Cálculo de Prestaciones Económicas y sus modificaciones dentro de su sección de normativa vigente de Prestaciones Económicas.

## Años calendario parciales en el salario base

El procedimiento reglamentario del cálculo de prestaciones trabaja con los años calendario en los que el total de ingresos cotizados resulta más alto. Cuando se seleccionan diez años para formar la base, la suma de esos diez años se lleva a promedio mensual dividiendo entre 120 meses.

Por esta razón, un año calendario parcial puede entrar dentro de los diez mejores si su total cotizado supera al de otro año candidato. La aplicación conserva las cuotas visibles de ese año y no anualiza artificialmente el salario cotizado.

Si no existieran diez años suficientes, el tratamiento especial deberá seguir la regla reglamentaria aplicable a meses efectivamente acreditados; esa excepción se implementará únicamente cuando aparezca un caso real que la requiera.

## Indemnización por vejez

El artículo 186 establece una Indemnización por Vejez para personas del SEBD o del componente de Beneficio Definido del Subsistema Mixto que, al solicitar la prestación y cumplir la edad de referencia, no hayan podido acreditar 180 cuotas. La prestación equivale a una mensualidad de la Pensión de Retiro por Vejez que habría correspondido por cada seis meses de cotizaciones acreditados.

El Reglamento para el Cálculo de Prestaciones Económicas desarrolla el procedimiento: primero se calcula la Pensión de Retiro por Vejez Normal hipotética; luego los meses de cotización registrados se dividen entre seis y el resultado se multiplica por esa mensualidad. `normativa/sebd.json` versiona el divisor `6`, la naturaleza de pago único y la fecha de transición.

La implementación conserva la división directa `meses / 6`; no usa cociente entero. Para construir la mensualidad hipotética se aplica la regla de los diez mejores años y el denominador de 120 meses. El mínimo indexado sigue pendiente de versionarse por fecha y, cuando pudiera afectar el cálculo, se genera una advertencia.

A partir del 1 de marzo de 2036, el artículo 186 dispone que la CSS deje de conceder esta indemnización y proceda conforme al SUCGS.


## Subsistema Mixto — parámetros versionados

`normativa/mixto.json` registra la primera parametrización del Subsistema Mixto.

### Componente de Beneficio Definido

Se documentan:

- participación salarial hasta B/.500.00 mensuales;
- diez mejores años para la base;
- 240 cuotas de referencia;
- 180 cuotas para la banda proporcional;
- tasa base de 60 %;
- incrementos por bloques completos de doce cuotas antes y después de la edad de referencia;
- máximo mensual del componente de B/.500.00;
- mínimo base B/.265.00 sujeto a indexación anual.

La indexación del mínimo continúa pendiente de versionarse por fecha.

### Componente de Ahorro Personal

El artículo 182 establece una pensión programada basada en el total ahorrado y capitalizado de la cuenta individual, dividido entre el valor actuarial de la expectativa de vida usando la tasa de descuento vigente y la tabla de mortalidad adoptada por la Junta Directiva.

En esta etapa no se ha localizado/versionado un divisor actuarial vigente por fecha que pueda utilizarse como parámetro general. Por ello:

- `valor_actuarial_expectativa_vida = null`;
- `tasa_descuento = null`;
- `tabla_mortalidad = null`;

en el archivo normativo. El motor exige esos datos de forma explícita cuando se quiera producir un cálculo CAP.

Los factores del SUCGS no se utilizarán como sustitutos.

### Bono de reconocimiento

El artículo 183 se conserva como regla separada para los casos en que proceda un bono de reconocimiento por incorporación voluntaria al Mixto desde el SEBD. Esta etapa acepta el monto ya determinado; el cálculo reglamentario del bono se implementará en una subfase posterior.

### Transición Mixto → SUCGS

Para la prestación de retiro, el artículo 188 y el Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria ubican la transición operativa en:

```text
último día bajo cálculo Mixto: 29/02/2032
inicio de cálculo SUCGS:       01/03/2032
```

El artículo 153 del mismo Texto Único contiene una referencia a 01/03/2036 para asegurados del Subsistema Mixto. Esta diferencia se documenta expresamente en vez de armonizarla de manera silenciosa. La implementación preliminar utiliza 2032 por ser la regla específica de cálculo del artículo 188 y la fecha utilizada por el reglamento operativo.

### Opción de sistema en 2026

La Resolución 57,805-2025-J.D. registró originalmente un plazo de opción hasta 17/03/2026. Comunicaciones oficiales posteriores de la CSS en 2026 utilizan 18/08/2026 como fecha límite operativa y explican que la decisión se dirige a personas del Sistema Mixto que no alcanzan la edad de retiro al 01/03/2032.

La aplicación documenta ambas fechas. La lógica de elegibilidad individual para ejercer la opción no se automatiza todavía debido a la evolución de las reglas operativas y a que debe evitarse inferir una decisión jurídica a partir de información incompleta.

### Parámetros históricos de seguros colectivos

Se conservan, solo para trazabilidad, porcentajes históricos de los seguros colectivos del CAP. Estos parámetros no se usan en 6D.1 para reconstruir el saldo actual de una cuenta individual.

## Subsistema Mixto — ampliación 6D.2

Fuentes oficiales consultadas para esta subfase:

- Texto Único de la Ley 51 de 2005, artículos 182–188, Gaceta Oficial 30284-B de 22/05/2025;
- Reglamento de Seguros Colectivos del Componente de Ahorro Personal del Subsistema Mixto, Resolución 41,055-2009-J.D., edición actualizada a junio de 2020;
- página oficial de Normativa de Prestaciones Económicas de la CSS.

Reglas versionadas:

1. **Artículo 182:** la pensión programada CAP divide el monto ahorrado/capitalizado por el valor actuarial de expectativa de vida con la tasa de descuento aplicable.
2. **Artículo 183:** el bono de reconocimiento se reconoce a determinados asegurados que ingresaron voluntariamente desde el SEBD. La aplicación no reconstruye su monto automáticamente.
3. **Artículo 184:** el seguro colectivo garantiza la continuidad de la pensión CAP si el pensionado sobrevive la expectativa de vida usada y se agotan los fondos.
4. **Artículo 187:** quien no cumpla los requisitos de la Pensión de Retiro por Vejez Normal puede solicitar, al alcanzar la edad de referencia, la devolución total de la suma ahorrada y capitalizada mediante un pago único.
5. **Reglamento de Seguros Colectivos, artículo 10:** el Seguro Colectivo de Renta Vitalicia continúa pagando el monto CAP hasta la muerte bajo la condición prevista.
6. **Reglamento de Seguros Colectivos, artículo 12:** las primas del seguro colectivo no se devuelven en la indemnización/devolución por vejez, porque forman parte del aporte de solidaridad.

La prima de 0.93 % del Seguro Colectivo de Renta Vitalicia se conserva como **referencia histórica reglamentaria** y no como parámetro vigente presumido para reconstruir cuentas individuales.

## SUCGS — artículos 194 a 197

La fuente principal versionada es el Texto Único de la Ley 51 de 2005 publicado en la Gaceta Oficial 30284-B de 22/05/2025.

El artículo 196 establece que la pensión mensual contributiva se obtiene dividiendo el saldo entre mil y multiplicándolo por el factor de pensionamiento actuarial correspondiente a la edad de retiro. La tabla legal usa factores similares para ambos sexos y establece 4.77 a los 57 años, 5.15 a los 62 años y 7.94 para 80 años o más.

En 6E.3 se materializan los artículos 194, 195 y 197. El artículo 194 introduce el Componente Solidario No Contributivo y usa como referencia el valor mínimo universal de B/.144.00, con indexación posterior. El artículo 195 fija la Pensión Garantizada Solidaria en al menos B/.265.00 para quien alcance la edad de referencia y tenga como mínimo 240 cuotas.

La redacción del numeral 2 del artículo 194 incluye literalmente 240 cuotas, mientras el artículo 195 comienza precisamente en 240. La implementación prioriza el artículo 195 en ese punto y deja constancia de la superposición.

El artículo 197 exige condiciones sobre número anual de cuotas, distribución durante la vida laboral y estabilidad salarial. La aplicación automatiza las dos primeras con historial anual completo y exige confirmación explícita para la tercera. El artículo 1 numeral 41 sirve como base para calcular el salario base mensual promedio a partir de salarios y meses cotizados.
