"use strict";

/*
 * Mi Retiro Proyectado — Portal Developer.
 *
 * Propósito: Gestiona las interacciones locales del shell Developer, sidebar y controles de acceso visual.
 * Alcance: Comportamiento de interfaz; no persiste credenciales, tokens ni estado de autenticación.
 */
(() => {
  const MOBILE_QUERY = "(max-width: 991.98px)";

  function iniciarVisibilidadPassword() {
    const toggle = document.querySelector(
      "[data-dev-password-toggle]",
    );

    const input =
      document.getElementById("dev-password")
      || document.getElementById("admin-token");

    if (!toggle || !input) {
      return;
    }

    toggle.addEventListener("click", () => {
      const mostrar = input.type === "password";

      input.type = mostrar
        ? "text"
        : "password";

      toggle.textContent = mostrar
        ? "Ocultar"
        : "Mostrar";

      toggle.setAttribute(
        "aria-pressed",
        mostrar ? "true" : "false",
      );

      input.focus();
    });
  }

  function iniciarSidebar() {
    const body = document.body;

    const sidebar = document.getElementById(
      "dev-sidebar",
    );

    const toggle = document.querySelector(
      "[data-dev-sidebar-toggle]",
    );

    const overlay = document.querySelector(
      "[data-dev-sidebar-overlay]",
    );

    if (!sidebar || !toggle) {
      return;
    }

    const mediaMobile = window.matchMedia(
      MOBILE_QUERY,
    );

    function estaAbierto() {
      if (mediaMobile.matches) {
        return body.classList.contains(
          "dev-sidebar-open",
        );
      }

      return !body.classList.contains(
        "dev-sidebar-collapsed",
      );
    }

    function sincronizarEstado() {
      const abierto = estaAbierto();

      toggle.setAttribute(
        "aria-expanded",
        abierto ? "true" : "false",
      );
    }

    function cerrarMovil() {
      body.classList.remove(
        "dev-sidebar-open",
      );

      sincronizarEstado();
    }

    toggle.addEventListener("click", () => {
      if (mediaMobile.matches) {
        body.classList.toggle(
          "dev-sidebar-open",
        );
      } else {
        body.classList.toggle(
          "dev-sidebar-collapsed",
        );
      }

      sincronizarEstado();
    });

    if (overlay) {
      overlay.addEventListener(
        "click",
        cerrarMovil,
      );
    }

    sidebar
      .querySelectorAll("a")
      .forEach((enlace) => {
        enlace.addEventListener(
          "click",
          () => {
            if (mediaMobile.matches) {
              cerrarMovil();
            }
          },
        );
      });

    document.addEventListener(
      "keydown",
      (event) => {
        if (
          event.key === "Escape"
          && mediaMobile.matches
          && body.classList.contains(
            "dev-sidebar-open",
          )
        ) {
          cerrarMovil();
          toggle.focus();
        }
      },
    );

    mediaMobile.addEventListener(
      "change",
      () => {
        body.classList.remove(
          "dev-sidebar-open",
        );

        body.classList.remove(
          "dev-sidebar-collapsed",
        );

        sincronizarEstado();
      },
    );

    sincronizarEstado();
  }

  document.addEventListener(
    "DOMContentLoaded",
    () => {
      iniciarVisibilidadPassword();
      iniciarSidebar();
    },
  );
})();
