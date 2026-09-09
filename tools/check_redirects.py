#!/usr/bin/env python3
"""Simulate the .htaccess rewrite rules and assert legacy-URL redirect behavior.

Namecheap runs Apache with mod_rewrite. There is no Apache in CI, so this
module implements the subset of mod_rewrite the site's .htaccess actually uses
(RewriteCond on REQUEST_URI / QUERY_STRING / REQUEST_FILENAME / DOCUMENT_ROOT /
HTTPS / HTTP_HOST, and RewriteRule with the L, R=301, NC and OR flags) and
replays the real rule list against the real on-disk tree.

It catches the two failures that actually hurt in Search Console: a legacy URL
that still resolves to a 404, and a rule pair that redirects in a loop.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_HOPS = 5


class Rule:
    def __init__(self, conds, pattern, sub, flags):
        self.conds = conds
        self.flags = flags
        nocase = re.IGNORECASE if "NC" in flags else 0
        self.regex = re.compile(pattern, nocase)
        self.sub = sub

    @property
    def redirect(self) -> bool:
        return any(f == "R" or f.startswith("R=") for f in self.flags)

    @property
    def last(self) -> bool:
        return "L" in self.flags


def parse(htaccess: str):
    """Parse the RewriteCond/RewriteRule pairs out of the .htaccess text."""
    rules, pending = [], []
    for raw in htaccess.splitlines():
        line = raw.strip()
        if line.startswith("RewriteCond"):
            parts = line.split(None, 3)
            flags = []
            if len(parts) == 4:
                flags = parts[3].strip("[]").split(",")
            pending.append((parts[1], parts[2], flags))
        elif line.startswith("RewriteRule"):
            parts = line.split(None, 3)
            flags = parts[3].strip("[]").split(",") if len(parts) == 4 else []
            rules.append(Rule(pending, parts[1], parts[2], flags))
            pending = []
    return rules


def _expand(template: str, uri: str, backrefs) -> str:
    out = template.replace("%{REQUEST_URI}", "/" + uri)
    for i, val in enumerate(backrefs):
        out = out.replace(f"${i + 1}", val or "")
    return out


def _cond_holds(test, pattern, flags, uri, query, backrefs) -> bool:
    subject = _expand(test, uri, backrefs)
    subject = subject.replace("%{QUERY_STRING}", query)
    subject = subject.replace("%{HTTPS}", "on")
    subject = subject.replace("%{HTTP_HOST}", "plumbingparamedic911.com")
    subject = subject.replace("%{DOCUMENT_ROOT}", str(ROOT))
    subject = subject.replace("%{REQUEST_FILENAME}", str(ROOT / uri))

    negate = pattern.startswith("!")
    body = pattern[1:] if negate else pattern

    if body == "-f":
        result = Path(subject).is_file()
    elif body == "-d":
        result = Path(subject).is_dir()
    else:
        nocase = re.IGNORECASE if "NC" in flags else 0
        result = re.search(body, subject, nocase) is not None
    return result != negate


def resolve(rules, uri: str, query: str = ""):
    """Return (status, final_uri, hops) for a request, following 301s."""
    hops = []
    for _ in range(MAX_HOPS):
        path, changed = uri, False
        i = 0
        while i < len(rules):
            rule = rules[i]
            i += 1
            match = rule.regex.search(path)
            if not match:
                continue
            backrefs = match.groups()

            ok, idx = True, 0
            conds = rule.conds
            while idx < len(conds):
                test, pattern, cflags = conds[idx]
                held = _cond_holds(test, pattern, cflags, path, query, backrefs)
                if "OR" in cflags:
                    # Consume the whole OR chain, passing if any member holds.
                    while idx < len(conds) and "OR" in conds[idx][2]:
                        idx += 1
                    if idx < len(conds) and not held:
                        t2, p2, f2 = conds[idx]
                        held = _cond_holds(t2, p2, f2, path, query, backrefs)
                    idx += 1
                    ok = held
                else:
                    ok = held
                    idx += 1
                if not ok:
                    break
            if not ok:
                continue

            target = _expand(rule.sub, path, backrefs)
            if target.endswith("?"):
                target, query = target[:-1], ""
            if rule.redirect:
                new = target.split("://", 1)[-1].split("/", 1)[-1] if "://" in target else target
                new = new.lstrip("/")
                hops.append("/" + new)
                if len(hops) > 1 and hops[-1] == hops[-2]:
                    return "LOOP", "/" + new, hops
                uri, changed = new, True
                break
            path = target.lstrip("/")
            if rule.last:
                break
        if not changed:
            break
    else:
        return "LOOP", "/" + uri, hops

    if len(hops) >= MAX_HOPS:
        return "LOOP", "/" + uri, hops

    served = ROOT / uri
    if served.is_dir() and (served / "index.html").is_file():
        return "200", "/" + uri, hops
    if uri == "":
        return "200", "/", hops
    if served.is_file():
        return "200", "/" + uri, hops
    return "404", "/" + uri, hops


# (request_path, query, expected_final_path). None = only assert it is not a 404.
CASES = [
    ("/about.html", "", "/about/"),
    ("/contact.html", "", "/contact/"),
    ("/services.html", "", "/services/"),
    ("/reviews.html", "", "/reviews/"),
    ("/financing.html", "", "/financing/"),
    ("/faq.html", "", "/faq/"),
    ("/pricing.html", "", "/pricing/"),
    ("/privacy.html", "", "/privacy/"),
    ("/terms.html", "", "/terms/"),
    ("/About/", "", "/about/"),
    ("/Contact/", "", "/contact/"),
    ("/Services/", "", "/services/"),
    ("/services/leak-detection.html", "", "/services/leak-detection/"),
    ("/services/well-pump-repair.html", "", "/services/well-pump-repair/"),
    ("/services/drain-cleaning.html", "", "/services/drain-cleaning/"),
    ("/services/commercial-plumbing.html", "", "/services/commercial-plumbing/"),
    ("/services/slab-leak-repair.html", "", "/services/slab-leak-repair/"),
    ("/services/water-filtration-softener-systems.html", "", "/services/water-filtration-softener-systems/"),
    ("/services/24-7-emergency-plumbing.html", "", "/services/24-7-emergency-plumbing/"),
    ("/services/fixture-installation.html", "", "/services/plumbing-fixture-installation-repair/"),
    ("/services/water-heater-repair.html", "", "/services/water-heater-repair-replacement/"),
    ("/services/backflow-testing.html", "", "/services/backflow-prevention-testing/"),
    ("/service-areas/mccormick-sc.html", "", "/service-areas/mccormick-sc/"),
    ("/service-areas/laurens-sc.html", "", "/service-areas/laurens-sc/"),
    ("/service-areas/greenwood-sc.html", "", "/service-areas/greenwood-sc/"),
    ("/service-areas/anderson-sc.html", "", "/service-areas/anderson-sc/"),
    ("/service-areas/abbeville-sc.html", "", "/service-areas/abbeville-sc/"),
    ("/service-areas/due-west-sc.html", "", "/service-areas/due-west-sc/"),
    ("/service-areas/ninety-six-sc.html", "", "/service-areas/ninety-six-sc/"),
    ("/service-areas/calhoun-falls-sc.html", "", "/service-areas/calhoun-falls-sc/"),
    ("/service-areas/iva-lake-secession-sc.html", "", "/service-areas/iva-lake-secession-sc/"),
    ("/service-areas/savannah-lakes-village-sc.html", "", "/service-areas/savannah-lakes-village-sc/"),
    ("/service-areas/iva-sc/", "", "/service-areas/iva-lake-secession-sc/"),
    ("/service-areas/starr-sc/", "", "/service-areas/anderson-sc/"),
    ("/site/f4d507af/home/", "", "/"),
    ("/site/f4d507af/", "", "/"),
    ("/cart/", "", "/pricing/"),
    ("/checkout/", "", "/pricing/"),
    ("/shop/", "", "/pricing/"),
    ("/", "add-to-cart=1234", "/"),
    ("/pricing/", "add-to-cart=99", "/pricing/"),
    ("/sitemap_index.xml", "", "/sitemap.xml"),
    ("/wp-sitemap.xml", "", "/sitemap.xml"),
    ("/page-sitemap.xml", "", "/sitemap.xml"),
    ("/post-sitemap.xml", "", "/sitemap.xml"),
    ("/sitemap.txt", "", "/sitemap.xml"),
    ("/costs/water-heater/", "", "/pricing/"),
    ("/blog/", "", "/faq/"),
    ("/index.html", "", "/"),
    # Canonical URLs must be served directly, never redirected.
    ("/", "", "/"),
    ("/about/", "", "/about/"),
    ("/services/", "", "/services/"),
    ("/services/drain-cleaning/", "", "/services/drain-cleaning/"),
    ("/service-areas/anderson-sc/", "", "/service-areas/anderson-sc/"),
    ("/sitemap.xml", "", "/sitemap.xml"),
    ("/robots.txt", "", "/robots.txt"),
    ("/404.html", "", "/404.html"),
    ("/llms.txt", "", "/llms.txt"),
    ("/css/style.css", "", "/css/style.css"),
]

NO_REDIRECT = {"/", "/about/", "/services/", "/services/drain-cleaning/",
               "/service-areas/anderson-sc/", "/sitemap.xml", "/robots.txt",
               "/404.html", "/llms.txt", "/css/style.css"}


def main() -> int:
    rules = parse((ROOT / ".htaccess").read_text(encoding="utf-8"))
    failures = []

    for path, query, expected in CASES:
        status, final, hops = resolve(rules, path.lstrip("/"), query)
        label = path + (("?" + query) if query else "")

        if status == "LOOP":
            failures.append(f"{label}: redirect loop {' -> '.join(hops)}")
            continue
        if status == "404":
            failures.append(f"{label}: resolves to 404 (ended at {final})")
            continue
        if expected and final != expected:
            failures.append(f"{label}: landed on {final}, expected {expected}")
            continue
        if path in NO_REDIRECT and not query and hops:
            failures.append(f"{label}: canonical URL should not redirect, got {' -> '.join(hops)}")
            continue
        if len(hops) > 1:
            failures.append(f"{label}: {len(hops)} redirect hops ({' -> '.join(hops)}); should be one")

    # Every sitemap URL must be served directly with no redirect hop.
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for loc in re.findall(r"<loc>\s*(.*?)\s*</loc>", sitemap):
        uri = re.sub(r"^https?://[^/]+", "", loc)
        status, final, hops = resolve(rules, uri.lstrip("/"))
        if status != "200" or hops:
            failures.append(f"sitemap URL {uri}: status {status}, hops {' -> '.join(hops) or 'none'}")

    if failures:
        print("REDIRECT VALIDATION FAILED")
        for f in failures:
            print(" - " + f)
        return 1

    print(f"Redirect validation passed: {len(CASES)} legacy/canonical routes, "
          f"{sitemap.count('<loc>')} sitemap URLs, no loops, no multi-hop chains.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
