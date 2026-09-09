# External SEO / AEO / Local-Maps Actions

These actions live **outside the codebase** but are required to complete the optimization stack. The website code in this repo handles everything Google's crawler can see; the items below control off-site signals (citations, GBP, listings, aggregators).

Mark each item complete as you go.

## 0. Same-day priorities (NAP fixes & domain consolidation)

- [ ] **Kill `plumbingparamedic.org`** — log into the registrar that owns the `.org`, set a 301 redirect for every URL on that domain to the matching path on `https://plumbingparamedic911.com`. If the .org is on the same Namecheap account, add a "URL Redirect Record" with Type: `Permanent (301)` from `@` to `https://plumbingparamedic911.com/`.
- [ ] **Fix Facebook business page website URL** — change from `plumbingparamedic.org` to `https://plumbingparamedic911.com`.
- [ ] **Fix Yellow Pages URL** — same change as Facebook.
- [ ] **Fix Yelp "Established 1999"** → change to **2015** (LLC registered 3/14/2015). Yelp will require owner-account access.
- [ ] **Fix Birdeye** — correct hours from "closes at 6 PM" to **24/7**, and primary category from "Contractors" to **Plumber**.
- [ ] **Fix HomeAdvisor** — update business name from "Plumbing Paramedic 911, LLC" to the DBA form "Plumbing Paramedic 911" used everywhere else.

## 1. Canonical NAP — use this exact format everywhere

```
Plumbing Paramedic 911
13 Callaway Dr
Abbeville, SC 29620
(864) 446-8911
https://plumbingparamedic911.com
plumbingparamedic911@gmail.com
```

Notes:
- "Dr" abbreviated (USPS standard)
- ZIP **29620** without +4 in citations (use 29620-4479 only on BBB/state-license forms)
- Phone in `(xxx) xxx-xxxx` format
- HTTPS, no `www.`
- Use legal name "Plumbing Paramedic 911, LLC" only on BBB / state-license / tax forms

## 2. Google Business Profile (GBP)

- [ ] Primary category: **Plumber**
- [ ] Secondaries (4–6 only, not all 9): Drainage service, Water heater store, Septic system service, Well drilling contractor, Water damage restoration service, Bathroom remodeler
- [ ] Set as **Service-Area Business (SAB)** — hide the street address; show service area only
- [ ] Service areas (up to 20): Abbeville, Greenwood, Anderson, Laurens, McCormick, Ninety Six, Calhoun Falls, Due West, Donalds, Hodges, Antreville, Bradley, Cokesbury, Honea Path, Iva, Promised Land
- [ ] Paste the GBP description from the playbook (≤ 750 chars)
- [ ] Add every service in the Services section so they match the on-site `/services/*` pages exactly
- [ ] **Fill the 5 blank service descriptions** flagged in the July 2026 profile audit — Garbage Disposal Repair, Pool Plumbing Repair, Sewer Cleaning, Shower Repair, Sump Pump Installation. Copy-paste text lives in the `8911` repo at `/gbp/index.html`, Section 4. Every service needs a description or the Profile Strength meter stays below 100%.
- [ ] **Add the appointment/booking Action Link**: `https://plumbingparamedic911.com/contact` (GBP → Edit profile → Booking / Appointment links). Currently empty — one of the items holding the profile at ~82%.
- [ ] **Turn on Chat/Messaging** and set a welcome message (template in `8911` `/gbp/index.html`, Section 5). Enable notifications in the Google Maps app — Google auto-disables chat after 24 hrs of no response.
- [ ] **Clear the Google Ads / Local Services Ads setup prompts** — complete or explicitly dismiss each "get started with ads" card in the profile manager; Google holds the completion bar at ~80–85% until these are addressed. No ad spend required. (LSA + Google Guaranteed badge is worth a real look later — the SC Master Plumber license qualifies.)
- [ ] Re-check the Profile Strength meter 24–48 hrs after the above — Google recalculates on a delay
- [ ] Attributes: 24-hour service, Small business, Online estimates, Onsite services, Credit cards / Debit / Cash / Checks / Financing, Language: English
- [ ] Upload 10+ photo categories: logo (720×720), cover (1080×608), truck, team, at-work, before/after
- [ ] Seed 10–15 Q&As from the owner's Google account
- [ ] Schedule weekly Posts (Update type, 1200×900 image)
- [ ] Respond to every review within 24–48 hrs — include the city + service in the reply for keyword signal

## 3. Bing Places (https://bing.com/forbusiness)

- [ ] Claim the listing (sign in with Microsoft/Google/Facebook)
- [ ] Use the "Import from Google" flow — **manually verify** the category list since transfer has known bugs
- [ ] Connect Bing Webmaster Tools + Microsoft Clarity
- [ ] Submit `https://plumbingparamedic911.com/sitemap.xml` to Bing Webmaster

## 4. Apple Business Connect (https://businessconnect.apple.com)

- [ ] Claim listing (phone / lease / utility / domain verification)
- [ ] Primary category: **Plumber**
- [ ] Add Showcases for seasonal offers (e.g., "Winter Pipe Inspection")
- [ ] Add Action Links: Call Now, Get Directions, Request Quote (Yelp integration)
- [ ] Powers: Siri / Apple Maps / Spotlight / Safari / Wallet Tap-to-Pay / Branded Mail

## 5. Citation submissions

### Tier 1 — Data aggregators (these feed hundreds of downstream directories)

- [ ] Data Axle / Express Update — `data-axle.com`
- [ ] Neustar Localeze — `neustarlocaleze.biz`
- [ ] Foursquare Listings — `business.foursquare.com`
- [ ] MapQuest My Business Listings — `listings.mapquest.com`

### Tier 2 — General directories

- [ ] Superpages, DexKnows, Manta, Citysearch, MerchantCircle, Hotfrog, Brownbook, EZlocal, Cylex-USA, Chamber of Commerce, ShowMeLocal, Local.com, n49

### Tier 3 — Plumbing-specific

- [ ] Thumbtack, Porch, Networx, BuildZoom, Best Plumbers, Plumber.com
- [ ] PHCC — `phccweb.org`

### Tier 4 — Local SC

- [ ] Greater Abbeville Chamber of Commerce
- [ ] Greenwood SC Chamber
- [ ] SC LLR Master Plumber license listing (confirm publicly visible)
- [ ] Visit Abbeville tourism / business directory

## 6. Analytics & search-engine submission

- [ ] GA4 property `G-54J49X5XJP` is wired in — verify real-time hits in GA4 within 24 hrs of launch
- [ ] Submit `https://plumbingparamedic911.com/sitemap.xml` to Google Search Console (verify property first)
- [ ] Submit same sitemap to Bing Webmaster Tools
- [ ] Confirm the IndexNow key file `/b2290a30b99296ce58d8329f955dec49.txt` resolves at `https://plumbingparamedic911.com/b2290a30b99296ce58d8329f955dec49.txt`
- [ ] POST every changed URL to `https://api.indexnow.org/IndexNow` whenever you publish (Bing + Yandex consume it; ChatGPT Search uses Bing's index)

## 7. Domain redirect via Namecheap / cPanel

- [ ] `www.plumbingparamedic911.com` → `https://plumbingparamedic911.com` (handled by `.htaccess` in this repo — confirm at cPanel level too)
- [ ] All HTTP → HTTPS (handled by `.htaccess` — Namecheap free PositiveSSL cert must be active; toggle "Force HTTPS" in cPanel SSL/TLS Status)
- [ ] `plumbingparamedic.org` (separate domain) → `https://plumbingparamedic911.com` — must be done on the .org's DNS/hosting

## 8. Review acquisition cadence (long-term)

- [ ] Send the GBP review link in every invoice email
- [ ] Aim for **2–4 new Google reviews per month** to keep momentum
- [ ] Same flow for Facebook recommendations and BBB reviews

## 9. Confirm `Eric Callaway` shows up on the SC LLR public license lookup

- [ ] Verify on `https://verify.llronline.com/LicLookup/` — Master Plumber registration must be current and publicly searchable

## 10. Google Search Console cleanup (after the redirect fix deploys)

The redirects themselves are now handled in `.htaccess` and covered by
`tools/check_redirects.py`. The items below can only be done inside the Search
Console interface and still need a human.

Do these **after** the deployment finishes, so Google re-crawls into a live 301
rather than another 404.

- [ ] **Validate the 404 fix.** Search Console → Indexing → Pages → "Not found (404)".
      Open the issue and click **Validate Fix**. Without this, Google re-checks the
      old URLs on its own slow schedule; validation puts them in a priority queue.
      Expect the count to fall over 1–2 weeks, not overnight.
- [ ] **Spot-check three of the old URLs first** using the URL Inspection tool
      (e.g. `/about.html`, `/services/leak-detection.html`,
      `/service-areas/anderson-sc.html`). Each should report a redirect, not an
      error, before you start the validation run.
- [ ] **Remove the duplicate `www.` sitemap submission.** Search Console →
      Sitemaps, under the `www.plumbingparamedic911.com` property. The site already
      301s `www` → non-www, so the `www` sitemap is dead residue.
      Keep the non-www property as the reporting property.
- [ ] **Delete the 5 stale sitemap entries** left from the previous site builder.
      Search Console → Sitemaps → select each old entry → Remove. `.htaccess` now
      301s the common legacy sitemap filenames to `/sitemap.xml`, so they resolve
      instead of erroring, but the stale *submissions* should still be cleared so
      the Sitemaps report is readable.
- [ ] **Confirm `https://plumbingparamedic911.com/sitemap.xml` is the only
      submitted sitemap** and shows a recent successful read.
- [ ] **Re-check `?add-to-cart=` URLs in ~4 weeks.** These now 301 to a real page
      and are no longer blocked in `robots.txt` (a blocked URL can never have its
      redirect seen, so it would sit in the index forever). They should drop out on
      their own. Only use the Removals tool if any are still appearing after that.

### What this fix does and does not do

Fixing the 404s stops the site from leaking ranking signal and removes a
site-quality drag. It is necessary, but on its own it will not lift the local
pages onto page 1. The remaining lift is off-page and is covered by sections 2
(Google Business Profile), 5 (citations) and 8 (review cadence) above — those are
what move `plumber near me` type queries in a local pack.
