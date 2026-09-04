"use strict";

/*
 * Mi Retiro Proyectado — shell principal.
 *
 * Propósito: Gestiona navegación lateral, estado compacto de escritorio
 * y drawer temporal en dispositivos móviles.
 * Alcance: La preferencia visual de escritorio puede persistir localmente;
 * no almacena datos previsionales, credenciales ni estado de autenticación.
 */

(() => {
  const MOBILE_QUERY = "(max-width: 991.98px)";

  const STORAGE_KEY = (
    "miRetiroProyectado.shell.sidebar"
  );


  function leerPreferencia() {
    try {
      return window.localStorage.getItem(
        STORAGE_KEY,
      );
    } catch {
      return null;
    }
  }


  function guardarPreferencia(
    colapsado,
  ) {
    try {
      window.localStorage.setItem(
        STORAGE_KEY,
        colapsado
          ? "collapsed"
          : "expanded",
      );
    } catch {
      /*
       * La navegación continúa funcionando aunque
       * el almacenamiento del navegador no esté disponible.
       */
    }
  }


  function iniciarSidebar() {
    const body = document.body;

    const sidebar = document.querySelector(
      "[data-app-sidebar]",
    );

    const toggle = document.querySelector(
      "[data-app-sidebar-toggle]",
    );

    const overlay = document.querySelector(
      "[data-app-sidebar-overlay]",
    );


    if (
      !sidebar
      || !toggle
    ) {
      return;
    }


    const mobile = window.matchMedia(
      MOBILE_QUERY,
    );


    function aplicarPreferencia() {
      body.classList.remove(
        "app-sidebar-open",
      );


      if (mobile.matches) {
        body.classList.remove(
          "app-sidebar-collapsed",
        );

        return;
      }


      const preferencia = leerPreferencia();


      /*
       * Primera utilización:
       * expandido por defecto.
       *
       * A partir del primer cambio manual se conserva
       * exactamente la elección del usuario.
       */
      body.classList.toggle(
        "app-sidebar-collapsed",
        preferencia === "collapsed",
      );
    }


    function estaAbierto() {
      if (mobile.matches) {
        return body.classList.contains(
          "app-sidebar-open",
        );
      }


      return !body.classList.contains(
        "app-sidebar-collapsed",
      );
    }


    function sincronizarAria() {
      toggle.setAttribute(
        "aria-expanded",
        estaAbierto()
          ? "true"
          : "false",
      );
    }


    function cerrarMovil() {
      body.classList.remove(
        "app-sidebar-open",
      );

      sincronizarAria();
    }


    toggle.addEventListener(
      "click",
      () => {
        if (mobile.matches) {
          body.classList.toggle(
            "app-sidebar-open",
          );
        } else {
          body.classList.toggle(
            "app-sidebar-collapsed",
          );


          guardarPreferencia(
            body.classList.contains(
              "app-sidebar-collapsed",
            ),
          );
        }


        sincronizarAria();
      },
    );


    overlay?.addEventListener(
      "click",
      cerrarMovil,
    );


    sidebar
      .querySelectorAll("a")
      .forEach(
        (link) => {
          link.addEventListener(
            "click",
            () => {
              /*
               * En escritorio NO se modifica la preferencia.
               * Al navegar se conserva el estado escogido.
               */
              if (mobile.matches) {
                cerrarMovil();
              }
            },
          );
        },
      );


    document.addEventListener(
      "keydown",
      (event) => {
        if (
          event.key === "Escape"
          && mobile.matches
          && body.classList.contains(
            "app-sidebar-open",
          )
        ) {
          cerrarMovil();
          toggle.focus();
        }
      },
    );


    mobile.addEventListener(
      "change",
      () => {
        aplicarPreferencia();
        sincronizarAria();
      },
    );


    aplicarPreferencia();
    sincronizarAria();
  }


  document.addEventListener(
    "DOMContentLoaded",
    iniciarSidebar,
  );
})();
