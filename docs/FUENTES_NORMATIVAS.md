# Fuentes normativas y enlaces oficiales

> Documento de referencia del proyecto. La lógica de cálculo debe remitirse a estas fuentes o a una fuente oficial posterior debidamente versionada.

## 1. Criterio de prioridad de fuentes

Para documentar o modificar una regla previsional se utiliza, en este orden:

1. **Texto Único vigente de la Ley 51 de 2005** publicado por la Caja de Seguro Social (CSS) y en la Gaceta Oficial.
2. **Reglamentos y resoluciones de la Junta Directiva de la CSS** que desarrollan el cálculo o la incorporación a un sistema.
3. **Páginas institucionales de Prestaciones Económicas** como apoyo operativo y de orientación.
4. **Comunicaciones oficiales de la CSS** para fechas, procedimientos o aclaraciones operativas que puedan cambiar con el tiempo.

Una nota de prensa o página informativa nunca sustituye una regla legal o reglamentaria cuando ambas existen.

## 2. Texto Único de la Ley 51 y reformas incorporadas

### 2.1. Texto Único vigente utilizado por el proyecto

- **Texto Único de la Ley 51 de 2005, Orgánica de la Caja de Seguro Social**, con reformas aprobadas por las Leyes 2 de 2007, 70 de 2011, 45 de 2017, 419 de 2024 y 462 de 2025.
- **Gaceta Oficial:** 30284-B, 22 de mayo de 2025.
- [Página oficial de normativa de la Ley Orgánica — CSS](https://www.css.gob.pa/normativas-ley-organica/)
- [PDF oficial del Texto Único — CSS](https://www.css.gob.pa/wp-content/uploads/2025/05/TEXTO-UNICO-DE-LA-LEY-51-DE-2005-CSS-GACETA-OFICIAL-22-5-25.pdf)
- [Gaceta Oficial 30284-B — PDF](https://www.gacetaoficial.gob.pa/pdfTemp/30284_B/GacetaNo_30284b_20250522.pdf)

Para localizar una disposición concreta en el PDF, buscar por `Artículo NNN` con `Ctrl+F`.

### 2.2. Ley 462 de 18 de marzo de 2025

Es la reforma que introdujo, entre otros cambios, el Sistema Único de Capitalización con Garantía Solidaria y modificó reglas del programa de Invalidez, Vejez y Muerte.

- [Ley 462 de 2025 — PDF oficial CSS/Gaceta](https://www.css.gob.pa/wp-content/uploads/2025/03/Ley-462-de-2025.pdf)
- [Página oficial de normativa de la Ley Orgánica — CSS](https://www.css.gob.pa/normativas-ley-organica/)

Las demás leyes incorporadas al Texto Único se consultan desde la misma página oficial de la CSS. El proyecto usa como referencia preferente el Texto Único consolidado, salvo que se necesite estudiar la historia de una modificación.

## 3. Mapa de artículos usados por el motor SEBD

| Artículo | Uso en la aplicación | Estado |
|---|---|---|
| 178 | Condiciones generales de retiro por vejez | Implementado |
| 179 | Edad de referencia y reglas relacionadas | Implementado |
| 180 | Salario base y diez mejores años | Implementado con historial anual; años parciales documentados |
| 181 | Normal, anticipada, proporcional, proporcional anticipada e incrementos por cuotas | Implementado |
| 186 | Indemnización por Vejez y transición desde 01/03/2036 | Implementado |
| 192 | Monto mínimo sujeto a ajuste anual | Referenciado; no se fuerza un valor indexado no versionado |
| 193 | Límites máximos ordinario y ampliados | Implementado según condiciones disponibles |

Fuentes complementarias:

- [Normativa de Prestaciones Económicas — CSS](https://www.css.gob.pa/normativa-prestaciones-economicas/)
- [Resolución 39,302-2007-J.D. — CSS](https://w3.css.gob.pa/wp-content/wdocs/Resolucion%20%2039%2C302-2007-J.D..pdf)

En la página de Prestaciones Económicas, consultar la sección **“Reglamento para el Cálculo de Prestaciones Económicas”**, donde la CSS lista la Resolución 39,302-2007-J.D. y sus modificaciones, entre ellas las Resoluciones 34,199-2003-J.D., 39,389-2007-J.D., 40,378-2008-J.D., 52,690-2018-J.D., 52,872-2018-J.D. y 8008-93-J.D.

Páginas oficiales de orientación:

- [Pensión por Vejez](https://www.css.gob.pa/pension-por-vejez/)
- [Pensión por Vejez Anticipada](https://www.css.gob.pa/pension-por-vejez-anticipada/)
- [Pensión por Vejez Proporcional](https://www.css.gob.pa/pension-por-vejez-proporcional/)
- [Pensión por Vejez Proporcional Anticipada](https://www.css.gob.pa/pension-por-vejez-proporcional-anticipada/)

## 4. Mapa de artículos y reglamentos usados por el Subsistema Mixto

| Artículo | Uso en la aplicación | Estado |
|---|---|---|
| 155 | Ámbito del Subsistema Mixto | Referenciado |
| 178–181 | Modalidades y reglas del Componente de Beneficio Definido | Implementado |
| 182 | Pensión programada del Componente de Ahorro Personal (CAP) | Implementado cuando se suministra el divisor actuarial aplicable |
| 183 | Bono de reconocimiento | Se acepta monto oficial/validado; no se reconstruye automáticamente |
| 184 | Seguro Colectivo de Renta Vitalicia | Modelado como garantía futura, no como aumento inicial |
| 185 | Reglas concordantes del Mixto | Referenciado |
| 186 | Indemnización del Componente de Beneficio Definido | Implementado |
| 187 | Devolución total del CAP | Implementado como opción expresa y pago único |
| 188 | Transición y opción hacia el componente de capitalización solidaria | Implementado con discrepancia documentada |
| 192–193 | Mínimos/máximos aplicables al componente definido | Aplicados según el alcance disponible |

### 4.1. Incorporación al Subsistema Mixto

- [Reglamento de Incorporación al Subsistema Mixto — PDF CSS](https://w3.css.gob.pa/wp-content/wdocs/REGLAMENTO%20DE%20INCORPORACION%20AL%20SUBSISTEMA%20MIXTO.pdf)
- [Resolución 39,470-2007-J.D. — PDF CSS](https://w3.css.gob.pa/wp-content/wdocs/RES%2039470-2007-JD.pdf)
- [Resolución 41,055-2009-J.D. — PDF CSS](https://w3.css.gob.pa/wp-content/wdocs/RES%2041%2C055-2009-J.D..pdf)
- [Normativa de Prestaciones Económicas — CSS](https://www.css.gob.pa/normativa-prestaciones-economicas/)

### 4.2. Seguros colectivos del CAP

- [Reglamento de Seguros Colectivos del Componente de Ahorro Personal del Subsistema Mixto — edición actualizada](https://www.css.gob.pa/wp-content/uploads/2023/10/REGLAMENTO-DE-SEGUROS-COLECTIVOS-DEL-COMPONENTE-DE-AHORRO-PERSONAL-DEL-SUBSISTEMA-MIXTO-actualizado.pdf)
- [Ley 58 de 2008 — PDF CSS](https://w3.css.gob.pa/wp-content/wdocs/LEY%2058%20DE%202008.pdf)
- [Normativa de Prestaciones Económicas — CSS](https://www.css.gob.pa/normativa-prestaciones-economicas/)

### 4.3. Incorporación al Componente Contributivo de Capitalización Solidaria

- **Resolución 57,805-2025-J.D., de 1 de julio de 2025.**
- [Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria — PDF CSS](https://www.css.gob.pa/wp-content/uploads/2025/07/REGLAMENTO-DE-INCORPORACION-AL-CCCS.pdf)
- [Normativa de Prestaciones Económicas — CSS](https://www.css.gob.pa/normativa-prestaciones-economicas/)

El artículo 5 del reglamento dispone que la prestación de quienes permanezcan en el Subsistema Mixto y la soliciten hasta el 29/02/2032 se calcula bajo las reglas del Mixto; desde el 01/03/2032 remite al artículo 196 y concordantes del SUCGS. El proyecto conserva, sin ocultarla, la referencia distinta a 01/03/2036 que aparece en el artículo 153 del Texto Único.

### 4.4. Fecha operativa de opción comunicada por la CSS en 2026

La Resolución 57,805-2025-J.D. publicada en 2025 contiene originalmente el 17/03/2026. Comunicaciones oficiales posteriores de la CSS utilizan el **18/08/2026** como fecha límite operativa para quienes cumplan los requisitos de la opción.

- [CSS — fecha clave del 18 de agosto de 2026 y alcance para personas del Sistema Mixto](https://prensa.css.gob.pa/2026/07/10/css-intensifica-jornadas-de-capacitacion-sobre-mi-retiro-seguro-ante-la-fecha-clave-del-18-de-agosto/)
- [CSS — cuenta regresiva hacia el 18 de agosto](https://prensa.css.gob.pa/2026/07/13/cuenta-regresiva-hacia-el-18-de-agosto-asegurados-deben-decidir-su-futuro-pensional/)

**Regla de documentación:** esta fecha es operativa y temporal. Debe volver a verificarse antes de usarla en una decisión individual.

## 5. Mapa de artículos usados por el SUCGS

| Artículo | Uso en la aplicación | Estado |
|---|---|---|
| 152 | Estructura del SUCGS | Referenciado |
| 153 | Ámbito/transición; contiene referencia temporal que se documenta junto al art. 188 | Referenciado |
| 194 | Componente Solidario No Contributivo y Beneficio Mínimo | Implementado con valores versionados/confirmables |
| 195 | Pensión Garantizada Solidaria | Implementado |
| 196 | Saldo ÷ 1,000 × factor actuarial y tabla de factores | Implementado |
| 197 | Garantía de reemplazo mínimo | Implementado con preevaluación conservadora y confirmación explícita de estabilidad salarial |
| 198 | Reglas concordantes del sistema | Referenciado |
| Art. 1, num. 41 | Definición usada para salario promedio base | Implementado |

Fuente principal:

- [Texto Único de la Ley 51 — PDF CSS](https://www.css.gob.pa/wp-content/uploads/2025/05/TEXTO-UNICO-DE-LA-LEY-51-DE-2005-CSS-GACETA-OFICIAL-22-5-25.pdf)
- [Gaceta Oficial 30284-B — PDF](https://www.gacetaoficial.gob.pa/pdfTemp/30284_B/GacetaNo_30284b_20250522.pdf)

Reglamento de transición relevante:

- [Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria — PDF CSS](https://www.css.gob.pa/wp-content/uploads/2025/07/REGLAMENTO-DE-INCORPORACION-AL-CCCS.pdf)

## 6. Regímenes especiales identificados pero fuera del motor general actual

La aplicación no debe presentar el motor general SEBD como universal para toda categoría de asegurado. Entre los regímenes que requieren tratamiento específico está la pensión de trabajadores estacionales agrícolas y de construcción de menor calificación.

- [Pensión por Vejez para Trabajadores Estacionales Agrícolas y de la Construcción — CSS](https://www.css.gob.pa/pension-por-vejez-para-los-trabajadores-estacionales-agricolas-y-de-la-construccion/)

Otros regímenes especiales deberán incorporarse solo después de documentar su fuente y sus pruebas propias.

## 7. Herramientas oficiales de verificación del asegurado

Estas herramientas son de orientación/verificación individual y no constituyen una fuente normativa del motor. Mi Retiro Seguro se consulta desde el ecosistema de Mi Caja Digital, por lo que no se presenta como recurso independiente en la interfaz:

- [Mi Caja Digital — acceso](https://micajadigital.css.gob.pa/Auth/SignIn)

## 8. Regla de mantenimiento de enlaces y parámetros

Cuando cambie una norma, un monto indexado, una tabla actuarial o una fecha operativa:

1. conservar la versión anterior cuando sea necesaria para cálculos históricos;
2. agregar la nueva fuente oficial y fecha de vigencia;
3. actualizar `normativa/*.json`;
4. actualizar `docs/NORMATIVA.md` y este documento;
5. agregar o modificar pruebas automatizadas;
6. registrar la decisión en `docs/DECISIONES.md` cuando exista interpretación o conflicto entre fuentes.

**Última verificación de enlaces públicos de esta edición documental:** 11 de agosto de 2026.


### 8.1. Uso de enlaces en la interfaz

La vista `Ver cálculo completo` consume los enlaces de `fuentes_oficiales` definidos en `normativa/*.json`. De esta manera, cada resultado puede abrir la fuente oficial sin duplicar URLs en JavaScript. La página `/metodologia` reutiliza el mismo registro.

## 9. Presentación de fuentes en la interfaz

La ruta `/metodologia` constituye el punto central visible de consulta normativa. Reutiliza las URLs versionadas en `normativa/*.json`, las agrupa por sistema y mantiene separadas las fuentes legales, reglamentarias, de orientación y los recursos de verificación individual.

En `Ver cálculo completo`, los IDs internos de integración (`texto_unico`, `ley_462`, `reglamento_calculo`, etc.) no se presentan literalmente. Cada paso muestra el título humano de la fuente y un enlace oficial cuando está disponible.

La página de metodología no sustituye este documento técnico: la interfaz está orientada al Asegurado(a) final y este archivo conserva el inventario y las notas de mantenimiento del repositorio.
