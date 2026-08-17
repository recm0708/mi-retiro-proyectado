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

El importador de Mi Retiro Seguro debe mantenerse independiente de los motores. Los cambios al parser se validan contra texto sintético y, de forma manual, contra documentos personales conservados fuera de Git. La respuesta del endpoint puede incluir identificadores personales opcionales desde UX.4.6b cuando están etiquetados de forma inequívoca; el código único del documento se omite y el archivo no se escribe en disco.

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



## UX.4.6b — reglas de mantenimiento del Paso 1

- No volver a mostrar simultáneamente captura manual e importación PDF.
- La Ficha Digital pertenece al Paso 3 salvo que cambie su contrato funcional.
- Mantener la descomposición de nombres limitada, revisable y protegida por pruebas; los campos explícitos prevalecen y el sufijo femenino `de Apellido` puede mapearse a apellido de casada.
- Mantener nombres/cédula/NSS fuera de motores, logs y fixtures reales.
- La vista previa del comprobante debe abrir bloqueada y requerir una acción explícita para editar.
- La barra común del wizard debe permanecer en flujo normal y no recuperar `position: sticky` o `fixed` sin una nueva decisión de UX.


### UX.4.6b R2 — privacidad y consentimiento

- `privacidad.js` no debe almacenar la simulación ni identificadores en `localStorage`; solo versión/estado/fecha técnica de aceptación. La autorización activa de la pestaña debe permanecer en `sessionStorage`.
- Un cambio material en categorías de datos, finalidades, terceros, retención o almacenamiento exige incrementar la versión del consentimiento y actualizar la documentación legal/técnica relacionada.
- No agregar un banner de cookies mientras no existan cookies. Si se incorpora analítica, telemetría o cookies no esenciales, implementar consentimiento granular antes de activarlas.
- Mantener `/api/simulacion/*` con `Cache-Control: no-store` y evitar logging de cuerpos/archivos/identificadores.
- Mantener las ayudas mediante icono `i` y el hover de tablas como patrones transversales para los siguientes pasos UX.4.6c–g.
- Antes de beta pública, preferir Bootstrap local sobre CDN y revisar jurídicamente los textos de privacidad/condiciones.


## UX.4.6b R3 — reglas transversales

- No mostrar `sessionStorage`, `localStorage` u otros nombres de implementación en textos destinados al usuario salvo que exista una razón funcional clara; describir el comportamiento en lenguaje común.
- Toda nueva versión material de términos debe incrementar `VERSION_PRIVACIDAD` y obligar a una nueva aceptación.
- La casilla de consentimiento no se habilita antes de llegar al final del documento.
- Las barras superior e inferior del wizard deben actualizarse desde la misma lógica y conservar simetría de ancho/alineación.
- Las ayudas contextuales nunca deben quedar recortadas por tarjetas o footer.


## UX.4.6b R4 — criterio de contenido público

- La casilla del consentimiento se habilita únicamente después de llegar al final del documento, pero no debe mostrarse un bloque de **Fin de los términos** ni una confirmación **Lectura completada**.
- Mientras todavía no se alcance el final puede mostrarse una instrucción breve que explique por qué la casilla está deshabilitada; al cumplirse el requisito, esa ayuda debe desaparecer.
- Toda redacción pública debe estar justificada por una necesidad funcional, previsional, legal, de privacidad, seguridad o accesibilidad.
- No presentar Mi Retiro Proyectado como aplicación educativa, didáctica o pedagógica salvo que en el futuro exista una función explícita de ese tipo aprobada como alcance del producto.
- No exponer jerga técnica, estados internos o mensajes meta de desarrollo cuando el usuario no necesite conocerlos para tomar una decisión.


## UX.4.6c — reglas de mantenimiento del Paso 2

- No bloquear un formulario completo por el solo hecho de existir una importación PDF; bloquear únicamente campos con origen documental confirmado.
- Un campo que el documento no aporta debe seguir siendo editable y debe indicar al usuario que necesita captura manual.
- No permitir una segunda vía de corrección de datos importados en pasos posteriores: la edición vuelve a la vista previa documental.
- Mantener `origen_campos_cuotas` separado de `DatosCuotas`; la procedencia es metadata de interfaz y no una regla legal.
- Cuando `continua_cotizando` sea `false`, retirar dinámicamente `required` de los campos futuros además de deshabilitarlos.
- Las barras del wizard concentran la acción primaria; no reintroducir botones equivalentes dentro del Paso 2.
- Los iconos del selector de apariencia deben seguir siendo decorativos y acompañarse siempre del nombre textual del tema.
- Usar `* Campo obligatorio` como leyenda estándar; la condicionalidad se expresa habilitando/deshabilitando el asterisco y `required`.
- Los inputs vacíos de texto/número deben ofrecer una pista breve; evitar repetir debajo del campo la misma explicación que ya existe en la ayuda contextual.
- Los disparadores de ayuda muestran solo el icono `i`, pero deben conservar `aria-label` descriptivo.
- Cualquier modal que deba abrirse desde varios pasos debe estar desacoplado visualmente de paneles ocultables del wizard.

## Patrón de revisión importada por contexto — UX.4.6c R3

- Paso 1: `revisarComprobanteImportado(1)` muestra todo el comprobante.
- Pasos posteriores: pasar siempre el número real del paso y etiquetar las secciones reutilizables con `data-preview-step`.
- No crear un modal nuevo para cada etapa.
- Si un dato resumen también vive dentro de una tabla importada —como las cuotas del año actual— sincronizar ambos controles antes de confirmar.
- El control `.context-help-trigger` no debe dibujar borde; `.context-help-icon` conserva el único círculo visible.

## UX.4.6d — reglas de mantenimiento del Paso 3

- No agregar acciones internas de Analizar/Continuar que dupliquen las barras comunes.
- No inferir 12 cuotas para años vacíos ni completar masivamente datos desconocidos.
- Los campos importados se bloquean por procedencia; la ausencia de origen debe dejar el control disponible cuando funcionalmente corresponda.
- Mi Retiro Seguro se revisa desde Paso 3 únicamente en su bloque de historial anual.
- Ficha Digital usa el patrón Seleccionar → Analizar → Revisar → Editar opcionalmente → Importar y limita su contrato al año actual.
- El detalle del año actual no debe duplicar el enlace a Mi Caja Digital ni afirmar que la importación ocurre desde Paso 1.
- Una base salarial automática se presenta como valor derivado de solo lectura; una base manual requiere monto y periodicidad.
- No reintroducir paneles `Próximo paso...`; la navegación común ya comunica la continuidad.
- Cualquier cambio a estas reglas debe actualizar pruebas UX.4.6d, especificación, ADR, arquitectura, modelo/seguridad cuando corresponda y el documento específico de fase.

### Regla de mantenimiento R2 para Ficha Digital

- Ficha Digital nunca debe escribir `simulacion.cuotas.cuotas_anio_actual` ni borrar `origen_campos_cuotas.cuotas_anio_actual`.
- El total del Paso 2 se pasa al detalle únicamente como referencia de coherencia.
- No se deben seleccionar automáticamente meses acreditados a partir de un total anual/mensual agregado.
- Si el detalle del año actual se desactiva, los salarios de Ficha Digital quedan fuera del cálculo hasta que el usuario lo reactive o complete el total anual.

### Regla de procedencia en tablas (UX.4.6d R4)

Cuando una tabla mezcle datos documentales y captura manual:

1. registrar procedencia por campo/registro;
2. aplicar `data-row-imported` a filas con información confirmada y `data-row-manual` a filas sin procedencia documental;
3. bloquear controles importados, incluidas casillas cuyo estado derive del documento;
4. mantener editables únicamente campos/filas que el documento no aporte;
5. no aplicar este bloqueo a casillas que expresen una decisión del usuario.


- No usar `--app-success-*` para señalar que un dato fue importado; éxito/completitud y procedencia son conceptos diferentes.
- Para procedencia documental usar `data-row-imported` con tokens primarios/seleccionados.
- Una casilla documental debe tener `checked`, `disabled` y `data-imported-locked="true"`; los estilos deben conservar visible el gancho en los tres temas.
- No crear checkboxes solo para indicar procedencia en tablas que no contienen un dato booleano real.

### Checkboxes importados — regla de mantenimiento UX.4.6d R5

- No depender exclusivamente de `:checked` para representar un checkbox documental deshabilitado.
- Mantener `checked=true`, `aria-checked=true` y `data-imported-locked=true`.
- La lectura debe considerar `data-imported-locked=true` como selección confirmada.
- No aplicar esta regla a checkboxes que representen decisiones manuales del usuario.

### Regla de limpieza e invalidación — UX.4.6d R6

- Nunca borrar solo el DOM: la fuente de verdad es el estado temporal de la simulación.
- Una limpieza parcial debe invalidar todos los resultados descendentes.
- **Reiniciar simulación** no debe borrar tema ni consentimiento.
- **Borrar datos de esta aplicación en este navegador** solo debe eliminar claves propiedad del proyecto; no usar `storage.clear()`.
- Cualquier nueva etapa futura debe incorporarse a la jerarquía de dependencias y a las regresiones de gestión de datos.
- Los textos legales deben actualizarse si cambia materialmente conservación, finalidad, terceros o controles del titular.

### Modal de privacidad en dos modos

- Incluir `partials/privacidad_consentimiento.html` una sola vez desde `base.html`.
- Cargar `privacidad.js` globalmente una sola vez.
- Usar `data-privacy-action="review"` para abrir el texto en modo consulta.
- Nunca navegar a `/simulacion?privacidad=1` desde Fuentes como mecanismo normal de revisión.
- En modo revisión no escribir consentimiento ni mostrar checkbox/botones de aceptar.
- Mantener `Opciones` únicamente en la navegación superior sticky.

### Estados tabulares y scroll adaptativo — UX.4.6d R8

- Una tabla editable por etapas debe recalcular su estado cuando cambie cualquiera de los campos que lo determinan.
- El filtro de pendientes debe reutilizar el mismo evaluador, no implementar una segunda interpretación.
- `table-scroll-compact` se usa para retirar desplazamiento vertical cuando hay pocas filas visibles; no se elimina el scroll de tablas extensas.
- Los mensajes de ayuda por fila no deben aumentar solo una celda y desalinear el resto de la tabla; preferir `title`, ayuda contextual o un mensaje común fuera de la fila.
- Todo selector de archivo nuevo debe ser un `input[type=file].form-control` y heredar el tratamiento visual global.

### Reactividad de tablas y ejemplos públicos — UX.4.6d R9

- Las tablas con filas generadas dinámicamente deben preferir delegación de `input`/`change` en un contenedor estable cuando el estado dependa de la captura en tiempo real.
- Un filtro derivado del estado debe reaplicarse en la misma transición; no debe requerir que el usuario salga y vuelva a entrar al filtro.
- Si una tabla no requiere desplazamiento vertical, no se debe mantener un carril/scrollbar decorativo.
- Los placeholders públicos deben ser sintéticos, breves y genéricos; no reutilizar datos de usuarios, PDFs reales ni capturas de validación.

### Superficie tabular común — UX.4.6d R10

- Toda tabla nueva debe vivir dentro de `.app-table-shell`.
- Si la tabla se construye por JavaScript, asignar la clase al wrapper en el mismo momento de crearlo.
- No duplicar radios, bordes o colores de encabezado por paso salvo que exista una necesidad funcional documentada.
- `table-scroll-compact` se usa únicamente cuando un contenedor con límite vertical deja de necesitar scroll por tener pocas filas visibles.
- `data-row-imported` / `data-row-manual`, filtros reactivos y estados progresivos se aplican solo a tablas cuya semántica lo justifique.
- Revisar siempre Claro, Oscuro y Alto contraste; Alto contraste debe conservar borde fuerte y no depender de sombra/color tenue para separar la tabla.



### Scrollbar contenido y carga PDF simétrica — UX.4.6d R11

- No estilizar scrollbars de tablas por paso: el contrato vive en `.app-table-shell`.
- Mantener ocultos `::-webkit-scrollbar-button`; las esquinas deben quedar libres mediante margen del track y fondo transparente.
- Si una tabla corta activa `table-scroll-compact`, no forzar un scrollbar decorativo mediante estilos locales.
- Los tres temas deben conservar el mismo ancho/radio de scroll; solo cambia la paleta.
- Los importadores deben reutilizar `.official-import-upload-file .official-import-file-input` y `.official-import-upload-action .btn` con una altura exterior común.

### Scroll global y filtros vacíos — UX.4.6d R12

- No añadir CSS de scrollbar aislado a una nueva pantalla. Extender el contrato común solo si aparece un nuevo tipo real de superficie desplazable.
- Mantener scroll nativo; no sustituirlo por una implementación JavaScript salvo una necesidad de accesibilidad comprobada.
- Las tablas usan `--app-radius-md`; las tarjetas pueden utilizar `--app-radius-lg` o superior.
- Un filtro de tabla con cero resultados debe valorar un estado vacío antes de dejar encabezados sin registros.
- Para `input[type=file]`, no usar `input:hover::file-selector-button` para un cambio de color que se active desde el nombre del archivo; el hover debe estar asociado al pseudo-elemento del botón.
- Verificar siempre Claro, Oscuro y Alto contraste después de modificar scroll, bordes o estados vacíos.


### Selector de archivo y hover — UX.4.6d R13

Para cargadores futuros, reutilizar el contrato global de `input[type=file].form-control`. No añadir reglas locales que cambien el botón mediante `input:hover::file-selector-button`; Bootstrap/Chromium puede activar ese estado al pasar por el texto del archivo. Mantener la paleta interna estable y usar borde/foco del input para feedback interactivo.


### Formulario personal del Paso 1 — UX.4.6d R14

- Mantener una sola sección visible **Información personal** para la captura manual; no reintroducir encabezados paralelos de identificación/previsión salvo que exista una necesidad funcional nueva.
- Mantener **Sexo** y **Apellido de casada** en la misma zona lógica. El campo condicional se muestra únicamente para Femenino y nunca se vuelve obligatorio.
- No cambiar IDs (`sexo`, `apellido_casada`, nombres, cédula, NSS, fechas o `sistema`) por razones puramente de layout, porque importación, estado y validaciones dependen de ese contrato.

### R15 — controles bloqueados y documentos

Usar los tokens `--app-field-locked-*` para controles no editables. No definir un gris particular por paso. En copy de importación, preferir **documento/comprobante/fuente**; reservar “PDF” para mensajes técnicos que realmente expliquen una limitación de formato o validación. Al crear un reset, comprobar tanto `sessionStorage` como defaults HTML/JS para garantizar que el formulario no repueble valores borrados.

## Regla de flujo para dependencias entre pasos — R16

Antes de redirigir a un paso anterior, distinguir entre **dato faltante** y **resultado derivado invalidado**. Si los datos fuente siguen completos, recalcular el derivado en segundo plano y conservar el paso actual. Solo una entrada realmente incompleta debe exigir revisión del paso anterior, y esa revisión no se debe ejecutar mediante navegación automática sorpresiva.

Las importaciones deben colocarse junto al bloque que alimentan. Ficha Digital es fuente del detalle mensual del año actual, por lo que su componente precede a esa tabla dentro de la misma subsección.


### Checklist R17 para importadores

1. Verificar por separado procedencia, editabilidad y valor booleano.
2. No dibujar checkmarks a partir de una marca `imported/locked`.
3. Conservar metadata de campos que el usuario haya editado durante la revisión.
4. Mostrar diferencias internas de la fuente como advertencias, no como correcciones automáticas.
5. Cuando existan cifras acreditadas y proyectadas en el mismo documento, nombrarlas explícitamente y no mezclarlas.

## Patrón de procedencia R18

Para campos mixtos usar los helpers comunes de procedencia y evitar textos ad hoc. Un origen importado bloquea únicamente cuando corresponde a un valor detectado/confirmado; `NO_DETECTADO` permanece editable. En tablas extensas puede comunicarse la procedencia mediante badge/metadata por registro o por campo según la granularidad real.

Los file inputs nunca se restauran con JavaScript. La continuidad tras F5 se implementa restaurando el modelo confirmado y mostrando `Importación vigente: <nombre>` cuando exista metadata.


## Regla de desarrollo R19 — evitar doble captura del año actual

Si una pantalla mensual/quincenal alimenta un total anual, no deben existir dos fuentes editables para el mismo dato. En Paso 3, la fila del año vigente es derivada y de solo lectura cuando el detalle está activo. Los eventos de salario actualizan la vista anual; los cambios manuales de casilla de cuota actualizan además la referencia agregada de Paso 2 y obligan a invalidar/revalidar dependencias.

No sumar salarios de meses sin cuota al historial acreditado. Sí conservarlos como salario disponible para bases recientes. Mantener pruebas separadas para: mes con salario sin cuota, mes con cuota sin salario y seis meses acreditados completos.


## Regla de desarrollo R20 — vigencia de documentos periódicos

Cuando un documento represente una fotografía periódica, evaluar su vigencia usando un período realmente extraído del contenido. No inferir actualidad por fecha del archivo, nombre o fecha de carga. La advertencia debe ser no bloqueante salvo que exista una regla normativa específica que exija lo contrario.

Para Ficha Digital, la tolerancia UX es mes actual + dos meses calendario anteriores. Si cambia esta regla, actualizar regresiones, ADR y especificación. El resumen visible del detalle debe consumir exclusivamente el resumen backend ya validado y ocultarse ante cualquier invalidación.


## Regla temporal para importadores — R21

No introduzcas lógica de vigencia con el reloj del cliente. Usa la metadata `fecha_referencia`, `fecha_referencia_confiable` y `fuente_fecha_referencia` suministrada por backend. Los fallos de red deben producir `FECHA_NO_VERIFICADA`, no un fallback invisible a la fecha local. Las pruebas unitarias deben mockear `app.servicios.fecha_referencia._consultar_fecha_http`.

### Fallos de validación con scroll/foco

No usar `scrollIntoView()` como única señal de error. Toda rama que devuelva `false` en una acción principal debe dejar un mensaje visible o una validación nativa inequívoca. Para dependencias entre pasos, reconciliar primero el estado derivable y revalidar sin navegación regresiva antes de pedir intervención manual.



### Ficha Digital y referencia agregada de cuotas — R23

Al modificar el flujo de Ficha Digital, no asumir que Paso 2 es inmutable. Si una ficha confirmada aporta más meses con cuota acreditada que la referencia agregada, debe actualizarse hacia arriba sin retroceder de paso y conservando las cuotas previas al año actual. Si aporta menos, conservar Paso 2 y mostrar incoherencia. No duplicar esta lógica en nuevas pantallas: reutilizar la reconciliación del detalle y mantener actualizada `cuotas_anio_actual_referencia`.
