# Sistema Único de Capitalización con Garantía Solidaria (SUCGS)

## Alcance actual

La subfase 6E.3 implementa el Componente Contributivo de Capitalización Solidaria del artículo 196, la capa solidaria de los artículos 194 y 195 y la garantía de reemplazo mínimo del artículo 197 del Texto Único vigente de la Ley 51.

## Fórmula contributiva

```text
pensión mensual contributiva = saldo / 1000 × factor actuarial por edad
```

La tabla legal actualmente versionada en `normativa/sucgs.json` incluye, entre otros, los factores 4.77 a los 57 años, 5.15 a los 62, 5.44 a los 65, 6.04 a los 70 y 7.94 para 80 años o más.

## Capa solidaria del artículo 194

A los 65 años, los casos con menos de 240 cuotas se clasifican según cuotas y resultado contributivo:

- menos de 120 cuotas y pensión contributiva inferior al valor mínimo universal: se conserva el monto contributivo;
- de 120 a menos de 240 cuotas y pensión contributiva igual o inferior al valor mínimo universal: se completa hasta el valor mínimo universal;
- menos de 240 cuotas y pensión contributiva igual o superior al valor mínimo universal: se conserva el monto contributivo dentro de los supuestos del artículo 194.

La referencia legal versionada del valor mínimo universal es B/.144.00. Las prestaciones del artículo 194 están sujetas a indexación, por lo que el motor permite reemplazar esa referencia por un valor vigente confirmado.

## Pensión Garantizada Solidaria del artículo 195

Al alcanzar la edad de referencia y acreditar al menos 240 cuotas, la Pensión Garantizada Solidaria se trata como el mínimo aplicable. La referencia legal versionada es de al menos B/.265.00 mensuales. Si la pensión contributiva es inferior, el motor muestra el complemento necesario y el monto después de la capa solidaria.

El límite exacto de 240 cuotas se superpone con la redacción del numeral 2 del artículo 194. La aplicación prioriza el artículo 195 para ese caso y documenta la interpretación.

## Garantía de reemplazo mínimo — artículo 197

La aplicación preevalúa con historial anual completo: al menos cinco cuotas en los años con cotización, un máximo de seis años sin cotización y no más de cinco consecutivos, y la distribución mínima de la mitad de las cuotas objetivo en los primeros veinte años de vida laboral y la otra mitad en los años restantes.

El salario promedio base mensual se obtiene dividiendo el total de salarios cotizados entre los meses cotizados, siguiendo la definición general del artículo 1 numeral 41. Con 240 o más cuotas, la tasa objetivo es 60 %. Para pensiones con requisito legal inferior, la tasa se reduce proporcionalmente mediante `60 % × cuotas / 240`; la implementación conservadora aplica esta variante desde 120 cuotas.

La condición de estabilidad salarial del numeral 3 no se deduce automáticamente. La redacción legal usa un umbral del 30 % cuya aplicación operativa debe ser controlada por la CSS. Por ello se exige una confirmación explícita. Si falta, el motor conserva el cálculo intermedio y deja la pensión total pendiente.

El saldo contributivo tampoco se reconstruye todavía desde el historial salarial porque el artículo 196 establece tratamientos distintos según el origen del asegurado y utiliza rendimientos que deben identificarse por periodo.

## Fuente primaria

Texto Único de la Ley 51 de 2005 con las reformas de la Ley 462 de 2025, Gaceta Oficial 30284-B de 22 de mayo de 2025, artículos 152, 153 y 194-198.

## Integración visual 6E.4

El Paso 6 expone las tres capas numéricas ya implementadas: componente contributivo, capa solidaria de los artículos 194 y 195 y garantía de reemplazo del artículo 197. La interfaz no replica las fórmulas en JavaScript; el cálculo permanece en el backend.

El usuario debe suministrar o confirmar únicamente los datos que no pueden derivarse con seguridad de los pasos previos: saldo de Capitalización Solidaria, vigencia de los valores solidarios, cobertura completa del historial y estado de la condición de estabilidad salarial. Las condiciones de cuotas y distribución continúan auditándose automáticamente con el historial anual consolidado.
