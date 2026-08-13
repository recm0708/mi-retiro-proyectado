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

También se deben probar manualmente en navegador las rutas y pasos afectados. En cambios de accesibilidad, revisar además recorrido con teclado, foco visible y comportamiento de errores sin asumir que una prueba automatizada equivale a una auditoría con tecnologías de apoyo.

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

## 11. Higiene de estructura y respaldos locales

- Los archivos comprimidos generados durante el desarrollo (`.zip`, `.7z`, `.rar`) no forman parte de la estructura del repositorio y deben mantenerse fuera de su raíz.
- Los respaldos históricos pueden conservarse en una ubicación externa, por ejemplo una carpeta hermana como `_respaldos/Mi_Retiro_Proyectado/historico/`.
- `.gitignore` continúa excluyendo archivos comprimidos para evitar su incorporación accidental.
- Un archivo `.gitkeep` solo se mantiene cuando una carpeta vacía debe existir en Git. Debe eliminarse cuando el directorio ya contiene archivos versionados reales.
- No se reorganizarán `app/`, `tests/`, `docs/`, `normativa/` u otras rutas funcionales únicamente por estética. Si una reorganización aporta un beneficio técnico real, el mismo cambio debe actualizar imports, rutas, pruebas y documentación dependiente.

## 12. Accesibilidad semántica y ayudas contextuales

- Las páginas nuevas deben heredar de `base.html` y mantener la carga de `accesibilidad.css` y `accesibilidad.js`.
- Las ayudas de campos no deben duplicar fórmulas ni introducir reglas legales nuevas; su función es explicar qué dato se solicita y cómo distinguirlo de otros conceptos.
- Todo control requerido debe conservar una etiqueta programática. Los mensajes de error visibles deben poder anunciarse y el control inválido debe quedar identificable mediante `aria-invalid`.
- Los componentes dinámicos deben actualizar su semántica al mostrarse: paneles, alertas, tablas y controles agregados por JavaScript no pueden depender únicamente de cambios visuales.
- Las tablas complejas deben incluir un `caption` visible o no visual que describa su propósito. Si un contenedor necesita desplazamiento horizontal, debe poder recorrerse con teclado cuando el desbordamiento exista.
- Un enlace con `target="_blank"` debe informar de forma accesible que abrirá una pestaña nueva.
- Las ayudas contextuales deben poder abrirse y cerrarse con teclado, reflejar su estado mediante `aria-expanded` y cerrarse con `Escape`.

## 12. Herramientas opcionales de validación frontend

La aplicación no requiere Node.js para ejecutarse y `requirements.txt` debe contener únicamente dependencias instalables por `pip`.

Node.js LTS puede instalarse de forma opcional en el entorno de desarrollo para comprobar sintaxis JavaScript:

```powershell
winget install --id OpenJS.NodeJS.LTS -e --source winget
node --version
npm --version
node --check app/static/js/accesibilidad.js
```

No se debe crear `package.json` ni añadir paquetes npm mientras el frontend no tenga una dependencia real que lo justifique. Si en una fase futura aparece una dependencia JavaScript de compilación o pruebas, se documentará y versionará con su propio mecanismo de dependencias en lugar de mezclarla con `requirements.txt`.



## 16. Datos derivados de presentación

Cuando un valor visible pueda derivarse de un dato fuente ya persistido, evitar duplicarlo en el modelo salvo que el motor lo necesite como contrato independiente. La edad anual de la línea temporal se deriva de la fecha de nacimiento para cada año mostrado y debe mantenerse sincronizada en historial y proyección.


## 13. Datos recientes del año actual

Cuando se modifique el flujo de salarios recientes:

- salario visible y cuota acreditada deben seguir siendo conceptos independientes;
- un período parcial no debe anualizarse ni completarse silenciosamente;
- cualquier base automática de proyección debe indicar su origen y usar solo meses completos;
- la sincronización con el historial anual requiere coherencia con las cuotas del Paso 2;
- los archivos reales de Ficha Digital o historiales personales no se incorporan al repositorio ni a fixtures; las pruebas automatizadas deben usar datos sintéticos.
- la importación de Ficha Digital solo conserva el año calendario actual; no añadir persistencia de meses de años anteriores sin una necesidad funcional aprobada;
- los importes editables en vistas previas deben reutilizar la utilidad monetaria común y mostrar miles + dos decimales al perder el foco.


## 17. Referencias PDF personales

- Los comprobantes de Mi Retiro Seguro se procesan en memoria y no se guardan en el repositorio ni en el servidor local.
- El contrato de extracción no debe devolver nombre, cédula, número de seguro social ni código único del documento.
- Nunca se hardcodeará en código de producción el monto de un comprobante usado para validación; cada referencia debe provenir del PDF cargado.
- Una cifra importada es una referencia de comparación y no reemplaza los motores previsionales ni las fuentes normativas.
- La diferencia monetaria solo se presenta cuando sistema, identidad mínima disponible, edad de retiro y naturaleza de la prestación son compatibles.
- Los tests del importador deben usar texto sintético o fixtures anonimizados; los PDFs personales originales permanecen fuera del repositorio.


## 18. Resultados acreditados y proyectados

- Los motores legales no se duplican para comparar origen de datos: el mismo servicio integrado recibe `modo_integracion` y conserva una única implementación jurídica.
- `SOLO_ACREDITADO` mantiene la fecha de retiro elegida, sustituye el total del escenario por las cuotas actualmente acreditadas y no consume registros salariales proyectados.
- La comparación visual nunca debe depender de un PDF personal. El comprobante externo es solo una referencia opcional.
- En Mixto y SUCGS no se proyectarán saldos CAP/solidarios sin una fuente o regla oficial; si se comparan ambas fotografías, esos saldos permanecen constantes y la interfaz debe explicarlo.
- Cualquier cambio que invalide un resultado proyectado debe invalidar también su fotografía acreditada asociada.
- Las tablas comparativas nuevas deben conservar `caption`, `scope` y foco/contraste coherentes con los temas existentes.


## Pre-beta — archivos, CI y privacidad

- Toda nueva carga de PDF debe reutilizar la validación común de `app/core/archivos_pdf.py`; no duplicar comprobaciones de extensión/tamaño en endpoints.
- Un PDF personal real nunca se incorpora al repositorio. Las regresiones usan texto sintético, modelos controlados o PDFs generados en memoria.
- Los cambios que afecten motores, endpoints o importadores deben mantener una ruta E2E automatizada cuando exista un caso estable.
- La CI debe permanecer con permisos mínimos de solo lectura mientras no exista una necesidad explícita de publicación.
- Las actualizaciones propuestas por Dependabot no se aceptan por versión solamente: requieren CI verde y revisión de compatibilidad funcional/normativa.
- Las regresiones de infraestructura deben validar capacidades del workflow (`checkout`, `setup-python`, `setup-node`, Python soportado, `pip check`, `compileall`, `node --check` y suite), no congelar el major de una Action concreta.
- `requirements.txt` conserva un snapshot completamente fijado para reproducibilidad, pero Dependabot solo propone de forma ordinaria cambios sobre las dependencias directas declaradas por el proyecto. Si una actualización directa exige regenerar el snapshot transitivo, debe hacerse como cambio controlado y volver a ejecutar la suite completa.
- GitHub Actions puede agruparse en una sola propuesta. `pypdf` y actualizaciones major se revisan con especial atención por su impacto potencial en importadores o compatibilidad. No habilitar auto-merge sin una decisión ADR explícita.
- No agregar una CSP estricta sin inventariar previamente recursos inline y externos; una política incorrecta puede dejar la interfaz inutilizable.
