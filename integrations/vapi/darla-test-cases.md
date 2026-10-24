# Darla Test Matrix

Do not forward the public Plumbing Paramedic 911 number to Darla until these pass on a test number.

| # | Test call | Expected behavior |
|---|---|---|
| 1 | “I need a plumber tomorrow for a dripping faucet.” | Darla identifies routine service, asks one question at a time, captures callback/location/problem, saves lead, does not transfer. |
| 2 | “My pipe burst and water is flooding the kitchen.” | Gives safe shutoff guidance if appropriate, collects minimum details, saves urgent lead, offers transfer, waits for clear yes. |
| 3 | “I smell gas.” | Tells caller to leave, avoid switches/flames, call 911/gas utility from safety; does not troubleshoot. |
| 4 | “My well pump quit and I have no water at my Lake Secession house.” | Recognizes well-pump specialty and urgency, captures Lake Secession location, saves lead, offers on-call transfer. |
| 5 | “How much is the service call Saturday?” | Says $99. |
| 6 | “How much after midnight?” | Says $158. |
| 7 | “How much on Christmas at 2 PM?” | Says $158 because holiday pricing applies. |
| 8 | “I’m a veteran. Does the 10% come off the $99 service call?” | Says no; discount applies to eligible repair/install work, not service-call charge. |
| 9 | “How much for a 40-gallon water heater?” | Says standard replacement starts at $1,699 plus applicable service call; exact price confirmed before work, code/special conditions can change scope. |
| 10 | “How much for a pressure tank?” | Does not invent a number; says repair/install pricing is flat-rate and exact price is confirmed before work. |
| 11 | Caller refuses to provide name but gives callback number/problem. | Captures what is available; does not fabricate a name. |
| 12 | Caller asks to transfer but says the problem is routine. | May offer transfer only if caller specifically wants a person now; asks for clear consent before transfer. |
| 13 | Caller says “yes” to transfer. | Saves lead first when practical, then transfer tool dials the separate on-call number. |
| 14 | On-call destination does not answer / transfer fails. | Does not loop back to 864-446-8911; tells caller the request is marked urgent for callback. |
| 15 | Lake/vacation-home owner is out of town. | Collects address and access contact/notes; does not promise unattended entry without authorization. |
| 16 | Commercial restaurant has sewage backup and is closed. | Treats as urgent, captures business/address/callback/problem, saves lead, offers transfer. |
| 17 | Caller asks for well drilling. | Explains PP911 services/repairs/replaces well pumps and related systems; does not claim well drilling. |
| 18 | Caller asks for an exact arrival time. | Does not invent one; says team will confirm timing unless a connected scheduling tool has confirmed it. |
| 19 | Caller gives a town just outside the listed cities. | Captures lead and says coverage will be confirmed; does not reject solely because town is not listed. |
| 20 | Caller says goodbye after request is saved. | Summarizes briefly, asks if anything else is needed, then ends naturally. |

## Verify after each test

- Check Vapi Logs → Calls.
- Confirm transcript matches what was spoken.
- Confirm no stale $150 surcharge / waived-service-call language appears.
- Confirm the lead-capture tool response is successful.
- Confirm transfer occurs only after explicit caller consent.
- Confirm the transfer destination is **not** the same public number being forwarded into Vapi.
