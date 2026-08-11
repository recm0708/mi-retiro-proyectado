"use strict";


/* ============================================================
   Navegación rápida persistente del asistente
   ============================================================ */

/*
 * La barra permanece visible mientras se desplaza un paso largo.
 * No duplica lógica de negocio: delega en los formularios y botones
 * originales para conservar sus validaciones.
 */


/**
 * Devuelve el estado y la acción principal apropiados para el paso.
 *
 * @returns {Object} Configuración visible de la barra.
 */
function obtenerConfiguracionNavegacionFlotante() {
  const simulacion = obtenerSimulacion();

  if (pasoActual === 1) {
    return {
      estado: "Paso 1 de 6 · Datos personales",
      etiqueta: "Continuar",
      deshabilitado: false,
    };
  }

  if (pasoActual === 2) {
    return {
      estado: (
        simulacion.resumen_cuotas
          ? "Paso 2 de 6 · Cuotas analizadas"
          : "Paso 2 de 6 · Falta analizar cuotas"
      ),
      etiqueta: (
        simulacion.resumen_cuotas
          ? "Continuar al historial"
          : "Analizar cuotas"
      ),
      deshabilitado: false,
    };
  }

  if (pasoActual === 3) {
    const modo = (
      simulacion.modo_historial
      || "MANUAL"
    );

    if (
      modo === "MANUAL"
      && !simulacion.resumen_historial
    ) {
      return {
        estado: "Paso 3 de 6 · Falta analizar historial",
        etiqueta: "Analizar historial",
        deshabilitado: false,
      };
    }

    if (!simulacion.resumen_salario) {
      return {
        estado: "Paso 3 de 6 · Falta analizar salario",
        etiqueta: "Analizar salario",
        deshabilitado: false,
      };
    }

    return {
      estado: "Paso 3 de 6 · Historial y salario listos",
      etiqueta: "Continuar a proyección",
      deshabilitado: false,
    };
  }

  if (pasoActual === 4) {
    return {
      estado: (
        simulacion.resumen_proyeccion
          ? "Paso 4 de 6 · Proyección generada"
          : "Paso 4 de 6 · Falta generar proyección"
      ),
      etiqueta: (
        simulacion.resumen_proyeccion
          ? "Continuar a retiro"
          : "Generar proyección"
      ),
      deshabilitado: false,
    };
  }

  if (pasoActual === 5) {
    if (!simulacion.resumen_retiro) {
      return {
        estado: "Paso 5 de 6 · Falta analizar retiro",
        etiqueta: "Analizar retiro",
        deshabilitado: false,
      };
    }

    if (
      simulacion.resumen_retiro
        .proyeccion_salarial_cubre_escenarios
      === false
    ) {
      return {
        estado: "Paso 5 de 6 · Debes ampliar la proyección salarial",
        etiqueta: "Ajustar proyección",
        deshabilitado: false,
      };
    }

    return {
      estado: "Paso 5 de 6 · Análisis listo",
      etiqueta: "Paso 6 próximamente",
      deshabilitado: true,
    };
  }

  return {
    estado: `Paso ${pasoActual} de 6`,
    etiqueta: "Continuar",
    deshabilitado: true,
  };
}


/**
 * Actualiza textos y disponibilidad de la barra persistente.
 */
function actualizarNavegacionFlotante() {
  const barra = document.getElementById(
    "wizard-sticky-nav",
  );

  if (!barra) {
    return;
  }

  const configuracion = (
    obtenerConfiguracionNavegacionFlotante()
  );

  const botonVolver = document.getElementById(
    "wizard-sticky-back",
  );

  botonVolver.textContent = (
    pasoActual === 1
      ? "← Inicio"
      : "← Anterior"
  );

  document.getElementById(
    "wizard-sticky-status",
  ).textContent = configuracion.estado;

  const principal = document.getElementById(
    "wizard-sticky-primary",
  );

  principal.textContent = configuracion.etiqueta;
  principal.disabled = configuracion.deshabilitado;
}


/**
 * Ejecuta la misma acción que el control principal del paso.
 */
function ejecutarAccionPrimariaFlotante() {
  const simulacion = obtenerSimulacion();

  if (pasoActual === 1) {
    document.getElementById(
      "form-datos-personales",
    ).requestSubmit();
    return;
  }

  if (pasoActual === 2) {
    if (simulacion.resumen_cuotas) {
      document.getElementById(
        "btn-continuar-paso-3",
      ).click();
    } else {
      document.getElementById(
        "form-cuotas",
      ).requestSubmit();
    }

    return;
  }

  if (pasoActual === 3) {
    const modo = (
      simulacion.modo_historial
      || "MANUAL"
    );

    if (
      modo === "MANUAL"
      && !simulacion.resumen_historial
    ) {
      document.getElementById(
        "btn-analizar-historial",
      ).click();
      return;
    }

    if (!simulacion.resumen_salario) {
      document.getElementById(
        "form-salario",
      ).requestSubmit();
      return;
    }

    document.getElementById(
      "btn-continuar-paso-4",
    ).click();
    return;
  }

  if (pasoActual === 4) {
    if (simulacion.resumen_proyeccion) {
      document.getElementById(
        "btn-continuar-paso-5",
      ).click();
    } else {
      document.getElementById(
        "form-proyeccion",
      ).requestSubmit();
    }

    return;
  }

  if (pasoActual === 5) {
    if (!simulacion.resumen_retiro) {
      document.getElementById(
        "form-retiro",
      ).requestSubmit();
      return;
    }

    if (
      simulacion.resumen_retiro
        .proyeccion_salarial_cubre_escenarios
      === false
    ) {
      document.getElementById(
        "btn-ajustar-proyeccion-retiro",
      ).click();
    }
  }
}


/**
 * Retrocede un paso sin alterar los datos guardados.
 */
function ejecutarRetrocesoFlotante() {
  if (pasoActual <= 1) {
    window.location.href = "/";
    return;
  }

  mostrarPaso(
    pasoActual - 1,
  );
}


document.addEventListener(
  "DOMContentLoaded",
  () => {
    document.getElementById(
      "wizard-sticky-back",
    ).addEventListener(
      "click",
      ejecutarRetrocesoFlotante,
    );

    document.getElementById(
      "wizard-sticky-primary",
    ).addEventListener(
      "click",
      ejecutarAccionPrimariaFlotante,
    );

    actualizarNavegacionFlotante();
  },
);
