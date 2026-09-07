"use strict";

/*
 * Mi Retiro Proyectado — estado temprano del shell.
 *
 * Propósito: Aplica antes del primer pintado la preferencia
 * persistida del sidebar en escritorio.
 * Alcance: Estado visual temprano del shell; no persiste datos
 * ni interviene en autenticación.
 */
(() => {
  const MOBILE_QUERY = "(max-width: 991.98px)";
  const STORAGE_KEY = "miRetiroProyectado.shell.sidebar";

  if (window.matchMedia(MOBILE_QUERY).matches) {
    return;
  }

  let preferencia = null;

  try {
    preferencia = window.localStorage.getItem(
      STORAGE_KEY,
    );
  } catch {
    return;
  }

  if (preferencia !== "collapsed") {
    return;
  }

  const clase = window.location.pathname.startsWith("/dev")
    ? "dev-sidebar-collapsed"
    : "app-sidebar-collapsed";

  document.documentElement.classList.add(clase);
})();
