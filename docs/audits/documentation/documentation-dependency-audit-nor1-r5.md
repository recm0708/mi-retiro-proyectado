# Auditoría de dependencias documentales NOR.1 R5

## Información general

**Proyecto:** Mi Retiro Proyectado

**Fase:** NOR.1 R5 — Auditoría de estructura documental y dependencias de rutas

## Objetivo

Evaluar la organización actual de la documentación y el impacto que tendría
cualquier movimiento o renombrado de archivos antes de ejecutar la
normalización estructural definitiva.

Esta fase es exclusivamente de auditoría y preparación. No autoriza movimientos
masivos, renombrados ni eliminación de documentación vigente.

## Evidencia utilizada

La auditoría utiliza como evidencia versionada:

- `nor1-r5-documentation-inventory.txt`;
- `documentation-classification-nor1-r3.md`;
- `naming-audit-nor1-r4.md`;
- los estándares vigentes ubicados en `docs/standards/`.

También se generó localmente una búsqueda completa de referencias a `docs/`
mediante `git grep -n "docs/"`. El resultado produjo 2407 coincidencias.

El volcado bruto de esa búsqueda no se conserva como archivo versionado porque
incluye referencias históricas a rutas técnicas que las pruebas de regresión
prohíben reintroducir en el árbol vigente. La búsqueda es reproducible y su
resultado agregado queda registrado en esta auditoría.

## Línea base

La revisión identificó 139 archivos dentro de `docs/`.

La estructura documental actual ya separa:

```text
docs/
├── archive/
├── audits/
├── standards/
└── templates/
```

Sin embargo, la raíz de `docs/` todavía concentra documentación de distintas
responsabilidades, entre ellas:

- arquitectura;
- desarrollo;
- normativa;
- privacidad;
- seguridad;
- gobierno;
- auditorías históricas;
- decisiones;
- validación;
- UX;
- versionado y releases.

## Dependencias de rutas

La búsqueda global de referencias a `docs/` produjo 2407 coincidencias.

Esto confirma que cualquier reorganización de rutas tiene un impacto
transversal y deberá tratarse como una migración controlada.

Las referencias aparecen, entre otros lugares, en:

- `README.md`;
- `CHANGELOG.md`;
- `CONTRIBUTING.md`;
- `GOVERNANCE.md`;
- `SECURITY.md`;
- `SUPPORT.md`;
- `VERSIONING.md`;
- documentación interna bajo `docs/`;
- pruebas automatizadas;
- archivos de gobierno y release.

## Riesgo de migración

El riesgo principal no es el movimiento físico de los archivos, sino dejar
referencias obsoletas después del cambio.

Una migración documental puede afectar:

- enlaces Markdown;
- rutas escritas como texto;
- índices documentales;
- matrices de trazabilidad;
- pruebas que validan nombres o ubicaciones;
- documentos que citan rutas canónicas;
- flujos de gobierno y release.

## Regla obligatoria para movimientos futuros

Todo movimiento o renombrado deberá completar este ciclo:

1. identificar la ruta actual;
2. definir la ruta nueva;
3. localizar todas las referencias a la ruta anterior;
4. mover o renombrar utilizando Git;
5. actualizar enlaces, índices, matrices y referencias cruzadas;
6. buscar nuevamente la ruta anterior;
7. ejecutar pruebas focales;
8. ejecutar la suite completa;
9. ejecutar validaciones de formato;
10. documentar el cambio antes del cierre de la fase.

## Evidencia bruta frente a invariantes del repositorio

Los inventarios y volcados generados durante una auditoría no tienen prioridad
sobre los invariantes vigentes del repositorio.

Si una evidencia bruta contiene cadenas, rutas o patrones prohibidos por una
prueba de regresión, se aplicará uno de estos criterios:

1. mantener la evidencia únicamente como artefacto local reproducible;
2. registrar en la auditoría el comando, el conteo y los hallazgos relevantes;
3. versionar solamente una representación compatible con los invariantes si
   conserva suficiente valor probatorio.

No se modificará ni excluirá una prueba de regresión únicamente para permitir
que un volcado bruto de auditoría sea versionado.

## Criterio para documentación vigente

No se moverá documentación viva únicamente para reducir la cantidad de archivos
en la raíz de `docs/`.

Cada cambio deberá justificar una responsabilidad documental clara y demostrar
que la nueva ubicación mejora:

- mantenibilidad;
- descubrimiento;
- trazabilidad;
- coherencia estructural;
- seguridad de referencias.

## Criterio para auditorías

Las auditorías deberán converger progresivamente hacia `docs/audits/`, separadas
por responsabilidad cuando corresponda.

La migración de auditorías antiguas se realizará únicamente después de revisar
sus referencias y su relación con pruebas de regresión.

## Criterio para históricos

Los documentos que representen estados sustituidos deberán permanecer bajo
`docs/archive/` cuando exista valor histórico o de auditoría.

El historial Git complementa esta conservación, pero no sustituye la necesidad
de mantener evidencia histórica que siga siendo parte del contrato documental
del proyecto.

## Estado de NOR.1 R5

**Inventario documental:** completado.

**Inventario reproducible de dependencias:** completado localmente.

**Resultado de dependencias:** 2407 coincidencias registradas.

**Clasificación preliminar:** completada.

**Movimientos o renombrados documentales masivos:** no ejecutados.

**Corrección estructural de evidencia R4:** completada mediante traslado del
inventario R4 desde la raíz hacia `docs/audits/repository/`.

**Sincronización de referencias:** pendiente de la fase que ejecute cada cambio.

## Salida hacia NOR.1 siguiente y NOR.2

NOR.1 continuará definiendo la estructura objetivo y los criterios de
normalización.

NOR.2 utilizará estas evidencias para:

- auditar el repositorio completo;
- identificar desviaciones concretas;
- ejecutar movimientos y renombrados controlados;
- consolidar documentos cuando corresponda;
- retirar del árbol actual archivos sustituidos;
- sincronizar todas las referencias y pruebas afectadas.

Ninguna migración se considerará terminada mientras existan referencias a rutas
anteriores o documentación desactualizada.
