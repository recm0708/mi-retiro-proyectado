# Changelog

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
