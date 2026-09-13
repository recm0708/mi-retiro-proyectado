"use strict";

/*
 * Mi Retiro Proyectado — Compatibilidad de interacción compartida.
 *
 * Propósito: Proporciona fallbacks de estado visual cuando selectores CSS modernos no están disponibles.
 * Alcance: Sincroniza clases de presentación; no modifica datos, credenciales, permisos ni reglas de negocio.
 */

(() => {
  function sincronizarGrupo(grupo) {
    if (!grupo) {
      return;
    }

    const invalido = Boolean(
      grupo.querySelector(
        '[aria-invalid="true"], .is-invalid',
      ),
    );

    grupo.classList.toggle(
      "is-invalid-group",
      invalido,
    );
  }

  function sincronizarComparacion(opcion) {
    if (!opcion) {
      return;
    }

    const deshabilitada = Boolean(
      opcion.querySelector(
        "input:disabled, select:disabled, button:disabled",
      ),
    );

    opcion.classList.toggle(
      "is-disabled",
      deshabilitada,
    );
  }

  function sincronizarNodo(nodo) {
    if (!(nodo instanceof Element)) {
      return;
    }

    if (nodo.matches(".input-group")) {
      sincronizarGrupo(nodo);
    }

    if (nodo.matches(".comparison-option")) {
      sincronizarComparacion(nodo);
    }

    nodo.querySelectorAll(".input-group").forEach(
      sincronizarGrupo,
    );

    nodo.querySelectorAll(".comparison-option").forEach(
      sincronizarComparacion,
    );
  }

  function iniciarCompatibilidad() {
    sincronizarNodo(document.documentElement);

    const observador = new MutationObserver(
      (mutaciones) => {
        mutaciones.forEach((mutacion) => {
          if (mutacion.type === "attributes") {
            const objetivo = mutacion.target;

            sincronizarGrupo(
              objetivo.closest?.(".input-group"),
            );

            sincronizarComparacion(
              objetivo.closest?.(".comparison-option"),
            );

            return;
          }

          mutacion.addedNodes.forEach(
            sincronizarNodo,
          );
        });
      },
    );

    observador.observe(
      document.documentElement,
      {
        subtree: true,
        childList: true,
        attributes: true,
        attributeFilter: [
          "aria-invalid",
          "class",
          "disabled",
        ],
      },
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      iniciarCompatibilidad,
      { once: true },
    );
  } else {
    iniciarCompatibilidad();
  }
})();
