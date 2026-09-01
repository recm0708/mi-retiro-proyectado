# Atestación histórica Git pre-UX.5

**Proyecto:** Mi Retiro Proyectado
**Fecha de auditoría:** 2026-09-01
**Base atestada:** `561d702f8c70aebfcc178e2351794ab5f3f01e57`
**Commit raíz:** `a0a9e09e603c95c18dbd48d44d4098ed4b95270e`
**Versión de aplicación preservada:** `0.1.19.05-beta`
**Clasificación:** Auditoría / Gobierno / Integridad Git
**Estado:** cerrado como snapshot histórico previo a UX.5

## 1. Motivo

El historial temprano del proyecto contiene commits creados antes de adoptar
firma criptográfica obligatoria y antes de consolidar el flujo ordinario por
Pull Request. Reescribir esos objetos para añadir firmas, cambiar mensajes o
rellenar números de PR destruiría sus SHA originales y obligaría a recrear
descendientes, firmas, tags y referencias históricas.

Esta atestación conserva el historial original y agrega una capa administrativa
auditable que no modifica ningún commit anterior.

## 2. Identidad HIST

Se define `HIST-NNNN` como el **ordinal determinista desde el commit raíz** en
el historial lineal alcanzable de `main`.

El snapshot atestado contiene:

- `HIST-0001`: `a0a9e09e603c95c18dbd48d44d4098ed4b95270e`;
- `HIST-0195`: `561d702f8c70aebfcc178e2351794ab5f3f01e57`;
- 195 commits en total;
- 0 merge commits reales.

`HIST` no se inserta en el mensaje del commit y no reemplaza el número de Pull
Request ni el identificador revision-aware G/E. Mientras `main` conserve
historial lineal y prohíba force push, el ordinal permanece estable.

El siguiente commit que se integre después de este snapshot será calculado como
`HIST-0196`.

## 3. Frontera criptográfica

La auditoría demuestra una frontera exacta, sin excepciones:

- `HIST-0001` a `HIST-0089`: 89 commits sin objeto de firma;
- `HIST-0090` a `HIST-0195`: 106 commits con objeto de firma;
- última entrada sin firma: `HIST-0089` /
  `07278f7a193ce964612d9697da57350691bf62c0`;
- primera entrada firmada: `HIST-0090` /
  `90e66a13eec554d616bb71a04e00da4ada68df54`;
- asunto de transición:
  `chore(gov): adoptar firma SSH y migracion controlada de tags`.

La ausencia de firma de los primeros 89 objetos se documenta como condición
histórica anterior a la política criptográfica. No se intenta una firma
retroactiva porque una firma nueva produciría objetos Git distintos.

## 4. Pull Requests y numeración

El primer número de PR explícitamente codificado en un asunto integrado es:

- `HIST-0092`;
- PR #9;
- `chore(gov): consolidar CI v7 y protecciones GitHub (#9)`.

Los números de PR son una secuencia independiente administrada por GitHub. Un
PR cerrado sin merge no genera un commit en `main`, y un commit directo o cuyo
asunto no contenga `(#PR)` no recibe retrospectivamente un número inventado.

Después del primer PR explícito existen 17 commits cuyo asunto no codifica un
número de PR. La atestación los conserva como
`sin_pr_explicito_en_asunto`; no presume una asociación que el propio objeto
commit no demuestra.

## 5. Idioma de mensajes históricos

R15 señaló 19 asuntos para revisión humana. La adjudicación final fue:

- 11 falsos positivos por prefijos técnicos convencionales con contenido ya en
  español;
- 2 asuntos con terminología mixta;
- 6 asuntos materialmente redactados en inglés.

Los mensajes originales permanecen inmutables. El manifiesto añade
`subject_canonical_es` para disponer de una lectura administrativa española
sin recrear ningún commit.

### Normalizaciones canónicas

- `HIST-0020` — original: `fix: incluir parametros normativos de indemnizacion por vejez`; canónico: `corrección: incluir parámetros normativos de indemnización por vejez`.
- `HIST-0036` — original: `refactor: alinear terminologia publica y trazabilidad previsional`; canónico: `refactorización: alinear terminología pública y trazabilidad previsional`.
- `HIST-0040` — original: `fix: evitar 404 temporal del favicon`; canónico: `corrección: evitar 404 temporal del favicon`.
- `HIST-0051` — original: `fix: cerrar validacion accesible y estabilidad de UX.4.3`; canónico: `corrección: cerrar validación accesible y estabilidad de UX.4.3`.
- `HIST-0067` — original: `test: desacoplar validaciones de versiones fijas`; canónico: `pruebas: desacoplar validaciones de versiones fijas`.
- `HIST-0070` — original: `test(ux): cubrir regresiones del rediseño UX.4.6a`; canónico: `pruebas(ux): cubrir regresiones del rediseño UX.4.6a`.
- `HIST-0073` — original: `test(ux): cubrir privacidad e importacion de UX.4.6b`; canónico: `pruebas(ux): cubrir privacidad e importación de UX.4.6b`.
- `HIST-0076` — original: `test(ux): cubrir cuotas e importacion contextual de UX.4.6c`; canónico: `pruebas(ux): cubrir cuotas e importación contextual de UX.4.6c`.
- `HIST-0084` — original: `test(gov): proteger estructura documental GOV.1.3 R1`; canónico: `pruebas(gov): proteger estructura documental GOV.1.3 R1`.
- `HIST-0105` — original: `docs(release): cerrar UX.4.6e en 0.0.25-beta (#22)`; canónico: `documentación(release): cerrar UX.4.6e en 0.0.25-beta (#22)`.
- `HIST-0107` — original: `fix(tests): eliminar SyntaxWarning antes de 0.0.26-beta (#24)`; canónico: `corrección(pruebas): eliminar SyntaxWarning antes de 0.0.26-beta (#24)`.
- `HIST-0140` — original: `VER.2 R5 — estabilización post-release (#61)`; canónico: `VER.2 R5 — estabilización posterior a la publicación (#61)`.
- `HIST-0156` — original: `security: iniciar SEC.2 R1 con hardening CodeQL (#77)`; canónico: `seguridad: iniciar SEC.2 R1 con endurecimiento CodeQL (#77)`.
- `HIST-0158` — original: `SEC.2 R4 — Security administrative audit and observability closure (#79)`; canónico: `SEC.2 R4 — auditoría administrativa de seguridad y cierre de observabilidad (#79)`.
- `HIST-0184` — original: `feat(dev): implement developer portal access (#107)`; canónico: `funcionalidad(dev): implementar acceso al portal Developer (#107)`.
- `HIST-0185` — original: `chore(release): promote DEV.2 R5 to G118/E04 (#108)`; canónico: `mantenimiento(release): promover DEV.2 R5 a G118/E04 (#108)`.
- `HIST-0186` — original: `docs(release): reconcile G118 publication state (#109)`; canónico: `documentación(release): reconciliar estado de publicación de G118 (#109)`.
- `HIST-0189` — original: `chore(release): promote DEV.2 R6 to G119/E05 (#112)`; canónico: `mantenimiento(release): promover DEV.2 R6 a G119/E05 (#112)`.
- `HIST-0194` — original: `maintenance: audit repository before UX.5 (#119)`; canónico: `mantenimiento: auditoría del repositorio previa a UX.5 (#119)`.

Los identificadores técnicos, nombres propios, nombres de herramientas y scopes
como `CodeQL`, `Developer`, `release`, `dev`, `UX.5` o `SyntaxWarning` se
preservan cuando aportan precisión técnica.

## 6. Tags

El snapshot contiene 38 commits con uno o más tags. Esta atestación no mueve,
reemite ni renombra tags y no altera GitHub Releases.

## 7. Evidencia machine-readable

La evidencia canónica se encuentra en
[`data/git-history-attestation.json`](../../../data/git-history-attestation.json).

El manifiesto registra, por cada commit:

- identidad `HIST-NNNN`;
- SHA original;
- fechas;
- asunto original;
- asunto canónico en español;
- presencia de firma;
- estado de verificación local observado directamente por Git;
- número de PR cuando está explícito en el asunto;
- tags que apuntan al commit.

La auditoría exploratoria R15 queda referenciada por sus hashes históricos:

- `historial-commits.json`: `77773B9D88E46FF80349DE2720C5FBA759D02F1913F07DCD499F61F54EBA553C`;
- ZIP R15: `360663C8A590756F19F8FF1D3E1F03A185331C07F1E50BE45324E1C888A1D735`.

La integración no depende de que esos artefactos temporales permanezcan en
`Downloads`. La atestación se reconstruye directamente desde los objetos Git de
la base `561d702f8c70aebfcc178e2351794ab5f3f01e57`, verificando SHA, orden,
asuntos UTF-8, firmas, PR explícitos y tags. Los hashes R15 se conservan como
referencia de la fase exploratoria previa.

## 8. Control permanente

El auditor
[`scripts/audit_git_history_attestation.py`](../../../scripts/audit_git_history_attestation.py)
comprueba que los primeros 195 commits de cualquier `HEAD` futuro coincidan
exactamente con el snapshot atestado y que la frontera 89/106 permanezca
intacta.

Las regresiones viven en
[`tests/test_git_history_attestation.py`](../../../tests/test_git_history_attestation.py).

## 9. Decisión

No se reescribe el historial. No se añaden firmas retroactivas a commits
antiguos. No se cambian mensajes históricos. No se inventan números de PR.

La trazabilidad se fortalece mediante:

1. SHA originales inmutables;
2. identidad ordinal `HIST`;
3. atestación firmada en un nuevo commit;
4. descripción canónica en español;
5. validación automática permanente.

Este mantenimiento no cambia `VERSION`, no consume G120/E01 y no inicia UX.5.
