# Fuentes normativas y enlaces oficiales

**Estado:** Vigente
**Versión de aplicación revisada:** `0.0.23-beta`
**Revisión documental:** GOV.1.3 R3 — 2026-08-17
**Clasificación:** Normativa / Técnica / Pública
**Última verificación documental de enlaces clave:** 2026-08-17

Este catálogo organiza las fuentes oficiales utilizadas por la documentación y la implementación. No convierte páginas informativas o notas de prensa en normas jurídicas.

## 1. Prioridad

1. Texto Único/Ley/Gaceta;
2. reglamentos y resoluciones;
3. páginas institucionales de prestaciones;
4. comunicaciones oficiales para información operativa temporal.

## 2. Texto Único y reforma principal

- CSS — Normativas Ley Orgánica: https://www.css.gob.pa/normativas-ley-organica/
- Texto Único Ley 51 PDF: https://www.css.gob.pa/wp-content/uploads/2025/05/TEXTO-UNICO-DE-LA-LEY-51-DE-2005-CSS-GACETA-OFICIAL-22-5-25.pdf
- Gaceta Oficial 30284-B: https://www.gacetaoficial.gob.pa/pdfTemp/30284_B/GacetaNo_30284b_20250522.pdf
- Ley 462 de 2025: https://www.css.gob.pa/wp-content/uploads/2025/03/Ley-462-de-2025.pdf

La CSS identifica el Texto Único como Ley 51 de 2005 con reformas aprobadas por las Leyes 2 de 2007, 70 de 2011, 45 de 2017, 419 de 2024 y 462 de 2025.

## 3. Prestaciones Económicas

- Normativa de Prestaciones Económicas: https://www.css.gob.pa/normativa-prestaciones-economicas/
- Resolución 39,302-2007-J.D.: https://w3.css.gob.pa/wp-content/wdocs/Resolucion%20%2039%2C302-2007-J.D..pdf
- Pensión por Vejez: https://www.css.gob.pa/pension-por-vejez/
- Pensión por Vejez Anticipada: https://www.css.gob.pa/pension-por-vejez-anticipada/
- Pensión por Vejez Proporcional: https://www.css.gob.pa/pension-por-vejez-proporcional/
- Pensión Proporcional Anticipada: https://www.css.gob.pa/pension-por-vejez-proporcional-anticipada/

## 4. Subsistema Mixto

- Reglamento de Incorporación al Subsistema Mixto: https://w3.css.gob.pa/wp-content/wdocs/REGLAMENTO%20DE%20INCORPORACION%20AL%20SUBSISTEMA%20MIXTO.pdf
- Resolución 39,470-2007-J.D.: https://w3.css.gob.pa/wp-content/wdocs/RES%2039470-2007-JD.pdf
- Resolución 41,055-2009-J.D.: https://w3.css.gob.pa/wp-content/wdocs/RES%2041%2C055-2009-J.D..pdf
- Reglamento de Seguros Colectivos CAP: https://www.css.gob.pa/wp-content/uploads/2023/10/REGLAMENTO-DE-SEGUROS-COLECTIVOS-DEL-COMPONENTE-DE-AHORRO-PERSONAL-DEL-SUBSISTEMA-MIXTO-actualizado.pdf
- Reglamento de Incorporación al CCCS: https://www.css.gob.pa/wp-content/uploads/2025/07/REGLAMENTO-DE-INCORPORACION-AL-CCCS.pdf

## 5. Fecha operativa de opción — 2026

La CSS continúa señalando el **18/08/2026 (18 de agosto de 2026)** como fecha límite operativa para los asegurados que cumplen los requisitos correspondientes.

Fuentes verificadas el 2026-08-17:

- https://prensa.css.gob.pa/2026/07/10/css-intensifica-jornadas-de-capacitacion-sobre-mi-retiro-seguro-ante-la-fecha-clave-del-18-de-agosto/
- https://prensa.css.gob.pa/2026/07/13/cuenta-regresiva-hacia-el-18-de-agosto-asegurados-deben-decidir-su-futuro-pensional/

**Clasificación:** información operativa temporal. Debe volver a verificarse antes de una decisión individual y no se trata como regla normativa permanente.

## 6. SUCGS

Fuente legal principal:

- Texto Único/Gaceta de la sección 2;
- Reglamento de Incorporación al CCCS: https://www.css.gob.pa/wp-content/uploads/2025/07/REGLAMENTO-DE-INCORPORACION-AL-CCCS.pdf

Los artículos utilizados por el motor están documentados en `NORMATIVA.md` y `MODALIDADES_SUCGS.md`.

## 7. Regímenes especiales identificados

- Trabajadores estacionales agrícolas y de la construcción: https://www.css.gob.pa/pension-por-vejez-para-los-trabajadores-estacionales-agricolas-y-de-la-construccion/

Su existencia demuestra que el motor general no debe presentarse como universal para toda categoría de asegurado.

## 8. Verificación individual

Mi Caja Digital es un recurso de consulta individual, no una fuente normativa del motor:

- https://micajadigital.css.gob.pa/Auth/SignIn

## 9. Protección de datos personales

Fuentes de referencia del bloque de privacidad:

- ANTAI — Protección de Datos Personales: https://antai.gob.pa/preguntas-frecuentes-proteccion-de-datos-personales/
- ANTAI — Preguntas frecuentes y plazos de derechos: https://antai.gob.pa/preguntas-frecuentes-de-proteccion-de-datos-personales/
- ANTAI — Reglamentación Ley 81 / Decreto Ejecutivo 285: https://antai.gob.pa/reglamentan-ley-81-de-proteccion-de-datos-personales/

La documentación del producto se mantiene en:

- `POLITICA_PRIVACIDAD.md`;
- `TERMINOS_USO_PRIVACIDAD.md`;
- `CUMPLIMIENTO_LEY_81.md`;
- `SEGURIDAD_PRIVACIDAD.md`.

## 10. Uso por la interfaz

Los enlaces normativos que necesita la aplicación se cargan desde `normativa/*.json` y se transforman en títulos humanos mediante `app/servicios/fuentes_normativas.py`.

Los IDs internos no deben mostrarse como si fueran nombres de fuentes.

## 11. Regla de mantenimiento

Cuando cambie una fuente, enlace, monto indexado, tabla o fecha operativa:

1. verificar la publicación oficial;
2. registrar fecha de revisión;
3. actualizar JSON/documentación/pruebas afectados;
4. conservar la referencia anterior cuando sea necesaria para reproducibilidad;
5. diferenciar fuente jurídica de comunicación operativa.

## 12. Historia

Snapshot anterior:

`docs/historico/normativa_privacidad/FUENTES_NORMATIVAS_PRE_GOV1_3_R3.md`
