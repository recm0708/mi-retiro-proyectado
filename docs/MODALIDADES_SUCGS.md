# Sistema Único de Capitalización con Garantía Solidaria (SUCGS)

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.26-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R3 — 2026-08-17
**Clasificación:** Normativa / Motor
**Revisión externa:** Pendiente

[Normativa](NORMATIVA.md) · [Fuentes](FUENTES_NORMATIVAS.md) · [Motor](MOTOR_DE_CALCULO.md)

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

`normativa/sucgs.json` contiene la tabla de factores y su metadata de actualización.

No deben utilizarse fuera de su versión como si fueran permanentes.

## 4. Capa solidaria

Los valores B/.144 y B/.265 permanecen identificados como referencias versionadas sujetas a la normativa aplicable/actualizaciones.

## 5. Garantía de reemplazo

La implementación preevalúa condiciones que pueden obtenerse del historial y conserva como confirmación explícita las condiciones que no pueden inferirse de forma segura.

Una condición pendiente puede impedir cerrar el resultado.

## 6. Saldo y datos individualizados

No se fabrica un saldo solidario real desde datos insuficientes.

## 7. Fuentes

Consultar `FUENTES_NORMATIVAS.md` y `normativa/sucgs.json`.

Artículos principales documentados: 152, 153, 194, 195, 196, 197 y 198.

## 8. Historia

`docs/historico/normativa_privacidad/MODALIDADES_SUCGS_PRE_GOV1_3_R3.md`
