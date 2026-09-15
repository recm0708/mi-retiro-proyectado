# Términos de uso, privacidad y tratamiento de datos

**Producto:** Mi Retiro Proyectado
**Versión del texto:** `2026-08-16.1`
**Estado:** Vigente en la aplicación
**Versión de aplicación revisada:** `0.1.25.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Versión base histórica preservada:** `0.0.23-beta`
**Revisión documental base:** GOV.1.3 R3 — 2026-08-17
**Última revisión documental:** AUD.SEC2 R1 — 2026-08-25
**Revisión jurídica externa:** Pendiente antes de la primera versión oficial o de un cambio material del tratamiento/despliegue

Este documento describe las condiciones funcionales actualmente implementadas. No constituye una certificación jurídica ni una resolución de la CSS.

Su alcance corresponde exclusivamente a la aplicación principal de simulación
y a las funciones públicas utilizadas por Asegurados(as). Las superficies
administrativas internas se rigen por controles y documentación separados.

## 1. Objeto

Mi Retiro Proyectado es una herramienta independiente para estimar, explicar y comparar escenarios previsionales.

## 2. Independencia

La aplicación:

- no pertenece a la CSS;
- no certifica cuotas;
- no reconoce derechos adquiridos;
- no emite resoluciones;
- no garantiza el monto definitivo de una pensión.

Las fuentes oficiales deben consultarse para decisiones individuales.

## 3. Responsable y contacto

Responsable del proyecto: **Rubén Enrique Cañizares Miranda**, Panamá.

Contacto: `ruben.canizares@outlook.com`

## 4. Uso de datos

La aplicación puede utilizarse en modalidad Manual o Asistida.

En modalidad Manual, el Asegurado(a) introduce y revisa directamente los datos.
En modalidad Asistida puede seleccionar voluntariamente Mi Retiro Seguro,
Ficha Digital o ambos para preparar información compatible con la simulación.

Los identificadores directos continúan siendo opcionales para las fórmulas
principales.

## 5. Importación

Los PDF seleccionados se procesan temporalmente para extraer información y
generar una vista previa.

Por ello:

- el usuario revisa los datos detectados;
- puede corregirlos cuando corresponda;
- los datos se aplican solo tras confirmación explícita;
- el **archivo original no se guarda** como parte de la simulación;
- no se conserva la ruta local ni el contenido binario del PDF.

Después de confirmar puede mantenerse durante la sesión metadata mínima de
continuidad, como el nombre visible del documento y los datos aceptados.

## 6. Consentimiento

El tratamiento dentro de Simular exige aceptación de la versión vigente.

La interfaz obliga a llegar al final del documento antes de habilitar la casilla.

Una aceptación activa está versionada y vinculada a la sesión actual además de conservar metadata local.

## 7. Conservación

La simulación se conserva temporalmente en la sesión de la pestaña del
navegador.

La aplicación principal no dispone de cuentas de Asegurado(a), base de datos
permanente de simulaciones, sincronización remota ni nube del proyecto para
conservar un historial personal de simulaciones.

## 8. Control local

Existen tres niveles:

- **Limpiar este paso**;
- **Reiniciar simulación**;
- **Borrar datos de esta aplicación en este navegador**.

Cada uno tiene el alcance descrito en `simulation-data-management.md`. El borrado integral invalida la aceptación local y vuelve a presentar las condiciones desde Inicio; si se cierran sin aceptar, el siguiente ingreso a Simular debe solicitarlas nuevamente antes de habilitar el asistente.

## 9. Documentos originales

Los PDF seleccionados no se incorporan a una base de datos permanente.

Puede conservarse metadata mínima de continuidad después de una importación confirmada.

## 10. Resultados

Los resultados son orientativos/predictivos.

La precisión depende de:

- datos suministrados;
- datos acreditados disponibles;
- supuestos futuros;
- parámetros normativos versionados;
- limitaciones del modelo.

## 11. Datos no confirmados, decisiones y cambio de modalidad

El modo Asistido prepara datos compatibles, pero **no decide por el
Asegurado(a)**. Cuando el motor requiere una decisión personal o un dato
individual que no puede inferirse con seguridad, debe quedar pendiente o
solicitarse explícitamente.

Si el usuario cambia a modalidad Manual después de una importación confirmada,
la aplicación advierte antes de retirar los **datos que proceden de documentos**
y reiniciar los cálculos posteriores que dependan de ellos. Los
**datos personales introducidos manualmente** que no procedan de documentos
pueden conservarse.

No se inventan saldos, decisiones o parámetros actuariales personales.

## 12. Terceros y conexiones

La interfaz carga actualmente Bootstrap desde jsDelivr.

El backend puede consultar la fecha HTTP de infraestructura oficial CSS para vigencia documental.

Estas conexiones se describen en `privacy-policy.md` y `security-and-privacy.md`.

## 13. Cookies y seguimiento de la aplicación principal

La aplicación principal no utiliza cookies propias para publicidad, analítica,
seguimiento o perfilado. El navegador puede conservar preferencias de
funcionamiento y la constancia versionada de aceptación, mientras que la
simulación previsional permanece limitada al estado temporal de la sesión.

Si cambia materialmente este modelo, los términos deberán revisarse antes de
habilitar la nueva finalidad o mecanismo.

## 14. Derechos

El proyecto toma como referencia los derechos reconocidos por la Ley 81 y las orientaciones de ANTAI.

El procedimiento formal interno ya se documenta en `data-subject-rights-procedure.md`.

Canal de contacto:

`ruben.canizares@outlook.com`

## 15. Uso de información de terceros

El usuario debe utilizar datos propios o información que esté autorizado a tratar.

No debe cargar documentación de otra persona sin autorización aplicable.

## 16. Seguridad

Se aplican controles técnicos documentados, pero no se garantiza riesgo cero.

Un despliegue remoto requiere endurecimiento y evaluación adicional antes de considerarse soportado.

## 17. Cambios

Los cambios materiales en tratamiento de datos exigen revisar la versión de privacidad y determinar si corresponde nueva aceptación.

## 18. Legislación de referencia

- Ley 81 de 2019;
- Decreto Ejecutivo 285 de 2021;
- fuentes ANTAI listadas en `regulatory-sources.md`.

## 19. Revisión externa

Estos términos requieren revisión jurídica formal en REV.1 antes de la primera versión oficial y deben revisarse nuevamente si cambia materialmente el tratamiento o el modelo de despliegue.

## 20. Historia

El documento acumulativo previo, incluidas revisiones UX, se conserva en:

`docs/archive/regulatory-privacy/terms-and-privacy-pre-gov1-3-r3.md`

La reorganización R3 no modifica por sí sola la versión material `2026-08-16.1`.
