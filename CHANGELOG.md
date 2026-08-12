# Changelog

Todos los cambios relevantes del proyecto se documentan aquí.

El proyecto todavía no ha publicado una versión estable; los cambios actuales se acumulan bajo **Unreleased** para la futura versión `0.1.0`.

## [Unreleased]

### Agregado

#### Asistente y base técnica

- Aplicación web local con FastAPI, Jinja2, Bootstrap, CSS y JavaScript.
- Asistente de seis pasos para datos personales, cuotas, historial, proyección, retiro y resultados.
- Estado temporal de simulación en `sessionStorage`.
- Navegación directa entre pasos ya disponibles y barra persistente para flujos largos.
- Normalización salarial entre periodicidades y proyección por salario constante, porcentaje, salario futuro conocido o varios escenarios.
- Línea temporal que separa datos históricos, año actual y proyecciones futuras.
- Precisión monetaria basada en `Decimal` y `ROUND_HALF_UP` al materializar importes.
- Formato monetario con separadores de miles y máximo dos decimales en campos editables.
- Archivos normativos versionados en `normativa/`.
- Documentación técnica, funcional, normativa y de validación.

#### SEBD

- Motor de Pensión de Retiro por Vejez Normal.
- Clasificación automática de Normal, Anticipada, Proporcional y Proporcional Anticipada.
- Tabla mensual de factores de reducción para retiro anticipado.
- Cálculo de Indemnización por Vejez como pago único separado de una pensión mensual.
- Límites máximos ordinario y ampliados conforme a las condiciones implementadas.
- Endpoints directos e integrados para cálculo SEBD.
- Integración visual completa en el Paso 6.
- Regresiones automatizadas, incluida una validación anonimizada que reproduce B/.741.59.

#### Subsistema Mixto

- Motor separado para Componente de Beneficio Definido y Componente de Ahorro Personal.
- Tope de participación de B/.500.00 mensuales en el componente BD, con advertencia cuando el historial anual obliga a aproximar el tope mensual.
- Pensión programada del CAP cuando se suministran saldo y divisor actuarial aplicable.
- Opción explícita `AUTO / PENSION_PROGRAMADA / DEVOLUCION_TOTAL`.
- Devolución total del CAP como pago único cuando corresponde.
- Separación de indemnización BD, devolución CAP y total de pagos únicos.
- Bono de reconocimiento como dato oficial/validado, sin reconstrucción automática no sustentada.
- Garantía futura del Seguro Colectivo de Renta Vitalicia.
- Transición operativa Mixto → SUCGS desde 01/03/2032 con discrepancia normativa documentada.
- Endpoint integrado y presentación visual completa en el Paso 6.

#### SUCGS

- Motor contributivo del artículo 196 con tabla actuarial versionada.
- Fórmula `saldo / 1000 × factor de pensionamiento actuarial`.
- Capa solidaria de los artículos 194 y 195.
- Pensión Garantizada Solidaria y Beneficio Mínimo con valores legales versionados y posibilidad de suministrar valores vigentes confirmados.
- Garantía de reemplazo mínimo del artículo 197.
- Preevaluación del mínimo anual de cuotas y distribución temporal 50 % / 50 %.
- Salario promedio base mensual calculado desde salarios cotizados y meses cotizados.
- Estabilidad salarial del artículo 197 como condición explícita y auditable.
- Endpoints directos e integrados e interfaz completa en el Paso 6.

#### Pruebas

- Suite automatizada con **57 pruebas** antes del bloque 6F.
- Casos para precisión monetaria, proyecciones, línea temporal y retiro.
- Regresiones SEBD para modalidades e indemnización.
- Casos Mixto para pensión programada, devolución, garantías y pagos únicos.
- Casos SUCGS para componente contributivo, capa solidaria, garantía de reemplazo y condiciones que impiden aplicarla.

#### Documentación y repositorio

- `docs/INDICE.md` como mapa de la documentación.
- `docs/FUENTES_NORMATIVAS.md` con leyes, artículos, reglamentos, resoluciones y enlaces oficiales.
- Normalización de la numeración ADR en `docs/DECISIONES.md`.
- Reorganización del roadmap y de la documentación por capacidades actuales en lugar de acumulación histórica de subfases.
- Mejora de `.gitignore`, `.gitattributes`, `.editorconfig` y `CONTRIBUTING.md`.

### Cambiado

- JavaScript queda limitado a navegación, presentación, persistencia temporal y comunicación con la API; las fórmulas previsionales permanecen en Python.
- Los datos históricos y proyectados se mantienen diferenciados en todos los pasos.
- La proyección de cuotas respeta primero el cierre del año actual y luego la densidad futura.
- Los escenarios de retiro exigen cobertura suficiente del horizonte salarial o muestran una advertencia.
- Los resultados dependientes se invalidan cuando cambia un dato que los originó.
- `SUCGS` se presenta con su nombre completo en la interfaz.
- Saldo CAP y bono del Mixto reutilizan el formato monetario común; el divisor actuarial no lleva prefijo monetario porque no representa balboas.
- Los pagos únicos y las pensiones mensuales permanecen separados tanto en la API como en la interfaz.
- Los valores normativos sujetos a indexación o actualización no se tratan como constantes eternas.
- La documentación normativa centraliza enlaces oficiales y distingue ley, reglamento y comunicación operativa.

### Corregido

- Estructura Jinja y jerarquía HTML en los pasos del asistente.
- Duplicación accidental de componentes del historial.
- Restauración de scripts específicos de simulación e historial.
- Clasificación visual de años sin cotización.
- Diferencias de un centavo provocadas por redondeos intermedios.
- Proyección de cuotas que podía agregar meses al año actual contra la expectativa declarada por el usuario.
- Artefactos de punto flotante en campos monetarios.
- Semántica de campos no aplicables en la Indemnización por Vejez, usando `null` en lugar de valores numéricos engañosos.
- Navegación del Paso 6 para reconocer SEBD, Mixto y SUCGS sin tratar motores ya implementados como pendientes.
- Numeración duplicada y no consecutiva de ADR en la documentación.
- Secciones documentales obsoletas que seguían marcando como pendientes motores ya implementados.

### Pendiente para 6F y fases posteriores

- Comparación transversal final entre escenarios de retiro y escenarios salariales.
- Vista de metodología y fuentes desde la interfaz.
- Desglose auditable de fórmula, sustitución numérica, redondeo y límites.
- Preparación de estructura para informes y PDF.
- Persistencia voluntaria con SQLite.
- Pulido final de identidad visual, temas, accesibilidad y enlaces institucionales.
