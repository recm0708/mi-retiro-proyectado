# Política de versionado

**Estado:** vigente

## Propósito

Esta política define cómo Mi Retiro Proyectado identifica estados de desarrollo,
publicaciones beta y versiones oficiales sin confundir commits, revisiones
funcionales, estados aceptados, tags o artefactos distribuibles.

La historia completa de estados aceptados pertenece al ledger y a los registros
de publicación. Este documento describe **el modelo vigente** y la compatibilidad
necesaria para interpretar identificadores ya publicados.

## Fuentes canónicas

La versión de aplicación tiene una única fuente:

- [`VERSION`](VERSION) — versión materializada en el árbol.

El estado revision-aware se conserva en:

- [ledger Markdown](docs/governance/pre-1-0-revision-ledger.md) — representación
  navegable;
- [ledger machine-readable](data/governance/pre-1-0-revision-ledger.json) —
  secuencia estructurada de estados aceptados.

La publicación se rige por:

- [Proceso de release](docs/operations/release-process.md);
- [manifest de publicación](data/governance/release-publication-manifest.json);
- [Releases](RELEASES.md).

La planificación futura se mantiene separada del contador aceptado. Una fase
planificada no recibe Global, Edition ni valor de `VERSION` por anticipado.

## Conceptos

### Estado material

Es una configuración del proyecto suficientemente distinta como para tener
valor independiente de auditoría y que ha superado el proceso de aceptación
aplicable.

No todo commit, checkpoint o corrección intermedia constituye un estado
material.

### Global

`GLOBAL` es el contador decimal de estados aceptados pre-1.0.

Reglas:

- aumenta únicamente cuando se acepta un nuevo estado material;
- no se consume por planificación;
- no se consume por un candidato fallido;
- no se consume por commits separados que forman parte del mismo estado;
- no se reutiliza una vez aceptado;
- una fase intermedia descubierta puede ocupar el siguiente Global solo cuando
  realmente se materializa y se acepta.

El ledger determina el último Global aceptado y el siguiente número
aritméticamente disponible. Que un número esté disponible **no lo reserva**.

### Edition

`EDITION` identifica el ordinal de un estado aceptado dentro de un mismo
bloque de trabajo reutilizable o evolutivo.

Puede diferir de la revisión funcional. Por ejemplo, una revisión `R6` no
implica necesariamente `E06`.

### Revisión funcional

`R#`, `R1.1`, `R3B2` y formas equivalentes describen la posición semántica
dentro de un bloque. Son metadata de trabajo y no se codifican directamente en
`VERSION`.

### Correction

En la familia revision-aware v2, `CORRECTION` distingue una corrección material
posterior a una línea funcional ya aceptada:

- `C0` representa la línea ordinaria;
- `C1..C999` representa una corrección material dentro de esa línea;
- una corrección material aceptada consume un nuevo Global;
- una corrección realizada antes de aceptar el candidato no crea otra Correction
  ni consume otro Global;
- una nueva línea funcional vuelve a `C0`.

### Maintenance ordinal

`maintenance_ordinal` permite conservar la secuencia propia de bloques de
mantenimiento recurrente. Es metadata y no sustituye Global, Edition ni
Correction.

## Familias de versión

### Beta legacy histórica

Los identificadores legacy usan:

```text
0.0.N-beta
```

Los tags ya publicados bajo esta familia permanecen inmutables. La familia se
mantiene únicamente para interpretar historia; no se utiliza para crear nuevos
estados prospectivos.

### Revision-aware v1 histórica

Los estados revision-aware publicados hasta G127 usan:

```text
0.<G_HI>.<G_LO>.<EE>-beta
```

donde:

- `G_HI = GLOBAL // 100`;
- `G_LO = GLOBAL % 100`, con dos dígitos;
- `EE` es Edition con dos dígitos.

Ejemplos históricos de formato:

```text
G071 / E01 -> 0.0.71.01-beta
G100 / E03 -> 0.1.00.03-beta
G127 / E02 -> 0.1.27.02-beta
```

Estos identificadores y tags no se renombran para adoptar el formato v2.

### Revision-aware v2 vigente para beta

Desde G128, una beta materializada usa:

```text
0.<GLOBAL>.<EDITION>.<CORRECTION>-beta
```

Ejemplos de formato:

```text
G128 / E2 / C0  -> 0.128.2.0-beta
G234 / E7 / C12 -> 0.234.7.12-beta
```

Reglas:

- `GLOBAL` se expresa directamente en decimal;
- `EDITION` está entre 1 y 99;
- `CORRECTION` está entre 0 y 999;
- la revisión funcional y el maintenance ordinal permanecen como metadata;
- el formato no codifica el nombre del bloque;
- ledger, `VERSION` y superficies de publicación deben describir el mismo
  estado material.

### Versiones oficiales

La primera versión oficial objetivo es:

```text
1.0.0.0
```

Las versiones oficiales usan cuatro componentes:

```text
MAYOR.MENOR.PARCHE.REVISIÓN
```

Semántica prevista:

- **MAYOR:** cambios incompatibles o nueva generación;
- **MENOR:** capacidades compatibles de alcance relevante;
- **PARCHE:** correcciones o mejoras compatibles que justifican una nueva
  versión funcional;
- **REVISIÓN:** hotfix o revisión puntual de una versión oficial.

Esta convención es propia del producto y no se presenta como SemVer estricto.

## Qué consume un Global

Un estado consume Global cuando, en conjunto:

1. existe trabajo material identificable;
2. su alcance y owner están definidos;
3. el estado resultante es auditable de forma independiente;
4. los gates aplicables son satisfactorios;
5. la aceptación queda registrada en el ledger;
6. `VERSION` codifica exactamente ese estado;
7. código, pruebas, datos estructurados y documentación dependiente son
   coherentes.

Pueden consumir Global los cambios funcionales, de seguridad, mantenimiento,
dependencias, gobierno o documentación cuando generan un estado material
independiente.

No consumen otro Global por sí mismos:

- commits de implementación, pruebas y documentación del mismo estado;
- checkpoints de una misma revisión;
- PR, squash, CI o tag que únicamente materializan la aceptación ya contada;
- revalidaciones sin cambio material;
- intentos fallidos;
- correcciones previas a aceptación;
- planificación de una fase futura.

Los casos históricos concretos y sus inclusiones/exclusiones se documentan en
las auditorías de versionado y en el ledger, no se duplican en esta política.

## Ciclo de un candidato beta

### 1. Planificación

Una Issue, roadmap o plan puede identificar trabajo futuro, pero mantiene:

- Global sin reservar;
- Edition sin reservar cuando todavía no existe candidato material;
- `VERSION` sin modificar.

### 2. Materialización

Cuando existe un árbol candidato real y la fase cumple sus condiciones de
entrada, puede evaluarse el identificador revision-aware que le corresponde.

La materialización no convierte por sí sola el candidato en publicación.

### 3. Aceptación

Antes de aceptar el estado deben quedar coherentes al menos:

- `VERSION`;
- ledger Markdown/JSON;
- artefactos declarativos de gobierno aplicables;
- pruebas y documentación dependiente;
- gates exigidos por el alcance.

### 4. Integración

El candidato aceptado entra en `main` mediante el flujo protegido del
repositorio. Los commits canónicos cumplen la política de firma vigente.

### 5. Publicación

Después de integrar y revalidar `main`:

1. se crea el tag formal firmado;
2. se verifica su firma y contrato;
3. se publica/reconcilia el GitHub Release;
4. el estado publicado se registra sin reescribir el tag.

Un tag no se crea dentro del PR candidato para simular una publicación futura.

## Tags y firmas

Los tags formales usan el prefijo `v`, por ejemplo:

```text
v0.128.2.0-beta
v1.0.0.0
v1.0.0.1
```

Reglas:

- los commits canónicos nuevos siguen la política de firma SSH;
- todo tag formal nuevo se firma y verifica;
- `.github/allowed_signers` contiene las claves públicas autorizadas;
- un tag publicado no se mueve, sustituye ni elimina para esconder cambios
  posteriores;
- una corrección posterior requiere un nuevo estado conforme al modelo, no
  modificar el tag anterior.

Las migraciones criptográficas históricas ya consumidas no crean una excepción
reutilizable para publicaciones futuras.

## Build oficial

Los artefactos oficiales distribuibles usarán un identificador de Build
independiente:

```text
Build 000001
Build 000002
Build 000003
```

El Build:

1. tiene seis dígitos decimales;
2. es monotónico y no se reutiliza;
3. identifica un artefacto reproducible;
4. no forma parte de `VERSION`;
5. no sustituye Global ni la versión de aplicación;
6. obtiene su fuente canónica cuando REL.1 materialice el proceso de
   empaquetado oficial;
7. no se inventa durante beta.

Presentación objetivo de la primera versión oficial:

```text
Mi Retiro Proyectado
Versión 1.0.0.0
Build 000001
```

## Metadata documental

Debe distinguirse:

- **versión de aplicación actual:** procede de `VERSION`;
- **versión de aplicación revisada por un documento:** puede conservar la base
  concreta contra la que ese documento fue validado;
- **versión jurídica, normativa o de esquema:** pertenece a su propio dominio y
  no se reemplaza por la versión de aplicación.

Un documento histórico, ADR o auditoría no se moderniza únicamente para mostrar
el valor actual de `VERSION`. Un documento vivo sí debe evitar presentar como
actual un estado ya superado.

## Separación de identificadores

No deben confundirse:

- versión de aplicación: `VERSION`;
- estado revision-aware pre-1.0: ledger;
- revisión funcional: metadata del bloque;
- Build: artefacto oficial reproducible;
- versión normativa: `regulations/*.json` o fuente aplicable;
- versión jurídica de políticas/consentimientos: identificador del documento;
- versión de esquema de datos/logs: contrato técnico correspondiente;
- estado de despliegue: decisión operativa independiente;
- visibilidad del repositorio: configuración de GitHub.

Un cambio en una categoría no obliga automáticamente a cambiar las demás.

## Gates de aceptación

Antes de aceptar una nueva beta revision-aware debe comprobarse:

- estado anterior trazable;
- definición contable del nuevo estado;
- continuidad y unicidad del ledger;
- correspondencia exacta entre `VERSION` y el candidato;
- coherencia de manifest/registry cuando apliquen;
- código, pruebas y documentación dependiente sincronizados;
- Quality Gate y controles adicionales requeridos;
- ausencia de una fase intermedia bloqueante conocida;
- no preasignación silenciosa de Globals futuros.

No existe transición automática a `1.0.0.0` por alcanzar un Global
determinado.

## Compatibilidad histórica

La historia previa permanece interpretable sin convertirla en política vigente:

- los tags legacy publicados son inmutables;
- los identificadores revision-aware v1 publicados permanecen válidos;
- G001–G070 pueden reconstruirse documentalmente sin crear tags revision-aware
  retrospectivos;
- auditorías, ADR, ledgers, Releases y snapshots históricos pueden conservar
  nombres y formatos sustituidos cuando describen fielmente su momento;
- las regresiones históricas deben proteger esa evidencia en su autoridad
  correspondiente, no obligar a documentos vivos a repetirla.

La metodología de reconstrucción y reconciliación histórica se conserva en:

- [Auditoría de versionado pre-1.0](docs/archive/governance/pre-1-0-versioning-audit.md);
- [Matriz de decisiones VER.2](docs/archive/governance/ver2-revision-decision-matrix.md);
- [Reconciliación post-G070](docs/audits/governance/post-g070-revision-reconciliation.md).

## Primera versión oficial

La primera versión oficial solo se materializa después de cerrar los gates
definidos por el programa pre-1.0, incluyendo como mínimo:

- alcance funcional previsto;
- validación de motores y trazabilidad de cálculos;
- seguridad y privacidad;
- accesibilidad;
- persistencia/exportaciones incluidas en el alcance oficial;
- revisión normativa/jurídica prevista;
- QA integral;
- empaquetado reproducible;
- inventario y avisos de terceros;
- hashes/firma del artefacto;
- documentación final de instalación, uso, soporte y release.

## Prohibiciones

- No hardcodear una segunda fuente de versión visible.
- No usar Build como sustituto de `VERSION`.
- No reservar Global/Edition/VERSION por mera planificación.
- No reutilizar un Global aceptado.
- No consumir Global por un candidato fallido.
- No contar commits del mismo estado como revisiones independientes.
- No crear tags revision-aware retrospectivos para G001–G070.
- No reescribir commits históricos para añadir firmas.
- No falsear fechas históricas de tags.
- No mover un tag publicado para corregir un estado posterior.
- No usar la versión de aplicación como versión normativa o jurídica.
- No presentar una beta como versión oficial.
- No declarar `1.0.0.0` antes de sus gates.
- No reactivar formatos u objetivos históricos sustituidos como política
  prospectiva.

## Referencias

- [Gobierno del proyecto](GOVERNANCE.md);
- [Proceso de release](docs/operations/release-process.md);
- [Ledger pre-1.0](docs/governance/pre-1-0-revision-ledger.md);
- [Plan maestro hacia 1.0](docs/governance/master-plan-to-1-0.md);
- [Estándares del repositorio](docs/standards/README.md).
