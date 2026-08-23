# Estándar de código y comentarios

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.26-beta`
**Versión base histórica:** `0.0.24-beta`
**Revisión documental:** UX.4.6e R4 — 2026-08-18
**Revisión de mantenimiento:** MANT.1 R3 — YAML de GitHub — 2026-08-23
**Clasificación:** Técnica / Mantenibilidad

Este documento define el patrón permanente para documentar código en Mi Retiro
Proyectado. Su objetivo es permitir que otro desarrollador entienda intención,
contratos, límites y dependencias sin convertir el código en una narración línea
por línea.

MANT.1 R1 registró la auditoría inicial de cobertura, MANT.1 R2 aplica la
primera mejora documental sobre scripts, hooks y automatización local, y
MANT.1 R3 documenta los YAML de GitHub sin modificar su comportamiento. Las
revisiones posteriores deben conservar esta misma trazabilidad incremental.

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

## 3. Python

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
