#!/usr/bin/env python3
"""Patch generator output with current Plumbing Paramedic 911 pricing policy.

The legacy calculator still contained an old $150 after-hours adjustment,
waived-service-call wording, and fixed $50 discount copy. Keep the calculator's
repair ranges as planning estimates, while publishing the current service-call
schedule separately and preventing stale policy claims from reaching search or
AI answer engines.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_SERVICE_ANSWER = (
    "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, "
    "and $158 after midnight or on holidays. Repair or installation work is priced separately and "
    "approved before we proceed."
)
CURRENT_AFTER_HOURS_ANSWER = (
    "After-hours and weekend service / diagnostic calls are $99. After-midnight and holiday service / "
    "diagnostic calls are $158. Repair or installation work is quoted separately before it begins."
)


def patch_pricing() -> None:
    file = ROOT / "pricing" / "index.html"
    text = file.read_text(encoding="utf-8")

    # Both JSON-LD and visible FAQ variants from the legacy generator.
    stale_service_answers = [
        "We do not charge a separate diagnostic fee on top of the repair price. The service call fee is waived when you proceed with the repair. We'll always tell you upfront what the full cost will be.",
    ]
    stale_after_answers = [
        "The $150 after-hours surcharge applies to jobs scheduled outside of regular business hours (Mon–Fri 8 AM–6 PM), including evenings, weekends, and holidays. It covers dispatching outside normal hours. There are no additional fees beyond what you're quoted.",
        "The $150 after-hours surcharge applies to jobs scheduled outside of regular business hours (Mon–Fri 8 AM–6 PM), including evenings, weekends, and holidays. It covers dispatching our team outside normal hours. There are no additional fees beyond what you're quoted.",
    ]
    for old in stale_service_answers:
        text = text.replace(old, CURRENT_SERVICE_ANSWER)
    for old in stale_after_answers:
        text = text.replace(old, CURRENT_AFTER_HOURS_ANSWER)

    text = text.replace(
        "What does the after-hours surcharge cover?",
        "What is the after-hours service-call charge?",
    )

    # The current service call is separate from the repair estimator. Do not
    # silently add the obsolete $150 surcharge to repair-range calculations.
    text = text.replace(
        "<button class=\"timing-btn active\" onclick=\"selectTiming(this,'business',0)\"><strong>Business Hours</strong><span>Mon–Fri 8 AM–6 PM</span></button>",
        "<button class=\"timing-btn active\" onclick=\"selectTiming(this,'business',0)\"><strong>Weekday</strong><span>Mon–Fri 9 AM–5 PM · $79 service call</span></button>",
    )
    text = text.replace(
        "<button class=\"timing-btn\" onclick=\"selectTiming(this,'after',150)\"><strong>After Hours / Emergency</strong><span>Evenings, Weekends, Holidays</span></button>",
        "<button class=\"timing-btn\" onclick=\"selectTiming(this,'after',0)\"><strong>After Hours / Weekend</strong><span>$99 service call · $158 after midnight/holiday</span></button>",
    )
    text = text.replace("<span>After-hours surcharge</span>", "<span>Repair timing adjustment</span>")
    text = text.replace(
        "* Estimate based on typical job conditions in the Abbeville, SC area. Final price confirmed before any work begins. Prices may vary for complex jobs, hard-to-reach areas, or special materials. Call for a free phone estimate on larger projects.",
        "* Repair estimate based on typical job conditions in the Abbeville, SC area. The service / diagnostic call is separate and shown above. Final repair price is confirmed before work begins; access, code requirements, equipment and special materials can change the written quote.",
    )

    # Current discount policy is percentage-based, not the old fixed $50 UI.
    text = re.sub(
        r"onclick=\"selectOption\(this,'discount','(military|senior|first-responder)',-50\)\"",
        lambda m: f"onclick=\"selectOption(this,'discount','{m.group(1)}',0)\"",
        text,
    )
    text = text.replace(
        '<div class="option-radio-price" style="color:var(--red)">−$50</div>',
        '<div class="option-radio-price" style="color:var(--green)">10% on written quote</div>',
    )

    file.write_text(text, encoding="utf-8")


def patch_faq() -> None:
    file = ROOT / "faq" / "index.html"
    text = file.read_text(encoding="utf-8")
    text = text.replace(
        "Plumbing Paramedic 911 gives free up-front estimates before any work begins. Standard service visits are quoted at flat-rate prices; emergency dispatch fees apply for after-hours calls. Call (864) 446-8911 for a no-obligation quote.",
        "The service / diagnostic call is $79 Monday–Friday 9 AM–5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. Repair work is priced separately and approved before it begins. Call (864) 446-8911 for the current dispatch availability.",
    )
    text = text.replace(
        "Yes. We offer $50 off for active-duty military, honorably discharged veterans, seniors aged 65+, and active police, fire, or EMS personnel. Mention the discount when scheduling.",
        "Yes. We offer a 10% discount where applicable for military, veterans, seniors, and first responders. Discounts do not stack; mention eligibility when scheduling so it can be reflected on the written quote.",
    )
    file.write_text(text, encoding="utf-8")


def apply() -> None:
    patch_pricing()
    patch_faq()
