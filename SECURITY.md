# Política de seguridad

## Versiones soportadas

Mi Retiro Proyectado se encuentra en desarrollo pre-beta. El repositorio de código es público, pero la aplicación no se declara todavía como beta pública desplegada.

| Línea | Soporte de seguridad |
|---|---|
| `0.0.25-beta` | Soportada durante el desarrollo pre-beta vigente |
| `0.0.24-beta` y anteriores | Históricas; no reciben correcciones independientes |

## Reportar una vulnerabilidad

**No publique una vulnerabilidad explotable como issue público.**

Canal preferido para el repositorio público:

- **GitHub Private vulnerability reporting**, mediante la opción privada de reporte de vulnerabilidades del repositorio.

Canal privado alternativo:

`ruben.canizares@outlook.com`

Incluya, si es posible y usando evidencia sintética o sanitizada: componente/ruta, versión o SHA, impacto, pasos mínimos y mitigación conocida.

No envíe cédulas/NSS reales, PDFs personales, historiales salariales reales, secretos ni dumps completos de Developer Diagnostics sin revisión.

## Controles del repositorio público

La configuración vigente incluye, según evidencia manual del mantenedor:

- Dependency graph;
- Dependabot alerts;
- Dependabot security updates;
- CodeQL con Default setup;
- Secret Protection / secret scanning;
- Push protection;
- Private vulnerability reporting.

Estos controles reducen riesgo y facilitan detección/reporte; no constituyen una garantía de ausencia de vulnerabilidades.

## Tratamiento del reporte

El mantenedor confirma recepción cuando sea razonablemente posible, clasifica el evento, contiene exposiciones activas, preserva evidencia mínima, corrige y añade regresiones cuando proceda, y evalúa comunicaciones/notificaciones conforme a `docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md`.

No existe un SLA contractual de respuesta.

## Divulgación coordinada

Se solicita no publicar detalles explotables antes de que exista una corrección o mitigación razonable, salvo obligación legal o riesgo urgente.

## GitHub Private vulnerability reporting

Esta función está habilitada y complementa el canal privado alternativo indicado arriba. Los Issues públicos no deben utilizarse para vulnerabilidades explotables.

## Documentos relacionados

- `docs/MODELO_AMENAZAS.md`
- `docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md`
- `docs/SEGURIDAD_PRIVACIDAD.md`
- `docs/AUDITORIA_GITHUB.md`
