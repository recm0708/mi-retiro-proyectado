# Términos de uso, privacidad y tratamiento de datos

**Producto:** Mi Retiro Proyectado
**Versión del texto:** 2026-08-13.2
**Estado:** Vigente desde el cierre de UX.4.6b; validado en PC/laptop. Revisión jurídica formal pendiente antes de una publicación pública o comercial.

> Este documento describe el contrato funcional y de privacidad implementado por la aplicación. No constituye una certificación jurídica. Antes de una publicación pública, comercial o con almacenamiento remoto se requiere revisión jurídica formal.

## 1. Objeto

Mi Retiro Proyectado es una herramienta independiente para estimar, explicar y comparar escenarios previsionales. Estos términos regulan el uso de la aplicación y explican qué información puede tratarse, para qué se usa, cuánto tiempo se conserva, cómo puede corregirse o eliminarse y qué derechos asisten al titular.

## 2. Responsable y contacto

Responsable de la aplicación: **Rubén Enrique Cañizares Miranda**, Panamá.

- Correo de privacidad y contacto: `ruben.canizares@outlook.com`
- Proyecto: `https://github.com/recm0708/calculadora-pension-css`

No se publica una dirección residencial. Si el proyecto se transforma en un servicio comercial o adopta una persona jurídica responsable, este apartado deberá actualizarse antes de operar ese servicio.

## 3. Marco legal de referencia

La arquitectura de privacidad toma como referencia:

- Ley 81 de 26 de marzo de 2019 sobre Protección de Datos Personales;
- Decreto Ejecutivo 285 de 28 de mayo de 2021, que reglamenta la Ley 81;
- orientaciones públicas de la Autoridad Nacional de Transparencia y Acceso a la Información (ANTAI).

El diseño busca respetar licitud, finalidad, proporcionalidad, seguridad, transparencia, confidencialidad y control del titular.

## 4. Obtención de información

Los datos pueden ser:

1. introducidos manualmente por el usuario; o
2. detectados desde un PDF compatible seleccionado voluntariamente por el usuario.

Todo dato importado se presenta primero en una vista previa. Ningún dato detectado por un documento se incorpora a la simulación hasta que el usuario confirme expresamente la importación.

## 5. Categorías de datos

La simulación puede tratar:

- primer y segundo nombre;
- primer y segundo apellido;
- apellido de casada, cuando corresponda;
- cédula;
- número de Seguro Social;
- fecha de nacimiento;
- sexo;
- fecha de ingreso a la CSS;
- sistema previsional;
- cuotas acreditadas y proyectadas;
- salarios e historial salarial;
- datos mensuales o quincenales cuando el usuario los proporcione;
- escenarios de crecimiento salarial y retiro;
- resultados estimados de la simulación.

Los identificadores personales no son necesarios para ejecutar las fórmulas y deben permanecer opcionales salvo que una función futura requiera justificadamente alguno de ellos.

## 6. Finalidades

Los datos se tratan únicamente para:

- construir la simulación solicitada;
- verificar coherencia interna;
- estimar edad y fechas previsionales;
- analizar cuotas e historial salarial;
- proyectar escenarios futuros;
- comparar alternativas de retiro;
- presentar resultados explicativos;
- generar, cuando exista esa función, una exportación solicitada por el usuario.

No se autorizan usos para publicidad, mercadeo, venta de información, perfilado comercial ni decisiones con efectos jurídicos.

## 7. Consentimiento

El flujo **Simular** exige aceptación previa de los términos antes de permitir captura o importación de datos. El usuario debe recorrer el documento hasta el final para habilitar la casilla de aceptación. La aceptación queda asociada a una versión del texto y se solicita nuevamente cuando la versión cambia o cuando se inicia una nueva sesión de uso que requiera confirmación.

Si el usuario selecciona **No acepto**, se elimina el estado temporal de la simulación disponible en esa pestaña y se regresa a Inicio.

## 8. Calidad y revisión de los datos

El usuario es responsable de revisar que la información sea correcta y corresponda a su situación. La extracción automática puede equivocarse al interpretar texto, nombres, valores o clasificaciones. Por ello la vista previa inicia bloqueada, permite una edición deliberada y exige confirmación antes de importar.

## 9. Documentos PDF

Los PDF se procesan para extraer únicamente la información necesaria para la simulación. El archivo original no se incorpora a una base de datos permanente de la aplicación. Se mantienen límites defensivos de extensión, MIME, tamaño, firma PDF, páginas y texto extraíble.

## 10. Conservación y eliminación

La simulación se conserva temporalmente en el navegador para permitir avanzar, retroceder y recuperar el estado mientras la sesión de uso siga activa. La versión actual no dispone de cuentas de usuario ni de una base de datos permanente de simulaciones.

El usuario debe disponer de una acción explícita **Borrar mi simulación** antes de beta pública. Cerrar la sesión de navegación elimina la información temporal asociada a esa sesión conforme al comportamiento del navegador.

## 11. Custodia, confidencialidad y seguridad

La aplicación aplica minimización de datos, procesamiento temporal de PDF, cabeceras `no-store`, política CSP, validación defensiva de archivos, separación entre identificadores y lógica previsional y pruebas que impiden introducir datos personales reales en fixtures o ejemplos públicos.

No se garantiza riesgo cero. Para una publicación remota deberán añadirse controles de transporte seguro, configuración de servidor, gestión de registros, respuesta a incidentes y revisión de proveedores.

## 12. Destinatarios y terceros

La versión actual no vende ni cede datos de simulación a terceros para fines comerciales. La interfaz todavía puede cargar recursos técnicos externos para Bootstrap; esos proveedores pueden recibir metadatos técnicos ordinarios de conexión, pero la aplicación no les transmite el contenido de la simulación.

Objetivo pre-beta: servir dependencias críticas localmente cuando sea viable y reevaluar cualquier servicio externo antes de enviarle datos personales.

## 13. Cookies y almacenamiento del navegador

La versión actual no crea cookies para publicidad, analítica, seguimiento ni perfilado. El navegador conserva temporalmente datos necesarios para continuar la simulación y puede recordar preferencias de interfaz y la versión de los términos aceptada.

No se muestra un banner de aceptación de cookies porque actualmente no se utilizan cookies no esenciales. Si en el futuro se incorporan cookies, analítica o seguimiento, deberá implementarse un consentimiento específico, previo y granular.

## 14. Derechos del titular

Conforme al marco de referencia panameño, deben contemplarse los derechos de acceso, rectificación, cancelación, oposición y portabilidad cuando procedan. La aplicación permite además revisar y corregir datos antes de usarlos y retirar la autorización para continuar la simulación.

## 15. Ejercicio de derechos

Las solicitudes pueden dirigirse a `ruben.canizares@outlook.com`. Debe solicitarse únicamente la información necesaria para identificar el asunto y evitar recopilar datos adicionales innecesarios. El titular también puede acudir a ANTAI en los casos que correspondan.

Antes de beta pública se debe documentar un procedimiento interno con recepción, verificación razonable de identidad, respuesta, registro de la solicitud y eliminación de información auxiliar cuando deje de ser necesaria.

## 16. Resultados y exportaciones

Los resultados son orientativos y predictivos. No constituyen certificación de cuotas, derecho adquirido, monto definitivo de pensión ni resolución de la CSS.

La futura exportación del Paso 6 deberá:

- mostrar esta advertencia de forma visible;
- permitir excluir identificadores personales;
- incluir solamente los datos seleccionados por el usuario;
- distinguir información acreditada de proyecciones;
- indicar fecha y versión de la aplicación/metodología.

## 17. Datos de terceros

El usuario debe introducir datos propios o información que esté autorizado a tratar. No debe cargar documentos de terceros sin autorización ni utilizar la herramienta para recopilar o compartir información personal ajena fuera de la finalidad previsional.

## 18. Menores de edad

La aplicación no está dirigida a recopilar intencionalmente identificadores personales de menores. Si se utiliza para orientación de un caso de una persona menor de edad, debe evitarse información identificativa innecesaria y observarse la autorización legal que corresponda.

## 19. Incidentes

Antes de beta pública deberá existir un procedimiento de respuesta a incidentes que contemple detección, contención, análisis, evidencia, alcance, medidas correctivas, evaluación de comunicaciones y registro interno.

## 20. Cambios a las condiciones

Cualquier cambio material en categorías de datos, finalidad, conservación, destinatarios, servicios externos o tecnologías de seguimiento obliga a revisar este documento y la Política de Privacidad. La versión del consentimiento debe incrementarse cuando corresponda solicitar una nueva aceptación.

## 21. Legislación y fuentes

Fuentes oficiales mantenidas en `docs/FUENTES_NORMATIVAS.md` y en la pantalla **Fuentes**:

- Ley 81 de 2019;
- Decreto Ejecutivo 285 de 2021;
- ANTAI — Dirección de Protección de Datos Personales y preguntas frecuentes.

## Referencia de estructura

La Revisión 3 tomó como referencia de organización la plantilla de términos compartida por el usuario del portal SERTRACEN, especialmente sus apartados de obtención de información, privacidad, cookies, protección de datos, legislación, modificaciones y canales de consulta. No se reutilizan cláusulas específicas de licencias, biometría, pagos, entregas o trámites porque no corresponden a Mi Retiro Proyectado.


## 22. Presentación y aceptación en la interfaz

La interfaz exige que el usuario llegue al final del documento antes de habilitar la casilla de aceptación. Este control no añade declaraciones de **Fin de los términos** ni mensajes de **Lectura completada**: una vez alcanzado el final, la casilla simplemente queda disponible para una decisión afirmativa. La redacción visible se limita a contenidos relacionados con el uso, alcance, privacidad y tratamiento de datos de Mi Retiro Proyectado.
