#!/usr/bin/env python3
"""Production release builder for Plumbing Paramedic 911.

Loads the existing generator, applies production SEO/AEO overrides, regenerates
all generator-owned pages, builds high-intent local service pages, applies the
current pricing policy, strengthens static internal linking, restores selected
legacy authority assets into the canonical source tree, and validates critical
search requirements before deployment.

Run:
    python3 tools/release_build.py
"""
from __future__ import annotations

import html
import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BUILD_FILE = ROOT / "tools" / "build.py"
MONEY_FILE = ROOT / "tools" / "local_money_pages.py"
PRICING_POLICY_FILE = ROOT / "tools" / "current_pricing_overrides.py"
SUPER_SITE_FILE = ROOT / "tools" / "super_site_content.py"
BASE_URL = "https://plumbingparamedic911.com"

TITLE_OVERRIDES = {
    ("SERVICES", "well-pump-repair"): "Well Pump Repair Abbeville SC | Plumbing Paramedic 911",
    ("SERVICES", "plumbing-fixture-installation-repair"): "Fixture Repair Abbeville SC | Plumbing Paramedic 911",
    ("SERVICES", "backflow-prevention-testing"): "Backflow Testing Upstate SC | Plumbing Paramedic 911",
    ("CITIES", "mccormick-sc"): "McCormick SC Plumber & Well Pumps | Plumbing Paramedic 911",
    ("CITIES", "calhoun-falls-sc"): "Calhoun Falls SC Plumber | Plumbing Paramedic 911",
}

DESCRIPTION_OVERRIDES = {
    ("SERVICES", "well-pump-repair"): "Same-day well pump repair, pressure tanks and no-water service in Abbeville, McCormick and Upstate SC. Upfront pricing. Call (864) 446-8911.",
    ("SERVICES", "plumbing-fixture-installation-repair"): "Faucet, toilet, sink, disposal and fixture repair or installation in Abbeville and Upstate SC. Upfront flat-rate pricing. Call (864) 446-8911.",
    ("SERVICES", "backflow-prevention-testing"): "Certified backflow testing, repair and installation for irrigation, fire and commercial systems across Upstate SC. Call (864) 446-8911.",
    ("CITIES", "mccormick-sc"): "24/7 plumber in McCormick SC for well pumps, lake homes, water heaters, drains and leaks. Upfront pricing. Call (864) 446-8911.",
    ("CITIES", "calhoun-falls-sc"): "24/7 plumber in Calhoun Falls SC for well pumps, lake homes, water heaters, drains and leaks. Upfront pricing. Call (864) 446-8911.",
}

CRITICAL_TITLE_PATHS = {
    "services/well-pump-repair/index.html",
    "services/plumbing-fixture-installation-repair/index.html",
    "services/backflow-prevention-testing/index.html",
    "service-areas/mccormick-sc/index.html",
    "service-areas/calhoun-falls-sc/index.html",
    "well-pump-repair-mccormick-sc/index.html",
    "well-pump-repair-iva-lake-secession-sc/index.html",
    "drain-cleaning-greenwood-sc/index.html",
    "water-heater-repair-greenwood-sc/index.html",
    "water-heater-repair-anderson-sc/index.html",
    "emergency-plumber-abbeville-sc/index.html",
    "drain-cleaning-abbeville-sc/index.html",
    "sewer-line-repair-abbeville-sc/index.html",
    "emergency-plumber-greenwood-sc/index.html",
}

LAKE_AREA_LINKS = (
    '<a href="/service-areas/iva-lake-secession-sc/">📍 Iva &amp; Lake Secession, SC</a>'
    '<a href="/service-areas/savannah-lakes-village-sc/">📍 Savannah Lakes Village, SC</a>'
)
LAKE_AREA_MOBILE_LINKS = (
    '  <a href="/service-areas/iva-lake-secession-sc/">📍 Iva &amp; Lake Secession, SC</a>\n'
    '  <a href="/service-areas/savannah-lakes-village-sc/">📍 Savannah Lakes Village, SC</a>\n'
)
LAKE_AREA_FOOTER_LINKS = (
    '<li><a href="/service-areas/iva-lake-secession-sc/">Iva &amp; Lake Secession, SC</a></li>'
    '<li><a href="/service-areas/savannah-lakes-village-sc/">Savannah Lakes Village, SC</a></li>'
)
AREA_CARDS = '''\
<a class="nav-card" href="/service-areas/iva-lake-secession-sc/"><h3>💧 Iva &amp; Lake Secession, SC</h3><p>Well pumps, lake homes and rural plumbing.</p><span class="arrow">Iva &amp; Lake Secession plumber →</span></a>
<a class="nav-card" href="/service-areas/savannah-lakes-village-sc/"><h3>🏡 Savannah Lakes Village, SC</h3><p>Well pumps, lift pumps and second-home plumbing.</p><span class="arrow">Savannah Lakes Village plumber →</span></a>
'''
WELL_PUMP_MARKET_BLOCK = '''\
<section id="lake-area-well-pump-focus" class="section" style="padding-top:34px;padding-bottom:34px">
  <div class="container">
    <div style="background:var(--blue-xlt);border:1.5px solid #90CAF9;border-radius:var(--r2);padding:26px">
      <span class="label">Priority Well-Pump Markets</span>
      <h2 style="font-size:1.45rem;margin:6px 0 10px">Lake Secession, Iva, McCormick &amp; Savannah Lakes Village</h2>
      <p style="color:var(--ink2);margin-bottom:16px">Extra focus on lake and rural properties where a failed well pump or pressure system can shut the entire home down.</p>
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <a class="btn btn-blue btn-sm" href="/service-areas/iva-lake-secession-sc/">Iva &amp; Lake Secession →</a>
        <a class="btn btn-blue btn-sm" href="/service-areas/savannah-lakes-village-sc/">Savannah Lakes Village →</a>
        <a class="btn btn-blue btn-sm" href="/service-areas/mccormick-sc/">McCormick →</a>
      </div>
    </div>
  </div>
</section>
'''


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_build_module():
    return load_module(BUILD_FILE, "pp911_build")


def load_money_module():
    return load_module(MONEY_FILE, "pp911_money_pages")


def load_pricing_policy_module():
    return load_module(PRICING_POLICY_FILE, "pp911_pricing_policy")


def load_super_site_module():
    return load_module(SUPER_SITE_FILE, "pp911_super_site")


def apply_overrides(build) -> None:
    for (group_name, slug), title in TITLE_OVERRIDES.items():
        group = getattr(build, group_name)
        if slug not in group:
            raise KeyError(f"Missing {group_name}[{slug!r}]")
        group[slug]["title"] = title
        group[slug]["description"] = DESCRIPTION_OVERRIDES[(group_name, slug)]

    desktop_needle = '<a href="/service-areas/due-west-sc/">📍 Due West, SC</a></div></li>'
    if desktop_needle in build.NAV_HTML and "/service-areas/iva-lake-secession-sc/" not in build.NAV_HTML:
        build.NAV_HTML = build.NAV_HTML.replace(desktop_needle, '<a href="/service-areas/due-west-sc/">📍 Due West, SC</a>' + LAKE_AREA_LINKS + '</div></li>')
    mobile_needle = '  <a href="/service-areas/due-west-sc/">📍 Due West, SC</a>\n'
    if mobile_needle in build.NAV_HTML and "Iva &amp; Lake Secession" not in build.NAV_HTML:
        build.NAV_HTML = build.NAV_HTML.replace(mobile_needle, mobile_needle + LAKE_AREA_MOBILE_LINKS)
    footer_needle = '<li><a href="/service-areas/due-west-sc/">Due West, SC</a></li></ul></div>'
    if footer_needle in build.FOOTER_HTML and "Iva &amp; Lake Secession" not in build.FOOTER_HTML:
        build.FOOTER_HTML = build.FOOTER_HTML.replace(footer_needle, '<li><a href="/service-areas/due-west-sc/">Due West, SC</a></li>' + LAKE_AREA_FOOTER_LINKS + '</ul></div>')


def strengthen_internal_links() -> None:
    area_file = ROOT / "service-areas" / "index.html"
    text = area_file.read_text(encoding="utf-8")
    if '/service-areas/iva-lake-secession-sc/' not in text:
        text, count = re.subn(r'(<div class="grid-4">)', r'\1\n' + AREA_CARDS, text, count=1)
        if count != 1:
            raise RuntimeError("Could not locate service-area grid")
        area_file.write_text(text, encoding="utf-8")

    well_file = ROOT / "services" / "well-pump-repair" / "index.html"
    text = well_file.read_text(encoding="utf-8")
    if 'id="lake-area-well-pump-focus"' not in text:
        text, count = re.subn(r'(<section class="service-hero".*?</section>)', r'\1\n' + WELL_PUMP_MARKET_BLOCK, text, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError("Could not locate well-pump service hero")
        well_file.write_text(text, encoding="utf-8")


def ensure_sitemap() -> None:
    sitemap = ROOT / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    required = [
        "https://plumbingparamedic911.com/service-areas/iva-lake-secession-sc/",
        "https://plumbingparamedic911.com/service-areas/savannah-lakes-village-sc/",
    ]
    for url in required:
        if url not in text:
            entry = f"  <url><loc>{url}</loc><lastmod>2026-08-13</lastmod></url>\n"
            text = text.replace("</urlset>", entry + "</urlset>")
    sitemap.write_text(text, encoding="utf-8")


def url_to_file(url: str) -> Path:
    path = urlparse(url).path
    if path == "/":
        return ROOT / "index.html"
    return ROOT / path.lstrip("/") / "index.html"


def normalize_internal_href(href: str) -> str | None:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    parsed = urlparse(href)
    if parsed.scheme and parsed.netloc not in {"plumbingparamedic911.com", "www.plumbingparamedic911.com"}:
        return None
    path = parsed.path or "/"
    if re.search(r"\.[A-Za-z0-9]{1,5}$", path):
        return None
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and not path.endswith("/"):
        path += "/"
    return path


def validate_release() -> None:
    errors: list[str] = []
    html_files = sorted(ROOT.rglob("*.html"))
    title_to_files: dict[str, list[str]] = {}
    desc_to_files: dict[str, list[str]] = {}
    incoming: dict[str, int] = {}

    for file in html_files:
        rel = file.relative_to(ROOT).as_posix()
        text = file.read_text(encoding="utf-8")
        title_match = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
        if not title_match:
            errors.append(f"{rel}: missing <title>")
        else:
            title = html.unescape(re.sub(r"\s+", " ", title_match.group(1))).strip()
            title_to_files.setdefault(title, []).append(rel)
            if rel in CRITICAL_TITLE_PATHS and len(title) > 62:
                errors.append(f"{rel}: critical title is too long ({len(title)} chars): {title}")

        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', text, re.I)
        if not desc_match:
            errors.append(f"{rel}: missing meta description")
        else:
            desc = html.unescape(desc_match.group(1)).strip()
            if desc:
                desc_to_files.setdefault(desc, []).append(rel)

        if not re.search(r'<link\s+rel="canonical"\s+href="https://plumbingparamedic911\.com/', text, re.I):
            errors.append(f"{rel}: missing/non-canonical canonical URL")
        if "<h1" not in text.lower():
            errors.append(f"{rel}: missing H1")
        if "schript" in text.lower():
            errors.append(f"{rel}: contains broken 'schript' tag typo")
        for block in re.findall(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S | re.I):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON-LD ({exc})")
        for href in re.findall(r'href=["\']([^"\']+)["\']', text, re.I):
            normalized = normalize_internal_href(href)
            if normalized:
                incoming[normalized] = incoming.get(normalized, 0) + 1

    for title, files in title_to_files.items():
        if len(files) > 1:
            errors.append(f"duplicate title {title!r}: {', '.join(files)}")
    for desc, files in desc_to_files.items():
        if len(files) > 1:
            errors.append(f"duplicate meta description: {', '.join(files)}")

    sitemap_text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sitemap_urls = re.findall(r"<loc>(https://plumbingparamedic911\.com[^<]+)</loc>", sitemap_text)
    for url in sitemap_urls:
        target = url_to_file(url)
        if not target.exists():
            errors.append(f"sitemap URL has no deployable file: {url}")
        path = urlparse(url).path
        if path != "/" and incoming.get(path, 0) == 0:
            errors.append(f"orphaned sitemap page (no static internal link): {url}")

    pricing = (ROOT / "pricing" / "index.html").read_text(encoding="utf-8")
    if 'id="current-service-call-pricing"' not in pricing:
        errors.append("pricing/index.html: missing current service-call disclosure")
    if "service call fee is waived" in pricing.lower():
        errors.append("pricing/index.html: stale waived-service-call wording remains")
    if "$150 after-hours surcharge" in pricing:
        errors.append("pricing/index.html: stale after-hours surcharge wording remains")
    if "−$50" in pricing or "selectOption(this,'discount','military',-50)" in pricing:
        errors.append("pricing/index.html: stale fixed-$50 discount calculator remains")

    faq = (ROOT / "faq" / "index.html").read_text(encoding="utf-8")
    if "We offer $50 off" in faq:
        errors.append("faq/index.html: stale fixed-$50 discount wording remains")
    if "gives free up-front estimates" in faq:
        errors.append("faq/index.html: stale free-estimate wording remains")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    if "## High-Intent Local Service Pages" not in llms:
        errors.append("llms.txt: local money-page index missing")
    if "## Preserved Super Site Assets" not in llms:
        errors.append("llms.txt: preserved super-site asset index missing")

    if errors:
        print("SEO/AEO RELEASE VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"SEO/AEO release validation passed: {len(html_files)} HTML pages, {len(sitemap_urls)} sitemap URLs.")


def main() -> None:
    build = load_build_module()
    money = load_money_module()
    pricing_policy = load_pricing_policy_module()
    super_site = load_super_site_module()

    # Apply the selective legacy-content migration before generator output is built.
    # This preserves good historical URLs/content while excluding old themes,
    # stale pricing, duplicate pages, and the legacy deployment system.
    super_site.apply(build, money)
    apply_overrides(build)
    build.main()
    strengthen_internal_links()
    money.generate(build)
    super_site.generate_guides(build)
    pricing_policy.apply()
    ensure_sitemap()
    super_site.ensure_metadata()
    super_site.validate_migration()
    validate_release()


if __name__ == "__main__":
    main()
