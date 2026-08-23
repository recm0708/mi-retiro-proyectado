# Auditoría de nombres de carpetas — MANT.1 R5E

**Estado:** Vigente
**Aplicación revisada:** `0.0.26-beta`
**Checkpoint técnico:** MANT.1 R5E — estandarización de nombres de carpetas
**Fecha:** 2026-08-23
**Clasificación:** Técnica / Mantenibilidad

Esta auditoría documenta el cambio controlado de carpetas con nombres en español
hacia nombres técnicos en inglés. El objetivo es reducir ambigüedad para futuros
desarrolladores sin cambiar lógica previsional, textos visibles, rutas públicas
de la aplicación ni archivos de entrega local.

## 1. Alcance aplicado

R5E renombra únicamente carpetas técnicas rastreadas por Git y actualiza las
referencias que apuntaban a esas rutas: imports Python, rutas en pruebas,
referencias documentales, hipervínculos Markdown, CODEOWNERS, `.gitignore` y
cadenas de error asociadas a archivos normativos.

No se renombran archivos en esta revisión. Los nombres de archivos de `tests/`,
`scripts/`, `regulations/`, `data/` y `docs/` quedan para revisiones posteriores
separadas, con menor riesgo de ruptura.

## 2. Mapa de carpetas renombradas

| Carpeta anterior | Carpeta vigente | Motivo |
|---|---|---|
| `app/modelos/` | `app/models/` | Paquete técnico Python de modelos de datos. |
| `app/motores/` | `app/engines/` | Paquete técnico Python de motores previsionales. |
| `app/servicios/` | `app/services/` | Paquete técnico Python de servicios de integración. |
| `normativa/` | `regulations/` | Directorio técnico de parámetros JSON versionados. |
| `tests/casos_validacion/` | `tests/validation_cases/` | Carpeta técnica de casos de validación. |
| `docs/historico/` | `docs/archive/` | Archivo documental histórico. |
| `docs/historico/gobierno/` | `docs/archive/governance/` | Subarchivo histórico de gobierno. |
| `docs/historico/normativa_privacidad/` | `docs/archive/regulatory-privacy/` | Subarchivo histórico normativo y de privacidad. |
| `docs/historico/tecnico/` | `docs/archive/technical/` | Subarchivo histórico técnico. |
| `docs/historico/ux/` | `docs/archive/ux/` | Subarchivo histórico UX; solo cambia la ruta padre. |

## 3. Carpetas excluidas

| Carpeta | Decisión |
|---|---|
| `_entregas/` | Se conserva sin cambios porque agrupa entregables/evidencias generadas y puede contener rutas históricas o paquetes ya referenciados fuera del código operativo. |
| `.github/` | Se conserva por convención de GitHub. |
| `.githooks/` | Se conserva por convención local del repositorio. |
| `.venv/`, `.pytest_cache/`, `__pycache__/` | No forman parte del árbol fuente operativo y no se renombran. |
| `assets/`, `data/`, `scripts/`, `app/static/`, `app/templates/`, `docs/templates/` | Ya están en inglés o se mantienen por contrato técnico vigente. |

## 4. Referencias actualizadas

La revisión sincroniza referencias en:

- imports Python: `app.models`, `app.engines`, `app.services`;
- rutas de documentación e hipervínculos Markdown;
- referencias a parámetros JSON bajo `regulations/*.json`;
- `CODEOWNERS` para áreas sensibles;
- `.gitignore` para originales de validación fuera de Git;
- pruebas que leían rutas físicas antiguas;
- documentos históricos movidos a `docs/archive/`.

## 5. Riesgos controlados

El cambio afecta rutas internas y paquetes Python. Por eso la validación debe
cubrir importación de módulos, carga de parámetros JSON, documentación con rutas
actualizadas y ausencia de rutas técnicas antiguas.

R5E no cambia:

- `VERSION`;
- `APP_VERSION`;
- fórmulas previsionales;
- valores JSON de parámetros;
- contratos públicos de endpoints;
- rutas del navegador;
- ids, clases o selectores de interfaz;
- archivos dentro de `_entregas/`;
- carpetas convencionales con punto inicial.

## 6. Continuación

Después de R5E pueden trabajarse revisiones separadas para nombres de archivos:

- `MANT.1 R5F` — renombre controlado de archivos en `tests/`, `scripts/`,
  `regulations/` y `data/`;
- `MANT.1 R5G` — reordenamiento o renombre documental en `docs/`, evaluando
  primero qué archivos son vigentes, históricos o de auditoría.
