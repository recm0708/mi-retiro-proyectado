# Política de seguridad

**Estado:** vigente
**Etapa soportada:** desarrollo beta
**Versión de desarrollo actual:** `0.129.3.0-beta`

## Alcance de soporte

La seguridad se mantiene sobre el estado de desarrollo actual del repositorio.
Las versiones beta anteriores, tags y Releases se conservan como historia
auditable, pero no reciben mantenimiento independiente salvo que una
vulnerabilidad obligue a revisar su impacto histórico.

Mi Retiro Proyectado todavía no se declara versión oficial ni despliegue público
de producción. La primera versión oficial objetivo es `1.0.0.0`.

La versión actual se obtiene de [`VERSION`](VERSION). La política de
numeración se documenta en [Política de versionado](VERSIONING.md).

## Reportar una vulnerabilidad

**No publiques una vulnerabilidad explotable como Issue público.**

Canal preferido:

- **GitHub Private vulnerability reporting** del repositorio.

Canal privado alternativo:

`ruben.canizares@outlook.com`

Incluye, si es posible:

- componente, ruta o superficie afectada;
- versión o SHA observado;
- impacto;
- pasos mínimos de reproducción;
- mitigación conocida;
- evidencia sintética o sanitizada.

No envíes cédulas, NSS, PDFs personales, historiales salariales reales,
credenciales, cookies, tokens, bases de datos ni dumps completos de logs sin una
revisión previa de sensibilidad.

## Tratamiento del reporte

El mantenedor:

1. confirma recepción cuando resulte razonablemente posible;
2. clasifica el impacto y la superficie afectada;
3. contiene exposiciones activas cuando sea necesario;
4. preserva la evidencia mínima útil;
5. corrige o mitiga;
6. añade regresiones cuando corresponda;
7. evalúa comunicaciones y obligaciones conforme al
   [procedimiento de incidentes](docs/security/security-incident-procedure.md).

No existe un SLA contractual de respuesta.

## Divulgación coordinada

Se solicita no divulgar públicamente detalles explotables antes de que exista
una corrección o mitigación razonable, salvo obligación legal o una situación
urgente que requiera otro tratamiento.

## Controles del repositorio

El repositorio utiliza controles automatizados y de plataforma, entre ellos:

- Dependency graph y Dependabot;
- análisis de dependencias;
- CodeQL;
- secret scanning y push protection cuando están disponibles;
- required checks en Pull Requests;
- commits/tags firmados según el contrato de gobierno;
- Private vulnerability reporting.

Estos controles reducen riesgo y facilitan detección, pero no garantizan la
ausencia de vulnerabilidades.

## Datos sensibles

No deben versionarse ni exponerse en evidencia pública:

- datos personales o previsionales identificables;
- documentos originales de personas usuarias;
- credenciales, secretos o tokens;
- cookies o sesiones administrativas;
- cuerpos HTTP sensibles;
- salarios, montos de pensión o historiales reales;
- bases de datos Developer locales;
- logs sin sanitizar.

Los casos de validación públicos deben ser sintéticos o anonimizados de forma
irreversible para su finalidad.

## Superficie Developer

El Portal Developer y Developer Diagnostics son superficies de desarrollo y no
forman parte de un despliegue público soportado.

La superficie administrativa permanece protegida por su configuración y
contratos de autenticación. No existe una credencial humana predeterminada en el
repositorio y los secretos técnicos no deben utilizarse como sustituto del login
humano.

La arquitectura y los controles específicos se documentan en:

- [Centro de desarrollo](docs/architecture/development-center.md);
- [Observabilidad y logs](docs/operations/observability-and-logs.md);
- [Seguridad y privacidad](docs/security/security-and-privacy.md);
- [Modelo de amenazas](docs/security/threat-model.md).

Una exposición remota o de producción requiere evaluación explícita de
despliegue, TLS, cookies, secretos, autenticación, autorización, retención y
riesgo de terceros antes de considerarse soportada.

## Documentos relacionados

- [Seguridad y privacidad](docs/security/security-and-privacy.md);
- [Modelo de amenazas](docs/security/threat-model.md);
- [Procedimiento de incidentes](docs/security/security-incident-procedure.md);
- [Evaluación de terceros y despliegue](docs/security/third-party-deployment-assessment.md);
- [Procedimiento de derechos del titular](docs/security/data-subject-rights-procedure.md);
- [Soporte](SUPPORT.md).
