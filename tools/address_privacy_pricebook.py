#!/usr/bin/env python3
"""Release-time public-address privacy and price-book consistency checks.

Plumbing Paramedic 911 serves customers at their locations; never publish the
owner's residential street address as a customer-facing storefront address.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_LOCATION = "Abbeville, SC"
OLD_STREET = "13 Callaway Dr"


def clean_jsonld(match: re.Match) -> str:
    opening, raw, closing = match.groups()
    data = json.loads(raw)

    def scrub(item):
        if isinstance(item, dict):
            for key in ("streetAddress", "geo", "hasMap", "latitude", "longitude"):
                item.pop(key, None)
            for value in item.values():
                scrub(value)
        elif isinstance(item, list):
            for value in item:
                scrub(value)

    scrub(data)
    return opening + json.dumps(data, ensure_ascii=False) + closing


def scrub_html(file: Path) -> None:
    text = file.read_text(encoding="utf-8")
    # Keep structured data valid while preserving city/region/service areas.
    text = re.sub(
        r'(<script\s+type="application/ld\+json"[^>]*>)(.*?)(</script>)',
        clean_jsonld, text, flags=re.S | re.I,
    )
    # Eliminate metadata that represents a private address as a storefront.
    text = re.sub(r'^<meta property="business:contact_data:street_address"[^>]*>\s*\n?', "", text, flags=re.M)
    text = re.sub(r'^<meta property="place:location:(?:latitude|longitude)"[^>]*>\s*\n?', "", text, flags=re.M)
    # Address-specific Google Maps embeds/directions expose a residential address.
    # Replace links with the existing business listing URL and remove embeds.
    text = re.sub(r'<div class="map-embed"><iframe[^>]*>\s*</iframe></div>',
                  '<p>We travel to customers throughout Abbeville and surrounding counties. Call for service; this is not a walk-in location.</p>',
                  text, flags=re.I | re.S)
    text = text.replace("13+Callaway+Dr%2C+Abbeville%2C+SC+29620", "Abbeville%2C+SC")
    text = text.replace("13+Callaway+Dr", "Abbeville+SC")
    text = text.replace("13%20Callaway%20Dr", "Abbeville%20SC")
    text = text.replace("13 Callaway Drive", PUBLIC_LOCATION)
    text = text.replace(OLD_STREET, PUBLIC_LOCATION)
    text = text.replace("Abbeville, SC<br>Abbeville, SC 29620", "Abbeville, SC 29620")
    text = text.replace("Abbeville, SC, Abbeville, SC", "Abbeville, SC")
    text = text.replace("📍 Abbeville, SC, Abbeville, SC 29620", "📍 Serving Abbeville, SC")
    text = text.replace("Visit Abbeville, SC", "Serving Abbeville, SC (no walk-in office)")
    text = text.replace("Based at Abbeville, SC", "Based in Abbeville, SC")
    text = text.replace("based at Abbeville, SC", "based in Abbeville, SC")
    text = text.replace("shop at Abbeville, SC", "Abbeville service-area home base")
    text = text.replace("Address</strong>Abbeville, SC", "Service Area</strong>Abbeville, SC")
    text = text.replace("on Google Maps", "service area")
    if OLD_STREET.lower() in text.lower() or "13 Callaway Drive" in text:
        raise RuntimeError(f"Unredacted street address in {file}")
    file.write_text(text, encoding="utf-8")


def reconcile_water_heater() -> None:
    snapshot = json.loads((ROOT / "tools/price_book_snapshot.json").read_text(encoding="utf-8"))
    rows = {row["sku"]: row for group in snapshot["groups"] for row in group["items"]}
    assert rows["24-03"]["standard_price"] == 1800
    assert rows["24-06"]["standard_price"] == 2065

    service = ROOT / "services/water-heater-repair-replacement/index.html"
    pricing = ROOT / "pricing/index.html"
    # These amounts are for ordinary electric tank installations; alternatives,
    # special access and repairs require a specific quote.
    for file in (service, pricing):
        text = file.read_text(encoding="utf-8")
        text = text.replace("tank replacement starts around $1,800",
                            "40-gallon electric tank installation starts around $1,800")
        text = text.replace("water heater replace from $899", "40-gallon electric water heater installation from $1,800")
        text = text.replace("A 40-gallon tank replacement is $899 to $1,299 installed.",
                            "A standard 40-gallon electric tank installation starts at $1,800, subject to job conditions.")
        text = text.replace("A 50-gallon tank replacement is $999 to $1,499 installed.",
                            "A standard 50-gallon electric tank installation starts at $2,065, subject to job conditions.")
        file.write_text(text, encoding="utf-8")
    actual = service.read_text(encoding="utf-8") + pricing.read_text(encoding="utf-8")
    for value in ("$1,800", "$2,065"):
        if value not in actual:
            raise RuntimeError(f"Water heater public pricing missing verified book amount {value}")
    if "water heater replace from $899" in actual.lower():
        raise RuntimeError("Stale water heater replacement price remains")


def apply() -> None:
    reconcile_water_heater()
    for file in ROOT.rglob("*.html"):
        if ".git" not in file.parts:
            scrub_html(file)
    for name in ("llms.txt", "llms-full.txt"):
        file = ROOT / name
        if file.exists():
            text = file.read_text(encoding="utf-8")
            text = text.replace("13 Callaway Drive", PUBLIC_LOCATION).replace(OLD_STREET, PUBLIC_LOCATION)
            file.write_text(text, encoding="utf-8")
