# Política de privacidad y tratamiento de datos

**Producto:** Mi Retiro Proyectado
**Versión del texto:** `2026-08-16.1`
**Estado:** Vigente en la aplicación
**Versión de aplicación revisada:** `0.0.22-beta`
**Revisión documental:** GOV.1.3 R3 — 2026-08-17
**Revisión jurídica externa:** Pendiente antes de publicación pública/comercial

Esta política describe el tratamiento implementado actualmente. No constituye certificación jurídica.

## 1. Responsable

**Rubén Enrique Cañizares Miranda**, Panamá.

Contacto: `ruben.canizares@outlook.com`

## 2. Marco de referencia

- Ley 81 de 26 de marzo de 2019 sobre Protección de Datos Personales;
- Decreto Ejecutivo 285 de 28 de mayo de 2021;
- orientaciones y preguntas frecuentes de ANTAI.

Fuentes: `FUENTES_NORMATIVAS.md`.

## 3. Principios aplicados

El diseño busca aplicar:

- finalidad;
- minimización;
- transparencia;
- seguridad;
- confidencialidad;
- control del titular.

## 4. Datos que puede tratar la simulación

### Identificación opcional

- nombres/apellidos;
- apellido de casada;
- cédula;
- número de Seguro Social.

Estos datos no son necesarios para ejecutar las fórmulas principales.

### Datos previsionales

- fecha de nacimiento;
- sexo;
- fecha de ingreso a CSS cuando se conozca;
- sistema previsional;
- cuotas;
- salarios/historial;
- detalle mensual/quincenal;
- escenarios;
- resultados.

## 5. Origen

Los datos provienen:

- de captura manual; o
- de documentos seleccionados voluntariamente.

Una importación se revisa antes de confirmar.

## 6. Finalidad

Los datos se utilizan para:

- construir la simulación;
- comprobar coherencia;
- proyectar;
- comparar escenarios;
- estimar prestaciones;
- explicar resultados.

No se autoriza su uso para publicidad, venta de información o perfilado comercial.

## 7. Consentimiento

La versión material vigente es **2026-08-16.1**.

Para utilizar Simular se requiere:

1. visualizar el documento;
2. llegar al final para habilitar la casilla;
3. marcar aceptación;
4. confirmar.

El registro local conserva versión/fecha de aceptación. La autorización activa exige además una marca de la misma versión en la sesión actual; por ello una sesión nueva puede requerir una nueva aceptación.

Consultar el documento desde Fuentes sin aceptar no crea consentimiento.

## 8. Rechazo

En el ingreso a Simular, rechazar elimina el estado temporal de simulación y la constancia de consentimiento aplicable a esa sesión, y vuelve a Inicio.

En una consulta desde Fuentes, cerrar/rechazar la ventana no registra aceptación y no impide seguir consultando información pública.

## 9. Conservación

La simulación utiliza almacenamiento temporal de sesión del navegador.

No existe actualmente:

- cuenta de usuario;
- base de datos permanente de simulaciones;
- sincronización remota;
- nube del proyecto para datos de simulación.

La aceptación/versionado y la apariencia utilizan almacenamiento local del navegador conforme al contrato implementado.

## 10. Documentos

Los archivos originales no se guardan en una base de datos.

Después de confirmar una importación puede conservarse metadata mínima como el nombre visible del archivo y los datos ya confirmados.

No se conserva la ruta local ni el binario del PDF.

## 11. Conexiones externas

### Bootstrap/CDN

La interfaz carga Bootstrap desde jsDelivr. Ese proveedor recibe metadatos ordinarios de una solicitud web, pero Mi Retiro Proyectado no envía el contenido de la simulación en esa petición.

### Fecha CSS

Para evaluar vigencia de Ficha Digital, el backend puede consultar por HTTPS infraestructura oficial de la CSS y leer el encabezado `Date`.

No se envían identidad, salarios, cuotas, resultados ni PDF.

## 12. Cookies, analítica y publicidad

La aplicación no implementa cookies propias de publicidad, analítica, seguimiento o perfilado.

No incorpora actualmente telemetría de producto.

## 13. Controles del usuario

El usuario dispone de:

- edición/revisión de datos;
- limpiar paso;
- reiniciar simulación;
- borrar datos de esta aplicación en este navegador.

Los controles locales no sustituyen un procedimiento formal de derechos si en el futuro existe tratamiento remoto/persistente.

## 14. Derechos

El marco panameño reconoce derechos de acceso, rectificación, cancelación, oposición y portabilidad.

Canal inicial del proyecto:

`ruben.canizares@outlook.com`

El procedimiento formal de atención se documentará en GOV.1.5 antes de una beta pública.

## 15. Seguridad

Controles actuales incluyen:

- procesamiento en memoria de PDF;
- validación defensiva;
- `no-store` en APIs de simulación;
- CSP y cabeceras;
- minimización;
- separación de identidad y motores;
- pruebas automatizadas.

No se garantiza riesgo cero.

## 16. Terceros

No se venden datos de simulación.

No existe integración comercial que reciba la simulación.

Recursos técnicos externos actuales se documentan en `SEGURIDAD_PRIVACIDAD.md`.

## 17. Cambios materiales

Un cambio material en:

- finalidad;
- categorías de datos;
- conservación;
- destinatarios;
- conexiones externas relevantes;
- seguimiento/analítica;

debe provocar revisión de esta política y evaluación de incremento de versión/renovación de consentimiento.

## 18. Revisión jurídica

Antes de una publicación pública, comercial o un despliegue remoto con tratamiento persistente se requiere revisión jurídica formal.

## 19. Historia

La evolución R6–R21 se conserva en:

`docs/historico/normativa_privacidad/POLITICA_PRIVACIDAD_PRE_GOV1_3_R3.md`

La reorganización R3 no cambia por sí sola la versión material `2026-08-16.1`.
