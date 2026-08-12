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
| Paso 3 — Historial salarial y salario actual | Implementado |
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

La suite actual contiene **108 pruebas automatizadas**. UX.3 añade regresiones para responsive, navegación móvil y la separación entre fecha de evaluación y último mes con cuotas acreditadas en el Paso 5; las regresiones de mantenimiento técnico verifican la normalización LF y la respuesta temporal de `/favicon.ico`; UX.4.1 incorpora pruebas para semántica del wizard, ayudas contextuales, validación accesible, tablas desplazables, enlaces externos y los ajustes visuales finales validados en PC/laptop.

## 3. Qué permite hacer el asistente

El Asegurado(a) puede:

1. registrar fecha de nacimiento, sexo, fecha de ingreso y sistema previsional;
2. registrar cuotas acreditadas y expectativas de cotización futura;
3. construir un historial anual de cuotas y salarios cotizados;
4. ingresar salario actual y normalizarlo entre periodicidades;
5. proyectar salario constante, variación porcentual, salario futuro conocido o varios escenarios;
6. combinar historial real y proyección en una línea temporal trazable;
7. indicar el último mes con cuotas acreditadas y construir escenarios de retiro por fecha y años adicionales;
8. seleccionar directamente cualquier paso disponible para revisar datos;
9. calcular la prestación aplicable según el motor del sistema seleccionado;
10. ver componentes mensuales, pagos únicos, factores y advertencias cuando correspondan;
11. comparar combinaciones de fechas de retiro y escenarios salariales contra un escenario base, con diferencias absolutas y porcentuales.

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

La interfaz ofrece cuatro preferencias visuales:

- **Seguir sistema**;
- **Claro**;
- **Oscuro**;
- **Alto contraste**.

La interfaz usa colores semánticos por tema para superficies, textos, estados y alertas. El modo Oscuro prioriza fondos casi negros y texto de alta legibilidad; Alto contraste usa negro, blanco, bordes explícitos y foco visible.

La preferencia se conserva localmente en el navegador y no se mezcla con los datos previsionales de la simulación. La interfaz incluye enlace de salto al contenido, foco visible para teclado, objetivos táctiles con altura mínima, soporte para `prefers-reduced-motion` y un pie de página compacto con autoría, aviso de independencia y acceso a Mi Caja Digital.

UX.4.1 amplía esta base con ayudas contextuales compactas que aparecen al pasar el puntero o al recibir foco —con clic como alternativa táctil—, regiones dinámicas para mensajes de error y estado, marcado `aria-invalid` con foco sobre el primer campo inválido, relaciones semánticas entre pasos y paneles del asistente, captions accesibles en tablas y aviso no visual para enlaces que abren una pestaña nueva. También mejora la selección de escenarios de retiro desde toda la fila y corrige pequeños detalles de jerarquía y alineación. La auditoría integral WCAG 2.2 con tecnologías de apoyo continúa dentro de la Fase 8.

## 9. Instalación

### 8.1. Clonar el repositorio

```powershell
git clone https://github.com/recm0708/calculadora-pension-css.git
cd calculadora-pension-css
```

### 8.2. Crear y activar el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 8.3. Instalar dependencias

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
