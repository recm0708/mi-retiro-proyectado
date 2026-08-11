# Modalidades de retiro por vejez — SEBD

Este documento resume la lógica implementada en el clasificador general del Paso 6. No sustituye la Ley ni una resolución de la Caja de Seguro Social.

## Árbol general de clasificación

```text
Fecha anterior a referencia - 2 años
└─ No elegible por la banda estándar

Desde referencia - 2 años hasta antes de referencia
├─ >= 240 cuotas → Anticipada
├─ 180–239       → Proporcional Anticipada
└─ < 180         → No elegible para pensión por vejez en esa fecha

Edad de referencia o superior
├─ >= 240 cuotas → Normal
├─ 180–239       → Proporcional
└─ < 180         → Indemnización por Vejez, si corresponde antes de 01/03/2036
```

Los regímenes especiales y trabajadores independientes requieren reglas adicionales y no se confunden con este árbol general.

## Normal

```text
Tasa = 60 %
     + 1.25 puntos por cada bloque completo de 12 cuotas excedentes antes de referencia
     + 2 puntos por cada bloque completo de 12 cuotas posteriores a referencia

Pensión preliminar = salario base × tasa
```

Después se aplican los límites legalmente correspondientes.

## Anticipada

```text
Tasa = 60 %
     + 1.25 puntos por cada bloque completo de 12 cuotas excedentes antes de referencia

Monto limitado = aplicar límites al salario base × tasa
Pensión = monto limitado × factor de reducción por edad
```

La tabla mensual del factor se versiona en `normativa/sebd.json`.

## Proporcional

```text
Monto base = 60 % del salario base
Monto limitado = aplicar límites
Factor de cuotas = cuotas acreditadas / 240
Pensión = monto limitado × factor de cuotas
```

La Ley permite que esta modalidad quede por debajo del mínimo general.

## Proporcional Anticipada

```text
Monto base = 60 % del salario base
Monto limitado = aplicar límites
Factor de cuotas = cuotas acreditadas / 240
Factor de edad = tabla de reducción anticipada

Pensión = monto limitado × factor de cuotas × factor de edad
```

## Salario base

La regla general utiliza el promedio mensual de los diez mejores años de cotizaciones. La implementación conserva cada año calendario con su salario cotizado real o proyectado y selecciona los diez totales anuales más altos disponibles hasta la fecha de retiro.

Un año parcial no se anualiza artificialmente. Si entra entre los diez mejores, conserva las cuotas y el salario efectivamente atribuido a ese año; la suma de los diez años se divide entre 120 meses.

## Prestaciones todavía no calculadas aquí

- monto de la Indemnización por Vejez;
- regímenes especiales;
- componente de Beneficio Definido del Subsistema Mixto;
- componente de ahorro del Mixto;
- SUCGS.

## Fuentes principales

- Texto Único de la Ley 51 de 2005 con reformas hasta la Ley 462 de 2025, Gaceta Oficial 30284-B del 22 de mayo de 2025, artículos 178–181 y 186.
- Reglamento para el Cálculo de Prestaciones Económicas, Resolución 39,302-2007-J.D. y modificaciones listadas por la CSS.
- Sección oficial de Normativa de Prestaciones Económicas de la CSS.
