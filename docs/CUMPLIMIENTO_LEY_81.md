# Matriz interna de alineación con Ley 81 de 2019

**Producto:** Mi Retiro Proyectado
**Versión de revisión:** UX.4.6b R4
**Objeto:** control técnico/documental interno; no constituye certificación jurídica.

## 1. Referencias

- Ley 81 de 26 de marzo de 2019 sobre Protección de Datos Personales.
- Decreto Ejecutivo 285 de 28 de mayo de 2021.
- Orientaciones públicas de ANTAI.

## 2. Matriz

| Área | Aplicación en Mi Retiro Proyectado | Estado UX.4.6b R4 |
|---|---|---|
| Información previa | Modal completo antes de capturar/importar datos | Implementado |
| Lectura del aviso | Casilla deshabilitada hasta llegar al final; al cumplirse el requisito se habilita sin mensajes meta de “fin” o “lectura completada” | Implementado |
| Consentimiento | Aceptación explícita, versionada y revocable | Implementado |
| Rechazo | Regresa a Inicio y elimina estado temporal de simulación de la pestaña | Implementado |
| Finalidad | Simulación, validación, proyección, comparación, explicación y exportación voluntaria | Documentado |
| Minimización | Identificadores opcionales; campos previsionales separados | Implementado |
| Origen | Manual o documento seleccionado por el titular | Implementado |
| Revisión documental | Vista previa bloqueada, edición deliberada, confirmación explícita | Implementado |
| Conservación | Estado temporal de la simulación; no base de datos permanente | Implementado |
| Cookies | No existen cookies de publicidad/analítica/seguimiento | Verificado por regresión |
| Terceros | No se envía contenido de simulación a terceros; recursos técnicos externos limitados | Parcial; revisar pre-beta |
| Seguridad | Validación PDF, `no-store`, CSP, CI, separación de identificadores | Implementado base |
| Confidencialidad | Política y reglas de no introducir PII real en fixtures/logs/docs | Documentado |
| Acceso/Rectificación | Revisión y edición en UI; canal de contacto | Implementado base |
| Cancelación/Oposición | Rechazo y borrado temporal; falta acción permanente dedicada | Parcial |
| Portabilidad | Exportación estructurada prevista en UX.4.6g | Pendiente |
| Incidentes | Debe existir procedimiento formal antes de beta pública | Pendiente |
| Logs/despliegue | Auditoría específica antes de hosting remoto | Pendiente |
| Revisión jurídica | Validación profesional previa a publicación pública/comercial | Pendiente |

## 3. Inventario de datos y necesidad

| Dato | Necesidad de cálculo | Finalidad |
|---|---|---|
| Nombres/apellidos | No | Identificar voluntariamente la simulación/exportación |
| Apellido de casada | No | Identificación voluntaria cuando corresponda |
| Cédula | No | Identificación voluntaria |
| Número de Seguro Social | No | Identificación voluntaria |
| Fecha de nacimiento | Sí | Edad y fechas previsionales |
| Sexo | Sí para reglas implementadas | Edad/condiciones aplicables |
| Fecha ingreso CSS | Funcional | Contexto de historial |
| Sistema previsional | Sí | Selección del motor aplicable |
| Cuotas | Sí | Evaluación previsional |
| Salarios/historial | Sí según cálculo | Base histórica/proyección |
| Escenarios | Sí para proyección | Comparación predictiva |
| Resultados | Derivado | Explicación/exportación |

## 4. Controles pre-beta obligatorios

1. [x] incorporar controles explícitos de limpieza por paso, reinicio total y borrado local integral;
2. finalizar la exportación con selección de identificadores y aviso no oficial;
3. crear procedimiento de derechos del titular;
4. crear procedimiento de gestión de incidentes;
5. revisar logs y configuración de despliegue;
6. requerir HTTPS/TLS si existe servicio remoto;
7. revisar terceros y servir dependencias críticas localmente cuando proceda;
8. documentar retención si aparece almacenamiento persistente;
9. revisar jurídicamente términos/política antes de beta pública o comercial;
10. repetir la evaluación si se incorporan cuentas, nube, analítica, telemetría, publicidad o nuevos terceros.

## 5. Criterio de cambio

Toda modificación material de finalidad, datos, conservación, destinatarios o tecnologías de seguimiento debe elevar la versión de privacidad, actualizar documentación y determinar si se requiere nuevo consentimiento.

## Controles de eliminación implementados

UX.4.6d R6 incorpora mecanismos directos para que el usuario controle la información local: limpieza del paso activo con invalidación de dependencias, reinicio integral de la simulación y borrado de los datos de la aplicación en el navegador. Estos mecanismos complementan los canales formales para el ejercicio de derechos ARCO y no se presentan como sustitutos de una solicitud formal cuando en el futuro exista un tratamiento remoto/persistente.

### Consulta transparente de condiciones

UX.4.6d R7 permite que el titular vuelva a consultar el texto vigente desde Fuentes sin que esa lectura se interprete como una nueva manifestación de consentimiento. La aceptación inicial y la consulta posterior quedan separadas funcionalmente, preservando trazabilidad y evitando registrar consentimientos redundantes. Esta mejora no introduce una nueva finalidad ni modifica la versión material **2026-08-15.1**.

### UX.4.6d R9 — coherencia del consentimiento en todos los puntos de acceso

R9 unifica los puntos de acceso al documento legal: una persona sin consentimiento puede otorgarlo desde Fuentes o desde el ingreso a Simular usando el mismo texto, versión y mecanismo trazable. Si ya existe aceptación vigente, la revisión posterior no crea una nueva constancia. El diseño mantiene la separación entre consultar información pública y habilitar el tratamiento de datos de la simulación. Este criterio es coherente con el deber de informar propósito/finalidad y obtener consentimiento previo e informado cuando corresponda.

### UX.4.6d R18 — metadata local de continuidad

Se documenta expresamente que la continuidad visual de una importación tras F5 utiliza únicamente metadata local de sesión —incluido, cuando esté disponible, el nombre del documento— y datos previamente confirmados. No se conserva el archivo original ni se introduce una base de datos remota. Por no cambiar finalidad, destinatarios ni tecnología de seguimiento, se mantiene la versión material 2026-08-15.1.


### UX.4.6d R21 — minimización en la verificación de fecha

La nueva consulta externa se limita a obtener una fecha de referencia desde infraestructura oficial de la CSS. No se transmiten categorías de datos previsionales ni el documento importado. Se informa expresamente al titular sobre la posible exposición de metadatos técnicos ordinarios de red y sobre el propósito de la consulta. Por incorporar una nueva interacción de red, el texto de privacidad se versiona como **2026-08-16.1**.
