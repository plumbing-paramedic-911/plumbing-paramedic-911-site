# Legacy `8911` Asset Audit — Cherry-Pick Decisions

Frozen source reviewed: `plumbing-paramedic-911/8911`, branch `archive/pre-consolidation-2026-08-29`, commit `6c08c355c65e82903be8baa71a633bea7dcd4f33`.

Purpose: preserve useful work without reintroducing stale pricing, duplicate search intent, an obsolete deployment path, old tracking/voice assumptions, or unsupported public claims.

## Public website content

### Migrated through the canonical generator / release layer
- Sewer line repair
- Pipe repair / repiping
- Toilet repair / installation
- Gas line services
- Hydro jetting
- Sump pump services
- Garbage disposal repair
- Drain cleaning — Abbeville local page
- Sewer line repair — Abbeville local page
- Emergency plumber — Greenwood local page
- Four paid homeowner guide pages and guide hub

These are not raw file copies. Their useful intent and subject matter were rebuilt under the current canonical design, schema, NAP and pricing rules.

### Already represented by stronger canonical pages
The old versions of emergency plumbing, drain cleaning, water heaters, leak detection, fixtures, well pumps, backflow, commercial plumbing, city hubs, about, contact, FAQ, financing, pricing and reviews were not copied over the newer canonical equivalents. Their subject matter was checked against the current site; duplicate templates were deliberately rejected.

### Intentionally redirected rather than restored
- Old blog hub and two old blog articles
- Old `/costs/*` content
- Old Iva city route
- Old Starr city route
- Backflow + Abbeville flat landing page
- Commercial plumber + Greenwood flat landing page

Reason: the current targets already cover those intents, and restoring both versions would risk duplicate/thin pages and split ranking signals.

## AI / AEO reference files

### `llms.txt`
The canonical site already has a current `llms.txt`, so the old file is not copied over it. The super-site release appends newly preserved service, guide and local-page entries to the current canonical file.

### `llms-full.txt`
The legacy concept was useful, but the old file contained stale pricing, response-time promises, old after-hours language and claims that no longer match the current public record. A new canonical `llms-full.txt` was written from current facts instead of copying the old file.

## Google Business Profile reference page

Legacy `gbp/index.html` is retained in the frozen archive as research/reference only. It is not restored as a public indexed page because GBP settings and completion guidance can become stale quickly and are better managed as an operational record than as public SEO content.

## Local SEO research

Legacy `docs/local-seo-heat-map.html` and `docs/session-recommendations.md` are retained in the frozen archive. They are not deployed publicly. Useful route strategy from that work is carried forward in the canonical service-area structure, high-intent local pages and migration map.

## Contact / lead capture

Legacy `contact/contact-handler.php` is NOT migrated. The canonical website already sends lead forms to the current Supabase `website-lead-capture` endpoint and tracks successful/failed lead events. Reintroducing the PHP handler would create a second lead path and make troubleshooting harder.

## JavaScript / voice

Legacy `js/main.js`, `js/vapi-widget.js` and `js/voice-agent.js` are not copied into production. The canonical `js/app.js` owns current navigation, lead capture, call tracking and pricing behavior. The old voice code is preserved in the frozen repository for reference while the Vapi/Twilio/Supabase dispatch platform is developed separately; putting the old browser agent back on the site without reconciling it to that architecture could create conflicting prompts, credentials, tracking and customer-routing behavior.

## Search-engine submission script

Legacy `scripts/submit-index.js` is not migrated. It references the old IndexNow key and describes deprecated/incorrect assumptions about search-engine ping endpoints and IndexNow distribution. Current sitemap, Search Console, Bing Webmaster and valid IndexNow processes should be maintained from the canonical site instead of reviving that script unchanged.

## CSS / theme / assets

Legacy `css/styles.css`, legacy markup shell and old design implementation are not copied. The canonical blue/green design system remains the only production UI layer. This avoids duplicate CSS systems, layout regressions and accidental return of stale copy embedded in old templates.

## `.htaccess`, robots, sitemap, manifest and 404

These files are not replaced wholesale. Existing canonical versions remain authoritative. Individual useful legacy redirects and route-preservation rules are retained or recreated explicitly in the canonical `.htaccess` and super-site migration layer.

## Deployment workflows

Legacy Namecheap FTP and Cloudflare Pages workflows are disabled and must stay disabled. Only `plumbing-paramedic-911-site/main` may publish the production website.

## What remains preserved, not lost

Nothing rejected above is destroyed. The full former production tree is frozen at `archive/pre-consolidation-2026-08-29`. A future feature can be recovered selectively if it is first compared with the current production architecture and business facts.
