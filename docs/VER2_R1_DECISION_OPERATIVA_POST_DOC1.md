# VER.2 R1 — Decisión operativa post-DOC.1 R1

- Fecha local de generación: 2026-08-23T21:55:30
- Rama: `ver/ver2-r1-reconciliacion-post-doc1`
- HEAD: `d991890`
- Base: `d991890 DOC.1 R1 — auditoría Markdown post-MANT.1 (#56)`
- Bloque anterior cerrado: `DOC.1 R1`
- Objetivo de esta fase: auditoría, clasificación y decisión; sin modificación de versionado real.

## 1. Decisión principal

VER.2 R1 queda definido como una fase de reconciliación documental y técnica previa a cualquier cambio de versión.

Durante VER.2 R1:

- No se modifica `VERSION`.
- No se modifica `app/core/version.py`.
- No se modifica `app/core/config.py`.
- No se modifica `regulations/`, `data/` ni `_entregas/`.
- No se crea tag.
- No se declara `0.0.71.01-beta` como versión publicada.
- No se consume el candidato VER.2.

## 2. Estado canónico preservado

- `VERSION` permanece en `0.0.26-beta`.
- `v0.0.26-beta` permanece como último tag formal.
- `0.0.71.01-beta` permanece como candidato VER.2 G071/E01.
- DOC.1 R1 queda como línea base documental post-MANT.1.
- MANT.1 permanece cerrado operativamente.

## 3. Resultado de clasificación

La matriz VER.2 R1 clasificó `1601` coincidencias relacionadas con VER.2, versiones beta, tags formales y referencias `revision-aware`.

| Categoría | Decisión VER.2 R1 |
|---|---|
| `PROTEGIDO_NO_MODIFICAR` | Se preserva sin cambios. |
| `PRESERVAR_EVIDENCIA_CERRADA` | Se preserva como evidencia histórica o auditoría cerrada. |
| `PRESERVAR_PRUEBA_REGRESION` | Se preserva como contrato de compatibilidad. |
| `PRESERVAR_ANCLA_HISTORICA` | Se preserva como ancla explícita, no como estado vigente. |
| `REVISAR_DOCUMENTACION_VIVA` | Pasa a VER.2 R2 para revisión controlada. |
| `REVISAR_POSIBLE_CONTRADICCION` | Pasa a VER.2 R2 como prioridad alta. |
| `REVISAR_MANUALMENTE` | Se conserva en inventario; se revisa solo si afecta al cierre de VER.2. |

## 4. Documentos vivos priorizados para VER.2 R2

- `README.md`
- `CHANGELOG.md`
- `GOVERNANCE.md`
- `RELEASES.md`
- `SECURITY.md`
- `VERSIONING.md`
- `docs/ARQUITECTURA.md`
- `docs/DEV2_CENTRO_DESARROLLO.md`
- `docs/INDICE.md`
- `docs/LEDGER_REVISIONES_PRE_1_0.md`
- `docs/MATRIZ_DECISION_REVISIONES_VER2.md`
- `docs/MATRIZ_TRAZABILIDAD.md`
- `docs/PLAN_MAESTRO_HACIA_1_0.md`
- `docs/PROCESO_RELEASE.md`
- `docs/ROADMAP.md`
- `docs/TRANSPARENCIA.md`

## 5. Posibles contradicciones detectadas

Las siguientes filas se trasladan a VER.2 R2 como prioridad alta:

| Archivo | Línea | Decisión | Patrones | Texto |
|---|---:|---|---|---|
| `docs/ARQUITECTURA.md` | 371 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.26-beta, VER.2` | La ruta usa `MRP_DEV_MODE` solo como indicador de activación diagnóstica, conserva `0.0.26-beta` como versión visible, no añade rutas públicas nuevas, no modifica motores previsionales, no crea tags y no adelanta el c... |
| `docs/LEDGER_REVISIONES_PRE_1_0.md` | 16 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.71.01-beta, VER.2, versión publicada` | - `0.0.71.01-beta` sigue siendo candidato VER.2, no versión publicada. |
| `docs/ROADMAP.md` | 20 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.71.01-beta, VER.2, tag formal, versión publicada` | - `0.0.71.01-beta` continúa reservado como candidato de reconciliación VER.2; no es versión publicada ni tag formal. |
| `GOVERNANCE.md` | 19 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.71.01-beta, VER.2, versión publicada` | - `0.0.71.01-beta` sigue siendo candidato VER.2, no versión publicada. |
| `README.md` | 26 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.71.01-beta, VER.2, tag formal, versión publicada, revision-aware` | - **Estado de VER.2:** reconciliación revision-aware pendiente. El candidato `0.0.71.01-beta` se conserva como candidato documental/contable, no como versión publicada ni tag formal. |
| `README.md` | 124 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.26-beta, v0.0.26-beta, VER.2` | Después de `v0.0.26-beta`, UX.4.6f–UX.4.6i continuaron históricamente sobre ese mismo valor de `VERSION`. VER.2 reconstruye todo el tramo sin inventar tags: el último estado aceptado de la base `7037addd` es **G070/E0... |
| `README.md` | 320 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.26-beta, VER.2, versión candidata, revision-aware` | - **Versión candidata de VER.2:** `0.0.26-beta` — referencia legacy preservada para las pruebas históricas previas a la reconciliación revision-aware. |
| `RELEASES.md` | 175 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.26-beta, v0.0.26-beta, VER.2` | ## 5. Estado posterior a `v0.0.26-beta` y candidato VER.2 |
| `RELEASES.md` | 177 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.26-beta, VER.2` | UX.4.6f, UX.4.6g, UX.4.6h y UX.4.6i se desarrollaron y cerraron históricamente **sin publicar un tag adicional y manteniendo `VERSION = 0.0.26-beta`**. VER.2 no inventa releases retroactivas para esos bloques; su posi... |
| `VERSIONING.md` | 19 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.71.01-beta, VER.2, versión publicada` | - `0.0.71.01-beta` se conserva como candidato de reconciliación VER.2, no como versión publicada. |
| `VERSIONING.md` | 195 | `REVISAR_POSIBLE_CONTRADICCION` | `0.0.26-beta, VER.2` | Todos permanecen inmutables. Las fases UX.4.6f–UX.4.6i se desarrollaron históricamente manteniendo `VERSION = 0.0.26-beta`; VER.2 no falsea tags retroactivos para ellas. Su posición se conserva en el ledger mediante G... |

## 6. Documentación viva detectada

Las referencias clasificadas como `REVISAR_DOCUMENTACION_VIVA` no se modifican en R1. Se trasladan a R2 para evaluar si deben quedar como estado vigente, candidato reservado, ancla histórica o texto obsoleto.

## 7. Criterio de cierre de VER.2 R1

VER.2 R1 puede cerrarse cuando existan:

- auditoría de reconciliación,
- matriz de decisión,
- decisión operativa,
- prueba de regresión mínima para proteger el alcance,
- validación local sin cambios en archivos protegidos.

## 8. Próximo bloque recomendado

Abrir VER.2 R2 para aplicar cambios controlados únicamente en documentación viva priorizada, sin modificar todavía `VERSION`, `data/`, `regulations/` ni tags.
