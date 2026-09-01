# Normativa

**Estado:** Vigente
**Versión de aplicación revisada:** `0.1.19.05-beta`
**Versión base histórica:** `0.0.23-beta`
**Revisión documental base:** GOV.1.3 R3 — 2026-08-17
**Última revisión documental:** Reconciliación post-G119 — 2026-08-30
**Clasificación:** Normativa / Técnica / Pública
**Revisión externa:** Pendiente en REV.1 antes de la primera versión oficial o de un despliegue/distribución que cambie materialmente el riesgo jurídico

Este documento describe cómo Mi Retiro Proyectado interpreta y versiona las reglas previsionales implementadas. No sustituye el texto legal, un reglamento, una resolución de la CSS ni una determinación individual.

[Índice](../README.md) · [Fuentes oficiales](regulatory-sources.md) · [Decisiones](../decisions/README.md)

## 1. Jerarquía documental

Para una regla previsional se prioriza:

1. Texto Único vigente de la Ley 51 de 2005 y sus reformas;
2. leyes especiales/reformatorias cuando sea necesario estudiar el origen del cambio;
3. reglamentos y resoluciones de la CSS;
4. páginas institucionales para orientación operativa;
5. comunicaciones oficiales para fechas o procedimientos temporales.

Una comunicación operativa no sustituye una disposición legal o reglamentaria.

## 2. Fuente base

El proyecto utiliza como referencia consolidada el **Texto Único de la Ley 51 de 2005, Orgánica de la Caja de Seguro Social**, con reformas aprobadas por las Leyes 2 de 2007, 70 de 2011, 45 de 2017, 419 de 2024 y 462 de 2025, publicado en la **Gaceta Oficial 30284-B de 22 de mayo de 2025**.

Fuentes oficiales:

- CSS: <https://www.css.gob.pa/normativas-ley-organica/>
- Texto Único PDF: <https://www.css.gob.pa/wp-content/uploads/2025/05/TEXTO-UNICO-DE-LA-LEY-51-DE-2005-CSS-GACETA-OFICIAL-22-5-25.pdf>
- Gaceta Oficial: <https://www.gacetaoficial.gob.pa/pdfTemp/30284_B/GacetaNo_30284b_20250522.pdf>

**Metadata de la fuente base:** `fecha_gaceta = 2025-05-22`.

**Última verificación documental:** 2026-08-17.

## 3. Contrato de versionado normativo

| Archivo | Alcance |
| --- | --- |
| `regulations/general-parameters.json` | Edades de referencia y metadatos generales. |
| `regulations/sebd.json` | SEBD, anticipación, mínimos/máximos e indemnización. |
| `regulations/mixto.json` | BD, CAP, transición y fuentes del Mixto. |
| `regulations/sucgs.json` | SUCGS, factores y garantías modeladas. |

Los JSON son parámetros de implementación, no sustitutos de la fuente oficial.

Cuando un monto, factor o fecha sea actualizable, debe conservar fuente y fecha. No se convierte en constante eterna.

## 4. Parámetros generales

El archivo vigente versiona:

- edad de referencia femenina: 57 años;
- edad de referencia masculina: 62 años;
- anticipación operativa de solicitud: 3 meses;
- Texto Único/Gaceta de referencia.

Los motores usan fechas completas cuando la regla depende del momento efectivo.

## 5. SEBD

Artículos principales documentados: **178, 179, 180, 181, 186, 192 y 193**.

Contrato técnico vigente:

- referencia general de 240 cuotas para pensión normal;
- umbral modelado de 180 cuotas para modalidades proporcionales;
- salario base conforme al criterio de mejores años implementado;
- factores anticipados almacenados por mes;
- Indemnización por Vejez separada como pago único;
- mínimo del artículo 192 no tratado como monto vigente eterno;
- máximos del artículo 193 sujetos a sus condiciones.

El historial anual puede introducir aproximaciones frente a un detalle mensual oficial. Esa limitación debe permanecer visible.

Consultar [Modalidades de retiro por vejez — SEBD](sebd-modalities.md).

## 6. Subsistema Mixto

El motor mantiene separados:

- Componente de Beneficio Definido;
- Componente de Ahorro Personal.

El CAP requiere saldo y parámetros individualizados cuando no puedan reconstruirse con fidelidad. La aplicación no fabrica una cuenta individual desde salarios anuales.

### 6.1. Transición

`regulations/mixto.json` conserva:

- fin del cálculo operativo Mixto: 29/02/2032;
- inicio operativo SUCGS: 01/03/2032;
- referencia distinta a 01/03/2036 presente en el artículo 153.

La discrepancia permanece explícita y vinculada al ADR correspondiente; no se armoniza silenciosamente.

### 6.2. Fecha operativa de 2026 y discrepancia documental

La CSS comunicó durante 2026 el **18/08/2026** como fecha límite operativa
para asegurados habilitados para ejercer la opción de sistema. Esa fecha ya
transcurrió y se conserva únicamente como antecedente operativo.

Las comunicaciones institucionales inmediatamente anteriores al vencimiento
reiteraron el 18 de agosto de 2026.

Sin embargo, el artículo 4 del Reglamento de Incorporación al Componente
Contributivo de Capitalización Solidaria, Resolución 57,805-2025-J.D.,
publicado en Gaceta Oficial 30314 de 3 de julio de 2025, contiene la fecha
**17/03/2026**.

El proyecto conserva ambas evidencias y no inventa una reconciliación
jurídica entre ellas.

Antes de utilizar nuevamente una fecha de opción en producto, documentación
orientada a una decisión individual o lógica ejecutable debe identificarse
la fuente jurídica vigente que explique, modifique o sustituya esa diferencia.

Fuentes:

- <https://www.gacetaoficial.gob.pa/storage/gacetas/2025/07/30314/GacetaNo_30314_20250703.pdf>
- <https://prensa.css.gob.pa/2026/07/10/css-intensifica-jornadas-de-capacitacion-sobre-mi-retiro-seguro-ante-la-fecha-clave-del-18-de-agosto/>
- <https://prensa.css.gob.pa/2026/07/13/cuenta-regresiva-hacia-el-18-de-agosto-asegurados-deben-decidir-su-futuro-pensional/>
- <https://prensa.css.gob.pa/2026/08/15/css-extendera-atencion-este-domingo-para-orientar-a-los-asegurados-sobre-mi-retiro-seguro/>
- <https://prensa.css.gob.pa/2026/08/18/css-realiza-capacitaciones-sobre-pensiones-con-jornada-en-el-organo-judicial/>

Última verificación documental: **2026-08-30**.

Consultar [Subsistema Mixto — diseño y alcance del motor](mixto-modalities.md).

## 7. SUCGS

Artículos principales versionados: **152, 153 y 194–198**.

El modelo separa:

- componente contributivo;
- componente solidario no contributivo;
- Pensión Garantizada Solidaria;
- garantía de reemplazo modelada.

Los factores actuariales se cargan desde `regulations/sucgs.json`. La propia metadata normativa indica que requieren actualización periódica.

Los valores de referencia indexables no se presentan como vigentes para siempre.

Consultar [Sistema Único de Capitalización con Garantía Solidaria (SUCGS)](sucgs-modalities.md).

## 8. Datos individualizados no inferibles

Saldo CAP, bono, divisor actuarial, saldo solidario y cualquier otro dato individual que no pueda determinarse con seguridad deben permanecer como:

- dato oficial suministrado;
- dato confirmado;
- o dato pendiente.

No se utilizan valores personales de casos de prueba como parámetros de producción.

## 9. Regímenes especiales

El motor general no afirma cubrir todos los regímenes especiales.

Antes de incorporar uno se requiere:

1. fuente oficial;
2. identificación inequívoca del régimen;
3. parámetros propios;
4. pruebas independientes;
5. actualización de documentación y trazabilidad.

## 10. Decisiones interpretativas

Una decisión técnica frente a una ambigüedad debe registrarse en `docs/decisions/README.md`.

Una ADR:

- explica la decisión de implementación;
- no crea una norma;
- no sustituye revisión jurídica;
- debe enlazarse con la fuente oficial que originó la decisión.

## 11. Mantenimiento

Ante un cambio normativo o reglamentario:

1. verificar fuente oficial y vigencia;
2. conservar trazabilidad de la versión anterior cuando sea necesaria;
3. actualizar `regulations/*.json`;
4. actualizar motores/servicios afectados;
5. actualizar pruebas;
6. actualizar `regulatory-sources.md`;
7. registrar ADR cuando exista interpretación;
8. actualizar changelog/versionado según corresponda.

## 12. Frontera documental y revisión externa

GOV.1.3 R3 realizó **alineación documental**. No declaró certificación jurídica ni resolvió por sí sola las discrepancias normativas ya documentadas.

GOV.1.5 completó posteriormente una revisión interna de seguridad, privacidad y riesgo, pero no constituyó una revisión jurídica externa.

La revisión jurídica profesional permanece pendiente en REV.1 antes de la primera versión oficial o antes de un despliegue, distribución o tratamiento que cambie materialmente el modelo de riesgo.

## 13. Historia

La versión acumulativa previa se conserva en:

`docs/archive/regulatory-privacy/regulatory-framework-pre-gov1-3-r3.md`
