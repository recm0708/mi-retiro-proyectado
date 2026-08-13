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
| Origen | Manual o PDF seleccionado por el titular | Implementado |
| Revisión PDF | Vista previa bloqueada, edición deliberada, confirmación explícita | Implementado |
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

1. agregar **Borrar mi simulación** desde el asistente;
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
