/* Theme controls — cycle mode button + surface select in nav.
 * External file; runs after DOM (script at body end). */
(function () {
  "use strict";
  var root = document.documentElement;
  var MODES = ["system", "light", "dark"];
  var ICONS = { system: "\u25D1", light: "\u2600", dark: "\u263E" };

  function getMode() {
    var t = root.getAttribute("data-theme");
    return t === "light" || t === "dark" ? t : "system";
  }
  function setMode(m) {
    if (m === "system") {
      root.removeAttribute("data-theme");
      try { localStorage.removeItem("agl-theme"); } catch (e) {}
    } else {
      root.setAttribute("data-theme", m);
      try { localStorage.setItem("agl-theme", m); } catch (e) {}
    }
    paint();
  }
  function getSurface() {
    return root.getAttribute("data-surface") || "frost";
  }
  function setSurface(s) {
    if (s === "frost") {
      root.removeAttribute("data-surface");
      try { localStorage.removeItem("agl-surface"); } catch (e) {}
    } else {
      root.setAttribute("data-surface", s);
      try { localStorage.setItem("agl-surface", s); } catch (e) {}
    }
  }

  var btn = document.getElementById("theme-mode");
  var sel = document.getElementById("theme-surface");
  if (!btn || !sel) return;

  function paint() {
    var m = getMode();
    btn.textContent = ICONS[m] + " " + m;
    btn.setAttribute("aria-label", "Theme: " + m + ". Activate to switch.");
  }
  btn.addEventListener("click", function () {
    var next = MODES[(MODES.indexOf(getMode()) + 1) % MODES.length];
    setMode(next);
  });
  sel.value = getSurface();
  sel.addEventListener("change", function () { setSurface(sel.value); });
  paint();
})();
