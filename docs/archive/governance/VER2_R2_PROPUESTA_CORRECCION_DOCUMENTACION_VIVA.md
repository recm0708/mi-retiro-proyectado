# VER.2 R2 — Propuesta de corrección de documentación viva

- Fecha local de generación: 2026-08-23T22:16:02
- Rama: `ver/ver2-r2-documentacion-viva-post-r1`
- HEAD: `b34d0bf`
- Base: `b34d0bf VER.2 R1 — auditoría de reconciliación post-DOC.1 (#57)`
- Fuente: `docs/VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md`

## 1. Hallazgos manuales detectados

### 1.x `docs/ARQUITECTURA.md:371`

```text
   L369: DEV.2 quedó cerrado documentalmente en R4 después de integrar R1, R2 y R3. R1 abrió la ruta interna, R2 añadió el visor diagnóstico seguro y la exportación ZIP sanitizada, R3 añadió el autodiagnóstico técnico local y R4 sincroniza la documentación viva del bloque.
   L370:
>> L371: La ruta usa `MRP_DEV_MODE` solo como indicador de activación diagnóstica, conserva `0.0.26-beta` como versión visible, no añade rutas públicas nuevas, no modifica motores previsionales, no crea tags y no adelanta el cierre transversal de VER.2.
   L372:
   L373: ## Política de estructura por extensión
```

- Decisión propuesta: `ACLARAR_SIN_CAMBIO_DE_FONDO`
- Acción propuesta: Mantener el sentido porque `0.0.26-beta` sigue siendo la versión visible/canónica, pero aclarar que no corresponde al candidato VER.2.

### 1.x `README.md:124`

```text
   L122: `0.0.22-beta` fue la primera versión formal adoptada bajo la política de GOV.1.2; `0.0.23-beta` cerró GOV.1.3; `0.0.24-beta` cerró integralmente GOV.1; `0.0.25-beta` cerró UX.4.6e; y `0.0.26-beta` cerró PLAN.1. Sus tags publicados permanecen firmados e inmutables.
   L123:
>> L124: Después de `v0.0.26-beta`, UX.4.6f–UX.4.6i continuaron históricamente sobre ese mismo valor de `VERSION`. VER.2 reconstruye todo el tramo sin inventar tags: el último estado aceptado de la base `7037addd` es **G070/E02**, cierre de UX.4.6i.
   L125:
   L126: La nueva familia beta usa `0.GG.RR.EE-beta`. El candidato actual de reconciliación es `0.0.71.01-beta` (G071/E01). Solo se convierte en estado aceptado si supera el ledger/validador, gate completo, PR/CI e integración; no se crean tags revision-aware retrospectivos para G001–G070.
```

- Decisión propuesta: `PRESERVAR_COMO_EXPLICACION_HISTORICA`
- Acción propuesta: Preservar como explicación histórica del tramo posterior a `v0.0.26-beta`, sin convertirlo en tag retroactivo ni versión publicada.

### 1.x `RELEASES.md:175`

```text
   L173: La segunda pasada de VER.2 reconoce dentro de PLAN.1 diez estados aceptados G051–G060: R1, R2A, R2B1, R2B2, R2C, R3A, R3B1, R3B2, R4.1 y R4.2. Esta granularidad revision-aware no crea ni mueve tags históricos.
   L174:
>> L175: ## 5. Estado posterior a `v0.0.26-beta` y candidato VER.2
   L176:
   L177: UX.4.6f, UX.4.6g, UX.4.6h y UX.4.6i se desarrollaron y cerraron históricamente **sin publicar un tag adicional y manteniendo `VERSION = 0.0.26-beta`**. VER.2 no inventa releases retroactivas para esos bloques; su posición se reconstruye en el ledger como G061–G070.
```

- Decisión propuesta: `REVISAR_TEXTO_EN_R2`
- Acción propuesta: Revisar manualmente en R2 antes de modificar.

## 2. Corrección mínima recomendada

R2 debe aplicar una corrección mínima sobre documentación viva para separar claramente:

- `0.0.26-beta` como versión canónica legacy vigente en `VERSION`;
- `v0.0.26-beta` como último tag formal;
- `0.0.71.01-beta` como candidato VER.2 G071/E01 no publicado;
- G001–G070 como estados aceptados reconstruidos, sin tags retroactivos.

## 3. Restricciones

- No modificar `VERSION`.
- No modificar `app/core/version.py`.
- No modificar `app/core/config.py`.
- No modificar `regulations/`, `data/` ni `_entregas/`.
- No crear tags.
