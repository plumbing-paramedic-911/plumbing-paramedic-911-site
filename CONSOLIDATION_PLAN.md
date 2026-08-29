# Repository Consolidation Status — Plumbing Paramedic 911

_Last updated: 2026-08-29_

This document replaces the earlier migration plan that described `8911` as the live production source. That information is now historical and must not be used to choose a deployment repository.

## Current production authority

The canonical live website repository is:

`plumbing-paramedic-911/plumbing-paramedic-911-site`

Production details:
- Domain: `https://plumbingparamedic911.com`
- Branch: `main`
- Build: `tools/release_build.py`
- PR validation: `.github/workflows/seo-quality.yml`
- Production deployment: `.github/workflows/deploy-seo-repair.yml`
- Host: Namecheap shared hosting over FTPS

This repository is the only GitHub codebase that should automatically write to the production website.

## Repository map

### 1. `plumbing-paramedic-911/plumbing-paramedic-911-site`

**Status: CANONICAL / LIVE**

This is the generator-assisted blue/green website with the current SEO/AEO release process, current pricing policy, city/service architecture, local landing pages, production validation and Namecheap deployment.

All new production website work belongs here.

### 2. `plumbing-paramedic-911/8911`

**Status: LEGACY WEBSITE ARCHIVE — DO NOT DEPLOY**

`8911` was the former hand-authored production site. It contains useful historical content, additional service pages, root-level local SEO landing pages, blog/resource content, GBP/SEO notes, old voice-agent code, redirects and other material worth reviewing.

On 2026-08-29:
- a frozen backup branch was created at `archive/pre-consolidation-2026-08-29`;
- the old automatic Namecheap FTPS deploy was disabled;
- the old Cloudflare Pages deploy was disabled;
- a root README was added marking the repository as legacy.

Do not turn either deployment workflow back on. Do not merge this repository wholesale into production because it also contains stale pricing, older schema/content assumptions, old routes and obsolete deployment conventions.

### 3. `plumbing-paramedic-911/plumbing-paramedic-911`

**Status: PROFILE/CONFIG REPOSITORY**

This is not a Plumbing Paramedic website deployment source and is not part of the website consolidation.

### 4. `plumbing-paramedic-911/github-slideshow`

**Status: UNRELATED OLD TRAINING REPOSITORY**

This is an old GitHub training/slideshow repository from 2019. It has nothing to merge into the Plumbing Paramedic production website.

## Safe consolidation strategy

We are not combining all repositories into one giant Git history. That would create more risk and confusion, not less.

The safe strategy is:
1. Keep `plumbing-paramedic-911-site` as the only production repository.
2. Keep `8911` as a read-only-in-practice historical archive with deployments disabled.
3. Selectively migrate only useful `8911` content into the canonical repository.
4. Normalize migrated content to the current business record, pricing policy, schema, visual system and URL conventions.
5. Preserve valuable historical URLs or add 301 redirects.
6. Validate every migration through the SEO/AEO quality gate.
7. Never create a second automatic production writer.

## Legacy migration tracker

GitHub issue #13 in the canonical repository tracks the useful `8911` material that still needs review. Major candidates include:
- garbage disposal repair;
- gas line services;
- hydro-jetting;
- pipe repair / repiping;
- sewer line repair;
- sump pump services;
- toilet repair / installation;
- Starr-area content;
- historical Iva URL reconciliation;
- additional root-level service × city landing pages;
- useful blog/resource pages;
- GBP and SEO research notes;
- older voice-agent code that may still be relevant.

Each item should be migrated as a focused PR rather than copied wholesale.

## Current pricing authority

The production service/diagnostic-call policy is:
- $79 Monday–Friday 9 AM–5 PM;
- $99 after hours and weekends;
- $158 after midnight or holidays;
- repair/installation pricing is separate and approved before work begins.

Do not restore legacy `$150 after-hours surcharge`, waived-service-call, free-diagnostic or old 8 AM–6 PM wording from `8911` or older site content.

## Remaining deployment cleanup

Two deployment-related items still deserve verification:

1. **Cloudflare/cache/origin behavior.** A public crawl has recently continued to surface stale homepage pricing even after the canonical Namecheap deployment succeeded. Do not assume that is resolved until the origin/cache path is verified and the public page is rechecked.
2. **GitHub Pages on the canonical repository.** GitHub has shown a Pages build/deployment workflow for this public repository. Treat that as a possible preview/alternate deployment until its configuration is inspected. It must not become a competing custom-domain production source.

## Definition of done

Repository consolidation is complete when:
- only `plumbing-paramedic-911-site/main` can automatically deploy the production site;
- `8911` remains archived with deploys disabled;
- the useful legacy pages have either been migrated or intentionally retired with redirects;
- stale production documentation no longer points developers/AI agents to `8911`;
- GitHub Pages/Cloudflare preview deployments cannot compete with the production domain;
- the live homepage and pricing pages show the same current service-call policy;
- Search Console does not show new 404/indexing damage from the consolidation.

For current authority, read the root `README.md` and `CLAUDE.md` in this repository before historical notes.
