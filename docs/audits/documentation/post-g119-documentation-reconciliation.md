# Reconciliación integral de documentación post-G119

**Estado:** reconciliación documental completada; gate integral final requerido para cierre Git
**Baseline técnico:** G119/E05 — `0.1.19.05-beta`
**Publicación vigente:** `v0.1.19.05-beta`
**Commit publicado de referencia:** `9424ea854f859a24fd01fe83bdf5d476b52fc213`
**Siguiente candidato reservado:** UX.5 R1 — G120/E01 — `0.1.20.01-beta`
**Fecha de auditoría:** 2026-08-30 / 2026-08-31

## 1. Propósito

Esta auditoría registra la reconciliación documental ejecutada después de la
publicación de DEV.2 R6 como G119/E05.

El trabajo no constituye un nuevo bloque funcional, no acepta UX.5 R1 y no
consume G120. Su finalidad es asegurar que la documentación viva, los
estándares, el gobierno, la seguridad, la normativa y la estructura del
repositorio describan de manera coherente el estado realmente publicado.

## 2. Alcance documental

La línea base previa a crear esta auditoría contenía 160 archivos Markdown
rastreados:

- 58 documentos vivos;
- 25 documentos de auditoría;
- 64 documentos históricos;
- 9 plantillas;
- 4 documentos de soporte.

La revisión distinguió deliberadamente documentación vigente de evidencia
histórica.

`docs/archive/` y las auditorías cerradas no fueron modernizados
mecánicamente. Una afirmación antigua se conserva cuando describe
correctamente el estado existente en el checkpoint documentado.

## 3. Estado revision-aware reconciliado

La verdad vigente queda establecida de la siguiente forma:

- DEV.2 R6 está cerrado, aceptado y publicado como G119/E05;
- la versión vigente es `0.1.19.05-beta`;
- el tag formal vigente es `v0.1.19.05-beta`;
- G120/E01 permanece reservado para UX.5 R1;
- UX.5 R1 continúa como candidato y no se considera aceptado;
- esta reconciliación documental no modifica `VERSION` ni consume un Global.

Se sincronizaron, cuando correspondía, README, CHANGELOG, RELEASES,
SECURITY, VERSIONING, gobierno, roadmap, ledger, validación, proceso de
release, trazabilidad y manifiesto de publicación.

## 4. DEV.2 R6, identidad y seguridad

La documentación técnica quedó alineada con el contrato real del Portal
Developer.

Se distingue entre:

- cuentas humanas Developer locales;
- autenticación técnica Bearer heredada para la superficie técnica que aún la
  utiliza;
- identidades Developer persistentes en SQLite;
- revisión de seguridad persistente;
- objetos y tokens de sesión temporales mantenidos en memoria;
- roles y permisos deny-by-default;
- CSRF y revalidación de contraseña para operaciones sensibles;
- revocación e invalidación por revisión de seguridad;
- kill switch `MRP_ADMIN_ENABLED`.

La documentación deja explícito que las cuentas Developer no son cuentas del
Asegurado(a) y que el almacén administrativo no constituye persistencia de la
simulación previsional.

También quedaron documentadas las variables de configuración relevantes del
Portal Developer y sus rutas vigentes.

## 5. Reconciliación normativa

La revisión actualizó el marco normativo y sus fuentes sin inventar una
reconciliación jurídica no demostrada.

Se dejó constancia de que:

- el 18/08/2026 fue comunicado institucionalmente como fecha operativa durante
  2026 y actualmente constituye un antecedente temporal;
- el Reglamento de Incorporación al Componente Contributivo de Capitalización
  Solidaria contiene una referencia al 17/03/2026;
- ambas evidencias se conservan;
- el proyecto no decide por inferencia cuál resuelve jurídicamente la
  diferencia;
- una reutilización futura de la fecha requiere verificar la fuente jurídica
  vigente;
- la revisión jurídica externa permanece como gate de REV.1 cuando corresponda.

Las modalidades SEBD, Mixto y SUCGS fueron sincronizadas con ese criterio sin
modificar motores previsionales.

## 6. Reconciliación de estándares

Se revisaron y sincronizaron los estándares canónicos de:

- estructura del repositorio;
- raíz y artefactos locales;
- ciclo de vida de artefactos;
- nomenclatura;
- documentación;
- archivos.

Las referencias que todavía trataban NOR.2 como una actuación futura fueron
actualizadas cuando pertenecían a documentación viva.

Los documentos históricos mantienen el lenguaje correspondiente a su
checkpoint.

## 7. Auditoría estructural

El inventario real produjo:

- 526 archivos rastreados por Git;
- 50 directorios canónicos derivados de `git ls-files`;
- 0 archivos no rastreados;
- 50 directorios canónicos representados finalmente en el árbol del README.

El árbol del README fue reconstruido para reflejar exactamente las áreas
versionadas y sus subdirectorios canónicos.

Entre las áreas incorporadas o explicitadas se encuentran:

- `app/cli/`;
- subdirectorios de `.github/`;
- `app/static/css/`, `app/static/img/` y `app/static/js/`;
- `assets/brand/` y sus derivados;
- subáreas de `docs/archive/`;
- subáreas de `docs/audits/`;
- subáreas de `docs/templates/`;
- `tests/validation_cases/`.

También se documentó `app/cli/admin.py` como parte de la arquitectura
administrativa Developer.

## 8. Directorios físicos no canónicos

La inspección física detectó 377 directorios sin contenido rastreado.

Ese número no representa 377 anomalías: la mayoría pertenecía a `.venv/` y a
subdirectorios de dependencias instaladas.

También se verificaron como legítimos e ignorados:

- `.pytest_cache/`;
- `__pycache__/`;
- `.venv/`;
- `logs/`;
- `logs/diagnostico/`;
- `data/developer/`.

`data/developer/` y `logs/` pueden contener estado local útil y no deben
eliminarse automáticamente.

Las cachés regenerables pueden limpiarse sin afectar el repositorio, aunque no
forman parte del árbol Git.

## 9. Referencias a rutas

El barrido inicial marcó 45 referencias a rutas aparentemente inexistentes.

La revisión contextual las clasificó en:

- 24 referencias históricas, renombradas o retiradas deliberadamente;
- 19 patrones glob válidos;
- 1 ubicación local legítima e ignorada;
- 1 notación histórica de comando;
- 0 referencias rotas vigentes confirmadas.

Por ello no se modificaron referencias históricas únicamente para hacerlas
coincidir con la estructura actual.

## 10. Huérfanos, stubs y duplicados

La auditoría final de mantenimiento documental obtuvo:

- 0 documentos vivos o de soporte sin referencia entrante;
- 0 posibles stubs;
- 0 grupos de duplicados exactos;
- 0 grupos de duplicados normalizados.

Se detectaron inicialmente seis estándares vivos no mencionados directamente
en `docs/README.md`:

- `docs/standards/artifact-lifecycle.md`;
- `docs/standards/documentation-standards.md`;
- `docs/standards/file-standards.md`;
- `docs/standards/naming-conventions.md`;
- `docs/standards/repository-structure.md`;
- `docs/standards/root-and-local-artifacts.md`.

Los seis ya tenían función canónica y navegación mediante
`docs/standards/README.md`, por lo que no eran huérfanos. Se añadió navegación
directa desde `docs/README.md` para completar el índice transversal.

## 11. Decisiones de conservación y eliminación

No se identificó ningún Markdown que justificara eliminación, fusión o archivo
adicional.

Por tanto:

- no se eliminan documentos históricos con valor de auditoría;
- no se eliminan documentos vivos con consumidores;
- no se elimina documentación únicamente por contener rutas o estados
  históricos;
- no se crean stubs de compatibilidad para rutas antiguas;
- no se elimina estado local Developer o logs de forma automática;
- Git continúa siendo la evidencia primaria de versiones anteriores.

La ausencia de eliminaciones es una decisión sustentada por la auditoría, no
una omisión del alcance de limpieza.

## 12. Archivos creados durante la reconciliación

Se incorporan:

- `docs/audits/README.md` como índice de auditorías;
- esta auditoría de reconciliación documental post-G119.

No se crean nuevos artefactos temporales versionados. Los informes auxiliares
de exploración se generaron fuera del repositorio.

## 13. Regresiones documentales adaptadas

Dos regresiones históricamente estrictas fueron actualizadas para validar la
verdad publicada actual en vez de forzar lenguaje obsoleto:

- `tests/test_doc1_r4_live_state_sanitization.py`;
- `tests/test_rel_gov1_r2_live_publication_state.py`.

Los contratos históricos protegidos continúan preservados donde corresponde.

## 14. Validaciones intermedias

Durante la reconciliación se obtuvieron, entre otros, los siguientes gates:

- auditor Markdown: OK;
- identificadores: 16 familias / 46 identificadores;
- revisión documental principal: 64 pruebas / 34 subtests;
- regresiones documentales y de release: 42 pruebas / 61 subtests;
- estándares y NOR.2 estructural: 29 pruebas / 18 subtests;
- contrato de árbol: 50 directorios Git = 50 directorios documentados;
- `git diff --check`: limpio en los checkpoints revisados.

## 15. Gate integral final

El gate integral final forma parte del cierre de esta reconciliación y debe
ejecutarse sobre el árbol definitivo después de incorporar esta auditoría y
sus enlaces de navegación.

Los conteos exactos del gate, la firma del commit, los checks remotos y la
integración pertenecen a la evidencia de ejecución del cierre y no se congelan
anticipadamente en este documento. De esta forma, la auditoría permanece
válida antes y después de esa ejecución sin afirmar un resultado que todavía
no existía al redactarla.

## 16. Resultado

La reconciliación deja una documentación coherente con G119/E05 publicado y
con UX.5 R1 aún reservado como G120/E01.

El repositorio conserva la separación entre:

- estado vigente;
- evidencia histórica;
- auditorías;
- estándares;
- datos versionados;
- estado local no versionado.

No se identificó deuda documental que justifique bloquear el inicio posterior
de UX.5 R1, sujeto a superar primero el gate integral final, commit firmado,
PR y controles remotos de esta reconciliación.
