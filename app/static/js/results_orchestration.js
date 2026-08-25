"use strict";

/*
 * Mi Retiro Proyectado — Paso 6 — Orquestación, decisiones y copia imprimible.
 *
 * Propósito: Complementa resultados.js con decisiones explícitas de interfaz, transición entre sistemas e impresión.
 * Alcance: No duplica fórmulas previsionales; coordina estado, invalidación y salida visual.
 */

(() => {
  let panelResultados = null;

  function cargarEstilosResultados() {
    if (document.querySelector(
      'link[data-resultados-orquestacion-css="1"]',
    )) {
      return;
    }

    const enlace = document.createElement("link");
    enlace.rel = "stylesheet";
    enlace.href = "/static/css/results.css";
    enlace.dataset.resultadosOrquestacionCss = "1";
    document.head.appendChild(enlace);
  }

  // Estos contenedores dependen del último cálculo válido y deben ocultarse
  // juntos cuando cambia una decisión transversal del Paso 6.
  const IDS_SALIDA_DEPENDIENTE = [
    "resultado-resumen-unificado",
    "resultado-comparacion-origen-datos",
    "resultado-comparacion-referencia",
    "resultado-trazabilidad-calculo",
    "resultado-exportacion",
  ];

  const IDS_SALIDA_ESPECIFICA = [
    "resultado-sebd",
    "resultado-mixto",
    "resultado-sucgs",
  ];

  const SISTEMAS_SELECT = {
    SEBD: {
      selectId: "resultado-escenario-salarial",
      ayudaId: "resultado-sebd-escenario-salarial-ayuda",
    },
    MIXTO: {
      selectId: "resultado-mixto-escenario-salarial",
      ayudaId: "resultado-mixto-escenario-salarial-ayuda",
    },
    SUCGS: {
      selectId: "resultado-sucgs-escenario-salarial",
      ayudaId: "resultado-sucgs-escenario-salarial-ayuda",
    },
  };


  function ocultarElemento(id) {
    document.getElementById(id)?.classList.add("d-none");
  }


  function ocultarSalidaDependientePaso6({
    incluirEspecificos = false,
  } = {}) {
    IDS_SALIDA_DEPENDIENTE.forEach(ocultarElemento);

    if (incluirEspecificos) {
      IDS_SALIDA_ESPECIFICA.forEach(ocultarElemento);
    }

    const detalle = document.getElementById(
      "resultado-trazabilidad-detalle",
    );
    detalle?.classList.remove("show");
  }


  function asegurarAyudaSelect(select, ayudaId) {
    let ayuda = document.getElementById(ayudaId);

    if (!ayuda) {
      const ayudaExistente = (
        select.nextElementSibling
        && select.nextElementSibling.classList.contains("form-text")
      )
        ? select.nextElementSibling
        : null;

      ayuda = ayudaExistente || document.createElement("div");
      ayuda.id = ayudaId;
      ayuda.className = "form-text";

      if (!ayudaExistente) {
        select.insertAdjacentElement("afterend", ayuda);
      }
    }

    const ids = new Set(
      (select.getAttribute("aria-describedby") || "")
        .split(/\s+/)
        .filter(Boolean),
    );
    ids.add(ayudaId);
    select.setAttribute(
      "aria-describedby",
      Array.from(ids).join(" "),
    );
    select.setAttribute("aria-required", "true");

    return ayuda;
  }


  function opcionesReales(select) {
    return Array.from(select.options).filter(
      (opcion) => opcion.value !== "",
    );
  }


  function aplicarSeleccionSalarialExplicita({
    // La selección explícita impide que un placeholder o una opción removida
    // mantenga resultados previos con un escenario salarial distinto.
    selectId,
    ayudaId,
    guardado,
  }) {
    const select = document.getElementById(selectId);

    if (!select) {
      return;
    }

    Array.from(select.options)
      .filter((opcion) => opcion.dataset.placeholderPaso6 === "1")
      .forEach((opcion) => opcion.remove());

    const opciones = opcionesReales(select);
    const ayuda = asegurarAyudaSelect(select, ayudaId);

    if (opciones.length === 0) {
      select.value = "";
      ayuda.textContent = (
        "No hay escenarios salariales disponibles. "
        + "Vuelve al Paso 4 y genera la proyección."
      );
      return;
    }

    const existeGuardado = Boolean(
      guardado
      && opciones.some((opcion) => opcion.value === guardado),
    );

    if (existeGuardado) {
      select.value = guardado;
      ayuda.textContent = (
        "Se conserva el escenario salarial que elegiste "
        + "anteriormente para este cálculo."
      );
      return;
    }

    if (opciones.length === 1) {
      select.value = opciones[0].value;
      ayuda.textContent = (
        "Solo existe un escenario salarial disponible en el Paso 4; "
        + "se utilizará automáticamente."
      );
      return;
    }

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Seleccione una opción";
    placeholder.disabled = true;
    placeholder.selected = true;
    placeholder.dataset.placeholderPaso6 = "1";
    select.prepend(placeholder);
    select.value = "";

    ayuda.textContent = (
      "Tienes varios escenarios salariales del Paso 4. "
      + "Elige cuál deseas usar en este cálculo."
    );
  }


  function guardadoSalarialSEBD(simulacion) {
    return simulacion.escenario_salarial_seleccionado || null;
  }


  function guardadoSalarialMixto(simulacion) {
    return (
      simulacion.configuracion_mixto_resultados
        ?.escenario_salarial_nombre
      || null
    );
  }


  function guardadoSalarialSUCGS(simulacion) {
    return (
      simulacion.configuracion_sucgs_resultados
        ?.escenario_salarial_nombre
      || null
    );
  }


  function contratoSeleccionPorSistema(sistema, simulacion) {
    const config = SISTEMAS_SELECT[sistema];

    if (!config) {
      return;
    }

    const guardado = sistema === "SEBD"
      ? guardadoSalarialSEBD(simulacion)
      : (
        sistema === "MIXTO"
          ? guardadoSalarialMixto(simulacion)
          : guardadoSalarialSUCGS(simulacion)
      );

    aplicarSeleccionSalarialExplicita({
      ...config,
      guardado,
    });
  }


  function envolverPreparador(nombre, sistema) {
    const original = window[nombre];

    if (typeof original !== "function") {
      return;
    }

    window[nombre] = function prepararConDecisionExplicita(
      simulacion,
    ) {
      const correcto = original(simulacion);

      if (correcto) {
        contratoSeleccionPorSistema(sistema, simulacion);
      }

      return correcto;
    };
  }


  function envolverInvalidacion(nombre) {
    const original = window[nombre];

    if (typeof original !== "function") {
      return;
    }

    window[nombre] = function invalidarConSalidaTransversal(
      ...args
    ) {
      const resultado = original(...args);
      ocultarSalidaDependientePaso6();
      return resultado;
    };
  }


  function escenarioMixtoEnTransicion(simulacion = obtenerSimulacion()) {
    return (
      simulacion.persona?.sistema === "MIXTO"
      && simulacion.resultado_mixto?.calculo?.estado_sistema
        === "TRANSICION_SUCGS"
    );
  }


  function construirSolicitudSUCGSConTransicion() {
    // La transición Mixto -> SUCGS reutiliza datos del escenario seleccionado,
    // pero marca el origen para que el backend aplique el contrato correcto.
    const simulacion = obtenerSimulacion();
    const persona = simulacion.persona || {};
    const seleccionado = simulacion.escenario_retiro_seleccionado;
    const transicionMixto = escenarioMixtoEnTransicion(simulacion);

    if (
      persona.sistema !== "SUCGS"
      && !transicionMixto
    ) {
      throw new Error(
        "El cálculo SUCGS solo puede ejecutarse cuando el sistema "
        + "seleccionado en el Paso 1 es SUCGS o cuando el motor Mixto "
        + "determinó una transición legal al SUCGS para este escenario.",
      );
    }

    if (!simulacion.historial || !simulacion.resumen_historial) {
      throw new Error(
        "El cálculo SUCGS requiere un historial salarial anual "
        + "analizado en el Paso 3.",
      );
    }

    if (!simulacion.resumen_linea_tiempo) {
      throw new Error(
        "Falta la línea temporal salarial del Paso 4.",
      );
    }

    if (!simulacion.resumen_retiro || !seleccionado) {
      throw new Error(
        "Falta analizar y seleccionar un escenario de retiro "
        + "en el Paso 5.",
      );
    }

    const escenarioSalarial = document.getElementById(
      "resultado-sucgs-escenario-salarial",
    ).value;

    if (!escenarioSalarial) {
      throw new Error(
        "Selecciona un escenario salarial para realizar "
        + "el cálculo SUCGS.",
      );
    }

    const saldo = leerMontoOpcionalResultados(
      "resultado-sucgs-saldo",
    );

    if (saldo == null) {
      throw new Error(
        "Introduce el saldo de Capitalización Solidaria "
        + "para calcular SUCGS.",
      );
    }

    const minimoUniversal = leerMontoOpcionalResultados(
      "resultado-sucgs-minimo-universal",
    );
    const pgs = leerMontoOpcionalResultados(
      "resultado-sucgs-pgs",
    );

    if (minimoUniversal == null || minimoUniversal <= 0) {
      throw new Error(
        "El valor mínimo universal debe ser mayor que cero.",
      );
    }

    if (pgs == null || pgs <= 0) {
      throw new Error(
        "La Pensión Garantizada Solidaria debe ser mayor que cero.",
      );
    }

    return {
      modo_integracion: "PROYECTADO",
      fecha_nacimiento: persona.fecha_nacimiento,
      sexo: persona.sexo,
      historial: simulacion.historial,
      linea_tiempo: simulacion.resumen_linea_tiempo,
      resumen_retiro: simulacion.resumen_retiro,
      fecha_retiro_seleccionada: seleccionado.fecha_retiro,
      escenario_salarial_nombre: escenarioSalarial,
      saldo_capitalizacion_solidaria: saldo,
      saldo_confirmado_oficialmente: document.getElementById(
        "resultado-sucgs-saldo-confirmado",
      ).checked,
      valor_minimo_universal_vigente: minimoUniversal,
      pension_garantizada_solidaria_vigente: pgs,
      valores_solidarios_confirmados_oficialmente:
        document.getElementById(
          "resultado-sucgs-valores-confirmados",
        ).checked,
      historial_laboral_completo_confirmado:
        document.getElementById(
          "resultado-sucgs-historial-completo",
        ).checked,
      estabilidad_salarial_art197_confirmada:
        leerEstabilidadSUCGS(),
    };
  }


  function mostrarContextoTransicionSUCGS(visible) {
    document.getElementById(
      "resultado-sucgs-contexto-transicion",
    )?.classList.toggle("d-none", !visible);
  }


  function prepararCalculoSUCGSDesdeTransicion() {
    const simulacion = obtenerSimulacion();

    if (!escenarioMixtoEnTransicion(simulacion)) {
      return;
    }

    const config = document.getElementById(
      "resultado-config-sucgs",
    );

    document.getElementById(
      "resultado-config-mixto",
    )?.classList.add("d-none");

    config?.classList.remove("d-none");
    mostrarContextoTransicionSUCGS(true);

    if (
      typeof window.prepararConfiguracionSUCGS
      === "function"
    ) {
      window.prepararConfiguracionSUCGS(simulacion);
    }

    config?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }


  function actualizarAccionTransicionMixto(resultado) {
    const contenedor = document.getElementById(
      "resultado-mixto-transicion-sucgs",
    );

    if (!contenedor) {
      return;
    }

    const aplica = (
      resultado?.calculo?.estado_sistema
      === "TRANSICION_SUCGS"
    );

    contenedor.classList.toggle("d-none", !aplica);
  }


  function crearInterfazTransicion() {
    // La interfaz se crea de forma idempotente para poder inicializar la página
    // varias veces sin duplicar controles ni listeners.
    if (document.getElementById("resultado-mixto-transicion-sucgs")) {
      return;
    }

    const estado = document.getElementById(
      "resultado-mixto-estado",
    );

    if (!estado) {
      return;
    }

    const bloque = document.createElement("div");
    bloque.id = "resultado-mixto-transicion-sucgs";
    bloque.className = (
      "results-transition-card d-none mb-4"
    );
    bloque.innerHTML = `
      <div>
        <strong>Este escenario debe calcularse bajo SUCGS.</strong>
        <p class="mb-0 mt-1">
          La fecha seleccionada cae dentro de la transición legal
          identificada por el motor Mixto. Puedes continuar con el
          mismo escenario sin cambiar silenciosamente el sistema
          informado en el Paso 1.
        </p>
      </div>
      <button
        type="button"
        id="btn-preparar-sucgs-transicion"
        class="btn btn-primary"
      >
        Preparar cálculo SUCGS
      </button>
    `;
    estado.insertAdjacentElement("afterend", bloque);

    bloque.querySelector(
      "#btn-preparar-sucgs-transicion",
    ).addEventListener(
      "click",
      prepararCalculoSUCGSDesdeTransicion,
    );

    const configSUCGS = document.getElementById(
      "resultado-config-sucgs",
    );
    const encabezado = configSUCGS?.querySelector(
      ".results-section-heading",
    );

    if (
      encabezado
      && !document.getElementById(
        "resultado-sucgs-contexto-transicion",
      )
    ) {
      const nota = document.createElement("div");
      nota.id = "resultado-sucgs-contexto-transicion";
      nota.className = (
        "alert alert-info d-none mt-3 mb-0"
      );
      nota.textContent = (
        "Este cálculo SUCGS se prepara porque el motor Mixto "
        + "determinó una transición legal para la fecha de retiro "
        + "seleccionada. Debes completar o confirmar los datos "
        + "específicos del SUCGS antes de calcular."
      );
      encabezado.insertAdjacentElement("afterend", nota);
    }
  }


  function envolverResultadoMixto() {
    const original = window.mostrarResultadoMixto;

    if (typeof original !== "function") {
      return;
    }

    window.mostrarResultadoMixto = function mostrarMixtoConTransicion(
      resultado,
    ) {
      const respuesta = original(resultado);
      actualizarAccionTransicionMixto(resultado);
      marcarOrigenMixtoVisible(
        "resultado-mixto-bd-anios-body",
        resultado?.anios_proyectados_incluidos,
      );
      return respuesta;
    };
  }


  function envolverRestauracionSUCGS() {
    const original = window.restaurarResultadoSUCGSGuardado;

    if (typeof original !== "function") {
      return;
    }

    window.restaurarResultadoSUCGSGuardado =
      function restaurarSUCGSIncluyendoTransicion() {
        const simulacion = obtenerSimulacion();

        if (
          simulacion.resultado_sucgs
          && escenarioMixtoEnTransicion(simulacion)
        ) {
          document.getElementById(
            "resultado-config-sucgs",
          )?.classList.remove("d-none");
          mostrarContextoTransicionSUCGS(true);
          window.prepararConfiguracionSUCGS?.(simulacion);
          mostrarResultadoSUCGS(simulacion.resultado_sucgs);
          mostrarComparacionOrigenDatos(
            simulacion.resultado_sucgs_acreditado || null,
            simulacion.resultado_sucgs,
          );
          return;
        }

        original();
      };
  }


  function asegurarAyudaDespuesDeGrupo(
    inputId,
    texto,
    idAyuda,
  ) {
    if (document.getElementById(idAyuda)) {
      return;
    }

    const input = document.getElementById(inputId);
    const grupo = input?.closest(".input-group");

    if (!input || !grupo) {
      return;
    }

    const ayuda = document.createElement("div");
    ayuda.id = idAyuda;
    ayuda.className = "form-text";
    ayuda.textContent = texto;
    grupo.insertAdjacentElement("afterend", ayuda);

    const ids = new Set(
      (input.getAttribute("aria-describedby") || "")
        .split(/\s+/)
        .filter(Boolean),
    );
    ids.add(idAyuda);
    input.setAttribute(
      "aria-describedby",
      Array.from(ids).join(" "),
    );
  }


  function unirMotivosNaturales(motivos) {
    if (motivos.length <= 1) {
      return motivos[0] || "";
    }

    if (motivos.length === 2) {
      return `${motivos[0]} y ${motivos[1]}`;
    }

    return (
      motivos.slice(0, -1).join(", ")
      + ` y ${motivos.at(-1)}`
    );
  }


  function resumenAcreditadoPorSistema(simulacion, sistema) {
    if (sistema === "SEBD") {
      return simulacion.resultado_sebd_acreditado?.resumen_unificado || null;
    }
    if (sistema === "MIXTO") {
      return simulacion.resultado_mixto_acreditado?.resumen_unificado || null;
    }
    if (sistema === "SUCGS") {
      return simulacion.resultado_sucgs_acreditado?.resumen_unificado || null;
    }
    return null;
  }


  function envolverComparacionReferencia() {
    const original = window.mostrarComparacionReferenciaMiRetiroSeguro;

    if (typeof original !== "function") {
      return;
    }

    window.mostrarComparacionReferenciaMiRetiroSeguro =
      function mostrarReferenciaConMotivoLegible(resumenActual) {
        const respuesta = original(resumenActual);
        const simulacion = obtenerSimulacion();
        const referencia = simulacion.referencia_mi_retiro_seguro;
        const estado = document.getElementById(
          "resultado-referencia-estado-comparacion",
        );
        const diferencia = document.getElementById(
          "resultado-referencia-diferencia",
        );

        if (
          !referencia
          || !estado
          || diferencia?.textContent?.trim() !== "No comparable"
        ) {
          return respuesta;
        }

        const sistema = simulacion.persona?.sistema;
        const resumenComparado = (
          resumenAcreditadoPorSistema(simulacion, sistema)
          || resumenActual
        );

        if (!resumenComparado) {
          return respuesta;
        }

        const motivos = [];
        const inconsistencias = (
          typeof window.obtenerInconsistenciasReferencia === "function"
        )
          ? window.obtenerInconsistenciasReferencia(referencia)
          : [];

        const mismaPersona = inconsistencias
          .filter((mensaje) => !mensaje.includes("sistema"))
          .length === 0;

        if (!mismaPersona) {
          motivos.push("los datos personales no coinciden");
        }

        if (
          referencia.sistema_elegido === "NO_IDENTIFICADO"
          || referencia.sistema_elegido !== resumenComparado.sistema
        ) {
          motivos.push("el sistema previsional es distinto");
        }

        if (
          referencia.edad_retiro_elegida == null
          || Number(referencia.edad_retiro_elegida)
            !== Number(resumenComparado.edad_retiro_anios)
        ) {
          motivos.push(
            "la edad de retiro del comprobante "
            + `(${referencia.edad_retiro_elegida ?? "—"} años) `
            + "es distinta de la edad del escenario actual "
            + `(${resumenComparado.edad_retiro_anios ?? "—"} años)`,
          );
        }

        if (motivos.length === 0) {
          motivos.push(
            "el tipo de prestación no permite una comparación directa",
          );
        }

        estado.textContent = (
          "El comprobante se conserva como referencia, pero no se calcula "
          + "una diferencia directa porque "
          + unirMotivosNaturales(motivos)
          + "."
        );

        return respuesta;
      };
  }


  function envolverComparacionOrigenDatos() {
    const original = window.mostrarComparacionOrigenDatos;

    if (typeof original !== "function") {
      return;
    }

    window.mostrarComparacionOrigenDatos =
      function mostrarComparacionConExplicacion(...args) {
        const respuesta = original(...args);

        const estado = document.getElementById(
          "resultado-origen-estado",
        );
        if (estado) {
          estado.textContent = (
            "Ambas columnas evalúan la misma fecha de retiro. "
            + "La diferencia muestra el efecto de incorporar las "
            + "cotizaciones futuras del escenario seleccionado; no reemplaza "
            + "la información ya acreditada."
          );
        }

        document.querySelector(
          "#resultado-comparacion-origen-datos "
          + ".result-origin-table-wrap",
        )?.classList.add("table-scroll-compact");

        return respuesta;
      };
  }


  function registroHistoricoDelAnio(anio) {
    const simulacion = obtenerSimulacion();
    return (simulacion.historial?.registros || []).find(
      (registro) => Number(registro.anio) === Number(anio),
    );
  }


  function marcarOrigenMixtoVisible(cuerpoId, aniosProyectados) {
    const cuerpo = document.getElementById(cuerpoId);
    if (!cuerpo) {
      return;
    }

    const proyectados = new Set(
      (aniosProyectados || []).map(Number),
    );

    cuerpo.querySelectorAll("tr").forEach((fila) => {
      const anio = Number(
        fila.querySelector("td")?.textContent?.trim(),
      );
      const badge = fila.querySelector(".results-origin");

      if (!badge || !proyectados.has(anio)) {
        return;
      }

      const historico = registroHistoricoDelAnio(anio);
      const contieneAcreditado = Boolean(
        historico
        && (
          Number(historico.cuotas) > 0
          || Number(historico.salario_cotizado) > 0
        )
      );

      if (contieneAcreditado) {
        badge.className = "results-origin results-origin-mixed";
        badge.textContent = "Histórico + proyectado";
      }
    });
  }


  function actualizarEstadoSEBD(calculo) {
    const alerta = document.getElementById(
      "resultado-sebd-elegibilidad",
    );

    if (
      !alerta
      || !calculo?.elegible
      || !calculo?.calculo_disponible
    ) {
      return;
    }

    alerta.replaceChildren();

    const titulo = document.createElement("strong");
    const detalle = document.createElement("span");

    if (calculo.modalidad === "INDEMNIZACION") {
      titulo.textContent = "Prestación calculable.";
      detalle.textContent = (
        " Con los datos ingresados, este escenario permite estimar "
        + "una Indemnización por Vejez de pago único."
      );
      alerta.className = "alert alert-info";
    } else {
      titulo.textContent = "Escenario calculable.";
      detalle.textContent = (
        " Con los datos ingresados, el motor puede calcular una "
        + "prestación SEBD para este escenario."
      );
      alerta.className = "alert alert-success";
    }

    alerta.append(titulo, detalle);
  }


  function ajustarFactoresSEBD(calculo) {
    const factores = document.getElementById(
      "resultado-sebd-factores",
    );
    if (!factores) {
      return;
    }

    const modalidadesConFactores = new Set([
      "ANTICIPADA",
      "PROPORCIONAL",
      "PROPORCIONAL_ANTICIPADA",
    ]);

    factores.classList.toggle(
      "d-none",
      !modalidadesConFactores.has(calculo?.modalidad),
    );
  }


  function normalizarFechaTrazabilidadVisible() {
    document.querySelectorAll(
      "#resultado-trazabilidad-datos .trace-data-card",
    ).forEach((tarjeta) => {
      const etiqueta = tarjeta.querySelector("span");
      const valor = tarjeta.querySelector("strong");

      if (
        etiqueta?.textContent?.trim() === "Fecha de retiro evaluada"
        && /^\d{4}-\d{2}-\d{2}$/.test(valor?.textContent?.trim() || "")
        && typeof window.formatearFechaRetiro === "function"
      ) {
        valor.textContent = window.formatearFechaRetiro(
          valor.textContent.trim(),
        );
      }
    });
  }


  function envolverTrazabilidadLegible() {
    const original = window.mostrarTrazabilidadCalculo;

    if (typeof original !== "function") {
      return;
    }

    window.mostrarTrazabilidadCalculo =
      function mostrarTrazabilidadConFechaLegible(...args) {
        const respuesta = original(...args);
        normalizarFechaTrazabilidadVisible();
        return respuesta;
      };
  }


  function envolverResultadoSEBDLegible() {
    const original = window.mostrarResultadoSEBD;

    if (typeof original !== "function") {
      return;
    }

    window.mostrarResultadoSEBD =
      function mostrarSEBDConJerarquia(resultado) {
        const respuesta = original(resultado);

        actualizarEstadoSEBD(resultado?.calculo);
        ajustarFactoresSEBD(resultado?.calculo);
        marcarOrigenMixtoVisible(
          "resultado-sebd-anios-body",
          resultado?.anios_proyectados_incluidos,
        );

        return respuesta;
      };
  }


  function retirarNavegacionLocalRedundante() {
    window.setTimeout(
      () => {
        const boton = document.getElementById(
          "btn-volver-paso-5",
        );
        const contenedor = boton?.parentElement;

        if (
          contenedor
          && contenedor.children.length === 1
        ) {
          contenedor.remove();
        } else {
          boton?.remove();
        }
      },
      0,
    );
  }


  function configurarTextosUtiles() {
    const parrafoResumen = document.querySelector(
      "#resultado-resumen-unificado "
      + ".results-section-heading p",
    );

    if (parrafoResumen) {
      parrafoResumen.textContent = (
        "Aquí se resume el tipo de prestación y los montos "
        + "del escenario seleccionado. Los pagos mensuales y "
        + "los pagos únicos se muestran por separado para evitar "
        + "confusiones."
      );
    }

    const etiquetaVMU = document.querySelector(
      'label[for="resultado-sucgs-minimo-universal"]',
    );
    if (etiquetaVMU) {
      etiquetaVMU.textContent = (
        "Referencia legal del valor mínimo universal"
      );
    }

    const etiquetaPGS = document.querySelector(
      'label[for="resultado-sucgs-pgs"]',
    );
    if (etiquetaPGS) {
      etiquetaPGS.textContent = (
        "Referencia legal de Pensión Garantizada Solidaria"
      );
    }

    const etiquetaConfirmacion = document.querySelector(
      'label[for="resultado-sucgs-valores-confirmados"]',
    );
    if (etiquetaConfirmacion) {
      etiquetaConfirmacion.textContent = (
        "Confirmo que ambos valores corresponden a los "
        + "valores oficiales aplicables a esta simulación"
      );
    }

    asegurarAyudaDespuesDeGrupo(
      "resultado-sucgs-minimo-universal",
      "B/.144.00 es la referencia legal versionada al 22/05/2025. "
        + "Sustitúyela si confirmaste un valor oficial aplicable distinto.",
      "resultado-sucgs-minimo-universal-ayuda",
    );

    asegurarAyudaDespuesDeGrupo(
      "resultado-sucgs-pgs",
      "B/.265.00 es la referencia legal versionada al 22/05/2025. "
        + "Sustitúyela si confirmaste un valor oficial aplicable distinto.",
      "resultado-sucgs-pgs-ayuda",
    );

    asegurarAyudaDespuesDeGrupo(
      "resultado-mixto-bono",
      "B/.0.00 significa que no se incorpora un bono de reconocimiento. "
        + "Si introduces un monto mayor que cero, marca la confirmación "
        + "solo cuando provenga de información oficial.",
      "resultado-mixto-bono-ayuda",
    );
  }


  function elementoVisibleParaImpresion(elemento) {
    if (!elemento || elemento.classList.contains("d-none")) {
      return false;
    }
    return window.getComputedStyle(elemento).display !== "none";
  }


  function limpiarClonParaInforme(origen) {
    const clon = origen.cloneNode(true);

    clon.querySelectorAll(
      "button, select, input, textarea, .results-calculation-card, "
      + ".results-export-card, .wizard-actions, .wizard-actions-start, "
      + ".wizard-actions-end, .skip-link",
    ).forEach((elemento) => elemento.remove());

    clon.querySelectorAll("[id]").forEach((elemento) => {
      elemento.removeAttribute("id");
    });

    clon.querySelectorAll(".d-none").forEach((elemento) => {
      elemento.remove();
    });

    clon.querySelectorAll(".collapse").forEach((elemento) => {
      elemento.classList.add("show");
      elemento.style.display = "block";
      elemento.style.height = "auto";
    });

    clon.querySelectorAll("a.btn").forEach((enlace) => {
      enlace.classList.remove("btn", "btn-outline-primary", "btn-primary");
    });

    return clon;
  }


  function agregarSeccionInforme(documento, origen, claseExtra = "") {
    if (!elementoVisibleParaImpresion(origen)) {
      return;
    }

    const seccion = document.createElement("section");
    seccion.className = `print-report-section ${claseExtra}`.trim();
    seccion.appendChild(limpiarClonParaInforme(origen));
    documento.appendChild(seccion);
  }


  function construirDocumentoImpresion() {
    document.getElementById("resultado-print-document")?.remove();

    const simulacion = typeof obtenerSimulacion === "function"
      ? obtenerSimulacion()
      : {};
    const sistema = document.getElementById("resultado-sistema")
      ?.textContent?.trim() || "—";
    const escenario = document.getElementById("resultado-escenario-retiro")
      ?.textContent?.trim() || "—";
    const fechaEdad = document.getElementById("resultado-fecha-edad")
      ?.textContent?.trim() || "—";
    const cuotas = document.getElementById("resultado-pension-cuotas")
      ?.textContent?.trim() || "—";
    const version = document.querySelector(".footer-version")
      ?.textContent?.trim() || "Versión no indicada";
    const generado = new Date().toLocaleString("es-PA", {
      dateStyle: "long",
      timeStyle: "short",
    });

    const documento = document.createElement("article");
    documento.id = "resultado-print-document";
    documento.className = "print-report-document";
    documento.setAttribute("aria-hidden", "true");

    const crearElementoInforme = (tag, clase = "", texto = null) => {
      const elemento = document.createElement(tag);

      if (clase) {
        elemento.className = clase;
      }

      if (texto !== null && texto !== undefined) {
        elemento.textContent = String(texto);
      }

      return elemento;
    };

    const crearFilaMetaInforme = (etiqueta, valor) => {
      const fila = document.createElement("div");
      const termino = crearElementoInforme("dt", "", etiqueta);
      const dato = crearElementoInforme("dd", "", valor ?? "—");

      fila.append(termino, dato);
      return fila;
    };

    const portada = crearElementoInforme(
      "header",
      "print-report-cover",
    );

    const filaMarca = crearElementoInforme(
      "div",
      "print-report-brand-row",
    );

    const marca = crearElementoInforme(
      "div",
      "print-report-brand",
    );

    const logo = document.createElement("img");
    logo.src = "/static/img/brand/logo-mark-128.png";
    logo.alt = "";

    const textoMarca = document.createElement("div");
    textoMarca.append(
      crearElementoInforme(
        "strong",
        "",
        "Mi Retiro Proyectado",
      ),
      crearElementoInforme(
        "span",
        "",
        "Planificación previsional independiente",
      ),
    );

    marca.append(logo, textoMarca);

    const versionInforme = crearElementoInforme(
      "span",
      "print-report-version",
      version,
    );

    filaMarca.append(marca, versionInforme);

    const bloqueTitulo = crearElementoInforme(
      "div",
      "print-report-title-block",
    );

    bloqueTitulo.append(
      crearElementoInforme(
        "p",
        "print-report-kicker",
        "Informe de simulación",
      ),
      crearElementoInforme(
        "h1",
        "",
        "Proyección de jubilación",
      ),
      crearElementoInforme(
        "p",
        "",
        "Resumen de la simulación realizada con los datos confirmados "
          + "y los supuestos seleccionados en la aplicación.",
      ),
    );

    const escenarioSalarial = (
      simulacion.escenario_salarial_seleccionado
      || simulacion.configuracion_mixto_resultados
        ?.escenario_salarial_nombre
      || simulacion.configuracion_sucgs_resultados
        ?.escenario_salarial_nombre
      || "—"
    );

    const meta = crearElementoInforme(
      "dl",
      "print-report-meta",
    );

    meta.append(
      crearFilaMetaInforme("Sistema previsional", sistema),
      crearFilaMetaInforme("Escenario de retiro", escenario),
      crearFilaMetaInforme("Fecha y edad", fechaEdad),
      crearFilaMetaInforme("Cuotas estimadas", cuotas),
      crearFilaMetaInforme(
        "Escenario salarial",
        escenarioSalarial,
      ),
      crearFilaMetaInforme("Generado", generado),
    );

    const aviso = crearElementoInforme(
      "div",
      "print-report-notice",
    );

    aviso.append(
      crearElementoInforme(
        "strong",
        "",
        "Resultado estimado.",
      ),
      document.createTextNode(
        " Este informe no es una resolución, certificación "
          + "ni documento oficial de la Caja de Seguro Social.",
      ),
    );

    portada.append(
      filaMarca,
      bloqueTitulo,
      meta,
      aviso,
    );

    documento.appendChild(portada);

    agregarSeccionInforme(
      documento,
      document.getElementById("resultado-resumen-unificado"),
      "print-report-summary",
    );
    agregarSeccionInforme(
      documento,
      document.getElementById("resultado-comparacion-origen-datos"),
      "print-report-comparison",
    );
    agregarSeccionInforme(
      documento,
      document.getElementById("resultado-comparacion-referencia"),
      "print-report-reference",
    );

    ["resultado-sebd", "resultado-mixto", "resultado-sucgs"].forEach((id) => {
      const origen = document.getElementById(id);
      if (elementoVisibleParaImpresion(origen)) {
        agregarSeccionInforme(documento, origen, "print-report-system");
      }
    });

    agregarSeccionInforme(
      documento,
      document.getElementById("resultado-trazabilidad-calculo"),
      "print-report-trace",
    );

    const pie = document.createElement("footer");
    pie.className = "print-report-footer";
    const marcaPie = document.createElement("strong");
    marcaPie.textContent = "Mi Retiro Proyectado";

    pie.append(
      marcaPie,
      document.createTextNode(
        " · " + String(version ?? ""),
      ),
      document.createElement("br"),
      document.createTextNode(
        "Cálculo independiente sujeto a los datos suministrados, "
          + "a las reglas implementadas y a la normativa aplicable "
          + "al momento de tramitar la prestación.",
      ),
    );
    documento.appendChild(pie);

    document.body.appendChild(documento);
  }


  function crearCabeceraImpresion() {
    if (document.getElementById("resultado-print-header")) {
      return;
    }

    const cuerpo = panelResultados.querySelector(
      ".simulation-card .card-body",
    );

    if (!cuerpo) {
      return;
    }

    const cabecera = document.createElement("section");
    cabecera.id = "resultado-print-header";
    cabecera.className = "results-print-header";
    cabecera.setAttribute(
      "aria-label",
      "Identificación de la copia imprimible",
    );
    cabecera.innerHTML = `
      <div class="results-print-brand">
        <strong>Mi Retiro Proyectado</strong>
        <span id="resultado-print-version">—</span>
      </div>
      <h2>Copia de la simulación previsional</h2>
      <p>
        Documento generado desde la vista de resultados.
        No es una resolución ni certificación de la Caja de Seguro Social.
      </p>
      <dl class="results-print-meta">
        <div>
          <dt>Sistema</dt>
          <dd id="resultado-print-sistema">—</dd>
        </div>
        <div>
          <dt>Escenario de retiro</dt>
          <dd id="resultado-print-escenario">—</dd>
        </div>
        <div>
          <dt>Fecha y edad</dt>
          <dd id="resultado-print-fecha-edad">—</dd>
        </div>
        <div>
          <dt>Generado</dt>
          <dd id="resultado-print-generado">—</dd>
        </div>
      </dl>
    `;

    cuerpo.prepend(cabecera);
  }


  function actualizarEnlaceComoSeCalcula(resumen) {
    const enlace = document.getElementById(
      "resultado-ver-como-se-calcula",
    );

    if (!enlace) {
      return;
    }

    const sistema = String(resumen?.sistema || "").toUpperCase();
    const anclas = {
      SEBD: "sebd",
      MIXTO: "mixto",
      SUCGS: "sucgs",
    };
    const ancla = anclas[sistema];

    enlace.href = ancla
      ? `/como-se-calcula#${ancla}`
      : "/como-se-calcula";
  }


  function crearAccionesExportacion() {
    if (document.getElementById("resultado-exportacion")) {
      return;
    }

    const resumen = document.getElementById(
      "resultado-resumen-unificado",
    );

    if (!resumen) {
      return;
    }

    const bloque = document.createElement("section");
    bloque.id = "resultado-exportacion";
    bloque.className = (
      "results-export-card mt-4 d-none"
    );
    bloque.setAttribute(
      "aria-labelledby",
      "resultado-exportacion-titulo",
    );
    bloque.innerHTML = `
      <div>
        <span class="text-primary fw-semibold">
          Copia de la simulación
        </span>
        <h3
          id="resultado-exportacion-titulo"
          class="h5 fw-bold mb-1"
        >
          Preparar informe para imprimir o guardar como PDF
        </h3>
        <p class="text-secondary mb-0">
          Se generará una versión A4 compacta y separada de la pantalla,
          con el resumen, el desglose, las advertencias y la trazabilidad
          disponibles. No es un documento oficial de la CSS.
        </p>
      </div>
      <div class="d-grid gap-2 flex-shrink-0">
        <a
          id="resultado-ver-como-se-calcula"
          class="btn btn-outline-primary btn-center-content"
          href="/como-se-calcula"
        >
          Ver cómo se obtuvo este cálculo
        </a>
        <button
          type="button"
          id="btn-imprimir-resultado"
          class="btn btn-primary btn-center-content"
        >
          Preparar informe para imprimir
        </button>
      </div>
    `;

    resumen.insertAdjacentElement("afterend", bloque);

    bloque.querySelector(
      "#btn-imprimir-resultado",
    ).addEventListener(
      "click",
      () => {
        prepararCabeceraImpresion();
        construirDocumentoImpresion();
        window.print();
      },
    );
  }


  function prepararCabeceraImpresion() {
    const copiar = (origenId, destinoId) => {
      const origen = document.getElementById(origenId);
      const destino = document.getElementById(destinoId);
      if (destino) {
        destino.textContent = origen?.textContent?.trim() || "—";
      }
    };

    copiar("resultado-sistema", "resultado-print-sistema");
    copiar(
      "resultado-escenario-retiro",
      "resultado-print-escenario",
    );
    copiar("resultado-fecha-edad", "resultado-print-fecha-edad");

    const version = document.querySelector(
      ".footer-version",
    )?.textContent?.trim();
    document.getElementById(
      "resultado-print-version",
    ).textContent = version || "Versión no indicada";

    document.getElementById(
      "resultado-print-generado",
    ).textContent = new Date().toLocaleString(
      "es-PA",
      {
        dateStyle: "medium",
        timeStyle: "short",
      },
    );
  }


  function envolverResumenUnificado() {
    const original = window.mostrarResumenResultadoUnificado;

    if (typeof original !== "function") {
      return;
    }

    window.mostrarResumenResultadoUnificado =
      function mostrarResumenConExportacion(resumen) {
        const respuesta = original(resumen);
        document.getElementById(
          "resultado-exportacion",
        )?.classList.toggle("d-none", !resumen);
        actualizarEnlaceComoSeCalcula(resumen);
        prepararCabeceraImpresion();
        return respuesta;
      };
  }


  function configurarPrecalculo() {
    [
      "btn-calcular-resultado-sebd",
      "btn-calcular-resultado-mixto",
      "btn-calcular-resultado-sucgs",
    ].forEach((id) => {
      document.getElementById(id)?.addEventListener(
        "click",
        () => {
          ocultarSalidaDependientePaso6({
            incluirEspecificos: true,
          });
        },
        true,
      );
    });
  }


  function instalarContratos() {
    envolverPreparador(
      "prepararEscenariosSalarialesResultados",
      "SEBD",
    );
    envolverPreparador(
      "prepararConfiguracionMixto",
      "MIXTO",
    );
    envolverPreparador(
      "prepararConfiguracionSUCGS",
      "SUCGS",
    );

    envolverInvalidacion("invalidarResultadoSEBD");
    envolverInvalidacion("invalidarResultadoMixto");
    envolverInvalidacion("invalidarResultadoSUCGS");

    if (
      typeof window.construirSolicitudResultadoSUCGS
      === "function"
    ) {
      window.construirSolicitudResultadoSUCGS =
        construirSolicitudSUCGSConTransicion;
    }

    envolverResultadoMixto();
    envolverRestauracionSUCGS();
    envolverResumenUnificado();
    envolverComparacionReferencia();
    envolverComparacionOrigenDatos();
    envolverTrazabilidadLegible();
    envolverResultadoSEBDLegible();

    crearInterfazTransicion();
    crearCabeceraImpresion();
    crearAccionesExportacion();
    configurarTextosUtiles();
    configurarPrecalculo();
    retirarNavegacionLocalRedundante();

    window.addEventListener(
      "beforeprint",
      () => {
        prepararCabeceraImpresion();
        construirDocumentoImpresion();
      },
    );
  }


  function iniciarOrquestacionResultados() {
    panelResultados = document.querySelector(
      '.wizard-panel[data-panel="6"]',
    );

    if (!panelResultados) {
      return;
    }

    cargarEstilosResultados();
    instalarContratos();
  }


  if (document.querySelector(
    '.wizard-panel[data-panel="6"]',
  )) {
    cargarEstilosResultados();
  }


  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      iniciarOrquestacionResultados,
      { once: true },
    );
  } else {
    iniciarOrquestacionResultados();
  }
})();
