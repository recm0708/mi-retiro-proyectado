# Guía de contribución

Este documento define el flujo mínimo para modificar código, parámetros normativos, pruebas y documentación sin perder trazabilidad.

## 1. Antes de empezar

Actualizar la rama local:

```powershell
git pull
```

Comprobar que el árbol de trabajo esté limpio:

```powershell
git status
```

## 2. Principios de trabajo

- La interfaz no debe duplicar fórmulas previsionales del backend.
- Los parámetros legales modificables deben residir en `normativa/` o estar claramente aislados.
- Los datos históricos y los proyectados deben permanecer diferenciados.
- Los pagos únicos y las pensiones mensuales no se deben mezclar.
- Cuando falta un dato oficial indispensable, la aplicación debe indicar que el resultado está incompleto en lugar de inventar un parámetro.
- Los cambios normativos deben poder rastrearse hasta una fuente oficial.

## 3. Convención de commits

Se utilizan mensajes breves y descriptivos:

```text
feat: agregar cálculo de cuotas proyectadas
fix: corregir cálculo de edad de referencia
docs: actualizar normativa del SEBD
test: agregar caso de validación femenino
refactor: reorganizar motor de pensiones
chore: actualizar configuración del repositorio
```

Cuando un avance afecta funcionalidad, pruebas y documentación, se recomienda mantener commits separados por tipo cuando resulte práctico.

## 4. Flujo recomendado de staging

Evitar `git add .` como hábito cuando hay cambios heterogéneos. Revisar y agrupar:

```powershell
git status
git diff
```

Ejemplo para funcionalidad:

```powershell
git add app normativa
git diff --cached --check
git status
git commit -m "feat: describir cambio"
```

Ejemplo para pruebas:

```powershell
git add tests
git diff --cached --check
git commit -m "test: describir validacion"
```

Ejemplo para documentación:

```powershell
git add README.md CHANGELOG.md CONTRIBUTING.md docs .gitignore .gitattributes .editorconfig
git diff --cached --check
git commit -m "docs: actualizar documentacion"
```

Finalmente:

```powershell
git push
git status
```

## 5. Validación mínima antes de un commit

Ejecutar:

```powershell
python -m compileall app
python -m unittest discover -s tests -v
```

También se deben probar manualmente en navegador las rutas y pasos afectados.

Para cambios en archivos Markdown o configuración, revisar además:

```powershell
git diff --check
```

## 6. Comentarios y formato del código

- **Python:** 4 espacios; docstrings cuando aporten contexto.
- **HTML/CSS/JavaScript/JSON:** 2 espacios.
- **JSON normativo:** sin comentarios, porque JSON estándar no los admite.
- **Markdown:** títulos jerárquicos y listas coherentes; evitar secciones históricas añadidas al final si el contenido puede integrarse en la estructura principal.

`.editorconfig` fija LF desde el editor y `.gitattributes` aplica `eol=lf` a todo archivo detectado como texto, incluidos archivos sin extensión como `.gitignore`. Esto evita que la configuración `core.autocrlf` de Windows introduzca conversiones CRLF dentro del proyecto.

Después de modificar reglas de finales de línea, normalizar el índice una sola vez con:

```powershell
git add --renormalize .
```

A continuación se debe revisar `git status` y `git diff --cached --check` antes de confirmar el cambio.

## 7. Precisión monetaria

- Usar `app/core/dinero.py` cuando exista riesgo de redondeo.
- Conservar precisión interna y materializar importes a dos decimales.
- Usar `ROUND_HALF_UP` como criterio técnico general, salvo regla normativa específica.
- No redondear valores intermedios para forzar una cifra visible.
- Los campos monetarios editables deben aceptar como máximo dos decimales y presentar separadores de miles.

## 8. Cambios en fórmulas o normativa

Todo cambio de fórmula, parámetro legal, tabla actuarial, fecha de transición o requisito debe incluir:

1. fuente oficial verificable;
2. fecha o versión de la fuente;
3. actualización de `normativa/*.json` cuando corresponda;
4. actualización de [docs/NORMATIVA.md](docs/NORMATIVA.md);
5. actualización de [docs/FUENTES_NORMATIVAS.md](docs/FUENTES_NORMATIVAS.md) si aparece una nueva fuente o enlace;
6. prueba automatizada nueva o ajustada;
7. ADR en [docs/DECISIONES.md](docs/DECISIONES.md) si existe interpretación, ambigüedad o decisión de diseño relevante.

No se debe usar una nota de prensa como sustituto de una ley o reglamento cuando la norma formal está disponible. Las comunicaciones institucionales pueden usarse para fechas o procedimientos operativos, dejando claro su carácter temporal.

## 9. Datos personales y casos de validación

Está prohibido versionar información personal real no anonimizada.

Los archivos originales utilizados para validar contra Mi Caja Digital, Mi Retiro Seguro u otra documentación oficial deben permanecer fuera del repositorio. `tests/casos_validacion/originales/` está ignorado por Git.

Los casos públicos deben ser:

- sintéticos; o
- anonimizados de forma irreversible para los fines del repositorio.

Ver [tests/casos_validacion/README.md](tests/casos_validacion/README.md).

## 10. Documentación que debe mantenerse coherente

No es necesario modificar todos los documentos en cada commit. Se actualizan únicamente los afectados, manteniendo consistencia entre:

- `README.md` — estado y uso general;
- `CHANGELOG.md` — cambios acumulados;
- `docs/INDICE.md` — mapa de documentación;
- `docs/ESPECIFICACION_FUNCIONAL.md` — requisitos;
- `docs/ARQUITECTURA.md` — estructura técnica;
- `docs/MODELO_DE_DATOS.md` — contratos de datos;
- `docs/MOTOR_DE_CALCULO.md` — algoritmos;
- `docs/NORMATIVA.md` y `docs/FUENTES_NORMATIVAS.md` — reglas y fuentes;
- `docs/VALIDACION.md` — regresiones;
- `docs/ROADMAP.md` — trabajo pendiente.


## Terminología visible

La interfaz y documentación funcional se dirigen a **Asegurados(as)**.

- usar **Asegurado(a)** en singular;
- usar **Asegurados(as)** en plural;
- no mostrar nombres internos de fases, ADR, rutas del repositorio ni IDs de fuentes;
- conservar el nombre visible de la aplicación en `app/core/config.py`;
- evitar introducir tamaños tipográficos aislados fuera de la escala definida en `app/static/css/style.css`.

Los detalles de estas convenciones se documentan en `docs/GUIA_INTERNA_DESARROLLO.md`.


## Documentación como parte del cambio

Todo cambio de código, UX, lógica, normativa, pruebas o configuración debe revisar y actualizar los archivos `.md` que dependan de él. La documentación no se corrige después del commit: forma parte de la misma unidad de trabajo. Si una decisión introduce una regla arquitectónica o funcional nueva, debe registrarse en `docs/DECISIONES.md` y, cuando corresponda, en la especificación, roadmap, modelo de datos y validación.
