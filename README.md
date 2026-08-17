# Mi Retiro Proyectado

Aplicación web local para **estimar y explicar** prestaciones de retiro de la Caja de Seguro Social (CSS) de Panamá a partir de datos de edad, cuotas, historial salarial, proyección de ingresos, escenario de retiro y sistema previsional.

**Nombre de producto:** Mi Retiro Proyectado. Está dirigido a **Asegurados(as)** que desean analizar escenarios previsionales con trazabilidad normativa.

> **Herramienta independiente de la CSS.** No es una aplicación oficial de la Caja de Seguro Social, no emite certificaciones y no sustituye una resolución de la CSS. Los resultados son estimaciones sujetas a la calidad de los datos ingresados y a la normativa vigente aplicable al caso individual.

## 1. Sistemas contemplados

La aplicación dispone actualmente de motores e integración visual para:

- **SEBD — Subsistema Exclusivamente de Beneficio Definido**;
- **Subsistema Mixto**;
- **SUCGS — Sistema Único de Capitalización con Garantía Solidaria**.

El desarrollo actual cubre las reglas generales implementadas para estos sistemas. Regímenes especiales requieren motores específicos y no deben asumirse cubiertos por el cálculo general.

## 2. Estado actual del desarrollo

La próxima versión `0.1.0` continúa en desarrollo. El asistente de seis pasos y los tres motores principales están implementados y validados con pruebas automatizadas y casos manuales.

| Área | Estado |
|---|---|
| Paso 1 — Datos personales y sistema | Implementado |
| Paso 2 — Cuotas | Implementado |
| Paso 3 — Historial salarial y base para proyección | UX.4.6d cerrada y validada en PC/laptop; integración Paso 1→3 certificada |
| Paso 4 — Proyección salarial | Implementado |
| Paso 5 — Escenarios de retiro | Implementado |
| Paso 6 — Resultados SEBD | Implementado |
| Paso 6 — Resultados Mixto | Implementado |
| Paso 6 — Resultados SUCGS | Implementado |
| Navegación directa entre pasos | Implementada |
| Comparador de escenarios — 6F.1 | Implementado |
| Ver cálculo completo — 6F.2 | Implementado |
| Metodología y fuentes — 6F.3 | Implementado |
| Unificación final de resultados — 6F.4 | Implementado |
| Persistencia permanente / SQLite | Pendiente |
| Informes PDF | Pendiente |
| Identidad, terminología y tipografía de producto | Implementado |
| Temas visuales y persistencia local | Implementados |
| Accesibilidad base: teclado, foco, movimiento reducido y objetivos táctiles | Implementada |
| Estabilización visual Claro/Oscuro/Alto contraste | Implementada |
| UX.3 — responsive real y navegación móvil | Implementada; validación manual inmediata en PC/laptop, multidispositivo diferida |
| UX.4.1 — semántica accesible y ayudas contextuales | Implementada y revisada manualmente en PC/laptop |
| UX.4.2 — estados activos y selección perceptible | Implementada y revisada manualmente en PC/laptop |
| UX.4.3 — errores, foco y operación por teclado | Validada manualmente en PC/laptop |
| UX.4.4 — edad anual, detalle salarial e importación oficial revisable | Implementada y validada manualmente en PC/laptop |
| UX.4.5 — origen acreditado/proyectado y cierre accesible | Implementada técnicamente; pendiente validación manual de cierre en PC/laptop |
| UX.4.6a — rediseño visual integral e Inicio | Cerrada y validada en PC/laptop |
| UX.4.6b — Simular / Paso 1 · Datos personales | Cerrada y validada en PC/laptop |
| UX.4.6c — Simular / Paso 2 · Cuotas | Cerrada y validada en PC/laptop; 253 pruebas automatizadas en OK |
| UX.4.6d — Simular / Paso 3 · Historial | Cerrada y validada en PC/laptop; R23 sincroniza Ficha Digital, Cuotas e historial sin navegación regresiva |

La suite actual contiene **396 pruebas automatizadas**. UX.3 protege responsive y la separación entre evaluación y último mes acreditado; UX.4.1–UX.4.3 cubren semántica del wizard, ayudas contextuales, validación accesible, estados seleccionados, recuperación de foco y estabilidad del `MutationObserver`; UX.4.4 añade la edad anual, un detalle opcional del año actual que separa salario disponible, cuota acreditada y períodos parciales, bases salariales recientes y una importación revisable de documentos oficiales. La Ficha Digital conserva únicamente salarios del año calendario actual y las vistas previas monetarias usan separador de miles con dos decimales.

## Hardening previo a beta

La preparación pre-beta incorpora una regresión E2E sobre los endpoints integrados de SEBD, Mixto y SUCGS, validación defensiva común para PDFs, cabeceras de navegador orientadas a privacidad local y CI en GitHub Actions. Los importadores rechazan extensión/MIME incompatibles, archivos vacíos, exceso de tamaño y contenido sin firma PDF antes de invocar `pypdf`.

La estrategia y los límites están documentados en [`docs/SEGURIDAD_PRIVACIDAD.md`](docs/SEGURIDAD_PRIVACIDAD.md). La CI se ejecuta sobre Python 3.13 y 3.14 y valida también la sintaxis de todo el JavaScript. La primera ejecución remota de `main` quedó en verde. Dependabot propone semanalmente actualizaciones de las dependencias directas mantenidas por el proyecto y de GitHub Actions; las Actions se agrupan y las pruebas verifican su presencia y contrato, no un major congelado. No existe auto-merge.

## 3. Qué permite hacer el asistente

El Asegurado(a) puede:

1. registrar fecha de nacimiento, sexo, fecha de ingreso y sistema previsional;
2. registrar cuotas acreditadas y expectativas de cotización futura;
3. construir un historial anual de cuotas y salarios cotizados;
4. opcionalmente detallar el año actual por total mensual o por quincenas, marcando qué meses ya tienen cuota acreditada;
5. elegir una base salarial manual o derivada de meses completos recientes y normalizarla para proyección;
6. proyectar salario constante, variación porcentual, salario futuro conocido o varios escenarios;
7. combinar historial real y proyección en una línea temporal trazable;
8. derivar el último mes acreditado desde el detalle reciente cuando las cuotas coinciden, o indicarlo manualmente cuando no existe ese detalle;
9. seleccionar directamente cualquier paso disponible para revisar datos;
10. calcular la prestación aplicable según el motor del sistema seleccionado;
11. ver componentes mensuales, pagos únicos, factores y advertencias cuando correspondan;
12. comparar combinaciones de fechas de retiro y escenarios salariales contra un escenario base, con diferencias absolutas y porcentuales.

## 4. Alcance de los motores

### 4.1. SEBD

El motor general cubre:

- Pensión de Retiro por Vejez Normal;
- Pensión de Retiro por Vejez Anticipada;
- Pensión de Retiro por Vejez Proporcional;
- Pensión de Retiro por Vejez Proporcional Anticipada;
- Indemnización por Vejez como pago único;
- límites máximos según las condiciones implementadas;
- transición de la indemnización al SUCGS desde la fecha legal correspondiente.

El monto mínimo indexado del artículo 192 no se fuerza sin un valor vigente versionado para la fecha de cálculo.

### 4.2. Subsistema Mixto

El motor mantiene separados:

- **Componente de Beneficio Definido (BD)**;
- **Componente de Ahorro Personal (CAP)**;
- pensión programada del CAP;
- devolución total del CAP cuando corresponde;
- indemnización del componente BD;
- pagos únicos frente a pagos mensuales;
- garantía futura del Seguro Colectivo de Renta Vitalicia;
- bono de reconocimiento informado/validado;
- transición operativa hacia SUCGS.

El saldo CAP y el valor actuarial no se reconstruyen artificialmente a partir del historial anual.

### 4.3. SUCGS

El motor implementa por capas:

1. componente contributivo del artículo 196;
2. componente solidario y referencias de los artículos 194 y 195;
3. garantía de reemplazo mínimo del artículo 197;
4. presentación de la pensión total cuando las condiciones pueden evaluarse.

Los valores solidarios sujetos a indexación pueden sustituirse por valores vigentes confirmados. La estabilidad salarial del artículo 197 permanece como confirmación explícita cuando la redacción o el mecanismo de control no permiten una deducción segura desde el historial anual.

## 5. Normativa y trazabilidad

Los parámetros legales no se dispersan dentro de la interfaz. Se mantienen versionados en `normativa/` y se documentan con su fuente.

Documentos principales:

- [Normativa implementada](docs/NORMATIVA.md)
- [Fuentes normativas y enlaces oficiales](docs/FUENTES_NORMATIVAS.md)
- [Modalidades SEBD](docs/MODALIDADES_SEBD.md)
- [Subsistema Mixto](docs/MODALIDADES_MIXTO.md)
- [SUCGS](docs/MODALIDADES_SUCGS.md)
- [Guía interna de desarrollo](docs/GUIA_INTERNA_DESARROLLO.md)

Fuente legal consolidada utilizada por el proyecto:

- [Normativa de la Ley Orgánica — CSS](https://www.css.gob.pa/normativas-ley-organica/)
- [Texto Único de la Ley 51 de 2005 — PDF CSS](https://www.css.gob.pa/wp-content/uploads/2025/05/TEXTO-UNICO-DE-LA-LEY-51-DE-2005-CSS-GACETA-OFICIAL-22-5-25.pdf)
- [Normativa de Prestaciones Económicas — CSS](https://www.css.gob.pa/normativa-prestaciones-economicas/)

## 6. Arquitectura resumida

```text
calculadora-pension-css/
├── app/
│   ├── core/          # configuración, dinero y carga normativa
│   ├── modelos/       # modelos Pydantic
│   ├── motores/       # SEBD, Mixto y SUCGS
│   ├── servicios/     # integración de pasos, proyecciones y resultados
│   ├── static/        # CSS y JavaScript
│   ├── templates/     # Jinja2
│   └── main.py        # FastAPI y endpoints
├── data/              # datos locales; información sensible no se versiona
├── docs/              # documentación funcional, técnica y normativa
├── normativa/         # parámetros legales versionados
├── tests/             # regresiones automatizadas
├── .editorconfig
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
└── requirements.txt
```

Para una descripción completa: [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md).

Los paquetes comprimidos y respaldos históricos no forman parte de esta estructura. Deben conservarse fuera de la raíz del repositorio para mantener limpia la copia de trabajo. Los archivos `.gitkeep` se usan únicamente en directorios vacíos que necesitan existir en Git y se eliminan cuando la carpeta ya contiene archivos versionados reales.

## 7. Tecnologías

Actualmente:

- Python;
- FastAPI;
- Uvicorn;
- Pydantic;
- Jinja2;
- HTML/CSS/JavaScript;
- Bootstrap;
- `sessionStorage` para estado temporal del asistente;
- `localStorage` exclusivamente para la preferencia visual del Asegurado(a);
- `unittest` para regresiones automatizadas.

Previstas en fases posteriores:

- SQLite para guardado voluntario;
- Chart.js para visualizaciones comparativas;
- generación de informes PDF.

## 8. Apariencia y accesibilidad

UX.4.6a consolida la presentación mediante `app/static/css/design-system.css`, cargado después de la base histórica `style.css` y antes de `accesibilidad.css`. Esta capa define la paleta, superficies, controles, cards, navegación, footer y jerarquía visual sin modificar contratos previsionales.

El control de apariencia es compacto y presenta como opciones principales:

- **Automático** — sigue la preferencia del sistema;
- **Claro**;
- **Oscuro**.

**Alto contraste** permanece disponible como opción secundaria de **Accesibilidad**. La preferencia se conserva localmente en el navegador y no se mezcla con los datos previsionales de la simulación.

El modo Oscuro usa un fondo profundo casi negro y superficies diferenciadas; Alto contraste conserva negro/blanco, bordes explícitos y foco amarillo. La interfaz mantiene enlace de salto al contenido, foco visible para teclado, objetivos táctiles con altura mínima y soporte para `prefers-reduced-motion`.

El footer global se centra y conserva nombre del producto, versión, aviso de independencia, enlace a **Fuentes oficiales**, autoría y copyright. **Mi Caja Digital** ya no se duplica en el footer: continúa disponible únicamente en los puntos funcionales donde sirve para verificar información individual.

UX.4.1 amplía esta base con ayudas contextuales compactas que aparecen al pasar el puntero o al recibir foco —con clic como alternativa táctil—, regiones dinámicas para mensajes de error y estado, marcado `aria-invalid` con foco sobre el primer campo inválido, relaciones semánticas entre pasos y paneles del asistente, captions accesibles en tablas y aviso no visual para enlaces que abren una pestaña nueva. También mejora la selección de escenarios de retiro desde toda la fila y corrige pequeños detalles de jerarquía y alineación. UX.4.2 refuerza estados activos y seleccionados: el número del paso activo usa texto blanco cuando el tema resuelto es Claro y la fila seleccionada de escenarios de retiro combina fondo, contorno, radio y badge diferenciados por tema, además de señal de foco y compatibilidad con colores forzados. UX.4.3 mejora la recuperación ante errores: los controles inválidos reciben un mensaje inline visible y asociado programáticamente mediante `aria-errormessage`, los errores dinámicos reciben foco cuando aparecen sin duplicar regiones `assertive`, las advertencias no urgentes pueden usar estado `polite` y el radio de escenarios de retiro admite Enter además de la operación nativa con teclado. El remate de estabilidad evita escrituras redundantes de clases dentro del `MutationObserver` y consulta `ValidityState.valid` sin redisparar eventos `invalid`, previniendo bloqueos o bucles de retroalimentación del frontend. UX.4.4 añade la columna **Edad** en las tablas de Historial salarial real y Proyección futura. La edad mostrada es la que el Asegurado(a) cumple durante el año calendario (`año - año de nacimiento`), siguiendo la convención observada en los comprobantes oficiales usados para validación. También incorpora un detalle opcional del año actual: puede capturarse un total mensual o primera/segunda quincena, marcar si la cuota ya está acreditada y distinguir meses completos, parciales o sin información. La suma de meses acreditados sincroniza el salario anual actual únicamente cuando coincide con las cuotas del Paso 2; los salarios visibles sin cuota acreditada permanecen separados. Para proyectar, el Asegurado(a) puede continuar con ingreso manual o usar el último mes completo, el promedio de meses completos del año actual, el promedio de los últimos tres meses completos o el promedio del salario acreditado por cuota del año actual.  UX.4.4 también permite cargar de forma opcional un comprobante PDF de Mi Retiro Seguro: el archivo se procesa en memoria, puede devolver de forma opcional nombre, cédula y número de Seguro Social cuando el PDF los etiqueta de forma inequívoca; el código único del documento continúa excluido, y se extraen de forma variable el sistema elegido, la edad de retiro, las cuotas históricas y el monto estimado. En el Paso 6 esa referencia personal se compara preferentemente con la fotografía propia de información acreditada cuando sistema, persona, edad y naturaleza de la prestación son compatibles; ningún monto de un comprobante concreto queda hardcodeado en la aplicación. La auditoría integral WCAG 2.2 con tecnologías de apoyo continúa dentro de la Fase 8.

### UX.4.6a — rediseño visual integral

La página de Inicio se orienta a beneficios y tareas del Asegurado(a), utiliza un mockup sin resultados monetarios ficticios y conserva la explicación de SEBD, Mixto y SUCGS sin exponer detalles de motores internos. La navegación pública se simplifica a **Inicio, Simular, Escenarios y Fuentes** sin cambiar rutas. La revisión final en PC/laptop ajustó escala del hero, centrado de los seis pasos, continuidad del aviso orientativo y composición centrada del footer. La validación multidispositivo permanece diferida para beta/RC.

### UX.4.6b — Paso 1 de Simular

El Paso 1 separa la captura **Manual** de la importación de **Mi Retiro Seguro**. Los identificadores personales son opcionales; fecha de nacimiento, sexo y sistema previsional se señalan como campos obligatorios y conservan validación accesible inline. La Ficha Digital se presenta en el Paso 3.

Antes de ingresar o importar información, la ruta **Simular** solicita un consentimiento informado y versionado sobre privacidad y tratamiento de datos. El documento visible contiene 21 apartados y la casilla de aceptación solo se habilita después de que el usuario llega al final. La Revisión 4 elimina mensajes meta como **Fin de los términos** o **Lectura completada**: el requisito de desplazamiento se mantiene sin añadir contenido que no forme parte del contrato. La versión actual no utiliza cookies de publicidad, analítica, seguimiento ni perfilado. El navegador mantiene temporalmente la simulación y puede recordar preferencias de funcionamiento y la versión aceptada de los términos. Rechazar el tratamiento devuelve a Inicio y elimina el estado temporal de esa simulación.

La vista previa de Mi Retiro Seguro abre en modo revisión. **Editar campos** habilita correcciones, **Finalizar edición** vuelve a bloquear los controles y **Importar datos** aplica lo confirmado. El parser puede descomponer nombres completos de forma conservadora y reconoce el patrón final `de Apellido` como apellido de casada cuando aparece en un nombre femenino; toda información importada sigue siendo revisable antes de aplicarse.

Los seis pasos comparten navegación superior e inferior sincronizada y alineada al mismo ancho de las tarjetas. En PC/laptop la superior permanece disponible durante formularios largos y la inferior ofrece la misma navegación al terminar el paso. Las tablas refuerzan el hover y las ayudas contextuales utilizan un botón compacto de información con icono `i`, sin texto redundante, que se reposiciona para evitar recortes.

La política detallada se documenta en [Política de privacidad](docs/POLITICA_PRIVACIDAD.md), [Términos de uso y tratamiento de datos](docs/TERMINOS_USO_PRIVACIDAD.md) y [Matriz de alineación con Ley 81](docs/CUMPLIMIENTO_LEY_81.md). La publicación pública/comercial deberá someter estos textos y controles a revisión jurídica formal.

La Revisión 4 de UX.4.6b quedó validada técnica y visualmente en PC/laptop y fue cerrada en `main` con CI verde en Python 3.13 y 3.14. La redacción pública se mantiene centrada en la finalidad previsional, funcional, legal y de privacidad del producto, sin posicionarlo como aplicación educativa o exponer jerga interna innecesaria.

### UX.4.6c — Paso 2 de Simular

UX.4.6c reorganiza el Paso 2 en **Cuotas acreditadas** y **Cotización futura**, aplica el mismo contrato de obligatoriedad accesible del Paso 1 y elimina acciones duplicadas dentro de la tarjeta. Cuando Mi Retiro Seguro aporta una cuota, ese campo se mantiene sin cambios en el Paso 2; si el PDF no aporta el dato, el control permanece habilitado para completarlo manualmente. Las correcciones de datos importados se realizan desde la vista previa del documento. El selector global de apariencia reemplaza el símbolo abstracto por iconos SVG de sistema, claro, oscuro y alto contraste. La Revisión 2 corrige la reapertura de la vista previa desde pasos posteriores, simplifica el mensaje de procedencia importada, normaliza `* Campo obligatorio`, elimina la palabra visible `Info` de las ayudas y añade pistas internas en campos editables que desaparecen cuando existe un valor. La Revisión 3 elimina el doble contorno visual del icono `i` y hace que **Revisar importación** sea contextual: Paso 1 muestra toda la información extraída y Paso 2 únicamente **Cuotas acreditadas (Paso 2)**. La vista previa etiqueta además cada grupo con su etapa de destino para reutilizar el mismo patrón en los pasos siguientes. Queda cerrada y validada en PC/laptop con **253 pruebas automatizadas en OK**.

## 9. Instalación

### UX.4.6d — Paso 3 de Simular

UX.4.6d reorganiza el Paso 3 como **Historial salarial anual**, **Detalle salarial del año actual** y **Base salarial para proyección**, con una sola acción principal desde las barras del asistente. La Revisión 2 corrigió inicialmente la interacción entre Ficha Digital y Cuotas evitando que una importación incompleta sustituyera el total del Paso 2; desde R23 esa regla queda refinada: una Ficha Digital confirmada que aporta **más cuotas acreditadas del año actual** puede ampliar la referencia agregada sin navegación regresiva, mientras una ficha con menos meses nunca reduce silenciosamente un valor superior. La Revisión 3 establece que los meses efectivamente detectados en una Ficha Digital se incorporan con su casilla de cuota marcada y bloqueada; los meses no presentes en el documento permanecen disponibles para captura manual. Las filas con información documental se distinguen visualmente de las filas manuales mediante un estilo de procedencia común reutilizable en tablas del asistente. El mismo principio se aplica a casillas cuya selección representa una clasificación importada: su estado automático no puede alterarse directamente en la pantalla principal. La Revisión 4 sustituye el verde de procedencia por una señal azul basada en la paleta primaria. La Revisión 5 corrige de forma defensiva la representación y lectura de las casillas de cuotas mensuales importadas: un mes documental siempre se muestra seleccionado, permanece bloqueado y se interpreta como seleccionado para el cálculo aun al restaurar estados generados por revisiones anteriores. La Revisión 6 añade gestión global de datos con **Limpiar este paso**, **Reiniciar simulación** y borrado integral local desde Fuentes/Privacidad; las dependencias posteriores se invalidan de forma determinista. La versión de privacidad se actualiza a **2026-08-15.1** para reflejar estos controles. La Revisión 7 hace que **Revisar términos de privacidad** abra el documento en la misma página y en modo consulta, sin alterar la aceptación vigente ni exigir una nueva aceptación; el modal incorpora cierre con `×`. El menú **Opciones** permanece exclusivo de la barra sticky superior. La validación visual y funcional completa en PC/laptop quedó cerrada posteriormente en R23. La Revisión 8 corrige los estados progresivos de la tabla anual, muestra inmediatamente el resumen del historial analizado, normaliza el color de **Seleccionar archivo** y evita que advertencias inline desalineen filas de Ficha Digital. La Revisión 9 refuerza la reactividad mediante eventos delegados para que estados y filtro **Pendientes** se actualicen mientras se escribe, elimina el carril vertical en tablas cortas y completa el comportamiento de privacidad pendiente: consentimiento desde Fuentes cuando aún no existe aceptación, cierre contextual con `Esc` y ejemplos de captura ficticios/genéricos. La Revisión 10 establece `app-table-shell` como contrato visual transversal para todas las tablas actuales y futuras: bordes redondeados coherentes con la interfaz, superficie/encabezado adaptados a Claro, Oscuro y Alto contraste y reutilización del mismo contenedor accesible en tablas estáticas y dinámicas. Los comportamientos funcionales específicos —estados progresivos, filtros reactivos, bloqueo documental o casillas— se reutilizan únicamente cuando la semántica de la tabla lo requiere. La Revisión 11 termina de integrar el scroll dentro de esa geometría: elimina los botones/flechas nativos del carril en Chromium/Windows, mantiene el track alejado de las esquinas redondeadas y adapta el thumb a los tres temas. También fija una altura exterior única para **Seleccionar archivo** y **Analizar documento** en todos los importadores PDF. La Revisión 12 extiende el scrollbar temático a términos, modales y otras superficies desplazables, reduce ligeramente el radio específico de las tablas para integrar mejor el carril, oculta por completo la tabla cuando el filtro **Pendientes** llega a cero y estabiliza el color de **Seleccionar archivo** para que no cambie al pasar el puntero por el nombre del archivo. La tabla de Comparador conserva el mismo contrato transversal `app-table-shell`.

### 9.1. Clonar el repositorio

```powershell
git clone https://github.com/recm0708/calculadora-pension-css.git
cd calculadora-pension-css
```

### 9.2. Crear y activar el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 9.3. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

`requirements.txt` contiene únicamente dependencias Python. **Node.js no es necesario para ejecutar la aplicación**; se utiliza de forma opcional durante desarrollo para validar sintaxis JavaScript con `node --check`.

En Windows, si se desea habilitar esa validación auxiliar:

```powershell
winget install --id OpenJS.NodeJS.LTS -e --source winget
```

Después de instalarlo, abrir una terminal nueva y comprobar:

```powershell
node --version
npm --version
```

## 10. Ejecución

```powershell
python -m uvicorn app.main:app --reload
```

Abrir:

```text
http://127.0.0.1:8000
```

Swagger/OpenAPI:

```text
http://127.0.0.1:8000/docs
```

## 11. API disponible

```text
GET  /
GET  /simulacion
GET  /comparar
GET  /salud

POST /api/simulacion/cuotas
POST /api/simulacion/historial-salarial
POST /api/simulacion/salario
POST /api/simulacion/proyeccion-salario
POST /api/simulacion/linea-tiempo
POST /api/simulacion/retiro

POST /api/simulacion/sebd/normal
POST /api/simulacion/resultados/sebd-normal
POST /api/simulacion/sebd
POST /api/simulacion/resultados/sebd

POST /api/simulacion/mixto
POST /api/simulacion/resultados/mixto

POST /api/simulacion/sucgs
POST /api/simulacion/resultados/sucgs
```

## 11. Validación local

Antes de consolidar cambios:

```powershell
python -m compileall app
python -m unittest discover -s tests -v
```

La estrategia y los casos de regresión se documentan en [docs/VALIDACION.md](docs/VALIDACION.md).

## 12. Precisión monetaria

Los cálculos monetarios sensibles usan `Decimal` y las utilidades de `app/core/dinero.py`.

Criterio técnico general:

- mantener precisión interna durante las operaciones;
- materializar importes a dos decimales;
- usar `ROUND_HALF_UP`, salvo que una norma aplicable establezca otro criterio;
- no redondear valores intermedios únicamente para forzar coincidencias visuales.

## 13. Privacidad

El repositorio no debe contener información personal real utilizada para validación.

`.gitignore` excluye, entre otros:

- `data/personales/`;
- `data/importaciones/`;
- `data/documentos_personales/`;
- `tests/casos_validacion/originales/`;
- PDF dentro de los casos de validación;
- bases de datos locales, archivos `.env`, logs y copias comprimidas.

Los casos versionados deben estar anonimizados o ser completamente sintéticos.

## 14. Documentación

Punto de entrada: [docs/INDICE.md](docs/INDICE.md).

Documentos clave:

- [Especificación funcional](docs/ESPECIFICACION_FUNCIONAL.md)
- [Arquitectura](docs/ARQUITECTURA.md)
- [Modelo de datos](docs/MODELO_DE_DATOS.md)
- [Motor de cálculo](docs/MOTOR_DE_CALCULO.md)
- [Normativa](docs/NORMATIVA.md)
- [Fuentes normativas](docs/FUENTES_NORMATIVAS.md)
- [Decisiones técnicas](docs/DECISIONES.md)
- [Validación](docs/VALIDACION.md)
- [Roadmap](docs/ROADMAP.md)

## 15. Cierre de la Fase 6 y siguiente trabajo

La **Fase 6 — Resultados, comparación y transparencia** queda cerrada funcionalmente con 6F.1–6F.4. Los tres sistemas comparten ahora una salida transversal que conserva por separado pensiones mensuales, pagos únicos, estado del cálculo, naturaleza de la prestación, modalidad, advertencias y trazabilidad.

La página `/metodologia` centraliza las fuentes legales y reglamentarias utilizadas por los motores. `Ver cálculo completo` presenta datos, reglas, fórmulas, sustituciones y enlaces oficiales con nombres legibles.

Los siguientes bloques del roadmap son persistencia/informes y el pulido de producto: identidad visual, accesibilidad, temas, pie de página, enlaces institucionales y mejoras responsivas.


### UX.4.5 — lectura del resultado por origen de datos

El Paso 6 calcula ahora dos fotografías con la misma fecha de retiro seleccionada. **Solo información acreditada** conserva únicamente salarios y cuotas ya registrados en el historial actual; **Proyección al retiro** incorpora las cotizaciones futuras del escenario seleccionado. La comparación es propia de la aplicación y existe aunque no se cargue un comprobante de Mi Retiro Seguro.

Cuando existe una referencia PDF personal, la comparación con ese comprobante prefiere la fotografía acreditada propia. Esto evita comparar directamente una fotografía histórica con una proyección que añade meses futuros. En Mixto y SUCGS, saldos y parámetros específicos introducidos en el Paso 6 se mantienen iguales entre ambas fotografías: la aplicación no proyecta automáticamente saldos que no puede reconstruir con fuentes oficiales.

La validación manual inmediata de UX.4.5 se concentra en PC/laptop. Las reglas responsive continúan protegidas por pruebas automatizadas; una comprobación real desde un teléfono Android en la misma red local puede realizarse como validación adicional. Tablet Android, iPhone/iPad, pantallas de escritorio muy grandes y equipos macOS quedan como matriz ampliada de compatibilidad y no bloquean por sí solos la primera beta mientras no aparezca una incidencia concreta.
UX.4.6d quedó cerrada tras R23 con **396 pruebas automatizadas en OK**, validación manual integral de Pasos 1–3 en PC/laptop y acceso correcto a Paso 4.

## UX.4.6d R15 — diferenciación de campos y limpieza real del Paso 2

Durante el recorrido integral se validó completamente Paso 1 manual e importado. R15 refuerza la diferencia entre controles editables y bloqueados en los tres temas mediante tokens comunes de formulario, hace que la copia visible de importación sea neutral respecto del formato del documento y corrige **Limpiar este paso** en Paso 2 para no conservar supuestos de cotización futura. El parser actual sigue recibiendo PDF digital; la UX y el contrato de importación quedan preparados para evolucionar sin convertir el formato en parte del lenguaje del producto.

## UX.4.6d R16 — flujo no regresivo y Ficha Digital integrada

R16 corrige una condición detectada durante el recorrido integral: Paso 3 no debe obligar al usuario a retroceder a Cuotas cuando los valores del Paso 2 siguen completos y únicamente se perdió su resumen derivado. Antes de analizar historial, la interfaz intenta revalidar las cuotas en segundo plano; si realmente faltan datos, mantiene al usuario en Paso 3, conserva su trabajo y explica qué dependencia debe completar. Al restaurar una sesión, el asistente tampoco vuelve a abrir un paso posterior cuyos prerrequisitos hayan sido limpiados o invalidados.

La jerarquía del Paso 3 queda como **Historial salarial anual → Detalle salarial del año actual → Base salarial para proyección**. Ficha Digital deja de ser una sección global independiente y pasa a estar integrada dentro de **Detalle salarial del año actual**; su cargador aparece antes de la tabla mensual que alimenta, de modo que fuente, revisión y resultado sigan el orden natural de lectura. No se modifican motores, fórmulas ni parsers.


### UX.4.6d R17 — auditoría documental de Pasos 1–3

- La vista previa de Mi Retiro Seguro diferencia **bloqueado** de **seleccionado**: una casilla documental solo muestra gancho cuando su valor booleano real está marcado. Las filas `HISTORICO_PROYECTADO` y `PROYECTADO` permanecen excluidas del historial real por defecto.
- La revisión de cuotas explica cuándo el total acumulado del comprobante incluye períodos proyectados y conserva por separado las cuotas ya acreditadas.
- El importador emite una advertencia no bloqueante cuando el propio comprobante contiene historial anterior a la fecha de ingreso CSS indicada.
- Los campos modificados durante **Editar campos** se identifican como **Editado por ti** o **Completado manualmente**, evitando presentarlos después como si hubieran sido detectados literalmente en el documento.
- El detalle del año actual distingue explícitamente salario disponible de cuota acreditada cuando existe una diferencia con el Paso 2.


### UX.4.6d R19 — sincronización del año actual

Cuando **Detalle salarial del año actual** está habilitado, la fila del año vigente en **Historial salarial anual** deja de ser una segunda captura independiente: sus cuotas y salario anual se derivan de los meses marcados con **Cuota acreditada** y de sus salarios conocidos. La actualización es reactiva; por ejemplo, enero–junio acreditados con salarios confirmados producen 6 cuotas y B/.8,883.50 para 2026.

Una casilla manual de **Cuota acreditada** constituye una confirmación explícita del usuario sobre información más reciente que la fotografía del comprobante. Si el conteo cambia respecto de Paso 2, la aplicación actualiza `cuotas_anio_actual` y `cuotas_totales` conservando las cuotas anteriores al año vigente, invalida los resúmenes dependientes y los revalida al analizar sin navegar hacia atrás. La procedencia queda registrada como edición del usuario.

El salario anual derivado solo suma meses con cuota marcada. Un salario conocido sin cuota acreditada permanece disponible para las bases recientes, pero no se incorpora al historial acreditado. Si una cuota marcada carece todavía de salario, la fila anual continúa indicando que falta salario y el análisis mensual mantiene su validación.

### UX.4.6d R22 — cierre robusto del Paso 3

El análisis del Paso 3 reconcilia antes de validar las cuotas manuales confirmadas en el detalle del año actual con la referencia del Paso 2 y revalida esa dependencia sin navegación regresiva. Si todavía existe una diferencia real, la interfaz muestra un mensaje explícito con los conteos implicados. El resumen visible del año actual conserva todas sus métricas porque cada una representa una dimensión distinta del dato reciente o una base salarial automática.



### UX.4.6d R23 — Ficha Digital como evidencia mensual más reciente

Cuando una Ficha Digital confirmada contiene más meses con **Cuota acreditada** que la referencia agregada del Paso 2, la aplicación actualiza hacia arriba `cuotas_anio_actual` y `cuotas_totales`, revalida Cuotas en segundo plano y conserva el flujo en Paso 3. La regla es monotónica para la importación documental: una ficha con menos meses nunca reduce automáticamente una referencia superior; en ese caso se conserva Paso 2 y se pide revisar/completar el detalle. Esta regla cubre tanto la importación inicial como la reconciliación defensiva al pulsar **Analizar historial** después de F5/restauración.

### Cierre UX.4.6d

La fase quedó validada manualmente en PC/laptop con recorrido limpio desde consentimiento y Paso 1 hasta **Continuar a proyección**. El caso final confirmó 5→6 cuotas del año actual desde Ficha Digital, actualización 281→282 acumuladas, fila 2026 derivada en 6 cuotas/B/.8,883.50, persistencia tras F5 y entrada al Paso 4 sin retrocesos. La suite de cierre alcanza **396 pruebas automatizadas en OK**.
