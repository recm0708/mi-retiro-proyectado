# Estándar de código y comentarios

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.71.01-beta`
**Versión base histórica:** `0.0.24-beta`
**Revisión documental:** UX.4.6e R4 — 2026-08-18
**Revisión de mantenimiento:** MANT.1 R5E — estandarización de nombres de carpetas — 2026-08-23
**Clasificación:** Técnica / Mantenibilidad


<!-- DOC1-R1-REVISION-MANUAL:START -->
## Nota de lectura post-MANT.1

Este estándar queda vigente después del cierre de MANT.1. Las referencias a MANT.1 explican su origen técnico y no implican que el bloque siga abierto.

Estado vigente:

- MANT.1 está cerrado.
- DOC.1 R1 está cerrado.
- NOR.1 y NOR.2 están cerrados.
- Los criterios de comentarios, encabezados, estructura y trazabilidad siguen aplicando.
- DOC.1 R2 está cerrado como auditoría de la documentación Markdown vigente posterior a NOR.2.
- SEC.2 está activo en R1.
- No se modifican reglas de cálculo ni normativa.
<!-- DOC1-R1-REVISION-MANUAL:END -->

Este documento define el patrón permanente para documentar código en Mi Retiro
Proyectado. Su objetivo es permitir que otro desarrollador entienda intención,
contratos, límites y dependencias sin convertir el código en una narración línea
por línea.

MANT.1 R1 registró la auditoría inicial de cobertura, MANT.1 R2 aplica la
primera mejora documental sobre scripts, hooks y automatización local,
MANT.1 R3 documenta los YAML de GitHub sin modificar su comportamiento,
MANT.1 R4 limpia encabezados operativos para que la trazabilidad histórica quede
fuera de código/configuración, MANT.1 R5A inicia comentarios internos de
intención en servicios Python de aplicación, MANT.1 R5B extiende el criterio a CSS
y plantillas grandes, y MANT.1 R5C cubre JavaScript complejo de interacción,
almacenamiento, importación y resultados. MANT.1 R5D formaliza política y plantillas por extensión, uniforma encabezados de JavaScript/CSS operativo y MANT.1 R5E estandariza carpetas técnicas en inglés sin renombrar archivos. Las revisiones posteriores deben
conservar esta misma trazabilidad incremental.

## 1. Principio general

Un comentario debe explicar al menos una de estas cosas:

- **intención**: qué responsabilidad cumple un bloque;
- **contrato**: qué recibe, devuelve, modifica o invalida;
- **motivo**: por qué se eligió una solución no obvia;
- **límite**: qué deliberadamente no hace;
- **riesgo**: qué podría romperse si se modifica sin contexto;
- **procedencia**: cuándo una decisión depende de normativa, privacidad,
  accesibilidad, compatibilidad o arquitectura.

No se añaden comentarios que repitan literalmente una instrucción evidente.

## 2. Historia frente a documentación permanente

Los identificadores `UX.*`, `GOV.*`, números de revisión y relatos cronológicos
pertenecen a `CHANGELOG.md`, `RELEASES.md`, ADR, pruebas de regresión o archivos
históricos. El código de runtime usa comentarios semánticos que sigan siendo
útiles aunque cambie la numeración del roadmap.

Las pruebas sí pueden conservar un identificador histórico cuando este explica
el origen de una regresión.

### Encabezados operativos permanentes

Los encabezados de archivos operativos deben describir el propósito permanente
del archivo. No deben usar la primera línea para declarar `MANT.*`, `DEV.*`,
`UX.*`, `VER.*`, números de PR ni el bloque que originó el cambio.

En archivos YAML, hooks, scripts y README técnicos de carpetas operativas, el
encabezado debe indicar:

- **qué hace el archivo**;
- **qué alcance conserva**;
- **qué límites protege** cuando exista riesgo de modificar comportamiento.

La trazabilidad de revisión se registra en `CHANGELOG.md`, `docs/governance/roadmap.md`,
`docs/operations/validation.md` y documentación técnica equivalente, no en encabezados de
archivos operativos.

### Nombres de carpetas técnicas

Las carpetas técnicas se nombran en inglés para evitar mezclas entre paquetes,
documentación, scripts, parámetros y pruebas. Los nombres vigentes de mayor
impacto son `app/models/`, `app/engines/`, `app/services/`, `regulations/`,
`tests/validation_cases/` y `docs/archive/`.

Un cambio de carpeta no se considera completo hasta actualizar imports,
hipervínculos, rutas de pruebas, documentación y configuración relacionada.

## 3. Python

### Comentarios internos en servicios de aplicación

Los servicios propios de `app/services/` deben explicar decisiones de flujo cuando
normalizan datos, separan totales, construyen matrices, agregan advertencias,
leen documentos o transforman resultados en salidas para la interfaz. Estos
comentarios deben describir intención y límites de negocio, no registrar el nombre
de la revisión, el PR que los agregó ni la historia del bloque.

En servicios de cálculo o integración no se comentan líneas evidentes. Se comenta
la razón por la que una rama evita mutación, por qué se omite una fecha, por qué
se conserva una advertencia o por qué una fuente se consulta en una capa concreta.


Todo módulo de aplicación debe comenzar con un docstring que describa su
responsabilidad. Clases, servicios y funciones del runtime deben tener un docstring breve cuando
exista un contrato, transformación o efecto que otro desarrollador deba entender.
Incluso los auxiliares privados pequeños se documentan cuando forman parte de una
frontera sensible —por ejemplo privacidad, parsing, red, trazabilidad o logs—.
La revisión transversal actual deja documentadas todas las funciones y clases de
`app/`; código futuro debe conservar esa cobertura sin añadir texto redundante.

Patrón recomendado:

```python
"""Responsabilidad del módulo y límites relevantes."""


# ============================================================
# Área funcional
# ============================================================

def operacion(...):
    """Explica el contrato y cualquier decisión no evidente."""
```

`Args`, `Returns`, `Raises` o notas adicionales se usan cuando aportan información
real; no son obligatorios para funciones triviales. La lógica monetaria debe
documentar dónde conserva precisión y dónde materializa redondeos.

## 4. JavaScript

Cada archivo debe identificar su responsabilidad y separar bloques funcionales.
JSDoc se prioriza para funciones que:

- coordinan API o almacenamiento;
- transforman estructuras relevantes;
- ejecutan acciones destructivas;
- actualizan procedencia/estado compartido;
- tienen efectos secundarios no evidentes;
- forman parte del contrato reutilizado por otros scripts.

Patrón:

```javascript
/* ============================================================
   Responsabilidad del módulo
   ============================================================ */

/*
 * Alcance, dependencias y límites.
 */

// ============================================================
// Área funcional
// ============================================================

/**
 * Contrato de una operación relevante.
 *
 * @param {Object} datos Entrada utilizada.
 * @returns {Object} Resultado normalizado.
 */
function operacion(datos) {
  // ...
}
```

Los motores previsionales no se duplican en JavaScript. Los comentarios deben
dejar claro cuándo el frontend únicamente recopila, presenta u orquesta datos.

En módulos con `sessionStorage`, `localStorage`, importación de documentos,
orquestación de resultados o acciones destructivas, el comentario debe explicar:

- qué estado se conserva o se invalida;
- qué operación queda delegada al backend;
- qué datos son borradores hasta confirmación explícita;
- qué selectores o claves no deben cambiarse sin revisar dependencias;
- por qué una acción se ejecuta de forma defensiva o idempotente.

## 5. HTML / Jinja

Los comentarios se colocan alrededor de bloques funcionales grandes: navegación,
pasos del asistente, modales, avisos, fuentes, privacidad y áreas dinámicas. No se
comenta cada `div`.

```html
<!-- =========================================================
     Importación revisable de información oficial
     ========================================================= -->
```

La plantilla describe responsabilidad visible; la historia de una revisión UX no
se deja incrustada como comentario permanente.

## 6. CSS

Los comentarios CSS delimitan contratos visuales por componente o responsabilidad
y nunca se usan como excusa para reordenar reglas si ello puede modificar la
cascada.

```css
/* ============================================================
   Tablas de datos de la aplicación
   ============================================================ */
```

Claro, Oscuro y Alto contraste comparten semántica; los comentarios explican el
componente, no el número de revisión que lo creó.

## 7. Pruebas

Cada módulo de pruebas debe explicar qué contrato protege. Los nombres de prueba
deben expresar comportamiento observable. Las regresiones pueden conservar
identificadores de fase/revisión porque sirven como trazabilidad histórica.

Una prueba no debe fijar accidentalmente un valor que necesariamente crecerá
—por ejemplo, el número máximo de ADR— cuando el contrato real sea continuidad
consecutiva.

## 8. JSON y normativa

Los JSON se mantienen como JSON estándar y no admiten comentarios. Cualquier
explicación vive en documentación, ADR, metadatos permitidos por el esquema o
pruebas. Los parámetros normativos no se explican mediante comentarios dispersos
en motores si ya existe una fuente versionada.

## 9. YAML y configuración

Los comentarios son aceptables únicamente cuando aclaran permisos, triggers,
restricciones o una decisión operacional. No duplican el nombre evidente de una
clave.

MANT.1 R3 fija que los YAML versionados de GitHub pueden iniciar con un
encabezado breve cuando ese encabezado documenta propósito, alcance y límites
operativos. En workflows no debe alterar `on`, `permissions`, `concurrency`,
`jobs`, matriz, actions ni comandos; en Issue Forms no debe cambiar `labels`,
campos requeridos, opciones ni advertencias de privacidad.


## 9.1. Scripts, hooks y automatización local

Los scripts operativos del repositorio deben documentar al inicio:

- **propósito**: qué tarea automatizan;
- **alcance**: qué archivos o configuración pueden leer o modificar;
- **límites**: qué no hacen y qué validaciones no sustituyen;
- **dependencias**: intérpretes, herramientas externas o configuración Git requerida;
- **modo de fallo**: cuándo deben terminar con código distinto de cero.

Los hooks versionados bajo `.githooks/` deben mantenerse como delegadores
pequeños. La lógica de validación vive en `scripts/` para que pueda probarse,
documentarse y ejecutarse manualmente sin depender del ciclo interno de Git.

Cada carpeta operativa versionada, como `scripts/` o `.githooks/`, debe tener un
`README.md` breve cuando su contenido afecte commits, CI, publicación,
seguridad, privacidad o reproducibilidad del proyecto.

## 10. Web Storage

Las claves propias de la aplicación usan el namespace `miRetiroProyectado.*`.
Cualquier cambio futuro de claves debe tratarse como cambio de esquema de estado:
debe decidir expresamente si existe migración, fallback o ruptura intencional y
proteger esa decisión con pruebas/documentación.

Claves vigentes:

- `miRetiroProyectado.simulacion`;
- `miRetiroProyectado.privacidadConsentimiento`;
- `miRetiroProyectado.privacidadConsentimientoSesion`;
- `miRetiroProyectado.tema`.

## 11. Cambios que obligan a revisar comentarios

Actualizar comentarios/docstrings cuando cambie:

- responsabilidad de un módulo;
- contrato de entrada/salida;
- persistencia o invalidación;
- fuente de datos;
- tratamiento de privacidad;
- comportamiento accesible;
- regla normativa o decisión de arquitectura;
- interacción entre frontend y backend.

Un comentario obsoleto se considera una deuda funcional de mantenibilidad: puede
inducir a otro desarrollador a implementar un cambio incorrecto aunque el código
actual todavía funcione.

## 9. Política por extensión y plantillas oficiales

La política permanente por tipo de archivo queda documentada en
`docs/standards/file-structure-by-extension.md` y la auditoría aplicada en
`docs/archive/technical/AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md`.

Las plantillas oficiales viven en `docs/templates/file-structure/`. Todo
archivo nuevo debe partir de la plantilla más cercana cuando exista. Si una
extensión nueva aparece de forma recurrente, primero debe definirse su política
mínima antes de multiplicar archivos con estilos distintos.

Criterios obligatorios para archivos operativos nuevos:

- explicar propósito y alcance permanente al inicio cuando el formato lo permita;
- usar comentarios de sección para bloques complejos, no para cada línea;
- mantener trazabilidad histórica en documentación, no en encabezados operativos;
- no cambiar contratos funcionales solo para acomodar comentarios;
- no inventar comentarios en formatos que no los admiten, como JSON o binarios.
