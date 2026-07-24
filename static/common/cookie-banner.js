(function () {
  "use strict";

  var STORAGE_KEY = "nk_cookie_consent";

  function getBanner() {
    return document.querySelector(".nk-cookie-banner");
  }

  function hideBanner() {
    var banner = getBanner();
    if (!banner) {
      return;
    }
    banner.style.display = "none";
  }

  function showBanner() {
    var banner = getBanner();
    if (!banner) {
      return;
    }
    banner.style.display = "block";
  }

  window.nk_hideCookieBanner = function () {
    try {
      window.localStorage.setItem(STORAGE_KEY, "1");
    } catch (err) {
      // Ignore storage errors and still hide the banner for this page view.
    }
    hideBanner();
  };

  document.addEventListener("DOMContentLoaded", function () {
    var accepted = "0";
    try {
      accepted = window.localStorage.getItem(STORAGE_KEY) || "0";
    } catch (err) {
      accepted = "0";
    }

    if (accepted === "1") {
      hideBanner();
    } else {
      showBanner();
    }
  });
})();
