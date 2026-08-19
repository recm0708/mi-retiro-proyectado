"use strict";

/* ============================================================
   Gestión e invalidación controlada de datos locales
   ============================================================ */

/*
 * Centraliza las acciones destructivas del asistente: limpiar un paso,
 * reiniciar la simulación y borrar exclusivamente las claves propias de
 * Mi Retiro Proyectado. La invalidación conserva las dependencias previas
 * que siguen siendo válidas y elimina los resultados descendientes.
 */

const CLAVE_GESTION_SIMULACION = "miRetiroProyectado.simulacion";
const CLAVE_GESTION_PRIVACIDAD = "miRetiroProyectado.privacidadConsentimiento";
const CLAVE_GESTION_PRIVACIDAD_SESION = "miRetiroProyectado.privacidadConsentimientoSesion";
const CLAVE_GESTION_TEMA = "miRetiroProyectado.tema";

// Identificadores pre-beta que solo se reconocen durante el borrado integral.
// No se leen ni migran para restaurar estado antiguo.
const CLAVES_GESTION_LEGACY_SESION = [
  "calculadoraPensionCSS.simulacion",
  "calculadoraPensionCSS.privacidadConsentimientoSesion",
];

const CLAVES_GESTION_LEGACY_LOCAL = [
  "calculadoraPensionCSS.privacidadConsentimiento",
  "mi-retiro-proyectado-tema",
];

let accionGestionDatosPendiente = null;


/**
 * Obtiene el estado actual usando la API del asistente o el almacenamiento
 * como respaldo cuando la función principal no está disponible.
 *
 * @returns {Object|null} Estado de simulación utilizable.
 */
function estadoSimulacionParaGestion() {
  if (typeof obtenerSimulacion === "function") {
    return obtenerSimulacion();
  }

  try {
    const texto = window.sessionStorage.getItem(CLAVE_GESTION_SIMULACION);
    return texto ? JSON.parse(texto) : null;
  } catch {
    return null;
  }
}


function guardarEstadoGestion(simulacion) {
  if (typeof guardarSimulacion === "function") {
    guardarSimulacion(simulacion);
    return;
  }

  window.sessionStorage.setItem(
    CLAVE_GESTION_SIMULACION,
    JSON.stringify(simulacion),
  );
}


function objetoTieneDatos(valor) {
  return Boolean(
    valor
    && typeof valor === "object"
    && Object.keys(valor).length,
  );
}


/**
 * Determina si un paso contiene información que requiere confirmación antes
 * de una operación destructiva.
 *
 * @param {number} numeroPaso Paso evaluado.
 * @param {Object|null} simulacion Estado actual.
 * @returns {boolean} true cuando existen datos relevantes.
 */
function pasoTieneDatos(numeroPaso, simulacion) {
  if (!simulacion) return false;

  if (numeroPaso === 1) {
    return Boolean(
      objetoTieneDatos(simulacion.persona)
      || simulacion.importacion_comprobante_confirmada
      || simulacion.referencia_mi_retiro_seguro,
    );
  }

  if (numeroPaso === 2) {
    return Boolean(
      objetoTieneDatos(simulacion.cuotas)
      || objetoTieneDatos(simulacion.origen_campos_cuotas)
      || simulacion.resumen_cuotas,
    );
  }

  if (numeroPaso === 3) {
    return Boolean(
      simulacion.historial
      || simulacion.resumen_historial
      || objetoTieneDatos(simulacion.origen_campos_historial)
      || simulacion.ficha_digital_importada
      || simulacion.importacion_ficha_digital_confirmada
      || simulacion.detalle_anio_actual
      || simulacion.resumen_detalle_anio_actual
      || objetoTieneDatos(simulacion.salario)
      || simulacion.resumen_salario,
    );
  }

  if (numeroPaso === 4) {
    return Boolean(
      objetoTieneDatos(simulacion.proyeccion)
      || simulacion.resumen_proyeccion
      || simulacion.resumen_linea_tiempo,
    );
  }

  if (numeroPaso === 5) {
    return Boolean(
      objetoTieneDatos(simulacion.retiro)
      || simulacion.resumen_retiro
      || simulacion.escenario_retiro_seleccionado,
    );
  }

  if (numeroPaso === 6) {
    return Boolean(
      simulacion.escenario_salarial_seleccionado
      || simulacion.resultado_sebd_normal
      || simulacion.resultado_sebd_acreditado
      || simulacion.resultado_mixto
      || simulacion.resultado_mixto_acreditado
      || simulacion.resultado_sucgs
      || simulacion.resultado_sucgs_acreditado
      || objetoTieneDatos(simulacion.configuracion_mixto_resultados)
      || objetoTieneDatos(simulacion.configuracion_sucgs_resultados),
    );
  }

  return false;
}


function limpiarResultadosPaso6(simulacion) {
  simulacion.escenario_salarial_seleccionado = null;
  simulacion.resultado_sebd_normal = null;
  simulacion.resultado_sebd_acreditado = null;
  simulacion.configuracion_mixto_resultados = {};
  simulacion.resultado_mixto = null;
  simulacion.resultado_mixto_acreditado = null;
  simulacion.configuracion_sucgs_resultados = {};
  simulacion.resultado_sucgs = null;
  simulacion.resultado_sucgs_acreditado = null;
}


function limpiarDesdePaso5(simulacion) {
  simulacion.retiro = {};
  simulacion.resumen_retiro = null;
  simulacion.escenario_retiro_seleccionado = null;
  limpiarResultadosPaso6(simulacion);
}


function limpiarDesdePaso4(simulacion) {
  simulacion.proyeccion = {};
  simulacion.resumen_proyeccion = null;
  simulacion.resumen_linea_tiempo = null;
  limpiarDesdePaso5(simulacion);
}


function limpiarDesdePaso3(simulacion) {
  simulacion.modo_historial = "MANUAL";
  simulacion.historial = null;
  delete simulacion.historial_anio_inicio_temporal;
  simulacion.origen_campos_historial = {};
  simulacion.resumen_historial = null;

  simulacion.ficha_digital_importada = null;
  simulacion.importacion_ficha_digital_confirmada = false;
  simulacion.campos_editados_importacion_ficha = [];
  simulacion.detalle_anio_actual_habilitado = false;
  simulacion.detalle_anio_actual = null;
  simulacion.origen_campos_detalle_anio_actual = {};
  simulacion.resumen_detalle_anio_actual = null;
  simulacion.ultimo_mes_cuotas_derivado = null;

  simulacion.origen_salario_proyeccion = "MANUAL";
  simulacion.salario = {};
  simulacion.resumen_salario = null;

  limpiarDesdePaso4(simulacion);
}


function limpiarDesdePaso2(simulacion) {
  simulacion.cuotas = {};
  simulacion.origen_campos_cuotas = {};
  simulacion.resumen_cuotas = null;
  limpiarDesdePaso3(simulacion);
}


/**
 * Limpia el paso indicado e invalida sus dependencias posteriores.
 *
 * @param {number} numeroPaso Paso que se reinicia.
 * @param {Object} simulacion Estado mutable del asistente.
 */
function limpiarPasoEnEstado(numeroPaso, simulacion) {
  if (numeroPaso === 1) {
    const vacia = typeof crearSimulacionVacia === "function"
      ? crearSimulacionVacia()
      : { paso_actual: 1 };
    return vacia;
  }

  const nueva = { ...simulacion };

  if (numeroPaso === 2) limpiarDesdePaso2(nueva);
  if (numeroPaso === 3) limpiarDesdePaso3(nueva);
  if (numeroPaso === 4) limpiarDesdePaso4(nueva);
  if (numeroPaso === 5) limpiarDesdePaso5(nueva);
  if (numeroPaso === 6) limpiarResultadosPaso6(nueva);

  nueva.paso_actual = numeroPaso;
  return nueva;
}


function obtenerNombrePasoGestion(numeroPaso) {
  const nombres = {
    1: "Datos personales",
    2: "Cuotas",
    3: "Historial",
    4: "Proyección",
    5: "Retiro",
    6: "Resultados",
  };
  return nombres[numeroPaso] || `Paso ${numeroPaso}`;
}


function modalGestionDatos() {
  const elemento = document.getElementById("modal-gestion-datos");
  if (!elemento || typeof bootstrap === "undefined") return null;
  return bootstrap.Modal.getOrCreateInstance(elemento);
}


function configurarModalGestion({ titulo, mensaje, confirmar, tipo }) {
  const tituloNodo = document.getElementById("gestion-datos-titulo");
  const mensajeNodo = document.getElementById("gestion-datos-mensaje");
  const boton = document.getElementById("btn-gestion-datos-confirmar");

  if (tituloNodo) tituloNodo.textContent = titulo;
  if (mensajeNodo) mensajeNodo.textContent = mensaje;
  if (boton) {
    boton.textContent = confirmar;
    boton.classList.toggle("btn-danger", tipo !== "step");
    boton.classList.toggle("btn-outline-danger", tipo === "step");
  }

  accionGestionDatosPendiente = tipo;
  modalGestionDatos()?.show();
}


function anunciarGestionDatos(mensaje) {
  if (typeof anunciarAccesibilidad === "function") {
    anunciarAccesibilidad(mensaje);
  }
}


function actualizarDisponibilidadGestionDatos() {
  const simulacion = estadoSimulacionParaGestion();
  const numeroPaso = Number(simulacion?.paso_actual || 1);
  const disponible = pasoTieneDatos(numeroPaso, simulacion);

  document
    .querySelectorAll('[data-data-action="clear-step"]')
    .forEach((control) => {
      control.disabled = !disponible;
      control.title = disponible
        ? `Limpiar los datos del Paso ${numeroPaso}`
        : `No hay datos que limpiar en el Paso ${numeroPaso}`;
    });
}


function solicitarLimpiarPasoActual() {
  const simulacion = estadoSimulacionParaGestion();
  const numeroPaso = Number(simulacion?.paso_actual || 1);

  if (!pasoTieneDatos(numeroPaso, simulacion)) {
    anunciarGestionDatos(`No hay datos que limpiar en el Paso ${numeroPaso}.`);
    return;
  }

  configurarModalGestion({
    titulo: `Limpiar Paso ${numeroPaso} — ${obtenerNombrePasoGestion(numeroPaso)}`,
    mensaje: (
      `Se eliminarán los datos de este paso y los resultados posteriores que dependan de ellos. `
      + `Los pasos anteriores se conservarán.`
    ),
    confirmar: "Limpiar paso",
    tipo: "step",
  });
}


function solicitarReiniciarSimulacion() {
  const simulacion = estadoSimulacionParaGestion();
  const hayDatos = [1, 2, 3, 4, 5, 6].some(
    (paso) => pasoTieneDatos(paso, simulacion),
  );

  if (!hayDatos) {
    anunciarGestionDatos("La simulación ya está vacía.");
    return;
  }

  configurarModalGestion({
    titulo: "Reiniciar toda la simulación",
    mensaje: (
      "Se eliminarán todos los datos introducidos o importados y todos los cálculos de esta simulación. "
      + "La apariencia y la aceptación vigente de privacidad se conservarán. Esta acción no se puede deshacer."
    ),
    confirmar: "Reiniciar simulación",
    tipo: "simulation",
  });
}


/**
 * Elimina exclusivamente claves propias de Mi Retiro Proyectado.
 *
 * Incluye identificadores pre-beta únicamente para garantizar que el botón
 * de borrado integral no deje una aceptación antigua que pueda reactivar una
 * sesión. No existe lectura, restauración ni migración desde esas claves.
 */
function borrarAlmacenamientoPropioAplicacion() {
  [
    CLAVE_GESTION_SIMULACION,
    CLAVE_GESTION_PRIVACIDAD_SESION,
    ...CLAVES_GESTION_LEGACY_SESION,
  ].forEach((clave) => window.sessionStorage.removeItem(clave));

  [
    CLAVE_GESTION_PRIVACIDAD,
    CLAVE_GESTION_TEMA,
    ...CLAVES_GESTION_LEGACY_LOCAL,
  ].forEach((clave) => window.localStorage.removeItem(clave));
}


function solicitarBorrarDatosAplicacion() {
  configurarModalGestion({
    titulo: "Borrar datos de la aplicación en este navegador",
    mensaje: (
      "Se eliminarán la simulación en curso, la constancia local de aceptación de términos, "
      + "las preferencias de apariencia y demás estados guardados por Mi Retiro Proyectado en este navegador. "
      + "Después volverás a Inicio y se abrirán nuevamente los términos para que puedas decidir si deseas aceptarlos otra vez. "
      + "Esta acción no se puede deshacer."
    ),
    confirmar: "Borrar datos",
    tipo: "browser",
  });
}


/**
 * Ejecuta la acción destructiva previamente confirmada en el modal.
 */
function ejecutarGestionDatosConfirmada() {
  if (accionGestionDatosPendiente === "step") {
    const simulacion = estadoSimulacionParaGestion();
    const numeroPaso = Number(simulacion?.paso_actual || 1);
    const nueva = limpiarPasoEnEstado(numeroPaso, simulacion || {});
    guardarEstadoGestion(nueva);
    window.location.reload();
    return;
  }

  if (accionGestionDatosPendiente === "simulation") {
    const vacia = typeof crearSimulacionVacia === "function"
      ? crearSimulacionVacia()
      : { paso_actual: 1 };
    guardarEstadoGestion(vacia);
    window.location.replace("/simulacion");
    return;
  }

  if (accionGestionDatosPendiente === "browser") {
    borrarAlmacenamientoPropioAplicacion();
    window.location.replace("/?privacidad=1");
  }
}


document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll('[data-data-action="clear-step"]')
    .forEach((control) => control.addEventListener("click", solicitarLimpiarPasoActual));

  document
    .querySelectorAll('[data-data-action="restart-simulation"]')
    .forEach((control) => control.addEventListener("click", solicitarReiniciarSimulacion));

  document
    .querySelectorAll('[data-data-action="clear-browser-data"]')
    .forEach((control) => control.addEventListener("click", solicitarBorrarDatosAplicacion));

  document.getElementById("btn-gestion-datos-confirmar")?.addEventListener(
    "click",
    ejecutarGestionDatosConfirmada,
  );

  actualizarDisponibilidadGestionDatos();

  document.getElementById("modal-gestion-datos")?.addEventListener(
    "hidden.bs.modal",
    () => {
      accionGestionDatosPendiente = null;
    },
  );
});
