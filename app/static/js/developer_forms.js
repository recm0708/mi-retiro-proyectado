"use strict";

/*
 * Mi Retiro Proyectado — Formularios del Portal Developer.
 *
 * Propósito: Gestiona preservación segura de formularios, validación de campos y copia de credenciales temporales.
 * Alcance: Comportamiento de interfaz; no persiste contraseñas, tokens CSRF ni secretos de autenticación.
 */

(() => {
  const STORAGE_KEY = "mrp.dev.form.pending.v2";
  const RESULTADOS_ERROR = new Set([
    "revalidacion-invalida",
    "crear-invalido",
    "editar-invalido",
    "eliminar-confirmacion",
  ]);

  function esSensible(control) {
    const tipo = String(control.type || "").toLowerCase();
    const nombre = String(control.name || "").toLowerCase();

    return (
      tipo === "password"
      || nombre.includes("password")
      || nombre.includes("contraseña")
      || nombre.includes("contrasena")
      || nombre.includes("csrf")
      || nombre.includes("token")
      || nombre.includes("confirmacion")
    );
  }

  function firmaFormulario(formulario) {
    return {
      action: formulario.getAttribute("action") || window.location.pathname,
      method: String(formulario.method || "get").toLowerCase(),
    };
  }

  function guardarFormulario(formulario) {
    if (
      !formulario
      || String(formulario.method).toLowerCase() !== "post"
    ) {
      return;
    }

    const valores = {};

    formulario.querySelectorAll(
      "input[name], select[name], textarea[name]",
    ).forEach((control) => {
      if (
        esSensible(control)
        || control.disabled
        || ["submit", "button", "file"].includes(
          String(control.type || "").toLowerCase(),
        )
      ) {
        return;
      }

      valores[control.name] = control.value;
    });

    try {
      sessionStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          ...firmaFormulario(formulario),
          valores,
          timestamp: Date.now(),
        }),
      );
    } catch (_error) {
      // Mejora de UX no bloqueante.
    }
  }

  function leerPendiente() {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (_error) {
      return null;
    }
  }

  function limpiarPendiente() {
    try {
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (_error) {
      // Sin acción.
    }
  }

  function buscarFormulario(payload) {
    if (!payload) {
      return null;
    }

    return Array.from(
      document.querySelectorAll("form"),
    ).find((formulario) => {
      const firma = firmaFormulario(formulario);

      return (
        firma.method === payload.method
        && firma.action === payload.action
      );
    }) || null;
  }

  function restaurarNoSensibles(formulario, valores) {
    Object.entries(valores || {}).forEach(([nombre, valor]) => {
      const control = formulario.elements.namedItem(nombre);

      if (
        !control
        || esSensible(control)
        || control.type === "file"
      ) {
        return;
      }

      control.value = valor;
    });
  }

  function limpiarErrorCampo(control) {
    if (!control) {
      return;
    }

    control.removeAttribute("aria-invalid");
    control.removeAttribute("aria-errormessage");

    if (control.id) {
      document.getElementById(`${control.id}-error`)?.remove();
    }
  }

  function marcarErrorCampo(control, texto) {
    if (!control) {
      return;
    }

    const id = control.id || `dev-field-${crypto.randomUUID()}`;
    control.id = id;

    let error = document.getElementById(`${id}-error`);

    if (!error) {
      error = document.createElement("div");
      error.id = `${id}-error`;
      error.className = "invalid-feedback d-block";
      error.setAttribute("role", "alert");

      const grupo = control.closest(".dev-secret-group");

      if (grupo) {
        grupo.insertAdjacentElement("afterend", error);
      } else {
        control.insertAdjacentElement("afterend", error);
      }
    }

    error.textContent = texto;
    control.setAttribute("aria-invalid", "true");
    control.setAttribute("aria-errormessage", error.id);

    window.setTimeout(() => {
      control.focus({ preventScroll: false });
    }, 0);
  }

  function validarRequeridos(formulario) {
    let primero = null;

    formulario.querySelectorAll("[required]").forEach((control) => {
      limpiarErrorCampo(control);

      if (!String(control.value || "").trim()) {
        marcarErrorCampo(
          control,
          "Este campo es obligatorio.",
        );

        primero ||= control;
      }
    });

    if (primero) {
      primero.focus({ preventScroll: false });
      return false;
    }

    return true;
  }

  function aplicarResultado() {
    const params = new URLSearchParams(window.location.search);
    const resultado = params.get("resultado");

    if (!RESULTADOS_ERROR.has(resultado)) {
      if (resultado) {
        limpiarPendiente();
      }
      return;
    }

    const payload = leerPendiente();
    const formulario = buscarFormulario(payload);

    if (!formulario) {
      return;
    }

    restaurarNoSensibles(
      formulario,
      payload.valores,
    );

    if (resultado === "revalidacion-invalida") {
      const password = formulario.querySelector(
        'input[type="password"][name="password_actual"]',
      );

      marcarErrorCampo(
        password,
        "La contraseña actual no coincide.",
      );
      return;
    }

    if (resultado === "eliminar-confirmacion") {
      marcarErrorCampo(
        formulario.querySelector('input[name="confirmacion"]'),
        "La confirmación no coincide con ELIMINAR USUARIO.",
      );
    }
  }

  async function copiarCredencial(boton) {
    const target = boton.getAttribute("data-dev-copy-target");
    const control = target ? document.getElementById(target) : null;

    if (!control) {
      return;
    }

    const texto = String(control.value || "").trim();

    if (!texto) {
      return;
    }

    try {
      await navigator.clipboard.writeText(texto);

      const label = boton.querySelector("[data-dev-copy-label]");
      const previo = label?.textContent || "Copiar";

      if (label) {
        label.textContent = "Copiado";
      }

      boton.classList.add("is-copied");
      boton.setAttribute("aria-label", "Contraseña copiada");

      window.setTimeout(() => {
        if (label) {
          label.textContent = previo;
        }

        boton.classList.remove("is-copied");
        boton.setAttribute(
          "aria-label",
          "Copiar contraseña temporal",
        );
      }, 1600);
    } catch (_error) {
      control.focus();
      control.select();
    }
  }

  function iniciar() {
    document.querySelectorAll(
      'form[method="post"], form[method="POST"]',
    ).forEach((formulario) => {
      formulario.addEventListener(
        "submit",
        (evento) => {
          if (!validarRequeridos(formulario)) {
            evento.preventDefault();
            return;
          }

          guardarFormulario(formulario);
        },
      );

      formulario.addEventListener(
        "input",
        (evento) => {
          const control = evento.target;

          if (
            control instanceof HTMLInputElement
            || control instanceof HTMLSelectElement
            || control instanceof HTMLTextAreaElement
          ) {
            limpiarErrorCampo(control);
          }
        },
      );
    });

    document.querySelectorAll(
      "[data-dev-copy-password]",
    ).forEach((boton) => {
      boton.addEventListener(
        "click",
        () => copiarCredencial(boton),
      );
    });

    aplicarResultado();
  }

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      iniciar,
    );
  } else {
    iniciar();
  }
})();

/* correccion final de foco de validacion */
(() => {
  const RESULTADOS_CON_ERROR = new Set([
    "revalidacion-invalida",
    "crear-invalido",
    "editar-invalido",
    "eliminar-confirmacion",
  ]);

  let focoProgramado = false;

  function enfocarPrimerInvalido() {
    focoProgramado = false;

    const control = document.querySelector(
      '.form-control[aria-invalid="true"],'
      + ' .form-select[aria-invalid="true"]',
    );

    if (!control) {
      return;
    }

    control.scrollIntoView({
      block: "center",
      inline: "nearest",
    });

    control.focus({
      preventScroll: true,
    });
  }

  function programarFoco() {
    if (focoProgramado) {
      return;
    }

    focoProgramado = true;

    const ejecutar = () => {
      window.requestAnimationFrame(
        enfocarPrimerInvalido,
      );
    };

    if (
      typeof window.requestAnimationFrame
      === "function"
    ) {
      window.requestAnimationFrame(
        ejecutar,
      );
      return;
    }

    window.setTimeout(
      enfocarPrimerInvalido,
      0,
    );
  }

  function iniciarCorreccionFoco() {
    const observador = new MutationObserver(
      (mutaciones) => {
        const cambioInvalido = mutaciones.some(
          (mutacion) => (
            mutacion.type === "attributes"
            && mutacion.attributeName === "aria-invalid"
            && mutacion.target.getAttribute("aria-invalid") === "true"
          ),
        );

        if (cambioInvalido) {
          programarFoco();
        }
      },
    );

    observador.observe(
      document.documentElement,
      {
        subtree: true,
        attributes: true,
        attributeFilter: ["aria-invalid"],
      },
    );

    document.addEventListener(
      "submit",
      () => {
        window.setTimeout(
          programarFoco,
          0,
        );
      },
      true,
    );

    const resultado = new URLSearchParams(
      window.location.search,
    ).get("resultado");

    if (RESULTADOS_CON_ERROR.has(resultado)) {
      window.setTimeout(
        programarFoco,
        0,
      );
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      iniciarCorreccionFoco,
    );
  } else {
    iniciarCorreccionFoco();
  }
})();
