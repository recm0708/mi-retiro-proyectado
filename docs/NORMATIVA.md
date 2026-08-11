# Normativa

## Estado

La capa normativa definitiva todavía no ha sido implementada.

Los parámetros legales y actuariales deberán mantenerse versionados dentro de `normativa/` y no dispersos dentro de HTML, JavaScript o múltiples módulos Python.

## Regla de implementación

Antes de implementar una fórmula legal definitiva se deberá:

1. identificar la fuente normativa aplicable;
2. registrar su vigencia;
3. documentar el parámetro o regla;
4. crear casos de validación;
5. implementar la lógica en el motor correspondiente.

## Parámetros actualmente presentes en el prototipo

El análisis preliminar de cuotas utiliza referencias de 180 y 240 cuotas para mostrar distancia respecto de hitos de cotización.

En esta fase esos valores deben considerarse **referencias preliminares del asistente**, no una determinación completa de elegibilidad ni una fórmula de pensión.

## Estructura prevista

Se prevé incorporar archivos versionados como:

```text
normativa/
├── parametros_generales.json
├── sebd.json
├── mixto.json
├── sucgs.json
├── factores_actuariales.json
└── transiciones.json
```

JSON estándar no admite comentarios; la explicación y trazabilidad normativa se mantendrán en este documento y en la documentación específica de cada motor.