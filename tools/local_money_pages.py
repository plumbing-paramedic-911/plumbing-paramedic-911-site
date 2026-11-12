#!/usr/bin/env python3
"""Generate high-intent local service pages for Plumbing Paramedic 911.

These pages are deliberately narrow, answer-first landing pages that connect a
real service to a real market. They are not programmatic doorway pages: each
page has unique local context, troubleshooting guidance, pricing factors, FAQs,
and internal links into the service/city/guide graph.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://plumbingparamedic911.com"
LASTMOD = "2026-08-13"

SERVICE_CALL_HTML = """\
<div class="grid-3" style="margin-top:18px">
  <div class="card"><span class="label">Weekday</span><h3 style="margin:6px 0">$79 service / diagnostic call</h3><p>Monday–Friday, 9 AM–5 PM.</p></div>
  <div class="card"><span class="label">After Hours</span><h3 style="margin:6px 0">$99 service / diagnostic call</h3><p>Evenings and weekends.</p></div>
  <div class="card"><span class="label">Late Night / Holiday</span><h3 style="margin:6px 0">$158 service / diagnostic call</h3><p>After midnight and holidays.</p></div>
</div>
<p style="font-size:.88rem;color:var(--ink3);margin-top:14px">Repair and replacement work is priced separately after diagnosis. If access, code-required upgrades, equipment, materials, or hidden conditions change the job, we explain the difference and get approval before proceeding.</p>
"""

MONEY_PAGES = {
    "well-pump-repair-mccormick-sc": {
        "title": "Well Pump Repair McCormick SC | Plumbing Paramedic 911",
        "description": "No water, low pressure or a cycling well pump in McCormick SC? We diagnose pumps, pressure tanks, switches, wiring and well-system problems with upfront pricing. Call (864) 446-8911.",
        "h1": "Well Pump Repair in McCormick, SC",
        "badge": "● No-Water & Low-Pressure Service",
        "city": "McCormick",
        "area_type": "City",
        "service_type": "Well Pump Repair",
        "parent_service": "/services/well-pump-repair/",
        "parent_service_name": "Well Pump Repair",
        "city_page": "/service-areas/mccormick-sc/",
        "city_page_name": "McCormick, SC",
        "guide": "/guides/well-pump-owners-manual-upstate-sc/",
        "guide_name": "Well Pump Owner's Manual",
        "og": "/images/og/well-pump-1200x630.jpg",
        "intro": "If a McCormick home suddenly has no water, the failed part is not automatically the pump. The problem can be the pressure switch, pressure tank, wiring, controls, drop pipe, low well yield, or the submersible pump itself. We diagnose the system as a whole before recommending what to replace.",
        "answer": "For a McCormick well system with no water or weak pressure, the first job is to separate an above-ground control problem from a down-hole pump problem. We check power, pressure-switch operation, tank condition, system pressure and pump behavior before deciding whether the pump needs to be pulled.",
        "local_context": """
<p>McCormick County has a large number of rural, lake-area and second-home properties where the well system is the home's entire water supply. That makes rapid cycling, a waterlogged tank, a burned pressure switch or a weak submersible pump more than an inconvenience — the whole house can be without water.</p>
<p>We also see longer service-line runs, outdoor well equipment, pressure tanks in utility buildings, and systems that have been modified over the years. Those details matter because the correct repair depends on how the pump, tank, switch, controls and plumbing work together.</p>
""",
        "symptoms": [
            "No water anywhere in the house",
            "Pressure drops badly when more than one fixture runs",
            "Pump starts and stops every few seconds (rapid cycling)",
            "Pump runs constantly but pressure never reaches cut-off",
            "Breaker trips or pressure switch chatters",
            "Air sputters from faucets or water becomes intermittent",
        ],
        "checks": [
            "Verify power and control operation without repeatedly resetting a tripping breaker",
            "Check pressure-switch contacts, cut-in/cut-out behavior and gauge reading",
            "Test pressure-tank air charge and look for a ruptured bladder / waterlogged tank",
            "Evaluate pump current, pressure recovery and whether the pump can build shut-off pressure",
            "Inspect accessible piping for leaks that can mimic a weak pump",
            "If the evidence points down-hole, plan the safest pull based on well depth, drop pipe and wire condition",
        ],
        "price_drivers": [
            "Whether the failure is above ground (switch/tank/controls) or down-hole",
            "Well depth and the amount/type of drop pipe that must be pulled",
            "Pump horsepower, voltage and replacement equipment required",
            "Condition of wire, check valves, fittings and existing pressure tank",
            "Access around the well head and whether previous repairs created nonstandard conditions",
        ],
        "faqs": [
            ("How much does well pump repair cost in McCormick, SC?", "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. The repair price depends on what failed, well depth, pump size, drop pipe, wire, tank condition and access. We give the repair price before proceeding."),
            ("Does no water always mean the well pump is bad?", "No. A failed pressure switch, waterlogged pressure tank, broken wire, tripped control, leak, low well level or damaged drop pipe can also cause no-water symptoms. We test the system before recommending a pump replacement."),
            ("Can you replace the pressure tank without replacing the pump?", "Yes. If the pump is healthy and the pressure tank has a ruptured bladder or is waterlogged, the tank can be replaced as a separate repair. Rapid cycling is one of the most common signs of a tank problem."),
            ("Do you service lake and rural properties around McCormick?", "Yes. McCormick County, Savannah Lakes Village and nearby rural/lake properties are priority well-pump markets for Plumbing Paramedic 911."),
            ("Can you come out if the well quits at night?", "Yes. Plumbing Paramedic 911 dispatches 24/7. After-hours, late-night and holiday service-call pricing is posted upfront on this page and on our pricing page."),
        ],
        "related": [
            ("💧", "Full Well Pump Service", "/services/well-pump-repair/", "Pressure tanks, switches, pumps, water treatment and troubleshooting."),
            ("📍", "McCormick Plumbing", "/service-areas/mccormick-sc/", "All plumbing services available in McCormick."),
            ("📘", "Well Pump Owner's Manual", "/guides/well-pump-owners-manual-upstate-sc/", "A deeper homeowner guide to well-system operation and failure signs."),
            ("💰", "Upfront Pricing", "/pricing/", "See the current dispatch schedule and planning ranges."),
        ],
    },
    "well-pump-repair-iva-lake-secession-sc": {
        "title": "Well Pump Repair Iva & Lake Secession SC | PP911",
        "description": "Well pump repair for Iva and Lake Secession SC: no water, pressure tanks, switches, low pressure, cycling pumps and rural well-system troubleshooting. Call (864) 446-8911.",
        "h1": "Well Pump Repair in Iva & Lake Secession, SC",
        "badge": "● Rural & Lake-Home Well Systems",
        "city": "Iva and Lake Secession",
        "area_type": "Place",
        "service_type": "Well Pump Repair",
        "parent_service": "/services/well-pump-repair/",
        "parent_service_name": "Well Pump Repair",
        "city_page": "/service-areas/iva-lake-secession-sc/",
        "city_page_name": "Iva & Lake Secession, SC",
        "guide": "/guides/well-pump-owners-manual-upstate-sc/",
        "guide_name": "Well Pump Owner's Manual",
        "og": "/images/og/well-pump-1200x630.jpg",
        "intro": "Lake Secession and the rural Iva area have many homes where a private well supplies every faucet, toilet, appliance and outdoor connection. When pressure disappears, we troubleshoot the entire well system — pump, switch, tank, wiring and piping — instead of assuming the most expensive component failed.",
        "answer": "If your Iva or Lake Secession property has no water, stop repeatedly cycling a tripping breaker and check whether the problem affects the whole house. A well-system diagnosis should confirm power, pressure-switch operation, tank condition and pump performance before the well is opened or the pump is pulled.",
        "local_context": """
<p>Lake and second-home properties create a few special problems: equipment may sit unused for periods, pressure tanks may be tucked into sheds or crawlspaces, long runs from the well can hide leaks, and seasonal use can make intermittent failures harder to reproduce.</p>
<p>We also see iron/sediment complaints, low-pressure complaints that are really pressure-tank problems, and pumps that short-cycle for months before finally stopping. Catching those symptoms early can prevent a burned-up pump motor.</p>
""",
        "symptoms": [
            "Whole house suddenly has no water",
            "Water pressure fades during showers or laundry",
            "Pump clicks on and off rapidly",
            "Faucets spit air after the system sits",
            "Pressure gauge falls when no water is being used",
            "Breaker trips when the pump tries to start",
        ],
        "checks": [
            "Confirm whether the outage is electrical, control-related, pressure-related or down-hole",
            "Inspect pressure switch, gauge, tank air charge and visible piping",
            "Look for leaks on long service runs between the well and the home",
            "Check pump performance and whether the system reaches normal shut-off pressure",
            "Evaluate water-quality symptoms separately from pump/pressure symptoms",
            "Recommend pump pulling only when the test results point to a down-hole failure",
        ],
        "price_drivers": [
            "Whether the problem is a switch, tank, control, leak or submersible pump",
            "Well depth and accessibility of the well head",
            "Pump horsepower and existing electrical configuration",
            "Condition of drop pipe, wire, fittings and check valves",
            "Whether long buried runs or lake-property access complicate the repair",
        ],
        "faqs": [
            ("Do you repair well pumps at Lake Secession?", "Yes. Iva and Lake Secession are specifically covered by our rural/lake service area. We handle no-water calls, pressure tanks, pressure switches, pump diagnostics and pump replacement."),
            ("How much is a well-pump service call in Iva?", "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. Repair or replacement is quoted separately after the failure is identified."),
            ("Should I keep resetting the breaker if the well pump trips it?", "No. Repeated resets can damage wiring, controls or the pump motor and can create an electrical hazard. If the breaker trips again after one reset, leave it off and have the system diagnosed."),
            ("Can a bad pressure tank make it seem like the pump is failing?", "Yes. A waterlogged or ruptured-bladder tank can make the pump start every few seconds, cause pressure swings and shorten pump life. Tank condition is one of the first things we check."),
            ("What if the water is rusty or has sediment after the house sits?", "That can be a well-water quality issue, sediment disturbance, iron, a pressure-system issue or a combination. We separate water-quality problems from pump-performance problems so the repair addresses the real cause."),
        ],
        "related": [
            ("💧", "Full Well Pump Service", "/services/well-pump-repair/", "Pump, pressure tank, switch and water-system troubleshooting."),
            ("🏡", "Iva & Lake Secession Plumbing", "/service-areas/iva-lake-secession-sc/", "Plumbing coverage for lake and rural homes."),
            ("📘", "Well Pump Owner's Manual", "/guides/well-pump-owners-manual-upstate-sc/", "Learn what each part of the well system does and what failure signs mean."),
            ("💰", "Upfront Pricing", "/pricing/", "Current service-call schedule and planning ranges."),
        ],
    },
    "drain-cleaning-greenwood-sc": {
        "title": "Drain Cleaning Greenwood SC | Plumbing Paramedic 911",
        "description": "Drain cleaning in Greenwood SC for kitchen, bathroom and main-line backups. We distinguish fixture clogs, sewer problems and septic issues before recommending the fix. Call (864) 446-8911.",
        "h1": "Drain Cleaning in Greenwood, SC",
        "badge": "● Clogs, Backups & Main-Line Problems",
        "city": "Greenwood",
        "area_type": "City",
        "service_type": "Drain Cleaning",
        "parent_service": "/services/drain-cleaning/",
        "parent_service_name": "Drain Cleaning",
        "city_page": "/service-areas/greenwood-sc/",
        "city_page_name": "Greenwood, SC",
        "guide": "/guides/drain-maintenance-playbook/",
        "guide_name": "Drain Maintenance Playbook",
        "og": "/images/og/drain-cleaning-1200x630.jpg",
        "intro": "A slow sink, overflowing toilet and whole-house sewer backup are three different problems. In Greenwood, we first identify whether the blockage is at one fixture, a branch line, the building sewer, or — on rural and lake properties — a septic-system issue. Then we choose the least destructive method that actually solves it.",
        "answer": "If more than one drain is backing up in a Greenwood home, stop running water until the main line is checked. Water rising in a tub or shower when a toilet flushes is a strong main-line warning. A single slow fixture is more likely a local trap or branch clog.",
        "local_context": """
<p>Greenwood has a wide range of plumbing systems: older in-town homes with aging cast-iron drains, newer subdivisions with PVC, commercial kitchens, and Lake Greenwood/rural properties where septic systems can mimic a sewer-line clog.</p>
<p>That mix is why we do not treat every backup with the same snake. Recurring clogs can come from grease, scale, roots, damaged pipe, a belly in the line, or a septic tank that needs attention. Clearing the symptom without identifying the pattern is how homeowners end up paying for the same clog again.</p>
""",
        "symptoms": [
            "Several drains slow down at the same time",
            "Toilet flushing makes water rise in a tub or shower",
            "Kitchen drain repeatedly clogs after being cleared",
            "Gurgling toilets or sewer odor inside the home",
            "Floor drain or cleanout overflows when appliances discharge",
            "Backup returns quickly after a previous snaking",
        ],
        "checks": [
            "Determine whether the blockage is fixture-level, branch-line or main sewer",
            "Check cleanouts and flow direction before running equipment",
            "Use the correct cable/head for the type and location of blockage",
            "Recommend camera inspection when a clog is recurring or pipe damage is suspected",
            "Separate septic-capacity problems from pipe blockages on rural/lake properties",
            "Use hydro jetting when grease, heavy scale or root debris calls for wall-to-wall cleaning",
        ],
        "price_drivers": [
            "Single fixture vs branch drain vs main sewer line",
            "Access to a usable cleanout and distance to the blockage",
            "Whether camera inspection is needed to explain a recurring problem",
            "Grease, roots, scale or damaged piping that requires more than basic cabling",
            "Septic-system conditions on properties not connected to municipal sewer",
        ],
        "faqs": [
            ("How much is drain cleaning in Greenwood, SC?", "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. The drain-cleaning price depends on whether it is a fixture, branch or main-line blockage, access and whether camera or jetting work is needed. We quote the work before proceeding."),
            ("How do I know if the main sewer line is clogged?", "Multiple fixtures backing up together, water rising in a tub when a toilet flushes, gurgling toilets and sewage at a floor drain or cleanout are common main-line signs. Stop using water until the line is checked."),
            ("Do you use a sewer camera?", "Yes, especially for recurring clogs. A camera can show roots, broken pipe, scale, a belly or another structural problem that a cable alone cannot explain."),
            ("Can a full septic tank look like a clogged drain?", "Yes. On Lake Greenwood and rural properties, a full or failing septic system can cause slow drains and whole-house backups. We distinguish a pipe blockage from a septic-capacity problem before recommending repeated snaking."),
            ("Is hydro jetting always better than snaking?", "No. A cable is often the fastest and least expensive tool for a simple blockage. Hydro jetting is more useful for heavy grease, scale and root debris where cleaning the pipe wall matters."),
        ],
        "related": [
            ("🚿", "Full Drain Cleaning Service", "/services/drain-cleaning/", "Augering, main-line clearing, camera inspection and hydro jetting."),
            ("📍", "Greenwood Plumbing", "/service-areas/greenwood-sc/", "All Plumbing Paramedic 911 services in Greenwood."),
            ("📗", "Drain Maintenance Playbook", "/guides/drain-maintenance-playbook/", "Homeowner guidance for preventing and recognizing drain problems."),
            ("💰", "Upfront Pricing", "/pricing/", "Current service-call schedule and planning ranges."),
        ],
    },
    "water-heater-repair-greenwood-sc": {
        "title": "Water Heater Repair Greenwood SC | Plumbing Paramedic 911",
        "description": "Water heater repair in Greenwood SC for no hot water, leaks, pilot/ignition problems, failed elements and noisy tanks. Repair-vs-replace guidance and upfront pricing. Call (864) 446-8911.",
        "h1": "Water Heater Repair in Greenwood, SC",
        "badge": "● Tank, Gas, Electric & Tankless",
        "city": "Greenwood",
        "area_type": "City",
        "service_type": "Water Heater Repair",
        "parent_service": "/services/water-heater-repair-replacement/",
        "parent_service_name": "Water Heater Services",
        "city_page": "/service-areas/greenwood-sc/",
        "city_page_name": "Greenwood, SC",
        "guide": "/guides/water-heater-buyers-guide-sc/",
        "guide_name": "SC Water Heater Buyer's Guide",
        "og": "/images/og/water-heater-1200x630.jpg",
        "intro": "No hot water does not automatically mean you need a new heater. In Greenwood, we diagnose thermostats, elements, gas controls, ignition components, venting, leaks, sediment symptoms and tank condition first — then explain whether repair or replacement makes better financial sense.",
        "answer": "A leaking tank body usually points toward replacement; a failed element, thermostat, igniter, thermocouple or control can often be repaired. Age matters, but the right decision comes from the failure, tank condition, safety/code requirements and the cost of the repair relative to replacement.",
        "local_context": """
<p>Greenwood homes range from older in-town properties to newer subdivisions and Lake Greenwood houses. We see electric tanks, natural-gas units, propane installations and more tankless systems than we did a decade ago. Each has a different diagnostic path.</p>
<p>Mineral scale and sediment can also show up as popping/rumbling, reduced hot-water capacity and shortened component life. A noisy heater is not always an emergency, but water around the base of the tank is something to address quickly.</p>
""",
        "symptoms": [
            "No hot water or only lukewarm water",
            "Hot water runs out much faster than it used to",
            "Water around the base of the tank",
            "Pilot will not stay lit or gas unit repeatedly faults",
            "Electric heater trips a breaker or stops heating one/both elements",
            "Popping, rumbling or rusty hot water",
        ],
        "checks": [
            "Confirm fuel/power and isolate whether the problem is electrical, gas-control or tank-related",
            "Inspect for active leaks and determine whether the tank shell itself is leaking",
            "Test thermostats/elements or ignition/control components as appropriate",
            "Check venting and combustion safety on gas equipment",
            "Review age, condition and repair cost before recommending replacement",
            "If replacing, identify code-required pan, drain, expansion, venting or connection upgrades before quoting",
        ],
        "price_drivers": [
            "Repairable component failure vs a leaking/failed tank",
            "Gas, electric, propane, heat-pump or tankless equipment",
            "Tank size, location and access for removal/replacement",
            "Code-required venting, expansion, drain-pan or connection upgrades",
            "Whether the replacement is like-for-like or a fuel/type/location conversion",
        ],
        "faqs": [
            ("How much is a water-heater service call in Greenwood?", "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. Repair or replacement is quoted after we identify the failed component, equipment type and any code/access requirements."),
            ("Should I repair or replace my water heater?", "A younger heater with a failed element, thermostat, igniter or similar component can often be repaired. A leaking tank shell, severe corrosion or an older heater needing a major repair usually pushes the decision toward replacement. We show both options when both are reasonable."),
            ("What should I do if the water heater is leaking?", "If water is actively escaping, shut off the cold-water supply to the heater if you can do so safely. For an electric unit, turn off the correct breaker; for a gas unit, follow the appliance shutoff instructions if safe. Call for service, especially if water is reaching floors or walls."),
            ("Do you work on tankless water heaters in Greenwood?", "Yes. We diagnose tankless ignition, flow, scale and control problems and can also discuss replacement or conversion when the existing unit is not worth repairing."),
            ("Can you replace a water heater the same day?", "Many standard tank replacements can be completed the same day when the correct equipment and code requirements are known. Availability, equipment type and any venting/gas/electrical upgrades can affect timing."),
        ],
        "related": [
            ("🔥", "Full Water Heater Service", "/services/water-heater-repair-replacement/", "Repair, replacement, tankless and heat-pump options."),
            ("📍", "Greenwood Plumbing", "/service-areas/greenwood-sc/", "All Plumbing Paramedic 911 services in Greenwood."),
            ("📕", "SC Water Heater Buyer's Guide", "/guides/water-heater-buyers-guide-sc/", "Compare tank, tankless and replacement decisions before you buy."),
            ("💰", "Upfront Pricing", "/pricing/", "Current service-call schedule and planning ranges."),
        ],
    },
    "water-heater-repair-anderson-sc": {
        "title": "Water Heater Repair Anderson SC | Plumbing Paramedic 911",
        "description": "Water heater repair in Anderson SC for leaks, no hot water, failed elements, ignition/control problems and tankless faults. Upfront repair-vs-replace guidance. Call (864) 446-8911.",
        "h1": "Water Heater Repair in Anderson, SC",
        "badge": "● Repair or Replace — Explained First",
        "city": "Anderson",
        "area_type": "City",
        "service_type": "Water Heater Repair",
        "parent_service": "/services/water-heater-repair-replacement/",
        "parent_service_name": "Water Heater Services",
        "city_page": "/service-areas/anderson-sc/",
        "city_page_name": "Anderson, SC",
        "guide": "/guides/water-heater-buyers-guide-sc/",
        "guide_name": "SC Water Heater Buyer's Guide",
        "og": "/images/og/water-heater-1200x630.jpg",
        "intro": "Anderson homeowners call us for everything from a dead electric element to a leaking gas tank or tankless error code. We test the actual failure, inspect the heater's condition and explain the repair-vs-replacement tradeoff before you authorize the work.",
        "answer": "If the tank itself is leaking, replacement is usually the correct path. If the tank is sound, many no-hot-water failures are component problems. The diagnosis should identify the failed part and any safety/code issues before the conversation turns to buying a new heater.",
        "local_context": """
<p>Anderson's housing mix ranges from older in-town homes to newer subdivisions and rural properties across the county. That means we encounter older atmospheric-vent gas heaters, electric tanks, propane, newer high-efficiency units and tankless equipment — sometimes in locations that make access or venting the biggest part of the job.</p>
<p>We pay particular attention to installation details because a heater can be the right size and still be wrong for the space if venting, combustion air, drainage or electrical/gas supply is not correct.</p>
""",
        "symptoms": [
            "No hot water, intermittent hot water or long recovery time",
            "Tank leaking or corrosion around fittings",
            "Gas heater will not light or repeatedly shuts down",
            "Electric heater trips breaker or loses one heating stage",
            "Tankless unit displays fault codes or goes cold under demand",
            "Popping, rumbling, discoloration or odor from hot water",
        ],
        "checks": [
            "Identify fuel/equipment type and reproduce the failure safely",
            "Check tank and connections for leaks before replacing controls or elements",
            "Test electrical heating components or gas ignition/control components",
            "Inspect gas venting / combustion conditions where applicable",
            "Compare repair cost, age and tank condition before recommending replacement",
            "Quote required connection, expansion, drainage, venting or fuel-supply changes before replacement",
        ],
        "price_drivers": [
            "Component repair vs tank failure",
            "Gas/electric/propane/tankless equipment and parts availability",
            "Tank capacity and whether the replacement matches the existing installation",
            "Attic, crawlspace, closet or other difficult access",
            "Venting, gas-line, electrical, drain-pan or expansion requirements",
        ],
        "faqs": [
            ("How much is a water-heater service call in Anderson, SC?", "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. We price the repair or replacement separately after diagnosing the heater and identifying any installation requirements."),
            ("Does a water heater have to be replaced if it stops heating?", "No. Electric elements and thermostats, gas ignition parts and some controls are repairable. A leaking tank body is different — once the tank shell fails, replacement is usually necessary."),
            ("Do you repair gas and electric water heaters?", "Yes. We service gas, electric and tankless equipment and evaluate each using the correct electrical, combustion and water-side checks."),
            ("Can you install a tankless water heater in Anderson?", "Yes, but a tankless conversion may require gas-line, venting or electrical changes. We inspect those requirements first so the quote reflects the whole installation rather than just the appliance."),
            ("What information helps when I call?", "If you can safely read it, the fuel type, approximate age, tank size and model/serial label help. Also tell us whether the tank is leaking, whether power/gas is on, and what changed immediately before the problem started."),
        ],
        "related": [
            ("🔥", "Full Water Heater Service", "/services/water-heater-repair-replacement/", "Repair, replacement, tankless and heat-pump options."),
            ("📍", "Anderson Plumbing", "/service-areas/anderson-sc/", "All Plumbing Paramedic 911 services in Anderson."),
            ("📕", "SC Water Heater Buyer's Guide", "/guides/water-heater-buyers-guide-sc/", "Compare replacement types and common tradeoffs."),
            ("💰", "Upfront Pricing", "/pricing/", "Current service-call schedule and planning ranges."),
        ],
    },    "water-heater-repair-abbeville-sc": {
        "title": "Water Heater Repair Abbeville SC | Plumbing Paramedic 911",
        "description": "Water heater repair in Abbeville SC for leaks, no hot water, failed elements, ignition/control problems and tankless faults. Upfront repair-vs-replace guidance. Call (864) 446-8911.",
        "h1": "Water Heater Repair in Abbeville, SC",
        "badge": "● Repair or Replace — Explained First",
        "city": "Abbeville",
        "area_type": "City",
        "service_type": "Water Heater Repair",
        "parent_service": "/services/water-heater-repair-replacement/",
        "parent_service_name": "Water Heater Services",
        "city_page": "/service-areas/abbeville-sc/",
        "city_page_name": "Abbeville, SC",
        "guide": "/guides/water-heater-buyers-guide-sc/",
        "guide_name": "SC Water Heater Buyer's Guide",
        "og": "/images/og/water-heater-1200x630.jpg",
        "intro": "Because our shop is on Callaway Drive, Abbeville water-heater calls start in our home market. We diagnose failed electric elements, thermostats, gas controls, ignition faults, leaking tanks and tankless error codes before explaining whether repair or replacement makes better financial sense.",
        "answer": "If the tank itself is leaking, replacement is usually the correct path. If the tank is sound, many no-hot-water failures are component problems. The diagnosis should identify the failed part and any safety/code issues before the conversation turns to buying a new heater.",
        "local_context": """
<p>Abbeville has historic in-town homes, mid-century houses, newer subdivisions and rural properties across the county. We encounter older atmospheric-vent gas heaters, electric tanks, propane equipment and newer tankless systems. Crawlspaces, closets and additions can make access, drainage or venting as important as the appliance itself.</p>
<p>Local hard-water and sediment symptoms can reduce hot-water capacity or create popping and rumbling. We also verify pans, drains, expansion control, electrical or gas supply and venting so a replacement quote covers the complete installation rather than only the tank.</p>
""",
        "symptoms": [
            "No hot water, intermittent hot water or long recovery time",
            "Tank leaking or corrosion around fittings",
            "Gas heater will not light or repeatedly shuts down",
            "Electric heater trips breaker or loses one heating stage",
            "Tankless unit displays fault codes or goes cold under demand",
            "Popping, rumbling, discoloration or odor from hot water",
        ],
        "checks": [
            "Identify fuel/equipment type and reproduce the failure safely",
            "Check tank and connections for leaks before replacing controls or elements",
            "Test electrical heating components or gas ignition/control components",
            "Inspect gas venting / combustion conditions where applicable",
            "Compare repair cost, age and tank condition before recommending replacement",
            "Quote required connection, expansion, drainage, venting or fuel-supply changes before replacement",
        ],
        "price_drivers": [
            "Component repair vs tank failure",
            "Gas/electric/propane/tankless equipment and parts availability",
            "Tank capacity and whether the replacement matches the existing installation",
            "Attic, crawlspace, closet or other difficult access",
            "Venting, gas-line, electrical, drain-pan or expansion requirements",
        ],
        "faqs": [
            ("How much is a water-heater service call in Abbeville, SC?", "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. We price the repair or replacement separately after diagnosing the heater and identifying any installation requirements."),
            ("Does a water heater have to be replaced if it stops heating?", "No. Electric elements and thermostats, gas ignition parts and some controls are repairable. A leaking tank body is different — once the tank shell fails, replacement is usually necessary."),
            ("Do you repair gas and electric water heaters?", "Yes. We service gas, electric and tankless equipment and evaluate each using the correct electrical, combustion and water-side checks."),
            ("Can you install a tankless water heater in Abbeville?", "Yes, but a tankless conversion may require gas-line, venting or electrical changes. We inspect those requirements first so the quote reflects the whole installation rather than just the appliance."),
            ("What information helps when I call?", "If you can safely read it, the fuel type, approximate age, tank size and model/serial label help. Also tell us whether the tank is leaking, whether power/gas is on, and what changed immediately before the problem started."),
        ],
        "related": [
            ("🔥", "Full Water Heater Service", "/services/water-heater-repair-replacement/", "Repair, replacement, tankless and heat-pump options."),
            ("📍", "Abbeville Plumbing", "/service-areas/abbeville-sc/", "All Plumbing Paramedic 911 services in Abbeville."),
            ("📕", "SC Water Heater Buyer's Guide", "/guides/water-heater-buyers-guide-sc/", "Compare replacement types and common tradeoffs."),
            ("💰", "Upfront Pricing", "/pricing/", "Current service-call schedule and planning ranges."),
        ],
    },
    "emergency-plumber-abbeville-sc": {
        "title": "Emergency Plumber Abbeville SC | Plumbing Paramedic 911",
        "description": "24/7 emergency plumber in Abbeville SC for burst pipes, flooding, sewer backups, leaking water heaters and no-water emergencies. Local Abbeville dispatch. Call (864) 446-8911.",
        "h1": "Emergency Plumber in Abbeville, SC",
        "badge": "● 24/7 Local Emergency Dispatch",
        "city": "Abbeville",
        "area_type": "City",
        "service_type": "Emergency Plumbing",
        "parent_service": "/services/24-7-emergency-plumbing/",
        "parent_service_name": "24/7 Emergency Plumbing",
        "city_page": "/service-areas/abbeville-sc/",
        "city_page_name": "Abbeville, SC",
        "guide": "/guides/sc-homeowner-plumbing-survival-guide/",
        "guide_name": "SC Homeowner Plumbing Survival Guide",
        "og": "/images/og/emergency-plumbing-1200x630.jpg",
        "intro": "Plumbing Paramedic 911 is based in Abbeville, so a local burst pipe, sewer backup, leaking water heater or no-water emergency starts from our home market instead of a dispatch center in another county. Typical Abbeville response is about 30–45 minutes when a technician is available.",
        "answer": "If water is actively damaging the home, shut off the closest fixture valve or the main water supply if you can do so safely, then call. If sewage is backing up, stop using toilets, sinks, showers and appliances until the blockage is controlled. If you smell gas, leave the building and contact the gas utility or 911 from a safe location before arranging plumbing repair.",
        "local_context": """
<p>Our shop is on Callaway Drive in Abbeville. That makes the city and nearby Abbeville County our closest emergency territory. We routinely deal with older-home supply piping, failed shutoff valves, sewer backups, water-heater leaks and rural no-water calls.</p>
<p>An emergency visit has two goals: stop the damage first, then diagnose the permanent repair. Sometimes that means an immediate isolation or temporary stabilization followed by a scheduled replacement after the property is safe.</p>
""",
        "symptoms": [
            "Burst or actively leaking pipe",
            "Water heater leaking onto floors or into a crawlspace",
            "Sewer backup into toilets, tubs or floor drains",
            "Whole house suddenly has no water",
            "Main shutoff valve will not close during a leak",
            "Water coming through a ceiling, wall or floor",
        ],
        "checks": [
            "Control active water flow or sewage exposure before secondary damage spreads",
            "Identify whether the source is supply, drain/sewer, water heater, fixture or well system",
            "Isolate the failed section when possible so the rest of the property can be stabilized",
            "Check for hidden damage or additional leaks that appeared after pressure loss/restoration",
            "Explain temporary vs permanent repair options when a full replacement cannot be completed immediately",
            "Give the repair price before moving from emergency stabilization into additional work",
        ],
        "price_drivers": [
            "Time of dispatch: weekday, after hours/weekend, or after midnight/holiday",
            "Whether the emergency can be isolated quickly or requires immediate repair to stop damage",
            "Access inside walls, ceilings, crawlspaces or buried piping",
            "Materials and code-required work needed for a permanent repair",
            "Whether water extraction, sewer cleanup or follow-up replacement work is required",
        ],
        "faqs": [
            ("How fast can an emergency plumber get to Abbeville, SC?", "Because Plumbing Paramedic 911 is based in Abbeville, our published typical response for Abbeville is about 30–45 minutes when a technician is available. Active calls, weather and job conditions can change response time, so call for the current ETA."),
            ("How much is an emergency plumbing service call?", "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. The repair itself is quoted separately after the emergency is diagnosed."),
            ("What should I do while a burst pipe is leaking?", "If you can safely reach the main water shutoff, turn it off. Then open a lower faucet to relieve pressure and move valuables away from the water. Avoid electrical panels, outlets or energized equipment in wet areas."),
            ("Is a sewer backup an emergency?", "Yes when sewage is entering occupied space or multiple fixtures are backing up. Stop using water and call. Continuing to flush or run appliances can push more sewage into the building."),
            ("What should I do if I smell gas?", "Leave the building, avoid switches/flames, and call the gas utility or 911 from a safe location. Do not stay inside waiting for a plumber. Once the immediate gas-safety situation is controlled, a qualified repair and pressure test can be arranged."),
        ],
        "related": [
            ("🚨", "24/7 Emergency Plumbing", "/services/24-7-emergency-plumbing/", "Emergency response information for the full service area."),
            ("📍", "Abbeville Plumbing", "/service-areas/abbeville-sc/", "All local plumbing services from our home market."),
            ("📙", "Homeowner Survival Guide", "/guides/sc-homeowner-plumbing-survival-guide/", "Know the shutoffs, warning signs and first moves before an emergency happens."),
            ("💰", "Upfront Pricing", "/pricing/", "Current service-call schedule and planning ranges."),
        ],
    },
    "emergency-plumber-anderson-sc": {
        "title": "Emergency Plumber Anderson SC | Plumbing Paramedic 911",
        "description": "24/7 emergency plumber for Anderson SC: burst pipes, polybutylene failures, sewer backups, leaking water heaters and no-water calls. Upfront dispatch pricing. Call (864) 446-8911.",
        "h1": "Emergency Plumber in Anderson, SC",
        "badge": "\u25cf 24/7 Emergency Dispatch to Anderson County",
        "city": "Anderson",
        "area_type": "City",
        "service_type": "Emergency Plumbing",
        "parent_service": "/services/24-7-emergency-plumbing/",
        "parent_service_name": "24/7 Emergency Plumbing",
        "city_page": "/service-areas/anderson-sc/",
        "city_page_name": "Anderson, SC",
        "guide": "/guides/sc-homeowner-plumbing-survival-guide/",
        "guide_name": "SC Homeowner Plumbing Survival Guide",
        "og": "/images/og/emergency-plumbing-1200x630.jpg",
        "intro": "Plumbing Paramedic 911 dispatches to Anderson 24 hours a day, every day of the year. Typical response is about 60 minutes when a technician is available. The service / diagnostic call is $79 weekdays 9 AM\u20135 PM, $99 after hours and weekends, and $158 after midnight or on holidays \u2014 with no distance or per-mile surcharge for Anderson.",
        "answer": "If water is actively damaging the home, close the fixture shutoff or the main water valve if you can reach it safely, then call. If sewage is backing up, stop using every toilet, sink, shower and appliance until the blockage is controlled \u2014 each additional flush pushes more sewage inside. If you smell gas, leave the building first and call the gas utility or 911 from outside before arranging plumbing repair.",
        "local_context": """
<p>Anderson is the largest city we serve, and the emergencies here follow the housing stock. In 1980s subdivisions we see polybutylene supply lines fail without warning \u2014 the gray plastic pipe was installed widely across the South and a lot of it is now past its service life. Those failures tend to be sudden, full-pressure leaks rather than slow drips, which is exactly the call that cannot wait for a scheduled appointment.</p>
<p>In the mid-century parts of Anderson, the emergency is more often a sewer backup out of a corroded cast-iron drain stack. In both cases the first job is the same: stop the damage, then diagnose the permanent repair. We will isolate and stabilize a property at 2 AM and schedule the full replacement in daylight when that is the safer and cheaper sequence for the homeowner.</p>
""",
        "symptoms": [
            "Burst or actively spraying supply line, including gray polybutylene pipe",
            "Water coming through a ceiling, wall or light fixture",
            "Sewage backing up into toilets, tubs or a floor drain",
            "Water heater leaking onto a floor, into a closet or into a crawlspace",
            "Whole house suddenly has no water or no pressure",
            "Main shutoff valve will not close while a leak is running",
        ],
        "checks": [
            "Control the active leak or sewage exposure before secondary damage spreads",
            "Identify whether the source is supply, drain/sewer, water heater, fixture or well system",
            "Isolate the failed section so the rest of the house can be put back in service",
            "Check for additional failures that appear once pressure is restored \u2014 common on aging polybutylene",
            "Explain temporary stabilization vs permanent repair when a full replacement cannot be finished that night",
            "Give the repair price before moving from emergency stabilization into additional work",
        ],
        "price_drivers": [
            "Time of dispatch: weekday, after hours/weekend, or after midnight/holiday",
            "Whether the failure can be isolated quickly or must be repaired on the spot to stop damage",
            "Access to the failed pipe \u2014 open crawlspace, finished ceiling, slab or buried line",
            "Pipe material: a polybutylene failure often means the surrounding line is also due",
            "Whether follow-up work (repipe, drain replacement, water extraction) is needed afterward",
        ],
        "faqs": [
            ("How fast can an emergency plumber get to Anderson, SC?", "Our published typical response for Anderson is about 60 minutes from the Abbeville shop when a technician is available. Active calls, weather and traffic change that, so call for the current ETA rather than assuming."),
            ("Do you charge extra to drive to Anderson?", "No. There is no distance or per-mile surcharge for Anderson. The service / diagnostic call is $79 Monday\u2013Friday 9 AM\u20135 PM, $99 after hours and weekends, and $158 after midnight or on holidays \u2014 the same schedule we charge in Abbeville."),
            ("My gray plastic water line burst. Can you fix it tonight?", "Usually yes, at least to stop the damage. Polybutylene is repairable in the short term, but a failure in one spot often means the rest of the line is near the end of its life. We stabilize the emergency first and then give you a written price for a permanent repair or repipe."),
            ("Is a sewer backup an emergency?", "Yes, when sewage is entering living space or several fixtures are backing up together. Stop running water and call. Every flush after that point adds to the cleanup."),
            ("What should I do while a pipe is leaking?", "Shut off the main water valve if you can reach it safely, open a low faucet to relieve pressure, and move belongings clear of the water. Stay away from panels, outlets and anything energized near standing water."),
            ("Do you answer the phone at night in Anderson?", "Yes. Dispatch is staffed 24/7, including nights, weekends and holidays. The after-midnight and holiday service-call rate is posted on this page before you book."),
        ],
        "related": [
            ("\U0001f6a8", "24/7 Emergency Plumbing", "/services/24-7-emergency-plumbing/", "How emergency dispatch works across the service area."),
            ("\U0001f4cd", "Anderson Plumbing", "/service-areas/anderson-sc/", "Every Plumbing Paramedic 911 service in Anderson."),
            ("\U0001f4b0", "Anderson Plumbing Prices", "/plumbing-prices-anderson-sc/", "Real flat-rate prices for common Anderson jobs."),
            ("\U0001f4d9", "Homeowner Survival Guide", "/guides/sc-homeowner-plumbing-survival-guide/", "Find your shutoffs before you need them."),
        ],
    },
    "drain-cleaning-anderson-sc": {
        "title": "Drain Cleaning Anderson SC | Plumbing Paramedic 911",
        "description": "Drain cleaning in Anderson SC for kitchen, bath and main-line backups. Cable, hydro jetting and camera inspection on cast-iron and PVC drains. Upfront pricing. Call (864) 446-8911.",
        "h1": "Drain Cleaning in Anderson, SC",
        "badge": "\u25cf Clogs, Recurring Backups & Cast-Iron Drains",
        "city": "Anderson",
        "area_type": "City",
        "service_type": "Drain Cleaning",
        "parent_service": "/services/drain-cleaning/",
        "parent_service_name": "Drain Cleaning",
        "city_page": "/service-areas/anderson-sc/",
        "city_page_name": "Anderson, SC",
        "guide": "/guides/drain-maintenance-playbook/",
        "guide_name": "Drain Maintenance Playbook",
        "og": "/images/og/drain-cleaning-1200x630.jpg",
        "intro": "A slow bathroom sink and a whole-house sewer backup are not the same job and should not carry the same price. In Anderson we identify whether the blockage is at one fixture, in a branch line, in the building sewer, or inside a corroded cast-iron stack \u2014 then use the least destructive method that actually fixes it. Clearing a clog in Anderson starts at $225 for a toilet auger and $245 for a sink, tub or shower line.",
        "answer": "If more than one drain in an Anderson home is backing up at the same time, stop running water and have the main line checked before anything else. Water rising in a tub or shower when a toilet flushes is a main-line symptom, not a fixture problem. A single slow drain with everything else running normally is usually a local trap or branch clog.",
        "local_context": """
<p>A large share of Anderson's housing was built mid-century with cast-iron drain stacks, and that changes the job. The inside of an old cast-iron pipe scales and corrodes until the usable diameter is a fraction of what the pipe size suggests. The symptom is a clog that keeps coming back a few weeks after it was cleared, usually at the same fixture.</p>
<p>Cabling that line opens a channel through the blockage. Hydro jetting scours the pipe wall and buys considerably more time. Neither one restores a pipe that has lost its structure \u2014 when the camera shows that, we say so and price the replacement instead of selling the same clog back to you twice a year.</p>
<p>Newer Anderson subdivisions are a different problem set: PVC drains that fail at a belly, a settled joint or tree roots at the property line rather than from internal corrosion.</p>
""",
        "symptoms": [
            "Several fixtures slow down or back up at the same time",
            "Water rises in a tub or shower when a toilet is flushed",
            "The same drain clogs again a few weeks after being cleared",
            "Gurgling toilets or sewer odor inside the house",
            "Floor drain or cleanout overflows when the washer discharges",
            "Kitchen line that never fully drains even when it is not blocked",
        ],
        "checks": [
            "Determine whether the blockage is fixture-level, branch-line or main sewer",
            "Locate and open a usable cleanout before running any equipment",
            "Match the cable and head to the pipe material, size and type of blockage",
            "Camera the line when a clog is recurring, so the cause is identified rather than guessed",
            "Check for internal scale and loss of diameter in older cast-iron stacks",
            "Use hydro jetting where grease, heavy scale or root debris means the pipe wall needs cleaning",
        ],
        "price_drivers": [
            "Single fixture vs branch drain vs main sewer line",
            "Whether a usable cleanout exists, and the distance to the blockage",
            "Pipe material and condition \u2014 scaled cast iron takes longer than clean PVC",
            "Whether camera inspection is needed to explain a repeating problem",
            "Grease, roots or structural damage that cabling alone will not resolve",
        ],
        "faqs": [
            ("How much does drain cleaning cost in Anderson, SC?", "Clearing a toilet with a hand auger is $225 and a sink, tub or shower line is $245. A difficult sink or lavatory arm is $289, electric hydro jetting of a branch or main drain is $325, and a video camera inspection of the drain line is $395. The service / diagnostic call is separate: $79 Monday\u2013Friday 9 AM\u20135 PM, $99 after hours and weekends, $158 after midnight or on holidays. Main sewer work is priced separately \u2014 see our Anderson price list."),
            ("How do I know if my main sewer line is clogged?", "Several fixtures backing up together, water rising in a tub when a toilet flushes, gurgling toilets, and sewage appearing at a floor drain or cleanout all point at the main line. Stop using water until it is checked."),
            ("Why does my drain keep clogging in the same place?", "In older Anderson homes that is usually internal scale in a cast-iron stack: the pipe's usable diameter has shrunk, so it re-blocks quickly. A camera inspection shows whether jetting will buy real time or whether the section needs replacing."),
            ("Do you use a sewer camera?", "Yes. Drain line inspection with a video camera is $395, and a full sewer line inspection is $495. We recommend it for recurring clogs, because a cable cannot tell you about roots, a belly, a broken joint or lost pipe structure."),
            ("Is hydro jetting better than snaking?", "Not always. A cable is often the faster and cheaper tool for a straightforward blockage. Jetting earns its price where grease, heavy scale or root debris means the pipe wall itself has to be cleaned."),
            ("Can you clear a drain the same day in Anderson?", "Usually yes. Drain calls are typically same-day, and we dispatch to Anderson 24/7 when a backup cannot wait."),
        ],
        "related": [
            ("\U0001f6bf", "Full Drain Cleaning Service", "/services/drain-cleaning/", "Cabling, main-line clearing, camera inspection and hydro jetting."),
            ("\U0001f4cd", "Anderson Plumbing", "/service-areas/anderson-sc/", "Every Plumbing Paramedic 911 service in Anderson."),
            ("\U0001f4b0", "Anderson Plumbing Prices", "/plumbing-prices-anderson-sc/", "Flat-rate prices for drains, heaters, toilets and well pumps."),
            ("\U0001f4d7", "Drain Maintenance Playbook", "/guides/drain-maintenance-playbook/", "How to stop paying for the same clog twice."),
        ],
    },
    "plumbing-prices-greenwood-sc": {
        "title": "Plumbing Prices Greenwood SC | Plumbing Paramedic 911",
        "description": "Real flat-rate plumbing prices for Greenwood SC: drain cleaning from $225, water heater installs from $1,800, well tanks from $795. Service call $79 weekdays. Call (864) 446-8911.",
        "h1": "Plumbing Prices in Greenwood, SC",
        "badge": "\u25cf Published Flat-Rate Prices \u2014 Not Estimates",
        "city": "Greenwood",
        "area_type": "City",
        "service_type": "Plumbing",
        "parent_service": "/pricing/",
        "parent_service_name": "Pricing",
        "city_page": "/service-areas/greenwood-sc/",
        "city_page_name": "Greenwood, SC",
        "guide": "/guides/water-heater-buyers-guide-sc/",
        "guide_name": "Water Heater Buyer\u2019s Guide",
        "og": "/images/og/greenwood-1200x630.jpg",
        "intro": "These are the actual flat-rate prices from our Greenwood price book \u2014 the same numbers the technician quotes at your door, not a range we work out later. The service / diagnostic call is $79 Monday\u2013Friday 9 AM\u20135 PM, $99 after hours and weekends, and $158 after midnight or on holidays. Repair prices below are for the work itself and are approved by you in writing before anything starts.",
        "answer": "In Greenwood, clearing a sink, tub or shower drain is $245 and a toilet auger is $225. A 40-gallon electric water heater installed is $1,800 and a 50-gallon is $2,065. Replacing a well tank pressure switch is $165 and a 22-gallon well tank is $795. Each price is flat-rate for the job under normal access conditions, and the service / diagnostic call is charged separately at $79 weekdays, $99 after hours and weekends, or $158 after midnight and on holidays.",
        "local_context": """
<p>Greenwood\u2019s municipal water is moderately hard, and that shows up in which prices on this page a Greenwood homeowner actually ends up paying. Scale shortens element and tank life, so thermostat and element replacements and full heater swaps are our most common Greenwood invoices by a wide margin. If you are replacing a heater for the second time in eight years, the price to look at is not on this page \u2014 it is the cost of treating the water feeding it.</p>
<p>Out toward Lake Greenwood and on rural Greenwood County properties, the well-pump prices matter more than the municipal ones. A pressure switch is a $165 job; a pressure tank is $795 to $895. Knowing which one failed before anyone opens a wallet is the entire point of diagnosing the system rather than replacing the pump by default.</p>
<p>There is no distance charge to Greenwood. These are the same prices we charge in Abbeville.</p>
""",
        "symptoms": [
            "You want a number before you book, not after",
            "Another company quoted hourly and you want to compare like for like",
            "You are deciding between repairing and replacing a water heater",
            "You are budgeting a job that is not an emergency",
            "You want to know what the VIP Diamond Plan actually saves",
            "You were told \u201cit depends\u201d and never got a figure",
        ],
        "checks": [
            "Flat-rate means the price is the price for that job, not an hourly meter",
            "The service / diagnostic call is separate and is posted before you book",
            "Prices assume normal access \u2014 we say so up front when a job does not qualify",
            "You approve the written price before any work begins",
            "If we find a second problem, it gets its own price before we touch it",
            "VIP Diamond Plan members pay the member column on covered repairs",
        ],
        "price_drivers": [
            "Access \u2014 an open crawlspace prices differently than a finished ceiling or a slab",
            "Pipe and fixture material and condition once the job is opened up",
            "Code-required upgrades triggered by replacing an old appliance",
            "Equipment you supply versus equipment we supply and warranty",
            "Time of dispatch, which sets the service-call charge only, not the repair price",
        ],
        "faqs": [
            ("How much does a plumber charge in Greenwood, SC?", "The service / diagnostic call is $79 Monday\u2013Friday 9 AM\u20135 PM, $99 after hours and weekends, and $158 after midnight or on holidays. Repair work is flat-rate on top of that: clearing a drain is $225\u2013$325, a 40-gallon electric water heater installed is $1,800, and a well tank pressure switch is $165. Full prices are listed on this page."),
            ("Do you charge by the hour?", "No. Every repair on this page is flat-rate, so the price does not change if the job takes longer than expected. The only hourly item in our book is extended gas hydro jetting of a main drain, which is priced in blocks and quoted before it starts."),
            ("How much is a water heater in Greenwood?", "Installed, with a 6-year warranty: a 40-gallon electric is $1,800, a 50-gallon electric is $2,065, a 40-gallon natural gas is $1,945, and a 50-gallon natural gas is $2,095. A condensing high-efficiency tankless is $4,495. If the existing heater is still under manufacturer warranty, replacing a 30\u201350 gallon electric is $995."),
            ("Is the service call charged on top of the repair price?", "Yes. The service / diagnostic call covers the trip and the diagnosis. The repair price listed here is for the work itself. We tell you both numbers before anything is done."),
            ("What does the VIP Diamond Plan save me?", "Members pay the member column \u2014 15% off covered repairs. On a $2,065 water heater that is $310 off; on a $245 drain clearing it is $37. The plan also includes an annual whole-home plumbing inspection. Discounts apply to covered work and cannot be combined with another promotion on the same service."),
            ("Will the price change once you are here?", "Not for the job quoted. The price changes only if the scope changes \u2014 different access, a failed part we could not see, or a code-required upgrade. If that happens we stop, explain it, and give you a new written price before continuing."),
            ("Do you charge extra to come to Greenwood?", "No. There is no mileage or distance surcharge. Greenwood pays the same service-call rate and the same flat repair prices as Abbeville."),
        ],
        "related": [
            ("\U0001f4b0", "Price Estimator", "/pricing/", "Build a planning estimate for your own job."),
            ("\U0001f4cd", "Greenwood Plumbing", "/service-areas/greenwood-sc/", "Every Plumbing Paramedic 911 service in Greenwood."),
            ("\U0001f48e", "VIP Diamond Plan", "/membership/", "What the member column costs and covers."),
            ("\U0001f4b3", "Financing", "/financing/", "In-house financing on larger jobs."),
        ],
        "price_table": [
            ("Drain cleaning and sewer", [
                ("Clear a toilet with a hand auger", 225, 191),
                ("Clear a sink, lavatory, tub or shower line with a hand snake", 245, 208),
                ("Clear a difficult sink or lavatory arm", 289, 246),
                ("Clear a branch or main drain with the electric hydro jet", 325, 276),
                ("Drain line inspection with a video camera", 395, 336),
                ("Clear a sewer drain up to 25 ft with the J-cable", 485, 412),
                ("Video inspect the sewer line with a camera", 495, 421),
                ("Clear the main sewer line with the hydro jet, up to 100 ft", 595, 506),
                ("Clear a main drain with the gas hydro jet, up to 1.5 hours", 695, 591),
            ]),
            ("Water heaters", [
                ("Replace a single thermostat", 165, 140),
                ("Replace both upper and lower thermostats", 245, 208),
                ("Replace the T&amp;P safety valve", 225, 191),
                ("Replace a single heating element, up to 4500W", 285, 242),
                ("Flush and refill the heater and replace the drain valve", 285, 242),
                ("Replace the expansion tank", 295, 251),
                ("Replace an electric heater still under warranty, 30\u201350 gal", 995, 846),
                ("40-gallon electric heater installed, 6-year warranty", 1800, 1530),
                ("40-gallon natural gas heater installed, 6-year warranty", 1945, 1653),
                ("50-gallon electric heater installed, 6-year warranty", 2065, 1755),
                ("50-gallon natural gas heater installed, 6-year warranty", 2095, 1781),
                ("Condensing high-efficiency tankless heater installed", 4495, 3821),
            ]),
            ("Toilets, faucets and disposals", [
                ("Replace a toilet supply connector", 115, 98),
                ("Replace a toilet shut-off valve", 135, 115),
                ("Rebuild a toilet tank \u2014 flapper and fill valve", 245, 208),
                ("Remove, reset and seal a toilet", 245, 208),
                ("Replace a garbage disposal you supply", 285, 242),
                ("Install a toilet you supply, with materials", 425, 361),
                ("Install a new 1/2 HP garbage disposal, parts included", 485, 412),
                ("Install an elongated toilet, 10\u201312 inch rough", 495, 421),
                ("Install a new 3/4 HP garbage disposal, parts included", 595, 506),
            ]),
            ("Well pumps and pressure tanks", [
                ("Replace the well tank pressure switch", 165, 140),
                ("Prime a jet pump", 195, 166),
                ("Replace the pressure switch and gauge", 195, 166),
                ("Replace the pressure switch, gauge and nipple", 245, 208),
                ("Replace a 1/2 HP 2-wire well motor, pump under warranty", 495, 421),
                ("Replace a submersible well pump you supply", 795, 676),
                ("Replace a 22-gallon well tank", 795, 676),
                ("Replace a 35-gallon well tank", 895, 761),
            ]),
        ],
    },
    "plumbing-prices-anderson-sc": {
        "title": "Plumbing Prices Anderson SC | Plumbing Paramedic 911",
        "description": "Real flat-rate plumbing prices for Anderson SC: drain cleaning from $225, camera inspection $395, water heater installs from $1,800. Service call $79 weekdays. Call (864) 446-8911.",
        "h1": "Plumbing Prices in Anderson, SC",
        "badge": "\u25cf Published Flat-Rate Prices \u2014 Not Estimates",
        "city": "Anderson",
        "area_type": "City",
        "service_type": "Plumbing",
        "parent_service": "/pricing/",
        "parent_service_name": "Pricing",
        "city_page": "/service-areas/anderson-sc/",
        "city_page_name": "Anderson, SC",
        "guide": "/guides/drain-maintenance-playbook/",
        "guide_name": "Drain Maintenance Playbook",
        "og": "/images/og/anderson-1200x630.jpg",
        "intro": "These are the actual flat-rate prices from our Anderson price book \u2014 the same numbers the technician quotes at your door, not a range we work out later. The service / diagnostic call is $79 Monday\u2013Friday 9 AM\u20135 PM, $99 after hours and weekends, and $158 after midnight or on holidays, with no distance charge for Anderson. Repair prices below are for the work itself and are approved by you in writing before anything starts.",
        "answer": "In Anderson, clearing a toilet with an auger is $225 and clearing a sink, tub or shower line is $245. A video camera inspection of a drain line is $395 and a full sewer line inspection is $495. A 40-gallon electric water heater installed is $1,800 and a 50-gallon is $2,065. Each price is flat-rate for the job under normal access conditions, and the service / diagnostic call is charged separately at $79 weekdays, $99 after hours and weekends, or $158 after midnight and on holidays.",
        "local_context": """
<p>Which of these prices an Anderson homeowner actually pays depends mostly on when the house was built. In the mid-century parts of town with original cast-iron drain stacks, the recurring expense is drain work \u2014 and the $395 camera inspection is usually the cheapest line on this page, because it answers whether $325 of jetting buys you three years or three weeks.</p>
<p>In the 1980s subdivisions, the call is more often a polybutylene supply failure. That is quoted as a repair rather than from a fixed list, because the honest answer depends on how much of the line is left and whether a repipe makes more sense than another patch. We give that price in writing before we start, same as everything else here.</p>
<p>On rural Anderson County properties and out toward Iva, Honea Path, Belton and Pendleton, the well-pump prices below are the ones that matter. There is no distance charge to any of it \u2014 Anderson pays the same rates as Abbeville.</p>
""",
        "symptoms": [
            "You want a number before you book, not after",
            "A drain keeps clogging and you want to know what the camera costs",
            "You are deciding between repairing and replacing a water heater",
            "You are comparing a flat-rate quote against an hourly one",
            "You want to know what the VIP Diamond Plan actually saves",
            "You were told \u201cit depends\u201d and never got a figure",
        ],
        "checks": [
            "Flat-rate means the price is the price for that job, not an hourly meter",
            "The service / diagnostic call is separate and is posted before you book",
            "Prices assume normal access \u2014 we say so up front when a job does not qualify",
            "You approve the written price before any work begins",
            "If we find a second problem, it gets its own price before we touch it",
            "VIP Diamond Plan members pay the member column on covered repairs",
        ],
        "price_drivers": [
            "Access \u2014 an open crawlspace prices differently than a finished ceiling or a slab",
            "Drain pipe material and internal condition, which decides cable vs jetting vs replacement",
            "Code-required upgrades triggered by replacing an old appliance",
            "Equipment you supply versus equipment we supply and warranty",
            "Time of dispatch, which sets the service-call charge only, not the repair price",
        ],
        "faqs": [
            ("How much does a plumber charge in Anderson, SC?", "The service / diagnostic call is $79 Monday\u2013Friday 9 AM\u20135 PM, $99 after hours and weekends, and $158 after midnight or on holidays. Repair work is flat-rate on top of that: clearing a drain is $225\u2013$325, a drain camera inspection is $395, and a 40-gallon electric water heater installed is $1,800. Full prices are listed on this page."),
            ("How much is drain cleaning in Anderson?", "A toilet auger is $225. A sink, lavatory, tub or shower line is $245, or $289 for a difficult lavatory arm. Electric hydro jetting of a branch or main drain is $325. Clearing the main sewer line with the hydro jet up to 100 feet is $595."),
            ("What does a sewer camera inspection cost in Anderson?", "A drain line inspection with a video camera is $395. A full sewer line video inspection is $495. On a drain that has clogged more than once, that is usually the cheapest money you can spend, because it shows whether the pipe can be cleaned or needs replacing."),
            ("Do you charge by the hour?", "No. Every repair on this page is flat-rate, so the price does not change if the job runs long. The only hourly item in our book is extended gas hydro jetting of a main drain, which is priced in blocks and quoted before it starts."),
            ("Do you charge extra to drive to Anderson?", "No. There is no mileage or distance surcharge for Anderson. Same service-call rate, same flat repair prices as Abbeville."),
            ("What does the VIP Diamond Plan save me?", "Members pay the member column \u2014 15% off covered repairs. On a $2,065 water heater that is $310 off; on a $395 camera inspection it is $59. The plan also includes an annual whole-home plumbing inspection. Discounts apply to covered work and cannot be combined with another promotion on the same service."),
            ("Will the price change once you are here?", "Not for the job quoted. It changes only if the scope changes \u2014 different access, a failed part we could not see, or a code-required upgrade. If that happens we stop, explain it, and give you a new written price before continuing."),
        ],
        "related": [
            ("\U0001f4b0", "Price Estimator", "/pricing/", "Build a planning estimate for your own job."),
            ("\U0001f4cd", "Anderson Plumbing", "/service-areas/anderson-sc/", "Every Plumbing Paramedic 911 service in Anderson."),
            ("\U0001f6bf", "Drain Cleaning Anderson", "/drain-cleaning-anderson-sc/", "What we do about a clog that keeps coming back."),
            ("\U0001f48e", "VIP Diamond Plan", "/membership/", "What the member column costs and covers."),
        ],
        "price_table": [
            ("Drain cleaning and sewer", [
                ("Clear a toilet with a hand auger", 225, 191),
                ("Clear a sink, lavatory, tub or shower line with a hand snake", 245, 208),
                ("Clear a difficult sink or lavatory arm", 289, 246),
                ("Clear a branch or main drain with the electric hydro jet", 325, 276),
                ("Drain line inspection with a video camera", 395, 336),
                ("Clear a sewer drain up to 25 ft with the J-cable", 485, 412),
                ("Video inspect the sewer line with a camera", 495, 421),
                ("Clear the main sewer line with the hydro jet, up to 100 ft", 595, 506),
                ("Clear a main drain with the gas hydro jet, up to 1.5 hours", 695, 591),
            ]),
            ("Water heaters", [
                ("Replace a single thermostat", 165, 140),
                ("Replace both upper and lower thermostats", 245, 208),
                ("Replace the T&amp;P safety valve", 225, 191),
                ("Replace a single heating element, up to 4500W", 285, 242),
                ("Flush and refill the heater and replace the drain valve", 285, 242),
                ("Replace the expansion tank", 295, 251),
                ("Replace an electric heater still under warranty, 30\u201350 gal", 995, 846),
                ("40-gallon electric heater installed, 6-year warranty", 1800, 1530),
                ("40-gallon natural gas heater installed, 6-year warranty", 1945, 1653),
                ("50-gallon electric heater installed, 6-year warranty", 2065, 1755),
                ("50-gallon natural gas heater installed, 6-year warranty", 2095, 1781),
                ("Condensing high-efficiency tankless heater installed", 4495, 3821),
            ]),
            ("Toilets, faucets and disposals", [
                ("Replace a toilet supply connector", 115, 98),
                ("Replace a toilet shut-off valve", 135, 115),
                ("Rebuild a toilet tank \u2014 flapper and fill valve", 245, 208),
                ("Remove, reset and seal a toilet", 245, 208),
                ("Replace a garbage disposal you supply", 285, 242),
                ("Install a toilet you supply, with materials", 425, 361),
                ("Install a new 1/2 HP garbage disposal, parts included", 485, 412),
                ("Install an elongated toilet, 10\u201312 inch rough", 495, 421),
                ("Install a new 3/4 HP garbage disposal, parts included", 595, 506),
            ]),
            ("Well pumps and pressure tanks", [
                ("Replace the well tank pressure switch", 165, 140),
                ("Prime a jet pump", 195, 166),
                ("Replace the pressure switch and gauge", 195, 166),
                ("Replace the pressure switch, gauge and nipple", 245, 208),
                ("Replace a 1/2 HP 2-wire well motor, pump under warranty", 495, 421),
                ("Replace a submersible well pump you supply", 795, 676),
                ("Replace a 22-gallon well tank", 795, 676),
                ("Replace a 35-gallon well tank", 895, 761),
            ]),
        ],
    },
}

LINK_TARGETS = {
    "services/well-pump-repair/index.html": ["well-pump-repair-mccormick-sc", "well-pump-repair-iva-lake-secession-sc"],
    "services/drain-cleaning/index.html": ["drain-cleaning-abbeville-sc", "drain-cleaning-greenwood-sc", "drain-cleaning-anderson-sc"],
    "services/water-heater-repair-replacement/index.html": ["water-heater-repair-abbeville-sc", "water-heater-repair-greenwood-sc", "water-heater-repair-anderson-sc"],
    "services/24-7-emergency-plumbing/index.html": ["emergency-plumber-abbeville-sc", "emergency-plumber-anderson-sc"],
    "service-areas/mccormick-sc/index.html": ["well-pump-repair-mccormick-sc"],
    "service-areas/iva-lake-secession-sc/index.html": ["well-pump-repair-iva-lake-secession-sc"],
    "service-areas/greenwood-sc/index.html": ["drain-cleaning-greenwood-sc", "water-heater-repair-greenwood-sc", "plumbing-prices-greenwood-sc"],
    "service-areas/anderson-sc/index.html": ["water-heater-repair-anderson-sc", "emergency-plumber-anderson-sc", "drain-cleaning-anderson-sc", "plumbing-prices-anderson-sc"],
    "service-areas/abbeville-sc/index.html": ["emergency-plumber-abbeville-sc", "drain-cleaning-abbeville-sc", "water-heater-repair-abbeville-sc", "sewer-line-repair-abbeville-sc"],
    "pricing/index.html": ["plumbing-prices-greenwood-sc", "plumbing-prices-anderson-sc"],
    "services/index.html": list(MONEY_PAGES.keys()),
}


def list_html(items: list[str]) -> str:
    return "\n".join(f"<li>{item}</li>" for item in items)


def related_cards(items: list[tuple[str, str, str, str]]) -> str:
    cards = []
    for icon, name, url, description in items:
        cards.append(
            f'<a class="nav-card" href="{url}"><div style="font-size:1.7rem;margin-bottom:8px">{icon}</div>'
            f'<h3>{name}</h3><p>{description}</p><span class="arrow">Open →</span></a>'
        )
    return "\n".join(cards)


def money(value: int) -> str:
    return f"${value:,}"


def price_table_html(groups: list[tuple[str, list[tuple[str, int, int]]]]) -> str:
    """Render the published flat-rate prices.

    The visible table and the Offer schema below are built from the same rows,
    so an answer engine can never quote a number the customer does not see.
    """
    blocks = []
    for title, rows in groups:
        body = "\n".join(
            f'<tr><td class="job-cell">{job}</td>'
            f'<td class="price-cell" data-label="Flat rate">{money(standard)}</td>'
            f'<td class="price-cell" data-label="Member">{money(member)}</td></tr>'
            for job, standard, member in rows
        )
        blocks.append(
            f'<h3 style="margin:28px 0 10px">{title}</h3>'
            f'<div class="table-wrap"><table class="price-table">'
            f'<thead><tr><th scope="col">Job</th><th scope="col">Flat-rate price</th>'
            f'<th scope="col">VIP Diamond member</th></tr></thead>'
            f'<tbody>{body}</tbody></table></div>'
        )
    return "\n".join(blocks)


def offer_catalog(p: dict, service_id: str) -> dict:
    offers = []
    for title, rows in p["price_table"]:
        for job, standard, _member in rows:
            offers.append({
                "@type": "Offer",
                "itemOffered": {"@type": "Service", "name": job, "category": title},
                "priceSpecification": {
                    "@type": "UnitPriceSpecification",
                    "price": str(standard),
                    "priceCurrency": "USD",
                    "valueAddedTaxIncluded": False,
                },
                "areaServed": {"@type": p["area_type"], "name": p["city"] + ", South Carolina"},
                "availability": "https://schema.org/InStock",
                "seller": {"@id": BASE_URL + "/#localbusiness"},
            })
    return {
        "@type": "OfferCatalog",
        "@id": service_id.replace("#service", "#prices"),
        "name": f"Flat-rate plumbing prices in {p['city']}, SC",
        "itemListElement": offers,
    }


def render_page(build, slug: str, p: dict) -> str:
    path = f"/{slug}/"
    service_id = BASE_URL + path + "#service"
    breadcrumb_items = [
        ("Home", "/"),
        (p["parent_service_name"], p["parent_service"]),
        (p["city_page_name"], p["city_page"]),
        (p["h1"], path),
    ]
    extra = [
        {
            "@type": "WebPage",
            "@id": BASE_URL + path + "#webpage",
            "url": BASE_URL + path,
            "name": p["title"].replace("&amp;", "&"),
            "about": {"@id": service_id},
            "isPartOf": {"@id": BASE_URL + "/#website"},
            "inLanguage": "en-US",
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": [".speakable-headline", ".speakable-summary", ".speakable-answer", ".speakable-phone"],
            },
        },
        {
            "@type": "Service",
            "@id": service_id,
            "name": p["h1"].replace("&amp;", "&"),
            "serviceType": p["service_type"],
            "url": BASE_URL + path,
            "description": p["description"],
            "provider": {"@id": BASE_URL + "/#localbusiness"},
            "areaServed": {"@type": p["area_type"], "name": p["city"] + ", South Carolina"},
            **({"hasOfferCatalog": offer_catalog(p, service_id)} if p.get("price_table") else {}),
        },
        build.breadcrumb_ld(breadcrumb_items),
        build.faq_ld(p["faqs"]),
    ]
    head = build.head(
        p["title"], p["description"], path, og_image=p["og"], extra_jsonld=extra,
        body_page=f"local-service-{slug}",
    )
    nav = build.nav("services")
    price_block = ""
    if p.get("price_table"):
        price_block = (
            '<h2 style="margin-top:40px">Published flat-rate repair prices</h2>'
            f'<p class="lead">Prices below are for the work itself, under normal access conditions, '
            f'and are separate from the service / diagnostic call above. '
            f'You approve the written price before any work begins.</p>'
            + price_table_html(p["price_table"])
            + '<p style="font-size:.88rem;color:var(--ink3);margin-top:16px">'
            'VIP Diamond Plan members pay the member column on covered repairs. '
            'If access, code-required upgrades, equipment, materials or hidden conditions change the job, '
            'we stop, explain the difference and get your approval before going further. '
            'Work not listed here is quoted the same way: in writing, before it starts.</p>'
        )
    body = f"""\
<main>
  <section class="page-header">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{build.breadcrumb_html(breadcrumb_items)}</nav>
      <span class="badge" style="display:inline-flex;margin-bottom:14px">{p['badge']}</span>
      <h1 class="speakable-headline">{p['h1']}</h1>
      <p class="speakable-summary">{p['intro']}</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px">
        <a class="btn btn-green btn-lg speakable-phone" href="tel:+18644468911">📞 Call (864) 446-8911</a>
        <a class="btn btn-blue btn-lg" href="/pricing/">💰 See Upfront Pricing</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:960px">
      <div class="card" style="border-left:5px solid var(--green)">
        <span class="label">Short answer</span>
        <h2 style="font-size:1.45rem;margin:7px 0 10px">What should you know first?</h2>
        <p class="lead speakable-answer" style="margin:0">{p['answer']}</p>
      </div>
    </div>
  </section>

  <section class="section bg-alt">
    <div class="container">
      <div class="grid-2" style="align-items:start;gap:48px">
        <article class="prose">
          <span class="label">Why this page exists</span>
          <h2>{p['service_type']} problems we see around {p['city']}</h2>
          {p['local_context']}
        </article>
        <div class="card">
          <span class="label">Call when you notice</span>
          <h3 style="margin:7px 0 12px">Common warning signs</h3>
          <ul class="check-list">{list_html(p['symptoms'])}</ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="grid-2" style="align-items:start;gap:48px">
        <div>
          <span class="label">How we diagnose it</span>
          <h2>We identify the failure before selling the repair.</h2>
          <div class="divider"></div>
          <ul class="check-list">{list_html(p['checks'])}</ul>
        </div>
        <div>
          <span class="label">What changes the price</span>
          <h2>Why two similar calls can price differently</h2>
          <div class="divider"></div>
          <ul class="check-list">{list_html(p['price_drivers'])}</ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section bg-alt" id="pricing">
    <div class="container">
      <span class="label">Transparent dispatch pricing</span>
      <h2>Know the service-call charge before you book.</h2>
      <p class="lead">The dispatch / diagnostic schedule is posted here so you are not guessing before the technician arrives.</p>
      {SERVICE_CALL_HTML}
      {price_block}
      <div style="margin-top:20px"><a href="/pricing/" class="btn btn-blue">Open the Plumbing Price Estimator →</a></div>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:880px">
      <span class="label">FAQ — {p['city']}</span>
      <h2 style="margin-bottom:28px">Questions homeowners ask before booking</h2>
      {build.faq_html(p['faqs'])}
    </div>
  </section>

  <section class="section bg-alt" id="related-resources">
    <div class="container">
      <span class="label">Keep going</span>
      <h2>Service, local coverage, pricing and homeowner guidance</h2>
      <div class="grid-4" style="margin-top:24px">{related_cards(p['related'])}</div>
    </div>
  </section>

  <section style="background:linear-gradient(135deg,var(--blue-dk),var(--blue));padding:64px 0">
    <div class="container" style="text-align:center;max-width:760px">
      <h2 style="color:white;margin-bottom:10px">Need {p['service_type'].lower()} help in {p['city']}?</h2>
      <p style="color:rgba(255,255,255,.9);margin-bottom:24px">Call Plumbing Paramedic 911. We will tell you the service-call charge up front, diagnose the actual problem, and price the repair before proceeding.</p>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
        <a href="tel:+18644468911" class="btn btn-outline-white btn-xl speakable-phone">📞 (864) 446-8911</a>
        <a href="/contact/" class="btn btn-outline-white">Request Service Online</a>
      </div>
    </div>
  </section>
</main>
"""
    return head + nav + body + build.FOOTER_HTML + "</body>\n</html>\n"


def write_pages(build) -> None:
    for slug, page in MONEY_PAGES.items():
        target = ROOT / slug / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(build, slug, page), encoding="utf-8")
        print(f"wrote {slug}/index.html")


def money_link_section(slugs: list[str]) -> str:
    cards = []
    for slug in slugs:
        p = MONEY_PAGES[slug]
        cards.append(
            f'<a class="nav-card" href="/{slug}/"><h3>{p["h1"]}</h3>'
            f'<p>{p["description"]}</p><span class="arrow">Local service page →</span></a>'
        )
    return f"""\
<section id="local-service-focus" class="section bg-alt">
  <div class="container">
    <span class="label">Local service focus</span>
    <h2>High-intent help for this service and market</h2>
    <div class="grid-2" style="margin-top:24px">{''.join(cards)}</div>
  </div>
</section>
"""


def inject_links() -> None:
    for rel_path, slugs in LINK_TARGETS.items():
        file = ROOT / rel_path
        if not file.exists():
            raise RuntimeError(f"Missing internal-link target: {rel_path}")
        text = file.read_text(encoding="utf-8")
        if 'id="local-service-focus"' in text:
            continue
        if "</main>" not in text:
            raise RuntimeError(f"Could not find </main> in {rel_path}")
        text = text.replace("</main>", money_link_section(slugs) + "\n</main>", 1)
        file.write_text(text, encoding="utf-8")


def update_sitemap() -> None:
    file = ROOT / "sitemap.xml"
    text = file.read_text(encoding="utf-8")
    for slug in MONEY_PAGES:
        url = f"{BASE_URL}/{slug}/"
        if url not in text:
            text = text.replace(
                "</urlset>",
                f"  <url><loc>{url}</loc><lastmod>{LASTMOD}</lastmod></url>\n</urlset>",
            )
    file.write_text(text, encoding="utf-8")


def update_llms() -> None:
    file = ROOT / "llms.txt"
    text = file.read_text(encoding="utf-8")
    marker = "## High-Intent Local Service Pages"
    if marker in text:
        return
    lines = ["", marker]
    for slug, p in MONEY_PAGES.items():
        lines.append(f'- [{p["h1"]}]({BASE_URL}/{slug}/): {p["description"]}')
    text = text.rstrip() + "\n" + "\n".join(lines) + "\n"
    file.write_text(text, encoding="utf-8")


def refresh_pricing_disclosures() -> None:
    """Bring service-call wording on the generated pricing page in line with current policy."""
    file = ROOT / "pricing" / "index.html"
    text = file.read_text(encoding="utf-8")
    text = text.replace(
        "We do not charge a separate diagnostic fee on top of the repair price. The service call fee is waived when you proceed with the repair. We'll always tell you upfront what the full cost will be.",
        "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. Repair or installation work is priced separately and approved before we proceed.",
    )
    text = text.replace(
        "The $150 after-hours surcharge applies to jobs scheduled outside of regular business hours (Mon–Fri 8 AM–6 PM), including evenings, weekends, and holidays. It covers dispatching outside normal hours. There are no additional fees beyond what you're quoted.",
        "After-hours and weekend service / diagnostic calls are $99. After-midnight and holiday service / diagnostic calls are $158. Any repair or installation work is quoted separately before it begins.",
    )
    panel = f"""\
<div id="current-service-call-pricing" style="background:var(--blue-xlt);border:1.5px solid #90CAF9;border-radius:var(--r2);padding:24px;margin-bottom:28px">
  <span class="label">Current service / diagnostic call</span>
  <h3 style="margin:6px 0 10px">$79 weekday · $99 after-hours/weekend · $158 after midnight/holiday</h3>
  <p style="margin:0;color:var(--ink2)">Repair and installation prices are quoted separately. The estimator below is for planning; access, equipment, materials, code-required upgrades and hidden conditions can change the final written quote.</p>
</div>
"""
    if 'id="current-service-call-pricing"' not in text:
        text = text.replace('<div class="calc-wrapper">', panel + '\n<div class="calc-wrapper">', 1)
    file.write_text(text, encoding="utf-8")


def generate(build) -> None:
    write_pages(build)
    inject_links()
    update_sitemap()
    update_llms()
    refresh_pricing_disclosures()
