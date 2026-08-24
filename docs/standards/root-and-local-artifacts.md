# Raíz y artefactos locales

## Propósito

Define qué puede permanecer en la raíz del repositorio y cómo se administran
entregables, evidencia temporal y otros artefactos locales.

## Regla de raíz

La raíz contiene únicamente archivos o carpetas con responsabilidad transversal
sobre el proyecto.

Se permiten:

- directorios canónicos de código, datos, documentación, pruebas y tooling;
- archivos convencionales de Git y del ecosistema;
- documentos transversales de comunidad, gobierno, seguridad, versionado,
  releases y licencia;
- archivos de configuración cuya herramienta requiera o espere la raíz.

## Archivos prohibidos en raíz

No se crean ni conservan como parte canónica de la raíz:

- inventarios de auditoría;
- volcados de comandos;
- evidencias `.txt` de una revisión;
- parches de trabajo;
- paquetes `.zip`;
- logs;
- copias manuales;
- archivos con sufijos `final`, `nuevo`, `copia` o versiones informales;
- temporales de una fase.

La evidencia versionable se ubica bajo `docs/audits/`.

## Artefactos locales no versionados

Los entregables y evidencias que solo tengan utilidad local no forman parte del
árbol canónico Git.

Para nuevos artefactos locales dentro del workspace se prefiere:

```text
_deliverables/
```

El directorio local heredado:

```text
_entregas/
```

se considera una excepción de transición. No se crean allí nuevos archivos
versionados. NOR.2 auditará su contenido y decidirá qué conservar, migrar o
retirar sin destruir evidencia útil.

Ambos directorios deben permanecer ignorados por Git mientras existan.

## Evidencia temporal externa

Cuando un volcado pueda interferir con pruebas o invariantes, se conserva fuera
del repositorio, por ejemplo en una carpeta hermana del workspace.

El documento de auditoría debe registrar como mínimo:

- comando o método de generación;
- fecha o fase cuando sea relevante;
- conteo o resultado agregado;
- hallazgos utilizados para tomar decisiones.

## Paquetes

Los paquetes comprimidos generados para transferencia no se versionan.

El repositorio conserva las fuentes; el paquete es un medio de entrega local.

## NOR.2

NOR.2 utilizará estas reglas para revisar la raíz completa, los directorios
locales heredados y cualquier evidencia colocada fuera de su ubicación
canónica.
