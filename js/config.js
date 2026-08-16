/* =========================================================
   Silver Star Plumbing — SITE CONFIG
   Single source of truth. Every page renders from this file.
   Edit here, not in the HTML.

   Anything left as "" (empty string) is intentionally BLANK
   because we do not have the real value yet. The site hides
   those elements rather than printing a guess.
   See NEEDS_FROM_CLIENT.md.
   ========================================================= */

window.SSP = {

  /* ---------- business identity ---------- */
  business: {
    name: "Silver Star Plumbing",
    owner: "Sergio Estrella",
    phone: "(209) 430-9063",
    phoneRaw: "+12094309063",
    email: "",                 // NEEDS: business email
    domain: "silverstarplumbing.co",

    // CA law (B&P §7027.1) requires the CSLB license number in advertising.
    // Leave "" until confirmed — the badge and footer line stay hidden.
    license: "",               // NEEDS: CSLB C-36 license number
    insured: false,            // NEEDS: confirm before flipping true
    emergency24: false,        // NEEDS: confirm 24/7 availability before flipping true
    yearsInBusiness: "",       // NEEDS: e.g. "15"

    hours: "",                 // NEEDS: e.g. "Mon–Sat 7am–6pm"
    mapsUrl: "",               // NEEDS: Google Business Profile link
    facebook: "",
    instagram: "",
    yelp: ""
  },

  /* ---------- contact form ----------
     endpoint "" => the form composes a pre-filled text message /
     email to the owner (works today, no backend).
     Set a Formspree/Netlify endpoint later to receive submissions
     as email instead. Both paths are live code, neither is a stub. */
  form: {
    endpoint: ""               // e.g. "https://formspree.io/f/xxxxxxx"
  },

  /* ---------- services ----------
     photo: "" => the generated illustration in img/ is used.
     Drop a real job photo in img/photos/ and put the path here
     to override it. */
  services: [
    {
      id: "water-heaters",
      name: "Water Heaters",
      short: "Tank and tankless — repair, replacement, and new installs.",
      art: "img/svc-water-heaters.svg",
      photo: "img/photos/water-heaters.jpg",
      bullets: [
        "Tank water heater replacement and repair",
        "Tankless installation and descaling",
        "No hot water, pilot and thermostat diagnostics",
        "T&P valve, expansion tank, and drain pan work",
        "Earthquake strapping and code-compliant venting"
      ]
    },
    {
      id: "shower-valves",
      name: "Shower & Tub Valves",
      short: "Leaking, seized, or scalding valves swapped out clean.",
      art: "img/svc-shower-valves.svg",
      photo: "img/photos/shower-valves.jpg",
      bullets: [
        "Shower and tub valve replacement",
        "Anti-scald / pressure-balancing valve upgrades",
        "Cartridge and trim kit replacement",
        "Diverter and shower arm repairs",
        "Access panel and tile-conscious approach"
      ]
    },
    {
      id: "water-softeners",
      name: "Water Softeners",
      short: "Hard water is rough on fixtures, heaters, and skin.",
      art: "img/svc-water-softeners.svg",
      photo: "",
      bullets: [
        "Whole-house softener installation",
        "Loop / bypass plumbing for new systems",
        "Resin, valve head, and brine tank service",
        "Salt-based and salt-free options",
        "Replacement of failed or aging units"
      ]
    },
    {
      id: "reverse-osmosis",
      name: "Reverse Osmosis",
      short: "Drinking water systems under the sink and whole-house.",
      art: "img/svc-reverse-osmosis.svg",
      photo: "",
      bullets: [
        "Under-sink reverse osmosis installation",
        "Filter and membrane replacement",
        "Dedicated RO faucet and air-gap setup",
        "Fridge and ice maker tie-ins",
        "Pressure tank troubleshooting"
      ]
    },
    {
      id: "gas-lines",
      name: "Gas Lines",
      short: "New runs, extensions, and leak repair — done to code.",
      art: "img/svc-gas-lines.svg",
      photo: "img/photos/gas-lines.jpg",
      bullets: [
        "New gas line runs for ranges, dryers, and heaters",
        "BBQ, fire pit, and outdoor kitchen stub-outs",
        "Gas leak location and repair",
        "Shut-off valve installation and replacement",
        "Pressure testing"
      ]
    },
    {
      id: "shutoff-valves",
      name: "Automatic Shut-Off Valves",
      short: "A valve that closes the water before the damage starts.",
      art: "img/svc-shutoff-valves.svg",
      photo: "",
      bullets: [
        "Automatic water leak shut-off valve installation",
        "Whole-house flow monitoring",
        "Phone alerts when something is wrong",
        "Main shut-off valve replacement",
        "Well-suited to second homes and rentals"
      ]
    },
    {
      id: "leak-detection",
      name: "Leak Detection",
      short: "Find it before you tear anything out.",
      art: "img/svc-leak-detection.svg",
      photo: "",
      bullets: [
        "Slab leak location",
        "Wall and ceiling leak tracing",
        "Water meter and pressure testing",
        "Irrigation and hose bib leaks",
        "Repair options explained before work starts"
      ]
    },
    {
      id: "repipe",
      name: "Repipes & Water Lines",
      short: "Whole-house repipes and main water line replacement.",
      art: "img/svc-repipe.svg",
      photo: "img/photos/repipe.jpg",
      bullets: [
        "Whole-house repipe (PEX and copper)",
        "Main water line replacement",
        "Galvanized and failing poly line replacement",
        "Pressure regulator (PRV) replacement",
        "Hose bibs and exterior lines"
      ]
    },
    {
      id: "drains",
      name: "Drains & Sewer",
      short: "Slow, backed up, or smelling like it shouldn't.",
      art: "img/svc-drains.svg",
      photo: "",
      bullets: [
        "Kitchen, bath, and main line drain clearing",
        "Hydro jetting",
        "Sewer camera inspection",
        "Root intrusion and broken line repair",
        "Cleanout installation"
      ]
    },
    {
      id: "fixtures",
      name: "Faucets, Toilets & Fixtures",
      short: "The everyday stuff, done right the first time.",
      art: "img/svc-fixtures.svg",
      photo: "img/photos/fixtures.jpg",
      bullets: [
        "Faucet and sink installation",
        "Toilet repair, rebuild, and replacement",
        "Garbage disposals",
        "Dishwasher and ice maker lines",
        "Angle stops and supply lines"
      ]
    },
    {
      id: "emergency",
      name: "Emergency Plumbing",
      short: "Burst line, no water, active leak — call, don't email.",
      art: "img/svc-emergency.svg",
      photo: "",
      bullets: [
        "Burst and broken water lines",
        "Active leaks and water shut-down",
        "No water / no hot water",
        "Sewage backups",
        "Storm and freeze damage"
      ]
    }
  ],

  /* ---------- service area ----------
     Cities the client named, plus immediate neighbors.
     No mileage radius is published anywhere on the site.
     Sergio should confirm or trim this list. */
  areas: {
    primary: ["Brentwood", "Discovery Bay", "Oakley", "Patterson"],
    also: [
      "Antioch", "Bethel Island", "Byron", "Knightsen", "Pittsburg",
      "Tracy", "Mountain House", "Livermore", "Manteca", "Lathrop",
      "Stockton", "Modesto", "Newman", "Crows Landing", "Westley"
    ],
    note: "Bay Area and Central Valley. If your town isn't on the list, call and ask — chances are the answer is yes."
  },

  /* ---------- reviews ----------
     REAL reviews only. Empty array = the section does not render.
     Do not add anything here that a customer did not actually say. */
  reviews: []
};
