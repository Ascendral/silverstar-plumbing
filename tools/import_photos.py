#!/usr/bin/env python3
"""
Import Sergio's job photos into the site.

Reads the client's photo folder, fixes orientation, strips EXIF (phone photos
of customers' homes carry GPS), resizes for the web, and writes:

  img/photos/hero.jpg          hero background
  img/photos/<service>.jpg     one per service that a photo genuinely shows
  img/gallery/<id>.jpg         full-size gallery image
  img/gallery/t_<id>.jpg       gallery thumbnail
  js/gallery-data.js           the categorised manifest the gallery renders from

The category and service assignments below are deliberate: a photo is only
attached to a service it actually depicts. Nothing is assigned to a service
just to fill the slot.

Run:  python3 tools/import_photos.py
"""

import json
import os
import subprocess
import tempfile

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/zanderone/Desktop/SilverstartPlumbing "   # trailing space is real
PHOTOS = os.path.join(ROOT, "img", "photos")
GALLERY = os.path.join(ROOT, "img", "gallery")

# ---- gallery categories: every photo, sorted by what it shows --------------
CATEGORIES = [
    ("water-heaters", "Water Heaters", [
        ("IMG_0434", "Tankless water heater install with gas and water manifold"),
        ("IMG_1226", "Wall-mounted heater with copper manifold and shut-offs"),
        ("IMG_1538", "Exterior tankless install with gas line and shut-off"),
        ("IMG_6179", "Tankless heater, copper manifold, isolation valves"),
    ]),
    ("showers", "Showers & Tubs", [
        ("AC9FEC66-C6E3-4C0D-B2A0-052F9FFD571C", "Shower system: rain head, handheld and valve trim"),
        ("IMG_1233", "Rain head, handheld and thermostatic trim"),
        ("IMG_4563", "Shower valve trim and handheld on tile"),
        ("IMG_6377", "Marble shower with rain head, handheld and niche"),
        ("IMG_6379", "Freestanding tub and shower with matte black trim"),
        ("IMG_8953", "Freestanding tub with floor-mount filler"),
        ("IMG_8954", "Tub and shower with black fixtures"),
        ("IMG_1236", "Freestanding tub with floor-mount tub filler"),
    ]),
    ("kitchens-fixtures", "Kitchens & Fixtures", [
        ("57DCEFC5-D294-40BE-95F5-50290FC526C2", "Pot filler over a gas range"),
        ("IMG_0955", "Kitchen sink and faucet"),
        ("IMG_1227", "Apron-front sink with bridge faucet"),
        ("IMG_1228", "Wall-mounted pot filler"),
        ("IMG_1229", "Vessel sink and faucet on a wood vanity"),
        ("IMG_1377", "Double vanity with undermount sinks and faucets"),
        ("IMG_5610", "Farmhouse sink with gooseneck faucet"),
    ]),
    ("repipe-roughin", "Repipes & Rough-In", [
        ("IMG_3448", "Water lines roughed into framed walls"),
        ("IMG_3670", "Overhead pipe runs"),
        ("IMG_4902", "PEX manifold and distribution under floor joists"),
        ("IMG_6393", "Drain, vent and water lines roughed in"),
        ("IMG_6420", "Copper manifold and distribution"),
        ("IMG_8023", "Rough-in through framing"),
    ]),
    ("commercial", "Commercial", [
        ("IMG_2492", "Overhead commercial pipe and conduit runs"),
        ("IMG_2493", "Commercial overhead piping grid"),
        ("IMG_8775", "Commercial wall-mount lavatory"),
        ("IMG_8776", "ADA-height toilet with grab bar"),
        ("IMG_8779", "Commercial urinal install"),
    ]),
    ("finished-baths", "Finished Bathrooms", [
        ("IMG_2459", "Finished bath with glass shower and vanity"),
        ("IMG_0425", "Finished master bath"),
    ]),
]

# ---- photos attached to a specific service --------------------------------
# ONLY where the photo unmistakably shows that service. Anything else keeps
# the generated illustration. An earlier pass filled every service using the
# "nearest available" job; the result was four near-identical tankless-heater
# photos labelled Water Heaters / Gas Lines / Shut-Off Valves / Emergency,
# which read as a mistake to anyone looking at the page. Reverted.
SERVICE_PHOTOS = {
    "water-heaters": "IMG_6179",   # Navien tankless, copper manifold
    "shower-valves": "IMG_6377",   # rain head, handheld, valve trim
    "fixtures":      "IMG_5610",   # farmhouse sink + faucet
    "repipe":        "IMG_4902",   # PEX manifold + water distribution
    "drains":        "IMG_6393",   # ABS drain and vent stacks in framing
}
NEAREST = set()   # nothing is assigned on "close enough" any more

HERO = "IMG_0425"


def load(stem):
    """Open a source photo by stem, converting HEIC through sips if needed."""
    for ext in (".jpeg", ".jpg", ".JPG", ".JPEG", ".png"):
        p = os.path.join(SRC, stem + ext)
        if os.path.exists(p):
            return ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    for ext in (".heic", ".HEIC"):
        p = os.path.join(SRC, stem + ext)
        if os.path.exists(p):
            tmp = os.path.join(tempfile.gettempdir(), stem + "_conv.jpg")
            subprocess.run(["sips", "-s", "format", "jpeg", p, "--out", tmp],
                           check=True, capture_output=True)
            return ImageOps.exif_transpose(Image.open(tmp)).convert("RGB")
    raise SystemExit("source photo not found: " + stem)


def fit(im, w, h):
    """Cover-crop to exactly w x h, centred."""
    src_r, dst_r = im.width / im.height, w / h
    if src_r > dst_r:
        nw = int(im.height * dst_r)
        im = im.crop(((im.width - nw) // 2, 0, (im.width + nw) // 2, im.height))
    else:
        nh = int(im.width / dst_r)
        im = im.crop((0, (im.height - nh) // 2, im.width, (im.height + nh) // 2))
    return im.resize((w, h), Image.LANCZOS)


def save(im, path, q=80):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)  # no exif= -> stripped
    return os.path.getsize(path)


def main():
    total = 0

    hero = fit(load(HERO), 2000, 1125)
    total += save(hero, os.path.join(PHOTOS, "hero.jpg"), 82)
    print("hero.jpg  2000x1125")

    captions = {}
    for _, _, entries in CATEGORIES:
        for stem, cap in entries:
            captions[stem] = cap

    alts = {}
    for svc, stem in SERVICE_PHOTOS.items():
        im = fit(load(stem), 1200, 900)
        total += save(im, os.path.join(PHOTOS, svc + ".jpg"))
        alts["img/photos/" + svc + ".jpg"] = captions[stem]
        tag = "NEAREST" if svc in NEAREST else "exact  "
        print(f"photos/{svc}.jpg  <- {stem}  [{tag}] {captions[stem]}")

    manifest = []
    for cat_id, cat_name, entries in CATEGORIES:
        for stem, caption in entries:
            im = load(stem)
            total += save(fit(im, 1400, 1050), os.path.join(GALLERY, stem + ".jpg"))
            total += save(fit(im, 700, 525), os.path.join(GALLERY, "t_" + stem + ".jpg"), 76)
            manifest.append({"id": stem, "cat": cat_id, "catName": cat_name, "caption": caption})

    cats = [{"id": c, "name": n} for c, n, _ in CATEGORIES]
    out = os.path.join(ROOT, "js", "gallery-data.js")
    with open(out, "w") as f:
        f.write("/* AUTO-GENERATED by tools/import_photos.py — do not hand-edit */\n")
        f.write("window.SSP_GALLERY = " + json.dumps(
            {"categories": cats, "photos": manifest}, indent=1) + ";\n")
        # alt text for service photos = what the photo actually shows
        f.write("window.SSP_PHOTO_ALT = " + json.dumps(alts, indent=1) + ";\n")

    # every photo must carry a caption and land in a real category
    assert all(p["caption"] and p["cat"] for p in manifest), "photo missing caption/category"
    print(f"\n{len(manifest)} gallery photos in {len(cats)} categories")
    print(f"wrote {out}")
    print(f"total image bytes: {total/1024/1024:.1f} MB")

    # confirm EXIF is gone from a sample of the output
    for probe in ("photos/hero.jpg", "gallery/" + manifest[0]["id"] + ".jpg"):
        n = len(Image.open(os.path.join(ROOT, "img", probe)).getexif())
        print(f"exif check {probe}: {n} keys")
        assert n == 0, "EXIF survived in " + probe


if __name__ == "__main__":
    main()
