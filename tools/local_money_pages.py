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
}

LINK_TARGETS = {
    "services/well-pump-repair/index.html": ["well-pump-repair-mccormick-sc", "well-pump-repair-iva-lake-secession-sc"],
    "services/drain-cleaning/index.html": ["drain-cleaning-greenwood-sc"],
    "services/water-heater-repair-replacement/index.html": ["water-heater-repair-greenwood-sc", "water-heater-repair-anderson-sc"],
    "services/24-7-emergency-plumbing/index.html": ["emergency-plumber-abbeville-sc"],
    "service-areas/mccormick-sc/index.html": ["well-pump-repair-mccormick-sc"],
    "service-areas/iva-lake-secession-sc/index.html": ["well-pump-repair-iva-lake-secession-sc"],
    "service-areas/greenwood-sc/index.html": ["drain-cleaning-greenwood-sc", "water-heater-repair-greenwood-sc"],
    "service-areas/anderson-sc/index.html": ["water-heater-repair-anderson-sc"],
    "service-areas/abbeville-sc/index.html": ["emergency-plumber-abbeville-sc"],
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
        },
        build.breadcrumb_ld(breadcrumb_items),
        build.faq_ld(p["faqs"]),
    ]
    head = build.head(
        p["title"], p["description"], path, og_image=p["og"], extra_jsonld=extra,
        body_page=f"local-service-{slug}",
    )
    nav = build.nav("services")
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
