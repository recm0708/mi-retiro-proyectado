# Política de estilo y lint de Markdown

**Estado:** vigente
**Clasificación:** estándar / documentación / calidad

## Propósito

Este estándar define cómo se aplica `markdownlint` a la documentación de
Mi Retiro Proyectado. Su objetivo es corregir problemas reales de estructura y
formato sin reescribir evidencia histórica ni silenciar reglas de manera
indiscriminada.

La configuración canónica vive en `.markdownlint-cli2.jsonc`. La extensión
Markdownlint de Visual Studio Code y `markdownlint-cli2` deben usar ese mismo
archivo para que el editor y la validación reproducible compartan contrato.

## Principios

- Las reglas permanecen habilitadas salvo excepción explícita y documentada.
- Una excepción debe corresponder a una necesidad estructural real.
- Los documentos vivos, de soporte, estándares, plantillas y auditorías se
  corrigen cuando una regla identifica un problema aplicable.
- `docs/archive/**` conserva evidencia histórica y no se reformatea para
  satisfacer reglas de estilo posteriores a su creación.
- No se usa `--fix` de forma masiva sobre todo el repositorio.
- Los cambios automáticos deben limitarse a archivos y reglas previamente
  clasificados.
- Todo archivo Markdown nuevo debe cumplir esta política desde su creación.

## Reglas observadas en la línea base PREUX5.4

La línea base detectó incidencias de las siguientes reglas:

- `MD001`: niveles de encabezado.
- `MD003`: estilo de encabezados.
- `MD012`: líneas en blanco consecutivas.
- `MD013`: longitud de línea.
- `MD022`: líneas en blanco alrededor de encabezados.
- `MD024`: encabezados duplicados.
- `MD025`: más de un encabezado de nivel superior.
- `MD026`: puntuación final en encabezados.
- `MD028`: líneas en blanco dentro de citas.
- `MD032`: líneas en blanco alrededor de listas.
- `MD033`: HTML embebido.
- `MD034`: URL sin sintaxis explícita de enlace.
- `MD036`: énfasis usado como encabezado.
- `MD041`: primer encabezado del documento.
- `MD060`: consistencia de columnas en tablas.

La existencia de una incidencia no implica que la regla deba desactivarse. Cada
caso se corrige o se justifica según el tipo de documento y su función.

## Decisiones de configuración

### MD003 — encabezados ATX

Los documentos nuevos y editados usan encabezados ATX con `#`. Los encabezados
Setext no forman parte del estilo canónico vivo.

### MD013 — longitud de línea

`MD013` se desactiva globalmente. La decisión no elimina requisitos de
legibilidad: evita imponer un límite artificial de 80 caracteres a tablas,
enlaces, identificadores técnicos, comandos y contenido que se vuelve menos
legible al fragmentarse.

Los párrafos pueden dividirse manualmente cuando mejore su lectura, pero la
longitud física de una línea no es un criterio bloqueante del repositorio.

### MD024 — encabezados repetidos

Se configura `siblings_only: true`. Un encabezado puede repetirse bajo padres
distintos, patrón normal en changelogs y registros acumulativos. Dos encabezados
hermanos con el mismo texto siguen siendo una infracción.

### MD033 — HTML embebido

HTML continúa prohibido por defecto. `README.md` puede usar únicamente los
elementos `p`, `h1`, `a` e `img` necesarios para el hero, badges y composición
visual de la portada del repositorio.

Cualquier otro archivo o elemento HTML requiere evaluación antes de incorporarse
a la configuración.

### MD041 — primer encabezado

La regla permanece habilitada.

`README.md` admite contenido de presentación antes de su `h1` porque su hero usa
HTML deliberado. `.github/pull_request_template.md` queda exceptuado porque GitHub
inyecta la plantilla dentro de la interfaz de creación del Pull Request y su
estructura comienza deliberadamente en `h2`.

Estas excepciones son por archivo y no autorizan documentos nuevos sin título.

### Documentación histórica

`docs/archive/**` queda fuera del lint activo. Es una exclusión de alcance, no una
declaración de que su formato sea canónico. Su función es preservar estados
históricos y evidencia, por lo que no debe normalizarse mecánicamente con reglas
adoptadas después de su creación.

### Artefactos locales generados

`.pytest_cache/**` queda fuera del lint porque es un artefacto local recreado por
`pytest` y no forma parte de la documentación versionada del proyecto. No se
corrige ni se versiona su `README.md` generado.

### MD025 — anexo RF histórico integrado

`docs/product/functional-specification.md` conserva un segundo `h1` exclusivamente
para iniciar **Anexo A — Registro cronológico RF preservado**, que integra un
documento histórico completo con su propia jerarquía. `MD025` se exceptúa solo en
ese archivo para no renivelar mecánicamente el registro preservado.

La excepción no aplica a otros documentos: todo Markdown nuevo mantiene un único
título principal.

## Reglas que deben corregirse

Las siguientes reglas permanecen activas y deben resolverse cuando aparezcan en
documentación no archivada:

- `MD001`;
- `MD003`;
- `MD012`;
- `MD022`;
- `MD026`;
- `MD028`;
- `MD032`;
- `MD034`;
- `MD036`;
- `MD060`.

`MD025`, `MD033`, `MD041` y `MD024` permanecen activas fuera de las excepciones
específicas definidas por la configuración.

## Tablas

Las tablas GFM pueden usar cualquiera de los estilos que `MD060` reconoce, pero
cada tabla debe ser internamente consistente. No se desactiva `MD060` para evitar
que tablas nuevas mezclen espaciado o alineación de separadores.

Cuando una tabla existente falle, se normaliza la tabla afectada sin alterar el
contenido semántico de sus celdas.

## URL

`MD034` permanece habilitada. Una URL destinada a ser enlace debe usar sintaxis
Markdown o ir entre `<` y `>`. Las fuentes regulatorias oficiales no se exceptúan
de forma global; se corrigen conservando exactamente el destino de la URL.

## Aplicación a archivos nuevos

Todo Markdown nuevo o editado debe:

1. tener una estructura de encabezados válida;
2. usar encabezados ATX;
3. mantener como máximo una línea en blanco consecutiva;
4. separar correctamente encabezados y listas;
5. tener un único título principal cuando corresponda;
6. evitar HTML salvo excepción aprobada;
7. representar URLs como enlaces explícitos;
8. usar tablas con estilo interno consistente;
9. superar `markdownlint` bajo `.markdownlint-cli2.jsonc`.

Una nueva excepción requiere una necesidad concreta, alcance mínimo y
documentación de la razón. No se agregan excepciones únicamente para ocultar una
advertencia.

## Integración reproducible con Visual Studio Code

El workspace versiona `.vscode/settings.json` para asociar correctamente archivos especiales cuyo contenido no es Markdown ni C/C++:

- `VERSION` → texto plano;
- `LICENSE` → texto plano;
- `.github/CODEOWNERS` → texto plano.

Estas asociaciones corrigen falsos positivos del editor sin desactivar validadores globales ni alterar el contenido de esos archivos.

`.markdownlint-cli2.jsonc` conserva validación por JSON Schema, pero apunta a la copia local fijada en `.vscode/schemas/markdownlint-cli2-config-schema.json`. La colección local conserva los schemas de `markdownlint-cli2` `0.23.2` y `markdownlint` `0.41.1`, junto con sus licencias MIT y las URLs upstream.

El schema local de `markdownlint-cli2` cambia únicamente su `$ref` interno al schema local de `markdownlint`; las reglas de lint no se modifican por esta decisión. La CLI continúa siendo la autoridad reproducible de validación y debe producir el mismo resultado con o sin acceso a Internet.

No se usa `json.schemaDownload.enable = false` ni una exclusión global equivalente para esconder errores de configuración.

## Validación reproducible

La comprobación manual de referencia es:

```powershell
npx --yes markdownlint-cli2@0.23.2 "**/*.md"
```

La configuración del repositorio se descubre automáticamente desde la raíz. El
cierre PREUX5.4 debe demostrar que la documentación no archivada queda sin
violaciones no justificadas.
