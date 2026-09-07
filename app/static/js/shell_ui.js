"use strict";

/*
 * Mi Retiro Proyectado — interacción visual compartida del shell.
 *
 * Propósito: Presenta las etiquetas contextuales del sidebar
 * colapsado con una sola implementación compartida.
 * Alcance: Interacción visual de App y Portal Developer; no
 * persiste datos, credenciales ni autenticación.
 */
(() => {
  const DESKTOP_QUERY = "(min-width: 992px)";

  let tooltip = null;
  let enlaceActivo = null;

  function obtenerTooltip() {
    if (tooltip) {
      return tooltip;
    }

    tooltip = document.createElement("div");
    tooltip.className = "shell-sidebar-tooltip";
    tooltip.setAttribute("role", "tooltip");
    tooltip.hidden = true;

    document.body.appendChild(
      tooltip,
    );

    return tooltip;
  }

  function sidebarColapsado(enlace) {
    if (
      !window.matchMedia(
        DESKTOP_QUERY,
      ).matches
    ) {
      return false;
    }

    if (
      enlace.closest(
        "#app-sidebar",
      )
    ) {
      return document.body.classList.contains(
        "app-sidebar-collapsed",
      );
    }

    if (
      enlace.closest(
        "#dev-sidebar",
      )
    ) {
      return document.body.classList.contains(
        "dev-sidebar-collapsed",
      );
    }

    return false;
  }

  function ocultarTooltip() {
    if (!tooltip) {
      return;
    }

    tooltip.classList.remove(
      "is-visible",
    );

    tooltip.hidden = true;
    enlaceActivo = null;
  }

  function posicionarTooltip(
    enlace,
  ) {
    const ayuda = obtenerTooltip();
    const rect = enlace.getBoundingClientRect();

    ayuda.style.left = (
      `${Math.round(rect.right + 10)}px`
    );

    ayuda.style.top = (
      `${Math.round(
        rect.top
        + (rect.height / 2)
      )}px`
    );
  }

  function mostrarTooltip(
    enlace,
  ) {
    const label = (
      enlace.dataset.sidebarLabel
      || ""
    ).trim();

    if (
      !label
      || !sidebarColapsado(enlace)
    ) {
      ocultarTooltip();
      return;
    }

    const ayuda = obtenerTooltip();

    ayuda.textContent = label;
    ayuda.hidden = false;

    enlaceActivo = enlace;

    posicionarTooltip(
      enlace,
    );

    window.requestAnimationFrame(
      () => {
        if (
          enlaceActivo === enlace
          && sidebarColapsado(enlace)
        ) {
          ayuda.classList.add(
            "is-visible",
          );
        }
      },
    );
  }

  function iniciar() {
    const enlaces = document.querySelectorAll(
      "[data-sidebar-label]",
    );

    enlaces.forEach(
      (enlace) => {
        enlace.addEventListener(
          "mouseenter",
          () => mostrarTooltip(enlace),
        );

        enlace.addEventListener(
          "mouseleave",
          ocultarTooltip,
        );

        enlace.addEventListener(
          "focus",
          () => mostrarTooltip(enlace),
        );

        enlace.addEventListener(
          "blur",
          ocultarTooltip,
        );
      },
    );

    window.addEventListener(
      "resize",
      ocultarTooltip,
    );

    window.addEventListener(
      "scroll",
      ocultarTooltip,
      true,
    );

    document.addEventListener(
      "keydown",
      (event) => {
        if (event.key === "Escape") {
          ocultarTooltip();
        }
      },
    );
  }

  document.addEventListener(
    "DOMContentLoaded",
    iniciar,
  );
})();
