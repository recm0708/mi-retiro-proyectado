"use strict";

/*
 * Mi Retiro Proyectado — presentación compartida de fecha y hora.
 *
 * Propósito: mostrar timestamps operativos en un formato local legible.
 * Alcance: App y Portal Developer; no transforma fechas previsionales sin hora.
 */
(() => {
  const SELECTOR = "[data-app-local-datetime]";

  const formateador = new Intl.DateTimeFormat(
    "es-PA",
    {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: true,
    },
  );

  function obtenerParte(partes, tipo) {
    return (
      partes.find(
        (parte) => parte.type === tipo,
      )?.value
      || ""
    );
  }

  function normalizarPeriodo(valor) {
    return String(valor || "")
      .replace(/\s+/g, " ")
      .trim()
      .toLocaleLowerCase("es-PA");
  }

  function formatearFechaHora(elemento) {
    const valor = elemento.getAttribute(
      "datetime",
    );

    if (!valor) {
      return;
    }

    const fecha = new Date(valor);

    if (Number.isNaN(fecha.getTime())) {
      elemento.textContent = "Fecha no disponible";
      return;
    }

    const partes = formateador.formatToParts(
      fecha,
    );

    const dia = obtenerParte(partes, "day");
    const mes = obtenerParte(partes, "month");
    const anio = obtenerParte(partes, "year");
    const hora = obtenerParte(partes, "hour");
    const minuto = obtenerParte(partes, "minute");
    const segundo = obtenerParte(partes, "second");
    const periodo = normalizarPeriodo(
      obtenerParte(partes, "dayPeriod"),
    );

    elemento.textContent = (
      `${dia}/${mes}/${anio} · `
      + `${hora}:${minuto}:${segundo}`
      + (periodo ? ` ${periodo}` : "")
    );

    const zona = (
      Intl.DateTimeFormat()
        .resolvedOptions()
        .timeZone
      || "zona local"
    );

    elemento.title = (
      `Hora local del navegador · ${zona}`
    );
  }

  function iniciarFechasLocales() {
    document
      .querySelectorAll(SELECTOR)
      .forEach(formatearFechaHora);
  }

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      iniciarFechasLocales,
    );
  } else {
    iniciarFechasLocales();
  }
})();
