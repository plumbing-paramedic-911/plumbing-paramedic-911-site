# CLAUDE.md — Plumbing Paramedic 911 canonical production site

Codebase instructions for AI assistants and developers working in this repository.

## Canonical repository — read this first

This repository, `plumbing-paramedic-911/plumbing-paramedic-911-site`, is the **single source of truth for the live website at https://plumbingparamedic911.com**.

- Production branch: `main`
- Production host: Namecheap shared hosting
- Production deploy: `.github/workflows/deploy-seo-repair.yml`
- PR quality gate: `.github/workflows/seo-quality.yml`
- A push to `main` builds, validates, uploads over FTPS, and verifies production.

The private repository `plumbing-paramedic-911/8911` is a **legacy website archive**. It was the former production site, but its automatic Namecheap and Cloudflare Pages deployment workflows were disabled on 2026-08-29. Do not treat `8911` as production truth and do not make new production website changes there.

Useful legacy content may be migrated selectively from `8911`, but it must be normalized to current business facts, pricing, schema and URL rules and merged here through a PR. Never merge the legacy repository wholesale.

Other repositories in the account are not production website sources:
- `plumbing-paramedic-911/plumbing-paramedic-911` — GitHub profile/config repository.
- `plumbing-paramedic-911/github-slideshow` — old GitHub training repository.

## Project overview

Plumbing Paramedic 911 is a generator-assisted static HTML/CSS/JS website for a plumbing contractor based in Abbeville, South Carolina.

- Main build source: `tools/build.py`
- Production release builder: `tools/release_build.py`
- Current pricing normalization: `tools/current_pricing_overrides.py`
- Local high-intent page generation: `tools/local_money_pages.py`
- Internal-link validation: `tools/check_internal_links.py`
- Runtime: static HTML/CSS/vanilla JS on Apache
- No npm/webpack/framework build is required.

Most generator-owned pages are recreated during the production release. The homepage and some richer pages are hand-authored but may be patched by the release builder before deployment. Make source changes in the correct source layer so a future build does not restore stale content.

## Canonical business facts

```
Business: Plumbing Paramedic 911
Address: 13 Callaway Dr, Abbeville, SC 29620
Phone: (864) 446-8911
Email: plumbingparamedic911@gmail.com
Website: https://plumbingparamedic911.com
Hours: 24/7 emergency dispatch
GTM: GTM-T33LBNF
GA4: G-54J49X5XJP
```

Use the non-www HTTPS domain in canonical URLs.

## Current service-call pricing policy

This is the current production service/diagnostic-call policy unless the owner explicitly changes it:

- $79 Monday–Friday, 9 AM–5 PM
- $99 after hours and weekends
- $158 after midnight or on holidays
- Repair/installation work is priced separately and approved before it begins.

Do not restore obsolete copy such as:
- `$150 after-hours surcharge`
- `service call fee is waived`
- `free diagnostic`
- `free up-front estimates before any work begins` when referring to a dispatched service/diagnostic visit
- old 8 AM–6 PM service-call windows

`tools/current_pricing_overrides.py` and the production release validation contain guards for stale pricing language. Keep those protections intact.

## Repository structure

Important top-level areas:

```
/
├── index.html
├── .htaccess
├── sitemap.xml
├── robots.txt
├── llms.txt
├── css/style.css
├── js/app.js
├── about/
├── contact/
├── faq/
├── financing/
├── pricing/
├── reviews/
├── privacy/
├── terms/
├── services/
├── service-areas/
├── tools/
└── .github/workflows/
```

The current release also includes high-intent service × market landing pages generated or maintained through the release tooling. Preserve indexed routes or add explicit 301 redirects when consolidating old URLs.

## Build and validation

For a production-equivalent local validation, run:

```bash
python3 tools/release_build.py
python3 tools/check_internal_links.py
```

The release builder regenerates generator-owned pages, creates local money pages, applies the current pricing policy, strengthens internal links, updates required sitemap entries and validates critical SEO/AEO requirements.

Do not rely on editing only a generated HTML file if the underlying generator will recreate it differently on the next release.

## Deployment

Production deployment is automatic from `main` through `.github/workflows/deploy-seo-repair.yml`.

The workflow:
1. Checks out the website.
2. Runs the production release build and internal-link validation.
3. Validates FTPS secrets.
4. Uploads the validated site to Namecheap over FTPS.
5. Fetches key live URLs and verifies production behavior.
6. Confirms deployment scope.

Do not add another repository or branch that can upload to the same production target. One production writer is intentional.

## Git workflow

- Create a focused feature/fix branch from `main`.
- Make source changes and run the release validation.
- Open a PR to `main`.
- Let `SEO AEO Quality Gate` pass.
- Merge only after the change is understood and safe.
- The merge to `main` triggers the production deployment.

## Legacy 8911 migration

`8911` contains useful historical material that is not all present here, including additional service pages, city/service landing pages, blog/resource content, GBP/SEO notes and older voice-agent code. The migration tracker is GitHub issue #13 in this repository.

When migrating a legacy page:
1. Check whether its URL has historical/indexed value.
2. Port useful content into this repository's current layout/generator conventions.
3. Replace stale NAP, pricing, schema, hours, links and claims.
4. Preserve the old URL or add a permanent redirect to the best current equivalent.
5. Run the SEO/AEO quality gate before merge.

Do not copy the legacy deployment workflows, old red-theme conventions, stale pricing or obsolete structured data into production.

## SEO/AEO rules

- Canonical domain is `https://plumbingparamedic911.com` (non-www).
- Keep unique page titles/descriptions and valid JSON-LD.
- Preserve LocalBusiness/Service entity consistency.
- Keep important pages statically linked; avoid orphaned sitemap URLs.
- Maintain crawl-safe redirects in `.htaccess` for retired/legacy URLs.
- `llms.txt` must reflect current business/pricing facts.
- Do not invent review counts, ratings, licensing details, guarantees or response times.

## Code conventions

- Static HTML5, CSS and vanilla JavaScript only unless a deliberate architecture change is approved.
- Keep `css/style.css` as the primary stylesheet.
- Keep `js/app.js` as the main site JavaScript unless a feature specifically requires another asset.
- Use accessible semantic HTML and one meaningful H1 per page.
- Do not introduce a JS framework merely for convenience.
- Do not expose secrets or API keys in client-side files or repository content.

## What not to do

- Do not deploy from `8911`.
- Do not treat `8911` as production truth.
- Do not add a second automatic Namecheap production deployment source.
- Do not wholesale-merge old repositories.
- Do not restore stale pricing wording.
- Do not bypass `tools/release_build.py` for production validation.
- Do not remove redirects or change indexed URL structure without checking SEO impact.
- Do not remove JSON-LD, analytics or lead-capture integrations without understanding the consequence.

If documentation conflicts, this file and the root `README.md` describe the current repository/deployment authority. Historical planning documents must not override them.
