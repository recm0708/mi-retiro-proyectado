# Calculadora de Pensión CSS

Aplicación web para estimar y comparar pensiones de jubilación de la Caja de Seguro Social de Panamá.

El proyecto contempla los distintos sistemas y subsistemas de pensiones aplicables conforme a la normativa vigente y permitirá realizar proyecciones considerando edad, cuotas, historial salarial, continuidad laboral y escenarios de crecimiento salarial.

## Sistemas contemplados

- Subsistema Exclusivamente de Beneficio Definido (SEBD)
- Subsistema Mixto
- Sistema Único de Capitalización con Garantía Solidaria (SUCGS)

## Objetivos principales

La aplicación busca permitir al usuario:

- registrar sus datos previsionales;
- calcular su edad de referencia;
- registrar cuotas históricas;
- proyectar cuotas futuras;
- ingresar salarios semanales, quincenales, mensuales o anuales;
- proyectar salarios futuros;
- determinar si cumple los requisitos para una prestación;
- calcular pensiones según el sistema correspondiente;
- estimar cuándo alcanzará determinados requisitos de cuotas;
- comparar distintas edades de retiro;
- simular años adicionales de trabajo;
- comparar escenarios salariales;
- visualizar la evolución estimada de la pensión;
- generar informes de resultados;
- mantener separados los datos históricos de los datos proyectados.

## Sistemas de cálculo

La arquitectura contempla motores independientes para:

### SEBD

Motor correspondiente al Subsistema Exclusivamente de Beneficio Definido.

### Subsistema Mixto

Motor encargado de calcular los componentes correspondientes al Subsistema Mixto.

### SUCGS

Motor correspondiente al Sistema Único de Capitalización con Garantía Solidaria.

## Tecnologías

- Python
- FastAPI
- Uvicorn
- Jinja2
- HTML
- CSS
- JavaScript
- Bootstrap
- Chart.js
- SQLite
- Pytest

Algunas tecnologías se incorporarán progresivamente durante el desarrollo.

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

## Estado del proyecto

**En desarrollo.**

Versión inicial:

```text
0.1.0
```

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