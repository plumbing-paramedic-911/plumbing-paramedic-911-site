#!/usr/bin/env python3
"""Fail a release when a sitemap page has no crawlable static <a> link."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "plumbingparamedic911.com"


def normalize(href: str) -> str | None:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    parsed = urlparse(href)
    if parsed.scheme and parsed.netloc not in {DOMAIN, f"www.{DOMAIN}"}:
        return None
    path = parsed.path or "/"
    if not path.startswith("/"):
        return None  # Site navigation is intentionally root-absolute.
    if re.search(r"\.[A-Za-z0-9]{1,5}$", path):
        return None
    if path != "/" and not path.endswith("/"):
        path += "/"
    return path


incoming: dict[str, set[str]] = {}
for file in sorted(ROOT.rglob("*.html")):
    source = "/" if file == ROOT / "index.html" else "/" + file.parent.relative_to(ROOT).as_posix().strip("/") + "/"
    text = file.read_text(encoding="utf-8")
    for href in re.findall(r'<a\b[^>]*\bhref=["\']([^"\']+)["\']', text, re.I):
        target = normalize(href)
        if target and target != source:
            incoming.setdefault(target, set()).add(source)

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
urls = re.findall(r"<loc>https://plumbingparamedic911\.com([^<]*)</loc>", sitemap)
paths = [u or "/" for u in urls]
orphans = [p for p in paths if p != "/" and not incoming.get(p)]

if orphans:
    print("Static internal-link validation failed. Orphaned sitemap pages:", file=sys.stderr)
    for path in orphans:
        print(f" - {path}", file=sys.stderr)
    raise SystemExit(1)

print(f"Static internal-link validation passed for {len(paths)} sitemap pages.")
