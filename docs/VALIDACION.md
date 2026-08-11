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
