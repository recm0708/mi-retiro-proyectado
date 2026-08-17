# Subsistema Mixto — diseño y alcance del motor

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.22-beta`
**Revisión documental:** GOV.1.3 R3 — 2026-08-17
**Clasificación:** Normativa / Motor
**Revisión externa:** Pendiente

[Normativa](NORMATIVA.md) · [Fuentes](FUENTES_NORMATIVAS.md) · [Motor](MOTOR_DE_CALCULO.md)

## 1. Estructura

```text
Subsistema Mixto
├── Beneficio Definido
└── Ahorro Personal
    ├── pensión programada
    └── devolución total cuando proceda
```

Pensión mensual y pagos únicos permanecen separados.

## 2. Beneficio Definido

La participación salarial se limita conforme al parámetro versionado de **B/.500 mensuales**.

Con historial anual, la aproximación utilizada debe advertirse cuando sustituye detalle mensual real.

## 3. CAP

El motor exige saldo CAP informado/validado cuando corresponda.

No reconstruye la cuenta individual acumulando porcentajes simplificados sobre salarios anuales.

## 4. Bono

Se acepta un monto oficial/validado cuando corresponda. No se inventa desde historial insuficiente.

## 5. Pensión programada

Requiere el valor actuarial aplicable.

Los factores del SUCGS no se reutilizan como sustituto del divisor CAP.

## 6. Devolución

La devolución del CAP es una opción expresa cuando está disponible y se presenta como pago único.

## 7. Seguro de renta vitalicia

Se modela como garantía futura bajo las condiciones documentadas, no como aumento automático de la pensión inicial.

## 8. Transición

La implementación versiona:

- hasta 29/02/2032: cálculo Mixto;
- desde 01/03/2032: transición operativa a SUCGS.

La referencia distinta a 01/03/2036 del artículo 153 se conserva como discrepancia y se relaciona con la ADR correspondiente.

## 9. Fecha operativa 2026

La CSS continúa comunicando **18/08/2026** como fecha límite para quienes cumplen los requisitos de la opción.

Es una referencia **operativa temporal**, verificada documentalmente el 2026-08-17. Debe revalidarse antes de usarla fuera de ese contexto.

## 10. Fuentes

Consultar `FUENTES_NORMATIVAS.md` y `normativa/mixto.json`.

## 11. Historia

`docs/historico/normativa_privacidad/MODALIDADES_MIXTO_PRE_GOV1_3_R3.md`
