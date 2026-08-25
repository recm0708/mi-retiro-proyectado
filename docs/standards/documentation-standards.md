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

## Metadata documental

Cuando un documento incluya metadata de cabecera, sus etiquetas se escriben en
negrita antes de los dos puntos, por ejemplo: `**Estado:** vigente`.

La metadata debe distinguir el significado de cada versión documentada:

- `**Versión de aplicación revisada:**` identifica la versión vigente contra la
  cual se revisó un documento actual;
- `**Versión base histórica preservada:**` identifica una versión anterior que
  se conserva únicamente como contexto o procedencia histórica.

No se repite una misma clave de metadata con valores distintos. Cuando sea
necesario conservar dos valores relacionados, se utilizan etiquetas
semánticamente diferentes que expliquen su función.

Los documentos vigentes que sean revisados formalmente actualizan su versión de
aplicación cuando esa metadata resulte aplicable. Los documentos históricos,
auditorías y evidencias conservan los valores correspondientes al momento que
documentan y no se modernizan únicamente para coincidir con la versión actual.

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

Los documentos históricos, auditorías y evidencias preservan la verdad del
momento que registran. Una ruta, versión, nombre de archivo o estado anterior no
se reemplaza mecánicamente por su equivalente actual cuando hacerlo alteraría
esa evidencia histórica.

Por esta razón, un enlace local roto dentro de documentación histórica o de
auditoría puede conservarse cuando representa una ruta válida en el estado
documentado. Esa excepción no se extiende a documentación vigente, estándares,
plantillas ni documentación técnica de soporte, cuyos enlaces locales deben
resolver contra el árbol actual.

## Compatibilidad

No se conserva un archivo antiguo únicamente como redirect documental para
evitar actualizar referencias internas.

Una ruta de compatibilidad solo se mantiene cuando existe un consumidor externo,
un enlace publicado o un contrato verificable que justifique su permanencia.

Las referencias negativas utilizadas por pruebas para comprobar que una ruta
retirada continúa ausente son válidas como regresión y no justifican recrear un
archivo de compatibilidad. Tampoco se mantiene un stub únicamente porque una
auditoría histórica registre que esa ruta existió durante una migración.

## Auditoría automática

La documentación Markdown versionada se valida mediante
`scripts/audit_markdown.py`. El auditor forma parte del gate local de
pre-commit y también dispone de un workflow específico de GitHub Actions.

El control automático verifica, según la clasificación documental aplicable:

- estructura Markdown básica y encabezado principal;
- bloques de código Markdown correctamente cerrados;
- metadata de cabecera y ausencia de claves duplicadas;
- coherencia entre documentación vigente y la versión definida en `VERSION`;
- enlaces locales de documentación vigente, estándares, plantillas y soporte;
- ausencia de stubs conservados únicamente por compatibilidad documental;
- comprobaciones conservadoras de idioma y de estados vigentes obsoletos.

Las excepciones históricas son deliberadas: auditorías, evidencias y documentos
archivados pueden conservar versiones, rutas y enlaces correspondientes al
estado que documentan cuando actualizarlos alteraría la trazabilidad histórica.

Una modificación documental no se considera validada únicamente porque el
archivo renderice correctamente. Debe superar también el auditor, sus pruebas de
regresión y los controles remotos aplicables.
