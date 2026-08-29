# Plumbing Paramedic 911 — CANONICAL LIVE WEBSITE

This repository is the **single source of truth for the live Plumbing Paramedic 911 website**.

## Production

- Live domain: `https://plumbingparamedic911.com`
- Canonical repository: `plumbing-paramedic-911/plumbing-paramedic-911-site`
- Production branch: `main`
- Deployment workflow: `.github/workflows/deploy-seo-repair.yml`
- Hosting target: Namecheap shared hosting over FTPS

All production website changes should be made here through a branch/PR and merged into `main` only after the SEO/AEO quality gate passes.

## Repository map

| Repository | Purpose | Website status |
|---|---|---|
| `plumbing-paramedic-911/plumbing-paramedic-911-site` | Current generator-driven website, SEO/AEO release build, pricing policy, deployment pipeline | **LIVE / CANONICAL** |
| `plumbing-paramedic-911/8911` | Former hand-authored website; contains historical pages, SEO work, redirects, GBP notes and older integrations | **LEGACY ARCHIVE — DO NOT DEPLOY** |
| `plumbing-paramedic-911/plumbing-paramedic-911` | GitHub profile/config repository | Not a website deployment source |
| `plumbing-paramedic-911/github-slideshow` | Old GitHub training/slideshow repository | Unrelated to Plumbing Paramedic production |

## Legacy-content rule

Do **not** merge the `8911` repository wholesale into production. It contains older business copy, pricing, schema, routes and deployment assumptions. Useful material should be migrated selectively into this repository, normalized to the current NAP/pricing/schema, tested, and merged by PR.

The legacy repo's automatic Namecheap and Cloudflare Pages deploy workflows were disabled on 2026-08-29 so it cannot overwrite production. A pre-change snapshot is preserved in `8911` as `archive/pre-consolidation-2026-08-29`.

## Current pricing policy

The production release builder is the authority for current service-call wording:

- $79 Monday–Friday 9 AM–5 PM
- $99 after hours and weekends
- $158 after midnight or on holidays
- Repair/installation work priced separately and approved before work begins

Do not restore legacy `$150 after-hours surcharge`, waived-service-call, or free-diagnostic copy.
