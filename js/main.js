/* =========================================================
   Silver Star Plumbing — site runtime
   Renders header, footer, service grids, service detail
   blocks, service areas and trust badges from js/config.js.
   Nothing on the page is hard-coded business data.
   ========================================================= */

(function () {
  "use strict";

  var C = window.SSP;
  if (!C) { console.error("SSP config missing — js/config.js must load first."); return; }
  var B = C.business;

  /* ---------- icons ---------- */
  var ICON = {
    phone: '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.7.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.7.1.4 0 .7-.2 1l-2.3 2.1z"/>',
    check: '<path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/>',
    msg: '<path d="M20 2H4a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2z"/>',
    pin: '<path d="M12 2a7 7 0 0 0-7 7c0 5.3 7 13 7 13s7-7.7 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>',
    clock: '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 10.4V6h-2v7.4l5.1 3.1 1-1.7z"/>',
    shield: '<path d="M12 1 3 5v6c0 5.5 3.8 10.7 9 12 5.2-1.3 9-6.5 9-12V5l-9-4zm-1.2 15-3.5-3.5 1.4-1.4 2.1 2.1 5-5 1.4 1.4z"/>',
    menu: '<path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/>',
    close: '<path d="m19 6.4-1.4-1.4-5.6 5.6L6.4 5 5 6.4l5.6 5.6L5 17.6 6.4 19l5.6-5.6 5.6 5.6 1.4-1.4-5.6-5.6z"/>',
    star: '<path d="m12 17.3 6.2 3.7-1.6-7 5.4-4.7-7.1-.6L12 2 9.1 8.7 2 9.3l5.4 4.7-1.6 7z"/>',
    mail: '<path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5z"/>',
    caret: '<path d="M7 10l5 5 5-5z"/>',
    up: '<path d="m12 8-6 6 1.4 1.4L12 10.8l4.6 4.6L18 14z"/>'
  };

  function svg(name, cls) {
    return '<svg viewBox="0 0 24 24" aria-hidden="true"' + (cls ? ' class="' + cls + '"' : '') + '>' + ICON[name] + "</svg>";
  }
  function el(id) { return document.getElementById(id); }

  /* Single-file build (tools/build_sample.py) swaps image paths for inlined
     data URIs and turns cross-page links into in-page anchors. On the real
     multi-page site both of these are pass-throughs. */
  function art(path) {
    return (window.SSP_ART && window.SSP_ART[path]) || path;
  }
  var SINGLE = !!window.SSP_SINGLE;
  function page(href, anchor) { return SINGLE ? "#" + anchor : href; }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  var telHref = "tel:" + B.phoneRaw;
  var smsHref = "sms:" + B.phoneRaw;

  /* ---------- trust points (only what config confirms) ---------- */
  function trustPoints() {
    var out = [];
    if (B.owner) out.push("Owner-operated — you deal with " + B.owner.split(" ")[0] + ", not a call center");
    if (B.license) out.push("CSLB Lic. #" + B.license);
    if (B.insured) out.push("Licensed and insured");
    if (B.yearsInBusiness) out.push(B.yearsInBusiness + "+ years in the trade");
    if (B.emergency24) out.push("24/7 emergency service");
    out.push("Straight pricing, explained before the work starts");
    return out;
  }

  /* ---------- header ---------- */
  var NAV = [
    { href: "index.html", anchor: "top", label: "Home" },
    { href: "services.html", anchor: "services", label: "Services" },
    { href: "areas.html", anchor: "areas", label: "Service Area" },
    { href: "about.html", anchor: "about", label: "About" },
    { href: "contact.html", anchor: "contact", label: "Contact" }
  ];

  function renderHeader() {
    var mount = el("site-header");
    if (!mount) return;
    var active = SINGLE ? "" : (location.pathname.split("/").pop() || "index.html");
    var links = NAV.map(function (n) {
      var a = '<a href="' + page(n.href, n.anchor) + '"' +
        (n.href === active ? ' class="active" aria-current="page"' : "") + ">" + n.label + "</a>";
      if (n.href !== "services.html") return a;

      /* Services gets a dropdown of every service, so a customer is never
         more than one tap from the thing they actually came here for. */
      var items = C.services.map(function (s) {
        return '<a href="' + page("services.html#" + s.id, s.id) + '">' + esc(s.name) + "</a>";
      }).join("");
      return '<span class="nav-item">' + a +
        '<button class="nav-caret" aria-label="Show all services" aria-expanded="false">' +
        svg("caret") + "</button>" +
        '<span class="mega">' + items + "</span></span>";
    }).join("");

    mount.innerHTML =
      '<div class="header-inner">' +
        '<a class="brand" href="' + page("index.html", "top") + '">' +
          '<img src="' + art("img/logo.svg") + '" alt="' + esc(B.name) + ' logo" width="44" height="44">' +
          '<span class="brand-text">' +
            '<span class="brand-name">Silver Star</span><br>' +
            '<span class="brand-sub">Plumbing</span>' +
          "</span>" +
        "</a>" +
        '<nav class="nav" id="nav" aria-label="Main">' + links + "</nav>" +
        '<div class="header-cta">' +
          '<a class="header-phone" href="' + telHref + '">' + svg("phone") + "<span>" + esc(B.phone) + "</span></a>" +
          '<button class="nav-toggle" id="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav">' + svg("menu") + "</button>" +
        "</div>" +
      "</div>";

    var btn = el("nav-toggle"), nav = el("nav");
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", String(open));
      btn.innerHTML = svg(open ? "close" : "menu");
    });

    var caret = nav.querySelector(".nav-caret");
    if (caret) {
      var item = caret.parentNode;
      caret.addEventListener("click", function (e) {
        e.preventDefault();
        var open = item.classList.toggle("open");
        caret.setAttribute("aria-expanded", String(open));
      });
      document.addEventListener("click", function (e) {
        if (!item.contains(e.target)) {
          item.classList.remove("open");
          caret.setAttribute("aria-expanded", "false");
        }
      });
      nav.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
          item.classList.remove("open");
          caret.setAttribute("aria-expanded", "false");
        }
      });
    }
  }

  /* ---------- in-page jump bar with scroll-spy (services page) ---------- */
  function renderJumpBar() {
    var mount = el("svc-jump");
    if (!mount) return;
    mount.innerHTML = C.services.map(function (s) {
      return '<a href="#' + s.id + '" data-jump="' + s.id + '">' + esc(s.name) + "</a>";
    }).join("");

    var links = {};
    Array.prototype.forEach.call(mount.querySelectorAll("[data-jump]"), function (a) {
      links[a.getAttribute("data-jump")] = a;
    });
    if (!("IntersectionObserver" in window)) return;

    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = en.target.id;
        if (id === current || !links[id]) return;
        if (current && links[current]) links[current].classList.remove("active");
        links[id].classList.add("active");
        current = id;
        /* keep the active chip in view without scrolling the page */
        var a = links[id];
        mount.scrollTo({ left: a.offsetLeft - mount.clientWidth / 2 + a.clientWidth / 2, behavior: "smooth" });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });

    Array.prototype.forEach.call(document.querySelectorAll(".svc"), function (s) { io.observe(s); });
  }

  /* ---------- back to top ---------- */
  function renderToTop() {
    var b = document.createElement("button");
    b.className = "to-top";
    b.type = "button";
    b.setAttribute("aria-label", "Back to top");
    b.innerHTML = svg("up");
    b.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduceMotion() ? "auto" : "smooth" });
    });
    document.body.appendChild(b);
    var tick = function () { b.classList.toggle("show", window.scrollY > 700); };
    window.addEventListener("scroll", tick, { passive: true });
    tick();
  }

  function reduceMotion() {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  /* ---------- scroll reveal ---------- */
  function initReveal() {
    if (reduceMotion() || !("IntersectionObserver" in window)) return;
    var targets = document.querySelectorAll(
      "section .wrap > .grid, section .wrap > .chips, .svc, .faq-item, .owner-card");
    if (!targets.length) return;
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        obs.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    Array.prototype.forEach.call(targets, function (t) {
      t.classList.add("reveal");
      io.observe(t);
    });
  }

  /* ---------- footer ---------- */
  function renderFooter() {
    var mount = el("site-footer");
    if (!mount) return;

    var svcLinks = C.services.slice(0, 6).map(function (s) {
      return '<li><a href="' + page("services.html#" + s.id, s.id) + '">' + esc(s.name) + "</a></li>";
    }).join("");

    var areaLinks = C.areas.primary.map(function (a) {
      return "<li>" + esc(a) + "</li>";
    }).join("");

    var legal = [];
    if (B.license) legal.push("CSLB Lic. #" + esc(B.license));
    legal.push("&copy; " + new Date().getFullYear() + " " + esc(B.name));

    var contactBits = '<a class="footer-phone" href="' + telHref + '">' + esc(B.phone) + "</a>";
    if (B.email) contactBits += '<br><a href="mailto:' + esc(B.email) + '">' + esc(B.email) + "</a>";
    if (B.hours) contactBits += "<br>" + esc(B.hours);

    mount.innerHTML =
      '<div class="wrap">' +
        '<div class="footer-grid">' +
          "<div>" +
            "<h4>" + esc(B.name) + "</h4>" +
            "<p>Plumbing for East Contra Costa, the Bay Area and the Central Valley. " +
            "Owner-operated by " + esc(B.owner) + ".</p>" +
            "<p>" + contactBits + "</p>" +
          "</div>" +
          "<div><h4>Services</h4><ul>" + svcLinks +
            '<li><a href="' + page("services.html", "services") + '">All services →</a></li></ul></div>' +
          "<div><h4>Service Area</h4><ul>" + areaLinks +
            '<li><a href="' + page("areas.html", "areas") + '">Full list →</a></li></ul></div>' +
        "</div>" +
        '<div class="footer-bottom"><span>' + legal.join(" &nbsp;·&nbsp; ") + "</span>" +
        "<span>" + esc(B.domain) + "</span></div>" +
      "</div>";
  }

  /* ---------- sticky mobile call bar ---------- */
  function renderCallBar() {
    var mount = el("call-bar");
    if (!mount) return;
    mount.innerHTML =
      '<a class="c1" href="' + telHref + '">' + svg("phone") + "Call Now</a>" +
      '<a class="c2" href="' + smsHref + '">' + svg("msg") + "Text Us</a>";
  }

  /* ---------- service cards ---------- */
  function renderServiceGrid() {
    var mount = el("service-grid");
    if (!mount) return;
    var limit = parseInt(mount.getAttribute("data-limit"), 10);
    var list = isNaN(limit) ? C.services : C.services.slice(0, limit);

    mount.innerHTML = list.map(function (s) {
      var img = art(s.photo || s.art);
      return '<a class="card" href="' + page("services.html#" + s.id, s.id) + '">' +
        '<div class="card-art"><img src="' + img + '" alt="' + esc(s.name) + '" loading="lazy" width="800" height="600"></div>' +
        '<div class="card-body"><h3>' + esc(s.name) + "</h3><p>" + esc(s.short) + "</p>" +
        '<span class="card-link">Details</span></div></a>';
    }).join("");
  }

  /* ---------- service detail blocks ---------- */
  function renderServiceDetails() {
    var mount = el("service-detail");
    if (!mount) return;

    mount.innerHTML = C.services.map(function (s) {
      var img = art(s.photo || s.art);
      var lis = s.bullets.map(function (b) {
        return "<li>" + svg("check") + "<span>" + esc(b) + "</span></li>";
      }).join("");
      return '<article class="svc" id="' + s.id + '">' +
        '<div class="svc-art"><img src="' + img + '" alt="' + esc(s.name) + '" loading="lazy" width="800" height="600"></div>' +
        "<div><h2>" + esc(s.name) + "</h2><p class=\"lede\">" + esc(s.short) + "</p><ul>" + lis + "</ul>" +
        '<p style="margin-top:1.3rem"><a class="btn btn-call" href="' + telHref + '">' + svg("phone") +
        esc(B.phone) + "</a></p></div></article>";
    }).join("");
  }

  /* ---------- service areas ---------- */
  function renderAreas() {
    var mount = el("area-chips");
    if (!mount) return;
    mount.innerHTML =
      C.areas.primary.map(function (a) { return '<span class="chip primary">' + esc(a) + "</span>"; }).join("") +
      C.areas.also.map(function (a) { return '<span class="chip">' + esc(a) + "</span>"; }).join("");
    var note = el("area-note");
    if (note) note.textContent = C.areas.note;
  }

  /* ---------- trust / hero list ---------- */
  function renderTrust() {
    var mount = el("hero-trust");
    if (mount) {
      mount.innerHTML = trustPoints().slice(0, 4).map(function (t) {
        return "<li>" + svg("check") + "<span>" + esc(t) + "</span></li>";
      }).join("");
    }
    var badges = el("badge-row");
    if (badges) {
      badges.innerHTML = trustPoints().map(function (t) {
        return '<span class="badge">' + svg("shield") + esc(t) + "</span>";
      }).join("");
    }
  }

  /* ---------- contact rail ---------- */
  function renderContactRail() {
    var mount = el("contact-rail");
    if (!mount) return;
    var rows = [
      { i: "phone", k: "Call or text", v: B.phone, href: telHref, big: true },
      { i: "pin", k: "Service area", v: C.areas.primary.join(" · ") + " and beyond" }
    ];
    if (B.email) rows.splice(1, 0, { i: "mail", k: "Email", v: B.email, href: "mailto:" + B.email });
    if (B.hours) rows.push({ i: "clock", k: "Hours", v: B.hours });

    mount.innerHTML = rows.map(function (r) {
      var v = '<span class="v' + (r.big ? " big" : "") + '">' + esc(r.v) + "</span>";
      if (r.href) v = '<a href="' + r.href + '">' + v + "</a>";
      return '<div class="contact-item">' + svg(r.i) + "<div><span class=\"k\">" + esc(r.k) + "</span><br>" + v + "</div></div>";
    }).join("");
  }

  /* ---------- reviews (real ones only; hidden when empty) ---------- */
  function renderReviews() {
    var section = el("reviews-section");
    if (!section) return;
    if (!C.reviews || !C.reviews.length) { section.remove(); return; }
    var mount = el("review-grid");
    mount.innerHTML = C.reviews.map(function (r) {
      var stars = "";
      for (var i = 0; i < (r.stars || 5); i++) stars += svg("star");
      return '<div class="card"><div class="card-body"><div style="fill:#f0b429;display:flex;gap:2px">' + stars + "</div>" +
        "<p style=\"margin:.7rem 0\">" + esc(r.text) + "</p><strong>" + esc(r.name) +
        (r.city ? " — " + esc(r.city) : "") + "</strong></div></div>";
    }).join("");
  }

  /* ---------- page title phone swaps ---------- */
  function renderPhoneLinks() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-phone]"), function (a) {
      a.setAttribute("href", telHref);
      if (a.hasAttribute("data-phone-text")) a.innerHTML = svg("phone") + esc(B.phone);
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-sms]"), function (a) {
      a.setAttribute("href", smsHref);
    });
    Array.prototype.forEach.call(document.querySelectorAll("[data-biz-name]"), function (n) {
      n.textContent = B.name;
    });
  }

  /* ---------- keep preview hosts out of search ----------
     Anything not served from the real domain (github.io preview,
     localhost, a staging host) gets noindex. The live site on
     silverstarplumbing.co is unaffected. */
  function guardPreview() {
    var host = location.hostname;
    if (!host || host === B.domain || host === "www." + B.domain) return;
    var m = document.createElement("meta");
    m.name = "robots";
    m.content = "noindex,nofollow";
    document.head.appendChild(m);
  }

  /* ---------- JSON-LD (only verified facts) ---------- */
  function injectSchema() {
    var data = {
      "@context": "https://schema.org",
      "@type": "Plumber",
      name: B.name,
      telephone: B.phone,
      url: "https://" + B.domain,
      areaServed: C.areas.primary.concat(C.areas.also).map(function (a) {
        return { "@type": "City", name: a };
      })
    };
    if (B.email) data.email = B.email;
    if (B.hours) data.openingHours = B.hours;
    var tag = document.createElement("script");
    tag.type = "application/ld+json";
    tag.textContent = JSON.stringify(data);
    document.head.appendChild(tag);
  }

  /* ---------- boot ---------- */
  function boot() {
    renderHeader();
    renderFooter();
    renderCallBar();
    renderServiceGrid();
    renderServiceDetails();
    renderAreas();
    renderTrust();
    renderContactRail();
    renderReviews();
    renderJumpBar();
    renderToTop();
    renderPhoneLinks();
    guardPreview();
    injectSchema();
    initReveal();
    /* The page is built after DOM ready, so the browser's own hash jump
       lands in the wrong place. Re-run it once images have settled. */
    if (location.hash) {
      var jump = function () {
        var t = document.getElementById(location.hash.slice(1));
        if (t) t.scrollIntoView();
      };
      setTimeout(jump, 60);
      window.addEventListener("load", function () { setTimeout(jump, 40); });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else { boot(); }

  window.SSP_UI = { svg: svg, esc: esc, telHref: telHref, smsHref: smsHref };
})();
