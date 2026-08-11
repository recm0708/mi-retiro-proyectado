# Roadmap

## Fase 1 — Base técnica

**Estado:** completada

- estructura del repositorio;
- entorno virtual y dependencias;
- FastAPI;
- Jinja2;
- Bootstrap y CSS propio;
- Git y GitHub;
- documentación inicial.

## Fase 2 — Asistente básico

**Estado:** en ampliación

- Paso 1 — Datos personales;
- Paso 2 — Cuotas;
- Paso 3 — historial salarial anual y salario actual;
- validación del historial contra las cuotas reales;
- persistencia temporal con `sessionStorage`;
- invalidación de resultados dependientes.

## Fase 3 — Historial y proyección salarial

**Estado:** en validación

- modelos Pydantic;
- endpoint y servicio de historial salarial;
- componente editable de historial anual;
- endpoint de proyección;
- salario constante;
- porcentaje anual;
- salario futuro conocido;
- comparación 0/1/2/3 % y escenarios personalizados;
- interfaz del Paso 4;
- tablas de resultados por escenario;
- servicio y endpoint de línea temporal;
- vista integrada de historial real, año actual mixto y futuro proyectado.

## Fase 4 — Fechas, cuotas y retiro

**Estado:** pendiente

- proyección mensual de cuotas;
- cálculo de edad y fechas exactas;
- Paso 5 — Retiro;
- escenarios de años adicionales de trabajo;
- motor de elegibilidad.

## Fase 5 — Motores previsionales

**Estado:** pendiente

- normativa versionada;
- SEBD;
- Subsistema Mixto;
- SUCGS;
- casos de validación anonimizados;
- pruebas automatizadas.

## Fase 6 — Resultados y comparación

**Estado:** pendiente

- Paso 6 — Resultados;
- comparador de escenarios;
- gráficos;
- desglose de supuestos;
- advertencias y trazabilidad.

## Fase 7 — Persistencia e informes

**Estado:** pendiente

- SQLite;
- guardado voluntario de simulaciones;
- importación de datos cuando sea viable;
- informes PDF;
- mejoras de accesibilidad y despliegue.