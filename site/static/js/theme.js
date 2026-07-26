/* Theme bootstrap — runs synchronously in <head> to prevent FOUC.
 * External file (CSP: script-src 'self'; no inline scripts).
 * Modes: system (default) | light | dark  → data-theme on <html>
 * Surfaces: frost (default) | graphite | midnight → data-surface
 * Persisted in localStorage (agl-theme / agl-surface). */
(function () {
  "use strict";
  var root = document.documentElement;
  root.className = root.className.replace(/\bno-js\b/, "js");
  var theme, surface;
  try {
    theme = localStorage.getItem("agl-theme");
    surface = localStorage.getItem("agl-surface");
  } catch (e) { /* storage blocked -> system defaults */ }
  if (theme === "light" || theme === "dark") root.setAttribute("data-theme", theme);
  if (surface === "graphite" || surface === "midnight") root.setAttribute("data-surface", surface);
})();
