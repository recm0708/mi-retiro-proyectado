"use strict";

/*
 * Mi Retiro Proyectado — modalidad de simulación.
 *
 * Propósito: Gestiona la elección consciente entre captura Manual
 * y preparación Asistida, junto con la completitud del recorrido.
 *
 * Alcance: Los documentos pueden preparar datos verificables,
 * pero nunca seleccionan decisiones personales por el usuario.
 */

const MODOS_FLUJO_SIMULACION = new Set([
  "MANUAL",
  "ASISTIDO",
]);


function origenEsDocumental(
  origen,
) {
  const valor = String(
    origen || "",
  ).toUpperCase();

  return Boolean(
    valor.includes(
      "MI_RETIRO_SEGURO",
    )
    || valor.includes(
      "FICHA_DIGITAL",
    )
  );
}


function mapaContieneOrigenDocumental(
  mapa,
) {
  if (
    !mapa
    || typeof mapa !== "object"
  ) {
    return false;
  }

  return origenEsDocumental(
    JSON.stringify(
      mapa,
    ),
  );
}


function simulacionTieneImportaciones(
  simulacion,
) {
  return Boolean(
    simulacion.referencia_mi_retiro_seguro
    || simulacion
      .referencia_mi_retiro_seguro_original
    || simulacion.importacion_comprobante_confirmada
    || simulacion.ficha_digital_importada
    || simulacion.ficha_digital_importada_original
    || simulacion.importacion_ficha_digital_confirmada
    || mapaContieneOrigenDocumental(
      simulacion.origen_campos_persona,
    )
    || mapaContieneOrigenDocumental(
      simulacion.origen_campos_cuotas,
    )
    || mapaContieneOrigenDocumental(
      simulacion.origen_campos_historial,
    )
    || mapaContieneOrigenDocumental(
      simulacion
        .origen_campos_detalle_anio_actual,
    )
  );
}


function retirarCamposPersonalesDocumentales(
  simulacion,
) {
  const persona = {
    ...(simulacion.persona || {}),
  };

  const origenes = {
    ...(simulacion.origen_campos_persona || {}),
  };

  Object.entries(
    origenes,
  ).forEach(
    ([campo, origen]) => {
      if (
        origenEsDocumental(
          origen,
        )
      ) {
        delete persona[campo];
      }
    },
  );

  simulacion.persona = persona;
  simulacion.origen_campos_persona = {};
}


function limpiarReferenciasDocumentalesParaManual(
  simulacion,
) {
  retirarCamposPersonalesDocumentales(
    simulacion,
  );

  /*
   * El proyecto ya posee una invalidación descendente canónica.
   * Se reutiliza para evitar mantener dos implementaciones.
   */
  if (
    typeof limpiarDesdePaso2
    === "function"
  ) {
    limpiarDesdePaso2(
      simulacion,
    );
  } else {
    /*
     * Respaldo defensivo: conserva únicamente los datos personales
     * que no procedían de documentos y reinicia el resto.
     */
    const persona = {
      ...(simulacion.persona || {}),
    };

    const base = crearSimulacionVacia();

    Object.assign(
      simulacion,
      base,
    );

    simulacion.persona = persona;
  }

  simulacion.referencia_mi_retiro_seguro = null;
  simulacion.referencia_mi_retiro_seguro_original = null;
  simulacion.importacion_comprobante_confirmada = false;
  simulacion.campos_editados_importacion_comprobante = [];

  simulacion.ficha_digital_importada = null;
  simulacion.ficha_digital_importada_original = null;
  simulacion.importacion_ficha_digital_confirmada = false;
  simulacion.campos_editados_importacion_ficha = [];

  simulacion.origen_persona = "MANUAL";
  simulacion.origen_campos_persona = {};
  simulacion.origen_campos_cuotas = {};
  simulacion.origen_campos_historial = {};
  simulacion.origen_campos_detalle_anio_actual = {};

  simulacion.modo_datos_personales = "MANUAL";
  simulacion.paso_actual = 1;
}


function sincronizarModoDatosPersonales(
  simulacion,
) {
  if (
    simulacion.modo_flujo
    === "MANUAL"
  ) {
    simulacion.modo_datos_personales = (
      "MANUAL"
    );

    return;
  }


  if (
    simulacion.modo_flujo
    === "ASISTIDO"
  ) {
    simulacion.modo_datos_personales = (
      simulacion.importacion_comprobante_confirmada
      && simulacion.referencia_mi_retiro_seguro
        ? "MI_RETIRO_SEGURO"
        : "MANUAL"
    );
  }
}

function aplicarVisibilidadModalidad(
  modo,
) {
  const valido = (
    MODOS_FLUJO_SIMULACION.has(
      modo,
    )
  );


  const gate = document.getElementById(
    "simulation-mode-gate",
  );

  const workspace = document.getElementById(
    "simulation-workspace",
  );

  const assistedPanel = document.getElementById(
    "assisted-preparation-panel",
  );

  const wizard = document.getElementById(
    "simulation-wizard-shell",
  );


  const simulacion = obtenerSimulacion();


  const fuenteConfirmada = Boolean(
    typeof fuenteAsistidaConfirmada
      === "function"
      ? fuenteAsistidaConfirmada(
          simulacion,
        )
      : (
          simulacion.importacion_comprobante_confirmada
          || simulacion.importacion_ficha_digital_confirmada
        )
  );


  function mostrar(
    elemento,
    visible,
  ) {
    if (!elemento) {
      return;
    }


    elemento.hidden = !visible;

    elemento.classList.toggle(
      "d-none",
      !visible,
    );
  }


  /*
   * Primero dejamos un estado completo y coherente
   * y solamente después ocultamos el selector.
   *
   * Así nunca puede quedar una pantalla totalmente vacía.
   */
  if (!valido) {
    mostrar(
      gate,
      true,
    );

    mostrar(
      workspace,
      false,
    );

    mostrar(
      assistedPanel,
      false,
    );

    mostrar(
      wizard,
      false,
    );


    delete document.body.dataset
      .simulationMode;

    return;
  }


  mostrar(
    workspace,
    true,
  );


  const esManual = (
    modo === "MANUAL"
  );

  const esAsistido = (
    modo === "ASISTIDO"
  );


  mostrar(
    assistedPanel,
    esAsistido,
  );


  /*
   * Mi Retiro Seguro posee su propia capa de visibilidad.
   * Al cambiar la modalidad global debemos resincronizarla,
   * porque durante la carga inicial nace oculta mientras
   * todavía no existe una modalidad confirmada.
   */
  if (
    typeof aplicarModoDatosPersonales
    === "function"
  ) {
    aplicarModoDatosPersonales(
      simulacion.modo_datos_personales
        || "MANUAL",
      simulacion,
    );
  }


  mostrar(
    wizard,
    esManual
    || (
      esAsistido
      && fuenteConfirmada
    ),
  );


  /*
   * Cualquier otra superficie marcada como exclusiva
   * de Asistido sigue el mismo estado.
   */
  document
    .querySelectorAll(
      "[data-assisted-only]",
    )
    .forEach(
      (elemento) => {
        if (
          elemento
          === assistedPanel
        ) {
          return;
        }


        elemento.hidden = !esAsistido;
      },
    );


  const badge = document.getElementById(
    "simulation-flow-badge",
  );


  if (badge) {
    badge.textContent = (
      esManual
        ? "Modalidad Manual"
        : "Modalidad Asistida"
    );
  }


  document.body.dataset.simulationMode = (
    modo.toLowerCase()
  );


  /*
   * Se oculta el selector al final.
   * Si alguna pieza previa fallara, el usuario nunca
   * queda atrapado en una página completamente vacía.
   */
  mostrar(
    gate,
    false,
  );
}

function mostrarSelectorModalidad() {
  const gate = document.getElementById(
    "simulation-mode-gate",
  );

  const workspace = document.getElementById(
    "simulation-workspace",
  );


  if (workspace) {
    workspace.hidden = true;

    workspace.classList.add(
      "d-none",
    );
  }


  if (gate) {
    gate.hidden = false;

    gate.classList.remove(
      "d-none",
    );
  }


  delete document.body.dataset
    .simulationMode;


  const titulo = document.getElementById(
    "simulation-mode-title",
  );


  if (titulo) {
    titulo.setAttribute(
      "tabindex",
      "-1",
    );

    titulo.focus({
      preventScroll: true,
    });
  }


  gate?.scrollIntoView({
    block: "start",
    behavior: "auto",
  });
}

function enfocarPasoActual(
  simulacion,
) {
  const numero = Number(
    simulacion.paso_actual || 1,
  );

  const panel = document.querySelector(
    `.wizard-panel[data-panel="${numero}"]`,
  );

  const titulo = panel?.querySelector(
    "h2",
  );

  if (!titulo) {
    return;
  }

  titulo.setAttribute(
    "tabindex",
    "-1",
  );

  titulo.focus({
    preventScroll: false,
  });
}


function simulacionTieneProgresoUsuario(
  simulacion,
) {
  const objetoTieneDatos = (
    objeto,
  ) => Boolean(
    objeto
    && Object.values(
      objeto,
    ).some(
      (valor) => (
        valor !== null
        && valor !== undefined
        && String(valor).trim() !== ""
      ),
    )
  );


  return Boolean(
    Number(
      simulacion.paso_actual || 1
    ) > 1
    || simulacionTieneImportaciones(
      simulacion,
    )
    || objetoTieneDatos(
      simulacion.persona,
    )
    || objetoTieneDatos(
      simulacion.cuotas,
    )
    || simulacion.historial
    || objetoTieneDatos(
      simulacion.salario,
    )
    || objetoTieneDatos(
      simulacion.proyeccion,
    )
    || objetoTieneDatos(
      simulacion.retiro,
    )
    || simulacion.resumen_cuotas
    || simulacion.resumen_historial
    || simulacion.resumen_proyeccion
    || simulacion.resumen_retiro
  );
}


function seleccionarModalidad(
  modo,
) {
  if (
    !MODOS_FLUJO_SIMULACION.has(
      modo,
    )
  ) {
    return;
  }


  const simulacion = obtenerSimulacion();

  const anterior = (
    simulacion.modo_flujo
  );

  const cambioReal = Boolean(
    anterior
    && anterior !== modo
  );


  if (
    cambioReal
    && simulacionTieneProgresoUsuario(
      simulacion,
    )
  ) {
    let mensaje = (
      "Ya existen datos o progreso en esta simulación. "
      + "Cambiar de modalidad puede modificar qué información "
      + "se conserva o qué cálculos deben repetirse. "
      + "¿Deseas continuar?"
    );


    if (
      modo === "MANUAL"
      && simulacionTieneImportaciones(
        simulacion,
      )
    ) {
      mensaje = (
        "Para continuar en modo Manual se retirarán los datos "
        + "que proceden de documentos. Las cuotas, el historial, "
        + "las proyecciones y los resultados posteriores se "
        + "reiniciarán para evitar mezclar procedencias. "
        + "Los datos personales introducidos manualmente se "
        + "conservarán. ¿Deseas continuar?"
      );
    }


    if (
      modo === "ASISTIDO"
      && anterior === "MANUAL"
    ) {
      mensaje = (
        "Cambiar a modo Asistido conservará los datos manuales "
        + "ya guardados. Para continuar deberás confirmar al "
        + "menos Mi Retiro Seguro o Ficha Digital. Cuando "
        + "confirmes información documental, los cálculos "
        + "dependientes podrán requerir actualización. "
        + "¿Deseas continuar?"
      );
    }


    if (
      !window.confirm(
        mensaje,
      )
    ) {
      aplicarVisibilidadModalidad(
        anterior,
      );

      return;
    }
  }


  if (
    modo === "MANUAL"
    && simulacionTieneImportaciones(
      simulacion,
    )
  ) {
    limpiarReferenciasDocumentalesParaManual(
      simulacion,
    );
  }


  simulacion.modo_flujo = modo;

  simulacion.modo_flujo_confirmado = (
    true
  );


  sincronizarModoDatosPersonales(
    simulacion,
  );


  guardarSimulacion(
    simulacion,
  );


  aplicarVisibilidadModalidad(
    modo,
  );


  const actualizado = obtenerSimulacion();


  if (
    modo === "ASISTIDO"
    && (
      typeof fuenteAsistidaConfirmada
      !== "function"
      || !fuenteAsistidaConfirmada(
        actualizado,
      )
    )
  ) {
    const titulo = document.getElementById(
      "assisted-preparation-title",
    );

    titulo?.setAttribute(
      "tabindex",
      "-1",
    );

    titulo?.focus({
      preventScroll: false,
    });

    return;
  }


  if (
    typeof mostrarPaso
    === "function"
  ) {
    mostrarPaso(
      Number(
        actualizado.paso_actual || 1,
      ),
    );
  }


  actualizarCompletitudManual(
    obtenerSimulacion(),
  );


  enfocarPasoActual(
    obtenerSimulacion(),
  );
}

function evaluarCompletitudManual(
  simulacion,
) {
  const persona = (
    simulacion.persona || {}
  );

  const datos = Boolean(
    persona.fecha_nacimiento
    && persona.sexo
    && persona.sistema
  );

  const decisiones = Boolean(
    simulacion
      .modo_historial_confirmado_usuario
    && [
      "MANUAL",
      "SOLO_ACTUAL",
    ].includes(
      simulacion.modo_historial || "",
    )
    && typeof simulacion
      .detalle_anio_actual_habilitado
      === "boolean"
    && simulacion
      .escenario_retiro_seleccionado
  );

  const fechas = Boolean(
    simulacion.resumen_retiro
    && simulacion.resumen_retiro
      .proyeccion_salarial_cubre_escenarios
      !== false
  );

  const dependencias = Boolean(
    simulacion.resumen_cuotas
    && simulacion.resumen_salario
    && simulacion.resumen_proyeccion
    && simulacion.resumen_retiro
  );

  const accion = Boolean(
    simulacion.modo_flujo === "MANUAL"
    && simulacion.modo_flujo_confirmado
    && simulacion
      .escenario_retiro_seleccionado
  );

  return {
    datos,
    decisiones,
    fechas,

    /*
     * En Manual no existe revisión documental pendiente.
     * Se marca cumplido y se presenta como "No aplica".
     */
    importados: true,

    dependencias,
    accion,
  };
}


function manualFlowCompleto(
  simulacion = obtenerSimulacion(),
) {
  if (
    simulacion.modo_flujo
    !== "MANUAL"
  ) {
    return true;
  }

  return Object.values(
    evaluarCompletitudManual(
      simulacion,
    ),
  ).every(Boolean);
}


function actualizarCompletitudManual(
  simulacion = obtenerSimulacion(),
) {
  const gate = document.getElementById(
    "manual-completeness-gate",
  );

  if (!gate) {
    return;
  }

  const esManual = (
    simulacion.modo_flujo
    === "MANUAL"
  );

  gate.hidden = !esManual;

  const mostrar = Boolean(
    esManual
    && Number(
      simulacion.paso_actual || 1,
    ) >= 5
  );

  gate.classList.toggle(
    "d-none",
    !mostrar,
  );

  if (!mostrar) {
    return;
  }

  const resultados = (
    evaluarCompletitudManual(
      simulacion,
    )
  );

  Object.entries(
    resultados,
  ).forEach(
    ([clave, listo]) => {
      const item = gate.querySelector(
        `[data-completeness-key="${clave}"]`,
      );

      const estado = item?.querySelector(
        "[data-completeness-state]",
      );

      item?.setAttribute(
        "data-completeness-result",
        listo
          ? "ok"
          : "pending",
      );

      if (!estado) {
        return;
      }

      if (clave === "importados") {
        estado.textContent = (
          "No aplica — modo Manual"
        );
        return;
      }

      estado.textContent = (
        listo
          ? "OK"
          : "Pendiente"
      );
    },
  );

  const completo = Object.values(
    resultados,
  ).every(Boolean);

  const resumen = document.getElementById(
    "manual-completeness-status",
  );

  if (resumen) {
    resumen.textContent = (
      completo
        ? "Completo"
        : "Pendiente"
    );
  }
}


function mostrarResumenCompletitudManual() {
  const simulacion = obtenerSimulacion();

  actualizarCompletitudManual(
    simulacion,
  );

  const gate = document.getElementById(
    "manual-completeness-gate",
  );

  if (!gate) {
    return;
  }

  gate.hidden = false;
  gate.classList.remove(
    "d-none",
  );

  const titulo = document.getElementById(
    "manual-completeness-title",
  );

  if (titulo) {
    titulo.setAttribute(
      "tabindex",
      "-1",
    );

    titulo.focus({
      preventScroll: false,
    });
  }

  gate.scrollIntoView({
    block: "center",
    behavior: "smooth",
  });
}


document.addEventListener(
  "DOMContentLoaded",
  () => {
    document
      .querySelectorAll(
        "[data-simulation-mode-choice]",
      )
      .forEach(
        (boton) => {
          boton.addEventListener(
            "click",
            () => {
              seleccionarModalidad(
                boton.dataset
                  .simulationModeChoice,
              );
            },
          );
        },
      );

    document
      .querySelector(
        "[data-simulation-mode-change]",
      )
      ?.addEventListener(
        "click",
        mostrarSelectorModalidad,
      );

    const simulacion = obtenerSimulacion();

    sincronizarModoDatosPersonales(
      simulacion,
    );

    if (
      MODOS_FLUJO_SIMULACION.has(
        simulacion.modo_flujo,
      )
      && simulacion
        .modo_flujo_confirmado
    ) {
      aplicarVisibilidadModalidad(
        simulacion.modo_flujo,
      );
    } else {
      aplicarVisibilidadModalidad(
        null,
      );
    }

    actualizarCompletitudManual(
      simulacion,
    );
  },
);
