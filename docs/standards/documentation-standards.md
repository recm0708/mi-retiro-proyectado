# Estándares de documentación

## Propósito

Define cómo se crean, mantienen, clasifican, sustituyen y enlazan documentos del
proyecto.

## Idioma

La documentación se redacta en español.

Los términos técnicos se mantienen cuando son nombres oficiales o conceptos
estandarizados. La regla de idioma del contenido no altera las convenciones
técnicas de nombres de archivo.

## Documento canónico

Debe existir una única versión oficial para cada política, norma o contrato
vigente.

No se mantienen variantes informales como:

```text
documento-final.md
documento-final-v2.md
documento-nuevo.md
```

## Clasificación

Todo documento debe poder clasificarse como uno de estos tipos:

- documentación vigente;
- estándar o política;
- auditoría o evidencia;
- plantilla;
- histórico con valor de trazabilidad.

Una bitácora de fase no se presenta como contrato vigente cuando solo describe
un estado pasado.

## Sustitución de documentos

Cuando un documento sea reemplazado:

1. se conserva el contenido todavía válido;
2. se define un único documento canónico;
3. se actualizan referencias;
4. se validan enlaces y pruebas;
5. se elimina del árbol vigente la copia sustituida;
6. se conserva bajo `docs/archive/` solo si mantiene valor histórico explícito.

Git conserva el historial aunque el archivo anterior salga del árbol actual.

## Enlaces y rutas

Todo movimiento o renombrado documental debe revisar:

- enlaces Markdown;
- rutas en `README.md` y documentos raíz;
- índices;
- matrices de trazabilidad;
- pruebas que validen nombres o ubicaciones;
- referencias textuales utilizadas como rutas;
- documentación de release, seguridad y gobierno.

La migración no se considera cerrada mientras una referencia vigente continúe
apuntando a la ruta anterior.

## Compatibilidad

No se conserva un archivo antiguo únicamente como redirect documental para
evitar actualizar referencias internas.

Una ruta de compatibilidad solo se mantiene cuando existe un consumidor externo,
un enlace publicado o un contrato verificable que justifique su permanencia.
