"use strict";

/* ============================================================
   Mi Retiro Proyectado
   Estado transversal de procesamiento de archivos adjuntos
   ============================================================ */

/*
 * Los documentos se procesan en memoria mediante peticiones al backend. Esta
 * capa ofrece una señal inmediata y accesible mientras una petición está en
 * curso, y evita dobles ejecuciones sobre el mismo botón de análisis.
 */

(() => {
  const MENSAJE_PROCESANDO = (
    "Analizando documento… Esto puede tardar unos segundos."
  );

  function estaActivo(boton) {
    return boton?.dataset.procesandoAdjunto === "true";
  }

  function mostrarEstado(estado, mensaje = MENSAJE_PROCESANDO) {
    if (!estado) return;

    const indicador = document.createElement("span");
    indicador.className = "spinner-border spinner-border-sm me-2";
    indicador.setAttribute("aria-hidden", "true");

    const texto = document.createElement("span");
    texto.textContent = mensaje;

    estado.replaceChildren(indicador, texto);
    estado.classList.remove("d-none");
    estado.classList.add("attachment-processing-status");
    estado.setAttribute("role", "status");
    estado.setAttribute("aria-live", "polite");
    estado.setAttribute("aria-atomic", "true");
    estado.setAttribute("aria-busy", "true");
  }

  function iniciar({
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
