#!/usr/bin/env python3
"""Normalize generated local landing pages after build, before SEO validation.

Do not promise a guaranteed arrival window or universal warranty, and add
helpful contextual links instead of adding thin or duplicate doorway pages.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
WARRANTY = "Warranty terms vary by service, product, and membership; ask for the written warranty for your job."
DISPATCH = "Emergency service is available 24/7. Call (864) 446-8911 for current availability and an arrival estimate."


def update_city(slug: str) -> None:
    file = ROOT / "service-areas" / slug / "index.html"
    content = file.read_text(encoding="utf-8")
    city = "Abbeville" if slug == "abbeville-sc" else "Greenwood"

    # Replace the unverified universal warranty assertions, including JSON-LD
    # FAQ answers, meta tags, and visible text.
    content = re.sub(r"2-year warranty on all work", "written warranty terms by service", content, flags=re.I)
    content = re.sub(r"2-year warranty on every (?:repair and installation|job)", "written warranty terms for qualifying work", content, flags=re.I)
    content = content.replace("2-Year on All Work", "Ask About Warranty")
    content = content.replace("Upfront flat-rate pricing. 2-year warranty. 24/7 dispatch.",
                              "Upfront flat-rate pricing. Written warranty terms. 24/7 dispatch.")
    content = re.sub(
        rf"Every repair and installation we do in {city} carries a 2-year warranty on parts and labor\. If anything fails within that window, we come back and fix it at no charge\.",
        WARRANTY, content,
    )

    # Drop exact minute claims while retaining the emergency-service offering.
    content = re.sub(r"Typical response time from our Abbeville shop is (?:30–45 min|~45 min)\.", DISPATCH, content)
    content = re.sub(r"and can be at a (?:Abbeville|Greenwood) home within (?:30–45 min|~45 min) for like-for-like replacement",
                     "and can discuss scheduling a like-for-like replacement", content)
    content = re.sub(r"most calls within Abbeville city limits get to you in 30 to 45 minutes — often faster",
                     "our team serves customers throughout Abbeville city limits", content)
    content = re.sub(r"with a typical emergency response time of around 45 minutes",
                     "with emergency dispatch available around the clock", content)
    content = re.sub(r"typical response (?:30–45 minutes from Callaway Drive shop|45 minutes)",
                     "call for current dispatch availability", content)
    content = re.sub(r'<span class="city-info-label">Response Time</span><span class="city-info-val">(?:30–45 min|~45 min)</span>',
                     '<span class="city-info-label">Dispatch</span><span class="city-info-val">Call for ETA</span>', content)
    content = re.sub(r"Same-day service is typical\.", "Availability depends on the schedule and the work required.", content)

    # Source-backed navigation: connect locality with the actual service pages
    # and transparent service-call disclosure without manufacturing claims.
    anchor = "</main>"
    extra = f"""  <section class="section" aria-labelledby="local-service-help">
    <div class="container">
      <h2 id="local-service-help">Plumbing help and upfront pricing in {city}, SC</h2>
      <p>Not sure whether to repair or replace? Read our <a href="/services/water-heater-repair-replacement/">water heater repair and replacement guide</a>, learn about <a href="/services/well-pump-repair/">well pump and pressure tank service</a>, or review <a href="/services/drain-cleaning/">drain cleaning</a>. For the service-call schedule and how quotes work, see our <a href="/pricing/">upfront plumbing pricing</a>. The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, or $158 after midnight or on holidays; repairs are quoted separately and approved before work begins.</p>
    </div>
  </section>
"""
    if 'id="local-service-help"' not in content:
        assert anchor in content, f"{file}: missing </main>"
        content = content.replace(anchor, extra + anchor, 1)
    file.write_text(content, encoding="utf-8")


def update_terms() -> None:
    file = ROOT / "terms" / "index.html"
    content = file.read_text(encoding="utf-8")
    content = re.sub(
        r"every repair and installation carries a 2-year warranty on parts and labor from the date of service\. The warranty covers defects in our workmanship and the parts we provided\.",
        "the applicable warranty depends on the product, scope of work, and any purchased membership benefits. The written invoice or estimate states the coverage and exclusions for the specific job.",
        content,
        flags=re.I,
    )
    content = content.replace("2-year warranty on all work", "warranty terms provided in writing")
    file.write_text(content, encoding="utf-8")


def apply() -> None:
    for slug in ("abbeville-sc", "greenwood-sc"):
        update_city(slug)
    update_terms()
