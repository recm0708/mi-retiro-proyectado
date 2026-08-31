# Subsistema Mixto — diseño y alcance del motor

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.19.05-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R3 — 2026-08-17
**Clasificación:** Normativa / Motor
**Revisión externa:** Pendiente en REV.1 antes de la primera versión oficial o de una decisión jurídica individual

[Normativa](regulatory-framework.md) · [Fuentes](regulatory-sources.md) · [Motor](../architecture/calculation-engine.md)

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

La CSS comunicó **18/08/2026** como fecha límite operativa para los
asegurados habilitados para ejercer la opción. Esa fecha ya transcurrió y se
conserva como antecedente temporal.

El artículo 4 del Reglamento de Incorporación al Componente Contributivo de
Capitalización Solidaria publicado en Gaceta Oficial 30314 contiene, en
cambio, la fecha **17/03/2026**.

La documentación conserva esta discrepancia sin resolverla por inferencia.
Antes de utilizar una fecha de opción para una decisión individual o una regla
ejecutable debe verificarse la fuente jurídica vigente que explique o
sustituya esa diferencia.

Última verificación documental: **2026-08-30**.

## 10. Fuentes

Consultar `regulatory-sources.md` y `regulations/mixto.json`.

## 11. Historia

`docs/archive/regulatory-privacy/mixto-modalities-pre-gov1-3-r3.md`
