"use strict";


/* ============================================================
   Mi Retiro Proyectado
   Comparador transversal de escenarios
   ============================================================ */

/*
 * Lee el estado temporal ya validado por el asistente, construye una solicitud
 * de comparación y presenta diferencias entre escenarios sin recalcular las
 * fórmulas previsionales en JavaScript. Los resultados provienen siempre del
 * backend y este módulo se limita a selección, formato y representación.
 */

const CLAVE_SIMULACION_COMPARADOR = "miRetiroProyectado.simulacion";


/**
 * Recupera la simulación temporal que sirve de contexto al comparador.
 *
 * @returns {Object|null} Estado serializado o null si no existe/es inválido.
 */
function obtenerSimulacionComparador() {
  const texto = sessionStorage.getItem(CLAVE_SIMULACION_COMPARADOR);

  if (!texto) {
    return null;
  }

  try {
    return JSON.parse(texto);
  } catch {
    return null;
  }
}


function nombreSistemaComparador(codigo) {
  const nombres = {
    SEBD: "SEBD — Beneficio Definido",
    MIXTO: "Subsistema Mixto",
    SUCGS: "SUCGS — Sistema Único de Capitalización con Garantía Solidaria",
  };

  return nombres[codigo] || codigo || "—";
}


function formatearFechaComparador(valor) {
  if (!valor) {
    return "—";
  }

  const partes = String(valor).split("-");

  if (partes.length !== 3) {
    return valor;
  }

  return `${partes[2]}/${partes[1]}/${partes[0]}`;
}


function formatearMonedaComparador(valor) {
  if (valor == null || !Number.isFinite(Number(valor))) {
    return "—";
  }

  return `B/.${Number(valor).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}


function formatearDiferenciaMonetaria(valor) {
  if (valor == null || !Number.isFinite(Number(valor))) {
    return "—";
  }

  const numero = Number(valor);
  const signo = numero > 0 ? "+" : "";

  return `${signo}${formatearMonedaComparador(numero)}`;
}


function formatearPorcentajeComparador(valor) {
  if (valor == null || !Number.isFinite(Number(valor))) {
    return "—";
  }

  const numero = Number(valor);
  const signo = numero > 0 ? "+" : "";

  return `${signo}${numero.toLocaleString("es-PA", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })} %`;
}


function obtenerEscenarioBase(simulacion) {
  const retiro = simulacion.escenario_retiro_seleccionado;

  if (!retiro) {
    return null;
  }

  let salario = simulacion.escenario_salarial_seleccionado;

  if (simulacion.persona?.sistema === "MIXTO") {
    salario = (
      simulacion.configuracion_mixto_resultados?.escenario_salarial_nombre
      || salario
    );
  }

  if (simulacion.persona?.sistema === "SUCGS") {
    salario = (
      simulacion.configuracion_sucgs_resultados?.escenario_salarial_nombre
      || salario
    );
  }

  salario = salario || simulacion.resumen_linea_tiempo?.escenarios?.[0]?.nombre;

  if (!salario) {
    return null;
  }

  return {
    fecha_retiro: retiro.fecha_retiro,
    nombre_retiro: retiro.nombre,
    escenario_salarial: salario,
  };
}


function simulacionListaParaComparar(simulacion) {
  return Boolean(
    simulacion
    && simulacion.persona?.sistema
    && simulacion.historial
    && simulacion.resumen_linea_tiempo?.escenarios?.length
    && simulacion.resumen_retiro?.escenarios?.length
    && simulacion.escenario_retiro_seleccionado
    && obtenerEscenarioBase(simulacion)
  );
}


function crearOpcionCheckbox({
  id,
  name,
  value,
  label,
  detalle,
  checked = true,
  disabled = false,
}) {
  const wrapper = document.createElement("label");
  wrapper.className = "comparison-option";
  wrapper.htmlFor = id;

  const input = document.createElement("input");
  input.type = "checkbox";
  input.className = "form-check-input";
  input.id = id;
  input.name = name;
  input.value = value;
  input.checked = checked;
  input.disabled = disabled;

  const texto = document.createElement("span");
  texto.className = "comparison-option-text";

  const principal = document.createElement("strong");
  principal.textContent = label;
  texto.appendChild(principal);

  if (detalle) {
    const secundario = document.createElement("small");
    secundario.textContent = detalle;
    texto.appendChild(secundario);
  }

  wrapper.append(input, texto);

  return wrapper;
}


function prepararOpcionesComparador(simulacion) {
  const base = obtenerEscenarioBase(simulacion);
  const retiros = document.getElementById("comparador-retiros");
  const salarios = document.getElementById("comparador-salarios");

  retiros.replaceChildren();
  salarios.replaceChildren();

  simulacion.resumen_retiro.escenarios
    .filter((escenario) => !escenario.fecha_ya_transcurrida)
    .forEach((escenario, indice) => {
      const esBase = escenario.fecha_retiro === base.fecha_retiro;

      retiros.appendChild(
        crearOpcionCheckbox({
          id: `comparador-retiro-${indice}`,
          name: "comparador-retiro",
          value: escenario.fecha_retiro,
          label: escenario.nombre,
          detalle: (
            `${formatearFechaComparador(escenario.fecha_retiro)} · `
            + `${escenario.edad_retiro_anios} años · `
            + `${escenario.cuotas_estimadas_totales} cuotas`
          ),
          checked: true,
          disabled: esBase,
        }),
      );
    });

  simulacion.resumen_linea_tiempo.escenarios.forEach((escenario, indice) => {
    const esBase = escenario.nombre === base.escenario_salarial;

    salarios.appendChild(
      crearOpcionCheckbox({
        id: `comparador-salario-${indice}`,
        name: "comparador-salario",
        value: escenario.nombre,
        label: escenario.nombre,
        detalle: Number.isFinite(Number(escenario.tasa_anual_pct))
          ? `Tasa anual: ${Number(escenario.tasa_anual_pct).toLocaleString("es-PA", {
            minimumFractionDigits: 0,
            maximumFractionDigits: 2,
          })} %`
          : "",
        checked: true,
        disabled: esBase,
      }),
    );
  });
}


// El comparador arma un contrato único para que Python combine retiro y salario;
// no replica reglas de elegibilidad ni fórmulas de pensión en el navegador.
function construirDatosIntegradosComparador(simulacion) {
  const persona = simulacion.persona;
  const base = obtenerEscenarioBase(simulacion);

  const comun = {
    fecha_nacimiento: persona.fecha_nacimiento,
    sexo: persona.sexo,
    historial: simulacion.historial,
    linea_tiempo: simulacion.resumen_linea_tiempo,
    resumen_retiro: simulacion.resumen_retiro,
    fecha_retiro_seleccionada: base.fecha_retiro,
    escenario_salarial_nombre: base.escenario_salarial,
  };

  if (persona.sistema === "SEBD") {
    return {
      sistema: "SEBD",
      datos_sebd: comun,
    };
  }

  if (persona.sistema === "MIXTO") {
    const config = simulacion.configuracion_mixto_resultados || {};

    return {
      sistema: "MIXTO",
      datos_mixto: {
        ...comun,
        saldo_ahorro_personal: config.saldo_ahorro_personal ?? null,
        bono_reconocimiento: config.bono_reconocimiento ?? 0,
        bono_reconocimiento_confirmado_oficialmente: Boolean(
          config.bono_reconocimiento_confirmado_oficialmente,
        ),
        valor_actuarial_expectativa_vida: (
          config.valor_actuarial_expectativa_vida ?? null
        ),
        opcion_prestacion_cap: config.opcion_prestacion_cap || "AUTO",
      },
    };
  }

  const config = simulacion.configuracion_sucgs_resultados || {};

  return {
    sistema: "SUCGS",
    datos_sucgs: {
      ...comun,
      saldo_capitalizacion_solidaria: (
        config.saldo_capitalizacion_solidaria ?? 0
      ),
      saldo_confirmado_oficialmente: Boolean(
        config.saldo_confirmado_oficialmente,
      ),
      valor_minimo_universal_vigente: (
        config.valor_minimo_universal_vigente ?? 144
      ),
      pension_garantizada_solidaria_vigente: (
        config.pension_garantizada_solidaria_vigente ?? 265
      ),
      valores_solidarios_confirmados_oficialmente: Boolean(
        config.valores_solidarios_confirmados_oficialmente,
      ),
      historial_laboral_completo_confirmado: Boolean(
        config.historial_laboral_completo_confirmado,
      ),
      estabilidad_salarial_art197_confirmada: (
        config.estabilidad_salarial_art197_confirmada ?? null
      ),
    },
  };
}


// Las opciones deshabilitadas también se envían cuando representan decisiones
// obligatorias ya fijadas por el estado de la simulación.
function valoresSeleccionados(nombre) {
  return Array.from(document.querySelectorAll(`input[name="${nombre}"]`))
    .filter((input) => input.checked || input.disabled)
    .map((input) => input.value);
}


/**
 * Construye la solicitud que el backend utilizará para comparar escenarios.
 *
 * @param {Object} simulacion Estado validado del asistente.
 * @returns {Object} Contrato de comparación listo para serializar.
 */
function construirSolicitudComparador(simulacion) {
  const solicitud = construirDatosIntegradosComparador(simulacion);

  solicitud.fechas_retiro = valoresSeleccionados("comparador-retiro");
  solicitud.escenarios_salariales = valoresSeleccionados("comparador-salario");

  if (solicitud.fechas_retiro.length === 0) {
    throw new Error("Selecciona al menos un escenario de retiro.");
  }

  if (solicitud.escenarios_salariales.length === 0) {
    throw new Error("Selecciona al menos un escenario salarial.");
  }

  return solicitud;
}


function mostrarErrorComparador(mensaje) {
  const alerta = document.getElementById("comparador-error");
  alerta.textContent = mensaje;
  alerta.classList.remove("d-none");
}


function ocultarErrorComparador() {
  const alerta = document.getElementById("comparador-error");
  alerta.textContent = "";
  alerta.classList.add("d-none");
}


function etiquetaEstadoFila(fila) {
  if (fila.calculo_completo) {
    return '<span class="badge text-bg-success">Completo</span>';
  }

  return '<span class="badge text-bg-warning">Incompleto</span>';
}


function textoPrestacionLegibleComparador(codigo) {
  const nombres = {
    PENSION: "Pensión mensual",
    INDEMNIZACION: "Indemnización por Vejez",
    PENSION_MENSUAL: "Pensión mensual",
    PAGO_UNICO: "Pago único",
    PENSION_MAS_PAGO_UNICO: "Pensión mensual + pago único",
    SIN_MONTO: "Sin monto calculable",
    TRANSICION: "Transición de sistema",
    PENSION_MAS_DEVOLUCION_CAP: "Pensión + devolución del CAP",
    DECISION_CAP_PENDIENTE: "Decisión del CAP pendiente",
    PENSION_CONTRIBUTIVA_SIN_COMPLEMENTO: "Pensión contributiva sin complemento",
    PENSION_BENEFICIO_SOLIDARIO: "Pensión con beneficio solidario",
    PENSION_BENEFICIO_MINIMO: "Pensión de beneficio mínimo",
    TRANSICION_SUCGS: "Transición a SUCGS",
  };

  if (!codigo) {
    return "";
  }

  if (nombres[codigo]) {
    return nombres[codigo];
  }

  return codigo
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/^./, (letra) => letra.toUpperCase());
}


function textoModalidadFila(fila) {
  const titulo = fila.modalidad_nombre || fila.modalidad || fila.tipo_prestacion || "—";
  const tipo = (
    fila.tipo_prestacion
    && fila.tipo_prestacion !== fila.modalidad
    && fila.tipo_prestacion !== fila.modalidad_nombre
  ) ? textoPrestacionLegibleComparador(fila.tipo_prestacion) : "";

  return {
    titulo,
    tipo,
  };
}


// Cada fila destaca base, mejor pensión y decisiones pendientes sin alterar
// el orden ni los montos que ya fueron normalizados por el backend.
function renderizarFilaComparador(fila, respuesta) {
  const tr = document.createElement("tr");

  if (fila.es_base) {
    tr.classList.add("comparison-row-base");
  }

  if (fila.clave === respuesta.clave_mejor_pension_mensual) {
    tr.classList.add("comparison-row-best");
  }

  const modalidad = textoModalidadFila(fila);
  const badges = [];

  if (fila.es_base) {
    badges.push('<span class="badge text-bg-primary ms-1">Base</span>');
  }

  if (fila.clave === respuesta.clave_mejor_pension_mensual) {
    badges.push('<span class="badge text-bg-success ms-1">Mayor mensual</span>');
  }

  tr.innerHTML = `
    <td>
      <div class="fw-semibold">${fila.escenario_retiro_nombre}</div>
      <small class="text-secondary">
        ${formatearFechaComparador(fila.fecha_retiro)} · ${fila.edad_retiro_anios} años
      </small>
      <div>${badges.join("")}</div>
    </td>
    <td>${fila.escenario_salarial_nombre}</td>
    <td class="text-nowrap">${fila.cuotas_estimadas_totales}</td>
    <td>
      <div class="fw-semibold">${modalidad.titulo}</div>
      ${modalidad.tipo ? `<small class="text-secondary">${modalidad.tipo}</small>` : ""}
    </td>
    <td class="text-end text-nowrap fw-semibold">
      ${formatearMonedaComparador(fila.pension_mensual_estimada)}
    </td>
    <td class="text-end text-nowrap">
      ${formatearDiferenciaMonetaria(fila.diferencia_mensual_absoluta)}
    </td>
    <td class="text-end text-nowrap">
      ${formatearPorcentajeComparador(fila.diferencia_mensual_pct)}
    </td>
    <td class="text-end text-nowrap">
      ${formatearMonedaComparador(fila.pago_unico_estimado)}
    </td>
    <td>${etiquetaEstadoFila(fila)}</td>
  `;

  if (Array.isArray(fila.advertencias) && fila.advertencias.length > 0) {
    tr.title = fila.advertencias.join("\n");
  }

  return tr;
}


function mostrarResumenComparador(respuesta) {
  const base = respuesta.filas.find((fila) => fila.es_base);
  const mejor = respuesta.filas.find(
    (fila) => fila.clave === respuesta.clave_mejor_pension_mensual,
  );

  document.getElementById("comparador-resumen-base").textContent = (
    formatearMonedaComparador(base?.pension_mensual_estimada)
  );

  document.getElementById("comparador-resumen-mejor").textContent = (
    formatearMonedaComparador(mejor?.pension_mensual_estimada)
  );

  document.getElementById("comparador-resumen-mejor-detalle").textContent = mejor
    ? `${mejor.escenario_retiro_nombre} · ${mejor.escenario_salarial_nombre}`
    : "No hay una pensión mensual completa comparable.";

  document.getElementById("comparador-resumen-completos").textContent = (
    `${respuesta.resultados_completos}`
  );
  document.getElementById("comparador-resumen-total").textContent = (
    `${respuesta.total_combinaciones}`
  );
}


// Las advertencias globales y por combinación se deduplican para no ocultar
// riesgos relevantes cuando varios escenarios comparten la misma condición.
function mostrarAdvertenciasComparador(respuesta) {
  const contenedor = document.getElementById("comparador-advertencias");
  const lista = document.getElementById("comparador-lista-advertencias");

  lista.replaceChildren();

  const mensajes = [...(respuesta.advertencias || [])];

  respuesta.filas.forEach((fila) => {
    (fila.advertencias || []).forEach((mensaje) => {
      const etiqueta = `${fila.escenario_retiro_nombre} / ${fila.escenario_salarial_nombre}: ${mensaje}`;
      if (!mensajes.includes(etiqueta)) {
        mensajes.push(etiqueta);
      }
    });
  });

  if (mensajes.length === 0) {
    contenedor.classList.add("d-none");
    return;
  }

  mensajes.forEach((mensaje) => {
    const li = document.createElement("li");
    li.textContent = mensaje;
    li.className = "mb-2";
    lista.appendChild(li);
  });

  contenedor.classList.remove("d-none");
}


function mostrarResultadoComparador(respuesta) {
  const cuerpo = document.getElementById("comparador-tabla-body");
  cuerpo.replaceChildren();

  respuesta.filas.forEach((fila) => {
    cuerpo.appendChild(renderizarFilaComparador(fila, respuesta));
  });

  mostrarResumenComparador(respuesta);
  mostrarAdvertenciasComparador(respuesta);

  document.getElementById("comparador-resultados").classList.remove("d-none");
}


/**
 * Envía la comparación al backend y presenta el resultado normalizado.
 *
 * Las fórmulas permanecen en Python; esta función solo orquesta la solicitud.
 */
async function ejecutarComparacion() {
  ocultarErrorComparador();
  const simulacion = obtenerSimulacionComparador();
  const boton = document.getElementById("btn-comparar-escenarios");

  let solicitud;

  try {
    solicitud = construirSolicitudComparador(simulacion);
  } catch (error) {
    mostrarErrorComparador(error.message);
    return;
  }

  boton.disabled = true;
  boton.textContent = "Comparando…";

  try {
    const respuesta = await fetch("/api/simulacion/comparar-escenarios", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(solicitud),
    });

    let contenido = null;

    try {
      contenido = await respuesta.json();
    } catch {
      contenido = null;
    }

    if (!respuesta.ok) {
      const detalle = contenido?.detail;
      mostrarErrorComparador(
        typeof detalle === "string"
          ? detalle
          : "No fue posible construir la comparación.",
      );
      return;
    }

    mostrarResultadoComparador(contenido);
  } catch {
    mostrarErrorComparador("No fue posible comunicarse con el servidor.");
  } finally {
    boton.disabled = false;
    boton.textContent = "Comparar escenarios";
  }
}


/**
 * Inicializa controles y opciones a partir de la simulación disponible.
 */
function prepararComparador() {
  const simulacion = obtenerSimulacionComparador();
  const sinSimulacion = document.getElementById("comparador-sin-simulacion");
  const contenido = document.getElementById("comparador-contenido");

  if (!simulacionListaParaComparar(simulacion)) {
    sinSimulacion.classList.remove("d-none");
    contenido.classList.add("d-none");
    return;
  }

  sinSimulacion.classList.add("d-none");
  contenido.classList.remove("d-none");

  const sistema = simulacion.persona.sistema;
  const base = obtenerEscenarioBase(simulacion);

  document.getElementById("comparador-sistema").textContent = (
    nombreSistemaComparador(sistema)
  );
  document.getElementById("comparador-base").textContent = (
    `${base.nombre_retiro} · ${base.escenario_salarial}`
  );

  prepararOpcionesComparador(simulacion);

  const aviso = document.getElementById("comparador-aviso-saldos");

  if (sistema === "MIXTO") {
    aviso.textContent = (
      "En Mixto, una fecha alternativa reutiliza el saldo CAP, bono y valor "
      + "actuarial ingresados en el Paso 6. Esto permite una comparación "
      + "hipotética, pero todavía no proyecta automáticamente esos valores."
    );
    aviso.classList.remove("d-none");
  } else if (sistema === "SUCGS") {
    aviso.textContent = (
      "En SUCGS, una fecha alternativa reutiliza el saldo de Capitalización "
      + "Solidaria ingresado en el Paso 6. El comparador todavía no proyecta "
      + "automáticamente ese saldo hacia cada fecha."
    );
    aviso.classList.remove("d-none");
  } else {
    aviso.classList.add("d-none");
  }
}


document.addEventListener("DOMContentLoaded", () => {
  prepararComparador();

  document.getElementById("btn-comparar-escenarios")?.addEventListener(
    "click",
    ejecutarComparacion,
  );
});
