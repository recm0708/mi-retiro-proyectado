# Validación

## Objetivo

Este documento registra cómo verificar cambios que puedan afectar cálculos, fechas, cuotas, precisión monetaria o integración entre pasos.

Los documentos personales originales utilizados como referencia **no deben versionarse**. Los casos permanentes deberán anonimizarse y conservar únicamente los datos mínimos necesarios para reproducir un cálculo.

## Validación automatizada

Ejecutar desde la raíz del proyecto:

```powershell
python -m compileall app
python -m unittest discover -s tests -v
```

Actualmente existen pruebas para:

- redondeo monetario `ROUND_HALF_UP`;
- límite de dos decimales;
- proyección salarial sin redondeo intermedio;
- línea temporal y años sin cotización;
- cierre del año actual;
- escenarios de retiro;
- integración del Paso 6 con escenario de retiro y escenario salarial;
- edad de referencia femenina y masculina;
- advertencia de horizonte salarial insuficiente.

## Validación manual del asistente

Además de las pruebas automatizadas se debe comprobar el flujo web cuando cambie la interfaz o el estado compartido:

1. completar los pasos afectados;
2. retroceder y avanzar para comprobar restauración;
3. recargar la página y verificar `sessionStorage`;
4. modificar un dato de origen y comprobar invalidación;
5. revisar advertencias y acciones de corrección;
6. comprobar que datos históricos y proyectados permanezcan diferenciados.

## Caso femenino anonimizado de integración

Caso de referencia utilizado para verificar el flujo sin versionar el documento original:

```text
Nacimiento:                     16/11/1969
Sexo:                           femenino
Sistema:                        SEBD
Cuotas reales:                  281
Cuotas acreditadas en 2026:       5
Cierre esperado 2026:             5
Cuotas por año futuro:            12
Salario mensual de prueba:  B/. 1,331.90
Variación 2027:                   1 %
Fecha de evaluación:          10/08/2026
Fecha de corte de cuotas:     10/08/2026
```

Comprobaciones principales después de las correcciones de precisión:

```text
Edad actual:                    56
Edad de referencia:             57
Fecha de referencia:    16/11/2026
Días hasta referencia:           98
Proyección salarial 2027: B/. 16,142.63
Cuotas estimadas a referencia:  281
```

Con escenarios +1/+2/+3/+5 y densidad futura de 12 cuotas/año, el servicio preliminar de retiro espera:

```text
16/11/2026 → 281
16/11/2027 → 291
16/11/2028 → 303
16/11/2029 → 315
16/11/2031 → 339
```

Estas cuotas son estimaciones de planificación por fecha; no constituyen elegibilidad legal.

## Caso masculino mínimo

Caso técnico para verificar la otra edad de referencia:

```text
Nacimiento:               04/12/1966
Sexo:                     masculino
Edad de referencia:       62
Fecha de referencia:      04/12/2028
```

Las fórmulas definitivas de pensión del caso masculino se validarán cuando se implemente el motor SEBD.

## Datos sensibles

No versionar:

- PDFs originales;
- nombres;
- cédulas;
- números de Seguro Social;
- comprobantes personales;
- archivos exportados que permitan identificar al asegurado.

`tests/casos_validacion/originales/` está excluido mediante `.gitignore`.

## Regresión SEBD anonimizada

Se añadió `tests/test_sebd.py` con datos sintéticos no identificables.

El caso de regresión reproduce matemáticamente el resultado oficial de referencia:

```text
Cuotas totales:                 281
Exceso sobre 240:                41
Bloques completos de 12:          3
Tasa adicional:                3.75 %
Tasa total:                   63.75 %
Suma de diez mejores años: B/.139,593.71
Salario base mensual:        B/.1,163.28 (visible)
Pensión mensual estimada:      B/.741.59
```

La prueba conserva precisión interna antes del redondeo monetario final. También se prueban el incremento posterior a la edad de referencia, el límite máximo ordinario y la advertencia de mínimo indexado pendiente.

## Integración del Paso 6

`tests/test_resultados.py` valida que la capa de integración:

- reproduzca B/.741.59 en el escenario de edad de referencia usando la regresión salarial conocida;
- conserve 41 cuotas excedentes anteriores a la referencia en el caso base;
- para un escenario posterior, separe las cuotas nuevas posteriores a la referencia;
- incorpore un año salarial proyectado y emita advertencia cuando se utiliza proyección.

La suite completa de esta etapa contiene 28 pruebas automatizadas.


## Paso 6C — clasificación de modalidades SEBD

La suite automatizada incorpora pruebas para:

- clasificación Normal;
- Anticipada;
- Proporcional;
- Proporcional Anticipada;
- identificación de Indemnización por Vejez;
- escenario no elegible antes de la banda anticipada;
- factor mensual `0.9927` a los 23 meses desde el límite inferior de la banda;
- combinación de factor proporcional y factor de reducción;
- integración del caso femenino con una fecha personalizada anticipada;
- conservación de la regresión normal B/.741.59;
- conservación del escenario +1 año B/.765.67 con año calendario parcial proyectado.

La prueba del año parcial confirma que el año proyectado conserva sus cuotas y salario prorrateados y puede formar parte de los diez mejores años cuando su total anual así lo determina.

## Paso 6C.2 — Indemnización por Vejez

`tests/test_indemnizacion_vejez.py` agrega regresiones específicas de la prestación de pago único:

- 120 cuotas con salario base mensual B/.1,000.00 → mensualidad hipotética B/.600.00, factor `120 / 6 = 20` y pago único B/.12,000.00;
- 179 cuotas → se conserva el cociente `179 / 6` sin truncarlo y el pago resultante es B/.17,900.00 con la base controlada del caso;
- desde el 01/03/2036 el clasificador deja de conceder Indemnización por Vejez y marca la transición SUCGS;
- la capa integrada del Paso 6 entrega la prestación como `INDEMNIZACION`, sin confundir el pago único con `pension_mensual_estimada`.
- los campos exclusivos de pensión proporcional se devuelven como `null` en una indemnización, evitando que `0` se interprete como un factor aplicado.

Estas pruebas usan datos sintéticos y no contienen información personal real.


## Paso 6D.1 — pruebas preliminares del Subsistema Mixto

`tests/test_mixto.py` incorpora cinco casos sintéticos:

1. **Normal Mixto con ambos componentes disponibles**
   - diez años con salario superior al tope BD;
   - salario base BD = B/.500.00;
   - 300 cuotas;
   - pensión BD = B/.331.25;
   - saldo CAP = B/.100,000.00;
   - bono sintético = B/.5,000.00;
   - divisor actuarial sintético = `200`;
   - pensión programada CAP = B/.525.00;
   - total Mixto = B/.856.25.

2. **CAP sin divisor actuarial**
   - el motor no inventa un parámetro;
   - `pension_programada_mensual = None`;
   - el total Mixto permanece en `None`.

3. **Modalidad proporcional**
   - 200 cuotas;
   - componente BD = B/.250.00 bajo el caso controlado.

4. **Transición temporal**
   - retiro el 01/03/2032;
   - estado `TRANSICION_SUCGS`;
   - no se calcula una pensión Mixto.

5. **Opción SUCGS explícita**
   - el motor respeta la selección y no ejecuta cálculo Mixto.

Los valores `saldo = 100000`, `bono = 5000` y `valor actuarial = 200` son exclusivamente datos de prueba. No representan un saldo, bono ni divisor oficial de la CSS.

Con esta fase la suite completa contiene 33 pruebas automatizadas.

## Paso 6D.2 — devolución y garantía del CAP

`tests/test_mixto_prestaciones_cap.py` agrega seis casos:

1. pensión programada CAP con garantía de renta vitalicia informada sin modificar el monto inicial;
2. 200 cuotas a edad de referencia con `AUTO` → decisión CAP pendiente;
3. 200 cuotas con devolución explícita → pensión proporcional BD + devolución CAP como pago único;
4. 120 cuotas → indemnización BD + devolución CAP, ambas sumadas únicamente como pagos únicos;
5. intento de devolución antes de la edad de referencia → no disponible;
6. bono de reconocimiento no confirmado → cifra visible pero cálculo marcado como provisional.

La suite completa de esta subfase contiene **39 pruebas automatizadas**.

## Paso 6D.3 — integración visual y servicio Mixto

`tests/test_resultados_mixto.py` agrega dos regresiones de integración:

1. caso normal Mixto con 300 cuotas, saldo B/.100,000.00, bono B/.5,000.00 y divisor sintético `200` → total mensual B/.856.25;
2. caso proporcional con 200 cuotas y `AUTO` → `DECISION_CAP_PENDIENTE`, sin pensión mensual total.

Además se verifican compilación Python, sintaxis JavaScript, correspondencia entre identificadores DOM utilizados por `resultados.js` y el parcial HTML, y carga HTTP de las rutas principales.

La suite completa de esta subfase contiene **51 pruebas automatizadas**.

## Casos controlados SUCGS 6E.3

Caso maestro del artículo 196:

```text
Sexo: femenino
Fecha de nacimiento: 16/11/1969
Fecha de retiro: 16/11/2026
Edad: 57
Cuotas: 300
Saldo contributivo: B/.100,000.00
Factor legal: 4.77
Pensión contributiva: B/.477.00
Capa solidaria: sin complemento porque supera B/.265.00
```

Casos adicionales automatizados:

- 300 cuotas, 57 años, pensión contributiva B/.190.80 → complemento B/.74.20 → B/.265.00 después de la PGS;
- 180 cuotas, 65 años, pensión contributiva B/.108.80 → Pensión de Beneficio Mínimo B/.144.00;
- 100 cuotas, 65 años, pensión contributiva B/.108.80 → conserva B/.108.80;
- 180 cuotas, 65 años, pensión contributiva B/.163.20 → conserva B/.163.20;
- 240 cuotas, 65 años, pensión contributiva B/.108.80 → se prioriza artículo 195 y queda B/.265.00.

Los casos 6E.2 permanecen como regresiones de las capas contributiva y solidaria. En 6E.3 se añaden casos que completan o descartan la garantía del artículo 197.

### Artículo 197

1. 240 cuotas equilibradas: 120 cuotas en los primeros veinte años y 120 después, salario promedio B/.1,000.00, estabilidad confirmada y saldo B/.100,000.00. La pensión contributiva B/.477.00 se eleva a B/.600.00.
2. 180 cuotas equilibradas: 90 cuotas por tramo, salario promedio B/.1,000.00 y estabilidad confirmada. La tasa proporcional es 45 % y el resultado final B/.450.00.
3. Distribución insuficiente: 180 cuotas en los primeros veinte años y 60 después. La garantía no aplica y se conserva B/.477.00.
4. Estabilidad no confirmada: aunque las otras condiciones pasen, la pensión total permanece pendiente.
5. Año con una a cuatro cuotas: falla la condición anual del artículo 197.

## Paso 6E.4 — integración visual SUCGS

Se añaden regresiones de integración para dos escenarios:

1. Caso maestro de 297 cuotas reales más 3 proyectadas, con saldo B/.100,000.00 y factor 4.77. El historial consolidado suma 300 cuotas y conserva B/.477.00 cuando la garantía del artículo 197 no aplica.
2. Caso equilibrado de 240 cuotas con distribución 120/120, salario promedio B/.1,000.00 y saldo B/.100,000.00. La integración conserva el resultado de B/.600.00 de la garantía de reemplazo.

La suite completa alcanza 57 pruebas automatizadas.
