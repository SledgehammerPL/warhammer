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
    banner.hidden = true;
    banner.style.display = "none";
  }

  function showBanner() {
    var banner = getBanner();
    if (!banner) {
      return;
    }
    banner.hidden = false;
    banner.style.display = "";
  }

  function hasConsent() {
    try {
      return window.localStorage.getItem(STORAGE_KEY) === "1";
    } catch (err) {
      return false;
    }
  }

  window.nk_hideCookieBanner = function () {
    try {
      window.localStorage.setItem(STORAGE_KEY, "1");
    } catch (err) {
      // Ignore storage errors and still hide the banner for this page view.
    }
    hideBanner();
  };

  function init() {
    if (hasConsent()) {
      hideBanner();
    } else {
      showBanner();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
