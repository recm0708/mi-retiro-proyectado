# Sistema Único de Capitalización con Garantía Solidaria (SUCGS)

El motor SUCGS se construye por capas para evitar confundir un resultado contributivo intermedio con la pensión total.

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

Fuentes y enlaces completos: [FUENTES_NORMATIVAS.md](FUENTES_NORMATIVAS.md).

## 1. Alcance implementado

El motor cubre:

1. Componente Contributivo de Capitalización Solidaria — artículo 196;
2. Componente Solidario No Contributivo — artículo 194;
3. Pensión Garantizada Solidaria — artículo 195;
4. garantía de reemplazo mínimo — artículo 197;
5. integración visual en el Paso 6.

## 2. Componente contributivo — artículo 196

Fórmula:

```text
pensión contributiva mensual
= saldo de capitalización solidaria / 1,000 × factor actuarial de la edad
```

Los factores por edad se almacenan en `regulations/sucgs.json` y deben actualizarse cuando la CSS publique una nueva tabla aplicable.

El saldo se ingresa explícitamente; la aplicación no lo reconstruye todavía desde salarios históricos porque esa conversión depende del origen previsional, aportes, reglas pre/post reforma y rendimientos efectivos.

## 3. Capa solidaria — artículo 194

La aplicación distingue los supuestos del Componente Solidario No Contributivo y mantiene versionados los valores legales de referencia.

El valor mínimo universal B/.144.00 se trata como referencia legal al 22/05/2025 y puede sustituirse por un valor vigente confirmado cuando exista indexación aplicable.

## 4. Pensión Garantizada Solidaria — artículo 195

Con edad de referencia y al menos 240 cuotas, el resultado contributivo se compara con la Pensión Garantizada Solidaria.

La referencia B/.265.00 también se conserva como valor versionado y no como constante eterna.

En 240 cuotas existe una superposición textual con el artículo 194. La implementación prioriza el artículo 195 como regla específica y documenta esta decisión en `DECISIONES.md`.

## 5. Garantía de reemplazo mínimo — artículo 197

La preevaluación usa:

- historial laboral anual completo;
- mínimo de cuotas por año activo;
- total y consecutividad de años sin cotización;
- distribución mínima 50 % / 50 %;
- salario promedio base mensual;
- confirmación explícita de estabilidad salarial.

Cuando todas las condiciones se determinan:

```text
pensión total
= mayor entre resultado previo y monto objetivo de garantía
```

Con 240 cuotas o más, la tasa mínima objetivo es 60 % cuando se cumplen las condiciones. Para requisitos inferiores admitidos por la implementación, se usa una proporción respecto de 240 cuotas.

## 6. Condición de estabilidad salarial

La aplicación no inventa una interpretación automática del numeral 3 del artículo 197. La condición se mantiene como:

- confirmada que cumple;
- confirmada que no cumple; o
- pendiente/no confirmada.

Si esta condición es indispensable para cerrar la garantía y permanece pendiente, la pensión total también permanece pendiente.

## 7. Datos mostrados en el Paso 6

La interfaz separa:

- saldo considerado;
- edad y factor actuarial;
- divisor legal;
- componente contributivo;
- tipo y complemento solidario;
- condiciones del artículo 197;
- salario promedio base;
- tasa mínima aplicable;
- monto objetivo de garantía;
- complemento de garantía;
- pensión mensual total.

## 8. Fuentes principales

- [Texto Único de la Ley 51 — PDF CSS](https://www.css.gob.pa/wp-content/uploads/2025/05/TEXTO-UNICO-DE-LA-LEY-51-DE-2005-CSS-GACETA-OFICIAL-22-5-25.pdf)
- [Gaceta Oficial 30284-B](https://www.gacetaoficial.gob.pa/pdfTemp/30284_B/GacetaNo_30284b_20250522.pdf)
- [Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria](https://www.css.gob.pa/wp-content/uploads/2025/07/REGLAMENTO-DE-INCORPORACION-AL-CCCS.pdf)
