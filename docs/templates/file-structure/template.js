"use strict";

/*
 * Mi Retiro Proyectado — Nombre del módulo JavaScript.
 *
 * Propósito: Describir la responsabilidad de interfaz, storage, eventos o API.
 * Alcance: Indicar qué modifica, qué conserva y qué no debe duplicar.
 */

(() => {
  const CLAVE_EJEMPLO = "miRetiroProyectado.ejemplo";

  function cargarEstadoEjemplo() {
    // El storage puede no existir en pruebas, navegación privada o navegadores restringidos.
    try {
      return window.sessionStorage.getItem(CLAVE_EJEMPLO);
    } catch (_error) {
      return null;
    }
  }

  cargarEstadoEjemplo();
})();
