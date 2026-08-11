# Guía de contribución

## Flujo básico de trabajo

Antes de comenzar a trabajar:

```powershell
git pull
```

Después de realizar cambios:

```powershell
git status
git add .
git commit -m "tipo: descripción del cambio"
git push
```

## Convención de commits

Se utilizarán mensajes descriptivos siguiendo una convención sencilla.

Ejemplos:

```text
feat: agregar cálculo de cuotas proyectadas
fix: corregir cálculo de edad de referencia
docs: actualizar normativa del SEBD
test: agregar caso de validación femenino
refactor: reorganizar motor de pensiones
chore: actualizar dependencias
```

## Datos personales

Está prohibido subir al repositorio información personal real utilizada durante las pruebas.

Los casos de validación deberán ser anonimizados.

## Cambios en fórmulas

Todo cambio relacionado con fórmulas, parámetros o reglas legales deberá:

1. estar documentado;
2. identificar la fuente normativa correspondiente;
3. incorporar o actualizar pruebas cuando corresponda.