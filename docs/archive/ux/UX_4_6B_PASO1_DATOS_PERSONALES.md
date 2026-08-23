# UX.4.6b — Simular / Paso 1 · Datos personales

## Estado

**Cerrada y validada en PC/laptop. CI remoto en verde para Python 3.13 y 3.14.**

Base: `main` después del cierre de UX.4.6a. La fase no modifica fórmulas previsionales.

## Objetivo

Reducir la carga visual del Paso 1, separar captura manual e importación documental, incorporar identificación opcional, introducir consentimiento informado antes de tratar datos y establecer patrones transversales de navegación, tablas y ayudas que se reutilizarán en UX.4.6c–g.

## Cambios funcionales y de interfaz

1. Modalidad **Ingresarlos manualmente** seleccionada por defecto.
2. Modalidad **Importar desde Mi Retiro Seguro**; una modalidad oculta a la otra.
3. Identificación opcional: primer/segundo nombre, primer/segundo apellido, apellido de casada, cédula y número de Seguro Social.
4. Fecha de nacimiento, sexo y sistema previsional se marcan con `*` como obligatorios y conservan validación accesible inline.
5. Apellido de casada condicionado a sexo femenino.
6. La separación visual original entre Identificación personal e Información previsional básica fue sustituida posteriormente por UX.4.6d R14: la captura manual usa un único bloque **Información personal** para reducir recorridos y mantener Sexo junto al Apellido de casada.
7. Eliminación del cuadro redundante sobre cálculo de edad; la ayuda se integra debajo de Fecha de nacimiento.
8. Ficha Digital trasladada al Paso 3.
9. Cargador PDF compacto con selector y **Analizar documento** alineados.
10. Vista previa del comprobante bloqueada inicialmente.
11. **Editar campos** habilita cambios; **Finalizar edición** vuelve al modo revisión; **Importar datos** aplica lo revisado y queda deshabilitado durante una edición abierta.
12. Se eliminan leyendas técnicas/redundantes de `Detectado/No detectado` y el aviso de nombre completo sin dividir.
13. El parser descompone nombres completos de forma conservadora y revisable; en mujeres reconoce un sufijo final `de Apellido` como apellido de casada.
14. Origen de datos personales: `MANUAL`, `MI_RETIRO_SEGURO`, `MI_RETIRO_SEGURO_EDITADO`.
15. Navegación dual y simétrica: barra superior dentro del mismo ancho del formulario y barra inferior equivalente. En escritorio la superior usa `sticky` bajo el encabezado para mantener Inicio/Anterior, selector de paso y acción primaria accesibles durante pasos largos; la inferior ofrece cierre natural del paso.
16. Hover de tablas más perceptible como regla transversal.
17. Ayuda contextual mediante icono `i` en lugar del círculo `?`, con reposicionamiento para evitar recortes.
18. Menor espacio vertical y alineación de la fila final de identificación en escritorio.

## Consentimiento, privacidad y cookies

Antes de ingresar o importar datos, `Simular` muestra un modal no descartable por clic exterior con un documento ampliado de 21 apartados: objeto, responsable, marco legal, obtención, categorías de datos, finalidad, consentimiento, calidad, documentos PDF, conservación, custodia, terceros, cookies, derechos, ejercicio de derechos, resultados/exportaciones, datos de terceros, menores, incidentes, modificaciones y legislación aplicable.

La casilla **He leído y acepto...** permanece deshabilitada hasta que el usuario llega al final del documento. Solo entonces puede marcarse y habilitar **Aceptar y continuar**. La Revisión 4 elimina el bloque **Fin de los términos** y el mensaje **Lectura completada**; al llegar al final simplemente se habilita la casilla y desaparece la ayuda previa de desplazamiento. **No acepto** elimina el estado temporal de la simulación de esa pestaña y regresa a Inicio. La aceptación está versionada para solicitarse nuevamente tras cambios materiales.

La interfaz evita exponer terminología técnica de almacenamiento que no aporta valor al usuario. Explica en lenguaje común que el navegador mantiene temporalmente la simulación y puede recordar preferencias. La aplicación actual **no crea cookies de publicidad, analítica, seguimiento ni perfilado**, por lo que no se implementa un banner de cookies ficticio. Si en el futuro aparecen cookies no esenciales, analítica o telemetría, se requerirá consentimiento específico previo.

La política pública completa se documenta en `POLITICA_PRIVACIDAD.md` y `TERMINOS_USO_PRIVACIDAD.md`; la matriz técnica de controles y pendientes en `CUMPLIMIENTO_LEY_81.md`.

## Privacidad de documentos e identificadores

Los PDF se procesan para extraer información y el archivo original no se persiste como parte de la simulación. Nombres, apellidos, cédula y NSS pueden formar parte del estado de sesión si el usuario los confirma. El código único del documento continúa excluido.

Los identificadores no se usan para fórmulas previsionales. No deben aparecer datos personales reales en logs, fixtures, capturas versionadas ni documentación.

## Ficha Digital

La Ficha Digital mantiene su endpoint, parser y contrato funcional. Solo cambia su ubicación: se presenta en el Paso 3 junto al historial salarial y detalle del año actual. Su rediseño integral queda reservado para UX.4.6d.

## Navegación común

La Revisión 4 conserva el patrón definido en R3 con dos barras con el mismo contrato visual y funcional, ambas alineadas al ancho `col-xl-11` de las tarjetas del asistente. La barra superior mantiene Inicio/Anterior, selector de salto directo, estado y acción primaria; en PC/laptop puede permanecer visible bajo el encabezado mientras se recorre un paso largo. La barra inferior repite esos controles al final del contenido. El JavaScript sincroniza disponibilidad, textos y selección entre ambas sin duplicar lógica de negocio.

## Seguridad R4

- `Cache-Control: no-store` para `/api/simulacion/*`;
- CSP y cabeceras defensivas globales;
- SRI para Bootstrap temporalmente servido por jsDelivr;
- validación defensiva de PDFs ya existente;
- recomendación pre-beta de servir Bootstrap localmente.

## Exportación futura

UX.4.6g deberá permitir exportar por acción expresa cuotas, historial, proyecciones, escenarios y resultados relevantes, marcando el archivo como **estimación orientativa/no oficial** y permitiendo excluir identificadores personales. La exportación no se enviará automáticamente a servicios externos.

## Pruebas

La Revisión 4 conserva las regresiones de lectura completa antes de consentir, ausencia de terminología técnica, navegación dual y ayudas sin recorte, y añade protección para que no reaparezcan **Fin de los términos**, **Lectura completada** ni un posicionamiento visible del producto como aplicación educativa/didáctica. La suite completa queda en **233 pruebas automatizadas en OK** después de la Revisión 4.

## Pendiente para cierre

Validación manual en PC/laptop de: consentimiento aceptar/rechazar y habilitación silenciosa de la casilla al llegar al final, Manual/PDF, asteriscos y errores obligatorios, cargador compacto, parser de nombre/apellido de casada, modal revisión/edición/importación, hover de tablas, ayuda mediante icono `i`, navegación superior/inferior y comportamiento `sticky` de escritorio, Fuentes/privacidad y los tres temas. Después de la aceptación se actualizará el estado documental y se prepararán commits lógicos por categorías.


## Criterio transversal de contenido visible

Los textos dirigidos al usuario deben responder a una necesidad real de operación, previsión, alcance, privacidad, seguridad, accesibilidad o cumplimiento legal. No se utilizará lenguaje que presente Mi Retiro Proyectado como producto educativo, didáctico o pedagógico, ni se mostrarán detalles internos de implementación cuando no ayuden a realizar una acción o comprender una consecuencia relevante.

## Ajuste posterior durante UX.4.6d R14

Durante la certificación integral de Pasos 1–3 se detectó una fricción de recorrido en captura manual: **Sexo** se encontraba en el bloque previsional inferior, mientras **Apellido de casada** aparecía en el bloque de identificación superior. R14 unifica ambos grupos bajo **Información personal** y sitúa Sexo inmediatamente antes del campo condicional. Nombres, apellidos, cédula y NSS siguen siendo opcionales; Fecha de nacimiento, Sexo y Sistema previsional conservan su obligatoriedad. La importación desde Mi Retiro Seguro y las fórmulas no cambian.

## Ajuste transversal R15

Durante la certificación integral de UX.4.6d, el Paso 1 adopta terminología neutral de documento: la modalidad se denomina **Importar desde Mi Retiro Seguro** y el encabezado evita “PDF compatible”. El formato técnico actual sigue siendo PDF. Los controles importados también heredan el nuevo contraste visual global de campos no editables.

### Nota R18 — procedencia por campo

Paso 1 adopta el contrato Detectado / Editado por ti / Completado manualmente / No detectado. Un campo ausente en Mi Retiro Seguro permanece editable en el formulario principal; los valores confirmados se bloquean y deben corregirse desde Revisar importación. La procedencia se conserva por campo para que un apellido de casada agregado manualmente no vuelva a presentarse como detectado.
