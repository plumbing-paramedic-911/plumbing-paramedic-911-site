# Plumbing Paramedic 911 — Super Site Migration Map

Canonical production repository: `plumbing-paramedic-911/plumbing-paramedic-911-site`
Production branch: `main`
Legacy source reviewed: `plumbing-paramedic-911/8911` at frozen branch `archive/pre-consolidation-2026-08-29`

## Migration rule

Do not merge the old repository wholesale. The former site contains useful content and historical URLs, but also old pricing, an older theme/CSS system, legacy deployment workflows, duplicate intent pages and claims that should not be reintroduced. Useful content is rebuilt through the current generator/design/schema layer and every old route is either preserved deliberately or permanently consolidated.

## Preserved as first-class canonical pages

These former-production URLs carry distinct service or local-search intent and are generated/source-controlled by the canonical release:

- `/services/sewer-line-repair/`
- `/services/pipe-repair-repiping/`
- `/services/toilet-repair-installation/`
- `/services/gas-line-services/`
- `/services/hydro-jetting/`
- `/services/sump-pump-services/`
- `/services/garbage-disposal-repair/`
- `/drain-cleaning-abbeville-sc/`
- `/sewer-line-repair-abbeville-sc/`
- `/emergency-plumber-greenwood-sc/`

All restored pages use the current NAP, non-www HTTPS canonicals, current schema graph, current blue/green design and current service-call policy. Exact legacy copy is not copied blindly.

## Preserved digital-guide authority assets

The legacy deploy left these live on the Namecheap document root even though the canonical Git repository did not own the files. They are now generated and source-controlled by the canonical release so a clean host migration will not lose them:

- `/guides/`
- `/guides/sc-homeowner-plumbing-survival-guide/` — $19
- `/guides/well-pump-owners-manual-upstate-sc/` — $17
- `/guides/water-heater-buyers-guide-sc/` — $14
- `/guides/drain-maintenance-playbook/` — $9
- Existing complete-bundle Gumroad checkout remains $48.

Product pages retain their historical canonical URLs and Product/Offer structured data while removing unsupported savings claims and old-site styling.

## Deliberate consolidations kept as 301 redirects

These routes are not restored because the stronger current target already covers the same intent and restoring both could split signals or create thin/duplicate pages:

- `/blog/` → `/faq/`
- `/blog/signs-water-heater-failing/` → `/services/water-heater-repair-replacement/`
- `/blog/how-to-shut-off-water-in-emergency/` → `/services/24-7-emergency-plumbing/`
- `/costs/*` → `/pricing/` (old cost articles carried stale price data)
- `/service-areas/iva-sc/` → `/service-areas/iva-lake-secession-sc/`
- `/service-areas/starr-sc/` → `/service-areas/anderson-sc/`
- `/backflow-testing-abbeville-sc/` → `/services/backflow-prevention-testing/`
- `/commercial-plumber-greenwood-sc/` → `/services/commercial-plumbing/`

The existing `.html` migration redirects remain in `.htaccess` for older indexed URL variants.

## Already-canonical high-intent pages retained

The newer canonical release already owns these service × market pages and they remain unchanged except for shared navigation/internal-link improvements:

- `/well-pump-repair-mccormick-sc/`
- `/well-pump-repair-iva-lake-secession-sc/`
- `/drain-cleaning-greenwood-sc/`
- `/water-heater-repair-greenwood-sc/`
- `/water-heater-repair-anderson-sc/`
- `/emergency-plumber-abbeville-sc/`

## Deployment safety

The old `8911` Namecheap and Cloudflare Pages auto-deploys are disabled. Do not re-enable them. The canonical `main` branch remains the only production website source.

The Namecheap document root is currently known to contain historical files left by the old deploy because the canonical deployment intentionally does not run a blanket remote delete. Do **not** enable `mirror --delete` until the full remote inventory is compared against the canonical public manifest. Host-managed files such as `.well-known` must never be removed blindly.

## Release gates

A super-site release must fail if:

- a preserved historical route has no source-controlled generated file;
- an intentional consolidation loses its 301 rule;
- a sitemap URL has no deployable file or no static internal link;
- duplicate titles or meta descriptions are introduced;
- JSON-LD becomes invalid;
- retired `$150` after-hours, waived-service-call or obsolete-hours wording returns;
- the current `$79 / $99 / $158` service-call policy is displaced on pricing-critical pages.

This file is the route-level record for future AI/developer sessions. When an old URL is found, classify it here before restoring, redirecting or deleting it.