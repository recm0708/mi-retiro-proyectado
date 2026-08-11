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

## Comentarios y documentación del código

Los archivos de código deben documentarse de forma consistente, evitando comentarios redundantes.

- Python: docstrings de módulo, clase y función cuando aporten contexto; 4 espacios de sangría.
- HTML: comentarios estructurales para secciones y pasos importantes; 2 espacios de sangría.
- CSS: comentarios por bloques funcionales; 2 espacios de sangría.
- JavaScript: encabezados por módulo y JSDoc en funciones relevantes; 2 espacios de sangría.
- JSON normativo: no utilizar comentarios, porque JSON estándar no los admite. La explicación de parámetros se mantendrá en `docs/NORMATIVA.md`.

Los archivos Markdown, `requirements.txt` y `.gitkeep` no requieren comentarios de código.

## Validación mínima antes de un commit

Ejecutar:

```powershell
python -m compileall app
python -m unittest discover -s tests -v
```

También se deben probar en el navegador las rutas y pasos afectados por el cambio.

Las pruebas automatizadas son obligatorias antes de consolidar cambios en motores de cálculo, precisión monetaria, cuotas o fechas de retiro.


## Precisión monetaria

- Los cálculos monetarios deben usar las utilidades de `app/core/dinero.py` cuando exista riesgo de redondeo.
- Se conservará precisión durante las operaciones y se redondeará al materializar importes monetarios.
- El criterio técnico general es `ROUND_HALF_UP` a dos decimales, salvo regla normativa específica.
- No se deben introducir redondeos intermedios únicamente para hacer coincidir una cifra visible con otra.
- Los campos monetarios editables deben admitir como máximo dos decimales.

## Finales de línea

`.editorconfig` y `.gitattributes` establecen LF para los archivos de texto principales. No se deben normalizar manualmente archivos completos salvo que sea necesario para evitar diffs masivos sin cambios funcionales.

## Datos personales

Está prohibido subir al repositorio información personal real utilizada durante las pruebas.

Los casos de validación deberán ser anonimizados.

## Cambios en fórmulas

Todo cambio relacionado con fórmulas, parámetros o reglas legales deberá:

1. estar documentado;
2. identificar la fuente normativa correspondiente;
3. incorporar o actualizar pruebas cuando corresponda;
4. mantener separados los parámetros legales de la lógica de presentación.

## Actualización de documentación

Los archivos de `docs/`, `README.md` y `CHANGELOG.md` se actualizarán cuando un cambio funcional, técnico o arquitectónico lo amerite. No es obligatorio modificar todos los documentos en cada avance.
