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

/* ==========================================================
 * R6 sidebar compact persistence
 * ========================================================== */

(() => {
  const PARAMETRO = "sidebar";
  const VALOR_COMPACTO = "compact";
  const DESKTOP_QUERY = "(min-width: 992px)";

  function urlConEstadoSidebar(
    href,
    compacto,
  ) {
    const url = new URL(
      href,
      window.location.origin,
    );

    if (compacto) {
      url.searchParams.set(
        PARAMETRO,
        VALOR_COMPACTO,
      );
    } else {
      url.searchParams.delete(
        PARAMETRO,
      );
    }

    return (
      url.pathname
      + url.search
      + url.hash
    );
  }

  function estadoCompactoEnUrl() {
    const url = new URL(
      window.location.href,
    );

    return (
      url.searchParams.get(
        PARAMETRO,
      ) === VALOR_COMPACTO
    );
  }

  function actualizarUrlActual(
    compacto,
  ) {
    const url = new URL(
      window.location.href,
    );

    if (compacto) {
      url.searchParams.set(
        PARAMETRO,
        VALOR_COMPACTO,
      );
    } else {
      url.searchParams.delete(
        PARAMETRO,
      );
    }

    window.history.replaceState(
      window.history.state,
      "",
      (
        url.pathname
        + url.search
        + url.hash
      ),
    );
  }

  function obtenerEtiqueta(
    enlace,
  ) {
    const elementos = enlace.querySelectorAll(
      "span",
    );

    if (!elementos.length) {
      return "";
    }

    return (
      elementos[
        elementos.length - 1
      ].textContent.trim()
    );
  }

  function iniciarPersistenciaSidebar() {
    const body = document.body;

    const boton = document.querySelector(
      "[data-dev-sidebar-toggle]",
    );

    const enlaces = Array.from(
      document.querySelectorAll(
        ".dev-sidebar-nav a",
      ),
    );

    const desktop = window.matchMedia(
      DESKTOP_QUERY,
    );

    if (!body || !boton) {
      return;
    }

    function estaCompacto() {
      return (
        desktop.matches
        && body.classList.contains(
          "dev-sidebar-collapsed",
        )
      );
    }

    function actualizarEnlaces(
      compacto,
    ) {
      enlaces.forEach((enlace) => {
        const href = enlace.getAttribute(
          "href",
        );

        if (
          !href
          || !href.startsWith("/dev")
        ) {
          return;
        }

        enlace.setAttribute(
          "href",
          urlConEstadoSidebar(
            href,
            compacto,
          ),
        );
      });
    }

    function actualizarAyudas(
      compacto,
    ) {
      enlaces.forEach((enlace) => {
        const etiqueta = obtenerEtiqueta(
          enlace,
        );

        if (!etiqueta) {
          return;
        }

        if (compacto) {
          enlace.setAttribute(
            "title",
            etiqueta,
          );
        } else {
          enlace.removeAttribute(
            "title",
          );
        }
      });
    }

    function sincronizarPresentacion(
      compacto,
    ) {
      actualizarEnlaces(
        compacto,
      );

      actualizarAyudas(
        compacto,
      );
    }

    function aplicarEstadoInicial() {
      if (!desktop.matches) {
        body.classList.remove(
          "dev-sidebar-collapsed",
        );

        sincronizarPresentacion(
          false,
        );

        return;
      }

      const compacto = (
        estadoCompactoEnUrl()
      );

      body.classList.toggle(
        "dev-sidebar-collapsed",
        compacto,
      );

      sincronizarPresentacion(
        compacto,
      );
    }

    /*
     * El controlador original realiza el toggle visual.
     * Después sincronizamos la URL actual y todos los enlaces.
     *
     * El estado visual se conserva únicamente en la URL.
     */
    boton.addEventListener(
      "click",
      () => {
        window.requestAnimationFrame(
          () => {
            if (!desktop.matches) {
              return;
            }

            const compacto = (
              estaCompacto()
            );

            actualizarUrlActual(
              compacto,
            );

            sincronizarPresentacion(
              compacto,
            );
          },
        );
      },
    );

    if (
      typeof desktop.addEventListener
      === "function"
    ) {
      desktop.addEventListener(
        "change",
        aplicarEstadoInicial,
      );
    }

    window.addEventListener(
      "pageshow",
      aplicarEstadoInicial,
    );

    aplicarEstadoInicial();
  }

  document.addEventListener(
    "DOMContentLoaded",
    iniciarPersistenciaSidebar,
  );
})();
