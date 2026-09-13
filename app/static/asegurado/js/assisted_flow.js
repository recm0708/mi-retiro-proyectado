"use strict";

/*
 * Mi Retiro Proyectado — flujo asistido.
 *
 * Propósito: Coordina preparación, completitud y procedencia de las
 * fuentes documentales utilizadas por la modalidad Asistida.
 * Alcance: Reutiliza los importadores existentes; no duplica parsers,
 * cálculos previsionales ni decisiones que corresponden al usuario.
 */

const CAMPOS_BASE_ASISTIDO = [
  "sexo",
  "fecha_nacimiento",
  "sistema",
  "cuotas_totales",
  "cuotas_anio_actual",
];


const DECISIONES_ASISTIDO = [
  "continua_cotizando",
  "modo_historial",
  "usar_detalle_anio_actual",
  "origen_salario_proyeccion",
  "modalidad_proyeccion",
];


function controlTieneValorAsistido(
  id,
) {
  const control = document.getElementById(
    id,
  );

  if (!control) {
    return true;
  }

  if (
    control.disabled
    && !control.required
  ) {
    return true;
  }

  if (
    control.type === "checkbox"
    || control.type === "radio"
  ) {
    return control.checked;
  }

  return String(
    control.value ?? "",
  ).trim() !== "";
}


function contarPendientesAsistidos(
  ids,
) {
  return ids.filter(
    (id) => (
      !controlTieneValorAsistido(
        id,
      )
    ),
  ).length;
}


function fuenteMiRetiroConfirmada(
  simulacion,
) {
  return Boolean(
    simulacion
      .importacion_comprobante_confirmada
    && simulacion
      .referencia_mi_retiro_seguro
  );
}


function fuenteFichaConfirmada(
  simulacion,
) {
  return Boolean(
    simulacion
      .importacion_ficha_digital_confirmada
    && simulacion
      .ficha_digital_importada
  );
}


function fuenteAsistidaConfirmada(
  simulacion = obtenerSimulacion(),
) {
  return Boolean(
    fuenteMiRetiroConfirmada(
      simulacion,
    )
    || fuenteFichaConfirmada(
      simulacion,
    )
  );
}


function actualizarEstadoFuenteAsistida(
  id,
  confirmada,
) {
  const elemento = document.getElementById(
    id,
  );

  if (!elemento) {
    return;
  }


  elemento.textContent = (
    confirmada
      ? "Confirmada"
      : "Pendiente"
  );


  elemento.classList.toggle(
    "text-bg-success",
    confirmada,
  );

  elemento.classList.toggle(
    "text-bg-secondary",
    !confirmada,
  );
}


function evaluarCompletitudAsistida(
  simulacion = obtenerSimulacion(),
) {
  const base = (
    typeof evaluarCompletitudManual
    === "function"
      ? evaluarCompletitudManual(
          simulacion,
        )
      : {
          datos: false,
          decisiones: false,
          dependencias: false,
        }
  );


  const fuente = fuenteAsistidaConfirmada(
    simulacion,
  );


  /*
   * Una fuente confirmada atravesó su revisión explícita.
   */
  const revision = fuente;


  const accion = Boolean(
    simulacion.modo_flujo
      === "ASISTIDO"
    && simulacion
      .modo_flujo_confirmado
    && simulacion
      .escenario_retiro_seleccionado
  );


  return {
    fuente,

    datos:
      Boolean(
        base.datos,
      ),

    decisiones:
      Boolean(
        base.decisiones,
      ),

    revision,

    dependencias:
      Boolean(
        base.dependencias,
      ),

    accion,
  };
}


function assistedFlowCompleto(
  simulacion = obtenerSimulacion(),
) {
  return Object.values(
    evaluarCompletitudAsistida(
      simulacion,
    ),
  ).every(
    Boolean,
  );
}


function actualizarItemCompletitudAsistida(
  clave,
  completo,
) {
  const elemento = document.querySelector(
    `[data-assisted-completeness="${clave}"]`,
  );

  if (!elemento) {
    return;
  }


  const textoBase = (
    elemento.dataset.label
    || elemento.textContent
      .replace(/^✓\s*/, "")
      .replace(/^Pendiente:\s*/, "")
      .trim()
  );


  elemento.dataset.label = textoBase;

  elemento.dataset.status = (
    completo
      ? "complete"
      : "pending"
  );


  elemento.textContent = (
    completo
      ? `✓ ${textoBase}`
      : `Pendiente: ${textoBase}`
  );
}


function actualizarCompletitudAsistida(
  simulacion = obtenerSimulacion(),
) {
  const gate = document.getElementById(
    "assisted-completeness-gate",
  );

  if (!gate) {
    return;
  }


  const estado = evaluarCompletitudAsistida(
    simulacion,
  );


  Object.entries(
    estado,
  ).forEach(
    ([clave, completo]) => {
      actualizarItemCompletitudAsistida(
        clave,
        completo,
      );
    },
  );


  const completo = Object.values(
    estado,
  ).every(
    Boolean,
  );


  gate.classList.toggle(
    "alert-success",
    completo,
  );

  gate.classList.toggle(
    "alert-info",
    !completo,
  );


  const mensaje = document.getElementById(
    "assisted-completeness-message",
  );

  if (mensaje) {
    mensaje.textContent = (
      completo
        ? (
          "La preparación asistida está completa. "
          + "Puedes continuar a Resultados."
        )
        : (
          "Todavía hay información o decisiones "
          + "pendientes antes de Resultados."
        )
    );
  }
}


function actualizarPanelAsistido(
  simulacion = obtenerSimulacion(),
) {
  const panel = document.getElementById(
    "assisted-preparation-panel",
  );

  if (!panel) {
    return;
  }


  const mrs = fuenteMiRetiroConfirmada(
    simulacion,
  );

  const ficha = fuenteFichaConfirmada(
    simulacion,
  );

  const existeFuente = (
    mrs || ficha
  );


  actualizarEstadoFuenteAsistida(
    "assisted-mrs-status",
    mrs,
  );

  actualizarEstadoFuenteAsistida(
    "assisted-ficha-status",
    ficha,
  );


  const contador = document.getElementById(
    "assisted-source-count",
  );

  if (contador) {
    contador.textContent = (
      `${Number(mrs) + Number(ficha)} de 2`
    );
  }


  const hechos = contarPendientesAsistidos(
    CAMPOS_BASE_ASISTIDO,
  );

  const decisiones = contarPendientesAsistidos(
    DECISIONES_ASISTIDO,
  );


  const hechosElemento = document.getElementById(
    "assisted-facts-pending",
  );

  if (hechosElemento) {
    hechosElemento.textContent = (
      hechos === 0
        ? "Sin pendientes detectados"
        : `${hechos} pendiente${hechos === 1 ? "" : "s"}`
    );
  }


  const decisionesElemento = document.getElementById(
    "assisted-decisions-pending",
  );

  if (decisionesElemento) {
    decisionesElemento.textContent = (
      decisiones === 0
        ? "Sin pendientes detectadas"
        : `${decisiones} pendiente${decisiones === 1 ? "" : "s"}`
    );
  }


  document.getElementById(
    "assisted-preparation-ready",
  )?.classList.toggle(
    "d-none",
    !existeFuente,
  );


  actualizarCompletitudAsistida(
    simulacion,
  );


  /*
   * Cuando se confirma la primera fuente se habilita
   * automáticamente el wizard, sin volver a preguntar
   * por documentos dentro de los pasos.
   */
  if (
    simulacion.modo_flujo
      === "ASISTIDO"
    && typeof aplicarVisibilidadModalidad
      === "function"
  ) {
    aplicarVisibilidadModalidad(
      "ASISTIDO",
    );
  }
}


function mostrarResumenCompletitudAsistida(
  simulacion = obtenerSimulacion(),
) {
  actualizarCompletitudAsistida(
    simulacion,
  );


  const gate = document.getElementById(
    "assisted-completeness-gate",
  );

  if (!gate) {
    return;
  }


  gate.scrollIntoView({
    behavior: "smooth",
    block: "center",
  });


  gate.setAttribute(
    "tabindex",
    "-1",
  );

  gate.focus({
    preventScroll: true,
  });
}


function bloquearResultadosAsistidos(
  numeroPaso,
) {
  if (
    Number(
      numeroPaso,
    ) !== 6
  ) {
    return false;
  }


  const simulacion = obtenerSimulacion();


  if (
    simulacion.modo_flujo
      !== "ASISTIDO"
    || assistedFlowCompleto(
      simulacion,
    )
  ) {
    return false;
  }


  mostrarResumenCompletitudAsistida(
    simulacion,
  );

  return true;
}


document.addEventListener(
  "DOMContentLoaded",
  () => {
    actualizarPanelAsistido();
  },
);
