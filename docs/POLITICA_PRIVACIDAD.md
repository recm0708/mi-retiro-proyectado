# Política de privacidad y tratamiento de datos

**Producto:** Mi Retiro Proyectado
**Versión:** 2026-08-13.2
**Estado:** UX.4.6b Revisión 4 — implementado técnicamente; pendiente validación manual en PC/laptop.

## 1. Principio general

Mi Retiro Proyectado aplica privacidad por diseño y minimización: solicita solo la información necesaria para las funciones utilizadas, mantiene opcionales los identificadores que no afectan el cálculo y evita persistir documentos PDF o simulaciones en una base de datos permanente en la versión actual.

## 2. Responsable

Rubén Enrique Cañizares Miranda, Panamá.
Correo: `ruben.canizares@outlook.com`
Proyecto: `https://github.com/recm0708/calculadora-pension-css`

## 3. Marco de referencia

- Ley 81 de 26 de marzo de 2019 sobre Protección de Datos Personales.
- Decreto Ejecutivo 285 de 28 de mayo de 2021.
- Orientaciones de ANTAI.

La aplicación busca aplicar licitud, finalidad, proporcionalidad, seguridad, transparencia, confidencialidad y control del titular.

## 4. Inventario de datos

### 4.1. Identificación opcional

- primer nombre;
- segundo nombre;
- primer apellido;
- segundo apellido;
- apellido de casada;
- cédula;
- número de Seguro Social.

Estos datos no modifican las fórmulas y deben poder omitirse.

### 4.2. Datos previsionales necesarios o funcionales

- fecha de nacimiento;
- sexo;
- fecha de ingreso a la CSS cuando se conozca;
- sistema previsional;
- cuotas;
- salarios e historial;
- datos mensuales/quincenales cuando se utilicen;
- escenarios salariales y de retiro;
- resultados estimados.

### 4.3. Metadatos técnicos mínimos

El navegador puede conservar información necesaria para mantener la sesión de uso, preferencias visuales y versión/fecha de aceptación de términos. No se utilizan cookies de publicidad, analítica o seguimiento en la versión actual.

## 5. Fuentes de los datos

Los datos provienen del propio usuario mediante captura manual o de documentos que el usuario selecciona voluntariamente. Los PDF pasan por una vista previa; la importación requiere confirmación explícita.

## 6. Finalidad

La información se utiliza únicamente para la simulación previsional solicitada, validación de coherencia, análisis, proyección, comparación, explicación y futura exportación voluntaria.

No se permite publicidad, venta, perfilado comercial ni decisiones con efectos jurídicos.

## 7. Consentimiento informado

La ruta **Simular** muestra un documento completo antes de permitir captura/importación. La casilla de aceptación permanece deshabilitada hasta llegar al final del texto. Rechazar devuelve a Inicio y elimina el estado temporal de la simulación de esa pestaña.

El consentimiento se versiona para volver a solicitarlo cuando cambie materialmente el tratamiento.

## 8. Conservación

La simulación se mantiene temporalmente durante la sesión de uso. No existe actualmente una base de datos permanente de simulaciones ni cuentas de usuario.

Pendiente pre-beta: acción explícita **Borrar mi simulación** visible desde el asistente y definición formal de plazos si en el futuro existe persistencia remota.

## 9. PDF

Los archivos originales no se persisten en una base de datos. Se validan extensión, MIME, tamaño, firma PDF, páginas y volumen de texto antes del análisis. La extracción debe conservar solo los datos necesarios para la función solicitada.

## 10. Destinatarios y transferencias

No se comparten datos de la simulación con terceros para fines comerciales. Los recursos técnicos externos de interfaz pueden recibir metadatos de conexión ordinarios, pero no el contenido de la simulación. Cualquier futura integración externa que reciba datos personales requiere evaluación previa y actualización de esta política.

## 11. Seguridad y confidencialidad

Controles actuales:

- procesamiento temporal de PDF;
- `Cache-Control: no-store` en endpoints sensibles;
- CSP y cabeceras defensivas;
- validación de archivos;
- separación de identificadores respecto de motores previsionales;
- prohibición de datos personales reales en pruebas y documentación pública;
- CI sobre Python 3.13/3.14 y sintaxis JavaScript.

Pendientes pre-beta:

- servir dependencias críticas localmente cuando sea viable;
- procedimiento de gestión de incidentes;
- revisión de logs y despliegue;
- TLS obligatorio si se publica remotamente;
- revisión jurídica de textos y controles.

## 12. Derechos

Debe poder atenderse, cuando corresponda, acceso, rectificación, cancelación, oposición y portabilidad. El canal inicial es `ruben.canizares@outlook.com`.

Antes de beta pública se documentará un procedimiento de atención de solicitudes que minimice datos adicionales y registre únicamente la evidencia necesaria.

## 13. Cookies y tecnologías del navegador

La versión actual no utiliza cookies para publicidad, analítica, seguimiento o perfilado. No se requiere un banner de cookies mientras esta condición siga siendo cierta.

El navegador sí conserva temporalmente información para mantener la simulación y preferencias de funcionamiento. En la interfaz se explica en lenguaje comprensible, sin exponer términos técnicos innecesarios.

## 14. Exportaciones

La futura exportación de resultados deberá ser voluntaria, permitir excluir identificadores, distinguir datos acreditados/proyectados, incluir advertencia de carácter orientativo y no oficial y documentar fecha/versión de metodología.

## 15. Cambios de arquitectura

Antes de habilitar cuentas, base de datos permanente, nube, telemetría, analítica, publicidad o transferencias a terceros se requiere una nueva evaluación de privacidad, actualización documental y nuevo consentimiento cuando corresponda.


## Criterio de presentación del consentimiento

La casilla de aceptación permanece deshabilitada hasta que el usuario llega al final del documento visible. Una vez cumplido ese requisito, la casilla se habilita sin añadir bloques de **Fin de los términos** ni mensajes de **Lectura completada**. La interfaz muestra solo la ayuda necesaria mientras el requisito todavía no se ha cumplido.
