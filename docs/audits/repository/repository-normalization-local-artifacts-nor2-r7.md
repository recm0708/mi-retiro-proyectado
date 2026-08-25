# NOR.2 R7 — migración y depuración de artefactos locales

**Base Git:** `365ba5b`
**Rama de trabajo:** `nor/nor2-r7-local-artifacts`
**Fecha local de ejecución:** 2026-08-24
**Estado:** migración local aplicada y gate local final superado; integración remota pendiente
**Versión:** `0.0.71.01-beta`

## 1. Objetivo

NOR.2 R7 resuelve la excepción transitoria `_entregas/` identificada durante la
normalización del repositorio.

El objetivo es conservar únicamente evidencia local útil, retirar copias
redundantes demostrables y establecer `_deliverables/` como ubicación local
canónica sin incorporar estos artefactos al árbol Git.

## 2. Línea base

El preflight de R7 confirmó:

- `_entregas/`: **29 archivos**;
- tamaño total: **9,874,828 bytes**;
- archivos `.txt`: **20**;
- archivos `.patch`: **8**;
- archivos `.zip`: **1**;
- `_deliverables/`: **0 archivos**;
- grupos SHA-256 duplicados: **7**;
- nombres repetidos: **0**;
- colisiones hacia `_deliverables/`: **0**.

La revisión de los grupos duplicados determinó **8 copias redundantes** porque
uno de los grupos contenía tres archivos idénticos.

## 3. Decisión aplicada

Los 29 archivos originales se clasificaron de la siguiente forma:

- **20 archivos únicos conservados**;
- **8 duplicados exactos retirados**;
- **1 ZIP reproducible desde Git retirado**.

Después de la operación:

- `_deliverables/dev2/`: **2 archivos**;
- `_deliverables/ver2-r2/`: **18 archivos**;
- `_entregas/`: **retirado**;
- total de evidencias locales conservadas: **20**.

No se eliminó evidencia local única.

## 4. Evidencias DEV.2 conservadas

Se conservaron en `_deliverables/dev2/`:

1. `main_log_antes_limpieza_dev2.txt`;
2. `ramas_locales_antes_limpieza_dev2.txt`.

## 5. Evidencias VER.2 R2 conservadas

Se conservaron en `_deliverables/ver2-r2/`:

1. `VER2_G071_R2_antes_anclas_historicas.patch`;
2. `VER2_G071_R2_antes_anclas_suite_completa.patch`;
3. `VER2_G071_R2_antes_anclas_suite_completa.status.txt`;
4. `VER2_G071_R2_antes_cirugia.patch`;
5. `VER2_G071_R2_antes_cirugia.status.txt`;
6. `VER2_G071_R2_estado_verde_pre_limpieza.diffstat.txt`;
7. `VER2_G071_R2_estado_verde_pre_limpieza.name-status.txt`;
8. `VER2_G071_R2_estado_verde_pre_limpieza.patch`;
9. `VER2_G071_R2_estado_verde_pre_limpieza.status.txt`;
10. `VER2_G071_R2_final_completo_pre_commit.diffstat.txt`;
11. `VER2_G071_R2_final_completo_pre_commit.name-status.txt`;
12. `VER2_G071_R2_final_completo_pre_commit.patch`;
13. `VER2_G071_R2_final_completo_pre_commit.status.txt`;
14. `VER2_G071_R2_post_consolidacion_tracked.diffstat.txt`;
15. `VER2_G071_R2_post_consolidacion_tracked.patch`;
16. `VER2_G071_R2_untracked_pre_limpieza.txt`;
17. `VER2_PR35_NETO_929628d_R2.files.txt`;
18. `VER2_PR35_NETO_929628d_R2.name-status.txt`.

## 6. Duplicados SHA-256 retirados

Cada archivo retirado fue comparado nuevamente mediante SHA-256 contra el
representante preservado antes de eliminarse.

| Copia retirada | Representante conservado |
| --- | --- |
| `VER2_G071_R2_antes_anclas_historicas.status.txt` | `VER2_G071_R2_antes_anclas_suite_completa.status.txt` |
| `VER2_G071_R2_antes_consolidar_anclas.patch` | `VER2_G071_R2_estado_verde_pre_limpieza.patch` |
| `VER2_G071_R2_antes_consolidar_anclas.status.txt` | `VER2_G071_R2_estado_verde_pre_limpieza.status.txt` |
| `VER2_G071_R2_final_pre_commit.diffstat.txt` | `VER2_G071_R2_final_completo_pre_commit.diffstat.txt` |
| `VER2_G071_R2_final_pre_commit.name-status.txt` | `VER2_G071_R2_final_completo_pre_commit.name-status.txt` |
| `VER2_G071_R2_final_pre_commit.patch` | `VER2_G071_R2_final_completo_pre_commit.patch` |
| `VER2_G071_R2_final_pre_commit.status.txt` | `VER2_G071_R2_final_completo_pre_commit.status.txt` |
| `VER2_G071_R2_post_consolidacion.status.txt` | `VER2_G071_R2_estado_verde_pre_limpieza.status.txt` |

La operación retira únicamente copias byte por byte y conserva un representante
de cada evidencia.

## 7. ZIP reproducible retirado

El archivo:

`VER2_PR35_NETO_929628d.zip`

tenía un tamaño de **8,412,675 bytes**.

Su nombre referencia el commit:

`929628df38d4750fb103ffc79bdb81f8405535bb`

Ese commit corresponde al `head` histórico utilizado por el PR #35 de VER.2.

La comparación del contenido del ZIP contra el árbol Git de ese commit se hizo
sin depender de una extracción permanente.

Resultado:

- archivos Git: **329**;
- archivos ZIP: **329**;
- archivos comunes: **329**;
- solo en Git: **0**;
- solo en ZIP: **0**;
- contenido diferente: **0**.

Por tanto, el ZIP era una reproducción completa del estado ya preservado por
Git y podía retirarse sin pérdida de evidencia única.

## 8. Política resultante

`_deliverables/` es la ubicación local canónica para entregables y evidencias
que deban permanecer en el workspace pero fuera del repositorio versionado.

`_entregas/` queda retirado como ubicación activa y no debe recrearse.

Las entradas de ambos nombres se conservan en `.gitignore`:

- `_deliverables/`, para mantener fuera del repositorio los artefactos locales;
- `_entregas/`, como protección contra la reaparición accidental de la ruta
  heredada.

## 9. Manifest externo

Antes de retirar o mover archivos se generó un manifest detallado con hashes,
tamaños y decisiones.

El manifest permanece fuera del repositorio en la carpeta hermana:

`../nor2_temporal/nor2-r7-migration-manifest.txt`

No se versiona porque documenta el estado físico local y contiene la
trazabilidad exhaustiva de la operación.

## 10. Invariantes preservados

R7 no modifica:

- motores previsionales;
- normativa;
- contratos JSON;
- rutas públicas;
- comportamiento funcional;
- `VERSION`;
- `APP_VERSION`;
- historial revision-aware;
- tags publicados.

`VERSION` permanece en:

`0.0.71.01-beta`

SEC.2 permanece pausado.

## 11. Estado posterior a la migración

La migración local quedó aplicada satisfactoriamente:

- origen inicial: **29 archivos / 9,874,828 bytes**;
- conservados: **20**;
- duplicados exactos retirados: **8**;
- ZIP reproducible retirado: **1**;
- `_entregas/`: inexistente;
- `_deliverables/`: **20 evidencias locales**;
- árbol Git: sin cambios provocados por los artefactos ignorados.

El gate local final de R7 quedó completado satisfactoriamente:

- `python -m pytest -q`: **1024 pruebas + 4902 subtests — OK**;
- `python -m unittest discover -s tests -q`: **984 tests — OK**;
- `python -m pip check`: **OK**;
- `python -m compileall -q app tests`: **OK**;
- Node.js: **v24.19.0**;
- `node --check`: **18 archivos JavaScript — OK**;
- `git diff --check`: **OK**;
- `VERSION`: **`0.0.71.01-beta`**;
- `APP_VERSION`: **`0.0.71.01-beta`**;
- `_entregas/`: **inexistente**;
- `_deliverables/`: **20 archivos locales, 0 trackeados por Git**.

Queda pendiente únicamente integrar R7 mediante Pull Request, verificar CI y confirmar el cierre post-merge.

## 12. Siguiente revisión

Después de integrar R7, la única revisión restante de NOR.2 será:

**NOR.2 R8 — auditoría integral y cierre formal de la normalización.**

SEC.2 solo podrá reanudarse después del cierre satisfactorio de R8.
