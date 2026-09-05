# Cierre UX.5 — sistema visual y flujo Manual/Asistido

**Estado:** candidato de cierre; aceptación revision-aware pendiente
**Candidato:** G120/E01 — `0.1.20.01-beta`
**Revisión funcional:** UX.5 R6
**Fecha:** 2026-09-04
**Clasificación:** Auditoría / UX / QA / Evidencia

## 1. Propósito

Este documento conserva la evidencia durable del cierre funcional y documental de UX.5 antes de su integración, aceptación revision-aware y publicación.

UX.5 se desarrolló mediante R1–R6 sin aceptar ni publicar estados intermedios independientes. El primer estado aceptable del bloque continúa siendo E01 y la revisión funcional de cierre es R6.

## 2. Alcance consolidado

El candidato integra:

- sistema visual y tokens reutilizables;
- shell de aplicación, navegación y temas;
- selección explícita Manual/Asistida antes del wizard;
- flujo Manual de seis pasos sin dependencia documental;
- preparación Asistida con Mi Retiro Seguro y Ficha Digital;
- requisito de confirmar al menos una fuente para habilitar el recorrido;
- procedencia, revisión y completado manual de información faltante;
- cambio de modalidad e invalidación descendente;
- gates de completitud y protección de Resultados;
- loaders y estados de procesamiento;
- revisión de URL para recursos estáticos locales;
- carga independiente de los scripts de modalidad y coordinación Asistida.

## 3. Flujo Manual

La modalidad Manual permite completar directamente los Pasos 1–6 sin solicitar documentos.

El usuario mantiene control sobre las decisiones previsionales y los datos necesarios para completar la simulación.

## 4. Flujo Asistido

La modalidad Asistida incorpora un Centro documental previo al wizard.

Las fuentes admitidas son:

- Mi Retiro Seguro;
- Ficha Digital.

Cada documento es opcional individualmente, pero el modo Asistido requiere confirmar al menos una fuente antes de habilitar el recorrido compartido.

Los documentos pueden aportar datos detectados, pero no toman decisiones previsionales en nombre del usuario.

La información faltante permanece completables manualmente dentro del wizard.

## 5. Mi Retiro Seguro

Durante la revisión final de UX.5 se detectó una representación aparentemente vacía del importador de Mi Retiro Seguro en un perfil normal de Chrome.

La comprobación con un perfil limpio demostró que el importador y sus controles estaban presentes y funcionales.

Posteriormente se corrigió la carga de los scripts de modalidad/asistencia y se agregó revisión de URL a los recursos estáticos para evitar combinar HTML actual con CSS o JavaScript almacenados anteriormente.

Después de la corrección se comprobó nuevamente el flujo en la ventana normal del navegador.

## 6. Evidencia funcional observada

Las regresiones focales posteriores a la corrección del flujo Asistido obtuvieron:

- 34 pruebas passed;
- 59 subtests passed;
- `git diff --check` limpio.

La revisión manual en Chrome confirmó:

- Mi Retiro Seguro visible en una ventana normal;
- selección de PDF de Mi Retiro Seguro;
- análisis del documento;
- detección de información;
- selección de PDF de Ficha Digital;
- análisis del documento;
- detección de información;
- presentación de estados de procesamiento.

La exactitud campo por campo, los textos finales de mensajes, la revisión visual exhaustiva y las mejoras de interacción quedan expresamente trasladadas a UX.6.

## 7. Frontera con UX.6

UX.6 concentrará:

- revisión visual pantalla por pantalla de App;
- revisión visual pantalla por pantalla del Portal Developer;
- temas Claro, Oscuro, Automático y Alto contraste;
- accesibilidad y navegación por teclado;
- foco y lector/axe;
- `prefers-reduced-motion`;
- nombres o tooltips al pasar o enfocar iconos del sidebar colapsado;
- microanimaciones;
- responsive;
- zoom y escalado;
- compatibilidad entre motores de navegador;
- revisión detallada de detecciones y mensajes de Mi Retiro Seguro y Ficha Digital;
- Portal Developer y gestión de usuarios;
- política y cambio de contraseñas Developer;
- auditoría integral de CSS, JavaScript, templates y Python;
- duplicados;
- cascadas;
- listeners repetidos;
- selectores huérfanos;
- código muerto;
- responsabilidades superpuestas.

UX.6 permanece planificado sin Global preasignado mientras G120 no haya sido aceptado.

## 7.1 Gate completo de cierre local

El Repository Quality Gate completo fue ejecutado sobre el candidato de cierre UX.5 R6 después de la reconciliación documental.

Resultado observado:

- `RESULTADO: PASS`;
- 11 checks PASS / 0 FAIL;
- 1404 pruebas `unittest` — OK;
- 1444 pruebas `pytest` passed;
- 6865 subtests passed;
- 166 archivos Markdown auditados;
- 60 documentos VIVO;
- 29 documentos AUDITORIA;
- 64 documentos HISTORICO;
- 9 documentos PLANTILLA;
- 4 documentos SOPORTE;
- 16 familias y 47 identificadores registrados;
- 586 archivos Git/versionables;
- 59 directorios canónicos;
- 0 enlaces locales rotos;
- 0 documentos vivos huérfanos;
- 0 grupos duplicados exactos;
- 0 grupos duplicados normalizados;
- 22 archivos JavaScript con sintaxis válida;
- `pip check` limpio;
- compilación Python limpia;
- contrato revision-aware G119/E05 válido;
- manifiesto de publicación G119/E05 válido;
- `git diff --check` limpio.

Este gate valida el estado de desarrollo de UX.5. No acepta todavía G120/E01 porque la aceptación formal requiere integración y promoción revision-aware.

## 8. Regla de aceptación

Este documento no acepta G120 por sí solo.

La aceptación de UX.5 requiere todavía:

1. reconciliación documental completa;
2. pruebas focales de cierre;
3. Repository Quality Gate completo;
4. commit firmado;
5. push de la rama;
6. Pull Request;
7. CI remoto;
8. integración;
9. promoción revision-aware de G120/E01;
10. revalidación post-merge;
11. tag firmado y publicación correspondiente.

Hasta completar esos pasos, `VERSION` permanece en `0.1.19.05-beta`.

## 9. Estado posterior

Una vez aceptado G120/E01:

- UX.5 quedará cerrado;
- la versión materializada será `0.1.20.01-beta`;
- la revisión funcional registrada será R6;
- el siguiente Global disponible será G121;
- UX.6 podrá convertirse en el nuevo candidato formal conforme a las reglas de versionado.

No se inicia PERSIST.1 mientras UX.6 permanezca abierto.
