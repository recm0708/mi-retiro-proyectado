# Política de versionado

**Proyecto:** Mi Retiro Proyectado
**Estado:** vigente desde GOV.1.2; revisada por PLAN.1 y VER.2
**Fecha de adopción:** 2026-08-17
**Revisión de transición a versión oficial:** 2026-08-19
**Revisión revision-aware:** 2026-08-22

<!-- NOR3-G122-PROMOTION:START -->
## Registro histórico — promoción G122-E01 post-NOR.3

> **Checkpoint histórico preservado.** Este bloque describe el estado inmediatamente posterior a la integración de NOR.3 y anterior a MANT.2 R1 / MANT.1 R8. No representa el estado vigente del repositorio; las secciones vigentes posteriores de este documento tienen precedencia.

- `VERSION` materializa `0.1.22.01-beta` para NOR.3 R8 / G122-E01.
- NOR.3 R1–R8 quedó integrado/aceptado mediante PR #162 / merge
  `b97cf61763479b80b8e8724b878089e8bb20fa00`.
- La revalidación automática de `main` quedó GREEN: Repository Quality Gate,
  Visual & Accessibility y CodeQL finalizaron en `success`.
- G123 es el siguiente Global disponible, pero **no tiene candidato ni bloque
  preasignado**.
- PERSIST.1 permanece planificado y no iniciado, sin Global preasignado.
- `v0.1.21.01-beta` / G121/E01 permanece como última publicación revision-aware
  hasta completar el tag/release firmado de G122/E01.
- `v0.1.22.01-beta` queda pendiente de creación/firma local y de la
  verificación/publicación gobernada por REL.GOV.1.
<!-- NOR3-G122-PROMOTION:END -->

<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:START -->
## Estado vigente — VER.2 R6 / G128-E02-C0 pendiente de integración

MANT.2 R2/#206 está cerrado, integrado y publicado como **G127/E02**
(`0.1.27.02-beta`) sobre
`main@2df33a5c24d1c7cea1a6db91539a92da02c91500`, mediante PR #207,
tag firmado `v0.1.27.02-beta` y GitHub Release prerelease 392412590.

El preflight #166 posterior a G127/E02 quedó **CLEAN** y habilitó
VER.2 R6/#164.

VER.2 R6/#164 materializó G128/E02/C0 como `0.128.2.0-beta` mediante la rama
`ver/ver2-r6-revision-aware` y el PR #208, actualmente listo para integración.
CP1–CP7 están cerrados y auditados; G128 está aceptado localmente y pendiente
de integración/publicación. **G129 permanece libre** y sin candidato, bloque ni
`VERSION` preasignados.

La continuidad material vigente es:

1. **integrar y publicar VER.2 R6 / G128-E02-C0**;
2. **repetir #166 post-publicación**;
3. **DOC.4 R1 / #171**;
4. **#142** y derivados funcionales obligatorios;
5. **PERSIST.1 / #130 → REP.1 / #143 → DEPLOY.1 / #157**;
6. **UX.7→UX.x / #129** bajo #189;
7. **SEC.2 R7 → rendimiento → A11Y.2 → REV.1 → #153 → DOC.1 R6 → QA.1 → REL.1**.

Un MANT.2 R3+ solo se inserta si #166 detecta trabajo material nuevo.
<!-- POST-NOR3-INTERMEDIATE-SEQUENCE:END -->


<!-- DOC1-R1-POST-MANT1:START -->
## Estado revision-aware vigente
- `VERSION` contiene `0.128.2.0-beta` y corresponde a VER.2 R6 / G128-E02-C0.
- G128 es el primer estado aceptado bajo `revision-aware-v2`.
- G127/E02 permanece como último estado publicado mediante `v0.1.27.02-beta` y Release 392412590.
- G087/E01 permanece como Edition histórica anterior de VER.2.
- G129 es el siguiente Global disponible, sin candidato ni bloque reservado.
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
- El contador y la procedencia de revisiones aceptadas se auditan en `docs/governance/pre-1-0-revision-ledger.md` y `data/governance/pre-1-0-revision-ledger.json`.
- `app/core/version_ledger.py` valida continuidad, unicidad y codificación del ledger estructurado.
- `docs/governance/pre-1-0-pending-matrix.md` ordena el trabajo pendiente hacia 1.0 sin preasignar Globales futuros.
- La regla que determina qué cuenta y qué no cuenta se documenta en `docs/archive/governance/ver2-revision-decision-matrix.md` y `docs/archive/governance/pre-1-0-versioning-audit.md`.
- README, CHANGELOG, RELEASES, ROADMAP y el ledger deben corresponder al estado vigente cuando lo describan como actual.
- Los documentos de dominio pueden conservar la versión en la que fueron revisados; esa metadata es histórica de revisión documental y no una segunda fuente de la versión vigente.
- La numeración de **Build** es independiente de `VERSION` y solo se materializa cuando exista un proceso reproducible de generación de artefactos oficiales.

No se deben introducir versiones independientes en plantillas, JavaScript, motores o normativa.

## 3. Familias admitidas

Mi Retiro Proyectado reconoce cuatro familias/etapas de identificadores.

### 3.1. Familia beta legacy histórica

La historia ya publicada conserva:

```text
0.0.N-beta
```

Ejemplos: `0.0.22-beta`, `0.0.25-beta` y `0.0.26-beta`.

Esta familia sigue siendo válida para leer y auditar estados históricos. Los
tags ya publicados no se renombran ni se mueven.

### 3.2. Familia revision-aware v1 histórica

Los estados revision-aware ya publicados hasta G127 conservan el esquema v1:

```text
0.<G_HI>.<G_LO>.<EE>-beta
```

donde `G_HI = G // 100`, `G_LO = G % 100` se expresa con dos dígitos y
`EE` es el ordinal aceptado del bloque con dos dígitos.

Ejemplos históricos:

```text
G071 / E01 -> 0.0.71.01-beta
G100 / E03 -> 0.1.00.03-beta
G127 / E02 -> 0.1.27.02-beta
```

La notación documental antigua `0.GG.RR.EE-beta` se conserva únicamente al
citar decisiones o evidencia histórica. No se usa para construir nuevos
identificadores después de VER.2 R6.

La **revisión funcional** (`R#`, `R1.1`, `R3B2`, etc.) es metadata semántica y
no un componente literal de `VERSION`. Puede divergir de Edition.

Precedente histórico de divergencia: DEV.2 R5 = G118/E04 y DEV.2 R6 = G119/E05. Estos estados ya publicados permanecen inmutables bajo la familia v1.

### 3.3. Familia revision-aware v2 prospectiva

A partir del primer estado aceptado posterior a G127 se usa:

```text
0.<GLOBAL>.<EDITION>.<CORRECTION>-beta
```

Reglas:

- `GLOBAL` es el contador global decimal directo y la familia v2 comienza en
  G128;
- `EDITION` es el ordinal del estado aceptado dentro del bloque, entre 1 y 99;
- `CORRECTION` es 0 para la línea ordinaria y 1..999 para una corrección
  material post-aceptación dentro de la misma línea funcional;
- una corrección material aceptada consume un nuevo Global;
- un intento fallido o una corrección previa a aceptación no consume Global;
- una nueva línea funcional reinicia `CORRECTION` a 0;
- `maintenance_ordinal` y la revisión funcional permanecen como metadata;
- el formato largo prospectivo de seis componentes queda sustituido antes de
  haber sido publicado y no se acepta como v2.

Ejemplos sintéticos:

```text
G128 / E2 / C0 -> 0.128.2.0-beta
G129 / E2 / C1 -> 0.129.2.1-beta
G234 / E7 / C12 -> 0.234.7.12-beta
```

G128 ya está materializado como G128/E02/C0 (`0.128.2.0-beta`); G129 permanece libre hasta que exista un candidato material posterior.

### 3.4. Versiones oficiales

Cuando todos los gates de producto se hayan cerrado, la primera versión oficial
prevista sigue siendo:

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
- **PARCHE**: correcciones o mejoras compatibles que justifican una nueva
  versión funcional;
- **REVISIÓN**: hotfix o revisión puntual de una versión oficial ya publicada.

La numeración de cuatro componentes es una convención propia del producto y no
se presenta como SemVer estricto.

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
v0.1.27.02-beta
v0.128.2.0-beta
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
- El contrato histórico protegido por `tests/governance/test_plan1_guard_referencias_historicas.py` evita borrar referencias legacy necesarias para auditar cierres anteriores.

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
