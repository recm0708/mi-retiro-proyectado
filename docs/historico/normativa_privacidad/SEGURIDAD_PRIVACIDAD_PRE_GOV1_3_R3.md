# Seguridad y privacidad

Este documento resume las defensas técnicas aplicables a la primera beta de **Mi Retiro Proyectado**. No sustituye una auditoría de seguridad externa ni convierte la aplicación en un servicio remoto multiusuario.

## 1. Modelo de ejecución

La primera beta está diseñada para ejecutarse localmente. Los datos del asistente permanecen en el navegador mediante `sessionStorage` y los cálculos se realizan contra la API local de FastAPI.

No existe persistencia de simulaciones en base de datos en esta versión.

## 2. Documentos personales importados

Los comprobantes de Mi Retiro Seguro y la Ficha Digital:

- se leen en memoria;
- no se guardan en el sistema de archivos por los endpoints de importación;
- no se incorporan al repositorio;
- no deben aparecer en fixtures de pruebas reales;
- se reducen a los campos operativos necesarios antes de devolver información al frontend.

Los contratos del importador minimizan identificadores directos. Desde UX.4.6b, Mi Retiro Seguro puede devolver nombres, apellidos, cédula y número de Seguro Social opcionales cuando aparecen con etiquetas inequívocas; el código único del documento continúa excluido.

## 3. Validación defensiva de PDF

Antes de invocar `pypdf`, la capa HTTP valida:

- extensión `.pdf`;
- tipo MIME compatible (`application/pdf`, genérico binario o ausente cuando el navegador no informa uno específico);
- archivo no vacío;
- límite de tamaño por importador;
- cabecera `%PDF-` dentro del primer KiB.

Los parsers mantienen además límites de páginas y de texto extraído. Los errores de parsing se convierten en mensajes controlados y no exponen trazas internas al Asegurado(a).

## 4. Cabeceras del navegador

Las respuestas incorporan defensas de bajo riesgo compatibles con la aplicación local:

- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options: DENY`;
- `Referrer-Policy: no-referrer`;
- `Permissions-Policy` sin cámara, micrófono ni geolocalización.

Desde UX.4.6b R2, todas las respuestas bajo `/api/simulacion/` usan `Cache-Control: no-store`. La aplicación incorpora Content Security Policy compatible con los recursos actuales y Bootstrap servido temporalmente por jsDelivr utiliza Subresource Integrity. Antes de beta pública se recomienda servir Bootstrap localmente para reducir dependencias de terceros.

## 5. CI y dependencias

`.github/workflows/ci.yml` ejecuta en cada `push` y `pull_request` sobre `main`:

- instalación limpia de dependencias;
- `pip check`;
- `compileall`;
- `node --check` para todos los JavaScript;
- suite completa de `unittest`.

La matriz cubre Python 3.13 y 3.14. Node.js se usa únicamente como herramienta de validación estática del frontend.

`.github/dependabot.yml` solicita revisiones semanales, pero evita actualizar transitivas fijadas de forma aislada. Para `pip` se permiten propuestas ordinarias únicamente sobre `fastapi`, `Jinja2`, `pydantic`, `python-multipart`, `pypdf` y `uvicorn`; las minor/patch compatibles del runtime se agrupan y `pypdf` queda separado para revisión específica. Las GitHub Actions se agrupan en una sola propuesta. La aceptación de cualquier actualización continúa requiriendo CI verde y revisión explícita; no existe auto-merge.

## 6. Datos sensibles y registros

No deben añadirse a logs, documentación pública, commits ni fixtures:

- nombre completo del Asegurado(a);
- cédula;
- número de seguro social;
- PDFs personales originales;
- capturas de Mi Caja Digital con identificadores;
- códigos únicos o QR personales.

Los casos reales de validación deben anonimizarse o transformarse en fixtures sintéticos antes de versionarse.

## 7. Límites de esta beta

Esta fase no afirma resistencia contra cargas hostiles a nivel de un servicio expuesto a Internet. Antes de desplegar la aplicación como servicio público remoto harían falta controles adicionales de infraestructura, límites de concurrencia, observabilidad, revisión/endurecimiento de CSP para el entorno de producción, revisión de dependencias y una evaluación de amenazas acorde al entorno de despliegue.


## 8. UX.4.6b — identificadores personales, consentimiento y Web Storage

La incorporación opcional de datos de identidad modifica la política anterior de exclusión total de identificadores, pero no habilita persistencia permanente. Se aplican estas condiciones:

- los PDF continúan procesándose en memoria y no se persiste el archivo original;
- nombre, apellidos, cédula y número de Seguro Social pueden devolverse cuando el parser reconoce el campo o una estructura de nombre revisable;
- un nombre completo puede descomponerse de forma conservadora, incluyendo el sufijo femenino `de Apellido` como apellido de casada; nunca se aplica sin vista previa;
- la vista previa se abre bloqueada y cualquier corrección requiere **Editar campos**;
- los datos confirmados permanecen en `sessionStorage` de la pestaña actual;
- `localStorage` no contiene la simulación: solo apariencia y versión/estado/fecha técnica de aceptación; la autorización activa de la pestaña se conserva en `sessionStorage`;
- la versión actual no usa cookies, analítica, publicidad ni rastreadores;
- no se escriben identificadores reales en logs, pruebas, fixtures, capturas versionadas ni documentación;
- el código único del documento no forma parte del contrato;
- los identificadores no se transmiten a los motores previsionales.

## 9. Controles R2 de navegador y API

Toda ruta `/api/simulacion/` utiliza `Cache-Control: no-store`. Se mantienen `X-Content-Type-Options`, denegación de framing, política de referrer y permisos, y se añade Content Security Policy. Mientras Bootstrap continúe servido por jsDelivr, la aplicación fija Subresource Integrity y `crossorigin`; antes de beta pública se recomienda empaquetar esas dependencias en `app/static/`.

El consentimiento informado se presenta antes de la captura/importación. Su versión se almacena localmente para poder solicitar una nueva aceptación cuando exista un cambio material de finalidad, categorías de datos, retención o terceros. Rechazar elimina la simulación de la pestaña y devuelve a Inicio.

## 10. Pendientes de seguridad y privacidad antes de beta pública

- servir Bootstrap localmente para retirar la dependencia de CDN;
- [x] disponer de controles accesibles para **Limpiar este paso**, **Reiniciar simulación** y borrar los datos locales de la aplicación;
- formalizar procedimiento de incidentes/vulneraciones y registro de respuesta;
- formalizar flujo de atención de derechos de acceso, rectificación, cancelación, oposición y portabilidad;
- verificar que la configuración de producción no registre cuerpos de solicitudes, PDFs ni identificadores;
- revisar jurídicamente política y consentimiento;
- reevaluar el modelo si se añaden cuentas, almacenamiento remoto, sincronización, analítica, telemetría, publicidad o terceros.


## Consentimiento visible UX.4.6b R4

El consentimiento previo se presenta como un documento extenso y versionado. La casilla de aceptación se habilita únicamente después de alcanzar el final del texto. La interfaz no agrega un bloque de **Fin de los términos** ni un mensaje de **Lectura completada**: al cumplirse el requisito desaparece la ayuda previa y la casilla queda disponible. La interfaz pública describe conservación temporal, cookies, terceros y derechos en lenguaje comprensible; la documentación técnica conserva los nombres de las tecnologías cuando son necesarios para auditoría.


## 9. UX.4.6c — integridad de datos importados por campo

La protección de información importada se aplica por campo y no por pantalla completa. Un valor confirmado desde Mi Retiro Seguro queda de solo lectura en los pasos posteriores para evitar modificaciones accidentales fuera del flujo de revisión documental. Si el PDF no aporta un dato, ese control permanece habilitado para que el titular lo complete manualmente.

La corrección de información documental vuelve a la vista previa del comprobante, de forma que exista una única vía explícita de edición. `origen_campos_cuotas` conserva únicamente metadata de procedencia en la sesión; no altera los datos enviados al motor ni agrega persistencia permanente.

## 10. UX.4.6d — integridad documental en historial y Ficha Digital

El Paso 3 extiende la regla de integridad por campo de UX.4.6c. Los datos confirmados desde Mi Retiro Seguro o Ficha Digital mantienen una marca temporal de procedencia y no se editan directamente en la pantalla principal. La ausencia de un dato en el documento no bloquea su captura manual.

La Ficha Digital conserva el mismo límite de privacidad ya vigente: solo utiliza registros del año calendario actual. Desde UX.4.6d R3, un mes efectivamente detectado con salario/estado utilizable se incorpora como registro documental confirmado y su casilla de cuota queda marcada y bloqueada. La vista previa abre bloqueada y cualquier corrección de los demás campos requiere activar **Editar campos** antes de volver a importar.

UX.4.6d no introduce cookies, telemetría, persistencia remota ni una nueva finalidad de tratamiento. La Revisión 6 sí amplía materialmente los controles disponibles para conservación y eliminación local, por lo que la versión del texto de privacidad se actualiza a **2026-08-15.1** y se solicita nuevamente aceptación. Los PDFs reales continúan fuera del repositorio y las pruebas usan datos sintéticos.

### Integridad interpaso en R2

R2/R3 establecieron inicialmente que la Ficha Digital no redefinía las cuotas del Paso 2. Desde R23, una ficha confirmada puede **ampliar** la referencia del año actual cuando aporta más cuotas documentales que la fotografía agregada previa, conservando las cuotas anteriores al año vigente y registrando la nueva procedencia. Una ficha con menos meses nunca reduce silenciosamente una referencia superior. Quitar la ficha no debe borrar arbitrariamente una referencia ya vigente.

### Integridad visual y semántica de selección — UX.4.6d R5

La corrección de casillas documentales no amplía la finalidad de tratamiento. Su objetivo es impedir que un dato confirmado aparezca visualmente desmarcado o se interprete como falso por una diferencia de estado de interfaz. Los meses manuales siguen siendo modificables únicamente cuando no proceden del documento.

### Gestión local de datos — UX.4.6d R6

El asistente incorpora tres niveles de borrado con alcances distintos. El borrado por paso invalida cualquier cálculo dependiente para impedir resultados obsoletos; el reinicio completo elimina toda la simulación sin borrar preferencias/aceptación; y el borrado desde Fuentes/Privacidad elimina además la constancia de aceptación y el tema visual. Ninguna acción borra indiscriminadamente todo el almacenamiento del dominio: solo las claves propiedad de Mi Retiro Proyectado.

### Consulta posterior sin mutación — UX.4.6d R7

La reapertura del documento legal desde Fuentes es una operación de lectura: no cambia la constancia de consentimiento, no elimina datos y no habilita tratamientos nuevos. El modal se comparte globalmente para evitar duplicación de contratos visibles. Cerrar la consulta solo oculta el modal; cerrar el consentimiento inicial sin aceptar conserva la frontera de privacidad y vuelve a Inicio.

### Consentimiento desde Fuentes y cierre contextual — UX.4.6d R9

Cuando no existe consentimiento vigente, Fuentes puede presentar el mismo documento en modo de consentimiento completo. La aceptación utiliza el mismo mecanismo y versión que Simular, por lo que no se duplica la manifestación. Cerrar con `×` o `Esc` sin aceptar no crea constancia de consentimiento. Si la solicitud se originó en Simular, el formulario permanece inaccesible; si se originó en Fuentes, el usuario puede continuar consultando esa sección sin que ello implique aceptación.

Los ejemplos visibles en campos de identidad se mantienen sintéticos y genéricos para evitar reutilizar datos reales en la interfaz o documentación de prueba.

## R15 — documento como concepto de UX, PDF como implementación actual

La interfaz y el consentimiento describen **documentos importados** sin exigir al titular conocer la noción de “compatibilidad” del layout. Técnicamente, esta versión continúa aceptando y validando PDF digital mediante extensión/MIME/firma/límites y `pypdf`. Este cambio de redacción no amplía finalidades, categorías de datos ni persistencia y no modifica la versión jurídica vigente.

## UX.4.6d R18 — recarga y nombre del documento

Por seguridad del navegador, `input[type=file]` se vacía después de recargar y la aplicación no intenta reconstruirlo. Para no confundir al usuario, la sesión puede conservar el **nombre del documento** como metadata de presentación junto con los datos que ya fueron confirmados. No se persisten bytes, ruta local, copia del PDF ni contenido adicional fuera de los datos extraídos/revisados. No se incorpora telemetría ni almacenamiento remoto y se mantiene la versión de privacidad **2026-08-15.1**.


## UX.4.6d R21 — verificación externa de fecha

La vigencia de Ficha Digital ya no se decide con el reloj local. El backend realiza una solicitud HTTPS mínima a infraestructura oficial de la CSS para leer el encabezado `Date`; no adjunta documentos ni datos de la simulación. La conexión puede revelar metadatos técnicos normales, incluida la IP, al sitio oficial consultado. Si la verificación falla, el sistema adopta un estado conservador y solicita revisión en lugar de confiar en la hora local. Este cambio se informa en la versión de privacidad **2026-08-16.1**.
