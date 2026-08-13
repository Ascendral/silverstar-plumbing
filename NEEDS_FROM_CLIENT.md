# What Sergio has to give us before this site goes live

Everything below is **blank on purpose**. I did not invent any of it. The site
is built so that blank values simply don't render — no fake badge, no made-up
number. Fill these into `js/config.js` and the matching elements appear.

## Legally required before advertising

| Item | Where it goes | Why it matters |
|---|---|---|
| **CSLB license number** | `business.license` | California B&P Code §7027.1 requires a licensed contractor's license number in *all* advertising, including a website. Right now the site advertises plumbing services with no license number on it. This one is not optional. |
| **Licensed & insured — confirm** | `business.insured` | Currently `false`, so no "licensed and insured" claim appears anywhere. Do not flip to `true` until confirmed. |

If Sergio is **not** licensed, that changes what the site is allowed to say and
what work he can legally take (unlicensed work in CA is capped at $500 total
including materials, and must be disclosed). Ask him directly before launch.

## Needed to make the site actually useful

| Item | Where it goes |
|---|---|
| Business email | `business.email` |
| Business hours | `business.hours` |
| Is it really 24/7 emergency? | `business.emergency24` (currently `false`) |
| Years in the trade | `business.yearsInBusiness` |
| Google Business Profile link | `business.mapsUrl` |
| Facebook / Instagram / Yelp | `business.facebook` etc. |

## Content that would make it much stronger

1. **Real job photos.** The artwork on the site right now is illustration I
   generated — it is deliberately abstract and clearly not photography, so it
   reads as brand art rather than a fake stock photo of somebody else's work.
   Ten to twenty real photos (water heater installs, repipes, softener loops,
   a clean finished bathroom) would beat it in every way. Drop them in
   `img/photos/` and set the `photo:` field on the matching service in
   `js/config.js` — it overrides the illustration automatically.
2. **Real reviews.** `reviews: []` in config is empty and the whole reviews
   section removes itself. I will not write testimonials. Give me real ones
   (name, city, what they said) and the section turns on.
3. **Sergio's story.** The About page currently talks about *how he works*,
   because that's all I could write truthfully. How long he's been doing this,
   where he trained, whether it's a family business — that's the part that
   sells, and I don't know any of it.
4. **Confirm the service area list.** `areas.primary` and `areas.also` in
   config are the four cities you named plus neighbors I inferred. Patterson
   is a ~70 mile drive from Discovery Bay — if he isn't really covering both
   ends every week, trim the list. No mileage radius is published anywhere.

## Decisions still open

- **Domain spelling.** You wrote `siverstarpluimbing.co`; the site is built for
  **`silverstarplumbing.co`**. Confirm the exact registered spelling — every
  canonical URL, the sitemap and the schema markup use it.
- **Where the contact form goes.** With `form.endpoint` empty (today), the form
  validates and then hands the customer a pre-filled text/call button — it works
  right now with no backend. Set a Formspree or Netlify Forms endpoint if
  Sergio wants submissions emailed instead.
- **Pricing.** Nothing on this site quotes a price, a service-call fee, or a
  free-estimate offer. Ask him what he actually charges before adding any.
