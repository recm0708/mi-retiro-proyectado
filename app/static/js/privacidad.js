"use strict";

/* ============================================================
   UX.4.6b R4 — Consentimiento informado y control de privacidad
   ============================================================ */

const CLAVE_PRIVACIDAD = "calculadoraPensionCSS.privacidadConsentimiento";
const VERSION_PRIVACIDAD = "2026-08-13.2";
const CLAVE_SIMULACION_PRIVACIDAD = "calculadoraPensionCSS.simulacion";
const CLAVE_PRIVACIDAD_SESION = "calculadoraPensionCSS.privacidadConsentimientoSesion";
const MARGEN_FINAL_LECTURA = 18;


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


function abrirCondicionesPrivacidad() {
  const modal = obtenerModalPrivacidad();
  if (!modal) return;

  reiniciarLecturaPrivacidad();
  modal.show();
}


document.addEventListener("DOMContentLoaded", () => {
  const modalElemento = document.getElementById("modal-privacidad-simulacion");
  if (!modalElemento) return;

  const contenido = document.getElementById("privacidad-contenido-desplazable");
  const check = document.getElementById("aceptar-privacidad-check");
  const aceptar = document.getElementById("btn-privacidad-aceptar");
  const rechazar = document.getElementById("btn-privacidad-rechazar");

  contenido?.addEventListener("scroll", actualizarEstadoLecturaPrivacidad, { passive: true });
  window.addEventListener("resize", actualizarEstadoLecturaPrivacidad, { passive: true });

  modalElemento.addEventListener("shown.bs.modal", () => {
    reiniciarLecturaPrivacidad();
    contenido?.focus({ preventScroll: true });
  });

  check?.addEventListener("change", () => {
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
    if (!check?.checked || !lecturaPrivacidadCompletada()) return;

    guardarConsentimientoPrivacidad();
    obtenerModalPrivacidad()?.hide();
    limpiarParametroPrivacidad();
  });

  rechazar?.addEventListener("click", () => {
    borrarDatosSimulacionPorPrivacidad();
    window.location.replace("/");
  });

  if (!obtenerConsentimientoPrivacidad() || debeForzarVistaPrivacidad()) {
    abrirCondicionesPrivacidad();
  }
});
