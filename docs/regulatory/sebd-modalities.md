# Modalidades de retiro por vejez — SEBD

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.17.02-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R3 — 2026-08-17
**Clasificación:** Normativa / Motor
**Revisión externa:** Pendiente

[Normativa](regulatory-framework.md) · [Fuentes](regulatory-sources.md) · [Motor](../architecture/calculation-engine.md)

## 1. Alcance

El clasificador general modela:

- Normal;
- Anticipada;
- Proporcional;
- Proporcional Anticipada;
- Indemnización por Vejez cuando legalmente corresponda;
- estados no elegibles/transición.

## 2. Árbol general

```text
Banda anticipada
├── >= 240 cuotas → Anticipada
├── 180–239 → Proporcional Anticipada
└── < 180 → No elegible por esa vía

Edad de referencia o posterior
├── >= 240 → Normal
├── 180–239 → Proporcional
└── < 180 → posible Indemnización por Vejez
```

El árbol es una representación funcional de la implementación; la fuente jurídica prevalece.

## 3. Salario base

La implementación usa el historial disponible y el criterio de mejores años versionado.

Con historial anual:

- un año parcial no se anualiza artificialmente;
- conserva el salario efectivamente reportado;
- la granularidad anual puede diferir del detalle oficial mensual.

## 4. Anticipación

Los factores mensuales se encuentran en `regulations/sebd.json`.

No se interpolan factores reglamentarios inventados.

## 5. Proporcionalidad

Las modalidades proporcionales conservan de forma separada el factor por cuotas y, cuando corresponde, el factor de anticipación.

## 6. Indemnización por Vejez

Se modela como **pago único**, no como pensión mensual.

El JSON normativo conserva la frontera `2036-03-01` y el divisor reglamentario modelado.

## 7. Mínimos y máximos

El monto mínimo base sujeto a actualización no se presenta como valor vigente eterno.

Los máximos ordinario/ampliados se aplican únicamente cuando los requisitos disponibles permiten evaluarlos.

## 8. Regímenes especiales

No quedan absorbidos por el clasificador general. Requieren fuentes y pruebas propias.

## 9. Fuentes

Consultar `regulatory-sources.md`. Los artículos principales documentados por el proyecto son 178, 179, 180, 181, 186, 192 y 193.

## 10. Historia

`docs/archive/regulatory-privacy/sebd-modalities-pre-gov1-3-r3.md`
