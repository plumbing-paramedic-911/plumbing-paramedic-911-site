# Consolidation Plan — one dominant site to rule them all

## Where we are today (2026-06-30 / 2026-07-08+)

Three separate versions of "the site" have been in play, and it's caused a lot of the confusion:

| # | What | Where | Theme | Pages | Status |
|---|------|-------|-------|-------|--------|
| 1 | **8911** (`plumbing-paramedic-911/8911`) | Private GitHub repo | Blue / green | ~60 (hand-authored) | **Currently deployed to plumbingparamedic911.com** — this is production truth, per PR #5's CLAUDE.md |
| 2 | **plumbing-paramedic-911-site** (this repo) | Public GitHub | Blue / green | 27 (generator-driven, cleaner AEO) | Newer, meant to replace 8911; not yet deployed |
| 3 | The "red site" the user remembers | Unknown host (Cloudflare Pages preview? WordPress attempt? Vercel? separate mock?) | Red | Unknown | Off the table — we're not keeping this |

The user's stated goal: **collapse all three into one canonical blue/green site**, keep the AEO/SEO strength that had Search Console going in the right direction, and layer on CRM + voice + chatbot.

## Which repo becomes the winner?

**This repo (`plumbing-paramedic-911-site`)** should be the canonical codebase going forward. Why:

- Its generator (`tools/build.py`) is the maintainable way to update 27+ pages without hand-editing each one.
- Its schema (`@graph` in the homepage with shared `@id`s across every sub-page) is materially better for AI-engine citation than hand-authored per-page schema in 8911.
- Its `.htaccess` has the current hardened security headers (HSTS preload, CSP, X-Frame-Options, COOP/CORP).
- The 27 pages are locally-grounded and voice-search-ready (H2-as-voice-query + 25–35-word answers wrapped in FAQPage schema).

But **8911 has content this repo doesn't**: the ~30 extra pages, the AEO research data, the passive-income references, whatever the pricing calculator has evolved into over there, and the actual production lead-capture wiring on the live site.

**So the merge direction is: keep this repo as the shell, absorb the missing content from 8911.**

## Blocker: I can't read 8911 from this session

My GitHub MCP access is scoped to `plumbing-paramedic-911-site` only. Attempts to read `8911` will be denied. To move forward, one of the following has to happen:

1. **Open a new Claude Code session with access to both repos.** From there I can pull pages, schema, research files, and copy from 8911 into this repo, deduplicate, and push a consolidated version.
2. **Export 8911 as a ZIP** and upload it into this session. I'll extract, diff, and merge.
3. **Rebuild missing pages from source data pasted in chat.** Slowest, but works.

Recommendation: **option 1**. Cleanest and fastest.

## What the consolidated site will contain

Assuming we can get to 8911's content, the final state is:

### Content
- All 27 pages already here (home, 8 services, 8 city pages, 2 hubs, about/contact/faq/reviews/financing/pricing/privacy/terms)
- Additional pages from 8911 (any service/city/blog/resource pages not present here)
- The AEO research findings (the "well on its way in Search Console" version) baked into the visible copy, not just marketing collateral
- Passive-income / affiliate / product references — surfaced as a `/shop/` or `/tools/` section with proper `Product` schema so Google Shopping and AI engines can cite it
- The Cutter Jax + Prime mascot section (already added via PR #3)

### Technical layer
- Blue/green theme (already the current CSS — no red)
- Generator-driven so regenerating doesn't lose GTM (now baked into `tools/build.py`), GA4, schema, or meta
- 27+ URLs with proper canonicals + sitemap.xml + llms.txt + robots.txt + IndexNow
- Master `@graph` JSON-LD with shared `@id`s so AI engines see one entity
- Hardened `.htaccess` with CSP + HSTS-preload + COOP/CORP
- Voice-optimized FAQ blocks on every service and city page

### CRM dashboard (protected admin area)
- Auth-gated `/admin/` section only Eric can see
- Lead pipeline: form submissions from the site land here with source page, timestamp, service requested, contact info
- Simple kanban: New → Quoted → Scheduled → Completed → Follow-up
- Notes/tasks per lead
- Cheapest tenable stack:
  - **HubSpot Free CRM** embedded — near-zero effort, hosted dashboard, forms convert into contacts automatically. Recommended for phase 1.
  - Alternative if HubSpot is too limiting later: Supabase (Postgres + Auth + Storage) with a custom SPA `/admin/` UI. That MCP is available if we go that direction.

### Voice + chatbot
- **Chatbot** — recommended stack: hosted widget (Tidio, Crisp, or HubSpot Live Chat) for phase 1 — drop-in script tag, no backend, ~$0–50/mo. Phase 2 upgrade: swap to a custom widget that calls the Claude API through a Cloudflare Worker for full control and per-message cost.
- **Voice** — recommended phase 1: browser-native Web Speech API "Speak your problem" button that transcribes and pre-fills the lead form. Phase 2 upgrade: Vapi.ai voice AI that answers the phone number and takes leads (~$0.05–$0.15/min).

## What we do RIGHT NOW without waiting on 8911 access

1. ✅ **Fix the GTM regeneration footgun** (done — `tools/build.py` now bakes GTM head+noscript into every generated page; regenerating no longer wipes it out).
2. ✅ **Keep the security headers hardened** in `.htaccess` (done in the initial build; carried forward on PR #4).
3. ✅ **Ship PR #4** — the GTM `'schript'` typo fix on the homepage. Once merged and re-deployed, the live site's homepage GTM stops silently failing.
4. Write this plan (you're reading it).
5. When user is ready: kick off the new session with access to `8911` so we can start migrating content.

## What we need from the user before phase 2 starts

- Confirmation of which repo becomes canonical (this one, unless they say otherwise)
- Access to `8911` (new Claude Code session OR a ZIP export)
- HubSpot account email so we can start the free CRM tier
- Choice on chatbot provider (Tidio / Crisp / HubSpot Live Chat / custom)
- Passive-income products list — what's being sold/referenced, affiliate links, prices
- Any Search Console data they can export (Performance report as CSV) so we know which keywords/URLs to protect during migration

## URL preservation (SEO safety)

Because the live site had ranking momentum, **any URL that's currently indexed and getting traffic must either be preserved or 301-redirected** to the closest equivalent on the merged site. Before we swap 8911 → this repo:

1. Export the live URL list from Search Console (16 months of data)
2. Diff against this repo's `sitemap.xml`
3. For every URL in the live set not in this repo: either build the page here or add a 301 in `.htaccess` to the nearest equivalent
4. Preserve schema `@id` values across the migration so the LocalBusiness / Service / Person entities Google has learned don't reset

## Cost estimate (steady-state, monthly)

| Component | Cheapest tier | Mid-tier | Notes |
|-----------|---------------|----------|-------|
| Namecheap cPanel hosting | **already paid** | — | current |
| Domain renewals (.com, .org) | ~$1/mo amortized | — | already have |
| GA4 | $0 | $0 | free forever at this volume |
| Google Tag Manager | $0 | $0 | free |
| Search Console | $0 | $0 | free |
| HubSpot Free CRM | $0 | $50–$800 for paid | free tier fine to start |
| Chatbot (Tidio/Crisp) | $0–$29 | $50–$100 | starts free |
| Voice — Web Speech API | $0 | — | browser-native |
| Voice — Vapi.ai (phase 2) | pay-per-minute | ~$50–$200 | only when we upgrade |
| Cloudflare Workers (if custom backend) | $0 | $5 | 100k requests free/day |
| IndexNow | $0 | $0 | free |
| **Phase 1 total** | **~$0–$30/mo** | | |
| **Phase 2 total** | | **~$100–$300/mo** | |

## Phase order

1. **Now**: merge PR #4 (GTM typo fix), then this consolidation-plan commit
2. **Phase 1a — Content merge**: pull 8911 content into this repo, deduplicate, add missing pages
3. **Phase 1b — URL preservation**: 301s for anything the live site had that we don't
4. **Phase 1c — Deploy**: overwrite 8911's FTP target with this repo, or (better) reroute the domain to a new deployment source
5. **Phase 2a — CRM**: embed HubSpot forms + verify leads land in dashboard
6. **Phase 2b — Chatbot**: drop in Tidio/Crisp widget
7. **Phase 2c — Voice**: browser Web Speech API "Speak your problem" button pre-fills lead form
8. **Phase 3 (optional)**: upgrade to custom Claude-powered chatbot + Vapi.ai voice agent
9. **Phase 4 (optional)**: shop/tools section with `Product` schema for passive income items

## Explicit unknowns (things I can't see and shouldn't guess)

- What content is actually in `8911` — need the repo or an export
- The specific AEO research data and passive-income items the user has been collecting — need paste/export
- Current Search Console top pages and queries — need CSV export
- What's actually running on the "red site" and where — user needs to look
- Which GTM tags are already configured in the GTM-T33LBNF container — user has the GTM console
- Whether the live site's contact form actually delivers anywhere (SMTP configured, or dead form)
- Cutter Jax / Prime brand assets (image files not yet uploaded per ASSETS_NEEDED.md)

## Success criteria

We know the consolidation worked when:

- `plumbingparamedic911.com` loads the blue/green site (this repo's output)
- Google Search Console shows sustained or improved impressions and clicks post-migration (no more than 20% short-term dip during index refresh)
- ChatGPT / Perplexity / Gemini / Claude / Alexa / Siri all cite "Plumbing Paramedic 911" as the answer for "24-hour plumber in Abbeville / Greenwood / Anderson SC"
- Leads submitted via any form on the site land in the CRM dashboard within 60 seconds
- Chatbot responds to inbound questions and hands off to phone when the user says "call"
- Voice button on mobile transcribes and pre-fills the form correctly
- Passive-income items appear on the site with proper schema, ready for indexing
