"use strict";

/* ============================================================
   Mi Retiro Proyectado
   Procedencia editable y control de datos importados
   ============================================================ */

/*
 * Los documentos importados son una fuente de referencia, no una jaula de
 * edición. Esta capa permite al Asegurado(a) ajustar datos confirmados sin
 * alterar silenciosamente la fotografía original del documento.
 *
 * El módulo se carga después de los scripts específicos de cada vista para
 * ampliar sus contratos sin duplicar la lógica previsional existente.
 */

(() => {
  if (!document.querySelector(".page-simulacion, [data-panel='1']")) {
    return;
  }

  const CAMPOS_PERSONA = {
    primer_nombre: {
      referencia: "primer_nombre",
      preview: "preview-comprobante-primer-nombre",
    },
    segundo_nombre: {
      referencia: "segundo_nombre",
      preview: "preview-comprobante-segundo-nombre",
    },
    primer_apellido: {
      referencia: "primer_apellido",
      preview: "preview-comprobante-primer-apellido",
    },
    segundo_apellido: {
      referencia: "segundo_apellido",
      preview: "preview-comprobante-segundo-apellido",
    },
    apellido_casada: {
      referencia: "apellido_casada",
      preview: "preview-comprobante-apellido-casada",
    },
    cedula: {
      referencia: "cedula",
      preview: "preview-comprobante-cedula",
    },
    numero_seguro_social: {
      referencia: "numero_seguro_social",
      preview: "preview-comprobante-seguro-social",
    },
    fecha_nacimiento: {
      referencia: "fecha_nacimiento",
      preview: "preview-comprobante-fecha-nacimiento",
    },
    sexo: {
      referencia: "sexo",
      preview: "preview-comprobante-sexo",
    },
    fecha_ingreso_css: {
      referencia: "fecha_ingreso_css",
      preview: "preview-comprobante-fecha-ingreso",
    },
    sistema: {
      referencia: "sistema_elegido",
      preview: "preview-comprobante-sistema",
    },
  };

  const MENSAJE_AJUSTE = (
    "Has ajustado, completado o excluido información asociada a un documento. "
    + "El documento original se conserva como referencia; Mi Retiro Proyectado "
    + "utilizará estos cambios únicamente para esta simulación y los "
    + "identificará por su procedencia."
  );

  const origenBloqueaCampoBase = window.origenBloqueaCampo;
  const bloquearFormularioPersonalBase = window.bloquearFormularioPersonal;
  const actualizarOrigenCamposCuotasBase = window.actualizarOrigenCamposCuotas;
  const aplicarOrigenCampoHistorialBase = window.aplicarOrigenCampoHistorial;
  const manejarEdicionDelegadaHistorialBase = window.manejarEdicionDelegadaHistorial;
  const marcarCampoDetalleImportadoBase = window.marcarCampoDetalleImportado;
  const actualizarProcedenciaFilaDetalleBase = window.actualizarProcedenciaFilaDetalle;
  const actualizarEstadoFilaDetalleBase = window.actualizarEstadoFilaDetalle;
  const actualizarColumnasModoDetalleBase = window.actualizarColumnasModoDetalle;
  const leerDetalleAnioActualBase = window.leerDetalleAnioActual;
  const establecerEdicionPreviewFichaBase = window.establecerEdicionPreviewFicha;
  const confirmarComprobanteImportacionBase = window.confirmarComprobanteImportacion;
  const confirmarFichaDigitalImportacionBase = window.confirmarFichaDigitalImportacion;
  const quitarComprobanteImportacionBase = window.quitarComprobanteImportacion;
  const quitarFichaDigitalImportacionBase = window.quitarFichaDigitalImportacion;

  function valorDetectado(valor) {
    return (
      valor !== null
      && valor !== undefined
      && String(valor).trim() !== ""
      && String(valor).toUpperCase() !== "NO_IDENTIFICADO"
    );
  }

  function textoComparable(valor) {
    if (valor === null || valor === undefined) return "";
    return String(valor).trim();
  }

  function valoresIguales(actual, original, monetario = false) {
    if (monetario && typeof obtenerValorMonetario === "function") {
      const a = obtenerValorMonetario(actual || "0");
      const b = Number(original || 0);
      return Number.isFinite(a) && Math.abs(a - b) < 0.005;
    }
    return textoComparable(actual) === textoComparable(original);
  }

  function codigoDesdeOrigenEditable(origen) {
    const valor = String(origen || "").toUpperCase();
    if (!valor) return null;
    if (valor.includes("EXCLUIDO")) return "EXCLUIDO_USUARIO";
    if (valor.includes("NO_DETECTADO")) return "NO_DETECTADO";
    if (valor.includes("COMPLETADO_MANUAL")) return "COMPLETADO_MANUAL";
    if (valor.includes("EDITADO")) return "EDITADO_USUARIO";
    if (
      valor.includes("MI_RETIRO_SEGURO")
      || valor.includes("FICHA_DIGITAL")
    ) {
      return "DETECTADO";
    }
    if (valor === "MANUAL") return "COMPLETADO_MANUAL";
    return (
      typeof origenBloqueaCampoBase === "function"
        ? null
        : null
    );
  }

  window.codigoProcedenciaDesdeOrigen = codigoDesdeOrigenEditable;

  window.textoProcedenciaDato = (codigo) => {
    const textos = {
      DETECTADO: "Detectado",
      EDITADO_USUARIO: "Editado por ti",
      COMPLETADO_MANUAL: "Completado manualmente",
      EXCLUIDO_USUARIO: "Excluido por ti",
      NO_DETECTADO: "No detectado",
    };
    return textos[codigo] || "";
  };

  window.claseProcedenciaDato = (codigo) => {
    const clases = {
      DETECTADO: "detected",
      EDITADO_USUARIO: "edited",
      COMPLETADO_MANUAL: "manual",
      EXCLUIDO_USUARIO: "excluded",
      NO_DETECTADO: "missing",
    };
    return clases[codigo] || "";
  };

  /*
   * Un origen documental ya no vuelve el control de solo lectura. La
   * procedencia continúa visible y la referencia original se conserva.
   */
  window.origenBloqueaCampo = () => false;

  function asegurarEstructuraProcedencia(simulacion) {
    if (!simulacion.origen_campos_persona) {
      simulacion.origen_campos_persona = {};
    }
    if (!simulacion.origen_campos_cuotas) {
      simulacion.origen_campos_cuotas = {};
    }
    if (!simulacion.origen_campos_historial) {
      simulacion.origen_campos_historial = {};
    }
    if (!simulacion.origen_campos_detalle_anio_actual) {
      simulacion.origen_campos_detalle_anio_actual = {};
    }
    if (!Array.isArray(simulacion.campos_editados_importacion_comprobante)) {
      simulacion.campos_editados_importacion_comprobante = [];
    }
    if (!Array.isArray(simulacion.campos_editados_importacion_ficha)) {
      simulacion.campos_editados_importacion_ficha = [];
    }
    if (!Array.isArray(simulacion.periodos_excluidos_importacion_ficha)) {
      simulacion.periodos_excluidos_importacion_ficha = [];
    }
    return simulacion;
  }

  function preservarReferenciasOriginales(simulacion) {
    asegurarEstructuraProcedencia(simulacion);

    if (
      simulacion.importacion_comprobante_confirmada
      && simulacion.referencia_mi_retiro_seguro
      && !simulacion.referencia_mi_retiro_seguro_original
    ) {
      simulacion.referencia_mi_retiro_seguro_original = structuredClone(
        simulacion.referencia_mi_retiro_seguro,
      );
    }

    if (
      simulacion.importacion_ficha_digital_confirmada
      && simulacion.ficha_digital_importada
      && !simulacion.ficha_digital_importada_original
    ) {
      simulacion.ficha_digital_importada_original = structuredClone(
        simulacion.ficha_digital_importada,
      );
    }

    return simulacion;
  }

  function invalidarResultadosDependientes(simulacion) {
    simulacion.resumen_cuotas = null;
    simulacion.resumen_historial = null;
    simulacion.resumen_detalle_anio_actual = null;
    simulacion.resumen_salario = null;
    simulacion.resumen_proyeccion = null;
    simulacion.resumen_linea_tiempo = null;
    simulacion.retiro = {};
    simulacion.resumen_retiro = null;
    simulacion.escenario_retiro_seleccionado = null;
    simulacion.escenario_salarial_seleccionado = null;
    simulacion.resultado_sebd_normal = null;
    simulacion.resultado_sebd_acreditado = null;
    simulacion.resultado_mixto = null;
    simulacion.resultado_mixto_acreditado = null;
    simulacion.resultado_sucgs = null;
    simulacion.resultado_sucgs_acreditado = null;
  }

  function insertarAviso(id, ancla) {
    let aviso = document.getElementById(id);
    if (aviso) return aviso;
    if (!ancla?.parentElement) return null;

    aviso = document.createElement("div");
    aviso.id = id;
    aviso.className = "alert alert-warning imported-adjustment-warning d-none";
    aviso.setAttribute("role", "status");
    aviso.setAttribute("aria-live", "polite");
    aviso.textContent = MENSAJE_AJUSTE;

    ancla.parentElement.insertBefore(aviso, ancla);
    return aviso;
  }

  function actualizarAviso(id, ancla, activo) {
    const aviso = insertarAviso(id, ancla);
    if (!aviso) return;
    aviso.classList.toggle("d-none", !activo);
  }

  function mostrarAviso(id, ancla) {
    actualizarAviso(id, ancla, true);
  }

  function actualizarLista(lista, clave, activo) {
    const conjunto = new Set(Array.isArray(lista) ? lista : []);
    if (activo) conjunto.add(clave);
    else conjunto.delete(clave);
    return Array.from(conjunto);
  }

  function referenciaComprobanteOriginal(simulacion) {
    return (
      simulacion.referencia_mi_retiro_seguro_original
      || simulacion.referencia_mi_retiro_seguro
      || {}
    );
  }

  function referenciaFichaOriginal(simulacion) {
    return (
      simulacion.ficha_digital_importada_original
      || simulacion.ficha_digital_importada
      || {}
    );
  }

  function registroFichaOriginal(simulacion, anio, mes) {
    return (referenciaFichaOriginal(simulacion).registros || []).find(
      (registro) => (
        Number(registro.anio) === Number(anio)
        && Number(registro.mes) === Number(mes)
      ),
    ) || null;
  }

  function clavePeriodoFicha(anio, mes) {
    return `${Number(anio)}-${String(Number(mes)).padStart(2, "0")}`;
  }

  function periodoExcluido(simulacion, anio, mes) {
    return (simulacion.periodos_excluidos_importacion_ficha || []).includes(
      clavePeriodoFicha(anio, mes),
    );
  }

  function valorOriginalCuotasAnioActual(referencia) {
    if (
      referencia.cuotas_anio_actual !== null
      && referencia.cuotas_anio_actual !== undefined
    ) {
      return referencia.cuotas_anio_actual;
    }
    const actual = (referencia.registros || []).find(
      (registro) => (
        Number(registro.anio) === Number(ANIO_ACTUAL)
        && registro.tipo !== "PROYECTADO"
      ),
    );
    return actual?.cuotas ?? null;
  }

  /*
   * Datos personales: todo campo queda editable y la procedencia cambia
   * inmediatamente al escribir, seleccionar o volver al valor original.
   */
  window.bloquearFormularioPersonal = (
    bloqueado,
    simulacion = obtenerSimulacion(),
  ) => {
    if (typeof bloquearFormularioPersonalBase === "function") {
      bloquearFormularioPersonalBase(false, simulacion);
    }

    document
      .querySelectorAll("#bloque-datos-personales input, #bloque-datos-personales select")
      .forEach((control) => {
        if (control.tagName === "SELECT") {
          control.disabled = false;
        } else {
          control.readOnly = false;
        }
        control.classList.remove("field-imported-readonly");
        control.removeAttribute("aria-readonly");
      });

    if (typeof actualizarProcedenciaDatosPersonales === "function") {
      actualizarProcedenciaDatosPersonales(simulacion);
    }
  };

  function actualizarProcedenciaPersonalDesdeControl(control) {
    const definicion = CAMPOS_PERSONA[control?.id];
    if (!definicion) return;

    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    if (
      !simulacion.importacion_comprobante_confirmada
      || !simulacion.referencia_mi_retiro_seguro
    ) {
      return;
    }

    const original = referenciaComprobanteOriginal(simulacion)[
      definicion.referencia
    ];
    const actual = control.value;
    const habiaOriginal = valorDetectado(original);
    const hayActual = valorDetectado(actual);
    let origen;

    if (!habiaOriginal && !hayActual) {
      origen = "MI_RETIRO_SEGURO_NO_DETECTADO";
    } else if (!habiaOriginal && hayActual) {
      origen = "MI_RETIRO_SEGURO_COMPLETADO_MANUAL";
    } else if (valoresIguales(actual, original)) {
      origen = "MI_RETIRO_SEGURO_DETECTADO";
    } else {
      origen = "MI_RETIRO_SEGURO_EDITADO";
    }

    simulacion.origen_campos_persona[control.id] = origen;
    simulacion.campos_editados_importacion_comprobante = actualizarLista(
      simulacion.campos_editados_importacion_comprobante,
      definicion.preview,
      origen.includes("EDITADO") || origen.includes("COMPLETADO_MANUAL"),
    );

    simulacion.persona = {
      ...(simulacion.persona || {}),
      [control.id]: hayActual ? actual : null,
    };

    /*
     * La referencia vigente funciona como copia de trabajo confirmada para
     * que "Revisar importación" refleje ajustes posteriores. La fotografía
     * documental intacta permanece en referencia_mi_retiro_seguro_original.
     */
    if (simulacion.referencia_mi_retiro_seguro) {
      simulacion.referencia_mi_retiro_seguro[definicion.referencia] = (
        hayActual ? actual : null
      );
    }

    invalidarResultadosDependientes(simulacion);
    guardarSimulacion(simulacion);

    if (typeof mostrarProcedenciaCampo === "function") {
      mostrarProcedenciaCampo(control, origen);
    }

    actualizarAvisosAjustes(simulacion);
  }

  /*
   * Cuotas del Paso 2: los valores detectados siguen identificados, pero
   * pueden corregirse directamente sin regresar al modal de importación.
   */
  window.actualizarOrigenCamposCuotas = (
    simulacion = obtenerSimulacion(),
  ) => {
    preservarReferenciasOriginales(simulacion);
    const importacionConfirmada = Boolean(
      simulacion.importacion_comprobante_confirmada,
    );

    const campos = [
      {
        id: "cuotas_totales",
        notaId: "origen-cuotas-totales",
      },
      {
        id: "cuotas_anio_actual",
        notaId: "origen-cuotas-anio-actual",
      },
    ];

    campos.forEach(({ id, notaId }) => {
      const control = document.getElementById(id);
      const nota = document.getElementById(notaId);
      if (!control || !nota) return;

      control.readOnly = false;
      control.classList.remove("field-imported-readonly");
      control.removeAttribute("aria-readonly");

      const origen = simulacion.origen_campos_cuotas?.[id] || null;
      const codigo = window.codigoProcedenciaDesdeOrigen(origen);

      if (codigo) {
        nota.textContent = window.textoProcedenciaDato(codigo);
        nota.className = (
          `field-origin-note data-provenance-note ${
            window.claseProcedenciaDato(codigo)
          }`
        );
        control.dataset.provenance = codigo;
      } else if (importacionConfirmada) {
        nota.textContent = "No detectado";
        nota.className = "field-origin-note data-provenance-note missing";
      } else {
        nota.textContent = "";
        nota.className = "field-origin-note d-none";
      }
    });

    const acciones = document.getElementById("cuotas-importadas-acciones");
    acciones?.classList.toggle("d-none", !importacionConfirmada);
    const estado = document.getElementById("cuotas-importadas-estado");
    if (estado && importacionConfirmada) {
      estado.textContent = (
        "Los valores importados pueden ajustarse. "
        + "La procedencia original se conserva y cualquier cambio se identifica."
      );
    }
  };

  function actualizarProcedenciaCuotasDesdeControl(control) {
    if (!["cuotas_totales", "cuotas_anio_actual"].includes(control?.id)) {
      return;
    }

    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    if (!simulacion.importacion_comprobante_confirmada) return;

    const referencia = referenciaComprobanteOriginal(simulacion);
    const original = control.id === "cuotas_totales"
      ? referencia.cuotas_historicas
      : valorOriginalCuotasAnioActual(referencia);

    const actual = control.value;
    const habiaOriginal = original !== null && original !== undefined;
    let origen;

    if (!habiaOriginal && actual === "") {
      origen = "MI_RETIRO_SEGURO_NO_DETECTADO";
    } else if (!habiaOriginal) {
      origen = "MI_RETIRO_SEGURO_COMPLETADO_MANUAL";
    } else if (Number(actual) === Number(original)) {
      origen = "MI_RETIRO_SEGURO_DETECTADO";
    } else {
      origen = "MI_RETIRO_SEGURO_EDITADO";
    }

    simulacion.origen_campos_cuotas[control.id] = origen;
    simulacion.cuotas = {
      ...(simulacion.cuotas || {}),
      [control.id]: actual === "" ? null : Number(actual),
    };
    invalidarResultadosDependientes(simulacion);
    guardarSimulacion(simulacion);
    window.actualizarOrigenCamposCuotas(simulacion);

    actualizarAvisosAjustes(simulacion);
  }

  /*
   * Historial anual: la fila conserva su señal documental, pero cuotas y
   * salario dejan de estar bloqueados. Revertir al valor original devuelve
   * el estado Detectado.
   */
  window.aplicarOrigenCampoHistorial = (control, anio, campo) => {
    if (!control) return;

    if (control.dataset.sincronizadoDetalle === "true") {
      control.readOnly = true;
      return;
    }

    const origen = typeof origenCampoHistorial === "function"
      ? origenCampoHistorial(anio, campo)
      : null;

    control.readOnly = false;
    control.removeAttribute("aria-readonly");
    control.classList.toggle("history-field-imported", Boolean(origen));

    if (!origen) {
      control.dataset.provenance = control.value.trim()
        ? "COMPLETADO_MANUAL"
        : "NO_DETECTADO";
      return;
    }

    const codigo = window.codigoProcedenciaDesdeOrigen(origen) || "DETECTADO";
    control.dataset.provenance = codigo;
    control.title = (
      `${window.textoProcedenciaDato(codigo)}. `
      + "Puedes ajustar el valor; la referencia original se conservará."
    );
  };

  function actualizarOrigenHistorialDesdeControl(control, fila) {
    const anio = Number(fila?.dataset.anio || 0);
    if (!anio) return null;

    const esCuotas = control.classList.contains("history-input-cuotas");
    const campo = esCuotas ? "cuotas" : "salario_cotizado";
    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    const referencia = referenciaComprobanteOriginal(simulacion);
    const original = (referencia.registros || []).find(
      (registro) => (
        Number(registro.anio) === anio
        && registro.tipo !== "PROYECTADO"
      ),
    );

    if (!simulacion.origen_campos_historial[String(anio)]) {
      simulacion.origen_campos_historial[String(anio)] = {};
    }

    let origen;
    if (!original) {
      origen = control.value.trim()
        ? "COMPLETADO_MANUAL"
        : "NO_DETECTADO";
    } else {
      const valorOriginal = esCuotas
        ? original.cuotas
        : original.salario_anual;
      const igual = valoresIguales(
        control.value,
        valorOriginal,
        !esCuotas,
      );
      origen = igual
        ? "MI_RETIRO_SEGURO_DETECTADO"
        : "MI_RETIRO_SEGURO_EDITADO";
    }

    simulacion.origen_campos_historial[String(anio)][campo] = origen;
    const clave = `historial:${anio}:${esCuotas ? "cuotas" : "salario"}`;
    simulacion.campos_editados_importacion_comprobante = actualizarLista(
      simulacion.campos_editados_importacion_comprobante,
      clave,
      origen.includes("EDITADO"),
    );

    invalidarResultadosDependientes(simulacion);
    guardarSimulacion(simulacion);
    control.dataset.provenance = window.codigoProcedenciaDesdeOrigen(origen);

    actualizarAvisosAjustes(simulacion);
    return origen;
  }

  window.manejarEdicionDelegadaHistorial = (evento) => {
    const control = evento.target.closest(
      ".history-input-cuotas, .history-input-salario",
    );
    if (!control) return;

    const fila = control.closest("tr");
    if (!fila) return;

    actualizarOrigenHistorialDesdeControl(control, fila);

    if (typeof actualizarEstadoFila === "function") {
      actualizarEstadoFila(fila);
    }
    if (typeof invalidarHistorial === "function") {
      invalidarHistorial();
    }
  };

  /*
   * Ficha Digital confirmada: los controles importados se mantienen
   * editables. Desmarcar una cuota detectada excluye el período completo de
   * la simulación, pero conserva sus valores originales como referencia.
   */
  window.marcarCampoDetalleImportado = (control, mes, campo) => {
    if (!control) return;

    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    const origenMes = (
      simulacion.origen_campos_detalle_anio_actual?.[String(mes)] || {}
    );
    const origen = origenMes[campo] || (
      control.type === "checkbox"
        ? origenMes.salario_mensual || origenMes.estado || null
        : null
    );

    if (!origen) {
      if (typeof marcarCampoDetalleImportadoBase === "function") {
        // El control manual conserva el comportamiento existente.
        return;
      }
      return;
    }

    control.readOnly = false;
    control.disabled = false;
    control.removeAttribute("aria-readonly");
    control.removeAttribute("disabled");
    control.removeAttribute("data-imported-locked");
    delete control.dataset.importedLocked;
    control.dataset.importedOriginally = "true";
    control.dataset.importedField = campo;
    control.dataset.importedMonth = String(mes);
    control.classList.add("detail-field-imported", "detail-field-imported-editable");

    if (control.type === "checkbox") {
      control.title = (
        "Dato detectado desde Ficha Digital. "
        + "Desmarca para excluir este período de la simulación; "
        + "el documento original se conservará como referencia."
      );
    } else {
      control.title = (
        "Dato detectado desde Ficha Digital. "
        + "Puedes editarlo y la aplicación identificará el ajuste."
      );
    }
  };

  function actualizarOrigenDetalleDesdeControl(control, fila) {
    const mes = Number(fila?.dataset.mes || 0);
    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    const anio = Number(
      simulacion.detalle_anio_actual?.anio
      || simulacion.ficha_digital_importada?.anio_mas_reciente
      || ANIO_ACTUAL,
    );
    const original = registroFichaOriginal(simulacion, anio, mes);

    if (!mes || !original) return;

    if (!simulacion.origen_campos_detalle_anio_actual[String(mes)]) {
      simulacion.origen_campos_detalle_anio_actual[String(mes)] = {};
    }

    const origenMes = simulacion.origen_campos_detalle_anio_actual[String(mes)];
    const clavePeriodo = clavePeriodoFicha(anio, mes);

    if (control.classList.contains("detalle-cuota-acreditada")) {
      const excluido = !control.checked;
      simulacion.periodos_excluidos_importacion_ficha = actualizarLista(
        simulacion.periodos_excluidos_importacion_ficha,
        clavePeriodo,
        excluido,
      );
      origenMes.cuota_acreditada = excluido
        ? "FICHA_DIGITAL_EXCLUIDO"
        : "FICHA_DIGITAL_DETECTADO";

      const clave = `ficha:${anio}:${mes}:cuota`;
      simulacion.campos_editados_importacion_ficha = actualizarLista(
        simulacion.campos_editados_importacion_ficha,
        clave,
        excluido,
      );

    } else if (control.classList.contains("detalle-salario-input")) {
      const igual = valoresIguales(
        control.value,
        original.salario,
        true,
      );
      origenMes.salario_mensual = igual
        ? "FICHA_DIGITAL_DETECTADO"
        : "FICHA_DIGITAL_EDITADO";

      simulacion.campos_editados_importacion_ficha = actualizarLista(
        simulacion.campos_editados_importacion_ficha,
        `ficha:${anio}:${mes}:salario`,
        !igual,
      );

    } else if (control.classList.contains("detalle-estado-salario")) {
      const igual = textoComparable(control.value) === textoComparable(
        original.estado || "COMPLETO",
      );
      origenMes.estado = igual
        ? "FICHA_DIGITAL_DETECTADO"
        : "FICHA_DIGITAL_EDITADO";

      simulacion.campos_editados_importacion_ficha = actualizarLista(
        simulacion.campos_editados_importacion_ficha,
        `ficha:${anio}:${mes}:estado`,
        !igual,
      );

    }

    invalidarResultadosDependientes(simulacion);
    guardarSimulacion(simulacion);
    actualizarAvisosAjustes(simulacion);
  }

  window.actualizarProcedenciaFilaDetalle = (fila) => {
    if (!fila) return;
    const mes = Number(fila.dataset.mes || 0);
    const etiqueta = fila.querySelector(".detail-row-provenance");
    if (!etiqueta || !mes) return;

    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    const anio = Number(
      simulacion.detalle_anio_actual?.anio
      || simulacion.ficha_digital_importada?.anio_mas_reciente
      || ANIO_ACTUAL,
    );
    const origenMes = (
      simulacion.origen_campos_detalle_anio_actual?.[String(mes)] || {}
    );
    const origenes = Object.values(origenMes).filter(Boolean);
    const excluido = periodoExcluido(simulacion, anio, mes)
      || origenes.some((origen) => String(origen).includes("EXCLUIDO"));
    const editado = origenes.some(
      (origen) => String(origen).includes("EDITADO"),
    );
    const importado = origenes.some(
      (origen) => String(origen).startsWith("FICHA_DIGITAL"),
    );

    let codigo = "NO_DETECTADO";
    if (excluido) {
      codigo = "EXCLUIDO_USUARIO";
    } else if (editado) {
      codigo = "EDITADO_USUARIO";
    } else if (importado) {
      codigo = "DETECTADO";
    } else if (typeof actualizarProcedenciaFilaDetalleBase === "function") {
      const check = fila.querySelector(".detalle-cuota-acreditada");
      const salario = fila.querySelector(
        ".detalle-col-mensual .detalle-salario-input",
      );
      const estado = fila.querySelector(".detalle-estado-salario");
      if (
        check?.checked
        || salario?.value.trim()
        || (estado?.value && estado.value !== "SIN_INFORMACION")
      ) {
        codigo = "COMPLETADO_MANUAL";
      }
    }

    etiqueta.textContent = window.textoProcedenciaDato(codigo);
    etiqueta.className = (
      `data-provenance-badge detail-row-provenance ${
        window.claseProcedenciaDato(codigo)
      }`
    );
    fila.dataset.provenance = codigo;
    fila.classList.toggle("detail-row-excluded", codigo === "EXCLUIDO_USUARIO");
  };

  window.actualizarEstadoFilaDetalle = (fila) => {
    if (typeof actualizarEstadoFilaDetalleBase === "function") {
      actualizarEstadoFilaDetalleBase(fila);
    }

    const mes = Number(fila?.dataset.mes || 0);
    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    const anio = Number(
      simulacion.detalle_anio_actual?.anio
      || simulacion.ficha_digital_importada?.anio_mas_reciente
      || ANIO_ACTUAL,
    );

    if (periodoExcluido(simulacion, anio, mes)) {
      const total = fila.querySelector(".detalle-total-mes");
      if (total) total.textContent = "B/.0.00";
      fila.classList.add("detail-row-excluded");
    } else {
      fila.classList.remove("detail-row-excluded");
    }
  };

  window.actualizarColumnasModoDetalle = () => {
    if (typeof actualizarColumnasModoDetalleBase === "function") {
      actualizarColumnasModoDetalleBase();
    }

    const modo = typeof obtenerModoDetalleAnioActual === "function"
      ? obtenerModoDetalleAnioActual()
      : "MENSUAL";

    document
      .querySelectorAll("#detalle-anio-actual-body tr")
      .forEach((fila) => {
        fila.querySelectorAll(".detalle-cuota-acreditada, .detalle-salario-input")
          .forEach((control) => {
            if (control.dataset.importedOriginally === "true") {
              control.disabled = false;
              control.readOnly = false;
            }
          });

        const estado = fila.querySelector(".detalle-estado-salario");
        if (
          estado?.dataset.importedOriginally === "true"
          && modo === "MENSUAL"
        ) {
          estado.disabled = false;
        }
      });
  };

  window.leerDetalleAnioActual = () => {
    const detalle = typeof leerDetalleAnioActualBase === "function"
      ? leerDetalleAnioActualBase()
      : null;

    if (!detalle) return detalle;

    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    detalle.registros = (detalle.registros || []).map((registro) => {
      if (!periodoExcluido(simulacion, detalle.anio, registro.mes)) {
        return registro;
      }

      return {
        ...registro,
        cuota_acreditada: false,
        estado: "SIN_INFORMACION",
        salario_mensual: null,
        primera_quincena: null,
        segunda_quincena: null,
      };
    });

    return detalle;
  };

  /*
   * En la vista previa de Ficha Digital la casilla detectada puede
   * desmarcarse durante "Editar campos". El lector existente utilizará su
   * valor real porque se retira importedLocked.
   */
  window.establecerEdicionPreviewFicha = (habilitada) => {
    if (typeof establecerEdicionPreviewFichaBase === "function") {
      establecerEdicionPreviewFichaBase(habilitada);
    }

    document
      .querySelectorAll("#modal-import-ficha-digital .preview-ficha-cuota")
      .forEach((control) => {
        const fila = control.closest("tr");
        const anio = Number(fila?.dataset.anio || ANIO_ACTUAL);
        const mes = Number(fila?.dataset.mes || 0);
        if (!control.dataset.provenanceKey) {
          control.dataset.provenanceKey = `ficha:${anio}:${mes}:cuota`;
        }
        if (!control.dataset.detectedOriginally) {
          control.dataset.detectedOriginally = (
            control.defaultChecked || control.checked
          ) ? "true" : "false";
        }
        control.removeAttribute("data-imported-locked");
        delete control.dataset.importedLocked;
        control.disabled = !habilitada;
      });
  };

  function actualizarProcedenciaPreviewFichaCheckbox(control) {
    if (
      !control?.classList.contains("preview-ficha-cuota")
      || typeof edicionPreviewFichaHabilitada === "undefined"
      || !edicionPreviewFichaHabilitada
    ) {
      return;
    }

    const fila = control.closest("tr");
    const etiqueta = fila?.querySelector(".data-provenance-badge");
    const clave = control.dataset.provenanceKey;

    if (typeof camposEditadosPreviewFicha !== "undefined" && clave) {
      if (control.checked) camposEditadosPreviewFicha.delete(clave);
      else camposEditadosPreviewFicha.add(clave);
    }

    if (typeof previewFichaFueEditado !== "undefined") {
      previewFichaFueEditado = (
        typeof camposEditadosPreviewFicha !== "undefined"
        && camposEditadosPreviewFicha.size > 0
      );
    }

    if (etiqueta) {
      etiqueta.textContent = control.checked
        ? "Detectado"
        : "Excluido por ti";
      etiqueta.className = (
        `data-provenance-badge ${
          control.checked ? "detected" : "excluded"
        }`
      );
    }
  }

  /*
   * La confirmación guarda una fotografía inmutable adicional. La referencia
   * vigente puede contener ajustes, pero la original queda disponible para
   * comparar, revertir procedencia y explicar diferencias.
   */
  if (typeof confirmarComprobanteImportacionBase === "function") {
    window.confirmarComprobanteImportacion = (...args) => {
      const original = (
        typeof borradorImportacionComprobante !== "undefined"
        && borradorImportacionComprobante
      )
        ? structuredClone(borradorImportacionComprobante)
        : null;

      const resultado = confirmarComprobanteImportacionBase(...args);
      const simulacion = asegurarEstructuraProcedencia(obtenerSimulacion());
      if (original) {
        simulacion.referencia_mi_retiro_seguro_original = original;
      }
      guardarSimulacion(simulacion);
      window.bloquearFormularioPersonal(false, simulacion);
      return resultado;
    };
  }

  if (typeof confirmarFichaDigitalImportacionBase === "function") {
    window.confirmarFichaDigitalImportacion = async (...args) => {
      const original = (
        typeof borradorImportacionFichaDigital !== "undefined"
        && borradorImportacionFichaDigital
      )
        ? structuredClone(borradorImportacionFichaDigital)
        : null;

      const resultado = await confirmarFichaDigitalImportacionBase(...args);
      const simulacion = asegurarEstructuraProcedencia(obtenerSimulacion());

      if (original) {
        simulacion.ficha_digital_importada_original = original;
      }

      const actuales = simulacion.ficha_digital_importada?.registros || [];
      actuales.forEach((registro) => {
        if (registro.cuota_acreditada !== false) return;
        const clave = clavePeriodoFicha(registro.anio, registro.mes);
        simulacion.periodos_excluidos_importacion_ficha = actualizarLista(
          simulacion.periodos_excluidos_importacion_ficha,
          clave,
          true,
        );
        const origenMes = (
          simulacion.origen_campos_detalle_anio_actual[
            String(registro.mes)
          ] || {}
        );
        origenMes.cuota_acreditada = "FICHA_DIGITAL_EXCLUIDO";
        simulacion.origen_campos_detalle_anio_actual[
          String(registro.mes)
        ] = origenMes;
      });

      guardarSimulacion(simulacion);
      return resultado;
    };
  }

  if (typeof quitarComprobanteImportacionBase === "function") {
    window.quitarComprobanteImportacion = (...args) => {
      const resultado = quitarComprobanteImportacionBase(...args);
      const simulacion = obtenerSimulacion();
      simulacion.referencia_mi_retiro_seguro_original = null;
      guardarSimulacion(simulacion);
      return resultado;
    };
  }

  if (typeof quitarFichaDigitalImportacionBase === "function") {
    window.quitarFichaDigitalImportacion = (...args) => {
      const resultado = quitarFichaDigitalImportacionBase(...args);
      const simulacion = obtenerSimulacion();
      simulacion.ficha_digital_importada_original = null;
      simulacion.periodos_excluidos_importacion_ficha = [];
      guardarSimulacion(simulacion);
      return resultado;
    };
  }

  function restaurarValoresVisualesExcluidos() {
    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    const detalle = simulacion.detalle_anio_actual || {};
    const anio = Number(
      detalle.anio
      || simulacion.ficha_digital_importada?.anio_mas_reciente
      || ANIO_ACTUAL,
    );

    document
      .querySelectorAll("#detalle-anio-actual-body tr")
      .forEach((fila) => {
        const mes = Number(fila.dataset.mes || 0);
        if (!periodoExcluido(simulacion, anio, mes)) return;

        const original = registroFichaOriginal(simulacion, anio, mes);
        if (!original) return;

        const check = fila.querySelector(".detalle-cuota-acreditada");
        const salario = fila.querySelector(
          ".detalle-col-mensual .detalle-salario-input",
        );
        const estado = fila.querySelector(".detalle-estado-salario");

        if (check) check.checked = false;
        if (
          salario
          && typeof formatearNumeroMonetario === "function"
        ) {
          salario.value = formatearNumeroMonetario(original.salario);
        }
        if (estado) estado.value = original.estado || "COMPLETO";

        window.actualizarEstadoFilaDetalle(fila);
        window.actualizarProcedenciaFilaDetalle(fila);
      });
  }

  function origenRepresentaAjuste(origen) {
    const valor = String(origen || "");
    return (
      valor.includes("EDITADO")
      || valor.includes("COMPLETADO_MANUAL")
      || valor.includes("EXCLUIDO")
    );
  }

  function actualizarAvisosAjustes(
    simulacion = preservarReferenciasOriginales(obtenerSimulacion()),
  ) {
    const personaActiva = Object.values(
      simulacion.origen_campos_persona || {},
    ).some(origenRepresentaAjuste);

    const cuotasActivas = Object.values(
      simulacion.origen_campos_cuotas || {},
    ).some(origenRepresentaAjuste);

    const historialActivo = Object.values(
      simulacion.origen_campos_historial || {},
    ).some((campos) => Object.values(campos || {}).some(
      origenRepresentaAjuste,
    ));

    const fichaActiva = (
      (simulacion.periodos_excluidos_importacion_ficha || []).length > 0
      || Object.values(
        simulacion.origen_campos_detalle_anio_actual || {},
      ).some((campos) => Object.values(campos || {}).some(
        origenRepresentaAjuste,
      ))
    );

    actualizarAviso(
      "aviso-ajustes-datos-personales",
      document.getElementById("form-datos-personales"),
      personaActiva,
    );
    actualizarAviso(
      "aviso-ajustes-cuotas",
      document.getElementById("cuotas-importadas-acciones"),
      cuotasActivas,
    );
    actualizarAviso(
      "aviso-ajustes-historial",
      document.getElementById("historial-importado-acciones"),
      historialActivo,
    );
    actualizarAviso(
      "aviso-ajustes-ficha",
      document.getElementById("acciones-ficha-digital-importada"),
      fichaActiva,
    );
  }

  function prepararControlesImportadosEditables() {
    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    guardarSimulacion(simulacion);

    window.bloquearFormularioPersonal(false, simulacion);
    window.actualizarOrigenCamposCuotas(simulacion);

    document
      .querySelectorAll("#historial-tabla-body tr")
      .forEach((fila) => {
        const anio = Number(fila.dataset.anio || 0);
        window.aplicarOrigenCampoHistorial(
          fila.querySelector(".history-input-cuotas"),
          anio,
          "cuotas",
        );
        window.aplicarOrigenCampoHistorial(
          fila.querySelector(".history-input-salario"),
          anio,
          "salario_cotizado",
        );
      });

    document
      .querySelectorAll("#detalle-anio-actual-body tr")
      .forEach((fila) => {
        const mes = Number(fila.dataset.mes || 0);
        const check = fila.querySelector(".detalle-cuota-acreditada");
        const salario = fila.querySelector(
          ".detalle-col-mensual .detalle-salario-input",
        );
        const estado = fila.querySelector(".detalle-estado-salario");

        window.marcarCampoDetalleImportado(
          check,
          mes,
          "cuota_acreditada",
        );
        window.marcarCampoDetalleImportado(
          salario,
          mes,
          "salario_mensual",
        );
        window.marcarCampoDetalleImportado(
          estado,
          mes,
          "estado",
        );

        window.actualizarProcedenciaFilaDetalle(fila);
      });

    window.actualizarColumnasModoDetalle();
    restaurarValoresVisualesExcluidos();
    actualizarAvisosAjustes(simulacion);
  }

  document.addEventListener(
    "input",
    (evento) => {
      const personal = evento.target.closest("#bloque-datos-personales input");
      if (personal) {
        actualizarProcedenciaPersonalDesdeControl(personal);
      }

      const cuota = evento.target.closest(
        "#cuotas_totales, #cuotas_anio_actual",
      );
      if (cuota) {
        actualizarProcedenciaCuotasDesdeControl(cuota);
      }

      const detalle = evento.target.closest(
        "#detalle-anio-actual-body .detalle-salario-input",
      );
      if (detalle) {
        actualizarOrigenDetalleDesdeControl(detalle, detalle.closest("tr"));
        queueMicrotask(() => {
          window.actualizarProcedenciaFilaDetalle(detalle.closest("tr"));
        });
      }
    },
    true,
  );

  document.addEventListener(
    "change",
    (evento) => {
      const personal = evento.target.closest(
        "#bloque-datos-personales input, #bloque-datos-personales select",
      );
      if (personal) {
        actualizarProcedenciaPersonalDesdeControl(personal);
      }

      const cuota = evento.target.closest(
        "#cuotas_totales, #cuotas_anio_actual",
      );
      if (cuota) {
        actualizarProcedenciaCuotasDesdeControl(cuota);
      }

      const detalle = evento.target.closest(
        "#detalle-anio-actual-body .detalle-cuota-acreditada, "
        + "#detalle-anio-actual-body .detalle-estado-salario, "
        + "#detalle-anio-actual-body .detalle-salario-input",
      );
      if (detalle) {
        actualizarOrigenDetalleDesdeControl(detalle, detalle.closest("tr"));
        queueMicrotask(() => {
          const fila = detalle.closest("tr");
          window.actualizarEstadoFilaDetalle(fila);
          window.actualizarProcedenciaFilaDetalle(fila);
          if (
            detalle.classList.contains("detalle-cuota-acreditada")
            && typeof sincronizarCuotasPaso2DesdeDetalle === "function"
          ) {
            sincronizarCuotasPaso2DesdeDetalle({
              fuente: "DETALLE_MANUAL",
            });
          }
        });
      }

      const previewFicha = evento.target.closest(
        "#modal-import-ficha-digital .preview-ficha-cuota",
      );
      if (previewFicha) {
        actualizarProcedenciaPreviewFichaCheckbox(previewFicha);
      }
    },
    true,
  );

  const observador = new MutationObserver((mutaciones) => {
    const hayFilasNuevas = mutaciones.some((mutacion) => (
      Array.from(mutacion.addedNodes || []).some((nodo) => (
        nodo.nodeType === Node.ELEMENT_NODE
        && nodo.matches?.("tr")
      ))
    ));

    if (!hayFilasNuevas) return;

    queueMicrotask(() => {
      prepararControlesImportadosEditables();
    });
  });

  document.addEventListener("DOMContentLoaded", () => {
    const simulacion = preservarReferenciasOriginales(obtenerSimulacion());
    guardarSimulacion(simulacion);

    prepararControlesImportadosEditables();

    [
      document.getElementById("historial-tabla-body"),
      document.getElementById("detalle-anio-actual-body"),
      document.getElementById("preview-ficha-digital-registros"),
    ].filter(Boolean).forEach((elemento) => {
      observador.observe(elemento, {
        childList: true,
        subtree: false,
      });
    });
  });
})();
