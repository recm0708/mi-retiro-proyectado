# Guía interna de desarrollo

Este documento concentra información técnica que no debe mostrarse en la interfaz dirigida al **Asegurado(a)**.

## 1. Identidad del producto

- **Nombre visible:** Mi Retiro Proyectado.
- **Naturaleza:** herramienta independiente de la Caja de Seguro Social de Panamá.
- **Público de la interfaz:** Asegurado(a) / Asegurados(as).
- El nombre **Mi Retiro Seguro** se reserva para la herramienta oficial de la CSS y no se utiliza como nombre de este proyecto.

La identidad visible se centraliza en `app/core/config.py`.

## 2. Convención de terminología

En textos destinados a la interfaz y documentación funcional:

- singular: **Asegurado(a)**;
- plural: **Asegurados(as)**;
- evitar `usuario` cuando se refiera a la persona que realiza la simulación.

`Usuario` puede aparecer únicamente cuando sea un término técnico inequívoco que no describa al público final.

## 3. Información exclusivamente técnica

Las siguientes referencias pertenecen al mantenimiento del proyecto y no deben mostrarse como contenido principal de la aplicación:

- nombres internos de fases como `6F.1`, `6F.2`, `6F.3` o `6F.4`;
- rutas como `docs/*.md`, `normativa/*.json`, nombres de módulos o identificadores internos;
- ADR y decisiones de implementación;
- detalles de estructura del repositorio.

La interfaz puede mostrar la metodología, la normativa y los enlaces oficiales, pero no debe exponer la organización interna del repositorio.

## 4. Tipografía visible

La interfaz usa una escala simple:

1. **texto base:** un único tamaño para párrafos, controles, ayudas, tablas y navegación;
2. **encabezados:** jerarquía estructural;
3. **valores importantes:** tamaño mayor para pensiones, saldos y métricas que requieren atención;
4. **badges de estado:** tamaño compacto únicamente para señalización.

No se deben introducir tamaños arbitrarios por componente sin una justificación de jerarquía visual.

## 5. Fases internas

Los nombres de fases y subfases pueden mantenerse en documentación técnica, pruebas y comentarios de código para conservar trazabilidad histórica, pero no como badges, títulos o mensajes visibles para el Asegurado(a).

## 6. Fuentes y metodología

La interfaz utiliza nombres humanos y enlaces oficiales. Los identificadores internos de fuentes se resuelven desde los metadatos normativos antes de mostrarse.

Documentos técnicos relacionados:

- [Arquitectura](ARQUITECTURA.md)
- [Decisiones](DECISIONES.md)
- [Normativa](NORMATIVA.md)
- [Fuentes normativas](FUENTES_NORMATIVAS.md)
- [Validación](VALIDACION.md)

## Temas visuales

- La preferencia visual se gestiona únicamente en `app/static/js/tema.js`.
- `style.css` conserva la base histórica y responsive; `design-system.css` es la capa visual transversal vigente de UX.4.6a; `accesibilidad.css` conserva precedencia para remates accesibles.
- Los componentes personalizados deben reutilizar tokens `--app-*` y evitar nuevas superficies mediante colores literales cuando exista un token semántico equivalente.
- Un componente nuevo debe revisarse al menos en Claro, Oscuro y Alto contraste.
- Alto contraste puede mostrarse como opción secundaria de Accesibilidad, pero no debe eliminarse ni degradarse por cambios de la capa Oscura.
- No guardar el tema dentro de la simulación ni usarlo como parámetro del backend.

## Accesibilidad de interfaz

- Mantener un foco visible para controles interactivos.
- Evitar objetivos táctiles principales menores de 44 px.
- No depender exclusivamente del color para comunicar estados.
- Respetar la preferencia de movimiento reducido.
- Las nuevas páginas deben heredar de `base.html` para conservar navegación, salto al contenido y footer legal.

## 7. Tokens visuales semánticos

A partir de UX.2.1, los componentes nuevos deben reutilizar los tokens semánticos definidos en `style.css` para texto, superficies, bordes y estados. No introducir un color literal en una tarjeta o badge si existe un token con la misma función.

Revisar como mínimo:

- Claro;
- Oscuro;
- Alto contraste;
- estados de foco y hover;
- alertas, badges, tablas y controles.

Alto contraste se considera un tema oscuro de contraste máximo: fondo negro, texto blanco, bordes explícitos y foco amarillo.

## 8. Contenido visible frente a detalles de implementación

La trazabilidad visible puede indicar artículo, reglamento, fórmula, nombre de la fuente y enlace oficial. No debe explicar al Asegurado(a) que el enlace procede de `normativa/*.json`, de un endpoint, del backend o de otra estructura interna. Esos detalles se documentan aquí, en Arquitectura o en Decisiones.


## 9. Responsive y navegación móvil

UX.3 establece estas reglas para componentes nuevos:

- no resolver una tabla compleja reduciendo indiscriminadamente tipografía o columnas; usar un contenedor horizontal localizado cuando corresponda;
- evitar desbordamiento horizontal de `body`;
- en móvil, las acciones de formulario importantes deben alcanzar 48 px de altura y pueden ocupar todo el ancho disponible;
- la barra persistente del wizard se mantiene abajo de 768 px y debe respetar `env(safe-area-inset-*)`;
- comprobar como mínimo 375 px, 768 px, 1024 px y un escritorio amplio;
- revisar Claro, Oscuro y Alto contraste también en los breakpoints móviles.

## 10. Criterio de cierre de cambios

Un cambio no se considera terminado si modifica código, comportamiento o UX y deja desactualizada la documentación dependiente. Antes de cerrar una fase deben revisarse, según corresponda, `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `DECISIONES.md`, especificaciones, modelo de datos, arquitectura, guía interna y validación. También deben agregarse o actualizarse regresiones automatizadas cuando el cambio sea verificable por pruebas.

## Recursos gráficos pendientes y favicon temporal

Hasta integrar la familia definitiva de iconos de **Mi Retiro Proyectado**, no se debe crear ni versionar un favicon genérico o provisional. La ruta `/favicon.ico` responde temporalmente `204 No Content` para evitar errores 404 provocados por solicitudes automáticas del navegador.

Cuando los iconos oficiales estén disponibles se deberá:

1. guardar los recursos en la estructura aprobada de `app/static/img/`;
2. declarar favicon y variantes necesarias en `app/templates/base.html`;
3. retirar la ruta temporal `/favicon.ico` de `app/main.py`;
4. actualizar pruebas, `CHANGELOG.md`, `README.md`, `ROADMAP.md` y esta guía.

## 11. Higiene de estructura y respaldos

- Los paquetes `.zip`, `.7z` y `.rar` creados durante revisiones o entregas son artefactos locales, no componentes del proyecto.
- Los respaldos históricos deben guardarse fuera de la raíz del repositorio, preferentemente en una carpeta externa o hermana dedicada a respaldos.
- Git y GitHub constituyen la historia principal del código versionado; los comprimidos externos son únicamente una capa adicional de recuperación.
- `.gitkeep` solo se utiliza para conservar en Git un directorio que todavía no contiene archivos versionados reales.
- Cuando una carpeta recibe su primer archivo real, el `.gitkeep` correspondiente debe eliminarse.
- No mover carpetas funcionales solo para mejorar la apariencia del árbol. Toda reorganización real debe actualizar código, imports, rutas, pruebas y documentación relacionada dentro de la misma unidad de cambio.

## 12. UX.4.1 — semántica accesible y ayudas contextuales

UX.4.1 desarrolla la accesibilidad transversal ya establecida en ADR-050 sin introducir una capa nueva de cálculo.

- `app/static/js/accesibilidad.js` concentra comportamiento accesible reutilizable: ayudas contextuales, `aria-invalid`, foco del primer campo inválido, relaciones del wizard, regiones vivas, captions y aviso de enlaces externos.
- `app/static/css/accesibilidad.css` contiene únicamente estilos de esa capa y debe reutilizar los tokens `--app-*`; no debe duplicar la paleta de `style.css`.
- Las ayudas contextuales explican el significado del dato solicitado y diferencias con conceptos cercanos. Se presentan como tooltips compactos al pasar el puntero o al enfocar el control de ayuda; el clic queda como alternativa para dispositivos táctiles. No deben afirmar una regla legal que no esté respaldada por el motor y la normativa versionada.
- Al agregar un campo ambiguo al asistente se debe evaluar si necesita una entrada en `AYUDAS_CONTEXTUALES`. No todos los campos requieren ayuda contextual y el indicador visual debe permanecer compacto para no competir con la etiqueta.
- Los errores visibles continúan siendo el contenido principal; `aria-live` y la región `a11y-global-status` sirven para anunciar cambios, no para ocultar mensajes al Asegurado(a).
- Los paneles del wizard deben conservar un encabezado estructural que pueda actuar como nombre accesible de la región.
- Las tablas generadas por JavaScript deben usar una de las clases reconocidas por `CAPTIONS_TABLAS` o incorporar su propio `caption`.
- Los contenedores de tablas solo reciben `tabindex="0"` cuando existe desbordamiento horizontal real, evitando paradas de foco innecesarias.
- La validación manual inmediata de este bloque se realiza en laptop/PC. La auditoría con lector de pantalla y la ronda multidispositivo quedan para el cierre integral de WCAG 2.2.

## 13. Node.js como herramienta opcional

Node.js no forma parte del runtime de Mi Retiro Proyectado ni de las dependencias Python. `requirements.txt` se reserva para paquetes instalables con `pip`.

Cuando esté disponible en el equipo de desarrollo, Node.js LTS puede usarse para validaciones auxiliares como:

```powershell
node --check app/static/js/accesibilidad.js
node --check app/static/js/retiro.js
```

La ausencia de Node.js no impide ejecutar FastAPI ni la suite `unittest`. Si en el futuro el frontend incorpora dependencias npm reales, deberán declararse en un manifiesto JavaScript independiente y documentarse en el mismo cambio.

## 14. UX.4.2 — estados activos y selección perceptible

- El paso activo del wizard debe mantener contraste suficiente entre número y círculo; cuando `data-bs-theme="light"`, el número activo se presenta en blanco sobre el color primario.
- Los estados seleccionados que afectan decisiones posteriores deben combinar más de una señal visual. En la tabla de retiro se utilizan fondo, contorno, radio y badge.
- Los tokens `--app-retirement-selected-*` son específicos de esta selección y no deben sustituirse por colores literales dentro de celdas o badges.
- Claro, Oscuro y Alto contraste definen valores propios para estos tokens.
- `:focus-within` debe hacer visible la fila asociada al radio cuando se navega con teclado.
- `forced-colors: active` debe delegar la selección en `Highlight` y `HighlightText` del sistema.
- No eliminar el control de radio: el clic sobre toda la fila es una mejora de puntero, mientras el radio conserva la semántica y operación de teclado.


## 15. UX.4.3 — errores y recuperación por teclado

- Un control inválido debe conservar su etiqueta y ayudas existentes; el mensaje de error específico se muestra inline y se asocia mediante `aria-errormessage`.
- `aria-invalid` y el mensaje asociado se eliminan cuando el valor vuelve a ser válido o el formulario se reinicia.
- No depender del globo nativo del navegador como única retroalimentación: suprimir su presentación en `invalid` y usar el mensaje inline propio.
- Un error general de operación usa `role="alert"`; no añadir además `aria-live="assertive"` al mismo nodo.
- Las advertencias no urgentes pueden usar `role="status"` con `aria-live="polite"`.
- Cuando un error general pasa de oculto a visible puede recibir foco programático, pero no debe desplazar el foco si el Asegurado(a) ya está corrigiendo un control inválido.
- No hacer enfocable una fila completa si ya contiene un radio, checkbox, enlace o botón que representa la acción. Para selección de retiro, el radio sigue siendo el control semántico y Enter actúa como alternativa adicional.
- Las páginas públicas deben conservar un único `h1`; los títulos de paneles y secciones deben continuar con niveles subordinados coherentes.
- Las funciones llamadas por el `MutationObserver` deben ser idempotentes sobre `class`; no repetir `classList.add()` para una clase ya presente ni `classList.remove()` para una ausente.
- En validación reactiva, usar `control.validity.valid` para consultar estado sin emitir de nuevo `invalid`; reservar `checkValidity()`/`reportValidity()` para flujos donde esa emisión sea intencional.


## 16. UX.4.4 — edad anual en la línea temporal

- La columna **Edad** de Paso 4 es derivada; no almacenar una segunda edad persistente.
- Usar la convención `año calendario - año de nacimiento`, que expresa la edad que se cumple durante ese año y coincide con los comprobantes usados en validación.
- Si falta una fecha de nacimiento válida, mostrar `—`; no asumir una edad.
- Mantener la columna inmediatamente después de **Año** en Historial salarial real y Proyección futura.
- Cualquier cambio futuro de esta convención debe actualizar pruebas, especificación, ADR y validación manual de los casos de referencia.


## 17. UX.4.4 — detalle reciente y base salarial

Reglas de implementación:

- no inferir una cuota acreditada únicamente porque exista salario visible en Ficha Digital;
- conservar `PARCIAL` cuando solo se conoce una parte del mes;
- en modo quincenal, derivar el estado del mes a partir de las quincenas disponibles;
- no sincronizar el salario anual actual si la cantidad de meses acreditados no coincide con el Paso 2;
- las bases automáticas de proyección solo usan meses completos y nunca reescriben salarios históricos de años anteriores;
- el último mes acreditado del Paso 5 solo puede quedar bloqueado cuando se deriva de un detalle coherente; en ausencia de ese detalle permanece manual;
- los importadores solo aceptan formatos cuya estructura pueda validarse; para PDF digital se exige texto extraíble y una vista previa editable antes de aplicar;
- no versionar fichas, comprobantes, capturas ni datos personales usados para validación manual.


## UX.4.4 — comprobante personal como referencia dinámica

El importador de Mi Retiro Seguro debe mantenerse independiente de los motores. Los cambios al parser se validan contra texto sintético y, de forma manual, contra documentos personales conservados fuera de Git. La respuesta del endpoint omite identificadores personales directos y el archivo no se escribe en disco.

La comparación de Resultados consume `resumen_unificado`; no debe conocer campos internos exclusivos de SEBD, Mixto o SUCGS. Un caso de validación puede aparecer en tests, pero su monto nunca debe formar parte de JavaScript, plantillas o servicios de producción.


## 18. UX.4.4 — importación revisable

- mantener análisis y aplicación como operaciones separadas;
- no escribir en `sessionStorage` hasta confirmar la vista previa;
- permitir editar los campos detectados que alimentarán el asistente;
- excluir filas proyectadas del historial real por defecto;
- no inferir cuotas acreditadas desde salarios de Ficha Digital;
- usar `money-input`, `formatearNumeroMonetario()` y `obtenerValorMonetario()` en todo importe editable de vistas previas;
- si la Ficha Digital contiene meses de dos años, filtrar antes de la vista previa y conservar únicamente el año calendario actual;
- al confirmar datos que afectan cálculos, invalidar resultados derivados y exigir recálculo;
- probar parsers con fixtures sintéticos; documentos personales reales se usan solo fuera de Git para validación manual;
- todo nuevo importador debe declarar límites de tamaño, formato, páginas y tratamiento de documentos sin texto extraíble.


## 19. UX.4.5 — cierre de resultados y accesibilidad

Para validar UX.4.5:

1. calcular primero la prestación normal del escenario;
2. confirmar que se genere automáticamente una segunda fotografía sin cuotas/salarios futuros;
3. verificar que ambas usen la misma fecha de retiro;
4. comprobar que la tabla de comparación siga siendo legible en Claro, Oscuro y Alto contraste;
5. recorrer la tabla, los botones de cálculo y los modales de importación con `Tab`, `Shift+Tab`, `Enter` y `Esc`;
6. comprobar que una referencia PDF compatible se compare preferentemente con el cálculo acreditado.

La validación manual obligatoria inmediata se limita a PC/laptop. La matriz real de dispositivos puede ampliarse con un teléfono Android en la misma red local. Tablet Android, iOS/iPadOS, pantallas de escritorio muy grandes y macOS se mantienen como compatibilidad diferida para la beta/RC y no bloquean por sí solos el cierre de UX.4.5. Las regresiones responsive automatizadas continúan siendo obligatorias.


## Pre-beta — criterio de hardening

Antes de `v0.1.0-beta.1`, cualquier cambio sobre importadores debe probar archivo válido, archivo ajeno, extensión/MIME incompatibles, archivo vacío y exceso de tamaño. Los datos personales reales permanecen fuera del repositorio.

Los cambios que rompan `.github/workflows/ci.yml`, `pip check`, `compileall`, `node --check` o la suite no se consideran candidatos a beta. La matriz de CI complementa, pero no sustituye, la revisión manual del producto.

Las pruebas que inspeccionan CI deben comprobar el contrato del pipeline y aceptar majors futuros de `actions/checkout`, `actions/setup-python` y `actions/setup-node` cuando Dependabot los proponga. No deben convertir una versión histórica (`@v6`, por ejemplo) en requisito funcional. De igual forma, una dependencia versionada como `pypdf` se valida por presencia de pin exacto y por sus regresiones funcionales, no por un número histórico inmutable.

Cuando Dependabot proponga un cambio Python, revisar primero si corresponde a una dependencia directa permitida. Si una actualización directa obliga a cambiar transitivas fijadas, regenerar el snapshot como un cambio controlado, ejecutar la instalación limpia y comprobar la suite. No activar auto-merge.

## 20. UX.4.6a — reglas para mantener el rediseño

- Mantener el orden de carga `style.css` → `design-system.css` → `accesibilidad.css`.
- No trasladar fórmulas, criterios previsionales ni estados de negocio a `design-system.css`.
- Conservar las rutas internas aunque las etiquetas públicas del header sean breves.
- En Inicio, priorizar lenguaje orientado a tareas y beneficios; evitar frases sobre motores, metadatos o estructura interna.
- No usar cifras monetarias ficticias en mockups que puedan confundirse con un resultado real.
- Mi Caja Digital debe aparecer donde ayuda a verificar información individual; el footer global se reserva para identidad, aviso legal, versión y acceso a Fuentes.
- El marcador de marca `MR` es temporal y deberá reemplazarse cuando se integren favicon e iconos definitivos.
- La validación inmediata de cambios visuales continúa en PC/laptop; la matriz completa de móvil/tablet/pantallas grandes se ejecutará en beta/RC.
