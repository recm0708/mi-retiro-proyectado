# Política de versionado

**Proyecto:** Mi Retiro Proyectado
**Estado:** vigente desde GOV.1.2; revisada por PLAN.1
**Fecha de adopción:** 2026-08-17
**Revisión de transición a versión oficial:** 2026-08-19

## 1. Objetivo

Esta política define cómo se identifica cada estado publicable o auditable de Mi Retiro Proyectado y evita que la versión visible, la API, la documentación, los artefactos y Git describan estados diferentes.

## 2. Fuentes canónicas

La fuente canónica de la versión de aplicación es el archivo raíz `VERSION`.

- `VERSION` contiene una sola línea con la versión de la aplicación.
- `app/core/version.py` valida y expone ese valor a Python.
- `app/core/config.py` importa `APP_VERSION`; no mantiene una copia literal.
- FastAPI usa `APP_VERSION` como versión de la aplicación.
- Jinja2 recibe `app_version` y el footer muestra el mismo valor.
- README, CHANGELOG, RELEASES y tags deben corresponder al valor canónico cuando describan el estado actual.
- La numeración de **Build** es independiente de `VERSION` y solo se materializará cuando exista un proceso reproducible de generación de artefactos oficiales.

No se deben introducir versiones independientes en plantillas, JavaScript, motores o normativa.

## 3. Esquema de versiones

Mi Retiro Proyectado usa dos etapas de numeración claramente separadas.

### 3.1. Desarrollo pre-beta

Durante la etapa beta de desarrollo:

```text
0.0.N-beta
```

Ejemplos:

```text
0.0.25-beta
0.0.26-beta
0.0.27-beta
```

Cada incremento de `N` representa un hito funcional, técnico, normativo, de seguridad, gobierno, documentación o UX cerrado y verificable.

Un cambio preparatorio dentro de una rama de trabajo no obliga por sí solo a incrementar `VERSION`. La nueva beta se asigna al formalizar un hito cerrado y trazable.

La **visibilidad pública del repositorio de código no cambia por sí sola** esta convención ni convierte un estado beta en versión oficial.

### 3.2. Primera versión oficial y posteriores

La etapa beta no conduce a otra familia beta `0.1.0-beta.*`. Cuando todos los gates de producto se hayan cerrado, la primera versión oficial prevista será:

```text
1.0.0.0
```

La versión oficial usa cuatro componentes:

```text
MAYOR.MENOR.PARCHE.REVISIÓN
```

Semántica adoptada:

- **MAYOR**: cambios incompatibles o una nueva generación del producto;
- **MENOR**: nuevas capacidades compatibles de alcance relevante;
- **PARCHE**: correcciones o mejoras compatibles que justifican una nueva versión funcional;
- **REVISIÓN**: hotfix o revisión puntual de una versión ya publicada.

Ejemplos:

```text
1.0.0.0   primera versión oficial
1.0.0.1   primera revisión/hotfix de 1.0.0
1.0.0.2   segunda revisión/hotfix de 1.0.0
1.0.1.0   nueva versión de parche
1.1.0.0   nueva versión menor
2.0.0.0   nueva versión mayor
```

La numeración de cuatro componentes es una convención propia del producto y no se presenta como SemVer estricto.

## 4. Build oficial

Los artefactos distribuibles oficiales usarán además un identificador de Build independiente:

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
6. su fuente canónica se incorporará en REL.1 junto con el proceso de empaquetado;
7. no se mostrará un Build ficticio durante la etapa beta si todavía no existe un artefacto formal que lo justifique.

Presentación prevista para la primera versión oficial:

```text
Mi Retiro Proyectado
Versión 1.0.0.0
Build 000001
```

Un nombre de artefacto podrá incluir ambos identificadores, por ejemplo:

```text
MiRetiroProyectado-1.0.0.0-build000001.zip
```

## 5. Reconstrucción histórica

GOV.1.1 reconstruyó retrospectivamente 21 estados anteriores:

```text
0.0.1-beta ... 0.0.21-beta
```

La reconstrucción se basa en los 80 commits reales existentes hasta `7941f58` y no reescribe commits históricos, autores, fechas, hashes o mensajes.

Durante la migración criptográfica del 2026-08-17 esos estados fueron materializados como tags retrospectivos firmados. Los tags apuntan al commit de cierre ya documentado, conservan su fecha real de creación, declaran en el mensaje la fecha histórica del hito y no existieron como tags en sus fechas históricas.

El antiguo valor `0.1.0` continúa clasificado como marcador histórico de desarrollo no publicado.

## 6. Versiones formales de la etapa beta

`0.0.22-beta` es el primer estado cuya numeración se adoptó deliberadamente bajo esta política.

A partir de ese punto, cada versión formal cerrada debe poder relacionarse con:

1. un commit concreto en `main`;
2. pruebas y validaciones del hito;
3. documentación actualizada;
4. una entrada en `CHANGELOG.md` o `RELEASES.md`;
5. un tag Git cuando el hito se declare formalmente cerrado.

La línea `0.0.N-beta` continúa hasta completar todos los gates previos a la versión oficial.

## 7. Tags

Los tags formales usan el prefijo `v`.

Ejemplos:

```text
v0.0.25-beta
v1.0.0.0
v1.0.0.1
```

Después de la adopción de firma SSH:

- **Todo commit nuevo** del mantenedor debe estar firmado;
- **Todo tag formal nuevo** debe estar firmado;
- se usa `git tag -s`;
- se verifica con `git tag -v`;
- `.github/allowed_signers` contiene las claves públicas autorizadas.

La migración del 2026-08-17 materializó `v0.0.1-beta` a `v0.0.21-beta` retrospectivamente y reemitió una sola vez `v0.0.22-beta` y `v0.0.23-beta` manteniendo exactamente sus commits objetivo.

La excepción histórica ya fue consumida y **los tags publicados vuelven a ser inmutables**.

## 8. Diferencia entre identificadores

No deben confundirse:

- **versión de aplicación:** `VERSION`;
- **Build oficial:** identificador del artefacto reproducible;
- **versión de normativa:** metadatos de `normativa/*.json`;
- **versión jurídica de privacidad/términos:** identificador propio del documento legal;
- **versión de esquema de logs:** identificador propio de Developer Diagnostics;
- **versión de esquema de datos:** se definirá cuando exista persistencia migrable;
- **visibilidad del repositorio:** configuración de GitHub;
- **estado de despliegue:** decisión operativa independiente.

Un cambio en una categoría no obliga automáticamente a modificar las demás.

## 9. Regla de incremento

Antes de cambiar `VERSION` se debe responder:

- ¿el hito anterior está cerrado y trazable?;
- ¿el cambio altera comportamiento, contrato, gobierno, seguridad, normativa, documentación o UX de forma auditable?;
- ¿código, pruebas y documentación coinciden?;
- ¿se ejecutaron los gates exigidos para esa etapa?

Durante la etapa beta se usa `0.0.N-beta`.

La transición a `1.0.0.0` solo puede realizarse después de cerrar REL.1 y todos sus prerrequisitos. No existe una transición automática por alcanzar un número determinado de betas.

## 10. Primera versión oficial

La primera versión oficial objetivo es:

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

## 11. Prohibiciones

- No hardcodear la versión visible fuera de la fuente canónica.
- No usar `Build` como sustituto de `VERSION`.
- No reutilizar un número de Build ya asignado a un artefacto formal.
- No reescribir commits históricos para añadir firmas.
- No falsear fechas de creación de tags retrospectivos.
- No presentar un tag retrospectivo como si hubiera sido publicado en la fecha histórica.
- No modificar tags publicados para ocultar cambios posteriores.
- No usar la versión de aplicación como sustituto de la versión normativa o jurídica.
- No presentar una beta `0.0.N-beta` como versión oficial.
- No presentar `1.0.0.0` como alcanzada antes de cerrar sus gates.
- No reintroducir `0.1.0-beta.1` como objetivo vigente; cualquier aparición conservada en documentación histórica debe identificarse como una planificación posteriormente sustituida.

## 12. Guard de referencias históricas

PLAN.1 distingue entre **evidencia histórica legítima** y **planificación vigente**.

Las expresiones `0.1.0-beta.1`, “beta pública” y determinadas etiquetas `pre-beta` pueden conservarse cuando forman parte de:

- snapshots bajo `docs/historico/`;
- documentos de cierre, auditoría, release, decisiones o changelog que describen el plan existente en una fecha anterior;
- el plan maestro vigente cuando cita una planificación anterior únicamente para documentar de forma explícita su sustitución por `1.0.0.0`;
- nombres históricos de hitos como GOV.1.8 o la denominación original de la licencia;
- contratos técnicos de limpieza que identifican residuos/keys antiguos.

Esas expresiones **no pueden volver a utilizarse como objetivo vigente** en documentación operativa.

La regresión `tests/test_plan1_guard_referencias_historicas.py` aplica dos controles:

1. los documentos operativos actuales no pueden contener formulaciones prospectivas obsoletas como “desarrollo pre-beta”, “pendiente antes de beta pública”, “objetivo pre-beta” o equivalentes;
2. una referencia a `0.1.0-beta.1` o “beta pública” fuera del archivo histórico solo es aceptable en documentos expresamente reconocidos como evidencia/ledger y debe coexistir con una señal clara de contexto histórico, sustitución posterior o PLAN.1.

Los documentos nuevos quedan sujetos al control por defecto; no se añaden excepciones para hacer pasar una prueba. Toda nueva excepción requiere demostrar que preserva una evidencia histórica real y no una planificación prospectiva obsoleta.
