"use strict";
// Contact button enhancement: copy the address to the clipboard on click and
// show a brief confirmation, while still letting the mailto: navigation run.
// If the clipboard API is unavailable (http, old browser), do nothing extra.
(function () {
  var ADDR = "hello@aigatewaylab.xyz";
  var zh = document.documentElement.lang &&
           document.documentElement.lang.indexOf("zh") === 0;
  var MSG = zh ? "已复制邮箱地址" : "address copied";

  function flash(msg) {
    var hints = document.querySelectorAll(".copy-hint");
    for (var i = 0; i < hints.length; i++) {
      hints[i].textContent = msg;
    }
    if (hints.length) {
      window.setTimeout(function () {
        for (var j = 0; j < hints.length; j++) hints[j].textContent = "";
      }, 2500);
    }
  }

  function onClick() {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return;
    navigator.clipboard.writeText(ADDR).then(function () {
      flash(MSG);
    }, function () { /* clipboard refused; mailto still proceeds */ });
  }

  var links = document.querySelectorAll("a.contact-mail");
  for (var i = 0; i < links.length; i++) {
    links[i].addEventListener("click", onClick);
  }
})();
