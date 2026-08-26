# Procedimiento de respuesta a incidentes de seguridad y privacidad

**Estado:** GOV.1.5 R2 — vigente como procedimiento interno
**Versión de aplicación revisada:** `0.1.12.07-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Fecha de cierre original:** 2026-08-18
**Última revisión documental:** PLAN.1 R3B2 — 2026-08-20
**Clasificación:** Seguridad / Privacidad / Procedimiento
**Revisión jurídica externa:** Pendiente antes de la primera versión oficial o cuando un incidente real requiera evaluación jurídica

Este procedimiento define la respuesta interna ante eventos que puedan comprometer confidencialidad, integridad, disponibilidad o tratamiento legítimo de datos personales en Mi Retiro Proyectado.

No constituye un plan certificado de respuesta a incidentes ni sustituye la evaluación jurídica de un incidente real.

## 1. Fuentes oficiales de referencia

- Ley No. 81 de 26 de marzo de 2019;
- Decreto Ejecutivo No. 285 de 28 de mayo de 2021;
- ANTAI — comunicado de 2 de febrero de 2023 sobre vulneraciones al principio de seguridad:
  `https://www.antai.gob.pa/antai-se-pronuncia-sobre-proteccion-de-datos-personales-y-violencia-de-genero-en-internet/`;
- ANTAI — comunicado de 26 de mayo de 2022 sobre un incidente investigado:
  `https://www.antai.gob.pa/comunicado-proteccion-de-datos-personales/`;
- ANTAI — preguntas frecuentes:
  `https://antai.gob.pa/preguntas-frecuentes-de-proteccion-de-datos-personales/`.

ANTAI ha reiterado públicamente el deber de confidencialidad y la necesidad de reportar **con inmediatez** vulneraciones al principio de seguridad e informar al titular cuando sus datos hayan sido violados.

## 2. Qué se considera incidente

Ejemplos:

- PDF personal persistido donde no debía;
- log con cédula, NSS, salario o resultado;
- repositorio/commit con datos reales;
- acceso no autorizado a archivos diagnósticos;
- exposición accidental de FastAPI fuera de la frontera prevista;
- dependencia comprometida utilizada por el runtime;
- XSS que permita leer estado de simulación;
- alteración no autorizada de normativa o motores;
- fuga de secretos/credenciales;
- pérdida de integridad de un artefacto de release;
- envío no previsto de datos de simulación a un tercero;
- dispositivo o entorno de desarrollo comprometido con acceso a datos del proyecto.

Un error funcional sin impacto de seguridad puede seguir el flujo de bugs ordinario.

## 3. Roles actuales

Mientras el proyecto sea mantenido por una sola persona:

- **Responsable de coordinación:** mantenedor del proyecto;
- **Responsable técnico:** mantenedor del proyecto;
- **Responsable de privacidad:** mantenedor del proyecto;
- **Asesoría jurídica:** externa y pendiente de designación cuando sea necesaria.

La coincidencia de roles no elimina la obligación de documentar decisiones y evidencias.

## 4. Principios

1. contener antes de investigar en profundidad si la exposición continúa;
2. preservar evidencia sin copiar datos personales innecesarios;
3. no ocultar ni minimizar el alcance;
4. separar hechos confirmados de hipótesis;
5. no borrar evidencia necesaria sin antes preservarla de forma controlada;
6. evitar que la respuesta amplifique la fuga;
7. notificar/escalar cuando corresponda;
8. corregir la causa, no solo el síntoma;
9. documentar lecciones y controles preventivos.

## 5. Severidad interna

### SEV-1 — Crítica

Ejemplos:

- exposición pública activa de datos personales;
- credencial con capacidad de acceso sensible comprometida;
- modificación no autorizada de motores/normativa distribuida;
- tercero recibiendo datos de simulación sin base prevista.

Acción: contención inmediata y evaluación de notificación/escalamiento.

### SEV-2 — Alta

Ejemplos:

- PII en logs o repositorio privado;
- PDF personal versionado accidentalmente;
- servicio expuesto en LAN/Internet sin controles previstos;
- vulnerabilidad explotable con acceso a estado de simulación.

Acción: contención prioritaria, análisis y corrección.

### SEV-3 — Media

Ejemplos:

- control defensivo degradado sin evidencia de acceso;
- dependencia vulnerable sin explotación confirmada;
- error de CSP/SRI que reduzca defensa.

Acción: corregir y evaluar exposición.

### SEV-4 — Baja

Evento de seguridad sin acceso sensible ni riesgo material inmediato.

La severidad es operativa, no una clasificación legal.

## 6. Flujo de respuesta

### Fase A — Detección y apertura

Registrar:

- `incident_id` aleatorio;
- fecha/hora de detección;
- fuente de detección;
- categoría técnica;
- severidad inicial;
- estado.

No registrar el contenido completo de datos comprometidos en el ledger.

### Fase B — Contención

Según el caso:

- retirar publicación/artefacto;
- deshabilitar endpoint o servicio;
- revocar credencial;
- detener sincronización;
- bloquear acceso;
- rotar secreto;
- revertir dependencia;
- aislar equipo comprometido;
- desactivar Developer Diagnostics si el propio log es la superficie.

### Fase C — Preservación de evidencia

Preservar de forma privada:

- hashes;
- timestamps;
- SHAs;
- nombres de archivos necesarios;
- eventos técnicos;
- alcance temporal;
- evidencia mínima del tipo de dato comprometido.

Evitar duplicar PDF, historiales o identificadores si no es necesario.

### Fase D — Evaluación

Determinar:

- qué ocurrió;
- cuándo;
- qué activos;
- qué categorías de datos;
- cuántos titulares, si puede determinarse;
- si hubo acceso, modificación, pérdida o divulgación;
- si continúa la exposición;
- qué terceros intervinieron;
- controles que fallaron;
- riesgo para titulares;
- obligaciones de notificación/escalamiento.

### Fase E — Comunicación y notificación

ANTAI ha señalado la necesidad de reportar **con inmediatez** vulneraciones al principio de seguridad e informar al titular cuando los datos han sido violados.

Por tanto, ante un incidente real que afecte datos personales:

1. evaluar inmediatamente la obligación de reportar a ANTAI;
2. evaluar e informar a titulares afectados cuando corresponda;
3. escalar a revisión jurídica cuando exista duda;
4. documentar decisión, momento y canal;
5. no retrasar una comunicación necesaria para completar un informe perfecto.

### Importante sobre "72 horas"

Este procedimiento **no establece 72 horas como plazo legal general**.

En un comunicado de 2022, ANTAI solicitó a una empresa un informe en 72 horas dentro de una investigación concreta. Ese requerimiento específico no se transforma aquí en un plazo universal para toda brecha.

## 7. Objetivos operativos internos

Estos objetivos son metas internas, **no plazos legales**:

| Hito | Objetivo interno |
|---|---|
| Clasificar evento inicial | Lo antes posible tras detección |
| Contener una exposición activa SEV-1 | Inmediato |
| Abrir registro mínimo | Durante la respuesta inicial |
| Evaluar si hay datos personales afectados | Prioridad alta |
| Evaluar notificación/escalamiento | Sin demora |
| Corregir causa raíz | Según severidad, antes de declarar cierre |
| Post-mortem | Después de estabilización |

No se usará un objetivo interno para retrasar una obligación legal.

## 8. Registro mínimo del incidente

El registro real debe mantenerse privado y fuera de Git.

Campos mínimos:

- `incident_id`;
- fecha/hora detección;
- categoría;
- severidad;
- estado;
- activo afectado;
- categorías generales de datos;
- alcance estimado;
- acciones de contención;
- decisión de notificación;
- fecha/hora de comunicaciones;
- causa raíz;
- acciones correctivas;
- fecha de cierre.

No incluir salvo necesidad estricta:

- cédulas completas;
- NSS completos;
- PDF;
- historia salarial completa;
- resultados previsionales;
- tokens/secretos;
- mensajes de excepción con PII.

## 9. Uso de GitHub durante un incidente

No publicar datos personales en:

- issue;
- Pull Request;
- comentario;
- commit;
- workflow log;
- artifact público.

Si el incidente está en Git:

1. detener nuevas propagaciones;
2. evaluar exposición local/remota;
3. preservar SHA/evidencia;
4. retirar o sanear siguiendo un plan controlado;
5. considerar que borrar un archivo en un commit nuevo no elimina copias históricas;
6. escalar la reescritura histórica solo cuando sea necesaria y documentada.

Los tags publicados siguen sujetos a las reglas de integridad; un incidente puede requerir un procedimiento excepcional separado.

## 10. Developer Diagnostics durante incidentes

Los logs son una posible fuente de evidencia, pero también una posible superficie.

Reglas:

- no ampliar su retención automáticamente;
- no compartir el ZIP diagnóstico sin revisión;
- inspeccionar si la sanitización funcionó;
- si existe PII, tratar el log como dato comprometido;
- preservar solo la evidencia necesaria;
- documentar correlation IDs y clases de eventos, no copiar datos sensibles a reportes generales.

## 11. Recuperación

Antes de declarar recuperación:

- corregir la causa raíz;
- rotar credenciales afectadas;
- actualizar dependencia si corresponde;
- agregar regresión automatizada cuando sea posible;
- ejecutar suite completa;
- revisar documentación dependiente;
- confirmar que no continúa la exposición;
- evaluar si se requiere nueva versión/release.

## 12. Post-mortem

Debe separar:

- hechos;
- impacto;
- línea de tiempo;
- controles que funcionaron;
- controles que fallaron;
- causa raíz;
- acciones correctivas;
- acciones preventivas;
- deuda pendiente.

El post-mortem versionado debe ser sanitizado. La evidencia sensible permanece fuera del repositorio.

## 13. Criterio de cierre

Un incidente no se cierra solo porque "ya no se ve".

Requiere:

- exposición contenida;
- causa evaluada;
- corrección aplicada o plan aceptado;
- notificaciones/escalamientos decididos;
- evidencia protegida;
- pruebas/documentación actualizadas;
- riesgos residuales registrados.

## 14. Disparadores de revisión del procedimiento

Revisar si cambia:

- legislación/criterio ANTAI;
- arquitectura local/remota;
- persistencia;
- autenticación;
- proveedor externo;
- Developer Diagnostics;
- repositorio/distribución;
- responsable/canal;
- proceso de releases.

## 15. Frontera de afirmación

Este procedimiento no afirma que:

- toda brecha deba manejarse idénticamente;
- exista un plazo general de 72 horas;
- el proyecto cuente ya con un SOC/CSIRT;
- se haya realizado una auditoría forense externa;
- la revisión jurídica esté completada.

## 16. Historia

El contrato funcional de este procedimiento se cerró originalmente en GOV.1.5 R2 sobre `0.0.23-beta`. PLAN.1 actualiza únicamente su metadata viva y el gate futuro; no cambia el flujo de respuesta ni convierte una meta interna en plazo legal.
