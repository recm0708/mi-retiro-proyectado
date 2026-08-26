# Procedimiento de derechos del titular

**Estado:** GOV.1.5 R2 — vigente como procedimiento interno
**Versión de aplicación revisada:** `0.1.09.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Fecha de cierre original:** 2026-08-18
**Última revisión documental:** PLAN.1 R3B2 — 2026-08-20
**Clasificación:** Privacidad / Procedimiento / Interna
**Revisión jurídica externa:** Pendiente antes de la primera versión oficial o de un cambio material del tratamiento/despliegue

Este procedimiento define cómo debe atender Mi Retiro Proyectado una solicitud de ejercicio de derechos sobre datos personales cuando el proyecto sea responsable de un tratamiento alcanzado por la normativa aplicable.

No constituye asesoría jurídica ni sustituye la revisión profesional prevista en REV.1 ni la evaluación que corresponda ante un despliegue remoto.

## 1. Marco de referencia

Fuentes oficiales consultadas:

- Ley No. 81 de 26 de marzo de 2019 sobre Protección de Datos Personales;
- Decreto Ejecutivo No. 285 de 28 de mayo de 2021, que reglamenta la Ley 81;
- ANTAI — Preguntas frecuentes de Protección de Datos Personales:
  `https://antai.gob.pa/preguntas-frecuentes-de-proteccion-de-datos-personales/`;
- ANTAI — Dirección de Protección de Datos Personales:
  `https://antai.gob.pa/direccion-de-proteccion-de-datos-personales/`.

La versión de aplicación y la versión material de privacidad son contratos diferentes.

## 2. Derechos contemplados

El procedimiento cubre:

- **Acceso:** conocer si se tratan datos personales, así como su origen/finalidad cuando corresponda;
- **Rectificación:** corregir información incorrecta, irrelevante, incompleta, desfasada, inexacta, falsa o impertinente;
- **Cancelación:** solicitar la eliminación cuando proceda;
- **Oposición:** oponerse a determinado tratamiento o revocar consentimiento cuando proceda;
- **Portabilidad:** obtener una copia estructurada en un formato genérico y de uso común cuando corresponda.

El proyecto no presentará estos derechos como equivalentes a los controles locales de "limpiar", "reiniciar" o "borrar datos del navegador". Esos controles son funciones de producto; el ejercicio formal de derechos es un procedimiento distinto.

## 3. Canal actual del proyecto

Canal inicial del responsable:

`ruben.canizares@outlook.com`

La solicitud debe poder presentarse en lenguaje sencillo. No se exige al titular utilizar terminología jurídica exacta para que una petición sea evaluada.

## 4. Recepción

Al recibir una solicitud:

1. registrar un identificador interno aleatorio;
2. registrar fecha y hora de recepción;
3. identificar el derecho solicitado;
4. confirmar recepción por el mismo canal o uno acordado;
5. calcular el plazo aplicable;
6. limitar la recopilación adicional a lo necesario para verificar legitimidad e identidad;
7. evitar copiar el contenido completo de la solicitud a logs técnicos o al repositorio.

## 5. Plazos de atención

Según la información publicada por ANTAI:

| Derecho | Plazo máximo publicado |
|---|---|
| Acceso | 10 días hábiles |
| Rectificación | 5 días hábiles |
| Cancelación | 10 días hábiles |
| Portabilidad | 10 días hábiles |
| Oposición | Efecto inmediato, sujeto a las salvedades legales indicadas por ANTAI |

Para oposición, ANTAI señala que el responsable debe cesar el tratamiento desde la solicitud, salvo que concurran motivos legítimos imperiosos o sea necesario para la formulación, ejercicio o defensa de reclamaciones.

Los plazos se cuentan como **días hábiles** cuando así lo publica ANTAI.

Si existe duda sobre el cómputo en un caso real, debe escalarse a revisión jurídica en vez de inventar una extensión.

## 6. Solicitud cuando el proyecto no conserva datos remotos

La arquitectura actual:

- no dispone de cuentas;
- no mantiene una base de datos permanente de simulaciones;
- no sincroniza casos a una nube del proyecto;
- mantiene la simulación principalmente en `sessionStorage`;
- procesa PDF en memoria;
- no envía el contenido de la simulación a GitHub.

Aun si el responsable **no mantiene datos almacenados del solicitante**, ANTAI indica que debe responder al ejercicio del derecho.

La respuesta debe explicar de forma clara:

- qué tratamiento existe realmente;
- si se localizaron o no datos bajo control del responsable;
- qué datos permanecen únicamente en el dispositivo/navegador del usuario;
- qué controles locales puede usar el titular;
- que no se inventó un registro inexistente.

## 7. Verificación de identidad y legitimidad

La verificación debe ser proporcional al riesgo.

Reglas internas:

- no pedir copia de cédula de forma automática;
- no recopilar más datos de los necesarios;
- usar primero información ya disponible y el canal de contacto;
- si la solicitud requiere revelar o modificar datos de alta sensibilidad, aumentar la verificación de manera proporcional;
- no guardar documentos de identidad en el repositorio;
- no incluir documentos de identidad en Developer Diagnostics;
- registrar solo el resultado de la verificación, no una copia íntegra de la evidencia, salvo necesidad real y controlada.

Cuando exista representación, minoría de edad u otra condición especial, el caso debe evaluarse conforme al marco aplicable y, si es necesario, escalarse a revisión jurídica.

## 8. Registro mínimo de la solicitud

El producto no implementa una base de datos de derechos.

Si se recibe una solicitud real, el responsable mantendrá un registro privado y separado del repositorio con el mínimo necesario:

- `case_id` aleatorio;
- fecha/hora de recepción;
- tipo de derecho;
- canal;
- estado de verificación (`pendiente`, `verificada`, `no_verificada`);
- fecha límite calculada;
- estado (`recibida`, `en_revision`, `respondida`, `cerrada`);
- fecha de respuesta/cierre;
- referencia a evidencia almacenada de forma separada si fuera estrictamente necesaria.

No deben registrarse en ese ledger:

- PDF de simulación;
- historial salarial completo;
- NSS/cédula completos;
- resultados previsionales;
- contraseñas o tokens;
- copia integral del correo cuando basten los campos mínimos.

El registro real de solicitudes **no se versiona en Git**.

## 9. Flujo de atención

### Acceso

1. localizar tratamientos y datos bajo control del responsable;
2. verificar identidad proporcionalmente;
3. preparar respuesta comprensible;
4. indicar origen/finalidad y demás información aplicable;
5. responder dentro del plazo.

### Rectificación

1. identificar el dato;
2. comprobar la corrección solicitada;
3. rectificar donde exista almacenamiento bajo control del responsable;
4. confirmar el resultado.

### Cancelación

1. identificar el dato/tratamiento;
2. evaluar si procede conservación por obligación o motivo legítimo aplicable;
3. eliminar o bloquear según corresponda;
4. documentar la decisión;
5. confirmar al titular.

### Oposición

1. identificar el tratamiento objeto de oposición;
2. cesar de inmediato cuando proceda;
3. si existe una excepción legal aplicable, documentarla y escalarla;
4. responder al titular.

### Portabilidad

1. localizar datos bajo control del responsable;
2. seleccionar únicamente datos personales cubiertos;
3. producir un formato estructurado y de uso común cuando corresponda;
4. evitar incluir datos de terceros;
5. entregar de forma segura.

## 10. Respuesta

Toda respuesta debe:

- identificar el `case_id`;
- indicar qué derecho se atendió;
- explicar las acciones realizadas;
- indicar si no se localizaron datos;
- identificar cualquier limitación o excepción aplicada;
- indicar fecha de cierre;
- evitar divulgar datos de terceros;
- utilizar un canal razonablemente seguro.

No se debe afirmar que "no existen datos" si solo se comprobó una parte del tratamiento.

## 11. Denegación o limitación

Una denegación o limitación:

- debe documentarse;
- debe tener un fundamento identificable;
- no debe basarse en conveniencia operativa;
- debe escalarse a revisión jurídica si la base no es clara;
- debe comunicarse al titular con transparencia.

## 12. Escalamiento a ANTAI

La Dirección de Protección de Datos Personales de ANTAI es la autoridad de control.

ANTAI publica, entre otros, estos medios para denuncias:

- opción ANTAI Smart CID en su sitio oficial;
- correo `protecciondedatos@antai.gob.pa`;
- presentación presencial en su sede principal.

La existencia de esos canales no elimina el deber del responsable de atender directamente las solicitudes que le correspondan.

## 13. Privacidad del propio procedimiento

Las solicitudes de derechos pueden contener datos sensibles.

Por ello:

- no se copian a Developer Diagnostics;
- no se incluyen en issues públicos;
- no se adjuntan a Pull Requests;
- no se guardan en `docs/`;
- no se usan como fixtures reales de prueba;
- cualquier caso de prueba debe ser sintético o anonimizado de forma irreversible.

## 14. Disparadores de revisión

Revisar este procedimiento si cambia:

- la Ley 81 o su reglamentación;
- la interpretación pública de ANTAI;
- el canal del responsable;
- la versión material de privacidad;
- la arquitectura local;
- la existencia de cuentas;
- la persistencia;
- la nube/sincronización;
- los destinatarios/terceros;
- el procedimiento de exportación de datos.

## 15. Frontera de afirmación

Este documento implementa una política interna verificable.

No afirma:

- certificación de cumplimiento;
- que todo caso pueda resolverse sin asesoría jurídica;
- que la ausencia de base de datos elimine todos los tratamientos de datos personales;
- que los plazos internos sustituyan el texto legal o criterios posteriores de la autoridad.

## 16. Historia

El contrato funcional de este procedimiento se cerró originalmente en GOV.1.5 R2 sobre `0.0.23-beta`. PLAN.1 actualiza únicamente su metadata viva y el gate futuro; no reescribe los plazos, derechos ni controles históricos validados.
