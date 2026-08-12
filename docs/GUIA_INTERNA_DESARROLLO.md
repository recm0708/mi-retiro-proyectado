# Guía interna de desarrollo

Este documento concentra información técnica que no debe mostrarse en la interfaz dirigida al **Asegurado(a)**.

## 1. Identidad del producto

- **Nombre visible:** Mi Retiro Proyectado.
- **Naturaleza:** herramienta independiente de la Caja de Seguro Social de Panamá.
- **Público de la interfaz:** Asegurado(a) / Asegurados(as).
- El nombre **Mi Retiro Seguro** se reserva para la herramienta oficial de la CSS y no se utiliza como nombre de este proyecto.

La identidad visible se centraliza en `app/core/config.py`.

## 2. Convención de terminología

En textos destinados a la interfaz y documentación funcional:

- singular: **Asegurado(a)**;
- plural: **Asegurados(as)**;
- evitar `usuario` cuando se refiera a la persona que realiza la simulación.

`Usuario` puede aparecer únicamente cuando sea un término técnico inequívoco que no describa al público final.

## 3. Información exclusivamente técnica

Las siguientes referencias pertenecen al mantenimiento del proyecto y no deben mostrarse como contenido principal de la aplicación:

- nombres internos de fases como `6F.1`, `6F.2`, `6F.3` o `6F.4`;
- rutas como `docs/*.md`, `normativa/*.json`, nombres de módulos o identificadores internos;
- ADR y decisiones de implementación;
- detalles de estructura del repositorio.

La interfaz puede mostrar la metodología, la normativa y los enlaces oficiales, pero no debe exponer la organización interna del repositorio.

## 4. Tipografía visible

La interfaz usa una escala simple:

1. **texto base:** un único tamaño para párrafos, controles, ayudas, tablas y navegación;
2. **encabezados:** jerarquía estructural;
3. **valores importantes:** tamaño mayor para pensiones, saldos y métricas que requieren atención;
4. **badges de estado:** tamaño compacto únicamente para señalización.

No se deben introducir tamaños arbitrarios por componente sin una justificación de jerarquía visual.

## 5. Fases internas

Los nombres de fases y subfases pueden mantenerse en documentación técnica, pruebas y comentarios de código para conservar trazabilidad histórica, pero no como badges, títulos o mensajes visibles para el Asegurado(a).

## 6. Fuentes y metodología

La interfaz utiliza nombres humanos y enlaces oficiales. Los identificadores internos de fuentes se resuelven desde los metadatos normativos antes de mostrarse.

Documentos técnicos relacionados:

- [Arquitectura](ARQUITECTURA.md)
- [Decisiones](DECISIONES.md)
- [Normativa](NORMATIVA.md)
- [Fuentes normativas](FUENTES_NORMATIVAS.md)
- [Validación](VALIDACION.md)

## Temas visuales

- La preferencia visual se gestiona únicamente en `app/static/js/tema.js`.
- Los componentes personalizados deben usar los tokens `--app-*` definidos en `style.css` en lugar de introducir nuevas superficies claras mediante colores literales.
- Un componente nuevo debe revisarse al menos en Claro, Oscuro y Alto contraste.
- No guardar el tema dentro de la simulación ni usarlo como parámetro del backend.

## Accesibilidad de interfaz

- Mantener un foco visible para controles interactivos.
- Evitar objetivos táctiles principales menores de 44 px.
- No depender exclusivamente del color para comunicar estados.
- Respetar la preferencia de movimiento reducido.
- Las nuevas páginas deben heredar de `base.html` para conservar navegación, salto al contenido y footer legal.

## 7. Tokens visuales semánticos

A partir de UX.2.1, los componentes nuevos deben reutilizar los tokens semánticos definidos en `style.css` para texto, superficies, bordes y estados. No introducir un color literal en una tarjeta o badge si existe un token con la misma función.

Revisar como mínimo:

- Claro;
- Oscuro;
- Alto contraste;
- estados de foco y hover;
- alertas, badges, tablas y controles.

Alto contraste se considera un tema oscuro de contraste máximo: fondo negro, texto blanco, bordes explícitos y foco amarillo.

## 8. Contenido visible frente a detalles de implementación

La trazabilidad visible puede indicar artículo, reglamento, fórmula, nombre de la fuente y enlace oficial. No debe explicar al Asegurado(a) que el enlace procede de `normativa/*.json`, de un endpoint, del backend o de otra estructura interna. Esos detalles se documentan aquí, en Arquitectura o en Decisiones.


## 9. Responsive y navegación móvil

UX.3 establece estas reglas para componentes nuevos:

- no resolver una tabla compleja reduciendo indiscriminadamente tipografía o columnas; usar un contenedor horizontal localizado cuando corresponda;
- evitar desbordamiento horizontal de `body`;
- en móvil, las acciones de formulario importantes deben alcanzar 48 px de altura y pueden ocupar todo el ancho disponible;
- la barra persistente del wizard se mantiene abajo de 768 px y debe respetar `env(safe-area-inset-*)`;
- comprobar como mínimo 375 px, 768 px, 1024 px y un escritorio amplio;
- revisar Claro, Oscuro y Alto contraste también en los breakpoints móviles.

## 10. Criterio de cierre de cambios

Un cambio no se considera terminado si modifica código, comportamiento o UX y deja desactualizada la documentación dependiente. Antes de cerrar una fase deben revisarse, según corresponda, `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `DECISIONES.md`, especificaciones, modelo de datos, arquitectura, guía interna y validación. También deben agregarse o actualizarse regresiones automatizadas cuando el cambio sea verificable por pruebas.

## Recursos gráficos pendientes y favicon temporal

Hasta integrar la familia definitiva de iconos de **Mi Retiro Proyectado**, no se debe crear ni versionar un favicon genérico o provisional. La ruta `/favicon.ico` responde temporalmente `204 No Content` para evitar errores 404 provocados por solicitudes automáticas del navegador.

Cuando los iconos oficiales estén disponibles se deberá:

1. guardar los recursos en la estructura aprobada de `app/static/img/`;
2. declarar favicon y variantes necesarias en `app/templates/base.html`;
3. retirar la ruta temporal `/favicon.ico` de `app/main.py`;
4. actualizar pruebas, `CHANGELOG.md`, `README.md`, `ROADMAP.md` y esta guía.
