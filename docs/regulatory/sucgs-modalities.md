# Sistema Único de Capitalización con Garantía Solidaria (SUCGS)

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.19.05-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R3 — 2026-08-17
**Clasificación:** Normativa / Motor
**Revisión externa:** Pendiente en REV.1 antes de la primera versión oficial o de una decisión jurídica individual

[Normativa](regulatory-framework.md) · [Fuentes](regulatory-sources.md) · [Motor](../architecture/calculation-engine.md)

## 1. Capas implementadas

1. componente contributivo;
2. componente solidario no contributivo;
3. Pensión Garantizada Solidaria;
4. garantía de reemplazo modelada;
5. integración de resultado.

## 2. Componente contributivo

El JSON vigente modela:

```text
saldo / 1000 × factor actuarial por edad
```

El saldo se suministra explícitamente cuando no puede reconstruirse con fidelidad.

## 3. Factores

`regulations/sucgs.json` contiene la tabla de factores y su metadata de actualización.

No deben utilizarse fuera de su versión como si fueran permanentes.

## 4. Capa solidaria

Los valores B/.144 y B/.265 permanecen identificados como referencias versionadas sujetas a la normativa aplicable/actualizaciones.

## 5. Garantía de reemplazo

La implementación preevalúa condiciones que pueden obtenerse del historial y conserva como confirmación explícita las condiciones que no pueden inferirse de forma segura.

Una condición pendiente puede impedir cerrar el resultado.

## 6. Saldo y datos individualizados

No se fabrica un saldo solidario real desde datos insuficientes.

## 7. Fuentes

Consultar `regulatory-sources.md` y `regulations/sucgs.json`.

Artículos principales documentados: 152, 153, 194, 195, 196, 197 y 198.

## 8. Historia

`docs/archive/regulatory-privacy/sucgs-modalities-pre-gov1-3-r3.md`
