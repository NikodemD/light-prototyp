(function () {
  var root = document.documentElement;
  var font = localStorage.getItem("light-font") || "0";
  var contrast = localStorage.getItem("light-contrast") === "1";

  function applyFont(value) {
    font = value;
    if (value === "0") delete root.dataset.font;
    else root.dataset.font = value;
    document.querySelectorAll("[data-font]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.getAttribute("data-font") === value ? "true" : "false");
    });
  }

  function applyContrast(on) {
    contrast = on;
    root.classList.toggle("contrast", on);
    var btn = document.querySelector("[data-contrast]");
    if (btn) btn.setAttribute("aria-pressed", on ? "true" : "false");
  }

  applyFont(font);
  applyContrast(contrast);

  document.querySelectorAll("[data-font]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var value = btn.getAttribute("data-font");
      localStorage.setItem("light-font", value);
      applyFont(value);
    });
  });

  var contrastBtn = document.querySelector("[data-contrast]");
  if (contrastBtn) {
    contrastBtn.addEventListener("click", function () {
      var on = !contrast;
      localStorage.setItem("light-contrast", on ? "1" : "0");
      applyContrast(on);
    });
  }

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  document.querySelectorAll("[data-filter]").forEach(function (bar) {
    var target = document.querySelector(bar.getAttribute("data-filter"));
    if (!target) return;
    bar.querySelectorAll("button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var cat = btn.getAttribute("data-cat");
        bar.querySelectorAll("button").forEach(function (b) {
          b.setAttribute("aria-pressed", b === btn ? "true" : "false");
        });
        target.querySelectorAll("[data-cat]").forEach(function (item) {
          var show = cat === "all" || item.getAttribute("data-cat").split(" ").indexOf(cat) !== -1;
          item.hidden = !show;
        });
      });
    });
  });

  var searchPage = document.querySelector("[data-search-page]");
  if (searchPage && window.LIGHT_INDEX) {
    var params = new URLSearchParams(location.search);
    var q = (params.get("q") || "").trim();
    var input = document.querySelector(".search input, [data-search-input]");
    if (input) input.value = q;
    var out = searchPage.querySelector("[data-results]");
    var prefix = document.body.getAttribute("data-root") || "";
    var lang = document.documentElement.lang || "pl";
    var words = q.toLowerCase().split(/\s+/).filter(Boolean);
    var hits = window.LIGHT_INDEX.filter(function (item) {
      if (item.lang !== lang) return false;
      if (!words.length) return false;
      var hay = (item.title + " " + item.text).toLowerCase();
      return words.every(function (w) { return hay.indexOf(w) !== -1; });
    });
    var empty = lang === "en"
      ? "No pages match this search."
      : "Brak stron pasujących do tego wyszukiwania.";
    var prompt = lang === "en" ? "Type a word and search again." : "Wpisz słowo i wyszukaj ponownie.";
    if (!q) {
      out.innerHTML = "<p>" + prompt + "</p>";
    } else if (!hits.length) {
      out.innerHTML = "<p>" + empty + "</p>";
    } else {
      out.innerHTML = hits.map(function (item) {
        return '<a class="search-hit" href="' + prefix + item.url + '"><strong>' + item.title + '</strong><span>' + item.text + '</span></a>';
      }).join("");
    }
  }
})();
