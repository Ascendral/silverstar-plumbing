#!/usr/bin/env python3
"""
Deploy the site to Netlify using the token the Netlify CLI already stored.

Uses the Netlify REST API directly (urllib only) so there is no 100 MB CLI
download and no interactive login step. Re-running it deploys over the same
site rather than creating a new one.

Run:  python3 tools/deploy_netlify.py [site-name]
"""

import hashlib
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.netlify.com/api/v1"
CONFIG = os.path.expanduser("~/Library/Preferences/netlify/config.json")
SITE_NAME = sys.argv[1] if len(sys.argv) > 1 else "silver-star-plumbing"

# published as-is; everything else in the repo is source, not site output
SKIP_DIRS = {".git", "tools", "__pycache__", ".claude"}
SKIP_FILES = {".gitignore", "README.md", "NEEDS_FROM_CLIENT.md", ".DS_Store"}


def token():
    with open(CONFIG) as f:
        cfg = json.load(f)
    uid = cfg["userId"]
    return cfg["users"][uid]["auth"]["token"]


TOKEN = token()


def call(method, path, body=None, raw=None, content_type="application/json"):
    url = path if path.startswith("http") else API + path
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    if data is not None:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt.strip() else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{method} {url} -> {e.code}\n{e.read().decode()[:600]}")


def collect():
    """Map of '/site/path' -> (abs path, sha1)."""
    files = {}
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n in SKIP_FILES:
                continue
            p = os.path.join(base, n)
            rel = "/" + os.path.relpath(p, ROOT).replace(os.sep, "/")
            with open(p, "rb") as f:
                sha = hashlib.sha1(f.read()).hexdigest()
            files[rel] = (p, sha)
    return files


def find_or_create_site():
    for s in call("GET", "/sites?per_page=100"):
        if s["name"] == SITE_NAME:
            print(f"using existing site {s['name']} ({s['id']})")
            return s
    s = call("POST", "/sites", {"name": SITE_NAME})
    print(f"created site {s['name']} ({s['id']})")
    return s


def main():
    files = collect()
    print(f"{len(files)} files to publish")

    site = find_or_create_site()
    digests = {k: v[1] for k, v in files.items()}
    deploy = call("POST", f"/sites/{site['id']}/deploys", {"files": digests})

    required = set(deploy.get("required", []))
    by_sha = {}
    for rel, (p, sha) in files.items():
        by_sha.setdefault(sha, []).append((rel, p))

    todo = [(rel, p) for sha in required for rel, p in by_sha.get(sha, [])]
    print(f"uploading {len(todo)} changed file(s)")
    for rel, p in todo:
        with open(p, "rb") as f:
            blob = f.read()
        ctype = mimetypes.guess_type(p)[0] or "application/octet-stream"
        call("PUT", f"{API}/deploys/{deploy['id']}/files{rel}", raw=blob, content_type=ctype)
        print("  ", rel)

    for _ in range(60):
        d = call("GET", f"/deploys/{deploy['id']}")
        if d["state"] in ("ready", "error"):
            break
        time.sleep(3)

    if d["state"] != "ready":
        raise SystemExit(f"deploy ended in state={d['state']} {d.get('error_message','')}")

    print("\nstate:      ", d["state"])
    print("deploy url: ", d.get("deploy_ssl_url") or d.get("deploy_url"))
    print("LIVE URL:   ", d.get("ssl_url") or site.get("ssl_url") or site.get("url"))


if __name__ == "__main__":
    main()
