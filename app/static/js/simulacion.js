"use strict";

const CLAVE_SIMULACION = "calculadoraPensionCSS.simulacion";

let pasoActual = 1;


// ============================================================
// Almacenamiento temporal
// ============================================================

function obtenerSimulacion() {
  const almacenada = sessionStorage.getItem(CLAVE_SIMULACION);

  if (!almacenada) {
    return {
      paso_actual: 1,
      persona: {},
      cuotas: {},
      resumen_cuotas: null,
    };
  }

  try {
    return JSON.parse(almacenada);
  } catch {
    return {
      paso_actual: 1,
      persona: {},
      cuotas: {},
      resumen_cuotas: null,
    };
  }
}


function guardarSimulacion(simulacion) {
  sessionStorage.setItem(
    CLAVE_SIMULACION,
    JSON.stringify(simulacion),
  );
}


// ============================================================
// Navegación del asistente
// ============================================================

function mostrarPaso(numeroPaso) {
  pasoActual = numeroPaso;

  document.querySelectorAll(".wizard-panel").forEach((panel) => {
    panel.classList.add("d-none");
  });

  const panelActivo = document.querySelector(
    `[data-panel="${numeroPaso}"]`,
  );

  if (panelActivo) {
    panelActivo.classList.remove("d-none");
  }

  document.querySelectorAll(".wizard-step").forEach((elemento) => {
    const numero = Number(elemento.dataset.step);

    elemento.classList.remove("active", "completed");

    if (numero === numeroPaso) {
      elemento.classList.add("active");
    } else if (numero < numeroPaso) {
      elemento.classList.add("completed");
    }
  });

  const simulacion = obtenerSimulacion();
  simulacion.paso_actual = numeroPaso;
  guardarSimulacion(simulacion);

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}


// ============================================================
// Paso 1 — Datos personales
// ============================================================

function guardarDatosPersonales() {
  const formulario = document.getElementById(
    "form-datos-personales",
  );

  if (!formulario.checkValidity()) {
    formulario.reportValidity();
    return false;
  }

  const simulacion = obtenerSimulacion();

  simulacion.persona = {
    fecha_nacimiento:
      document.getElementById("fecha_nacimiento").value,

    sexo:
      document.getElementById("sexo").value,

    fecha_ingreso_css:
      document.getElementById("fecha_ingreso_css").value || null,

    sistema:
      document.getElementById("sistema").value,
  };

  guardarSimulacion(simulacion);

  return true;
}


function restaurarDatosPersonales(simulacion) {
  if (!simulacion.persona) {
    return;
  }

  const persona = simulacion.persona;

  if (persona.fecha_nacimiento) {
    document.getElementById(
      "fecha_nacimiento",
    ).value = persona.fecha_nacimiento;
  }

  if (persona.sexo) {
    document.getElementById(
      "sexo",
    ).value = persona.sexo;
  }

  if (persona.fecha_ingreso_css) {
    document.getElementById(
      "fecha_ingreso_css",
    ).value = persona.fecha_ingreso_css;
  }

  if (persona.sistema) {
    document.getElementById(
      "sistema",
    ).value = persona.sistema;
  }
}


// ============================================================
// Paso 2 — Cuotas
// ============================================================

function actualizarEstadoContinuidad() {
  const continua =
    document.getElementById("continua_cotizando").value;

  const cuotasActuales = Number(
    document.getElementById("cuotas_anio_actual").value || 0,
  );

  const cierre = document.getElementById(
    "cuotas_esperadas_cierre_anio",
  );

  const futuras = document.getElementById(
    "cuotas_esperadas_por_anio",
  );

  if (continua === "false") {
    cierre.value = cuotasActuales;
    futuras.value = 0;

    cierre.disabled = true;
    futuras.disabled = true;
  } else {
    cierre.disabled = false;
    futuras.disabled = false;

    if (!cierre.value || Number(cierre.value) < cuotasActuales) {
      cierre.value = 12;
    }

    if (!futuras.value || Number(futuras.value) === 0) {
      futuras.value = 12;
    }
  }
}


function restaurarDatosCuotas(simulacion) {
  if (!simulacion.cuotas) {
    return;
  }

  const cuotas = simulacion.cuotas;

  if (cuotas.cuotas_totales !== undefined) {
    document.getElementById(
      "cuotas_totales",
    ).value = cuotas.cuotas_totales;
  }

  if (cuotas.cuotas_anio_actual !== undefined) {
    document.getElementById(
      "cuotas_anio_actual",
    ).value = cuotas.cuotas_anio_actual;
  }

  if (cuotas.continua_cotizando !== undefined) {
    document.getElementById(
      "continua_cotizando",
    ).value = String(cuotas.continua_cotizando);
  }

  if (cuotas.cuotas_esperadas_cierre_anio !== undefined) {
    document.getElementById(
      "cuotas_esperadas_cierre_anio",
    ).value = cuotas.cuotas_esperadas_cierre_anio;
  }

  if (cuotas.cuotas_esperadas_por_anio !== undefined) {
    document.getElementById(
      "cuotas_esperadas_por_anio",
    ).value = cuotas.cuotas_esperadas_por_anio;
  }

  actualizarEstadoContinuidad();

  if (simulacion.resumen_cuotas) {
    mostrarResumenCuotas(simulacion.resumen_cuotas);
  }
}


async function analizarCuotas(evento) {
  evento.preventDefault();

  const formulario = document.getElementById(
    "form-cuotas",
  );

  if (!formulario.checkValidity()) {
    formulario.reportValidity();
    return;
  }

  const continua =
    document.getElementById("continua_cotizando").value === "true";

  const cuotasAnioActual = Number(
    document.getElementById("cuotas_anio_actual").value,
  );

  const datos = {
    cuotas_totales: Number(
      document.getElementById("cuotas_totales").value,
    ),

    cuotas_anio_actual: cuotasAnioActual,

    continua_cotizando: continua,

    cuotas_esperadas_cierre_anio: continua
      ? Number(
          document.getElementById(
            "cuotas_esperadas_cierre_anio",
          ).value,
        )
      : cuotasAnioActual,

    cuotas_esperadas_por_anio: continua
      ? Number(
          document.getElementById(
            "cuotas_esperadas_por_anio",
          ).value,
        )
      : 0,
  };

  ocultarErrorCuotas();

  try {
    const respuesta = await fetch(
      "/api/simulacion/cuotas",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify(datos),
      },
    );

    const contenido = await respuesta.json();

    if (!respuesta.ok) {
      const mensaje =
        contenido.detail ||
        "No fue posible analizar las cuotas.";

      mostrarErrorCuotas(mensaje);
      return;
    }

    const simulacion = obtenerSimulacion();

    simulacion.cuotas = datos;
    simulacion.resumen_cuotas = contenido;

    guardarSimulacion(simulacion);

    mostrarResumenCuotas(contenido);

  } catch {
    mostrarErrorCuotas(
      "No fue posible comunicarse con el servidor.",
    );
  }
}


function mostrarResumenCuotas(resumen) {
  document.getElementById(
    "resultado-cuotas",
  ).classList.remove("d-none");

  document.getElementById(
    "resultado-cuotas-reales",
  ).textContent = resumen.cuotas_reales;

  document.getElementById(
    "resultado-cuotas-cierre",
  ).textContent = resumen.cuotas_proyectadas_cierre_anio;

  document.getElementById(
    "resultado-faltantes-180",
  ).textContent = resumen.faltantes_180;

  document.getElementById(
    "resultado-faltantes-240",
  ).textContent = resumen.faltantes_240;

  document.getElementById(
    "resultado-tiempo-180",
  ).textContent = formatearTiempo(
    resumen.anios_aprox_180,
  );

  document.getElementById(
    "resultado-tiempo-240",
  ).textContent = formatearTiempo(
    resumen.anios_aprox_240,
  );
}


function formatearTiempo(anios) {
  if (anios === null) {
    return "No alcanzable con la proyección actual";
  }

  if (anios === 0) {
    return "Requisito alcanzado";
  }

  const meses = Math.round(anios * 12);

  const aniosCompletos = Math.floor(meses / 12);
  const mesesRestantes = meses % 12;

  const partes = [];

  if (aniosCompletos > 0) {
    partes.push(
      `${aniosCompletos} ${
        aniosCompletos === 1 ? "año" : "años"
      }`,
    );
  }

  if (mesesRestantes > 0) {
    partes.push(
      `${mesesRestantes} ${
        mesesRestantes === 1 ? "mes" : "meses"
      }`,
    );
  }

  return partes.join(" y ");
}


function mostrarErrorCuotas(mensaje) {
  const error = document.getElementById(
    "error-cuotas",
  );

  error.textContent = mensaje;
  error.classList.remove("d-none");
}


function ocultarErrorCuotas() {
  document.getElementById(
    "error-cuotas",
  ).classList.add("d-none");
}


// ============================================================
// Inicialización
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
  const simulacion = obtenerSimulacion();

  restaurarDatosPersonales(simulacion);
  restaurarDatosCuotas(simulacion);

  const pasoGuardado = Number(
    simulacion.paso_actual || 1,
  );

  mostrarPaso(
    pasoGuardado >= 1 && pasoGuardado <= 2
      ? pasoGuardado
      : 1,
  );

  document.getElementById(
    "form-datos-personales",
  ).addEventListener("submit", (evento) => {
    evento.preventDefault();

    if (guardarDatosPersonales()) {
      mostrarPaso(2);
    }
  });

  document.getElementById(
    "form-cuotas",
  ).addEventListener(
    "submit",
    analizarCuotas,
  );

  document.getElementById(
    "btn-volver-paso-1",
  ).addEventListener("click", () => {
    mostrarPaso(1);
  });

  document.getElementById(
    "continua_cotizando",
  ).addEventListener(
    "change",
    actualizarEstadoContinuidad,
  );

  document.getElementById(
    "cuotas_anio_actual",
  ).addEventListener(
    "input",
    actualizarEstadoContinuidad,
  );
});