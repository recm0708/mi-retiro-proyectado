# Política de privacidad y tratamiento de datos

**Producto:** Mi Retiro Proyectado
**Versión del texto:** `2026-08-16.1`
**Estado:** Vigente en la aplicación
**Versión de aplicación revisada:** `0.1.22.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Base documental:** GOV.1.3 R3 — 2026-08-17
**Revisión transversal histórica:** GOV.1.5 R3 — 2026-08-18
**Última revisión documental previa:** PLAN.1 R3B1 — 2026-08-20
**Última revisión documental:** AUD.SEC2 R1 — 2026-08-25
**Revisión jurídica externa:** Pendiente antes de la primera versión oficial o de un despliegue remoto que cambie el tratamiento

<!-- DOC1-R1-REVISION-MANUAL:START -->
## Nota de lectura vigente

Esta política describe la aplicación principal de simulación y el tratamiento
de datos previsionales del Asegurado(a).

Estado funcional consolidado:

- la simulación puede utilizarse en modalidad Manual o Asistida;
- Mi Retiro Seguro y Ficha Digital son fuentes documentales opcionales;
- toda importación exige vista previa y confirmación explícita;
- el archivo PDF original no forma parte del estado persistente de la simulación;
- el estado previsional se mantiene temporalmente en la sesión del navegador;
- la aplicación principal no crea cuentas de Asegurado(a) ni un historial
  permanente de simulaciones;
- las decisiones personales permanecen bajo control del usuario;
- las superficies administrativas internas se documentan por separado y no
  forman parte de este consentimiento.

La versión material de privacidad continúa siendo `2026-08-16.1` porque estas
revisiones consolidan y aclaran el tratamiento ya implementado sin añadir una
nueva finalidad, categoría de datos, destinatario ni persistencia remota.
<!-- DOC1-R1-REVISION-MANUAL:END -->

Esta política describe el tratamiento implementado actualmente. No constituye certificación jurídica.

Su alcance se limita a la aplicación principal de simulación, sus funciones
públicas y los datos previsionales proporcionados por el Asegurado(a). Las
superficies administrativas internas se documentan por separado y no forman
parte de este consentimiento.

## 1. Responsable

**Rubén Enrique Cañizares Miranda**, Panamá.

Contacto: `ruben.canizares@outlook.com`

## 2. Marco de referencia

- Ley 81 de 26 de marzo de 2019 sobre Protección de Datos Personales;
- Decreto Ejecutivo 285 de 28 de mayo de 2021;
- orientaciones y preguntas frecuentes de ANTAI.

Fuentes: `regulatory-sources.md`.

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

## 5. Origen y modalidad

La simulación puede utilizarse de dos formas:

- **Manual:** el Asegurado(a) introduce y revisa directamente la información;
- **Asistida:** el Asegurado(a) puede seleccionar voluntariamente Mi Retiro
  Seguro, Ficha Digital o ambos para preparar datos compatibles.

La modalidad Asistida prepara información, pero **no toma decisiones personales
por el Asegurado(a)**. Cada importación presenta una vista previa y requiere
confirmación explícita antes de aplicar datos.

Si el usuario cambia a Manual después de confirmar información documental, la
aplicación solicita confirmación y retira los **datos que proceden de documentos**
junto con los resultados posteriores que dependan de ellos. Los **datos personales introducidos manualmente** que no procedan de documentos pueden conservarse.

## 6. Finalidad

Los datos se utilizan para:

- construir la simulación;
- comprobar coherencia;
- analizar cuotas y salarios;
- proyectar;
- comparar escenarios;
- registrar la procedencia de la información;
- estimar prestaciones;
- explicar resultados;
- generar exportaciones solo cuando el usuario las solicite.

No se autoriza su uso para publicidad, venta de información, perfilado
comercial ni para tomar automáticamente decisiones personales o jurídicas
sobre el Asegurado(a).

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

No existe para la simulación previsional:

- cuenta de Asegurado(a);
- base de datos permanente de simulaciones;
- sincronización remota;
- nube del proyecto para datos de simulación.

La aceptación versionada y la apariencia pueden conservar metadata local de
funcionamiento. La simulación previsional no se almacena como historial
permanente en ese almacenamiento local.

## 10. Documentos

Los PDF de Mi Retiro Seguro y Ficha Digital se procesan temporalmente para
extraer la información necesaria y generar una vista previa.

El **archivo original no se guarda** como parte de la simulación ni se incorpora
a una base de datos permanente. Los datos detectados solo se aplican después de
la confirmación explícita del usuario.

Después de una importación confirmada puede conservarse, durante la sesión,
metadata mínima de continuidad como el nombre visible del archivo y los datos
ya aceptados. No se conserva la ruta local ni el contenido binario del PDF.

## 11. Conexiones externas

### Bootstrap/CDN

La interfaz carga Bootstrap desde jsDelivr. Ese proveedor recibe metadatos ordinarios de una solicitud web, pero Mi Retiro Proyectado no envía el contenido de la simulación en esa petición.

### Fecha CSS

Para evaluar vigencia de Ficha Digital, el backend puede consultar por HTTPS infraestructura oficial de la CSS y leer el encabezado `Date`.

No se envían identidad, salarios, cuotas, resultados ni PDF.

## 12. Cookies, analítica y publicidad de la aplicación principal

La aplicación principal de simulación no implementa cookies propias de
publicidad, analítica, seguimiento o perfilado.

El estado previsional en curso se mantiene temporalmente en la sesión del
navegador. La apariencia y la constancia versionada de aceptación pueden
recordarse localmente para el funcionamiento de la aplicación.

No se incorpora actualmente telemetría de producto sobre la actividad del
Asegurado(a). Cualquier cambio futuro de finalidad, analítica o seguimiento
requiere revisar esta política antes de habilitarse.

## 13. Controles del usuario

El Asegurado(a) dispone de:

- revisión y edición de datos;
- elección entre modalidad Manual y Asistida;
- confirmación explícita antes de aplicar una importación;
- cambio de modalidad con advertencia cuando existan datos documentales;
- limpiar paso;
- reiniciar simulación;
- borrar datos de esta aplicación en este navegador.

Al cambiar de Asistida a Manual después de una importación, se retiran los
**datos que proceden de documentos** y se reinician los cálculos dependientes,
mientras que los **datos personales introducidos manualmente** que no procedan
de documentos pueden conservarse.

El borrado integral elimina también la constancia local de aceptación y vuelve a presentar las condiciones desde Inicio. Los controles locales no sustituyen
un procedimiento formal de derechos si en el futuro existe tratamiento remoto
o persistente.

## 14. Derechos

El marco panameño reconoce derechos de acceso, rectificación, cancelación, oposición y portabilidad.

Canal inicial del proyecto:

`ruben.canizares@outlook.com`

El procedimiento interno se documenta en `data-subject-rights-procedure.md`. La revisión jurídica externa continúa pendiente antes de la primera versión oficial o de un cambio material del tratamiento.

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

Recursos técnicos externos actuales se documentan en `security-and-privacy.md`.

## 16.1. Seguridad e incidentes

Los datos previsionales y los documentos personales no deben incluirse en
registros de diagnóstico, ejemplos públicos ni evidencias versionadas.

El procedimiento interno de respuesta a incidentes se documenta en
`security-incident-procedure.md`.

La revisión de UX.6 no introduce una nueva finalidad, categoría de datos,
destinatario ni persistencia remota para la aplicación principal; por ello se
mantiene la versión material `2026-08-16.1`. Esta conclusión técnica no
sustituye la revisión jurídica externa.

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

Antes de la primera versión oficial, o antes de un despliegue remoto con tratamiento persistente o un cambio material de finalidad/destinatarios, se requiere la revisión jurídica definida por REV.1.

## 19. Historia

La evolución R6–R21 se conserva en:

`docs/archive/regulatory-privacy/privacy-policy-pre-gov1-3-r3.md`

La reorganización R3 no cambia por sí sola la versión material `2026-08-16.1`.
