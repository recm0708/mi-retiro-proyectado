# Normativa

## Estado

La capa normativa **general** ya comenzó a implementarse.

Actualmente existen:

```text
normativa/parametros_generales.json
app/core/normativa.py
```

El archivo JSON mantiene parámetros generales versionados y el módulo Python concentra su lectura.

Los parámetros de la primera modalidad SEBD normal ya se encuentran versionados en `normativa/sebd.json`. Los parámetros del Subsistema Mixto, SUCGS y las demás modalidades SEBD continúan pendientes y deberán incorporarse con trazabilidad normativa antes de considerarse definitivos.

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
