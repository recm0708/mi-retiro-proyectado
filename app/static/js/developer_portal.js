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
    const MOBILE_QUERY = "(max-width: 991.98px)";

    const STORAGE_KEY = (
      "miRetiroProyectado.shell.sidebar"
    );


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


    if (
      !sidebar
      || !toggle
    ) {
      return;
    }


    const mobile = window.matchMedia(
      MOBILE_QUERY,
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
        // El shell continúa siendo utilizable.
      }
    }


    function aplicarPreferencia() {
      body.classList.remove(
        "dev-sidebar-open",
      );


      if (mobile.matches) {
        body.classList.remove(
          "dev-sidebar-collapsed",
        );

        return;
      }


      body.classList.toggle(
        "dev-sidebar-collapsed",
        leerPreferencia()
          === "collapsed",
      );
    }


    function estaAbierto() {
      if (mobile.matches) {
        return body.classList.contains(
          "dev-sidebar-open",
        );
      }


      return !body.classList.contains(
        "dev-sidebar-collapsed",
      );
    }


    function sincronizarEstado() {
      toggle.setAttribute(
        "aria-expanded",
        estaAbierto()
          ? "true"
          : "false",
      );
    }


    function cerrarMovil() {
      body.classList.remove(
        "dev-sidebar-open",
      );

      sincronizarEstado();
    }


    toggle.addEventListener(
      "click",
      () => {
        if (mobile.matches) {
          body.classList.toggle(
            "dev-sidebar-open",
          );
        } else {
          body.classList.toggle(
            "dev-sidebar-collapsed",
          );


          guardarPreferencia(
            body.classList.contains(
              "dev-sidebar-collapsed",
            ),
          );
        }


        sincronizarEstado();
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
            "dev-sidebar-open",
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
        sincronizarEstado();
      },
    );


    aplicarPreferencia();
    sincronizarEstado();
  }

  document.addEventListener(
    "DOMContentLoaded",
    () => {
      iniciarVisibilidadPassword();
      iniciarSidebar();
    },
  );

  function iniciarVisorEventos() {
    const filas = Array.from(
      document.querySelectorAll("[data-dev-event-row]"),
    );

    if (!filas.length) {
      return;
    }

    const buscar = document.querySelector(
      "[data-dev-event-search]",
    );
    const nivel = document.querySelector(
      "[data-dev-event-level]",
    );
    const tamano = document.querySelector(
      "[data-dev-event-page-size]",
    );
    const limpiar = document.querySelector(
      "[data-dev-event-reset]",
    );
    const anterior = document.querySelector(
      "[data-dev-event-prev]",
    );
    const siguiente = document.querySelector(
      "[data-dev-event-next]",
    );
    const resumen = document.querySelector(
      "[data-dev-event-summary]",
    );
    const paginaTexto = document.querySelector(
      "[data-dev-event-page]",
    );
    const vacio = document.querySelector(
      "[data-dev-event-empty]",
    );

    let pagina = 1;

    function obtenerFiltradas() {
      const termino = (buscar?.value || "")
        .trim()
        .toLocaleLowerCase();

      const nivelElegido = nivel?.value || "";

      return filas.filter((fila) => {
        const coincideNivel =
          !nivelElegido
          || fila.dataset.level === nivelElegido;

        const coincideTexto =
          !termino
          || (fila.dataset.search || "").includes(termino);

        return coincideNivel && coincideTexto;
      });
    }

    function renderizar() {
      const filtradas = obtenerFiltradas();
      const porPagina = Number.parseInt(
        tamano?.value || "25",
        10,
      );

      const paginas = Math.max(
        1,
        Math.ceil(filtradas.length / porPagina),
      );

      pagina = Math.min(
        Math.max(1, pagina),
        paginas,
      );

      const inicio = (pagina - 1) * porPagina;
      const fin = inicio + porPagina;

      filas.forEach((fila) => {
        fila.hidden = true;
      });

      filtradas
        .slice(inicio, fin)
        .forEach((fila) => {
          fila.hidden = false;
        });

      if (resumen) {
        resumen.textContent =
          `${filtradas.length} de ${filas.length} evento(s)`;
      }

      if (paginaTexto) {
        paginaTexto.textContent =
          `Página ${pagina} de ${paginas}`;
      }

      if (anterior) {
        anterior.disabled =
          pagina <= 1 || filtradas.length === 0;
      }

      if (siguiente) {
        siguiente.disabled =
          pagina >= paginas || filtradas.length === 0;
      }

      if (vacio) {
        vacio.hidden = filtradas.length !== 0;
      }
    }

    buscar?.addEventListener("input", () => {
      pagina = 1;
      renderizar();
    });

    nivel?.addEventListener("change", () => {
      pagina = 1;
      renderizar();
    });

    tamano?.addEventListener("change", () => {
      pagina = 1;
      renderizar();
    });

    limpiar?.addEventListener("click", () => {
      if (buscar) {
        buscar.value = "";
      }

      if (nivel) {
        nivel.value = "";
      }

      pagina = 1;
      renderizar();

      buscar?.focus();
    });

    anterior?.addEventListener("click", () => {
      pagina -= 1;
      renderizar();
    });

    siguiente?.addEventListener("click", () => {
      pagina += 1;
      renderizar();
    });

    renderizar();
  }

  document.addEventListener(
    "DOMContentLoaded",
    iniciarVisorEventos,
  );

})();
