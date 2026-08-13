# Changelog

### UX.4.5 — información acreditada, proyección y cierre accesible

- El Paso 6 genera una segunda evaluación `SOLO_ACREDITADO` con la misma fecha de retiro pero sin añadir salarios ni cuotas futuras.
- SEBD reproduce de forma separada la fotografía acreditada y la proyección; el caso de regresión femenino conserva B/.741.59 acreditados frente a B/.769.42 cuando el escenario añade cinco cuotas a B/.1,500 mensuales.
- Mixto y SUCGS reutilizan la misma separación sin proyectar automáticamente sus saldos específicos; esos valores permanecen iguales en ambas fotografías.
- La interfaz incorpora una tabla accesible **Información acreditada y proyección al retiro**, con caption, encabezados de fila/columna, cuotas, pensión, pago único y diferencias.
- La referencia importada de Mi Retiro Seguro prefiere el cálculo propio acreditado cuando está disponible.
- Los resultados acreditados se almacenan e invalidan junto a su resultado proyectado correspondiente.
- Se refuerza el contraste de la tabla comparativa en Alto contraste y se revisa la semántica de los modales de importación.
- La suite alcanza **170 pruebas automatizadas**.

### UX.4.4 — edad anual y detalle salarial del año actual

- Historial salarial real incorpora la columna **Edad** inmediatamente después de Año.
- Proyección futura incorpora la misma columna para mantener continuidad entre datos históricos y estimaciones.
- La edad se deriva de la fecha de nacimiento ya guardada en el Paso 1 usando la convención de año calendario observada en los comprobantes de validación: `año - año de nacimiento`.
- El Paso 3 incorpora un detalle opcional del año actual con captura por total mensual o primera/segunda quincena.
- Cada mes diferencia salario disponible, estado completo/parcial y cuota ya acreditada; un salario puede existir sin que su cuota haya sido acreditada todavía.
- `POST /api/simulacion/detalle-anio-actual` valida el detalle, calcula totales disponibles/acreditados, último mes acreditado y bases salariales sugeridas.
- Cuando las cuotas marcadas coinciden con el Paso 2, el salario acreditado del detalle sincroniza la fila anual actual y el Paso 5 deriva automáticamente el último mes acreditado.
- La base de proyección puede continuar siendo manual o derivarse del último mes completo, del promedio de meses completos del año, de los últimos tres meses completos o del promedio salarial por cuota acreditada del año actual.
- El Paso 3 incorpora acceso contextual a Mi Caja Digital y centra esa acción dentro de su bloque.
- Se agrega carga opcional del comprobante PDF de Mi Retiro Seguro para extraer una referencia personal variable sin persistir el archivo ni exponer nombre, cédula o seguro social.
- El Paso 6 compara la referencia importada con la proyección actual únicamente cuando sistema, edad de retiro, persona y naturaleza de prestación son compatibles; si no, muestra ambas cifras sin fabricar una diferencia.
- La tabla temporal aumenta su ancho mínimo para conservar legibilidad con la columna adicional.
- La Ficha Digital importada se limita al año calendario actual; los salarios de años anteriores dejan de mostrarse y no se conservan en el estado de simulación.
- Los importes monetarios editables de las vistas previas usan separador de miles y exactamente dos decimales al mostrarse, reutilizando la utilidad monetaria común.
- La vista previa de Ficha Digital elimina las columnas redundantes Año y Aplicación porque todos sus registros pertenecen al año actual.
- La suite alcanza **161 pruebas automatizadas**.


Todos los cambios relevantes del proyecto se documentan aquí.

El proyecto todavía no ha publicado una versión estable; los cambios actuales se acumulan bajo **Unreleased** para la futura versión `0.1.0`.


## [Unreleased]

### Identidad y experiencia del producto

- La aplicación adopta el nombre visible **Mi Retiro Proyectado**.
- La identidad se centraliza en `app/core/config.py` para evitar nombres duplicados en plantillas y metadatos.
- La terminología pública usa **Asegurado(a)** y **Asegurados(as)** en lugar de `usuario` para referirse a quienes realizan simulaciones.
- Se eliminan de la interfaz etiquetas internas como `Paso 6F.1`, `Metodología 6F.2` y `Cierre funcional 6F.4`.
- La información sobre archivos `docs/*.md`, `normativa/*.json`, ADR y fases internas queda reservada a documentación de desarrollo.
- Se unifica el tamaño base de texto en formularios, ayudas, tablas, navegación y contenido explicativo; encabezados y valores previsionales mantienen jerarquía propia.
- El pie de página incorpora autoría, aviso de independencia y acceso directo a Mi Caja Digital.
- El acceso pendiente de importación se denomina `Importar desde Mi Caja Digital` para no presentar Mi Retiro Seguro como un recurso separado.
- Se agrega `docs/GUIA_INTERNA_DESARROLLO.md` con convenciones de marca, terminología y contenido exclusivamente técnico.
- Se agregan pruebas de regresión de identidad e interfaz.
- Se incorporan los modos **Seguir sistema**, **Claro**, **Oscuro** y **Alto contraste**, con persistencia local independiente de la simulación.
- Se añade enlace de salto al contenido, foco visible global, objetivos táctiles mínimos y respeto a movimiento reducido.
- El pie de página se compacta en dos líneas con copyright, aviso de independencia y acceso a Mi Caja Digital.
- La suite alcanza **96 pruebas automatizadas** después de añadir regresiones de mantenimiento técnico.
- UX.2.1 oscurece las superficies del modo Oscuro, convierte Alto contraste en un tema negro/blanco de contraste máximo y unifica colores semánticos para estados, alertas y badges.
- Se rediseña Inicio como portada del producto con propósito, sistemas contemplados, capacidades, proceso guiado y acciones principales.
- El wizard y la navegación rápida pasan a utilizar superficies adaptativas por tema en lugar de conservar fondos claros.
- Las tarjetas equivalentes alinean verticalmente sus contenidos y mantienen acciones al mismo nivel.
- Se elimina de Resultados la explicación técnica sobre `normativa/*.json`; la interfaz conserva únicamente la referencia oficial útil para el Asegurado(a).
- El footer evita partir el enlace a Mi Caja Digital y mantiene su segunda línea como una fila flexible compacta.
- El remate final de UX.2.1 centra únicamente los botones identificados en Inicio, Datos personales, Resultados y Metodología, sin alterar los botones que ya estaban correctos.
- En escritorios amplios, el aviso legal y `Abrir Mi Caja Digital` permanecen juntos en la segunda línea del footer.
- UX.3 adapta Inicio, navegación, formularios, tarjetas, Metodología, Comparador y resultados a laptop, tablet y móvil.
- En móvil, la navegación persistente del wizard se traslada a la parte inferior, respeta áreas seguras y mantiene retroceso, selector de paso y acción principal.
- Las tablas extensas conservan columnas legibles mediante desplazamiento horizontal dentro de su propio contenedor.
- El Paso 5 reemplaza la fecha exacta visible de actualización de cuotas por **Último mes con cuotas acreditadas**, separado de la fecha de evaluación y de las fechas de retiro.
- El backend deriva y valida la fecha técnica de corte desde el último mes acreditado y rechaza meses posteriores a la evaluación.
- Los dos botones de **Recursos oficiales para verificar información individual** reciben el mismo centrado visual que las demás acciones de Metodología y conservan `Abrir recurso oficial`, porque esos enlaces no son necesariamente fuentes normativas del cálculo.
- `.gitattributes` fuerza LF para todo archivo detectado como texto, incluidos archivos sin extensión, evitando advertencias de conversión LF/CRLF en Windows.
- `/favicon.ico` responde temporalmente con `204 No Content` y `Cache-Control: no-store` hasta integrar el favicon definitivo, eliminando el `404` del navegador sin inventar un icono provisional.
- UX.4.2 mantiene el número del paso activo en blanco cuando el tema efectivo es Claro, mejorando contraste sobre el círculo azul.
- La fila seleccionada de **Fechas y cuotas estimadas de retiro** refuerza su estado mediante fondo, contorno, radio y badge específicos para Claro, Oscuro y Alto contraste, con señal adicional de foco y soporte para colores forzados.
- La suite alcanza **112 pruebas automatizadas** con regresiones específicas de estados activos y selección perceptible.
- UX.4.3 asocia los errores de validación nativa con cada control mediante `aria-errormessage` y limpia ese estado cuando el dato vuelve a ser válido.
- Los errores dinámicos se enfocan al aparecer y usan `role="alert"` sin duplicar una segunda región viva `assertive`; las advertencias no urgentes pueden anunciarse como `status` de prioridad `polite`.
- El selector de escenario de retiro admite Enter sobre el radio, manteniendo la operación nativa con Espacio y flechas sin agregar un tab stop a toda la fila.
- Se corrige un ciclo de mutaciones de clase en la capa de accesibilidad que podía mantener ocupado el hilo principal y dejar las páginas públicas cargando indefinidamente; las mutaciones observadas pasan a ser idempotentes.
- La limpieza de errores usa `ValidityState.valid` en lugar de `checkValidity()`, evitando redisparar eventos `invalid` durante `input`/`change`.
- La suite alcanza **122 pruebas automatizadas** con regresiones específicas de UX.4.3 y su remate de estabilidad.
- UX.4.1 incorpora una capa global de accesibilidad mediante `accesibilidad.js` y `accesibilidad.css`, sin trasladar lógica previsional al frontend.
- Los campos que suelen generar dudas reciben ayudas contextuales desplegables y accesibles mediante `aria-expanded` y `aria-controls`.
- Los formularios marcan controles inválidos con `aria-invalid`, llevan el foco al primer campo que requiere corrección y anuncian el problema mediante una región viva global.
- El wizard relaciona pasos y paneles con regiones etiquetadas; las tablas reciben captions accesibles y sus contenedores desplazables pueden recibir foco cuando existe desbordamiento horizontal.
- Los enlaces que abren una pestaña nueva incorporan una indicación para lectores de pantalla sin añadir ruido visual.
- La suite alcanza **108 pruebas automatizadas** después del remate visual e interactivo de UX.4.1.
- Las ayudas contextuales pasan a un formato compacto tipo tooltip: aparecen con `hover` o foco de teclado y conservan clic como alternativa para interacción táctil.
- El selector del Paso 1 abrevia SUCGS como **Capitalización con Garantía Solidaria** sin cambiar la denominación jurídica utilizada en metodología, resultados o documentación normativa.
- La acción **Completar cuotas vacías con 12** recibe un tratamiento visual propio y distinguible en Claro, Oscuro y Alto contraste.
- En el Paso 5, cualquier punto de una fila de escenario futuro seleccionable activa el mismo escenario que su control de radio.
- En el Paso 6, la acción de cálculo SEBD se alinea con el selector de escenario salarial.
- Node.js LTS se documenta como herramienta opcional de desarrollo para `node --check`; no se incorpora como dependencia de `pip` ni como requisito de ejecución.

### Agregado

#### Cierre funcional 6F

- 6F.1: comparador transversal de escenarios de retiro y salario.
- 6F.2: `Ver cálculo completo` con trazabilidad de datos, regla, fórmula, sustitución y resultado.
- 6F.3: página `/metodologia`, enlaces normativos con nombres humanos y recursos oficiales de verificación.
- 6F.4: contrato transversal `resumen_unificado` para SEBD, Mixto y SUCGS.
- El comparador consume el contrato común en lugar de extraer montos con semánticas distintas de cada motor.
- El Paso 6 presenta un resumen final homogéneo que mantiene separadas mensualidades y pagos únicos.
- Al cierre funcional 6F.4, la suite alcanzó **69 pruebas automatizadas**.
- Mi Retiro Seguro deja de mostrarse como recurso independiente; la verificación individual queda centralizada en Mi Caja Digital junto con el régimen especial identificado.

#### Asistente y base técnica

- Aplicación web local con FastAPI, Jinja2, Bootstrap, CSS y JavaScript.
- Asistente de seis pasos para datos personales, cuotas, historial, proyección, retiro y resultados.
- Estado temporal de simulación en `sessionStorage`.
- Navegación directa entre pasos ya disponibles y barra persistente para flujos largos.
- Normalización salarial entre periodicidades y proyección por salario constante, porcentaje, salario futuro conocido o varios escenarios.
- Línea temporal que separa datos históricos, año actual y proyecciones futuras.
- Precisión monetaria basada en `Decimal` y `ROUND_HALF_UP` al materializar importes.
- Formato monetario con separadores de miles y máximo dos decimales en campos editables.
- Archivos normativos versionados en `normativa/`.
- Documentación técnica, funcional, normativa y de validación.

#### SEBD

- Motor de Pensión de Retiro por Vejez Normal.
- Clasificación automática de Normal, Anticipada, Proporcional y Proporcional Anticipada.
- Tabla mensual de factores de reducción para retiro anticipado.
- Cálculo de Indemnización por Vejez como pago único separado de una pensión mensual.
- Límites máximos ordinario y ampliados conforme a las condiciones implementadas.
- Endpoints directos e integrados para cálculo SEBD.
- Integración visual completa en el Paso 6.
- Regresiones automatizadas, incluida una validación anonimizada que reproduce B/.741.59.

#### Subsistema Mixto

- Motor separado para Componente de Beneficio Definido y Componente de Ahorro Personal.
- Tope de participación de B/.500.00 mensuales en el componente BD, con advertencia cuando el historial anual obliga a aproximar el tope mensual.
- Pensión programada del CAP cuando se suministran saldo y divisor actuarial aplicable.
- Opción explícita `AUTO / PENSION_PROGRAMADA / DEVOLUCION_TOTAL`.
- Devolución total del CAP como pago único cuando corresponde.
- Separación de indemnización BD, devolución CAP y total de pagos únicos.
- Bono de reconocimiento como dato oficial/validado, sin reconstrucción automática no sustentada.
- Garantía futura del Seguro Colectivo de Renta Vitalicia.
- Transición operativa Mixto → SUCGS desde 01/03/2032 con discrepancia normativa documentada.
- Endpoint integrado y presentación visual completa en el Paso 6.

#### SUCGS

- Motor contributivo del artículo 196 con tabla actuarial versionada.
- Fórmula `saldo / 1000 × factor de pensionamiento actuarial`.
- Capa solidaria de los artículos 194 y 195.
- Pensión Garantizada Solidaria y Beneficio Mínimo con valores legales versionados y posibilidad de suministrar valores vigentes confirmados.
- Garantía de reemplazo mínimo del artículo 197.
- Preevaluación del mínimo anual de cuotas y distribución temporal 50 % / 50 %.
- Salario promedio base mensual calculado desde salarios cotizados y meses cotizados.
- Estabilidad salarial del artículo 197 como condición explícita y auditable.
- Endpoints directos e integrados e interfaz completa en el Paso 6.

#### Comparación 6F.1

- Comparador transversal de escenarios de retiro y trayectorias salariales.
- Endpoint `POST /api/simulacion/comparar-escenarios` que reutiliza los servicios integrados SEBD, Mixto y SUCGS.
- Escenario base explícito y diferencias mensuales absolutas y porcentuales.
- Pagos únicos separados de pensiones mensuales dentro de la matriz comparativa.
- Advertencias de saldo constante para comparaciones hipotéticas Mixto y SUCGS.
- Página `/comparar` habilitada con selección de escenarios y tabla responsiva.

#### Pruebas

- Suite automatizada con **60 pruebas** después de 6F.1.
- Casos para precisión monetaria, proyecciones, línea temporal y retiro.
- Regresiones SEBD para modalidades e indemnización.
- Casos Mixto para pensión programada, devolución, garantías y pagos únicos.
- Casos SUCGS para componente contributivo, capa solidaria, garantía de reemplazo y condiciones que impiden aplicarla.

#### Documentación y repositorio

- `docs/INDICE.md` como mapa de la documentación.
- `docs/FUENTES_NORMATIVAS.md` con leyes, artículos, reglamentos, resoluciones y enlaces oficiales.
- Normalización de la numeración ADR en `docs/DECISIONES.md`.
- Reorganización del roadmap y de la documentación por capacidades actuales en lugar de acumulación histórica de subfases.
- Mejora de `.gitignore`, `.gitattributes`, `.editorconfig` y `CONTRIBUTING.md`.
- Los respaldos históricos y paquetes comprimidos de trabajo (`.zip`, `.7z`, `.rar`) se mantienen fuera de la raíz del repositorio; Git conserva la historia versionada y los paquetes locales quedan como respaldo secundario externo.
- Se eliminan archivos `.gitkeep` de directorios que ya contienen archivos versionados reales. `.gitkeep` se conserva únicamente cuando una carpeta vacía necesita existir en el repositorio.

### Cambiado

- JavaScript queda limitado a navegación, presentación, persistencia temporal y comunicación con la API; las fórmulas previsionales permanecen en Python.
- Los datos históricos y proyectados se mantienen diferenciados en todos los pasos.
- La proyección de cuotas respeta primero el cierre del año actual y luego la densidad futura.
- Los escenarios de retiro exigen cobertura suficiente del horizonte salarial o muestran una advertencia.
- Los resultados dependientes se invalidan cuando cambia un dato que los originó.
- `SUCGS` se presenta con su nombre completo en la interfaz.
- Saldo CAP y bono del Mixto reutilizan el formato monetario común; el divisor actuarial no lleva prefijo monetario porque no representa balboas.
- Los pagos únicos y las pensiones mensuales permanecen separados tanto en la API como en la interfaz.
- Los valores normativos sujetos a indexación o actualización no se tratan como constantes eternas.
- La documentación normativa centraliza enlaces oficiales y distingue ley, reglamento y comunicación operativa.

### Corregido

- Estructura Jinja y jerarquía HTML en los pasos del asistente.
- Duplicación accidental de componentes del historial.
- Restauración de scripts específicos de simulación e historial.
- Clasificación visual de años sin cotización.
- Diferencias de un centavo provocadas por redondeos intermedios.
- Proyección de cuotas que podía agregar meses al año actual contra la expectativa declarada por el Asegurado(a).
- Artefactos de punto flotante en campos monetarios.
- Semántica de campos no aplicables en la Indemnización por Vejez, usando `null` en lugar de valores numéricos engañosos.
- Navegación del Paso 6 para reconocer SEBD, Mixto y SUCGS sin tratar motores ya implementados como pendientes.
- Numeración duplicada y no consecutiva de ADR en la documentación.
- Secciones documentales obsoletas que seguían marcando como pendientes motores ya implementados.

### Pendiente para fases posteriores

- Preparación de estructura para informes y PDF.
- Persistencia voluntaria con SQLite.
- Pulido final de identidad visual, temas, accesibilidad y enlaces institucionales.

### 6F.3 — Metodología y fuentes

- Se agrega `/metodologia` como punto central de consulta de metodología, artículos, reglamentos, resoluciones y recursos oficiales.
- `Ver cálculo completo` deja de mostrar identificadores internos como `texto_unico` o `ley_462`; ahora presenta nombres humanos y enlaces oficiales.
- Se centraliza la presentación de fuentes de SEBD, Mixto y SUCGS reutilizando las URLs versionadas de `normativa/*.json`.
- Se documentan limitaciones conocidas, jerarquía de fuentes y recursos oficiales de verificación individual.
