"use strict";

/* ============================================================
   UX.4.6d R7 — Consentimiento y consulta no disruptiva
   ============================================================ */

const CLAVE_PRIVACIDAD = "calculadoraPensionCSS.privacidadConsentimiento";
const VERSION_PRIVACIDAD = "2026-08-16.1";
const CLAVE_SIMULACION_PRIVACIDAD = "calculadoraPensionCSS.simulacion";
const CLAVE_PRIVACIDAD_SESION = "calculadoraPensionCSS.privacidadConsentimientoSesion";
const MARGEN_FINAL_LECTURA = 18;

let modoPrivacidadActual = "consentimiento";
let contextoPrivacidadActual = "simulacion";


function obtenerConsentimientoPrivacidad() {
  try {
    const texto = window.localStorage.getItem(CLAVE_PRIVACIDAD);
    if (!texto) return null;

    const consentimiento = JSON.parse(texto);
    const aceptadoEnSesion = (
      window.sessionStorage.getItem(CLAVE_PRIVACIDAD_SESION)
      === VERSION_PRIVACIDAD
    );

    if (
      consentimiento?.version !== VERSION_PRIVACIDAD
      || consentimiento?.aceptado !== true
      || !aceptadoEnSesion
    ) {
      return null;
    }

    return consentimiento;
  } catch {
    return null;
  }
}


function guardarConsentimientoPrivacidad() {
  window.localStorage.setItem(
    CLAVE_PRIVACIDAD,
    JSON.stringify({
      version: VERSION_PRIVACIDAD,
      aceptado: true,
      aceptado_en: new Date().toISOString(),
    }),
  );

  window.sessionStorage.setItem(
    CLAVE_PRIVACIDAD_SESION,
    VERSION_PRIVACIDAD,
  );
}


function borrarDatosSimulacionPorPrivacidad() {
  window.sessionStorage.removeItem(CLAVE_SIMULACION_PRIVACIDAD);
  window.sessionStorage.removeItem(CLAVE_PRIVACIDAD_SESION);
  window.localStorage.removeItem(CLAVE_PRIVACIDAD);
}


function obtenerModalPrivacidad() {
  const elemento = document.getElementById("modal-privacidad-simulacion");
  if (!elemento || typeof bootstrap === "undefined") return null;

  return bootstrap.Modal.getOrCreateInstance(elemento, {
    backdrop: "static",
    keyboard: false,
  });
}


function debeForzarVistaPrivacidad() {
  return new URLSearchParams(window.location.search).get("privacidad") === "1";
}


function limpiarParametroPrivacidad() {
  const url = new URL(window.location.href);
  if (!url.searchParams.has("privacidad")) return;

  url.searchParams.delete("privacidad");
  const destino = `${url.pathname}${url.search}${url.hash}`;
  window.history.replaceState({}, "", destino);
}


function esRutaSimulacion() {
  return window.location.pathname === "/simulacion";
}


function lecturaPrivacidadCompletada() {
  const contenido = document.getElementById("privacidad-contenido-desplazable");
  if (!contenido) return false;

  return (
    contenido.scrollHeight
    - contenido.scrollTop
    - contenido.clientHeight
    <= MARGEN_FINAL_LECTURA
  );
}


function actualizarEstadoLecturaPrivacidad() {
  if (modoPrivacidadActual !== "consentimiento") return;

  const check = document.getElementById("aceptar-privacidad-check");
  const estado = document.getElementById("privacidad-lectura-estado");
  const aceptar = document.getElementById("btn-privacidad-aceptar");

  if (!check) return;

  const lecturaCompleta = lecturaPrivacidadCompletada();

  if (lecturaCompleta) {
    check.disabled = false;
    if (estado) {
      estado.textContent = "";
      estado.hidden = true;
    }
  } else {
    check.checked = false;
    check.disabled = true;
    if (aceptar) aceptar.disabled = true;
    if (estado) {
      estado.hidden = false;
      estado.textContent = "Desplázate hasta el final del documento para habilitar esta casilla.";
    }
  }
}


function reiniciarLecturaPrivacidad() {
  const contenido = document.getElementById("privacidad-contenido-desplazable");
  const check = document.getElementById("aceptar-privacidad-check");
  const aceptar = document.getElementById("btn-privacidad-aceptar");

  if (contenido) contenido.scrollTop = 0;
  if (check) {
    check.checked = false;
    check.disabled = true;
  }
  if (aceptar) aceptar.disabled = true;

  window.requestAnimationFrame(actualizarEstadoLecturaPrivacidad);
}


function configurarModoPrivacidad(modo) {
  modoPrivacidadActual = modo === "revision" ? "revision" : "consentimiento";

  const kicker = document.getElementById("privacidad-modal-kicker");
  const resumen = document.getElementById("privacidad-simulacion-resumen");
  const footer = document.getElementById("privacidad-consent-footer");

  if (modoPrivacidadActual === "revision") {
    if (kicker) kicker.textContent = "Consulta de privacidad";
    if (resumen) {
      resumen.textContent = (
        "Consulta las condiciones vigentes. Revisarlas no modifica tu aceptación ni exige aceptarlas nuevamente."
      );
    }
    if (footer) footer.hidden = true;
    return;
  }

  if (kicker) kicker.textContent = "Antes de comenzar";
  if (resumen) {
    resumen.textContent = "Lee el documento completo. Al llegar al final podrás habilitar la aceptación.";
  }
  if (footer) footer.hidden = false;
}


function abrirCondicionesPrivacidad(modo = "consentimiento", contexto = "simulacion") {
  const modal = obtenerModalPrivacidad();
  if (!modal) return;

  contextoPrivacidadActual = contexto;
  configurarModoPrivacidad(modo);

  const contenido = document.getElementById("privacidad-contenido-desplazable");
  if (modoPrivacidadActual === "consentimiento") {
    reiniciarLecturaPrivacidad();
  } else if (contenido) {
    contenido.scrollTop = 0;
  }

  modal.show();
}


function rechazarPrivacidad() {
  if (contextoPrivacidadActual === "fuentes") {
    obtenerModalPrivacidad()?.hide();
    return;
  }

  borrarDatosSimulacionPorPrivacidad();
  window.location.replace("/");
}


function cerrarModalPrivacidad() {
  if (modoPrivacidadActual === "revision" || contextoPrivacidadActual === "fuentes") {
    obtenerModalPrivacidad()?.hide();
    return;
  }

  // En Simular, cerrar el consentimiento sin aceptarlo impide continuar.
  rechazarPrivacidad();
}


function manejarEscapePrivacidad(evento) {
  if (evento.key !== "Escape") return;

  const modalElemento = document.getElementById("modal-privacidad-simulacion");
  if (!modalElemento?.classList.contains("show")) return;

  // Bootstrap usa un efecto visual cuando el modal es estático. Interceptamos
  // Escape antes de ese comportamiento para que la acción sea inequívoca.
  evento.preventDefault();
  evento.stopImmediatePropagation();
  cerrarModalPrivacidad();
}


document.addEventListener("DOMContentLoaded", () => {
  const modalElemento = document.getElementById("modal-privacidad-simulacion");
  if (!modalElemento) return;

  const contenido = document.getElementById("privacidad-contenido-desplazable");
  const check = document.getElementById("aceptar-privacidad-check");
  const aceptar = document.getElementById("btn-privacidad-aceptar");
  const rechazar = document.getElementById("btn-privacidad-rechazar");
  const cerrar = document.getElementById("btn-privacidad-cerrar");

  contenido?.addEventListener("scroll", actualizarEstadoLecturaPrivacidad, { passive: true });
  window.addEventListener("resize", actualizarEstadoLecturaPrivacidad, { passive: true });

  modalElemento.addEventListener("shown.bs.modal", () => {
    if (modoPrivacidadActual === "consentimiento") {
      reiniciarLecturaPrivacidad();
    }
    contenido?.focus({ preventScroll: true });
  });

  check?.addEventListener("change", () => {
    if (modoPrivacidadActual !== "consentimiento") return;

    if (!lecturaPrivacidadCompletada()) {
      check.checked = false;
      check.disabled = true;
      if (aceptar) aceptar.disabled = true;
      actualizarEstadoLecturaPrivacidad();
      return;
    }

    if (aceptar) aceptar.disabled = !check.checked;
  });

  aceptar?.addEventListener("click", () => {
    if (modoPrivacidadActual !== "consentimiento") return;
    if (!check?.checked || !lecturaPrivacidadCompletada()) return;

    guardarConsentimientoPrivacidad();
    obtenerModalPrivacidad()?.hide();
    limpiarParametroPrivacidad();
  });

  rechazar?.addEventListener("click", rechazarPrivacidad);
  cerrar?.addEventListener("click", cerrarModalPrivacidad);
  document.addEventListener("keydown", manejarEscapePrivacidad, true);

  document
    .querySelectorAll('[data-privacy-action="review"]')
    .forEach((control) => {
      control.addEventListener("click", () => {
        const consentimiento = obtenerConsentimientoPrivacidad();
        abrirCondicionesPrivacidad(
          consentimiento ? "revision" : "consentimiento",
          "fuentes",
        );
      });
    });

  const consentimiento = obtenerConsentimientoPrivacidad();

  if (esRutaSimulacion() && !consentimiento) {
    abrirCondicionesPrivacidad("consentimiento", "simulacion");
  } else if (debeForzarVistaPrivacidad()) {
    abrirCondicionesPrivacidad(
      consentimiento ? "revision" : "consentimiento",
      "fuentes",
    );
    limpiarParametroPrivacidad();
  }
});
