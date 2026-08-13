# Silver Star Plumbing — silverstarplumbing.co

Static site for Silver Star Plumbing (owner: Sergio Estrella). No build step,
no framework, no dependencies. Open `index.html` and it runs.

## Structure

```
index.html        home
services.html     all services + detail blocks + FAQ
areas.html        service area
about.html        owner / how we work
contact.html      request form + emergency instructions

css/style.css     the whole design system
js/config.js      *** ALL business data lives here ***
js/main.js        renders header, footer, service grids, areas, schema
js/contact.js     request form: validation + submit

img/*.svg         generated brand artwork (see below)
tools/make_art.py     regenerates img/*.svg
tools/build_sample.py builds the single-file client sample into dist/
```

**Edit `js/config.js`, not the HTML.** Phone number, services, service area
and every trust claim render from that one file. Change it once, it changes on
all five pages.

## Running it locally

```bash
python3 -m http.server 8351 --directory /Users/zanderone/ClaudeWork/silverstar-plumbing
```

Then open http://localhost:8351

## The artwork

`img/*.svg` is generated, not photographed and not stock. `tools/make_art.py`
draws every illustration from a shared set of primitives (pipe, coupling,
tank, gauge, valve, droplet) so the whole set shares one palette and one line
weight. Regenerate after any palette change:

```bash
python3 tools/make_art.py
```

Real job photos beat this. Drop them in `img/photos/`, set the `photo:` field
on the matching service in `js/config.js`, and the illustration is replaced —
no other change needed.

## The client sample

```bash
python3 tools/build_sample.py
```

Produces `dist/silver-star-sample.html` — the entire site (all sections, all
artwork, all scripts) inlined into one self-contained file. Email it, AirDrop
it, open it offline. It is generated from the same sources as the live site,
so it cannot drift from it. The build asserts that nothing external is left
referenced and fails loudly if it is.

`dist/artifact-body.html` is the same content without the document wrapper,
for publishing as a shareable link.

## What is deliberately NOT on this site

No license number, no "licensed and insured" badge, no "24/7", no years-in-
business, no reviews, no prices. Those are claims, and nobody has given me the
facts behind them yet. Blank config values render nothing rather than
rendering a guess. See `NEEDS_FROM_CLIENT.md` — the CSLB license number is a
legal requirement for advertising in California and has to be resolved before
launch.

## Contact form

`config.form.endpoint` is empty by default. In that state the form validates
input and then composes the request into a pre-filled text message / email /
call button — it works today with no backend and nothing is silently dropped.
Set an endpoint (Formspree, Netlify Forms) to receive submissions by email
instead; that path POSTs JSON and reports real HTTP errors to the customer
with the phone number as the fallback.

## Deploy

Static hosting, any provider. Netlify/Vercel/Cloudflare Pages: point at this
directory, no build command, publish directory `.`. Set the domain to
`silverstarplumbing.co` and confirm the canonical URLs in each page's `<head>`
match the final spelling.
