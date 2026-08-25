# VER.2 R2 — Análisis de contradicciones post-R1

- **Fecha local de generación:** 2026-08-23T22:15:00
- Rama: `ver/ver2-r2-documentacion-viva-post-r1`
- HEAD: `b34d0bf`
- Base: `b34d0bf VER.2 R1 — auditoría de reconciliación post-DOC.1 (#57)`
- **Fuente:** `docs/VER2_R1_DECISION_OPERATIVA_POST_DOC1.md`

## 1. Objetivo

Revisar las 11 posibles contradicciones detectadas en VER.2 R1 antes de modificar documentación viva.

## 2. Criterio de lectura

Una referencia a `0.0.71.01-beta` junto con las frases `no versión publicada`, `no es versión publicada` o `no es tag formal` no se considera contradicción real; se clasifica como negación explícita.

Una referencia a `0.0.26-beta` como versión candidata de VER.2 sí debe revisarse, porque el candidato operativo de VER.2 es `0.0.71.01-beta`.

## 3. Resumen

| Clasificación R2 | Total |
|---|---:|
| `FALSA_CONTRADICCION_NEGACION_EXPLICITA` | 7 |
| `PRESERVAR_ANCLA_HISTORICA` | 1 |
| `REVISAR_MANUALMENTE_R2` | 3 |

## 4. Detalle por hallazgo

### 4.1. `docs/ARQUITECTURA.md:371`

- Patrones R1: `0.0.26-beta, VER.2`
- Clasificación R2: `REVISAR_MANUALMENTE_R2`

```text
   L368:
   L369: DEV.2 quedó cerrado documentalmente en R4 después de integrar R1, R2 y R3. R1 abrió la ruta interna, R2 añadió el visor diagnóstico seguro y la exportación ZIP sanitizada, R3 añadió el autodiagnóstico técnico local y R4 sincroniza la documentación viva del bloque.
   L370:
>> L371: La ruta usa `MRP_DEV_MODE` solo como indicador de activación diagnóstica, conserva `0.0.26-beta` como versión visible, no añade rutas públicas nuevas, no modifica motores previsionales, no crea tags y no adelanta el cierre transversal de VER.2.
   L372:
   L373: ## Política de estructura por extensión
   L374:
```

### 4.2. `docs/LEDGER_REVISIONES_PRE_1_0.md:16`

- Patrones R1: `0.0.71.01-beta, VER.2, versión publicada`
- Clasificación R2: `FALSA_CONTRADICCION_NEGACION_EXPLICITA`

```text
   L13:
   L14: Estado vigente:
   L15:
>> L16: - `0.0.71.01-beta` sigue siendo candidato VER.2, no versión publicada.
   L17: - `0.0.26-beta` sigue siendo la versión canónica en `VERSION`.
   L18: - MANT.1 R7 quedó integrado en `main` como cierre operativo posterior.
   L19: - DOC.1 R1 no modifica el contador de versión; solo sincroniza documentación Markdown.
```

### 4.3. `docs/ROADMAP.md:20`

- Patrones R1: `0.0.71.01-beta, VER.2, tag formal, versión publicada`
- Clasificación R2: `FALSA_CONTRADICCION_NEGACION_EXPLICITA`

```text
   L17:
   L18: - `VERSION` continúa en `0.0.26-beta`.
   L19: - `v0.0.26-beta` continúa siendo el tag formal vigente.
>> L20: - `0.0.71.01-beta` continúa reservado como candidato de reconciliación VER.2; no es versión publicada ni tag formal.
   L21: - MANT.1 queda cerrado después de R5H, R6 y R7.
   L22: - DOC.1 R1 queda activo para auditar y actualizar la documentación Markdown vigente posterior a MANT.1.
   L23: - La primera versión oficial objetivo sigue siendo `1.0.0.0` con `Build 000001`, sujeta a los gates del plan maestro.
```

### 4.4. `GOVERNANCE.md:19`

- Patrones R1: `0.0.71.01-beta, VER.2, versión publicada`
- Clasificación R2: `FALSA_CONTRADICCION_NEGACION_EXPLICITA`

```text
   L16: - `VERSION` sigue siendo la fuente única de versión.
   L17: - `0.0.26-beta` sigue siendo la versión canónica vigente.
   L18: - `v0.0.26-beta` sigue siendo el último tag formal.
>> L19: - `0.0.71.01-beta` sigue siendo candidato VER.2, no versión publicada.
   L20: - MANT.1 quedó cerrado operativamente en R7.
   L21: - DOC.1 R1 queda activo como auditoría documental Markdown post-MANT.1.
   L22: <!-- DOC1-R1-POST-MANT1:END -->
```

### 4.5. `README.md:26`

- Patrones R1: `0.0.71.01-beta, VER.2, tag formal, versión publicada, revision-aware`
- Clasificación R2: `FALSA_CONTRADICCION_NEGACION_EXPLICITA`

```text
   L23: - **Versión canónica vigente:** `0.0.26-beta`, obtenida exclusivamente desde `VERSION` -> `VERSION`.
   L24: - **Último cierre integrado en `main`:** MANT.1 R7 — cierre operativo post-auditoría, PR #55, commit squash `57078f2`.
   L25: - **Estado de MANT.1:** cerrado operativamente después de R5H, R6 y R7. El cierre confirma documentación de auditoría, pruebas focalizadas, suite completa local y ausencia de cambios en archivos protegidos.
>> L26: - **Estado de VER.2:** reconciliación revision-aware pendiente. El candidato `0.0.71.01-beta` se conserva como candidato documental/contable, no como versión publicada ni tag formal.
   L27: - **Última versión formal legacy etiquetada:** `0.0.26-beta` — tag firmado e inmutable `v0.0.26-beta`.
   L28: - **Etapa:** desarrollo beta; repositorio público y ejecución orientada actualmente a entorno local.
   L29: - **Programa GOV.1:** cerrado — Auditoría, Gobierno y Trazabilidad Pre-Beta.
```

### 4.6. `README.md:124`

- Patrones R1: `0.0.26-beta, v0.0.26-beta, VER.2`
- Clasificación R2: `REVISAR_MANUALMENTE_R2`

```text
   L121:
   L122: `0.0.22-beta` fue la primera versión formal adoptada bajo la política de GOV.1.2; `0.0.23-beta` cerró GOV.1.3; `0.0.24-beta` cerró integralmente GOV.1; `0.0.25-beta` cerró UX.4.6e; y `0.0.26-beta` cerró PLAN.1. Sus tags publicados permanecen firmados e inmutables.
   L123:
>> L124: Después de `v0.0.26-beta`, UX.4.6f–UX.4.6i continuaron históricamente sobre ese mismo valor de `VERSION`. VER.2 reconstruye todo el tramo sin inventar tags: el último estado aceptado de la base `7037addd` es **G070/E02**, cierre de UX.4.6i.
   L125:
   L126: La nueva familia beta usa `0.GG.RR.EE-beta`. El candidato actual de reconciliación es `0.0.71.01-beta` (G071/E01). Solo se convierte en estado aceptado si supera el ledger/validador, gate completo, PR/CI e integración; no se crean tags revision-aware retrospectivos para G001–G070.
   L127:
```

### 4.7. `README.md:320`

- Patrones R1: `0.0.26-beta, VER.2, versión candidata, revision-aware`
- Clasificación R2: `PRESERVAR_ANCLA_HISTORICA`

```text
   L317:
   L318: Estas referencias conservan evidencia de regresiones históricas sin cambiar el estado vigente de VER.2.
   L319:
>> L320: - **Versión candidata de VER.2:** `0.0.26-beta` — referencia legacy preservada para las pruebas históricas previas a la reconciliación revision-aware.
   L321: - **GOV.1.8:** Auditoría final y cierre pre-beta de gobierno preservado como cierre histórico del programa GOV.1.
   L322: - **GOV.1.4:** Observabilidad y Developer Diagnostics cerrado.
   L323: - **GOV.1.5:** Seguridad, privacidad y transparencia cerrado internamente.
```

### 4.8. `RELEASES.md:175`

- Patrones R1: `0.0.26-beta, v0.0.26-beta, VER.2`
- Clasificación R2: `REVISAR_MANUALMENTE_R2`

```text
   L172:
   L173: La segunda pasada de VER.2 reconoce dentro de PLAN.1 diez estados aceptados G051–G060: R1, R2A, R2B1, R2B2, R2C, R3A, R3B1, R3B2, R4.1 y R4.2. Esta granularidad revision-aware no crea ni mueve tags históricos.
   L174:
>> L175: ## 5. Estado posterior a `v0.0.26-beta` y candidato VER.2
   L176:
   L177: UX.4.6f, UX.4.6g, UX.4.6h y UX.4.6i se desarrollaron y cerraron históricamente **sin publicar un tag adicional y manteniendo `VERSION = 0.0.26-beta`**. VER.2 no inventa releases retroactivas para esos bloques; su posición se reconstruye en el ledger como G061–G070.
   L178:
```

### 4.9. `RELEASES.md:177`

- Patrones R1: `0.0.26-beta, VER.2`
- Clasificación R2: `FALSA_CONTRADICCION_NEGACION_EXPLICITA`

```text
   L174:
   L175: ## 5. Estado posterior a `v0.0.26-beta` y candidato VER.2
   L176:
>> L177: UX.4.6f, UX.4.6g, UX.4.6h y UX.4.6i se desarrollaron y cerraron históricamente **sin publicar un tag adicional y manteniendo `VERSION = 0.0.26-beta`**. VER.2 no inventa releases retroactivas para esos bloques; su posición se reconstruye en el ledger como G061–G070.
   L178:
   L179: La base inmediatamente anterior a VER.2 es:
   L180:
```

### 4.10. `VERSIONING.md:19`

- Patrones R1: `0.0.71.01-beta, VER.2, versión publicada`
- Clasificación R2: `FALSA_CONTRADICCION_NEGACION_EXPLICITA`

```text
   L16:
   L17: - `VERSION` conserva `0.0.26-beta`.
   L18: - `v0.0.26-beta` continúa siendo el último tag formal vigente.
>> L19: - `0.0.71.01-beta` se conserva como candidato de reconciliación VER.2, no como versión publicada.
   L20: - MANT.1 quedó cerrado operativamente en R7 mediante PR #55 y commit squash `57078f2`.
   L21: - DOC.1 R1 no modifica la política de versionado; solo sincroniza documentación Markdown vigente después de MANT.1.
   L22:
```

### 4.11. `VERSIONING.md:195`

- Patrones R1: `0.0.26-beta, VER.2`
- Clasificación R2: `FALSA_CONTRADICCION_NEGACION_EXPLICITA`

```text
   L192: v0.0.26-beta
   L193: ```
   L194:
>> L195: Todos permanecen inmutables. Las fases UX.4.6f–UX.4.6i se desarrollaron históricamente manteniendo `VERSION = 0.0.26-beta`; VER.2 no falsea tags retroactivos para ellas. Su posición se conserva en el ledger mediante G061–G070.
   L196:
   L197: ## 8. Tags nuevos
   L198:
```

## 5. Decisión preliminar

- Las falsas contradicciones por negación explícita no requieren cambio de fondo.
- Las anclas históricas deben preservarse si el texto deja claro que no son estado vigente.
- Las ambigüedades donde `0.0.26-beta` aparezca como versión candidata de VER.2 deben corregirse en R2.
- R2 no modifica `VERSION`, `data/`, `regulations/`, `_entregas/` ni tags.
