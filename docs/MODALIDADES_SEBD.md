# Modalidades de retiro por vejez — SEBD

Este documento resume las modalidades generales implementadas del **Subsistema Exclusivamente de Beneficio Definido (SEBD)**. Las fuentes oficiales y enlaces se centralizan en [FUENTES_NORMATIVAS.md](FUENTES_NORMATIVAS.md).

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Árbol general de clasificación

La aplicación determina automáticamente la modalidad a partir de:

- sexo;
- fecha de nacimiento;
- fecha de retiro seleccionada;
- edad de referencia;
- cuotas totales estimadas a esa fecha.

Clasificación general:

```text
Antes de la banda anticipada
└── No elegible por edad

Dentro de la banda anticipada
├── 240 o más cuotas → Anticipada
├── 180 a 239 cuotas → Proporcional Anticipada
└── menos de 180 → No elegible por esta vía

Edad de referencia o posterior
├── 240 o más cuotas → Normal
├── 180 a 239 cuotas → Proporcional
└── menos de 180 → Indemnización por Vejez, cuando legalmente corresponda
```

## 2. Pensión Normal

Condiciones generales implementadas:

- haber alcanzado la edad de referencia;
- contar con al menos 240 cuotas.

La tasa parte de 60 % del salario base y puede incrementarse por bloques completos de doce cuotas excedentes según hayan sido aportadas antes o después de la edad de referencia.

## 3. Pensión Anticipada

La banda general permite solicitar la prestación hasta dos años antes de la edad de referencia cuando se cumplen las cuotas requeridas.

El motor:

1. calcula la pensión antes de reducción;
2. aplica límites correspondientes;
3. obtiene el factor reglamentario mensual según la anticipación;
4. aplica el factor de edad.

Los factores se versionan en `normativa/sebd.json` y su fuente reglamentaria es el Reglamento para el Cálculo de Prestaciones Económicas.

## 4. Pensión Proporcional

Con edad de referencia y entre 180 y 239 cuotas:

```text
pensión proporcional
= pensión base aplicable × cuotas / 240
```

El motor conserva por separado el factor de cuotas y el resultado posterior a su aplicación.

## 5. Pensión Proporcional Anticipada

Dentro de la banda anticipada y con 180 a 239 cuotas:

1. se calcula la base de la pensión;
2. se aplica el factor proporcional `cuotas / 240`;
3. se aplica el factor de reducción por edad.

## 6. Salario base

La implementación usa el promedio mensual de los diez mejores años conforme al artículo 180 y al procedimiento reglamentario disponible.

Con historial anual:

- no se anualiza artificialmente un año parcial;
- se conserva su salario efectivamente cotizado;
- cuando se seleccionan diez años, la suma se lleva a promedio mensual sobre 120 meses.

Esta aproximación debe revisarse si se incorpora detalle mensual oficial.

## 7. Indemnización por Vejez

Cuando la persona alcanza la edad de referencia con menos de 180 cuotas y el régimen de indemnización sigue vigente:

1. se calcula una mensualidad hipotética de retiro;
2. se divide el total de meses/cuotas acreditados entre seis;
3. se multiplica ese factor por la mensualidad hipotética;
4. el resultado se presenta como **pago único**, no como pensión mensual.

Desde **01/03/2036**, el artículo 186 remite estos casos al SUCGS.

## 8. Mínimos y máximos

### 8.1. Monto mínimo

El artículo 192 establece un monto sujeto a ajuste anual. La aplicación no fuerza un mínimo indexado sin tener el valor vigente versionado para la fecha de cálculo.

### 8.2. Límites máximos

El artículo 193 establece:

- máximo ordinario de B/.1,500.00;
- máximo de B/.2,000.00 bajo requisitos ampliados;
- máximo de B/.2,500.00 bajo requisitos superiores.

Las condiciones se evalúan con los años de salario y cuotas requeridos cuando la información disponible lo permite.

## 9. Prestaciones fuera del motor general

El clasificador no debe tratar como idénticos todos los regímenes de asegurados. Los regímenes especiales —por ejemplo, trabajadores estacionales agrícolas y de la construcción— requieren reglas propias y una identificación explícita del tipo de Asegurado(a).

## 10. Fuentes principales

- [Texto Único de la Ley 51 — PDF CSS](https://www.css.gob.pa/wp-content/uploads/2025/05/TEXTO-UNICO-DE-LA-LEY-51-DE-2005-CSS-GACETA-OFICIAL-22-5-25.pdf)
- [Normativa de Prestaciones Económicas — CSS](https://www.css.gob.pa/normativa-prestaciones-economicas/)
- [Resolución 39,302-2007-J.D. — CSS](https://w3.css.gob.pa/wp-content/wdocs/Resolucion%20%2039%2C302-2007-J.D..pdf)
- [Mapa completo de fuentes del proyecto](FUENTES_NORMATIVAS.md)
