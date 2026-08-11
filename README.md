# Calculadora de Pensión CSS

Aplicación web para estimar y comparar pensiones de jubilación de la Caja de Seguro Social de Panamá.

El proyecto contempla los distintos sistemas y subsistemas previsionales y permitirá realizar proyecciones considerando edad, cuotas, historial salarial, continuidad laboral y escenarios de crecimiento salarial. Los cálculos legales definitivos se incorporarán únicamente después de consolidar y versionar la normativa aplicable.

## Sistemas contemplados

- Subsistema Exclusivamente de Beneficio Definido (SEBD)
- Subsistema Mixto
- Sistema Único de Capitalización con Garantía Solidaria (SUCGS)

## Objetivos principales

La aplicación busca permitir al usuario:

- registrar sus datos previsionales;
- calcular su edad y fechas de referencia;
- registrar cuotas históricas y proyectar cuotas futuras;
- registrar historial anual de cuotas y salario cotizado/reportado;
- ingresar el salario actual como semanal, quincenal, mensual o anual;
- normalizar el salario actual a diferentes periodicidades;
- proyectar salarios futuros mediante distintos escenarios;
- combinar historial real, año actual parcial y proyección futura en una línea temporal;
- determinar si cumple requisitos para una prestación;
- calcular pensiones según el sistema correspondiente;
- estimar cuándo alcanzará determinados requisitos de cuotas;
- comparar edades de retiro y años adicionales de trabajo;
- visualizar la evolución estimada de la pensión;
- generar informes de resultados;
- mantener separados los datos históricos de los datos proyectados.

## Estado actual del desarrollo

La versión `0.1.0` se encuentra en desarrollo.

El asistente está organizado en seis pasos:

1. **Datos personales:** implementado.
2. **Cuotas:** implementado con análisis preliminar mediante API.
3. **Historial:** en implementación. Incluye captura anual de cuotas y salario cotizado/reportado, validación contra las cuotas reales del Paso 2 y salario actual normalizado para proyección.
4. **Proyección:** implementado en validación. Incluye salario constante, variación porcentual, salario futuro conocido, comparación de escenarios y línea temporal que separa historial real, año actual mixto y futuro proyectado.
5. **Retiro:** pendiente.
6. **Resultados:** pendiente.

Todavía no se han implementado los motores legales definitivos de SEBD, Mixto y SUCGS.

## API disponible

Actualmente FastAPI expone:

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
```

La documentación automática está disponible en `/docs` durante la ejecución local.

## Tecnologías

Implementadas actualmente:

- Python
- FastAPI
- Uvicorn
- Pydantic
- Jinja2
- HTML
- CSS
- JavaScript
- Bootstrap
- `sessionStorage` para el estado temporal del asistente

Previstas para fases posteriores:

- Chart.js
- SQLite
- Pytest
- generación de informes PDF

## Estructura general

```text
calculadora-pension-css/
├── app/
│   ├── core/
│   ├── modelos/
│   ├── motores/
│   ├── servicios/
│   ├── static/
│   ├── templates/
│   └── main.py
├── data/
├── docs/
├── normativa/
├── tests/
├── .editorconfig
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
└── requirements.txt
```

## Instalación

### 1. Clonar el repositorio

```powershell
git clone https://github.com/recm0708/calculadora-pension-css.git
cd calculadora-pension-css
```

### 2. Crear un entorno virtual

```powershell
python -m venv .venv
```

### 3. Activarlo en PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

## Ejecución

Con el entorno virtual activado:

```powershell
python -m uvicorn app.main:app --reload
```

Abrir en el navegador:

```text
http://127.0.0.1:8000
```

Documentación automática de la API:

```text
http://127.0.0.1:8000/docs
```

## Validación rápida

Para verificar que los módulos Python no contienen errores de sintaxis:

```powershell
python -m compileall app
```

Después se deben validar manualmente las rutas principales y el flujo del asistente en el navegador.

## Documentación técnica

Los documentos de `docs/` registran progresivamente:

- arquitectura;
- especificación funcional;
- modelo de datos;
- motores de cálculo;
- normativa;
- decisiones técnicas;
- hoja de ruta.

La documentación debe actualizarse cuando un cambio funcional o arquitectónico lo amerite; no es necesario modificar todos los archivos `.md` en cada commit.

## Privacidad

El repositorio no debe contener:

- nombres reales de asegurados utilizados para pruebas;
- números de cédula;
- números de Seguro Social;
- comprobantes privados;
- PDFs personales;
- bases de datos reales;
- información confidencial.

Los casos utilizados para validar los cálculos deberán estar anonimizados.

## Advertencia

Esta aplicación genera estimaciones con fines informativos, educativos y de planificación.

Los resultados no constituyen una certificación ni determinación oficial de una pensión.

La determinación oficial de prestaciones corresponde exclusivamente a la Caja de Seguro Social de Panamá.