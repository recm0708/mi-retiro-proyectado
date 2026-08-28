"use strict";

/*
 * Mi Retiro Proyectado — Portal Developer.
 *
 * Propósito: Gestiona interacciones locales del acceso Developer sin persistir credenciales.
 * Alcance: Comportamiento visual local; no almacena secretos ni altera el contrato de autenticación.
 */
(() => {
  document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector("[data-dev-password-toggle]");
    const input = document.getElementById("admin-token");
    if (!toggle || !input) return;

    toggle.addEventListener("click", () => {
      const mostrar = input.type === "password";
      input.type = mostrar ? "text" : "password";
      toggle.textContent = mostrar ? "Ocultar" : "Mostrar";
      toggle.setAttribute("aria-pressed", mostrar ? "true" : "false");
      input.focus();
    });
  });
})();
