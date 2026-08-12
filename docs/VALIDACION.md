# Validación

La validación combina pruebas automatizadas, casos sintéticos controlados y regresiones anonimizadas contra resultados conocidos.

[Índice de documentación](INDICE.md) · [Normativa](NORMATIVA.md) · [Fuentes oficiales](FUENTES_NORMATIVAS.md)

## 1. Objetivo

Las pruebas deben detectar regresiones en:

- precisión monetaria;
- cuotas y fechas;
- proyección salarial;
- línea temporal;
- modalidades SEBD;
- componentes Mixto;
- capas SUCGS;
- servicios integrados del Paso 6.

## 2. Comandos de validación

Antes de consolidar cambios:

```powershell
python -m compileall app
python -m unittest discover -s tests -v
```

Estado antes del bloque 6F:

```text
Ran 57 tests
OK
```

El número de pruebas puede aumentar; lo importante es que la suite completa finalice en `OK`.

## 3. Cobertura automatizada actual

Archivos principales:

```text
tests/test_dinero.py
tests/test_proyeccion_salarios.py
tests/test_linea_tiempo.py
tests/test_retiro.py

tests/test_sebd.py
tests/test_sebd_modalidades.py
tests/test_indemnizacion_vejez.py
tests/test_resultados.py
tests/test_resultados_modalidades.py

tests/test_mixto.py
tests/test_mixto_prestaciones_cap.py
tests/test_resultados_mixto.py

tests/test_sucgs.py
tests/test_sucgs_capa_solidaria.py
tests/test_sucgs_reemplazo.py
tests/test_resultados_sucgs.py
```

## 4. Reglas para casos reales

Los documentos personales originales no se versionan.

Si una regresión deriva de un caso real:

1. conservar el original fuera de Git;
2. extraer únicamente los valores necesarios;
3. anonimizar fechas o datos cuando sea posible sin destruir la propiedad matemática que se prueba;
4. versionar solo el caso sintético/anonimizado;
5. documentar qué propiedad debe reproducirse.

Ver [tests/casos_validacion/README.md](../tests/casos_validacion/README.md).

## 5. Regresión SEBD anonimizada principal

Existe una regresión femenina anonimizada que reproduce una pensión mensual de:

```text
B/.741.59
```

Propiedades controladas:

- 281 cuotas históricas;
- diez mejores años conocidos;
- salario base aproximado de B/.1,163.28;
- tres bloques completos de 12 cuotas excedentes;
- tasa resultante de 63.75 %.

Esta regresión protege el cálculo normal y su precisión monetaria.

## 6. Caso masculino de edad de referencia

Se valida al menos:

- fecha de nacimiento masculina;
- edad de referencia de 62 años;
- fecha exacta de referencia;
- comportamiento de escenarios de retiro.

No se fuerza una coincidencia monetaria con una estimación oficial cuando el historial mensual necesario no está disponible.

## 7. Caso maestro sintético del asistente

Para pruebas visuales transversales se utiliza un caso sintético estable.

Datos base:

```text
Fecha de nacimiento: 16/11/1969
Sexo: femenino
Fecha de ingreso: 01/11/2001
Cuotas históricas al corte: 297
Cuotas 2026 al corte: 7
Cierre esperado 2026: 12
Cuotas futuras por año: 12
Salario mensual: B/.1,000.00
Proyección: constante
Retiro de referencia: 16/11/2026
Cuotas estimadas al retiro: 300
```

El historial sintético suma 297 cuotas y B/.297,000.00 de salario cotizado acumulado, con 2 cuotas en 2001 y años completos posteriores.

## 8. Validación SEBD del caso maestro

Con 300 cuotas y salario base B/.1,000.00:

```text
cuotas excedentes = 60
bloques de 12 = 5
incremento = 6.25 puntos porcentuales
tasa total = 66.25 %
pensión = B/.662.50
```

Resultado patrón:

```text
B/.662.50 mensuales
```

## 9. Validación Mixto del caso maestro

Datos específicos sintéticos:

```text
Saldo CAP: B/.100,000.00
Bono: B/.5,000.00
Bono confirmado: sí
Valor actuarial sintético: 200
Opción CAP: pensión programada
```

Resultado controlado:

```text
Componente BD: B/.331.25
Componente CAP: B/.525.00
Pensión total: B/.856.25
```

El valor actuarial 200 es **sintético para pruebas** y no representa un divisor oficial general.

También se validan:

- CAP sin divisor → cálculo incompleto;
- 200 cuotas + `AUTO` → decisión pendiente;
- 200 cuotas + devolución → B/.20,000.00 como pago único y B/.250.00 mensuales de BD;
- menos de 180 cuotas → indemnización BD y devolución CAP separadas;
- transición a SUCGS desde 01/03/2032.

## 10. Validación SUCGS — componente contributivo

Caso controlado:

```text
Edad: 57
Saldo: B/.100,000.00
Factor: 4.77
Divisor: 1,000
```

Resultado:

```text
100,000 / 1,000 × 4.77 = B/.477.00
```

## 11. Validación SUCGS — capa solidaria

### 11.1. Contributiva superior a garantía

```text
Contributiva: B/.477.00
Resultado después de capa solidaria: B/.477.00
```

### 11.2. Pensión Garantizada Solidaria

```text
Saldo: B/.40,000.00
Contributiva: B/.190.80
Referencia PGS: B/.265.00
Complemento: B/.74.20
Resultado: B/.265.00
```

### 11.3. Beneficio Mínimo a los 65

```text
Saldo: B/.20,000.00
Factor a 65: 5.44
Contributiva: B/.108.80
Valor mínimo universal: B/.144.00
Complemento: B/.35.20
Resultado: B/.144.00
```

## 12. Validación SUCGS — artículo 197

### 12.1. Garantía completa

Caso sintético equilibrado de 240 cuotas:

```text
Cuotas primeros 20 años: 120
Cuotas años restantes: 120
Salario promedio base: B/.1,000.00
Tasa mínima: 60 %
Objetivo: B/.600.00
Resultado contributivo previo: B/.477.00
Complemento: B/.123.00
Pensión total: B/.600.00
```

### 12.2. Garantía proporcional

Caso sintético de 180 cuotas:

```text
Cuotas por tramo: 90 / 90
Tasa proporcional: 45 %
Salario promedio base: B/.1,000.00
Objetivo: B/.450.00
Resultado previo: B/.144.00
Complemento: B/.306.00
Pensión total: B/.450.00
```

### 12.3. Distribución insuficiente

Caso de 240 cuotas con distribución 180 / 60:

```text
Condición 50/50: no cumple
Garantía art. 197: no aplica
Pensión final conservada: B/.477.00
```

### 12.4. Estabilidad pendiente

Si las condiciones objetivas cumplen pero la estabilidad salarial permanece sin confirmar:

```text
garantia_reemplazo_evaluada = false
calculo_total_disponible = false
pension_mensual_total_estimada = null
```

La aplicación no debe suponer el cumplimiento.

## 13. Validación visual del Paso 6

Antes de 6F se ha validado manualmente que:

- SEBD muestra modalidad, pensión y desglose;
- Mixto muestra BD, CAP, pensión mensual, pagos únicos y garantía;
- SUCGS muestra componente contributivo, capa solidaria, condiciones del artículo 197 y pensión total;
- los importes usan formato monetario coherente;
- los factores actuariales no se presentan como balboas;
- la navegación directa entre pasos funciona.

## 14. Criterios para nuevas pruebas

Toda nueva fórmula o interpretación normativa debe incluir al menos:

- caso positivo;
- caso límite;
- caso donde no aplica;
- caso de dato faltante cuando la ausencia sea legalmente relevante.

Si una corrección responde a un error encontrado manualmente, debe añadirse una regresión automatizada antes de cerrar el cambio.


## Comparador 6F.1

La suite incorpora `tests/test_comparador.py` con tres regresiones transversales:

1. SEBD reproduce B/.741.59 como base y B/.765.67 en +1 año, con diferencia de B/.24.08.
2. Mixto normaliza B/.856.25 como pensión mensual y mantiene separado cualquier pago único.
3. SUCGS normaliza el caso maestro de B/.477.00 como resultado mensual completo.

Estado después de 6F.1: **60 pruebas automatizadas en OK**.


## 12. Validación 6F.2

La suite contiene **63 pruebas**. `tests/test_trazabilidad.py` valida tres cadenas explicativas:

1. SEBD normal: salario base, tasa y resultado mensual;
2. Mixto: separación BD/CAP y suma mensual;
3. SUCGS: fórmula saldo ÷ 1,000 × factor y evaluación del artículo 197.

También se verifica que las fuentes expuestas por la trazabilidad utilicen URLs oficiales `https://` cargadas desde los JSON normativos.

## Validación 6F.3

Se valida que el catálogo incluya SEBD, Mixto y SUCGS, que sus fuentes tengan URLs HTTPS y títulos legibles y que `/metodologia` responda correctamente incluyendo el Texto Único, la Resolución 57,805-2025-J.D. y el acceso a Mi Caja Digital.

## Validación 6F.4

La suite queda en **69 pruebas automatizadas**. `tests/test_resultado_unificado.py` valida el contrato transversal en tres situaciones: 

1. SEBD: una Indemnización por Vejez se normaliza como **pago único** y no como pensión mensual;
2. Mixto: una decisión pendiente del CAP conserva `DECISION_REQUERIDA` y no finge un cálculo completo;
3. SUCGS: el caso completo de B/.477.00 se conserva como **pensión mensual** sin pago único.

Las pruebas integradas existentes de SEBD, Mixto y SUCGS también comprueban que los servicios anexen `resumen_unificado` sin modificar las cifras de regresión validadas. El comparador consume este resumen común y continúa calculando diferencias sin replicar fórmulas previsionales.

