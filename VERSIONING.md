# Política de versionado

**Proyecto:** Mi Retiro Proyectado
**Estado:** vigente desde GOV.1.2
**Fecha de adopción:** 2026-08-17

## 1. Objetivo

Esta política define cómo se identifica cada estado publicable o auditable de Mi Retiro Proyectado y evita que la versión visible, la API, la documentación y Git describan estados diferentes.

## 2. Fuente única de versión

La fuente canónica es el archivo raíz `VERSION`.

- `VERSION` contiene una sola línea con la versión de la aplicación.
- `app/core/version.py` valida y expone ese valor a Python.
- `app/core/config.py` importa `APP_VERSION`; no mantiene una copia literal.
- FastAPI usa `APP_VERSION` como versión de la aplicación.
- Jinja2 recibe `app_version` y el footer muestra el mismo valor.
- README, CHANGELOG, releases y tags deben corresponder al valor canónico cuando describan el estado actual.

No se deben introducir versiones independientes en plantillas, JavaScript, motores o normativa.

## 3. Esquema

La política toma como referencia SemVer para ordenar versiones, con una convención pre-1.0 propia del proyecto.

### 3.1. Desarrollo interno pre-beta

Mientras el producto siga antes de su primera beta pública:

```text
0.0.N-beta
```

Cada incremento de `N` representa un hito funcional, técnico, normativo, de seguridad, gobierno o UX cerrado y verificable. Un commit menor de documentación o una corrección preparatoria dentro del mismo hito no obliga por sí sola a incrementar la versión.

### 3.2. Primera beta pública y posteriores

Cuando se cumplan los criterios de publicación:

```text
0.1.0-beta.1
0.1.0-beta.2
...
0.1.0-rc.1
0.1.0
```

Una beta o RC no implica certificación oficial de la CSS ni elimina las limitaciones documentadas.

## 4. Reconstrucción histórica

GOV.1.1 reconstruyó retrospectivamente 21 estados anteriores:

```text
0.0.1-beta ... 0.0.21-beta
```

La reconstrucción se basa en los 80 commits reales existentes hasta `7941f58` y **no reescribe commits históricos**, autores, fechas, hashes o mensajes.

Durante la migración criptográfica del 2026-08-17 se autoriza materializar esos estados como **tags retrospectivos firmados**. Esos tags apuntan al commit de cierre ya documentado, conservan su fecha real de creación, declaran en el mensaje la fecha histórica del hito y **no existieron como tags en sus fechas históricas**.

El antiguo valor `0.1.0` continúa clasificado como marcador histórico de desarrollo no publicado.

## 5. Primera versión formal bajo esta política

`0.0.22-beta` es el primer estado cuya numeración se adopta deliberadamente bajo esta política.

A partir de este punto, cada versión formal cerrada debe poder relacionarse con:

1. un commit concreto en `main`;
2. pruebas y validaciones del hito;
3. documentación actualizada;
4. una entrada en `CHANGELOG.md` o `RELEASES.md` según corresponda;
5. un tag Git cuando el hito se declare formalmente cerrado.

## 6. Tags

Los tags formales usan el prefijo `v`.

Después de la adopción de firma SSH:

- **Todo commit nuevo** del mantenedor debe estar firmado;
- **Todo tag formal nuevo** debe estar firmado;
- se usa `git tag -s`;
- se verifica con `git tag -v`;
- `.github/allowed_signers` contiene las claves públicas autorizadas.

La migración del 2026-08-17 crea `v0.0.1-beta` a `v0.0.21-beta` retrospectivamente sin falsear fechas y reemite una sola vez `v0.0.22-beta` y `v0.0.23-beta` manteniendo exactamente los mismos commits objetivo.

Después de esa migración, los tags publicados vuelven a ser inmutables.

## 7. Diferencia entre versiones

No deben confundirse:

- **versión de aplicación:** `VERSION`;
- **versión de normativa:** metadatos de `normativa/*.json`;
- **versión jurídica de privacidad/términos:** identificador propio del documento legal;
- **versión de esquema de logs:** se definirá en GOV.1.4;
- **versión de esquema de datos:** se definirá cuando exista una necesidad de migración persistente.

Un cambio en una de estas categorías no implica automáticamente que las demás adopten el mismo número.

## 8. Regla de incremento

Antes de cambiar `VERSION` se debe responder:

- ¿el hito anterior está cerrado y trazable?;
- ¿el cambio altera comportamiento, contrato, gobierno, seguridad, normativa o UX de forma auditable?;
- ¿código, pruebas y documentación coinciden?;

Si la respuesta es sí, se asigna el siguiente número aplicable. Durante GOV.1 se utilizará la secuencia `0.0.N-beta`.

## 9. Prohibiciones

- No hardcodear la versión visible fuera de la fuente canónica.
- No reescribir commits históricos para añadir firmas.
- No falsear fechas de creación de tags retrospectivos.
- No presentar un tag retrospectivo como si hubiera sido publicado en la fecha histórica.
- No modificar tags publicados para ocultar cambios posteriores.
- La única sustitución autorizada es la reemisión firmada de `v0.0.22-beta` y `v0.0.23-beta` documentada en `docs/MIGRACION_FIRMAS_GIT_2026-08-17.md`.
- No usar la versión de aplicación como sustituto de la versión normativa o jurídica.
