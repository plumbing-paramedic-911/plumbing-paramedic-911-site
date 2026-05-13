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
