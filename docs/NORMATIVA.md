# Normativa

## Estado

La capa normativa **general** ya comenzó a implementarse.

Actualmente existen:

```text
normativa/parametros_generales.json
app/core/normativa.py
```

El archivo JSON mantiene parámetros generales versionados y el módulo Python concentra su lectura.

Los parámetros específicos de los motores SEBD, Subsistema Mixto y SUCGS todavía están pendientes y deberán incorporarse con trazabilidad normativa antes de considerarse definitivos.

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
