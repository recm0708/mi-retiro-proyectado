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

## 19. Cambios del sistema visual UX.4.6a

- Conservar el orden de hojas `style.css` → `design-system.css` → `accesibilidad.css`.
- Los cambios puramente visuales deben concentrarse preferentemente en `design-system.css`; no reescribir la base histórica si una regla de capa puede resolver el cambio sin afectar comportamiento.
- No eliminar Alto contraste al simplificar el selector de apariencia.
- Toda modificación transversal de header, footer, Inicio, controles o tokens debe actualizar sus regresiones visuales y la documentación afectada en la misma unidad de trabajo.
- Un cambio de etiqueta visible no implica renombrar rutas, IDs o contratos consumidos por JavaScript salvo que exista una decisión funcional explícita.



## Privacidad — tratamiento de datos en cambios de producto

Todo cambio que añada un dato personal, una finalidad, almacenamiento, exportación, telemetría, analítica, cookie, servicio remoto o tercero debe revisar conjuntamente `docs/POLITICA_PRIVACIDAD.md`, `docs/CUMPLIMIENTO_LEY_81.md`, `docs/SEGURIDAD_PRIVACIDAD.md`, `docs/ESPECIFICACION_FUNCIONAL.md`, `docs/MODELO_DE_DATOS.md`, `docs/DECISIONES.md` y `docs/VALIDACION.md`.

Reglas mínimas:

- no incluir datos personales reales en pruebas, fixtures, logs, capturas versionadas ni commits;
- mantener identificadores fuera de los motores previsionales salvo decisión jurídica/funcional documentada;
- no introducir cookies, analítica o telemetría silenciosamente;
- cualquier almacenamiento permanente o transferencia a terceros exige revisar finalidad, consentimiento/base jurídica, retención, destinatarios y medidas de seguridad;
- los endpoints que reciban o devuelvan información de simulación deben conservar `Cache-Control: no-store` salvo justificación explícita;
- cambios materiales de la política deben incrementar la versión del consentimiento para solicitar aceptación nuevamente;
- antes de publicar una beta remota, verificar que la configuración de logs no registre cuerpos, archivos ni identificadores.


## Integridad de datos importados en el asistente

Desde UX.4.6c, cualquier cambio que consuma datos provenientes de un PDF debe conservar trazabilidad por campo cuando la fuente pueda ser parcial. Los campos confirmados desde el documento no se editan silenciosamente en pasos posteriores; los campos ausentes deben permanecer disponibles para captura manual. Las regresiones deben cubrir ambos casos.


### Patrón transversal de campos y ayudas desde UX.4.6c R2

- Los campos editables deben ofrecer una pista o ejemplo breve dentro del control cuando el tipo de entrada lo permita; la pista no sustituye la etiqueta y desaparece al existir un valor.
- No duplicar debajo del control una explicación que ya esté disponible en la ayuda contextual, salvo que sea necesaria para validar o decidir una acción.
- Las ayudas contextuales se representan con un botón compacto de icono `i`; la palabra visible `Info` no forma parte del patrón. El `aria-label` debe conservar un nombre accesible descriptivo.
- Los modales reutilizables del wizard deben poder abrirse desde cualquier paso visible; no deben depender de permanecer dentro de un panel que pueda ocultarse con `display: none`.
- La leyenda de obligatoriedad visible se redacta de forma uniforme como `* Campo obligatorio`; la obligatoriedad condicional se comunica mediante el estado dinámico del campo, no mediante una leyenda distinta.

### Revisión contextual de importaciones por paso

Desde UX.4.6c R3, los controles que reabran un comprobante ya confirmado deben llamar la vista previa indicando el paso activo. El Paso 1 es la única vista completa; los pasos posteriores muestran únicamente las secciones etiquetadas para esa etapa mediante `data-preview-step`. No se deben duplicar modales por paso.

Las ayudas contextuales conservan un área de interacción accesible, pero visualmente solo dibujan el círculo interno que contiene `i`; no se debe reintroducir un segundo borde circular en el botón exterior.

### Datos importados en tablas y casillas

- Una fila que contenga información documental confirmada debe poder distinguirse visualmente de una fila de captura manual sin depender únicamente del color.
- Si una casilla representa un estado derivado directamente de un documento confirmado, su valor se fija automáticamente y no se modifica desde la pantalla principal.
- Los campos o filas que el documento no aporte permanecen editables para captura manual.
- Este patrón debe reutilizarse en Pasos 1–6 y futuras vistas equivalentes; no debe aplicarse a casillas que representan decisiones propias del usuario.


### Procedencia documental en tablas

Cuando una tabla combine datos importados y manuales, la procedencia documental debe usar el patrón `data-row-imported` con la paleta primaria del sistema visual. No usar verde de éxito para indicar origen. Las casillas que provienen de un documento confirmado deben quedar marcadas y bloqueadas; las casillas que representan decisiones del usuario permanecen editables.

### Casillas documentales en tablas

Cuando un checkbox representa un dato confirmado por una importación, su estado visual y su lectura deben derivarse también de la metadata de procedencia y no exclusivamente del pintado nativo de `:checked`. Mantener separadas estas casillas de las decisiones manuales del usuario y actualizar las regresiones/documentación de la fase correspondiente.

## Gestión de datos e invalidación

Los cambios que añadan pasos, resultados o nuevas dependencias deben actualizar `gestion_datos.js` para que **Limpiar este paso** no deje cálculos obsoletos. Nunca usar `localStorage.clear()` o `sessionStorage.clear()`; deben eliminarse únicamente las claves que pertenecen a Mi Retiro Proyectado. Cualquier cambio material en conservación/eliminación requiere revisar Términos, Política de Privacidad, Cumplimiento Ley 81, Seguridad/Privacidad y sus pruebas.

## Consulta no disruptiva de términos

- El documento de Términos/Privacidad debe poder consultarse desde **Fuentes** sin cambiar de ruta ni alterar el consentimiento vigente.
- La consulta posterior usa el mismo documento versionado, pero oculta los controles de aceptación.
- El cierre `×` en modo consulta solo cierra el modal; en el consentimiento inicial no debe permitir acceder a Simular sin aceptar.
- Las acciones destructivas del asistente se mantienen únicamente en la barra sticky superior.

## Estados progresivos en tablas editables

Cuando una tabla represente información que puede completarse por etapas, el estado visual debe derivarse de los datos reales de la fila y actualizarse al modificar cualquiera de sus campos. No se debe mantener un rótulo `Pendiente` si la fila ya reúne una combinación válida parcial o completa. Los contenedores desplazables deben mostrar scroll vertical únicamente cuando el contenido realmente lo requiera.

Los controles de carga de archivos deben reutilizar el tratamiento visual global de `input[type=file]`; no se crearán variantes incongruentes por paso. Los mensajes contextuales dentro de una tabla no deben alterar la alineación vertical de controles equivalentes entre filas.

## UX.4.6d R9 — criterios para tablas dinámicas y privacidad

Toda contribución que regenere filas editables debe conservar actualización de estado en tiempo real y filtros reactivos. Los controles de privacidad deben reutilizar el modal global y respetar la diferencia entre consentimiento pendiente y consulta de una aceptación vigente. Los ejemplos públicos de formularios deben usar datos sintéticos/genéricos.

## UX.4.6d R10 — contrato de tablas actuales y futuras

- Toda tabla nueva debe reutilizar `.app-table-shell`; no crear una geometría paralela por pantalla.
- Las tablas generadas dinámicamente deben incluir la clase en su wrapper desde JavaScript.
- La paleta tabular debe probarse en Claro, Oscuro y Alto contraste.
- Reactividad, filtros de pendientes y bloqueo documental son patrones semánticos: reutilizarlos cuando correspondan, no añadirlos a tablas meramente informativas.
- Si una tabla necesita scroll horizontal, debe conservar el foco accesible del contenedor; si no existe desbordamiento real, no debe recibir tabulación artificial.



## UX.4.6d R11 — scrollbars y controles de importación

- Toda tabla nueva debe mantener `app-table-shell`; no reintroducir scrollbars nativos con botones/flechas que invadan el radio del contenedor.
- Los carriles internos deben permanecer visualmente dentro de la superficie y conservar contraste suficiente en Claro, Oscuro y Alto contraste.
- Un importador PDF debe usar `official-import-upload-grid`, `official-import-file-input` y `official-import-upload-action`; selector y acción deben compartir altura exterior.
- No crear estilos locales por pantalla para **Seleccionar archivo** o **Analizar documento** si el contrato común resuelve el caso.

## UX.4.6d R12 — scroll común y estados vacíos

- Las superficies con desplazamiento deben reutilizar el scrollbar temático común; no se deben crear carriles, flechas o colores locales por pantalla.
- `app-table-shell` conserva un radio menor que las tarjetas para integrar scroll y borde sin perder simetría.
- Si un filtro tabular deja cero filas visibles, la tabla debe ocultarse y presentar un estado vacío en vez de mantener encabezados sin registros.
- El estilo de `input[type=file]` no debe cambiar al pasar el puntero por el área que muestra el nombre del archivo; el hover visual pertenece al botón **Seleccionar archivo**.
- Comparador y cualquier tabla futura deben continuar utilizando `app-table-shell` cuando el contrato sea aplicable.

## R15 — formularios bloqueados e importadores neutrales al formato

- Todo nuevo `form-control`/`form-select` bloqueado o de solo lectura debe reutilizar los tokens `--app-field-locked-*`; no crear fondos locales por pantalla.
- La diferencia editable/no editable debe conservarse en Claro, Oscuro y Alto contraste y no depender exclusivamente del color.
- Los textos de producto deben hablar de **documento**, **comprobante** o la fuente concreta (Mi Retiro Seguro/Ficha Digital). El formato técnico admitido se documenta en validación/seguridad y puede ampliarse mediante adaptadores.
- Una acción **Limpiar este paso** debe restaurar el estado lógico vacío, no los valores predeterminados del HTML. Si existen sugerencias, solo se aplican después de una decisión explícita del usuario.

## UX.4.6d R16 — dependencias sin navegación regresiva

- Una acción del paso actual no debe enviar automáticamente al usuario a un paso anterior cuando la dependencia pueda reconstruirse con datos válidos ya presentes. En ese caso se revalida en segundo plano.
- Si la dependencia anterior está realmente incompleta, el paso actual conserva los datos y muestra una explicación contextual; el usuario decide cuándo revisar el paso anterior.
- Al restaurar `paso_actual`, se debe comprobar `puedeAccederDirectamenteAPaso()` y retroceder al último paso seguro.
- Una fuente documental específica de una subsección debe ubicarse junto al resultado que alimenta. En Paso 3, Ficha Digital pertenece a **Detalle salarial del año actual** y precede a la tabla mensual.


### Regla de importaciones revisables — R17

Al crear o modificar una vista previa documental:

- no uses `disabled` o metadata de procedencia como sinónimo de `checked`; bloqueo y valor booleano son estados distintos;
- conserva la clasificación real/proyectada del documento y excluye por defecto de historial real las filas que no sean `HISTORICO`;
- si el usuario modifica un campo detectado, registra su procedencia como editada y no lo vuelvas a presentar como detectado literalmente;
- cuando dos datos oficiales del mismo documento sean internamente inconsistentes, conserva la fuente y muestra una advertencia revisable en lugar de corregirla silenciosamente.

## UX.4.6d R18 — reglas para procedencia e importaciones

Cuando una pantalla mezcle datos importados y manuales, reutilizar el contrato de procedencia común: `DETECTADO`, `EDITADO_USUARIO`, `COMPLETADO_MANUAL` y `NO_DETECTADO`. No usar “Detectado” para un valor que fue modificado por el usuario. La procedencia es independiente de la validez del dato y no debe reutilizar colores de éxito para comunicar origen.

Nunca intentar rellenar programáticamente un `input[type=file]` después de una recarga. Los navegadores lo impiden por seguridad. Si la importación ya fue confirmada, restaurar únicamente metadata segura (por ejemplo, nombre del documento) y el estado derivado guardado; mantener disponibles las acciones de revisar/quitar importación.


### Regla de sincronización del año actual

No introduzcas una segunda entrada editable para un total que ya puede derivarse del detalle mensual/quincenal. Si una casilla de cuota actual modifica una referencia agregada de un paso anterior, registra procedencia, invalida dependencias y revalida mediante los servicios existentes; no dupliques fórmulas previsionales en JavaScript.


## UX.4.6d R20 — vigencia documental y resúmenes derivados

- La vigencia de una Ficha Digital se determina por el **último período salarial detectado**, no por el nombre del archivo ni por una fecha inventada.
- La advertencia por antigüedad es orientativa y no bloqueante: siempre debe ofrecer continuar con el documento actual o seleccionar uno más reciente.
- No ocultar resultados derivados que el usuario necesita auditar. Si un servicio ya calcula un resumen usado por decisiones posteriores, puede exponerse en interfaz siempre que se invalide/oculte junto con el estado fuente.
- No persistir una copia del archivo para resolver vigencia; reutilizar `anio_mas_reciente`/`mes_mas_reciente` ya confirmados.

### Regla de validación UX para dependencias entre pasos

Una acción principal no debe fallar únicamente desplazando el viewport. Si una dependencia previa puede reconciliarse a partir de una confirmación explícita del usuario, debe revalidarse sin navegación regresiva; si no puede reconciliarse, debe mostrarse un error visible y accionable en la sección enfocada. Las métricas visibles solo deben eliminarse como redundantes cuando representen exactamente la misma semántica en todos los estados soportados.



### Regla de sincronización Ficha Digital → Paso 2 (UX.4.6d R23)

- Una Ficha Digital confirmada puede ampliar el número de cuotas del año actual cuando contiene más casillas documentales confirmadas que Paso 2.
- No se permite reducir automáticamente Paso 2 por una ficha con menos meses; ese caso requiere revisión/completado explícito.
- Toda reconciliación debe preservar las cuotas anteriores al año vigente, actualizar la referencia persistida del detalle, invalidar resultados dependientes y revalidar Cuotas sin navegación regresiva.
- Las pruebas deben cubrir importación, F5/restauración y discrepancias tanto al alza como a la baja.
