"use strict";


/* ============================================================
   Navegación común del asistente
   ============================================================ */

/*
 * El asistente dispone de una barra superior y otra inferior con el mismo
 * contrato funcional. La superior puede mantenerse visible en escritorio
 * sin ampliar el ancho del contenido; la inferior ofrece cierre natural del paso.
 * Ambas delegan en los formularios y botones originales para conservar validaciones.
 */


const PASOS_NAVEGACION = [
  { numero: 1, nombre: "Datos personales" },
  { numero: 2, nombre: "Cuotas" },
  { numero: 3, nombre: "Historial" },
  { numero: 4, nombre: "Proyección" },
  { numero: 5, nombre: "Retiro" },
  { numero: 6, nombre: "Resultados" },
];


/**
 * Indica si un paso puede abrirse directamente con el estado guardado.
 *
 * Los pasos anteriores siempre pueden revisarse cuando sus datos base
 * ya existen. Los pasos posteriores se habilitan solo si continúan
 * cumpliéndose los prerrequisitos que usa el flujo normal.
 *
 * @param {number} numeroPaso Paso solicitado.
 * @param {Object} simulacion Estado persistido del asistente.
 * @returns {boolean} true cuando el salto es seguro.
 */
function puedeAccederDirectamenteAPaso(
  numeroPaso,
  simulacion,
) {
  if (numeroPaso === 1) {
    return true;
  }

  const persona = simulacion.persona || {};
  const personaLista = Boolean(
    persona.fecha_nacimiento
    && persona.sexo
    && persona.sistema,
  );

  if (numeroPaso === 2) {
    return personaLista;
  }

  if (numeroPaso === 3) {
    return Boolean(
      personaLista
      && simulacion.resumen_cuotas,
    );
  }

  const historialListo = (
    typeof paso3EstaCompleto === "function"
      ? paso3EstaCompleto(simulacion)
      : (
          ((simulacion.modo_historial || "MANUAL") !== "MANUAL"
            || Boolean(simulacion.resumen_historial))
          && Boolean(simulacion.resumen_salario)
        )
  );

  if (numeroPaso === 4) {
    return Boolean(
      simulacion.resumen_cuotas
      && historialListo,
    );
  }

  if (numeroPaso === 5) {
    return Boolean(
      simulacion.resumen_proyeccion,
    );
  }

  if (numeroPaso === 6) {
    return Boolean(
      simulacion.resumen_retiro
      && simulacion.escenario_retiro_seleccionado
      && simulacion.resumen_retiro
        .proyeccion_salarial_cubre_escenarios !== false,
    );
  }

  return false;
}


/**
 * Actualiza los accesos directos del progreso y del selector persistente.
 */
function actualizarNavegacionDirecta() {
  const simulacion = obtenerSimulacion();

  document
    .querySelectorAll(".wizard-step")
    .forEach((control) => {
      const numeroPaso = Number(
        control.dataset.step,
      );
      const disponible = (
        numeroPaso === pasoActual
        || puedeAccederDirectamenteAPaso(
          numeroPaso,
          simulacion,
        )
      );

      control.disabled = !disponible;
      control.setAttribute(
        "aria-current",
        numeroPaso === pasoActual
          ? "step"
          : "false",
      );

      const paso = PASOS_NAVEGACION.find(
        (item) => item.numero === numeroPaso,
      );

      control.title = disponible
        ? `Ir al paso ${numeroPaso}: ${paso?.nombre || ""}`
        : "Completa primero los pasos anteriores.";
    });

  document
    .querySelectorAll("[data-wizard-step-jump]")
    .forEach((selector) => {
      Array.from(selector.options).forEach(
        (opcion) => {
          const numeroPaso = Number(opcion.value);
          opcion.disabled = !puedeAccederDirectamenteAPaso(
            numeroPaso,
            simulacion,
          ) && numeroPaso !== pasoActual;
        },
      );

      selector.value = String(pasoActual);
    });
}


/**
 * Prepara los datos visuales necesarios y abre un paso concreto.
 *
 * @param {number} numeroPaso Paso de destino.
 */
function irDirectamenteAPaso(numeroPaso) {
  const simulacion = obtenerSimulacion();

  if (
    numeroPaso !== pasoActual
    && !puedeAccederDirectamenteAPaso(
      numeroPaso,
      simulacion,
    )
  ) {
    actualizarNavegacionDirecta();
    return;
  }

  if (
    numeroPaso === 3
    && typeof sincronizarHistorialConDatosActuales === "function"
  ) {
    sincronizarHistorialConDatosActuales();
  }

  if (
    numeroPaso === 4
    && typeof prepararPasoProyeccion === "function"
  ) {
    prepararPasoProyeccion(simulacion);
  }

  if (
    numeroPaso === 5
    && typeof prepararPasoRetiro === "function"
  ) {
    prepararPasoRetiro();
  }

  mostrarPaso(numeroPaso);

  if (
    numeroPaso === 6
    && typeof prepararPasoResultados === "function"
  ) {
    prepararPasoResultados();
    restaurarResultadoSEBDGuardado();
    restaurarResultadoMixtoGuardado();
  }
}


/**
 * Devuelve el estado y la acción principal apropiados para el paso.
 *
 * @returns {Object} Configuración visible de la barra.
 */
function obtenerConfiguracionNavegacionFlotante() {
  const simulacion = obtenerSimulacion();

  if (pasoActual === 1) {
    const modoDatos = simulacion.modo_datos_personales || "MANUAL";
    const importacionLista = Boolean(
      simulacion.importacion_comprobante_confirmada
      && simulacion.referencia_mi_retiro_seguro,
    );

    if (modoDatos === "MI_RETIRO_SEGURO" && !importacionLista) {
      return {
        estado: "Paso 1 de 6 · Importa y revisa el documento",
        etiqueta: "Importa datos para continuar",
        deshabilitado: true,
      };
    }

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
    const listo = (
      typeof paso3EstaCompleto === "function"
      && paso3EstaCompleto(simulacion)
    );

    return {
      estado: listo
        ? "Paso 3 de 6 · Historial y base listos"
        : "Paso 3 de 6 · Falta analizar historial",
      etiqueta: listo
        ? "Continuar a proyección"
        : "Analizar historial",
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

    if (!simulacion.escenario_retiro_seleccionado) {
      return {
        estado: "Paso 5 de 6 · Selecciona un escenario futuro",
        etiqueta: "Selecciona escenario",
        deshabilitado: true,
      };
    }

    return {
      estado: "Paso 5 de 6 · Escenario listo para calcular",
      etiqueta: "Continuar a resultados",
      deshabilitado: false,
    };
  }

  if (pasoActual === 6) {
    const sistema = simulacion.persona?.sistema;

    if (sistema === "SEBD") {
      return {
        estado: (
          simulacion.resultado_sebd_normal
            ? "Paso 6 de 6 · Resultado SEBD calculado"
            : "Paso 6 de 6 · Listo para calcular SEBD"
        ),
        etiqueta: (
          simulacion.resultado_sebd_normal
            ? "Recalcular pensión"
            : "Calcular pensión SEBD"
        ),
        deshabilitado: false,
      };
    }

    if (sistema === "MIXTO") {
      return {
        estado: (
          simulacion.resultado_mixto
            ? "Paso 6 de 6 · Resultado Mixto calculado"
            : "Paso 6 de 6 · Listo para calcular Mixto"
        ),
        etiqueta: (
          simulacion.resultado_mixto
            ? "Recalcular Mixto"
            : "Calcular prestación Mixto"
        ),
        deshabilitado: false,
      };
    }

    if (sistema === "SUCGS") {
      return {
        estado: (
          simulacion.resultado_sucgs
            ? "Paso 6 de 6 · Resultado SUCGS calculado"
            : "Paso 6 de 6 · Listo para calcular SUCGS"
        ),
        etiqueta: (
          simulacion.resultado_sucgs
            ? "Recalcular SUCGS"
            : "Calcular prestación SUCGS"
        ),
        deshabilitado: false,
      };
    }

    return {
      estado: "Paso 6 de 6 · Sistema por identificar",
      etiqueta: "Identificar sistema",
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
  const barras = document.querySelectorAll("[data-wizard-nav]");

  if (!barras.length) {
    return;
  }

  const configuracion = (
    obtenerConfiguracionNavegacionFlotante()
  );

  document
    .querySelectorAll('[data-wizard-action="back"]')
    .forEach((botonVolver) => {
      botonVolver.textContent = (
        pasoActual === 1
          ? "← Inicio"
          : "← Anterior"
      );
    });

  document
    .querySelectorAll("[data-wizard-status]")
    .forEach((estado) => {
      estado.textContent = configuracion.estado;
    });

  document
    .querySelectorAll('[data-wizard-action="primary"]')
    .forEach((principal) => {
      principal.textContent = configuracion.etiqueta;
      principal.disabled = configuracion.deshabilitado;
    });
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
      if (typeof continuarDesdePasoCuotas === "function") {
        continuarDesdePasoCuotas();
      }
    } else {
      document.getElementById(
        "form-cuotas",
      ).requestSubmit();
    }

    return;
  }

  if (pasoActual === 3) {
    if (
      typeof paso3EstaCompleto === "function"
      && paso3EstaCompleto(simulacion)
    ) {
      if (typeof continuarDesdePasoHistorial === "function") {
        continuarDesdePasoHistorial();
      }
    } else if (typeof analizarPasoHistorialCompleto === "function") {
      analizarPasoHistorialCompleto();
    }

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
      return;
    }

    if (simulacion.escenario_retiro_seleccionado) {
      document.getElementById(
        "btn-continuar-paso-6",
      ).click();
    }

    return;
  }

  if (pasoActual === 6) {
    if (simulacion.persona?.sistema === "SEBD") {
      document.getElementById(
        "btn-calcular-resultado-sebd",
      ).click();
      return;
    }

    if (simulacion.persona?.sistema === "MIXTO") {
      document.getElementById(
        "btn-calcular-resultado-mixto",
      ).click();
      return;
    }

    if (simulacion.persona?.sistema === "SUCGS") {
      document.getElementById(
        "btn-calcular-resultado-sucgs",
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
    document
      .querySelectorAll('[data-wizard-action="back"]')
      .forEach((control) => {
        control.addEventListener(
          "click",
          ejecutarRetrocesoFlotante,
        );
      });

    document
      .querySelectorAll('[data-wizard-action="primary"]')
      .forEach((control) => {
        control.addEventListener(
          "click",
          ejecutarAccionPrimariaFlotante,
        );
      });

    document
      .querySelectorAll("[data-wizard-step-jump]")
      .forEach((selector) => {
        selector.addEventListener(
          "change",
          (evento) => {
            irDirectamenteAPaso(
              Number(evento.target.value),
            );
          },
        );
      });

    document
      .querySelectorAll(".wizard-step")
      .forEach((control) => {
        control.addEventListener(
          "click",
          () => {
            irDirectamenteAPaso(
              Number(control.dataset.step),
            );
          },
        );
      });

    actualizarNavegacionFlotante();
    actualizarNavegacionDirecta();
  },
);
