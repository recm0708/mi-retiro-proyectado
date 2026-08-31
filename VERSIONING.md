# Política de versionado

**Proyecto:** Mi Retiro Proyectado
**Estado:** vigente desde GOV.1.2; revisada por PLAN.1 y VER.2
**Fecha de adopción:** 2026-08-17
**Revisión de transición a versión oficial:** 2026-08-19
**Revisión revision-aware:** 2026-08-22


<!-- DOC1-R1-POST-MANT1:START -->
## Estado post-MANT.1

La fuente canónica de versión continúa siendo `VERSION`.

Estado vigente:

- `VERSION` contiene `0.1.19.05-beta` y materializa G119/E05
  para DEV.2 R6.
- G119/E05 está publicado mediante el tag firmado
  `v0.1.19.05-beta`.
- G118/E04 permanece preservado mediante `v0.1.18.04-beta` como
  publicación anterior.
- G119 incorpora la revisión funcional R6 de DEV.2 con ordinal E05.
- G120/E01 (`0.1.20.01-beta`) queda reservado para UX.5 R1.
- DEV.2 queda cerrado después de R6.
- UX.5 es un bloque nuevo y por eso inicia su secuencia aceptable en E01.
- Las etapas posteriores no tienen Global preasignado más allá del
  candidato vigente.
- Un PR, squash, tag o GitHub Release que materializa el mismo estado
  no consume por sí solo otro Global.

Cualquier publicación requiere gate completo, PR/CI, revalidación,
tag firmado y evidencia reproducible.
<!-- DOC1-R1-POST-MANT1:END -->

## 1. Objetivo

Esta política identifica de forma auditable cada estado aceptado de Mi Retiro Proyectado y evita que versión visible, API, documentación, artefactos y Git describan estados diferentes.

VER.2 corrige una limitación de la política original `0.0.N-beta`: los hitos formales estaban bien identificados, pero las revisiones internas aceptadas entre releases no podían expresarse sin inventar betas retrospectivas o confundir commits con revisiones.

## 2. Fuentes canónicas

La fuente canónica de la versión de aplicación es el archivo raíz `VERSION`.

- `VERSION` contiene una sola línea con la versión de la aplicación.
- `app/core/version.py` valida y expone ese valor a Python.
- `app/core/config.py` importa `APP_VERSION`; no mantiene una copia literal.
- FastAPI usa `APP_VERSION` como versión de la aplicación.
- Jinja2 recibe `app_version` y el footer muestra el mismo valor.
- El contador y la procedencia de revisiones aceptadas se auditan en `docs/governance/pre-1-0-revision-ledger.md` y `data/pre-1-0-revision-ledger.json`.
- `app/core/version_ledger.py` valida continuidad, unicidad y codificación del ledger estructurado.
- `docs/governance/pre-1-0-pending-matrix.md` ordena el trabajo pendiente hacia 1.0 sin preasignar Globales futuros.
- La regla que determina qué cuenta y qué no cuenta se documenta en `docs/archive/governance/ver2-revision-decision-matrix.md` y `docs/archive/governance/pre-1-0-versioning-audit.md`.
- README, CHANGELOG, RELEASES, ROADMAP y el ledger deben corresponder al estado vigente cuando lo describan como actual.
- Los documentos de dominio pueden conservar la versión en la que fueron revisados; esa metadata es histórica de revisión documental y no una segunda fuente de la versión vigente.
- La numeración de **Build** es independiente de `VERSION` y solo se materializa cuando exista un proceso reproducible de generación de artefactos oficiales.

No se deben introducir versiones independientes en plantillas, JavaScript, motores o normativa.

## 3. Familias admitidas

Mi Retiro Proyectado reconoce tres familias de identificadores.

### 3.1. Familia beta legacy histórica

La historia ya publicada conserva:

```text
0.0.N-beta
```

Ejemplos:

```text
0.0.22-beta
0.0.25-beta
0.0.26-beta
```

Esta familia sigue siendo válida para leer y auditar estados históricos. Los tags `v0.0.1-beta` a `v0.0.26-beta` no se renombran ni se mueven.

Después del cierre de VER.2, **los estados beta nuevos no continúan incrementando esta familia legacy**.

### 3.2. Familia beta revision-aware

Los candidatos y estados nuevos gobernados por VER.2 usan:

```text
0.GG.RR.EE-beta
```

Donde:

- `G` es el contador global de estados aceptados;
- `GG = G // 100`;
- `RR = G % 100`, siempre con dos dígitos;
- `EE` es el ordinal aceptado dentro del bloque vigente, siempre con dos dígitos entre `01` y `99`.

La **revisión funcional `R#`** y el **ordinal aceptado `E##`** son conceptos distintos. Normalmente coinciden, pero pueden divergir cuando una revisión intermedia no consume Global. DEV.2 R5 es el caso canónico: R1–R3 consumieron E01–E03, R4 no consumió Global y R5 se acepta como **G118/E04**. El siguiente estado aceptado del mismo bloque, DEV.2 R6, usa por tanto **G119/E05**. El ledger puede declarar `functional_revision` para que la publicación muestre la revisión funcional correcta sin alterar `EE`.

Ejemplos:

```text
G001 / E01 -> 0.0.01.01-beta
G070 / E02 -> 0.0.70.02-beta
G071 / E01 -> 0.0.71.01-beta
G100 / E03 -> 0.1.00.03-beta
G425 / E12 -> 0.4.25.12-beta
```

Los identificadores revision-aware usados en el ledger para G001–G070 son **identificadores de reconstrucción/auditoría**. No existieron como versiones publicadas y no autorizan tags retroactivos.

### 3.3. Versiones oficiales

Cuando todos los gates de producto se hayan cerrado, la primera versión oficial prevista sigue siendo:

```text
1.0.0.0
```

La versión oficial usa cuatro componentes:

```text
MAYOR.MENOR.PARCHE.REVISIÓN
```

Semántica:

- **MAYOR**: cambios incompatibles o nueva generación del producto;
- **MENOR**: capacidades compatibles de alcance relevante;
- **PARCHE**: correcciones o mejoras compatibles que justifican una nueva versión funcional;
- **REVISIÓN**: hotfix o revisión puntual de una versión oficial ya publicada.

La numeración de cuatro componentes es una convención propia del producto y no se presenta como SemVer estricto.

## 4. Qué incrementa el contador global

Una entrada consume `G` únicamente si representa un **estado aceptado y auditable**.

Reglas:

1. los 21 estados retrospectivos GOV.1.1 cuentan una vez cada uno;
2. una revisión interna cuenta cuando queda documentada como cerrada, completada o validada y el proyecto avanza desde ese estado;
3. un candidato pendiente de validación, PR, CI, tag o revisión manual no cuenta todavía como estado aceptado;
4. un intento que falla el gate no consume un Global nuevo;
5. los commits `feat/test/docs` de la misma revisión no se cuentan por separado;
6. PR, squash, CI y tag son evidencia de un estado y no generan otra revisión cuando solo materializan el mismo estado;
7. un mantenimiento técnico, de seguridad, gobierno, dependencias o documentación puede contar si crea un estado materialmente distinto, validado y aceptado; un checkpoint que solo agrupa estados ya contabilizados no cuenta de nuevo;
8. no se inventan retrospectivamente revisiones que nunca existieron.

La aplicación concreta de estas reglas está auditada en `docs/archive/governance/ver2-revision-decision-matrix.md`.

## 5. Contador global reconstruido

La base `main` en `7037addd44253e528c77460b678d2b3ccd540dd5`, correspondiente al cierre de UX.4.6i, contiene según la segunda pasada:

```text
70 estados aceptados
```

Conceptualmente, el último estado de esa base es:

```text
G070 / E02 -> 0.0.70.02-beta
```

Ese identificador **no reemplaza** el valor histórico que el árbol todavía mostraba (`0.0.26-beta`) ni crea un tag retrospectivo.

VER.2 R1 usa como candidato el siguiente estado:

```text
G071 / E01 -> 0.0.71.01-beta
```

G071 solo queda consumido como estado aceptado cuando VER.2 supera su ledger estructurado, validador, gate completo, PR/CI e integración. Si el candidato falla, se corrige manteniendo el mismo identificador candidato mientras no se acepte un estado distinto.

## 6. Reconstrucción histórica

GOV.1.1 reconstruyó retrospectivamente 21 estados anteriores:

```text
0.0.1-beta ... 0.0.21-beta
```

La reconstrucción se basa en los 80 commits reales existentes hasta `7941f58` y no reescribe commits históricos, autores, fechas, hashes o mensajes.

Durante la migración criptográfica del 2026-08-17 esos estados fueron materializados como tags retrospectivos firmados. Los tags apuntan al commit de cierre ya documentado, conservan su fecha real de creación, declaran en el mensaje la fecha histórica del hito y no existieron como tags en sus fechas históricas.

El antiguo valor `0.1.0` continúa clasificado como marcador histórico de desarrollo no publicado.

La reconstrucción revision-aware de G001–G070 es exclusivamente documental. No se crean tags `v0.GG.RR.EE-beta` para estados anteriores a VER.2.

## 7. Versiones formales legacy

`0.0.22-beta` fue el primer estado cuya numeración se adoptó deliberadamente bajo GOV.1.2.

Los hitos formales legacy cerrados son:

```text
v0.0.22-beta
v0.0.23-beta
v0.0.24-beta
v0.0.25-beta
v0.0.26-beta
```

Todos permanecen inmutables. Las fases UX.4.6f–UX.4.6i se desarrollaron históricamente manteniendo `VERSION = 0.0.26-beta`; VER.2 no falsea tags retroactivos para ellas. Su posición se conserva en el ledger mediante G061–G070.

## 8. Tags nuevos

Los tags formales usan el prefijo `v`.

Ejemplos:

```text
v0.0.71.01-beta
v1.0.0.0
v1.0.0.1
```

Después de la adopción de firma SSH:

- todo commit nuevo del mantenedor debe estar firmado cuando el flujo local lo permita;
- todo tag formal nuevo debe estar firmado;
- se verifica la firma antes de declarar el hito cerrado;
- `.github/allowed_signers` contiene las claves públicas autorizadas.

Los tags publicados son inmutables. Un tag formal nuevo no se crea dentro del PR del candidato: se crea únicamente después de merge, revalidación post-merge y verificación de firma, conforme a `docs/operations/release-process.md`.

## 9. Build oficial

Los artefactos distribuibles oficiales usarán un identificador de Build independiente:

```text
Build 000001
Build 000002
Build 000003
...
```

Reglas:

1. tiene exactamente seis dígitos decimales;
2. es monotónico y no se reutiliza;
3. no sustituye la versión de aplicación;
4. no forma parte del archivo `VERSION`;
5. identifica un artefacto reproducible concreto;
6. su fuente canónica se incorporará en REL.1;
7. no se muestra un Build ficticio durante beta.

Presentación prevista para la primera versión oficial:

```text
Mi Retiro Proyectado
Versión 1.0.0.0
Build 000001
```

## 10. Metadata documental

VER.2 separa dos conceptos que antes se confundían:

- **versión vigente/candidata de la aplicación:** únicamente `VERSION` y las superficies de estado actual;
- **versión en la que un documento fue revisado:** metadata histórica válida del propio documento.

Por tanto, un documento técnico que diga `Versión de aplicación revisada: 0.0.26-beta` puede conservar esa línea si realmente documenta la base sobre la que fue revisado. No tiene que reescribirse en cada incremento global si su contenido no cambió.

Los documentos que sí describen el estado actual —README, ROADMAP, SECURITY, índice operativo, CHANGELOG/RELEASES vigentes y ledger— deben actualizarse cuando corresponda.

## 11. Diferencia entre identificadores

No deben confundirse:

- versión de aplicación: `VERSION`;
- contador global/local pre-1.0: ledger revision-aware;
- Build oficial: artefacto reproducible;
- versión de normativa: `regulations/*.json`;
- versión jurídica de privacidad/términos: identificador propio del documento legal;
- versión de esquema de logs: Developer Diagnostics;
- versión de esquema de datos: futura persistencia migrable;
- visibilidad del repositorio: configuración de GitHub;
- estado de despliegue: decisión operativa independiente.

Un cambio en una categoría no obliga automáticamente a modificar las demás.

## 12. Gate de incremento

Antes de aceptar una nueva beta revision-aware se debe comprobar:

- que el estado anterior esté cerrado y trazable;
- que la revisión nueva cumpla la definición contable de estado aceptado;
- que código, pruebas y documentación dependiente coincidan;
- que el ledger Markdown y JSON tengan secuencia continua sin duplicados;
- que el validador estructurado acepte el ledger;
- que `VERSION` codifique exactamente el candidato que se está validando;
- que se ejecuten los gates exigidos para la etapa;
- que cualquier tag se cree únicamente después de integración y revalidación.

No existe una transición automática a `1.0.0.0` por alcanzar un valor determinado de `G`.

## 13. Primera versión oficial

La primera versión oficial objetivo sigue siendo:

```text
1.0.0.0
Build 000001
```

Antes de materializarla deben estar cerrados, como mínimo:

- alcance funcional previsto;
- validación de los tres motores;
- trazabilidad y explicación manual de cálculos;
- seguridad y privacidad;
- accesibilidad;
- persistencia/exportaciones que formen parte del alcance oficial;
- revisión normativa y jurídica prevista;
- QA integral;
- empaquetado reproducible;
- inventario de dependencias y avisos de terceros;
- hashes y firma del artefacto;
- documentación final de instalación, uso, soporte y release.

## 14. Prohibiciones

- No hardcodear la versión visible fuera de la fuente canónica.
- No usar Build como sustituto de `VERSION`.
- No reutilizar un número global ya aceptado para otro estado.
- No consumir un número global por un candidato fallido.
- No contar commits `feat/test/docs` como revisiones distintas del mismo estado.
- No crear tags revision-aware retrospectivos para G001–G070.
- No reescribir commits históricos para añadir firmas.
- No falsear fechas de creación de tags retrospectivos.
- No presentar un tag retrospectivo como si hubiera sido publicado en la fecha histórica.
- No modificar tags publicados para ocultar cambios posteriores.
- No usar la versión de aplicación como sustituto de la versión normativa o jurídica.
- No presentar una beta como versión oficial.
- No presentar `1.0.0.0` como alcanzada antes de cerrar sus gates.
- No reintroducir `0.1.0-beta.1` como objetivo vigente.

## 15. Guard de referencias históricas

PLAN.1 y VER.2 distinguen entre evidencia histórica legítima y planificación vigente.

Las expresiones antiguas (`0.1.0-beta.1`, beta pública, `0.0.N-beta`, identificadores de revisiones anteriores) pueden conservarse cuando forman parte de:

- snapshots bajo `docs/archive/`;
- auditorías/cierres/releases/ADR que describen un estado anterior;
- el ledger y la auditoría VER.2;
- pruebas históricas cuyo contrato sea precisamente preservar esa evidencia.

No pueden volver a utilizarse como objetivo vigente si la política actual las sustituyó.

Las regresiones documentales deben validar la diferencia entre historia y estado actual, no obligar a que toda documentación pasada copie indefinidamente el valor de `VERSION`.

<!-- ANCLAS_HISTORICAS_VER2_VERSIONING_CONSOLIDADAS -->

## Compatibilidad histórica preservada por VER.2

- No se crean tags revision-aware retrospectivos para G001–G070.
- Todo commit nuevo debe seguir el flujo ordinario de firma y verificación definido por la política del repositorio.
- Todo tag formal nuevo debe estar firmado conforme a la política vigente.
- Todo tag formal nuevo se crea con `git tag -s` y debe verificarse antes de declarar cerrado el hito.
- La visibilidad pública del repositorio de código no cambia por sí sola la versión de producto, el estado de despliegue ni la licencia aplicable.
- Las expresiones históricas sustituidas no pueden volver a utilizarse como objetivo vigente.
- El contrato histórico protegido por `tests/test_plan1_guard_referencias_historicas.py` evita borrar referencias legacy necesarias para auditar cierres anteriores.

### 3.1. Desarrollo pre-beta

Esta sección preserva la separación histórica entre visibilidad pública del repositorio y versión de producto.

## 12. Guard de referencias históricas

El guard de referencias históricas preserva menciones legacy necesarias para no borrar evidencia de cierres anteriores durante una reconciliación transversal.

## Reconciliación extraordinaria post-G070

La primera promoción revision-aware partió de un ledger cuya base auditada
terminaba en `7037addd` (G070). Antes de la promoción de VER.2 ya existían
estados aceptados posteriores —DEV.2, MANT.1 y DOC.1— que no habían sido
incorporados al contador. La auditoría de 2026-08-25 reconstruye la secuencia
completa hasta SEC.2 R6 y la fija en G108. AUD.SEC2 R1 queda aceptado posteriormente como G109/E01 mediante PR #83 y merge `ec1842d`.

Esta corrección es **prospectiva y documental**: preserva los tags publicados y
no genera tags retroactivos para G071–G108. El snapshot exacto del ledger G070
se conserva en `docs/archive/governance/pre-1-0-revision-ledger-g070.json` y la
matriz de reconciliación vive en
`docs/audits/governance/post-g070-revision-reconciliation.md`.
