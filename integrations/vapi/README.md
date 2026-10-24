# Darla Vapi Receptionist

This folder contains the production-ready **configuration-as-code** for Darla, Plumbing Paramedic 911's automated phone receptionist.

## What this migration fixes

The old `8911` prototype is a legacy reference only. It contains stale pricing and a dangerous emergency instruction that could send a forwarded caller back to the same public number.

This version uses current business rules:

- $79 regular service/diagnostic call — Mon–Fri, 9 AM–5 PM
- $99 after-hours and weekends
- $158 after midnight
- $158 holidays
- 10% military/veteran, senior, and first-responder discount on eligible repair/install work only
- service-call charge is not discounted
- standard 40-gallon tank water-heater replacement starts at $1,699
- well-pump service is a priority specialty
- Iva / Lake Secession, McCormick, and Savannah Lakes Village are priority lake/rural markets

## What Darla does

Darla:

1. identifies herself as automated
2. discloses that the call may be recorded
3. triages hazards before ordinary intake
4. asks one question at a time
5. collects name, callback number, service location, and problem
6. saves the request to the same existing PP911 lead endpoint used by the live website
7. offers an urgent transfer to a **separate on-call number**
8. avoids circular transfers back into the public business line
9. records/logs/transcribes calls through Vapi artifacts
10. never invents repair prices or arrival times

## Create Darla in Vapi

Requires Node.js 22+.

Set these environment variables locally. Do **not** commit the values:

```bash
export VAPI_API_KEY="your-private-vapi-key"
export ON_CALL_TRANSFER_NUMBER="+1XXXXXXXXXX"
```

The on-call number must be a separate destination that rings Eric/on-call personnel directly. It must **not** be the public `864-446-8911` number if that public number forwards to Vapi.

Optional:

```bash
export VAPI_MODEL="gpt-6-luna"
export PP911_LEAD_ENDPOINT="https://wuwgvtjktppjueiykcww.supabase.co/functions/v1/website-lead-capture"
```

Then run:

```bash
node integrations/vapi/create-darla-assistant.mjs
```

The script prints the new Vapi Assistant ID.

## Phone-number rollout

Do not send live customers to Darla first.

1. Assign Darla to a Vapi or imported Twilio **test number**.
2. Run every scenario in `darla-test-cases.md`.
3. Confirm the lead appears in the existing PP911 intake pipeline.
4. Confirm the transfer destination rings and does not loop.
5. Review Vapi call logs/transcripts/recordings.
6. Only then configure the public `864-446-8911` number to route to Darla for the desired hours.

Vapi supports inbound assistants on Vapi numbers and imported provider numbers. The transfer destination should be an E.164 phone number.

## Production routing recommendation

Start with **after-hours / missed-call coverage**, not 24/7 takeover.

That lets Eric continue answering normal daytime calls while Darla protects evenings, weekends, after-midnight calls, and overflow. Once call logs look good, routing can be expanded.

## Urgent-text fallback

This first production-safe version guarantees that the urgent lead is saved before transfer when practical. It does **not** enable an unrestricted SMS tool in the assistant because that could allow model-selected destinations.

The next telephony step is to add a server-controlled owner alert (Twilio or another fixed-destination webhook) so a failed transfer can text the on-call phone without exposing arbitrary SMS routing to the model.

## Files

- `darla-system-prompt.md` — current receptionist behavior and business rules
- `create-darla-assistant.mjs` — creates the Vapi assistant and tools
- `darla-test-cases.md` — required test matrix before public routing
