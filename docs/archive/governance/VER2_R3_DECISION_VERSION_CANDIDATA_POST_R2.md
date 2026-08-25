# VER.2 R3 — Decisión de versión candidata post-R2

- **Fecha local de generación:** 2026-08-23T23:39:26
- Rama: `ver/ver2-r3-cierre-post-r2`
- HEAD base: `5e7e2b9`
- Base: `5e7e2b9 VER.2 R2 — documentación viva post-R1 (#58)`

## 1. Pregunta resuelta

Determinar si las revisiones VER.2 R1, R2 y R3 obligan a recalcular el candidato `0.0.71.01-beta` antes de promover una nueva versión.

## 2. Decisión

El candidato se mantiene en `0.0.71.01-beta` como VER.2 G071/E01.

R1, R2 y R3 se consideran correcciones, auditorías y cierres internos del mismo candidato G071/E01. No consumen G072, no incrementan EE y no publican versión nueva mientras no exista aceptación formal post-gate.

## 3. Fundamento

- La familia beta revision-aware vigente usa el formato `0.GG.RR.EE-beta`.
- La base previa a VER.2 queda cerrada como G070/E02.
- VER.2 reserva G071/E01 como candidato `0.0.71.01-beta`.
- Un candidato no aceptado puede corregirse manteniendo el mismo identificador mientras no se publique ni se etiquete.
- Los identificadores G001–G070 siguen siendo reconstrucción/auditoría y no crean tags retrospectivos.

## 4. Estado que no cambia en R3

- `VERSION` permanece en `0.0.26-beta`.
- `v0.0.26-beta` permanece como último tag formal.
- `v0.0.71.01-beta` no existe todavía.
- `0.0.71.01-beta` permanece como candidato VER.2 G071/E01, no como versión publicada.

## 5. Punto futuro de cambio de versión

La modificación de `VERSION` corresponde a una fase posterior de promoción controlada del candidato, después de cerrar R3 y validar que el candidato G071/E01 puede aceptarse.

Esa fase deberá modificar explícitamente las superficies de versión/runtime/documentación que correspondan, ejecutar suite completa, pasar PR/CI, integrarse a `main`, revalidarse post-merge y solo entonces crear el tag firmado `v0.0.71.01-beta`, si corresponde.

## 6. Restricciones

- R3 no modifica `VERSION`.
- R3 no modifica `app/core/version.py`.
- R3 no modifica `app/core/config.py`.
- R3 no modifica `regulations/`, `data/` ni `_entregas/`.
- R3 no crea tags.
- R3 no publica `0.0.71.01-beta`.
