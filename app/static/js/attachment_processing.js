"use strict";

/*
 * Mi Retiro Proyectado — Estado transversal de procesamiento de archivos adjuntos.
 *
 * Propósito: Muestra una señal accesible mientras el backend analiza documentos y evita dobles ejecuciones sobre el mismo botón.
 * Alcance: Los documentos se procesan en memoria mediante peticiones al backend; este módulo solo coordina estado visual.
 */

(() => {
  const MENSAJE_PROCESANDO = (
    "Analizando documento… Esto puede tardar unos segundos."
  );

  function estaActivo(boton) {
    return boton?.dataset.procesandoAdjunto === "true";
  }

  function mostrarEstado(
    estado,
    mensaje = MENSAJE_PROCESANDO,
  ) {
    if (!estado) {
      return;
    }


    const linea = document.createElement(
      "div",
    );

    linea.className = (
      "d-flex align-items-center gap-2"
    );


    const indicador = document.createElement(
      "span",
    );

    indicador.className = (
      "spinner-border spinner-border-sm"
    );

    indicador.setAttribute(
      "aria-hidden",
      "true",
    );


    const texto = document.createElement(
      "span",
    );

    texto.textContent = mensaje;


    linea.append(
      indicador,
      texto,
    );


    /*
     * El backend no informa porcentaje de avance.
     * La barra representa actividad indeterminada y
     * nunca presenta un porcentaje artificial.
     */
    const progreso = document.createElement(
      "div",
    );

    progreso.className = (
      "progress mt-2"
    );

    progreso.setAttribute(
      "role",
      "progressbar",
    );

    progreso.setAttribute(
      "aria-label",
      "Análisis del documento",
    );

    progreso.setAttribute(
      "aria-valuetext",
      "Procesando documento",
    );


    const barra = document.createElement(
      "div",
    );

    barra.className = (
      "progress-bar progress-bar-striped "
      + "progress-bar-animated w-100"
    );


    progreso.appendChild(
      barra,
    );


    estado.replaceChildren(
      linea,
      progreso,
    );

    estado.classList.remove(
      "d-none",
    );

    estado.classList.add(
      "attachment-processing-status",
    );

    estado.setAttribute(
      "role",
      "status",
    );

    estado.setAttribute(
      "aria-live",
      "polite",
    );

    estado.setAttribute(
      "aria-atomic",
      "true",
    );

    estado.setAttribute(
      "aria-busy",
      "true",
    );
  }

  function iniciar({
    // El token conserva el estado original de botón/input para restaurarlo
    // exactamente cuando termina la petición, incluso si hubo error.
    boton,
    input = null,
    estado = null,
    textoBoton = "Analizando…",
    mensaje = MENSAJE_PROCESANDO,
  }) {
    if (!boton || estaActivo(boton)) {
      return null;
    }

    const token = {
      boton,
      input,
      estado,
      textoBotonOriginal: boton.textContent,
      botonDeshabilitadoOriginal: boton.disabled,
      inputDeshabilitadoOriginal: input?.disabled ?? false,
    };

    boton.dataset.procesandoAdjunto = "true";
    boton.disabled = true;
    boton.setAttribute("aria-busy", "true");
    boton.textContent = textoBoton;

    if (input) {
      input.disabled = true;
      input.setAttribute("aria-busy", "true");
    }

    mostrarEstado(estado, mensaje);
    return token;
  }

  function finalizar(token) {
    // Finalizar limpia la marca de procesamiento y devuelve accesibilidad visual
    // al mismo estado previo al análisis.
    if (!token?.boton) return;

    const {
      boton,
      input,
      estado,
      textoBotonOriginal,
      botonDeshabilitadoOriginal,
      inputDeshabilitadoOriginal,
    } = token;

    boton.textContent = textoBotonOriginal;
    boton.disabled = botonDeshabilitadoOriginal;
    boton.removeAttribute("aria-busy");
    delete boton.dataset.procesandoAdjunto;

    if (input) {
      input.disabled = inputDeshabilitadoOriginal;
      input.removeAttribute("aria-busy");
    }

    if (estado?.classList.contains("attachment-processing-status")) {
      estado.classList.add("d-none");
      estado.classList.remove("attachment-processing-status");
      estado.removeAttribute("aria-busy");
      estado.replaceChildren();
    }
  }

  window.ProcesamientoAdjuntos = Object.freeze({
    MENSAJE_PROCESANDO,
    estaActivo,
    iniciar,
    finalizar,
  });
})();
