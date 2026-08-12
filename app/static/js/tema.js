/**
 * Gestión de apariencia de Mi Retiro Proyectado.
 *
 * La preferencia se conserva únicamente en el navegador mediante
 * localStorage. No forma parte de los datos de la simulación.
 */
(() => {
  "use strict";

  const STORAGE_KEY = "mi-retiro-proyectado-tema";
  const VALID_THEMES = new Set(["system", "light", "dark", "contrast"]);
  const mediaDark = window.matchMedia("(prefers-color-scheme: dark)");

  function readPreference() {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      return VALID_THEMES.has(saved) ? saved : "system";
    } catch {
      return "system";
    }
  }

  function resolveBootstrapTheme(preference) {
    if (preference === "contrast") {
      return "dark";
    }

    if (preference === "system") {
      return mediaDark.matches ? "dark" : "light";
    }

    return preference;
  }

  function applyTheme(preference) {
    const normalized = VALID_THEMES.has(preference)
      ? preference
      : "system";

    const bootstrapTheme = resolveBootstrapTheme(normalized);
    const root = document.documentElement;

    root.setAttribute("data-app-theme", normalized);
    root.setAttribute("data-bs-theme", bootstrapTheme);
    root.style.colorScheme = bootstrapTheme;

    return normalized;
  }

  function savePreference(preference) {
    try {
      window.localStorage.setItem(STORAGE_KEY, preference);
    } catch {
      // La aplicación sigue funcionando aunque el navegador bloquee storage.
    }
  }

  const initialPreference = applyTheme(readPreference());

  document.addEventListener("DOMContentLoaded", () => {
    const selector = document.getElementById("selector-tema");

    if (!selector) {
      return;
    }

    selector.value = initialPreference;

    selector.addEventListener("change", () => {
      const preference = applyTheme(selector.value);
      selector.value = preference;
      savePreference(preference);
    });
  });

  mediaDark.addEventListener("change", () => {
    if (readPreference() === "system") {
      applyTheme("system");
    }
  });
})();
