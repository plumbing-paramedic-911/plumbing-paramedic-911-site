#!/usr/bin/env python3
"""
Plumbing Paramedic 911 — static page generator.

Produces the service pages, city pages, hub pages, and utility pages in this
repo from a single source-of-truth dict. The homepage and the emergency-plumbing
service page are authored by hand (richer content); everything else is generated
from this script.

Usage:
    python3 tools/build.py

Output: writes index.html into each target directory under repo root.
"""
from __future__ import annotations
import os, textwrap, json, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

BASE_URL = "https://plumbingparamedic911.com"
PHONE_DISPLAY = "(864) 446-8911"
PHONE_TEL = "+18644468911"
GA_ID = "G-54J49X5XJP"
GTM_ID = "GTM-T33LBNF"

# ─── Shared HTML chunks ────────────────────────────────────────────────────
NAV_HTML = """\
<div class="topbar">
  <div class="container">
    <div class="topbar-inner">
      <span>📍 13 Callaway Dr, Abbeville, SC 29620 · Serving Abbeville, Greenwood, Anderson, Laurens, McCormick &amp; Upstate SC</span>
      <div class="topbar-right">
        <a href="mailto:plumbingparamedic911@gmail.com">✉ plumbingparamedic911@gmail.com</a>
        <a href="tel:+18644468911"><strong>📞 (864) 446-8911</strong></a>
      </div>
    </div>
  </div>
</div>

<nav class="site-nav" aria-label="Primary">
  <div class="container">
    <div class="nav-inner">
      <a href="/" class="nav-logo" aria-label="Plumbing Paramedic 911 — Home">
        <svg class="logo-mark" viewBox="0 0 42 42" fill="none" aria-hidden="true"><polygon points="21,1 27,8 36,8 36,17 42,21 36,25 36,34 27,34 21,41 15,34 6,34 6,25 0,21 6,17 6,8 15,8" fill="#1565C0"/><polygon points="21,1 27,8 36,8 36,17 42,21 36,25 36,34 27,34 21,41 15,34 6,34 6,25 0,21 6,17 6,8 15,8" fill="none" stroke="#43A047" stroke-width="2"/><rect x="18" y="10" width="6" height="22" rx="1.5" fill="white"/><rect x="10" y="18" width="22" height="6" rx="1.5" fill="white"/></svg>
        <div class="logo-text">PLUMBING PARAMEDIC 911<span class="logo-sub">When Emergencies Happen...</span></div>
      </a>
      <ul class="nav-links">
        <li><a href="/"{HOME_ACTIVE}>Home</a></li>
        <li class="has-dropdown"><a href="/services/"{SERVICES_ACTIVE}>Services ▾</a><div class="dropdown"><a href="/services/24-7-emergency-plumbing/">🚨 Emergency Plumbing</a><a href="/services/drain-cleaning/">🚿 Drain Cleaning</a><a href="/services/water-heater-repair-replacement/">🔥 Water Heater Services</a><a href="/services/leak-detection/">💦 Leak Detection</a><a href="/services/plumbing-fixture-installation-repair/">🚰 Fixture Install &amp; Repair</a><a href="/services/well-pump-repair/">💧 Well Pump Repair</a><a href="/services/backflow-prevention-testing/">🛡️ Backflow Testing</a><a href="/services/commercial-plumbing/">🏢 Commercial Plumbing</a></div></li>
        <li class="has-dropdown"><a href="/service-areas/"{AREAS_ACTIVE}>Service Areas ▾</a><div class="dropdown"><a href="/service-areas/abbeville-sc/">📍 Abbeville, SC</a><a href="/service-areas/greenwood-sc/">📍 Greenwood, SC</a><a href="/service-areas/anderson-sc/">📍 Anderson, SC</a><a href="/service-areas/laurens-sc/">📍 Laurens, SC</a><a href="/service-areas/mccormick-sc/">📍 McCormick, SC</a><a href="/service-areas/ninety-six-sc/">📍 Ninety Six, SC</a><a href="/service-areas/calhoun-falls-sc/">📍 Calhoun Falls, SC</a><a href="/service-areas/due-west-sc/">📍 Due West, SC</a></div></li>
        <li><a href="/pricing/"{PRICING_ACTIVE}>💰 Pricing</a></li>
        <li><a href="/about/"{ABOUT_ACTIVE}>About</a></li>
        <li><a href="/contact/"{CONTACT_ACTIVE}>Contact</a></li>
      </ul>
      <div style="display:flex;align-items:center;gap:12px"><a href="tel:+18644468911" class="nav-phone speakable-phone">📞 (864) 446-8911</a><a href="tel:+18644468911" class="btn btn-green btn-sm">Call Now</a></div>
      <button class="hamburger" id="ham" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>

<div class="mobile-nav" id="mobileNav">
  <a href="/">🏠 Home</a>
  <span class="mobile-section-label">Services</span>
  <a href="/services/24-7-emergency-plumbing/">🚨 Emergency Plumbing</a>
  <a href="/services/drain-cleaning/">🚿 Drain Cleaning</a>
  <a href="/services/water-heater-repair-replacement/">🔥 Water Heater Services</a>
  <a href="/services/leak-detection/">💦 Leak Detection</a>
  <a href="/services/plumbing-fixture-installation-repair/">🚰 Fixtures</a>
  <a href="/services/well-pump-repair/">💧 Well Pump Repair</a>
  <a href="/services/backflow-prevention-testing/">🛡️ Backflow Testing</a>
  <a href="/services/commercial-plumbing/">🏢 Commercial</a>
  <span class="mobile-section-label">Service Areas</span>
  <a href="/service-areas/abbeville-sc/">📍 Abbeville, SC</a>
  <a href="/service-areas/greenwood-sc/">📍 Greenwood, SC</a>
  <a href="/service-areas/anderson-sc/">📍 Anderson, SC</a>
  <a href="/service-areas/laurens-sc/">📍 Laurens, SC</a>
  <a href="/service-areas/mccormick-sc/">📍 McCormick, SC</a>
  <a href="/service-areas/ninety-six-sc/">📍 Ninety Six, SC</a>
  <a href="/service-areas/calhoun-falls-sc/">📍 Calhoun Falls, SC</a>
  <a href="/service-areas/due-west-sc/">📍 Due West, SC</a>
  <span class="mobile-section-label">More</span>
  <a href="/pricing/">💰 Pricing Calculator</a>
  <a href="/about/">👤 About</a>
  <a href="/contact/">✉ Contact</a>
  <a href="tel:+18644468911" class="btn btn-green" style="margin-top:8px;justify-content:center">📞 Call (864) 446-8911</a>
</div>
"""

FOOTER_HTML = """\
<footer>
  <div class="container">
    <div class="footer-grid">
      <div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px"><svg width="36" height="36" viewBox="0 0 42 42" fill="none" aria-hidden="true"><polygon points="21,1 27,8 36,8 36,17 42,21 36,25 36,34 27,34 21,41 15,34 6,34 6,25 0,21 6,17 6,8 15,8" fill="#1565C0"/><rect x="18" y="10" width="6" height="22" rx="1.5" fill="white"/><rect x="10" y="18" width="22" height="6" rx="1.5" fill="white"/></svg><strong style="color:white;font-family:var(--ff-head);font-size:1.05rem">PLUMBING PARAMEDIC 911</strong></div>
        <p class="footer-brand-desc">SC Master Plumber serving Abbeville, Greenwood, Anderson &amp; Upstate South Carolina since 2015. In the trade since 1996. 24/7 emergency dispatch, upfront flat-rate pricing, 2-year warranty on all work.</p>
        <div class="footer-phone"><a href="tel:+18644468911">📞 (864) 446-8911</a></div>
        <div class="footer-tagline">When emergencies happen, we respond.</div>
        <address class="footer-addr">13 Callaway Dr<br>Abbeville, SC 29620<br><a href="mailto:plumbingparamedic911@gmail.com" style="color:rgba(255,255,255,.6)">plumbingparamedic911@gmail.com</a></address>
      </div>
      <div><h4>Services</h4><ul class="footer-links"><li><a href="/services/24-7-emergency-plumbing/">Emergency Plumbing</a></li><li><a href="/services/drain-cleaning/">Drain Cleaning</a></li><li><a href="/services/water-heater-repair-replacement/">Water Heater Services</a></li><li><a href="/services/leak-detection/">Leak Detection</a></li><li><a href="/services/plumbing-fixture-installation-repair/">Fixture Install &amp; Repair</a></li><li><a href="/services/well-pump-repair/">Well Pump Repair</a></li><li><a href="/services/backflow-prevention-testing/">Backflow Testing</a></li><li><a href="/services/commercial-plumbing/">Commercial Plumbing</a></li></ul></div>
      <div><h4>Service Areas</h4><ul class="footer-links"><li><a href="/service-areas/abbeville-sc/">Abbeville, SC</a></li><li><a href="/service-areas/greenwood-sc/">Greenwood, SC</a></li><li><a href="/service-areas/anderson-sc/">Anderson, SC</a></li><li><a href="/service-areas/laurens-sc/">Laurens, SC</a></li><li><a href="/service-areas/mccormick-sc/">McCormick, SC</a></li><li><a href="/service-areas/ninety-six-sc/">Ninety Six, SC</a></li><li><a href="/service-areas/calhoun-falls-sc/">Calhoun Falls, SC</a></li><li><a href="/service-areas/due-west-sc/">Due West, SC</a></li></ul></div>
      <div><h4>Company</h4><ul class="footer-links"><li><a href="/about/">About Eric Callaway</a></li><li><a href="/pricing/">Pricing Calculator</a></li><li><a href="/financing/">Financing</a></li><li><a href="/reviews/">Reviews</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy/">Privacy</a></li><li><a href="/terms/">Terms</a></li></ul></div>
    </div>
    <div class="footer-bottom">
      <div>© <span id="y">2026</span> Plumbing Paramedic 911, LLC · SC Master Plumber · Licensed &amp; Insured</div>
      <div>Built for Upstate South Carolina</div>
    </div>
  </div>
</footer>
<script>document.getElementById('y').textContent=new Date().getFullYear();</script>
<script src="/js/app.js" defer></script>
"""


def nav(active: str | None = None) -> str:
    flags = {k: '' for k in ['HOME_ACTIVE','SERVICES_ACTIVE','AREAS_ACTIVE','PRICING_ACTIVE','ABOUT_ACTIVE','CONTACT_ACTIVE']}
    if active:
        key = active.upper() + '_ACTIVE'
        if key in flags:
            flags[key] = ' class="active"'
    return NAV_HTML.format(**flags)


def head(title: str, description: str, path: str, og_image: str = "/og-image.jpg",
         extra_jsonld: list[dict] | None = None, og_type: str = "website",
         body_page: str = "site") -> str:
    canonical = BASE_URL + path
    og_url = canonical
    og_image_url = og_image if og_image.startswith("http") else BASE_URL + og_image
    jsonld = ""
    if extra_jsonld:
        graph = {"@context": "https://schema.org", "@graph": extra_jsonld}
        jsonld = '<script type="application/ld+json">\n' + json.dumps(graph, ensure_ascii=False) + '\n</script>'
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0D47A1">
<meta name="format-detection" content="telephone=yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="PP911">
<meta name="mobile-web-app-capable" content="yes">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png">
<link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png">
<link rel="apple-touch-icon" sizes="76x76" href="/apple-touch-icon-76x76.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Plumbing Paramedic 911">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{og_url}">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{og_image_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="business:contact_data:street_address" content="13 Callaway Dr">
<meta property="business:contact_data:locality" content="Abbeville">
<meta property="business:contact_data:region" content="SC">
<meta property="business:contact_data:postal_code" content="29620">
<meta property="business:contact_data:country_name" content="United States">
<meta property="business:contact_data:phone_number" content="+1-864-446-8911">
<meta property="business:contact_data:website" content="https://plumbingparamedic911.com/">
<meta property="place:location:latitude" content="34.178172">
<meta property="place:location:longitude" content="-82.379015">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image_url}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;400;500;600;700;800;900&family=Barlow:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
{jsonld}
</head>
<body data-page="{body_page}">
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""


def breadcrumb_ld(items):
    return {
        "@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":i+1,"name":name,"item":BASE_URL+path}
            for i,(name,path) in enumerate(items)
        ]
    }


def faq_ld(faqs):
    return {
        "@type":"FAQPage",
        "mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
            for q,a in faqs
        ]
    }


def faq_html(faqs):
    return "\n".join(
        f'<div class="faq-item"><button class="faq-q" type="button" aria-expanded="false"><span>{q}</span><span class="faq-arrow">+</span></button><div class="faq-a">{a}</div></div>'
        for q,a in faqs
    )


def breadcrumb_html(items):
    """Items: list of (name, path) tuples; last is current (no link)."""
    parts = []
    for i,(name,path) in enumerate(items):
        if i == len(items)-1:
            parts.append(f"<span>{name}</span>")
        else:
            parts.append(f'<a href="{path}">{name}</a>')
    return '<span>/</span>'.join(parts)


# ─── Service pages ─────────────────────────────────────────────────────────
SERVICES = {
    "drain-cleaning": {
        "title": "Drain Cleaning &amp; Hydro Jetting in Abbeville, SC | Plumbing Paramedic 911",
        "description": "Clogged drains and main sewer lines cleared fast in Abbeville, Greenwood, Anderson, Laurens &amp; McCormick. Hydro jetting, augering, camera inspection. Flat-rate from $149. Call (864) 446-8911.",
        "h1": "Drain Cleaning in Abbeville &amp; Upstate SC",
        "badge": "● Same-Day Service Available",
        "intro": "Slow sinks, gurgling toilets, sewer smells, water backing up in the shower — most clogs are not random. They are buildup that's been forming for months and finally chose today to announce itself. We clear them quickly, identify what caused the clog, and tell you whether you have a deeper sewer problem before it floods your floor.",
        "schema_id": "https://plumbingparamedic911.com/#service-draincleaning",
        "service_type": "Drain Cleaning",
        "schema_desc": "Hydro-jetting, augering, and rooter service to clear clogged sinks, tubs, toilets, and main sewer lines across Abbeville, Greenwood, Anderson, Laurens, and McCormick counties.",
        "price_range": "$149 – $699",
        "price_note": "Single drain from $149. Hydro jetting from $399. Sewer camera $199.",
        "og": "/images/og/drain-cleaning-1200x630.jpg",
        "body": """
<h3>What we clear, and how</h3>
<p>A clogged drain is a symptom. Hair and soap film build up in shower drains. Grease and food waste line kitchen drains. Wipes and "flushable" products absolutely do not flush — they catch on every pipe joint in your main line. Tree roots find old clay sewer lines from the outside in. Our job is figuring out which of those is causing your specific problem and clearing it without making it worse.</p>
<p>For most household drains — sinks, tubs, showers, toilets — a hand or power auger ("snake") clears the obstruction in 15 to 30 minutes. For a main sewer line, we typically pull a heavier machine. For lines that re-clog repeatedly, hydro jetting (high-pressure water) scrubs the inside of the pipe back to its original diameter and is the only thing that truly clears grease buildup or root intrusion.</p>
<h3>When to call a plumber instead of pouring a chemical</h3>
<ul>
  <li>If a chemical drain cleaner didn't fix it the first time, stop — repeated chemicals corrode old galvanized and cast-iron pipes from the inside</li>
  <li>If more than one drain is slow at the same time, the clog is downstream of those fixtures — likely in the main line</li>
  <li>If water rises in another fixture when you flush a toilet, you have a main-line block — stop running water and call</li>
  <li>If you smell sewer gas inside the house, you have a venting issue or a dry trap — needs professional inspection</li>
  <li>If your house has clay or Orangeburg sewer lines (most homes built before 1980 in Abbeville and Greenwood), you may need camera inspection before recurring clogs return</li>
</ul>
<h3>What's included</h3>
<ul>
  <li>Diagnosis of where the clog is — fixture, branch line, or main</li>
  <li>Single-drain clear with auger, or main-line clear from cleanout</li>
  <li>Camera inspection on request — see the inside of your pipe on a real video screen</li>
  <li>Hydro jetting for grease, scale, and root intrusion</li>
  <li>Honest assessment of whether you have a deeper issue (root damage, sewer-line collapse) and what it would cost to address</li>
  <li>2-year warranty on the repair (excluding new clogs caused by new buildup)</li>
</ul>
<h3>Why drains in Upstate SC clog the way they do</h3>
<p>Abbeville and Greenwood have a lot of older housing stock — pre-1960 homes still on galvanized supply and cast-iron drain stacks. As cast iron ages, its inside surface gets rougher; everything that goes down a drain catches on it. That's why a 70-year-old house seems to clog twice a year and a brand-new build never does. Out in rural Abbeville and McCormick counties, septic systems mean that a clog can also be a full tank — we'll tell you before you spend on a snake.</p>
""",
        "faqs": [
            ("How much does drain cleaning cost in Abbeville SC?",
             "A single drain clear starts at $149 with our flat-rate pricing. Main sewer line cleaning is $249 to $449. Hydro jetting for grease or roots is $399 to $699. The exact quote is given in writing before any work begins."),
            ("What's the difference between snaking and hydro jetting?",
             "Snaking (augering) pokes a hole through the clog and pulls debris back. Hydro jetting scrubs the entire inner wall of the pipe with high-pressure water. Snaking is faster and cheaper; hydro jetting is the only fix for grease coating or root intrusion."),
            ("Will Drano damage my pipes?",
             "Chemical drain cleaners are caustic and can corrode old galvanized, copper, and cast-iron pipes from the inside. They are also dangerous to handle. We do not recommend them — especially in pre-1980 Upstate SC homes with original drain stacks."),
            ("Do you offer camera inspection?",
             "Yes. A sewer camera inspection runs $199 to $299 and lets you see exactly what's inside your pipe — roots, breaks, bellies, or scale — on a video screen during the appointment. We recommend it for recurring clogs."),
            ("How do I know if my sewer line is broken vs just clogged?",
             "Signs of a broken sewer line include sewage smells outside, soft or sunken patches in the yard, multiple drain backups across the house, gurgling sounds in toilets, and slow drains that return immediately after clearing. A camera inspection confirms it."),
            ("Can roots really break a sewer line?",
             "Yes — especially in older clay or Orangeburg pipes common in Abbeville, Greenwood, and McCormick. Tree roots find joints, push in, then expand and crack the pipe. Hydro jetting clears them but a permanent fix requires section replacement or pipe lining."),
        ],
    },

    "water-heater-repair-replacement": {
        "title": "Water Heater Repair &amp; Replacement in Abbeville, SC | Plumbing Paramedic 911",
        "description": "Same-day water heater repair and replacement in Abbeville, Greenwood, Anderson, Laurens, McCormick — tank, tankless, gas, electric, heat-pump. Flat-rate from $149 repair, $899 replacement. Call (864) 446-8911.",
        "h1": "Water Heater Repair &amp; Replacement",
        "badge": "● Same-Day Replacement Available",
        "intro": "Cold shower today, no hot water tomorrow — water heaters give some warning before they quit, but not much. We diagnose, repair, and replace tank and tankless models same day in most cases, with stock heaters ranging from 40 to 80 gallons on the truck.",
        "schema_id": "https://plumbingparamedic911.com/#service-waterheater",
        "service_type": "Water Heater Repair",
        "schema_desc": "Diagnose, repair, and install tank and tankless water heaters — gas, electric, and heat-pump models. Same-day replacement in Abbeville, Greenwood, Anderson, Laurens, and McCormick counties.",
        "price_range": "$149 – $2,899",
        "price_note": "Repair from $149. 40-gallon tank from $899. 50-gallon from $999. Tankless install $1,599 – $2,899.",
        "og": "/images/og/water-heater-1200x630.jpg",
        "body": """
<h3>Repair or replace?</h3>
<p>The rule of thumb: if your heater is under 8 years old, repair almost always makes sense. Common repairs include thermocouple/igniter on a gas unit (under $200), heating element on an electric unit (under $250), or T&P relief valve and anode rod ($149–$199). Past 10 years, replacement is usually the smarter spend — efficiency, warranty, and reliability all tilt toward a new unit.</p>
<h3>Tank vs tankless</h3>
<p>A 40 or 50-gallon tank is what most Upstate SC homes already have. It's the cheapest install, holds 40–50 gallons of hot water ready to go, and lasts 8–12 years. A tankless unit ("on-demand") heats water as you use it — never runs out, lasts 18–20 years, takes up almost no space, and saves about 25% on energy. The trade-off: tankless costs more to install ($1,599–$2,899 vs $899–$1,499) and may require gas-line or electrical upgrades. We'll walk you through both options at quote time.</p>
<h3>What's included in a replacement</h3>
<ul>
  <li>Removal and disposal of the old unit</li>
  <li>New heater (stocked sizes 40, 50, 65, 75, 80 gallons; tankless on order)</li>
  <li>New flex connectors, ball valves, T&amp;P relief valve, expansion tank if required by SC code</li>
  <li>Drip pan and drain line if installed in living space</li>
  <li>Code-compliant venting on gas units</li>
  <li>Permit if your municipality requires one (Abbeville, Greenwood, Anderson all do for new installs)</li>
  <li>Pressure test and full hot-water test before we leave</li>
  <li>Manufacturer warranty (typically 6 years on tank, 10–15 on tankless) plus our 2-year labor warranty</li>
</ul>
<h3>Signs your water heater is dying</h3>
<ul>
  <li>Hot water runs out faster than it used to</li>
  <li>Rust-colored water from hot taps (anode rod or tank corrosion)</li>
  <li>Popping or rumbling sounds (sediment buildup)</li>
  <li>Water around the base of the tank (leak — almost always means replacement)</li>
  <li>Pilot light won't stay lit (thermocouple — usually repairable)</li>
  <li>Heater is older than 10 years</li>
</ul>
<h3>What this won't cost you</h3>
<p>Diagnostic is included in the repair price. No separate "trip fee" added on after. The quoted price is the final price. If your install requires a new gas line, vent, or electrical circuit, we'll tell you in writing before we start — never as a surprise on the invoice.</p>
""",
        "faqs": [
            ("How much does it cost to replace a water heater in Abbeville SC?",
             "A 40-gallon tank replacement is $899 to $1,299 installed. A 50-gallon tank is $999 to $1,499. Tankless installation runs $1,599 to $2,899 depending on whether gas-line or electrical upgrades are needed. All flat-rate, written quote before we start."),
            ("How long does water heater installation take?",
             "A like-for-like tank replacement (same fuel, same size, same location) is typically 2 to 3 hours. A tankless installation is 4 to 7 hours. Conversion from electric to gas, or relocation to a different room, can take a full day."),
            ("Tank or tankless — which is better for a home in Upstate SC?",
             "Tank heaters are cheaper to install and fine for most households. Tankless is worth it if you have a large family, run multiple showers at once, or want to save 25% on energy and don't mind the higher install cost. Both work well in our climate."),
            ("Do you install heat-pump water heaters?",
             "Yes. Heat-pump (or hybrid) water heaters are the most efficient option — they pull heat from the surrounding air. They cost $1,500 to $2,500 installed but qualify for federal tax credits and can cut water-heating bills by 60% in our climate."),
            ("Why is my water heater making a popping noise?",
             "That sound is water bubbling under a layer of mineral sediment that has settled to the bottom of the tank. It's reducing efficiency and shortening the tank's life. We can flush it ($149) and add an anode rod, but tanks more than 10 years old typically need replacing."),
            ("Do you offer financing on water heater replacement?",
             "Yes. In-house financing is available on any job over $500, including water heater replacement. We work with all credit profiles. Ask at quote time and we'll walk you through the options."),
        ],
    },

    "leak-detection": {
        "title": "Leak Detection in Abbeville &amp; Upstate SC | Plumbing Paramedic 911",
        "description": "Find and fix hidden leaks fast in Abbeville, Greenwood, Anderson, Laurens, McCormick. Acoustic, thermal &amp; pressure leak detection. Slab leaks, wall leaks, underground supply lines. Call (864) 446-8911.",
        "h1": "Leak Detection &amp; Repair",
        "badge": "● Same-Day Diagnostic",
        "intro": "A leak you can see is easy. A leak you can hear but can't find — behind drywall, under a slab, buried 18 inches under the front yard — is the one that runs up the water bill and rots out a wall before you notice. We find them with acoustic listening, thermal imaging, and line pressure testing, then fix the specific spot without tearing apart your house.",
        "schema_id": "https://plumbingparamedic911.com/#service-leakdetection",
        "service_type": "Leak Detection",
        "schema_desc": "Acoustic, thermal, and pressure-based leak detection for slab leaks, wall leaks, supply-line breaks, and underground leaks across Abbeville, Greenwood, Anderson, Laurens, and McCormick counties.",
        "price_range": "$149 – $399 detection",
        "price_note": "Diagnostic with locating equipment from $149. Spot repair after location identified from $149.",
        "og": "/images/og/leak-detection-1200x630.jpg",
        "body": """
<h3>Where leaks hide</h3>
<p>The leak you can see is a 5-minute fix. The leaks we get called about are the ones nobody can find:</p>
<ul>
  <li><strong>Slab leaks</strong> — supply lines run under concrete slab in many post-1970 Abbeville and Greenwood homes; a pinhole leak can flood under the floor for weeks before water finds its way up.</li>
  <li><strong>Wall leaks</strong> — supply lines inside walls or running up to second-floor bathrooms drip behind drywall, damaging studs and insulation invisibly.</li>
  <li><strong>Underground supply-line leaks</strong> — between the meter and the house, often in old galvanized or polybutylene; a 1/16th-inch hole leaks 200+ gallons a day.</li>
  <li><strong>Drain leaks</strong> — sometimes inside the floor between stories; you only notice when ceiling stains appear below the upstairs bathroom.</li>
  <li><strong>Pinhole copper leaks</strong> — common in 30+ year old copper plumbing; usually pre-corroded, often appearing in clusters.</li>
</ul>
<h3>How we find them without tearing your house apart</h3>
<p>The traditional method ("cut drywall until we find it") wastes time and damages your home. We use three modern techniques:</p>
<ul>
  <li><strong>Acoustic leak listening</strong> — a high-sensitivity microphone amplifies the sound of escaping water; we trace it to within inches of the leak before cutting anything</li>
  <li><strong>Thermal imaging</strong> — infrared cameras read surface temperature; warm water leaks show up as bright spots, cold leaks as dark</li>
  <li><strong>Line pressure testing</strong> — we isolate sections of plumbing and measure pressure loss to confirm where (not just whether) a leak exists</li>
  <li><strong>Moisture mapping</strong> — for wall or ceiling leaks where the leak point may be several feet from where you see the stain</li>
</ul>
<h3>What you'll see on a typical visit</h3>
<p>We arrive, you show us the symptom (water bill spike, wet spot, stained ceiling, sound of running water). We start with a meter check — if your shut-off valves are all closed and the meter still spins, there is definitely a leak between the meter and your shut-offs. Then we locate it acoustically, mark the spot, and quote the repair. Total diagnostic time is usually 30 to 60 minutes; you'll know what's wrong and what it costs before we open a single wall.</p>
<h3>Repair after detection</h3>
<p>Once located, a typical wall leak repair runs $149 to $399. A slab leak repair (where we can re-route through accessible space) is $399 to $999. A full re-route or pipe replacement varies depending on length and access. We always quote the repair in writing before starting and explain the trade-off between a spot fix and a longer-term re-route.</p>
""",
        "faqs": [
            ("How do I know if I have a hidden water leak?",
             "Sudden spike in your water bill with no usage change, sound of water running when no fixtures are on, warm or wet spots on floor (slab leak), mildew or mold smells, low water pressure, or your water meter spinning with everything shut off. Any of these means call."),
            ("How much does leak detection cost in Abbeville SC?",
             "Flat-rate diagnostic with full locating equipment starts at $149. We give you the location, what's leaking, and a written repair quote in the same visit. The diagnostic fee is credited toward the repair if you proceed."),
            ("What is a slab leak?",
             "A slab leak is a leak in the hot or cold water supply lines that run under the concrete slab foundation of your home. Symptoms include warm spots on the floor, water damage at the base of walls, and sudden water bill increases."),
            ("Can a leak in the wall really cause mold?",
             "Yes — wood framing and drywall are organic, and once wet they support mold growth within 24 to 48 hours. A wall leak left untreated for a week can produce health-affecting mold. We find leaks fast specifically to prevent this."),
            ("Do you fix the leak or just locate it?",
             "Both. We locate first, quote the repair before opening anything, and complete the repair the same day in most cases. Larger jobs (slab re-routes, underground supply-line replacement) are scheduled within a few days."),
            ("Will insurance cover a hidden water leak?",
             "Most homeowner's policies cover sudden and accidental water damage, but not the leak itself or gradual seepage. We document the leak location and provide an itemized invoice that helps your claim — call your insurer the same day you discover the leak."),
        ],
    },

    "plumbing-fixture-installation-repair": {
        "title": "Faucet, Toilet, Sink &amp; Fixture Install in Abbeville, SC | Plumbing Paramedic 911",
        "description": "Faucet, toilet, sink, garbage disposal, shower &amp; fixture installation and repair in Abbeville, Greenwood, Anderson, Laurens, McCormick. Flat-rate from $89. Call (864) 446-8911.",
        "h1": "Plumbing Fixture Install &amp; Repair",
        "badge": "● Same-Day Booking",
        "intro": "Faucets, toilets, sinks, garbage disposals, showers, outdoor spigots, washing-machine valves — every plumbing fixture in your house eventually needs repair or replacement. We do them quickly, with flat-rate pricing and standard parts on the truck.",
        "schema_id": "https://plumbingparamedic911.com/#service-fixtures",
        "service_type": "Plumbing Fixture Installation",
        "schema_desc": "Install and repair faucets, toilets, sinks, garbage disposals, showers, outdoor spigots, washing-machine valves, and other plumbing fixtures across Abbeville, Greenwood, Anderson, Laurens, and McCormick counties.",
        "price_range": "$89 – $1,999",
        "price_note": "Toilet repair from $89. Faucet install $129–$199. Sink install $149–$349. Shower install $599–$1,499.",
        "og": "/images/og/fixtures-1200x630.jpg",
        "body": """
<h3>Fixtures we install and repair</h3>
<ul>
  <li><strong>Toilets</strong> — fill valves, flappers, supply lines, wax rings, and full bowl/tank replacement. Standard install $249–$449; high-efficiency or wall-hung models on request.</li>
  <li><strong>Faucets</strong> — bath, kitchen, laundry, outdoor. Install supplied faucet $129–$199; faucet repair $89–$169.</li>
  <li><strong>Sinks</strong> — drop-in, undermount, farmhouse, vessel. $149–$349 for a like-for-like swap; more for new countertop work.</li>
  <li><strong>Garbage disposals</strong> — Insinkerator, Waste King, KitchenAid. Install $149–$299; jam-clearing $89.</li>
  <li><strong>Showers and tub valves</strong> — single-handle, dual-handle, pressure-balanced, thermostatic. Valve replacement $349–$699 in finished walls; new shower install $599–$1,499.</li>
  <li><strong>Outdoor spigots and hose bibs</strong> — frost-free replacement $149–$249, including soldered copper or PEX connection.</li>
  <li><strong>Washing-machine valves and laundry boxes</strong> — old gate valves replaced with quarter-turn ball valves, $179–$249.</li>
  <li><strong>Bidets, water filters, ice-maker lines, dishwasher hookups</strong> — quoted on request.</li>
</ul>
<h3>"You break it, you fix it" — fixtures that have already failed</h3>
<p>The most common emergency call we get on a fixture: a homeowner tried to swap a toilet or kitchen faucet, hit a frozen shut-off valve, broke it off, and water is now spraying. Don't panic — shut off the main, call us, we'll have the right shut-off valve and angle stops on the truck. We can usually clean up a DIY fail, install the new fixture, and have you back to running water in under two hours.</p>
<h3>What's included with every install</h3>
<ul>
  <li>Removal and disposal of the old fixture</li>
  <li>New supply lines, valves, and wax rings (toilets) or flanges as needed</li>
  <li>Code-compliant connections with quarter-turn shut-offs</li>
  <li>Pressure test and full functional check (drain, fill, water-tight)</li>
  <li>2-year warranty on labor</li>
</ul>
<h3>When to repair, when to replace</h3>
<p>A leaking faucet under 5 years old is almost always a $20 cartridge repair. Over 10 years, the seats and stems are worn and replacement makes more sense. Toilets that wobble usually need a new wax ring and flange repair. Garbage disposals that hum but don't spin can usually be unjammed for $89; if the motor is dead, replacement is the only option. We'll always tell you up-front which path is cheaper over the next 5 years.</p>
""",
        "faqs": [
            ("How much does it cost to replace a kitchen faucet?",
             "Installation of a customer-supplied kitchen faucet is $129 to $199 flat-rate. If you'd like us to supply the faucet, mid-range models add $99 to $299 depending on brand and style."),
            ("How much does it cost to install a toilet?",
             "Like-for-like toilet replacement is $249 to $449 installed. That includes the new bowl/tank assembly (standard height or comfort height), new wax ring, new supply line, new fill valve, and disposal of the old toilet."),
            ("Why does my toilet rock?",
             "A rocking toilet means the toilet isn't sitting flush on the floor — usually because the closet flange is broken or set too low. Left long enough, water will leak under the toilet, rotting the subfloor. The fix is to lift the toilet, repair the flange, and reset on a new wax ring."),
            ("Can you install a customer-supplied fixture?",
             "Yes. We install your fixture (faucet, toilet, sink, disposal, etc.) for the flat install price. We don't warranty manufacturer defects on customer-supplied parts — only our installation workmanship — but standard 2-year labor warranty applies."),
            ("My faucet drips constantly — repair or replace?",
             "A constant drip is almost always a worn cartridge or O-ring. If your faucet is under 5 years old and a quality brand (Moen, Delta, Kohler), repair is $89 to $169 and lasts. Older or low-end faucets often make more sense to replace."),
            ("Do you install bidets?",
             "Yes. Both add-on bidet seats (which connect to the existing water supply, $129 install) and standalone bidet fixtures (full install $349–$699). Heated and electronic models welcome."),
        ],
    },

    "well-pump-repair": {
        "title": "Well Pump Repair &amp; Installation in Abbeville &amp; Upstate SC | Plumbing Paramedic 911",
        "description": "Submersible &amp; jet well pump repair, pressure tank replacement, water-line install across rural Abbeville, McCormick, Calhoun Falls &amp; Upstate SC. Same-day service. Call (864) 446-8911.",
        "h1": "Well Pump Repair &amp; Installation",
        "badge": "● Same-Day Rural Service",
        "intro": "If you're on well water, your house has no water when the pump fails — period. We diagnose and repair submersible and jet pumps, replace pressure tanks, and fix pressure-switch and bladder-tank problems same-day across rural Abbeville, McCormick, Calhoun Falls, and the surrounding farms.",
        "schema_id": "https://plumbingparamedic911.com/#service-wellpump",
        "service_type": "Well Pump Service",
        "schema_desc": "Submersible and jet pump repair, pressure tank replacement, pressure-switch troubleshooting, well water testing, and well water filtration across rural Upstate South Carolina.",
        "price_range": "$349 – $1,599",
        "price_note": "Pump repair from $349. Pump replacement $799–$1,599. Pressure tank $499–$899. Water test $99–$199.",
        "og": "/images/og/well-pump-1200x630.jpg",
        "body": """
<h3>What kind of well pump do you have?</h3>
<p>Two basic types: submersible (the pump is at the bottom of the well, underwater) and jet (the pump is on the surface, suction-pulling water up). Most Upstate SC wells drilled in the last 30 years are submersible — they last longer and push water from any depth. Older shallow wells (under 25 feet) often have jet pumps. The repair cost and process is different for each; we identify which you have on arrival.</p>
<h3>Common well-water problems we fix</h3>
<ul>
  <li><strong>No water at any tap</strong> — pump has failed, pressure switch is bad, breaker is tripped, or pressure tank is waterlogged. We diagnose in under 30 minutes.</li>
  <li><strong>Water pressure too low</strong> — pressure switch set wrong, bladder in pressure tank failed, or pump worn. Cheap fix in most cases.</li>
  <li><strong>Pump runs constantly</strong> — leak somewhere on the system, check valve failed, or pressure tank lost its air charge. Cycling like this kills pumps in months.</li>
  <li><strong>Air spitting from faucets</strong> — drawing air into the system, usually from a low water table or a leaking suction line on jet pumps.</li>
  <li><strong>Dirty, cloudy, or sandy water</strong> — well casing may be silting in, or you need a sediment filter. We can test the water and recommend filtration.</li>
  <li><strong>Iron or sulfur (rotten egg) smell</strong> — common in Upstate SC well water; treatable with appropriate filtration or aeration.</li>
</ul>
<h3>What's included in a pump replacement</h3>
<ul>
  <li>Pull the old pump from the well (200+ feet of pipe and wire) — this is the labor-intensive part</li>
  <li>New pump matched to your well depth and household demand</li>
  <li>New torque arrestor, splice kit, and rope/safety line</li>
  <li>New check valve and pitless adapter seal if needed</li>
  <li>Reset the system, pressure-test, and confirm full house flow</li>
  <li>2-year warranty on labor; manufacturer warranty on pump (typically 5 years)</li>
</ul>
<h3>Pressure tanks</h3>
<p>The blue or red tank in your basement or pump house is the pressure tank. It contains a rubber bladder filled with compressed air. As the pump runs, water fills the bladder; the air keeps water under pressure between pump cycles. When that bladder fails — every 8–15 years — the pump short-cycles and burns up. Replacement is $499–$899 depending on size (20, 32, or 44 gallon).</p>
<h3>Well water testing</h3>
<p>If you've moved into a home with a well, or you haven't tested in a few years, we recommend a basic water test ($99–$199). It checks bacteria (coliform, E. coli), nitrates, iron, hardness, and pH. Based on results we can recommend appropriate filtration — softeners for hard water, sediment filters, iron filters, or UV sterilization.</p>
""",
        "faqs": [
            ("Why does my well pump keep running?",
             "Three common reasons: a leak somewhere on the supply system, a failed check valve letting water drain back, or a pressure tank that has lost its air charge. Constant running burns out pumps quickly — call before the motor fails."),
            ("How much does it cost to replace a well pump in Upstate SC?",
             "Submersible pump replacement runs $799 to $1,599 installed, depending on well depth and pump horsepower. Jet pump replacement is $499 to $999. Both include the new pump, pull and reinstall labor, and 2-year warranty."),
            ("My water has a sulfur smell — is the pump bad?",
             "No — that's hydrogen sulfide gas, common in Upstate SC well water. It's a water-quality issue, not a pump issue. Aeration or activated-carbon filtration eliminates it. We can recommend a system after a basic water test."),
            ("How long does a submersible well pump last?",
             "Average life is 10 to 15 years. Pumps that short-cycle (turn on and off constantly because of a bad pressure tank or leak) fail much sooner — often in 3 to 5 years. Properly sized and maintained, 20+ years is achievable."),
            ("Do you service wells in Calhoun Falls and McCormick?",
             "Yes. We routinely service wells across rural Abbeville County, McCormick County (including lakefront properties near Lake Thurmond), Calhoun Falls, Iva, Donalds, Antreville, and Bradley. Most rural calls are 40 to 60 minutes from our shop in Abbeville."),
            ("Should I get my well water tested?",
             "Yes — at least every 2 years if you've never had issues, and immediately if you've moved into a new home with well water or notice taste/smell changes. A basic test is $99 to $199 and screens for bacteria, nitrates, iron, hardness, and pH."),
        ],
    },

    "backflow-prevention-testing": {
        "title": "Backflow Prevention Testing &amp; Repair in South Carolina | Plumbing Paramedic 911",
        "description": "State-certified backflow prevention assembly testing, repair, and installation in Abbeville, Greenwood, Anderson, Laurens &amp; Upstate SC. Annual testing for irrigation, fire systems, commercial. Call (864) 446-8911.",
        "h1": "Backflow Prevention Testing",
        "badge": "● SC-Certified Testing",
        "intro": "If you have an irrigation system, a fire-sprinkler system, or a commercial property in Upstate SC, your municipal water utility almost certainly requires annual backflow prevention assembly testing. We perform certified testing, file the paperwork with your utility, and repair or replace failing assemblies same-day.",
        "schema_id": "https://plumbingparamedic911.com/#service-backflow",
        "service_type": "Backflow Testing",
        "schema_desc": "South Carolina state-certified backflow prevention assembly testing, repair, and installation for residential, commercial, and irrigation properties. Annual testing and paperwork filing with municipal water utilities.",
        "price_range": "$129 – $599",
        "price_note": "Annual test from $129. Repair from $199. Full assembly replacement $399–$599.",
        "og": "/images/og/backflow-1200x630.jpg",
        "body": """
<h3>What is backflow, and why does it matter?</h3>
<p>"Backflow" is when contaminated water flows backward into the municipal supply — for example, irrigation water (which has been sitting in pipes, in the dirt, mixed with whatever fertilizer or pesticide is on your lawn) being sucked back into the city's drinking water when there's a pressure drop in the main. A backflow prevention assembly is a one-way valve that physically blocks this from happening. South Carolina state law and most municipal water utilities require annual testing of these assemblies on:</p>
<ul>
  <li>Lawn irrigation systems</li>
  <li>Fire-suppression sprinkler systems</li>
  <li>Commercial properties with boilers, dishwashers, or chemical injection</li>
  <li>Properties with auxiliary water supplies (wells in addition to city water)</li>
  <li>Multi-family buildings (apartments, condos)</li>
</ul>
<h3>Annual testing</h3>
<p>If you got a letter from Abbeville Water, Greenwood Commissioners of Public Works, Anderson Joint Regional Water System, or Laurens Commission of Public Works asking for proof of annual backflow testing, that's us. The test takes 20–30 minutes per assembly and consists of measuring pressure differentials across the check valves to confirm they hold. We submit the paperwork to your utility within 5 business days; you get a copy for your records.</p>
<h3>Repair and replacement</h3>
<p>Backflow assemblies that fail testing usually need a rubber check kit or relief valve replacement ($199–$349). If the body is corroded or the assembly is more than 20 years old, full replacement is often more cost-effective ($399–$599 for standard residential RPZ or DCVA). We carry common Watts, Wilkins, Apollo, and Febco parts on the truck.</p>
<h3>New installations</h3>
<p>If you're adding an irrigation system, fire sprinkler, or commercial-use water connection, your project will likely require a backflow assembly. We install in-line or above-ground assemblies to municipal code, schedule the required initial test, and submit paperwork.</p>
<h3>What's included with every test</h3>
<ul>
  <li>Test of every required check valve and relief valve in the assembly</li>
  <li>Written report with measurements (pass/fail and pressure readings)</li>
  <li>Submission of the report to your municipal water utility</li>
  <li>Sticker on the assembly showing date of last test</li>
  <li>Reminder one year out for next test</li>
</ul>
""",
        "faqs": [
            ("How often does my backflow preventer need to be tested?",
             "Annually. South Carolina state law and every major Upstate SC water utility (Abbeville, Greenwood, Anderson, Laurens) require yearly testing of backflow prevention assemblies on irrigation, fire, and commercial connections."),
            ("How much does backflow testing cost?",
             "An annual test on a standard residential or commercial assembly is $129 to $179, depending on type (RPZ, DCVA, PVB). We file the paperwork with your utility at no additional cost. Testing multiple assemblies on one site is discounted."),
            ("Why did I get a letter from my water utility about backflow?",
             "Your water utility tracks which connections have backflow assemblies and requires proof of annual testing to keep your water service active. If you got a notice, schedule a test before the deadline to avoid service interruption."),
            ("Do you test commercial fire-sprinkler backflow?",
             "Yes. We test residential and commercial RPZ (Reduced Pressure Zone), DCVA (Double Check Valve Assembly), and PVB (Pressure Vacuum Breaker) assemblies on irrigation, fire-suppression, and chemical-injection systems across Upstate SC."),
            ("My backflow preventer failed the test — what now?",
             "We can almost always repair on the spot. Most failures are a worn rubber check kit or relief valve, $199 to $349 in parts and labor. If the assembly body is corroded or obsolete, full replacement is $399 to $599. We re-test before leaving and file the updated paperwork."),
            ("Are you certified to test backflow in South Carolina?",
             "Yes. Owner Eric Callaway holds the appropriate South Carolina certifications to test backflow prevention assemblies and is recognized by the major Upstate SC water utilities. Our test reports satisfy state and municipal requirements."),
        ],
    },

    "commercial-plumbing": {
        "title": "Commercial Plumbing in Abbeville &amp; Upstate SC | Plumbing Paramedic 911",
        "description": "Full-service commercial plumbing for restaurants, offices, retail, multi-family &amp; industrial in Abbeville, Greenwood, Anderson, Laurens, McCormick SC. 24/7 service, scheduled maintenance. Call (864) 446-8911.",
        "h1": "Commercial Plumbing Services",
        "badge": "● 24/7 Commercial Service",
        "intro": "When a restaurant's grease trap backs up at 11 AM, or an office building's water heater fails on a Monday morning, the cost isn't just the repair — it's lost revenue, unhappy customers, and frustrated tenants. We service commercial properties across Upstate SC with the same 24/7 responsiveness and flat-rate pricing we bring to homes.",
        "schema_id": "https://plumbingparamedic911.com/#service-commercial",
        "service_type": "Commercial Plumbing",
        "schema_desc": "Full-service commercial plumbing for restaurants, offices, retail, industrial, and multi-family properties across Abbeville, Greenwood, Anderson, Laurens, and McCormick counties. 24/7 service, scheduled maintenance, code-compliant installs.",
        "price_range": "Quoted per job",
        "price_note": "Service call $129. Commercial water heaters, grease traps, backflow, and repipes priced on-site.",
        "og": "/images/og/commercial-1200x630.jpg",
        "body": """
<h3>Properties we serve</h3>
<ul>
  <li><strong>Restaurants and food service</strong> — grease traps, dish stations, ice machines, walk-in cooler drains, three-compartment sinks, mop sinks, gas connections</li>
  <li><strong>Offices and professional buildings</strong> — restrooms, breakroom kitchens, water heaters (commercial gas/electric), drinking fountains</li>
  <li><strong>Retail spaces</strong> — restroom plumbing, customer-facing fixtures, mop sinks, ADA compliance</li>
  <li><strong>Multi-family</strong> — apartment buildings, condos, duplexes — unit-level repairs, common-area plumbing, shared water heaters, backflow assemblies</li>
  <li><strong>Light industrial</strong> — boiler feed, process water, chemical injection systems with required backflow protection</li>
  <li><strong>Schools, churches, community centers</strong> — large-volume restroom plumbing, ADA compliance, scheduled inspection</li>
  <li><strong>Medical and dental offices</strong> — clinical sinks, vacuum drains, code-compliant fixture spacing</li>
</ul>
<h3>What's different about commercial work</h3>
<p>Commercial plumbing has different rules: higher-volume fixtures, stricter code compliance (especially for grease, backflow, and gas), and downtime is expensive. We schedule service outside business hours when possible to avoid disrupting your operation; for emergencies, we treat commercial calls with the same 24/7 urgency as residential — often higher, since a backed-up restaurant kitchen costs $1,000+ per hour in lost service.</p>
<h3>Services on offer</h3>
<ul>
  <li><strong>Grease trap pumping, cleaning, and replacement</strong> — restaurant-required intervals, manifest-tracked disposal</li>
  <li><strong>Commercial water heaters</strong> — gas, electric, and tankless; 75–199-gallon capacity</li>
  <li><strong>Backflow testing and repair</strong> — annual, with paperwork filed to your utility</li>
  <li><strong>Drain and sewer service</strong> — main-line clearing, hydro jetting, camera inspection</li>
  <li><strong>Repipes and re-routes</strong> — copper, PEX, CPVC, galvanized replacement</li>
  <li><strong>Fixture replacement</strong> — commercial-grade faucets, flushometers, urinals, ADA-compliant fixtures</li>
  <li><strong>Gas-line install and repair</strong> — for kitchen appliances, water heaters, boilers</li>
  <li><strong>Preventive maintenance contracts</strong> — quarterly or annual inspection on a fixed schedule</li>
</ul>
<h3>Pricing and billing</h3>
<p>Commercial work is quoted on-site after inspection. We use the same flat-rate, written-quote-before-work-starts policy as on residential, but we can also bill against open POs for property management companies and offer monthly statements for recurring service contracts. Net-30 terms available for established accounts.</p>
""",
        "faqs": [
            ("Do you service commercial accounts on emergency dispatch?",
             "Yes — and we prioritize commercial emergencies because the downtime cost is so much higher than residential. Average response time for a commercial emergency in Abbeville or Greenwood is under an hour."),
            ("Do you offer property management contracts?",
             "Yes. We work with property management companies across Upstate SC on recurring maintenance contracts and tenant-call dispatch. Monthly statement billing and net-30 terms available for established accounts."),
            ("Can you handle restaurant grease traps?",
             "Yes. We service indoor and outdoor grease interceptors, perform required cleaning intervals, and provide manifest-tracked disposal. We can also retrofit non-compliant kitchens to bring them up to current municipal code."),
            ("Do you do commercial water-heater replacements after hours?",
             "Yes — and we recommend it for active businesses. Most commercial water heater replacements happen overnight to avoid customer-facing downtime. Same flat-rate pricing applies, plus after-hours surcharge."),
            ("Are you certified for commercial backflow testing?",
             "Yes. We test commercial RPZ and DCVA backflow assemblies on irrigation, fire-suppression, and process-water connections across Upstate SC, and file the required paperwork with the appropriate municipal water utility."),
            ("Can you work with our general contractor on a new build?",
             "Yes. We sub on new commercial construction and tenant build-outs across Upstate SC, including restaurants, retail, and office space. We work to plans, pull permits, and schedule inspections directly with the municipality."),
        ],
    },
}


SERVICE_PAGE_TPL = """\
<main>
  <section class="service-hero">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{breadcrumb}</nav>
      <div class="service-hero-badge">{badge}</div>
      <h1 class="speakable-headline" style="color:white;margin-bottom:12px">{h1}</h1>
      <p class="lead lead-white speakable-summary" style="max-width:640px;margin-bottom:28px">{intro}</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <a href="tel:+18644468911" class="btn btn-green btn-lg speakable-phone">📞 Call (864) 446-8911</a>
        <a href="/pricing/" class="btn btn-outline-white">💰 See Pricing</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="grid-2" style="gap:56px;align-items:start">
        <article class="prose">
          <span class="label">About This Service</span>
          <h2>{h1}</h2>
          <div class="divider"></div>
          {body}
        </article>
        <aside>
          <div class="card" style="margin-bottom:20px;border-color:var(--green);background:var(--green-xlt)">
            <div style="font-size:1.5rem;margin-bottom:8px">💰</div>
            <h3 style="margin-bottom:6px;font-size:1.1rem">Typical Price Range</h3>
            <div style="font-family:var(--ff-head);font-size:2rem;font-weight:900;color:var(--green-dk);margin-bottom:8px">{price_range}</div>
            <p style="font-size:.82rem;color:var(--ink3)">{price_note}</p>
            <a href="/pricing/" class="btn btn-green btn-sm" style="margin-top:12px">Open Pricing Calculator →</a>
          </div>
          <div class="card">
            <h3 style="margin-bottom:14px;font-size:1.1rem">Request Service</h3>
            <form class="lead-form" method="post" action="#">
              <div class="form-success">✅ Request received. We'll call you shortly.</div>
              <div class="form-field"><label>Name</label><input type="text" name="name" autocomplete="name"></div>
              <div class="form-field"><label>Phone *</label><input type="tel" name="phone" required autocomplete="tel"></div>
              <div class="form-field"><label>City / Town</label><input type="text" name="city" placeholder="Abbeville, Greenwood, etc."></div>
              <div class="form-field"><label>Describe the issue</label><textarea name="message" style="min-height:60px"></textarea></div>
              <button type="submit" class="btn btn-green" style="width:100%;justify-content:center">Request Service →</button>
            </form>
          </div>
          <div class="card" style="margin-top:20px;text-align:center;background:var(--blue-dk);color:#fff">
            <div style="font-size:2rem;margin-bottom:8px">🚨</div>
            <div style="font-family:var(--ff-head);font-weight:800;font-size:1rem;color:white;margin-bottom:4px">Active emergency?</div>
            <a href="tel:+18644468911" class="speakable-phone" style="font-family:var(--ff-head);font-size:1.6rem;font-weight:900;color:var(--green-lt)">(864) 446-8911</a>
            <div style="font-size:.78rem;color:rgba(255,255,255,.65);margin-top:4px">24/7 · 365 days a year</div>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <section class="section bg-alt">
    <div class="container" style="max-width:820px">
      <span class="label">Frequently Asked Questions</span>
      <h2 style="margin-bottom:28px">Common questions about this service</h2>
      {faqs_html}
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div style="text-align:center;margin-bottom:28px">
        <span class="label">Service available across</span>
        <h2>Upstate South Carolina</h2>
      </div>
      <div class="nav-grid">
        <a class="nav-card" href="/service-areas/abbeville-sc/"><h3>📍 Abbeville, SC</h3><p>Same-day service. Our home base.</p><span class="arrow">Abbeville →</span></a>
        <a class="nav-card" href="/service-areas/greenwood-sc/"><h3>📍 Greenwood, SC</h3><p>Full coverage county-wide.</p><span class="arrow">Greenwood →</span></a>
        <a class="nav-card" href="/service-areas/anderson-sc/"><h3>📍 Anderson, SC</h3><p>Licensed service across Anderson Co.</p><span class="arrow">Anderson →</span></a>
        <a class="nav-card" href="/service-areas/mccormick-sc/"><h3>📍 McCormick, SC</h3><p>Rural &amp; lakefront properties.</p><span class="arrow">McCormick →</span></a>
      </div>
    </div>
  </section>

  <section style="background:linear-gradient(135deg,var(--green-dk),var(--green));padding:64px 0">
    <div class="container" style="text-align:center">
      <h2 style="color:white;margin-bottom:10px">Ready to schedule?</h2>
      <p style="color:rgba(255,255,255,.9);margin-bottom:24px">Upfront flat-rate pricing. 2-year warranty. No hidden fees.</p>
      <a href="tel:+18644468911" class="btn btn-outline-white btn-xl speakable-phone">📞 (864) 446-8911</a>
    </div>
  </section>
</main>
"""


def render_service_page(slug: str, s: dict) -> str:
    path = f"/services/{slug}/"
    breadcrumb_items = [("Home","/"),("Services","/services/"),(s["h1"].replace("&amp;","&"), path)]
    breadcrumb_h = breadcrumb_html(breadcrumb_items)
    extra = [
        {"@type":"WebPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":s["title"].replace("&amp;","&"),"about":{"@id":s["schema_id"]},"isPartOf":{"@id":BASE_URL+"/#website"},"inLanguage":"en-US","speakable":{"@type":"SpeakableSpecification","cssSelector":[".speakable-headline",".speakable-summary",".speakable-phone"]}},
        {"@type":"Service","@id":s["schema_id"],"name":s["h1"].replace("&amp;","&"),"serviceType":s["service_type"],"url":BASE_URL+path,"description":s["schema_desc"],"provider":{"@id":BASE_URL+"/#localbusiness"},"areaServed":[{"@type":"City","name":c} for c in ["Abbeville","Greenwood","Anderson","Laurens","McCormick","Ninety Six","Calhoun Falls","Due West"]],"hoursAvailable":{"@type":"OpeningHoursSpecification","dayOfWeek":["https://schema.org/Monday","https://schema.org/Tuesday","https://schema.org/Wednesday","https://schema.org/Thursday","https://schema.org/Friday","https://schema.org/Saturday","https://schema.org/Sunday"],"opens":"00:00","closes":"23:59"}},
        breadcrumb_ld(breadcrumb_items),
        faq_ld(s["faqs"]),
    ]
    h = head(s["title"], s["description"], path, og_image=s["og"], extra_jsonld=extra, body_page=f"service-{slug}")
    n = nav("services")
    body = SERVICE_PAGE_TPL.format(
        breadcrumb=breadcrumb_h,
        badge=s["badge"],
        h1=s["h1"],
        intro=s["intro"],
        body=s["body"],
        price_range=s["price_range"],
        price_note=s["price_note"],
        faqs_html=faq_html(s["faqs"]),
    )
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


# ─── City pages ────────────────────────────────────────────────────────────
CITIES = {
    "abbeville-sc": {
        "city":"Abbeville","state":"South Carolina","abbr":"SC",
        "wiki":"https://en.wikipedia.org/wiki/Abbeville,_South_Carolina",
        "lat":34.178172,"lng":-82.379015,
        "response":"30–45 min",
        "title":"Plumber in Abbeville, SC | 24/7 Service | Plumbing Paramedic 911",
        "description":"Local SC Master Plumber in Abbeville, SC. 24/7 emergency dispatch, flat-rate pricing, drain cleaning, water heaters, well pumps, leak detection. Based at 13 Callaway Dr — call (864) 446-8911.",
        "og":"/images/og/abbeville-1200x630.jpg",
        "intro":"Abbeville is our home base. Our shop is on Callaway Drive, a few minutes from the historic square, and most calls within Abbeville city limits get to you in 30 to 45 minutes — often faster. We've been the plumber Abbeville homeowners trust for decades.",
        "body":"""
<h3>Local plumbing problems specific to Abbeville</h3>
<p>Abbeville has a deep stock of historic homes — many built in the late 1800s and early 1900s, particularly around the Trinity Episcopal and Court Square neighborhoods. These houses often have original galvanized supply lines or early copper that's reaching the end of its life. We see a lot of pinhole copper leaks, low water pressure from corroded galvanized, and 80-year-old cast-iron drain stacks that finally give up. We also see the opposite — newer subdivisions on the edge of town with slab foundations where a hot-water supply leak under the slab causes warm patches on the floor and water bills that double overnight.</p>
<h3>Common services in Abbeville</h3>
<ul>
  <li><strong>Emergency dispatch</strong> — typical response 30–45 minutes from Callaway Drive shop</li>
  <li><strong>Galvanized and old-copper repipes</strong> — especially for Trinity, Court Square, and historic-district homes</li>
  <li><strong>Slab leak detection and repair</strong> — for 1970s+ subdivisions</li>
  <li><strong>Water heater replacement</strong> — most Abbeville homes are on city water with electric or gas tank heaters</li>
  <li><strong>Drain cleaning and main sewer line work</strong> — older cast-iron mains, plus city sewer connections</li>
  <li><strong>Backflow testing</strong> — for Abbeville Water utility annual compliance on irrigation and commercial</li>
  <li><strong>Well work</strong> — for the rural fringe of Abbeville County (Antreville, Donalds, Lowndesville)</li>
</ul>
<h3>About Abbeville</h3>
<p>Abbeville sits in the heart of Upstate South Carolina at the seat of Abbeville County. It's a town with a strong sense of history — the "Birthplace and Deathbed of the Confederacy" — and a well-preserved downtown square with the Abbeville Opera House at its center. Around 5,200 people live in the city; another 25,000 in the surrounding county. Most municipal water service is provided by Abbeville Public Utilities; rural areas rely on private wells.</p>
<h3>Why Abbeville homeowners call us first</h3>
<ul>
  <li>We're local — based at 13 Callaway Dr, not driving in from another county</li>
  <li>Eric Callaway is a licensed SC Master Plumber with 30 years in the trade</li>
  <li>BBB A+ rated, 32+ Google reviews, 4.9-star average</li>
  <li>Flat-rate pricing — no hourly surprises</li>
  <li>2-year warranty on every job</li>
  <li>In-house financing on jobs over $500</li>
  <li>Discounts for military, seniors, police, fire, and EMS</li>
</ul>
"""
    },
    "greenwood-sc": {
        "city":"Greenwood","state":"South Carolina","abbr":"SC",
        "wiki":"https://en.wikipedia.org/wiki/Greenwood,_South_Carolina",
        "lat":34.196601,"lng":-82.161262,
        "response":"~45 min",
        "title":"Plumber in Greenwood, SC | 24/7 Service | Plumbing Paramedic 911",
        "description":"SC Master Plumber serving Greenwood, SC 24/7. Drain cleaning, water heaters, well pumps, leak detection, hard-water solutions. Flat-rate pricing. Call (864) 446-8911.",
        "og":"/images/og/greenwood-1200x630.jpg",
        "intro":"Greenwood is our biggest neighboring city — about a 30-minute drive from our Abbeville shop. We service Greenwood city limits and the surrounding Greenwood County area for everything from same-day drain calls to full bathroom remodels, with a typical emergency response time of around 45 minutes.",
        "body":"""
<h3>Local plumbing problems specific to Greenwood</h3>
<p>Greenwood's municipal water is moderately hard, and we see the consequences on water heaters and fixtures. Scale builds up on heating elements (electric heaters) and shortens tank life from a 12-year average to 6 or 7. Faucet aerators and showerheads clog faster. Pressure-balanced shower valves develop intermittent function. The fix is usually a softener or scale-inhibiting filter on the main supply line — something we install regularly here and almost never need to install in Abbeville (which has different source water chemistry).</p>
<p>Greenwood also has a wide mix of housing stock — from 1920s-era homes near Uptown to 1970s subdivisions to brand-new construction in the Lake Greenwood area. We do everything from cast-iron drain stack work in the older parts of town to slab leak detection in newer builds. Lakeside properties around Lake Greenwood often have well water and septic systems, even though they're close to the city — we handle both.</p>
<h3>Common services in Greenwood</h3>
<ul>
  <li><strong>Same-day service</strong> — typical response 45 minutes</li>
  <li><strong>Water heater repair and replacement</strong> — hard-water-related failures are our #1 Greenwood call</li>
  <li><strong>Water softeners and filtration</strong> — to extend fixture and heater life</li>
  <li><strong>Drain cleaning and sewer service</strong> — including main line clearing for older neighborhoods</li>
  <li><strong>Leak detection</strong> — acoustic, thermal, and slab leak locating</li>
  <li><strong>Well pump work</strong> — for Lake Greenwood and rural Greenwood County properties</li>
  <li><strong>Backflow testing</strong> — annual compliance for Greenwood CPW</li>
  <li><strong>Commercial plumbing</strong> — restaurants on Main and Uptown, multi-family, retail</li>
</ul>
<h3>About Greenwood</h3>
<p>Greenwood is the seat of Greenwood County and home to about 23,000 people in the city limits and 70,000+ in the county. Lander University is here; so is the headquarters of Self Regional Healthcare. Municipal water comes from Greenwood Commissioners of Public Works (CPW), which sources from Lake Greenwood. We're roughly 20 miles east of our Abbeville shop on US 178 / SC 72.</p>
<h3>Why Greenwood homeowners call us</h3>
<ul>
  <li>We bring the same flat-rate pricing and same 24/7 response to Greenwood as we do to Abbeville</li>
  <li>Licensed SC Master Plumber on every job</li>
  <li>BBB A+ rated</li>
  <li>2-year warranty on every repair and installation</li>
  <li>In-house financing on jobs over $500</li>
  <li>Military, senior, and first-responder discounts</li>
</ul>
"""
    },
    "anderson-sc": {
        "city":"Anderson","state":"South Carolina","abbr":"SC",
        "wiki":"https://en.wikipedia.org/wiki/Anderson,_South_Carolina",
        "lat":34.503376,"lng":-82.650123,
        "response":"~60 min",
        "title":"Plumber in Anderson, SC | 24/7 Service | Plumbing Paramedic 911",
        "description":"Licensed plumber serving Anderson, SC and surrounding Anderson County 24/7. Water heaters, drain cleaning, well pumps, fixture install, leak detection. Call (864) 446-8911.",
        "og":"/images/og/anderson-1200x630.jpg",
        "intro":"Anderson is about an hour north of our Abbeville shop, and we make the drive every week for both emergency and scheduled work. We serve homeowners and businesses in Anderson city limits, the suburbs along US 29 and SC 81, and the surrounding Anderson County area including Iva, Honea Path, Belton, and Pendleton.",
        "body":"""
<h3>Local plumbing problems specific to Anderson</h3>
<p>Anderson is a larger city with a broader mix of plumbing systems than Abbeville or Greenwood — heavier commercial and industrial, more multi-family, and a wider age range of residential plumbing. We see polybutylene supply-line failures fairly often in 1980s subdivisions (Quail Creek, Concord, and others); these gray plastic lines were widely installed in the South and many are reaching failure age. Replacement with PEX is usually the right answer.</p>
<p>The Anderson area also has a lot of mid-century homes with original cast-iron drain stacks, and we get called regularly to address the slow-drain, recurring-clog pattern that signals the inside of those stacks is heavily corroded. Hydro jetting buys you a few years; full replacement is the long-term fix.</p>
<h3>Common services in Anderson</h3>
<ul>
  <li><strong>Emergency dispatch</strong> — typical response 60 minutes from Abbeville</li>
  <li><strong>Polybutylene repipes</strong> — common in 1980s Anderson subdivisions</li>
  <li><strong>Cast-iron drain stack replacement</strong> — for mid-century homes</li>
  <li><strong>Water heater repair and replacement</strong></li>
  <li><strong>Drain cleaning and hydro jetting</strong></li>
  <li><strong>Leak detection</strong> — acoustic, thermal, slab</li>
  <li><strong>Backflow testing</strong> — for Anderson Joint Regional Water System / Anderson Regional Joint</li>
  <li><strong>Commercial plumbing</strong> — restaurants, offices, retail, multi-family</li>
</ul>
<h3>About Anderson</h3>
<p>Anderson is the seat of Anderson County and the largest city we serve, with about 28,000 in the city limits and 200,000+ in the county. It's part of the Greenville–Anderson metropolitan area. Municipal water comes from Anderson Regional Joint Water System; rural areas may be on well or co-op water. We're roughly 45 miles north of Abbeville via SC 28 or US 178.</p>
<h3>Why Anderson homeowners and businesses call us</h3>
<ul>
  <li>SC Master Plumber on every job — Eric Callaway personally on most calls</li>
  <li>Flat-rate pricing — same as Abbeville, with no distance markup</li>
  <li>24/7 emergency dispatch</li>
  <li>2-year warranty on all parts and labor</li>
  <li>In-house financing for larger jobs</li>
  <li>BBB A+ rating</li>
</ul>
"""
    },
    "laurens-sc": {
        "city":"Laurens","state":"South Carolina","abbr":"SC",
        "wiki":"https://en.wikipedia.org/wiki/Laurens,_South_Carolina",
        "lat":34.499264,"lng":-82.018776,
        "response":"~60 min",
        "title":"Plumber in Laurens, SC | 24/7 Service | Plumbing Paramedic 911",
        "description":"Licensed plumber serving Laurens, SC and Laurens County 24/7. Drain cleaning, water heaters, well pumps, leak detection, fixture install. Flat-rate. Call (864) 446-8911.",
        "og":"/images/og/laurens-1200x630.jpg",
        "intro":"Laurens is about an hour from our Abbeville shop, just up SC 252. We service Laurens city, Clinton, Cross Hill, Gray Court, and surrounding Laurens County for emergencies, scheduled work, and well-pump service on the more rural properties.",
        "body":"""
<h3>Local plumbing problems specific to Laurens</h3>
<p>Laurens County has a mix of small-town residential and a lot of rural acreage. Many homes outside Laurens and Clinton city limits are on well water and septic systems. Our well-pump and pressure-tank work is heavily concentrated in this area. Inside the city, we see a similar pattern to Abbeville — older housing with galvanized or early copper supply, and cast-iron drains starting to corrode.</p>
<p>Laurens also has Presbyterian College in Clinton, several manufacturing employers, and a strong agricultural footprint. We handle commercial plumbing for restaurants and retail along the I-26 corridor and Highway 76, including grease traps and backflow on irrigation systems.</p>
<h3>Common services in Laurens</h3>
<ul>
  <li><strong>Emergency dispatch</strong> — typical 60-minute response</li>
  <li><strong>Well pump and pressure-tank replacement</strong> — heavy demand on rural properties</li>
  <li><strong>Water heater repair and replacement</strong></li>
  <li><strong>Drain cleaning, sewer line, and hydro jetting</strong></li>
  <li><strong>Slab leak and wall leak detection</strong></li>
  <li><strong>Backflow testing</strong> — for Laurens CPW</li>
  <li><strong>Commercial plumbing</strong> — restaurants, retail, schools, churches</li>
  <li><strong>Fixture installs</strong> — kitchens, bathrooms, laundry</li>
</ul>
<h3>About Laurens</h3>
<p>Laurens is the seat of Laurens County, with about 9,000 in the city and 65,000+ countywide. It's roughly 35 miles east of Abbeville. Municipal water is provided by Laurens Commission of Public Works; rural areas are typically on private wells.</p>
<h3>Why Laurens homeowners call us</h3>
<ul>
  <li>We bring our full Abbeville/Greenwood capacity to Laurens — same parts, same response, same flat-rate pricing</li>
  <li>SC Master Plumber license on every job</li>
  <li>2-year warranty</li>
  <li>In-house financing on jobs over $500</li>
  <li>Military, senior, police, fire, EMS discounts</li>
</ul>
"""
    },
    "mccormick-sc": {
        "city":"McCormick","state":"South Carolina","abbr":"SC",
        "wiki":"https://en.wikipedia.org/wiki/McCormick,_South_Carolina",
        "lat":33.913,"lng":-82.292,
        "response":"~40 min",
        "title":"Plumber in McCormick, SC | Well Pumps, Lakefront Plumbing | Plumbing Paramedic 911",
        "description":"24/7 plumber serving McCormick, SC and lakefront properties near Lake Thurmond. Well pumps, water heaters, drain cleaning, leak detection. Call (864) 446-8911.",
        "og":"/images/og/mccormick-1200x630.jpg",
        "intro":"McCormick is about 30 miles south of our Abbeville shop, on the way to the Georgia border and Lake Thurmond. A huge share of our McCormick calls are well-pump work and lakefront plumbing — homes off the grid, on well-and-septic, with seasonal occupancy patterns that create their own issues.",
        "body":"""
<h3>Local plumbing problems specific to McCormick</h3>
<p>McCormick County has Lake Thurmond on its southwestern edge and Sumter National Forest covering much of the rest. Most rural properties — and most lakefront homes — are on private well water and septic. The most common calls we get:</p>
<ul>
  <li><strong>Well pump failure</strong> — submersible pumps in 200+-foot wells eventually fail; we replace them with new equipment, pull, splice, and test in a single visit</li>
  <li><strong>Pressure tank failure</strong> — the diaphragm tank that maintains house pressure between pump cycles fails about every 10 years</li>
  <li><strong>Frozen-pipe damage at lake homes</strong> — seasonal homes left unheated through winter routinely lose lines; we repair and add freeze protection</li>
  <li><strong>Septic-line clogs</strong> — between the house and the tank, we clear with augers or jetting; tank pumping is handled by our septic partners</li>
  <li><strong>Sediment in well water</strong> — older wells silt in; we install whole-house sediment filtration</li>
  <li><strong>Sulfur smell</strong> — common in McCormick County well water; treatable with appropriate filtration</li>
</ul>
<h3>Lake Thurmond properties</h3>
<p>Lakefront homes have their own pattern — long supply runs from a pump house to the main house, often through unheated crawl space; multiple bathrooms that see usage spikes (weekend guests); and freeze-vulnerable plumbing because nobody is home to catch a leak in February. We do a lot of winterization work in October–November and rapid response in January–February when something didn't get fully drained.</p>
<h3>Common services in McCormick</h3>
<ul>
  <li><strong>Well pump repair, replacement, and pressure tank service</strong></li>
  <li><strong>Water quality testing and whole-house filtration</strong></li>
  <li><strong>Sediment, iron, and sulfur filter installation</strong></li>
  <li><strong>Septic line repair (house-side)</strong></li>
  <li><strong>Water heater repair and replacement</strong></li>
  <li><strong>Frozen pipe repair and winterization</strong></li>
  <li><strong>Drain cleaning</strong></li>
  <li><strong>Lakefront fixture installations</strong></li>
</ul>
<h3>About McCormick</h3>
<p>McCormick is the seat of McCormick County, with about 2,800 people in the town and 9,000 countywide. It's bordered by Lake Thurmond (also called Clarks Hill Lake) and Sumter National Forest, making it one of the least densely populated and most outdoor-oriented counties in South Carolina.</p>
<h3>Why McCormick homeowners call us</h3>
<ul>
  <li>We specialize in well-and-septic systems — this isn't an after-thought for us</li>
  <li>40-minute typical response from Abbeville</li>
  <li>SC Master Plumber license</li>
  <li>2-year warranty</li>
  <li>Flat-rate pricing — no per-mile charges</li>
</ul>
"""
    },
    "ninety-six-sc": {
        "city":"Ninety Six","state":"South Carolina","abbr":"SC",
        "wiki":"https://en.wikipedia.org/wiki/Ninety_Six,_South_Carolina",
        "lat":34.175,"lng":-82.027,
        "response":"~25 min",
        "title":"Plumber in Ninety Six, SC | 24/7 Service | Plumbing Paramedic 911",
        "description":"Local plumber serving Ninety Six, SC 24/7 — water heaters, drain cleaning, well pumps, leak detection. Flat-rate pricing. Call (864) 446-8911.",
        "og":"/images/og/ninety-six-1200x630.jpg",
        "intro":"Ninety Six sits between Greenwood and Saluda, and is about 25 minutes from our Abbeville shop — one of our fastest-response cities. We've serviced homes and businesses in Ninety Six and the surrounding Greenwood County area for years.",
        "body":"""
<h3>Local plumbing problems specific to Ninety Six</h3>
<p>Ninety Six is small but has a wide range of housing — from historic homes near Star Fort to newer subdivisions on the edge of town. Many of the older properties have well-and-septic systems even though they're inside town; the newer subdivisions are typically on Greenwood CPW water and city sewer. Hard water from CPW source is a common issue here, just like in Greenwood — water heaters and fixtures wear faster than they would in Abbeville's softer water.</p>
<h3>Common services in Ninety Six</h3>
<ul>
  <li><strong>Same-day service</strong> — typical 25-minute response</li>
  <li><strong>Water heater repair and replacement</strong> — hard-water-related failures</li>
  <li><strong>Drain cleaning and sewer service</strong></li>
  <li><strong>Well pump repair</strong> — for properties on private well</li>
  <li><strong>Water softener installation</strong></li>
  <li><strong>Leak detection</strong></li>
  <li><strong>Fixture installation</strong> — kitchens, bathrooms</li>
  <li><strong>Commercial plumbing</strong> for businesses along Highway 246</li>
</ul>
<h3>About Ninety Six</h3>
<p>Ninety Six is a town of about 2,000 in Greenwood County, named for its historic distance (in miles) from the Cherokee village of Keowee. Ninety Six National Historic Site preserves the site of the Revolutionary War siege. The town is small but tightly knit; word-of-mouth referrals are how most of our Ninety Six customers find us.</p>
<h3>Why Ninety Six homeowners call us</h3>
<ul>
  <li>Fastest response of any of our outlying cities — 25 minutes typical</li>
  <li>Same flat-rate pricing as Abbeville</li>
  <li>SC Master Plumber license</li>
  <li>2-year warranty on every job</li>
  <li>In-house financing</li>
</ul>
"""
    },
    "calhoun-falls-sc": {
        "city":"Calhoun Falls","state":"South Carolina","abbr":"SC",
        "wiki":"https://en.wikipedia.org/wiki/Calhoun_Falls,_South_Carolina",
        "lat":34.094,"lng":-82.595,
        "response":"~40 min",
        "title":"Plumber in Calhoun Falls, SC | Lakefront &amp; Well Service | Plumbing Paramedic 911",
        "description":"24/7 plumber in Calhoun Falls, SC. Lakefront plumbing, well pumps, freeze protection, water heaters, leak detection on Lake Russell/Richard B. Russell Lake. Call (864) 446-8911.",
        "og":"/images/og/calhoun-falls-1200x630.jpg",
        "intro":"Calhoun Falls is on the western edge of Abbeville County, right on Richard B. Russell Lake. It's about 40 minutes from our shop. Most of our calls here are lakefront and rural well work — pumps, freeze damage, and seasonal-home plumbing.",
        "body":"""
<h3>Local plumbing problems specific to Calhoun Falls</h3>
<p>Calhoun Falls sits on Richard B. Russell Lake and is the gateway to Calhoun Falls State Park. A high proportion of homes are lakefront or near-lakefront — many of them seasonal or weekend properties. The pattern we see most:</p>
<ul>
  <li><strong>Frozen pipes after long unoccupied stretches</strong> — every winter, multiple lake homes lose a line because the house dropped below freezing and nobody was there</li>
  <li><strong>Well pump and pressure tank failure</strong> — most lakefront properties are on private wells</li>
  <li><strong>Long-run supply line leaks</strong> — pump houses far from the main house mean long buried supply lines, which leak underground without obvious signs</li>
  <li><strong>Sediment and iron in well water</strong> — common in this part of Upstate SC; filtration is the fix</li>
  <li><strong>Seasonal turn-on / turn-off service</strong> — winterizing in fall, recommissioning in spring</li>
</ul>
<h3>Common services in Calhoun Falls</h3>
<ul>
  <li><strong>Well pump repair, replacement, and pressure tank service</strong></li>
  <li><strong>Frozen pipe repair and winterization</strong></li>
  <li><strong>Whole-house water filtration</strong></li>
  <li><strong>Underground supply line leak detection</strong></li>
  <li><strong>Water heater repair and replacement</strong></li>
  <li><strong>Drain cleaning and septic line clearing</strong></li>
  <li><strong>Seasonal turn-on/off for second homes</strong></li>
</ul>
<h3>About Calhoun Falls</h3>
<p>Calhoun Falls is a town of about 1,800 in western Abbeville County, on the South Carolina–Georgia border at Richard B. Russell Lake. Calhoun Falls State Park brings significant seasonal traffic; the town has a small downtown and a strong outdoor-recreation economy.</p>
<h3>Why Calhoun Falls homeowners call us</h3>
<ul>
  <li>We service Calhoun Falls regularly — we know the lakeside properties and their seasonal patterns</li>
  <li>Same SC Master Plumber license, same flat-rate pricing as Abbeville</li>
  <li>2-year warranty</li>
  <li>40-minute typical response</li>
  <li>24/7 emergency dispatch — critical for unoccupied lake homes</li>
</ul>
"""
    },
    "due-west-sc": {
        "city":"Due West","state":"South Carolina","abbr":"SC",
        "wiki":"https://en.wikipedia.org/wiki/Due_West,_South_Carolina",
        "lat":34.330,"lng":-82.391,
        "response":"~20 min",
        "title":"Plumber in Due West, SC | 24/7 Service | Plumbing Paramedic 911",
        "description":"Local plumber serving Due West, SC and Erskine College area 24/7. Water heaters, drain cleaning, well pumps, leak detection. Flat-rate pricing. Call (864) 446-8911.",
        "og":"/images/og/due-west-1200x630.jpg",
        "intro":"Due West is the closest town to our Abbeville shop — typically 20 minutes door-to-door. We serve Due West, Donalds, and the Erskine College area for both routine plumbing and emergency dispatch.",
        "body":"""
<h3>Local plumbing problems specific to Due West</h3>
<p>Due West is home to Erskine College — the oldest four-year college in South Carolina — and the town's housing reflects that: many late-1800s and early-1900s homes around campus, plus newer faculty and family housing on the outskirts. Older homes here have the same plumbing issues as Abbeville's historic district: original galvanized, early copper, and cast-iron drain stacks at the end of their service life. Newer construction is generally on city water and standard PEX or copper.</p>
<p>Outside town limits, much of the surrounding area is rural — wells and septic predominate. We do steady well-pump work in this part of Abbeville County.</p>
<h3>Common services in Due West</h3>
<ul>
  <li><strong>Same-day service</strong> — typical 20-minute response</li>
  <li><strong>Historic-home repipes</strong> — galvanized and old-copper replacement</li>
  <li><strong>Water heater repair and replacement</strong></li>
  <li><strong>Drain cleaning and main sewer line work</strong></li>
  <li><strong>Cast-iron drain stack assessment and replacement</strong></li>
  <li><strong>Well pump repair</strong> — for rural Due West properties</li>
  <li><strong>Leak detection</strong></li>
  <li><strong>Fixture installation</strong></li>
</ul>
<h3>About Due West</h3>
<p>Due West is a small town of about 1,200 in Abbeville County, in the northeast corner. Erskine College and Erskine Theological Seminary anchor the community. The town has a quiet, historic feel with a tight network of residents — we get a lot of referrals here.</p>
<h3>Why Due West homeowners call us</h3>
<ul>
  <li>Closest outlying city to our Abbeville shop — fastest response time</li>
  <li>Experience with the historic housing stock around the college</li>
  <li>SC Master Plumber license on every job</li>
  <li>Flat-rate pricing</li>
  <li>2-year warranty</li>
  <li>In-house financing on jobs over $500</li>
</ul>
"""
    },
}


def city_faqs(c):
    return [
        (f"Do you offer 24/7 emergency plumbing service in {c['city']}, {c['abbr']}?",
         f"Yes. Plumbing Paramedic 911 dispatches emergency plumbing service to {c['city']}, {c['abbr']} 24 hours a day, 365 days a year. Typical response time from our Abbeville shop is {c['response']}. Call (864) 446-8911 any time."),
        (f"How much do you charge to come out to {c['city']}, {c['abbr']}?",
         f"Standard service call in {c['city']} is $129 to $179 — the same flat-rate pricing as Abbeville, with no per-mile or distance surcharge. The exact repair quote is written before any work begins."),
        (f"Are you a licensed plumber for work in {c['city']}, {c['abbr']}?",
         f"Yes. Eric Callaway holds a South Carolina Master Plumber license, valid for residential and commercial work statewide including {c['city']} and the surrounding {c['state']} area."),
        (f"Do you replace water heaters same-day in {c['city']}?",
         f"In most cases, yes. We stock 40-, 50-, 65-, 75-, and 80-gallon tank water heaters and can be at a {c['city']} home within {c['response']} for like-for-like replacement. Tankless installations are usually scheduled within a few days."),
        (f"Do you fix well pumps in the {c['city']} area?",
         f"Yes. We service submersible and jet well pumps, pressure tanks, and pressure switches across the {c['city']} area and rural surrounding properties. Same-day service is typical."),
        (f"What's your warranty on plumbing work in {c['city']}?",
         f"Every repair and installation we do in {c['city']} carries a 2-year warranty on parts and labor. If anything fails within that window, we come back and fix it at no charge."),
    ]


CITY_PAGE_TPL = """\
<main>
  <section class="city-hero">
    <div class="container">
      <nav class="city-breadcrumb" aria-label="Breadcrumb">{breadcrumb}</nav>
      <div class="chip chip-live" style="margin-bottom:14px">● Serving {city} Now</div>
      <h1 class="speakable-headline" style="color:white">{h1}</h1>
      <p class="lead lead-white speakable-summary" style="max-width:620px;margin-bottom:28px">{intro}</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <a href="tel:+18644468911" class="btn btn-green btn-lg speakable-phone">📞 Call (864) 446-8911</a>
        <a href="/pricing/" class="btn btn-outline-white">💰 See Upfront Pricing</a>
      </div>
      <div class="city-info-bar">
        <div class="city-info-item"><div class="city-info-icon">⚡</div><div><span class="city-info-label">Response Time</span><span class="city-info-val">{response}</span></div></div>
        <div class="city-info-item"><div class="city-info-icon">📞</div><div><span class="city-info-label">Emergency Line</span><span class="city-info-val">(864) 446-8911</span></div></div>
        <div class="city-info-item"><div class="city-info-icon">⏰</div><div><span class="city-info-label">Availability</span><span class="city-info-val">24/7 · 365 days</span></div></div>
        <div class="city-info-item"><div class="city-info-icon">🛡️</div><div><span class="city-info-label">Warranty</span><span class="city-info-val">2-Year on All Work</span></div></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="grid-2" style="gap:56px;align-items:start">
        <article class="prose">
          <span class="label">Local Plumbing Service</span>
          <h2>Your local plumber in {city}, {abbr}</h2>
          <div class="divider"></div>
          {body}
        </article>
        <aside>
          <div class="card" style="margin-bottom:20px">
            <h3 style="margin-bottom:14px;font-size:1.1rem">Request Service in {city}</h3>
            <form class="lead-form" method="post" action="#">
              <div class="form-success">✅ Received. We'll call you shortly.</div>
              <div class="form-field"><label>Name</label><input type="text" name="name" autocomplete="name"></div>
              <div class="form-field"><label>Phone *</label><input type="tel" name="phone" required autocomplete="tel"></div>
              <div class="form-field"><label>Service Needed</label>
                <select name="service"><option>Select a service…</option><option>Emergency / Burst Pipe</option><option>Drain Cleaning</option><option>Water Heater</option><option>Well Pump</option><option>Leak Detection</option><option>Backflow Testing</option><option>Fixture Install/Repair</option><option>Other</option></select>
              </div>
              <div class="form-field"><label>Describe the Issue</label><textarea name="message" style="min-height:72px"></textarea></div>
              <button type="submit" class="btn btn-green" style="width:100%;justify-content:center">Send Request →</button>
            </form>
          </div>
          <div style="background:var(--blue-xlt);border-radius:var(--r2);padding:32px;text-align:center;border:2px solid #90CAF9">
            <div style="font-size:2.2rem;margin-bottom:10px">🗺️</div>
            <div style="font-family:var(--ff-head);font-weight:800;font-size:1.05rem;color:var(--blue-dk);margin-bottom:8px">Serving {city}, {abbr} &amp; surrounding area</div>
            <p style="font-size:.85rem;color:var(--blue);margin-bottom:16px">Open in Google Maps to see service area boundaries.</p>
            <a href="https://www.google.com/maps/search/?api=1&amp;query=Plumber+near+{city_q}+{abbr}" target="_blank" rel="noopener" class="btn btn-blue btn-sm">Open in Google Maps</a>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <section class="section bg-alt">
    <div class="container">
      <div style="text-align:center;margin-bottom:28px">
        <span class="label">Services available in {city}</span>
        <h2>Every plumbing service you need — local to {city}</h2>
      </div>
      <div class="grid-4">
        <a class="nav-card" href="/services/24-7-emergency-plumbing/"><h3>🚨 Emergency Plumbing</h3><p>24/7 dispatch.</p><span class="arrow">Learn more →</span></a>
        <a class="nav-card" href="/services/drain-cleaning/"><h3>🚿 Drain Cleaning</h3><p>Augering &amp; hydro jetting.</p><span class="arrow">Learn more →</span></a>
        <a class="nav-card" href="/services/water-heater-repair-replacement/"><h3>🔥 Water Heater</h3><p>Tank, tankless, heat-pump.</p><span class="arrow">Learn more →</span></a>
        <a class="nav-card" href="/services/leak-detection/"><h3>💦 Leak Detection</h3><p>Slab, wall, underground.</p><span class="arrow">Learn more →</span></a>
        <a class="nav-card" href="/services/plumbing-fixture-installation-repair/"><h3>🚰 Fixtures</h3><p>Toilets, faucets, disposals.</p><span class="arrow">Learn more →</span></a>
        <a class="nav-card" href="/services/well-pump-repair/"><h3>💧 Well Pump</h3><p>Pumps, tanks, filtration.</p><span class="arrow">Learn more →</span></a>
        <a class="nav-card" href="/services/backflow-prevention-testing/"><h3>🛡️ Backflow Testing</h3><p>Annual compliance.</p><span class="arrow">Learn more →</span></a>
        <a class="nav-card" href="/services/commercial-plumbing/"><h3>🏢 Commercial</h3><p>Restaurants &amp; offices.</p><span class="arrow">Learn more →</span></a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:820px">
      <span class="label">FAQ — {city}, {abbr}</span>
      <h2 style="margin-bottom:28px">Common questions from {city} homeowners</h2>
      {faqs_html}
    </div>
  </section>

  <section style="background:linear-gradient(135deg,var(--green-dk),var(--green));padding:64px 0">
    <div class="container" style="text-align:center">
      <h2 style="color:white;margin-bottom:10px">{city} plumbing problem? We're {response} away.</h2>
      <p style="color:rgba(255,255,255,.9);margin-bottom:24px">Upfront flat-rate pricing. 2-year warranty. 24/7 dispatch.</p>
      <a href="tel:+18644468911" class="btn btn-outline-white btn-xl speakable-phone">📞 (864) 446-8911</a>
    </div>
  </section>
</main>
"""


def render_city_page(slug: str, c: dict) -> str:
    path = f"/service-areas/{slug}/"
    breadcrumb_items = [("Home","/"),("Service Areas","/service-areas/"),(f"{c['city']}, {c['abbr']}", path)]
    breadcrumb_h = breadcrumb_html(breadcrumb_items)
    h1 = f"Plumber in {c['city']}, {c['abbr']}"
    extra = [
        {"@type":"WebPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":c["title"],"isPartOf":{"@id":BASE_URL+"/#website"},"about":{"@id":BASE_URL+"/#localbusiness"},"inLanguage":"en-US","speakable":{"@type":"SpeakableSpecification","cssSelector":[".speakable-headline",".speakable-summary",".speakable-phone"]}},
        {
            "@type":"LocalBusiness",
            "@id":BASE_URL+path+"#localbusiness-"+slug,
            "name":f"Plumbing Paramedic 911 — {c['city']}, {c['abbr']}",
            "url":BASE_URL+path,
            "parentOrganization":{"@id":BASE_URL+"/#localbusiness"},
            "telephone":"+1-864-446-8911",
            "address":{"@type":"PostalAddress","streetAddress":"13 Callaway Dr","addressLocality":"Abbeville","addressRegion":"SC","postalCode":"29620","addressCountry":"US"},
            "areaServed":{"@type":"City","name":c["city"],"sameAs":c["wiki"]},
            "geo":{"@type":"GeoCoordinates","latitude":c["lat"],"longitude":c["lng"]},
            "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["https://schema.org/Monday","https://schema.org/Tuesday","https://schema.org/Wednesday","https://schema.org/Thursday","https://schema.org/Friday","https://schema.org/Saturday","https://schema.org/Sunday"],"opens":"00:00","closes":"23:59"}]
        },
        breadcrumb_ld(breadcrumb_items),
        faq_ld(city_faqs(c)),
    ]
    h = head(c["title"], c["description"], path, og_image=c["og"], extra_jsonld=extra, body_page=f"city-{slug}")
    n = nav("areas")
    body = CITY_PAGE_TPL.format(
        breadcrumb=breadcrumb_h,
        city=c["city"], abbr=c["abbr"], response=c["response"],
        h1=h1, intro=c["intro"], body=c["body"],
        city_q=c["city"].replace(" ","+"),
        faqs_html=faq_html(city_faqs(c)),
    )
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


# ─── Services hub page ─────────────────────────────────────────────────────
def render_services_hub():
    path = "/services/"
    title = "Plumbing Services in Abbeville &amp; Upstate SC | Plumbing Paramedic 911"
    description = "Every plumbing service in Abbeville, Greenwood, Anderson, Laurens, McCormick &amp; Upstate SC — emergency, drain cleaning, water heaters, leak detection, well pumps, backflow, commercial. Call (864) 446-8911."
    breadcrumb_items = [("Home","/"),("Services", path)]
    extra = [
        {"@type":"CollectionPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":"Plumbing Services","isPartOf":{"@id":BASE_URL+"/#website"},"about":{"@id":BASE_URL+"/#localbusiness"},"inLanguage":"en-US"},
        breadcrumb_ld(breadcrumb_items),
    ]
    h = head(title, description, path, og_image="/og-image.jpg", extra_jsonld=extra, body_page="services-hub")
    n = nav("services")
    cards = [
        ("24-7-emergency-plumbing","🚨","24/7 Emergency Plumbing","Burst pipes, sewer backups, flooding — dispatched 24/7."),
        ("drain-cleaning","🚿","Drain Cleaning","Augering, hydro jetting, camera inspection."),
        ("water-heater-repair-replacement","🔥","Water Heater Services","Tank, tankless, heat-pump — repair &amp; install."),
        ("leak-detection","💦","Leak Detection","Slab, wall, underground — find &amp; fix hidden leaks."),
        ("plumbing-fixture-installation-repair","🚰","Fixture Install &amp; Repair","Toilets, faucets, sinks, disposals, showers."),
        ("well-pump-repair","💧","Well Pump Repair","Pumps, tanks, filtration, water testing."),
        ("backflow-prevention-testing","🛡️","Backflow Testing","Annual SC-certified testing &amp; repair."),
        ("commercial-plumbing","🏢","Commercial Plumbing","Restaurants, offices, retail, multi-family."),
    ]
    cards_html = "\n".join(
        f'<a class="nav-card" href="/services/{slug}/"><div style="font-size:1.8rem;margin-bottom:8px">{icon}</div><h3>{name}</h3><p>{desc}</p><span class="arrow">Learn more →</span></a>'
        for slug,icon,name,desc in cards
    )
    body = f"""\
<main>
  <section class="page-header">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
      <h1 class="speakable-headline">Plumbing Services in Abbeville &amp; Upstate SC</h1>
      <p class="speakable-summary">Every plumbing service homes and businesses need — handled by an SC Master Plumber with 30 years in the trade. Flat-rate pricing, 24/7 dispatch, 2-year warranty.</p>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="grid-4">
        {cards_html}
      </div>
    </div>
  </section>
  <section class="section bg-alt">
    <div class="container" style="text-align:center;max-width:680px">
      <span class="label">Not sure which service you need?</span>
      <h2>Call us and describe what you're seeing.</h2>
      <p class="lead" style="margin:14px auto 24px">We'll diagnose over the phone in most cases and give you a flat-rate quote range before we even leave the shop.</p>
      <a href="tel:+18644468911" class="btn btn-green btn-lg speakable-phone">📞 (864) 446-8911</a>
    </div>
  </section>
</main>
"""
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


# ─── Service areas hub ────────────────────────────────────────────────────
def render_areas_hub():
    path = "/service-areas/"
    title = "Service Areas — Plumbing Paramedic 911 across Upstate SC"
    description = "Plumbing Paramedic 911 services 8 cities across Upstate South Carolina — Abbeville, Greenwood, Anderson, Laurens, McCormick, Ninety Six, Calhoun Falls, Due West. Call (864) 446-8911."
    breadcrumb_items = [("Home","/"),("Service Areas", path)]
    extra = [
        {"@type":"CollectionPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":"Service Areas","isPartOf":{"@id":BASE_URL+"/#website"},"about":{"@id":BASE_URL+"/#localbusiness"},"inLanguage":"en-US"},
        breadcrumb_ld(breadcrumb_items),
    ]
    h = head(title, description, path, og_image="/og-image.jpg", extra_jsonld=extra, body_page="areas-hub")
    n = nav("areas")
    cards = []
    for slug,c in CITIES.items():
        cards.append(f'<a class="nav-card" href="/service-areas/{slug}/"><h3>📍 {c["city"]}, {c["abbr"]}</h3><p>Response time: {c["response"]}.</p><span class="arrow">{c["city"]} plumber →</span></a>')
    body = f"""\
<main>
  <section class="page-header">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
      <h1 class="speakable-headline">Service Areas Across Upstate South Carolina</h1>
      <p class="speakable-summary">Eight cities, one phone number. Based at 13 Callaway Dr in Abbeville — we dispatch to every city below 24/7.</p>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="grid-4">
        {chr(10).join(cards)}
      </div>
    </div>
  </section>
  <section class="section bg-alt">
    <div class="container" style="text-align:center;max-width:680px">
      <span class="label">Don't see your city?</span>
      <h2>Call — we likely serve your area too.</h2>
      <p class="lead" style="margin:14px auto 24px">We also routinely service Donalds, Hodges, Antreville, Bradley, Cokesbury, Honea Path, Iva, and Promised Land.</p>
      <a href="tel:+18644468911" class="btn btn-green btn-lg speakable-phone">📞 (864) 446-8911</a>
    </div>
  </section>
</main>
"""
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


# ─── Utility pages ────────────────────────────────────────────────────────
def render_about():
    path = "/about/"
    title = "About Eric Callaway, SC Master Plumber | Plumbing Paramedic 911"
    description = "Plumbing Paramedic 911 owner Eric Callaway is a South Carolina Master Plumber with 30 years in the trade. Family-owned, founded 2015, A+ BBB. Abbeville SC. Call (864) 446-8911."
    breadcrumb_items = [("Home","/"),("About", path)]
    extra = [
        {"@type":"AboutPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":"About Plumbing Paramedic 911","isPartOf":{"@id":BASE_URL+"/#website"},"about":{"@id":BASE_URL+"/#localbusiness"},"mainEntity":{"@id":BASE_URL+"/#eric-callaway"},"inLanguage":"en-US"},
        breadcrumb_ld(breadcrumb_items),
    ]
    h = head(title, description, path, extra_jsonld=extra, body_page="about")
    n = nav("about")
    body = f"""\
<main>
  <section class="page-header">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
      <h1 class="speakable-headline">About Plumbing Paramedic 911</h1>
      <p class="speakable-summary">Family-owned. SC Master Plumber-led. 30 years in the trade. Headquartered in Abbeville, South Carolina.</p>
    </div>
  </section>
  <section class="section">
    <div class="container" style="max-width:820px" class="prose">
      <article class="prose">
        <span class="label">Our Story</span>
        <h2>Eric Callaway, SC Master Plumber</h2>
        <div class="divider"></div>
        <p>Eric Callaway started in the plumbing trade in 1996 — apprenticing, learning the craft, eventually earning his South Carolina Master Plumber license. In 2015, he founded Plumbing Paramedic 911 in Abbeville. The shop has been at 13 Callaway Drive ever since.</p>
        <p>The "911" in the name is intentional. From day one, the company has been organized around the idea that plumbing emergencies don't wait — and a real human, with real licensure, should be on the other end of the phone when something goes wrong at 2 AM. There's no answering service. You call (864) 446-8911 and you reach someone who can dispatch.</p>
        <h3>What we believe</h3>
        <ul>
          <li><strong>Pricing should be transparent before we arrive.</strong> The traditional plumbing industry asks you to take it on faith — wait for a truck to show up, then wait for a verbal quote. We publish flat-rate prices online and confirm them in writing before any work begins.</li>
          <li><strong>Diagnostic shouldn't be a separate line item.</strong> We don't charge a "trip fee" on top of the repair. The quoted price is what you pay.</li>
          <li><strong>Quality should be warrantied.</strong> Every repair and installation carries a 2-year warranty on parts and labor. If it's not right, we come back and fix it at no charge.</li>
          <li><strong>Honesty about scope.</strong> If we find something hidden mid-job (extra leak behind a wall, rotted subfloor, a second issue upstream), we stop, explain, and re-quote before continuing.</li>
        </ul>
        <h3>Credentials &amp; recognition</h3>
        <ul>
          <li>South Carolina Master Plumber license — issued by SC Contractor's Licensing Board (LLR)</li>
          <li>BBB A+ Rating</li>
          <li>4.9-star average across Google, Facebook, and BBB</li>
          <li>32+ Google reviews and counting</li>
          <li>Licensed and insured for residential and commercial work statewide</li>
          <li>Certified for backflow prevention assembly testing across South Carolina</li>
        </ul>
        <h3>The team</h3>
        <p>Plumbing Paramedic 911 is family-run. Eric leads the shop. Blake and Dylan — Eric's sons — work alongside him and represent the next generation of plumbers being trained the right way: apprenticing, learning code, taking pride in clean work.</p>
        <h3>Where we work</h3>
        <p>We service eight cities in Upstate South Carolina from our Abbeville shop: <a href="/service-areas/abbeville-sc/">Abbeville</a>, <a href="/service-areas/greenwood-sc/">Greenwood</a>, <a href="/service-areas/anderson-sc/">Anderson</a>, <a href="/service-areas/laurens-sc/">Laurens</a>, <a href="/service-areas/mccormick-sc/">McCormick</a>, <a href="/service-areas/ninety-six-sc/">Ninety Six</a>, <a href="/service-areas/calhoun-falls-sc/">Calhoun Falls</a>, and <a href="/service-areas/due-west-sc/">Due West</a> — plus surrounding small towns and rural areas.</p>
        <h3>Want to talk?</h3>
        <p>Call (864) 446-8911 — emergencies are 24/7. For routine inquiries, we typically respond within 30 minutes during business hours. Or <a href="/contact/">drop us a message</a> and we'll call you back.</p>
      </article>
    </div>
  </section>
</main>
"""
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


def render_contact():
    path = "/contact/"
    title = "Contact Plumbing Paramedic 911 — (864) 446-8911 | Abbeville SC"
    description = "Call (864) 446-8911 for 24/7 plumbing service in Abbeville, Greenwood, Anderson, Laurens, McCormick &amp; Upstate SC. Or email plumbingparamedic911@gmail.com. Visit 13 Callaway Dr, Abbeville, SC."
    breadcrumb_items = [("Home","/"),("Contact", path)]
    extra = [
        {"@type":"ContactPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":"Contact","isPartOf":{"@id":BASE_URL+"/#website"},"about":{"@id":BASE_URL+"/#localbusiness"},"inLanguage":"en-US"},
        breadcrumb_ld(breadcrumb_items),
    ]
    h = head(title, description, path, extra_jsonld=extra, body_page="contact")
    n = nav("contact")
    body = f"""\
<main>
  <section class="page-header">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
      <h1 class="speakable-headline">Contact Plumbing Paramedic 911</h1>
      <p class="speakable-summary">Available 24 hours a day, 365 days a year for emergencies. Routine inquiries get a callback within 30 minutes during business hours.</p>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="grid-2" style="align-items:start;gap:48px">
        <div>
          <span class="label">Reach us</span>
          <h2>How to get in touch</h2>
          <div class="divider"></div>
          <div style="display:flex;flex-direction:column;gap:18px">
            <div style="display:flex;gap:14px;align-items:flex-start"><div style="font-size:1.6rem">📞</div><div><strong style="display:block;font-size:1.1rem">Phone (24/7)</strong><a href="tel:+18644468911" class="speakable-phone" style="font-family:var(--ff-head);font-weight:900;font-size:1.4rem;color:var(--blue);text-decoration:none">(864) 446-8911</a></div></div>
            <div style="display:flex;gap:14px;align-items:flex-start"><div style="font-size:1.6rem">✉</div><div><strong style="display:block;font-size:1.1rem">Email</strong><a href="mailto:plumbingparamedic911@gmail.com" style="color:var(--blue);font-weight:600">plumbingparamedic911@gmail.com</a></div></div>
            <div style="display:flex;gap:14px;align-items:flex-start"><div style="font-size:1.6rem">📍</div><div><strong style="display:block;font-size:1.1rem">Address</strong>13 Callaway Dr<br>Abbeville, SC 29620</div></div>
            <div style="display:flex;gap:14px;align-items:flex-start"><div style="font-size:1.6rem">⏰</div><div><strong style="display:block;font-size:1.1rem">Hours</strong>24 hours a day, 7 days a week<br>Every holiday — including Christmas Day</div></div>
          </div>
          <h3 style="margin-top:32px;font-size:1.2rem">Service area</h3>
          <p style="color:var(--ink2);line-height:1.8">Abbeville, Greenwood, Anderson, Laurens, McCormick, Ninety Six, Calhoun Falls, Due West, and surrounding Upstate South Carolina towns.</p>
        </div>
        <div>
          <div class="card">
            <h3 style="margin-bottom:14px">Send us a message</h3>
            <form class="lead-form" method="post" action="#">
              <div class="form-success">✅ Thanks — we'll be in touch within 30 minutes during business hours.</div>
              <div class="form-row-2">
                <div class="form-field"><label>Name</label><input type="text" name="name" autocomplete="name"></div>
                <div class="form-field"><label>Phone *</label><input type="tel" name="phone" required autocomplete="tel"></div>
              </div>
              <div class="form-field"><label>Email</label><input type="email" name="email" autocomplete="email"></div>
              <div class="form-field"><label>City / Town</label><input type="text" name="city"></div>
              <div class="form-field"><label>Service Needed</label>
                <select name="service"><option>Select…</option><option>Emergency</option><option>Drain Cleaning</option><option>Water Heater</option><option>Well Pump</option><option>Leak Detection</option><option>Backflow Testing</option><option>Fixture Install/Repair</option><option>Commercial</option><option>Other</option></select>
              </div>
              <div class="form-field"><label>Message</label><textarea name="message" style="min-height:90px"></textarea></div>
              <button type="submit" class="btn btn-green" style="width:100%;justify-content:center">Send →</button>
            </form>
            <p style="font-size:.78rem;color:var(--ink3);text-align:center;margin-top:12px">For active emergencies, please call (864) 446-8911 directly.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
"""
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


def render_pricing():
    path = "/pricing/"
    title = "Upfront Plumbing Pricing in Abbeville SC | Plumbing Paramedic 911"
    description = "Real flat-rate plumbing prices online — drain cleaning from $149, water heater replace from $899, well pump replace from $799. No hourly billing. Abbeville SC. Call (864) 446-8911."
    breadcrumb_items = [("Home","/"),("Pricing", path)]
    extra = [
        {"@type":"WebPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":"Pricing","isPartOf":{"@id":BASE_URL+"/#website"},"about":{"@id":BASE_URL+"/#localbusiness"},"inLanguage":"en-US"},
        breadcrumb_ld(breadcrumb_items),
        faq_ld([
            ("Is this price final or just an estimate?",
             "The ranges shown are honest estimates based on typical jobs in the Abbeville area. When we arrive, we give you an exact written price before any work starts. That price doesn't change — if the job goes longer than expected, that's on us, not you."),
            ("Do you charge a service call or diagnostic fee?",
             "We do not charge a separate diagnostic fee on top of the repair price. The service call fee is waived when you proceed with the repair. We'll always tell you upfront what the full cost will be."),
            ("What does the after-hours surcharge cover?",
             "The $150 after-hours surcharge applies to jobs scheduled outside of regular business hours (Mon–Fri 8 AM–6 PM), including evenings, weekends, and holidays. It covers dispatching outside normal hours. There are no additional fees beyond what you're quoted."),
            ("What if my job is more complicated than expected?",
             "If we discover additional issues during the job, we stop, explain what we found, quote any additional work, and get your approval before proceeding. We never add costs without your sign-off."),
            ("How does in-house financing work?",
             "For jobs over $500, we offer in-house financing with low interest rates regardless of your credit score. Ask us about financing options when you call or when our technician arrives."),
        ]),
    ]
    h = head(title, description, path, extra_jsonld=extra, body_page="pricing")
    n = nav("pricing")
    body = """\
<main>
  <div class="page-header">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><span>Pricing Calculator</span></nav>
      <h1 class="speakable-headline">Upfront Plumbing Pricing</h1>
      <p class="speakable-summary">Know your price before you book. Flat-rate pricing — no hourly guessing, no hidden fees.</p>
    </div>
  </div>

  <section class="section">
    <div class="container">
      <div class="grid-2" style="gap:48px;margin-bottom:56px;align-items:start">
        <div>
          <span class="label">Why We Do This</span>
          <h2>Transparent pricing that flips the industry</h2>
          <div class="divider"></div>
          <p class="lead" style="margin-bottom:16px">Most plumbers won't tell you what something costs until they're already in your home. We believe that's wrong.</p>
          <p style="color:var(--ink2);line-height:1.75;margin-bottom:20px">Our flat-rate pricing calculator gives you a real estimate for your specific job — before you make a single call. Every price includes labor and standard materials. There are no hourly rates, no travel fees, and no surprises on your invoice.</p>
          <ul class="check-list">
            <li>Same price regardless of how long the job takes</li>
            <li>After-hours &amp; emergency pricing shown upfront</li>
            <li>In-house financing on jobs over $500</li>
            <li>All estimates backed by our 2-year warranty</li>
            <li>Military, senior, police, fire &amp; EMS discounts apply</li>
          </ul>
        </div>
        <div style="background:var(--bg);border-radius:var(--r2);padding:28px;border:1.5px solid var(--line)">
          <div style="font-size:2.5rem;margin-bottom:12px;text-align:center">🏆</div>
          <h3 style="text-align:center;font-size:1.2rem;margin-bottom:16px">Our pricing promise</h3>
          <div style="display:flex;flex-direction:column;gap:14px">
            <div style="display:flex;align-items:flex-start;gap:12px"><div style="font-size:1.2rem">💎</div><div><strong style="display:block;font-size:.9rem">Price-Lock Guarantee</strong><span style="font-size:.82rem;color:var(--ink3)">The price you see is the price you pay. Period.</span></div></div>
            <div style="display:flex;align-items:flex-start;gap:12px"><div style="font-size:1.2rem">📋</div><div><strong style="display:block;font-size:.9rem">Written quote before we start</strong><span style="font-size:.82rem;color:var(--ink3)">You approve the price in writing before any work begins.</span></div></div>
            <div style="display:flex;align-items:flex-start;gap:12px"><div style="font-size:1.2rem">🛡️</div><div><strong style="display:block;font-size:.9rem">2-Year warranty included</strong><span style="font-size:.82rem;color:var(--ink3)">Every job covered for 2 years on parts and labor.</span></div></div>
            <div style="display:flex;align-items:flex-start;gap:12px"><div style="font-size:1.2rem">🏦</div><div><strong style="display:block;font-size:.9rem">In-house financing</strong><span style="font-size:.82rem;color:var(--ink3)">Flexible payments regardless of credit score on jobs $500+.</span></div></div>
          </div>
        </div>
      </div>

      <div class="calc-wrapper">
        <div class="calc-header">
          <h2>💰 Plumbing Price Estimator</h2>
          <p>Select your service → choose your options → get your upfront price estimate instantly.</p>
        </div>
        <div class="calc-tabs">
          <button class="calc-tab active" onclick="setCalcTab('common',this)">Common Repairs</button>
          <button class="calc-tab" onclick="setCalcTab('water-heater',this)">Water Heaters</button>
          <button class="calc-tab" onclick="setCalcTab('drain',this)">Drains &amp; Sewer</button>
          <button class="calc-tab" onclick="setCalcTab('well',this)">Well &amp; Pump</button>
          <button class="calc-tab" onclick="setCalcTab('remodel',this)">Remodel &amp; Install</button>
        </div>
        <div class="calc-body">
          <div id="calc-common" class="calc-tab-content">
            <h3 style="margin-bottom:16px;font-size:1rem">Select the service</h3>
            <div class="calc-service-grid">
              <button class="calc-service-btn selected" onclick="selectService(this,'Toilet Repair',89,149)"><span class="icon">🚽</span><span class="name">Toilet Repair</span><span class="range">$89 – $149</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Toilet Replace',249,449)"><span class="icon">🚽</span><span class="name">Toilet Replace</span><span class="range">$249 – $449</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Faucet Repair',89,169)"><span class="icon">🚰</span><span class="name">Faucet Repair</span><span class="range">$89 – $169</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Faucet Install',129,199)"><span class="icon">🚰</span><span class="name">Faucet Install</span><span class="range">$129 – $199</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Garbage Disposal',149,299)"><span class="icon">🔩</span><span class="name">Disposal Install</span><span class="range">$149 – $299</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Pipe Leak Repair',149,399)"><span class="icon">💦</span><span class="name">Pipe Leak Repair</span><span class="range">$149 – $399</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Burst Pipe Emergency',349,699)"><span class="icon">🚨</span><span class="name">Burst Pipe (Emergency)</span><span class="range">$349 – $699</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Shut-off Valve',149,249)"><span class="icon">🔧</span><span class="name">Shut-off Valve</span><span class="range">$149 – $249</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Plumbing Inspection',149,199)"><span class="icon">🔍</span><span class="name">Plumbing Inspection</span><span class="range">$149 – $199</span></button>
            </div>
          </div>
          <div id="calc-water-heater" class="calc-tab-content" style="display:none">
            <h3 style="margin-bottom:16px;font-size:1rem">Select water heater service</h3>
            <div class="calc-service-grid">
              <button class="calc-service-btn" onclick="selectService(this,'WH Repair',149,349)"><span class="icon">🔧</span><span class="name">Water Heater Repair</span><span class="range">$149 – $349</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'WH Replace 40gal',899,1299)"><span class="icon">🔥</span><span class="name">Replace 40-Gal Tank</span><span class="range">$899 – $1,299</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'WH Replace 50gal',999,1499)"><span class="icon">🔥</span><span class="name">Replace 50-Gal Tank</span><span class="range">$999 – $1,499</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Tankless Install',1599,2899)"><span class="icon">⚡</span><span class="name">Tankless Install</span><span class="range">$1,599 – $2,899</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Tankless Repair',199,499)"><span class="icon">⚡</span><span class="name">Tankless Repair</span><span class="range">$199 – $499</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Anode Rod',149,199)"><span class="icon">🛡️</span><span class="name">Anode Rod Replace</span><span class="range">$149 – $199</span></button>
            </div>
          </div>
          <div id="calc-drain" class="calc-tab-content" style="display:none">
            <h3 style="margin-bottom:16px;font-size:1rem">Select drain / sewer service</h3>
            <div class="calc-service-grid">
              <button class="calc-service-btn" onclick="selectService(this,'Drain Clean (1 drain)',149,249)"><span class="icon">🚿</span><span class="name">Single Drain Clean</span><span class="range">$149 – $249</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Main Line Clean',249,449)"><span class="icon">🌊</span><span class="name">Main Line Clean</span><span class="range">$249 – $449</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Hydro Jetting',399,699)"><span class="icon">💪</span><span class="name">Hydro Jetting</span><span class="range">$399 – $699</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Sewer Inspection',199,299)"><span class="icon">🔍</span><span class="name">Sewer Camera Inspect</span><span class="range">$199 – $299</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Sewer Line Repair',899,2499)"><span class="icon">🛠️</span><span class="name">Sewer Line Repair</span><span class="range">$899 – $2,499</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Sewer Line Replace',2499,5999)"><span class="icon">⚠️</span><span class="name">Sewer Line Replace</span><span class="range">$2,499 – $5,999</span></button>
            </div>
          </div>
          <div id="calc-well" class="calc-tab-content" style="display:none">
            <h3 style="margin-bottom:16px;font-size:1rem">Select well / pump service</h3>
            <div class="calc-service-grid">
              <button class="calc-service-btn" onclick="selectService(this,'Well Pump Repair',349,699)"><span class="icon">🔧</span><span class="name">Well Pump Repair</span><span class="range">$349 – $699</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Well Pump Replace',799,1599)"><span class="icon">💧</span><span class="name">Well Pump Replace</span><span class="range">$799 – $1,599</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Pressure Tank',499,899)"><span class="icon">⚙️</span><span class="name">Pressure Tank Replace</span><span class="range">$499 – $899</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Water Test',99,199)"><span class="icon">🧪</span><span class="name">Water Quality Test</span><span class="range">$99 – $199</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Water Filtration',599,1499)"><span class="icon">🌿</span><span class="name">Filtration System</span><span class="range">$599 – $1,499</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Sump Pump',349,699)"><span class="icon">🪣</span><span class="name">Sump Pump Install</span><span class="range">$349 – $699</span></button>
            </div>
          </div>
          <div id="calc-remodel" class="calc-tab-content" style="display:none">
            <h3 style="margin-bottom:16px;font-size:1rem">Select remodel / install service</h3>
            <div class="calc-service-grid">
              <button class="calc-service-btn" onclick="selectService(this,'Shower Install',599,1499)"><span class="icon">🚿</span><span class="name">Shower Install</span><span class="range">$599 – $1,499</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Bathtub Install',799,1999)"><span class="icon">🛁</span><span class="name">Bathtub Install</span><span class="range">$799 – $1,999</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Sink Install',149,349)"><span class="icon">🚰</span><span class="name">Sink Install</span><span class="range">$149 – $349</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Full Bath Remodel (plumbing)',1499,3999)"><span class="icon">🏠</span><span class="name">Full Bath Remodel (plumbing)</span><span class="range">$1,499 – $3,999</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Whole House Repipe',3499,8999)"><span class="icon">🔩</span><span class="name">Whole-House Repipe</span><span class="range">$3,499 – $8,999</span></button>
              <button class="calc-service-btn" onclick="selectService(this,'Water Line Install',499,1499)"><span class="icon">🏗️</span><span class="name">Water Line Install</span><span class="range">$499 – $1,499</span></button>
            </div>
          </div>
          <div class="calc-options">
            <h3 style="font-size:1rem;margin-bottom:6px">Customize your estimate</h3>
            <p style="font-size:.8rem;color:var(--ink3);margin-bottom:16px">Adjust options to match your situation for a more accurate estimate.</p>
            <div style="margin-bottom:20px">
              <div style="font-weight:700;font-size:.88rem;margin-bottom:10px;color:var(--ink)">🏠 Property Type</div>
              <div class="option-group">
                <div class="option-radio selected" onclick="selectOption(this,'property','residential',0)"><div class="option-radio-left"><div class="option-radio-dot"></div><div><div class="option-radio-name">Residential Home</div><div class="option-radio-desc">Single-family, townhome, or manufactured home</div></div></div><div class="option-radio-price">Base price</div></div>
                <div class="option-radio" onclick="selectOption(this,'property','commercial',150)"><div class="option-radio-left"><div class="option-radio-dot"></div><div><div class="option-radio-name">Commercial / Business</div><div class="option-radio-desc">Office, retail, restaurant, or other commercial property</div></div></div><div class="option-radio-price">+$150</div></div>
              </div>
            </div>
            <div style="margin-bottom:20px">
              <div style="font-weight:700;font-size:.88rem;margin-bottom:10px;color:var(--ink)">🕐 Timing</div>
              <div class="calc-timing">
                <button class="timing-btn active" onclick="selectTiming(this,'business',0)"><strong>Business Hours</strong><span>Mon–Fri 8 AM–6 PM</span></button>
                <button class="timing-btn" onclick="selectTiming(this,'after',150)"><strong>After Hours / Emergency</strong><span>Evenings, Weekends, Holidays</span></button>
              </div>
            </div>
            <div>
              <div style="font-weight:700;font-size:.88rem;margin-bottom:10px;color:var(--ink)">🎖️ Discount (if applicable)</div>
              <div class="option-group">
                <div class="option-radio selected" onclick="selectOption(this,'discount','none',0)"><div class="option-radio-left"><div class="option-radio-dot"></div><div><div class="option-radio-name">No discount</div></div></div><div class="option-radio-price">—</div></div>
                <div class="option-radio" onclick="selectOption(this,'discount','military',-50)"><div class="option-radio-left"><div class="option-radio-dot"></div><div><div class="option-radio-name">Military / Veteran</div><div class="option-radio-desc">Active duty or honorably discharged veteran</div></div></div><div class="option-radio-price" style="color:var(--red)">−$50</div></div>
                <div class="option-radio" onclick="selectOption(this,'discount','senior',-50)"><div class="option-radio-left"><div class="option-radio-dot"></div><div><div class="option-radio-name">Senior Citizen (65+)</div></div></div><div class="option-radio-price" style="color:var(--red)">−$50</div></div>
                <div class="option-radio" onclick="selectOption(this,'discount','first-responder',-50)"><div class="option-radio-left"><div class="option-radio-dot"></div><div><div class="option-radio-name">Police / Fire / EMS</div></div></div><div class="option-radio-price" style="color:var(--red)">−$50</div></div>
              </div>
            </div>
          </div>
          <div class="calc-result">
            <div class="calc-result-label">Your flat-rate estimate</div>
            <div class="calc-price-row">
              <div>
                <div class="calc-price-main" id="calcPriceDisplay">$89 – $149</div>
                <div class="calc-price-sub" id="calcPriceSub">Toilet Repair · Business Hours · Residential</div>
              </div>
              <div style="text-align:right">
                <div style="font-family:var(--ff-head);font-size:.82rem;font-weight:700;opacity:.7;letter-spacing:1px">Includes</div>
                <div style="font-size:.82rem;opacity:.8;margin-top:3px">Labor + standard materials</div>
                <div style="font-size:.82rem;opacity:.8">2-year warranty</div>
              </div>
            </div>
            <div class="calc-breakdown">
              <div class="breakdown-row"><span>Base service</span><span id="bd-base">$89 – $149</span></div>
              <div class="breakdown-row"><span>After-hours surcharge</span><span id="bd-surcharge">$0</span></div>
              <div class="breakdown-row"><span>Commercial adjustment</span><span id="bd-commercial">$0</span></div>
              <div class="breakdown-row"><span id="bd-discount-label">Discount</span><span id="bd-discount">$0</span></div>
              <div class="breakdown-row"><span>Estimated total</span><span id="bd-total">$89 – $149</span></div>
            </div>
            <div class="calc-disclaimer">* Estimate based on typical job conditions in the Abbeville, SC area. Final price confirmed before any work begins. Prices may vary for complex jobs, hard-to-reach areas, or special materials. Call for a free phone estimate on larger projects.</div>
            <div class="calc-actions">
              <a href="tel:+18644468911" class="btn btn-green">📞 Call to book: (864) 446-8911</a>
              <button class="btn btn-outline-white btn-sm" onclick="printEstimate()">🖨️ Print estimate</button>
            </div>
          </div>
          <div class="calc-trust">
            <div class="calc-trust-item"><div class="calc-trust-icon">💎</div><span class="calc-trust-label">Price-Lock Guarantee</span><span class="calc-trust-sub">Quoted price is final price</span></div>
            <div class="calc-trust-item"><div class="calc-trust-icon">🛡️</div><span class="calc-trust-label">2-Year Warranty</span><span class="calc-trust-sub">All parts &amp; labor covered</span></div>
            <div class="calc-trust-item"><div class="calc-trust-icon">🏦</div><span class="calc-trust-label">In-House Financing</span><span class="calc-trust-sub">Jobs $500+ · any credit</span></div>
          </div>
        </div>
      </div>

      <div style="margin-top:56px;max-width:760px">
        <span class="label">Pricing FAQ</span>
        <h2 style="margin-bottom:28px">Common pricing questions</h2>
        <div class="faq-item"><button class="faq-q" type="button" aria-expanded="false"><span>Is this price final or just an estimate?</span><span class="faq-arrow">+</span></button><div class="faq-a">The ranges shown are honest estimates based on typical jobs in the Abbeville area. When we arrive, we give you an exact written price before any work starts. That price doesn't change — if the job goes longer than expected, that's on us, not you.</div></div>
        <div class="faq-item"><button class="faq-q" type="button" aria-expanded="false"><span>Do you charge a service call or diagnostic fee?</span><span class="faq-arrow">+</span></button><div class="faq-a">We do not charge a separate diagnostic fee on top of the repair price. The service call fee is waived when you proceed with the repair. We'll always tell you upfront what the full cost will be.</div></div>
        <div class="faq-item"><button class="faq-q" type="button" aria-expanded="false"><span>What does the after-hours surcharge cover?</span><span class="faq-arrow">+</span></button><div class="faq-a">The $150 after-hours surcharge applies to jobs scheduled outside of regular business hours (Mon–Fri 8 AM–6 PM), including evenings, weekends, and holidays. It covers dispatching our team outside normal hours. There are no additional fees beyond what you're quoted.</div></div>
        <div class="faq-item"><button class="faq-q" type="button" aria-expanded="false"><span>What if my job is more complicated than expected?</span><span class="faq-arrow">+</span></button><div class="faq-a">If we discover additional issues during the job, we'll stop, explain what we found, quote any additional work, and get your approval before proceeding. We never add costs without your sign-off.</div></div>
        <div class="faq-item"><button class="faq-q" type="button" aria-expanded="false"><span>How does in-house financing work?</span><span class="faq-arrow">+</span></button><div class="faq-a">For jobs over $500, we offer in-house financing with low interest rates regardless of your credit score. Ask us about financing options when you call or when our technician arrives.</div></div>
      </div>
    </div>
  </section>
</main>
"""
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


def render_faq():
    path = "/faq/"
    title = "Plumbing FAQ — Abbeville, Greenwood &amp; Upstate SC | Plumbing Paramedic 911"
    description = "Common questions about plumbing service in Abbeville, Greenwood, Anderson, Laurens &amp; Upstate SC. Pricing, warranty, licensing, financing, emergencies. Call (864) 446-8911."
    breadcrumb_items = [("Home","/"),("FAQ", path)]
    faqs = [
        ("Who is the best 24-hour emergency plumber near me in Abbeville, SC?",
         "Plumbing Paramedic 911, owned by SC Master Plumber Eric Callaway, offers 24/7 emergency plumbing in Abbeville, Greenwood, Anderson, Laurens, McCormick, Ninety Six, Calhoun Falls, and Due West. Call (864) 446-8911 any time."),
        ("What plumbing services does Plumbing Paramedic 911 offer?",
         "Drain cleaning, water heater repair and replacement, leak detection, fixture installation and repair, well pump repair, backflow prevention testing, commercial plumbing, and 24/7 emergency plumbing for residential and commercial customers."),
        ("Are you a licensed Master Plumber in South Carolina?",
         "Yes. Owner Eric Callaway is a licensed South Carolina Master Plumber. He has worked in the plumbing trade since 1996 and founded Plumbing Paramedic 911 in 2015."),
        ("How much does an emergency plumber cost in Abbeville SC?",
         "Plumbing Paramedic 911 gives free up-front estimates before any work begins. Standard service visits are quoted at flat-rate prices; emergency dispatch fees apply for after-hours calls. Call (864) 446-8911 for a no-obligation quote."),
        ("Do you test backflow preventers in South Carolina?",
         "Yes. We are certified to perform backflow prevention assembly testing, repair, and installation for residential and commercial properties throughout South Carolina, meeting state and municipal cross-connection control requirements."),
        ("Do you repair well pumps in rural Upstate SC?",
         "Yes. We repair submersible and jet well pumps, replace pressure tanks, and troubleshoot well water systems across rural Abbeville, McCormick, and Anderson counties. Same-day service is available in most cases."),
        ("Do you offer financing?",
         "Yes. In-house financing is available on any job over $500. We work with all credit profiles — there is no credit-score minimum. Ask at quote time and we'll walk you through the options."),
        ("What is your warranty?",
         "Every repair and installation we perform carries a 2-year warranty on parts and labor. If anything fails within that window, we come back and fix it at no charge."),
        ("Do you charge for travel?",
         "No. Our flat-rate pricing includes travel within our normal service area — Abbeville, Greenwood, Anderson, Laurens, McCormick, and surrounding cities. There is no per-mile or distance surcharge."),
        ("Do you offer military, senior, or first-responder discounts?",
         "Yes. We offer $50 off for active-duty military, honorably discharged veterans, seniors aged 65+, and active police, fire, or EMS personnel. Mention the discount when scheduling."),
        ("How fast can you get to my house?",
         "Within Abbeville city limits, typical emergency response is 30 to 45 minutes from your call. Surrounding cities (Greenwood, Anderson, Laurens, McCormick) are 45 to 75 minutes depending on time of day and current job queue."),
        ("Do you handle commercial accounts?",
         "Yes. We work with property management companies, restaurants, offices, retail, and multi-family properties across Upstate SC. Monthly statement billing and net-30 terms available for established accounts."),
        ("What if you don't serve my area?",
         "Call (864) 446-8911 — we likely do. In addition to our 8 named service-area cities, we routinely service Donalds, Hodges, Antreville, Bradley, Cokesbury, Honea Path, Iva, and Promised Land. If we can't help, we'll point you to someone who can."),
        ("Can I get a price over the phone?",
         "In most cases, yes. We'll give you a flat-rate range based on what you describe before we dispatch. The exact price is confirmed in writing on-site, before any work begins."),
        ("Why is my water bill suddenly high?",
         "Most sudden water-bill jumps come from a hidden leak — a running toilet, an underground supply-line leak, a slab leak, or a leaking irrigation system. Check your meter with all fixtures off; if it spins, you have a leak. We can find it in 30–60 minutes."),
    ]
    extra = [
        {"@type":"FAQPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":"FAQ","isPartOf":{"@id":BASE_URL+"/#website"},"about":{"@id":BASE_URL+"/#localbusiness"},"inLanguage":"en-US","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
        breadcrumb_ld(breadcrumb_items),
    ]
    h = head(title, description, path, extra_jsonld=extra, body_page="faq")
    n = nav()
    body = f"""\
<main>
  <section class="page-header">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
      <h1 class="speakable-headline">Plumbing FAQ</h1>
      <p class="speakable-summary">The questions we get every week — answered straight, with prices and details where they help.</p>
    </div>
  </section>
  <section class="section">
    <div class="container" style="max-width:820px">
      {faq_html(faqs)}
    </div>
  </section>
  <section class="section bg-alt">
    <div class="container" style="text-align:center;max-width:680px">
      <h2>Still have a question?</h2>
      <p class="lead" style="margin:14px auto 24px">Call (864) 446-8911 or <a href="/contact/">send a message</a>. We answer fast.</p>
      <a href="tel:+18644468911" class="btn btn-green btn-lg speakable-phone">📞 (864) 446-8911</a>
    </div>
  </section>
</main>
"""
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


def render_reviews():
    path = "/reviews/"
    title = "Reviews — Plumbing Paramedic 911 | Abbeville SC"
    description = "Real customer reviews of Plumbing Paramedic 911 from homeowners across Abbeville, Greenwood, Anderson &amp; Upstate SC. 4.9★ average, 32+ Google reviews, A+ BBB. Call (864) 446-8911."
    breadcrumb_items = [("Home","/"),("Reviews", path)]
    reviews = [
        ("James T.","Abbeville, SC",5,"Eric showed up at midnight for a burst pipe. Fixed it fast, price was exactly what he said on the phone. No invoice surprises. This is the only plumber I'll ever call."),
        ("Susan M.","Greenwood, SC",5,"Well pump died on a Friday. The Plumbing Paramedic 911 team came out same afternoon. They explained the price before starting, got the job done right, and everything's been perfect since."),
        ("Robert K.","McCormick, SC",5,"Got a quote from another company for $2,800 to replace my water heater. Plumbing Paramedic 911 did the same job for $1,100 with a 2-year warranty. The transparency alone is worth 5 stars."),
        ("Linda P.","Anderson, SC",5,"Called for a slab leak. They located it in 45 minutes — turned out to be a pinhole leak in the hot water line. Repaired it the same day without tearing up the whole floor. Excellent work."),
        ("Mark D.","Laurens, SC",5,"Drain backed up on a Sunday. They had it cleared in under an hour, then ran a camera to show me a root intrusion. Hydro-jetted it the next week. Fair price, did what they said they'd do."),
        ("Patricia S.","Due West, SC",5,"Our 1920s house had original galvanized supply lines. They repiped the whole house with PEX in two days. Clean job, great crew, water pressure is incredible now."),
        ("Daniel R.","Calhoun Falls, SC",5,"Frozen pipe at our lake house in January. They drove out from Abbeville the same morning, thawed and repaired the line, and added insulation. Saved us from a flooded house."),
        ("Karen H.","Ninety Six, SC",5,"Quick faucet install — under $200 like the website said. They came when scheduled, did the work in 30 minutes, cleaned up. No upselling. Just honest plumbing."),
        ("Tom B.","Greenwood, SC",5,"Tankless water heater install. Eric walked me through every option before quoting. The install was clean, code-compliant, and the price was exactly what he wrote down."),
        ("Beth K.","Abbeville, SC",5,"Backflow test for our irrigation. Easy scheduling, paperwork filed with the city, done in 30 minutes. They'll be doing this every year for us now."),
    ]
    extra = [
        {"@type":"WebPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":"Reviews","isPartOf":{"@id":BASE_URL+"/#website"},"about":{"@id":BASE_URL+"/#localbusiness"},"inLanguage":"en-US"},
        breadcrumb_ld(breadcrumb_items),
    ]
    h = head(title, description, path, extra_jsonld=extra, body_page="reviews")
    n = nav()
    cards = []
    for name,city,stars,text in reviews:
        initials = "".join(p[0] for p in name.split()[:2]).upper()
        cards.append(f'<article class="review-card"><div class="review-quote">"</div><div class="stars" aria-label="{stars} out of 5 stars">{"★"*stars}{"☆"*(5-stars)}</div><p class="review-text">{text}</p><div class="reviewer"><div class="avatar">{initials}</div><div><div class="reviewer-name">{name}</div><div class="reviewer-meta">{city}</div></div></div></article>')
    body = f"""\
<main>
  <section class="page-header">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
      <h1 class="speakable-headline">Customer Reviews</h1>
      <p class="speakable-summary">4.9★ average across Google, Facebook, and BBB. 32+ Google reviews and growing. Here's what Upstate SC homeowners say.</p>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <div class="grid-3">
        {chr(10).join(cards)}
      </div>
    </div>
  </section>
  <section class="section bg-alt">
    <div class="container" style="text-align:center;max-width:680px">
      <h2>Had a good experience? Leave a review.</h2>
      <p class="lead" style="margin:14px auto 24px">Your review helps other Upstate SC homeowners find an honest plumber.</p>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
        <a href="https://www.google.com/search?q=Plumbing+Paramedic+911+Abbeville+SC" target="_blank" rel="noopener" class="btn btn-blue">Review on Google</a>
        <a href="https://www.bbb.org/us/sc/abbeville/profile/plumber/plumbing-paramedic-911-0673-90010577" target="_blank" rel="noopener" class="btn btn-blue">Review on BBB</a>
        <a href="https://www.facebook.com/PlumbingParamedic911/" target="_blank" rel="noopener" class="btn btn-blue">Review on Facebook</a>
      </div>
    </div>
  </section>
</main>
"""
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


def render_financing():
    path = "/financing/"
    title = "Plumbing Financing — Abbeville SC | Plumbing Paramedic 911"
    description = "In-house plumbing financing on jobs over $500. All credit profiles welcome. Flexible payments for water heaters, repipes, sewer line, and emergency repairs in Upstate SC. Call (864) 446-8911."
    breadcrumb_items = [("Home","/"),("Financing", path)]
    extra = [
        {"@type":"WebPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":"Financing","isPartOf":{"@id":BASE_URL+"/#website"},"about":{"@id":BASE_URL+"/#localbusiness"},"inLanguage":"en-US"},
        breadcrumb_ld(breadcrumb_items),
    ]
    h = head(title, description, path, extra_jsonld=extra, body_page="financing")
    n = nav()
    body = f"""\
<main>
  <section class="page-header">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
      <h1 class="speakable-headline">Plumbing Financing</h1>
      <p class="speakable-summary">A plumbing emergency shouldn't push you into financial stress. We offer in-house financing on any job over $500 — flexible payments, any credit profile.</p>
    </div>
  </section>
  <section class="section">
    <div class="container" style="max-width:820px">
      <article class="prose">
        <span class="label">How It Works</span>
        <h2>Straightforward, in-house, no third-party paperwork</h2>
        <div class="divider"></div>
        <p>For jobs over $500 — water heater replacements, sewer line repairs, repipes, emergency repairs, well-pump replacements, full bathroom remodels — we offer in-house financing. That means no separate finance company, no hard credit check, no application that can drag on for days.</p>
        <h3>What we offer</h3>
        <ul>
          <li>Available on any job over $500</li>
          <li>All credit profiles welcome — there is no minimum score</li>
          <li>Fixed monthly payments — you know exactly what you owe each month</li>
          <li>Flexible terms — choose what works for your budget</li>
          <li>No prepayment penalty — pay it off early without fees</li>
          <li>Quick approval — usually same-day, often during the initial quote</li>
        </ul>
        <h3>What you'll need</h3>
        <p>To start, we need basic information: name, address, ID, and a way to verify income (pay stub, bank statement, or SSI/disability documentation if applicable). That's it. Most approvals happen within the first hour of the service visit.</p>
        <h3>What jobs are commonly financed</h3>
        <ul>
          <li>Water heater replacement — $899 to $2,899</li>
          <li>Whole-house repipe — $3,499 to $8,999</li>
          <li>Sewer line repair or replacement — $899 to $5,999</li>
          <li>Well pump replacement — $799 to $1,599</li>
          <li>Full bath remodel (plumbing) — $1,499 to $3,999</li>
          <li>Backflow assembly replacement — $399 to $599</li>
        </ul>
        <h3>How to apply</h3>
        <p>Easiest path: call (864) 446-8911 and let us know you want to discuss financing during the quote. We'll work through the numbers with you on-site. You'll know exactly what your monthly payment is before you sign off on any work.</p>
        <p>You can also <a href="/contact/">send us a message</a> with the details and we'll call back to walk you through options.</p>
      </article>
    </div>
  </section>
  <section class="section bg-alt">
    <div class="container" style="text-align:center;max-width:680px">
      <h2>Need to schedule and finance a job?</h2>
      <p class="lead" style="margin:14px auto 24px">Call us. We'll walk through the work and the payment plan in one conversation.</p>
      <a href="tel:+18644468911" class="btn btn-green btn-lg speakable-phone">📞 (864) 446-8911</a>
    </div>
  </section>
</main>
"""
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


def render_legal(slug: str, title_str: str, body_html: str):
    path = f"/{slug}/"
    description = f"{title_str} for Plumbing Paramedic 911, an Abbeville, SC plumbing company."
    breadcrumb_items = [("Home","/"),(title_str, path)]
    extra = [
        {"@type":"WebPage","@id":BASE_URL+path+"#webpage","url":BASE_URL+path,"name":title_str,"isPartOf":{"@id":BASE_URL+"/#website"},"inLanguage":"en-US"},
        breadcrumb_ld(breadcrumb_items),
    ]
    h = head(f"{title_str} | Plumbing Paramedic 911", description, path, extra_jsonld=extra, body_page=slug)
    n = nav()
    body = f"""\
<main>
  <section class="page-header">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
      <h1>{title_str}</h1>
    </div>
  </section>
  <section class="section">
    <div class="container" style="max-width:820px">
      <article class="prose">
        {body_html}
      </article>
    </div>
  </section>
</main>
"""
    return h + n + body + FOOTER_HTML + "</body>\n</html>\n"


# ─── Main entry ────────────────────────────────────────────────────────────
def write(path_rel: str, html: str):
    target = os.path.join(ROOT, path_rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {path_rel}")


def main():
    # Services (7 — the 8th, emergency-plumbing, is hand-authored)
    for slug, s in SERVICES.items():
        write(f"services/{slug}/index.html", render_service_page(slug, s))
    # Cities
    for slug, c in CITIES.items():
        write(f"service-areas/{slug}/index.html", render_city_page(slug, c))
    # Hubs
    write("services/index.html", render_services_hub())
    write("service-areas/index.html", render_areas_hub())
    # Utilities
    write("about/index.html", render_about())
    write("contact/index.html", render_contact())
    write("pricing/index.html", render_pricing())
    write("faq/index.html", render_faq())
    write("reviews/index.html", render_reviews())
    write("financing/index.html", render_financing())
    # Legal
    privacy_body = """\
<p><em>Last updated: May 2026</em></p>
<p>Plumbing Paramedic 911, LLC ("we," "us," or "our") respects your privacy. This Privacy Policy explains how we collect, use, and protect information when you visit plumbingparamedic911.com or use our plumbing services.</p>
<h3>Information we collect</h3>
<ul>
  <li><strong>Contact details</strong> you provide through forms or by phone — name, phone number, email, address, and service description</li>
  <li><strong>Service records</strong> — what work we performed, parts used, dates, and warranty information</li>
  <li><strong>Payment information</strong> — for jobs paid by card or financed, processed by our payment processor</li>
  <li><strong>Site analytics</strong> — through Google Analytics 4: pages viewed, time on site, browser type, approximate location. No personally identifying information is collected in this stream.</li>
  <li><strong>Cookies</strong> — limited cookies for analytics and form functionality. No advertising cookies.</li>
</ul>
<h3>How we use information</h3>
<ul>
  <li>To dispatch plumbers, complete service, and bill correctly</li>
  <li>To follow up on warranty claims or scheduled service</li>
  <li>To respond to questions you send through forms or email</li>
  <li>To improve the website (anonymous analytics only)</li>
</ul>
<h3>How we don't use information</h3>
<ul>
  <li>We do not sell your information to anyone, for any reason</li>
  <li>We do not share your information with advertisers</li>
  <li>We do not send you marketing emails unless you explicitly request them</li>
</ul>
<h3>Third parties</h3>
<p>Google Analytics 4 collects anonymous site usage data. Our payment processor handles card transactions. Both are governed by their own privacy policies.</p>
<h3>Your rights</h3>
<p>You may request a copy of any personal information we hold about you, request correction, or request deletion, by emailing <a href="mailto:plumbingparamedic911@gmail.com">plumbingparamedic911@gmail.com</a> or calling (864) 446-8911.</p>
<h3>Contact</h3>
<p>Plumbing Paramedic 911, LLC<br>13 Callaway Dr<br>Abbeville, SC 29620<br>(864) 446-8911<br>plumbingparamedic911@gmail.com</p>
"""
    terms_body = """\
<p><em>Last updated: May 2026</em></p>
<h3>Service terms</h3>
<p>By scheduling service with Plumbing Paramedic 911, LLC, you agree to the following:</p>
<ul>
  <li><strong>Quotes</strong> are provided in writing before any work begins. The quoted price is the final price unless we discover hidden conditions, in which case we will stop, explain, and re-quote before continuing.</li>
  <li><strong>Payment</strong> is due on completion of work for cash, check, and card transactions. Financed jobs are governed by the financing agreement signed at the time of service.</li>
  <li><strong>Warranty</strong>: every repair and installation carries a 2-year warranty on parts and labor from the date of service. The warranty covers defects in our workmanship and the parts we provided. It does not cover damage caused by misuse, unrelated future failures, or work performed by others on the same system after our visit.</li>
  <li><strong>Access</strong>: you authorize Plumbing Paramedic 911 staff to access the work area at the time of the appointment.</li>
  <li><strong>Permits</strong>: where municipal permits are required, we pull the permit at our standard rate; the permit fee is your responsibility.</li>
</ul>
<h3>Limitation of liability</h3>
<p>Plumbing Paramedic 911, LLC's liability is limited to the amount paid for the work in question. We are not liable for incidental or consequential damages.</p>
<h3>Website terms</h3>
<p>Content on this website is provided for general information. Prices shown are estimates; final quotes are provided on-site.</p>
<h3>Governing law</h3>
<p>These terms are governed by the laws of the State of South Carolina. Any disputes will be resolved in the courts of Abbeville County, SC.</p>
<h3>Contact</h3>
<p>Plumbing Paramedic 911, LLC<br>13 Callaway Dr<br>Abbeville, SC 29620<br>(864) 446-8911<br>plumbingparamedic911@gmail.com</p>
"""
    write("privacy/index.html", render_legal("privacy","Privacy Policy", privacy_body))
    write("terms/index.html", render_legal("terms","Terms of Service", terms_body))


if __name__ == "__main__":
    main()
