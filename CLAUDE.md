# CLAUDE.md — Plumbing Paramedic 911 (site build)

Codebase reference for AI assistants working on this repository.

---

## Project Overview

**Plumbing Paramedic 911** — a static HTML website for a licensed SC Master
Plumber based in Abbeville, SC. This repository is a **generator-based** static
site: most pages are produced by a single Python script from a source-of-truth
dict, then committed alongside the generated output.

- **Build tool** — `tools/build.py` (single-file Python 3, stdlib only)
- **Runtime** — pure static HTML/CSS/JS served by Apache
- **No CSS/JS framework** — hand-crafted CSS, vanilla JS
- **No backend or database** — everything is static
- **Deployment** — no CI workflow yet; deploy by uploading the repo contents to
  Namecheap shared hosting via FTP/SFTP

There is a companion repository (`8911`) that carries the currently-shipped,
richer, hand-authored version of this site. **This repo is the newer
generator-driven implementation**; if the two disagree, treat `8911` as the
production truth unless the user says otherwise.

### Business Facts (canonical NAP — see `SEO_EXTERNAL_ACTIONS.md`)

```
Name:    Plumbing Paramedic 911
Owner:   Eric Callaway, SC Master Plumber (in the trade since 1996, LLC since 2015)
Address: 13 Callaway Dr, Abbeville, SC 29620
Phone:   (864) 446-8911   (tel:+18644468911)
Email:   plumbingparamedic911@gmail.com
URL:     https://plumbingparamedic911.com  (non-www, HTTPS)
GTM:     GTM-T33LBNF
GA4:     G-54J49X5XJP
```

---

## Repository Structure

```
/
├── index.html                              # Homepage (hand-authored, NOT regenerated)
├── sitemap.xml
├── robots.txt
├── .htaccess                               # Apache rewrite/caching/security rules
├── site.webmanifest                        # PWA manifest
├── llms.txt                                # AI-readable business reference
├── b2290a30b99296ce58d8329f955dec49.txt    # IndexNow key file
│
├── ASSETS_NEEDED.md                        # Checklist of image files still required
├── SEO_EXTERNAL_ACTIONS.md                 # Off-site tasks (GBP, citations, aggregators)
│
├── css/
│   └── style.css                           # Single stylesheet (~24 KB, ~315 lines)
├── js/
│   └── app.js                              # Nav toggle + minor UI JS
│
├── about/index.html                        # Generated
├── contact/index.html                      # Generated
├── faq/index.html                          # Generated
├── financing/index.html                    # Generated
├── pricing/index.html                      # Generated
├── reviews/index.html                      # Generated
├── privacy/index.html                      # Generated
├── terms/index.html                        # Generated
│
├── services/                               # Service hub + one subdir per service
│   ├── index.html                          # Generated hub
│   ├── 24-7-emergency-plumbing/index.html  # Hand-authored (per build.py docstring)
│   ├── backflow-prevention-testing/index.html
│   ├── commercial-plumbing/index.html
│   ├── drain-cleaning/index.html
│   ├── leak-detection/index.html
│   ├── plumbing-fixture-installation-repair/index.html
│   ├── water-heater-repair-replacement/index.html
│   └── well-pump-repair/index.html
│
├── service-areas/                          # Area hub + one subdir per city
│   ├── index.html
│   ├── abbeville-sc/index.html
│   ├── anderson-sc/index.html
│   ├── calhoun-falls-sc/index.html
│   ├── due-west-sc/index.html
│   ├── greenwood-sc/index.html
│   ├── laurens-sc/index.html
│   ├── mccormick-sc/index.html
│   └── ninety-six-sc/index.html
│
└── tools/
    └── build.py                            # Static-site generator (~1,900 lines)
```

---

## How the Build Script Works

`tools/build.py` is a single Python 3 file (stdlib only — no dependencies). It
holds the entire site's content in two large in-file dicts and renders each
page directly into its target `directory/index.html`.

```
tools/build.py
├── Shared HTML chunks
│   ├── NAV_HTML             (top bar, main nav, mobile nav)
│   └── FOOTER_HTML
├── Helpers
│   ├── nav(active)          — inject the active-link class into NAV_HTML
│   ├── head(title, description, path, og_image, extra_ld)
│                            — full <head>, meta, OG/Twitter, JSON-LD injection
│   ├── breadcrumb_ld(items) — BreadcrumbList JSON-LD
│   ├── faq_ld(faqs) / faq_html(faqs)
│   └── breadcrumb_html(items)
├── SERVICES = { slug: { title, description, h1, badge, intro, schema_id,
│                        service_type, schema_desc, price_range, price_note,
│                        og, body, faqs, … } }
├── CITIES = { slug: { … city hero + local content … } }
├── Renderers
│   ├── render_service_page(slug, s)
│   ├── render_city_page(slug, c)
│   ├── render_services_hub()
│   ├── render_areas_hub()
│   ├── render_about() / render_contact() / render_pricing()
│   ├── render_faq() / render_reviews() / render_financing()
│   └── render_legal(slug, title, body_html)      — privacy, terms
└── main()                                        — iterate + call write()
```

**Not regenerated by `build.py`** (hand-authored, richer content):
- `/index.html` (homepage)
- `/services/24-7-emergency-plumbing/index.html`

Everything else in `about/`, `contact/`, `faq/`, `financing/`, `pricing/`,
`reviews/`, `privacy/`, `terms/`, `services/*`, `service-areas/*` is regenerated
on every build.

### Running the build

```bash
python3 tools/build.py
```

- Requires Python 3.9+ (uses `str | None` union syntax)
- Zero third-party dependencies
- Writes into the repo. Commit the generated files alongside content changes
  so the deployed FTP copy matches the repo.

### Editing content

- **Service copy** → edit the `SERVICES` dict entry, then rerun the build
- **City copy** → edit the `CITIES` dict entry, then rerun the build
- **Utility pages** (about/contact/pricing/faq/reviews/financing/privacy/terms)
  → edit the corresponding `render_*` function
- **Nav, footer, `<head>` boilerplate** → edit `NAV_HTML`, `FOOTER_HTML`, or the
  `head()` helper — a single change propagates to every generated page on rebuild
- **Homepage** and **`/services/24-7-emergency-plumbing/`** → edit the HTML directly

---

## Code Conventions

### HTML (both generated and hand-authored)

- One page per directory: `directory/index.html`
- Skip link, semantic landmarks, one `<h1>` per page
- Canonical tag, meta description, `theme-color` (`#0D47A1` on this build —
  note the blue vs. red used on the `8911` build), OG + Twitter Card
- **GTM snippet inlined** in every `<head>` (container `GTM-T33LBNF`)
- **NOTE — bug in `tools/build.py`**: the inlined GTM snippet contains a typo
  (`'schript'` instead of `'script'`) that breaks the tag on every generated
  page. When editing content, fix this at the source in `NAV_HTML`/`head()` in
  `build.py` (grep for `schript`) rather than post-editing generated HTML.
- Trailing slashes ARE used on internal links here (e.g., `/services/`) —
  `.htaccess` forces trailing slashes on directory URLs (opposite of the `8911`
  repo). Match the existing convention.

### CSS

- All styles live in `css/style.css` (singular — do not create a second file)
- CSS custom properties for brand color, spacing, and radius
- Mobile-first with `@media (min-width: ...)` breakpoints

### JavaScript

- `js/app.js` — hamburger nav toggle, dropdown behavior, minor UI helpers
- IIFE + `'use strict'`
- **Do not add frameworks** (React, Vue, jQuery)

### URL Structure

- Canonical URLs are **non-www** and use **HTTPS**
- Directory URLs use a **trailing slash** on this build (`.htaccess` enforces it)
- Kebab-case slugs

---

## Structured Data (JSON-LD)

Every generated page carries a JSON-LD block built by `head()` + `breadcrumb_ld()`
+ per-page schema (Service/Place/FAQPage). The `LocalBusiness` node's `@id` is
referenced by service schema via `provider.@id`.

Do not remove or restructure JSON-LD in either the generator or generated files.

---

## Apache / .htaccess

Handles, in order:
1. `DirectoryIndex index.html`, `AddDefaultCharset UTF-8`, `Options -Indexes`
2. Force HTTPS
3. Force non-www (`www.plumbingparamedic911.com` → apex)
4. Force trailing slash on directory-style URLs (skip files with extensions)
5. Browser caching and security headers

Do not remove or reorder rules — mod_rewrite condition order matters.

---

## Deployment

- **No GitHub Actions workflow** in this repo yet. Deployment is manual FTP
  upload to Namecheap.
- Upload the full repo tree except `.git`, `tools/`, `*.md` planning files.
- Suggested setup: mirror the `8911` repo's `.github/workflows/ftp-deploy.yml`
  (lftp with STARTTLS explicit TLS on port 21) if/when CI deploy is wanted.

---

## Assets Still Required

`ASSETS_NEEDED.md` lists the image/icon files the HTML references but that are
not in the repo (favicons, `/logo.png`, `/og-image.jpg`, per-page OG images
under `/images/og/`). Upload those to the deployed site before shipping.

---

## Off-Site SEO Actions

`SEO_EXTERNAL_ACTIONS.md` is a checklist of manual off-repo tasks (kill the
`.org` domain, fix Facebook/YP/Yelp/Birdeye/HomeAdvisor listings, submit
sitemap to GSC/Bing, GBP updates). These are **not** code changes — treat that
file as a task list, not a spec that affects HTML output.

---

## Git Branch Conventions

- Feature branches: `claude/[description]-[id]` (e.g., `claude/claude-md-docs-ovgxyj`)
- Merge into main via PR; no automatic deploy yet

---

## What NOT to Do

- Do not add npm, `package.json`, or a JS build toolchain
- Do not introduce CSS/JS frameworks
- Do not commit real GTM/GA/Meta Pixel/Vapi API keys
- Do not hand-edit generated pages when the content lives in the `SERVICES` /
  `CITIES` dict — edit the dict and rerun the build
- Do not remove the hand-authored homepage or emergency-plumbing page — they
  are intentionally outside the generator
- Do not use `www.` in any URLs (site is non-www)
- Do not drop the trailing slash from directory URLs on this build
- Do not remove JSON-LD structured data from any page
