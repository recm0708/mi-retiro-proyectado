# Registro de decisiones técnicas

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.14.01-beta`
**Versión base histórica:** `0.0.25-beta`
**Base documental histórica:** `0.0.23-beta` — GOV.1.3 R4 — 2026-08-17
**Revisión documental:** GOV.1.3 R4 — 2026-08-17
**Última actualización de gobierno:** PLAN.1 / ADR-168 — 2026-08-20
**Última actualización técnica:** VER.2 / ADR-179; reconciliación AUD.SEC2 R1 — 2026-08-25
**Clasificación:** Técnica / Gobierno / Auditoría
**ADR indexadas:** 179 (`ADR-001` a `ADR-179`)


<!-- DOC1-R1-REVISION-MANUAL:START -->
## Nota de lectura post-MANT.1

Este registro conserva decisiones técnicas históricas y vigentes. Las menciones a R6, R7, UX.4.6 o bloques anteriores deben leerse según el contexto de cada ADR.

Estado vigente para lectura transversal:

- MANT.1 quedó cerrado operativamente en R7.
- DOC.1 R1 está cerrado.
- VER.2 está cerrado y `v0.0.71.01-beta` fue publicado.
- NOR.1 y NOR.2 están cerrados.
- DOC.1 R2 está cerrado como auditoría de la documentación Markdown vigente posterior a NOR.2.
- Las decisiones históricas no se reescriben como si hubieran sido tomadas en una revisión posterior.
- `VERSION` está sincronizado en `0.1.11.01-beta` (G111/E01); `v0.0.26-beta` se conserva como referencia legacy histórica.
- SEC.2 quedó cerrado después de R1–R6; AUD.SEC2 R1 reconcilia la trazabilidad revision-aware sin reescribir decisiones históricas.
<!-- DOC1-R1-REVISION-MANUAL:END -->

Este registro conserva decisiones de arquitectura, modelado, UX, precisión, seguridad y aplicación normativa. Una ADR explica por qué el proyecto adoptó una decisión; no crea una norma jurídica.

## 1. Reglas de lectura

- La numeración es única y consecutiva.
- El campo **Estado** dentro de cada ADR es la fuente de vigencia de esa decisión.
- Una decisión sustituida no se elimina.
- Las relaciones de sustitución se conservan en el texto de las ADR implicadas.
- Una ADR normativa debe leerse junto con la fuente oficial correspondiente.
- El snapshot pre-R4 se conserva en `docs/archive/governance/DECISIONES_PRE_GOV1_3_R4.md`.

## 2. Anomalías históricas de metadata

Las ADR siguientes no declaraban una línea `**Estado:**` en el registro inmediatamente anterior a R4:

`ADR-086`

R4 **no inventa un estado retroactivo** para esas decisiones. El índice las marca como `No declarado explícitamente en el registro pre-R4` y el registro íntegro inferior conserva su contenido original sin alterarlo.

## 3. Índice de decisiones

| ADR | Decisión | Estado declarado |
|---|---|---|
| ADR-001 | Aplicación web local | Aceptada |
| ADR-002 | FastAPI como backend | Aceptada |
| ADR-003 | Separación del motor de cálculo | Aceptada |
| ADR-004 | Normativa separada del código | Aceptada |
| ADR-005 | Fechas reales | Aceptada |
| ADR-006 | Historial y proyección separados | Aceptada |
| ADR-007 | GitHub como repositorio principal | Aceptada |
| ADR-008 | Estado temporal del asistente en `sessionStorage` | Aceptada |
| ADR-009 | API como frontera entre interfaz y cálculos | Aceptada |
| ADR-010 | Normalización salarial mediante valor anual común | Aceptada |
| ADR-011 | Proyecciones salariales por escenarios | Aceptada |
| ADR-012 | Proyección anual no sustituye cálculos por fecha exacta | Aceptada |
| ADR-013 | Historial anual separado del salario actual | Aceptada |
| ADR-014 | Línea temporal única con separación entre realidad y proyección | Aceptada |
| ADR-015 | Salario cotizado futuro proporcional a las cuotas proyectadas | Aceptada |
| ADR-016 | Precisión monetaria con `Decimal` y redondeo al materializar | Aceptada |
| ADR-017 | El cierre del año actual precede a la densidad futura | Aceptada |
| ADR-018 | El horizonte salarial debe cubrir el escenario de retiro | Aceptada |
| ADR-019 | Navegación rápida `sticky` sin duplicar lógica de negocio | Aceptada |
| ADR-020 | Clasificar explícitamente cuotas excedentes por edad de referencia | Aceptada |
| ADR-021 | Selección explícita del escenario que alimenta el Paso 6 | Aceptada |
| ADR-022 | Capa de integración entre el asistente y los motores legales | Aceptada |
| ADR-023 | Clasificación automática de modalidad SEBD | Aceptada |
| ADR-024 | Años calendario parciales dentro de los mejores años | Aceptada |
| ADR-025 | Factores anticipados versionados por mes | Aceptada |
| ADR-026 | Indemnización por Vejez como pago único separado | Aceptada |
| ADR-027 | No reconstruir el saldo CAP desde historial anual | Aceptada |
| ADR-028 | Reutilizar clasificación SEBD en el componente BD del Mixto | Aceptada |
| ADR-029 | Frontera operativa del Mixto en 01/03/2032 | Aceptada con discrepancia normativa documentada |
| ADR-030 | La opción del CAP no se decide automáticamente | Aceptada |
| ADR-031 | La garantía de renta vitalicia no incrementa la pensión inicial | Aceptada |
| ADR-032 | El bono de reconocimiento requiere un monto oficial o validado | Aceptada |
| ADR-033 | Pagos únicos y pensiones mensuales permanecen separados | Aceptada |
| ADR-034 | La interfaz Mixto consume el motor integrado y no replica fórmulas | Aceptada |
| ADR-035 | Navegación directa condicionada entre pasos del asistente | Aceptada |
| ADR-036 | Separar saldo SUCGS y garantías | Aceptada |
| ADR-037 | Versionar referencias solidarias y permitir valores vigentes | Aceptada |
| ADR-038 | Prioridad del artículo 195 en el límite exacto de 240 cuotas | Aceptada |
| ADR-039 | Preevaluación conservadora del artículo 197 | Aceptada |
| ADR-040 | Integrar SUCGS al Paso 6 sin duplicar fórmulas | Aceptada |
| ADR-041 | El comparador coordina motores y no recalcula fórmulas | Aceptada |
| ADR-042 | La trazabilidad explica resultados y no recalcula prestaciones | Aceptada |
| ADR-043 | Las fuentes visibles usan nombres humanos y metadatos versionados | Aceptada |
| ADR-044 | Contrato transversal común para el resultado final | Aceptada |
| ADR-045 | Adoptar una identidad de producto independiente | Aceptada |
| ADR-046 | Denominar Asegurado(a) al público de la aplicación | Aceptada |
| ADR-047 | Unificar la escala tipográfica visible | Aceptada |
| ADR-048 | Separar información del Asegurado(a) y documentación interna | Aceptada |
| ADR-049 | Preferencia visual local e independiente de la simulación | Aceptada |
| ADR-050 | Accesibilidad base transversal en la plantilla global | Aceptada |
| ADR-051 | Pie de página compacto como información legal global | Aceptada |
| ADR-052 | Usar tokens semánticos para todos los colores visibles | Aceptada |
| ADR-053 | Tratar Alto contraste como tema oscuro de contraste máximo | Aceptada |
| ADR-054 | Convertir Inicio en una portada orientada al Asegurado(a) | Aceptada |
| ADR-055 | Reservar detalles de implementación para documentación interna | Aceptada |
| ADR-056 | Responsive por contenido y no por reducción indiscriminada | Aceptada |
| ADR-057 | Navegación persistente inferior en móvil | Aceptada |
| ADR-058 | El Paso 5 solicita el último mes acreditado, no una fecha de retiro implícita | Aceptada |
| ADR-059 | Forzar LF para todo archivo de texto del repositorio | Aceptada |
| ADR-060 | Responder temporalmente `/favicon.ico` sin crear un icono ficticio | Aceptada |
| ADR-061 | Mantener respaldos comprimidos fuera de la raíz y limitar `.gitkeep` | Aceptada |
| ADR-062 | Ayuda contextual compacta mediante hover, foco y alternativa táctil | Aceptada |
| ADR-063 | Los estados seleccionados deben usar señales redundantes por tema | Aceptada |
| ADR-064 | Separar validación de campo, alerta urgente y advertencia no urgente | Aceptada |
| ADR-065 | Las mutaciones observadas de accesibilidad deben ser idempotentes | Aceptada |
| ADR-066 | Los errores de campo deben ser visibles y no depender del globo nativo | Aceptada |
| ADR-067 | Mostrar la edad que se cumple durante cada año de la línea temporal | Aceptada |
| ADR-068 | Separar salario visible, cuota acreditada y períodos parciales del año actual | Aceptada; criterio de confirmación manual de Ficha Digital sustituido parcialmente por ADR-103 |
| ADR-069 | La referencia de Mi Retiro Seguro se extrae del PDF personal y no es una constante | Aceptada |
| ADR-070 | La comparación con un comprobante es contextual y puede no ser directa | Aceptada |
| ADR-071 | Toda importación oficial requiere vista previa editable y confirmación explícita | Aceptada |
| ADR-072 | La Ficha Digital se limita al año calendario actual | Aceptada |
| ADR-073 | Separar una fotografía acreditada de la proyección al retiro | Aceptada |
| ADR-074 | Validar PDFs en la frontera HTTP antes del parser | Aceptada |
| ADR-075 | La primera beta exige CI reproducible y vigilancia de dependencias | Aceptada |
| ADR-076 | Dependabot no debe convertir versiones concretas en falsos fallos de CI | Aceptada |
| ADR-077 | Mantener una capa visual transversal separada antes de la beta | Aceptada |
| ADR-078 | Priorizar tareas del Asegurado(a) y simplificar controles globales | Aceptada |
| ADR-079 | Separar captura manual e importación documental en Datos personales | Aceptada |
| ADR-080 | Identificadores personales opcionales y de sesión | Aceptada |
| ADR-081 | La navegación del wizard no debe superponerse al contenido | Superada por ADR-086 durante UX.4.6b R3 |
| ADR-082 | Consentimiento informado y versionado antes de Simular | Aceptada |
| ADR-083 | No mostrar un banner de cookies cuando la aplicación no usa cookies | Aceptada |
| ADR-084 | Descomposición conservadora y revisable del nombre completo | Aceptada |
| ADR-085 | Privacidad por diseño y hardening de la frontera de simulación | Aceptada |
| ADR-086 | Consentimiento con lectura completa y navegación dual del wizard (UX.4.6b R3) | No declarado explícitamente en el registro pre-R4 |
| ADR-087 | El contenido público debe ser pertinente al propósito del producto | Aceptada |
| ADR-088 | Los datos importados se bloquean por campo, no por paso | Sustituida parcialmente por ADR-167: se conserva la procedencia por campo, pero el bloqueo deja de ser obligatorio |
| ADR-089 | El Paso 2 separa información acreditada y supuestos futuros | Aceptada, aplicada y validada en UX.4.6c |
| ADR-090 | La apariencia usa iconografía reconocible sin activos externos | Aceptada, aplicada y validada en UX.4.6c |
| ADR-091 | Los modales de importación son superficies globales del wizard | Aceptada, aplicada y validada en UX.4.6c R2 |
| ADR-092 | Las pistas de captura viven dentro del campo cuando sea posible | Aceptada, aplicada y validada en UX.4.6c R2 |
| ADR-093 | Las ayudas contextuales usan iconografía compacta sin la palabra Info | Aceptada, aplicada y validada en UX.4.6c R2 |
| ADR-094 | Una vista previa documental, filtrada por el paso que la invoca | Aceptada, aplicada y validada en UX.4.6c R3 |
| ADR-095 | El control de ayuda conserva un único círculo visual | Aceptada, aplicada y validada en UX.4.6c R3 |
| ADR-096 | El Paso 3 se valida como una sola unidad funcional | Aceptada para validación UX.4.6d |
| ADR-097 | Un dato histórico desconocido permanece pendiente | Aceptada para validación UX.4.6d |
| ADR-098 | Ficha Digital reutiliza el contrato de revisión documental | Aceptada para validación UX.4.6d |
| ADR-099 | El asistente no necesita paneles que anuncien el siguiente paso | Aceptada para validación UX.4.6d |
| ADR-100 | Paso 3 conserva tres secciones internas y un resumen único | Aceptada para validación UX.4.6d |
| ADR-101 | Ficha Digital no redefine las cuotas acreditadas del Paso 2 | Sustituida parcialmente por ADR-155 en UX.4.6d R23; se conserva como historial de la protección introducida en R2 |
| ADR-102 | El detalle del año actual es opcional y debe explicar cuándo una importación queda inactiva | Aceptada para validación UX.4.6d R2 |
| ADR-103 | Los meses detectados por Ficha Digital fijan la casilla de cuota en la captura principal | Sustituida parcialmente por ADR-167: un mes detectado inicia incluido, pero puede excluirse y reincluirse explícitamente |
| ADR-104 | Las tablas distinguen visualmente procedencia documental y captura manual | Aceptada en su distinción de procedencia; el criterio de solo lectura queda sustituido por ADR-167 |
| ADR-105 | Las casillas importadas deben conservar una marca visual inequívoca | Aceptada en la marca visual; el bloqueo permanente queda sustituido por ADR-167 |
| ADR-106 | Estado seleccionado de casillas documentales independiente del pintado nativo | Sustituida parcialmente por ADR-167: la metadata conserva procedencia, pero la inclusión puede cambiar por decisión explícita |
| ADR-107 | Borrado por paso con invalidación descendente | Aceptada para validación UX.4.6d R6. |
| ADR-108 | Reinicio integral separado de preferencias y consentimiento | Aceptada para validación UX.4.6d R6. |
| ADR-109 | Borrado local integral desde Privacidad | Aceptada para validación UX.4.6d R6. |
| ADR-110 | Nueva versión de términos por controles de conservación y eliminación | Aceptada para validación UX.4.6d R6. |
| ADR-111 | Consulta posterior de términos no modifica el consentimiento | Aceptada para validación UX.4.6d R7. |
| ADR-112 | El estado de una fila editable deriva de sus datos actuales | Aceptada para UX.4.6d R8. |
| ADR-113 | El resumen anual debe ser visible antes de terminar todo el Paso 3 | Aceptada para UX.4.6d R8. |
| ADR-114 | El scroll de tablas y los mensajes de fila no deben introducir ruido visual | Aceptada para UX.4.6d R8. |
| ADR-115 | Seleccionar archivo usa un tratamiento visual global | Aceptada para UX.4.6d R8. |
| ADR-116 | La reactividad tabular se resuelve por delegación de eventos | Aceptada para UX.4.6d R9. |
| ADR-117 | Una tabla corta no dibuja carril vertical | Aceptada para UX.4.6d R9. |
| ADR-118 | Fuentes puede captar consentimiento pendiente y Escape es contextual | Aceptada para UX.4.6d R9. |
| ADR-119 | Los ejemplos de captura son sintéticos y genéricos | Aceptada para UX.4.6d R9. |
| ADR-120 | Todas las tablas usan una superficie visual común | Aceptada para UX.4.6d R10. |
| ADR-121 | Las reglas transversales de tabla se aplican por semántica | Aceptada para UX.4.6d R10. |
| ADR-122 | Claro, Oscuro y Alto contraste comparten geometría tabular | Aceptada para UX.4.6d R10. |
| ADR-123 | El scrollbar tabular forma parte de la geometría de `app-table-shell` | Aceptada para UX.4.6d R11. |
| ADR-124 | Selector de archivo y acción de análisis comparten altura | Aceptada para UX.4.6d R11. |
| ADR-125 | El scrollbar temático es transversal a las superficies desplazables | Aceptada para UX.4.6d R12. |
| ADR-126 | Las tablas usan un radio específico menor que las tarjetas | Aceptada para UX.4.6d R12. |
| ADR-127 | Un filtro sin filas no conserva una tabla vacía | Aceptada para UX.4.6d R12. |
| ADR-128 | El selector nativo de archivo no depende del hover interno | Aceptada para UX.4.6d R13. |
| ADR-129 | El Paso 1 manual usa un único bloque de Información personal | Aceptada para UX.4.6d R14. |
| ADR-130 | Los campos no editables tienen una semántica visual transversal | Aceptada para UX.4.6d R15. |
| ADR-131 | El lenguaje de importación no acopla el producto al formato del archivo | Aceptada para UX.4.6d R15. |
| ADR-132 | Limpiar Paso 2 elimina también los supuestos futuros | Aceptada para UX.4.6d R15. |
| ADR-133 | Paso 3 revalida dependencias recuperables sin navegar hacia atrás | Aceptada para UX.4.6d R16. |
| ADR-134 | La restauración nunca reabre un paso con prerrequisitos inválidos | Aceptada para UX.4.6d R16. |
| ADR-135 | Ficha Digital pertenece al Detalle salarial del año actual | Aceptada para UX.4.6d R16. |
| ADR-136 | Bloqueo documental y valor booleano son estados independientes | Aceptada para UX.4.6d R17. |
| ADR-137 | Cuotas acreditadas y cuotas acumuladas con proyección se muestran separadas | Aceptada para UX.4.6d R17. |
| ADR-138 | Las inconsistencias internas del documento se conservan y se advierten | Aceptada para UX.4.6d R17. |
| ADR-139 | Un dato editado por el usuario deja de etiquetarse como detectado | Aceptada para UX.4.6d R17. |
| ADR-140 | Salario disponible no equivale automáticamente a cuota acreditada | Aceptada para UX.4.6d R17. |
| ADR-141 | La procedencia se modela separada del valor y de su validez | Aceptada para UX.4.6d R18. |
| ADR-142 | El selector nativo de archivos no se restaura tras F5 | Aceptada para UX.4.6d R18. |
| ADR-143 | El nombre del documento es metadata local, no persistencia del archivo | Aceptada para UX.4.6d R18. |
| ADR-144 | El detalle del año actual es la fuente de la fila anual vigente cuando está habilitado | Aceptada para UX.4.6d R19. |
| ADR-145 | Una casilla manual de cuota actual puede actualizar Paso 2 sin navegación regresiva | Aceptada para UX.4.6d R19. |
| ADR-146 | Salario disponible y salario anual acreditado continúan separados | Aceptada para UX.4.6d R19. |
| ADR-147 | La vigencia de Ficha Digital se evalúa por el último período detectado | Sustituida por ADR-149 en UX.4.6d R21; se conserva como historial de R20. |
| ADR-148 | Los resúmenes derivados relevantes deben ser auditables desde el Paso 3 | Aceptada para UX.4.6d R20. |
| ADR-149 | Una Ficha Digital anterior al mes actual siempre requiere revisión | Aceptada para UX.4.6d R21. Sustituye el criterio de tolerancia de ADR-147. |
| ADR-150 | La vigencia documental no confía en el reloj local del cliente | Aceptada para UX.4.6d R21. |
| ADR-151 | La consulta de fecha oficial no transmite información previsional | Aceptada para UX.4.6d R21. |
| ADR-152 | El Paso 3 reconcilia cuotas manuales antes de validar el detalle | Aceptada para UX.4.6d R22. |
| ADR-153 | Ningún bloqueo del Paso 3 puede ser silencioso | Aceptada para UX.4.6d R22. |
| ADR-154 | El resumen del detalle conserva métricas semánticamente distintas | Aceptada para UX.4.6d R22. |
| ADR-155 | Una Ficha Digital confirmada puede ampliar la referencia agregada del año actual | Aceptada para UX.4.6d R23. Sustituye parcialmente ADR-101 para discrepancias documentales al alza. |
| ADR-156 | Una Ficha Digital nunca reduce silenciosamente una referencia superior de Paso 2 | Aceptada para UX.4.6d R23. |
| ADR-157 | VERSION es la fuente canónica de versión de aplicación | vigente. |
| ADR-158 | Reconstrucción histórica sin tags retroactivos | Parcialmente sustituida por ADR-159 para la materialización criptográfica de tags. |
| ADR-159 | Firma SSH obligatoria y materialización controlada de tags históricos | vigente. |
| ADR-160 | Salario futuro conocido conserva precisión decimal en toda la trayectoria | Sustituida parcialmente por ADR-173: se conserva precisión decimal, pero la tasa inferida solo se aplica hasta el año objetivo. |
| ADR-161 | Web Storage usa un namespace único de producto sin compatibilidad pre-beta | Aceptada para UX.4.6e R3. |
| ADR-162 | Los comentarios de runtime son semánticos y no cronológicos | Aceptada para UX.4.6e R4. |
| ADR-163 | La preparación pública separa información útil al usuario de gobierno interno | Aceptada para UX.4.6e R5. |
| ADR-164 | La renumeración vigente no reescribe la historia UX anterior | Aceptada para UX.4.6e R6. |
| ADR-165 | La auditoría transversal es un gate antes de la validación funcional manual | Aceptada para UX.4.6e R7. |
| ADR-166 | El borrado integral invalida también residuos pre-beta y fuerza reconsentimiento | Aceptada para UX.4.6e R8. |
| ADR-167 | Los datos documentales confirmados son editables sin perder la referencia original | Sustituida parcialmente por ADR-171: la edición de datos detectados se concentra en la ventana de revisión; se preservan referencia original y copia de trabajo |
| ADR-168 | La etapa `0.0.N-beta` conduce directamente a la versión oficial `1.0.0.x` con Build independiente | Aceptada para PLAN.1. |
| ADR-169 | Las decisiones explícitas no usan valores predeterminados silenciosos y los valores derivados muestran procedencia automática | Aceptada para UX.4.6f R1. |
| ADR-170 | Todo análisis de adjuntos usa un estado de procesamiento global, accesible y no duplicable | Aceptada para UX.4.6f R1. |
| ADR-171 | Los datos documentales detectados se editan en la ventana de revisión y quedan bloqueados en la vista principal | Aceptada para UX.4.6f R1.1. |
| ADR-172 | La línea temporal del Paso 4 exige coherencia entre historial y cuotas y transporta el salario mensual proyectado | Aceptada para UX.4.6f R2. |
| ADR-173 | El Paso 4 no extrapola silenciosamente un salario futuro conocido y registra el origen del horizonte | Aceptada para UX.4.6f R2. |
| ADR-174 | Paso 5 deriva sugerencias posteriores desde Paso 4 sin convertirlas en decisiones del usuario | Aceptada para UX.4.6g R1 |
| ADR-175 | El retiro anticipado se compara solo por decisión explícita y las fechas transcurridas no son acciones futuras | Aceptada para UX.4.6g R1 |
| ADR-176 | Los campos de fecha usan validación calendárica transversal y ancho compacto | Aceptada para UX.4.6g R1 |
| ADR-177 | Los bloques comparables conservan alineación y densidad visual en escritorio | Aceptada para UX.4.6g R1.4.3 |
| ADR-178 | La guía pública explica parámetros versionados sin convertirse en un segundo motor | Aceptada para UX.4.6i R1–R1.4 |
| ADR-179 | El versionado beta usa un ledger de estados aceptados y no cuenta commits como revisiones | Aceptada; reconciliada post-G070 en AUD.SEC2 R1 |

## 4. Registro íntegro de ADR

## ADR-001 — Aplicación web local

**Estado:** Aceptada

La aplicación se desarrollará inicialmente como una aplicación web ejecutada en localhost.

Esto permitirá utilizar la misma arquitectura posteriormente en un servidor web sin reconstruir el motor de cálculo.

---

## ADR-002 — FastAPI como backend

**Estado:** Aceptada

Se utilizará Python con FastAPI para la lógica del servidor y la exposición de los servicios internos de la aplicación.

---

## ADR-003 — Separación del motor de cálculo

**Estado:** Aceptada

Los cálculos previsionales serán independientes de la interfaz gráfica.

Existirán motores separados para:

- SEBD;
- Subsistema Mixto;
- SUCGS.

---

## ADR-004 — Normativa separada del código

**Estado:** Aceptada

Los parámetros legales que puedan modificarse no deberán quedar dispersos o codificados directamente dentro de los algoritmos.

Se mantendrán archivos de configuración versionados en el directorio `regulations/`.

---

## ADR-005 — Fechas reales

**Estado:** Aceptada

Los cálculos utilizarán fechas completas y no únicamente la diferencia entre años calendario.

Esto es necesario para determinar correctamente:

- edad cumplida;
- fecha de referencia;
- cuotas anteriores a la edad de referencia;
- cuotas posteriores a la edad de referencia.

---

## ADR-006 — Historial y proyección separados

**Estado:** Aceptada

La aplicación diferenciará permanentemente:

- datos históricos reales;
- datos proyectados.

Una proyección futura nunca deberá modificar o reemplazar silenciosamente información histórica.

---

## ADR-007 — GitHub como repositorio principal

**Estado:** Aceptada

GitHub será la fuente principal del proyecto.

Esto permitirá desarrollar indistintamente desde diferentes computadoras utilizando `git pull` y `git push`.
---

## ADR-008 — Estado temporal del asistente en `sessionStorage`

**Estado:** Aceptada

Durante la primera etapa del proyecto, los datos de una simulación en curso se conservarán temporalmente en `sessionStorage`.

Esto permite mantener la información al recargar la pestaña sin guardar automáticamente datos personales en una base de datos. Una futura persistencia permanente deberá ser una acción explícita del Asegurado(a).

---

## ADR-009 — API como frontera entre interfaz y cálculos

**Estado:** Aceptada

La interfaz JavaScript no implementará las fórmulas principales de cuotas, salarios o pensiones.

Los formularios enviarán datos a endpoints de FastAPI y Python será responsable de las validaciones y cálculos de negocio. JavaScript se limitará principalmente a navegación, estado temporal, presentación y comunicación con la API.

---

## ADR-010 — Normalización salarial mediante valor anual común

**Estado:** Aceptada

Los salarios ingresados como semanales, quincenales, mensuales o anuales se normalizan primero a un equivalente anual.

A partir de ese valor se obtienen las demás periodicidades, reduciendo conversiones encadenadas y manteniendo un criterio uniforme.

---

## ADR-011 — Proyecciones salariales por escenarios

**Estado:** Aceptada

El Paso 4 permitirá cuatro modalidades iniciales:

- salario constante;
- porcentaje anual;
- salario futuro conocido;
- comparación de varios porcentajes.

Las proyecciones son datos estimados y permanecerán diferenciadas de los datos salariales históricos.

---

## ADR-012 — Proyección anual no sustituye cálculos por fecha exacta

**Estado:** Aceptada

Las tablas salariales del Paso 4 utilizan años calendario para facilitar la planificación y comparación visual.

Estas tablas no se utilizarán por sí solas para decidir si una cuota o salario ocurrió antes o después de una fecha legal crítica. Los motores de elegibilidad y pensión utilizarán fechas y meses exactos cuando corresponda.
---

## ADR-013 — Historial anual separado del salario actual

**Estado:** Aceptada

El Paso 3 distinguirá explícitamente el historial salarial real de la remuneración actual utilizada para proyectar el futuro.

El historial anual almacenará cuotas y salario cotizado/reportado por año calendario. El salario actual conservará su periodicidad original y se normalizará para las proyecciones. Esta separación evita tratar un año parcial como si fuera un salario anual completo y mantiene trazabilidad entre datos reales y supuestos futuros.

---

## ADR-014 — Línea temporal única con separación entre realidad y proyección

**Estado:** Aceptada

El Paso 4 presentará el historial real una sola vez y separará explícitamente:

- años históricos;
- año actual con componentes real y proyectado;
- años completamente proyectados.

Cuando existan varios escenarios salariales, solo la parte futura se repetirá por escenario. Esto evita duplicar décadas de información histórica y reduce el riesgo de confundir datos reales con estimaciones.

---

## ADR-015 — Salario cotizado futuro proporcional a las cuotas proyectadas

**Estado:** Aceptada

Si un año futuro contiene menos de 12 cuotas proyectadas, el salario cotizado estimado no utilizará el salario anual completo. Se calculará a partir del salario mensual del escenario multiplicado por la cantidad de cuotas/meses proyectados.

Esta equivalencia anual es provisional y será refinada con detalle mensual cuando los motores de elegibilidad y pensión lo requieran.

---

## ADR-016 — Precisión monetaria con `Decimal` y redondeo al materializar

**Estado:** Aceptada

Los cálculos monetarios sensibles utilizarán `Decimal` para evitar artefactos binarios de punto flotante.

El criterio técnico general será conservar precisión durante las operaciones y redondear a centavos con `ROUND_HALF_UP` al materializar un importe. No se redondearán valores intermedios únicamente para forzar coincidencia con otra cifra visible.

Si una norma aplicable establece un método de redondeo distinto, esa regla normativa tendrá prioridad dentro del motor correspondiente.

---

## ADR-017 — El cierre del año actual precede a la densidad futura

**Estado:** Aceptada

La proyección de cuotas del Paso 5 respetará primero `cuotas_esperadas_cierre_anio` del Paso 2.

La densidad `cuotas_esperadas_por_anio` se utilizará para los años futuros y, cuando sea necesario, se prorrateará el año de retiro. Esto evita agregar cuotas en el año actual cuando el Asegurado(a) ya indicó que no espera nuevas acreditaciones antes de cerrarlo.

---

## ADR-018 — El horizonte salarial debe cubrir el escenario de retiro

**Estado:** Aceptada

Un escenario de retiro no se considerará completamente cubierto si su fecha se extiende más allá del último año de la proyección salarial.

La aplicación advertirá la inconsistencia y ofrecerá volver al Paso 4 para extender el horizonte. No se extrapolarán silenciosamente salarios sin confirmación del Asegurado(a).

---

## ADR-019 — Navegación rápida `sticky` sin duplicar lógica de negocio

**Estado:** Aceptada

Los pasos largos del asistente dispondrán de una barra de navegación rápida visible al desplazarse.

La barra delegará sus acciones en los formularios y botones existentes. No contendrá fórmulas ni validaciones previsionales paralelas, evitando duplicar lógica y manteniendo accesibles las acciones Anterior/Continuar/Analizar.

## ADR-020 — Clasificar explícitamente cuotas excedentes por edad de referencia

**Estado:** Aceptada

**Decisión:** el motor SEBD no inferirá silenciosamente, para retiros posteriores a la edad de referencia, qué cuotas excedentes corresponden al incremento de 1.25 % y cuáles al incremento de 2 %.

**Motivo:** la ley asigna porcentajes diferentes según el momento en que fueron aportadas. Cuando el historial anual no ofrece granularidad suficiente, el dato debe ser proporcionado o derivado por una capa con mejor detalle antes de ejecutar el cálculo definitivo.

---

## ADR-021 — Selección explícita del escenario que alimenta el Paso 6

**Estado:** Aceptada

El Paso 5 no enviará implícitamente el primer escenario disponible al cálculo de pensión. La persona debe disponer de una selección visible del escenario futuro que se utilizará en Resultados.

Los escenarios ya transcurridos permanecen visibles para comparación, pero no se seleccionan automáticamente mientras el proyecto solo disponga de historial anual. Reconstruir cuotas exactas en una fecha pasada requiere mayor granularidad.

---

## ADR-022 — Capa de integración entre el asistente y los motores legales

**Estado:** Aceptada

La transformación de historial real, salarios proyectados y cuotas estimadas en una entrada para el motor legal se realizará en Python mediante `app/services/results.py`.

JavaScript enviará el estado validado y presentará la respuesta, pero no decidirá fórmulas legales ni repartirá silenciosamente cuotas excedentes.

Cuando un año futuro solo se utiliza parcialmente hasta la fecha de retiro, el salario proyectado se prorrateará por las cuotas consumidas y se mostrará una advertencia de que se trata de una estimación.


## ADR-023 — Clasificación automática de modalidad SEBD

**Estado:** Aceptada

**Decisión:** el Asegurado(a) selecciona una fecha/escenario de retiro y la aplicación determina automáticamente si corresponde Normal, Anticipada, Proporcional, Proporcional Anticipada, posible Indemnización por Vejez o un escenario no elegible.

**Motivo:** evita que el Asegurado(a) tenga que conocer de antemano la denominación jurídica correcta y reduce inconsistencias entre edad, cuotas y modalidad seleccionada manualmente.

## ADR-024 — Años calendario parciales dentro de los mejores años

**Estado:** Aceptada

**Decisión:** no anualizar un año parcial. Se conserva su total cotizado y puede competir entre los mejores años por su total anual. Cuando se seleccionan diez años, la suma se lleva a promedio mensual sobre 120 meses.

**Motivo:** mantener el tratamiento del procedimiento reglamentario y evitar inventar salarios no cotizados.

## ADR-025 — Factores anticipados versionados por mes

**Estado:** Aceptada

**Decisión:** los factores de reducción de la banda anticipada se almacenan como parámetros normativos y no se interpolan en el motor.

**Motivo:** un factor reglamentario debe reproducirse desde una tabla versionada, no deducirse por aproximación matemática.


## ADR-026 — Indemnización por Vejez como pago único separado

**Estado:** Aceptada

La Indemnización por Vejez no se almacenará ni presentará como `pension_mensual_estimada`. El motor conservará por separado la mensualidad normal hipotética, el divisor reglamentario, el factor `meses cotizados / 6` y el pago único resultante.

El cociente entre meses acreditados y seis se calculará mediante división decimal directa, sin truncarlo a bloques enteros, porque el procedimiento reglamentario ordena dividir el total de meses registrados entre seis y multiplicar el resultado por la mensualidad hipotética.

Desde el 01/03/2036 el clasificador no calculará esta indemnización y derivará el escenario a la transición SUCGS prevista por el artículo 186.


## ADR-027 — No reconstruir el saldo CAP desde historial anual

**Estado:** Aceptada

El Componente de Ahorro Personal del Subsistema Mixto no se estimará acumulando porcentajes sobre el historial anual mientras no exista una regla versionada que permita reproducir la cuenta individual con sus movimientos y rendimientos.

Para calcular la pensión programada se exigirá el saldo ahorrado/capitalizado oficial o validado y el valor actuarial aplicable. Si el parámetro actuarial no está disponible, el motor mostrará el componente como pendiente en lugar de reutilizar factores del SUCGS.

**Motivo:** el CAP depende del saldo efectivo de la cuenta, su capitalización y parámetros actuariales adoptados periódicamente. Reconstruirlo con datos anuales produciría una precisión aparente no auditable.

---

## ADR-028 — Reutilizar clasificación SEBD en el componente BD del Mixto

**Estado:** Aceptada

El Componente de Beneficio Definido del Subsistema Mixto reutilizará el clasificador general de modalidades de retiro por vejez, pero con un historial salarial limitado a la participación propia del Mixto y con el máximo mensual específico del componente.

**Motivo:** las modalidades legales comparten estructura de edad/cuotas, mientras el salario participante y los límites monetarios del Mixto son distintos. Reutilizar el clasificador reduce duplicación sin confundir parámetros.

---

## ADR-029 — Frontera operativa del Mixto en 01/03/2032

**Estado:** Aceptada con discrepancia normativa documentada

Para determinar si un retiro continúa calculándose bajo el Subsistema Mixto, la aplicación utilizará 01/03/2032 como inicio de la transición a SUCGS, conforme al artículo 188 y al Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria.

El artículo 153 del Texto Único contiene una referencia a 01/03/2036 para asegurados del Subsistema Mixto. La aplicación no oculta ni corrige silenciosamente esa diferencia: la conserva en `regulations/mixto.json` y en `docs/regulatory/regulatory-framework.md`.

**Motivo:** la lógica operativa del retiro debe seguir la disposición específica de cálculo y el reglamento aplicable, dejando trazabilidad de la inconsistencia textual para revisión jurídica futura.

---

## ADR-030 — La opción del CAP no se decide automáticamente

**Estado:** Aceptada

Cuando el artículo 187 habilite la devolución total del Componente de Ahorro Personal, el motor no escogerá silenciosamente entre pensión programada y devolución total.

La entrada `opcion_prestacion_cap` admite `AUTO`, `PENSION_PROGRAMADA` y `DEVOLUCION_TOTAL`. En `AUTO`, si ambas vías requieren una decisión del asegurado, el resultado quedará pendiente hasta que exista una selección expresa.

**Motivo:** la devolución es una facultad del asegurado y cambia la naturaleza del resultado entre renta mensual y pago único.

---

## ADR-031 — La garantía de renta vitalicia no incrementa la pensión inicial

**Estado:** Aceptada

La garantía del artículo 184 se modelará como continuidad futura del pago del CAP cuando el pensionado sobreviva la expectativa de vida utilizada y se extingan los fondos de su cuenta.

No se sumará un complemento a la pensión inicial. La salida conservará la pensión CAP programada, la condición de activación y la referencia al Seguro Colectivo de Renta Vitalicia.

**Motivo:** el seguro cubre el agotamiento posterior del capital; no constituye un aumento inicial de la prestación.

---

## ADR-032 — El bono de reconocimiento requiere un monto oficial o validado

**Estado:** Aceptada

La aplicación no reconstruirá automáticamente el bono de reconocimiento del artículo 183 a partir del historial anual. Aceptará un monto ya determinado y registrará si fue confirmado oficialmente.

Un bono mayor que cero que no esté marcado como confirmado permitirá mostrar un resultado provisional, pero impedirá considerar el cálculo Mixto como completo.

**Motivo:** la Ley define el derecho y la naturaleza del bono, pero la aplicación no dispone todavía de granularidad y reglas reglamentarias suficientes para reconstruir su valor individual con garantías de exactitud.

---

## ADR-033 — Pagos únicos y pensiones mensuales permanecen separados

**Estado:** Aceptada

Las indemnizaciones del componente BD y las devoluciones del CAP se almacenarán como pagos únicos independientes de `pension_mensual_total_estimada`.

Cuando ambos pagos únicos procedan, el motor podrá presentar un total de pagos únicos, pero nunca convertirlo en una pensión mensual.

**Motivo:** evita mezclar prestaciones de naturaleza y periodicidad diferentes en la API, la interfaz y futuros informes.

## ADR-034 — La interfaz Mixto consume el motor integrado y no replica fórmulas

**Estado:** Aceptada

El Paso 6 no implementará fórmulas previsionales Mixto en JavaScript. La interfaz recopila los datos explícitos del CAP y los datos ya validados del asistente, y los envía a `POST /api/simulacion/resultados/mixto`.

La clasificación de modalidad, la decisión pendiente, la pensión programada, las devoluciones, las indemnizaciones y la garantía provienen exclusivamente del backend.

**Motivo:** evita divergencia entre la API y la interfaz y conserva una única fuente de verdad para el cálculo legal.

---

## ADR-035 — Navegación directa condicionada entre pasos del asistente

**Estado:** Aceptada

Los indicadores de progreso y la barra persistente permitirán abrir directamente un paso anterior o posterior que siga teniendo satisfechos sus prerrequisitos. Los pasos no disponibles permanecerán deshabilitados hasta que se completen nuevamente los datos dependientes.

El salto directo reutiliza las funciones existentes de preparación de Historial, Proyección, Retiro y Resultados; no duplica validaciones ni reglas de cálculo.

**Motivo:** permite corregir o revisar datos sin presionar repetidamente `Anterior`, pero evita saltar a resultados que hayan quedado inválidos después de modificar información de origen.

## ADR-036 — Separar saldo SUCGS y garantías

**Estado:** Aceptada

**Decisión:** el SUCGS calcula el componente contributivo a partir de un saldo explícito y no reconstruye todavía ese saldo desde el historial anual. La pensión contributiva, la capa solidaria de los artículos 194 y 195 y la pensión total definitiva se mantienen como niveles separados.

**Motivo:** la reconstrucción del saldo depende del origen previsional del asegurado, aportes previos y posteriores a la reforma y rendimientos efectivos del Fondo Único Solidario. Además, el artículo 197 puede elevar el resultado después de la capa solidaria, por lo que no debe confundirse un resultado intermedio con la pensión definitiva.

## ADR-037 — Versionar referencias solidarias y permitir valores vigentes

**Estado:** Aceptada

**Decisión:** B/.144.00 y B/.265.00 se conservan en `regulations/sucgs.json` como referencias legales al 22/05/2025. El motor permite suministrar valores vigentes confirmados y advierte cuando utiliza las referencias base.

**Motivo:** el artículo 194 somete sus prestaciones a indexación y el artículo 195 establece la Pensión Garantizada Solidaria como un monto de al menos B/.265.00. Tratar esos importes como eternamente fijos produciría resultados desactualizados.

## ADR-038 — Prioridad del artículo 195 en el límite exacto de 240 cuotas

**Estado:** Aceptada

**Decisión:** cuando existen exactamente 240 cuotas y se cumple la edad de referencia, el motor aplica la Pensión Garantizada Solidaria del artículo 195 antes de la regla del numeral 2 del artículo 194.

**Motivo:** el numeral 2 del artículo 194 incluye literalmente hasta 240 cuotas, mientras el artículo 195 concede la Pensión Garantizada Solidaria desde 240 cuotas. La aplicación documenta esta superposición y usa el artículo 195 como regla específica de la garantía mínima, sin ocultar la interpretación adoptada.

## ADR-039 — Preevaluación conservadora del artículo 197

**Estado:** Aceptada

**Decisión:** automatizar las condiciones de número anual de cuotas y distribución temporal con historial anual completo; calcular el salario promedio base como salarios cotizados dividido entre meses cotizados; y exigir confirmación explícita para la estabilidad salarial.

**Motivo:** el artículo 197 formula de manera directa las dos primeras condiciones, mientras el numeral 3 contiene una redacción sobre variación del 30 % cuya aplicación operativa no debe ser corregida ni reinterpretada silenciosamente por la aplicación. La propia Ley dispone que la CSS implemente mecanismos de control. Hasta contar con una regla operativa oficial inequívoca, la confirmación de estabilidad permanece separada y auditable.

**Consecuencia:** `pension_mensual_total_estimada` solo se completa cuando la garantía puede determinarse o cuando una condición comprobada demuestra que no aplica.

## ADR-040 — Integrar SUCGS al Paso 6 sin duplicar fórmulas

**Estado:** Aceptada

**Decisión:** la interfaz SUCGS reutilizará los Pasos 1–5 y enviará al backend el historial, la línea temporal y el escenario de retiro seleccionados. JavaScript no implementará la fórmula del artículo 196 ni las garantías de los artículos 194, 195 y 197.

El año inicial usado para distribuir cuotas en el artículo 197 se tomará del inicio del historial declarado en el Paso 3. La confirmación de que ese historial cubre toda la vida laboral relevante permanecerá como una declaración explícita, y la estabilidad salarial conservará un estado pendiente cuando no exista confirmación suficiente.


## ADR-041 — El comparador coordina motores y no recalcula fórmulas

**Estado:** Aceptada

**Decisión:** la comparación transversal de 6F.1 construirá combinaciones de fecha de retiro y escenario salarial y delegará cada cálculo al servicio integrado SEBD, Mixto o SUCGS. La capa transversal solo normaliza resultados y calcula diferencias contra una combinación base.

Para Mixto y SUCGS, cuando se evalúe una fecha alternativa se reutilizarán explícitamente los saldos y parámetros específicos ingresados en el Paso 6 y se mostrará una advertencia de escenario hipotético con saldo constante. No se proyectarán silenciosamente cuentas CAP o de Capitalización Solidaria.

**Motivo:** evita una cuarta implementación de fórmulas previsionales y, al mismo tiempo, impide presentar como proyección actuarial un saldo futuro que la aplicación todavía no puede reconstruir con datos oficiales suficientes.


## ADR-042 — La trazabilidad explica resultados y no recalcula prestaciones

**Estado:** Aceptada

**Decisión:** `Ver cálculo completo` se construye en backend a partir del resultado ya emitido por cada motor. La capa transversal puede presentar datos, reglas, fórmulas, sustituciones, redondeos y fuentes, pero no vuelve a ejecutar ni replica la lógica jurídica del motor.

Los enlaces oficiales provienen de `regulations/*.json`; JavaScript solo renderiza la estructura recibida.

**Motivo:** evita inconsistencias entre la cifra mostrada y su explicación, permite reutilizar una misma estructura en SEBD, Mixto y SUCGS y permite reutilizar la metodología y los futuros informes sin crear una cuarta implementación de las fórmulas previsionales.

## ADR-043 — Las fuentes visibles usan nombres humanos y metadatos versionados

**Estado:** Aceptada

**Decisión:** los identificadores internos como `texto_unico`, `ley_462` o `reglamento_cccs` no se mostrarán literalmente al Asegurado(a). La interfaz resolverá cada identificador contra el catálogo de fuentes recibido del backend y presentará el título humano y, cuando exista, un enlace oficial.

La página `/metodologia` reutiliza las URLs versionadas de `regulations/*.json` y las agrupa por SEBD, Mixto y SUCGS. La capa de presentación puede añadir etiquetas y alcance, pero no sustituye la fuente normativa ni introduce reglas de cálculo.

**Motivo:** los IDs internos son adecuados para integrar servicios, pero no son una referencia jurídica legible. Mantener títulos humanos y enlaces oficiales mejora la auditabilidad sin duplicar URLs ni fórmulas en JavaScript.

## ADR-044 — Contrato transversal común para el resultado final

**Estado:** Aceptada

**Decisión:** los resultados integrados de SEBD, Mixto y SUCGS expondrán un `resumen_unificado` con la misma semántica para estado, naturaleza de la prestación, monto mensual, pago único, modalidad, escenario, datos no confirmados y advertencias.

El resumen transversal se construye después de ejecutar el motor y la trazabilidad. No recalcula importes ni sustituye `calculo`, que continúa siendo el desglose jurídico específico de cada sistema. El comparador debe consumir este contrato común cuando normalice filas.

**Motivo:** evita que la interfaz, el comparador y futuros informes mantengan tres interpretaciones distintas de conceptos equivalentes. También garantiza que una indemnización o devolución no pueda confundirse con una pensión mensual y que los estados pendientes o de transición conserven una interpretación homogénea.

## ADR-045 — Adoptar una identidad de producto independiente

**Estado:** Aceptada

**Decisión:** la aplicación se denomina **Mi Retiro Proyectado** en la interfaz, documentación y metadatos públicos.

**Motivo:** `Mi Retiro Seguro` es el nombre de una herramienta oficial de la CSS. Usar ese nombre con un sufijo como `v2` podría sugerir una versión oficial, sucesora o afiliada. El nombre adoptado mantiene el propósito previsional sin crear esa apariencia.

## ADR-046 — Denominar Asegurado(a) al público de la aplicación

**Estado:** Aceptada

**Decisión:** los textos visibles y la documentación funcional utilizan **Asegurado(a)** en singular y **Asegurados(as)** en plural para referirse a quienes realizan simulaciones.

**Motivo:** alinea la terminología con el dominio de seguridad social y evita usar `usuario` como denominación pública genérica.

## ADR-047 — Unificar la escala tipográfica visible

**Estado:** Aceptada

**Decisión:** párrafos, ayudas, controles, tablas y navegación comparten un tamaño base. Solo encabezados, valores previsionales relevantes y elementos compactos de estado pueden apartarse de esa escala.

**Motivo:** reduce variaciones arbitrarias de tamaño, mejora consistencia y conserva énfasis para montos y resultados que requieren atención.

## ADR-048 — Separar información del Asegurado(a) y documentación interna

**Estado:** Aceptada

**Decisión:** la interfaz no muestra nombres de subfases, rutas del repositorio, ADR, archivos `docs/*.md` ni identificadores técnicos. Esos elementos permanecen en la documentación de desarrollo.

**Motivo:** el Asegurado(a) necesita metodología, fuentes y resultados, no detalles de organización interna del proyecto.

## ADR-049 — Preferencia visual local e independiente de la simulación

**Estado:** Aceptada

**Decisión:** la aplicación ofrece los modos **Seguir sistema**, **Claro**, **Oscuro** y **Alto contraste**. La preferencia se conserva en `localStorage` con una clave propia y no forma parte del objeto previsional ni del estado de cálculo almacenado en `sessionStorage`.

**Motivo:** la apariencia es una preferencia del navegador, no un dato de la prestación. Separarla evita contaminar simulaciones y permite respetar la configuración del sistema operativo cuando el Asegurado(a) así lo elige.

## ADR-050 — Accesibilidad base transversal en la plantilla global

**Estado:** Aceptada

**Decisión:** la plantilla global incorpora enlace de salto al contenido, `aria-current` para navegación activa, foco visible, objetivos táctiles principales de al menos 44 px y respeto a `prefers-reduced-motion`. Las mejoras se aplican de forma transversal y no se duplican en cada pantalla.

**Motivo:** estas medidas reducen barreras de teclado, movilidad y sensibilidad al movimiento y constituyen una base verificable para la revisión WCAG 2.2 posterior.

## ADR-051 — Pie de página compacto como información legal global

**Estado:** Aceptada

**Decisión:** el pie de página utiliza dos líneas compactas: la primera concentra nombre, copyright, autor y reserva de derechos; la segunda concentra el aviso de independencia y el acceso a Mi Caja Digital. Se evita presentarlo como una tarjeta o bloque separado.

**Motivo:** el contenido legal debe estar siempre disponible sin competir visualmente con los resultados previsionales ni aumentar innecesariamente la altura de cada página.

## ADR-052 — Usar tokens semánticos para todos los colores visibles

**Estado:** Aceptada

**Decisión:** los componentes visibles deben consumir tokens semánticos de superficie, texto, borde, información, éxito, advertencia, neutral y selección. Los colores literales quedan limitados a la definición central de cada tema y no deben introducirse directamente en tarjetas, estados o alertas nuevas.

**Motivo:** evita que un componente diseñado para Claro conserve fondos o textos de bajo contraste al cambiar a Oscuro o Alto contraste y permite mantener una jerarquía cromática consistente en toda la aplicación.

## ADR-053 — Tratar Alto contraste como tema oscuro de contraste máximo

**Estado:** Aceptada

**Decisión:** Alto contraste utiliza fondo negro, texto blanco, bordes visibles y foco amarillo, con acciones primarias claramente diferenciadas. No se implementa como una variante clara con bordes más fuertes.

**Motivo:** un modo de alto contraste debe reducir ambigüedad visual y depender también de bordes y forma, no solamente de cambios de color sobre superficies claras.

## ADR-054 — Convertir Inicio en una portada orientada al Asegurado(a)

**Estado:** Aceptada

**Decisión:** la página de Inicio prioriza propósito, acción principal, sistemas cubiertos, capacidades, proceso de seis pasos y aviso breve de independencia. Se eliminan composiciones de maqueta que no ayudan a decidir qué hacer a continuación.

**Motivo:** la portada debe explicar en pocos segundos qué hace Mi Retiro Proyectado y cómo comenzar, sin exponer terminología de desarrollo ni competir con las pantallas de cálculo.

## ADR-055 — Reservar detalles de implementación para documentación interna

**Estado:** Aceptada

**Decisión:** expresiones sobre metadatos, rutas `regulations/*.json`, backend, endpoints, estructura del repositorio y mecanismos internos de carga no deben mostrarse al Asegurado(a). Cuando sea útil explicar una fuente, se presenta únicamente su nombre humano, alcance y enlace oficial.

**Motivo:** la trazabilidad jurídica es contenido del producto; el mecanismo técnico con el que se obtiene esa trazabilidad pertenece a mantenimiento y desarrollo.

## ADR-056 — Responsive por contenido y no por reducción indiscriminada

**Estado:** Aceptada

**Decisión:** UX.3 utiliza los breakpoints de Bootstrap como referencia, pero cada componente define su adaptación según su contenido. Las tablas extensas conservan un ancho mínimo legible y se desplazan dentro de su propio contenedor; las tarjetas, formularios y acciones sí se reorganizan en una sola columna cuando el ancho disponible lo requiere.

**Motivo:** comprimir todas las columnas hasta que entren en una pantalla móvil degrada la lectura y puede ocultar la relación entre datos. El desplazamiento localizado conserva la estructura de tablas previsionales sin provocar desbordamiento horizontal de toda la página.

## ADR-057 — Navegación persistente inferior en móvil

**Estado:** Aceptada

**Decisión:** en anchos menores de 768 px la navegación persistente del asistente se fija en la parte inferior, respeta las áreas seguras del dispositivo y mantiene la acción principal, retroceso y selector de paso. El progreso de seis pasos permanece arriba como una franja horizontal desplazable.

**Motivo:** una barra superior persistente consume demasiado espacio vertical en móvil y compite con encabezados y formularios. La barra inferior mantiene las acciones al alcance del pulgar sin eliminar la navegación directa entre pasos.

## ADR-058 — El Paso 5 solicita el último mes acreditado, no una fecha de retiro implícita

**Estado:** Aceptada

**Decisión:** la interfaz del Paso 5 separa tres conceptos: fecha de evaluación, último mes con cuotas acreditadas y fechas de retiro. El Asegurado(a) selecciona el último mes acreditado mediante un control mensual `YYYY-MM`. El servicio deriva la fecha técnica de corte al último día de ese mes; si el mes coincide con el de evaluación, la fecha se limita al propio día de evaluación. La fecha exacta anterior se conserva como campo de compatibilidad.

Los botones de la sección **Recursos oficiales para verificar información individual** conservan el texto **Abrir recurso oficial**, porque Mi Caja Digital es un recurso de consulta personal y no una fuente normativa utilizada por el motor. Su alineación visual sí se unifica con los demás botones de Metodología.

**Motivo:** preguntar por una fecha exacta de actualización podía confundirse con la fecha prevista de retiro y sugería una precisión diaria que el historial principal no posee. Trabajar con el último mes acreditado corresponde mejor a la granularidad disponible y mantiene clara la diferencia entre dato real, fecha de evaluación y escenario futuro.

## ADR-059 — Forzar LF para todo archivo de texto del repositorio

**Estado:** Aceptada

**Decisión:** `.gitattributes` utiliza `* text=auto eol=lf` como regla transversal. Los formatos binarios continúan marcados como `binary`. Cuando cambien estas reglas se ejecutará `git add --renormalize .` y se revisará el diff antes del commit.

**Motivo:** en Windows, `core.autocrlf` puede convertir a CRLF archivos de texto sin extensión que antes solo heredaban `text=auto`, como `.gitignore`. Forzar LF desde el repositorio elimina advertencias de conversión, evita diffs exclusivos por plataforma y mantiene coherencia con `.editorconfig`.

## ADR-060 — Responder temporalmente `/favicon.ico` sin crear un icono ficticio

**Estado:** Aceptada

**Decisión:** mientras los iconos definitivos no estén integrados, FastAPI responderá `204 No Content` a `/favicon.ico`, fuera del esquema OpenAPI y con `Cache-Control: no-store`. La ruta temporal se retirará cuando exista el favicon oficial y `base.html` lo declare explícitamente.

**Motivo:** los navegadores solicitan `/favicon.ico` de forma automática. Devolver `204` elimina el `404` de desarrollo sin versionar un recurso gráfico provisional ni favorecer que el navegador almacene permanentemente la ausencia de icono.

## ADR-061 — Mantener respaldos comprimidos fuera de la raíz y limitar `.gitkeep`

**Estado:** Aceptada

**Decisión:** los paquetes comprimidos de revisiones, entregas y respaldos históricos se conservarán fuera de la raíz del repositorio. Git y GitHub continúan siendo la historia principal del código versionado. Los archivos `.gitkeep` se utilizarán únicamente para directorios vacíos que necesiten existir en Git y se eliminarán cuando esas carpetas contengan archivos versionados reales.

No se reorganizarán rutas funcionales del proyecto únicamente por estética. Si una reorganización futura aporta un beneficio técnico suficiente, deberá modificar en la misma unidad de trabajo todos los imports, rutas, pruebas y documentos que dependan de la estructura anterior.

**Motivo:** separar respaldos locales de la copia de trabajo reduce ruido, evita incluir artefactos históricos en búsquedas o paquetes y mantiene el árbol del repositorio representativo del producto actual. Limitar `.gitkeep` evita archivos sin función una vez que el directorio ya está materializado por contenido real.

## ADR-062 — Ayuda contextual compacta mediante hover, foco y alternativa táctil

**Estado:** Aceptada

**Decisión:** las ayudas breves asociadas a campos previsionales se presentan como tooltips compactos anclados a un indicador `?`. En equipos con puntero la información aparece al pasar sobre el indicador y en navegación por teclado aparece al recibir foco. El clic se conserva como alternativa para dispositivos táctiles y `Esc` puede cerrar ayudas abiertas.

El indicador continúa siendo un control enfocable para que la información no dependa exclusivamente del ratón. El tooltip reutiliza tokens visuales de la aplicación y no incorpora reglas previsionales propias.

**Motivo:** el patrón reduce el tamaño visual del indicador de ayuda y evita obligar a hacer clic en PC, sin perder acceso mediante teclado o interacción táctil. Mantener el contenido fuera de la lógica de negocio preserva la separación entre explicación contextual y cálculo previsional.

## ADR-063 — Los estados seleccionados deben usar señales redundantes por tema

**Estado:** Aceptada

**Decisión:** los estados activos o seleccionados que condicionan una acción posterior no dependerán de una única diferencia de color. En el wizard, el paso activo debe mantener contraste suficiente entre número y círculo. En la tabla de escenarios de retiro, la selección utiliza conjuntamente fondo, contorno, realce del radio y badge de estado, con tokens específicos para Claro, Oscuro y Alto contraste.

Cuando el sistema operativo fuerce colores, la selección debe delegar en los colores de resaltado del sistema en lugar de conservar una paleta propia que pueda perder contraste. El foco de teclado sobre el radio debe permitir localizar también la fila asociada.

**Motivo:** una selección previsional puede determinar el escenario utilizado por el Paso 6. Hacerla perceptible mediante varias señales reduce ambigüedad visual, mejora orientación con teclado y evita que una combinación de tema o contraste convierta una decisión importante en un cambio cromático demasiado sutil.

## ADR-064 — Separar validación de campo, alerta urgente y advertencia no urgente

**Estado:** Aceptada

**Decisión:** la interfaz distinguirá tres canales de retroalimentación accesible. Un error de validación nativa se asocia directamente con su control mediante `aria-invalid` y `aria-errormessage`; un error dinámico de operación usa `role="alert"`, se vuelve enfocable programáticamente al aparecer y no añade una segunda región `aria-live="assertive"`; una advertencia no urgente puede usar `role="status"` con prioridad `polite`.

La asociación de error de campo debe retirarse cuando el valor vuelve a ser válido o el formulario se reinicia. El foco automático de una alerta dinámica no debe desplazar al Asegurado(a) si ya está corrigiendo un control marcado como inválido.

**Motivo:** separar estos canales evita anuncios duplicados, reduce ruido para tecnologías de apoyo y conserva una relación clara entre el problema, el control que debe corregirse y los mensajes generales emitidos por una operación.


## ADR-065 — Las mutaciones observadas de accesibilidad deben ser idempotentes

**Estado:** Aceptada

**Decisión:** cualquier función invocada desde el `MutationObserver` global de accesibilidad debe evitar escrituras redundantes sobre los atributos que el propio observador vigila. Antes de añadir una clase se comprobará que no exista y antes de retirarla se comprobará que esté presente. Para consultar validez durante `input` o `change` se utilizará `ValidityState.valid` cuando no se quiera emitir de nuevo el evento `invalid`.

**Motivo:** escribir repetidamente una clase observada puede generar una cadena de notificaciones del `MutationObserver`, saturar el hilo principal y dejar la interfaz cargando sin responder aunque FastAPI siga devolviendo HTTP 200. Asimismo, `checkValidity()` puede volver a emitir `invalid` y provocar retroalimentación innecesaria durante la corrección de un campo.


## ADR-066 — Los errores de campo deben ser visibles y no depender del globo nativo

**Estado:** Aceptada

**Decisión:** cuando un control falle la validación, la interfaz mostrará un mensaje inline visible junto al campo y lo asociará programáticamente mediante `aria-errormessage`. El manejador `invalid` suprimirá únicamente la presentación nativa del navegador mediante `preventDefault()`; la restricción de validación y el bloqueo de avance permanecen activos.

**Motivo:** los globos nativos no se presentan de forma uniforme entre navegadores, tipos de control ni plataformas. Un borde rojo sin texto tampoco comunica por sí solo la causa del problema. El mensaje propio mantiene consistencia visual, accesibilidad, trazabilidad y permite validar el comportamiento de manera automatizada.


## ADR-067 — Mostrar la edad que se cumple durante cada año de la línea temporal

**Estado:** Aceptada

**Decisión:** el Paso 4 mostrará una columna **Edad** inmediatamente después de **Año** tanto en Historial salarial real como en Proyección futura. La edad se calculará exclusivamente para presentación como `año calendario - año de nacimiento`. Si la fecha de nacimiento no está disponible o no puede interpretarse, se mostrará una raya.

La edad no se incorporará al contrato de los motores ni se persistirá como un dato independiente, porque puede derivarse de la fecha de nacimiento ya capturada.

**Motivo:** los comprobantes oficiales utilizados como referencia presentan Año y Edad de forma conjunta. Mostrar ambos valores facilita contrastar la simulación con el historial de la CSS y evita que el Asegurado(a) tenga que calcular manualmente su edad para cada período. Mantenerla como dato derivado evita duplicidad y riesgo de inconsistencias.


## ADR-068 — Separar salario visible, cuota acreditada y períodos parciales del año actual

**Estado:** Aceptada; criterio de confirmación manual de Ficha Digital sustituido parcialmente por ADR-103

**Decisión:** el detalle reciente del año actual se modelará separando el salario disponible en la Ficha Digital del estado de acreditación de la cuota. Un mes puede estar **completo**, **parcial** o **sin información**, y puede disponer de salario aunque su cuota todavía no aparezca acreditada. La captura puede hacerse como total mensual o como primera/segunda quincena.

Cuando la cantidad de meses marcados con cuota acreditada coincide con `cuotas_anio_actual` del Paso 2, la suma salarial de esos meses puede sincronizar la fila anual del año actual y el último mes acreditado puede derivarse para el Paso 5. Si no coincide, el sistema muestra la discrepancia y no inventa el mes faltante.

La base de proyección futura permanece conceptualmente separada del salario acreditado. El Asegurado(a) puede usar ingreso manual o una base derivada únicamente de meses completos: último mes completo, promedio de meses completos del año actual o promedio de los últimos tres meses completos.

La interfaz ofrece acceso a Mi Caja Digital y, cuando el documento PDF contiene texto estructurado reconocible, permite analizar la Ficha Digital. El parser nunca aplica datos directamente: la información detectada pasa primero por una vista previa editable y requiere confirmación explícita.

**Motivo:** la información salarial y la acreditación de cuotas pueden actualizarse en momentos distintos; además, una consulta puede capturar solo una quincena de un mes. Mezclar estos estados como si fueran un único dato anual puede alterar el corte real y la base utilizada para proyección.


## ADR-069 — La referencia de Mi Retiro Seguro se extrae del PDF personal y no es una constante

**Estado:** Aceptada

**Decisión:** el Asegurado(a) puede cargar opcionalmente un comprobante PDF digital de Mi Retiro Seguro. El backend procesa el archivo únicamente en memoria con `pypdf`, valida que corresponda al formato esperado y extrae solo datos operativos para comparación: fecha del comprobante, sistema elegido, edad de retiro, cuotas históricas, naturaleza y monto estimado de la prestación y filas anuales reconocibles. El contrato continúa excluyendo el código único del documento. Desde UX.4.6b puede devolver identificadores opcionales cuando están etiquetados de forma inequívoca y el Asegurado(a) los revisa antes de importarlos.

Ningún monto procedente de los comprobantes usados durante el desarrollo puede quedar hardcodeado en código de producción. El PDF original no se persiste. El análisis por sí solo no modifica la simulación; después de una confirmación explícita, los datos detectados pueden utilizarse para prellenar campos, mientras la referencia personal continúa separada de los motores y de la normativa versionada.

**Motivo:** cada comprobante representa una fotografía personal y temporal distinta. Tratar un caso de validación como valor universal produciría comparaciones falsas y mezclaría evidencia individual con reglas generales.

## ADR-070 — La comparación con un comprobante es contextual y puede no ser directa

**Estado:** Aceptada

**Decisión:** el Paso 6 mostrará la referencia importada y la proyección actual como cifras separadas. La diferencia se calculará únicamente cuando coincidan la persona según los datos mínimos disponibles, el sistema, la edad de retiro y la naturaleza económica de la prestación. Si alguno de esos elementos no es compatible, ambas referencias pueden mostrarse, pero la interfaz debe indicar que no existe una comparación directa.

La fecha de corte, cuotas y supuestos salariales pueden diferir entre el comprobante y la simulación actual; por ello una diferencia válida se interpreta como variación entre fotografías, no como prueba automática de error de una de ellas.

**Motivo:** una referencia personal puede haber sido calculada con información acreditada o supuestos distintos a los actuales. Separar contexto y compatibilidad evita presentar diferencias engañosas.


## ADR-071 — Toda importación oficial requiere vista previa editable y confirmación explícita

**Estado:** Aceptada

**Decisión:** los documentos oficiales se analizan en el Paso 1, pero su detección no escribe inmediatamente sobre la simulación. Tanto el comprobante de Mi Retiro Seguro como la Ficha Digital deben abrir una vista previa modal donde el Asegurado(a) pueda revisar y corregir los campos detectados antes de confirmar. Cancelar la vista previa no modifica datos existentes.

El comprobante puede prellenar datos personales, sistema, cuotas y filas anuales seleccionadas. Las filas clasificadas como proyectadas no se importan como historial real por defecto; las filas mixtas requieren decisión explícita. La Ficha Digital puede prellenar salarios mensuales del año actual. Desde UX.4.6d R3, los meses efectivamente detectados se consideran registros documentales confirmados y su casilla de cuota queda marcada/bloqueada; los meses no detectados continúan bajo captura manual. Los registros de años anteriores se descartan en esta importación: la Ficha Digital se usa únicamente para el detalle salarial del año calendario actual.

Los archivos se procesan en memoria. Los contratos del backend limitan los identificadores directos a los campos opcionales que UX.4.6b permite revisar y confirmar para la sesión actual; no se persiste el documento ni su código único. Los valores confirmados conservan trazabilidad de origen en `sessionStorage`, pero el documento original no se persiste.

**Motivo:** los documentos pueden contener valores parciales, proyectados o actualizados en momentos distintos. Prellenar sin revisión podría convertir una detección imperfecta en un dato operativo y alterar el cálculo. La confirmación explícita mantiene al Asegurado(a) en control y permite corregir errores del parser sin renunciar a la automatización.


## ADR-072 — La Ficha Digital se limita al año calendario actual

**Estado:** Aceptada

**Decisión:** la importación de Ficha Digital debe extraer, mostrar y conservar únicamente los salarios cuyo año coincida con el año calendario actual de ejecución. Los meses de años anteriores presentes en la sección “Salarios del último año” no se utilizan como contexto ni se persisten en la simulación.

Las vistas previas monetarias deben utilizar el mismo formato público del resto de la aplicación: coma como separador de miles y dos decimales, manteniendo edición segura mediante la utilidad común `currency.js`.

**Motivo:** el objetivo de la Ficha Digital dentro de UX.4.4 es completar el detalle reciente del año actual y separar salario disponible, cuota acreditada y períodos parciales. Conservar meses del año anterior añadía información que no alimentaba ninguna decisión posterior y aumentaba el riesgo de confusión. Un formato monetario uniforme reduce errores de revisión antes de confirmar la importación.


## ADR-073 — Separar una fotografía acreditada de la proyección al retiro

**Estado:** Aceptada

**Decisión:** el Paso 6 ofrecerá, para la misma fecha de retiro seleccionada, dos lecturas calculadas por los mismos motores jurídicos. `PROYECTADO` conserva el comportamiento habitual e incorpora las cuotas y salarios futuros del escenario. `SOLO_ACREDITADO` usa el total de cuotas actualmente acreditadas y el historial salarial real disponible, sin consumir períodos proyectados.

La comparación existe aunque el Asegurado(a) no cargue un comprobante de Mi Retiro Seguro. Cuando sí exista una referencia PDF compatible, la aplicación preferirá comparar esa referencia con la fotografía acreditada propia antes que con la proyección futura.

En Mixto y SUCGS los datos específicos del Paso 6 que la aplicación no puede proyectar de forma fiable —por ejemplo, saldos acumulados— se mantienen iguales en ambas fotografías y esta limitación se comunica expresamente.

**Motivo:** mezclar salarios/cuotas ya acreditados con períodos futuros impedía distinguir una referencia basada en la fotografía actual de una estimación que supone continuidad laboral. Separar ambas lecturas mejora transparencia sin duplicar fórmulas legales ni convertir un PDF personal en una regla general.


## ADR-074 — Validar PDFs en la frontera HTTP antes del parser

**Estado:** Aceptada

**Decisión:** los endpoints que reciben documentos personales reutilizarán una única validación de archivo antes de invocar `pypdf`. Se exige extensión `.pdf`, MIME compatible o genérico aceptado, archivo no vacío, límite de tamaño y presencia de la firma `%PDF-` dentro del primer KiB. El archivo se cierra siempre y permanece en memoria. Los parsers mantienen límites adicionales de páginas y texto extraído.

Las respuestas de importación se marcan `Cache-Control: no-store` y la aplicación añade cabeceras defensivas de navegador que no alteran los motores.

**Motivo:** validar únicamente el nombre o el MIME permite que contenido ajeno alcance un parser complejo. Centralizar la frontera evita reglas divergentes entre importadores, reduce superficie de error y protege mejor documentos personales sin añadir persistencia.

## ADR-075 — La primera beta exige CI reproducible y vigilancia de dependencias

**Estado:** Aceptada

**Decisión:** `main` y los pull requests se validarán con GitHub Actions sobre Python 3.13 y 3.14, con instalación desde `requirements.txt`, `pip check`, `compileall`, `node --check` y `unittest`. El token del workflow mantendrá `contents: read`. Dependabot revisará semanalmente `pip` y GitHub Actions.

**Motivo:** las pruebas locales no detectan por sí solas una instalación limpia rota, incompatibilidades entre versiones de Python o cambios de dependencias. Automatizar el mismo contrato antes de la beta reduce el riesgo de publicar un paquete que solo funciona en la máquina de desarrollo.


## ADR-076 — Dependabot no debe convertir versiones concretas en falsos fallos de CI

**Estado:** Aceptada

**Decisión:** las regresiones que inspeccionan `.github/workflows/ci.yml` validarán que existan `actions/checkout`, `actions/setup-python` y `actions/setup-node` con una versión mayor explícita, además del contrato funcional del pipeline, pero no exigirán que dichas Actions permanezcan para siempre en un major específico. De forma equivalente, la regresión de `pypdf` comprobará que exista una única versión exacta con formato `X.Y.Z`, mientras los tests funcionales de importación determinan si una versión nueva es compatible.

`requirements.txt` se mantiene completamente fijado como snapshot reproducible, pero documenta sus dependencias directas. Dependabot solo propone actualizaciones ordinarias para `fastapi`, `Jinja2`, `pydantic`, `python-multipart`, `pypdf` y `uvicorn`; las dependencias transitivas fijadas no generan ruido de actualización individual. Las actualizaciones minor/patch del runtime, salvo `pypdf`, se agrupan; GitHub Actions se agrupa en una sola propuesta. `pypdf` y las actualizaciones major permanecen fuera del grupo general para revisión específica. No se habilita auto-merge.

**Motivo:** la primera ejecución de Dependabot demostró dos clases de falsos negativos: una Action actualizada podía completar correctamente instalación, compilación y validación de JavaScript pero fallar porque una prueba exigía literalmente `@v6`; y `pypdf` podía superar los tests del parser pero fallar porque una regresión esperaba exactamente `5.9.0`. Al mismo tiempo, proponer por separado paquetes transitivos fijados, como `pydantic_core`, puede crear combinaciones incompatibles con su dependencia principal. La estrategia nueva conserva reproducibilidad, reduce ruido y hace que CI mida compatibilidad real en vez de números históricos.

## ADR-077 — Mantener una capa visual transversal separada antes de la beta

**Estado:** Aceptada

**Decisión:** UX.4.6a incorpora `app/static/css/design-system.css` como capa explícita de presentación cargada después de `style.css` y antes de `accessibility.css`. `style.css` conserva la base histórica, reglas funcionales y responsive ya estabilizadas; `design-system.css` concentra los tokens y acabados visuales modernos; `accessibility.css` mantiene la última precedencia para ayudas, foco y estados accesibles.

La modernización visual no puede cambiar IDs consumidos por JavaScript, contratos de formularios, rutas, persistencia ni fórmulas previsionales. Una consolidación futura de CSS solo se hará después de estabilizar la beta y deberá conservar las regresiones existentes.

**Motivo:** separar la nueva presentación reduce el riesgo de una reescritura masiva del CSS histórico inmediatamente antes de la beta, permite aislar regresiones visuales y mantiene clara la frontera entre cálculo, comportamiento y apariencia.


## ADR-078 — Priorizar tareas del Asegurado(a) y simplificar controles globales

**Estado:** Aceptada

**Decisión:** la navegación pública utilizará etiquetas breves —**Inicio, Simular, Escenarios y Fuentes**— sin cambiar las rutas internas. El control de apariencia mostrará **Automático, Claro y Oscuro** como opciones principales y conservará **Alto contraste** dentro de una sección secundaria de Accesibilidad.

La página de Inicio debe comunicar beneficios y tareas del Asegurado(a) antes que detalles de implementación. Cualquier mockup de resultado utilizado como recurso visual no mostrará una cifra monetaria ficticia que pueda interpretarse como estimación real.

El footer global se presentará centrado con nombre, versión, aviso de independencia, enlace a Fuentes oficiales, autoría y copyright. Mi Caja Digital no se duplicará en el footer; permanecerá en los puntos funcionales destinados a verificar información individual.

**Motivo:** reducir terminología y controles globales visibles mejora jerarquía sin perder funcionalidad. Separar recursos normativos de recursos personales evita que el footer se convierta en un contenedor de acciones operativas y mantiene la portada enfocada en orientar al Asegurado(a).


## ADR-079 — Separar captura manual e importación documental en Datos personales

**Estado:** Aceptada

**Decisión:** el Paso 1 presenta dos modalidades excluyentes: captura manual e importación desde un comprobante de Mi Retiro Seguro. La captura manual es predeterminada. La Ficha Digital se traslada al Paso 3 porque sus datos describen salarios del año actual, no identidad personal.

**Motivo:** mostrar simultáneamente formularios manuales y dos importadores sobrecargaba el primer paso y mezclaba dominios distintos. Separar intención antes de capturar datos reduce ruido y evita que la Ficha Digital se interprete como fuente de identidad.

## ADR-080 — Identificadores personales opcionales y de sesión

**Estado:** Aceptada

**Decisión:** nombres, apellidos, cédula y número de Seguro Social pueden capturarse manualmente o devolverse desde Mi Retiro Seguro cuando el PDF los etiqueta de forma inequívoca. Son opcionales para el cálculo, permanecen en `sessionStorage` durante la simulación actual y no se escriben en archivos, base de datos, logs, fixtures ni documentación. El código único del documento continúa excluido.

Si el PDF ofrece un nombre completo, el parser puede descomponerlo de forma conservadora y siempre revisable. Los campos explícitamente etiquetados tienen prioridad. En nombres femeninos, un patrón final `de Apellido` se interpreta como apellido de casada cuando está presente; cualquier resultado puede corregirse antes de importar.

**Motivo:** estos datos pueden ser útiles para identificar una simulación o un futuro informe, pero no justifican persistencia permanente. Una descomposición conservadora reduce captura manual sin convertir el parser en fuente definitiva de identidad, porque la vista previa sigue siendo obligatoria y editable solo por decisión del Asegurado(a).

## ADR-081 — La navegación del wizard no debe superponerse al contenido

**Estado:** Superada por ADR-086 durante UX.4.6b R3

**Decisión:** la barra común de los Pasos 1–6 conserva su lógica de retroceso, salto directo, estado y acción principal, pero deja de usar posicionamiento `sticky/fixed`. Se renderiza después del contenido activo.

**Motivo:** la persistencia flotante cumplía una decisión UX anterior, pero en formularios largos ocultaba información y competía con el contenido. Mantener un único componente estático conserva consistencia sin sacrificar legibilidad.


## ADR-082 — Consentimiento informado y versionado antes de Simular

**Estado:** Aceptada

**Decisión:** antes de permitir captura manual o importación documental, `/simulacion` debe presentar información clara sobre datos tratados, finalidades, almacenamiento temporal, derechos, contacto y ausencia actual de cookies/rastreadores. La aceptación se versiona en `localStorage` sin copiar la simulación y requiere además una marca de sesión en `sessionStorage`, por lo que una nueva pestaña/sesión vuelve a presentar las condiciones. Rechazar elimina el estado temporal de la simulación y devuelve a Inicio. Un cambio material de la política incrementará la versión y solicitará aceptación nuevamente.

**Motivo:** cédula, NSS, salarios e historial son datos personales y económicos que requieren transparencia y control previo. Un consentimiento trazable y versionado evita que la captura preceda a la información sobre su finalidad.

## ADR-083 — No mostrar un banner de cookies cuando la aplicación no usa cookies

**Estado:** Aceptada

**Decisión:** la versión actual no mostrará un banner independiente de cookies porque no crea cookies, no integra analítica, publicidad ni rastreadores. La política sí informará el uso de `sessionStorage` para la simulación y `localStorage` para apariencia y consentimiento. Si se añaden cookies no esenciales, analítica o telemetría, se diseñará consentimiento granular previo y se actualizará la política.

**Motivo:** equiparar Web Storage con cookies sería técnicamente impreciso y podría inducir al usuario a creer que existe un seguimiento que la aplicación no realiza.

## ADR-084 — Descomposición conservadora y revisable del nombre completo

**Estado:** Aceptada

**Decisión:** Mi Retiro Seguro puede descomponer un nombre completo cuando la estructura sea suficientemente reconocible. Para cuatro o más componentes, conserva el primer token como primer nombre, los dos últimos como apellidos y el bloque intermedio como segundo nombre; para nombres femeninos, un sufijo final `de Apellido` se extrae como apellido de casada. Los campos explícitamente etiquetados por el documento siempre prevalecen y la importación no se aplica sin revisión previa.

**Motivo:** los comprobantes reales pueden ofrecer un nombre completo sin campos separados. La heurística limitada reduce trabajo manual, pero la revisión obligatoria evita tratar una inferencia de presentación como dato oficial incuestionable.

## ADR-085 — Privacidad por diseño y hardening de la frontera de simulación

**Estado:** Aceptada

**Decisión:** toda respuesta bajo `/api/simulacion/` debe declarar `Cache-Control: no-store`; la aplicación mantiene CSP, políticas de referrer/permisos, protección contra framing y `nosniff`. Bootstrap servido temporalmente por jsDelivr usa SRI y deberá evaluarse para localización antes de beta pública. La política de privacidad y la matriz de cumplimiento forman parte del contrato documental de cualquier cambio que agregue datos, almacenamiento, exportaciones, analítica o terceros.

**Motivo:** el flujo ya maneja identificadores, salarios y documentos personales. Las medidas deben proteger el conjunto de la simulación y no solamente los endpoints de PDF.


## ADR-086 — Consentimiento con lectura completa y navegación dual del wizard (UX.4.6b R3)

- El aviso de privacidad visible se amplía a un documento de 21 apartados alineado con Ley 81/Decreto 285 y adaptado a la realidad de Mi Retiro Proyectado.
- La casilla de aceptación permanece deshabilitada hasta que el usuario llega al final del documento; aceptar requiere además una acción afirmativa sobre la casilla.
- La interfaz evita términos internos de almacenamiento cuando no aportan valor al usuario y explica el comportamiento en lenguaje común.
- El asistente usa dos barras simétricas dentro del mismo ancho del contenido: superior e inferior. En PC/laptop la superior puede permanecer disponible bajo el encabezado durante pasos largos; la inferior ofrece cierre natural.
- Las ayudas contextuales no deben quedar recortadas por `overflow` de la tarjeta de simulación.


## ADR-087 — El contenido público debe ser pertinente al propósito del producto

**Estado:** Aceptada

**Decisión:** la interfaz solo debe presentar información que ayude a operar la aplicación, comprender una estimación previsional, conocer su alcance, ejercer decisiones de privacidad, cumplir requisitos legales o utilizar funciones de seguridad/accesibilidad. Se eliminan mensajes meta como **Fin de los términos** y **Lectura completada** cuando no aportan una decisión adicional. Mi Retiro Proyectado no se presentará como aplicación educativa, didáctica o pedagógica mientras ese no sea un propósito real del producto.

**Motivo:** reducir texto ajeno a la tarea mejora claridad, evita confundir el posicionamiento del producto y mantiene coherencia entre interfaz, finalidad previsional y documentación.


## ADR-088 — Los datos importados se bloquean por campo, no por paso

**Estado:** Aceptada, aplicada y validada en UX.4.6c

**Decisión:** un valor detectado y confirmado desde Mi Retiro Seguro queda protegido contra edición directa en los pasos posteriores. La protección se aplica únicamente al campo efectivamente aportado por el documento. Si un dato no fue detectado, ese control permanece habilitado para captura manual. La corrección de un valor importado se realiza desde la vista previa documental mediante el flujo explícito **Editar campos → Finalizar edición → Importar datos**.

Para el Paso 2, `origen_campos_cuotas` registra de forma independiente el origen de `cuotas_totales` y `cuotas_anio_actual`. Los supuestos futuros (`continua_cotizando`, cierre del año y cuotas futuras por año) siguen siendo decisiones manuales.

**Motivo:** bloquear todo el paso cuando el PDF está incompleto impediría completar la simulación; permitir editar cualquier dato importado en cada pantalla rompería la trazabilidad y crearía múltiples lugares de corrección para un mismo valor.

## ADR-089 — El Paso 2 separa información acreditada y supuestos futuros

**Estado:** Aceptada, aplicada y validada en UX.4.6c

**Decisión:** la interfaz del Paso 2 se organiza en **Cuotas acreditadas** y **Cotización futura**. Las acciones internas duplicadas se eliminan y la navegación dual concentra Analizar/Continuar. Si el Asegurado(a) indica que no continuará cotizando, los campos futuros se deshabilitan y dejan de ser requeridos.

**Motivo:** la separación reduce el riesgo de interpretar una expectativa futura como dato ya acreditado y mantiene coherencia con la distinción acreditado/proyectado aplicada en fases anteriores.

## ADR-090 — La apariencia usa iconografía reconocible sin activos externos

**Estado:** Aceptada, aplicada y validada en UX.4.6c

**Decisión:** el control global de apariencia usa SVG inline para representar Sistema, Claro, Oscuro y Alto contraste. Los SVG son decorativos (`aria-hidden`) y el nombre textual del tema sigue siendo la fuente accesible de significado.

**Motivo:** la iconografía de monitor, sol, luna y contraste comunica mejor el estado que el símbolo circular abstracto anterior, sin añadir archivos gráficos ni dependencias externas.


## ADR-091 — Los modales de importación son superficies globales del wizard

**Estado:** Aceptada, aplicada y validada en UX.4.6c R2

**Decisión:** antes de abrir una vista previa documental, el modal se reubica como hijo directo de `body` si todavía se encuentra dentro de un panel del wizard. De esta forma puede abrirse desde Cuotas o pasos posteriores aunque el Paso 1 esté oculto.

**Motivo:** Bootstrap puede mostrar el backdrop pero mantener invisible un modal cuyo ancestro está oculto con `display: none`. La vista previa es una única superficie de corrección compartida por todo el flujo, no un componente exclusivo del Paso 1.

## ADR-092 — Las pistas de captura viven dentro del campo cuando sea posible

**Estado:** Aceptada, aplicada y validada en UX.4.6c R2

**Decisión:** los campos editables de texto/número usan placeholders breves y orientados al formato esperado. Cuando existe un valor manual o importado, la pista desaparece de forma nativa. Las explicaciones extensas permanecen en ayudas contextuales y no se duplican debajo del control salvo necesidad funcional.

**Motivo:** reduce ruido visual y conserva orientación justo cuando el campo está vacío. El patrón es reutilizable en UX.4.6d–g y pasos futuros.

## ADR-093 — Las ayudas contextuales usan iconografía compacta sin la palabra Info

**Estado:** Aceptada, aplicada y validada en UX.4.6c R2

**Decisión:** el disparador visual de ayuda muestra únicamente un icono `i` circular. El significado accesible se conserva mediante `aria-label`, hover, foco, clic táctil y panel reposicionable.

**Motivo:** la etiqueta del campo ya aporta contexto y la palabra `Info` repetida en cada control añade anchura y ruido sin mejorar la comprensión.

## ADR-094 — Una vista previa documental, filtrada por el paso que la invoca

**Estado:** Aceptada, aplicada y validada en UX.4.6c R3

**Decisión:** Mi Retiro Seguro mantiene un único modal de revisión. El Paso 1 muestra todas las secciones extraídas; cualquier paso posterior invoca `revisarComprobanteImportado(numeroPaso)` y solo presenta los grupos etiquetados para esa etapa. Los títulos visibles indican explícitamente el paso de destino.

**Motivo:** evita obligar al usuario a recorrer datos ajenos a la tarea actual y, al mismo tiempo, conserva una sola fuente de verdad para edición, confirmación y trazabilidad.

## ADR-095 — El control de ayuda conserva un único círculo visual

**Estado:** Aceptada, aplicada y validada en UX.4.6c R3

**Decisión:** el botón exterior de ayuda mantiene su área de interacción, foco y semántica, pero no dibuja borde propio. El único contorno circular visible pertenece a `.context-help-icon`.

**Motivo:** elimina el efecto de doble círculo observado en la interfaz sin reducir la accesibilidad por teclado ni el área útil del control.

## ADR-096 — El Paso 3 se valida como una sola unidad funcional

**Estado:** Aceptada para validación UX.4.6d

**Decisión:** las barras superior e inferior del wizard son la única acción primaria del Paso 3. `Analizar historial` debe validar, en orden coherente, el detalle del año actual cuando esté habilitado, el historial anual cuando corresponda y la base salarial. Solo cuando el conjunto queda válido la acción cambia a `Continuar a proyección`.

**Motivo:** tres botones independientes de análisis dentro de un único paso fragmentaban la tarea y permitían estados parciales difíciles de interpretar.

## ADR-097 — Un dato histórico desconocido permanece pendiente

**Estado:** Aceptada para validación UX.4.6d

**Decisión:** se elimina la acción masiva `Completar cuotas vacías con 12`. Los años sin información permanecen pendientes hasta que el Asegurado(a) los complete o la fuente documental los aporte. Cuotas y salario de una fila se validan conjuntamente cuando se inicia su captura.

**Motivo:** asumir doce cuotas para todos los años vacíos puede transformar ausencia de información en un dato previsional falso.

## ADR-098 — Ficha Digital reutiliza el contrato de revisión documental

**Estado:** Aceptada para validación UX.4.6d

**Decisión:** la Ficha Digital usa el mismo patrón visible que Mi Retiro Seguro: selección, análisis, vista previa bloqueada, edición por decisión explícita y confirmación mediante `Importar datos`. La procedencia se conserva por mes/campo y solo los datos efectivamente importados quedan bloqueados en el formulario principal.

**Motivo:** dos documentos personales no deben ofrecer modelos de interacción contradictorios ni permitir correcciones silenciosas después de la confirmación.

## ADR-099 — El asistente no necesita paneles que anuncien el siguiente paso

**Estado:** Aceptada para validación UX.4.6d

**Decisión:** se eliminan de los Pasos 2–6 y de futuros pasos los bloques `Próximo paso...`. El indicador de progreso, el selector de paso y la acción primaria común son suficientes para comunicar continuidad.

**Motivo:** estos paneles duplicaban navegación ya visible, aumentaban longitud y competían con resultados relevantes.

## ADR-100 — Paso 3 conserva tres secciones internas y un resumen único

**Estado:** Aceptada para validación UX.4.6d

**Decisión:** el Paso 3 no se divide en un séptimo paso. Se organiza como Historial salarial anual, Detalle salarial del año actual y Base salarial para proyección. Al finalizar presenta un resumen único con cuotas de referencia, cuotas identificadas, diferencia, total salarial reportado y base mensual utilizada.

**Motivo:** la división interna reduce carga perceptiva sin alterar la arquitectura de seis pasos ni fragmentar datos que deben validarse conjuntamente antes de proyectar.


## ADR-101 — Ficha Digital no redefine las cuotas acreditadas del Paso 2

**Estado:** Sustituida parcialmente por ADR-155 en UX.4.6d R23; se conserva como historial de la protección introducida en R2

**Decisión histórica R2:** `cuotas_anio_actual` se mantuvo inicialmente como referencia inmutable del Paso 2 para impedir que una importación incompleta transformara la ausencia de confirmación mensual en cero cuotas. **Vigencia actual:** ADR-155 sustituye parcialmente esta regla: una Ficha Digital confirmada puede ampliar la referencia cuando aporta más cuotas documentales del año actual, pero nunca reducirla silenciosamente cuando aporta menos.

**Motivo:** una Ficha Digital puede mostrar salarios antes de que la cuota asociada esté acreditada. Reemplazar el total del Paso 2 con la cantidad de casillas marcadas generaba inconsistencias entre pasos y podía transformar ausencia de confirmación mensual en cero cuotas acreditadas.

## ADR-102 — El detalle del año actual es opcional y debe explicar cuándo una importación queda inactiva

**Estado:** Aceptada para validación UX.4.6d R2

**Decisión:** importar una Ficha Digital activa inicialmente el detalle mensual, pero el usuario puede elegir trabajar con el total anual del historial. Si desactiva el detalle, los salarios de la Ficha no se aplican al historial y la interfaz debe explicarlo. En modo manual sin Ficha siguen disponibles captura mensual y quincenal. Un salario anual pendiente del año actual no se presenta como `0.00` cuando existen cuotas acreditadas.

**Motivo:** el usuario debe poder decidir entre detalle reciente y total anual sin que la interfaz mezcle ambas fuentes o haga parecer válido un dato todavía ausente.

## ADR-103 — Los meses detectados por Ficha Digital fijan la casilla de cuota en la captura principal

**Estado:** Aceptada para validación UX.4.6d R3

**Decisión:** cuando Ficha Digital detecta un mes con salario y estado utilizables, ese mes se incorpora como registro documental confirmado. La casilla **Cuota acreditada** se marca automáticamente y queda bloqueada tanto en la vista previa como en el detalle principal. Los meses no presentes en el documento permanecen sin marcar y editables.

`cuotas_anio_actual` del Paso 2 continuaba siendo la referencia agregada en R3. Desde R23, ADR-155 permite que una Ficha Digital confirmada **amplíe** esa referencia cuando aporta más cuotas del año actual; una ficha con menos meses no puede reducirla automáticamente.

**Motivo:** evita que el usuario deshaga accidentalmente un estado procedente del documento, mantiene simetría con el bloqueo por campo ya aplicado a otras importaciones y deja la captura manual únicamente para información ausente.

## ADR-104 — Las tablas distinguen visualmente procedencia documental y captura manual

**Estado:** Aceptada para validación UX.4.6d R4

**Decisión:** las filas que contienen información importada confirmada reciben una clase visual común `data-row-imported`; las filas sin procedencia documental usan `data-row-manual`. El patrón debe reutilizarse en Pasos 1–6 y vistas futuras cuando una tabla mezcle datos importados y manuales. Desde R4 la procedencia documental usa la paleta primaria/azul y no el verde semántico de éxito. La señal visual se acompaña siempre de controles de solo lectura/deshabilitados y no se utiliza para casillas que representan decisiones del usuario.

**Motivo:** permite identificar de inmediato qué información proviene de un documento y cuál requiere intervención manual sin depender exclusivamente del texto de ayuda o del color de un campo individual.


## ADR-105 — Las casillas importadas deben conservar una marca visual inequívoca

**Estado:** Aceptada para validación UX.4.6d R4

**Decisión:** una casilla cuyo valor forma parte de un registro documental confirmado debe restaurarse como marcada, quedar bloqueada y conservar visualmente el gancho de selección en los tres temas. El estilo no puede depender únicamente de la representación nativa del navegador cuando el control está deshabilitado.

**Motivo:** una casilla bloqueada sin marca visible se interpreta como dato no confirmado. La representación debe corresponder al estado real almacenado y mantener simetría entre Claro, Oscuro y Alto contraste.

## ADR-106 — Estado seleccionado de casillas documentales independiente del pintado nativo

**Estado:** Aceptada para validación UX.4.6d R5

Las casillas que representan cuotas mensuales procedentes de Ficha Digital deben permanecer seleccionadas tanto semántica como visualmente. El estado importado se identifica mediante metadata de procedencia y no depende únicamente de `:checked` o de cómo cada navegador represente un control `disabled`. La lectura del formulario considera la metadata importada equivalente a `true`, mientras que los meses no importados conservan el checkbox editable normal.

## ADR-107 — Borrado por paso con invalidación descendente

**Estado:** Aceptada para validación UX.4.6d R6.

**Decisión:** cada paso puede limpiarse sin alterar los anteriores, pero debe eliminar o invalidar todos los estados posteriores dependientes. Esto impide conservar resultados calculados con datos que ya no existen.

## ADR-108 — Reinicio integral separado de preferencias y consentimiento

**Estado:** Aceptada para validación UX.4.6d R6.

**Decisión:** **Reiniciar simulación** elimina la simulación completa, pero no cambia el tema visual ni la aceptación vigente de términos. Estos estados no forman parte del caso previsional.

## ADR-109 — Borrado local integral desde Privacidad

**Estado:** Aceptada para validación UX.4.6d R6.

**Decisión:** Fuentes/Privacidad ofrece una acción distinta para borrar las claves locales de simulación, consentimiento y tema. No se usa `localStorage.clear()` ni `sessionStorage.clear()` para evitar afectar datos ajenos a la aplicación en el mismo origen.

## ADR-110 — Nueva versión de términos por controles de conservación y eliminación

**Estado:** Aceptada para validación UX.4.6d R6.

**Decisión:** el texto de privacidad cambia a **2026-08-15.1** porque se amplía materialmente la información entregada al usuario sobre conservación, limpieza, reinicio y eliminación local. La nueva versión requiere aceptación nuevamente.

## ADR-111 — Consulta posterior de términos no modifica el consentimiento

**Estado:** Aceptada para validación UX.4.6d R7.

**Decisión:** Términos/Privacidad utiliza un único documento y modal con dos modos. El consentimiento inicial exige lectura/aceptación antes de usar Simular; una consulta posterior desde Fuentes abre el mismo contenido en la ruta actual, oculta los controles de aceptación y no modifica la constancia vigente. El cierre `×` solo cierra en revisión; durante el consentimiento inicial equivale a no continuar.

**Motivo:** revisar un contrato ya aceptado no debe obligar al usuario a repetir el consentimiento ni cambiar de contexto, pero tampoco debe existir una vía para cerrar el consentimiento inicial y continuar capturando datos sin una decisión afirmativa.

## ADR-112 — El estado de una fila editable deriva de sus datos actuales

**Estado:** Aceptada para UX.4.6d R8.

La tabla anual no mantiene `Pendiente` como estado estático. Cada modificación de cuotas o salario recalcula un estado progresivo: pendiente, dato faltante, revisar, sin cotización, parcial o completo. El filtro de pendientes usa la misma evaluación para evitar resultados contradictorios.

## ADR-113 — El resumen anual debe ser visible antes de terminar todo el Paso 3

**Estado:** Aceptada para UX.4.6d R8.

Un análisis válido del historial anual muestra inmediatamente cuotas de referencia, cuotas identificadas, diferencia y total salarial. No es necesario haber definido todavía la base salarial. El resumen final de Paso 3 permanece como cierre integral con la base mensual.

## ADR-114 — El scroll de tablas y los mensajes de fila no deben introducir ruido visual

**Estado:** Aceptada para UX.4.6d R8.

Las tablas con pocas filas visibles eliminan el scroll vertical innecesario; las extensas mantienen desplazamiento. Las advertencias de una fila no se insertan debajo de un control si eso rompe la alineación de columnas equivalentes.

## ADR-115 — Seleccionar archivo usa un tratamiento visual global

**Estado:** Aceptada para UX.4.6d R8.

Todo `input[type=file]` de la aplicación utiliza un botón nativo estilizado con la paleta primaria y adaptación para Claro, Oscuro y Alto contraste. Las fases futuras deben reutilizar este contrato en lugar de definir colores por pantalla.

## ADR-116 — La reactividad tabular se resuelve por delegación de eventos

**Estado:** Aceptada para UX.4.6d R9.

Las tablas editables que regeneran filas no deben depender exclusivamente de listeners instalados en cada control. El historial anual escucha `input` y `change` en su `tbody`, localiza la fila afectada, recalcula el estado y reaplica el filtro vigente. El patrón queda recomendado para tablas dinámicas futuras.

## ADR-117 — Una tabla corta no dibuja carril vertical

**Estado:** Aceptada para UX.4.6d R9.

Cuando el número de filas visibles no requiere desplazamiento, el contenedor elimina el overflow interno vertical en escritorio. En viewport estrecho se permite desplazamiento horizontal sin reservar un carril vertical vacío.

## ADR-118 — Fuentes puede captar consentimiento pendiente y Escape es contextual

**Estado:** Aceptada para UX.4.6d R9.

Si el usuario abre los términos desde Fuentes y todavía no existe una aceptación válida, la misma ventana funciona como consentimiento completo. Si ya existe, funciona solo como consulta. Cerrar con `×` o `Esc` desde Fuentes no registra aceptación; en Simular, cerrar el consentimiento obligatorio impide continuar sin aceptar.

## ADR-119 — Los ejemplos de captura son sintéticos y genéricos

**Estado:** Aceptada para UX.4.6d R9.

Los placeholders públicos no reutilizan nombres, apellidos, identificadores o importes procedentes de casos reales de prueba. Se emplean ejemplos neutros y ficticios que explican el formato sin sugerir que pertenecen a una persona concreta.

## ADR-120 — Todas las tablas usan una superficie visual común

**Estado:** Aceptada para UX.4.6d R10.

**Decisión:** las tablas visibles del producto deben envolverse en `app-table-shell`, tanto si se renderizan desde Jinja como si se generan por JavaScript. La superficie común define borde, radio, fondo, encabezado y adaptación de tema; el overflow concreto sigue perteneciendo a cada tabla según su contenido.

**Motivo:** una tabla cuadrada o con un contenedor distinto rompe la geometría establecida por tarjetas, formularios y barras del asistente. Un contrato común evita divergencias entre pasos actuales y futuros.

## ADR-121 — Las reglas transversales de tabla se aplican por semántica

**Estado:** Aceptada para UX.4.6d R10.

**Decisión:** geometría, accesibilidad, paleta y procedencia documental son reutilizables globalmente. Estados progresivos, filtro **Pendientes**, casillas bloqueadas o edición reactiva solo se incorporan en tablas donde esos conceptos existan realmente.

**Motivo:** reutilizar patrones no significa inventar estados o controles en tablas informativas. La consistencia debe conservar el significado de cada dato.

## ADR-122 — Claro, Oscuro y Alto contraste comparten geometría tabular

**Estado:** Aceptada para UX.4.6d R10.

**Decisión:** los tres temas mantienen el mismo radio y jerarquía de tabla. Claro y Oscuro ajustan sutilmente borde, superficie y encabezado; Alto contraste usa borde blanco reforzado y elimina sombras. Los colores de éxito, advertencia y procedencia no cambian de significado entre temas.

**Motivo:** la accesibilidad visual exige que cambiar de tema no cambie la estructura percibida ni confunda origen documental con estado funcional.



## ADR-123 — El scrollbar tabular forma parte de la geometría de `app-table-shell`

**Estado:** Aceptada para UX.4.6d R11.

**Decisión:** las tablas desplazables eliminan los botones/flechas nativos del scrollbar en Chromium/Windows, usan un carril transparente separado de las esquinas redondeadas y un thumb temático. Firefox mantiene una representación equivalente mediante propiedades estándar.

**Motivo:** un scrollbar que atraviesa o sobresale sobre el radio derecho rompe la simetría visual de la tabla aunque el borde exterior esté correctamente redondeado.

## ADR-124 — Selector de archivo y acción de análisis comparten altura

**Estado:** Aceptada para UX.4.6d R11.

**Decisión:** los importadores PDF usan una altura exterior común para `official-import-file-input` y el botón de `official-import-upload-action`. El contrato es transversal a Mi Retiro Seguro, Ficha Digital e importadores futuros.

**Motivo:** ambos controles representan los pasos consecutivos de una misma operación y deben percibirse como una fila simétrica, no como componentes de jerarquía o tamaño diferentes.

## ADR-125 — El scrollbar temático es transversal a las superficies desplazables

**Estado:** Aceptada para UX.4.6d R12.

**Decisión:** la representación temática del scrollbar deja de ser exclusiva de tablas y se comparte con términos, modales, página y navegación desplazable. Se mantiene el mecanismo nativo de scroll y se suprimen botones/flechas cuando el motor del navegador permite estilizar esas piezas.

**Motivo:** el usuario debe percibir el mismo lenguaje visual al desplazarse por términos, vistas previas y tablas, sin mezclar carriles nativos de Windows con componentes tematizados.

## ADR-126 — Las tablas usan un radio específico menor que las tarjetas

**Estado:** Aceptada para UX.4.6d R12.

**Decisión:** `app-table-shell` usa `--app-radius-md` mientras las tarjetas pueden conservar radios mayores.

**Motivo:** una tabla desplazable necesita integrar el carril interno en una arista más compacta; mantener exactamente el radio grande de una card fuerza al scrollbar contra una esquina excesivamente curva.

## ADR-127 — Un filtro sin filas no conserva una tabla vacía

**Estado:** Aceptada para UX.4.6d R12.

**Decisión:** cuando el filtro **Pendientes** del historial anual llega a cero, se oculta el contenedor tabular completo y se muestra un estado vacío accesible. El patrón es reutilizable en tablas filtrables futuras donde cero resultados haga innecesaria la cabecera.

**Motivo:** una cabecera sin filas aparenta contenido incompleto y añade ruido visual; un estado vacío comunica de manera directa que no quedan registros pendientes.


## ADR-128 — El selector nativo de archivo no depende del hover interno

**Estado:** Aceptada para UX.4.6d R13.

**Decisión:** el botón nativo de `input[type=file]` mantiene una paleta estable en estados base, hover y focus. El feedback interactivo se expresa en el control exterior, sin depender de `::file-selector-button:hover`.

**Motivo:** Bootstrap/Chromium puede considerar `:hover` activo sobre todo el input cuando el puntero está sobre el nombre del archivo, y la pseudoclase del botón no ofrece un comportamiento suficientemente uniforme entre motores. La regla estable evita regresar accidentalmente a la paleta predeterminada.


## ADR-129 — El Paso 1 manual usa un único bloque de Información personal

**Estado:** Aceptada para UX.4.6d R14.

**Decisión:** la captura manual del Paso 1 deja de separar visualmente `Identificación personal` e `Información previsional básica`. Todos los campos se presentan dentro de **Información personal**; **Sexo** queda inmediatamente antes de **Apellido de casada** para que el campo condicional aparezca en la misma zona al seleccionar Femenino.

**Motivo:** la separación anterior obligaba a recorrer el formulario para seleccionar Sexo y luego volver visualmente hacia los apellidos para localizar el campo que acababa de aparecer. La unificación mejora continuidad sin mezclar responsabilidades de negocio: los campos opcionales siguen sin afectar cálculos y los obligatorios conservan la misma validación.

## ADR-130 — Los campos no editables tienen una semántica visual transversal

**Estado:** Aceptada para UX.4.6d R15.

**Decisión:** `form-control` y `form-select` en estado `readonly`/`disabled` usan tokens de superficie, texto y borde propios, más una señal lateral primaria. La regla es común a importaciones, cálculos automáticos y campos deshabilitados por una decisión previa.

**Motivo:** en Oscuro y Alto contraste la superficie anterior era demasiado parecida a un control editable. El estado debe ser perceptible sin depender únicamente del color.

## ADR-131 — El lenguaje de importación no acopla el producto al formato del archivo

**Estado:** Aceptada para UX.4.6d R15.

**Decisión:** la interfaz habla de **Mi Retiro Seguro**, **Ficha Digital**, **comprobante** o **documento**. El PDF continúa siendo el formato técnico actualmente admitido y validado, pero no forma parte del nombre de la modalidad ni de sus encabezados principales.

**Motivo:** la CSS puede cambiar el diseño del comprobante o, en una evolución futura, el formato de entrega. La experiencia de revisión/importación debe sobrevivir a esos cambios; el parser se adapta por separado.

## ADR-132 — Limpiar Paso 2 elimina también los supuestos futuros

**Estado:** Aceptada para UX.4.6d R15.

**Decisión:** una simulación nueva o un Paso 2 recién limpiado no selecciona automáticamente continuidad ni conserva `12/12`. Los campos de supuestos futuros permanecen vacíos/deshabilitados hasta que el usuario elija Sí o No. Al elegir Sí, se pueden ofrecer 12 cuotas como sugerencia vigente.

**Motivo:** una acción de limpieza debe producir un estado realmente vacío y no reintroducir valores por atributos HTML o rutinas de inicialización. La reconstrucción defensiva de procedencia para sesiones antiguas exige además que el valor correspondiente exista, evitando controles vacíos bloqueados tras limpiar el paso.

## ADR-133 — Paso 3 revalida dependencias recuperables sin navegar hacia atrás

**Estado:** Aceptada para UX.4.6d R16.

**Decisión:** si el resumen de cuotas fue invalidado pero el formulario de Paso 2 conserva datos completos y válidos, **Analizar historial** reconstruye el resumen en segundo plano. Si los datos están incompletos, Paso 3 conserva su contenido y presenta una advertencia contextual; no cambia de paso automáticamente.

**Motivo:** obligar al usuario a retroceder y volver a avanzar por una derivación que puede recalcularse automáticamente introduce fricción y rompe continuidad.

## ADR-134 — La restauración nunca reabre un paso con prerrequisitos inválidos

**Estado:** Aceptada para UX.4.6d R16.

**Decisión:** `paso_actual` guardado se normaliza al último paso permitido por `puedeAccederDirectamenteAPaso()` antes de mostrar el asistente.

**Motivo:** una limpieza o invalidación puede dejar un número de paso antiguo en almacenamiento; restaurarlo sin verificar dependencias produce estados imposibles.

## ADR-135 — Ficha Digital pertenece al Detalle salarial del año actual

**Estado:** Aceptada para UX.4.6d R16.

**Decisión:** el cargador/revisor de Ficha Digital deja de ser una subsección paralela entre Historial anual y Detalle. Se integra dentro de **Detalle salarial del año actual** y se muestra antes de la tabla mensual que alimenta.

**Motivo:** la fuente debe preceder visualmente al resultado que genera y la Ficha Digital solo aporta información del año actual.


## ADR-136 — Bloqueo documental y valor booleano son estados independientes

**Estado:** Aceptada para UX.4.6d R17.

**Decisión:** `data-imported-locked` impide editar un checkbox, pero el gancho visual solo se fuerza cuando `checked=true`.

**Motivo:** en la vista previa de Mi Retiro Seguro una fila proyectada puede estar correctamente bloqueada y, al mismo tiempo, correctamente excluida del historial real. Pintarla marcada por el solo hecho de estar bloqueada comunica un dato falso.

## ADR-137 — Cuotas acreditadas y cuotas acumuladas con proyección se muestran separadas

**Estado:** Aceptada para UX.4.6d R17.

**Decisión:** Paso 2 utiliza la cifra documental de cuotas históricas/acreditadas. Si el comprobante también contiene un total acumulado mayor por períodos proyectados, la vista previa lo explica como contexto y no lo utiliza como acreditado.

**Motivo:** evita confundir una proyección del comprobante con aportes ya acreditados.

## ADR-138 — Las inconsistencias internas del documento se conservan y se advierten

**Estado:** Aceptada para UX.4.6d R17.

**Decisión:** cuando el historial detectado comienza antes del año de la fecha de ingreso CSS indicada en el mismo comprobante, el parser conserva ambos datos y genera una advertencia no bloqueante.

**Motivo:** la aplicación no debe corregir silenciosamente una fuente oficial ni descartar registros históricos que sí aparecen en ella.

## ADR-139 — Un dato editado por el usuario deja de etiquetarse como detectado

**Estado:** Aceptada para UX.4.6d R17.

**Decisión:** la vista previa registra los campos modificados y los presenta posteriormente como **Editado por ti** o **Completado manualmente**.

**Motivo:** `Detectado` debe reservarse a valores extraídos del documento; de lo contrario se pierde trazabilidad sobre el origen real del dato.

## ADR-140 — Salario disponible no equivale automáticamente a cuota acreditada

**Estado:** Aceptada para UX.4.6d R17.

**Decisión:** una diferencia entre el detalle mensual y Paso 2 no modifica silenciosamente las cuotas. La advertencia explica que puede conservarse un salario conocido sin marcar cuota si esta todavía no figura acreditada.

**Motivo:** la Ficha Digital y otros comprobantes pueden actualizar salario y cuota en momentos distintos.

## ADR-141 — La procedencia se modela separada del valor y de su validez

**Estado:** Aceptada para UX.4.6d R18.

**Decisión:** los campos que mezclan importación y edición usan cuatro estados visibles: **Detectado**, **Editado por ti**, **Completado manualmente** y **No detectado**. El estado de procedencia no sustituye validaciones de obligatoriedad, coherencia o cálculo.

**Motivo:** un dato puede ser válido y manual, o importado y posteriormente corregido; mezclar esas dimensiones pierde trazabilidad.

## ADR-142 — El selector nativo de archivos no se restaura tras F5

**Estado:** Aceptada para UX.4.6d R18.

**Decisión:** después de una recarga no se intenta repoblar `input[type=file]`. La aplicación restaura la importación confirmada, sus datos y el nombre del documento como metadata visual, dejando disponibles **Revisar importación** y **Quitar importación**.

**Motivo:** los navegadores impiden restaurar rutas/archivos seleccionados por seguridad; simular que el archivo sigue adjunto sería incorrecto.

## ADR-143 — El nombre del documento es metadata local, no persistencia del archivo

**Estado:** Aceptada para UX.4.6d R18.

**Decisión:** el nombre del documento puede conservarse en `sessionStorage` dentro del estado de la importación para identificarla visualmente. No se conservan bytes, ruta local ni contenido original fuera del procesamiento en memoria.

**Motivo:** permite continuidad de UX tras F5 sin alterar el modelo de privacidad ni introducir almacenamiento remoto.


## ADR-144 — El detalle del año actual es la fuente de la fila anual vigente cuando está habilitado

**Estado:** Aceptada para UX.4.6d R19.

**Decisión:** mientras **Detalle salarial del año actual** esté activo, la fila del año calendario vigente en el historial anual deriva automáticamente sus cuotas de las casillas **Cuota acreditada** y su salario anual de los salarios de esos mismos meses. La fila queda de solo lectura para evitar doble captura.

**Motivo:** pedir el mismo dato mensual y anual genera inconsistencias y obliga al usuario a mantener dos representaciones manualmente.

## ADR-145 — Una casilla manual de cuota actual puede actualizar Paso 2 sin navegación regresiva

**Estado:** Aceptada para UX.4.6d R19.

**Decisión:** marcar/desmarcar una casilla editable de **Cuota acreditada** se considera una confirmación explícita de información más reciente. La aplicación recalcula `cuotas_anio_actual` y `cuotas_totales` del Paso 2 conservando `cuotas_totales - cuotas_anio_actual` como base previa al año vigente. Los resultados dependientes se invalidan y se revalidan al analizar; no se cambia de pantalla.

**Motivo:** un comprobante puede ser una fotografía anterior del año. Obligar al usuario a volver a Paso 2 después de confirmar una cuota más reciente en Paso 3 duplica trabajo; ignorar el cambio deja el modelo incoherente.

## ADR-146 — Salario disponible y salario anual acreditado continúan separados

**Estado:** Aceptada para UX.4.6d R19.

**Decisión:** el salario anual sincronizado suma únicamente meses con cuota acreditada. Un salario conocido de un mes sin casilla marcada permanece en `total_salario_disponible` y puede alimentar bases salariales recientes, pero no incrementa el salario anual acreditado. Una cuota marcada sin salario mantiene el año como pendiente.

**Motivo:** conserva la distinción temporal entre información salarial conocida y acreditación efectiva, evitando sumar como histórico un mes que aún no se confirmó como cuota.


## ADR-147 — La vigencia de Ficha Digital se evalúa por el último período detectado

**Estado:** Sustituida por ADR-149 en UX.4.6d R21; se conserva como historial de R20.

**Decisión:** la interfaz compara `anio_mas_reciente`/`mes_mas_reciente` con el mes local actual. Se acepta sin advertencia el mes actual y hasta dos meses calendario anteriores. Una diferencia mayor se presenta como posible desactualización y exige elegir entre seleccionar una ficha más reciente o continuar con la actual.

**Motivo:** los datos salariales pueden publicarse con retraso; exigir coincidencia con el mes actual produciría falsos positivos, mientras que ignorar varios meses de desfase puede llevar al usuario a asumir que la ficha representa información reciente.

## ADR-148 — Los resúmenes derivados relevantes deben ser auditables desde el Paso 3

**Estado:** Aceptada para UX.4.6d R20.

**Decisión:** `resumen_detalle_anio_actual` se muestra en una sección compacta dentro del Paso 3 sin crear un nuevo modelo ni recalcular fórmulas en JavaScript. El bloque se oculta cuando el detalle se invalida.

**Motivo:** las bases salariales automáticas dependen de valores que antes solo existían internamente. Mostrar el resumen permite verificar las cifras antes de continuar y evita depender de cálculos externos.


## ADR-149 — Una Ficha Digital anterior al mes actual siempre requiere revisión

**Estado:** Aceptada para UX.4.6d R21. Sustituye el criterio de tolerancia de ADR-147.

**Decisión:** si el último período detectado es anterior al mes actual verificado, la Ficha Digital se presenta como potencialmente desactualizada, aunque la diferencia sea de un solo mes. La advertencia no bloquea: permite seleccionar una ficha del mes actual o continuar.

**Motivo:** el usuario quiere conocer explícitamente cualquier desfase respecto del mes actual y decidir conscientemente si trabaja con información anterior.

## ADR-150 — La vigencia documental no confía en el reloj local del cliente

**Estado:** Aceptada para UX.4.6d R21.

**Decisión:** el backend obtiene una fecha de referencia por HTTPS desde infraestructura oficial de la CSS. Si no puede verificarla, el sistema no usa silenciosamente la fecha del navegador/equipo para declarar una ficha reciente; muestra un estado de fecha no verificada y solicita decisión.

**Motivo:** el reloj local puede modificarse y no constituye una fuente suficientemente confiable para una decisión de vigencia.

## ADR-151 — La consulta de fecha oficial no transmite información previsional

**Estado:** Aceptada para UX.4.6d R21.

**Decisión:** la verificación solicita únicamente la fecha publicada por servidores oficiales. No envía documento, nombres, identificadores, salarios, cuotas ni resultados. La política de privacidad informa que la conexión puede exponer metadatos ordinarios de red como la IP y se versiona a **2026-08-16.1**.

**Motivo:** la fuente externa mejora integridad temporal, pero debe mantenerse minimización y transparencia del tratamiento.

## ADR-152 — El Paso 3 reconcilia cuotas manuales antes de validar el detalle

**Estado:** Aceptada para UX.4.6d R22.

**Decisión:** cuando el detalle del año actual contiene una cuota confirmada manualmente o la referencia de Paso 2 ya proviene de ese detalle, **Analizar historial** reconcilia primero `cuotas_anio_actual`/`cuotas_totales` y, si hubo cambios, revalida Paso 2 en segundo plano antes de enviar el detalle al backend.

**Motivo:** la confirmación mensual es una fuente más reciente que la fotografía importada. Depender exclusivamente del evento `change` puede dejar un estado incoherente tras restauraciones o eventos perdidos.

## ADR-153 — Ningún bloqueo del Paso 3 puede ser silencioso

**Estado:** Aceptada para UX.4.6d R22.

**Decisión:** si el backend devuelve `cuotas_coinciden=false`, la sección del detalle muestra un error explícito con cuotas identificadas, referencia de Paso 2 y orientación sobre las casillas **Cuota acreditada**. El scroll/foco complementa el mensaje, pero nunca lo sustituye.

**Motivo:** desplazar al usuario hacia una sección sin explicar qué condición falla impide corregir el problema y parece una navegación defectuosa.

## ADR-154 — El resumen del detalle conserva métricas semánticamente distintas

**Estado:** Aceptada para UX.4.6d R22.

**Decisión:** se mantienen cuotas identificadas, salarios disponible/acreditado, meses con información/completos, últimos períodos, último salario y los tres promedios. Aunque algunos valores coincidan en un escenario totalmente acreditado, divergen con salarios no acreditados o períodos parciales y los tres promedios alimentan opciones automáticas distintas.

**Motivo:** eliminarlos por coincidencia circunstancial ocultaría diferencias relevantes para el asegurado y reduciría auditabilidad.



## ADR-155 — Una Ficha Digital confirmada puede ampliar la referencia agregada del año actual

**Estado:** Aceptada para UX.4.6d R23. Sustituye parcialmente ADR-101 para discrepancias documentales al alza.

**Decisión:** cuando la Ficha Digital confirmada contiene más meses con `cuota_acreditada=true` que `cuotas_anio_actual` del Paso 2, el detalle mensual se considera evidencia más reciente del año vigente. Se conserva el total de cuotas anteriores al año actual y se sustituye únicamente el componente del año corriente; el resumen de Cuotas se revalida sin abandonar Paso 3.

**Motivo:** una Ficha Digital posterior puede incorporar meses acreditados después de la fotografía agregada usada por Mi Retiro Seguro. Mantener indefinidamente la cifra antigua produce un bloqueo artificial aunque la aplicación ya posea evidencia mensual confirmada.

## ADR-156 — Una Ficha Digital nunca reduce silenciosamente una referencia superior de Paso 2

**Estado:** Aceptada para UX.4.6d R23.

**Decisión:** la sincronización automática desde Ficha Digital es monotónica: puede aumentar `cuotas_anio_actual`, pero si la ficha tiene menos cuotas que Paso 2 se conserva la referencia superior y se muestra una advertencia para revisar/completar los meses. Una reducción solo puede provenir de una decisión explícita del usuario dentro de un detalle que ya sea la fuente vigente.

**Motivo:** una ficha anterior, parcial o incompleta no debe borrar cuotas que otra fuente más reciente o una confirmación previa ya reconoce.

## ADR-157 — VERSION es la fuente canónica de versión de aplicación

**Estado:** vigente.
**Fecha:** 2026-08-17.

**Decisión:** la versión de aplicación se declara en el archivo raíz `VERSION`. `app/core/version.py` es el único adaptador Python autorizado para leerla y `app/core/config.py` importa `APP_VERSION` desde ese módulo. FastAPI y Jinja2 continúan recibiendo el mismo valor sin copias literales.

**Motivo:** eliminar divergencias entre API, footer, documentación y releases y permitir validaciones automáticas de coherencia.

**Consecuencia:** un cambio de versión requiere modificar `VERSION` y actualizar los documentos de release afectados; no se hardcodea la versión en plantillas, JavaScript o motores.

## ADR-158 — Reconstrucción histórica sin tags retroactivos

**Estado:** Parcialmente sustituida por ADR-159 para la materialización criptográfica de tags.
**Fecha:** 2026-08-17.

**Decisión:** los 80 commits previos a GOV.1.2 se agrupan documentalmente en `0.0.1-beta` a `0.0.21-beta`. No se reescribe Git ni se crean tags retrospectivos que aparenten haber existido en esas fechas. `0.0.22-beta` es la primera versión formal adoptada conscientemente bajo `VERSIONING.md`.

**Motivo:** preservar la evidencia primaria de Git y, al mismo tiempo, ofrecer a revisores y auditores una cronología legible.

**Consecuencia:** `RELEASES.md` distingue explícitamente versiones retrospectivas de versiones formales y clasifica el antiguo `0.1.0` como marcador histórico de desarrollo no publicado.

## ADR-159 — Firma SSH obligatoria y materialización controlada de tags históricos

**Estado:** vigente; materialización histórica ejecutada el 2026-08-17.
**Fecha:** 2026-08-17.

**Decisión:** a partir del primer commit posterior a `v0.0.23-beta`, los commits nuevos del mantenedor y todos los tags formales nuevos se firman criptográficamente con SSH. La clave pública autorizada se versiona en `.github/allowed_signers`; la clave privada permanece fuera del repositorio.

Se autoriza además una migración histórica controlada: `v0.0.1-beta` a `v0.0.21-beta` se materializan como tags retrospectivos firmados que apuntan a los commits de cierre reconstruidos, conservando la fecha real de creación del tag y declarando por separado la fecha histórica del hito. `v0.0.22-beta` y `v0.0.23-beta`, originalmente publicados como tags anotados sin firma, pueden reemitirse una sola vez como objetos tag firmados **sin cambiar sus commits objetivo**.

**Motivo:** añadir autenticidad criptográfica y una cadena verificable de releases sin reescribir commits históricos, sin falsificar fechas y sin ocultar que los primeros 21 tags fueron materializados posteriormente.

**Consecuencia:** ADR-158 sigue vigente en su prohibición de reescribir Git o aparentar existencia histórica de los tags, pero queda parcialmente sustituida respecto de no crear ningún tag retrospectivo. La materialización autorizada fue ejecutada el 2026-08-17; la excepción para reemitir `v0.0.22-beta` y `v0.0.23-beta` quedó consumida y vuelve a regir la inmutabilidad estricta.

## ADR-160 — Salario futuro conocido conserva precisión decimal en toda la trayectoria

**Estado:** Sustituida parcialmente por ADR-173; se conserva íntegramente el criterio de precisión decimal y se limita la reutilización de la tasa inferida al año objetivo.

**Decisión:** la modalidad `FUTURO_CONOCIDO` deriva la tasa anual compuesta equivalente mediante `Decimal` desde el salario mensual actual, el salario mensual futuro y la cantidad de años. La trayectoria reutiliza esa tasa sin convertirla a aritmética binaria de `float`; el redondeo monetario continúa ocurriendo únicamente al materializar cada registro visible.

**Nota posterior UX.4.6f R2:** ADR-173 mantiene esta precisión durante el tramo base → objetivo, pero deja de reutilizar la tasa después del año conocido; el salario objetivo se mantiene constante salvo que exista otro supuesto explícito.

**Motivo:** el Paso 4 sirve como entrada a la línea temporal y posteriormente a escenarios previsionales. Una conversión innecesaria a `float` contradice el contrato general de precisión monetaria y puede introducir pequeñas derivas acumulativas sin aportar información adicional.

**Alcance:** la corrección fue detectada durante la estandarización técnica UX.4.6e R2. No constituye el rediseño funcional/visual del Paso 4, que queda reservado a UX.4.6f.

## ADR-161 — Web Storage usa un namespace único de producto sin compatibilidad pre-beta

**Estado:** Aceptada para UX.4.6e R3.

**Decisión:** todas las claves propias de Web Storage se normalizan bajo
`miRetiroProyectado.*`: simulación, consentimiento persistente, autorización de
sesión y apariencia. Se eliminan los identificadores pre-beta
`calculadoraPensionCSS.*` y `mi-retiro-proyectado-tema` sin fallback ni migración.

**Motivo:** la aplicación ya adoptó formalmente la identidad Mi Retiro Proyectado
y todavía no existe una beta pública cuyos datos locales deban preservarse. El
mantenedor confirmó el borrado de los estados de prueba existentes y autorizó una
ruptura limpia para evitar arrastrar indefinidamente nombres técnicos anteriores.

**Consecuencia:** después de aplicar esta revisión, un navegador que conserve datos
bajo claves anteriores no los recuperará automáticamente. Cualquier cambio futuro
de namespace se tratará como una migración de esquema y deberá decidir de forma
explícita cómo conservar o descartar estado.

## ADR-162 — Los comentarios de runtime son semánticos y no cronológicos

**Estado:** Aceptada para UX.4.6e R4.

**Decisión:** el código vigente de `app/` describe responsabilidades, contratos,
límites y motivos sin conservar identificadores de fase `UX.*`/`GOV.*` en
comentarios o docstrings. La historia de una revisión permanece en ADR, pruebas,
`CHANGELOG.md`, `RELEASES.md` y documentación histórica. Las funciones y clases
del runtime mantienen docstrings suficientes para que otro desarrollador pueda
identificar fronteras de privacidad, parsing, red, trazabilidad y efectos
secundarios sin narrar línea por línea.

**Motivo:** un número de revisión envejece como comentario de implementación y no
explica qué responsabilidad conserva el bloque. Los comentarios semánticos son
más útiles para mantenimiento, revisión de seguridad y evolución del producto.

**Consecuencia:** las pruebas pueden conservar identificadores históricos cuando
forman parte de la trazabilidad de una regresión. La normalización de CSS no
reordena reglas ni cambia la cascada; esta decisión es documental y de
mantenibilidad, no un rediseño visual.

## ADR-163 — La preparación pública separa información útil al usuario de gobierno interno

**Estado:** Aceptada para UX.4.6e R5.

**Decisión:** la interfaz puede mostrar ayuda, contacto, repositorio del proyecto, privacidad, fuentes oficiales, versión y carácter independiente. No expone como contenido de producto CODEOWNERS, rulesets, firmas Git, Dependabot, nombres de jobs CI, ADR internos ni otros controles de gobierno que no ayudan al Asegurado(a). La metadata de comunidad de GitHub —topics, labels, badges, Issue Forms y social preview— se prepara de forma separada en el repositorio.

**Motivo:** preparar un repositorio para publicación no implica trasladar sus mecanismos internos de ingeniería a la interfaz de usuario. La aplicación debe conservar transparencia sobre lo que afecta a uso, datos, fuentes y soporte, mientras GitHub conserva la información de contribución, mantenimiento y auditoría.

**Consecuencia:** el enlace al repositorio puede existir desde la interfaz sin afirmar que el acceso sea público en todas las etapas. Las labels se aplican a Issues/PR, no a commits; el README puede mostrar badges de estado del repositorio sin convertir esos controles en elementos del asistente previsional.
## ADR-164 — La renumeración vigente no reescribe la historia UX anterior

**Estado:** Aceptada para UX.4.6e R6.

**Decisión:** UX.4.6e queda reservado al bloque transversal de estandarización técnica, comentarios, coherencia de interfaz y preparación del repositorio. El trabajo funcional posterior se identifica como UX.4.6f — Paso 4, UX.4.6g — Paso 5 y UX.4.6h — Paso 6. Los documentos vigentes deben usar esta secuencia. Los releases, auditorías, snapshots y bitácoras que registraron la numeración prospectiva anterior conservan sus identificadores originales y, cuando sea necesario para evitar ambigüedad, reciben una nota posterior explícita en vez de reescribirse.

**Motivo:** la trazabilidad exige distinguir entre el plan que existía en un momento histórico y la planificación vigente. Renumerar retrospectivamente evidencias antiguas haría parecer que decisiones posteriores ya existían en revisiones anteriores.

**Consecuencia:** pruebas documentales deben comprobar tanto la secuencia actual como la preservación histórica. La reasignación no modifica los números visibles del asistente: Paso 4, Paso 5 y Paso 6 continúan siendo los mismos pasos funcionales para el Asegurado(a).

## ADR-165 — La auditoría transversal es un gate antes de la validación funcional manual

**Estado:** Aceptada para UX.4.6e R7.

**Decisión:** antes de iniciar la prueba funcional manual/automática de cierre hasta el Paso 3, UX.4.6e ejecuta una auditoría transversal que comprueba coherencia entre código runtime, comentarios/docstrings, interfaz visible, documentación vigente, regresiones automatizadas y metadata manual de GitHub. Los snapshots históricos no se reinterpretan; cuando una referencia antigua pueda inducir a error, se añade una nota posterior explícita.

**Motivo:** la fase modifica de forma simultánea mantenibilidad, almacenamiento local, documentación, presentación al usuario y preparación del repositorio. Un gate transversal reduce el riesgo de que cada cambio pase sus pruebas aisladas pero el conjunto quede documental o semánticamente incoherente. La auditoría no sustituye la prueba funcional de R8 ni la validación remota de CI del cierre.

## ADR-166 — El borrado integral invalida también residuos pre-beta y fuerza reconsentimiento

**Estado:** Aceptada para UX.4.6e R8.

**Decisión:** **Borrar datos de esta aplicación en este navegador** elimina las claves vigentes `miRetiroProyectado.*` y, únicamente durante esa operación destructiva, purga identificadores pre-beta conocidos que puedan permanecer en Web Storage. Las claves antiguas no se consultan para recuperar, restaurar ni migrar datos. Después del borrado, la aplicación vuelve a Inicio solicitando una nueva presentación de términos; si el usuario cierra esa consulta sin aceptar, un acceso posterior a Simular vuelve a exigir consentimiento antes de habilitar el asistente.

**Motivo:** la validación manual de R8 evidenció que un navegador podía conservar estado pre-beta o una combinación de recursos en caché suficiente para que el borrado nominal no provocara el reconsentimiento esperado. Un botón que declara eliminar la aceptación debe garantizar ese efecto incluso en instalaciones de prueba anteriores al namespace vigente.

**Consecuencia:** ADR-161 continúa vigente: no existe compatibilidad, fallback ni migración desde claves pre-beta. La única excepción es su reconocimiento para borrado defensivo. No se usa `localStorage.clear()` ni `sessionStorage.clear()`, por lo que no se eliminan claves ajenas a la aplicación dentro del mismo origen. La versión material de privacidad permanece `2026-08-16.1` porque la finalidad, categorías de datos, destinatarios y conservación no cambian; se corrige el cumplimiento técnico de un control ya informado.

## ADR-167 — Los datos documentales confirmados son editables sin perder la referencia original

**Estado:** Aceptada para cierre funcional UX.4.6e R8.

**Decisión:** una importación confirmada de Mi Retiro Seguro o Ficha Digital deja de convertir el dato detectado en un control permanentemente bloqueado. El Asegurado(a) puede ajustar, completar, excluir o reincluir información desde las superficies habilitadas. La aplicación conserva separadas la **fotografía original del documento** y la **copia de trabajo utilizada por la simulación**, actualiza en tiempo real la procedencia visible y vuelve a invalidar/reconciliar los resultados dependientes.

Los estados de procedencia visibles son:

- `Detectado`: valor procedente del documento y sin modificación activa;
- `Editado por ti`: el documento aportó un valor y la copia de trabajo difiere;
- `Completado manualmente`: el documento no aportó el dato y el usuario lo añadió;
- `Excluido por ti`: un período detectado se conserva como referencia pero no alimenta la simulación;
- `No detectado`: el dato continúa ausente.

Para Ficha Digital, un mes detectado comienza incluido. Desmarcar su cuota constituye una **exclusión explícita** del período para la simulación: no aporta cuota, salario acreditado ni mes utilizado, aunque el valor original permanezca visible como referencia. Reintegrarlo restaura la procedencia `Detectado` cuando no existen otras modificaciones en ese período.

**Motivo:** la validación funcional R8 mostró dos necesidades legítimas. Primero, un Asegurado(a) puede necesitar reproducir un corte anterior o corregir una detección sin eliminar la evidencia de qué decía el documento. Segundo, un campo que el documento no detectó puede completarse después de confirmar la importación y debe reflejar inmediatamente esa procedencia en todas las vistas. El bloqueo absoluto impedía ambos casos y confundía “fuente documental” con “valor inmutable”.

**Consecuencia:** ADR-088, ADR-103, ADR-105 y ADR-106 quedan sustituidas parcialmente en sus criterios de bloqueo/inclusión inmutable; ADR-104 conserva la distinción visual de procedencia, pero no exige solo lectura. ADR-156 continúa vigente: una Ficha Digital **no reduce silenciosamente** una referencia superior; una reducción solo ocurre por una acción explícita del usuario y queda identificada como exclusión. La edición no modifica el archivo PDF ni afirma que el documento original contenía el valor ajustado.

La aplicación mantiene como referencias de frontend, entre otras:

- `referencia_mi_retiro_seguro_original`;
- `ficha_digital_importada_original`;
- `periodos_excluidos_importacion_ficha`;
- mapas de `origen_campos_*`.

Estas estructuras forman parte del estado temporal de la simulación, no de los modelos jurídicos de la CSS.

## ADR-168 — La etapa `0.0.N-beta` conduce directamente a la versión oficial `1.0.0.x` con Build independiente

**Estado:** Aceptada para PLAN.1.
**Fecha:** 2026-08-20.

**Decisión:** Mi Retiro Proyectado conserva `0.0.N-beta` como familia de versiones durante la etapa beta de desarrollo. Cuando se cierren todos los gates funcionales, normativos, de seguridad, privacidad, accesibilidad, calidad y release definidos por el plan maestro, la transición prevista será directamente a la primera versión oficial `1.0.0.0`.

Las versiones oficiales utilizan cuatro componentes propios del producto:

```text
MAYOR.MENOR.PARCHE.REVISIÓN
```

La cuarta posición representa revisiones/hotfix de una versión oficial ya publicada. Esta convención de cuatro componentes es propia de Mi Retiro Proyectado y no se presenta como SemVer estricto.

Los artefactos oficiales incorporarán además un identificador **Build** independiente, de seis dígitos, monotónico y no reutilizable:

```text
Build 000001
```

El Build:

- no forma parte de `VERSION`;
- no forma parte del tag Git;
- no se incrementa por cada commit;
- identifica un artefacto reproducible concreto;
- solo se materializa cuando exista el proceso formal de empaquetado definido en REL.1.

Los tags continúan derivándose de la versión canónica: `v0.0.N-beta` durante la etapa beta y, para versiones oficiales, valores como `v1.0.0.0`.

La planificación anterior que reservaba `0.1.0-beta.1` como futura primera beta pública queda sustituida como **objetivo vigente**. Las menciones conservadas en releases, cierres, snapshots o regresiones históricas no se borran ni se reinterpretan: permanecen como evidencia del plan que existía en ese momento y pueden acompañarse de una nota posterior que documente su sustitución.

**Motivo:** el proyecto ya venía publicando hitos formales con sufijo `-beta`. Introducir después otra familia denominada “primera beta” produciría una distinción artificial entre betas ya existentes y una beta posterior, además de complicar la trazabilidad sin aportar una diferencia funcional real. La transición directa a `1.0.0.0` permite que la salida de beta represente un gate explícito de producto completo.

**Consecuencia:** `VERSIONING.md`, el validador canónico de versión, el proceso de release, el plan maestro, la documentación vigente y sus regresiones deben aceptar la línea oficial de cuatro componentes sin modificar retroactivamente `v0.0.25-beta` ni otros tags publicados. No existe una promoción automática a `1.0.0.0`: el cambio solo puede ocurrir después de cerrar la secuencia de catorce bloques y REL.1.

La fuente canónica del Build y el mecanismo exacto para asignarlo, reproducirlo, firmarlo y asociarlo con hashes de artefactos se definirán en REL.1. Hasta entonces no se versiona ni se muestra un Build ficticio.

## ADR-169 — Las decisiones explícitas no usan valores predeterminados silenciosos y los valores derivados muestran procedencia automática

**Estado:** Aceptada para UX.4.6f R1.
**Fecha:** 2026-08-20.

**Decisión:** los controles que representan una decisión del Asegurado(a) deben comenzar sin una elección almacenada cuando todavía no existe una acción explícita ni una fuente confirmada que permita derivarla. La interfaz muestra `Seleccione una opción` y el estado serializado conserva la ausencia de decisión mediante cadena vacía o `null`, según el tipo del campo.

Cuando la aplicación deriva un valor a partir de una regla transparente o de información ya confirmada, la procedencia visible es `Calculado automáticamente`. Si el Asegurado(a) modifica después ese valor, la procedencia pasa a `Editado por ti`. Este contrato se aplica inicialmente al año inicial del historial y al horizonte salarial sugerido, y puede reutilizarse en valores derivados equivalentes.

Marcar explícitamente que se continuará cotizando puede sugerir 12 cuotas al cierre del año y 12 cuotas por año futuro. La sugerencia se explica en la interfaz y continúa editable. Del mismo modo, el horizonte del Paso 4 puede iniciar en cinco años posteriores al año calendario actual; no se presenta como una elección hecha por el usuario.

Una fuente documental confirmada puede determinar una selección cuando exista una relación inequívoca y trazable. Por ejemplo, una Ficha Digital confirmada puede habilitar el detalle del año actual y establecer captura mensual. Esa excepción es un valor derivado de la importación, no un predeterminado silencioso.

**Motivo:** una opción preseleccionada y persistida antes de cualquier decisión puede atribuir al usuario una elección que nunca realizó. A la vez, ocultar que un año o una densidad inicial fueron calculados por la aplicación dificulta auditar la simulación.

**Consecuencia:** Paso 3 exige decisiones explícitas antes de considerarse completo; limpiar datos descendentes vuelve a los estados sin decisión; los valores automáticos tienen una procedencia diferenciada y editable. Esta ADR no altera fórmulas previsionales, normativa ni motores de cálculo.

## ADR-170 — Todo análisis de adjuntos usa un estado de procesamiento global, accesible y no duplicable

**Estado:** Aceptada para UX.4.6f R1.
**Fecha:** 2026-08-20.

**Decisión:** todo control actual o futuro que analice un archivo adjunto debe reutilizar una capa transversal de estado de procesamiento. Al comenzar el análisis debe aparecer inmediatamente el mensaje `Analizando documento… Esto puede tardar unos segundos.`, acompañado de un indicador de actividad; el botón y el selector de archivo quedan temporalmente bloqueados y exponen `aria-busy`. La región de estado usa `role=status`, `aria-live=polite` y `aria-atomic=true`.

Mientras un análisis está activo, una segunda ejecución desde el mismo control se rechaza en el cliente. Al finalizar, los estados habilitado/deshabilitado originales se restauran. Un error específico producido por el importador no debe ser borrado por la limpieza del indicador temporal.

El contrato cubre inicialmente los tres selectores de archivo existentes: importación de Mi Retiro Seguro, importación de Ficha Digital y comprobante de referencia de Mi Retiro Seguro. Cualquier adjunto futuro debe integrarse mediante la misma capa en vez de implementar un indicador ad hoc.

**Motivo:** el análisis de PDFs puede introducir una latencia perceptible. Cambiar solo el texto de un botón no comunica suficientemente que el proceso continúa, favorece dobles clics y ofrece una señal limitada a tecnologías de apoyo.

**Consecuencia:** `attachment_processing.js` se carga de forma global antes de los scripts específicos de cada página. El cambio es exclusivamente de coordinación de interfaz: no modifica validación HTTP, parsers, persistencia de archivos, límites de seguridad ni política de privacidad.


## ADR-171 — Los datos documentales detectados se editan en la ventana de revisión y quedan bloqueados en la vista principal

**Estado:** Aceptada para UX.4.6f R1.1.
**Fecha:** 2026-08-20.

**Decisión:** cuando Mi Retiro Seguro o Ficha Digital aportan un valor identificable, la vista principal de los Pasos 1–6 —y cualquier paso futuro que reutilice este contrato— debe presentarlo como dato documental de solo lectura. La corrección, exclusión o reinclusión de un valor detectado se realiza desde **Revisar importación** y requiere activar explícitamente **Editar campos** antes de confirmar nuevamente la copia de trabajo.

Los campos que el documento **no detectó originalmente** permanecen editables en la vista principal para permitir completar información faltante. La condición de edición depende de la fotografía documental original, no solo de la etiqueta de procedencia vigente: un dato originalmente ausente puede seguir siendo completado manualmente, mientras que un dato originalmente detectado continúa bloqueado aunque haya sido corregido dentro del modal y su estado visible sea `Editado por ti`.

La vista principal conserva la semántica visual transversal de campos no editables: superficie diferenciada y una franja primaria en el borde izquierdo, perceptible en temas Claro, Oscuro y Alto contraste. La señal no depende únicamente del color ni sustituye `readonly`/`disabled`.

La iconografía de procedencia recupera símbolos diferenciados sin círculos decorativos añadidos: `✓` para **Detectado**, `✎` para **Editado por ti** y **Completado manualmente**, `⊘` para **Excluido por ti**, `!` para **No detectado** y `↳` para **Calculado automáticamente**. El símbolo de exclusión forma parte del propio glifo semántico y debe permanecer centrado respecto a la etiqueta.

La importación de registros históricos no responde automáticamente la pregunta **Disponibilidad del historial**. Los registros pueden conservarse en el estado temporal, pero el selector permanece en `Seleccione una opción` hasta que el Asegurado(a) realice una elección explícita. La derivación documental de otros controles solo se mantiene cuando la relación sea inequívoca y esté documentada.

**Motivo:** la revisión manual de R1 mostró que permitir editar en las superficies principales hacía visualmente indistinguible un dato documental confirmado de un dato manual y eliminaba la señal de bloqueo que ya utilizaban los tres temas. También permitía alterar accidentalmente información detectada sin pasar por el flujo de revisión que conserva contexto y procedencia.

**Consecuencia:** ADR-167 queda sustituida parcialmente en su permiso de edición directa desde la vista principal, pero se mantienen vigentes la fotografía original, la copia de trabajo, los estados de procedencia y la capacidad de corregir/excluir/reincluir dentro del modal. ADR-088, ADR-103, ADR-104, ADR-105 y ADR-106 recuperan su criterio de bloqueo visual/funcional en las superficies principales en la medida compatible con esta ADR. Los valores `Calculado automáticamente` —por ejemplo el año inicial del historial o el horizonte salarial— no se consideran datos documentales detectados y conservan su contrato específico de edición cuando corresponda.

## ADR-172 — La línea temporal del Paso 4 exige coherencia entre historial y cuotas y transporta el salario mensual proyectado

**Estado:** Aceptada para UX.4.6f R2.
**Fecha:** 2026-08-20.

**Decisión:** `construir_linea_tiempo()` solo puede materializar una línea temporal integrada cuando el historial anual cubre todo el período declarado, la suma de cuotas coincide con la referencia histórica, esa referencia coincide con `cuotas_totales` del Paso 2 y las cuotas de la fila del año actual coinciden con `cuotas_anio_actual`. Una discrepancia se rechaza antes de combinar información real con proyecciones.

Los registros futuros transportan explícitamente `salario_mensual_proyectado` desde el motor salarial. La interfaz utiliza ese valor como referencia mensual y no lo reconstruye dividiendo un salario cotizado ya prorrateado por la cantidad de cuotas. `salario_proyectado` continúa representando el salario cotizado estimado del período y se prorratea por la densidad de cuotas conforme a ADR-015.

Cuando existen años futuros dentro del horizonte pero `continua_cotizando` es falso, la trayectoria salarial puede seguir existiendo como escenario, pero la línea temporal registra cero cuotas y cero salario cotizado con estado `PROYECTADO_SIN_COTIZACION`. Esto evita presentar como “Proyectado” un período que, según la propia decisión del Asegurado(a), no contiene cotización prevista.

**Motivo:** la auditoría de R2 detectó que una solicitud desincronizada podía combinar las cuotas restantes calculadas desde Paso 2 con una fila anual distinta y producir cierres internamente imposibles. También detectó que la interfaz reconstruía el salario mensual desde un importe ya prorrateado, perdiendo trazabilidad directa respecto al escenario salarial original.

**Consecuencia:** la API de línea temporal se vuelve una frontera de coherencia y no depende únicamente de que el navegador haya ejecutado validaciones previas. `RegistroLineaTiempo` incorpora un campo mensual opcional para conservar compatibilidad con fotografías históricas y objetos de pruebas anteriores. No se modifican las fórmulas previsionales de SEBD, Mixto o SUCGS.

## ADR-173 — El Paso 4 no extrapola silenciosamente un salario futuro conocido y registra el origen del horizonte

**Estado:** Aceptada para UX.4.6f R2.
**Fecha:** 2026-08-20.

**Decisión:** la modalidad `FUTURO_CONOCIDO` deriva una tasa anual compuesta únicamente entre el salario base y el año/monto futuro aportado por el Asegurado(a). El monto del año objetivo se materializa exactamente; si el horizonte de Paso 4 continúa después, ese salario se mantiene constante hasta el final del horizonte en lugar de prolongar silenciosamente la tasa inferida.

Las modalidades `PORCENTAJE` y `ESCENARIOS` siguen siendo compuestas: cada año posterior parte del salario proyectado del año anterior. La interfaz debe explicarlo junto al control correspondiente. En `ESCENARIOS` no se precargan tasas sugeridas: el campo inicia vacío y el contrato de datos usa una lista vacía hasta que el Asegurado(a) indique explícitamente qué porcentajes desea comparar.

Cuando Paso 5 detecta que un escenario de retiro queda fuera de la proyección y el Asegurado(a) utiliza la acción para ampliar el horizonte, Paso 4 registra `AJUSTADO_DESDE_RETIRO`, conserva el nuevo año final como borrador y muestra una procedencia específica. Si el usuario modifica después el año, la procedencia pasa a `EDITADO_USUARIO`.

**Motivo:** ADR-018 prohíbe extrapolar salarios silenciosamente fuera de un horizonte confirmado. Extender indefinidamente la CAGR inferida desde un único salario futuro añadía una hipótesis que el usuario no había proporcionado. Del mismo modo, etiquetar un horizonte ampliado desde Paso 5 como si siguiera siendo la sugerencia inicial de cinco años ocultaba la causa real del valor.

**Consecuencia:** conocer un salario futuro no equivale a declarar una tasa permanente después de ese año. Quien desee crecimiento posterior puede usar `PORCENTAJE` o `ESCENARIOS`, o ajustar explícitamente sus supuestos. La procedencia del horizonte permanece auditable durante la navegación entre Pasos 4 y 5.

## ADR-174 — Paso 5 deriva sugerencias posteriores desde Paso 4 sin convertirlas en decisiones del usuario

**Estado:** Aceptada para UX.4.6g R1.
**Fecha:** 2026-08-20.

**Decisión:** la edad de referencia es el único escenario seguro por defecto. Los escenarios `+1` a `+5` se marcan automáticamente solo cuando la fecha correspondiente queda cubierta por el año final realmente generado en Paso 4. La interfaz identifica esa selección como `SUGERIDO_PASO4`. Si el Asegurado(a) marca o desmarca una alternativa, la procedencia cambia a `EDITADO_USUARIO` y futuras sincronizaciones no sobrescriben esa decisión.

La omisión histórica de `+4` se corrige para que la secuencia posterior sea continua. El modelo HTTP tampoco conserva la antigua lista fija de escenarios: `DatosRetiro.anios_adicionales` usa `[0]` como valor seguro cuando el cliente no envía una selección.

**Motivo:** una casilla marcada por HTML no demuestra intención del usuario. Paso 4 sí aporta un contexto útil —el horizonte salarial confirmado—, pero ese contexto debe presentarse como sugerencia explicada y reversible, no como una decisión atribuida al Asegurado(a).

**Consecuencia:** la selección contextual vive en estado temporal separado del resultado legal y puede ser auditada como sugerencia o edición. Si el usuario mantiene una selección que rebasa Paso 4, la advertencia de cobertura existente continúa siendo la barrera de coherencia.

## ADR-175 — El retiro anticipado se compara solo por decisión explícita y las fechas transcurridas no son acciones futuras

**Estado:** Aceptada para UX.4.6g R1.
**Fecha:** 2026-08-20.

**Decisión:** los escenarios estándar `-2` y `-1` años permanecen desmarcados hasta una acción explícita. Paso 5 calcula sus fechas exactas y deshabilita cualquier alternativa cuya fecha sea anterior a la fecha de evaluación. Cuando la fecha de evaluación está dentro de la banda anticipada estándar versionada, la interfaz puede ofrecer **Retirarme en la fecha de evaluación** como escenario adicional opcional.

El backend valida esa opción contra `maximo_anios_anticipacion` de `regulations/sebd.json`; fuera de la banda se rechaza. Generar el escenario no afirma elegibilidad: el Paso 6 y los motores legales conservan la clasificación de modalidad, cuotas y factores de reducción. Para SUCGS u otros contextos en los que la modalidad no corresponda, la existencia de una fecha comparativa no crea un derecho.

**Motivo:** disponibilidad normativa y decisión del usuario son conceptos distintos. Además, presentar 2024 o 2025 como una decisión futura en una evaluación de 2026 induce a error aunque la fecha pueda conservar valor histórico o comparativo.

**Consecuencia:** la interfaz distingue opción futura, fecha transcurrida y fecha de evaluación dentro de banda. La fecha personalizada permanece disponible para comparaciones específicas y la clasificación jurídica sigue centralizada en los motores del Paso 6.
## ADR-176 — Los campos de fecha usan validación calendárica transversal y ancho compacto

**Estado:** Aceptada para UX.4.6g R1.
**Fecha:** 2026-08-21.

**Decisión:** todos los controles actuales y futuros `input[type=date]` se integran mediante una regla transversal en `accessibility.js`. Cuando el control no declara límites más específicos, la interfaz aplica `1900-01-01` como mínimo y `2200-12-31` como máximo, exige un año de exactamente cuatro dígitos y verifica que día/mes/año materialicen una fecha real del calendario. Un valor con año de más de cuatro dígitos o una entrada nativa inválida no puede conservarse como fecha válida.

Los mismos controles reciben la clase `app-date-input`, que limita su ancho en escritorio y recupera ancho completo en pantallas pequeñas. La regla se aplica también a controles de fecha incorporados dinámicamente, por lo que futuros pasos no deben implementar validadores o anchos ad hoc salvo que exista una necesidad funcional más restrictiva.

En Paso 5, la fecha personalizada informa de forma visible si queda cubierta por el horizonte salarial vigente o si lo supera. La detección de la edad de referencia en frontend reconoce tanto las formas largas `FEMENINO`/`MASCULINO` como las abreviaturas persistidas `F`/`M`; esta normalización no modifica el sexo almacenado ni las reglas de los motores.

**Motivo:** los controles nativos de fecha pueden permitir introducir manualmente años con más de cuatro dígitos según navegador/locale y un campo innecesariamente ancho dificulta la lectura de formularios. Además, la revisión manual de UX.4.6g mostró que una abreviatura `F` impedía mostrar la opción de retiro en la fecha de evaluación aunque el caso estuviera dentro de la banda anticipada.

**Consecuencia:** la validación de fechas pasa a ser una responsabilidad transversal de interfaz, con semántica y geometría comunes. Los límites específicos que ya existan en un campo conservan prioridad; la validación jurídica y previsional continúa en backend.

## ADR-177 — Los bloques comparables conservan alineación y densidad visual en escritorio

**Estado:** Aceptada para UX.4.6g R1.4.3.
**Fecha:** 2026-08-21.

**Decisión:** los pares visuales Año inicial/Período del historial y Año inicial/Proyectar hasta el año deben alinear sus superficies de captura o resumen en la misma línea visual. El resumen contextual del Paso 5 distribuye el ancho de escritorio según la longitud real de sus etiquetas: Sexo usa una columna más estrecha y Cierre esperado este año recibe espacio adicional para evitar saltos de línea innecesarios. En móvil se conserva el apilado responsive.

**Motivo:** la validación manual mostró desalineaciones entre controles equivalentes y un salto de línea evitable en el resumen de retiro, pese a existir ancho horizontal disponible. La geometría debe facilitar comparación rápida sin aumentar altura ni alterar contenido funcional.

**Consecuencia:** este ajuste es exclusivamente de presentación; no modifica estados, fórmulas, normativa ni resultados previsionales.

## ADR-178 — La guía pública explica parámetros versionados sin convertirse en un segundo motor

**Estado:** Aceptada para UX.4.6i R1–R1.4.
**Fecha:** 2026-08-21.

**Decisión:** la sección pública `/como-se-calcula` describe el orden de operaciones de SEBD, Subsistema Mixto y SUCGS, pero no ejecuta prestaciones. `app/services/calculation_guide.py` puede leer y estructurar parámetros de `regulations/*.json`; no importa motores previsionales ni reconstruye resultados personales. Las fórmulas ejecutables permanecen en Python dentro de los motores existentes y la sustitución con cifras de una simulación continúa en la trazabilidad del Paso 6.

La guía reutiliza `construir_catalogo_metodologia()` para las fuentes oficiales y el Paso 6 enlaza únicamente mediante el identificador público del sistema (`#sebd`, `#mixto`, `#sucgs`). No se serializan datos personales, salarios, cuotas ni montos de la simulación en la URL.

**Motivo:** la transparencia exige que una persona pueda comprender y reproducir el procedimiento general, pero duplicar lógica normativa en JavaScript o en una segunda calculadora introduciría riesgo de divergencia entre explicación y motor. La vinculación por sistema permite contextualizar la ayuda sin ampliar la superficie de datos personales.

**Consecuencia:** cualquier cambio futuro en reglas, parámetros, trazabilidad o fuentes debe revisar también la guía pública. Los ejemplos permanecen ilustrativos y cualquier parámetro hipotético debe identificarse expresamente como no oficial.

**Refinamiento R1.2:** la guía se incorpora también a la navegación principal con estado activo propio y hace explícita la transformación de datos entre los Pasos 1–6. Las tablas extensas de factores se compactan únicamente mediante CSS responsive y los importes de esta guía usan separador de miles y dos decimales; estos cambios no modifican parámetros, fórmulas ni resultados.

**Refinamiento R1.3:** la explicación conserva cada fórmula general y añade debajo una sustitución numérica marcada como ejemplo. Los términos previsionales se definen dentro de la sección donde se utilizan, evitando un glosario aislado y evitando también replicarlos todavía por todo el asistente. El espaciado de tablas, notas y fuentes se ajusta con tokens semánticos; no se modifica ningún motor ni parámetro normativo.


## ADR-179 — El versionado beta usa un ledger de estados aceptados y no cuenta commits como revisiones

**Estado:** Aceptada; reconciliada documentalmente por AUD.SEC2 R1.
**Fecha:** 2026-08-21; reconciliación 2026-08-25.

**Decisión:** durante la etapa beta, los estados nuevos usan `0.GG.RR.EE-beta` y el contador global consume únicamente estados materialmente distintos y aceptados. Commits, PR, squash, CI y tags son evidencia del estado, no revisiones adicionales por sí solos.

La segunda pasada de VER.2 fijó G070 sobre `7037addd`. AUD.SEC2 R1 reconstruyó los estados posteriores hasta G108, preservó `v0.0.71.01-beta` como tag publicado e inmutable con anomalía histórica de numeración y quedó aceptado como G109/E01 (`0.1.09.01-beta`) mediante PR #83; G110/E01 quedó aceptado como REL.GOV.1 mediante PR #85 y merge `5cd1cea`; G111/E01 (`0.1.11.01-beta`) quedó aceptado como DOC.2 mediante PR #87 y merge `1041b59`; G112/E07 (`0.1.12.07-beta`) queda aceptado para NOR.1 R8; G113/E03 (`0.1.13.03-beta`) queda reservado para DOC.1 R3 antes de PERSIST.1.

El detalle, alternativas y evidencia completa permanecen en [`adr-179-revision-aware-versioning.md`](adr-179-revision-aware-versioning.md).
