# Motor de cálculo

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.71.01-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R2 — 2026-08-17
**Clasificación:** Técnica / Pública

Este documento describe la arquitectura matemática vigente. Las reglas jurídicas detalladas se mantienen en [regulatory-framework.md](../regulatory/regulatory-framework.md) y las fuentes en [regulatory-sources.md](../regulatory/regulatory-sources.md).

## 1. Pipeline

```text
Entrada confirmada
    ↓
Modelos Pydantic
    ↓
Servicios de normalización/integración
    ↓
Motor previsional
    ↓
Resultado específico
    ↓
Trazabilidad + resumen unificado
    ↓
Interfaz / comparador
```

JavaScript no implementa una segunda copia de las fórmulas principales.

## 2. Precisión monetaria

La lógica sensible usa `Decimal` y utilidades de `app/core/money.py`.

Criterios:

- preservar precisión interna;
- materializar importes a centavos;
- no redondear valores intermedios solo para coincidir con una referencia externa;
- no tratar factores/divisores actuariales como moneda.

## 3. Cuotas

El análisis recibe cuotas reales del año actual y supuestos futuros.

La proyección:

1. completa primero el año actual conforme al cierre esperado;
2. aplica la densidad futura a años posteriores;
3. mantiene diferenciadas cuotas acreditadas y proyectadas.

Una reconciliación posterior del Paso 3 obliga a revalidar antes de utilizar el resumen.

## 4. Historial y detalle actual

El historial anual conserva:

```text
año + cuotas + salario cotizado/reportado
```

Un año parcial no se anualiza artificialmente.

El detalle mensual/quincenal mantiene separados:

- salario disponible;
- salario acreditado;
- estado salarial;
- cuota mensual.

La base salarial futura puede ser manual o derivarse de información reciente completa según las opciones soportadas.

## 5. Importadores

Mi Retiro Seguro y Ficha Digital son **capas de entrada**.

No:

- ejecutan SEBD/Mixto/SUCGS;
- ajustan fórmulas para hacer coincidir una cifra PDF;
- convierten una prestación externa en parámetro del motor;
- persisten el archivo original.

Después de confirmar, sus datos pasan a los mismos contratos ordinarios que utiliza la captura manual.

## 6. Proyección salarial

Modalidades vigentes:

- salario constante;
- variación porcentual;
- salario futuro conocido;
- múltiples escenarios porcentuales.

La proyección compuesta conserva precisión interna y permanece separada del historial. El año inicial conserva la base; `PORCENTAJE` y cada tasa de `ESCENARIOS` se aplican sobre el salario proyectado del año anterior. `ESCENARIOS` no incorpora porcentajes predeterminados: si el usuario no proporciona al menos una tasa, el motor rechaza esa modalidad.

En `FUTURO_CONOCIDO` se calcula la tasa anual compuesta equivalente entre la base y el monto/año objetivo. El año objetivo materializa exactamente el monto indicado. Si el horizonte continúa después, ese monto se mantiene constante: no se prolonga automáticamente la tasa inferida más allá del dato aportado.

## 7. Línea temporal

`timeline.py` combina:

- historia real;
- año actual;
- futuro proyectado.

Antes de combinar etapas, `timeline.py` exige historial completo, total de cuotas coherente con Paso 2 y coincidencia de las cuotas del año actual. Así evita sumar cuotas restantes a una fotografía histórica distinta.

Cuando un período futuro contiene menos de doce cuotas, el salario cotizado proyectado se limita al período correspondiente. La referencia mensual del escenario viaja separada mediante `salario_mensual_proyectado`. Si no se proyectan cuotas, el salario cotizado es cero y el estado se identifica como `PROYECTADO_SIN_COTIZACION`.

## 8. Retiro

`retirement.py` construye escenarios de retiro a partir de:

- fecha de nacimiento/sexo;
- fecha de evaluación;
- último mes de cuotas;
- cuotas acreditadas;
- cierre del año;
- densidad futura;
- horizonte salarial.

El dato visible mensual se convierte a una fecha técnica; la precisión diaria no se inventa cuando la entrada solo tiene granularidad mensual.

## 9. SEBD

El motor se divide entre:

- cálculo normal base;
- clasificación/modalidades generales.

Modalidades generales implementadas según la documentación normativa:

- Normal;
- Anticipada;
- Proporcional;
- Proporcional Anticipada;
- Indemnización por Vejez;
- No elegible/transición cuando corresponda.

El salario base se construye con el historial disponible y los criterios versionados. Un dato faltante que impida separar cuotas antes/después de una referencia produce advertencia o limitación explícita.

## 10. Subsistema Mixto

El motor conserva dos componentes:

```text
Beneficio Definido
+
Ahorro Personal
```

El componente BD reutiliza la clasificación pertinente con parámetros propios.

El CAP utiliza saldos/bonos/valores actuariales explícitos. La aplicación no reconstruye una cuenta individual real sumando porcentajes simplificados sobre salarios anuales cuando no dispone de movimientos y rendimientos suficientes.

Pensión mensual y devoluciones/pagos únicos permanecen separados.

## 11. SUCGS

El motor se organiza por capas:

1. componente contributivo;
2. componente solidario;
3. Pensión Garantizada Solidaria cuando corresponde;
4. garantía de reemplazo modelada;
5. resultado total.

Los factores y valores versionables provienen de `regulations/sucgs.json`.

La aplicación no reconstruye un saldo solidario real a partir de datos insuficientes.

## 12. Resultados integrados

Los servicios `resultados_*.py` preparan una entrada coherente a cada motor usando el estado de Pasos 1–5.

Soportan dos modos:

- `PROYECTADO`;
- `SOLO_ACREDITADO`.

Ambos reutilizan los mismos motores; no existen fórmulas duplicadas para la fotografía acreditada.

## 13. Comparador

`comparator.py` ejecuta los servicios existentes para diferentes escenarios y normaliza salidas comparables.

No suma pagos únicos con pensiones mensuales ni crea una cuarta fórmula previsional.

## 14. Trazabilidad

`traceability.py` transforma resultados emitidos por los motores en una secuencia explicativa:

```text
dato
→ regla
→ fórmula
→ sustitución
→ resultado
→ redondeo/límite
→ fuente
```

La trazabilidad explica; no recalcula el monto jurídico.

## 15. Resultado unificado

`unified_result.py` adapta el resultado específico a un contrato transversal común para interfaz/comparación.

`calculo` continúa siendo el detalle específico del motor.

## 16. Referencias externas

Una referencia de Mi Retiro Seguro sirve para contraste del resultado y contexto del asegurado.

El motor actual **no se calibra** contra esa cifra. Diferencias pueden provenir de fecha del comprobante, datos históricos, proyecciones, granularidad o parámetros que la herramienta no posee.

## 17. Datos no confirmados

Saldo CAP, bono, valores actuariales, saldo solidario u otros datos individualizados que no puedan inferirse con seguridad permanecen explícitos como entrada/pendiente.

No se sustituyen por constantes personales de un caso de prueba.

## 18. Historia

La versión anterior se conserva en:

`docs/archive/technical/MOTOR_DE_CALCULO_PRE_GOV1_3_R2.md`

### UX.4.6g R1 — preanálisis de fechas de retiro

El servicio de Paso 5 construye fechas y cuotas estimadas, pero no decide elegibilidad. Los desplazamientos `-2`, `-1`, `0` y `+N` solo se materializan cuando llegan en `DatosRetiro`. `anios_adicionales` usa `[0]` por defecto. La opción `incluir_fecha_evaluacion_como_retiro` solo se acepta si la fecha de evaluación está dentro de la banda anticipada estándar versionada; la clasificación de pensión anticipada, proporcional anticipada, normal u otra prestación continúa en los motores del Paso 6.
