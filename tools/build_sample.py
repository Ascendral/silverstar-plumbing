#!/usr/bin/env python3
"""
Silver Star Plumbing — single-file sample builder.

Takes the real multi-page site (css/style.css, js/config.js, js/main.js,
js/contact.js, img/*.svg) and stitches it into ONE self-contained HTML file
with every stylesheet, script and image inlined. Nothing is retyped: the
sample is generated from the same sources as the live site, so it can never
drift from it.

Outputs:
  dist/silver-star-sample.html   standalone page — email it, open it offline
  dist/artifact-body.html        same content, no <html>/<head>/<body>
                                 wrapper, for publishing as a shareable link

Run:  python3 tools/build_sample.py
"""

import base64
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


MIME = {".svg": "image/svg+xml", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def data_uri(rel):
    with open(os.path.join(ROOT, *rel.split("/")), "rb") as f:
        raw = f.read()
    mime = MIME[os.path.splitext(rel)[1].lower()]
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode("ascii"))


def art_map():
    """Every illustration and job photo the one-pager uses, as path -> data URI.

    The gallery (img/gallery/) is deliberately excluded — 32 photos would make
    the single file far too heavy to text or email. The gallery lives on
    work.html on the real site."""
    out = {}
    for name in sorted(os.listdir(os.path.join(ROOT, "img"))):
        if name.endswith(".svg"):
            out["img/" + name] = data_uri("img/" + name)
    photos = os.path.join(ROOT, "img", "photos")
    if os.path.isdir(photos):
        for name in sorted(os.listdir(photos)):
            if os.path.splitext(name)[1].lower() in MIME:
                out["img/photos/" + name] = data_uri("img/photos/" + name)
    return out


ART = art_map()


HERO_CSS_REF = 'url("../img/photos/hero.jpg")'


def css():
    """Stylesheet with the hero background rewritten to an inline data URI."""
    s = read("css", "style.css")
    assert HERO_CSS_REF in s, "hero background reference changed — update HERO_CSS_REF"
    return s.replace(HERO_CSS_REF, 'url("%s")' % ART["img/photos/hero.jpg"])


def js_art_map():
    pairs = ",\n".join('  "%s": "%s"' % (k, v) for k, v in ART.items())
    return "window.SSP_SINGLE = true;\nwindow.SSP_ART = {\n%s\n};" % pairs


# --------------------------------------------------------------------------
# page content — sections lifted from the real pages, joined into one scroll
# --------------------------------------------------------------------------

BODY = """
<a class="skip" href="#main">Skip to content</a>
<header class="site-header" id="site-header"></header>

<main id="main">

  <section class="hero on-dark" id="top">
    <div class="wrap">
      <p class="eyebrow light">Brentwood &middot; Discovery Bay &middot; Oakley &middot; Patterson</p>
      <h1>Plumbing done right<span class="accent">the first time.</span></h1>
      <p class="lede">Water heaters, shower valves, softeners, reverse osmosis, gas lines, leak detection and automatic shut-off valves. If it carries water or gas in your house, we work on it.</p>
      <div class="hero-actions">
        <a class="btn btn-call" href="#" data-phone data-phone-text></a>
        <a class="btn btn-ghost" href="#contact">Request Service</a>
      </div>
      <ul class="hero-trust" id="hero-trust"></ul>
    </div>
  </section>

  <div class="strip">
    Water running where it shouldn't? <a href="#" data-phone>Call now</a> &mdash; emergencies get answered first.
  </div>

  <nav class="jump-bar" id="svc-jump" aria-label="Jump to a service"></nav>

  <section id="services">
    <div class="wrap">
      <p class="eyebrow">What we do</p>
      <h2>Every kind of plumbing</h2>
      <p class="lede" style="margin-bottom:2.2rem">From a dripping shower valve to a whole-house repipe. One plumber, one number, no runaround.</p>
      <div class="grid grid-4" id="service-grid"></div>
    </div>
  </section>

  <section class="band-dark on-dark">
    <div class="wrap">
      <div class="grid grid-2" style="align-items:center">
        <div>
          <p class="eyebrow light">Why Silver Star</p>
          <h2>You get the owner, not a dispatcher</h2>
          <p class="lede">Silver Star Plumbing is owner-operated. The person who answers the phone is the person who shows up, looks at the job, and tells you what it will take. No upsell script, no mystery invoice.</p>
          <div class="badge-row" id="badge-row"></div>
          <p style="margin-top:1.6rem"><a class="btn btn-call" href="#" data-phone data-phone-text></a></p>
        </div>
        <div class="grid" style="gap:1rem">
          <div class="step"><h3>Straight answers</h3><p>We explain what failed, what it takes to fix it, and what it costs &mdash; before anything gets opened up.</p></div>
          <div class="step"><h3>Clean work</h3><p>Drop cloths, shoe covers, and the site left the way we found it. Your house isn't a job site.</p></div>
          <div class="step"><h3>Code-correct</h3><p>Venting, strapping, pressure, permits where they're needed. Done so it passes and so it lasts.</p></div>
        </div>
      </div>
    </div>
  </section>

  <section class="band-tint">
    <div class="wrap" id="service-detail"></div>
  </section>

  <section class="band-dark on-dark" id="about">
    <div class="wrap">
      <div class="owner-card">
        <div class="owner-mark"><img id="about-mark" alt="Silver Star Plumbing" width="130" height="130"></div>
        <div>
          <p class="eyebrow light">About</p>
          <h2>Sergio Estrella, Silver Star Plumbing</h2>
          <p class="lede">Silver Star Plumbing is owner-operated. Sergio answers the phone, quotes the job, and does the work. There's no dispatch layer between you and the person holding the wrench &mdash; which is why the answers you get are straight ones.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="band-tint">
    <div class="wrap">
      <p class="eyebrow">How it goes</p>
      <h2>Simple from the first call</h2>
      <div class="grid grid-4 steps" style="margin-top:2rem">
        <div class="step"><h3>Call or text</h3><p>Tell us what's happening. Photos help &mdash; text them right to the same number.</p></div>
        <div class="step"><h3>We take a look</h3><p>Diagnose the real problem, not the symptom, and walk you through the options.</p></div>
        <div class="step"><h3>You approve</h3><p>Price and scope agreed up front. Nothing starts until you say go.</p></div>
        <div class="step"><h3>Fixed and clean</h3><p>Work done, area cleaned, and we make sure it's right before we leave.</p></div>
      </div>
    </div>
  </section>

  <section id="areas">
    <div class="wrap">
      <p class="eyebrow">Where we work</p>
      <h2>East Contra Costa, the Bay Area &amp; the Valley</h2>
      <p class="lede" id="area-note"></p>
      <div class="chips" id="area-chips"></div>
    </div>
  </section>

  <section class="band-dark on-dark" id="contact">
    <div class="wrap">
      <p class="eyebrow light">Contact</p>
      <h2>Fastest way to get help: call</h2>
      <p class="lede" style="margin-bottom:2rem">Plumbing problems don't wait for email. If water is running or you have no hot water, pick up the phone &mdash; the form below is for everything that can wait a bit.</p>

      <div class="grid grid-2" style="align-items:start">
        <div class="contact-rail" id="contact-rail"></div>

        <div class="form-wrap" style="color:var(--ink)">
          <h3 style="margin-bottom:.9rem">Request service</h3>
          <form id="request-form" novalidate>
            <input type="text" name="_hp" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
            <div class="field-row">
              <div class="field">
                <label for="f-name">Name <span class="req">*</span></label>
                <input id="f-name" name="name" type="text" autocomplete="name" required>
                <span class="field-error">We need a name.</span>
              </div>
              <div class="field">
                <label for="f-phone">Phone <span class="req">*</span></label>
                <input id="f-phone" name="phone" type="tel" autocomplete="tel" required>
                <span class="field-error">A 10-digit phone number, please.</span>
              </div>
            </div>
            <div class="field-row">
              <div class="field">
                <label for="f-email">Email</label>
                <input id="f-email" name="email" type="email" autocomplete="email">
              </div>
              <div class="field">
                <label for="f-city">City</label>
                <input id="f-city" name="city" type="text" autocomplete="address-level2">
              </div>
            </div>
            <div class="field">
              <label for="f-service">What do you need? <span class="req">*</span></label>
              <select id="f-service" name="service" required><option value="">Choose one&hellip;</option></select>
              <span class="field-error">Pick the closest match.</span>
            </div>
            <div class="field">
              <label for="f-message">What's going on? <span class="req">*</span></label>
              <textarea id="f-message" name="message" required placeholder="Where is it, when did it start, and what have you already tried?"></textarea>
              <span class="field-error">A sentence or two is enough.</span>
            </div>
            <button class="btn btn-primary" type="submit" style="width:100%">Send Request</button>
            <p class="form-note">Urgent? Don't wait on the form &mdash; call or text. We answer the phone.</p>
            <div class="form-status" id="form-status" role="status" aria-live="polite"></div>
          </form>
        </div>
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="wrap">
      <h2>Need a plumber today?</h2>
      <p class="lede">Call or text and we'll tell you straight whether it's an emergency or it can wait until Tuesday.</p>
      <div class="cta-actions">
        <a class="btn btn-call" href="#" data-phone data-phone-text></a>
        <a class="btn btn-ghost" href="#" data-sms>Text us a photo</a>
      </div>
    </div>
  </section>

</main>

<footer class="site-footer" id="site-footer"></footer>
<div class="call-bar" id="call-bar"></div>
"""

# the About portrait mark is set from the inlined art map
EXTRA_JS = """
(function () {
  var m = document.getElementById("about-mark");
  if (m && window.SSP_ART) m.src = window.SSP_ART["img/logo.svg"];
})();
"""

TITLE = "Silver Star Plumbing — Brentwood, Discovery Bay, Oakley &amp; Patterson"


def content():
    parts = [
        "<title>%s</title>" % TITLE,
        "<style>\n%s\n</style>" % css(),
        BODY,
        "<script>\n%s\n</script>" % js_art_map(),
        "<script>\n%s\n</script>" % read("js", "config.js"),
        "<script>\n%s\n</script>" % read("js", "main.js"),
        "<script>\n%s\n</script>" % read("js", "contact.js"),
        "<script>\n%s\n</script>" % EXTRA_JS,
    ]
    return "\n".join(parts)


STANDALONE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Owner-operated plumbing for Brentwood, Discovery Bay, Oakley, Patterson and the surrounding Bay Area.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
%s
</head>
<body>
%s
</body>
</html>
"""


def main():
    os.makedirs(DIST, exist_ok=True)
    body = content()

    # split the <title>/<style> head bits out for the standalone document
    head_end = body.index("</style>") + len("</style>")
    head, rest = body[:head_end], body[head_end:]

    standalone = STANDALONE % (head, rest)
    p1 = os.path.join(DIST, "silver-star-sample.html")
    with open(p1, "w", encoding="utf-8") as f:
        f.write(standalone)

    p2 = os.path.join(DIST, "artifact-body.html")
    with open(p2, "w", encoding="utf-8") as f:
        f.write(body)

    for p in (p1, p2):
        print("wrote %s (%.0f KB)" % (p, os.path.getsize(p) / 1024))

    # sanity checks — fail loudly rather than shipping a broken sample.
    # Scripts are skipped: they build hrefs by string concatenation at runtime,
    # and every path they touch goes through art()/page() already.
    markup = re.sub(r"<script>.*?</script>", "", standalone, flags=re.S)
    bad = re.findall(r'(?:src|href)="(?!#|tel:|sms:|mailto:|https?:|data:)([^"]+)"', markup)
    assert not bad, "sample still references external files: %s" % set(bad)
    assert "../img/" not in css(), "an image reference in the CSS was not inlined"
    print("OK — no un-inlined local references in the sample")


if __name__ == "__main__":
    main()
