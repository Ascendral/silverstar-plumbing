/* =========================================================
   Silver Star Plumbing — request form
   Two real submit paths, no silent failure:
     1. config.form.endpoint set  -> POST the request there.
     2. endpoint empty (default)  -> compose the request and
        hand the customer a pre-filled text / email / call
        button. Nothing is thrown away.
   ========================================================= */

(function () {
  "use strict";

  var form = document.getElementById("request-form");
  if (!form || !window.SSP) return;

  var C = window.SSP, B = C.business, UI = window.SSP_UI;
  var statusBox = document.getElementById("form-status");

  /* populate the service dropdown from config */
  var sel = form.querySelector('select[name="service"]');
  if (sel) {
    C.services.forEach(function (s) {
      var o = document.createElement("option");
      o.value = s.name;
      o.textContent = s.name;
      sel.appendChild(o);
    });
    var other = document.createElement("option");
    other.value = "Something else";
    other.textContent = "Something else / not sure";
    sel.appendChild(other);
  }

  function fieldOf(input) { return input.closest(".field") || input.parentNode; }

  function validate() {
    var ok = true;
    Array.prototype.forEach.call(form.querySelectorAll("[required]"), function (input) {
      var v = input.value.trim();
      var bad = !v;
      if (!bad && input.name === "phone") {
        bad = (v.replace(/\D/g, "").length < 10);
      }
      fieldOf(input).classList.toggle("invalid", bad);
      if (bad && ok) input.focus();
      if (bad) ok = false;
    });
    return ok;
  }

  form.addEventListener("input", function (e) {
    var f = fieldOf(e.target);
    if (f && f.classList.contains("invalid") && e.target.value.trim()) f.classList.remove("invalid");
  });

  function values() {
    var d = {};
    Array.prototype.forEach.call(form.elements, function (n) {
      if (n.name && n.type !== "submit") d[n.name] = n.value.trim();
    });
    return d;
  }

  function compose(d) {
    var lines = [
      "Plumbing request — " + (d.service || "General"),
      "Name: " + d.name,
      "Phone: " + d.phone,
      d.email ? "Email: " + d.email : null,
      d.city ? "City: " + d.city : null,
      d.address ? "Address: " + d.address : null,
      "",
      d.message
    ];
    return lines.filter(function (l) { return l !== null; }).join("\n");
  }

  function show(kind, html) {
    if (!statusBox) return;
    statusBox.className = "form-status show " + kind;
    statusBox.innerHTML = html;
    statusBox.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (form.querySelector('[name="_hp"]').value) return;   // honeypot
    if (!validate()) {
      show("err", "Please fill in the highlighted fields — we need a name, a phone number and a short description.");
      return;
    }

    var d = values();
    var body = compose(d);
    var btn = form.querySelector('button[type="submit"]');

    if (C.form.endpoint) {
      btn.disabled = true;
      btn.textContent = "Sending…";
      fetch(C.form.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(d)
      }).then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        form.reset();
        show("ok", "<strong>Got it.</strong> Your request is in — " + UI.esc(B.owner.split(" ")[0]) +
          " will get back to you. If it's urgent, call <a href=\"" + UI.telHref + "\">" + UI.esc(B.phone) + "</a>.");
      }).catch(function (err) {
        show("err", "That didn't send (" + UI.esc(err.message) + "). Call or text " +
          "<a href=\"" + UI.telHref + "\">" + UI.esc(B.phone) + "</a> and we'll take care of it.");
      }).then(function () {
        btn.disabled = false;
        btn.textContent = "Send Request";
      });
      return;
    }

    /* no backend configured — hand off to the phone, pre-filled */
    var sms = "sms:" + B.phoneRaw + (/iPhone|iPad|Mac/.test(navigator.userAgent) ? "&" : "?") +
              "body=" + encodeURIComponent(body);
    var mail = B.email
      ? "mailto:" + B.email + "?subject=" + encodeURIComponent("Plumbing request — " + (d.service || "General")) +
        "&body=" + encodeURIComponent(body)
      : "";

    show("ok",
      "<strong>Ready to send.</strong> Tap one of these and it goes straight to " + UI.esc(B.owner.split(" ")[0]) + ":" +
      '<div style="display:flex;flex-wrap:wrap;gap:.6rem;margin:.9rem 0">' +
        '<a class="btn btn-call" href="' + UI.telHref + '">Call ' + UI.esc(B.phone) + "</a>" +
        '<a class="btn btn-primary" href="' + sms + '">Send as text</a>' +
        (mail ? '<a class="btn btn-ghost" href="' + mail + '">Send as email</a>' : "") +
      "</div>" +
      '<details><summary style="cursor:pointer">Or copy the details</summary>' +
      '<pre style="white-space:pre-wrap;margin-top:.6rem;font:inherit">' + UI.esc(body) + "</pre></details>");
  });
})();
