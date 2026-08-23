# Casos de validación

Este directorio contiene únicamente casos sintéticos o anonimizados aptos para control de versiones.

## 1. Reglas

- No guardar cédulas, nombres completos, números de asegurado, direcciones, teléfonos ni correos reales.
- No versionar PDF, capturas o exportaciones originales de Mi Caja Digital/Mi Retiro Seguro con datos personales.
- Los originales deben mantenerse fuera de Git en `tests/validation_cases/originals/`, ruta excluida por `.gitignore`.
- Un caso anonimizado debe conservar solo los datos necesarios para reproducir la propiedad matemática que se prueba.
- Un caso sintético debe indicar expresamente que sus parámetros actuariales o saldos son de prueba cuando no representan valores oficiales.

## 2. Nombres recomendados

```text
sebd_normal_regresion_741_59.json
mixto_pension_programada_sintetico.json
mixto_devolucion_cap_sintetico.json
sucgs_art197_240_cuotas_sintetico.json
```

## 3. Documentación

La descripción consolidada de regresiones se mantiene en [`docs/VALIDACION.md`](../../docs/VALIDACION.md).
