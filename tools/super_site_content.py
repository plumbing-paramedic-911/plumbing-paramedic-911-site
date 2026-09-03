#!/usr/bin/env python3
"""Safe consolidation layer for the Plumbing Paramedic 911 super site.

This module selectively restores useful assets from the former 8911 site into
the canonical generator-driven site. It intentionally does NOT copy legacy
templates, CSS, deployment logic, stale pricing, or duplicate pages wholesale.

The migration rules are:
- preserve proven/valuable legacy URLs when they add distinct search intent;
- keep deliberate 301 consolidations when a legacy URL would cannibalize a
  stronger current page;
- normalize every restored page to the canonical NAP, current pricing model,
  current schema graph, current design system, and current internal links.
"""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://plumbingparamedic911.com"
LASTMOD = "2026-08-29"

SERVICE_ADDITIONS = {
    "sewer-line-repair": {
        "title": "Sewer Line Repair Abbeville SC | Plumbing Paramedic 911",
        "description": "Sewer line diagnosis and repair in Abbeville, Greenwood and Upstate SC. Camera inspection, spot repair and replacement planning with upfront pricing. Call (864) 446-8911.",
        "h1": "Sewer Line Repair in Abbeville & Upstate SC",
        "badge": "● Camera-First Sewer Diagnosis",
        "intro": "Recurring backups, several slow drains, sewer odor, gurgling fixtures or a wet area over the building sewer can point to more than a simple clog. We diagnose the line first, identify the damaged section and explain the least disruptive repair that fits the actual condition.",
        "schema_id": f"{BASE_URL}/#service-sewerline",
        "service_type": "Sewer Line Repair",
        "schema_desc": "Sewer line inspection, diagnosis, spot repair and replacement planning for damaged, root-intruded, offset or deteriorated building sewers in Upstate South Carolina.",
        "price_range": "$899 – $5,999+",
        "price_note": "Planning range from the current price book: repair $899–$2,499; replacement $2,499–$5,999. The service / diagnostic call is separate and the written repair price is approved before work begins.",
        "og": "/images/og/sewer-line-1200x630.jpg",
        "body": """
<h3>Signs the problem may be in the sewer line</h3>
<ul>
  <li>Several fixtures slow down or back up at the same time</li>
  <li>Water rises in a tub or shower when a toilet is flushed</li>
  <li>Recurring main-line clogs after previous clearing</li>
  <li>Gurgling fixtures or persistent sewer odor</li>
  <li>Wet, settled or unusually soft ground along the sewer route</li>
</ul>
<h3>Diagnosis before excavation</h3>
<p>We first separate a fixture or branch-line blockage from a main sewer problem. When recurring clogs or pipe damage are suspected, camera inspection can help locate roots, offsets, breaks, bellies or deteriorated pipe before repair work is recommended.</p>
<h3>Repair options depend on the pipe</h3>
<p>A short damaged section may be repairable without replacing the entire sewer. A line with widespread deterioration, repeated offsets or structural failure may need a larger replacement. Access, depth, length, existing material and site conditions all affect the repair plan.</p>
<h3>Why older properties need a careful look</h3>
<p>Homes across Abbeville and the surrounding Upstate have a mix of older and newer drain materials. Older cast iron, clay or previously repaired lines can fail differently from modern PVC. The goal is to identify the actual failure instead of repeatedly clearing the same symptom.</p>
""",
        "faqs": [
            ("How much does sewer line repair cost in Abbeville, SC?", "Our current planning range is $899–$2,499 for sewer line repair and $2,499–$5,999 for replacement. The service / diagnostic call is separate: $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. Site conditions, depth, access and pipe condition can change the written quote."),
            ("Do you camera the sewer before recommending repair?", "When the symptoms suggest recurring blockage or structural damage, camera inspection can help identify the location and condition before excavation or replacement is recommended."),
            ("Can tree roots cause repeat sewer backups?", "Yes. Roots can enter damaged joints or cracks and catch waste. Clearing roots can restore flow, but repeated intrusion usually means the underlying pipe condition should be evaluated."),
            ("Does every sewer backup mean the line must be replaced?", "No. Some backups are caused by a removable blockage or one localized damaged section. We diagnose the cause before recommending replacement."),
        ],
    },
    "pipe-repair-repiping": {
        "title": "Pipe Repair & Repiping Abbeville SC | Plumbing Paramedic 911",
        "description": "Pipe leak repair and whole-home repiping in Abbeville and Upstate SC. Galvanized, copper, CPVC, PEX and aging supply-line problems. Call (864) 446-8911.",
        "h1": "Pipe Repair & Whole-Home Repiping",
        "badge": "● Leak Repair to Full Repiping",
        "intro": "One isolated leak and a house full of failing supply pipe are two different jobs. We inspect the material, age, access and failure pattern so you can choose between a targeted repair and a longer-term repipe without paying to replace good piping unnecessarily.",
        "schema_id": f"{BASE_URL}/#service-piperepair",
        "service_type": "Pipe Repair and Repiping",
        "schema_desc": "Water supply pipe repair and repiping for leaking, corroded or aging residential and commercial piping across Upstate South Carolina.",
        "price_range": "$149 – $8,999+",
        "price_note": "Current planning ranges: spot pipe leak repair $149–$399 and whole-house repipe $3,499–$8,999. Access, home size, pipe material and finish repair can change the written quote.",
        "og": "/images/og/pipe-repair-1200x630.jpg",
        "body": """
<h3>When a spot repair makes sense</h3>
<p>A single damaged fitting, freeze split, pinhole leak or failed valve can often be repaired without replacing the rest of the system. We isolate the failure, check nearby pipe condition and price the repair before proceeding.</p>
<h3>When repiping deserves consideration</h3>
<ul>
  <li>Repeated leaks in different parts of the home</li>
  <li>Severely restricted flow from corroded galvanized supply piping</li>
  <li>Known problem materials with a history of failures</li>
  <li>Widespread corrosion, brittle pipe or multiple previous patches</li>
  <li>A remodel where old piping is already exposed and accessible</li>
</ul>
<h3>PEX and other replacement options</h3>
<p>Replacement material depends on the building, code requirements, water conditions and access. PEX is common for residential repiping because it can reduce the number of fittings and wall openings, but the right layout still depends on the individual property.</p>
<h3>Protect the parts of the home that are not plumbing</h3>
<p>Repiping is also an access project. We plan routes around crawlspaces, attics, cabinets and finished walls so the plumbing work solves the problem without creating unnecessary demolition.</p>
""",
        "faqs": [
            ("How much does a whole-house repipe cost?", "Our current planning range is $3,499–$8,999 for a whole-house repipe. Home size, number of fixtures, access, existing material and required finish work can change the final written quote."),
            ("Should I repair one leak or repipe the house?", "If the surrounding piping is healthy, a spot repair is usually appropriate. Repeated leaks, severe corrosion, restriction or widespread deterioration are reasons to compare the long-term cost of continued repairs with repiping."),
            ("Can old galvanized pipe cause low water pressure?", "Yes. Galvanized steel can corrode internally and restrict flow over time. A pressure problem should still be diagnosed because valves, regulators, well systems and other conditions can cause similar symptoms."),
            ("How long does repiping take?", "Timing depends on the size of the home, access, number of fixtures and how much finish work is required. We explain the expected schedule before the job begins."),
        ],
    },
    "toilet-repair-installation": {
        "title": "Toilet Repair & Installation Abbeville SC | Plumbing Paramedic 911",
        "description": "Toilet repair and replacement in Abbeville, Greenwood and Upstate SC. Running toilets, leaks, weak flushes, wax rings, flanges and new installs. Call (864) 446-8911.",
        "h1": "Toilet Repair & Installation",
        "badge": "● Running, Leaking or Wobbly Toilets",
        "intro": "A running toilet, weak flush, rocking base or leak at the floor can waste water or damage the bathroom. We identify whether the problem is inside the tank, in the bowl/trap, at the flange or in the drain before recommending repair or replacement.",
        "schema_id": f"{BASE_URL}/#service-toilet",
        "service_type": "Toilet Repair and Installation",
        "schema_desc": "Toilet repair, flange and wax seal repair, clog diagnosis, and toilet replacement for homes and businesses in Upstate South Carolina.",
        "price_range": "$89 – $449",
        "price_note": "Current planning ranges: toilet repair $89–$149 and toilet replacement $249–$449. Flange, drain or floor damage can change the written quote.",
        "og": "/images/og/toilet-1200x630.jpg",
        "body": """
<h3>Common toilet problems we repair</h3>
<ul>
  <li>Toilet keeps running after the tank fills</li>
  <li>Weak or incomplete flush</li>
  <li>Water leaking from the supply connection or tank</li>
  <li>Water or staining around the base</li>
  <li>Toilet rocks or moves on the floor</li>
  <li>Repeated clogs that may point to a fixture or drain problem</li>
</ul>
<h3>Rocking toilets need more than tighter bolts</h3>
<p>A loose toilet can damage the seal at the floor. We remove the fixture when needed, inspect the flange and mounting surface, repair the actual support or seal problem, then reset and test the toilet.</p>
<h3>Repair or replace?</h3>
<p>Tank components and seals are often repairable. A cracked bowl or tank, badly damaged fixture, repeated performance problem or major remodel can make replacement the better value. We explain both options when both are reasonable.</p>
""",
        "faqs": [
            ("How much does toilet repair cost?", "Our current planning range is $89–$149 for common toilet repairs. A standard replacement is typically $249–$449. Flange damage, drain problems or unusual installation conditions can change the written quote."),
            ("Why does my toilet keep running?", "Common causes include a worn flapper or seal, a fill-valve problem, an incorrect water level or a tank component that is not shutting off correctly."),
            ("Why is my toilet rocking?", "A loose mount, uneven support, damaged flange or failed seal can let the toilet move. It should be inspected before water damages the floor."),
            ("Can you install a customer-supplied toilet?", "Yes, provided the fixture is compatible with the existing rough-in and installation. We verify the condition of the flange, shutoff and connection before setting it."),
        ],
    },
    "gas-line-services": {
        "title": "Gas Line Repair & Installation Abbeville SC | Plumbing Paramedic 911",
        "description": "Gas piping inspection, leak repair, appliance connections, line extensions and pressure testing in Abbeville and Upstate SC. Call (864) 446-8911 after the property is safe.",
        "h1": "Gas Line Repair & Installation",
        "badge": "● Gas Piping, Testing & Appliance Connections",
        "intro": "Gas piping work starts with safety. We repair leaks, cap abandoned branches, extend piping, connect approved appliances and perform required testing within applicable licensing, permit and inspection requirements.",
        "schema_id": f"{BASE_URL}/#service-gasline",
        "service_type": "Gas Line Repair and Installation",
        "schema_desc": "Gas piping leak repair, pressure testing, appliance connections, line extensions and capping of unused branches in Upstate South Carolina.",
        "price_range": "Quoted after inspection",
        "price_note": "Gas work varies by pipe size, length, access, appliance demand, testing and permit/inspection requirements. The service / diagnostic call is posted separately on the pricing page.",
        "og": "/images/og/gas-line-1200x630.jpg",
        "body": """
<h3>If you smell gas, leave first</h3>
<p><strong>If you smell gas or suspect an active gas leak, leave the building, avoid switches or flames, and contact 911 or the gas utility from a safe location.</strong> Plumbing repair comes after the immediate hazard has been controlled.</p>
<h3>Gas piping work we handle</h3>
<ul>
  <li>Leak diagnosis and damaged gas-pipe repair</li>
  <li>Pressure testing after utility lockout or repair</li>
  <li>Capping unused appliance or furnace branches</li>
  <li>Approved appliance connections and line extensions</li>
  <li>Gas piping changes associated with water-heater work</li>
</ul>
<h3>Why sizing matters</h3>
<p>Adding an appliance is not just a matter of connecting to the nearest pipe. Available fuel pressure, pipe size, developed length and the demand of existing appliances all matter. We evaluate the system before adding load.</p>
""",
        "faqs": [
            ("What should I do if I smell gas?", "Leave the building, avoid flames and electrical switches, and call 911 or the gas utility from a safe location. Do not remain inside waiting for a plumber."),
            ("Can you pressure-test gas piping after the utility shuts service off?", "Yes, we perform gas piping testing and repairs when required for restoration, subject to the applicable utility, permit and inspection process."),
            ("Can you cap an unused gas line?", "Yes. Abandoned appliance branches should be properly capped and tested rather than left connected to unused equipment."),
            ("Can you run a new gas line for an appliance?", "We can evaluate new appliance piping and line extensions. The existing system must have adequate capacity and the work must meet applicable code, permit and inspection requirements."),
        ],
    },
    "hydro-jetting": {
        "title": "Hydro Jetting Abbeville SC | Plumbing Paramedic 911",
        "description": "Hydro jetting for recurring drain and sewer buildup in Abbeville, Greenwood and Upstate SC. Grease, scale, debris and some root intrusion. Call (864) 446-8911.",
        "h1": "Hydro Jetting Drain & Sewer Lines",
        "badge": "● High-Pressure Line Cleaning",
        "intro": "Snaking opens a path through a blockage; hydro jetting can clean buildup from more of the pipe wall. We use it when the line condition and the type of blockage make high-pressure cleaning the right tool, especially for recurring grease, scale and heavy debris.",
        "schema_id": f"{BASE_URL}/#service-hydrojetting",
        "service_type": "Hydro Jetting",
        "schema_desc": "Hydro jetting and high-pressure drain cleaning for recurring grease, scale, debris and suitable sewer-line conditions in Upstate South Carolina.",
        "price_range": "$399 – $699",
        "price_note": "Current planning range for hydro jetting is $399–$699. Line size, access, blockage type and pipe condition can change the written quote.",
        "og": "/images/og/drain-cleaning-1200x630.jpg",
        "body": """
<h3>When jetting is worth considering</h3>
<ul>
  <li>A line repeatedly clogs after basic cabling</li>
  <li>Grease coats kitchen or commercial drain piping</li>
  <li>Scale and debris restrict an older drain line</li>
  <li>Loose root material remains after opening a sewer line</li>
</ul>
<h3>Pipe condition comes first</h3>
<p>High-pressure cleaning is not the first choice for every pipe. Older, damaged or badly deteriorated lines may need inspection before jetting. The goal is to clean a serviceable pipe, not force a damaged line beyond what it can safely handle.</p>
<h3>Jetting is cleaning, not structural repair</h3>
<p>Hydro jetting can remove material from inside the line, but it does not fix a broken joint, collapsed section, belly or failed pipe wall. When a structural problem causes recurring clogs, we explain the repair separately.</p>
""",
        "faqs": [
            ("How much does hydro jetting cost?", "Our current planning range is $399–$699. The exact price depends on access, line size, blockage type, pipe condition and the amount of cleaning required."),
            ("Is hydro jetting better than a drain snake?", "They solve different problems. Cabling is often appropriate for a straightforward obstruction. Jetting is useful when buildup coats the pipe wall or a line repeatedly clogs from grease, scale or debris."),
            ("Is hydro jetting safe for old pipes?", "Only after the pipe condition is considered. Severely damaged or deteriorated piping may need a different cleaning approach or repair instead."),
            ("Will hydro jetting permanently fix tree roots?", "It can remove root material inside a line, but roots often return when they are entering through damaged joints or cracks. The underlying pipe condition may still need repair."),
        ],
    },
    "sump-pump-services": {
        "title": "Sump Pump Repair & Installation Abbeville SC | Plumbing Paramedic 911",
        "description": "Sump pump repair and installation in Abbeville and Upstate SC. Pumps, float switches, check valves, discharge lines and battery backup options. Call (864) 446-8911.",
        "h1": "Sump Pump Repair & Installation",
        "badge": "● Crawlspace & Basement Water Protection",
        "intro": "A sump pump is only useful if it starts when water rises and can discharge that water away from the structure. We inspect the pump, switch, check valve, basin and discharge path, then repair or replace the failed part.",
        "schema_id": f"{BASE_URL}/#service-sumppump",
        "service_type": "Sump Pump Repair and Installation",
        "schema_desc": "Sump pump repair, replacement, float switch and check valve service, discharge-line repair and battery backup options in Upstate South Carolina.",
        "price_range": "$349 – $699",
        "price_note": "Current planning range for sump pump installation is $349–$699. New pits, drainage work, electrical requirements or backup systems are quoted separately.",
        "og": "/images/og/sump-pump-1200x630.jpg",
        "body": """
<h3>Common sump pump failures</h3>
<ul>
  <li>Pump does not start when the basin fills</li>
  <li>Float switch sticks or hangs up</li>
  <li>Check valve fails and water falls back into the pit</li>
  <li>Discharge line is blocked, damaged or poorly routed</li>
  <li>Pump runs constantly but cannot keep up</li>
  <li>Power loss leaves the property unprotected during a storm</li>
</ul>
<h3>Battery backup can cover the worst timing</h3>
<p>Heavy weather and power outages can happen together. Where the property risk justifies it, we can discuss a properly sized backup option rather than relying on one powered pump.</p>
<h3>Drainage problems may be bigger than the pump</h3>
<p>A pump cannot correct every groundwater or drainage problem. If water is entering faster than the system was designed to handle, the basin, discharge or surrounding drainage may need additional evaluation.</p>
""",
        "faqs": [
            ("How much does sump pump installation cost?", "Our current planning range is $349–$699 for a typical installation. A new basin, drainage changes, electrical work or battery backup can change the written quote."),
            ("How do I know whether my sump pump works?", "The pump should activate when the float rises, move water through the discharge and shut off normally. If you are unsure, testing before storm season is better than discovering a failure during heavy rain."),
            ("Do you install battery backup sump pumps?", "Yes. We can evaluate backup options based on the basin, discharge arrangement, expected inflow and the amount of protection the property needs."),
            ("Why does my sump pump keep cycling?", "A stuck switch, check-valve problem, short discharge path, high inflow or an undersized system can cause frequent cycling. The cause should be identified before simply replacing the pump."),
        ],
    },
    "garbage-disposal-repair": {
        "title": "Garbage Disposal Repair Abbeville SC | Plumbing Paramedic 911",
        "description": "Garbage disposal repair and installation in Abbeville, Greenwood and Upstate SC. Humming, jammed, leaking or dead disposals and replacements. Call (864) 446-8911.",
        "h1": "Garbage Disposal Repair & Installation",
        "badge": "● Jams, Leaks & Replacement",
        "intro": "A disposal that hums, leaks or will not start is often either jammed, electrically tripped or internally failed. We isolate the problem, check the sink and drain connections and recommend repair or replacement based on the condition of the unit.",
        "schema_id": f"{BASE_URL}/#service-disposal",
        "service_type": "Garbage Disposal Repair and Installation",
        "schema_desc": "Garbage disposal jam diagnosis, leak repair, replacement and new installation for residential kitchens in Upstate South Carolina.",
        "price_range": "$149 – $299",
        "price_note": "Current planning range for disposal installation is $149–$299. Sink-flange, drain, electrical or cabinet conditions can change the written quote.",
        "og": "/images/og/fixtures-1200x630.jpg",
        "body": """
<h3>What the symptom usually means</h3>
<ul>
  <li><strong>Hums but will not turn:</strong> often a jammed grinding mechanism</li>
  <li><strong>Completely dead:</strong> reset, power or internal motor problem</li>
  <li><strong>Leaks at the sink:</strong> mounting/flange seal or connection issue</li>
  <li><strong>Leaks from the unit body:</strong> often an internal failure that favors replacement</li>
  <li><strong>Backs water into the sink:</strong> may be a disposal or downstream drain problem</li>
</ul>
<h3>Safe checks before calling</h3>
<p>Turn the wall switch off before touching the unit. You can check whether the reset button has tripped and whether the breaker is on. Never put a hand into the grinding chamber. If the unit repeatedly trips or the electrical condition is uncertain, leave it off for service.</p>
<h3>Repair vs. replacement</h3>
<p>A simple jam or connection leak can be repairable. A cracked body, leaking internal seal or failed motor often makes replacement more sensible. We also check the dishwasher and drain connections so the new or repaired unit drains correctly.</p>
""",
        "faqs": [
            ("How much does garbage disposal installation cost?", "Our current planning range is $149–$299. Electrical, drain, sink-flange or cabinet changes can affect the written quote."),
            ("Why does my disposal hum but not grind?", "The motor may be energized while the grinding mechanism is jammed. Turn the switch off and do not put your hand in the unit. A jam can often be cleared without replacing the disposal."),
            ("Why is my disposal leaking from the bottom?", "A leak from the body of the unit can indicate an internal seal or housing failure. Depending on the unit, replacement may be more practical than repair."),
            ("Can a disposal problem actually be a clogged drain?", "Yes. If water backs up after leaving the disposal, the blockage may be in the trap or branch drain rather than in the disposal itself."),
        ],
    },
}

LOCAL_PAGE_ADDITIONS = {
    "drain-cleaning-abbeville-sc": {
        "title": "Drain Cleaning Abbeville SC | Plumbing Paramedic 911",
        "description": "Drain cleaning in Abbeville SC for kitchen, bathroom and main-line clogs. Local diagnosis for older and newer homes with upfront pricing. Call (864) 446-8911.",
        "h1": "Drain Cleaning in Abbeville, SC",
        "badge": "● Local Abbeville Drain Service",
        "city": "Abbeville", "area_type": "City", "service_type": "Drain Cleaning",
        "parent_service": "/services/drain-cleaning/", "parent_service_name": "Drain Cleaning",
        "city_page": "/service-areas/abbeville-sc/", "city_page_name": "Abbeville, SC",
        "guide": "/guides/drain-maintenance-playbook/", "guide_name": "Drain Maintenance Playbook",
        "og": "/images/og/drain-cleaning-1200x630.jpg",
        "intro": "Abbeville homes range from older downtown properties to newer subdivisions and rural addresses. That means a recurring backup can come from very different pipe materials and drainage systems. We identify whether the clog is at one fixture, a branch line or the main sewer before choosing the clearing method.",
        "answer": "If several Abbeville drains back up together, stop running water until the main line is checked. A single slow sink or tub is more likely a local branch problem. Repeated whole-house backups deserve a sewer-condition check instead of another blind clearing.",
        "local_context": "<p>Older drain materials can develop scale, rough interior surfaces or root-entry points that make repeat clogs more likely. Newer PVC systems can still clog from grease, wipes, foreign objects or poor flow. Rural properties can also have septic-side conditions that mimic a building-sewer blockage.</p><p>We match the tool to the problem: cabling for a straightforward obstruction, camera inspection for recurring or structural concerns, and hydro jetting when suitable pipe condition and heavy buildup call for wall-to-wall cleaning.</p>",
        "symptoms": ["Multiple drains slow at once", "Toilet flush makes water rise in a tub", "Kitchen clog returns repeatedly", "Gurgling or sewer odor", "Main cleanout or lowest drain overflows", "Previous clearing did not last"],
        "checks": ["Separate fixture, branch and main-line symptoms", "Check available cleanouts and drainage direction", "Use the least destructive clearing method that fits the blockage", "Recommend camera inspection when recurrence suggests pipe damage", "Evaluate septic-side conditions when relevant", "Explain repair separately if the pipe itself is damaged"],
        "price_drivers": ["Fixture vs branch vs main line", "Cleanout access and blockage distance", "Recurring problem requiring camera inspection", "Grease, scale or roots requiring additional cleaning", "Structural pipe defects beyond simple clog removal"],
        "faqs": [
            ("How much is drain cleaning in Abbeville, SC?", "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. Drain cleaning is then quoted based on the location, access and clearing method."),
            ("How do I know if the main line is clogged?", "Multiple fixtures backing up together or water rising in a tub when a toilet flushes are common main-line warning signs."),
            ("Do you use a sewer camera?", "Yes when recurring clogs or suspected pipe damage make inspection useful. A camera is not required for every simple fixture clog."),
            ("Can you hydro-jet an Abbeville sewer line?", "Yes when the pipe condition and buildup make hydro jetting appropriate. Damaged or badly deteriorated piping may need a different approach."),
        ],
        "related": [("🚿", "Full Drain Cleaning Service", "/services/drain-cleaning/", "Drain, sewer and hydro-jetting options."), ("📍", "Abbeville Plumbing", "/service-areas/abbeville-sc/", "All local Plumbing Paramedic 911 services."), ("📘", "Drain Maintenance Playbook", "/guides/drain-maintenance-playbook/", "Homeowner drain-care guidance."), ("💰", "Upfront Pricing", "/pricing/", "Current service-call schedule and planning ranges.")],
    },
    "sewer-line-repair-abbeville-sc": {
        "title": "Sewer Line Repair Abbeville SC | Plumbing Paramedic 911",
        "description": "Sewer line repair in Abbeville SC for recurring backups, roots, damaged pipe and failed building sewers. Camera-first diagnosis and upfront pricing. Call (864) 446-8911.",
        "h1": "Sewer Line Repair in Abbeville, SC", "badge": "● Recurring Backups & Damaged Sewer Lines",
        "city": "Abbeville", "area_type": "City", "service_type": "Sewer Line Repair",
        "parent_service": "/services/sewer-line-repair/", "parent_service_name": "Sewer Line Repair",
        "city_page": "/service-areas/abbeville-sc/", "city_page_name": "Abbeville, SC",
        "guide": "/guides/sc-homeowner-plumbing-survival-guide/", "guide_name": "SC Homeowner Plumbing Survival Guide",
        "og": "/images/og/sewer-line-1200x630.jpg",
        "intro": "Abbeville's mix of older homes, mature trees and multiple generations of drain material makes recurring sewer problems worth diagnosing carefully. We locate the failure before recommending excavation or replacement.",
        "answer": "A sewer line that repeatedly clogs after clearing may have roots, an offset joint, a belly, deterioration or another structural problem. The next step is to identify where the failure is and whether a localized repair can solve it before considering a larger replacement.",
        "local_context": "<p>Historic and older properties may have drain materials and joints that behave differently from newer PVC. Mature landscaping can also put root pressure near older joints. None of that automatically means a full replacement—the actual line condition has to be seen and diagnosed.</p><p>We separate a blockage from a broken pipe because the right repair, cost and disruption are very different.</p>",
        "symptoms": ["Whole-house backup returns after clearing", "Several fixtures gurgle or drain slowly", "Sewer odor persists", "Wet or settled ground over the sewer route", "Camera shows roots, offsets or damaged pipe", "Cleanout overflows during normal use"],
        "checks": ["Confirm the issue is in the building sewer", "Open the line safely if blocked", "Use camera inspection when structural failure is suspected", "Locate the damaged section before excavation", "Compare spot repair with larger replacement when appropriate", "Confirm flow after repair"],
        "price_drivers": ["Depth and location of the sewer", "Length and material of damaged pipe", "Access for excavation", "Spot repair vs larger replacement", "Roots, offsets, bellies or multiple failures"],
        "faqs": [("How much does sewer line repair cost in Abbeville?", "Our current planning range is $899–$2,499 for repair and $2,499–$5,999 for replacement, with the service / diagnostic call separate. Final price depends on access, depth, length and pipe condition."), ("Does a recurring clog mean the sewer is broken?", "Not always, but repeated main-line clogs are a good reason to inspect for roots, offsets, bellies or deterioration instead of treating every recurrence as an isolated blockage."), ("Can one section of sewer be repaired?", "Yes when the damage is localized and the surrounding pipe is serviceable. The inspection determines whether a spot repair is reasonable."), ("Do you repair sewer lines on older Abbeville homes?", "Yes. Older properties often need a careful diagnosis because pipe material, previous repairs and mature roots can all affect the best repair method.")],
        "related": [("🛠️", "Full Sewer Line Service", "/services/sewer-line-repair/", "Diagnosis, repair and replacement planning."), ("🚿", "Drain Cleaning", "/services/drain-cleaning/", "Clear blockages and determine whether the pipe is damaged."), ("📍", "Abbeville Plumbing", "/service-areas/abbeville-sc/", "Local plumbing coverage from our home market."), ("💰", "Upfront Pricing", "/pricing/", "Current service-call and planning ranges.")],
    },
    "emergency-plumber-greenwood-sc": {
        "title": "Emergency Plumber Greenwood SC | Plumbing Paramedic 911",
        "description": "24/7 emergency plumber serving Greenwood SC for burst pipes, sewer backups, leaking water heaters, no-water calls and active leaks. Call (864) 446-8911.",
        "h1": "Emergency Plumber in Greenwood, SC", "badge": "● 24/7 Greenwood Emergency Dispatch",
        "city": "Greenwood", "area_type": "City", "service_type": "Emergency Plumbing",
        "parent_service": "/services/24-7-emergency-plumbing/", "parent_service_name": "24/7 Emergency Plumbing",
        "city_page": "/service-areas/greenwood-sc/", "city_page_name": "Greenwood, SC",
        "guide": "/guides/sc-homeowner-plumbing-survival-guide/", "guide_name": "SC Homeowner Plumbing Survival Guide",
        "og": "/images/og/emergency-plumbing-1200x630.jpg",
        "intro": "When water is actively damaging a Greenwood home or sewage is backing up, the first goal is to stop the damage and make the property safe. Plumbing Paramedic 911 dispatches emergency calls 24/7 across Greenwood and the surrounding area.",
        "answer": "For an active water leak, shut off the nearest fixture valve or the main supply if you can reach it safely. For a sewer backup, stop using plumbing fixtures. If you smell gas, leave the building and call the gas utility or 911 from a safe location before arranging plumbing repair.",
        "local_context": "<p>Greenwood emergency calls range from older-home supply leaks and sewer backups to water-heater failures, slab leaks and rural no-water problems. The response plan depends on whether the immediate risk is clean water, sewage, gas or loss of the home's water supply.</p><p>Call for the current ETA. Active calls, weather, distance and job conditions can affect arrival time.</p>",
        "symptoms": ["Burst or actively leaking pipe", "Water heater leaking into occupied or finished space", "Sewage backing into fixtures", "Main shutoff will not stop an active leak", "Whole house suddenly loses water", "Water coming through a ceiling, wall or floor"],
        "checks": ["Control active water or sewage exposure first", "Identify the failed system", "Isolate the damaged section when possible", "Check for secondary leaks after pressure is restored", "Explain temporary stabilization vs permanent repair", "Quote additional repair work before proceeding"],
        "price_drivers": ["Dispatch time window", "Whether immediate stabilization is possible", "Access in walls, ceilings, slabs or crawlspaces", "Materials and code-required repair work", "Follow-up replacement or restoration needs"],
        "faqs": [("Do you have an emergency plumber in Greenwood at night?", "Plumbing Paramedic 911 dispatches 24/7. Call (864) 446-8911 for current availability and ETA."), ("How much is the emergency service call?", "The service / diagnostic call is $99 after hours and weekends and $158 after midnight or on holidays. Weekday 9 AM–5 PM service calls are $79. Repair work is quoted separately."), ("What should I do during a burst pipe?", "If you can safely reach the main shutoff, turn it off and keep away from wet electrical equipment. Then call for emergency service."), ("Is a sewer backup an emergency?", "Yes when sewage is entering the building or several fixtures are backing up. Stop using water until the blockage is controlled.")],
        "related": [("🚨", "24/7 Emergency Plumbing", "/services/24-7-emergency-plumbing/", "Emergency response across the full service area."), ("📍", "Greenwood Plumbing", "/service-areas/greenwood-sc/", "All Plumbing Paramedic 911 services in Greenwood."), ("📙", "Homeowner Survival Guide", "/guides/sc-homeowner-plumbing-survival-guide/", "Know shutoffs and first steps before an emergency."), ("💰", "Upfront Pricing", "/pricing/", "Current dispatch schedule and planning ranges.")],
    },
}

GUIDES = {
    "sc-homeowner-plumbing-survival-guide": {"title": "SC Homeowner Plumbing Survival Guide | Plumbing Paramedic 911", "description": "42-page digital plumbing guide for South Carolina homeowners: shutoffs, pipe materials, seasonal prep, contractor questions and emergency documentation. $19.", "name": "SC Homeowner's Plumbing Survival Guide", "price": "19.00", "price_display": "$19", "pages": "42 pages", "gumroad": "https://plumbingparamedic911.gumroad.com/l/survival-guide", "eyebrow": "Home plumbing reference", "intro": "A practical guide for understanding the plumbing systems in a South Carolina home before an emergency happens. It covers shutoffs, common pipe materials, seasonal preparation, contractor questions, DIY limits and documentation basics.", "bullets": ["Find and label the main and fixture shutoffs", "Recognize common supply-pipe materials and warning signs", "Prepare exposed plumbing for cold weather", "Know which jobs are reasonable DIY work and which are not", "Compare written plumbing proposals more confidently", "Document a water-damage event before repairs begin"]},
    "well-pump-owners-manual-upstate-sc": {"title": "Well Pump Owner's Manual Upstate SC | Plumbing Paramedic 911", "description": "28-page digital guide for Upstate SC well-water homeowners: pumps, pressure tanks, switches, failure signs, water quality and repair questions. $17.", "name": "Well Pump & Water System Owner's Manual", "price": "17.00", "price_display": "$17", "pages": "28 pages", "gumroad": "https://plumbingparamedic911.gumroad.com/l/well-pump-manual", "eyebrow": "Private well reference", "intro": "A plain-language guide to how the pump, pressure tank, pressure switch and household plumbing work together. It helps well-water homeowners recognize failure signs and ask better questions before authorizing repairs.", "bullets": ["Understand the pump, tank and pressure-switch cycle", "Recognize rapid cycling and low-pressure symptoms", "Separate a tank problem from a down-hole pump problem", "Know what information helps before a no-water service call", "Plan routine water-quality checks", "Compare repair and replacement recommendations"]},
    "water-heater-buyers-guide-sc": {"title": "Water Heater Buyers Guide for SC Homes | Plumbing Paramedic 911", "description": "22-page digital water-heater guide for SC homeowners: tank vs tankless, sizing, fuel types, installation requirements and quote comparison. $14.", "name": "Water Heater Buyers Guide: Tank vs. Tankless for SC Homes", "price": "14.00", "price_display": "$14", "pages": "22 pages", "gumroad": "https://plumbingparamedic911.gumroad.com/l/water-heater-guide", "eyebrow": "Replacement planning guide", "intro": "A homeowner-friendly comparison of tank, tankless and other common water-heating options, with attention to sizing, fuel type, venting, electrical needs and the installation items that can change a quote.", "bullets": ["Compare tank and tankless tradeoffs", "Estimate the capacity a household actually needs", "Understand gas, electric and heat-pump requirements", "Spot installation items that are easy to leave out of a quote", "Compare equipment and labor proposals on the same basis", "Prepare the questions to ask before replacement day"]},
    "drain-maintenance-playbook": {"title": "Drain Maintenance Playbook | Plumbing Paramedic 911", "description": "16-page digital drain-maintenance guide: safe routine care, clog warning signs, what to keep out of drains and when to call a plumber. $9.", "name": "The Smart Homeowner's Drain Maintenance Playbook", "price": "9.00", "price_display": "$9", "pages": "16 pages", "gumroad": "https://plumbingparamedic911.gumroad.com/l/drain-playbook", "eyebrow": "Preventive drain care", "intro": "A short maintenance guide for reducing preventable clogs and recognizing when a slow drain is really a warning sign of a larger branch or sewer problem.", "bullets": ["Build a simple monthly and seasonal drain-care routine", "Know what should never go down kitchen or bathroom drains", "Use safer basic maintenance instead of harsh chemical overuse", "Recognize the difference between one slow fixture and a main-line problem", "Know when recurring clogs justify camera inspection", "Keep a printable maintenance checklist"]},
}

BUNDLE_URL = "https://plumbingparamedic911.gumroad.com/l/complete-bundle"
BUNDLE_PRICE = "$48"
PRESERVED_LEGACY_PATHS = ["/services/sewer-line-repair/", "/services/pipe-repair-repiping/", "/services/toilet-repair-installation/", "/services/gas-line-services/", "/services/hydro-jetting/", "/services/sump-pump-services/", "/services/garbage-disposal-repair/", "/guides/", "/guides/sc-homeowner-plumbing-survival-guide/", "/guides/well-pump-owners-manual-upstate-sc/", "/guides/water-heater-buyers-guide-sc/", "/guides/drain-maintenance-playbook/", "/drain-cleaning-abbeville-sc/", "/sewer-line-repair-abbeville-sc/", "/emergency-plumber-greenwood-sc/"]
INTENTIONAL_REDIRECT_RULES = {"/blog/": "RewriteRule ^blog/?$ /faq/", "/blog/signs-water-heater-failing/": "RewriteRule ^blog/signs-water-heater-failing/?$ /services/water-heater-repair-replacement/", "/blog/how-to-shut-off-water-in-emergency/": "RewriteRule ^blog/how-to-shut-off-water-in-emergency/?$ /services/24-7-emergency-plumbing/", "/costs/": "RewriteRule ^costs(?:/.*)?$ /pricing/", "/service-areas/iva-sc/": "RewriteRule ^service-areas/iva-sc/?$ /service-areas/iva-lake-secession-sc/", "/service-areas/starr-sc/": "RewriteRule ^service-areas/starr-sc/?$ /service-areas/anderson-sc/", "/backflow-testing-abbeville-sc/": "RewriteRule ^backflow-testing-abbeville-sc/?$ /services/backflow-prevention-testing/", "/commercial-plumber-greenwood-sc/": "RewriteRule ^commercial-plumber-greenwood-sc/?$ /services/commercial-plumbing/"}
BANNED_PUBLIC_PHRASES = ("$150 after-hours surcharge", "flat $150 after-hours surcharge", "service call fee is waived", "gives free up-front estimates before any work begins", "Monday through Friday, 8 AM to 6 PM")


def _patch_navigation(build) -> None:
    if 'href="/guides/"' not in build.NAV_HTML:
        build.NAV_HTML = build.NAV_HTML.replace('<li><a href="/contact/"{CONTACT_ACTIVE}>Contact</a></li>', '<li><a href="/contact/"{CONTACT_ACTIVE}>Contact</a></li><li><a href="/guides/">Guides</a></li>')
        build.NAV_HTML = build.NAV_HTML.replace('  <a href="/about/">👤 About</a>\n', '  <a href="/about/">👤 About</a>\n  <a href="/guides/">📚 Homeowner Guides</a>\n')
    if 'href="/guides/">Homeowner Guides</a>' not in build.FOOTER_HTML:
        build.FOOTER_HTML = build.FOOTER_HTML.replace('<li><a href="/faq/">FAQ</a></li><li><a href="/contact/">Contact</a></li>', '<li><a href="/faq/">FAQ</a></li><li><a href="/guides/">Homeowner Guides</a></li><li><a href="/contact/">Contact</a></li>')


def apply(build, money) -> None:
    build.SERVICES.update(SERVICE_ADDITIONS)
    money.MONEY_PAGES.update(LOCAL_PAGE_ADDITIONS)
    money.LINK_TARGETS.setdefault("services/drain-cleaning/index.html", []).append("drain-cleaning-abbeville-sc")
    money.LINK_TARGETS.setdefault("services/sewer-line-repair/index.html", []).append("sewer-line-repair-abbeville-sc")
    money.LINK_TARGETS.setdefault("services/24-7-emergency-plumbing/index.html", []).append("emergency-plumber-greenwood-sc")
    money.LINK_TARGETS.setdefault("service-areas/abbeville-sc/index.html", []).extend(["drain-cleaning-abbeville-sc", "sewer-line-repair-abbeville-sc"])
    money.LINK_TARGETS.setdefault("service-areas/greenwood-sc/index.html", []).append("emergency-plumber-greenwood-sc")
    _patch_navigation(build)


def _guide_product_schema(slug: str, guide: dict) -> dict:
    return {"@type": "Product", "@id": f"{BASE_URL}/guides/{slug}/#product", "name": guide["name"], "description": guide["description"], "url": f"{BASE_URL}/guides/{slug}/", "brand": {"@type": "Brand", "name": "Plumbing Paramedic 911"}, "author": {"@type": "Person", "name": "Eric Callaway", "url": f"{BASE_URL}/about/"}, "offers": {"@type": "Offer", "price": guide["price"], "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": guide["gumroad"]}}


def render_guide(build, slug: str, guide: dict) -> str:
    path = f"/guides/{slug}/"
    crumbs = [("Home", "/"), ("Guides", "/guides/"), (guide["name"], path)]
    extra = [{"@type": "WebPage", "@id": f"{BASE_URL}{path}#webpage", "url": f"{BASE_URL}{path}", "name": guide["title"], "about": {"@id": f"{BASE_URL}{path}#product"}, "isPartOf": {"@id": f"{BASE_URL}/#website"}, "inLanguage": "en-US"}, _guide_product_schema(slug, guide), build.breadcrumb_ld(crumbs)]
    h = build.head(guide["title"], guide["description"], path, extra_jsonld=extra, og_type="product", body_page=f"guide-{slug}")
    bullets = "".join(f"<li>{html.escape(item)}</li>" for item in guide["bullets"])
    body = f'''<main><section class="page-header"><div class="container"><nav class="breadcrumb" aria-label="Breadcrumb">{build.breadcrumb_html(crumbs)}</nav><span class="badge" style="display:inline-flex;margin-bottom:14px">📘 {guide['eyebrow']}</span><h1 class="speakable-headline">{html.escape(guide['name'])}</h1><p class="speakable-summary">{html.escape(guide['intro'])}</p></div></section><section class="section"><div class="container" style="max-width:980px"><div class="grid-2" style="gap:36px;align-items:start"><article class="card"><span class="label">What's inside</span><h2 style="margin:8px 0 16px">Practical homeowner reference</h2><ul class="check-list">{bullets}</ul><p style="margin-top:18px;color:var(--ink3)">Digital PDF · {guide['pages']}. This guide is educational and does not replace an on-site diagnosis when a plumbing system is unsafe, leaking or failing.</p></article><aside class="card" style="border-color:var(--green);background:var(--green-xlt)"><span class="label">Digital download</span><div style="font-family:var(--ff-head);font-size:3rem;font-weight:900;color:var(--green-dk);margin:8px 0">{guide['price_display']}</div><p style="margin-bottom:18px">{guide['pages']} · secure checkout and delivery handled by Gumroad.</p><a class="btn btn-green btn-lg" href="{guide['gumroad']}">Buy on Gumroad →</a><div style="margin-top:18px"><a href="/guides/">← See all homeowner guides</a></div></aside></div></div></section><section class="section bg-alt"><div class="container" style="max-width:900px;text-align:center"><span class="label">Need hands-on help?</span><h2>A guide helps you plan. A plumbing emergency still needs a plumber.</h2><p class="lead">For active leaks, sewer backups, no-water calls or unsafe conditions, call Plumbing Paramedic 911 for current dispatch availability.</p><a href="tel:+18644468911" class="btn btn-blue btn-lg speakable-phone">📞 (864) 446-8911</a></div></section></main>'''
    return h + build.nav() + body + build.FOOTER_HTML + "</body>\n</html>\n"


def render_guides_hub(build) -> str:
    path = "/guides/"
    crumbs = [("Home", "/"), ("Guides", path)]
    item_list, cards = [], []
    for position, (slug, guide) in enumerate(GUIDES.items(), start=1):
        item_list.append({"@type": "ListItem", "position": position, "url": f"{BASE_URL}/guides/{slug}/"})
        cards.append(f'''<a class="card" href="/guides/{slug}/" style="display:block;text-decoration:none"><span class="label">{guide['pages']}</span><h3 style="margin:8px 0">{html.escape(guide['name'])}</h3><p>{html.escape(guide['intro'])}</p><div style="font-family:var(--ff-head);font-weight:900;font-size:1.45rem;color:var(--green-dk);margin-top:14px">{guide['price_display']}</div><span class="arrow">View guide →</span></a>''')
    extra = [{"@type": "WebPage", "@id": f"{BASE_URL}/guides/#webpage", "url": f"{BASE_URL}/guides/", "name": "Plumbing Guides for South Carolina Homeowners", "isPartOf": {"@id": f"{BASE_URL}/#website"}, "inLanguage": "en-US"}, {"@type": "ItemList", "name": "Plumbing Paramedic 911 Homeowner Guides", "itemListElement": item_list}, build.breadcrumb_ld(crumbs)]
    h = build.head("Plumbing Guides for SC Homeowners | Plumbing Paramedic 911", "Digital plumbing guides for South Carolina homeowners covering emergency prep, well pumps, water heaters and drain maintenance.", path, extra_jsonld=extra, body_page="guides")
    body = f'''<main><section class="page-header"><div class="container"><nav class="breadcrumb" aria-label="Breadcrumb">{build.breadcrumb_html(crumbs)}</nav><span class="badge" style="display:inline-flex;margin-bottom:14px">📚 Homeowner Education</span><h1 class="speakable-headline">Plumbing Guides for South Carolina Homeowners</h1><p class="speakable-summary">Practical digital references built from years of service-plumbing experience: emergency preparation, well systems, water-heater decisions and drain maintenance.</p></div></section><section class="section"><div class="container"><div class="grid-2">{''.join(cards)}</div></div></section><section class="section bg-alt"><div class="container" style="max-width:760px;text-align:center"><span class="label">Complete bundle</span><h2>All four digital guides — {BUNDLE_PRICE}</h2><p class="lead">The bundle keeps the same four guide URLs intact while providing one checkout for the complete set.</p><a class="btn btn-green btn-lg" href="{BUNDLE_URL}">Get the Complete Bundle →</a><p style="margin-top:14px;color:var(--ink3)">Checkout and digital delivery are handled by Gumroad.</p></div></section></main>'''
    return h + build.nav() + body + build.FOOTER_HTML + "</body>\n</html>\n"


def generate_guides(build) -> None:
    hub = ROOT / "guides" / "index.html"
    hub.parent.mkdir(parents=True, exist_ok=True)
    hub.write_text(render_guides_hub(build), encoding="utf-8")
    for slug, guide in GUIDES.items():
        target = ROOT / "guides" / slug / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_guide(build, slug, guide), encoding="utf-8")


def ensure_metadata() -> None:
    sitemap = ROOT / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    for path in PRESERVED_LEGACY_PATHS:
        url = BASE_URL + path
        if url not in text:
            text = text.replace("</urlset>", f"  <url><loc>{url}</loc><lastmod>{LASTMOD}</lastmod></url>\n</urlset>")
    sitemap.write_text(text, encoding="utf-8")
    llms = ROOT / "llms.txt"
    content = llms.read_text(encoding="utf-8")
    marker = "## Preserved Super Site Assets"
    if marker not in content:
        lines = ["", marker]
        for slug, guide in GUIDES.items(): lines.append(f"- [{guide['name']}]({BASE_URL}/guides/{slug}/): {guide['description']}")
        for slug, s in SERVICE_ADDITIONS.items(): lines.append(f"- [{html.unescape(s['h1'])}]({BASE_URL}/services/{slug}/): {s['description']}")
        for slug, p in LOCAL_PAGE_ADDITIONS.items(): lines.append(f"- [{html.unescape(p['h1'])}]({BASE_URL}/{slug}/): {p['description']}")
        llms.write_text(content.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def _path_to_file(path: str) -> Path:
    return ROOT / "index.html" if path == "/" else ROOT / path.lstrip("/") / "index.html"


def validate_migration() -> None:
    errors = []
    for path in PRESERVED_LEGACY_PATHS:
        if not _path_to_file(path).exists(): errors.append(f"preserved legacy route has no source-controlled file: {path}")
    htaccess = (ROOT / ".htaccess").read_text(encoding="utf-8")
    for path, rule in INTENTIONAL_REDIRECT_RULES.items():
        if rule not in htaccess: errors.append(f"intentional redirect missing for {path}")
    for file in [p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "docs" not in p.parts]:
        text = file.read_text(encoding="utf-8")
        for phrase in BANNED_PUBLIC_PHRASES:
            if phrase.lower() in text.lower(): errors.append(f"{file.relative_to(ROOT)} contains retired pricing phrase: {phrase}")
    for slug in GUIDES:
        if not (ROOT / "guides" / slug / "index.html").exists(): errors.append(f"missing guide product page: {slug}")
    if errors: raise RuntimeError("SUPER SITE MIGRATION VALIDATION FAILED\n - " + "\n - ".join(errors))
    print(f"Super-site migration validated: {len(PRESERVED_LEGACY_PATHS)} preserved legacy routes, {len(INTENTIONAL_REDIRECT_RULES)} intentional consolidations.")
