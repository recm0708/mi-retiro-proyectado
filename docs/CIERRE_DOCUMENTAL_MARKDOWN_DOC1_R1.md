# DOC.1 R1 — Cierre documental de auditoría Markdown post-MANT.1

## Resultado

DOC.1 R1 queda cerrado como auditoría integral de documentación Markdown posterior al cierre operativo de MANT.1 R7.

El trabajo revisó todos los archivos Markdown detectados en el repositorio, separó documentación vigente, documentación histórica, auditorías cerradas, documentos de soporte y archivos sin señales de desfase.

## Alcance revisado

- Total Markdown evaluados: `106`.
- Documentos marcados `ACTUALIZAR`: `15`.
- Documentos marcados `REVISAR_MANUALMENTE`: `8`.
- Documentos marcados `REVISAR_SOLO_SI_APLICA`: `7`.
- Documentos marcados `PRESERVAR_AUDITORIA_CERRADA`: `25`.
- Documentos marcados `PRESERVAR_HISTORICO`: `27`.
- Documentos marcados `SIN_CAMBIO_INICIAL`: `25`.

## Evidencia generada

- `AUDITORIA_MARKDOWN_POST_MANT1_DOC1_R1.md`
- `MATRIZ_DECISION_MARKDOWN_DOC1_R1.md`
- `CONTEXTO_ACTUALIZACION_MARKDOWN_DOC1_R1.md`
- `LINEA_BASE_DOCUMENTAL_POST_MANT1_DOC1_R1.md`
- `REVISION_SOLO_SI_APLICA_DOC1_R1.md`
- `CIERRE_DOCUMENTAL_MARKDOWN_DOC1_R1.md`

## Documentación vigente sincronizada

Se sincronizaron documentos raíz, documentación transversal, versionado, release, seguridad, gobierno, roadmap, validación, arquitectura, especificación funcional, trazabilidad, privacidad, transparencia, observabilidad y documentos de decisión relacionados.

La actualización distingue entre:

- estado vigente posterior a MANT.1;
- referencias históricas preservadas;
- candidato VER.2 no publicado;
- versión canónica vigente;
- evidencia de auditorías cerradas.

## Estado canónico después del cierre

- `VERSION` permanece en `0.0.26-beta`.
- `v0.0.26-beta` permanece como último tag formal vigente.
- `0.0.71.01-beta` permanece como candidato VER.2, no como versión publicada.
- MANT.1 queda cerrado operativamente después de R5H, R6 y R7.
- DOC.1 R1 queda cerrado como auditoría documental Markdown post-MANT.1.

## Límites respetados

DOC.1 R1 no modifica:

- fórmulas previsionales;
- motores de cálculo;
- parámetros normativos;
- `VERSION`;
- `app/core/version.py`;
- `app/core/config.py`;
- `regulations/`;
- `data/`;
- `_entregas/`.

## Validación DOC.1 R1

Se agrega regresión documental en:

- `tests/test_doc1_r1_auditoria_markdown_post_mant1.py`

La prueba protege que:

- exista la evidencia documental DOC.1 R1;
- la línea base post-MANT.1 preserve el estado canónico;
- `VERSION` permanezca en `0.0.26-beta`;
- `README.md` no promueva VER.2 como versión publicada;
- `SECURITY.md` no clasifique `0.0.26-beta` como candidata VER.2;
- la documentación vigente revisada no conserve frases de estado obsoleto;
- `docs/INDICE.md` liste la evidencia DOC.1 R1.
